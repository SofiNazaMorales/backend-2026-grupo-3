import pytest
from pydantic import ValidationError

from app.domain.modelos import Facultad
from app.schemas.carrera import CarreraCreate


def test_crear_carrera_valida():
    carrera = CarreraCreate(
        id_carrera="ICI-INF",
        codigo="PLAN-2023-INF",
        nombre_carrera="Ingenieria Civil Informatica",
        facultad=Facultad.INGENIERIA,
        duracion_semestre=10
    )

    assert carrera.id_carrera == "ICI-INF"
    assert carrera.codigo == "PLAN-2023-INF"
    assert carrera.nombre_carrera == "Ingenieria Civil Informatica"
    assert carrera.facultad == Facultad.INGENIERIA
    assert carrera.duracion_semestre == 10


def test_rechazar_id_carrera_muy_corto():
    with pytest.raises(ValidationError):
        CarreraCreate(
            id_carrera="I",
            codigo="PLAN-2023-INF",
            nombre_carrera="Ingenieria Civil Informatica",
            facultad=Facultad.INGENIERIA,
            duracion_semestre=10
        )


def test_rechazar_codigo_muy_corto():
    with pytest.raises(ValidationError):
        CarreraCreate(
            id_carrera="ICI-INF",
            codigo="123",
            nombre_carrera="Ingenieria Civil Informatica",
            facultad=Facultad.INGENIERIA,
            duracion_semestre=10
        )


def test_rechazar_nombre_muy_corto():
    with pytest.raises(ValidationError):
        CarreraCreate(
            id_carrera="ICI-INF",
            codigo="PLAN-2023-INF",
            nombre_carrera="IC",
            facultad=Facultad.INGENIERIA,
            duracion_semestre=10
        )


def test_rechazar_duracion_cero():
    with pytest.raises(ValidationError):
        CarreraCreate(
            id_carrera="ICI-INF",
            codigo="PLAN-2023-INF",
            nombre_carrera="Ingenieria Civil Informatica",
            facultad=Facultad.INGENIERIA,
            duracion_semestre=0
        )


def test_rechazar_duracion_mayor_a_14():
    with pytest.raises(ValidationError):
        CarreraCreate(
            id_carrera="ICI-INF",
            codigo="PLAN-2023-INF",
            nombre_carrera="Ingenieria Civil Informatica",
            facultad=Facultad.INGENIERIA,
            duracion_semestre=15
        )


def test_rechazar_facultad_invalida():
    with pytest.raises(ValidationError):
        CarreraCreate(
            id_carrera="ICI-INF",
            codigo="PLAN-2023-INF",
            nombre_carrera="Ingenieria Civil Informatica",
            facultad="Facultad Inventada",
            duracion_semestre=10
        )