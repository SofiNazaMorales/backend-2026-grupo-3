from pydantic import BaseModel, Field


class CursoCreate(BaseModel):
    id_curso: str = Field(min_length=1)
    codigo_curso: str = Field(min_length=1)
    nombre_curso: str = Field(min_length=1)
    semestre: int = Field(ge=1)
    id_carrera: str = Field(min_length=1)


class CursoUpdate(BaseModel):
    codigo_curso: str | None = Field(default=None, min_length=1)
    nombre_curso: str | None = Field(default=None, min_length=1)
    semestre: int | None = Field(default=None, ge=1)
    id_carrera: str | None = Field(default=None, min_length=1)


class CursoResponse(BaseModel):
    id_curso: str
    codigo_curso: str
    nombre_curso: str
    semestre: int
    id_carrera: str