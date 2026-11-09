from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories.curso_repository import CursoRepository
from app.infrastructure.repositories.estudiante_repository import EstudianteRepository
from app.services.curso_service import CursoService
from app.services.estudiante_service import EstudianteService

def get_curso_service(db: Session = Depends(get_db)):
    return CursoService(CursoRepository(db))

def get_estudiante_service(db: Session = Depends(get_db)):
    return EstudianteService(EstudianteRepository(db))
