from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base

class CursoModel(Base):
    __tablename__ = "cursos"

    id_curso: Mapped[str] = mapped_column(String(50), primary_key=True)
    codigo_curso: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre_curso: Mapped[str] = mapped_column(String(100), nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False)
    id_carrera: Mapped[str] = mapped_column(String(50), ForeignKey("carreras.id_carrera"), nullable=False)