import multiprocessing as mp
from hashlib import sha256
import json
import datetime
import time

record = {
    str(i): {
        "hash": "",
        "cur_nonce": -1,
        "time": None,
        "tried_nonce": []
    }
    for i in range(1, 10)
}

date_format = '%Y/%m/%d %H:%M:%S'

def get_utc_timestamp():
    return time.mktime(datetime.datetime.now().timetuple())

def log_message(msg: str, level: str = "INFO", timestamp: str = None):
    if timestamp is None:
        timestamp = datetime.datetime.now().strftime(date_format)
    
    print(f"{timestamp} [{level}] {msg}")
    
    with open("logger.log", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} [{level}] {msg}\n")

def logout():
    with open("history_max.json", "r", encoding="utf-8") as r:
        record = json.load(r)

    block_hash = record["PreImage"]["hash"]
    cur_time = record["PreImage"]["time"]
    timestamp = datetime.datetime.fromtimestamp(cur_time).strftime(date_format)
    log_message(f"[PreImage] {block_hash}", timestamp=timestamp)

    for i in range(1, 10):
        data = record[str(i)]
        if data["time"] is not None:
            timestamp = datetime.datetime.fromtimestamp(data["time"]).strftime(date_format) 
        else:
            continue
        
        if data["cur_nonce"] != -1:
            block_hash = data["hash"]
            log_message(
                f"[Round {i} with nonce {hex(data['cur_nonce'])[2:]}] {block_hash}",
                timestamp=timestamp
            )
        else:
            if i != 9:
                log_message(
                    f"[Round {i} without nonce] {block_hash}",
                    timestamp=timestamp
                )
            else:
                log_message(
                    f"[Round {i}] not found with running out of nonce",
                    level="EROR",
                    timestamp=timestamp
                )

def record_clean(round_number: int):
    record[str(round_number)]["hash"] = ""
    record[str(round_number)]["cur_nonce"] = -1
    record[str(round_number)]["tried_nonce"] = []
    record[str(round_number)]["time"] = None

def worker(args: tuple[str, str, list[int], int, int]) -> tuple[int, str]:
    block_hash, target_prefix, tried, start_nonce, end_nonce = args

    for nonce in range(start_nonce, end_nonce + 1):
        if nonce in tried: continue

        candidate = sha256((block_hash + hex(nonce)[2:]).encode()).hexdigest()
        if candidate.startswith(target_prefix):
            return nonce, candidate
        
        if (nonce+1) % 10000000 == 0:
            # print(f"[{mp.current_process().name} have done with {(100*(nonce - start_nonce)/(end_nonce - start_nonce)):.2f}%]")
            pass

    # print(f"[{mp.current_process().name} have done all the nonces")
    return None, None

def parallel(round_number: int, block_hash: str, target_prefix: str) -> tuple[int, str]:
    num_processes = mp.cpu_count()

    with mp.Pool(processes=num_processes) as p:
        nonce_range = 0xffffffff
        chunk_size = nonce_range // num_processes
        tried = record[str(round_number)]["tried_nonce"]

        args_list = [
            (block_hash, target_prefix, tried, i*chunk_size, (i+1)*chunk_size if i < num_processes - 1 else nonce_range)
            for i in range(num_processes)
        ]

        for res in p.imap_unordered(worker, args_list):
            if res[0] is not None:
                p.terminate()
                p.join()

                record[str(round_number)]["hash"] = res[1]
                record[str(round_number)]["cur_nonce"] = res[0]
                record[str(round_number)]["tried_nonce"].append(res[0])
                record[str(round_number)]["time"] = get_utc_timestamp()
                
                return res
    
    return None, None

logout()

"""
if __name__ == "__main__":
    student_id = "113550023"

    pre_image = sha256(student_id.encode()).hexdigest()
    block_hash = pre_image

    record["PreImage"] = {
        "hash": pre_image,
        "time": get_utc_timestamp()
    }
    # logger.info(f"[PreImage] {block_hash}")
    print(f"[PreImage] {block_hash}")

    start_digit = 0
    for i in range(len(student_id)):
        if not block_hash.startswith(student_id[:i+1]):
            break
        start_digit = i + 1

    round_number = 1

    max_round = 0
    while start_digit < len(student_id):
        target_prefix = student_id[:start_digit + 1]

        nonce, candidate = parallel(round_number, block_hash, target_prefix)
        
        if nonce is not None:
            block_hash = candidate

            # logger.info(f"[Round {round_number} with nonce {hex(nonce)[2:]}] {block_hash}")
            print(f"[Round {round_number} with nonce {hex(nonce)[2:]}] {block_hash}")
            max_round = max(max_round, round_number)

            if round_number >= max_round:
                with open("history_max.json", "w", encoding="utf-8") as w:
                    json.dump(record, w)

            round_number += 1
            start_digit += 1

            check_prefix = student_id[:start_digit + 1] 
            while block_hash.startswith(check_prefix) and start_digit < len(student_id): 
                start_digit += 1
                if start_digit < len(student_id):
                    record_clean(round_number)
                    # logger.info(f"[Round {round_number} without nonce] {block_hash}")
                    print(f"[Round {round_number} without nonce] {block_hash}")
                    round_number += 1
                    check_prefix = student_id[:start_digit + 1]
        else:
            # logger.error(f"[Round {round_number}] not found with running out of nonce")
            print(f"[Round {round_number}] not found with running out of nonce")

            if round_number == 1: 
                break

            print(f"Backtracking to round {round_number-1}")
            round_number -= 1
            start_digit -= 1
            record_clean(round_number)
            
            while round_number > 1 and record[str(round_number-1)]["cur_nonce"] == -1:
                print(f"Backtracking from round {round_number}")
                round_number -= 1
                start_digit -= 1
                record_clean(round_number)

            if round_number == 1: 
                break
    
    logout()"""