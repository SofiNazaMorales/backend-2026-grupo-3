from datetime import date
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.infrastructure.models import CarreraModel, CursoModel, EstudianteModel, JustificativoModel

def ejecutar_seeders(session: Session) -> None:
    """Carga idempotente: completa los registros faltantes sin borrar ni duplicar."""
    with session.begin():
        for id_,codigo,nombre in [("ICI-INF","PLAN-2023-INF","Ingeniería Civil Informatica"),("ICI-IND","PLAN-2023-IND","Ingeniería Civil Industrial")]:
            if session.get(CarreraModel,id_) is None:
                session.add(CarreraModel(id_carrera=id_,codigo=codigo,nombre_carrera=nombre,duracion_semestre=10,facultad="Facultad de Ingeniería"))
        session.flush()
        for id_,codigo,nombre,semestre in [("CRS-INF1108","INF-1108","Desarrollo de Backend",2),("CRS-INF1101","INF-1101","Arquitectura de Redes",4)]:
            if session.get(CursoModel,id_) is None:
                session.add(CursoModel(id_curso=id_,codigo_curso=codigo,nombre_curso=nombre,semestre=semestre,id_carrera="ICI-INF"))
        for rut,nombre,apellido,correo,carrera in [("20.123.554-5","Roberto","Díaz","rdiaz2026@alu.uct.cl","ICI-INF"),("19.876.543-2","María","López","mlopez2025@alu.uct.cl","ICI-IND")]:
            if session.get(EstudianteModel,rut) is None:
                session.add(EstudianteModel(rut_estudiante=rut,nombre=nombre,apellido=apellido,email_institucional=correo,id_carrera=carrera,estado_alumno=True))
        session.flush()
        for pk,rut,curso,tipo in [("JUS-001","20.123.554-5","CRS-INF1108","Clase Regular"),("JUS-002","19.876.543-2","CRS-INF1101","Evaluación")]:
            if session.get(JustificativoModel,pk) is None:
                session.add(JustificativoModel(id_justificativo=pk,rut_estudiante=rut,id_curso=curso,fecha_inasistencia=date.today(),tipo_inasistencia=tipo,motivo=("Lo dque sucedio es que me ewnfermé duranté el fin de smana" if pk == "JUS-001" else "Hola buenas tardes, me ausente a la evaluación por motivos familiares de fuerza mayor, comprobable mediante certificado."),fecha_registro=date.today(),veces_editado=0,estado="Pendiente"))
    for modelo in (CarreraModel,CursoModel,EstudianteModel,JustificativoModel):
        print(f"{modelo.__tablename__}: {session.scalar(select(func.count()).select_from(modelo))} registros")
    session.rollback()  # Cierra la transacción de lectura de los conteos.
    print("Seeder completado correctamente")
