"""Contrato de respuestas compartido; mantiene el envoltorio global del grupo."""
from datetime import date
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from pydantic.json_schema import models_json_schema
from typing import Generic, TypeVar, Literal
from app.schemas.curso_dto import CursoResponseDTO
from app.schemas.estudiante_dto import EstudianteResponseDTO
from app.schemas.carrera_dto import CarreraResponseDTO
from app.schemas.justificativo_dto import JustificativoResponseDTO, JustificativoPaginaDTO

T = TypeVar("T")
class Respuesta(BaseModel, Generic[T]):
    success: Literal[True] = True
    data: T
    error: None = None
    message: str

class Coleccion(BaseModel, Generic[T]):
    items: list[T]
    total: int

class FacultadDTO(BaseModel):
    codigo: str
    nombre: str

class ErrorDetalle(BaseModel):
    code: str
    message: str
    details: list = Field(default_factory=list)

class RespuestaError(BaseModel):
    error: ErrorDetalle

EJEMPLOS = {
    "cursos": {"id_curso":"CRS-INF1108", "codigo_curso":"INF-1108", "nombre_curso":"Desarrollo de Backend", "semestre":2, "id_carrera":"ICI-INF"},
    "estudiantes": {"rut_estudiante":"20.123.554-5", "nombre":"Roberto", "apellido":"Díaz", "email_institucional":"rdiaz2026@alu.uct.cl", "id_carrera":"ICI-INF", "estado_alumno":True},
    "carreras": {"id_carrera":"ICI-INF", "codigo":"PLAN-2023-INF", "nombre_carrera":"Ingeniería Civil Informatica", "duracion_semestre":10, "facultad":"Facultad de Ingeniería"},
    "justificativos": {"id_justificativo":"JUS-001", "rut_estudiante":"20.123.554-5", "id_curso":"CRS-INF1108", "fecha_inasistencia":date.today().isoformat(), "tipo_inasistencia":"Clase Regular", "motivo":"Cita médica de urgencia", "fecha_registro":date.today().isoformat(), "veces_editado":0, "estado":"Pendiente"},
    "facultades": {"codigo":"INGENIERIA", "nombre":"Facultad de Ingeniería"},
}

def configurar_contrato(app):
    def openapi():
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(title=app.title, version=app.version, description=app.description, routes=app.routes)
        recursos = {"cursos":CursoResponseDTO, "estudiantes":EstudianteResponseDTO,
                    "carreras":CarreraResponseDTO, "justificativos":JustificativoResponseDTO,
                    "facultades":FacultadDTO}
        modelos = [RespuestaError, Respuesta[JustificativoPaginaDTO]]
        for modelo in recursos.values():
            modelos.extend([Respuesta[modelo], Respuesta[Coleccion[modelo]]])
        referencias, definiciones = models_json_schema([(m,"serialization") for m in modelos], ref_template="#/components/schemas/{model}")
        schema.setdefault("components",{}).setdefault("schemas",{}).update(definiciones["$defs"])
        for path, operaciones in schema["paths"].items():
            if path == "/":
                continue
            recurso = path.split("/")[1]
            if recurso not in recursos:
                continue
            for metodo, operacion in operaciones.items():
                if metodo not in {"get","post","put","delete","patch"}:
                    continue
                coleccion = metodo == "get" and "{" not in path
                entidad = recursos[recurso]
                respuesta = Respuesta[JustificativoPaginaDTO] if coleccion and recurso == "justificativos" else Respuesta[Coleccion[entidad]] if coleccion else Respuesta[entidad]
                accion = {"get":"Listar" if coleccion else "Obtener", "post":"Crear", "put":"Actualizar", "patch":"Actualizar", "delete":"Eliminar"}[metodo]
                operacion["summary"] = f"{accion} {recurso}"
                operacion["description"] = f"{accion} {recurso}. La operación recorre presentación, servicio y repositorio ORM cuando corresponde; facultades es un catálogo fijo del dominio."
                if recurso == "justificativos" and coleccion:
                    operacion["description"] += " Aplica filtro, orden estable y paginación en SQL. Los totales corresponden al filtro."
                if recurso == "justificativos" and metodo in {"post","put"}:
                    operacion["description"] += " No admite fechas futuras; las evaluaciones tienen plazo de cinco días hábiles (lunes a viernes, sin feriados); máximo dos ediciones."
                codigo = "201" if metodo == "post" else "204" if metodo == "delete" else "200"
                ejemplo = dict(EJEMPLOS[recurso])
                if coleccion:
                    ejemplo = {"items":[ejemplo], "total":1}
                    if recurso == "justificativos":
                        ejemplo.update(pagina=1,limite=20,total_paginas=1)
                operacion["responses"] = {codigo: {"description": "Operación completada"}}
                if codigo != "204":
                    operacion["responses"][codigo]["content"] = {"application/json": {"schema": referencias[(respuesta,"serialization")], "example": {"success":True,"data":ejemplo,"error":None,"message":"Operación realizada correctamente"}}}
                errores = {422:("VALIDATION_ERROR","Los datos no cumplen el esquema")}
                if "{" in path:
                    errores[404] = ("NOT_FOUND","El recurso solicitado no existe")
                if metodo in {"post","put","delete"}:
                    errores[409] = ("CONFLICT","Registro duplicado o relación inexistente/en uso")
                if recurso == "justificativos" and metodo in {"post","put"}:
                    errores[400] = ("BUSINESS_RULE","La operación viola una regla de negocio")
                for estado,(code,message) in errores.items():
                    operacion["responses"][str(estado)] = {"description":message,"content":{"application/json":{"schema":referencias[(RespuestaError,"serialization")],"example":{"error":{"code":code,"message":message,"details":[]}}}}}
                if "requestBody" in operacion:
                    entrada = dict(EJEMPLOS[recurso])
                    if recurso == "estudiantes":
                        entrada.pop("estado_alumno",None)
                    if recurso == "justificativos":
                        for campo in ("id_justificativo","fecha_registro","veces_editado","estado"):
                            entrada.pop(campo,None)
                    if metodo == "put":
                        campo = {"justificativos":"motivo", "cursos":"semestre", "estudiantes":"nombre"}[recurso]
                        entrada = {campo:entrada[campo]}
                    operacion["requestBody"]["content"]["application/json"]["example"] = entrada
                for parametro in operacion.get("parameters",[]):
                    nombre = parametro["name"]
                    parametro.setdefault("description", "Identificador del recurso" if parametro["in"]=="path" else f"Parámetro de consulta: {nombre}")
                    if parametro["in"] == "path":
                        parametro["example"] = EJEMPLOS[recurso].get(nombre, EJEMPLOS[recurso].get("rut_estudiante",EJEMPLOS[recurso].get("codigo","JUS-001")))
        app.openapi_schema = schema
        return schema
    app.openapi = openapi
