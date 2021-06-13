from firebase_admin import credentials
import firebase_admin
import pyrebase


class Config_firebase:
    def __init__(self, path_db, path_auth):
        self.path_db = path_db
        self.path_auth = credentials.Certificate(path_auth)
        firebase_admin.initialize_app(self.path_auth)

    def authentication(self):
        firebase = self.path_db
        pb = pyrebase.initialize_app(firebase).auth()
        return pb

    def database_fb(self):
        firebase = self.path_db
        config = pyrebase.initialize_app(firebase)
        db = config.database()
        return db
