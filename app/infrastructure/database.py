import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, false
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

url = URL.create(
    "postgresql+psycopg2",
    username=os.environ.get("DB_USER", "alumno"),
    password=os.environ.get("DB_PASSWORD", "mi_clave_segura"),
    host=os.environ.get("DB_HOST", "localhost"),
    port=int(os.environ.get("DB_PORT", 5432)),
    database=os.environ.get("DB_NAME", "clase"),
)

engine = create_engine(url, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()