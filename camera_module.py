# camera_module_ui.py

import cv2
from face_recognition_module import FaceRecognitionModule
from database_module import FaceDatabaseLogger
import time

# Initialize face recognition and logger
face_recog = FaceRecognitionModule()
logger = FaceDatabaseLogger()

# To avoid repeated logging for the same face within a few seconds
recently_logged = {}
LOG_COOLDOWN = 5  # seconds

# Open webcam
cap = cv2.VideoCapture(0)  # 0 is default camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Camera started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Save frame temporarily to recognize
    temp_file = "temp_frame.jpg"
    cv2.imwrite(temp_file, frame)

    # Recognize face
    name = face_recog.recognize_face(temp_file)

    # ------------------ UI Improvements ------------------
    # Draw a rectangle in the center as guide
    h, w, _ = frame.shape
    rect_w, rect_h = 250, 300
    top_left = (w//2 - rect_w//2, h//2 - rect_h//2)
    bottom_right = (w//2 + rect_w//2, h//2 + rect_h//2)
    cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)

    # Display name above the rectangle
    cv2.putText(frame, name, (top_left[0], top_left[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Add subtitle/message at bottom
    subtitle = "Keep your face straight in front of the camera"
    text_size = cv2.getTextSize(subtitle, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    text_x = (w - text_size[0]) // 2
    text_y = h - 20
    # Draw background rectangle for better readability
    cv2.rectangle(frame, (text_x-5, text_y-25), (text_x + text_size[0]+5, text_y+5), (0,0,0), -1)
    cv2.putText(frame, subtitle, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Log face if not logged recently
    current_time = time.time()
    if name != "Unknown":
        last_logged = recently_logged.get(name, 0)
        if current_time - last_logged > LOG_COOLDOWN:
            logger.log_recognition(name)
            recently_logged[name] = current_time

    # Show frame
    cv2.imshow("Face Recognition", frame)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
