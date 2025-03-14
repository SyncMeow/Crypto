from libs.io import read_file, write_file
from libs.basic import *

TARGET = 1

PLAIN_FILE = f"./files/plain{TARGET}.txt"
CIPHER_FILE = f"./files/cipher{TARGET}.txt"
ANSWER_FILE = f"./files/answer{TARGET}.txt"

toggle = 2

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
    cipher = [vigenere_cipher(t, "CryptographyEngineering") for t in plain]
    write_file(CIPHER_FILE, cipher)
    print(f"Encrypted {PLAIN_FILE} to {CIPHER_FILE}")

    answer = [vigenere_cipher(t, "CryptographyEngineering", enc=False) for t in cipher]
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
