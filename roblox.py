import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import threading
import re
from datetime import datetime

class AutoRobloxDownloader(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(" Roblox Asset Downloader")
        self.geometry("520x420")
        self.resizable(False, False)

        self.cookie_var = tk.StringVar()
        self.running = False

        self.build_ui()
    def build_ui(self):
        title = ttk.Label(self, text="Roblox Asset Downloader", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        ttk.Label(self, text="ALT ACCOUNT ROBLOSECURITY Cookie").pack(anchor="w", padx=10)
        self.cookie_entry = ttk.Entry(self, textvariable=self.cookie_var, show="*", width=70)
        self.cookie_entry.pack(padx=10, pady=5)

        ttk.Label(self, text="Asset IDs (one per line)").pack(anchor="w", padx=10)
        self.asset_box = tk.Text(self, height=10, width=65)
        self.asset_box.pack(padx=10, pady=5)

        self.start_btn = ttk.Button(self, text="Start Auto Download", command=self.start)
        self.start_btn.pack(pady=10)

        self.log_box = tk.Text(self, height=8, width=65, state="disabled")
        self.log_box.pack(padx=10, pady=5)
    def log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"{datetime.now().strftime('%H:%M:%S')} | {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")
    def clean_id(self, text):
        return re.sub(r"\D+", "", text)
    def download_asset(self, asset_id, cookie):
        url = f"https://assetdelivery.roblox.com/v1/asset?id={asset_id}"

        headers = {
            "User-Agent": "Roblox/WinInet"
        }

        cookies = {}
        if cookie:
            cookies[".ROBLOSECURITY"] = cookie

        try:
            r = requests.get(url, headers=headers, cookies=cookies, timeout=15)

            if r.status_code == 401:
                return f"[401] Unauthorized - invalid cookie or no permission for {asset_id}"

            if r.status_code != 200:
                return f"[{r.status_code}] Failed for {asset_id}"

            data = r.content
            ext = "bin"
            if data.startswith(b"\x89PNG"):
                ext = "png"
            elif data.startswith(b"\xff\xd8"):
                ext = "jpg"
            elif b"ROBLOX" in data[:50]:
                ext = "rbxm"

            out_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            os.makedirs(out_dir, exist_ok=True)

            path = os.path.join(out_dir, f"{asset_id}.{ext}")

            with open(path, "wb") as f:
                f.write(data)

            return f"Saved: {path}"

        except requests.RequestException as e:
            return f"Network error: {e}"
    def start(self):
        if self.running:
            return

        self.running = True
        self.start_btn.config(state="disabled")

        thread = threading.Thread(target=self.run_auto, daemon=True)
        thread.start()

    def run_auto(self):
        cookie = self.cookie_entry.get().strip()
        ids = self.asset_box.get("1.0", "end").splitlines()

        cleaned = [self.clean_id(i) for i in ids if i.strip()]

        if not cleaned:
            self.log("No asset IDs provided.")
            self.running = False
            self.start_btn.config(state="normal")
            return

        self.log(f"Starting auto download for {len(cleaned)} assets...")

        for asset_id in cleaned:
            self.log(f"Downloading {asset_id} ...")

            result = self.download_asset(asset_id, cookie)
            self.log(result)

        self.log("Done.")
        self.running = False
        self.start_btn.config(state="normal")
if __name__ == "__main__":
    app = AutoRobloxDownloader()
    app.mainloop()
