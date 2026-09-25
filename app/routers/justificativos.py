from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/justificativos", tags=["Justificativos"])


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

    data_prueba = {"items": [], "total": 0, "pagina": pagina, "limite": limite}
    return _envelope(True, data_prueba, None, "Justificativos obtenidos correctamente (datos de prueba)")


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_justificativo():
  
    data_prueba = data_prueba = {"id_justificativo": "0", "estado": "PENDIENTE"}
    return _envelope(True, data_prueba, None, "Justificativo creado correctamente (datos de prueba)")


@router.get("/{id_justificativo}")
def obtener_justificativo(id_justificativo: str, response: Response):
  
    response.status_code = status.HTTP_404_NOT_FOUND
    return _envelope(
        False, None,
        [{"code": "NOT_FOUND", "details": "No existe un justificativo con el ID solicitado"}],
        "Recurso no encontrado (datos de prueba)",
    )


@router.put("/{id_justificativo}")
def actualizar_justificativo(id_justificativo: str):
  
    data_prueba = {"id_justificativo": id_justificativo, "veces_editado": 1}
    return _envelope(True, data_prueba, None, "Justificativo actualizado correctamente (datos de prueba)")


@router.delete("/{id_justificativo}")
def eliminar_justificativo(id_justificativo: str):
    return _envelope(True, None, None, "Justificativo eliminado correctamente")