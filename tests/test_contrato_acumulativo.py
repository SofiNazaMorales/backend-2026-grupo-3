import socket
import subprocess
import sys
import time
from pathlib import Path
from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_integracion_api import client, datos

@pytest.mark.parametrize("path", ["/justificativos/NO-EXISTE", "/estudiantes/12345678-5", "/carreras/NO-EXISTE", "/facultades/NO-EXISTE", "/ruta-inexistente"])
def test_errores_uniformes(db,path):
    with client(db) as api:
        response=api.get(path)
        assert response.status_code == 404
        error=response.json()["error"]
        assert isinstance(error["code"],str) and isinstance(error["message"],str)
        assert isinstance(error["details"],list)

def test_cuatro_entidades_y_usuarios_originales(db):
    with client(db) as api:
        careers=api.get("/carreras").json()["data"]["items"]
        assert len(careers)==2
        assert api.get("/carreras/ICI-INF").status_code == 200
        student=api.get("/estudiantes/20.123.554-5").json()["data"]
        assert (student["nombre"],student["apellido"],student["email_institucional"]) == ("Roberto","Díaz","rdiaz2026@alu.uct.cl")
        assert api.get("/estudiantes/19.876.543-2").json()["data"]["nombre"]=="María"

def test_filtro_orden_paginacion_y_total_filtrado(db):
    with client(db) as api:
        for n in range(3):
            assert api.post("/justificativos",json=datos(fecha_inasistencia=(date.today()-timedelta(days=n)).isoformat())).status_code==201
        query="/justificativos?id_curso=CRS-INF1108&direccion=desc&ordenar_por=fecha_inasistencia&limite=2"
        first=api.get(query+"&pagina=1").json()["data"]
        second=api.get(query+"&pagina=2").json()["data"]
        assert first["total"]==second["total"]==4
        assert first["total_paginas"]==2
        ids=[x["id_justificativo"] for x in first["items"]+second["items"]]
        assert len(set(ids))==4
        fechas=[x["fecha_inasistencia"] for x in first["items"]+second["items"]]
        assert fechas==sorted(fechas,reverse=True)
        empty=api.get("/justificativos?id_curso=NO-EXISTE").json()["data"]
        assert empty["total"]==empty["total_paginas"]==0 and empty["items"]==[]

def test_reglas_al_editar_y_actualizacion_vacia(db):
    with client(db) as api:
        created=api.post("/justificativos",json=datos()).json()["data"]
        path="/justificativos/"+created["id_justificativo"]
        assert api.put(path,json={}).status_code==422
        assert api.put(path,json={"motivo":None}).status_code==422
        assert api.put(path,json={"fecha_inasistencia":(date.today()+timedelta(days=1)).isoformat()}).status_code==400
        assert api.put(path,json={"tipo_inasistencia":"Evaluación","fecha_inasistencia":(date.today()-timedelta(days=20)).isoformat()}).status_code==400
        assert api.get(path).json()["data"]["veces_editado"]==0

def test_openapi_contrato_y_referencias():
    schema=app.openapi()
    assert sum(len(v) for v in schema["paths"].values())>=12
    def refs(value):
        if isinstance(value,dict):
            if "$ref" in value:
                target=schema
                for part in value["$ref"].split("/")[1:]:
                    target=target[part]
            for child in value.values(): refs(child)
        elif isinstance(value,list):
            for child in value: refs(child)
    refs(schema)
    for path,operations in schema["paths"].items():
        if path=="/": continue
        for method,operation in operations.items():
            assert operation["summary"] and operation["description"]
            assert "422" in operation["responses"]
            success=operation["responses"].get("201",operation["responses"].get("200"))
            if success: assert success["content"]["application/json"]["schema"]
            if method in {"post","put"}:
                assert operation["requestBody"]["content"]["application/json"]["example"]

def test_arranque_con_puerto_ocupado(tmp_path):
    root=Path(__file__).resolve().parents[1]
    with socket.socket() as ocupado:
        ocupado.bind(("127.0.0.1",0)); ocupado.listen()
        port=ocupado.getsockname()[1]
        log=tmp_path/"api.log"
        with log.open("w",encoding="utf-8") as output:
            process=subprocess.Popen([sys.executable,"-X","utf8","run_api.py","--port",str(port)],cwd=root,stdout=output,stderr=output)
            try:
                for _ in range(100):
                    content=log.read_text(encoding="utf-8")
                    if "Application startup complete" in content: break
                    if process.poll() is not None: pytest.fail(content)
                    time.sleep(.1)
                assert "Application startup complete" in content
                assert "Swagger: http://127.0.0.1:" in content
                assert f":{port}/docs" not in content
            finally:
                process.terminate(); process.wait(timeout=10)
