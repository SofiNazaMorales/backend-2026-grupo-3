# Integración ORM en main

La integración activa utiliza app/infrastructure/database.py, get_db y una sesión
por solicitud. Los modelos viven en app/infrastructure/models y los repositorios
activos en app/infrastructure/repositories. Las rutas antiguas app/database.py y
app/models no se usan ni son requisitos pendientes.

Los identificadores de texto y los usuarios semilla se conservan. Los nuevos
justificativos reciben UUID. Los mappers convierten ORM y dominio sin cambiar
RUT ni códigos. Las escrituras hacen commit/refresh y rollback ante fallos;
la dependencia revierte errores pendientes y cierra la sesión.

Los servicios de cursos y estudiantes reciben repositorios por inyección.
El servicio de justificativos conserva su interfaz de funciones con contexto de
persistencia, sin importar SQLAlchemy ni ejecutar consultas; delega en infraestructura.
La consulta combinada se ejecuta en SQL con un conteo sobre el filtro.

Alembic prepara una base vacía; run_seeder.py carga faltantes sin sobrescribir datos.
Consultar README y docs/cumplimiento_I_II.md para ejecución y verificaciones reales.
