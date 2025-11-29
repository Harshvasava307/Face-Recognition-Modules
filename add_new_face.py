# add_new_face.py

import cv2
import os
from face_recognition_module import FaceRecognitionModule

# Initialize face recognition module
face_recog = FaceRecognitionModule()

# Get new employee name
employee_name = input("Enter your name: ").strip()
if not employee_name:
    print("Name cannot be empty!")
    exit()

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Camera started. Press 'c' to capture your photo or 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # ------------------ UI ------------------
    h, w, _ = frame.shape
    rect_w, rect_h = 250, 300
    top_left = (w//2 - rect_w//2, h//2 - rect_h//2)
    bottom_right = (w//2 + rect_w//2, h//2 + rect_h//2)
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)  # Red rectangle

    # Subtitle instruction
    subtitle = "Keep your face straight in front of the camera and press 'c' to capture"
    text_size = cv2.getTextSize(subtitle, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
    text_x = (w - text_size[0]) // 2
    text_y = h - 20
    cv2.rectangle(frame, (text_x-5, text_y-25), (text_x + text_size[0]+5, text_y+5), (0,0,0), -1)
    cv2.putText(frame, subtitle, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show frame
    cv2.imshow("Add New Face", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        # Capture photo
        save_path = os.path.join(face_recog.database_path, f"{employee_name}.jpg")
        cv2.imwrite(save_path, frame)
        print(f"Photo captured and saved as {save_path}")
        break
    elif key == ord('q'):
        print("Quitting without saving.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
