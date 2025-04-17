import cv2
import numpy as np
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Remove "./backend/"
firebase_admin.initialize_app(cred)
db = firestore.client()

# Create a folder for storing known faces
KNOWN_FACES_DIR = "./backend/known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# Load images and encode faces
def encode_faces():
    known_faces = []
    known_names = []

    for filename in os.listdir(KNOWN_FACES_DIR):
        img_path = os.path.join(KNOWN_FACES_DIR, filename)
        img = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(img)

        if len(encoding) > 0:
            known_faces.append(encoding[0])
            known_names.append(os.path.splitext(filename)[0])

    return known_faces, known_names

# Capture new face and save it
def capture_face(student_name):
    cap = cv2.VideoCapture(0)
    print("Press 'C' to capture your face...")

    while True:
        ret, frame = cap.read()
        cv2.imshow("Capture Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            img_path = os.path.join(KNOWN_FACES_DIR, f"{student_name}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"✅ Face saved as {img_path}")
            break

    cap.release()
    cv2.destroyAllWindows()

# Recognize faces and mark attendance
def recognize_faces():
    known_faces, known_names = encode_faces()

    cap = cv2.VideoCapture(0)
    print("Scanning for faces... Press 'Q' to quit")

    while True:
        ret, frame = cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.5)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

                # Mark attendance in Firebase
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.collection("attendance").add({
                    "name": name,
                    "timestamp": timestamp
                })
                print(f"✅ Attendance marked for {name} at {timestamp}")

                # Draw rectangle around recognized face
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
