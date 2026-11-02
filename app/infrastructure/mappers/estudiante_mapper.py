from app.domain.estudiante import Estudiante
from app.infrastructure.models.estudiante_model import EstudianteModel

def estudiante_a_dominio(modelo: EstudianteModel) -> Estudiante:
    return Estudiante(
        rut_estudiante=modelo.rut_estudiante,
        nombre=modelo.nombre,
        apellido=modelo.apellido,
        email_institucional=modelo.email_institucional,
        id_carrera=modelo.id_carrera,
        estado_alumno=modelo.estado_alumno,
    )


def estudiante_a_modelo(dominio: Estudiante) -> EstudianteModel:
    return EstudianteModel(
        rut_estudiante=dominio.rut_estudiante,
        nombre=dominio.nombre,
        apellido=dominio.apellido,
        email_institucional=dominio.email_institucional,
        id_carrera=dominio.id_carrera,
        estado_alumno=dominio.estado_alumno,
    )