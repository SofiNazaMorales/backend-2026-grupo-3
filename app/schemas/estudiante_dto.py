import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EstudianteCreateDTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid"
    )

    rut_estudiante: str = Field(
        ..., 
        min_length=8, 
        max_length=12, 
        description="RUT chileno formato",
        examples=["12345678-K o 12.345.678-K"]
    )
    nombre: str = Field(
        ..., 
        min_length=2, 
        max_length=50
    )
    apellido: str = Field(
        ..., 
        min_length=2, 
        max_length=50
    )
    email_institucional: EmailStr = Field(
        ...,
        description="Correo institucional UCT"
    )
    id_carrera: str = Field(
        ...,
        min_length=2,
        max_length=12,
        description="Acrónimo de las carrera a la que pertenece"
    )

    @field_validator("rut_estudiante")
    @classmethod
    def validar_y_formatear_rut(cls, v:str) -> str:
        rut_limpio = v.strip().upper()

        if "-" not in rut_limpio:
            raise ValueError("El RUT debe incluir el guión de su dígito verificador (ej: 12345678-K)")

        cuerpo, dv = rut_limpio.split("-")
        cuerpo_sin_puntos = cuerpo.replace(".", "")

        if not cuerpo_sin_puntos.isdigit() or not re.match(r"^[0-9K]$", dv):
            raise ValueError("El RUT contiene caracteres no válidos")

        cuerpo_formateado = f"{int(cuerpo_sin_puntos):,}". replace(",", ".")
        return f"{cuerpo_formateado}-{dv}"

class EstudianteUpdateDTO(BaseModel):
    model_config = ConfigDict(
            str_strip_whitespace=True,
            extra="forbid"
        )

    nombre: str | None = Field(None, min_length=2, max_length=50)
    apellido: str | None = Field(None, min_length=2, max_length=50)
    email_institucional: EmailStr | None = None
    id_carrera: str | None = Field(None, min_length=2, max_length=12)
    estado_alumno: bool | None = None

class EstudianteResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rut_estudiante: str
    nombre: str
    apellido: str
    email_institucional: EmailStr
    id_carrera: str
    estado_alumno: bool

class EstudiantePaginaDTO(BaseModel):
    items: list[EstudianteResponseDTO]
    total: int
    pagina: int
    limite: int
    total_paginas: int