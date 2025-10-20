# Vigenère Encryption System (Python)

## Overview

This project implements a three-program system that communicates through **pipes** using Python’s `subprocess` module.  
The system includes:

1. **Logger** – records program activity with timestamps.
2. **Encryption Service** – performs Vigenère cipher encryption and decryption.
3. **Driver** – provides an interactive menu and coordinates communication between the other two programs.

Running the driver automatically launches the logger and encryption programs and connects them via standard input/output streams.

---

## Files and Their Roles

| File                      | Description                                                                                                                                                        |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **driver.py**             | The main entry point. Spawns the logger and encryption services, provides the user interface, manages history, validates input, and logs all commands and results. |
| **logger_service.py**     | Accepts log messages via standard input and writes them to the specified log file in the format `YYYY-MM-DD HH:MM [ACTION] MESSAGE`. Stops when receiving `QUIT`.  |
| **encryption_service.py** | Implements the Vigenère cipher. Accepts commands: `PASS` / `PASSKEY`, `ENCRYPT`, `DECRYPT`, and `QUIT`. Returns either `RESULT <output>` or `ERROR <message>`.     |
| **devlog.md**             | Developer log containing session-by-session notes and progress updates.                                                                                            |
| **README.md**             | This file describes the project, how to run it, and grading notes.                                                                                                 |
| **.gitignore**            | Standard ignore file for Python caches and logs.                                                                                                                   |

---

## How to Run

### 1. Run the Driver (starts the whole system)

```bash
python3 driver.py app.log
```
