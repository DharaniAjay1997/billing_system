from typing import Any

from sqlalchemy.orm import Session


class BaseService:

    def __init__(self, db: Session):
        self.db = db

    def commit(self) -> None:
        """
        Commit the current transaction.
        Rolls back automatically if commit fails.
        """
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def rollback(self) -> None:
        """
        Rollback the current transaction.
        """
        self.db.rollback()

    def refresh(self, instance: Any) -> None:
        """
        Refresh an instance from the database.
        """
        self.db.refresh(instance)

    def add(self, instance: Any) -> None:
        """
        Add an entity to the current session.
        """
        self.db.add(instance)

    def delete(self, instance: Any) -> None:
        """
        Delete an entity from the current session.
        """
        self.db.delete(instance)

    def flush(self) -> None:
        """
        Flush pending SQL statements without committing.
        """
        self.db.flush()