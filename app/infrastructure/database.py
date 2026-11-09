import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

load_dotenv()
url = os.getenv("DATABASE_URL") or URL.create(
    "postgresql+psycopg2", username=os.getenv("DB_USER", "alumno"),
    password=os.getenv("DB_PASSWORD", "mi_clave_segura"),
    host=os.getenv("DB_HOST", "localhost"), port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "clase"),
)
options = {}
if str(url).startswith("sqlite"):
    options["connect_args"] = {"check_same_thread": False}
    if str(url) in {"sqlite://", "sqlite:///:memory:"}:
        options["poolclass"] = StaticPool
engine = create_engine(url, **options)
if engine.dialect.name == "sqlite":
    @event.listens_for(engine, "connect")
    def activar_claves_foraneas(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")

SessionLocal = sessionmaker(bind=engine, autoflush=False)
class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        try:
            yield db
        except Exception:
            db.rollback()
            raise
