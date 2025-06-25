import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from network.client_net import client_net
from network.server_net import server_net

class SendCryptedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SendCrypted")
        self.geometry("600x300")
        self.resizable(False, False)

        self.mode = tk.StringVar(value="Server")
        self.ip = tk.StringVar()
        self.port = tk.StringVar(value="5000")
        self.file_path = tk.StringVar()
        self.modals()

    def modals(self):
        tk.Label(self, text="Mode:").pack(pady=(20,5))
        tk.Radiobutton(self, text="Client", variable=self.mode, value="Client", command=self.update_fields).pack()
        tk.Radiobutton(self, text="Server", variable=self.mode, value="Server", command=self.update_fields).pack()

        self.ip_label = tk.Label(self, text="Server IP:")
        self.ip_entry = tk.Entry(self, textvariable=self.ip)

        tk.Label(self, text="Port:").pack(pady=(10, 0))
        self.port_entry = tk.Entry(self, textvariable=self.port)
        self.port_entry.pack()

        self.file_frame = ttk.Frame(self)
        tk.Label(self.file_frame, text="File to Send:").pack(side=tk.LEFT, padx=(0, 10))
        self.file_entry = tk.Entry(self.file_frame, textvariable=self.file_path, width=40)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.browse_button = tk.Button(self.file_frame, text="Browse", command=self.browse)
        self.browse_button.pack(side=tk.LEFT, padx=(10, 0))

        self.action_button = tk.Button(self, text="Send File", command=self.server_start)
        self.action_button.pack(pady=(20, 0))
        self.update_fields()

    def update_fields(self):
        mode = self.mode.get()
        if mode == "Client":
            self.ip_label.pack(pady=(10, 0))
            self.ip_entry.pack()
            self.file_frame.pack(pady=(10, 0))
            self.action_button.config(text="Send File")
        else:
            self.ip_label.pack_forget()
            self.ip_entry.pack_forget()
            self.file_frame.pack_forget()
            self.action_button.config(text="Start Server")

    def browse(self):
        file_path = filedialog.askopenfilename(title="Select a file to send")
        if file_path:
            self.file_path.set(file_path)

    def server_start(self):
        mode = self.mode.get()
        # ip = self.ip.get()
        ip = "127.0.0.1"
        port = self.port.get()
        file = self.file_path.get()

        if not port.isdigit() or not (1024 <= int(port) <= 65535):
            messagebox.showerror("Error", "Port must be a number between 1024 and 65535.")
            return

        if mode == "Client":
            if not ip:
                messagebox.showerror("Error", "IP address is required for Client mode.")
                return
            if not file:
                messagebox.showerror("Error", "File path is required.")
                return
            messagebox.showinfo("Info", f"Sending file '{file}' to {ip}:{port}")
            threading.Thread(target=self.send_file, args=(ip, int(port), file), daemon=True).start()
        else:
            messagebox.showinfo("Info", f"Starting server on port {port}")
            threading.Thread(target=self.start_server, args=(int(port),), daemon=True).start()

    def send_file(self, ip, port, file):
        try:
            client = client_net(ip, port)
            client.connectToServerSocket()
            client.sendingFilesToServer(file)
            self.after(0, lambda: messagebox.showinfo("Success", "File sent successfully!"))
        except Exception as e:
            self.after(0, lambda e=e: messagebox.showerror("Error", f"Failed to send file: {e}"))

    def start_server(self, port):
        try:
            server = server_net(port=port)
            server.accept_and_receive_file()
            self.after(0, lambda: messagebox.showinfo("Success", "File received successfully!"))
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"[Server][ERROR] {e}\nTraceback:\n{tb}")
            self.after(0, lambda e=e, tb=tb: messagebox.showerror("Error", f"Server error: {e}\nSee console for traceback."))

if __name__ == "__main__":
    app = SendCryptedApp()
    app.mainloop()