
from math import ceil

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.estudiante import Estudiante

from app.infrastructure.repositories.estudiante_repository import (
    EstudianteRepository,
)
from app.infrastructure.repositories.carrera_repository import (
    CarreraRepository,
)
from app.infrastructure.repositories.justificativo_repository import (
    JustificativoRepository,
)

from app.schemas.estudiante_dto import (
    EstudianteCreateDTO,
    EstudianteUpdateDTO,
    EstudianteResponseDTO,
    EstudiantePaginaDTO,
)
from app.schemas.estudiante_query_dto import EstudianteQueryDTO


class EstudianteService:

    def __init__(self, session: Session):
        self.session = session
        self.repository = EstudianteRepository(session)
        self.carrera_repository = CarreraRepository(session)
        self.justificativo_repository = JustificativoRepository(session)

    def crear_estudiante(
        self,
        datos: EstudianteCreateDTO
    ) -> Estudiante:

        if self.repository.obtener_por_id(datos.rut_estudiante):
            raise HTTPException(
                status_code=409,
                detail="Ya existe un estudiante con ese RUT."
            )

        if self.repository.obtener_por_email(
            str(datos.email_institucional)
        ):
            raise HTTPException(
                status_code=409,
                detail="Ya existe un estudiante con ese correo institucional."
            )

        carrera = self.carrera_repository.obtener_por_id(
            datos.id_carrera
        )

        if carrera is None:
            raise HTTPException(
                status_code=404,
                detail="La carrera indicada no existe."
            )

        estudiante = Estudiante(
            rut_estudiante=datos.rut_estudiante,
            nombre=datos.nombre,
            apellido=datos.apellido,
            email_institucional=str(datos.email_institucional),
            id_carrera=datos.id_carrera,
        )

        try:
            nuevo = self.repository.crear(estudiante)
            self.session.commit()
            return nuevo

        except IntegrityError as error:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="No se pudo registrar el estudiante por un conflicto de integridad."
            ) from error

        except Exception:
            self.session.rollback()
            raise

    def obtener_estudiante(self, rut_estudiante: str) -> Estudiante:

        estudiante = self.repository.obtener_por_id(rut_estudiante)

        if estudiante is None:
            raise HTTPException(
                status_code=404,
                detail="No existe un estudiante con el RUT indicado."
            )

        return estudiante

    def actualizar_estudiante(
        self,
        rut_estudiante: str,
        datos: EstudianteUpdateDTO
    ) -> Estudiante:

        existente = self.repository.obtener_por_id(rut_estudiante)

        if existente is None:
            raise HTTPException(
                status_code=404,
                detail="No existe un estudiante con el RUT indicado."
            )

        cambios = datos.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        nuevo_email = cambios.get(
            "email_institucional",
            existente.email_institucional
        )

        email_existente = self.repository.obtener_por_email(
            str(nuevo_email),
            excluir_rut=rut_estudiante
        )

        if email_existente is not None:
            raise HTTPException(
                status_code=409,
                detail="El correo institucional ya pertenece a otro estudiante."
            )

        nueva_carrera = cambios.get(
            "id_carrera",
            existente.id_carrera
        )

        if self.carrera_repository.obtener_por_id(nueva_carrera) is None:
            raise HTTPException(
                status_code=404,
                detail="La carrera indicada no existe."
            )

        estudiante_actualizado = Estudiante(
            rut_estudiante=existente.rut_estudiante,
            nombre=cambios.get("nombre", existente.nombre),
            apellido=cambios.get("apellido", existente.apellido),
            email_institucional=str(nuevo_email),
            id_carrera=nueva_carrera,
            estado_alumno=cambios.get(
                "estado_alumno",
                existente.estado_alumno
            ),
        )

        try:
            actualizado = self.repository.actualizar(
                estudiante_actualizado
            )

            self.session.commit()

            return actualizado

        except IntegrityError as error:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="No se pudo actualizar el estudiante por un conflicto de integridad."
            ) from error

        except Exception:
            self.session.rollback()
            raise

    def eliminar_estudiante(self, rut_estudiante: str) -> dict:

        estudiante = self.repository.obtener_por_id(rut_estudiante)

        if estudiante is None:
            raise HTTPException(
                status_code=404,
                detail="No existe un estudiante con el RUT indicado."
            )

        if self.justificativo_repository.existen_por_estudiante(
            rut_estudiante
        ):
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar el estudiante porque tiene justificativos asociados."
            )

        try:
            eliminado = self.repository.eliminar(rut_estudiante)

            if not eliminado:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontró el estudiante para eliminar."
                )

            self.session.commit()

            return {
                "mensaje": "Estudiante eliminado correctamente.",
                "rut_estudiante": rut_estudiante
            }

        except IntegrityError as error:
            self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar el estudiante debido a registros relacionados."
            ) from error

        except Exception:
            self.session.rollback()
            raise

    def listar_estudiantes(
        self,
        filtros: EstudianteQueryDTO
    ) -> EstudiantePaginaDTO:

        estudiantes, total = self.repository.listar_paginado(
            id_carrera=filtros.id_carrera,
            estado_alumno=filtros.estado_alumno,
            ordenar_por=filtros.ordenar_por,
            direccion=filtros.direccion,
            pagina=filtros.pagina,
            limite=filtros.limite,
        )

        total_paginas = ceil(total / filtros.limite) if total else 0

        return EstudiantePaginaDTO(
            items=[
                EstudianteResponseDTO.model_validate(estudiante)
                for estudiante in estudiantes
            ],
            total=total,
            pagina=filtros.pagina,
            limite=filtros.limite,
            total_paginas=total_paginas,
        )
