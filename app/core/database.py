from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker

from app.core.config import settings

import app.models

engine = create_engine(
    settings.database_url,
    echo=True,  # We'll make this configurable later
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


