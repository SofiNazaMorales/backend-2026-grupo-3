from pydantic import BaseModel
from datetime import date
from app.domain.models import TipoInasistencia, EstadoJustificativo
 
 
class JustificacionCreate(BaseModel):
    rut_estudiante: str
    id_curso: str
    fecha_inasistencia: date
    tipo_inasistencia: TipoInasistencia
 
 
class JustificacionUpdate(BaseModel):
    fecha_inasistencia: date | None = None
    tipo_inasistencia: TipoInasistencia | None = None
 
 
class JustificacionResponse(JustificacionCreate):
    id_justificativo: int
    estado: EstadoJustificativo
    fecha_registro: date
    veces_editado: int
 