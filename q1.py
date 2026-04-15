#!/usr/bin/env python3
"""Encrypt/decrypt text: reads raw_text.txt, writes encrypted and decrypted files, verifies match.

Plaintext input file name is fixed: raw_text.txt. This stage only rotates lowercase a-z by shift1
on the full alphabet; shift2 is read but unused. Other characters unchanged.
"""

import os


def encrypt_char(char, shift1, shift2):
    _ = shift2
    if char.islower():
        pos = ord(char) - ord("a")
        return chr(ord("a") + (pos + shift1) % 26)
    return char


def decrypt_char(char, shift1, shift2):
    _ = shift2
    if char.islower():
        pos = ord(char) - ord("a")
        return chr(ord("a") + (pos - shift1) % 26)
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
    raw_path = os.path.join(base, "raw_text.txt")
    enc_path = os.path.join(base, "encrypted_text.txt")
    dec_path = os.path.join(base, "decrypted_text.txt")

    if not os.path.isfile(raw_path):
        print(f"Missing {raw_path}")
        return

    try:
        s1 = input("shift1 (default 3): ").strip() or "3"
        s2 = input("shift2 (default 5): ").strip() or "5"
        k1, k2 = int(s1), int(s2)
    except ValueError:
        print("Invalid integers.")
        return

    print("Only shift1 affects lowercase a-z; shift2 is unused.")
    encryption_function(raw_path, enc_path, k1, k2)
    decryption_function(enc_path, dec_path, k1, k2)
    print("Verification OK." if verification_function(raw_path, dec_path) else "Verification failed.")


if __name__ == "__main__":
    main()
