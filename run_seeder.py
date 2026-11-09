from app.infrastructure.database import SessionLocal
from app.infrastructure.seeders.initial_seeder import ejecutar_seeders

if __name__ == "__main__":
    with SessionLocal() as db:
        ejecutar_seeders(db)
