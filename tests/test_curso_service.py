import pytest
from app.domain.errores import ErrorAplicacion

from app.repositories.curso_repository import CursoRepository
from app.schemas.curso_dto import CursoCreateDTO as CursoCreate, CursoUpdateDTO as CursoUpdate
from app.services.curso_service import CursoService


def crear_servicio(db):
    repository = CursoRepository(db)
    return CursoService(repository)


def crear_curso_prueba(servicio):
    datos = CursoCreate(
        id_curso="CRS-INF1108",
        codigo_curso="INF-1108",
        nombre_curso="Desarrollo de Backend",
        semestre=4,
        id_carrera="ICI-INF"
    )
    return servicio.crear_curso(datos)


def test_crear_curso_correctamente(db):
    servicio = crear_servicio(db)

    curso = crear_curso_prueba(servicio)

    assert curso.id_curso == "CRS-INF1108"
    assert curso.codigo_curso == "INF-1108"


def test_rechazar_id_duplicado_con_http_409(db):
    servicio = crear_servicio(db)
    crear_curso_prueba(servicio)

    duplicado = CursoCreate(
        id_curso="CRS-INF1108",
        codigo_curso="OTRO-001",
        nombre_curso="Otro Curso",
        semestre=5,
        id_carrera="ICI-INF"
    )

    with pytest.raises(ErrorAplicacion) as error:
        servicio.crear_curso(duplicado)

    assert error.value.status_code == 409
    assert "Ya existe un curso" in error.value.detail


def test_rechazar_codigo_duplicado_con_http_409(db):
    servicio = crear_servicio(db)
    crear_curso_prueba(servicio)

    duplicado = CursoCreate(
        id_curso="CRS-OTRO",
        codigo_curso="INF-1108",
        nombre_curso="Otro Curso",
        semestre=5,
        id_carrera="ICI-INF"
    )

    with pytest.raises(ErrorAplicacion) as error:
        servicio.crear_curso(duplicado)

    assert error.value.status_code == 409
    assert "Ya existe un curso" in error.value.detail


def test_curso_inexistente_devuelve_http_404(db):
    servicio = crear_servicio(db)

    with pytest.raises(ErrorAplicacion) as error:
        servicio.obtener_curso("CRS-NO-EXISTE")

    assert error.value.status_code == 404
    assert "No existe un curso" in error.value.detail


def test_rechazar_codigo_duplicado_al_actualizar(db):
    servicio = crear_servicio(db)

    crear_curso_prueba(servicio)

    segundo = CursoCreate(
        id_curso="CRS-INF2200",
        codigo_curso="INF-2200",
        nombre_curso="Segundo Curso",
        semestre=5,
        id_carrera="ICI-INF"
    )
    servicio.crear_curso(segundo)

    actualizacion = CursoUpdate(
        codigo_curso="INF-1108"
    )

    with pytest.raises(ErrorAplicacion) as error:
        servicio.actualizar_curso(
            "CRS-INF2200",
            actualizacion
        )

    assert error.value.status_code == 409