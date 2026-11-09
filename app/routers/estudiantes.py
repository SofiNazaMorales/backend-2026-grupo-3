from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.presentation.dependencies import get_estudiante_service as get_service
from app.schemas.estudiante_dto import EstudianteCreateDTO, EstudianteUpdateDTO
from app.services.estudiante_service import EstudianteService
from app.respuestas import envelope

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.post("", status_code=status.HTTP_201_CREATED)
def crear_estudiante(payload: EstudianteCreateDTO, service: EstudianteService = Depends(get_service)):
    return envelope(True, service.crear(payload), message="Estudiante creado correctamente")

@router.get("")
def listar_estudiantes(service: EstudianteService = Depends(get_service)):
    items = service.listar()
    return envelope(True, {"items": items, "total": len(items)}, message="Estudiantes obtenidos correctamente")

@router.get("/{rut}")
def obtener_estudiante(rut: str, service: EstudianteService = Depends(get_service)):
    return envelope(True, service.obtener(rut), message="Estudiante obtenido correctamente")

@router.put("/{rut}")
def actualizar_estudiante(rut: str, payload: EstudianteUpdateDTO, service: EstudianteService = Depends(get_service)):
    return envelope(True, service.actualizar(rut, payload), message="Estudiante actualizado correctamente")

@router.delete("/{rut}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(rut: str, service: EstudianteService = Depends(get_service)):
    service.eliminar(rut)
    return Response(status_code=204)
