from sqlalchemy.orm import Session
from app.service.base_repository import BaseRepository


class BaseSyncRepository(BaseRepository):
    def __init__(self, db: Session):
        self._db = db

    def _flush(self):
        self._db.flush()