from pydantic import BaseModel, ConfigDict, Field, field_validator

class CursoCreateDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    id_curso: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        description="Identificador único del curso (Formato: CRS-CODIGO)",
        examples=["CRS-INF1108"],
    )
    codigo_curso: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="Sigla oficial de la asignatura en el plan de estudio UCT",
        examples=["INF-1108"],
    )
    nombre_curso: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre de la asignatura",
        examples=["Desarrollo de Backend"],
    )
    semestre: int = Field(
        ...,
        ge=1,
        le=14,
        description="Semestre dentro del plan de estudios",
        examples=[4],
    )
    id_carrera: str = Field(
        ...,
        min_length=2,
        max_length=12,
        description="Código de la carrera asociada (Acrónimo UCt)",
        examples=["ICI-INF"]
    )

class CursoUpdateDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    codigo_curso: str | None = Field(None, min_length=3, max_length=10)
    nombre_curso: str | None = Field(None, min_length=3, max_length=100)
    semestre: int | None = Field(None, ge=1, le=14)
    id_carrera: str | None = Field(None, min_length=2, max_length=12)

class CursoResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_curso: str
    codigo_curso: str
    nombre_curso: str
    semestre: int
    id_carrera: str

class CursoPaginaDTO(BaseModel):
    items: list[CursoResponseDTO]
    total: int
    pagina: int
    limite: int
    total_paginas: int