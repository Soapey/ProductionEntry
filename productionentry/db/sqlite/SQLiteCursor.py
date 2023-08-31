import sqlite3
import os
from productionentry.utils import join_to_project_folder


class SQLiteCursor:
    def __init__(self, path=None):
        self.path: str = path or join_to_project_folder(os.path.join("db", "production_entry.db"))
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        print("SQLITE | Connected to path:", self.path)
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
