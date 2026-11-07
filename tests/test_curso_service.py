
import pytest

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.database import Base
from app.infrastructure.models import (
    CarreraModel,
    CursoModel,
    EstudianteModel,
    JustificativoModel,
)
from app.repositories.curso_repository import CursoRepository
from app.schemas.curso_dto import CursoCreateDTO, CursoUpdateDTO
from app.services.curso_service import CursoService


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    db = TestingSessionLocal()

    carrera = CarreraModel(
        id_carrera="ICI-INF",
        codigo="PLAN-2023-INF",
        nombre_carrera="Ingeniería Civil Informática",
        duracion_semestre=10,
        facultad="Ingeniería",
    )

    db.add(carrera)
    db.commit()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def servicio(db_session):
    repository = CursoRepository(db_session)
    return CursoService(repository)


def crear_curso_prueba(servicio):
    datos = CursoCreateDTO(
        id_curso="CRS-INF1108",
        codigo_curso="INF-1108",
        nombre_curso="Desarrollo de Backend",
        semestre=4,
        id_carrera="ICI-INF",
    )

    return servicio.crear_curso(datos)


def test_crear_curso_correctamente(servicio):
    curso = crear_curso_prueba(servicio)

    assert curso.id_curso == "CRS-INF1108"
    assert curso.codigo_curso == "INF-1108"


def test_rechazar_id_duplicado_con_http_400(servicio):
    crear_curso_prueba(servicio)

    duplicado = CursoCreateDTO(
        id_curso="CRS-INF1108",
        codigo_curso="OTRO-001",
        nombre_curso="Otro Curso",
        semestre=5,
        id_carrera="ICI-INF",
    )

    with pytest.raises(HTTPException) as error:
        servicio.crear_curso(duplicado)

    assert error.value.status_code == 400
    assert "Ya existe un curso" in error.value.detail


def test_rechazar_codigo_duplicado_con_http_400(servicio):
    crear_curso_prueba(servicio)

    duplicado = CursoCreateDTO(
        id_curso="CRS-OTRO",
        codigo_curso="INF-1108",
        nombre_curso="Otro Curso",
        semestre=5,
        id_carrera="ICI-INF",
    )

    with pytest.raises(HTTPException) as error:
        servicio.crear_curso(duplicado)

    assert error.value.status_code == 400
    assert "Ya existe un curso" in error.value.detail


def test_curso_inexistente_devuelve_http_404(servicio):
    with pytest.raises(HTTPException) as error:
        servicio.obtener_curso("CRS-NO-EXISTE")

    assert error.value.status_code == 404
    assert "No existe un curso" in error.value.detail


def test_rechazar_codigo_duplicado_al_actualizar(servicio):
    crear_curso_prueba(servicio)

    segundo = CursoCreateDTO(
        id_curso="CRS-INF2200",
        codigo_curso="INF-2200",
        nombre_curso="Segundo Curso",
        semestre=5,
        id_carrera="ICI-INF",
    )

    servicio.crear_curso(segundo)

    actualizacion = CursoUpdateDTO(
        codigo_curso="INF-1108"
    )

    with pytest.raises(HTTPException) as error:
        servicio.actualizar_curso(
            "CRS-INF2200",
            actualizacion,
        )

    assert error.value.status_code == 400
