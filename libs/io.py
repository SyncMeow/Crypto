import os

def read_file(FILE):
    with open(FILE, "r", encoding="utf-8") as r:
        t = r.readlines()
        return "".join(t)
        
def write_file(FILE, text):
    with open(FILE, "w", encoding = "utf-8") as w:
        w.writelines(text)
    return

abs_dir = lambda loc, src: os.path.join(os.path.dirname(os.path.abspath(loc)), src)