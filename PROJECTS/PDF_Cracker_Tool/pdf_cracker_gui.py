import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import pikepdf
import itertools
import string
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
import os

class PDFCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 PDF Cracker Tool")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Variables
        self.pdf_file = ""
        self.wordlist_file = ""
        self.attack_mode = tk.StringVar(value="dictionary")
        self.charset = string.ascii_letters + string.digits
        self.min_length = tk.IntVar(value=1)
        self.max_length = tk.IntVar(value=3)
        self.max_threads = tk.IntVar(value=4)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="PDF Cracker Tool", font=("Arial", 18, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Button(frame, text="Select PDF File", command=self.load_pdf).grid(row=0, column=0, padx=5, pady=5)
        self.pdf_label = tk.Label(frame, text="No file selected", width=40, anchor="w")
        self.pdf_label.grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Select Wordlist (Optional)", command=self.load_wordlist).grid(row=1, column=0, padx=5, pady=5)
        self.wordlist_label = tk.Label(frame, text="No wordlist selected", width=40, anchor="w")
        self.wordlist_label.grid(row=1, column=1, padx=5)

        tk.Label(self.root, text="Select Attack Mode:").pack(pady=5)
        tk.Radiobutton(self.root, text="Dictionary", variable=self.attack_mode, value="dictionary").pack()
        tk.Radiobutton(self.root, text="Brute-Force", variable=self.attack_mode, value="brute").pack()

        bf_frame = tk.LabelFrame(self.root, text="Brute-force Settings", padx=10, pady=10)
        bf_frame.pack(pady=5)
        tk.Label(bf_frame, text="Min Length:").grid(row=0, column=0, sticky="w")
        tk.Entry(bf_frame, textvariable=self.min_length, width=5).grid(row=0, column=1)
        tk.Label(bf_frame, text="Max Length:").grid(row=0, column=2)
        tk.Entry(bf_frame, textvariable=self.max_length, width=5).grid(row=0, column=3)
        tk.Label(bf_frame, text="Threads:").grid(row=0, column=4)
        tk.Entry(bf_frame, textvariable=self.max_threads, width=5).grid(row=0, column=5)

        tk.Button(self.root, text="Start Cracking", command=self.start_cracking, bg="green", fg="white").pack(pady=10)

        self.progress = ttk.Progressbar(self.root, mode="determinate", length=400)
        self.progress.pack(pady=5)

        self.status_text = tk.Text(self.root, height=8, width=70, wrap="word")
        self.status_text.pack(pady=10)
        self.status_text.config(state="disabled")

    def log(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")

    def load_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.pdf_label.config(text=os.path.basename(self.pdf_file) if self.pdf_file else "No file selected")

    def load_wordlist(self):
        self.wordlist_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.wordlist_label.config(text=os.path.basename(self.wordlist_file) if self.wordlist_file else "No wordlist selected")

    def generate_passwords(self):
        for length in range(self.min_length.get(), self.max_length.get() + 1):
            for password in itertools.product(self.charset, repeat=length):
                yield ''.join(password)

    def load_passwords_from_wordlist(self):
        with open(self.wordlist_file, 'r') as f:
            for line in f:
                yield line.strip()

    def try_password(self, password):
        try:
            with pikepdf.open(self.pdf_file, password=password):
                return password
        except pikepdf._core.PasswordError:
            return None
        except Exception as e:
            self.log(f"Error: {e}")
            return None

    def crack_pdf(self):
        start_time = time.time()
        self.log("Starting attack...")
        found = None

        if self.attack_mode.get() == "dictionary":
            if not self.wordlist_file:
                messagebox.showerror("Error", "No wordlist selected for dictionary attack.")
                return
            passwords = list(self.load_passwords_from_wordlist())
        else:
            passwords = list(self.generate_passwords())

        self.progress.config(maximum=len(passwords))

        with ThreadPoolExecutor(max_workers=self.max_threads.get()) as executor:
            futures = {executor.submit(self.try_password, pwd): pwd for pwd in passwords}

            for i, future in enumerate(futures):
                result = future.result()
                self.progress['value'] = i + 1
                self.root.update_idletasks()
                if result:
                    found = result
                    break

        duration = time.time() - start_time

        if found:
            self.log(f"✅ Password found: {found}")
            with open("result.txt", "w") as f:
                f.write(found)
        else:
            self.log("❌ Password not found.")

        self.log(f"🕒 Time Taken: {duration:.2f} seconds")
        messagebox.showinfo("Done", "Cracking completed.")

    def start_cracking(self):
        if not self.pdf_file:
            messagebox.showerror("Error", "Please select a PDF file.")
            return
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state="disabled")
        thread = threading.Thread(target=self.crack_pdf)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFCrackerGUI(root)
    root.mainloop()
