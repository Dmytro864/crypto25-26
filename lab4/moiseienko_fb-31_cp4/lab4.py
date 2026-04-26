import random

def power_mod(base, exponent, modulus):
    res = 1
    base %= modulus
    while exponent > 0:
        if exponent % 2 == 1:
            res = (res * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return res

def is_prime_miller_rabin(p, k=10):
    if p < 2: return False
    if p % 2 == 0: return p == 2

    for small_prime in [3, 5, 7, 11, 13, 17, 19, 23]:
        if p == small_prime: return True
        if p % small_prime == 0: return False

    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        x = random.randint(2, p - 2)

        val = power_mod(x, d, p)
        if val == 1 or val == p - 1:
            continue

        for _ in range(s - 1):
            val = power_mod(val, 2, p)
            if val == p - 1:
                break
        else:
            return False
    return True

def generate_random_prime(bit_length):
    while True:
        p = random.getrandbits(bit_length)
        p |= (1 << (bit_length - 1)) | 1
        if is_prime_miller_rabin(p):
            return p

def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def GenerateKeyPair(bit_length=256):
    p = generate_random_prime(bit_length)
    q = generate_random_prime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    gcd, d, _ = extended_gcd(e, phi)
    d %= phi

    return {"public": (e, n), "private": (d, p, q)}

def Encrypt(message, e,  n):
    return power_mod(message, e, n)

def Decrypt(ciphertext, d, n):
    return power_mod(ciphertext, d, n)

def Sign(message, d, n):
    return power_mod(message, d, n)

def Verify(message, signature, e, n):
    return message == power_mod(signature, e, n)

def SendKey(k, d_A, n_A, e_B, n_B):
    k1 = power_mod(k, e_B, n_B)

    S = Sign(k, d_A, n_A)

    S1 = power_mod(S, e_B, n_B)

    return k1, S1

def ReceiveKey(k1, S1, d_B, n_B, e_A, n_A):
    k = power_mod(k1, d_B, n_B)

    S = power_mod(S1, d_B, n_B)

    is_authentic = Verify(k, S, e_A, n_A)

    return k, is_authentic

def main():
    print("Генерація ключів для абонентів A та B")
    while True:
        key_A = GenerateKeyPair(256)
        key_B = GenerateKeyPair(256)

        n_A = key_A["public"][1]
        n_B = key_B["public"][1]

        if n_B >= n_A:
            break

    e_A, n_A = key_A["public"]
    d_A, p_A, q_A = key_A["private"]

    e_B, n_B = key_B["public"]
    d_b, p_B, q_B = key_B["private"]

    print(f"Абонент A:\n p={p_A}\n q={q_A}\n n={n_A}\n e={e_A}\n d={d_A}\n")
    print(f"Абонент B:\n p={p_B}\n q={q_B}\n n={n_B}\n e={e_B}\n d={d_b}\n")

    print("Шифрування та Цифровий підпис")
    M = random.randint(100, n_A - 1)
    print(f"Відкрите повідомлення M: {M}")

    C = Encrypt(M, e_B, n_B)
    print(f"Шифртекст (C): {C}")

    M_decrypted = Decrypt(C, d_b, n_B)
    print(f"Розшифроване повідомлення: {M_decrypted}")
    print(f"Перевірка розшифрування: {'Успішно' if M == M_decrypted else 'Помилка'}")

    S = Sign(M, d_A, n_A)
    print(f"Цифровий підпис (S): {S}")

    is_valid = Verify(M, S, e_A, n_A)
    print(f"Перевірка підпису: {'Вірний' if is_valid else 'Невірний'}")

    print("\nПротокол конфіденційного розсилання ключів")
    k = random.randint(100, n_A - 1)
    print(f"Секретний ключ k для передачі: {k}")

    k1, S1 = SendKey(k, d_A, n_A, e_B, n_B)
    print(f"Характеристики передачі:\n k1 (шифр. ключ)={k1}\n S1 (шифр. підпис)={S1}")

    received_k, authentic = ReceiveKey(k1, S1, d_b, n_B, e_A, n_A)
    print(f"Отриманий ключ k: {received_k}")
    print(f"Автентифікація відправника: {'Підтверджено' if authentic else 'Відхилено'}")

if __name__ == "__main__":
    main()


