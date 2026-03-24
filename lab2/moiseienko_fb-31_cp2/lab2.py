import collections

Alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

Rus_freqs = {
    'а': 0.07998, 'б': 0.01592, 'в': 0.04533, 'г': 0.01687, 'д': 0.02977,
    'е': 0.08483, 'ж': 0.00940, 'з': 0.01641, 'и': 0.07367, 'й': 0.01208,
    'к': 0.03486, 'л': 0.04343, 'м': 0.03203, 'н': 0.06700, 'о': 0.10983,
    'п': 0.02804, 'р': 0.04746, 'с': 0.05473, 'т': 0.06318, 'у': 0.02615,
    'ф': 0.00267, 'х': 0.00966, 'ц': 0.00486, 'ч': 0.01450, 'ш': 0.00718,
    'щ': 0.00361, 'ъ': 0.00037, 'ы': 0.01898, 'ь': 0.01735, 'э': 0.00331,
    'ю': 0.00639, 'я': 0.02013
}

def vigenere_encrypt(text, key):
    res = ""
    for i in range(len(text)):
        p_idx = Alphabet.index(text[i])
        k_idx = Alphabet.index(key[i % len(key)])
        res += Alphabet[(p_idx + k_idx) % 32]
    return res

def vigenere_decrypt(text, key):
    res = ""
    for i in range(len(text)):
        p_idx = Alphabet.index(text[i])
        k_idx = Alphabet.index(key[i % len(key)])
        res += Alphabet[(p_idx - k_idx) % 32]
    return res

def identify_key(text, r):
    key = ""
    for i in range(r):
        block = text[i::r]
        n = len(block)
        counts = collections.Counter(block)

        best_shift = 0
        max_mg = -1.0

        for g in range(32):
            m_g = 0
            for j in range(32):
                char_at_shift = Alphabet[(j + g) % 32]
                observed_freq = counts.get(char_at_shift, 0) / n
                theoretical_freq = Rus_freqs[Alphabet[j]]
                m_g += observed_freq * theoretical_freq
            
            
            if m_g > max_mg:
                max_mg = m_g
                best_shift = g

        key += Alphabet[best_shift]
    return key

def get_clean_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_text = f.read().lower()
    return "".join([c for c in raw_text if c in Alphabet])

def calculate_ic(text):
    n = len(text)
    if n <= 1: return 0

    frequencies = collections.Counter(text)

    numerator = sum(ni * (ni - 1) for ni in frequencies.values())
    denominator = n * (n - 1)

    return numerator / denominator

def analyse_period(text, max_r=30):
    print(f"{'r':>2} | {'Середній ІВ (Mr)':<10}")
    print("-" * 20)

    for r in range(2, max_r + 1):
        ics = []
        for i in range(r):
            block = text[i::r]
            ics.append(calculate_ic(block))

        mr = sum(ics) / len(ics)
        print(f"{r:>2} | {mr:.5f}")

if __name__ == "__main__":
    try:
        cipher_text = get_clean_text('cipher_text_v4.txt')
        print(f"Довжина очищеного тексту: {len(cipher_text)} символів\n")

        test_text = get_clean_text('text_lab2.txt')
        print("Пункт 2: Порівняння ІВ")
        print(f"ІВ відкритого тексту: {calculate_ic(test_text):.5f}")

        test_keys = ["да", "три", "хлеб", "экран", "деньзатмения"]
        for k in test_keys:
            encrypted_test = vigenere_encrypt(test_text, k)
            print(f"r = {len(k):>2} | ІВ: {calculate_ic(encrypted_test):.5f}")
        print("\n")
    except FileNotFoundError:
        print("Попередження: Файл 'text_lab2.txt' не знайдено. \n")

        analyse_period(cipher_text)
    except FileNotFoundError:
        print("Помилка: Текстовий файл 'cipher_text_v4.txt' не знайдено!")

    r_length = 13
    key_found = identify_key(cipher_text, r_length)
    print(f"\nЙмовірний ключ (r={r_length}): {key_found}")

    decrypted_text = vigenere_decrypt(cipher_text, key_found)
    print("\nРозшифрований текст першими 200 символами:")
    print(decrypted_text[:200])

    with open('decrypted_v4.txt', 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    print("\nТекст збережено у файл 'decrypted_v4.txt'")    
