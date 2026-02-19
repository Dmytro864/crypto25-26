import re
import math
from collections import Counter

def clean_and_prepare_text(input_filename):
    print(f"Обробка файлу: {input_filename}")

    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            content = file.read().lower()
    except FileNotFoundError:
        print(f"Помилка: Файл '{input_filename}' немає в папці")
        return None, None

    content = content.replace('ë', 'е').replace('ъ', 'ь')
    text_with_spaces = re.sub(r'[^а-я ]', '', content)
    text_with_spaces = re.sub(r'\s+', ' ', text_with_spaces).strip()
    text_no_spaces = text_with_spaces.replace(' ', '')

    with open('with_spaces.txt', 'w', encoding='utf-8') as f:
        f.write(text_with_spaces)

    with open('no_spaces.txt', 'w', encoding='utf-8') as f:
        f.write(text_no_spaces)

    print("Успіх")
    print(f"Створений файл з пробілами: with_spaces.txt (символів: {len(text_with_spaces)})")
    print(f"Створений файл без пробілів: no_spaces.txt (символів: {len(text_no_spaces)})")

    return 'with_spaces.txt', 'no_spaces.txt'

def calculate_h1(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        
    total = len(text)
    if total == 0: return 0

    counts = Counter(text)
    entropy = 0

    print(f"\n--- Результати для {filename} ---")  
    for char in sorted(counts.keys()):
        p_i = counts[char] / total
        entropy -= p_i * math.log2(p_i)
        

    print(f"Ентропія H1: {entropy:.5f} біт/символ")
    return entropy

def calculate_h2(filename, step=1):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, step)]

    total_bigrams = len(bigrams)
    counts = Counter(bigrams)

    entropy = 0
    for bigram in counts:
        p_i = counts[bigram] / total_bigrams
        entropy -= p_i * math.log2(p_i)

    h2 = entropy / 2

    mode = "з перетинами" if step == 1 else "без перетинів"
    print(f"Ентропія H2 ({mode}) для {filename}: {h2:.5f} біт/символ")
    return h2

if __name__ == "__main__":
    file_to_open = 'Брати Карамазови Федір Достоєвський.txt'
    f1, f2 = clean_and_prepare_text(file_to_open)

    if f1 and f2:
        print("\n Розрахунок H1")
        calculate_h1(f1)
        calculate_h1(f2)

        print("\n Розрахунок H2 (з перетинами)")
        calculate_h2(f1, step=1)
        calculate_h2(f2, step=1)

        print("\n Розрахунок H2 (без перетинів)")
        calculate_h2(f1, step=2)
        calculate_h2(f2, step=2)
        
