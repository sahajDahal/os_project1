#!/usr/bin/env python3
import sys
import argparse
from datetime import datetime

def main():
    ap = argparse.ArgumentParser(description="Logger service")
    ap.add_argument("logfile", help="Path to log file")
    args = ap.parse_args()

    try:
        with open(args.logfile, "a", encoding="utf-8") as f:
            for raw in sys.stdin:
                line = raw.rstrip("\n")
                if line.strip() == "QUIT":
                    break
                if not line.strip():
                    continue
                # first token = ACTION, rest = MESSAGE
                parts = line.split(None, 1)
                action = parts[0].upper()
                message = parts[1] if len(parts) > 1 else ""
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                f.write(f"{ts} [{action}] {message}\n")
                f.flush()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()