from app.domain.errores import ErrorAplicacion
from app.infrastructure.repositories.curso_repository import CursoRepository
from app.domain.curso import Curso
from app.schemas.curso_dto import CursoCreateDTO, CursoUpdateDTO


class CursoService:
    def __init__(self, repository: CursoRepository):
        self.repository = repository

    def crear_curso(self, datos: CursoCreateDTO) -> Curso:

        curso_existente = self.repository.obtener_por_id(datos.id_curso)

        if curso_existente is not None:
            raise ErrorAplicacion(
                status_code=409,
                detail=f"Ya existe un curso con el ID '{datos.id_curso}'."
            )

        codigo_existente = self.repository.obtener_por_codigo(
            datos.codigo_curso
        )

        if codigo_existente is not None:
            raise ErrorAplicacion(
                status_code=409,
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

        curso = self.repository.obtener_por_id(id_curso.upper())

        if curso is None:
            raise ErrorAplicacion(
                status_code=404,
                detail=f"No existe un curso con el ID '{id_curso}'."
            )

        return curso

    def actualizar_curso(self, id_curso: str, datos: CursoUpdateDTO) -> Curso:
        curso = self.obtener_curso(id_curso)
        cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
        if "codigo_curso" in cambios:
            otro = self.repository.obtener_por_codigo(cambios["codigo_curso"])
            if otro is not None and otro.id_curso != curso.id_curso:
                raise ErrorAplicacion(409, "Ya existe un curso con ese código.")
        valores = {"id_curso": curso.id_curso, "codigo_curso": curso.codigo_curso,
                   "nombre_curso": curso.nombre_curso, "semestre": curso.semestre,
                   "id_carrera": curso.id_carrera}
        valores.update(cambios)
        return self.repository.actualizar(Curso(**valores))
