# src/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base

SQLALCHEMY_DATABASE_URL = 'postgresql://neondb_owner:npg_pj6nZqvVfdG4@ep-odd-math-adtyawv1-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
