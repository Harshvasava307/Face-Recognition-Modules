# face_recognition_module.py

import os
from deepface import DeepFace

class FaceRecognitionModule:
    def __init__(self, database_path="faces_database"):
        """
        database_path: Folder containing known face images
                       Each image file name should be the person's name.
                       e.g., faces_database/Harsh.jpg
        """
        self.database_path = database_path
        if not os.path.exists(database_path):
            os.makedirs(database_path)

    def recognize_face(self, image_path):
        """
        Compare the given image with the database and return the person's name.
        If no match is found, return "Unknown".
        """
        if not os.path.exists(image_path):
            print(f"Error: {image_path} does not exist!")
            return "Unknown"

        try:
            results = DeepFace.find(img_path=image_path, db_path=self.database_path, enforce_detection=False)
            if len(results) > 0 and len(results[0]) > 0:
                match_path = results[0].iloc[0]['identity']
                person_name = os.path.splitext(os.path.basename(match_path))[0]
                return person_name
            else:
                return "Unknown"
        except Exception as e:
            print("Face recognition error:", e)
            return "Unknown"

    def add_face_to_database(self, person_name, image_path):
        """
        Save a new face to the database.
        """
        if not os.path.exists(image_path):
            print(f"Error: {image_path} does not exist!")
            return

        ext = os.path.splitext(image_path)[1]
        save_path = os.path.join(self.database_path, f"{person_name}{ext}")
        if os.path.exists(save_path):
            print(f"{person_name} already exists in database, skipping.")
            return

        try:
            with open(image_path, "rb") as f_src:
                with open(save_path, "wb") as f_dst:
                    f_dst.write(f_src.read())
            print(f"Saved {person_name} to database.")
        except Exception as e:
            print("Error saving face:", e)


# ------------------- Dynamic Folder Import -------------------
if __name__ == "__main__":
    # Initialize the face recognition module
    face_recog = FaceRecognitionModule()

    # Automatically add all images from faces_to_add/
    faces_folder = "faces_to_add"
    if os.path.exists(faces_folder):
        for file in os.listdir(faces_folder):
            if file.lower().endswith((".jpg", ".png")):
                person_name = os.path.splitext(file)[0]  # Use file name as person name
                image_path = os.path.join(faces_folder, file)
                face_recog.add_face_to_database(person_name, image_path)
    else:
        print(f"Folder '{faces_folder}' does not exist. Create it and put face images there.")

