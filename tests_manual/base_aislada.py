"""Contexto de pruebas: SQLite temporal o esquema PostgreSQL exclusivo y descartable."""
from contextlib import contextmanager
from pathlib import Path
import os
from uuid import uuid4
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

@contextmanager
def base_aislada(temp, postgres=False):
    if not postgres:
        yield "sqlite:///"+(Path(temp)/"persistencia.db").as_posix(), "SQLite persistente en archivo temporal"
        return
    load_dotenv()
    # No reutilizar DATABASE_URL para evitar tomar una SQLite de desarrollo.
    url=URL.create("postgresql+psycopg2", username=os.getenv("DB_USER","alumno"),
                   password=os.getenv("DB_PASSWORD","mi_clave_segura"),
                   host=os.getenv("DB_HOST","localhost"),port=int(os.getenv("DB_PORT","5432")),
                   database=os.getenv("DB_NAME","clase"))
    schema="prueba_backend_"+uuid4().hex
    engine=create_engine(url,connect_args={"connect_timeout":5})
    creado=False
    try:
        with engine.begin() as connection:
            connection.exec_driver_sql(f'CREATE SCHEMA "{schema}"')
        creado=True
        test_url=url.update_query_dict({"options":f"-csearch_path={schema}","connect_timeout":"5"})
        yield test_url.render_as_string(hide_password=False), "PostgreSQL en esquema temporal aislado"
    finally:
        if creado:
            with engine.begin() as connection:
                # schema es un nombre propio generado, no una entrada del usuario.
                connection.exec_driver_sql(f'DROP SCHEMA "{schema}" CASCADE')
        engine.dispose()
