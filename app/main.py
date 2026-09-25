from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app= FastAPI(title="API - justificacion de inasistencias")

@app.exception_handler(RequestValidationError)
async def manejador_global_errores(request,exc):

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