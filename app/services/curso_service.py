from fastapi import HTTPException

from app.domain.curso import Curso
from app.repositories.curso_repository import CursoRepository
from app.schemas.curso import CursoCreate, CursoUpdate


class CursoService:
    def __init__(self, repository: CursoRepository):
        self.repository = repository

    def crear_curso(self, datos: CursoCreate) -> Curso:

        curso_existente = self.repository.obtener_por_id(datos.id_curso)

        if curso_existente is not None:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un curso con el ID '{datos.id_curso}'."
            )

        codigo_existente = self.repository.obtener_por_codigo(
            datos.codigo_curso
        )

        if codigo_existente is not None:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Ya existe un curso con el código "
                    f"'{datos.codigo_curso}'."
                )
            )

        curso = Curso(
            id_curso=datos.id_curso,
            codigo_curso=datos.codigo_curso,
            nombre_curso=datos.nombre_curso,
            semestre=datos.semestre,
            id_carrera=datos.id_carrera
        )

        return self.repository.crear(curso)

    def obtener_curso(self, id_curso: str) -> Curso:

        curso = self.repository.obtener_por_id(id_curso)

        if curso is None:
            raise HTTPException(
                status_code=404,
                detail=f"No existe un curso con el ID '{id_curso}'."
            )

        return curso

    def actualizar_curso(
        self,
        id_curso: str,
        datos: CursoUpdate
    ) -> Curso:

        curso = self.obtener_curso(id_curso)

        if datos.codigo_curso is not None:
            curso_con_codigo = self.repository.obtener_por_codigo(
                datos.codigo_curso
            )

            if (
                curso_con_codigo is not None
                and curso_con_codigo.id_curso != id_curso
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Ya existe un curso con el código "
                        f"'{datos.codigo_curso}'."
                    )
                )

            curso.codigo_curso = datos.codigo_curso

        if datos.nombre_curso is not None:
            curso.nombre_curso = datos.nombre_curso

        if datos.semestre is not None:
            curso.semestre = datos.semestre

        if datos.id_carrera is not None:
            curso.id_carrera = datos.id_carrera

        return self.repository.actualizar(curso)