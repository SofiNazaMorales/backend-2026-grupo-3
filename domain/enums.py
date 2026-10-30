from enum import Enum

class TipoInasistencia(str, Enum):
    CLASE = "Clase Regular"
    EVALUACION = "Evaluación"

class EstadoJustificativo(str, Enum):
    PENDIENTE = "Pendiente"
    ACEPTADO = "Aceptado"
    RECHAZADO = "Rechazado"

class Facultad(str, Enum):
    INGENIERIA = "Facultad de Ingeniería"
    HUMANIDADES = "Facultad de Humanidades"
    SALUD = "Facultad de Ciencias de la Salud"
    CIENCIAS_POLITICAS = "Facultad de Ciencias Políticas"
