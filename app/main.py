from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from app.domain.errores import ErrorAplicacion
from app.routers.curso import router as curso_router
from app.routers.facultad import router as facultad_router
from app.routers.estudiantes import router as estudiante_router
from app.routers.carreras import router as carrera_router
from app.routers import justificativos
from app.respuestas import envelope

app = FastAPI(title="API - justificacion de inasistencias", version="2.0.0",
              description="Gestión de justificativos, estudiantes, cursos y carreras con persistencia ORM.")
for router in (curso_router, justificativos.router, facultad_router, estudiante_router, carrera_router):
    app.include_router(router)

@app.get("/", summary="Comprobar disponibilidad", description="Indica que el proceso de la API está disponible; no certifica la conexión a PostgreSQL.")
def raiz():
    return {"mensaje": "API funcionando correctamente"}

@app.exception_handler(RequestValidationError)
async def manejador_validacion(request, exc):
    errores = [{"campo": ".".join(map(str,e["loc"])), "error": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"error": {"code": "VALIDATION_ERROR", "message": "Fallo en la validación de los datos enviados", "details": errores}})

@app.exception_handler(ErrorAplicacion)
@app.exception_handler(HTTPException)
async def manejador_http(request, exc):
    code = {400: "BAD_REQUEST", 404: "NOT_FOUND", 409: "CONFLICT", 422: "VALIDATION_ERROR"}.get(exc.status_code,"APPLICATION_ERROR")
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": code, "message": str(exc.detail), "details": []}}, headers=getattr(exc, "headers", None))

@app.exception_handler(IntegrityError)
async def manejador_integridad(request, exc):
    return JSONResponse(status_code=409, content={"error": {"code": "CONFLICT", "message": "Registro duplicado o relación inexistente/en uso", "details": []}})

from app.presentation.openapi import configurar_contrato
configurar_contrato(app)
