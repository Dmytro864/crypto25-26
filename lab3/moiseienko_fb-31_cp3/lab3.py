import collections

Alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
M = 31
M2 = M * M

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def mod_inverse(a, n):
    d, x, y = extended_gcd(a, n)
    if d != 1:
        return None
    return x % n

def solve_linear_congruence(a, b, n):
    d, x, y = extended_gcd(a, n)
    if b % d != 0:
        return []

    x0 = (x * (b // d)) % (n // d)
    return [(x0 + i * (n // d)) % n for i in range(d)]

def get_bigram_val(bg):
    return Alphabet.index(bg[0]) * M + Alphabet.index(bg[1])

def get_val_bigram(val):
    return Alphabet[val // M] + Alphabet[val % M]

def get_clean_text(file_path):
    with open (file_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()

    text = text.replace('ë', 'е').replace('ъ', 'ь')

    cleaned = "".join([c for c in text if c in Alphabet])
    return cleaned

def count_bigrams(text):
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 2)]
    return collections.Counter(bigrams)

if __name__ == "__main__":
    cipher_text = get_clean_text('04.txt')
    print(f"Довжина очищеного тексту: {len(cipher_text)} символів")

    b_counts = count_bigrams(cipher_text)
    total_bigrams = sum(b_counts.values())

    print("\n --- 5 біграм шифртексту ---")
    most_common = b_counts.most_common(5)
    for bg, count in most_common:
        print(f"Біграма '{bg}': кількість = {count}, частота = {count/total_bigrams:.5f}")
