from libs.io import read_file, write_file
from libs.basic import *

PLAIN_FILE = "./files/plain.txt"
CIPHER_FILE = "./files/cipher.txt"
ANSWER_FILE = "./files/answer.txt"

plain = read_file(PLAIN_FILE)
cipher = caesar_cipher(plain, 5)
write_file(CIPHER_FILE, cipher)
answer = caesar_cipher(cipher, -5)
write_file(ANSWER_FILE, answer)

"""
plain = read_file(PLAIN_FILE)
cipher = positional_xor(affine_encrypt(plain, 28, 93))
write_file(CIPHER_FILE, cipher)
answer = affine_decrypt(positional_xor(cipher), 28, 93)
write_file(ANSWER_FILE, answer)
"""