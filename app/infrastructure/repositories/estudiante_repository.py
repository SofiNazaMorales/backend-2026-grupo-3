from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.estudiante import Estudiante
from app.infrastructure.models.estudiante_model import EstudianteModel
from app.infrastructure.mappers.estudiante_mapper import estudiante_a_dominio, estudiante_a_modelo

class EstudianteRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def crear(self, estudiante: Estudiante) -> Estudiante:
        modelo = estudiante_a_modelo(estudiante)
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return estudiante_a_dominio(modelo)

    def obtener_por_id(self, estudiante_id: str) -> Estudiante | None:
        modelo = self.session.get(EstudianteModel, estudiante_id)
        if modelo is None:
            return None
        return estudiante_a_dominio(modelo)

    def listar(self) -> list[Estudiante]:
        stmt = select(EstudianteModel)
        modelos = self.session.scalars(stmt).all()
        return [estudiante_a_dominio(m) for m in modelos]