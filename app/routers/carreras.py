from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories.carrera_repository import CarreraRepository
from app.services.carrera_service import CarreraService
from app.schemas.carrera_dto import CarreraCreateDTO
from app.respuestas import envelope

router = APIRouter(prefix="/carreras", tags=["Carreras"])

def get_service(db: Session = Depends(get_db)):
    return CarreraService(CarreraRepository(db))

@router.get("")
def listar_carreras(service: CarreraService = Depends(get_service)):
    items = service.listar()
    return envelope(True, {"items": items, "total": len(items)}, message="Carreras obtenidas correctamente")

@router.get("/{id_carrera}")
def obtener_carrera(id_carrera: str, service: CarreraService = Depends(get_service)):
    return envelope(True, service.obtener(id_carrera), message="Carrera obtenida correctamente")

@router.post("", status_code=201)
def crear_carrera(payload: CarreraCreateDTO, service: CarreraService = Depends(get_service)):
    return envelope(True, service.crear(payload), message="Carrera creada correctamente")
