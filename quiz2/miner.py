import logging
from hashlib import sha256
from dotenv import load_dotenv
import os
from datetime import datetime
import threading
from queue import Queue

logging.addLevelName(logging.ERROR, "EROR")

log_format = '%(asctime)s [%(levelname)s] %(message)s'
date_format = '%Y/%m/%d %H:%M:%S'

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt=date_format
)
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("logger.log")
file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
logger.addHandler(file_handler)

def worker(block_hash: str, start_nonce: int, end_nonce: int, 
               target_prefix: str, result_queue: Queue, stop_event: threading.Event):
    nonce = start_nonce
    while not stop_event.is_set() and nonce <= end_nonce:
        candidate = sha256((block_hash + hex(nonce)[2:]).encode()).hexdigest()
        if candidate.startswith(target_prefix):
            result_queue.put((nonce, candidate))
            stop_event.set()
            return
        nonce += 1
        if nonce % 1000000 == 0:
            #print(f"[Thread {threading.current_thread().name} with nonce {hex(nonce)[2:]}] {candidate[:10]}...")
            pass

def parallel(block_hash: str, target_prefix: str, num_threads: int = 8) -> tuple[int, str]:
    result_queue = Queue()
    stop_event = threading.Event()
    threads = []
    
    nonce_range = 0xffffffff
    chunk_size = nonce_range // num_threads
    
    for i in range(num_threads):
        start_nonce = i * chunk_size
        end_nonce = start_nonce + chunk_size - 1 if i < num_threads - 1 else 0xffffffff
        
        t = threading.Thread(
            target=worker,
            args=(block_hash, start_nonce, end_nonce, target_prefix, result_queue, stop_event),
            name=f"Miner-{i}"
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    if not result_queue.empty():
        return result_queue.get()
    return None, None

if __name__ == "__main__":
    load_dotenv()
    student_id = os.getenv("STUDENT_ID")
    pre_image = sha256(student_id.encode()).hexdigest()
    block_hash = pre_image

    logger.info(f"[PreImage] {block_hash[:10]}...")

    start_digit = 0
    for i in range(len(student_id)):
        if not block_hash.startswith(student_id[:i+1]):
            break
        start_digit = i + 1

    logger.info(f"[Round 1 without nonce] {block_hash[:10]}...")
    round_number = 2

    while start_digit < len(student_id):
        target_prefix = student_id[:start_digit + 1]
        nonce, candidate = parallel(block_hash, target_prefix)
        
        if nonce is not None:
            block_hash = candidate
            if nonce == 0:
                logger.info(f"[Round {round_number} without nonce] {block_hash[:10]}...")
            else:
                logger.info(f"[Round {round_number} with nonce {hex(nonce)[2:]}] {block_hash[:10]}...")
            round_number += 1
            start_digit += 1
        else:
            logger.error(f"[Round {round_number}] not found with running out of nonce")
            break

