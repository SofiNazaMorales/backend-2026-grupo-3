from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.curso import Curso
from app.mappers import curso_a_dict, curso_a_dominio
from app.infrastructure.models.curso_model import CursoModel as curso_model


class CursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, curso: Curso) -> Curso:
        nuevo = curso_model(**curso_a_dict(curso))
        try:
            self.db.add(nuevo)
            self.db.commit()
            self.db.refresh(nuevo)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return curso_a_dominio(nuevo)

    def obtener_por_id(self, id_curso: str) -> Curso | None:
        encontrado = self.db.query(curso_model).filter(curso_model.id_curso == id_curso).first()
        return curso_a_dominio(encontrado) if encontrado is not None else None

    def obtener_por_codigo(self, codigo_curso: str) -> Curso | None:
        encontrado = self.db.query(curso_model).filter(
            curso_model.codigo_curso == codigo_curso
        ).first()
        return curso_a_dominio(encontrado) if encontrado is not None else None

    def actualizar(self, curso: Curso) -> Curso:
        actual = self.db.query(curso_model).filter(curso_model.id_curso == curso.id_curso).first()
        if actual is None:
            raise ValueError("No existe el curso que se intenta actualizar.")
        try:
            for campo, valor in curso_a_dict(curso).items():
                if campo != "id_curso":
                    setattr(actual, campo, valor)
            self.db.commit()
            self.db.refresh(actual)
        except SQLAlchemyError:
            self.db.rollback()
            raise
        return curso_a_dominio(actual)

    def listar(self) -> list[Curso]:
        return [curso_a_dominio(curso) for curso in self.db.query(curso_model).all()]
