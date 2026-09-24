import pytest
from pydantic import ValidationError

from app.schemas.estudiante import EstudianteCreate


def test_crear_estudiante_valido():
    estudiante = EstudianteCreate(
        rut_estudiante="20.123.554-5",
        nombre="Roberto",
        apellido="Diaz",
        email_institucional="rdiaz2026@alu.uct.cl",
        id_carrera="ICI-INF"
    )

    assert estudiante.rut_estudiante == "20.123.554-5"
    assert estudiante.nombre == "Roberto"
    assert estudiante.apellido == "Diaz"
    assert estudiante.email_institucional == "rdiaz2026@alu.uct.cl"
    assert estudiante.id_carrera == "ICI-INF"


def test_formatear_rut_sin_puntos():
    estudiante = EstudianteCreate(
        rut_estudiante="20123554-5",
        nombre="Roberto",
        apellido="Diaz",
        email_institucional="rdiaz2026@alu.uct.cl",
        id_carrera="ICI-INF"
    )

    assert estudiante.rut_estudiante == "20.123.554-5"


def test_rechazar_rut_sin_guion():
    with pytest.raises(ValidationError):
        EstudianteCreate(
            rut_estudiante="201235545",
            nombre="Roberto",
            apellido="Diaz",
            email_institucional="rdiaz2026@alu.uct.cl",
            id_carrera="ICI-INF"
        )


def test_rechazar_rut_con_dv_invalido():
    with pytest.raises(ValidationError):
        EstudianteCreate(
            rut_estudiante="20.123.554-X",
            nombre="Roberto",
            apellido="Diaz",
            email_institucional="rdiaz2026@alu.uct.cl",
            id_carrera="ICI-INF"
        )


def test_rechazar_email_invalido():
    with pytest.raises(ValidationError):
        EstudianteCreate(
            rut_estudiante="20.123.554-5",
            nombre="Roberto",
            apellido="Diaz",
            email_institucional="correo-invalido",
            id_carrera="ICI-INF"
        )


def test_rechazar_nombre_muy_corto():
    with pytest.raises(ValidationError):
        EstudianteCreate(
            rut_estudiante="20.123.554-5",
            nombre="R",
            apellido="Diaz",
            email_institucional="rdiaz2026@alu.uct.cl",
            id_carrera="ICI-INF"
        )