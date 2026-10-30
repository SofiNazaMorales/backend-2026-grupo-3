from .enums import EstadoJustificativo, TipoInasistencia
from datetime import date
from typing import Optional

class Justificativo:
    def __init__(
            self,
            id_justificativo: str,
            rut_estudiante: str,
            id_curso: str,
            fecha_inasistencia: date,
            tipo_inasistencia : TipoInasistencia,
            motivo: str,
            fecha_registro: Optional[date] = None,
            veces_editado: int = 0,
            estado: EstadoJustificativo = EstadoJustificativo.PENDIENTE,
                 ):
         self.id_justificativo = id_justificativo
         self.rut_estudiante = rut_estudiante
         self.id_curso = id_curso
         self.fecha_inasistencia = fecha_inasistencia
         self.tipo_inasistencia = tipo_inasistencia
         self.estado = estado
         self.motivo = motivo
         self.fecha_registro = fecha_registro or date.today()
         self.veces_editado = veces_editado

    def __repr__(self) -> str:
        return f"<Justificativo {self.id_justificativo} [{self.estado.value}]>"