from libs.io import read_file

TARGET = 1
CIPHER_FILE = f"./files/cipher{TARGET}.txt"

def frequency_analyze(texts: list[str], only_alpha = False): # cnt_table: {ord: cnt}  ordered_list: {ord, cnt, freq}
    table = {}
    N = 0

    for text in texts:
        for t in text:
            if only_alpha and ord(t) not in range(65, 91) and ord(t) not in range(97, 123):
                continue
            
            N += 1
            if ord(t) not in table.keys():
                table[ord(t)] = 1
            else:
                table[ord(t)] += 1

    arr = [[o, c, c/N] for o, c in table.items()]
    arr = sorted(arr, key=lambda x: x[1], reverse=True)

    return table, arr

def index_of_coincidence(cnt_table: dict, only_alpha=False):
    N = 0
    for k, v in cnt_table.items():
        if only_alpha and k not in range(65, 91) and k not in range(97, 123):
            continue
        N += v

    if N <= 1:
        return 0.0

    ic = 0.0
    if only_alpha:
        for alpha in range(26):
            n = 0
            if 65+alpha in cnt_table.keys(): 
                n += cnt_table[65+alpha]
            if 97+alpha in cnt_table.keys(): 
                n += cnt_table[97+alpha]
            if n > 1:
                ic += n*(n-1)
    else:
        for v in cnt_table.values():
            ic += v*(v-1)
    
    return ic / (N * (N-1))

cipher = read_file(CIPHER_FILE)
table, ordered_list = frequency_analyze(cipher, only_alpha=True)
ic = index_of_coincidence(table, only_alpha=True)

print(f"Index Of Coincidence: {ic:.6}")
for idx, i in enumerate(ordered_list):
    print(f"{chr(i[0])}: cnt = {i[1]}  freq = {round(i[2]*10000)/100}%")