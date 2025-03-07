import json

def check(a, b, guess_idx = 3): # (ax + b mod 95) + 32
    FILE = "./solution.json"
    isAvaliable = True

    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)[f"guess{guess_idx}"]
        
        for key, value in data.items():
            computed = (a*int(key) + b)%95 + 32
            
            if computed != ord(value):
                print(f"{key} -> {value}: but computed {key} -> {computed} ({chr(computed)})")
                isAvaliable = False
                break
        
    return isAvaliable

def compute(a, b):
    FILE = "./solution.json"
    with open(FILE, "r", encoding="utf-8") as r:
        data = json.load(r)

    with open(FILE, "w") as w:
        tmp = {}
        for i in range(32, 127):
            tmp[i] = chr((a*i+b)%95 + 32)

        data["guess111"] = tmp
        json.dump(data, w)
    