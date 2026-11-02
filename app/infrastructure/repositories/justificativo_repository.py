from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.justificativo import Justificativo
from app.infrastructure.models.justificativo_model import JustificativoModel
from app.infrastructure.mappers.justificativo_mapper import justificativo_a_dominio, justificativo_a_modelo

class JustificativoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def crear(self, justificativo: Justificativo) -> Justificativo:
        modelo = justificativo_a_modelo(justificativo)
        self.session.add(modelo)
        self.session.commit()
        self.session.refresh(modelo)
        return justificativo_a_dominio(modelo)

    def obtener_por_id(self, justificativo_id: str) -> Justificativo | None:
        modelo = self.session.get(JustificativoModel, justificativo_id)
        if modelo is None:
            return None
        return justificativo_a_dominio(modelo)

    def listar(self) -> list[Justificativo]:
        stmt = select(JustificativoModel)
        modelos = self.session.scalars(stmt).all()
        return [justificativo_a_dominio(m) for m in modelos]