#!/usr/bin/env python3
"""Full Q1: raw_text.txt (fixed name), split-alphabet cipher, encrypt/decrypt/verify with detailed mismatch diagnostics."""

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
    print(f"Reading {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        body = f.read()
    print(f"{len(body)} chars; encrypting...")
    out = encrypt_text(body, shift1, shift2)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Wrote {output_file}")
    return out


def decryption_function(input_file, output_file, shift1, shift2):
    print(f"Reading {input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        body = f.read()
    plain = decrypt_text(body, shift1, shift2)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(plain)
    print(f"Wrote {output_file}")
    return plain


def verification_function(original_file, decrypted_file):
    print("Verifying...")
    with open(original_file, "r", encoding="utf-8") as f:
        a = f.read()
    with open(decrypted_file, "r", encoding="utf-8") as f:
        b = f.read()
    if a == b:
        print(f"Match ({len(a)} chars).")
        return True
    print(f"Lengths: {len(a)} vs {len(b)}")
    n = min(len(a), len(b))
    bad = [i for i in range(n) if a[i] != b[i]][:10]
    if bad:
        print(f"First differing indices: {bad}")
        for i in bad[:5]:
            print(f"  {i}: {a[i]!r} vs {b[i]!r}")
    return False


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
    result = verification_function(raw_f, dec_f)
    print("OK" if result else "Mismatch")

if __name__ == "__main__":
    main()
