from app.domain.curso import Curso


class CursoRepository:
    def __init__(self):
        self._cursos: dict[str, Curso] = {}

    def crear(self, curso: Curso) -> Curso:

        self._cursos[curso.id_curso] = curso
        return curso

    def obtener_por_id(self, id_curso: str) -> Curso | None:

        return self._cursos.get(id_curso)

    def obtener_por_codigo(self, codigo_curso: str) -> Curso | None:

        for curso in self._cursos.values():
            if curso.codigo_curso == codigo_curso:
                return curso

        return None

    def actualizar(self, curso: Curso) -> Curso:

        self._cursos[curso.id_curso] = curso
        return curso

    def listar(self) -> list[Curso]:

        return list(self._cursos.values())