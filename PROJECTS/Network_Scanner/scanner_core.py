# scanner_core.py

import scapy.all as scapy
import socket
import threading
from queue import Queue
import ipaddress

def scan_ip(ip, result_queue):
    """Sends an ARP request to a single IP and captures response."""
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    answer = scapy.srp(packet, timeout=1, verbose=False)[0]

    for sent, received in answer:
        client_info = {
            'IP': received.psrc,
            'MAC': received.hwsrc,
            'Hostname': get_hostname(received.psrc)
        }
        result_queue.put(client_info)

def get_hostname(ip):
    """Attempts to resolve hostname for an IP address."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def run_scan(cidr, on_result=None):
    """
    Main function to run the scan.
    :param cidr: IP range in CIDR format (e.g., 192.168.1.0/24)
    :param on_result: Optional callback for real-time GUI updates
    :return: List of all discovered clients
    """
    network = ipaddress.ip_network(cidr, strict=False)
    result_queue = Queue()
    threads = []

    for ip in network.hosts():
        thread = threading.Thread(target=scan_ip, args=(str(ip), result_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    clients = []
    while not result_queue.empty():
        client = result_queue.get()
        clients.append(client)
        if on_result:
            on_result(client)  # Real-time update (for GUI)

    return clients
