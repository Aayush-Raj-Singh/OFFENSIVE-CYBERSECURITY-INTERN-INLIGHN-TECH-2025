import requests
import threading

domain = 'youtube.com'  # Target domain

discovered_subdomains = []   # List to store discovered subdomains

lock = threading.Lock()   # Lock for thread-safe list access

def check_subdomain(subdomain):   # Function to check if subdomain exists
    url = f"http://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code < 400:
            print(f"[+] Found: {url}")
            with lock:
                discovered_subdomains.append(url)
    except requests.ConnectionError:
        pass
    except requests.Timeout:
        print(f"[-] Timeout: {url}")

with open("subdomains.txt") as file:   # Read subdomains from file
    subdomains = file.read().splitlines()

threads = []    # Create and start threads
for subdomain in subdomains:
    t = threading.Thread(target=check_subdomain, args=(subdomain,))
    t.start()
    threads.append(t)

for t in threads:      # Wait for all threads to finish
    t.join()

with open("discovered_subdomains.txt", "w") as f:   # Save discovered subdomains to file
    for sub in discovered_subdomains:
        f.write(sub + "\n")

print(f"\n[✔] Scan complete. Results saved to discovered_subdomains.txt")
