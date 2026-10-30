from dataclasses import dataclass
from datetime import date
from .enums import EstadoJustificativo, TipoInasistencia

@dataclass
class Justificativo:
    """
    Entidad de Dominio: Justificativo.
    Representa el aviso del Estudiante ante la falta de una clase o evaluación.

    Relación de Dominio:
    - Un Estudiante puede generar muchos Justificativos (1:N) y a la vez,
    un Curso puede tener muchos Justificativos (1:N) generados por Estudiantes diferentes,
    - rut_estudiante e id_curso actúan como las Claves Foráneas (FK) de la clase
    justificativo, referenciando a estudiante.rut_estudiante y curso.id_curso
    """
    
    id_justificativo: str | None
    rut_estudiante: str
    id_curso: str
    fecha_inasistencia: date
    tipo_inasistencia : TipoInasistencia
    motivo: str
    fecha_registro: date | None = None
    veces_editado: int = 0
    estado: EstadoJustificativo = EstadoJustificativo.PENDIENTE

    def __post_init__(self) -> None:

        self.rut_estudiante = self.rut_estudiante.strip().upper()
        self.id_curso = self.id_curso.strip().upper()

        if not self.motivo or len(self.motivo.strip()) < 10:
            raise ValueError("El motivo debe tener al menos 10 caracteres explícitos.")

        if self.fecha_inasistencia > date.today():
            raise ValueError("La fecha de inasistencia no puede ser una fecha futura.")

    def aceptar(self) -> None:
        if self.estado == EstadoJustificativo.RECHAZADO:
            raise ValueError("No se puede aceptar un justificativo que ya fue rechazado.")
        self.estado = EstadoJustificativo.ACEPTADO

    def rechazar(self) -> None:
        self.estado = EstadoJustificativo.RECHAZADO