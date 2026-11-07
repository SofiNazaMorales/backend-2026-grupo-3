
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domain.justificativo import Justificativo
from app.infrastructure.models.justificativo_model import JustificativoModel
from app.infrastructure.mappers.justificativo_mapper import (
    justificativo_a_dominio,
    justificativo_a_modelo,
)


def crear_justificativo(
    db: Session,
    justificativo: Justificativo
) -> Justificativo:
    """Agrega un justificativo a la transacción actual."""

    if justificativo.id_justificativo is None:
        justificativo.id_justificativo = str(uuid4())

    nuevo = justificativo_a_modelo(justificativo)

    db.add(nuevo)
    db.flush()
    db.refresh(nuevo)

    return justificativo_a_dominio(nuevo)


def listar_justificativos(db: Session) -> list[Justificativo]:
    """Obtiene todos los justificativos."""

    modelos = db.query(JustificativoModel).all()

    return [
        justificativo_a_dominio(modelo)
        for modelo in modelos
    ]


def obtener_justificativo_por_id(
    db: Session,
    id_justificativo: str
) -> Justificativo | None:
    """Busca un justificativo por su identificador."""

    modelo = db.get(JustificativoModel, id_justificativo)

    if modelo is None:
        return None

    return justificativo_a_dominio(modelo)


def actualizar_justificativo(
    db: Session,
    id_justificativo: str,
    cambios: dict
) -> Justificativo | None:
    """Actualiza un justificativo dentro de la transacción actual."""

    actual = db.get(JustificativoModel, id_justificativo)

    if actual is None:
        return None

    campos_editables = {
        "fecha_inasistencia",
        "tipo_inasistencia",
        "motivo",
        "veces_editado",
    }

    for campo, valor in cambios.items():
        if campo in campos_editables and valor is not None:
            if campo == "tipo_inasistencia" and hasattr(valor, "value"):
                valor = valor.value

            setattr(actual, campo, valor)

    db.flush()
    db.refresh(actual)

    return justificativo_a_dominio(actual)


def eliminar_justificativo(
    db: Session,
    id_justificativo: str
) -> bool:
    """Elimina un justificativo dentro de la transacción actual."""

    actual = db.get(JustificativoModel, id_justificativo)

    if actual is None:
        return False

    db.delete(actual)
    db.flush()

    return True
