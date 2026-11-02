from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.schemas.curso_dto import CursoUpdateDTO
from app.services import curso_service

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

@router.put("/{id_curso}")
def actualizar_curso(id_curso: str, curso_data: CursoUpdateDTO, db: Session = Depends(get_db)):
    curso_actualizado = curso_service.actualizar_curso(db, id_curso, curso_data)
    if not curso_actualizado:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    return {
        "success": True,
        "data": curso_actualizado,
        "error": None,
        "message": "Curso actualizado con éxito"
    }