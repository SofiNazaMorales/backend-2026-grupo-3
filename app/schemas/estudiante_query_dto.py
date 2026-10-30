from pydantic import BaseModel, Field

class EstudianteQueryDTO(BaseModel):
    id_carrera: str | None = Field(
        default=None,
        description="Filtrar estudiantes por carrera"
    )
    estado_alumno: bool | None = Field(
        default=None,
        description="Filtrar por estado activo/inactivo"
    )
    ordenar_por: str = Field(
        default="rut_estudiante",
        description="Atributo por el cual se ordenarán los resultados"
    )
    direccion: str= Field(
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