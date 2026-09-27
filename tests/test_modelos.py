from datetime import date

from app.domain.modelos import (
    Carrera,
    Curso,
    Estudiante,
    Justificativo,
    EstadoJustificativo,
    Facultad,
    TipoInasistencia,
)


def test_crear_justificativo():
    justificativo = Justificativo(
        id_justificativo=1,
        rut_estudiante="20.123.554-5",
        id_curso="CRS-INF1108",
        fecha_inasistencia=date(2026, 9, 20),
        tipo_inasistencia=TipoInasistencia.CLASE,
        estado=EstadoJustificativo.PENDIENTE,
    )

    assert justificativo.id_justificativo == 1
    assert justificativo.rut_estudiante == "20.123.554-5"
    assert justificativo.id_curso == "CRS-INF1108"
    assert justificativo.fecha_inasistencia == date(2026, 9, 20)
    assert justificativo.tipo_inasistencia == TipoInasistencia.CLASE
    assert justificativo.estado == EstadoJustificativo.PENDIENTE


def test_tipos_inasistencia():
    assert TipoInasistencia.CLASE.value == "Clase Regular"
    assert TipoInasistencia.EVALUACION.value == "Evaluación"


def test_estados_justificativo():
    assert EstadoJustificativo.PENDIENTE.value == "Pendiente"
    assert EstadoJustificativo.ACEPTADO.value == "Aceptado"
    assert EstadoJustificativo.RECHAZADO.value == "Rechazado"


def test_crear_estudiante():
    estudiante = Estudiante(
        rut_estudiante="20.123.554-5",
        nombre="Roberto",
        apellido="Diaz",
        email_institucional="rdiaz2026@alu.uct.cl",
        id_carrera="ICI-INF",
    )

    assert estudiante.rut_estudiante == "20.123.554-5"
    assert estudiante.nombre == "Roberto"
    assert estudiante.estado_alumno is True


def test_crear_curso():
    curso = Curso(
        id_curso="CRS-INF1108",
        codigo_curso="INF-1108",
        nombre_curso="Desarrollo de Backend",
        semestre=4,
        id_carrera="ICI-INF",
    )

    assert curso.id_curso == "CRS-INF1108"
    assert curso.codigo_curso == "INF-1108"
    assert curso.semestre == 4


def test_crear_carrera():
    carrera = Carrera(
        id_carrera="ICI-INF",
        codigo="PLAN-2023-INF",
        nombre_carrera="Ingenieria Civil Informatica",
        facultad=Facultad.INGENIERIA,
        duracion_semestre=10,
    )

    assert carrera.id_carrera == "ICI-INF"
    assert carrera.facultad == Facultad.INGENIERIA
    assert carrera.duracion_semestre == 10