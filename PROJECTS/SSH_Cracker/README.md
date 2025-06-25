# SSH Cracker Tool

This project provides a simple and advanced SSH brute-force tool using Python. It includes:
- A basic command-line SSH brute forcer
- An advanced version with multithreading and password generation
- A GUI version built with Tkinter

## Features
- Username/password list support
- Dynamic password generation
- Retry mechanism
- Threaded brute-force
- GUI interface

## Usage

### Basic:
```bash
python3 ssh_brute.py <host> -u <user> -P <passwords.txt>
```

### Advanced:
```bash
python3 advanced_ssh_brute.py <host> -u <user> -P <passwords.txt> --threads 5
```

### GUI:
```bash
python3 gui_ssh_cracker.py
```

