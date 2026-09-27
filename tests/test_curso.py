import pytest
from pydantic import ValidationError

from app.schemas.curso import CursoCreate


def test_crear_curso_valido():
    curso = CursoCreate(
        id_curso="CRS-INF1108",
        codigo_curso="INF-1108",
        nombre_curso="Desarrollo de Backend",
        semestre=4,
        id_carrera="ICI-INF"
    )

    assert curso.id_curso == "CRS-INF1108"
    assert curso.codigo_curso == "INF-1108"
    assert curso.nombre_curso == "Desarrollo de Backend"
    assert curso.semestre == 4
    assert curso.id_carrera == "ICI-INF"


def test_normalizar_id_curso():
    curso = CursoCreate(
        id_curso="crs-inf1108",
        codigo_curso="INF-1108",
        nombre_curso="Desarrollo de Backend",
        semestre=4,
        id_carrera="ICI-INF"
    )

    assert curso.id_curso == "CRS-INF1108"


def test_rechazar_semestre_cero():
    with pytest.raises(ValidationError):
        CursoCreate(
            id_curso="CRS-TEST",
            codigo_curso="TEST-001",
            nombre_curso="Curso prueba",
            semestre=0,
            id_carrera="ICI-INF"
        )


def test_rechazar_semestre_negativo():
    with pytest.raises(ValidationError):
        CursoCreate(
            id_curso="CRS-TEST",
            codigo_curso="TEST-001",
            nombre_curso="Curso prueba",
            semestre=-1,
            id_carrera="ICI-INF"
        )