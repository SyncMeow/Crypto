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

def vigenere_cipher(text: str, key: str, enc = True):
    """
    encryption: enc = True
    decryption: enc = False
    """
    sgn = 1 if enc else -1

    processed = ""
    for i, t in enumerate(text):
        idx = i if i < len(key) else i % len(key)
        shift = ord(key[idx].lower()) - ord("a")

        if ord("A") <= ord(t) and ord(t) <= ord("Z"):
            processed += chr(ord("A") + (ord(t) - ord("A") + sgn*shift) % 26)
        elif ord("a") <= ord(t) and ord(t) <= ord("z"):
            processed += chr(ord("a") + (ord(t) - ord("a") + sgn*shift) % 26)
        else:
            processed += t
        
    return processed