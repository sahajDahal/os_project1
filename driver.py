#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import re

ONLY_LETTERS = re.compile(r"^[A-Za-z]+$")

def valid_letters(s: str) -> bool:
    return bool(ONLY_LETTERS.fullmatch(s))

def send_log(log_stdin, action: str, message: str = ""):
    try:
        line = f"{action} {message}".rstrip()
        print(line, file=log_stdin, flush=True)
    except BrokenPipeError:
        pass  # logger already closed

def start_processes(logfile: str):
    # Start logger
    logger = subprocess.Popen(
        [sys.executable, os.path.join(os.path.dirname(__file__), "logger_service.py"), logfile],
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    # Start encryption service
    crypto = subprocess.Popen(
        [sys.executable, os.path.join(os.path.dirname(__file__), "encryption_service.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    return logger, crypto

def crypto_cmd(crypto_proc, cmd: str, arg: str = ""):
    line = f"{cmd} {arg}".strip()
    crypto_proc.stdin.write(line + "\n")
    crypto_proc.stdin.flush()
    # One-line response: "RESULT ..." or "ERROR ..."
    resp = crypto_proc.stdout.readline()
    if not resp:
        return ("ERROR", "Encryption service not responding")
    resp = resp.rstrip("\n")
    parts = resp.split(None, 1)
    rtype = parts[0].upper()
    rest = parts[1] if len(parts) > 1 else ""
    return (rtype, rest)

def choose_from_history(history):
    if not history:
        print("History is empty.")
        return None
    while True:
        print("\nHistory:")
        for i, s in enumerate(history, 1):
            print(f"  {i}. {s}")
        print("  0. Enter a new string")
        choice = input("Select a number: ").strip()
        if choice == "0":
            return None
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(history):
                return history[idx - 1]
        print("Invalid choice. Try again.")

def main():
    ap = argparse.ArgumentParser(description="Driver program")
    ap.add_argument("logfile", help="Path to log file for the logger")
    args = ap.parse_args()

    logger, crypto = start_processes(args.logfile)
    send_log(logger.stdin, "START", "Driver started")

    history = []  # holds all entered strings and results (uppercase)
    current_menu = """
Commands:
  password  - set or reuse a passkey (not stored in history)
  encrypt   - encrypt a string (store input and result in history)
  decrypt   - decrypt a string (store input and result in history)
  history   - show this run's history
  quit      - exit
"""

    try:
        while True:
            print(current_menu)
            cmd = input("Enter command: ").strip().lower()

            if cmd == "quit":
                send_log(logger.stdin, "CMD", "quit")
                # tell services to quit
                if crypto.stdin:
                    try:
                        crypto.stdin.write("QUIT\n"); crypto.stdin.flush()
                    except BrokenPipeError:
                        pass
                if logger.stdin:
                    try:
                        print("QUIT", file=logger.stdin, flush=True)
                    except BrokenPipeError:
                        pass
                send_log(logger.stdin, "EXIT", "Driver exiting")  # may or may not reach logger in time
                break

            elif cmd == "history":
                send_log(logger.stdin, "CMD", "history")
                if history:
                    print("\nHistory:")
                    for i, s in enumerate(history, 1):
                        print(f"  {i}. {s}")
                    print()
                else:
                    print("History is empty.\n")
                send_log(logger.stdin, "RESULT", f"history_count={len(history)}")

            elif cmd == "password":
                send_log(logger.stdin, "CMD", "password")
                use = choose_from_history(history)
                if use is None:
                    pw = input("Enter new passkey (letters only): ").strip()
                    if not valid_letters(pw):
                        print("Error: passkey must contain letters only.\n")
                        send_log(logger.stdin, "ERROR", "invalid_passkey")
                        continue
                    # Do NOT store passkey in history
                    rtype, rest = crypto_cmd(crypto, "PASS", pw.upper())
                else:
                    # reuse a history string as passkey
                    pw = use
                    rtype, rest = crypto_cmd(crypto, "PASS", pw.upper())

                if rtype == "RESULT":
                    print("Passkey set.\n")
                    send_log(logger.stdin, "RESULT", "passkey_set")
                else:
                    print(f"Error: {rest}\n")
                    send_log(logger.stdin, "ERROR", rest)

            elif cmd == "encrypt":
                send_log(logger.stdin, "CMD", "encrypt")
                use = choose_from_history(history)
                if use is None:
                    plain = input("Enter string to encrypt (letters only): ").strip()
                    if not valid_letters(plain):
                        print("Error: input must contain letters only.\n")
                        send_log(logger.stdin, "ERROR", "invalid_encrypt_input")
                        continue
                    plain = plain.upper()
                    history.append(plain)
                else:
                    plain = use.upper()

                rtype, rest = crypto_cmd(crypto, "ENCRYPT", plain)
                if rtype == "RESULT":
                    print(f"Encrypted: {rest}\n")
                    history.append(rest)
                    send_log(logger.stdin, "RESULT", "encrypt_ok")
                else:
                    print(f"Error: {rest}\n")
                    send_log(logger.stdin, "ERROR", rest)

            elif cmd == "decrypt":
                send_log(logger.stdin, "CMD", "decrypt")
                use = choose_from_history(history)
                if use is None:
                    cipher = input("Enter string to decrypt (letters only): ").strip()
                    if not valid_letters(cipher):
                        print("Error: input must contain letters only.\n")
                        send_log(logger.stdin, "ERROR", "invalid_decrypt_input")
                        continue
                    cipher = cipher.upper()
                    history.append(cipher)
                else:
                    cipher = use.upper()

                rtype, rest = crypto_cmd(crypto, "DECRYPT", cipher)
                if rtype == "RESULT":
                    print(f"Decrypted: {rest}\n")
                    history.append(rest)
                    send_log(logger.stdin, "RESULT", "decrypt_ok")
                else:
                    print(f"Error: {rest}\n")
                    send_log(logger.stdin, "ERROR", rest)

            else:
                print("Unknown command. Try: password | encrypt | decrypt | history | quit\n")

    finally:
        # Clean shutdown
        try:
            if crypto.stdin:
                crypto.stdin.close()
            if crypto.stdout:
                crypto.stdout.close()
        except Exception:
            pass
        try:
            crypto.wait(timeout=2)
        except Exception:
            pass
        try:
            if logger.stdin:
                logger.stdin.close()
        except Exception:
            pass
        try:
            logger.wait(timeout=2)
        except Exception:
            pass

if __name__ == "__main__":
    main()
