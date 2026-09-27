from datetime import date, timedelta
from app.domain.justificativo import Justificativo
from app.domain.enums import TipoInasistencia
from app.repositories import repositorios as repo


MAX_EDICIONES_JUSTIFICATIVO = 2  # TODO: 
PLAZO_DIAS_HABILES_JUSTIFICATIVO = 5


class ReglaDeNegocioError(Exception):
    def __init__(self, code: str, details: str):
        self.code = code
        self.details = details


def _dias_habiles_entre(inicio: date, fin: date) -> int:
    dias = 0
    actual = inicio
    while actual < fin:
        actual += timedelta(days=1)
        if actual.weekday() < 5: 
            dias += 1
    return dias


def _justificativo_a_dict(j: Justificativo) -> dict:
    return {
        "id_justificativo": j.id_justificativo,
        "rut_estudiante": j.rut_estudiante,
        "id_curso": j.id_curso,
        "fecha_inasistencia": j.fecha_inasistencia,
        "tipo_inasistencia": j.tipo_inasistencia,
        "motivo": j.motivo,
        "fecha_registro": j.fecha_registro,
        "veces_editado": j.veces_editado,
        "estado": j.estado,
    }


def crear_justificativo(data: dict) -> dict:
    hoy = date.today()

    if data["fecha_inasistencia"] > hoy:
        raise ReglaDeNegocioError(
            "INVALID_DATE", "fecha_inasistencia: no puede ser una fecha futura"
        )

    if data["tipo_inasistencia"] == TipoInasistencia.EVALUACION:
        dias_transcurridos = _dias_habiles_entre(data["fecha_inasistencia"], hoy)
        if dias_transcurridos > PLAZO_DIAS_HABILES_JUSTIFICATIVO:
            raise ReglaDeNegocioError(
                "DEADLINE_EXCEEDED",
                f"El plazo de {PLAZO_DIAS_HABILES_JUSTIFICATIVO} días hábiles para justificar venció",
            )

    nuevo = Justificativo(
        id_justificativo="", 
        rut_estudiante=data["rut_estudiante"],
        id_curso=data["id_curso"],
        fecha_inasistencia=data["fecha_inasistencia"],
        tipo_inasistencia=data["tipo_inasistencia"],
        motivo=data["motivo"],
    )
    creado = repo.crear_justificativo(nuevo)
    return _justificativo_a_dict(creado)


def editar_justificativo(id_justificativo: str, cambios: dict) -> dict:
    actual = repo.obtener_justificativo_por_id(id_justificativo)
    if actual is None:
        raise ReglaDeNegocioError(
            "NOT_FOUND", "No existe un justificativo con el ID solicitado"
        )

    if actual.veces_editado >= MAX_EDICIONES_JUSTIFICATIVO:
        raise ReglaDeNegocioError(
            "EDIT_LIMIT_REACHED",
            f"El justificativo ya alcanzó el máximo de {MAX_EDICIONES_JUSTIFICATIVO} ediciones",
        )

    cambios["veces_editado"] = actual.veces_editado + 1
    actualizado = repo.actualizar_justificativo(id_justificativo, cambios)
    return _justificativo_a_dict(actualizado)


def eliminar_justificativo(id_justificativo: str) -> bool:
    return repo.eliminar_justificativo(id_justificativo)


def obtener_justificativo(id_justificativo: str) -> dict | None:
    encontrado = repo.obtener_justificativo_por_id(id_justificativo)
    return _justificativo_a_dict(encontrado) if encontrado else None


def listar_justificativos_con_filtros(
    id_curso: str | None = None,
    estado: str | None = None,
    tipo_inasistencia: str | None = None,
    ordenar_por: str = "fecha_inasistencia",
    direccion: str = "asc",
    pagina: int = 1,
    limite: int = 20,
) -> tuple[list[dict], int]:
    items = [_justificativo_a_dict(j) for j in repo.listar_justificativos()]

    if id_curso:
        items = [i for i in items if i["id_curso"] == id_curso]
    if estado:
        items = [i for i in items if i["estado"] == estado]
    if tipo_inasistencia:
        items = [i for i in items if i["tipo_inasistencia"] == tipo_inasistencia]

    items.sort(key=lambda i: i[ordenar_por], reverse=(direccion == "desc"))

    total = len(items)
    inicio = (pagina - 1) * limite
    pagina_items = items[inicio: inicio + limite]
    return pagina_items, total