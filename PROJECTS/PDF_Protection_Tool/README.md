# 🔐 PDF Protection Tool (Flask + PyPDF2 + Google Drive)

A simple web-based tool to add password protection to PDF files, built using **Flask**, **PyPDF2**, and **Bootstrap 5**. Optionally uploads protected files to **Google Drive** for cloud storage.

---

## 🛠 Features

- Upload any PDF file and set a password
- Encrypts the PDF using `PyPDF2`
- Option to upload the encrypted PDF to your **Google Drive**
- Log of previously encrypted files
- User-friendly UI styled after institutional portals (Bootstrap 5)
- Signup form for future access control (no auth backend yet)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Aayush-Raj-Singh/pdf-protection-tool.git
cd pdf-protection-tool
```

### 2. Install Required Libraries

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:

```bash
pip install Flask PyPDF2 PyDrive
```

### 3. Set Up Google Drive API (For Cloud Upload)

- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Enable **Google Drive API**
- Create OAuth 2.0 credentials (type: Desktop app)
- Download the `client_secrets.json` file
- Place it in the root of your project folder

> The first upload will trigger a browser popup for authentication

---

### 4. Run the Flask App

```bash
python app.py
```

Open in browser:
```
http://127.0.0.1:5000/
```

---

## 📂 Project Structure

```
pdf-protection-tool/
├── app.py
├── client_secrets.json       # <- Not committed
├── templates/
│   ├── index.html
│   └── signup.html
├── uploads/                  # <- Auto-created
├── log.csv                   # <- Auto-generated
├── .gitignore
└── README.md
```

---

## ⚙ Technologies Used

- [Flask](https://flask.palletsprojects.com/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [PyDrive](https://pypi.org/project/PyDrive/)
- [Bootstrap 5](https://getbootstrap.com/)
- HTML/CSS, Python

---

## ✍️ Future Plans

- 🔒 User login/authentication
- ☁️ Allow choosing a Google Drive folder
- 🧾 Export logs as CSV or PDF
- 🖼 UI themes for dark/light mode

---

## 📄 License

MIT License – free to use, fork, and modify.

---

## 🙌 Acknowledgements

Project by **Aayuysh Raj**  
Internship with **InLighn Tech**
