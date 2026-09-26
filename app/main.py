from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from fastapi import FastAPI

from app.routers import justificativos

app = FastAPI(title="API - justificacion de inasistencias")

app.include_router(justificativos.router)


@app.get("/")
def raiz():
    return {"mensaje": "API funcionando correctamente"}


@app.exception_handler(RequestValidationError)
async def manejador_global_errores(request, exc):

    detalles = [{"campo": err["loc"][-1], "error": err["msg"]} for err in exc.errors()]

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Fallo en la validación de los datos enviados",
                "details": detalles
            }
        }
    )


@app.exception_handler(HTTPException)
async def manejador_httpexception(request, exc):

    if exc.status_code == 400:
        codigo_texto = "BAD_REQUEST"

    elif exc.status_code == 404:
        codigo_texto = "NOT_FOUND"

    elif exc.status_code == 409:
        codigo_texto = "CONFLICT"

    else:
        codigo_texto = "APPLICATION_ERROR"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": codigo_texto,
                "message": exc.detail,
                "details": []
            }
        }
    )