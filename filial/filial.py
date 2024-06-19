import os, json, atexit, copy

__all__ = ["add_filial", "del_filial", "get_filial", "get_filiais", "get_filial_proxima"]

# Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")
_ID_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "proximo_id.txt")
_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "filiais.json")

# [
#     {
#         "id": int,
#         "nome": str,
#         "bairro": str
#     },
#     ...
# ]
_filiais: list[dict] = []

# Internas
def _gera_novo_id() -> int:
    """
    Gera sequencialmente um novo ID único, para uma nova instância de dicionário

    Utiliza o arquivo especificado em ID_FILE_PATH para guardar o próximo ID que deve ser gerado

    Cria os arquivos e diretórios necessários caso não existam

    Retorna -1 caso ocorra um erro de I/O ao ler ou escrever o arquivo de ID
    """
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    if not os.path.exists(_ID_FILE_PATH):
        id_atual = 1
    else:
        try:
            with open(_ID_FILE_PATH, 'r') as file:
                id_atual = int(file.read())
        except Exception as e:
            print(f"Erro de I/O em gera_novo_id: {e}")
            return -1

    id_proximo = id_atual + 1

    try:
        with open(_ID_FILE_PATH, 'w') as file:
            file.write(str(id_proximo))
    except Exception as e:
        print(f"Erro de I/O em gera_novo_id: {e}")
        return -1

    return id_atual

def _read() -> None:
    """
    Iniciaiza
    """
    global _filiais

    if not os.path.exists(_JSON_FILE_PATH):
        _write()
        return

    try:
        with open(_JSON_FILE_PATH, 'r') as file:
            _filiais = json.load(file)
    except Exception as e:
        print(f"Erro de I/O em filial: {e}")

def _write() -> None:
    """
    Salva
    """
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    try:
        with open(_JSON_FILE_PATH, 'w') as file:
            json.dump(_filiais, file, indent=2)
    except Exception as e:
        print(f"Erro de I/O em filial: {e}")

# Acesso

# Setup
# Popula lista
_read()

# Salva lista ao final da execução
atexit.register(_write)
