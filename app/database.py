from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL format: postgresql://username:password@host:port/database_name
# local throw away db
DEFAULT_DATABASE_URL = "postgresql://postgres:7702@localhost:5432/finances_tracker"

engine = create_engine(DEFAULT_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
