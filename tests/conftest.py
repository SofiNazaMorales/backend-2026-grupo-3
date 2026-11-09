import os
# Base exclusiva de tests, nunca la base real de la persona que ejecuta pytest.
os.environ["DATABASE_URL"] = "sqlite://"
import pytest
from app.infrastructure.database import Base, engine, SessionLocal
from app.infrastructure.models import CarreraModel

@pytest.fixture
def db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        session.add(CarreraModel(id_carrera="ICI-INF",codigo="PLAN-INF",nombre_carrera="Informática",duracion_semestre=10,facultad="Facultad de Ingeniería"))
        session.commit()
        yield session
    Base.metadata.drop_all(engine)
