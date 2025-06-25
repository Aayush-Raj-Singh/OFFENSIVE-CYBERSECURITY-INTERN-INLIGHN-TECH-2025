# 🔐 Password Cracker Using Python

A multithreaded Python tool that cracks hashed passwords using either a wordlist or brute-force attack.

## 🚀 Features
- Supports MD5, SHA1, SHA256, SHA3, and more
- Uses wordlists or generated passwords
- Multithreaded for speed
- Real-time progress display

## 🧠 How It Works
- Hash comparison using Python's `hashlib`
- Generates all possible combinations of characters for brute-force
- Uses `tqdm` for progress bar and `ThreadPoolExecutor` for threading

## 🔧 Usage

### Dictionary Attack
```bash
python hash_cracker.py <hash> -w wordlist.txt --hash_type sha256
```

### Brute-force Attack
```bash
python hash_cracker.py <hash> --hash_type sha1 --min_length 3 --max_length 5 -c abc123
```

## 📚 Supported Hash Types
- md5
- sha1
- sha224
- sha256
- sha384
- sha512
- sha3_224
- sha3_256
- sha3_384
- sha3_512

## 📂 Project Structure
```
Password-Cracker/
├── hash_cracker.py
├── requirements.txt
├── README.md
└── Password Cracker Using Python.pdf
```

## ⚠️ Disclaimer
This project is for educational and ethical hacking purposes only. Do not use it on unauthorized systems.

---

Made with ❤️ by  **Aayush-Raj-Singh**