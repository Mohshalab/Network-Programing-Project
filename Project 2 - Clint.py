import tkinter as tk
from tkinter import ttk
import requests

class RequestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTTP Requester")

        # URL Entry
        self.url_label = ttk.Label(root, text="Server URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        self.url_entry.insert(tk.END, "http://localhost:8080/")  # Default server URL

        # Method Selector
        self.method_label = ttk.Label(root, text="Method:")
        self.method_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.method_combobox = ttk.Combobox(root, values=["GET", "POST", "PUT", "DELETE"])
        self.method_combobox.current(0)
        self.method_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Headers Entry
        self.headers_label = ttk.Label(root, text="Headers:")
        self.headers_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.headers_entry = ttk.Entry(root, width=50)
        self.headers_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="we")

        # Authentication Entry
        self.auth_label = ttk.Label(root, text="Authentication:")
        self.auth_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.auth_entry = ttk.Entry(root, width=50)
        self.auth_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="we")

        # Cookies Entry
        self.cookies_label = ttk.Label(root, text="Cookies:")
        self.cookies_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.cookies_entry = ttk.Entry(root, width=50)
        self.cookies_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="we")

        # Send Button
        self.send_button = ttk.Button(root, text="Send Request", command=self.send_request)
        self.send_button.grid(row=5, column=2, padx=5, pady=5, sticky="e")

        # Response Display
        self.response_text = tk.Text(root, height=15, width=60)
        self.response_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    def send_request(self):
        server_url = self.url_entry.get()
        method = self.method_combobox.get()
        headers = self.parse_headers(self.headers_entry.get())
        auth = self.parse_auth(self.auth_entry.get())
        cookies = self.parse_cookies(self.cookies_entry.get())

        try:
            url = server_url.strip('/')  # Remove trailing slash from server URL
            response = None
            if method == "GET":
                response = requests.get(url, headers=headers, auth=auth, cookies=cookies)
            elif method == "POST":
                response = requests.post(url, headers=headers, auth=auth, cookies=cookies)
            elif method == "PUT":
                response = requests.put(url, headers=headers, auth=auth, cookies=cookies)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, auth=auth, cookies=cookies)

            self.response_text.delete(1.0, tk.END)
            if response:
                self.response_text.insert(tk.END, f"Status Code: {response.status_code}\n")
                self.response_text.insert(tk.END, "Response Headers:\n")
                for header, value in response.headers.items():
                    self.response_text.insert(tk.END, f"{header}: {value}\n")
                self.response_text.insert(tk.END, "\nResponse Content:\n")
                self.response_text.insert(tk.END, response.text)
            else:
                self.response_text.insert(tk.END, "No response received.")
        except Exception as e:
            self.response_text.delete(1.0, tk.END)
            self.response_text.insert(tk.END, f"Error: {e}")

    def parse_headers(self, headers_str):
        headers = {}
        if headers_str:
            for line in headers_str.split('\n'):
                if line.strip():
                    key, value = line.split(':')
                    headers[key.strip()] = value.strip()
        return headers

    def parse_auth(self, auth_str):
        if auth_str:
            username, password = auth_str.split(':')
            return (username, password)
        return None

    def parse_cookies(self, cookies_str):
        cookies = {}
        if cookies_str:
            for cookie in cookies_str.split(';'):
                name, value = cookie.split('=')
                cookies[name.strip()] = value.strip()
        return cookies

def main():
    root = tk.Tk()
    app = RequestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
