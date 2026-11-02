# Integración de repositorios ORM

La rama API y lógica de negocio reemplaza los repositorios en memoria por sesiones
SQLAlchemy síncronas. No crea modelos ORM, conexiones, migraciones ni datos de prueba
en la aplicación: esas implementaciones son responsabilidad de los otros integrantes.

## Contrato para integrar el trabajo del equipo

- Sofía: `app/database.py`, función generadora `get_db()` que entregue una
  `sqlalchemy.orm.Session` por petición y la cierre en `finally`. Debe usar la
  conexión real configurada por el equipo. Los repositorios hacen commit/rollback;
  la dependencia no debe confirmar transacciones automáticamente.
- Carlos: `app/models/justificativo.py`, clase `justificativo_model`, con atributos
  `id_justificativo`, `rut_estudiante`, `id_curso`, `fecha_inasistencia`,
  `tipo_inasistencia`, `motivo`, `fecha_registro`, `veces_editado`, `estado`.
- Carlos: `app/models/curso.py`, clase `curso_model`, con atributos `id_curso`,
  `codigo_curso`, `nombre_curso`, `semestre`, `id_carrera`.
- Usar los Enums existentes de `app/domain/enums.py` para tipo y estado.
  Los mappers conservan fechas como `date` y Enums; FastAPI serializa el JSON.
- `id_justificativo` mantiene el contrato actual de texto. El repositorio genera
  UUID de 36 caracteres para los nuevos registros; los IDs de texto existentes
  siguen siendo consultables. El modelo debe aceptar texto de al menos 36 caracteres.
- Cursos mantiene sus identificadores de texto actuales y su código debe ser único.
  Los modelos y migraciones deben establecer las claves foráneas correspondientes.

Los nombres anteriores son el contrato que propone esta implementación: deben
coordinarse con las implementaciones definitivas antes de integrarla a main.

## Cambios de esta rama

`repositorios.py` recibe `db` como primer argumento en cada función.
`servicios.py` recibe y propaga la misma sesión, y usa `justificativo_a_dict` de
`app/mappers.py`. Se conservan las reglas de fechas, plazo de evaluaciones,
límite de dos ediciones y el filtrado/ordenamiento/paginación en el servicio.
La fecha de registro se completa al crear el justificativo.

`CursoRepository(db)` recibe una sesión obligatoria. Sus métodos continúan
devolviendo `Curso` de dominio mediante el mapper; `CursoService` conserva su
interfaz. Quien conecte el router de cursos debe construir
`CursoService(CursoRepository(db))` con la sesión de la petición.

Las escrituras confirman con `commit`; ante errores de SQLAlchemy ejecutan
`rollback` y propagan la excepción. No se cambia el manejador global de errores.
Cada escritura del repositorio es una transacción independiente.
El DELETE exitoso de justificativos conserva 204 sin cuerpo.

## Verificación con la base definitiva

Esta copia no contiene todavía `app/database.py` ni `app/models/`. Por eso no
arrancará la API actualizada hasta integrar esas dependencias; no se añadieron
versiones temporales ni un almacenamiento alternativo en memoria.

1. Integrar los archivos anteriores y las migraciones/seeders del equipo.
2. Instalar `pip install -r requirements.txt` con el entorno virtual activo.
3. Ejecutar las migraciones y seeders según la configuración definitiva.
4. Iniciar `uvicorn app.main:app --reload`.
5. Crear un justificativo con un estudiante y curso existentes y guardar su ID.
6. Reiniciar el servidor y comprobar que GET por ese ID devuelve el registro.
7. Probar actualización, límite de ediciones, filtros y paginación.
8. Eliminarlo y comprobar que una nueva consulta devuelve 404.

Las rutas de conexión propuestas difieren de la reorganización guardada en la
rama de Alexis (`infrastructure/`). No mezclar ambas estructuras sin ajustar los
imports conjuntamente con el equipo.
