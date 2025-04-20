from libs.io import read_file, write_file, abs_dir
from libs.basic import *
import os

class Crypto:
    def __init__(self):
        pass
        
    def encrypt(self, s: str, key: str):
        s = rm_space(s)
        s = rm_punc(s)

        print("===== Performing Encryption =====\n")
        if not key: key = "AADEADAIAIHAZ"
        for i in range(5):
            print(f"Round {i+1} key: {key}")

            s = vigenere_cipher(s, key)
            s = transposition_cipher(s, 9, "924637815")
            key = transposition_cipher(key, 9, "491753286")

            print(f"ciphertext: {s[:20]}...\n")

        s = formatting(s, 5, 10)
        return s

if __name__ == "__main__":

    target = int(input("target: "))
    PLAIN_FILE = abs_dir(__file__, f"./files/plain{target}.txt")
    CIPHER_FILE = abs_dir(__file__, f"./files/cipher{target}.txt")
    ANSWER_FILE = abs_dir(__file__, f"./files/answer{target}.txt")

    crypto = Crypto()
    print(f"Read plaintext from plain{target}.txt\n")
    plaintext = read_file(PLAIN_FILE)
    ciphertext = crypto.encrypt(plaintext, "AADEADAIAIHAZ")
    