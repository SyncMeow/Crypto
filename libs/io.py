def read_file(FILE):
    with open(FILE, "r", encoding="utf-8") as r:
        t = r.readlines()
        return t
        
def write_file(FILE, text):
    with open(FILE, "w", encoding = "utf-8") as w:
        w.writelines(text)
    return