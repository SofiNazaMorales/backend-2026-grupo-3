# Verificación de la entrega acumulativa I y II

## Copia y alcance

Cambios locales en C:/Users/ACER/Documents/backend-2026-grupo-3, rama main,
partiendo del commit 846bd83. No se hizo commit, push ni merge de estos cambios.
No se editaron otras copias de la aplicación ni se cambió ningún usuario de la API
o de PostgreSQL. No existía .env en esta copia; se agregó solo .env.example.

## Diagnóstico inicial y solución

| Componente | Estado encontrado | Corrección |
|---|---|---|
| Justificativos | Router sin import de service; repositorio con modelo indefinido | Imports y flujo ORM corregidos |
| Modelo de datos | FK a carreras.id/cursos.id inexistentes; PK de justificativo no coincidía | FK y nombres alineados con dominio/migración |
| Cursos | POST/GET provisionales y PUT con servicio/repositorio incompatibles | Operaciones reales y mappers corregidos |
| Estudiantes | Sin endpoints registrados en main | CRUD y listado con servicio/repositorio |
| Cuarta entidad | Carrera persistida pero no consultable desde API | POST/listado/detalle de carreras |
| Esquema | Sin revisión inicial en migrations/versions | Migración 0001 reproducible |
| Seeders | Commits parciales y omisión completa si había una carrera | Una transacción, inserción de faltantes por ID |
| Contrato | Errores inconsistentes; DTO duplicados | Error uniforme y DTO compartidos documentados |
| Consulta | Paginación sin total_paginas; acceso ineficiente | Filtro/conteo/orden/página en SQL con desempate |
| Pruebas | Imports antiguos y ausencia de colección exportada | Tests reparados, colección y prueba de reinicio |

## Matriz de requisitos y rúbrica de código

| Requisito | Implementación / evidencia | Estado |
|---|---|---|
| Ejecución y >=12 endpoints | 18 operaciones de recursos más disponibilidad; Uvicorn HTTP real | Verificado con SQLite; falta ejecución PostgreSQL |
| 4 entidades con ID y >=4 atributos | Carrera, Curso, Estudiante y Justificativo; diagramas en modelo_y_alcance.md | Implementado |
| Relación 1:N persistente | Carreras-cursos, carreras-estudiantes, cursos/estudiantes-justificativos con FK | Verificado con SQLite |
| REST, DTO y OpenAPI | Métodos/URI, esquemas de entrada y salida, ejemplos y errores; referencias comprobadas | Verificado |
| CRUD completo y persistencia | CRUD de estudiantes y justificativos; reinicio de dos procesos contra misma base | Verificado con SQLite |
| 6 validaciones / 3 reglas | Longitud, semestre, Enum, formatos, referencias; fecha/plazo/ediciones | Pruebas aprobadas |
| Errores y códigos | 200/201/204/400/404/409/422; error.code/message/details uniforme | Pytest y colección aprobados |
| Filtro/orden/paginación | Mismo GET, SQL, total filtrado y total_paginas, parámetros validados | Pruebas aprobadas |
| Cuatro capas | Agrupación equivalente documentada; repositorios activos en infraestructura | Implementado y recorrido verificado |
| Migraciones y seeders | Alembic 0001, seeder repetible, dos filas por entidad, referencias válidas | Verificado con SQLite; pendiente PostgreSQL |
| >=6 casos reproducibles | Colección exportada, pytest, script de persistencia y resultados guardados | Verificado con SQLite |

## Resultados realmente obtenidos

- `python -m pytest -q tests`: 50 pruebas aprobadas. Motor SQLite de memoria aislado.
- `python tests_manual/verificar_persistencia.py`: 21 comprobaciones aprobadas,
  incluidas migración, seeder repetido y recuperación tras reinicio real de Uvicorn.
  Evidencia: tests_manual/evidencia_persistencia.json.
- Colección Postman ejecutada con Newman: 31 solicitudes y 60 aserciones, cero fallos.
  Servidor HTTP real y SQLite temporal. Cada aserción esperada y estado obtenido
  figura en tests_manual/evidencia_coleccion.json.
- `alembic upgrade head` en una base temporal vacía seguido de `alembic check`:
  no hay diferencias entre la migración y los modelos.
- Caso de puerto ocupado: el iniciador reserva otro puerto y arranca sin detener
  el proceso que ya ocupaba el puerto solicitado.
- PostgreSQL: se intentó la conexión configurada a localhost:5432 y fue rechazada.
  Docker Desktop no tenía motor accesible. No se aplicaron migraciones ni seeders
  a PostgreSQL, no se crearon usuarios ni se modificaron sus tablas.

Una ejecución SQLite no certifica PostgreSQL. Cuando esté disponible, ejecutar
`python tests_manual/verificar_persistencia.py --postgres`: prepara un esquema
temporal exclusivo, usa el mismo usuario y puerto y limpia solo su esquema.
Después comprobar también la instalación real siguiendo el README.

## Pendientes externos al código

- Iniciar PostgreSQL y realizar la comprobación específica anterior.
- Validar con el grupo la formulación P1-P7 propuesta en modelo_y_alcance.md.
- Revisar la presentación existente: máximo 15 diapositivas, 10 minutos y 5 de preguntas.
  No se generó otra presentación porque no se solicitó.
- Confirmar cinco commits propios significativos y un PR por integrante. El historial
  local muestra contribuciones y ramas del equipo, pero su cantidad no certifica
  significancia, autoría académica ni estado de PR en GitHub. No se fabricó historial.
- Si una instalación anterior ya tiene tablas sin versión Alembic, revisar su esquema
  antes de migrar. No se borró ni estampó una base existente para ocultar diferencias.

No se asigna una nota ni se afirma cumplimiento total mientras falte la validación
del motor de entrega y las evidencias de defensa/contribución del equipo.
