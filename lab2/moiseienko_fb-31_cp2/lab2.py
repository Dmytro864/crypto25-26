import collections
import matplotlib.pyplot as plt

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

def plot_ic_comparison(results_dict):
    rs = list(results_dict.keys())
    ics = list(results_dict.values())

    plt.figure(figsize=(10, 6))
    plt.plot(rs, ics, marker='o', linestyle='-', color='b')
    plt.axhline(y=0.0553, color='r', linestyle='--', label='Еталон (0.0553)')
    plt.axhline(y=0.0312, color='g', linestyle='--', label='Випадковий (0.0312)')

    plt.title('Залежність ІВ від довжини ключа r')
    plt.xlabel('Довжина ключа (r)')
    plt.ylabel('ІВ')
    plt.xticks(rs)
    plt.grid(True)
    plt.legend()
    plt.savefig('ic_comparison.png')
    print("Графік ic_comparison.")
    plt.show()

def plot_period_analysis(r_values, ic_values):
     plt.figure(figsize=(12, 6))
     plt.bar(r_values, ic_values, color='skyblue', edgecolor='navy')

     for i, r in enumerate(r_values):
         if r in [13, 26]:
             plt.bar(r, ic_values[i], color='salmon', edgecolor='red')

     plt.title('Аналіз періоду для варіанту 4')
     plt.xlabel('r')
     plt.ylabel('Середній ІВ')
     plt.xticks(range(2, 31))
     plt.axhline(y=0.0553, color='r', linestyle='--', alpha=0.5)
     plt.grid(axis='y', linestyle='--', alpha=0.7)
     plt.savefig('period_analysis.png')
     print("Діаграма period_analysis.png.")
     plt.show()

if __name__ == "__main__":
    try:
        cipher_text = get_clean_text('cipher_text_v4.txt')
        print(f"Довжина очищеного тексту: {len(cipher_text)} символів\n")

        test_text = get_clean_text('text_lab2.txt')
        print("Пункт 2: Порівняння ІВ")
        ic_results = {0: calculate_ic(test_text)}
        print(f"r = 0(ВТ) | ІВ: {ic_results[0]:.5f}")
              
        test_keys = ["да", "три", "хлеб", "экран", "деньзатмения"]
        for k in test_keys:
            encrypted_test = vigenere_encrypt(test_text, k)
            val = calculate_ic(encrypted_test)
            ic_results[len(k)] = val
            print(f"r = {len(k):>2} | ІВ: {calculate_ic(encrypted_test):.5f}")
        plot_ic_comparison(ic_results)    
        print("\n")

        r_range = list(range(2, 31))
        ic_list = []
        for r in r_range:
            ics = [calculate_ic(cipher_text[i::r]) for i in range(r)]
            ic_list.append(sum(ics) / len(ics))

        plot_period_analysis(r_range, ic_list)    
            
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

       
