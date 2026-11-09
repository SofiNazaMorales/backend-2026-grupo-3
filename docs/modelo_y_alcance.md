# Modelo, alcance y decisiones

## P1 a P7: propuesta para validar por el equipo

P1. Los avisos y antecedentes de inasistencias universitarias se reciben por medios
separados y su seguimiento puede depender de consultas manuales. Esta formulación
debe contrastarse con el levantamiento real del grupo; no representa una observación nueva.

P2. Estudiantes que presentan justificativos y personal académico que los consulta.
P3. Dificultad para localizar antecedentes y aplicar de manera consistente plazos
y límites de modificación.
P4. Carreras, cursos, estudiantes y justificativos, incluyendo fechas, motivos,
tipos, estados y contador de ediciones.

P5. El sistema debe permitir: (1) registrar estudiantes, (2) consultarlos por RUT,
(3) actualizar sus datos, (4) registrar cursos, (5) consultar cursos, (6) registrar
justificativos, (7) modificarlos respetando reglas, (8) eliminarlos, (9) consultar
su detalle, (10) filtrar/ordenar/paginar y (11) consultar carreras persistidas.

P6. Se excluyen frontend, autenticación/autorización y verificación documental
externa de certificados. No se agregó un servicio de correo ni carga de archivos.

P7. Aceptación verificable: crear y recuperar un justificativo; conservarlo tras
reinicio; rechazar una tercera edición; rechazar evaluaciones fuera de plazo;
rechazar datos inválidos; devolver una colección filtrada/ordenada/paginada con
totales correctos; rechazar referencias inexistentes.

## Diagrama de clases

```mermaid
classDiagram
class Carrera {
  +str id_carrera
  +str codigo
  +str nombre_carrera
  +int duracion_semestre
  +Facultad facultad
}
class Curso {
  +str id_curso
  +str codigo_curso
  +str nombre_curso
  +int semestre
  +str id_carrera
}
class Estudiante {
  +str rut_estudiante
  +str nombre
  +str apellido
  +str email_institucional
  +str id_carrera
  +bool estado_alumno
  +activar_estudiante()
  +desactivar_estudiante()
}
class Justificativo {
  +str id_justificativo
  +str rut_estudiante
  +str id_curso
  +date fecha_inasistencia
  +TipoInasistencia tipo_inasistencia
  +str motivo
  +date fecha_registro
  +int veces_editado
  +EstadoJustificativo estado
  +aceptar()
  +rechazar()
}
Carrera "1" --> "*" Curso
Carrera "1" --> "*" Estudiante
Estudiante "1" --> "*" Justificativo
Curso "1" --> "*" Justificativo
```

## Diagrama de datos

```mermaid
erDiagram
    carreras ||--o{ cursos : contiene
    carreras ||--o{ estudiantes : agrupa
    cursos ||--o{ justificativos : recibe
    estudiantes ||--o{ justificativos : presenta
    carreras {
        string id_carrera PK
        string codigo UK
        string nombre_carrera
        int duracion_semestre
        string facultad
    }
    cursos {
        string id_curso PK
        string codigo_curso UK
        string nombre_curso
        int semestre
        string id_carrera FK
    }
    estudiantes {
        string rut_estudiante PK
        string nombre
        string apellido
        string email_institucional UK
        boolean estado_alumno
        string id_carrera FK
    }
    justificativos {
        string id_justificativo PK
        string rut_estudiante FK
        string id_curso FK
        date fecha_inasistencia
        string tipo_inasistencia
        string motivo
        date fecha_registro
        int veces_editado
        string estado
    }
```

## Decisiones para la defensa

- Separar DTO, dominio y ORM evita acoplar el contrato HTTP a las tablas.
- PostgreSQL permite persistencia e integridad referencial; ORM concentra el acceso.
- Migraciones versionadas permiten preparar una instalación vacía de forma repetible.
- Seeders idempotentes completan ejemplos sin reemplazar usuarios existentes.
- Rechazar borrados referenciados evita perder justificativos por cascadas accidentales.
- Filtrar/ordenar/paginar en SQL evita cargar toda la tabla para devolver una página.
- Rollback revierte escrituras pendientes fallidas; no deshace una transacción confirmada.
- El puerto HTTP se configura independientemente del de PostgreSQL; el iniciador
  reserva un puerto libre sin cerrar procesos ajenos.

Limitación: días hábiles se calculan sin feriados. Mejoras futuras: calendario
académico de feriados y autenticación/autorización por roles. La edición bloquea la fila con SELECT FOR UPDATE en PostgreSQL hasta confirmar
la escritura, para serializar el contador. SQLite no ofrece esa misma garantía de
bloqueo por fila; sus pruebas aisladas no certifican concurrencia PostgreSQL.
