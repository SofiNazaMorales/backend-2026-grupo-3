from datetime import date
from pydantic import BaseModel, Field
from fastapi import APIRouter, Response, status
from app.domain.enums import TipoInasistencia
from app.services import servicios as service
from app.services.servicios import ReglaDeNegocioError

router = APIRouter(prefix="/justificativos", tags=["Justificativos"])


class JustificativoCreate(BaseModel):
    rut_estudiante: str
    id_curso: str
    fecha_inasistencia: date
    tipo_inasistencia: TipoInasistencia
    motivo: str = Field(min_length=1, max_length=500)


class JustificativoUpdate(BaseModel):
    fecha_inasistencia: date | None = None
    tipo_inasistencia: TipoInasistencia | None = None
    motivo: str | None = Field(default=None, min_length=1, max_length=500)


def _envelope(success: bool, data=None, error=None, message: str = ""):
    return {"success": success, "data": data, "error": error, "message": message}


@router.get("")
def obtener_justificativos(
    id_curso: str | None = None,
    estado: str | None = None,
    tipo_inasistencia: str | None = None,
    ordenar_por: str = "fecha_inasistencia",
    direccion: str = "asc",
    pagina: int = 1,
    limite: int = 20,
):
    items, total = service.listar_justificativos_con_filtros(
        id_curso, estado, tipo_inasistencia, ordenar_por, direccion, pagina, limite
    )
    data = {"items": items, "total": total, "pagina": pagina, "limite": limite}
    return _envelope(True, data, None, "Justificativos obtenidos correctamente")


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_justificativo(payload: JustificativoCreate, response: Response):
    try:
        creado = service.crear_justificativo(payload.model_dump())
    except ReglaDeNegocioError as e:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return _envelope(False, None, [{"code": e.code, "details": e.details}],
                          "La solicitud contiene errores de validación")
    return _envelope(True, creado, None, "Justificativo creado correctamente")


@router.get("/{id_justificativo}")
def obtener_justificativo(id_justificativo: str, response: Response):
    encontrado = service.obtener_justificativo(id_justificativo)
    if encontrado is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return _envelope(False, None,
                          [{"code": "NOT_FOUND", "details": "No existe un justificativo con el ID solicitado"}],
                          "Recurso no encontrado")
    return _envelope(True, encontrado, None, "Justificativo obtenido correctamente")


@router.put("/{id_justificativo}")
def actualizar_justificativo(id_justificativo: str, payload: JustificativoUpdate, response: Response):
    try:
        actualizado = service.editar_justificativo(id_justificativo, payload.model_dump())
    except ReglaDeNegocioError as e:
        response.status_code = (
            status.HTTP_404_NOT_FOUND if e.code == "NOT_FOUND" else status.HTTP_409_CONFLICT
        )
        return _envelope(False, None, [{"code": e.code, "details": e.details}],
                          "No se pudo actualizar el justificativo")
    return _envelope(True, actualizado, None, "Justificativo actualizado correctamente")


@router.delete("/{id_justificativo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_justificativo(id_justificativo: str):
    service.eliminar_justificativo(id_justificativo)
    return None
