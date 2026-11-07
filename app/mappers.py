
"""Conversiones entre entidades de dominio y estructuras de respuesta."""

from app.domain.curso import Curso
from app.domain.justificativo import Justificativo
from app.infrastructure.models.curso_model import CursoModel


def justificativo_a_dict(j: Justificativo) -> dict:
    return {
        "id_justificativo": j.id_justificativo,
        "rut_estudiante": j.rut_estudiante,
        "id_curso": j.id_curso,
        "fecha_inasistencia": j.fecha_inasistencia,
        "tipo_inasistencia": j.tipo_inasistencia,
        "motivo": j.motivo,
        "fecha_registro": j.fecha_registro,
        "veces_editado": j.veces_editado,
        "estado": j.estado,
    }


def curso_a_dominio(curso: CursoModel) -> Curso:
    return Curso(
        id_curso=curso.id_curso,
        codigo_curso=curso.codigo_curso,
        nombre_curso=curso.nombre_curso,
        semestre=curso.semestre,
        id_carrera=curso.id_carrera,
    )


def curso_a_dict(curso: Curso) -> dict:
    return {
        "id_curso": curso.id_curso,
        "codigo_curso": curso.codigo_curso,
        "nombre_curso": curso.nombre_curso,
        "semestre": curso.semestre,
        "id_carrera": curso.id_carrera,
    }
