from datetime import date
from . import (
    Carrera,
    Curso,
    Estudiante,
    Justificativo,
    EstadoJustificativo,
    TipoInasistencia,
    Facultad,
)

# 1. Semillas para Carreras
CARRERAS_MOCK: list[Carrera] = [
    Carrera(
        id_carrera="ICI-INF",
        codigo="PLAN-2023-INF",
        nombre_carrera="Ingeniería Civil Informatica",
        facultad=Facultad.INGENIERIA,
        duracion_semestre=10,
    ),
    Carrera(
        id_carrera="ICI-IND",
        codigo="PLAN-2023-IND",
        nombre_carrera="Ingeniería Civil Industrial",
        facultad=Facultad.INGENIERIA,
        duracion_semestre=10,
    )
]

#2. Semillas para Cursos
CURSO_MOCK: list[Curso] = [
    Curso(
        id_curso="CRS-INF1108",
        codigo_curso="INF-1108",
        nombre_curso="Desarrollo de Backend",
        semestre=4,
        id_carrera="ICI-INF",
    ),
    Curso(
        id_curso="CRS-INF1101",
        codigo_curso="INF-1101",
        nombre_curso="Introducción a la Ingeniería",
        semestre=1,
        id_carrera="ICI-INF",
    )
]

# 3. Semillas para Estudiantes
ESTUDIANTES_MOCK: list[Estudiante] = [
    Estudiante(
        rut_estudiante="20.123.554-5",
        nombre="Roberto",
        apellido="Díaz",
        email_institucional="rdiaz2026@alu.uct.cl",
        id_carrera="ICI-INF",
        estado_alumno=True,
    )
]

# 4. Semillas para Justificaciones
JUSTIFICACIONES_MOCK: list[Justificativo] = [
    Justificativo(
        id_justificativo="JUS-001",
        rut_estudiante="20.123.554-5",
        id_curso="CRS-INF1101",
        fecha_inasistencia=date(2026, 9, 20),
        tipo_inasistencia=TipoInasistencia.CLASE,
        estado=EstadoJustificativo.PENDIENTE,
        motivo="Cita médica de urgencia",
    )
]