from datetime import date
from typing import Literal
from fastapi import Query
from app.services import servicios as service
from app.schemas.justificativo_dto import JustificativoCreateDTO as JustificativoCreate, JustificativoUpdateDTO as JustificativoUpdate
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.services.servicios import ReglaDeNegocioError
from app.domain.enums import TipoInasistencia, EstadoJustificativo

router = APIRouter(prefix="/justificativos", tags=["Justificativos"])


from app.respuestas import envelope as _envelope


@router.get("")
def obtener_justificativos(
    id_curso: str | None = None,
    estado: EstadoJustificativo | None = None,
    tipo_inasistencia: TipoInasistencia | None = None,
    ordenar_por: Literal["fecha_inasistencia", "fecha_registro", "id_justificativo"] = "fecha_inasistencia",
    direccion: Literal["asc", "desc"] = "asc",
    pagina: int = Query(1, ge=1),
    limite: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    items, total = service.listar_justificativos_con_filtros(
        db, id_curso, estado, tipo_inasistencia, ordenar_por, direccion, pagina, limite
    )
    data = {"items": items, "total": total, "pagina": pagina, "limite": limite, "total_paginas": (total + limite - 1) // limite}
    return _envelope(True, data, None, "Justificativos obtenidos correctamente")


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_justificativo(payload: JustificativoCreate, response: Response, db: Session = Depends(get_db)):
    try:
        creado = service.crear_justificativo(db, payload.model_dump(exclude_none=True))
    except ReglaDeNegocioError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return _envelope(False, None, [{"code": e.code, "details": e.details}],
                          "La solicitud contiene errores de validación")
    return _envelope(True, creado, None, "Justificativo creado correctamente")


@router.get("/{id_justificativo}")
def obtener_justificativo(id_justificativo: str, response: Response, db: Session = Depends(get_db)):
    encontrado = service.obtener_justificativo(db, id_justificativo)
    if encontrado is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return _envelope(False, None,
                          [{"code": "NOT_FOUND", "details": "No existe un justificativo con el ID solicitado"}],
                          "Recurso no encontrado")
    return _envelope(True, encontrado, None, "Justificativo obtenido correctamente")


@router.put("/{id_justificativo}")
def actualizar_justificativo(id_justificativo: str, payload: JustificativoUpdate, response: Response, db: Session = Depends(get_db)):
    try:
        actualizado = service.editar_justificativo(db, id_justificativo, payload.model_dump(exclude_none=True))
    except ReglaDeNegocioError as e:
        response.status_code = (
            status.HTTP_404_NOT_FOUND if e.code == "NOT_FOUND" else status.HTTP_400_BAD_REQUEST
        )
        return _envelope(False, None, [{"code": e.code, "details": e.details}],
                          "No se pudo actualizar el justificativo")
    return _envelope(True, actualizado, None, "Justificativo actualizado correctamente")


@router.delete("/{id_justificativo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_justificativo(id_justificativo: str, db: Session = Depends(get_db)):
    if not service.eliminar_justificativo(db, id_justificativo):
        from fastapi import HTTPException
        raise HTTPException(404, "Justificativo no encontrado")
    return None
