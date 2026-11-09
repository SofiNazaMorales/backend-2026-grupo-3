from app.domain.curso import Curso
from app.infrastructure.models.curso_model import CursoModel

def curso_a_dominio(modelo: CursoModel) -> Curso:
    return Curso(
        id_curso=modelo.id_curso,
        codigo_curso=modelo.codigo_curso,
        nombre_curso=modelo.nombre_curso,
        semestre=modelo.semestre,
        id_carrera=modelo.id_carrera,
    )


def curso_a_modelo(dominio: Curso) -> CursoModel:
    return CursoModel(
        id_curso=dominio.id_curso,
        codigo_curso=dominio.codigo_curso,
        nombre_curso=dominio.nombre_curso,
        semestre=dominio.semestre,
        id_carrera=dominio.id_carrera,
    )