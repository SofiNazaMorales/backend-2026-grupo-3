from app.domain.curso import Curso


class CursoRepository:
    def __init__(self):
        self._cursos: dict[str, Curso] = {}
        self.db = db

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

    def actualizar_en_bd(self, id_curso: str, datos_actualizados: dict):
        if not self.db:
            raise ValueError("No hay conexión a la base de datos")
            
        curso_db = self.db.query(CursoModel).filter(CursoModel.id_curso == id_curso).first()
        if curso_db:
            for key, value in datos_actualizados.items():
                setattr(curso_db, key, value)
            
            self.db.commit()
            self.db.refresh(curso_db)
            return curso_db
            
        return None

    def listar(self) -> list[Curso]:

        return list(self._cursos.values())