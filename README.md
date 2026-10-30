# Proyecto desarrollo de backend grupo 3

Backend desarrollado en Python, utilizando FastAPI, y Arquitectura: para la gestión de justificaciones a inasistencias estudiantiles.

integrantes y responsabilidades: 

Carlos Melendez / Dominio y datos: Diseño de Modelos de Dominio y generación de la base de datos simulada

Macarena Melin / API y lógica de negocio: Desarrollo de la capa de Enrutadores (Routers), exposición de Endpoints web y validación de peticiones HTTP.

Angel Obreque / Calidad y pruebas: Implementación de la capa de Servicios y Repositorios, Pruebas postman

Sofia Morales / Coordinación  y seguimiento + documentación e integración:  Arquitectura base, configuración global (`main.py`), manejador de errores estandarizado, documentación (README)

## Estructura del proyecto

El proyecto sigue una arquitectura por capas (presentation → application → domain, con infrastructure para persistencia):

```
app/main.py                    # crea y ensambla la API
presentation/
    dependencies.py            # inyección de dependencias
    routers/                   # endpoints HTTP
    schemas/dtos/              # DTO y validación
application/services/          # coordinación de casos de uso
domain/                        # entidades y reglas de negocio
infrastructure/
    database.py                # conexión y sesiones de BD (pendiente)
    models/                    # modelos ORM/ODM (pendiente)
    mappers/                   # conversión dominio-ORM (pendiente)
    repositories/              # acceso y persistencia (en memoria por ahora)
    seeders/                   # carga inicial (datos semilla)
migrations/                    # migraciones Alembic (pendiente)
    env.py
    versions/
tests/                         # pruebas unitarias (pytest)
tests_manual/                  # colección Postman
.env.example                   # variables sin secretos
README.md
```

### Instrucciones de Instalación y Ejecución

Para levantar este proyecto de manera local, lo primero a considerar es tener Python 3.10 o superior instalado

pasos:

1. **Clonar y ubicarse en repositorio:**
```bash
   git clone https://github.com/SofiNazaMorales/backend-2026-grupo-3
   cd backend-2026-grupo-3
```

2. **Crear y activar el entorno virtual (Obligatorio para aislar dependencias):**

   Para Linux o macOS:
```bash
   python3 -m venv venv
```
   Para Windows
```bash
    python -m venv venv
    venv\Scripts\activate.bat
```

3. **Instalar las dependencias del proyecto:**
```bash
    pip install -r requirements.txt
```


4. **Levantar el servidor web (Uvicorn):**
```bash
   uvicorn app.main:app --reload
```

### Contrato global

**1. Respuestas Exitosas (200, 201)**
Utilizan una estructura global de envoltorio (`_envelope`):

```json
{
  "success": true, 
  "data": { ... }, 
  "error": null,
  "message": "Operación realizada con éxito"
}
```

**2. Respuestas de Error (400, 404, 409, 422)**

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "array"
  }
}
```

#### Acceso a documentación
