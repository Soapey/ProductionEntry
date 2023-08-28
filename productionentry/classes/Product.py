from productionentry.db.sqlite.Table import Table, Column, ColumnDataType
from productionentry.db.sqlite.SQLiteConnector import SQLiteConnector


class Product:
    def __init__(self, name, gl_code, obj_id=None):
        self.obj_id = obj_id
        self.name = name
        self.gl_code = gl_code

    def __repr__(self):
        attrs = ', '.join([f'{attr}={getattr(self, attr)}' for attr in vars(self)])
        return f'{self.__class__.__name__}({attrs})'

    @classmethod
    def table(cls):
        return Table(
            name='product', columns=[
                Column(name='id', data_type=ColumnDataType.INTEGER, is_primary=True),
                Column(name='name', data_type=ColumnDataType.TEXT, is_unique=True, is_nullable=False),
                Column(name='gl_code', data_type=ColumnDataType.TEXT, is_nullable=False),
            ]
        )

    @classmethod
    def create_table(cls):
        tbl = cls.table()
        tbl.create()

    def save_self(self):
        with SQLiteConnector() as cur:
            if self.obj_id:
                query = "UPDATE product SET name = ?, gl_code = ? WHERE id = ?;"
                parameters = (self.name, self.gl_code, self.obj_id)
                cur.execute(query, parameters)
            else:
                query = "INSERT product site (name, gl_code) VALUES (?, ?);"
                parameters = (self.name, self.gl_code)
                cur.execute(query, parameters)
                self.obj_id = cur.lastrowid

    def delete_self(self):
        with SQLiteConnector() as cur:
            query = "DELETE FROM product WHERE id = ?;"
            parameters = (self.obj_id,)
            cur.execute(query, parameters)

    @classmethod
    def delete(cls, obj_id):
        with SQLiteConnector() as cur:
            query = "DELETE FROM product WHERE id = ?;"
            parameters = (obj_id,)
            cur.execute(query, parameters)

    @classmethod
    def get(cls, obj_id=None):
        with SQLiteConnector() as cur:
            if obj_id:
                query = "SELECT * FROM product WHERE id = ?;"
                parameters = (obj_id,)
                row = cur.execute(query, parameters).fetchone()
                return Product(
                    name=row[1],
                    gl_code=row[2],
                    obj_id=row[0]
                )
            else:
                query = "SELECT * FROM product;"
                cur.execute(query)
                rows = cur.fetchall()
                return {
                    row[0]: Product(
                        name=row[1],
                        gl_code=row[2],
                        obj_id=row[0]
                    )
                    for row in rows
                }
