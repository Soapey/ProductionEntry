from productionentry.db.sqlite.Table import Table, Column, ColumnDataType
from productionentry.db.sqlite.SQLiteConnector import SQLiteConnector


class Site:
    def __init__(self, name, is_simple, obj_id=None):
        self.obj_id = obj_id
        self.name = name
        self.is_simple = is_simple

    def __repr__(self):
        attrs = ', '.join([f'{attr}={getattr(self, attr)}' for attr in vars(self)])
        return f'{self.__class__.__name__}({attrs})'

    @classmethod
    def table(cls):
        return Table(
            name='site', columns=[
                Column(name='id', data_type=ColumnDataType.INTEGER, is_primary=True),
                Column(name='name', data_type=ColumnDataType.TEXT, is_unique=True, is_nullable=False),
                Column(name='is_simple', data_type=ColumnDataType.INTEGER, is_nullable=False),
            ]
        )

    @classmethod
    def create_table(cls):
        tbl = cls.table()
        tbl.create()

    def save_self(self):
        with SQLiteConnector() as cur:
            if self.obj_id:
                query = "UPDATE site SET name = ?, is_simple = ? WHERE id = ?;"
                parameters = (self.name, self.is_simple, self.obj_id)
                cur.execute(query, parameters)
            else:
                query = "INSERT INTO site (name, is_simple) VALUES (?, ?);"
                parameters = (self.name, self.is_simple)
                cur.execute(query, parameters)
                self.obj_id = cur.lastrowid

    def delete_self(self):
        with SQLiteConnector() as cur:
            query = "DELETE FROM site WHERE id = ?;"
            parameters = (self.obj_id,)
            cur.execute(query, parameters)

    @classmethod
    def delete(cls, obj_id):
        with SQLiteConnector() as cur:
            query = "DELETE FROM site WHERE id = ?;"
            parameters = (obj_id,)
            cur.execute(query, parameters)

    @classmethod
    def get(cls, obj_id=None):
        with SQLiteConnector() as cur:
            if obj_id:
                query = "SELECT * FROM site WHERE id = ?;"
                parameters = (obj_id,)
                row = cur.execute(query, parameters).fetchone()
                return Site(
                    name=row[1],
                    is_simple=row[2],
                    obj_id=row[0]
                )
            else:
                query = "SELECT * FROM site;"
                cur.execute(query)
                rows = cur.fetchall()
                return {
                    row[0]: Site(
                        name=row[1],
                        is_simple=row[2],
                        obj_id=row[0]
                    )
                    for row in rows
                }
