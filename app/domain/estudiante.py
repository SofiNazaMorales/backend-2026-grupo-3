from dataclasses import dataclass

@dataclass
class Estudiante:
    """
    Entidad de Dominio: Estudiante.
    Representa a la persona que enviará su justificativo.

    Relación de Dominio:
    - Una Carrera tiene muchos estudiantes (1:N).
    - id_carrera actúa como Clave Foránea al igual que la clase curso,
    referenciando a carrera.id_carrera.
    """
                 
    rut_estudiante: str
    nombre: str
    apellido: str
    email_institucional: str
    id_carrera: str
    estado_alumno: bool = True

    def __post_init__(self) -> None:

         
         self.rut_estudiante = self.rut_estudiante.strip().upper()
         self.nombre = self.nombre.strip()
         self.apellido = self.apellido.strip()
         self.email_institucional = self.email_institucional.strip().lower()
         self.id_carrera = self.id_carrera.strip().upper()

         if not self.rut_estudiante or len(self.rut_estudiante) < 8:
              raise ValueError("El RUT del estudiante es inválido o está incompleto.")

         if not self.nombre or not self.apellido:
              raise ValueError("El nombre y apellido del estudiante son obligatorios.")

         if "@" not in self.email_institucional:
              raise ValueError("El correo institucional debe tener un formato de email válido.")

    @property
    def nombre_completo(self) -> str:
         return f"{self.nombre} {self.apellido}"

    def desactivar_estudiante(self) -> None:
         self.estado_alumno = False

    def activar_estudiante(self) -> None:
         self.estado_alumno = True