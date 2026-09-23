from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.domain.modelos import TipoInasistencia, EstadoJustificativo

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