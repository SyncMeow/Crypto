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