import json

def decrypt(FILE = "./ciphertext.txt", SOLUTION = "./solution.json", guess_idx = 1):
    output_file = f"./answer/answer{guess_idx}.txt"
    output_html = f"./answer/answer{guess_idx}.html"

    with open(SOLUTION, "r", encoding="utf-8") as r:
        table = json.load(r)[f"guess{guess_idx}"]

    with open(FILE, "r", encoding="utf-8") as f:
        with open(output_file, "w", encoding="utf-8") as w, open(output_html, "w", encoding="utf-8") as wh:
            wh.write("<html><body>")
            t = f.read(1)
            while t != "":
                if str(ord(t)) in table.keys():
                    decrypted_char = table[str(ord(t))]
                    w.write(decrypted_char)
                    wh.write(f"<span style='color:black; background-color:green'>{decrypted_char}</span>")
                else:
                    w.write(t)
                    wh.write(f"<span style='color:black; background-color:red'>{t}</span>")
                t = f.read(1)
            wh.write("</body></html>")
