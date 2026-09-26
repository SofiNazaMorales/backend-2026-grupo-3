from .enums import Facultad

class Carrera:
    def __init__(self, 
                 id_carrera: str, 
                 codigo: str, 
                 nombre_carrera: str, 
                 duracion_semestre: int,
                 facultad: Facultad,
                 ):
         self.id_carrera = id_carrera
         self.codigo = codigo
         self.nombre_carrera = nombre_carrera
         self.facultad = facultad
         self.duracion_semestre = duracion_semestre

    def __repr__(self) -> str:
        return f"<Carrera {self.id_carrera}>"