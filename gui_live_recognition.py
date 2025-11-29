# gui_live_recognition.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import threading
import time
import os

from face_recognition_module import FaceRecognitionModule
from database_module import FaceDatabaseLogger

# ---------------- Initialize Modules ----------------
face_recog = FaceRecognitionModule()
logger = FaceDatabaseLogger()

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Face Recognition System")
root.geometry("800x600")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Face Recognition System", font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

# Canvas for Camera Feed
camera_canvas = tk.Label(root)
camera_canvas.pack(padx=10, pady=10)

# Feedback / Subtitle
subtitle_var = tk.StringVar()
subtitle_var.set("Instructions: Keep your face straight in front of the camera")
subtitle_label = tk.Label(root, textvariable=subtitle_var, font=("Helvetica", 12), fg="blue")
subtitle_label.pack(pady=5)

# ----------------- Logging Variables ----------------
recently_logged = {}
LOG_COOLDOWN = 5  # seconds

# ----------------- Functions ----------------
def add_new_employee():
    """Capture new employee face"""
    import subprocess
    subprocess.Popen(["python", "add_new_face.py"])

def view_logs():
    """Show recognition logs"""
    try:
        with open("recognized_faces.csv", "r") as f:
            logs = f.read()
        log_window = tk.Toplevel(root)
        log_window.title("Recognition Logs")
        text = tk.Text(log_window, width=80, height=25)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, logs)
    except FileNotFoundError:
        messagebox.showinfo("Logs", "No logs found yet.")

# ----------------- Camera Feed ----------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def update_frame():
    """Update camera frame inside GUI"""
    ret, frame = cap.read()
    if not ret:
        camera_canvas.after(10, update_frame)
        return

    # ----------------- Face Recognition -----------------
    temp_file = "temp_frame.jpg"
    cv2.imwrite(temp_file, frame)
    name = face_recog.recognize_face(temp_file)

    # Log recognized face
    current_time = time.time()
    if name != "Unknown":
        last_logged = recently_logged.get(name, 0)
        if current_time - last_logged > LOG_COOLDOWN:
            logger.log_recognition(name)
            recently_logged[name] = current_time

    # Draw rectangle guide in center
    h, w, _ = frame.shape
    rect_w, rect_h = 250, 300
    top_left = (w//2 - rect_w//2, h//2 - rect_h//2)
    bottom_right = (w//2 + rect_w//2, h//2 + rect_h//2)
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)

    # Draw recognized name
    cv2.putText(frame, name, (top_left[0], top_left[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Convert frame to ImageTk for Tkinter
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    camera_canvas.imgtk = imgtk
    camera_canvas.configure(image=imgtk)

    # Call the function again after 10ms
    camera_canvas.after(10, update_frame)

# ----------------- Buttons ----------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_add = tk.Button(btn_frame, text="Add New Employee", font=("Helvetica", 12), width=20, command=add_new_employee)
btn_add.grid(row=0, column=0, padx=10)

btn_logs = tk.Button(btn_frame, text="View Logs", font=("Helvetica", 12), width=20, command=view_logs)
btn_logs.grid(row=0, column=1, padx=10)

btn_quit = tk.Button(btn_frame, text="Quit", font=("Helvetica", 12), width=20, command=root.destroy)
btn_quit.grid(row=0, column=2, padx=10)

# ----------------- Start Camera Feed ----------------
update_frame()
root.mainloop()

# Release camera
cap.release()
cv2.destroyAllWindows()
