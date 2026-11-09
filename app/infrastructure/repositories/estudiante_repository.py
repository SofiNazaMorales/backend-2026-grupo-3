from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.domain.estudiante import Estudiante
from app.infrastructure.models.estudiante_model import EstudianteModel
from app.infrastructure.mappers.estudiante_mapper import estudiante_a_dominio, estudiante_a_modelo

class EstudianteRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, estudiante: Estudiante):
        modelo = estudiante_a_modelo(estudiante)
        try:
            self.session.add(modelo)
            self.session.commit()
            self.session.refresh(modelo)
        except SQLAlchemyError:
            self.session.rollback()
            raise
        return estudiante_a_dominio(modelo)

    def obtener_por_id(self, estudiante_id: str):
        modelo = self.session.get(EstudianteModel, estudiante_id)
        return estudiante_a_dominio(modelo) if modelo is not None else None

    def listar(self):
        return [estudiante_a_dominio(m) for m in self.session.scalars(select(EstudianteModel)).all()]

    def actualizar(self, estudiante: Estudiante):
        modelo = self.session.get(EstudianteModel, estudiante.rut_estudiante)
        if modelo is None:
            return None
        try:
            for name in ("nombre", "apellido", "email_institucional", "id_carrera", "estado_alumno"):
                setattr(modelo, name, getattr(estudiante, name))
            self.session.commit()
            self.session.refresh(modelo)
        except SQLAlchemyError:
            self.session.rollback()
            raise
        return estudiante_a_dominio(modelo)

    def eliminar(self, rut: str):
        modelo = self.session.get(EstudianteModel, rut)
        if modelo is None:
            return False
        try:
            self.session.delete(modelo)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise
        return True
