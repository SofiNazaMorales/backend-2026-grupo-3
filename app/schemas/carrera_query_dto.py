from pydantic import BaseModel, Field
from app.domain.enums import Facultad

class CarreraQueryDTO(BaseModel):
    facultad: Facultad | None = Field(
        default=None,
        description="Filtrar carreras por facultad"
    )
    ordenar_por: str =Field(
        default="nombre_carrera",
        description="Atributo por el cual se ordenarán los resultados"
    )
    direccion: str = Field(
        default="asc",
        pattern="^(asc|desc)$",
        description="Dirección del ordenamiento (asc o desc)"
    )
    pagina: int = Field(
        default=1,
        ge=1,
        description="Número de página a consultar"
    )
    limite: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Cantidad de registros por página"
    )