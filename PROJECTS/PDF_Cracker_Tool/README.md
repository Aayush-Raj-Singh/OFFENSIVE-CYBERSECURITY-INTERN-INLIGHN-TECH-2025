
# 🔐 PDF Cracker Tool (CLI + GUI)

A Python-based tool to crack password-protected PDF files using **dictionary** or **brute-force** attacks. Built for both **command-line users** and **non-technical users** via a simple **Tkinter GUI**.

---

## 🧰 Features

- 🗂 Upload and crack password-protected PDFs
- 🧠 Supports Dictionary & Brute-force attacks
- 💡 Multi-threaded cracking for speed
- 🧾 GUI with progress bar and real-time logging
- 📜 CLI version with customizable arguments
- 💾 Saves cracked password to `result.txt`

---

## 🗃️ Folder Structure

```
pdf_cracker_tool/
├── cracker_core.py        # Shared cracking logic
├── cracker.py             # CLI version  &&  Code provided
├── pdf_cracker_gui.py     # Tkinter GUI version
├── requirements.txt
└── README.md
```

---

## 🖥️ CLI Usage

```bash
python cracker.py path/to/file.pdf --wordlist wordlist.txt
```

OR brute-force:

```bash
python cracker.py path/to/file.pdf --generate --min_length 1 --max_length 3 --max_workers 4
```

---

## 🖼️ GUI Usage

```bash
python pdf_cracker_gui.py
```

- Upload PDF
- (Optional) Upload wordlist
- Choose **Dictionary** or **Brute-force**
- Set charset range and threads (for brute-force)
- Click **Start Cracking**

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚠️ Disclaimer

> This tool is intended for **educational** and **ethical hacking** purposes only.  
> Use it responsibly and legally on PDFs you own or have permission to test.

---

## 🛡️ Developed by:
**Aayush-Raj_Singh under InLighn Tech - Cybersecurity Training**
