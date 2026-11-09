from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import select, func
from app.main import app
from app.infrastructure.database import get_db, SessionLocal
from app.infrastructure.models import CarreraModel, CursoModel, EstudianteModel, JustificativoModel
from app.infrastructure.seeders.initial_seeder import ejecutar_seeders

def client(db):
    ejecutar_seeders(db)
    def dependency():
        yield db
    app.dependency_overrides[get_db] = dependency
    return TestClient(app)

def datos(**cambios):
    value = dict(rut_estudiante="20.123.554-5",id_curso="CRS-INF1108",fecha_inasistencia=date.today().isoformat(),tipo_inasistencia="Clase Regular",motivo="Justificación válida para pruebas")
    value.update(cambios)
    return value

def test_seed_repetible_y_dos_por_entidad(db):
    ejecutar_seeders(db)
    ejecutar_seeders(db)
    for model in (CarreraModel,CursoModel,EstudianteModel,JustificativoModel):
        assert db.scalar(select(func.count()).select_from(model)) == 2

def test_crud_estudiantes_y_conflicto(db):
    with client(db) as api:
        body=dict(rut_estudiante="12345678-5",nombre="Ana",apellido="Prueba",email_institucional="ana.prueba@alu.uct.cl",id_carrera="ICI-INF")
        assert api.post("/estudiantes",json=body).status_code == 201
        assert api.post("/estudiantes",json=body).status_code == 409
        assert api.get("/estudiantes/12345678-5").status_code == 200
        assert api.put("/estudiantes/12345678-5",json={"nombre":"Ana María"}).json()["data"]["nombre"] == "Ana María"
        result=api.delete("/estudiantes/12345678-5")
        assert result.status_code == 204 and result.content == b""
        assert api.get("/estudiantes/12345678-5").status_code == 404

def test_crud_cursos_reales(db):
    with client(db) as api:
        body=dict(id_curso="CRS-TEST",codigo_curso="TST-001",nombre_curso="Curso de prueba",semestre=2,id_carrera="ICI-INF")
        assert api.post("/cursos",json=body).status_code == 201
        assert api.get("/cursos/CRS-TEST").json()["data"]["nombre_curso"] == "Curso de prueba"
        assert api.put("/cursos/CRS-TEST",json={"semestre":3}).json()["data"]["semestre"] == 3

def test_justificativo_persistido_nueva_sesion(db):
    with client(db) as api:
        response=api.post("/justificativos",json=datos())
        assert response.status_code == 201, response.text
        pk=response.json()["data"]["id_justificativo"]
        with SessionLocal() as otra:
            assert otra.get(JustificativoModel,pk) is not None
        assert api.get("/justificativos/"+pk).status_code == 200

def test_reglas_validacion_filtros_y_eliminacion(db):
    with client(db) as api:
        assert api.post("/justificativos",json=datos(motivo="Mal")).status_code == 422
        assert api.post("/justificativos",json=datos(fecha_inasistencia=(date.today()+timedelta(days=1)).isoformat())).status_code == 422
        assert api.post("/justificativos",json=datos(fecha_inasistencia=(date.today()-timedelta(days=20)).isoformat(),tipo_inasistencia="Evaluación")).status_code == 400
        response=api.post("/justificativos",json=datos())
        pk=response.json()["data"]["id_justificativo"]
        result=api.get("/justificativos",params={"id_curso":"CRS-INF1108","tipo_inasistencia":"Clase Regular","pagina":1,"limite":1}).json()["data"]
        assert len(result["items"]) == 1 and result["total"] >= 2
        assert api.get("/justificativos?pagina=0").status_code == 422
        assert api.get("/justificativos?ordenar_por=inexistente").status_code == 422
        for edits in (1,2):
            result=api.put("/justificativos/"+pk,json={"motivo":"Motivo corregido de prueba"})
            assert result.status_code == 200 and result.json()["data"]["veces_editado"] == edits
        assert api.put("/justificativos/"+pk,json={"motivo":"Tercera modificación de prueba"}).status_code == 400
        assert api.delete("/justificativos/"+pk).status_code == 204
        assert api.get("/justificativos/"+pk).status_code == 404
        assert api.delete("/justificativos/"+pk).status_code == 404

def test_fk_rollback_no_rompe_sesion(db):
    with client(db) as api:
        assert api.post("/justificativos",json=datos(id_curso="NO-EXISTE")).status_code == 409
        assert api.post("/justificativos",json=datos()).status_code == 201
        assert api.delete("/estudiantes/20.123.554-5").status_code == 409
        assert api.get("/estudiantes/20.123.554-5").status_code == 200
