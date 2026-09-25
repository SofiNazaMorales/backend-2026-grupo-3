# Proyecto desarrollo de backend grupo 3

Backend desarrollado en Python, utilizando FastAPI, y Arquitectura: para la gestión de justificaciones a inasistencias estudiantiles.

## Instrucciones de Instalación y Ejecución

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
```json
    {
    "success": true,
    "data": null,
    "error": [
        {
        "code": "STRING",
        "details": "STRING"
        }
    ],
    "message": "Mensaje descriptivo de la operación"
    }
```