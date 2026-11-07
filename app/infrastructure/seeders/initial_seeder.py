
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
    """
    Carga los registros iniciales del proyecto.
    Comprueba cada registro para evitar duplicados.
    """

    carrera_repo = CarreraRepository(session)
    curso_repo = CursoRepository(session)
    estudiante_repo = EstudianteRepository(session)
    justificativo_repo = JustificativoRepository(session)

    # --------------------------------------------------
    # CARRERAS
    # --------------------------------------------------

    c1 = carrera_repo.obtener_por_id("ICI-INF")

    if c1 is None:
        c1 = carrera_repo.crear(
            Carrera(
                id_carrera="ICI-INF",
                codigo="PLAN-2023-INF",
                nombre_carrera="Ingeniería Civil Informática",
                duracion_semestre=10,
                facultad=Facultad.INGENIERIA,
            )
        )

    c2 = carrera_repo.obtener_por_id("ICI-IND")

    if c2 is None:
        c2 = carrera_repo.crear(
            Carrera(
                id_carrera="ICI-IND",
                codigo="PLAN-2023-IND",
                nombre_carrera="Ingeniería Civil Industrial",
                duracion_semestre=10,
                facultad=Facultad.INGENIERIA,
            )
        )

    # --------------------------------------------------
    # CURSOS
    # --------------------------------------------------

    cu1 = curso_repo.obtener_por_id("CRS-INF1108")

    if cu1 is None:
        cu1 = curso_repo.crear(
            Curso(
                id_curso="CRS-INF1108",
                codigo_curso="INF-1108",
                nombre_curso="Desarrollo de Backend",
                semestre=2,
                id_carrera=c1.id_carrera,
            )
        )

    cu2 = curso_repo.obtener_por_id("CRS-INF1101")

    if cu2 is None:
        cu2 = curso_repo.crear(
            Curso(
                id_curso="CRS-INF1101",
                codigo_curso="INF-1101",
                nombre_curso="Arquitectura de Redes",
                semestre=4,
                id_carrera=c1.id_carrera,
            )
        )

    # --------------------------------------------------
    # ESTUDIANTES
    # --------------------------------------------------

    e1 = estudiante_repo.obtener_por_id("20.123.554-5")

    if e1 is None:
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

    e2 = estudiante_repo.obtener_por_id("19.876.543-0")

    if e2 is None:
        e2 = estudiante_repo.crear(
            Estudiante(
                rut_estudiante="19.876.543-0",
                nombre="María",
                apellido="López",
                email_institucional="mlopez2025@alu.uct.cl",
                id_carrera=c2.id_carrera,
                estado_alumno=True,
            )
        )

    # --------------------------------------------------
    # JUSTIFICATIVOS
    # --------------------------------------------------

    j1 = justificativo_repo.obtener_por_id("JUS-001")

    if j1 is None:
        justificativo_repo.crear(
            Justificativo(
                id_justificativo="JUS-001",
                rut_estudiante=e1.rut_estudiante,
                id_curso=cu1.id_curso,
                fecha_inasistencia=date.today(),
                tipo_inasistencia=TipoInasistencia.CLASE,
                motivo="Lo que sucedió es que me enfermé durante el fin de semana",
                fecha_registro=date.today(),
                estado=EstadoJustificativo.PENDIENTE,
            )
        )

    j2 = justificativo_repo.obtener_por_id("JUS-002")

    if j2 is None:
        justificativo_repo.crear(
            Justificativo(
                id_justificativo="JUS-002",
                rut_estudiante=e2.rut_estudiante,
                id_curso=cu2.id_curso,
                fecha_inasistencia=date.today(),
                tipo_inasistencia=TipoInasistencia.EVALUACION,
                motivo=(
                    "Hola buenas tardes, me ausenté a la evaluación "
                    "por motivos familiares de fuerza mayor, "
                    "comprobable mediante certificado."
                ),
                fecha_registro=date.today(),
                estado=EstadoJustificativo.PENDIENTE,
            )
        )

    print("Seeder ejecutado correctamente.")
