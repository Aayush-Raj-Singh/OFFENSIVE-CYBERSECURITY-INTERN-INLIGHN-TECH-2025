# 🔍 Python Network Scanner (Tkinter GUI + Multithreaded ARP)

A powerful Python-based network scanner that identifies devices on a network using **ARP requests**, **multithreading**, and an easy-to-use **Tkinter GUI**.

## 🧰 Features

- 🧾 Accepts IP range in CIDR notation (e.g., `192.168.1.0/24`)
- ⚙️ Uses ARP to detect active hosts
- 🌐 Retrieves IP, MAC address, and Hostname
- 🧵 Multithreaded for faster scanning
- 🖼️ GUI built with Tkinter (no terminal needed)
- 💾 Option to save results to a `.txt` file

## 🗂️ Project Structure

```
network_scanner/
├── scanner_core.py      # Core scanning logic
├── gui_app.py           # Tkinter GUI application
├── requirements.txt     # Dependencies
└── README.md          
```

## 🚀 How to Run

### 1. 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. ▶️ Launch the GUI

```bash
python gui_app.py
```

## ⚠️ Legal Notice

> This tool is for **educational** and **authorized use** only.
> Scanning networks without permission is illegal.
> Always test on networks you own or are allowed to scan.

## 🛡️ Developed by

**Aayush-Raj-Singh under InLighn Tech - Cybersecurity Learning Project**

## 🧱 Windows Users: Npcap Required

If you encounter this error:

```
RuntimeError: Sniffing and sending packets is not available at layer 2: winpcap is not installed.
```

👉 It means **Npcap** is not installed on your system. Scapy needs it to send ARP packets on Windows.

### ✅ How to Fix

1. Download Npcap: https://nmap.org/npcap/
2. During installation, check:
   - ✅ "Install Npcap in WinPcap API-compatible Mode"
3. Restart your system after installation.
4. Run the script again.

