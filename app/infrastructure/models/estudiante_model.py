from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.infrastructure.models.carrera_model import CarreraModel


class EstudianteModel(Base):
    __tablename__ = "estudiantes"

    rut_estudiante: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    email_institucional: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    estado_alumno: Mapped[bool] = mapped_column(Boolean, default=True)

    id_carrera: Mapped[str] = mapped_column(
        String(50), ForeignKey("carreras.id"), nullable=False
    )

    carrera: Mapped["CarreraModel"] = relationship(back_populates="estudiantes")