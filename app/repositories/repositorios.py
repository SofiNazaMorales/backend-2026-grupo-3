"""Persistencia de justificativos mediante la sesión recibida por petición."""
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.justificativo import Justificativo
from app.models.justificativo import justificativo_model


def crear_justificativo(db: Session, justificativo: Justificativo) -> justificativo_model:
    nuevo = justificativo_model(
        id_justificativo=justificativo.id_justificativo or str(uuid4()),
        rut_estudiante=justificativo.rut_estudiante,
        id_curso=justificativo.id_curso,
        fecha_inasistencia=justificativo.fecha_inasistencia,
        tipo_inasistencia=justificativo.tipo_inasistencia,
        motivo=justificativo.motivo,
        fecha_registro=justificativo.fecha_registro,
        veces_editado=justificativo.veces_editado,
        estado=justificativo.estado,
    )
    try:
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
    except SQLAlchemyError:
        db.rollback()
        raise
    return nuevo


def listar_justificativos(db: Session) -> list[justificativo_model]:
    return db.query(justificativo_model).all()


def obtener_justificativo_por_id(db: Session, id_justificativo: str) -> justificativo_model | None:
    return db.query(justificativo_model).filter(
        justificativo_model.id_justificativo == id_justificativo
    ).first()


def actualizar_justificativo(db: Session, id_justificativo: str, cambios: dict) -> justificativo_model | None:
    actual = obtener_justificativo_por_id(db, id_justificativo)
    if actual is None:
        return None
    campos_editables = {"fecha_inasistencia", "tipo_inasistencia", "motivo", "veces_editado"}
    try:
        for campo, valor in cambios.items():
            if campo in campos_editables and valor is not None:
                setattr(actual, campo, valor)
        db.commit()
        db.refresh(actual)
    except SQLAlchemyError:
        db.rollback()
        raise
    return actual


def eliminar_justificativo(db: Session, id_justificativo: str) -> bool:
    actual = obtener_justificativo_por_id(db, id_justificativo)
    if actual is None:
        return False
    try:
        db.delete(actual)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    return True
