import json

def analyze(FILE = "./ciphertext.txt", SOLUTION = "./solution.json", sgl = 0, guess_idx = 1):
    """
    sgl: Space Guess Location
    guess_idx: the index of the current guess

    """
    cipher_word_cnt = [0 for i in range(1024)]
    total_cnt = 0

    with open(FILE, "r", encoding="utf-8") as f:
        t = f.read(1)
        while t != "":
            cipher_word_cnt[ord(t)] += 1
            total_cnt += 1
            t = f.read(1)

    ordered_array: list[tuple[int, int, float]] = []
    for code, cnt in enumerate(cipher_word_cnt):
        if cnt != 0:
            ordered_array.append([code, cnt, 100 * round(cnt / total_cnt, 4)])

    ordered_array = sorted(ordered_array, key=lambda x: x[1], reverse=True)
    freq_str = "eariotnslcudpmhgbfywkvxzjq"

    freq_str = freq_str[:sgl] + " " + freq_str[sgl:]

    with open(SOLUTION, "r", encoding="utf-8") as r:
        data = json.load(r)

    new_guess = {}
    for idx, i in enumerate(ordered_array):
        if idx < len(freq_str):
            new_guess[i[0]] = freq_str[idx]
            print(f"{i[0]}: cnt={i[1]}  freq={i[2]}  guess={freq_str[idx]}")
        else:
            print(f"{i[0]}: cnt={i[1]}  freq={i[2]}  guess=None")
            pass

    data[f"guess{guess_idx}"] = new_guess

    with open(SOLUTION, "w", encoding="utf-8") as w:
        json.dump(data, w)

    #print(f"New Guess<{guess_idx}> is Completely Written")
