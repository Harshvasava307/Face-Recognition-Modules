# gui_add_new_face.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
from face_recognition_module import FaceRecognitionModule
from deepface import DeepFace

# ---------------- Initialize ----------------
face_recog = FaceRecognitionModule()
capture_count = 0
MAX_CAPTURE = 3  # number of photos per employee
current_detected_name = "Unknown"

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Add New Employee / Recognition")
root.geometry("750x750")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Employee Registration & Recognition", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Entry for Name
name_label = tk.Label(root, text="Enter Employee Name:", font=("Helvetica", 12))
name_label.pack(pady=5)

name_entry = tk.Entry(root, font=("Helvetica", 12))
name_entry.pack(pady=5)

# Canvas for Camera Feed
camera_canvas = tk.Label(root)
camera_canvas.pack(pady=10)

# Subtitle / Instructions
subtitle_var = tk.StringVar()
subtitle_var.set("Instructions: Keep your face straight in front of the camera")
subtitle_label = tk.Label(root, textvariable=subtitle_var, font=("Helvetica", 12), fg="blue")
subtitle_label.pack(pady=5)

# Status / Feedback
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 12), fg="green")
status_label.pack(pady=5)

# ----------------- Camera ----------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ----------------- Functions ----------------
def capture_image():
    """Capture image(s) for new employee"""
    global capture_count
    employee_name = name_entry.get().strip()
    if employee_name == "":
        messagebox.showwarning("Input Error", "Please enter employee name.")
        return

    # Check if employee already exists
    existing_files = os.listdir(face_recog.database_path)
    for f in existing_files:
        if f.lower().startswith(employee_name.lower() + "_") or f.lower() == employee_name.lower() + ".jpg":
            messagebox.showinfo("Duplicate Entry", f"Employee '{employee_name}' already exists!")
            return

    capture_count += 1
    filename = f"{employee_name}_{capture_count}.jpg"
    save_path = os.path.join(face_recog.database_path, filename)

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(save_path, frame)
        status_var.set(f"Captured {capture_count}/{MAX_CAPTURE} images for {employee_name}")
    else:
        status_var.set("Failed to capture image!")

    if capture_count >= MAX_CAPTURE:
        status_var.set(f"Finished capturing {MAX_CAPTURE} images for {employee_name}")
        capture_count = 0
        name_entry.delete(0, tk.END)
        add_button.pack_forget()  # hide button after done

def update_frame():
    """Update camera feed in GUI and perform face recognition"""
    global current_detected_name
    ret, frame = cap.read()
    if not ret:
        camera_canvas.after(10, update_frame)
        return

    # Draw guide rectangle
    h, w, _ = frame.shape
    rect_w, rect_h = 250, 300
    top_left = (w//2 - rect_w//2, h//2 - rect_h//2)
    bottom_right = (w//2 + rect_w//2, h//2 + rect_h//2)
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)

    # ----------------- Face Recognition ----------------
    temp_file = "temp_frame.jpg"
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    cv2.imwrite(temp_file, small_frame)

    try:
        results = DeepFace.find(img_path=temp_file, db_path=face_recog.database_path, enforce_detection=False)
        if len(results) > 0 and len(results[0]) > 0:
            match_path = results[0].iloc[0]['identity']
            person_name = os.path.splitext(os.path.basename(match_path))[0]
            current_detected_name = person_name
            subtitle_var.set(f"Existing Employee: {person_name}")
            if add_button.winfo_ismapped():
                add_button.pack_forget()  # hide add button if face exists
        else:
            current_detected_name = "Unknown"
            subtitle_var.set("New Employee: Enter Name and Click 'Capture Image'")
            if not add_button.winfo_ismapped():
                add_button.pack(side=tk.LEFT, padx=10)  # show button for new employee
    except:
        current_detected_name = "Unknown"
        subtitle_var.set("New Employee: Enter Name and Click 'Capture Image'")
        if not add_button.winfo_ismapped():
            add_button.pack(side=tk.LEFT, padx=10)

    # Convert frame to ImageTk
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    camera_canvas.imgtk = imgtk
    camera_canvas.configure(image=imgtk)

    camera_canvas.after(10, update_frame)

# ----------------- Buttons ----------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)


# ----------------- Buttons ----------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

add_button = tk.Button(btn_frame, text="Capture Image", font=("Helvetica", 12), width=20, command=capture_image)
# Initially hidden, will appear dynamically in update_frame()

btn_quit = tk.Button(btn_frame, text="Quit", font=("Helvetica", 12), width=20, command=quit)
btn_quit.pack(side=tk.LEFT, padx=10)

# ----------------- Start Camera ----------------
update_frame()
root.mainloop()

# Release camera
cap.release()
cv2.destroyAllWindows()
