from datetime import date
from pydantic import BaseModel, ConfigDict ,Field
from app.domain.enums import EstadoJustificativo, TipoInasistencia

class JustificativoCreateDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    rut_estudiante: str = Field(
        ...,
        description="RUT del estudiante que justifica",
        examples=["20.123.554-5"]
    )
    id_curso: str = Field(
        ...,
        description="ID del curso/ramo involucrado",
        examples=["CRS-INF1108"]
    )
    fecha_inasistencia: date = Field(
        ...,
        description="Fecha en que el estudiante faltó"
    )
    tipo_inasistencia: TipoInasistencia = Field(
        ...,
        description="Tipo de falta: CLASE o EVALUACION."
    )
    motivo: str = Field(
        ..., 
        min_length=10, 
        max_length=500, 
        description="Descripción del motivo de la inasistencia"
        )

class JustificativoUpdateDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    fecha_inasistencia: date | None = None
    tipo_inasistencia: TipoInasistencia | None = None
    motivo: str | None = Field(None, min_length=10, max_length=500)
    estado: EstadoJustificativo | None = None

class JustificativoResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_justificativo: str
    rut_estudiante: str
    id_curso: str
    fecha_inasistencia: date
    tipo_inasistencia: TipoInasistencia
    motivo: str
    estado: EstadoJustificativo
    fecha_registro: date | None = None
    veces_editado: int = 0

class JustificativoPaginaDTO(BaseModel):
    items: list[JustificativoResponseDTO]
    total: int
    pagina: int
    limite: int
    total_paginas: int