from libs.numth import mod_inverse
from libs.io import read_file, write_file

PLAIN_FILE = "./files/plain.txt"
CIPHER_FILE = "./files/cipher.txt"
ANSWER_FILE = "./files/answer.txt"

def affine_encrypt(text, a, b):
    """ y = (a*x + b) mod 95 + 32 """
    encrypted = "".join(chr((a*ord(t) + b)%95 + 32) for t in text)
    return encrypted

def positional_xor(text):
    """ z = y ^ (pos(x)**3 mod 31) """
    encrypted = ""

    for i, t in enumerate(text):
        pos = (i + 1) % 31 # 1-base
        encrypted += chr(ord(t) ^ ((pos**3) % 31))

    return encrypted

def affine_decrypt(text, a, b):
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

plain = read_file(PLAIN_FILE)
cipher = positional_xor(affine_encrypt(plain, 28, 93))
write_file(CIPHER_FILE, cipher)
answer = affine_decrypt(positional_xor(cipher), 28, 93)
write_file(ANSWER_FILE, answer)
