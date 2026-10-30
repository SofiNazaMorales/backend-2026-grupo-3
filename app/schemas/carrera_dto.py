from pydantic import BaseModel, ConfigDict, Field
from app.domain.enums import Facultad


class CarreraCreateDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    id_carrera: str = Field(
        ..., 
        min_length=2, 
        max_length=12, 
        description="Código identificador de la carrera, usar acrónimos", 
        examples=["ICI-INF"]
    )
    codigo: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description="Código de plan de estudios de la carrera en la UCT",
        examples=["PLAN-2023-INF"]
    )
    nombre_carrera: str = Field(
        ..., 
        min_length=3, 
        max_length=100,
        description="Nombre oficial de la carrera"
    )
    facultad: Facultad
    duracion_semestre: int = Field(
        ..., 
        ge=1, 
        le=14, 
        description="Duración válida entre 1 y 14 semestres")

class CarreraUpdateDTO(BaseModel):
    model_config = ConfigDict(
            str_strip_whitespace=True,
            extra="forbid"
    )

    codigo: str | None = Field(None, min_length=5, max_length=20)
    nombre_carrera: str | None = Field(None, min_length=3, max_length=100)
    facultad: Facultad | None = None
    duracion_semestre: int | None = Field(None, ge=1, le=14)

class CarreraResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_carrera: str
    codigo: str
    nombre_carrera: str
    facultad: Facultad
    duracion_semestre: int

class CarreraPaginaDTO(BaseModel):
    items: list[CarreraResponseDTO]
    total: int
    pagina: int
    limite: int
    total_paginas: int