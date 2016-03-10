#!/usr/bin/env python3
import random
import argparse


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(n**0.5) + 1, 2))


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(e, phi):
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('Odwrotność modulo nie istnieje')
    else:
        return x % phi


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Obie liczby muszą być pierwsze.')
    elif p == q:
        raise ValueError('Liczby nie mogą być równe.')
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = modinv(e, phi)
    return (e, n), (d, n)  # public, private


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Implementacja RSA')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--generate", type=int, nargs=2, help="generowanie kluczy publicznego i prywatnego")
    group.add_argument("-e", "--encrypt", type=str, nargs=3, help="szyfrowanie widomosci")
    group.add_argument("-d", "--decrypt", type=str, nargs='+', help="deszyfracja wiadomosci")
    args = parser.parse_args()

    if args.generate:
        p = args.generate[0]
        q = args.generate[1]
        public, private = generate_keypair(p, q)
        print("Klucz publiczny to", public, ",klucz prywatny to", private)
    elif args.encrypt:
        e = int(args.encrypt[0])
        n = int(args.encrypt[1])
        message = args.encrypt[2]
        encrypted_msg = encrypt((e, n), message)
        print("Zaszyfrowana wiadomość: ")
        print(' '.join(map(lambda x: str(x), encrypted_msg)))
    elif args.decrypt:
        d = int(args.decrypt[0])
        n = int(args.decrypt[1])
        message = [int(args.decrypt[x]) for x in range(2, len(args.decrypt))]
        decrypted_msg = decrypt((d, n), message)
        print("Odszyfrowana wiadomość: ", decrypted_msg)

