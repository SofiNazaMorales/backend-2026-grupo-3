
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routers.estudiante import router as estudiante_router
from app.routers.curso import router as curso_router
from app.routers.facultad import router as facultad_router
from app.routers import justificativos

app = FastAPI(
    title="API - Justificación de Inasistencias"
)
app.include_router(estudiante_router)
app.include_router(curso_router)
app.include_router(justificativos.router)
app.include_router(facultad_router)


@app.get("/")
def raiz():
    return {
        "success": True,
        "error": None,
        "data": {
            "estado": "funcionando"
        },
        "message": "API funcionando correctamente",
        "statusCode": 200
    }


@app.exception_handler(RequestValidationError)
async def manejador_global_errores(request, exc):

    detalles = [
        {
            "campo": str(err["loc"][-1]),
            "error": err["msg"]
        }
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Falló la validación de los datos enviados.",
                "details": detalles
            },
            "data": None,
            "message": "La solicitud contiene errores de validación.",
            "statusCode": 422
        }
    )


@app.exception_handler(HTTPException)
async def manejador_httpexception(request, exc):

    codigos = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR"
    }

    codigo_texto = codigos.get(
        exc.status_code,
        "APPLICATION_ERROR"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": codigo_texto,
                "message": str(exc.detail),
                "details": []
            },
            "data": None,
            "message": "No se pudo completar la operación.",
            "statusCode": exc.status_code
        }
    )
