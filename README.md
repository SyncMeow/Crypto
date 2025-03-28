# Crypto

## Overview
Crypto is a set of encryption and decryption utilities that demonstrate different classical ciphers, including Caesar, Vigenère, and custom ciphers based on positional XOR and affine encryption.

## Features
- Caesar cipher  
- Vigenère cipher  
- Affine encryption with optional XOR positional shifts  
- Configurable toggles for selecting different cipher modes  

## Directory Structure
- ./files/plainN.txt – Plaintext files used for input (N represents the file index).  
- ./files/cipherN.txt – Output ciphertext files.  
- ./files/answerN.txt – Decrypted text files.  
- enc.py – Main script to encrypt or decrypt based on the cipher type selected via the toggle variable.  
- libs/ – Support scripts for I/O and various cipher functions.

## Usage
1. Select the desired cipher by setting toggle to 0, 1, or 2 in enc.py:
   - 0: Caesar cipher  
   - 1: Vigenère cipher  
   - 2: Affine cipher with XOR

2. Run the encryption and decryption:
   ▶ On Windows:  
   » Open Terminal in the project directory  
   » python enc.py

3. Inspect the resulting files in the ./files/ directory.

## Example
Toggle 2 uses an affine function followed by an XOR operation. Then it reverses the process to decrypt.

## Contributing
1. Fork the repository.  
2. Create a new branch for your changes.  
3. Submit a pull request with a clear description.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
Open an issue on GitHub for any questions or feedback.