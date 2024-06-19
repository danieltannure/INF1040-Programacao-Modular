import os, json, atexit
from .. import filial, turma

__all__ = ["add_aula", "del_aula", "get_turmas_by_filial", "get_filial_by_turma"]

# Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")
_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "aulas.json")

# [
#     {
#         "id_filial": int,
#         "id_turma": int
#     },
#     ...
# ]
_aulas: list[dict] = []

# internas
def _read() -> None:
    """
    Iniciaiza
    """
    global _aulas

    if not os.path.exists(_JSON_FILE_PATH):
        _write()
        return

    try:
        with open(_JSON_FILE_PATH, 'r') as file:
            _aulas = json.load(file)
    except Exception as e:
        print(f"Erro de I/O em aula: {e}")

def _write() -> None:
    """
    Salva
    """
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    try:
        with open(_JSON_FILE_PATH, 'w') as file:
            json.dump(_aulas, file, indent=2)
    except Exception as e:
        print(f"Erro de I/O em aula: {e}")

# Funcs de acesso
def add_aula(id_filial: int, id_turma: int) -> tuple[int, None]:
    """
    Adiciona uma nova aula
    """
    # Checando se existem
    err, filial_dict = filial.get_filial(id_filial)
    if err != 0:
        return err, None
    
    err, turma_dict = turma.get_turma(id_turma)
    if err != 0:
        return err, None
    
    # Checando se o par já existe
    for aula_dict in _aulas:
        if aula_dict["id_turma"] == id_turma:
            # Turma ja existe associada a alguma filial
            return 36, None
    
    nova_aula = {
        "id_filial": id_filial,
        "id_turma": id_turma
    }
    _aulas.append(nova_aula)

    return 0, None

def del_aula(id_turma: int) -> tuple[int, None]:
    """
    Exclui uma aula
    """
    for aula_dict in _aulas:
        if aula_dict["id_turma"] == id_turma:
            _aulas.remove(aula_dict)
            return 0, None

	# Turma nao encontrada
    return 1, None

def get_turmas_by_filial(id_filial: int) -> tuple[int, list[int]]:
    """
    Retorna uma lista com os IDs das turmas associadas a uma filial
    """
    turmas = []

    err, filial_dict = filial.get_filial(id_filial)
    if err != 0:
        # Filial não existe
        return err, None # type: ignore

    for aula_dict in _aulas:
        if aula_dict["id_filial"] == id_filial:
            turmas.append(aula_dict["id_turma"])
    
    if turmas:
        return 0, turmas
    else:
        return 59, None # type: ignore

def get_filial_by_turma(id_turma: int) -> tuple[int, int]:
    """
    Retorna o ID da filial associada a uma turma
    """
    err, turma_dict = turma.get_turma(id_turma)
    if err != 0:
        # Turma não existe
        return err, None # type: ignore

    for aula_dict in _aulas:
        if aula_dict["id_turma"] == id_turma:
            return 0, aula_dict["id_filial"]
    
    # Turma não encontrada
    return 1, None # type: ignore

# Setup
# Popula lista
_read()

# Salva lista ao final da execução
atexit.register(_write)
