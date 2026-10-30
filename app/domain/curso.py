from dataclasses import dataclass

@dataclass
class Curso:
    """
    Entidad de Dominio: Curso.
    (Representa la asignatura o ramo académico)

    Relación de Dominio:
    - Una Carrera tiene muchos Cursos (1:N).
    - id_carrera representa la Clave Foránea (FK), referenciando a carrera.id_carrera.
    """
        
    id_curso: str
    codigo_curso: str
    nombre_curso: str
    semestre: int
    id_carrera: str

    def __post_init__(self) -> None:

        self.id_curso = self.id_curso.strip().upper()
        self.codigo_curso = self.codigo_curso.strip().upper()
        self.nombre_curso = self.nombre_curso.strip()
        self.id_carrera = self.id_carrera.strip().upper()

        if not self.id_curso:
            raise ValueError("El ID del curso es obligatorio.")

        if not self.codigo_curso:
            raise ValueError("El código del curso es obligatorio.")

        if not self.nombre_curso:
            raise ValueError("El nombre el curso no puede estar vacío.")

        if self.semestre < 1 or self.semestre > 14:
            raise ValueError("El semestre del curso debe estar en un rango válido entre 1 y 14.")