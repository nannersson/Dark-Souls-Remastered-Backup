import lib
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":

    root = tk.Tk()
    root.resizable(0,0)
    root.style = ttk.Style()
    root.iconbitmap('ds.ico')
    root.style.theme_use("vista")
    app = lib.mainWindow(root)
    root.mainloop()
