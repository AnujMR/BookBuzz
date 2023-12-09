import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)

# Read a document from Firestore
def getUserByPass(username, password):
    db = firestore.client()
    
    # Query documents where 'username' is equal to 'anuj'
    doc_ref = db.collection("users").where("username", "==", username).where("password", "==", password)
    
    # Get the documents returned by the query
    documents = doc_ref.get()
    
    # Check if any documents match the conditions
    if documents:
        for document in documents:
            print('Document data:', document.to_dict())
            return document.to_dict()
    else:
        print('No such document!')
        return None

# Read a document from Firestore
def getUserById(uid):
    db = firestore.client()
    doc_ref = db.collection("users").document(uid)
    document = doc_ref.get()
    if document.exists:
        return document.to_dict()
        # print('Document data:', document.to_dict())
    else:
        print('No such document!')

