from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.domain.modelos import TipoInasistencia
from app.schemas.justificacion import JustificacionCreate


def test_crear_justificacion_valida():
    justificacion = JustificacionCreate(
        rut_estudiante="20.123.554-5",
        id_curso="CRS-INF1101",
        fecha_inasistencia=date.today(),
        tipo_inasistencia=TipoInasistencia.CLASE,
        motivo="Cita medica de urgencia"
    )

    assert justificacion.rut_estudiante == "20.123.554-5"
    assert justificacion.id_curso == "CRS-INF1101"
    assert justificacion.fecha_inasistencia == date.today()
    assert justificacion.tipo_inasistencia == TipoInasistencia.CLASE
    assert justificacion.motivo == "Cita medica de urgencia"


def test_aceptar_fecha_pasada():
    fecha_pasada = date.today() - timedelta(days=1)

    justificacion = JustificacionCreate(
        rut_estudiante="20.123.554-5",
        id_curso="CRS-INF1101",
        fecha_inasistencia=fecha_pasada,
        tipo_inasistencia=TipoInasistencia.CLASE,
        motivo="Problema de salud"
    )

    assert justificacion.fecha_inasistencia == fecha_pasada


def test_rechazar_fecha_futura():
    fecha_futura = date.today() + timedelta(days=1)

    with pytest.raises(ValidationError):
        JustificacionCreate(
            rut_estudiante="20.123.554-5",
            id_curso="CRS-INF1101",
            fecha_inasistencia=fecha_futura,
            tipo_inasistencia=TipoInasistencia.CLASE,
            motivo="Problema de salud"
        )


def test_rechazar_motivo_muy_corto():
    with pytest.raises(ValidationError):
        JustificacionCreate(
            rut_estudiante="20.123.554-5",
            id_curso="CRS-INF1101",
            fecha_inasistencia=date.today(),
            tipo_inasistencia=TipoInasistencia.CLASE,
            motivo="Mal"
        )


def test_rechazar_tipo_inasistencia_invalido():
    with pytest.raises(ValidationError):
        JustificacionCreate(
            rut_estudiante="20.123.554-5",
            id_curso="CRS-INF1101",
            fecha_inasistencia=date.today(),
            tipo_inasistencia="Vacaciones",
            motivo="Motivo utilizado para realizar la prueba"
        )


def test_crear_justificacion_evaluacion():
    justificacion = JustificacionCreate(
        rut_estudiante="20.123.554-5",
        id_curso="CRS-INF1108",
        fecha_inasistencia=date.today(),
        tipo_inasistencia=TipoInasistencia.EVALUACION,
        motivo="No pudo asistir a la evaluacion"
    )

    assert justificacion.tipo_inasistencia == TipoInasistencia.EVALUACION