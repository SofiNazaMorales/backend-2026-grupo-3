from dataclasses import dataclass
from .enums import Facultad

@dataclass
class Carrera:
    """
    Entidad del Dominio: Carrera.
    (Representa la carrera a la que pertenece un estudiante)

    Relación de Dominio:
    - Una Carrera posee muchos Cursos (1:N) y a la vez,
    una Carrera posee muchos Estudiantes (1:N)
    - La ID de esta clase, permite que las clases de carrera y estudiante
    se puedan relacionar por medio de Claves Foráneas en sus atributos.
    """
                 
    id_carrera: str
    codigo: str 
    nombre_carrera: str
    duracion_semestre: int 
    facultad: Facultad

    def __post_init__(self) -> None:

        self.id_carrera = self.id_carrera.strip().upper()
        self.codigo = self.codigo.strip().upper()
        self.nombre_carrera = self.nombre_carrera.strip()

        if not self.id_carrera:
            raise ValueError("El identificador de la carrera es obligatorio.")

        if len(self.codigo) < 5:
            raise ValueError("El código de la carrera debe tener al menos 5 caracteres.")

        if not self.nombre_carrera:
            raise ValueError("El nombre de la carrera no puede estar vacío.")

        if self.duracion_semestre < 1 or self.duracion_semestre > 14:
            raise ValueError("La duración de la carrera debe estar entre 1 y 14 semestres.")