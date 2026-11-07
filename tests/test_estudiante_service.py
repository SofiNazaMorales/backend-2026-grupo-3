
import pytest

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.domain.enums import Facultad
from app.infrastructure.database import Base
from app.infrastructure.models import CarreraModel
from app.schemas.estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
)
from app.schemas.estudiante_query_dto import EstudianteQueryDTO
from app.services.estudiante_service import EstudianteService


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
        nombre_carrera="Ingenieria Civil Informatica",
        duracion_semestre=10,
        facultad=Facultad.INGENIERIA.value,
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
    return EstudianteService(db_session)


def crear_datos_estudiante(
    rut="21.234.567-8",
    nombre="Carlos",
    apellido="Perez",
    email="carlos@alu.uct.cl",
    carrera="ICI-INF",
):
    return EstudianteCreateDTO(
        rut_estudiante=rut,
        nombre=nombre,
        apellido=apellido,
        email_institucional=email,
        id_carrera=carrera,
    )


def test_crear_estudiante_correctamente(servicio):
    datos = crear_datos_estudiante()

    estudiante = servicio.crear_estudiante(datos)

    assert estudiante.rut_estudiante == "21.234.567-8"
    assert estudiante.nombre == "Carlos"
    assert estudiante.email_institucional == "carlos@alu.uct.cl"


def test_rechazar_rut_duplicado(servicio):
    servicio.crear_estudiante(crear_datos_estudiante())

    duplicado = crear_datos_estudiante(
        email="otro@alu.uct.cl"
    )

    with pytest.raises(HTTPException) as error:
        servicio.crear_estudiante(duplicado)

    assert error.value.status_code == 409


def test_rechazar_email_duplicado(servicio):
    servicio.crear_estudiante(crear_datos_estudiante())

    duplicado = crear_datos_estudiante(
        rut="22.345.678-9"
    )

    with pytest.raises(HTTPException) as error:
        servicio.crear_estudiante(duplicado)

    assert error.value.status_code == 409


def test_rechazar_carrera_inexistente(servicio):
    datos = crear_datos_estudiante(
        carrera="CARRERA-NO"
    )

    with pytest.raises(HTTPException) as error:
        servicio.crear_estudiante(datos)

    assert error.value.status_code == 404


def test_estudiante_inexistente_devuelve_http_404(servicio):
    with pytest.raises(HTTPException) as error:
        servicio.obtener_estudiante("99.999.999-9")

    assert error.value.status_code == 404


def test_actualizar_estudiante_correctamente(servicio):
    servicio.crear_estudiante(crear_datos_estudiante())

    cambios = EstudianteUpdateDTO(
        nombre="Pedro",
        apellido="Gonzalez",
    )

    actualizado = servicio.actualizar_estudiante(
        "21.234.567-8",
        cambios,
    )

    assert actualizado.nombre == "Pedro"
    assert actualizado.apellido == "Gonzalez"


def test_rechazar_email_duplicado_al_actualizar(servicio):
    servicio.crear_estudiante(crear_datos_estudiante())

    segundo = crear_datos_estudiante(
        rut="22.345.678-9",
        email="segundo@alu.uct.cl",
    )

    servicio.crear_estudiante(segundo)

    cambios = EstudianteUpdateDTO(
        email_institucional="carlos@alu.uct.cl"
    )

    with pytest.raises(HTTPException) as error:
        servicio.actualizar_estudiante(
            "22.345.678-9",
            cambios,
        )

    assert error.value.status_code == 409


def test_rechazar_eliminacion_con_justificativos(
    servicio,
    monkeypatch,
):
    servicio.crear_estudiante(crear_datos_estudiante())

    monkeypatch.setattr(
        servicio.justificativo_repository,
        "existen_por_estudiante",
        lambda rut: True,
    )

    with pytest.raises(HTTPException) as error:
        servicio.eliminar_estudiante("21.234.567-8")

    assert error.value.status_code == 409


def test_eliminar_estudiante_correctamente(servicio):
    servicio.crear_estudiante(crear_datos_estudiante())

    resultado = servicio.eliminar_estudiante(
        "21.234.567-8"
    )

    assert resultado["rut_estudiante"] == "21.234.567-8"

    with pytest.raises(HTTPException) as error:
        servicio.obtener_estudiante("21.234.567-8")

    assert error.value.status_code == 404


def test_filtrar_estudiantes_por_estado(servicio):
    servicio.crear_estudiante(crear_datos_estudiante())

    segundo = crear_datos_estudiante(
        rut="22.345.678-9",
        email="segundo@alu.uct.cl",
    )

    servicio.crear_estudiante(segundo)

    cambios = EstudianteUpdateDTO(
        estado_alumno=False
    )

    servicio.actualizar_estudiante(
        "22.345.678-9",
        cambios,
    )

    filtros = EstudianteQueryDTO(
        estado_alumno=False,
        pagina=1,
        limite=10,
    )

    resultado = servicio.listar_estudiantes(filtros)

    assert resultado.total == 1
    assert resultado.items[0].rut_estudiante == "22.345.678-9"
    assert resultado.items[0].estado_alumno is False


def test_listar_estudiantes_con_paginacion(servicio):
    servicio.crear_estudiante(crear_datos_estudiante())

    servicio.crear_estudiante(
        crear_datos_estudiante(
            rut="22.345.678-9",
            email="segundo@alu.uct.cl",
        )
    )

    servicio.crear_estudiante(
        crear_datos_estudiante(
            rut="23.456.789-K",
            email="tercero@alu.uct.cl",
        )
    )

    filtros = EstudianteQueryDTO(
        pagina=2,
        limite=2,
    )

    resultado = servicio.listar_estudiantes(filtros)

    assert resultado.total == 3
    assert len(resultado.items) == 1
    assert resultado.pagina == 2
    assert resultado.limite == 2
    assert resultado.total_paginas == 2
