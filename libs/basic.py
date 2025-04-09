from libs.numth import mod_inverse

def affine_encrypt(text: str, a: int, b: int):
    """ y = (a*x + b) mod 95 + 32 """
    encrypted = "".join(chr((a*ord(t) + b)%95 + 32) for t in text)
    return encrypted

def positional_xor(text: str):
    """ z = y ^ (pos(x)**3 mod 31) """
    encrypted = ""

    for i, t in enumerate(text):
        pos = (i + 1) % 31 # 1-base
        encrypted += chr(ord(t) ^ ((pos**3) % 31))

    return encrypted

def affine_decrypt(text: str, a: int, b: int):
    """ 
    x = a^-1 * (y - 32 - b) mod 95 
    x += 95 if x < 32
    """
    decrypted = ""

    a_inv = mod_inverse(a, 95)

    for t in text:
        res = (a_inv * (ord(t) - 32 - b)) % 95
        if res < 32: res += 95
        decrypted += chr(res)
    
    return decrypted

def caesar_cipher(text: str, key: int):
    """
    encryption: key
    decryption: -key
    """
    processed = ""
    for t in text:
        if ord("A") <= ord(t) and ord(t) <= ord("Z"):
            processed += chr(ord("A") + (ord(t) - ord("A") + key) % 26)
        elif ord("a") <= ord(t) and ord(t) <= ord("z"):
            processed += chr(ord("a") + (ord(t) - ord("a") + key) % 26)
        else:
            processed += t
        
    return processed

def vigenere_cipher(text: str, key: str, enc=True):
    """
    encryption: enc = True
    decryption: enc = False
    """
    sgn = 1 if enc else -1
    processed = ""
    key_len = len(key)
    key_index = 0 

    for t in text:
        if ord("A") <= ord(t) <= ord("Z"):
            shift = ord(key[key_index % key_len].lower()) - ord("a")
            processed += chr(ord("A") + (ord(t) - ord("A") + sgn * shift) % 26)
            key_index += 1
        elif ord("a") <= ord(t) <= ord("z"):
            shift = ord(key[key_index % key_len].lower()) - ord("a")
            processed += chr(ord("a") + (ord(t) - ord("a") + sgn * shift) % 26)
            key_index += 1 
        else:
            processed += t 

    return processed

def transposition_cipher(text: str, key_len: int, key: str):
    """
    key_len: n
    key: str of a permutation of 1~n
    """

    def find_index(x):
        for i in range(key_len):
            if (key[i] == f"{x}"):
                return i
        return -1

    order = [find_index(i) for i in range(1, key_len+1)]
    
    res = ""
    group = ["" for i in range(key_len)]

    
    for i, c in enumerate(text):
        group[i%key_len] += c

    for i in order:
        res += group[i]
    
    return res

def xor_str(text: str, num: int):
    return "".join(chr(ord(char) ^ num) for char in text)

def rm_punc(text: str):
    res =""
    for t in text:
        if t not in ",.?!\\/{}[]()-+=<>'*&^%$#@:;\"\'":
            res += t
    return res

def rm_space(text: str):
    return "".join(text.split())

def permutate(text: str, group: int, col: int):
    res = ""

    col_cnt = 0
    for i, c in enumerate(text):
        res += c.upper()
        if (i+1) % group == 0:
            res += " "
            col_cnt += 1
        if (col_cnt+1) % col == 0:
            res += "\n"
            col_cnt = 0
    
    return res