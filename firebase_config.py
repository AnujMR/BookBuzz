import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)

def getUserByPass(username, password):
    db = firestore.client()
    
    # Query documents where 'username' is equal to 'anuj'
    doc_ref = db.collection("users").where("username", "==", username).where("password", "==", password)
    
    # Get the documents returned by the query
    documents = doc_ref.get()
    
    # Check if any documents match the conditions
    if documents:
        for document in documents:
            userDoc = document.to_dict()
            userDoc.update({"id" : document.id})
            print('Document data:', userDoc)
            return userDoc
    else:
        print('No such document!')
        return None

def updateUser(uid, body):
    db = firestore.client()
    
    doc_ref = db.collection("users").document(uid)
    
    # Get the documents returned by the query
    document = doc_ref.get()
    print(document.to_dict())
    
    if document:
        document.reference.update(body)
        print("User updated successfully")
        updatedDocRef = db.collection("users").document(uid)
        updatedDocument = updatedDocRef.get()
        userDoc = updatedDocument.to_dict()
        userDoc.update({"id" : updatedDocument.id})
        print('Updated user data:', userDoc)
        return {"status" : True, "user" : userDoc}    
    else:
        print('No such document!')
        return {"status" : False}

def getUserById(uid):
    db = firestore.client()
    doc_ref = db.collection("users").document(uid)
    document = doc_ref.get()
    if document.exists:
        return document.to_dict()
        # print('Document data:', document.to_dict())
    else:
        print('No such document!')

def registerUser(body):
    try:
        db = firestore.client()
        doc_ref = db.collection("users").document()
        doc_ref.set(body)
        userDoc = doc_ref.to_dict()
        userDoc.update({"id" : doc_ref.id})
        print('New user data:', userDoc)
        return {"status" : True, "user" : userDoc}
    except Exception as e:
        print("Exception occured while registering user : ", e)
        return {"status" : False}


