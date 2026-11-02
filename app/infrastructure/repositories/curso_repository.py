from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.curso import Curso
from app.infrastructure.models.curso_model import CursoModel
from app.infrastructure.mappers.curso_mapper import curso_a_dominio, curso_a_modelo

class CursoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def crear(self, curso: Curso) -> Curso:
        modelo = curso_a_modelo(curso)
        self.session.add(modelo)
        self.session.flush()
        self.session.refresh(modelo)
        return curso_a_dominio(modelo)

    def obtener_por_id(self, curso_id: str) -> Curso | None:
        modelo = self.session.get(CursoModel, curso_id)
        if modelo is None:
            return None
        return curso_a_dominio(modelo)

    def listar(self) -> list[Curso]:
        stmt = select(CursoModel)
        modelos = self.session.scalars(stmt).all()
        return [curso_a_dominio(m) for m in modelos]