CIPHER_FILE = "./files/cipher.txt"

def read_file(FILE):
    with open(FILE, "r", encoding="utf-8") as r:
        t = r.read(1)
        res = t
        
        while t != "":
            t = r.read(1)
            res += t
        
        return res
        
def write_file(FILE, text):
    with open(FILE, "w", encoding = "utf-8") as w:
        for t in text: 
            w.write(t)
    return

def analyze(text, cnt_table: dict, ordered_list: list[tuple[int, int, float]]): # cnt_table: {ord: cnt}  ordered_list: {ord, cnt, freq}
    table = {}
    for t in text:
        if ord(t) not in table.keys():
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

table = {}
ordered_list = []

cipher = read_file(CIPHER_FILE)
analyze(cipher, table, ordered_list)

for idx, i in enumerate(ordered_list):
    print(f"{chr(i[0])}: cnt = {i[1]}  freq = {round(i[2]*10000)/100}%")