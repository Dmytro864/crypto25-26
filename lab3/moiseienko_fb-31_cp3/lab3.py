from collections import Counter

Alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
Letter_to_id = {char: i for i, char in enumerate(Alphabet)}
id_to_Letter = {i: char for i, char in enumerate(Alphabet)}

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, n):
    gcd, x, _ = extended_gcd(a, n)
    if gcd != 1:
        return None
    return x % n

def solve_linear_congruence(a, b, n):
    a %= n
    b %= n
    gcd, x0, _ = extended_gcd(a, n)

    if b % gcd != 0:
        return []

    n1 = n // gcd
    a1 = a // gcd
    b1 = b // gcd

    initial_x = (mod_inverse(a1, n1) * b1) % n1

    results = [(initial_x + i * n1) % n for i in range(gcd)]
    return results

Alphabet_size = 31
Modulo = Alphabet_size ** 2

def get_bigram_frequencies(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip().replace('\n', '').replace(' ', '')

    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 2)]

    return Counter(bigrams).most_common(5)

top_5_cipher = get_bigram_frequencies('04.txt')

def decrypt_affine(ciphertext, a, b):
    m_sq = 31**2
    a_inv = mod_inverse(a, m_sq)
    if a_inv is None:
        return None

    plaintext = []
    for i in range(0, len(ciphertext) - 1, 2):
        y = Letter_to_id[ciphertext[i]] * 31 + Letter_to_id[ciphertext[i+1]]
        x = (a_inv * (y - b)) % m_sq
        plaintext.append(id_to_Letter[x // 31])
        plaintext.append(id_to_Letter[x % 31])
    return "".join(plaintext)

def is_meaningful(text):
    forbidden = ['ьь', 'ьы', 'ыь', 'ыы', 'йь', 'йй', 'чщ', 'чя', 'щя']
    for f in forbidden:
        if f in text:
            return False

    counts = Counter(text)
    total = len(text)
    if (counts.get('о', 0) / total) < 0.05:
        return False

    return True

lang_top_bg = ['ст', 'но', 'то', 'на', 'ен']
cipher_top_bg = [bg for bg, count in top_5_cipher]

x_values = [Letter_to_id[bg[0]] * 31 + Letter_to_id[bg[1]] for bg in lang_top_bg]
y_values = [Letter_to_id[bg[0]] * 31 + Letter_to_id[bg[1]] for bg in cipher_top_bg]

with open('04.txt', 'r', encoding='utf-8') as f:
    full_ciphertext = f.read().strip().replace('\n', '').replace(' ', '')

print("\nПеребір ключів...")

found_keys = set()
for x1 in x_values:
    for x2 in x_values:
        if x1 == x2: continue
        for y1 in y_values:
            for y1 in y_values:
                for y2 in y_values:
                    if y1 == y2: continue

                    a_candidates = solve_linear_congruence(x1 - x2, y1 - y2, 961)

                    for a in a_candidates:
                        if a % 31 == 0: continue

                        b = (y1 - a * x1) % 961

                        if (a, b) not in found_keys:
                            found_keys.add((a, b))

                            sample = decrypt_affine(full_ciphertext[:100], a, b)
                            if sample and is_meaningful(sample):
                                print(f"\nЗнайдений потенційний ключ: a={a}, b={b}")
                                print(f"Текст: {sample[:70]}...")

                                final_text = decrypt_affine(full_ciphertext, a, b)
                                with open('decrypted_04.txt', 'w', encoding='utf-8') as f_out:
                                    f_out.write(final_text)
                                print("Текст у 'decrypted_04.txt'")    

print(" 5 найчастіших біграм шифртексту:")
for bg, count in top_5_cipher:
    val = Letter_to_id[bg[0]] * 31 + Letter_to_id[bg[1]]
    print(f"Біграма: '{bg}' | Кількість: {count} | Числове значення: {val}")
