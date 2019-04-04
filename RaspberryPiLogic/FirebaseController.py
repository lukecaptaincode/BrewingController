import firebase_admin
from firebase_admin import credentials, db
from random import randint


class FirebaseController:

    """
    Init firebase
    """
    def __init__(self):
        cred = credentials.Certificate(
            'iot-apps-project-firebase-adminsdk-vz7fv-51c7726077.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://iot-apps-project.firebaseio.com/'
        })
    """
    test-method
    """
    def test_firebase(self):
        ref = db.reference('/')
        ref.update({'test': randint(0, 100)})
        ref.set({'test': randint(0, 100)})
        print(ref.get())
