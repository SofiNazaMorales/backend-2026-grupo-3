from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app= FastAPI(title="API - justificacion de inasistencias")

#manejador global de errores de validacion

@app.exception_handler(RequestValidationError)
async def manejador_global_errores(request,exc):
    errores_formateados=[{"code": "VALIDATION_ERROR", "details": err["msg"]} for err in exc.errors()]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": None,
            "error": errores_formateados,
            "message": "Fallo en la validación de los datos enviados"
        }
    )