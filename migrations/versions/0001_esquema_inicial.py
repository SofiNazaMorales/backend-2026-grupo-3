"""Crear tablas y relaciones iniciales."""
from alembic import op
import sqlalchemy as sa
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("carreras", sa.Column("id_carrera",sa.String(50),primary_key=True),sa.Column("codigo",sa.String(20),nullable=False,unique=True),sa.Column("nombre_carrera",sa.String(200),nullable=False),sa.Column("duracion_semestre",sa.Integer,nullable=False),sa.Column("facultad",sa.String(100),nullable=False))
    op.create_table("cursos",sa.Column("id_curso",sa.String(50),primary_key=True),sa.Column("codigo_curso",sa.String(20),nullable=False,unique=True),sa.Column("nombre_curso",sa.String(100),nullable=False),sa.Column("semestre",sa.Integer,nullable=False),sa.Column("id_carrera",sa.String(50),sa.ForeignKey("carreras.id_carrera"),nullable=False))
    op.create_table("estudiantes",sa.Column("rut_estudiante",sa.String(20),primary_key=True),sa.Column("nombre",sa.String(50),nullable=False),sa.Column("apellido",sa.String(50),nullable=False),sa.Column("email_institucional",sa.String(100),nullable=False,unique=True),sa.Column("estado_alumno",sa.Boolean,nullable=False),sa.Column("id_carrera",sa.String(50),sa.ForeignKey("carreras.id_carrera"),nullable=False))
    op.create_table("justificativos",sa.Column("id_justificativo",sa.String(50),primary_key=True),sa.Column("rut_estudiante",sa.String(20),sa.ForeignKey("estudiantes.rut_estudiante"),nullable=False),sa.Column("id_curso",sa.String(50),sa.ForeignKey("cursos.id_curso"),nullable=False),sa.Column("fecha_inasistencia",sa.Date,nullable=False),sa.Column("tipo_inasistencia",sa.String(20),nullable=False),sa.Column("motivo",sa.String(500),nullable=False),sa.Column("fecha_registro",sa.Date,nullable=True),sa.Column("veces_editado",sa.Integer,nullable=False),sa.Column("estado",sa.String(20),nullable=False))

def downgrade():
    for tabla in ("justificativos","estudiantes","cursos","carreras"):
        op.drop_table(tabla)
