# gui_app.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from scanner_core import run_scan

class NetworkScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Network Scanner")
        self.root.geometry("700x500")
        self.clients = []

        self.build_ui()

    def build_ui(self):
        # Entry Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter CIDR (e.g., 192.168.1.0/24):").grid(row=0, column=0, padx=5)
        self.cidr_entry = tk.Entry(input_frame, width=30)
        self.cidr_entry.grid(row=0, column=1)

        self.scan_button = tk.Button(input_frame, text="Start Scan", command=self.start_scan, bg="green", fg="white")
        self.scan_button.grid(row=0, column=2, padx=5)

        # Table Frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("IP", "MAC", "Hostname"), show="headings")
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("MAC", text="MAC Address")
        self.tree.heading("Hostname", text="Hostname")
        self.tree.pack(fill="both", expand=True)

        # Save Button
        save_button = tk.Button(self.root, text="Save Results", command=self.save_results)
        save_button.pack(pady=10)

    def start_scan(self):
        cidr = self.cidr_entry.get()
        if not cidr:
            messagebox.showwarning("Input Error", "Please enter a valid CIDR range.")
            return

        self.clients.clear()
        self.tree.delete(*self.tree.get_children())
        self.scan_button.config(state="disabled", text="Scanning...")

        threading.Thread(target=self.scan_network, args=(cidr,), daemon=True).start()

    def scan_network(self, cidr):
        def update_table(client):
            self.clients.append(client)
            self.tree.insert("", "end", values=(client['IP'], client['MAC'], client['Hostname']))

        try:
            run_scan(cidr, on_result=update_table)
            self.scan_button.config(state="normal", text="Start Scan")
            messagebox.showinfo("Scan Complete", f"Scan completed. {len(self.clients)} devices found.")
        except Exception as e:
            messagebox.showerror("Error", f"Scan failed: {e}")
            self.scan_button.config(state="normal", text="Start Scan")

    def save_results(self):
        if not self.clients:
            messagebox.showwarning("No Data", "No scan results to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for client in self.clients:
                    f.write(f"{client['IP']}\t{client['MAC']}\t{client['Hostname']}\n")
            messagebox.showinfo("Saved", "Results saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkScannerGUI(root)
    root.mainloop()
