# 🔍 Port Scanner Using Python

A multithreaded TCP port scanner built with Python. This tool scans a given IP for open ports, detects running services, and attempts banner grabbing.

## 🚀 Features

- ✅ Scan a range of TCP ports
- ⚡ Multithreaded for faster results
- 🔐 Banner grabbing for open ports
- 📋 Formatted color-coded terminal output
- 🛠️ Lightweight and dependency-free

## 📂 Project Structure

```bash
Port-Scanner-Python/
├── port_scanner.py                # Main port scanner script
├── requirements.txt              # No dependencies (empty file for conventwion)
```

## 🛠️ How to Use

### Prerequisites
- Python 3.x

### Run the Script
```bash
python port_scanner.py
```

### Sample Input
```text
Enter your target ip: scanme.nmap.org
Enter the start port: 20
Enter end port: 100
```

## 📌 Example Output

```text
Starting scan on host: 45.33.32.156
Progress: 81/81 ports scanned

Port Scan Results:
Port     Service         Status
-----------------------------------------------------
22       ssh             Open
          SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.7
```

## ⚠️ Disclaimer
This tool is intended for **educational and ethical testing purposes only**. Do not use it on networks you do not own or have permission to scan.

---

Made with ❤️ by **Aayush-Raj-Singh** 
