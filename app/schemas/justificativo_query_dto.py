from datetime import date
from pydantic import BaseModel, Field
from app.domain.enums import EstadoJustificativo, TipoInasistencia

class JustificativoQueryDTO(BaseModel):
    rut_estudiante: str | None = Field(
        default=None,
        description="Filtrar justificativo por RUT de estudiante"
    )
    id_curso: str | None = Field(
        default=None,
        description="Filtrar justificativos por ID de curso"
    )
    estado: EstadoJustificativo | None = Field(
        default=None,
        description="Filtrar por estado: PENDIENTE, ACEPTADO, RECHAZADO"
    )
    tipo_inasistencia: TipoInasistencia | None = Field(
        default=None,
        description="Filtrar por tipo de inasistencia"
    )
    fecha_desde: date | None = Field(
        default=None,
        description="Filtrar inasistencia hasta esta fecha"
    )
    ordenar_por: str = Field(
        default="fecha_inasistencia",
        description="Atributo para ordenar los resultados"
    )
    direccion: str =Field(
        default="desc",
        pattern="^(asc|desc)$",
        description="Dirección del orden (asc o desc)"
    )
    pagina: int = Field(
        default=1,
        ge=1,
        description="Numero de página"
    )
    limite: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Cantidad de registros por página"
    )