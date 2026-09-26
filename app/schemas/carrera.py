from pydantic import BaseModel, ConfigDict, Field
from app.domain.enums import Facultad


class CarreraBase(BaseModel):
    id_carrera: str = Field(
        ..., 
        min_length=2, 
        max_length=12, 
        description="Código identificador de la carrera, usar acronimos", 
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
        max_length=100
    )
    facultad: Facultad
    duracion_semestre: int = Field(
        ..., 
        ge=1, 
        le=14, 
        description="Duración válida entre 1 y 14 semestres")

class CarreraCreate(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id_carrera: str

    model_config = ConfigDict(from_attributes=True)



