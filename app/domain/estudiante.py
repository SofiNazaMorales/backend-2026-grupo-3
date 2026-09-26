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

    def __repr__(self) -> str:
        return f"<Estudiante {self.rut_estudiante}>"
