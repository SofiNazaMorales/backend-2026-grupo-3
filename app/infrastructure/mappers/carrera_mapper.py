from app.domain.carrera import Carrera
from app.domain.enums import Facultad
from app.infrastructure.models.carrera_model import CarreraModel

def carrera_a_dominio(modelo: CarreraModel) -> Carrera:
    
    return Carrera(
        id_carrera=modelo.id_carrera,
        codigo=modelo.codigo,
        nombre_carrera=modelo.nombre_carrera,
        duracion_semestre=modelo.duracion_semestre,
        facultad=Facultad(modelo.facultad) if isinstance(modelo.facultad, str) else modelo.facultad,
    )


def carrera_a_modelo(dominio: Carrera) -> CarreraModel:
    
    return CarreraModel(
        id_carrera=dominio.id_carrera,
        codigo=dominio.codigo,
        nombre_carrera=dominio.nombre_carrera,
        duracion_semestre=dominio.duracion_semestre,
        facultad=dominio.facultad.value if hasattr(dominio.facultad, 'value') else str(dominio.facultad),
    )