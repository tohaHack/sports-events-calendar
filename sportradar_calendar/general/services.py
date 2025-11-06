from ..db import get_db
from sqlite3 import IntegrityError

class ItemServiceError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
    def __str__(self):
        return f'ItemServiceError: {super().__str__()}'


class DatabaseManager():
    def __init__(self, table_name: str, nullable_fields: list[str] | None = None) -> None:
        self.table_name = table_name 
        self.nullable_fields = set(nullable_fields) if nullable_fields else set()
    
    def add(self, **kwargs) -> None:
        processed_kwargs: dict = {}

        for key, value in kwargs.items():
            if not value:
                if key in self.nullable_fields:
                    processed_kwargs[key] = None
                else:
                    raise ItemServiceError(f'{key} cannot be empty.')
            else:
                processed_kwargs[key] = value
        db = get_db()
        columns = ', '.join(processed_kwargs.keys())
        placeholders = ', '.join(['?'] * len(processed_kwargs))
        values = tuple(processed_kwargs.values())
        print(f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})')
        try:
            db.execute(
                f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})',
                values
            )
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ItemServiceError(f'Item with values {processed_kwargs} already exists.')

    def delete(self, id: int) -> None:
        if not id:
            raise ItemServiceError('ID is required.')
        db = get_db()
        db.execute(f'DELETE FROM {self.table_name} WHERE {self.table_name}_id = ?', (id,))
        db.commit()
        

    def get_all(self) -> list:
        db = get_db()
        cur = db.execute(f'SELECT * FROM {self.table_name}').fetchall()
        return cur
    
    def get_columns(self) -> list:
        db = get_db()
        columns = db.execute(f'PRAGMA table_info({self.table_name});').fetchall()
        return columns 