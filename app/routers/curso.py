from fastapi import APIRouter, Depends, status
from app.schemas.curso_dto import CursoCreateDTO, CursoUpdateDTO
from app.services.curso_service import CursoService

router = APIRouter(prefix="/cursos", tags=["Cursos"])

def get_curso_service():
    return None 

def _envelope(success: bool, data=None, error=None, message: str = ""):
    return {"success": success, "data": data, "error": error, "message": message}

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_curso(payload: CursoCreateDTO, service: CursoService = Depends(get_curso_service)):
    return _envelope(True, payload.model_dump(), None, "Curso creado (Estructura lista)")

@router.get("/{id_curso}")
def obtener_curso(id_curso: str, service: CursoService = Depends(get_curso_service)):
    return _envelope(True, {"id_curso": id_curso}, None, "Curso obtenido (Estructura lista)")