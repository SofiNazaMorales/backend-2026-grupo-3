from app.domain.errores import ErrorAplicacion
from app.domain.carrera import Carrera

class CarreraService:
    def __init__(self, repository):
        self.repository = repository

    def listar(self):
        return self.repository.listar()

    def obtener(self, id_carrera):
        item = self.repository.obtener_por_id(id_carrera.upper())
        if item is None:
            raise ErrorAplicacion(404, "Carrera no encontrada")
        return item

    def crear(self, datos):
        item = Carrera(**datos.model_dump())
        if self.repository.obtener_por_id(item.id_carrera):
            raise ErrorAplicacion(409, "Ya existe una carrera con ese ID")
        return self.repository.crear(item)
