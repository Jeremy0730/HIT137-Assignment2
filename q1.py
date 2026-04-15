#!/usr/bin/env python3
"""Split-alphabet encrypt/decrypt for raw_text.txt (fixed name). Each half of a-z and A-Z uses mod-13 shifts."""

import os


def encrypt_char(char, shift1, shift2):
    if char.islower():
        if "a" <= char <= "m":
            s = shift1 * shift2
            p = (ord(char) - ord("a") + s) % 13
            return chr(ord("a") + p)
        s = shift1 + shift2
        p = (ord(char) - ord("n") - s) % 13
        return chr(ord("n") + p)
    if char.isupper():
        if "A" <= char <= "M":
            p = (ord(char) - ord("A") - shift1) % 13
            return chr(ord("A") + p)
        s = shift2 ** 2
        p = (ord(char) - ord("N") + s) % 13
        return chr(ord("N") + p)
    return char


def decrypt_char(char, shift1, shift2):
    if char.islower():
        if "a" <= char <= "m":
            s = shift1 * shift2
            p = (ord(char) - ord("a") - s) % 13
            return chr(ord("a") + p)
        s = shift1 + shift2
        p = (ord(char) - ord("n") + s) % 13
        return chr(ord("n") + p)
    if char.isupper():
        if "A" <= char <= "M":
            p = (ord(char) - ord("A") + shift1) % 13
            return chr(ord("A") + p)
        s = shift2 ** 2
        p = (ord(char) - ord("N") - s) % 13
        return chr(ord("N") + p)
    return char


def encrypt_text(text, shift1, shift2):
    return "".join(encrypt_char(c, shift1, shift2) for c in text)


def decrypt_text(text, shift1, shift2):
    return "".join(decrypt_char(c, shift1, shift2) for c in text)


def encryption_function(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        body = f.read()
    out = encrypt_text(body, shift1, shift2)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(out)
    return out


def decryption_function(input_file, output_file, shift1, shift2):
    with open(input_file, "r", encoding="utf-8") as f:
        body = f.read()
    plain = decrypt_text(body, shift1, shift2)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(plain)
    return plain


def verification_function(original_file, decrypted_file):
    with open(original_file, "r", encoding="utf-8") as f:
        a = f.read()
    with open(decrypted_file, "r", encoding="utf-8") as f:
        b = f.read()
    return a == b


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    raw_f = os.path.join(base, "raw_text.txt")
    enc_f = os.path.join(base, "encrypted_text.txt")
    dec_f = os.path.join(base, "decrypted_text.txt")

    if not os.path.isfile(raw_f):
        print(f"Missing {raw_f}")
        return

    try:
        k1 = int(input("shift1 (default 3): ").strip() or "3")
        k2 = int(input("shift2 (default 5): ").strip() or "5")
    except ValueError:
        print("Invalid integers.")
        return

    encryption_function(raw_f, enc_f, k1, k2)
    decryption_function(enc_f, dec_f, k1, k2)
    print("OK" if verification_function(raw_f, dec_f) else "Mismatch")


if __name__ == "__main__":
    main()
