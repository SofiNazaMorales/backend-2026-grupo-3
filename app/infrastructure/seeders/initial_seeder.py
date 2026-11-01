from datetime import date
from sqlalchemy.orm import Session
from app.domain.carrera import Carrera
from app.domain.curso import Curso
from app.domain.estudiante import Estudiante
from app.domain.justificativo import Justificativo
from app.domain.enums import Facultad, EstadoJustificativo, TipoInasistencia
from app.infrastructure.repositories.carrera_repository import CarreraRepository
from app.infrastructure.repositories.curso_repository import CursoRepository
from app.infrastructure.repositories.estudiante_repository import EstudianteRepository
from app.infrastructure.repositories.justificativo_repository import JustificativoRepository

def ejecutar_seeders(session: Session) -> None:
    """Cargando los registros iniciales basándose en las entidades de prueba del proyecto."""
    carrera_repo = CarreraRepository(session)
    curso_repo = CursoRepository(session)
    estudiante_repo = EstudianteRepository(session)
    justificativo_repo = JustificativoRepository(session)

    if len(carrera_repo.listar()) > 0:
        print("La base de datos ya contiene registros. Se omite el seeder.")
        return

    # Ejemplos de insertar datos sobre Carreras.
    c1 = carrera_repo.crear(
        Carrera(
            id_carrera="ICI-INF",
            codigo="PLAN-2023-INF",
            nombre_carrera="Ingeniería Civil Informatica",
            duracion_semestre=10,
            facultad=Facultad.INGENIERIA,
        )
    )
    c2 = carrera_repo.crear(
        Carrera(
            id_carrera="ICI-IND",
            codigo="PLAN-2023-IND",
            nombre_carrera="Ingeniería Civil Industrial",
            duracion_semestre=10,
            facultad=Facultad.INGENIERIA,
        )
    )

    # Ejemplos de insertar datos sobre Cursos.
    cu1 = curso_repo.crear(
        Curso(
            id_curso="CRS-INF1108", 
            codigo_curso="INF-1108",
            nombre_curso="Desarrollo de Backend",
            semestre=2,
            id_carrera=c1.id_carrera,
            )
    )
    cu2 = curso_repo.crear(
        Curso(id_curso="CRS-INF1101", 
              codigo_curso="INF-1101",
              nombre_curso="Arquitectura de Redes",
              semestre=4,
                id_carrera=c1.id_carrera,
              )
    )

    # Ejemplos de insertar datos sobre Estudiantes.
    e1 = estudiante_repo.crear(
        Estudiante(
            rut_estudiante="20.123.554-5",
            nombre="Roberto",
            apellido="Díaz",
            email_institucional="rdiaz2026@alu.uct.cl",
            id_carrera=c1.id_carrera,
            estado_alumno=True,
        )
    )
    e2 = estudiante_repo.crear(
        Estudiante(
            rut_estudiante="19.876.543-2",
            nombre="María",
            apellido="López",
            email_institucional="mlopez2025@alu.uct.cl",
            id_carrera=c2.id_carrera,
            estado_alumno=True,
        )
    )

    # Ejemplos de insertar datos sobre Justificativos.
    justificativo_repo.crear(
        Justificativo(
            id_justificativo="JUS-001",
            rut_estudiante=e1.rut_estudiante,
            id_curso=cu1.id_curso,
            fecha_inasistencia=date.today(),
            tipo_inasistencia=TipoInasistencia.CLASE,
            motivo="Lo dque sucedio es que me ewnfermé duranté el fin de smana",
            fecha_registro=date.today(),
            estado=EstadoJustificativo.PENDIENTE,
        )
    )
    justificativo_repo.crear(
        Justificativo(
            id_justificativo="JUS-002",
            rut_estudiante=e2.rut_estudiante,
            id_curso=cu2.id_curso,
            fecha_inasistencia=date.today(),
            tipo_inasistencia=TipoInasistencia.EVALUACION,
            motivo="Hola buenas tardes, me ausente a la evaluación por motivos familiares de fuerza mayor, comprobable mediante certificado.",
            fecha_registro=date.today(),
            estado=EstadoJustificativo.PENDIENTE,
        )
    )

    print("¡Seeder ejecutable con éxito! Datos alineados a las entidades de domain.")