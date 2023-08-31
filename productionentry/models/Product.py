import sqlite3

from productionentry.db.sqlite.SQLiteCursor import SQLiteCursor


class Product:
    def __init__(self, name: str, obj_id: int = None):
        self.obj_id = obj_id
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        class_name = self.__class__.__name__
        attrs = ', '.join(f'{attr}={value}' for attr, value in vars(self).items())
        return f"{class_name}({attrs})"

    def save(self):
        if self.obj_id:
            # Update
            with SQLiteCursor() as cur:
                query = "UPDATE product SET name = ? WHERE id = ?"
                params = (self.name, self.obj_id)
                cur.execute(query, params)
        else:
            # Insert
            with SQLiteCursor() as cur:
                query = "INSERT INTO product (name) VALUES (?)"
                params = (self.name,)
                cur.execute(query, params)
                self.obj_id = cur.lastrowid

    def delete(self):
        with SQLiteCursor() as cur:
            query = "DELETE FROM product WHERE id = ?"
            params = (self.obj_id,)
            cur.execute(query, params)

    @classmethod
    def delete_by_id(cls, obj_id: int):
        with SQLiteCursor() as cur:
            query = "DELETE FROM product WHERE id = ?"
            params = (obj_id,)
            cur.execute(query, params)

    @classmethod
    def get(cls, obj_id: int = None):
        if obj_id:
            # Fetch one
            with SQLiteCursor() as cur:
                query = "SELECT id, name FROM product WHERE id = ?"
                params = (obj_id,)
                cur.execute(query, params)
                row = cur.fetchone()
                return Product(name=row[1], obj_id=row[0])
        else:
            # Fetch all
            with SQLiteCursor() as cur:
                query = "SELECT id, name FROM product"
                cur.execute(query)
                rows = cur.fetchall()
                return {row[0]: Product(name=row[1], obj_id=row[0]) for row in rows}

    @classmethod
    def create_table(cls):
        with SQLiteCursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
            """)
            print("SQLITE | Table product initialised.")
