from pydantic import BaseModel, ConfigDict, Field
from app.domain.modelos import Facultad


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



