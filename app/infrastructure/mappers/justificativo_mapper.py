from datetime import date
from app.domain.enums import EstadoJustificativo, TipoInasistencia
from app.domain.justificativo import Justificativo
from app.infrastructure.models.justificativo_model import JustificativoModel

def justificativo_a_dominio(modelo: JustificativoModel) -> Justificativo:
    return Justificativo(
        id_justificativo=modelo.id,
        rut_estudiante=modelo.rut_estudiante,
        id_curso=modelo.id_curso,
        fecha_inasistencia=modelo.fecha_inasistencia,
        tipo_inasistencia=TipoInasistencia(modelo.tipo_inasistencia)
        if isinstance(modelo.tipo_inasistencia, str) 
        else modelo.tipo_inasistencia,
        motivo=modelo.motivo,
        fecha_registro=modelo.fecha_registro,
        veces_editado=modelo.veces_editado,
        estado=EstadoJustificativo(modelo.estado)
        if isinstance(modelo.estado, str) 
        else modelo.estado,
    )


def justificativo_a_modelo(dominio: Justificativo) -> JustificativoModel:
    return JustificativoModel(
        id=dominio.id_justificativo or f"JUS-{dominio.rut_estudiante[:4]}",
        rut_estudiante=dominio.rut_estudiante,
        id_curso=dominio.id_curso,
        fecha_inasistencia=dominio.fecha_inasistencia,
        tipo_inasistencia=dominio.tipo_inasistencia.value
        if hasattr(dominio.tipo_inasistencia, "value")
        else str(dominio.tipo_inasistencia),
        motivo=dominio.motivo,
        fecha_registro=dominio.fecha_registro or date.today(),
        veces_editado=dominio.veces_editado,
        estado=dominio.estado.value 
        if hasattr(dominio.estado, "value") 
        else dominio.estado,
    )