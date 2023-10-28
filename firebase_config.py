import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)

# Read a document from Firestore
def getAdmin(collection, document_id):
    db = firestore.client()
    doc_ref = db.collection(collection).document(document_id)
    document = doc_ref.get()
    if document.exists:
        return document.to_dict()
        # print('Document data:', document.to_dict())
    else:
        print('No such document!')

