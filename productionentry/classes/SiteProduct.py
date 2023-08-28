from productionentry.db.sqlite.Table import Table, Column, ColumnDataType, ColumnReference, ColumnConstraint
from productionentry.db.sqlite.SQLiteConnector import SQLiteConnector


class SiteProduct:
    def __init__(self, site_id, product_id, obj_id=None):
        self.obj_id = obj_id
        self.site_id = site_id
        self.product_id = product_id

    def __repr__(self):
        attrs = ', '.join([f'{attr}={getattr(self, attr)}' for attr in vars(self)])
        return f'{self.__class__.__name__}({attrs})'

    @classmethod
    def table(cls):
        return Table(
            name='siteproduct', columns=[
                Column(name='id', data_type=ColumnDataType.INTEGER, is_primary=True),
                Column(name='site_id', data_type=ColumnDataType.INTEGER, is_nullable=False, column_reference=ColumnReference(reference_table_name="site", reference_column_name="id", on_delete_constraint=ColumnConstraint.CASCADE)),
                Column(name='product_id', data_type=ColumnDataType.INTEGER, is_nullable=False, column_reference=ColumnReference(reference_table_name="product", reference_column_name="id", on_delete_constraint=ColumnConstraint.CASCADE))
            ]
        )

    @classmethod
    def create_table(cls):
        tbl = cls.table()
        tbl.create()

    def save_self(self):
        with SQLiteConnector() as cur:
            if self.obj_id:
                query = "UPDATE siteproduct SET site_id = ?, product_id = ? WHERE id = ?;"
                parameters = (self.site_id, self.product_id, self.obj_id)
                cur.execute(query, parameters)
            else:
                query = "INSERT INTO siteproduct (site_id, product_id) VALUES (?, ?);"
                parameters = (self.site_id, self.product_id)
                cur.execute(query, parameters)
                self.obj_id = cur.lastrowid

    def delete_self(self):
        with SQLiteConnector() as cur:
            query = "DELETE FROM siteproduct WHERE id = ?;"
            parameters = (self.obj_id,)
            cur.execute(query, parameters)

    @classmethod
    def delete(cls, obj_id):
        with SQLiteConnector() as cur:
            query = "DELETE FROM siteproduct WHERE id = ?;"
            parameters = (obj_id,)
            cur.execute(query, parameters)

    @classmethod
    def get(cls, obj_id=None):
        with SQLiteConnector() as cur:
            if obj_id:
                query = "SELECT * FROM siteproduct WHERE id = ?;"
                parameters = (obj_id,)
                row = cur.execute(query, parameters).fetchone()
                return SiteProduct(
                    site_id=row[1],
                    product_id=row[2],
                    obj_id=row[0]
                )
            else:
                query = "SELECT * FROM siteproduct;"
                cur.execute(query)
                rows = cur.fetchall()
                return {
                    row[0]: SiteProduct(
                        site_id=row[1],
                        product_id=row[2],
                        obj_id=row[0]
                    )
                    for row in rows
                }
