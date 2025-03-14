from libs.io import read_file, write_file
from libs.basic import *

PLAIN_FILE = "./files/plain.txt"
CIPHER_FILE = "./files/cipher.txt"
ANSWER_FILE = "./files/answer.txt"

toggle = 0

if toggle == 0:
    plain = read_file(PLAIN_FILE)
    cipher = caesar_cipher(plain, 11)
    write_file(CIPHER_FILE, cipher)
    answer = caesar_cipher(cipher, -11)
    write_file(ANSWER_FILE, answer)

elif toggle == 1:
    plain = read_file(PLAIN_FILE)
    cipher = vigenere_cipher(plain, "WorldVanquisherIsCool")
    write_file(CIPHER_FILE, cipher)
    answer = vigenere_cipher(cipher, "Crypto", enc=False)
    write_file(ANSWER_FILE, answer)
    

elif toggle == 2:
    plain = read_file(PLAIN_FILE)
    cipher = positional_xor(affine_encrypt(plain, 28, 93))
    write_file(CIPHER_FILE, cipher)
    answer = affine_decrypt(positional_xor(cipher), 28, 93)
    write_file(ANSWER_FILE, answer)
