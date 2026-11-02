
from sqlalchemy import select, func, asc, desc
from sqlalchemy.orm import Session

from app.domain.estudiante import Estudiante
from app.infrastructure.models.estudiante_model import EstudianteModel
from app.infrastructure.mappers.estudiante_mapper import (
    estudiante_a_dominio,
    estudiante_a_modelo,
)


class EstudianteRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def crear(self, estudiante: Estudiante) -> Estudiante:
        modelo = estudiante_a_modelo(estudiante)

        self.session.add(modelo)
        self.session.flush()
        self.session.refresh(modelo)

        return estudiante_a_dominio(modelo)

    def obtener_por_id(self, estudiante_id: str) -> Estudiante | None:
        modelo = self.session.get(EstudianteModel, estudiante_id)

        if modelo is None:
            return None

        return estudiante_a_dominio(modelo)

    def obtener_por_email(
        self,
        email: str,
        excluir_rut: str | None = None
    ) -> Estudiante | None:

        stmt = select(EstudianteModel).where(
            EstudianteModel.email_institucional == email
        )

        if excluir_rut is not None:
            stmt = stmt.where(
                EstudianteModel.rut_estudiante != excluir_rut
            )

        modelo = self.session.scalars(stmt).first()

        if modelo is None:
            return None

        return estudiante_a_dominio(modelo)

    def listar(self) -> list[Estudiante]:
        stmt = select(EstudianteModel).order_by(
            EstudianteModel.rut_estudiante
        )

        modelos = self.session.scalars(stmt).all()

        return [estudiante_a_dominio(modelo) for modelo in modelos]

    def actualizar(self, estudiante: Estudiante) -> Estudiante | None:
        modelo = self.session.get(
            EstudianteModel,
            estudiante.rut_estudiante
        )

        if modelo is None:
            return None

        modelo.nombre = estudiante.nombre
        modelo.apellido = estudiante.apellido
        modelo.email_institucional = estudiante.email_institucional
        modelo.id_carrera = estudiante.id_carrera
        modelo.estado_alumno = estudiante.estado_alumno

        self.session.flush()
        self.session.refresh(modelo)

        return estudiante_a_dominio(modelo)

    def eliminar(self, estudiante_id: str) -> bool:
        modelo = self.session.get(EstudianteModel, estudiante_id)

        if modelo is None:
            return False

        self.session.delete(modelo)
        self.session.flush()

        return True

    def listar_paginado(
        self,
        id_carrera: str | None = None,
        estado_alumno: bool | None = None,
        ordenar_por: str = "rut_estudiante",
        direccion: str = "asc",
        pagina: int = 1,
        limite: int = 10,
    ) -> tuple[list[Estudiante], int]:

        columnas_ordenables = {
            "rut_estudiante": EstudianteModel.rut_estudiante,
            "nombre": EstudianteModel.nombre,
            "apellido": EstudianteModel.apellido,
            "email_institucional": EstudianteModel.email_institucional,
            "id_carrera": EstudianteModel.id_carrera,
            "estado_alumno": EstudianteModel.estado_alumno,
        }

        columna = columnas_ordenables[ordenar_por]

        stmt = select(EstudianteModel)
        stmt_total = select(func.count()).select_from(EstudianteModel)

        if id_carrera is not None:
            stmt = stmt.where(
                EstudianteModel.id_carrera == id_carrera
            )
            stmt_total = stmt_total.where(
                EstudianteModel.id_carrera == id_carrera
            )

        if estado_alumno is not None:
            stmt = stmt.where(
                EstudianteModel.estado_alumno == estado_alumno
            )
            stmt_total = stmt_total.where(
                EstudianteModel.estado_alumno == estado_alumno
            )

        total = self.session.scalar(stmt_total) or 0

        if direccion.lower() == "desc":
            stmt = stmt.order_by(desc(columna))
        else:
            stmt = stmt.order_by(asc(columna))

        stmt = stmt.offset((pagina - 1) * limite).limit(limite)

        modelos = self.session.scalars(stmt).all()

        estudiantes = [
            estudiante_a_dominio(modelo)
            for modelo in modelos
        ]

        return estudiantes, total
