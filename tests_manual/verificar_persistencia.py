"""Ejecuta migración, seeder y HTTP con dos procesos Uvicorn distintos.
Por defecto usa SQLite temporal. Con --postgres usa un esquema PostgreSQL propio.
No borra ni modifica tablas existentes ni usuarios de la base configurada.
"""
import json
from base_aislada import base_aislada
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from datetime import date, timedelta, datetime, timezone
import urllib.request
import urllib.error

ROOT=Path(__file__).resolve().parents[1]

def main():
    checks=[]
    def record(name,condition,detail=None):
        assert condition, f"Falló: {name}: {detail}"
        checks.append({"prueba":name,"resultado":"OK"})

    with tempfile.TemporaryDirectory(prefix="backend-g3-", dir=os.getenv("TEST_TMPDIR")) as temp, base_aislada(temp, "--postgres" in sys.argv) as (database_url, motor):
        env=os.environ.copy()
        env["DATABASE_URL"]=database_url
        env["PYTHONPATH"]=str(ROOT)+os.pathsep+env.get("PYTHONPATH","")
        env["PYTHONIOENCODING"]="utf-8"
        migrated=subprocess.run([sys.executable,"-m","alembic","upgrade","head"],cwd=ROOT,env=env,capture_output=True,text=True,encoding="utf-8")
        record("Migración inicial sobre base vacía",migrated.returncode==0,migrated.stderr)
        for n in (1,2):
            seeded=subprocess.run([sys.executable,"run_seeder.py"],cwd=ROOT,env=env,capture_output=True,text=True,encoding="utf-8")
            record(f"Seeder repetible, ejecución {n}",seeded.returncode==0 and seeded.stdout.count(": 2 registros")==4,seeded.stdout+seeded.stderr)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1",0));port=sock.getsockname()[1]
        url=f"http://127.0.0.1:{port}"
        log=open(Path(temp)/"servidor.log","w",encoding="utf-8")
        process=None
        pids=[]
        def request(method,path,body=None):
            data=json.dumps(body).encode() if body is not None else None
            req=urllib.request.Request(url+path,data=data,method=method,headers={"Content-Type":"application/json"})
            try:
                with urllib.request.urlopen(req,timeout=10) as response:
                    raw=response.read();return response.status,json.loads(raw) if raw else None
            except urllib.error.HTTPError as error:
                return error.code,json.loads(error.read())
        def stop():
            nonlocal process
            if process is not None:
                process.terminate()
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:process.kill();process.wait()
                process=None
        def start():
            nonlocal process
            process=subprocess.Popen([sys.executable,"-m","uvicorn","app.main:app","--host","127.0.0.1","--port",str(port)],cwd=ROOT,env=env,stdout=log,stderr=log)
            pids.append(process.pid)
            for _ in range(100):
                if process.poll() is not None:raise RuntimeError("Uvicorn no arrancó; revisar imports/configuración")
                try:
                    if request("GET","/")[0]==200:return
                except (urllib.error.URLError,ConnectionError,OSError):pass
                time.sleep(.1)
            raise RuntimeError("Tiempo agotado al iniciar Uvicorn")
        try:
            start()
            student={"rut_estudiante":"12345678-5","nombre":"Ana","apellido":"Prueba","email_institucional":"persistencia@alu.uct.cl","id_carrera":"ICI-INF"}
            record("Estudiantes POST 201",request("POST","/estudiantes",student)[0]==201)
            record("Estudiantes duplicado 409",request("POST","/estudiantes",student)[0]==409)
            body={"rut_estudiante":"20.123.554-5","id_curso":"CRS-INF1108","fecha_inasistencia":date.today().isoformat(),"tipo_inasistencia":"Clase Regular","motivo":"Certificado de prueba para persistencia"}
            code,created=request("POST","/justificativos",body)
            record("Justificativos POST 201",code==201,created)
            pk=created["data"]["id_justificativo"]
            stop()
            start()
            record("Dos procesos de servidor diferentes",pids[0]!=pids[1])
            code,found=request("GET","/justificativos/"+pk)
            record("Mismo justificativo después de reiniciar",code==200 and found["data"]["motivo"]==body["motivo"],found)
            record("Estudiante después de reiniciar",request("GET","/estudiantes/12345678-5")[0]==200)
            code,filtered=request("GET","/justificativos?id_curso=CRS-INF1108&tipo_inasistencia=Clase%20Regular&pagina=1&limite=1")
            record("Filtro y paginación",code==200 and len(filtered["data"]["items"])==1 and filtered["data"]["total"]>=2)
            for n in (1,2):
                code,result=request("PUT","/justificativos/"+pk,{"motivo":"Motivo corregido para la prueba"})
                record(f"Edición {n} persistida",code==200 and result["data"]["veces_editado"]==n)
            record("Tercera edición rechazada 400",request("PUT","/justificativos/"+pk,{"motivo":"Tercera edición no permitida"})[0]==400)
            record("Validación 422",request("POST","/justificativos",dict(body,motivo="Mal"))[0]==422)
            old=dict(body,fecha_inasistencia=(date.today()-timedelta(days=20)).isoformat(),tipo_inasistencia="Evaluación")
            record("Plazo vencido 400",request("POST","/justificativos",old)[0]==400)
            record("No encontrado 404",request("GET","/justificativos/NO-EXISTE")[0]==404)
            record("Actualizar estudiante 200",request("PUT","/estudiantes/12345678-5",{"nombre":"Ana María"})[0]==200)
            record("Eliminar estudiante 204",request("DELETE","/estudiantes/12345678-5")[0]==204)
            record("Estudiante eliminado 404",request("GET","/estudiantes/12345678-5")[0]==404)
            record("Eliminar justificativo 204",request("DELETE","/justificativos/"+pk)[0]==204)
            record("Justificativo eliminado 404",request("GET","/justificativos/"+pk)[0]==404)
        finally:
            stop();log.close()
        report={"resultado":"APROBADO","fecha_utc":datetime.now(timezone.utc).isoformat(),"motor":motor+"; modelos ORM reales, sin dobles", "servidor":"Uvicorn HTTP real; dos procesos separados", "procesos":pids,"comprobaciones":checks,"limite":"La ejecución sin --postgres no certifica PostgreSQL. No se certifica Docker."}
        target=ROOT/("tests_manual/evidencia_postgresql.json" if "--postgres" in sys.argv else "tests_manual/evidencia_persistencia.json")
        target.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print(f"APROBADO: {len(checks)} comprobaciones, incluido reinicio real del servidor")
        print(target)

if __name__=="__main__":
    from sqlalchemy.exc import OperationalError
    try:
        main()
    except OperationalError:
        print("No se pudo conectar a la base de pruebas. Comprueba PostgreSQL, el puerto y las variables DB_*; no se modificaron los usuarios.", file=sys.stderr)
        raise SystemExit(1)
