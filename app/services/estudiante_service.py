from app.domain.errores import ErrorAplicacion
from app.domain.estudiante import Estudiante
from app.schemas.estudiante_dto import EstudianteCreateDTO, EstudianteUpdateDTO
from app.infrastructure.repositories.estudiante_repository import EstudianteRepository

class EstudianteService:
    def __init__(self, repository: EstudianteRepository):
        self.repository = repository

    def _rut(self, rut: str) -> str:
        try:
            return EstudianteCreateDTO.validar_y_formatear_rut(rut)
        except ValueError as exc:
            raise ErrorAplicacion(422, str(exc)) from exc

    def obtener(self, rut: str) -> Estudiante:
        estudiante = self.repository.obtener_por_id(self._rut(rut))
        if estudiante is None:
            raise ErrorAplicacion(404, "Estudiante no encontrado")
        return estudiante

    def listar(self):
        return self.repository.listar()

    def crear(self, datos: EstudianteCreateDTO):
        if self.repository.obtener_por_id(datos.rut_estudiante) is not None:
            raise ErrorAplicacion(409, "Ya existe un estudiante con ese RUT")
        return self.repository.crear(Estudiante(**datos.model_dump()))

    def actualizar(self, rut: str, datos: EstudianteUpdateDTO):
        actual = self.obtener(rut)
        valores = {"rut_estudiante": actual.rut_estudiante, "nombre": actual.nombre,
                   "apellido": actual.apellido, "email_institucional": actual.email_institucional,
                   "id_carrera": actual.id_carrera, "estado_alumno": actual.estado_alumno}
        valores.update(datos.model_dump(exclude_unset=True, exclude_none=True))
        return self.repository.actualizar(Estudiante(**valores))

    def eliminar(self, rut: str):
        actual = self.obtener(rut)
        self.repository.eliminar(actual.rut_estudiante)
