import matplotlib.pyplot as plt
import os

class Analyzer:
    def __init__(self, src):
        self.src = src

        self.cipher = ""
        self.freq_map = {
            'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.13,
            'F': 0.022, 'G': 0.02, 'H': 0.061, 'I': 0.07, 'J': 0.0015,
            'K': 0.0077, 'L': 0.04, 'M': 0.024, 'N': 0.067, 'O': 0.075,
            'P': 0.019, 'Q': 0.00095, 'R': 0.06, 'S': 0.063, 'T': 0.091,
            'U': 0.028, 'V': 0.0098, 'W': 0.024, 'X': 0.0015, 'Y': 0.02,
            'Z': 0.00074
        }

    #region
    def isAlpha(self, char: str):
        if (len(char) != 1): 
            return -1
        return (ord(char) in range(65, 91)) or (ord(char) in range(97, 123))
    
    def load(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cipher_dir = os.path.join(script_dir, self.src)
        with open(cipher_dir, "r", encoding="utf-8") as r:
            self.cipher = "".join(["".join(s.split()) for s in r.readlines()])

    def count(self, cipher = None):
        if cipher == None:
            cipher = self.cipher
        
        N = 0
        cnt_table = {}

        for i in range(26):
            cnt_table[chr(ord("A")+i)] = 0

        for t in cipher:
            if not self.isAlpha(t):
                continue
            
            N += 1
            cnt_table[t.upper()] += 1
        
        freq_table = {
            k: v/N
            for k, v in cnt_table.items()
        }

        return N, cnt_table, freq_table

    def group(self, n):
        result: list[str] = ["" for i in range(n)]

        for i, t in enumerate(self.cipher):
            result[i%n] += t
        
        return result

    def caesar_decrypt(self, text: str, key: int):
        processed = ""
        for t in text:
            if self.isAlpha(t):
                processed += chr(ord("A") + (ord(t) - ord("A") - key) % 26)
            else:
                processed += t
            
        return processed

    def vigenere_decrypt(self, text: str, key: str):
        processed = ""
        for i, t in enumerate(text):
            idx = i if i < len(key) else i % len(key)
            shift = ord(key[idx].lower()) - ord("a")

            if self.isAlpha(t):
                processed += chr(ord("A") + (ord(t) - ord("A") - shift) % 26)
            else:
                processed += t
            
        return processed

    #endregion

    #region
    def index_of_coincidence(self, N, cnt_table):
        ic = 0.0
        for alpha in range(26):
            n = cnt_table[chr(ord("A") + alpha)]
            ic += n*(n-1)
        
        return ic/(N*(N-1))
    
    def chi_square(self, freq_table, k):
        chisq = 0.0

        for c in freq_table.keys():
            observed = freq_table[chr((ord(c)+k-ord("A"))%26 + ord("A"))]
            expected = self.freq_map[c]
            chisq += (observed - expected)**2 / expected
        
        return chisq
    #endregion

    def caesar_crack(self):
        N, cnt_table, freq_table = self.count()

        print("=====performing caesar crack=====\n")

        res:tuple[int, float] = [0, 114514.0]
        for k in range(1, 26):
            chisq = self.chi_square(freq_table, k)
            
            if chisq < res[1]:
                res[0], res[1] = k, chisq

            print(f"key = {k}  chi-square = {chisq}")
            
        print(f"Found key: {res[0]} with the lowest chi-square: {res[1]:.6}")
        
        ans = self.caesar_decrypt(self.cipher, res[0])
        print(f"Decrypted text: {ans[:20]}...")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        answer_dir = os.path.join(script_dir, "answer.txt")
        with open(answer_dir, "w", encoding="utf-8") as w:
            w.writelines(ans)

        print(f"Decrypted file saved as {answer_dir}")

    def vigener_crack(self):
        MAX_KEY_LEN = 8

        print("=====performing vigener crack=====\n")

        key_res:tuple[int, float, float] = [0, 114514.0, 1919810.0]
        for key_length in range(2, MAX_KEY_LEN):
            avg_ic = 0.0
            grouped = self.group(key_length)
            
            for substr in grouped:
                N, cnt_table, freq_table = self.count(cipher=substr)
                ic = self.index_of_coincidence(N, cnt_table)
                avg_ic += ic
            
            avg_ic /= key_length

            diff = abs(avg_ic - 0.068)/ 0.068

            if diff < key_res[2]:
                key_res[0], key_res[1], key_res[2] = key_length, avg_ic, diff

            print(f"Tried key length = {key_length} avg ic = {avg_ic:.6} diff = {diff:.6}")

        print(f"Found key length {key_res[0]} with the closest avg ic {key_res[1]}\n")

        founded_key = ""

        grouped = self.group(key_res[0])
        for substr in grouped:
            N, cnt_table, freq_table = self.count(cipher=substr)

            print(f"cracking substr '{substr[:10]}...'")

            res:tuple[int, float] = [0, 114514.0]
            for k in range(26):
                chisq = self.chi_square(freq_table, k)
                
                if chisq < res[1]:
                    res[0], res[1] = k, chisq
            
            founded_key += chr(ord("A") + res[0])
            print(f"Found partial key: {chr(ord("A") + res[0])} with the lowest chi-square: {res[1]:.6}\n")
            
        print(f"Found Key: {founded_key}")
            
        ans = self.vigenere_decrypt(self.cipher, founded_key)
        print(f"Decrypted text: {ans[:20]}...")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        answer_dir = os.path.join(script_dir, "answer.txt")
        with open(answer_dir, "w", encoding="utf-8") as w:
            w.writelines(ans)

        print(f"Decrypted file saved as {answer_dir}")

    def analyze(self):
        N, cnt_table, freq_table = self.count()

        arr = sorted([[k, freq_table[k]] for k in cnt_table.keys()], key = lambda x: x[1], reverse=True)
        ic = self.index_of_coincidence(N, cnt_table)

        print("=====frequency of alphabets in descending order=====\n")
        print(f"Index of Coincidence: {ic:.6}\n")
        for i, t in enumerate(arr):
            print(f"[{i+1}] {t[0]} : {t[1]}")

        labels = [chr(ord("A") + i) for i in range(26)]
        frequencies = [freq_table[k] for k in labels]

        plt.bar(labels, frequencies, color='skyblue')
        plt.xlabel('Alphabets')
        plt.ylabel('Frequency')
        plt.title('Frequency of Alphabets')

        script_dir = os.path.dirname(os.path.abspath(__file__))
        chart_dir = os.path.join(script_dir, "freqency_chart.png")
        plt.savefig(chart_dir)
        print(f"Chart saved as {chart_dir}\n")
        
if __name__ == "__main__":
    analyzer = Analyzer("problem3Ciphertext.txt")

    analyzer.load()
    analyzer.analyze()
    analyzer.vigener_crack()
    