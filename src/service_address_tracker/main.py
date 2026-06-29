import tkinter as tk
from tkinter import messagebox
from service_address_tracker.services.app import App

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    # Properly close the app if prompted to
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()