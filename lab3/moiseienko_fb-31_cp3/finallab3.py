import collections

Alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
Letter_to_id = {char: i for i, char in enumerate(Alphabet)}
id_to_Letter = {i: char for i, char in enumerate(Alphabet)}

M = 31
M_sq = M ** 2

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    return d, y1 - (b // a) * x1, x1

def mod_inverse(a, n):
    d, x, y = extended_gcd(a, n)
    if d != 1: return None
    return x % n

def decrypt_text(ciphertext, a, b):
    a_inv = mod_inverse(a, M_sq)
    if a_inv is None: return None

    res = []
    for i in range(0, len(ciphertext) - 1, 2):
        y = Letter_to_id[ciphertext[i]] * M + Letter_to_id[ciphertext[i+1]]
        x = (a_inv * (y - b)) % M_sq
        res.append(id_to_Letter[x // M] + id_to_Letter[x % M])
    return "".join(res)

if __name__ == "__main__":

    best_a, best_b = 390, 10

    with open('04.txt', 'r', encoding='utf-8') as f:
        cipher = f.read().strip().replace('\n', '').replace(' ', '')

    print(f"Розшифрування з ключем a={best_a}, b={best_b}...")
    decrypted = decrypt_text(cipher, best_a, best_b)

    with open('decrypted_04.txt', 'w', encoding='utf-8') as f_out:
        f_out.write(decrypted)

    print("Текст у 'decrypted_04.txt'")
    print(f"Текст: {decrypted[:100]}...")
