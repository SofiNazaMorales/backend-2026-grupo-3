import re
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.schemas.justificacion import  JustificacionResponse


class EstudianteBase(BaseModel):
    rut_estudiante: str = Field(..., min_length=8, max_length=12, description="RUT chileno formato 12345678-K o 12.345.678-K")
    nombre: str = Field(..., min_length=2, max_length=50)
    apellido: str = Field(..., min_length=2, max_length=50)
    email_institucional: EmailStr
    id_carrera: str

    @field_validator("rut_estudiante")
    @classmethod
    def validar_y_formatear_rut(cls, v:str) -> str:
        rut_limpio = v.strip().upper()

        if "-" not in rut_limpio:
            raise ValueError("El RUT debe incluir guión verificador (ej: 12345678-K)")

        cuerpo, dv = rut_limpio.split("-")
        cuerpo_sin_puntos = cuerpo.replace(".", "")

        if not cuerpo_sin_puntos.isdigit() or not re.match(r"^[0-9K]$", dv):
            raise ValueError("El RUT contiene caracteres no válidos")

        cuerpo_formateado = f"{int(cuerpo_sin_puntos):,}". replace(",", ".")

        return f"{cuerpo_formateado}-{dv}"

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteResponse(EstudianteBase):
    model_config = ConfigDict(from_attributes=True)

class EstudianteConJustificacionesResponse(EstudianteResponse):
    justificaciones: List[JustificacionResponse] = []