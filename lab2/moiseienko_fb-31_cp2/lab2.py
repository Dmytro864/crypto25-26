import collections

Alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

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

        analyse_period(cipher_text)
    except FileNotFoundError:
        print("Помилка: Текстовий файл 'cipher_text_v4.txt' не знайдено!")
