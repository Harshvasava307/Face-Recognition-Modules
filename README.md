Face Recognition Software (Python)

A modular Python-based system for real-time face detection, face recognition, logging, and analytics. Designed for quick prototyping and scalable to production.

Features

Real-time face detection using MediaPipe / OpenCV / Dlib

Face recognition with FaceNet / ArcFace / DeepFace

Database support: SQLite / PostgreSQL / MongoDB

GUI for live camera feed using Tkinter / PyQt

Logging & analytics with Pandas + Matplotlib

Required Libraries
pip install opencv-python numpy dlib face_recognition mediapipe Pillow imutils tensorflow keras deepface sqlalchemy psycopg2-binary pymongo pyqt5 pandas matplotlib scikit-learn scipy


tkinter and sqlite3 are usually pre-installed with Python.

Architecture
Camera Input ---> Face Detection ---> Face Recognition ---> Database Storage
      |                   |                     |
      |                   |                     ---> Logging & Analytics
      |                   |
      |                   ---> Draw bounding boxes/landmarks
      |
      ---> GUI Display (Tkinter / PyQt)


Components:

Face Detection: Identify faces in real-time

Face Recognition: Match detected faces with stored embeddings

Database: Store face embeddings, names, timestamps

GUI: Display live camera feed with recognized faces

Analytics: Track recognition statistics, visualize logs

Quick Start
Database (SQLite)
import sqlite3

conn = sqlite3.connect("faces.db")
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    embedding BLOB,
    timestamp TEXT
)
''')
conn.commit()
conn.close()

Face Detection (MediaPipe)
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.7)

while True:
    ret, frame = cap.read()
    if not ret: break
    results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            h, w, _ = frame.shape
            x, y, w_box, h_box = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

Face Recognition (DeepFace)
from deepface import DeepFace

result = DeepFace.find(img_path="captured_face.jpg", db_path="faces_database_folder")
print("Face recognized" if len(result) > 0 else "Unknown face")

GUI (Tkinter)
import tkinter as tk
from PIL import Image, ImageTk
import cv2

root = tk.Tk()
label = tk.Label(root)
label.pack()

cap = cv2.VideoCapture(0)

def show_frame():
    ret, frame = cap.read()
    if ret:
        img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        label.configure(image=img)
        label.imgtk = img
    label.after(10, show_frame)

show_frame()
root.mainloop()

Logging & Analytics
import pandas as pd
from datetime import datetime

df = pd.DataFrame(columns=["name", "timestamp"])
df = pd.concat([df, pd.DataFrame([{"name": "John", "timestamp": datetime.now()}])])
df.to_csv("face_log.csv", index=False)


Plot recognition frequency:

import matplotlib.pyplot as plt
data = pd.read_csv("face_log.csv")
data['name'].value_counts().plot(kind='bar')
plt.show()

Roadmap

Start with one known face and SQLite database

Test real-time detection & recognition

Add multiple faces and logging

Optimize speed (MediaPipe recommended)

Optional: Multi-camera support, web interface, email alerts

Project File Structure
face_recognition_app/
│
├── main.py                # Main program to launch GUI & camera
├── camera_module.py       # Handles camera input & face detection
├── face_recognition_module.py  # Handles face recognition & embedding
├── database_module.py     # Handles database storage & retrieval
├── gui_module.py          # GUI using Tkinter / PyQt
├── logger_module.py       # Logging recognized faces
├── requirements.txt       # List of all Python dependencies
└── faces_database/        # Folder to store known face images (optional)