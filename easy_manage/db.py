from pymongo import MongoClient
uri = "mongodb+srv://easy-manage:admin@easy-manage-t2mek.mongodb.net/test?retryWrites=true"


class DatabaseConnector:
    def __init__(self):
        self.db = MongoClient(uri).get_default_database()

