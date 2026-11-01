from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base

if TYPE_CHECKING:
    from app.infrastructure.models.estudiante_model import EstudianteModel

class CarreraModel(Base):
    __tablename__ = "carreras"

    id_carrera: Mapped[str] = mapped_column(String(50), primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre_carrera: Mapped[str] = mapped_column(String(200), nullable=False)
    duracion_semestre: Mapped[int] = mapped_column(Integer, nullable=False)
    facultad: Mapped[str] = mapped_column(String(100), nullable=False)
    

    estudiantes: Mapped[list["EstudianteModel"]] = relationship(
        back_populates="carrera",
    )