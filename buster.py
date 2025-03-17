import requests
from hashlib import sha1
from libs.formatter import output_format1

def load_from(src_type: int, src: str) -> list[str]:
    """
    Load a list of passwords from the specified source
    
    src_type:
    0: online (URL)
    1: files (local file path)
    """
    if src_type == 0:
        response = requests.get(src)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            raise ValueError(f"Failed to fetch data from URL: {src}")
    elif src_type == 1:
        with open(src, "r", encoding = "utf-8") as file:
            return file.read().splitlines()
    else:
        raise ValueError("Invalid source type.")

def sha1_brute_force(sec_list: list[str], target: str, salt: str) -> str:
    for i, sec in enumerate(sec_list):
        if sha1((salt + sec).encode()).hexdigest() == target:
            output_format1(target, sec, i+1)
            return sec

if __name__ == "__main__":
    SRC_URL = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"
    target = [
        ["dfc3e4f0b9b5fb047e9be9fb89016f290d2abb06", "Salt"],
        ["884950a05fe822dddee8030304783e21cdc2b246", "Easy hash"], 
        ["9b467cbabe4b44ce7f34332acc1aa7305d4ac2ba", "Medium hash"], 
        ["9d6b628c1f81b4795c0266c0f12123c1e09a7ad3", "Leet hacker hash"]
    ]
    sec_list = load_from(0, SRC_URL)

    result_list = []
    for i in range(4):
        print(f"Applying brute-force on {target[i][1]}: {target[i][0]}\n")
        result = sha1_brute_force(sec_list, target[i][0], result_list[0] if i == 3 else "")
        result_list.append(result)
        print()
