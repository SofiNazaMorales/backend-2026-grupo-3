from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.carrera import Carrera
from app.infrastructure.models.carrera_model import CarreraModel
from app.infrastructure.mappers.carrera_mapper import carrera_a_dominio, carrera_a_modelo

class CarreraRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def crear(self, carrera: Carrera) -> Carrera:
        modelo = carrera_a_modelo(carrera)
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return carrera_a_dominio(modelo)

    def obtener_por_id(self, carrera_id: str) -> Carrera | None:
        modelo = self.session.get(CarreraModel, carrera_id)
        if modelo is None:
            return None
        return carrera_a_dominio(modelo)

    def listar(self) -> list[Carrera]:
        stmt = select(CarreraModel)
        modelos = self.session.scalars(stmt).all()
        return [carrera_a_dominio(m) for m in modelos]