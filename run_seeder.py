from app.infrastructure.database import SessionLocal
from app.infrastructure.seeders.initial_seeder import ejecutar_seeders

if __name__ == "__main__":
    print("Conectando a la base de datos...")
    db = SessionLocal()
    try:
        ejecutar_seeders(db)
    except Exception as e:
        print(f"Error al ejecutar los seeders: {e}")
    finally:
        db.close()