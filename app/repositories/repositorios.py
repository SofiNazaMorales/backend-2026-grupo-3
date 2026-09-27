from app.domain.justificativo import Justificativo


_justificativos: dict[str, Justificativo] = {}
_contador_id_justificativo = 1


def crear_justificativo(justificativo: Justificativo) -> Justificativo:
    global _contador_id_justificativo
    justificativo.id_justificativo = str(_contador_id_justificativo)
    _justificativos[justificativo.id_justificativo] = justificativo
    _contador_id_justificativo += 1
    return justificativo


def listar_justificativos() -> list[Justificativo]:
    return list(_justificativos.values())


def obtener_justificativo_por_id(id_justificativo: str) -> Justificativo | None:
    return _justificativos.get(id_justificativo)


def actualizar_justificativo(id_justificativo: str, cambios: dict) -> Justificativo | None:
    actual = _justificativos.get(id_justificativo)
    if actual is None:
        return None
    for campo, valor in cambios.items():
        if valor is not None:
            setattr(actual, campo, valor)
    return actual


def eliminar_justificativo(id_justificativo: str) -> bool:
    return _justificativos.pop(id_justificativo, None) is not None