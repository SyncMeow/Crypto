from libs.io import read_file, write_file
from libs.basic import *

class Crypto:
    def __init__(self):
        pass
        
    def encrypt(self, s: str):
        s = rm_punc(rm_space(s))
        key = ""
        for i in range(5):
            print(f"Round {i+1} key: {key}")

            s = vigenere_cipher(s, key)
            s = transposition_cipher(s, 9, "924637815")
            key = transposition_cipher(key, 9, "491753286")

            print(f"ciphertext: {s}")

        s = permutate(s, 5, 10)
        return s

TARGET = 1

PLAIN_FILE = f"./files/plain{TARGET}.txt"
CIPHER_FILE = f"./files/cipher{TARGET}.txt"
ANSWER_FILE = f"./files/answer{TARGET}.txt"

toggle = 3

if toggle == 0:
    plain = read_file(PLAIN_FILE)
    cipher = [caesar_cipher(t, 11) for t in plain]
    write_file(CIPHER_FILE, cipher)
    print(f"Encrypted {PLAIN_FILE} to {CIPHER_FILE}")

    answer = [caesar_cipher(t, -11) for t in cipher]
    write_file(ANSWER_FILE, answer)
    print(f"Decrypted {CIPHER_FILE} to {ANSWER_FILE}")

elif toggle == 1:
    plain = read_file(PLAIN_FILE)
    cipher = permutate(vigenere_cipher(rm_space("".join(plain)), "CryptographyEngineering"), 5, 10)
    write_file(CIPHER_FILE, cipher)
    print(f"Encrypted {PLAIN_FILE} to {CIPHER_FILE}")

    answer = vigenere_cipher(rm_space(cipher), "CryptographyEngineering", enc=False)
    write_file(ANSWER_FILE, answer)
    print(f"Decrypted {CIPHER_FILE} to {ANSWER_FILE}")

elif toggle == 2:
    plain = read_file(PLAIN_FILE)
    cipher = [positional_xor(affine_encrypt(t, 28, 93)) for t in plain]
    write_file(CIPHER_FILE, cipher)
    print(f"Encrypted {PLAIN_FILE} to {CIPHER_FILE}")

    answer = [affine_decrypt(positional_xor(t), 28, 93) for t in cipher]
    write_file(ANSWER_FILE, answer)
    print(f"Decrypted {CIPHER_FILE} to {ANSWER_FILE}")

elif toggle == 3:
    crypto = Crypto()

    plain = read_file(PLAIN_FILE)
    plain = "".join(plain)
    cipher = crypto.encrypt(plain)
    write_file(CIPHER_FILE, cipher)

    print(f"Encrypted {PLAIN_FILE} to {CIPHER_FILE}")
