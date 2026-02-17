import re

def clean_and_prepare_text(input_filename):
    print(f"Обробка файлу: {input_filename}")

    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            content = file.read().lower()
    except FileNotFoundError:
        print(f"Помилка: Файл '{input_filename}' немає в папці")
        return

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

clean_and_prepare_text('Брати Карамазови Федір Достоєвський.txt')
