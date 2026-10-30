from functools import lru_cache

from fastapi import Depends

from application.services.curso_service import CursoService
from infrastructure.repositories.curso_repository import CursoRepository


@lru_cache
def get_curso_repository() -> CursoRepository:
    # Una sola instancia compartida: el repositorio guarda los datos en memoria.
    return CursoRepository()


def get_curso_service(
    repository: CursoRepository = Depends(get_curso_repository),
) -> CursoService:
    return CursoService(repository)
