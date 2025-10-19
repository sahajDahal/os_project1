#!/usr/bin/env python3
import sys
import string

ALPHA = string.ascii_uppercase
A2I = {c:i for i,c in enumerate(ALPHA)}

def is_letters(s: str) -> bool:
    return s.isalpha()

def vigenere(text: str, key: str, decrypt: bool=False) -> str:
    text = text.upper()
    key = key.upper()
    out = []
    klen = len(key)
    ki = 0
    for ch in text:
        # This service expects only letters; driver enforces this.
        t = A2I[ch]
        k = A2I[key[ki % klen]]
        if decrypt:
            val = (t - k) % 26
        else:
            val = (t + k) % 26
        out.append(ALPHA[val])
        ki += 1
    return "".join(out)

def main():
    passkey = None
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        # Command is first word; rest is argument (may be empty)
        parts = line.split(None, 1)
        cmd = parts[0].upper()
        arg = parts[1].strip().upper() if len(parts) > 1 else ""

        if cmd in ("QUIT",):
            break

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

        if cmd == "ENCRYPT":
            if passkey is None:
                print("ERROR Password not set", flush=True)
                continue
            if not arg or not is_letters(arg):
                print("ERROR Input must contain letters only", flush=True)
                continue
            print("RESULT " + vigenere(arg, passkey, decrypt=False), flush=True)
            continue

        if cmd == "DECRYPT":
            if passkey is None:
                print("ERROR Password not set", flush=True)
                continue
            if not arg or not is_letters(arg):
                print("ERROR Input must contain letters only", flush=True)
                continue
            print("RESULT " + vigenere(arg, passkey, decrypt=True), flush=True)
            continue

        print("ERROR Unknown command", flush=True)

if __name__ == "__main__":
    main()
