
from app.infrastructure.database import SessionLocal
from app.infrastructure.seeders.initial_seeder import ejecutar_seeders


if __name__ == "__main__":
    print("Conectando a la base de datos...")

    db = SessionLocal()

    try:
        with db.begin():
            ejecutar_seeders(db)

        print("Seeder ejecutado correctamente.")

    except Exception as e:
        print(f"Error al ejecutar los seeders: {e}")
        raise

    finally:
        db.close()
        print("Conexión a la base de datos cerrada.")
