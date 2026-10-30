from pydantic import BaseModel, Field

class CursoQueryDTO(BaseModel):
    id_carrera: str | None = Field(
        default=None,
        description="Filtrar por ID de carrera"
    )
    semestre: int | None = Field(
        default=None,
        ge=1,
        le=14,
        description="Filtrar por semestre"
    )
    ordenar_por: str = Field(
        default="codigo_curso",
        description="Atributo para ordenar"
    )
    direccion: str = Field(
        default="asc",
        pattern="^(asc|desc)$",
        description="Dirección del orden (asc o desc)"
    )
    pagina: int =Field(
        default=1,
        ge=1,
        description="Número de página"
    )
    tamano: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Cantidad de registros por página"
    )