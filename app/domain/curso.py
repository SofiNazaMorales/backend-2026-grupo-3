class Curso:
    def __init__(
        self,
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

    def __repr__(self) -> str:
        return (
            f"Curso("
            f"id_curso='{self.id_curso}', "
            f"codigo_curso='{self.codigo_curso}', "
            f"nombre_curso='{self.nombre_curso}', "
            f"semestre={self.semestre}, "
            f"id_carrera='{self.id_carrera}'"
            f")"
        )