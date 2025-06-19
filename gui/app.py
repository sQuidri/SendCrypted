import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SendCryptedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SendCrypted")
        self.geometry("600x300")

        self.resizable(False, False)
        
if __name__ == "__main__":
    app = SendCryptedApp()
    app.mainloop()
    app.mainloop()
