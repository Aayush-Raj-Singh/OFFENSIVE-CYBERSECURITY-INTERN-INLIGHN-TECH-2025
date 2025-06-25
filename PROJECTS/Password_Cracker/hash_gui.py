import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import hashlib
import itertools
import string
from concurrent.futures import ThreadPoolExecutor

# Supported hash types
HASH_TYPES = [
    'md5', 'sha1', 'sha224', 'sha256', 'sha384',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'sha512'
]

def check_hash(hash_fn, password, target_hash):
    return hash_fn(password.encode()).hexdigest() == target_hash

def crack_with_wordlist(target_hash, wordlist_path, hash_type, log_area):
    try:
        hash_fn = getattr(hashlib, hash_type)
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f.readlines()]
        log_area.insert(tk.END, f"[*] Loaded {len(passwords)} passwords.\n")
        for pwd in passwords:
            if check_hash(hash_fn, pwd, target_hash):
                return pwd
    except Exception as e:
        log_area.insert(tk.END, f"[!] Error: {e}\n")
    return None

def crack_brute_force(target_hash, hash_type, min_len, max_len, characters, log_area):
    try:
        hash_fn = getattr(hashlib, hash_type)
        for length in range(min_len, max_len + 1):
            for pwd in itertools.product(characters, repeat=length):
                guess = ''.join(pwd)
                if check_hash(hash_fn, guess, target_hash):
                    return guess
    except Exception as e:
        log_area.insert(tk.END, f"[!] Error: {e}\n")
    return None

def start_cracking():
    hash_value = hash_entry.get()
    hash_type = hash_type_var.get()
    use_wordlist = wordlist_var.get()
    wordlist_path = wordlist_path_var.get()
    min_len = int(min_length_var.get() or 0)
    max_len = int(max_length_var.get() or 0)
    characters = character_set_var.get() or string.ascii_letters + string.digits

    output_area.delete(1.0, tk.END)
    output_area.insert(tk.END, f"[*] Cracking hash using {hash_type}...\n")

    def crack():
        result = None
        if use_wordlist:
            result = crack_with_wordlist(hash_value, wordlist_path, hash_type, output_area)
        else:
            result = crack_brute_force(hash_value, hash_type, min_len, max_len, characters, output_area)

        if result:
            output_area.insert(tk.END, f"\n[+] Password found: {result}\n")
        else:
            output_area.insert(tk.END, "\n[!] Password not found.\n")

    ThreadPoolExecutor(max_workers=1).submit(crack)

# GUI Setup
root = tk.Tk()
root.title("Password Cracker Using Python")
root.geometry("700x600")

tk.Label(root, text="Enter Hash:").pack()
hash_entry = tk.Entry(root, width=80)
hash_entry.pack()

tk.Label(root, text="Select Hash Type:").pack()
hash_type_var = tk.StringVar(value="md5")
tk.OptionMenu(root, hash_type_var, *HASH_TYPES).pack()

wordlist_var = tk.BooleanVar()
tk.Checkbutton(root, text="Use Wordlist", variable=wordlist_var).pack()

wordlist_path_var = tk.StringVar()
tk.Entry(root, textvariable=wordlist_path_var, width=50).pack()
tk.Button(root, text="Browse Wordlist", command=lambda: wordlist_path_var.set(filedialog.askopenfilename())).pack()

tk.Label(root, text="Min Length (for Brute Force):").pack()
min_length_var = tk.StringVar()
tk.Entry(root, textvariable=min_length_var).pack()

tk.Label(root, text="Max Length (for Brute Force):").pack()
max_length_var = tk.StringVar()
tk.Entry(root, textvariable=max_length_var).pack()

tk.Label(root, text="Character Set (optional):").pack()
character_set_var = tk.StringVar()
tk.Entry(root, textvariable=character_set_var).pack()

tk.Button(root, text="Start Cracking", command=start_cracking, bg='green', fg='white').pack(pady=10)

tk.Label(root, text="Output:").pack()
output_area = scrolledtext.ScrolledText(root, height=20, width=80)
output_area.pack()

root.mainloop()
