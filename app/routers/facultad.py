from fastapi import APIRouter, Response, status
from app.domain.modelos import Facultad

router = APIRouter(prefix="/facultades", tags=["Facultades"])


def _envelope(success: bool, data=None, error=None, message: str = ""):
    return {"success": success, "data": data, "error": error, "message": message}


@router.get("")
def obtener_facultades():
  
    items = [{"codigo": f.name, "nombre": f.value} for f in Facultad]
    return _envelope(True, {"items": items, "total": len(items)}, None, "Facultades obtenidas correctamente")


@router.get("/{codigo}")
def obtener_facultad(codigo: str, response: Response):
    try:
        facultad = Facultad[codigo]
    except KeyError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return _envelope(
            False, None,
            [{"code": "NOT_FOUND", "details": "No existe una facultad con ese código"}],
            "Recurso no encontrado",
        )
    return _envelope(True, {"codigo": facultad.name, "nombre": facultad.value}, None,
                      "Facultad obtenida correctamente")