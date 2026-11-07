from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.mappers import justificativo_a_dict
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

def crear_justificativo(db: Session, data: dict) -> dict:
    hoy = date.today()

    if data["fecha_inasistencia"] > hoy:
        raise ReglaDeNegocioError(
            "INVALID_DATE",
            "fecha_inasistencia: no puede ser una fecha futura"
        )

    if data["tipo_inasistencia"] == TipoInasistencia.EVALUACION:
        dias_transcurridos = _dias_habiles_entre(
            data["fecha_inasistencia"], hoy
        )

        if dias_transcurridos > PLAZO_DIAS_HABILES_JUSTIFICATIVO:
            raise ReglaDeNegocioError(
                "DEADLINE_EXCEEDED",
                f"El plazo de {PLAZO_DIAS_HABILES_JUSTIFICATIVO} días hábiles para justificar venció"
            )

    nuevo = Justificativo(
        id_justificativo=None,
        rut_estudiante=data["rut_estudiante"],
        id_curso=data["id_curso"],
        fecha_inasistencia=data["fecha_inasistencia"],
        tipo_inasistencia=data["tipo_inasistencia"],
        motivo=data["motivo"],
        fecha_registro=hoy,
    )

    try:
        creado = repo.crear_justificativo(db, nuevo)
        db.commit()
        return justificativo_a_dict(creado)

    except Exception:
        db.rollback()
        raise
def editar_justificativo(
    db: Session,
    id_justificativo: str,
    cambios: dict
) -> dict:

    try:
        actual = repo.obtener_justificativo_por_id(
            db, id_justificativo
        )

        if actual is None:
            raise ReglaDeNegocioError(
                "NOT_FOUND",
                "No existe un justificativo con el ID solicitado"
            )

        if actual.veces_editado >= MAX_EDICIONES_JUSTIFICATIVO:
            raise ReglaDeNegocioError(
                "EDIT_LIMIT_REACHED",
                f"El justificativo ya alcanzó el máximo de {MAX_EDICIONES_JUSTIFICATIVO} ediciones"
            )

        cambios["veces_editado"] = actual.veces_editado + 1

        actualizado = repo.actualizar_justificativo(
            db, id_justificativo, cambios
        )

        db.commit()

        return justificativo_a_dict(actualizado)

    except Exception:
        db.rollback()
        raise

def eliminar_justificativo(
    db: Session,
    id_justificativo: str
) -> bool:

    try:
        eliminado = repo.eliminar_justificativo(
            db, id_justificativo
        )

        db.commit()

        return eliminado

    except Exception:
        db.rollback()
        raise

def obtener_justificativo(db: Session, id_justificativo: str) -> dict | None:
    encontrado = repo.obtener_justificativo_por_id(db, id_justificativo)
    return justificativo_a_dict(encontrado) if encontrado else None


def listar_justificativos_con_filtros(
    db: Session,
    id_curso: str | None = None,
    estado: str | None = None,
    tipo_inasistencia: str | None = None,
    ordenar_por: str = "fecha_inasistencia",
    direccion: str = "asc",
    pagina: int = 1,
    limite: int = 20,
) -> tuple[list[dict], int]:
    items = [justificativo_a_dict(j) for j in repo.listar_justificativos(db)]

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