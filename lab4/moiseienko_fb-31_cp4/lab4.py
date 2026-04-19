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
