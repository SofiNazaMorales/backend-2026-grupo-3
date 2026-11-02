
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.services.estudiante_service import EstudianteService

from app.schemas.estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
    EstudianteResponseDTO,
    EstudiantePaginaDTO,
)

from app.schemas.estudiante_query_dto import EstudianteQueryDTO


router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)


def obtener_servicio_estudiante(
    db: Session = Depends(get_db)
) -> EstudianteService:
    return EstudianteService(db)


def crear_respuesta(
    success: bool,
    data=None,
    error=None,
    message: str = "",
    status_code: int = 200
):
    return {
        "success": success,
        "error": error,
        "data": data,
        "message": message,
        "statusCode": status_code
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_estudiante(
    payload: EstudianteCreateDTO,
    service: EstudianteService = Depends(obtener_servicio_estudiante)
):
    estudiante = service.crear_estudiante(payload)

    data = EstudianteResponseDTO.model_validate(
        estudiante
    ).model_dump(mode="json")

    return crear_respuesta(
        True,
        data,
        None,
        "Estudiante creado correctamente.",
        201
    )


@router.get("")
def listar_estudiantes(
    filtros: EstudianteQueryDTO = Depends(),
    service: EstudianteService = Depends(obtener_servicio_estudiante)
):
    resultado = service.listar_estudiantes(filtros)

    data = resultado.model_dump(mode="json")

    return crear_respuesta(
        True,
        data,
        None,
        "Estudiantes obtenidos correctamente.",
        200
    )


@router.get("/{rut_estudiante}")
def obtener_estudiante(
    rut_estudiante: str,
    service: EstudianteService = Depends(obtener_servicio_estudiante)
):
    estudiante = service.obtener_estudiante(rut_estudiante)

    data = EstudianteResponseDTO.model_validate(
        estudiante
    ).model_dump(mode="json")

    return crear_respuesta(
        True,
        data,
        None,
        "Estudiante obtenido correctamente.",
        200
    )


@router.put("/{rut_estudiante}")
def actualizar_estudiante(
    rut_estudiante: str,
    payload: EstudianteUpdateDTO,
    service: EstudianteService = Depends(obtener_servicio_estudiante)
):
    estudiante = service.actualizar_estudiante(
        rut_estudiante,
        payload
    )

    data = EstudianteResponseDTO.model_validate(
        estudiante
    ).model_dump(mode="json")

    return crear_respuesta(
        True,
        data,
        None,
        "Estudiante actualizado correctamente.",
        200
    )


@router.delete("/{rut_estudiante}")
def eliminar_estudiante(
    rut_estudiante: str,
    service: EstudianteService = Depends(obtener_servicio_estudiante)
):
    resultado = service.eliminar_estudiante(rut_estudiante)

    return crear_respuesta(
        True,
        resultado,
        None,
        "Estudiante eliminado correctamente.",
        200
    )
