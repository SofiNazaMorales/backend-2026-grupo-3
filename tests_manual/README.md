# Pruebas reproducibles

## Colección exportada

Importar Backend_g3.postman_collection.json en Postman y ajustar base_url al puerto
HTTP real. Aplicar migraciones y ejecutar run_seeder.py antes. Las seis carpetas
contienen 31 solicitudes: CRUD de estudiantes, CRUD de justificativos, entradas
inválidas, reglas, consulta combinada, inexistentes/duplicados/integridad.
No se borran ni cambian los usuarios semilla; los casos usan registros propios.

Cada solicitud tiene resultado esperado mediante aserciones. Los resultados obtenidos
se guardan al ejecutar el Runner o Newman; no confundir una colección escrita con
una colección ejecutada. La evidencia actual se registra en docs/cumplimiento_I_II.md.

## Persistencia con reinicio real

```powershell
python tests_manual/verificar_persistencia.py
```

Usa SQLite en un directorio temporal, migra, carga dos registros por entidad y repite
el seeder. Inicia Uvicorn, crea datos por HTTP, detiene el proceso y arranca otro
contra el mismo archivo. Comprueba el dato y luego actualiza y elimina los registros
propios. Ejecuta 21 comprobaciones y guarda evidencia_persistencia.json.
Esta ejecución no certifica PostgreSQL.

```powershell
python tests_manual/verificar_persistencia.py --postgres
```

Lee DB_USER/DB_PASSWORD/DB_HOST/DB_PORT/DB_NAME de .env (mismos valores de la API).
Requiere PostgreSQL en ejecución y permiso para crear esquemas. Crea un esquema
con nombre aleatorio, aplica migraciones y seeders allí, y ejecuta el mismo recorrido
HTTP con reinicio. Elimina únicamente ese esquema propio al terminar; no toca tablas
ni usuarios existentes. Guarda evidencia_postgresql.json solo si termina correctamente.

Ambas modalidades reservan un puerto temporal para el servidor de prueba; no usan
8000 ni cambian el puerto de PostgreSQL. En un entorno con TEMP restringido se puede
definir TEST_TMPDIR a una carpeta existente y escribible.

## Seis casos y resultados esperados

| Caso | Entrada / acción | Esperado |
|---|---|---|
| CRUD | Crear estudiante propio; leer, editar y borrar | 201, 200, 200, 204, luego 404 |
| Validación | Motivo de menos de diez caracteres | 422 y error.code/message/details |
| Inexistente | GET justificativo con ID inexistente | 404 uniforme |
| Negocio | Evaluación con fecha de hace veinte días; tercera edición | 400; no se guarda el cambio |
| Consulta | Filtrar curso, ordenar fecha y paginar con límite 1 | 200, orden correcto y total filtrado |
| Persistencia | POST, detener servidor, iniciar y GET del ID | 200 con el mismo registro |

pytest usa memoria aislada y verifica además contrato OpenAPI, relaciones, usuarios
semilla y arranque si el puerto solicitado está ocupado. La limpieza de pytest
solo afecta su motor SQLite de memoria; no usa la base configurada por el usuario.
