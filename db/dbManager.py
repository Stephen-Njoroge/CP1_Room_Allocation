import sqlite3 as lite


class DbManager:
    """Initialize a db connection with sqlite3"""
    def __init__(self):
        db_name = "amity.db"
        self.connection = lite.connect(db_name)
        self.cursor = self.connection.cursor()
        self.migrations()
     