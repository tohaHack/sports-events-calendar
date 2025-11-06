from ..general.services import DatabaseManager
from ..db import get_db


class DatabaseManagerEvent(DatabaseManager):
    def __init__(self):
        super().__init__("event", nullable_fields=['description'])

    def get_all_ordered(self) -> list:
        db = get_db()
        return db.execute(
            f"SELECT * FROM {self.table_name} ORDER BY event_date DESC"
        ).fetchall()

    def get_filtered(self, sport_id=None, date_from=None, date_to=None):
        db = get_db()
        where = []
        params = {}
        if sport_id:
            where.append(" _sport_id = :sport_id ")
            params["sport_id"] = sport_id
        if date_from:
            where.append(" event_date >= :date_from ")
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to if "T" in date_to else f"{date_to}T23:59"
            where.append(" event_date <= :date_to ")

        sql = f"SELECT * FROM {self.table_name}"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY event_date DESC"
        return db.execute(sql, params).fetchall()


manager = DatabaseManagerEvent()
