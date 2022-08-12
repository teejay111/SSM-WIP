import pyrebase
import string
import random
config = {
    'apiKey': "AIzaSyATF5UzBoZ2ECUoChJuLG-ixn0jetUbLAI",
    'authDomain': "ecommerce-93ad0.firebaseapp.com",
    'databaseURL': "https://ecommerce-93ad0-default-rtdb.firebaseio.com/",
    'storageBucket': "gs://ecommerce-93ad0.appspot.com",
}

firebase = pyrebase.initialize_app(config)
firebaseAuth = firebase.auth()
database = firebase.database()


def isFirebaseAuthenticated(uid):
    try:
        user = firebaseAuth.get_account_info(uid)
        if user is None:
            return None
        else:
            return user['users'][0]
    except:
        return None


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
