
from fastapi import HTTPException

from app.domain.curso import Curso
from app.repositories.curso_repository import CursoRepository
from app.schemas.curso_dto import CursoCreateDTO, CursoUpdateDTO


class CursoService:
    def __init__(self, repository: CursoRepository):
        self.repository = repository

    def crear_curso(self, datos: CursoCreateDTO) -> Curso:

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
                detail=f"Ya existe un curso con el código '{datos.codigo_curso}'."
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
        datos_actualizados: CursoUpdateDTO
    ) -> Curso:

        curso_existente = self.repository.obtener_por_id(id_curso)

        if curso_existente is None:
            raise HTTPException(
                status_code=404,
                detail=f"No existe un curso con el ID '{id_curso}'."
            )

        cambios = datos_actualizados.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        nuevo_codigo = cambios.get("codigo_curso")

        if nuevo_codigo is not None:
            codigo_existente = self.repository.obtener_por_codigo(
                nuevo_codigo
            )

            if (
                codigo_existente is not None
                and codigo_existente.id_curso != id_curso
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un curso con el código '{nuevo_codigo}'."
                )

        curso_actualizado = Curso(
            id_curso=curso_existente.id_curso,
            codigo_curso=cambios.get(
                "codigo_curso", curso_existente.codigo_curso
            ),
            nombre_curso=cambios.get(
                "nombre_curso", curso_existente.nombre_curso
            ),
            semestre=cambios.get(
                "semestre", curso_existente.semestre
            ),
            id_carrera=cambios.get(
                "id_carrera", curso_existente.id_carrera
            )
        )

        return self.repository.actualizar(curso_actualizado)
