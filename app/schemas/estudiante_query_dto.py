
from pydantic import BaseModel, Field, field_validator


class EstudianteQueryDTO(BaseModel):
    id_carrera: str | None = Field(
        default=None,
        description="Filtrar estudiantes por carrera"
    )

    estado_alumno: bool | None = Field(
        default=None,
        description="Filtrar por estado activo o inactivo"
    )

    ordenar_por: str = Field(
        default="rut_estudiante",
        description="Campo por el cual se ordenarán los resultados"
    )

    direccion: str = Field(
        default="asc",
        pattern="^(asc|desc)$",
        description="Dirección del ordenamiento: asc o desc"
    )

    pagina: int = Field(
        default=1,
        ge=1,
        description="Número de página"
    )

    limite: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Cantidad de registros por página"
    )

    @field_validator("ordenar_por")
    @classmethod
    def validar_ordenamiento(cls, valor: str) -> str:
        campos_permitidos = {
            "rut_estudiante",
            "nombre",
            "apellido",
            "email_institucional",
            "id_carrera",
            "estado_alumno",
        }

        if valor not in campos_permitidos:
            raise ValueError(
                "Campo de ordenamiento no permitido."
            )

        return valor
