from datetime import date
from enum import Enum
from typing import Optional

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

class Carrera:
    def __init__(self, 
                 id_carrera: str, 
                 codigo: str, 
                 nombre_carrera: str, 
                 facultad: Facultad, 
                 duracion_semestre: int
                 ):
         self.id_carrera = id_carrera
         self.codigo = codigo
         self.nombre_carrera = nombre_carrera
         self.facultad = facultad
         self.duracion_semestre = duracion_semestre


class Estudiante:
    def __init__(self, 
                 rut_estudiante: str, 
                 nombre: str, 
                 apellido: str, 
                 email_institucional: str, 
                 id_carrera: str, 
                 estado_alumno: bool = True
                 ):
         self.rut_estudiante = rut_estudiante
         self.nombre = nombre
         self.apellido = apellido
         self.email_institucional = email_institucional
         self.id_carrera = id_carrera
         self.estado_alumno = estado_alumno

class Curso:
    def __init__(self, 
                 id_curso: str, 
                 codigo_curso: str, 
                 nombre_curso: str, 
                 semestre: int, 
                 id_carrera: str
                 ):
         self.id_curso = id_curso
         self.codigo_curso = codigo_curso
         self.nombre_curso = nombre_curso
         self.semestre = semestre
         self.id_carrera = id_carrera

class Justificativo:
    def __init__(self, 
                 id_justificativo: int, 
                 rut_estudiante: str, 
                 id_curso: str, 
                 fecha_inasistencia: date, 
                 tipo_inasistencia: TipoInasistencia, 
                 estado: EstadoJustificativo.PENDIENTE
                 ):
         self.id_justificativo = id_justificativo
         self.rut_estudiante = rut_estudiante
         self.id_curso = id_curso
         self.fecha_inasistencia = fecha_inasistencia
         self.tipo_inasistencia = tipo_inasistencia
         self.estado = estado
