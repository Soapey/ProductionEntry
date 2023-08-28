import sqlite3
from productionentry.utils import join_to_project_folder, read_config
import os


def default_path():

    config = read_config()

    database_path_value = config.get("sqlite", "path", fallback=str())

    return database_path_value if os.path.exists(database_path_value) else join_to_project_folder(os.path.join("productionentry", "db", "productionentry.db"))


class SQLiteConnector:
    def __init__(self, database_path=None):
        self.database_path = database_path or default_path()
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
