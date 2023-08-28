from enum import Enum
from productionentry.db.sqlite.SQLiteConnector import SQLiteConnector


class ColumnDataType(Enum):
    INTEGER = "INTEGER"
    REAL = "REAL"
    TEXT = "TEXT"
    BLOB = "BLOB"
    NUMERIC = "NUMERIC"


class ColumnConstraint(Enum):
    NONE = None
    CASCADE = "CASCADE"
    RESTRICT = "RESTRICT"


class ColumnReference:
    def __init__(self, reference_table_name: str, reference_column_name: str,
                 on_delete_constraint: ColumnConstraint = ColumnConstraint.NONE,
                 on_update_constraint: ColumnConstraint = ColumnConstraint.NONE):
        self.reference_table_name = reference_table_name
        self.reference_column_name = reference_column_name
        self.on_delete_constraint = on_delete_constraint
        self.on_update_constraint = on_update_constraint


class Column:
    def __init__(self, name: str, data_type: ColumnDataType, is_primary: bool = False, is_unique: bool = False,
                 is_nullable: bool = False, column_reference: ColumnReference = None):
        self.name = name
        self.data_type = data_type
        self.is_primary = is_primary
        self.is_unique = is_unique
        self.is_nullable = is_nullable
        self.column_reference = column_reference

    def get_string(self):
        sections = [self.name, self.data_type.value]
        sections.append("UNIQUE") if self.is_unique else None
        sections.append("NOT NULL") if not self.is_nullable else None
        sections.append("PRIMARY KEY AUTOINCREMENT") if self.is_primary else None
        return ' '.join(sections)


class Table:
    def __init__(self, name: str, columns: list[Column]):
        self.name = name
        self.columns = columns

    def create(self):
        cols = list()
        references = list()

        for col in self.columns:
            cols.append(col.get_string())
            if col.column_reference:
                ref = col.column_reference
                ref_base = f'FOREIGN KEY ({col.name}) REFERENCES {ref.reference_table_name}({ref.reference_column_name})'
                ref_on_delete = f"ON DELETE {ref.on_delete_constraint.value}" if ref.on_delete_constraint != ColumnConstraint.NONE else str()
                ref_on_update = f"ON UPDATE {ref.on_update_constraint.value}" if ref.on_update_constraint != ColumnConstraint.NONE else str()
                references.append(
                    " ".join([ref_base, ref_on_delete, ref_on_update])
                )

        cols_string = ', '.join(cols + references)

        query = f"CREATE TABLE IF NOT EXISTS {self.name} ({cols_string});"

        with SQLiteConnector() as cur:
            cur.execute(query)
