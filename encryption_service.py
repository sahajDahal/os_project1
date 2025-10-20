#!/usr/bin/env python3
import sys
import string

ALPHA = string.ascii_uppercase
A2I = {c: i for i, c in enumerate(ALPHA)}

def is_letters(s: str) -> bool:
    """Check that the string contains only letters."""
    return s.isalpha()

def vigenere(text: str, key: str, decrypt: bool = False) -> str:
    """Perform Vigenère cipher encryption or decryption."""
    text = text.upper()
    key = key.upper()
    out = []
    klen = len(key)
    ki = 0
    for ch in text:
        t = A2I[ch]
        k = A2I[key[ki % klen]]
        val = (t - k) % 26 if decrypt else (t + k) % 26
        out.append(ALPHA[val])
        ki += 1
    return "".join(out)

def main():
    passkey = None
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue

        parts = line.split(None, 1)
        cmd = parts[0].upper()
        arg = parts[1].strip().upper() if len(parts) > 1 else ""

        # Handle quit
        if cmd == "QUIT":
            break

        # Handle passkey setup (alias PASSKEY → PASS)
        if cmd in ("PASS", "PASSKEY"):
            if not arg:
                print("ERROR Missing passkey", flush=True)
                continue
            if not is_letters(arg):
                print("ERROR Passkey must contain letters only", flush=True)
                continue
            passkey = arg
            print("RESULT", flush=True)
            continue

        # Encrypt
        if cmd == "ENCRYPT":
            if passkey is None:
                print("ERROR Password not set", flush=True)
                continue
            if not arg or not is_letters(arg):
                print("ERROR Input must contain letters only", flush=True)
                continue
            result = vigenere(arg, passkey, decrypt=False)
            print("RESULT " + result, flush=True)
            continue

        # Decrypt
        if cmd == "DECRYPT":
            if passkey is None:
                print("ERROR Password not set", flush=True)
                continue
            if not arg or not is_letters(arg):
                print("ERROR Input must contain letters only", flush=True)
                continue
            result = vigenere(arg, passkey, decrypt=True)
            print("RESULT " + result, flush=True)
            continue

        # Unknown command
        print("ERROR Unknown command", flush=True)

if __name__ == "__main__":
    main()
