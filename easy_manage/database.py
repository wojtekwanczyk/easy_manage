from pymongo import MongoClient
URI = "mongodb+srv://easy-manage:admin@easy-manage-t2mek.mongodb.net/test?retryWrites=true"


class DatabaseConnector:
    def __init__(self):
        self.database = MongoClient(URI).get_default_database()
