import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# List documents in 'users' collection
docs = db.collection("users").list_documents()
print(list(docs))  # should print document references
