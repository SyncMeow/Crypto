from libs.io import read_file, write_file

CIPHER_FILE = "./files/cipher.txt"

def frequency_analyze(text, cnt_table: dict, ordered_list: list[tuple[int, int, float]], only_alpha = False): # cnt_table: {ord: cnt}  ordered_list: {ord, cnt, freq}
    table = {}
    for t in text:
        if ord(t) not in table.keys():
            if only_alpha and ord(t) not in range(65, 91) and ord(t) not in range(97, 123):
                continue
            table[ord(t)] = 1
        else:
            table[ord(t)] += 1

    arr = [[o, c, c/len(text)] for o, c in table.items()]
    arr = sorted(arr, key=lambda x: x[1], reverse=True)

    cnt_table.clear()
    cnt_table.update(table)

    ordered_list.clear()
    ordered_list.extend(arr)
    return

def index_of_coincidence(text, cnt_table: dict):
    N = len(text)
    if N <= 1:
        return 0.0

    ic = 0.0
    for alpha in range(26):
        n = 0
        if 65+alpha in cnt_table.keys(): 
            n += cnt_table[65+alpha]
        if 97+alpha in cnt_table.keys(): 
            n += cnt_table[97+alpha]
        ic += (n/N)*((n-1)/(N-1))
    
    return ic

table = {}
ordered_list = []

cipher = read_file(CIPHER_FILE)
frequency_analyze(cipher, table, ordered_list, only_alpha=True)
ic = index_of_coincidence(cipher, table)

print(f"Index Of Coincidence: {round(ic*1000000)/1000000}")
for idx, i in enumerate(ordered_list):
    print(f"{chr(i[0])}: cnt = {i[1]}  freq = {round(i[2]*10000)/100}%")