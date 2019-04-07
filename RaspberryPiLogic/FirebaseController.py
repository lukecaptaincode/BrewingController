import firebase_admin
from firebase_admin import credentials, db
from random import randint

"""
All firebase interaction logic
"""
class FirebaseController:
    ref = ""

    """
    Init firebase
    """
    def __init__(self):
        cred = credentials.Certificate(
            'iot-apps-project-firebase-adminsdk-vz7fv-51c7726077.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://iot-apps-project.firebaseio.com/'
        })
        self.ref = db.reference('/')

    """
    Post data to firebase
    @param ref - where to post
    @param data - what to post
    """
    def post_to_firebase(self, ref, data):
        self.ref.update({ref: data})
        print('posted to ' + ref)
    """
    Gets and returns data from firebase based on passed ref
    @param ref - where to source the data
    @return - the data
    """
    def get_from_firebase(self, ref):
        getRef = db.reference('/' + ref)
        return getRef.get(ref)

    """
    test-method
    """
    def test_firebase(self):
        self.ref.update({'test': randint(0, 100)})
        self.ref.set({'test': randint(0, 100)})
        print(self.ref.get())
