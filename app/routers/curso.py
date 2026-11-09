from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.presentation.dependencies import get_curso_service
from app.schemas.curso_dto import CursoCreateDTO, CursoUpdateDTO
from app.services.curso_service import CursoService
from app.respuestas import envelope

router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_curso(payload: CursoCreateDTO, service: CursoService = Depends(get_curso_service)):
    return envelope(True, service.crear_curso(payload), message="Curso creado correctamente")

@router.get("/{id_curso}")
def obtener_curso(id_curso: str, service: CursoService = Depends(get_curso_service)):
    return envelope(True, service.obtener_curso(id_curso), message="Curso obtenido correctamente")

@router.put("/{id_curso}")
def actualizar_curso(id_curso: str, payload: CursoUpdateDTO, service: CursoService = Depends(get_curso_service)):
    return envelope(True, service.actualizar_curso(id_curso, payload), message="Curso actualizado correctamente")
