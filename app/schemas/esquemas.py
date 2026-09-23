import re
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.domain.modelos import TipoInasistencia, EstadoJustificativo, Facultad


class CarreraBase(BaseModel):
    codigo: str = Field(..., min_length=2, max_length=12, description="Código de la carrera, ej: ICINF11-08")
    nombre_carrera: str = Field(..., min_length=3, max_length=100)
    facultad: Facultad
    duracion_semestre: int = Field(..., ge=1, le=14, description="Duración válida entre 1 y 14 semestres")

class CarreraCreate(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id_carrera: str

    model_config = ConfigDict(from_attributes=True)


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


class JustificacionCreate(BaseModel):
    rut_estudiante: str 
    id_curso: str
    fecha_inasistencia: date
    tipo_inasistencia: TipoInasistencia

    @field_validator("fecha_inasistencia")
    @classmethod
    def validar_fecha(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("La fecha de inasistencia no puede ser una fecha futura")
        return v

class JustificacionUpdate(BaseModel):
    fecha_inasistencia: Optional[date] = None
    tipo_inasistencia: Optional[TipoInasistencia] = None

class JustificacionResponse(JustificacionCreate):
    id_justificativo: int
    estado: EstadoJustificativo
    fecha_registro: date
    veces_editado: int

    model_config = ConfigDict(from_attributes=True)