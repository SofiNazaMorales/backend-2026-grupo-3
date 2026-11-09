from datetime import date, timedelta
from app.mappers import justificativo_a_dict
from app.domain.justificativo import Justificativo
from app.domain.enums import TipoInasistencia
from app.infrastructure.repositories import justificativo_repository as repo


MAX_EDICIONES_JUSTIFICATIVO = 2
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


def crear_justificativo(db, data: dict) -> dict:
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
        id_justificativo=None, 
        rut_estudiante=data["rut_estudiante"],
        id_curso=data["id_curso"],
        fecha_inasistencia=data["fecha_inasistencia"],
        tipo_inasistencia=data["tipo_inasistencia"],
        motivo=data["motivo"],
        fecha_registro=hoy,
    )
    creado = repo.crear_justificativo(db, nuevo)
    return justificativo_a_dict(creado)


def editar_justificativo(db, id_justificativo: str, cambios: dict) -> dict:
    actual = repo.obtener_justificativo_por_id(db, id_justificativo, bloquear=True)
    if actual is None:
        raise ReglaDeNegocioError(
            "NOT_FOUND", "No existe un justificativo con el ID solicitado"
        )

    if actual.veces_editado >= MAX_EDICIONES_JUSTIFICATIVO:
        raise ReglaDeNegocioError(
            "EDIT_LIMIT_REACHED",
            f"El justificativo ya alcanzó el máximo de {MAX_EDICIONES_JUSTIFICATIVO} ediciones",
        )

    fecha = cambios.get("fecha_inasistencia", actual.fecha_inasistencia)
    tipo = cambios.get("tipo_inasistencia", actual.tipo_inasistencia)
    if fecha > date.today():
        raise ReglaDeNegocioError("INVALID_DATE", "La fecha no puede ser futura")
    if tipo == TipoInasistencia.EVALUACION and _dias_habiles_entre(fecha, date.today()) > PLAZO_DIAS_HABILES_JUSTIFICATIVO:
        raise ReglaDeNegocioError("DEADLINE_EXCEEDED", "El plazo de evaluación venció")
    cambios["veces_editado"] = actual.veces_editado + 1
    actualizado = repo.actualizar_justificativo(db, id_justificativo, cambios)
    return justificativo_a_dict(actualizado)


def eliminar_justificativo(db, id_justificativo: str) -> bool:
    return repo.eliminar_justificativo(db, id_justificativo)


def obtener_justificativo(db, id_justificativo: str) -> dict | None:
    encontrado = repo.obtener_justificativo_por_id(db, id_justificativo)
    return justificativo_a_dict(encontrado) if encontrado else None


def listar_justificativos_con_filtros(
    db,
    id_curso: str | None = None,
    estado: str | None = None,
    tipo_inasistencia: str | None = None,
    ordenar_por: str = "fecha_inasistencia",
    direccion: str = "asc",
    pagina: int = 1,
    limite: int = 20,
) -> tuple[list[dict], int]:
    items, total = repo.consultar_pagina(db, id_curso, estado, tipo_inasistencia,
                                        ordenar_por, direccion, pagina, limite)
    return [justificativo_a_dict(item) for item in items], total
