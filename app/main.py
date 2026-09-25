from fastapi import FastAPI
from app.routers import justificativos

app = FastAPI(title="API - Justificación de Inasistencias")

app.include_router(justificativos.router)


@app.get("/")
def raiz():
    return {"mensaje": "API funcionando correctamente"}