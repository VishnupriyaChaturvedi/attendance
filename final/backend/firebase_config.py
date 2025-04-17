import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials (make sure the file path is correct)
cred = credentials.Certificate("./backend/serviceAccountKey.json")

# Initialize Firebase
firebase_admin.initialize_app(cred)

# Connect to Firestore database
db = firestore.client()

print("🔥 Firebase Firestore Connected Successfully!")
