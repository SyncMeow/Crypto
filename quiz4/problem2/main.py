import os
import copy
import random
import statistics
import matplotlib.pyplot as plt

abs_dir = lambda src: os.path.join(os.path.dirname(os.path.abspath(__file__)), src)

cards = [1, 2, 3, 4]

def Naive(cards):
    for i, card in enumerate(cards):
        n = random.randint(0, len(cards) - 1)
        cards[i], cards[n] = cards[n], cards[i]

def Fisher_Yates(cards):
    for i, card in enumerate(cards):
        n = random.randint(0, i)
        cards[i], cards[n] = cards[n], cards[i]  

def enpattern(cards):
    return "".join(str(i) for i in cards)

def draw(pattern_times, title, filename):
    patterns = list(pattern_times.keys())
    frequencies = list(pattern_times.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(patterns, frequencies)
    plt.xticks(rotation=90)
    plt.xlabel("Patterns")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.tight_layout()

    plt.savefig(filename)
    plt.close() 

if __name__ == "__main__":
    num_rounds = 1000000
    pattern_times = {}

    #region Naive
    for i in range(num_rounds):
        cur_cards = copy.deepcopy(cards)
        Naive(cur_cards)
        if enpattern(cur_cards) not in pattern_times.keys():
            pattern_times[enpattern(cur_cards)] = 0
        pattern_times[enpattern(cur_cards)] += 1

    print("Naive algotrithm:")
    for key, value in pattern_times.items():
        output_pattern = " ".join(c for c in key)
        print(f"[{output_pattern}]: {value}")
    
    Naive_stdev = statistics.stdev(pattern_times.values())
    print(f"standard deviation: {Naive_stdev}\n")
    draw(pattern_times, "Naive Algorithm Distribution", abs_dir("naive_distribution.png"))
    #endregion

    #region Fisher-Yates
    pattern_times = {}
    for i in range(num_rounds):
        cur_cards = copy.deepcopy(cards)
        Fisher_Yates(cur_cards)
        if enpattern(cur_cards) not in pattern_times.keys():
            pattern_times[enpattern(cur_cards)] = 0
        pattern_times[enpattern(cur_cards)] += 1

    print("Fisher-Yates algotrithm:")
    for key, value in pattern_times.items():
        output_pattern = " ".join(c for c in key)
        print(f"[{output_pattern}]: {value}")

    Fisher_Yates_stdev = statistics.stdev(pattern_times.values())
    print(f"standard deviation: {Fisher_Yates_stdev}\n")
    draw(pattern_times, "Fisher-Yates Algorithm Distribution", abs_dir("fisher_yates_distribution.png"))
    #endregion 