from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database import Base

class JustificativoModel(Base):
    __tablename__ = "justificativos"

    id_justificativo: Mapped[str] = mapped_column(String(50), primary_key=True)
    rut_estudiante: Mapped[str] = mapped_column(
            String(20), ForeignKey("estudiantes.rut_estudiante"), nullable=False
        )
    id_curso: Mapped[str] = mapped_column(
            String(50), ForeignKey("cursos.id_curso"), nullable=False
        )
    fecha_inasistencia: Mapped[Date] = mapped_column(Date, nullable=False)
    tipo_inasistencia: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_registro: Mapped[Date] = mapped_column(Date, nullable=True)
    veces_editado: Mapped[int] = mapped_column(Integer, default=0)
    estado: Mapped[str] = mapped_column(String(20), default="Pendiente")