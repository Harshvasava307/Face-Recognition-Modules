# gui_main.py

import tkinter as tk
from tkinter import messagebox
import subprocess

# Functions for button actions
def add_new_employee():
    # Calls the add_new_face.py script
    subprocess.Popen(["python", "gui_add_new_face.py"])

def start_recognition():
    # Calls the camera_module_ui.py script
    subprocess.Popen(["python", "gui_live_recognition.py"])

def view_logs():
    try:
        with open("recognized_faces.csv", "r") as f:
            logs = f.read()
        log_window = tk.Toplevel(root)
        log_window.title("Recognition Logs")
        text = tk.Text(log_window, width=60, height=20)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, logs)
    except FileNotFoundError:
        messagebox.showinfo("Logs", "No logs found yet.")

# ----------------- GUI -----------------
root = tk.Tk()
root.title("Face Recognition System")
root.geometry("500x400")
root.resizable(False, False)

# Title Label
title_label = tk.Label(root, text="Face Recognition System", font=("Helvetica", 20, "bold"))
title_label.pack(pady=20)

# Buttons
btn_add = tk.Button(root, text="Add New Employee", font=("Helvetica", 14), width=25, command=add_new_employee)
btn_add.pack(pady=10)

btn_recognize = tk.Button(root, text="Start Recognition", font=("Helvetica", 14), width=25, command=start_recognition)
btn_recognize.pack(pady=10)

btn_logs = tk.Button(root, text="View Logs", font=("Helvetica", 14), width=25, command=view_logs)
btn_logs.pack(pady=10)

# Footer / Subtitle
footer_label = tk.Label(root, text="Ensure good lighting and a clear face", font=("Helvetica", 10), fg="gray")
footer_label.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
