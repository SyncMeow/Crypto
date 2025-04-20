import hashlib

def derive_keystream(key: str, length: int, salt: bytes = b'') -> bytes:
    shake = hashlib.shake_256()
    shake.update(key.encode("utf-8") + salt)
    return shake.digest(length)

def xor_bytes(data: bytes, keystream: bytes) -> bytes:
    return bytes([b ^ k for b, k in zip(data, keystream)])

def encrypt(plaintext: str, key: str, salt: bytes = b'') -> str:
    plaintext_bytes = plaintext.encode("utf-8")
    keystream = derive_keystream(key, len(plaintext_bytes), salt)
    ciphertext_bytes = xor_bytes(plaintext_bytes, keystream)
    return ciphertext_bytes.hex()

def decrypt(ciphertext_hex: str, key: str, salt: bytes = b'') -> str:
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    keystream = derive_keystream(key, len(ciphertext_bytes), salt)
    plaintext_bytes = xor_bytes(ciphertext_bytes, keystream)
    return plaintext_bytes.decode("utf-8")

if __name__ == "__main__":
    password = "NYCU"
    message = "Bang Dream it's MyGO!!!!!"
    salt = b'1145141919810'

    print("Password:", password)
    print("Salt:", salt)
    print("Origin message:", message)

    keystream = derive_keystream(password, len(message.encode("utf-8")), salt)
    print("Keystream from SHAKE256 (hex):", keystream.hex())

    cipher = encrypt(message, password, salt)
    print("Encrypted (hex):", cipher)

    plain = decrypt(cipher, password, salt)
    print("Decrypted:", plain)