from pydantic import BaseModel, ConfigDict, Field, field_validator

class CursoBase(BaseModel):
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
        gt=0,
        lt=13,
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

    @field_validator("id_curso")
    @classmethod
    def normalizar_id_curso(cls, v: str) -> str:
        return v.strip().upper()

class CursoCreate(CursoBase):
    pass

class CursoUpdate(BaseModel):
    codigo_curso: str | None = Field(None, min_length=3, max_length=10)
    nombre_curso: str | None = Field(None, min_length=3, max_length=100)
    semestre: int | None = Field(None, gt=0, lt=13)
    id_carrera: str | None = Field(None, min_length=2, max_length=12)

class CursoResponse(CursoBase):

    model_config = ConfigDict(from_attributes=True)