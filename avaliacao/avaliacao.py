import os, stat, sys, json, subprocess, atexit, copy, datetime

# Exportando funções de acesso
__all__ = [
    "get_avaliacao",
    "get_avaliacoes",
    "add_avaliacao",
    "del_avaliacao",
    "set_avaliacao",
]

# Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")
_ID_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "proximo_id.txt")
_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "avaliacoes.json")
_BIN_FILE_PATH: str = _JSON_FILE_PATH.replace(".json", ".bin")

if os.name == "nt":
    _COMPACTADOR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "compactador_win.exe")
elif os.name == "posix":
    _COMPACTADOR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "compactador_unix")

    # Aplica permissão de executável
    os.chmod(_COMPACTADOR_PATH, os.stat(_COMPACTADOR_PATH).st_mode | stat.S_IEXEC)
else:
    print(f"Sistema operacional {os.name} não suportado")
    sys.exit(1)

# [
#     {
#         "id": int,
#         "nome": str,
#         "tipo": int,
#         "gabarito": list[int],
#         "perguntas": list[str]
#     },
#     ...
# ]
_avaliacoes: list[dict] = []


# Funções internas
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
            with open(_ID_FILE_PATH, "r") as file:
                id_atual = int(file.read())
        except Exception as e:
            print(f"Erro de I/O em gera_novo_id: {e}")
            return -1

    id_proximo = id_atual + 1

    try:
        with open(_ID_FILE_PATH, "w") as file:
            file.write(str(id_proximo))
    except Exception as e:
        print(f"Erro de I/O em gera_novo_id: {e}")
        return -1

    return id_atual


def _read_avaliacoes() -> None:
    """
    Descompacta o arquivo .bin em _BIN_FILE_PATH, lê o arquivo .json resultante em _JSON_FILE_PATH
    e armazena o conteúdo em _avaliacoes, uma lista de dicionários

    Se não existir, chama _write_avaliacoes parar criar um novo vazio
    """
    global _avaliacoes

    if not os.path.exists(_BIN_FILE_PATH):
        _write_avaliacoes()
        return

    # Descompactação
    subprocess.run([_COMPACTADOR_PATH, _BIN_FILE_PATH])

    try:
        with open(_JSON_FILE_PATH, "r") as file:
            _avaliacoes = json.load(file, object_hook=_str_para_datetime)
    except Exception as e:
        print(f"Erro de I/O em _read_avaliacoes: {e}")

    # Aqui deveríamos deletar o .json, mas vamos manter para fins de debug
    # os.remove(_JSON_FILE_PATH)


def _write_avaliacoes() -> None:
    """
    Realiza o dump da lista _avaliacoes para um arquivo json, definido em _JSON_FILE_PATH,
    e depois o compacta para um arquivo .bin usando o compactador em _COMPACTADOR_PATH

    Cria os arquivos necessários caso não existam, gerando uma lista vazia de avaliacoes
    """
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    try:
        with open(_JSON_FILE_PATH, "w") as file:
            json.dump(_avaliacoes, file, indent=2, default=_datetime_para_str)
    except Exception as e:
        print(f"Erro de I/O em _write_avaliacoes: {e}")

    # Compactação
    subprocess.run([_COMPACTADOR_PATH, _JSON_FILE_PATH])

    # Aqui deveríamos deletar o .json, mas vamos manter para fins de debug
    # os.remove(_JSON_FILE_PATH)


def _datetime_para_str(dt: datetime.datetime) -> str:
    """
    Converte um objeto datetime para uma string armanezável em JSON

    Chamada pelo json.dump quando ele não sabe como serializar um objeto
    """
    if isinstance(dt, datetime.datetime):
        return dt.isoformat()

    print(
        f"Erro ao converter objeto de tipo {type(dt).__name__} para uma string de datetime"
    )


def _str_para_datetime(turma_dict: dict) -> dict:
    """
    Converte uma string de datetime para um objeto datetime

    Chamada pelo json.load quando ele não sabe como desserializar um objeto
    """
    for key, value in turma_dict.items():
        if key == "data_ini" and isinstance(value, str):
            try:
                turma_dict[key] = datetime.datetime.fromisoformat(value)
            except ValueError:
                print(f"Erro ao converter {value} para datetime")

    return turma_dict


# Funções de acesso
def get_avaliacao(id_turma: int) -> tuple[int, dict]:
    """
    Retorna o dicionário com os atributos da avaliacao especificada
    """
    for avaliacao in _avaliacoes:
        if avaliacao["id"] == id_turma:
            return 0, copy.deepcopy(avaliacao)

    # Avaliacao não encontrada
    return 52, None  # type: ignore


def get_avaliacoes() -> tuple[int, list[dict]]:
    """
    Retorna uma lista com todos os dicionários contendo os atributos de cada avaliacao
    """
    return 0, copy.deepcopy(_avaliacoes)


def add_avaliacao(
    nome: str, tipo: int, gabarito: list[int], perguntas: list[str]
) -> tuple[int, int]:
    """
    Cria uma nova avaliacao com os atributos especificados

    Retorna o ID da nova avaliacao
    """
    if not len(gabarito) == len(perguntas):
        # Perguntas e Gabarito tem tamanhos diferentes
        return 56, None  # type: ignore

    novo_id = _gera_novo_id()
    if novo_id == -1:
        # Erro ao gerar o ID
        return 8, None  # type: ignore

    nova_avaliacao = {
        "id": novo_id,
        "nome": nome,
        "tipo": tipo,
        "gabarito": gabarito,
        "perguntas": perguntas,
    }

    _avaliacoes.append(nova_avaliacao)

    return 0, novo_id


def set_avaliacao(
    id_avaliacao: int, nome: str, tipo: int, gabarito: list[int], perguntas: list[str]
) -> tuple[int, int]:
    """
    Atualiza uma avaliação
    """

    if not len(gabarito) == len(perguntas):
        # Perguntas e Gabarito tem tamanhos diferentes
        return 56, None  # type: ignore

    if perguntas == []:
        # Avaliação não possui nenhuma questão
        return 57, None  # type: ignore

    for avaliacao in _avaliacoes:
        if avaliacao["id"] == id_turma:
            avaliacao["nome"] = nome
            avaliacao["tipo"] = nome
            avaliacao["gabarito"] = gabarito
            avaliacao["perguntas"] = perguntas
            return 0, copy.deepcopy(turma)

    # avaliação não encontrada
    return 52, None


def del_avaliacao(id_turma: int) -> tuple[int, None]:
    """
    Remove uma avaliacao pelo seu ID
    """
    for avaliacao in _avaliacoes:
        if avaliacao["id"] == id_turma:
            _avaliacoes.remove(avaliacao)
            return 0, None

    # avaliação não encontrada
    return 52, None


# Setup
# Popular lista de avaliacoes
_read_avaliacoes()

# Salvar avaliacoes ao final do programa
atexit.register(_write_avaliacoes)

# Isso executa quando avaliacao.py é executado diretamente, mas não quando importado
# Testes iniciais podem ser feitos aqui

# avaliacao = {"Perguntas":["Oi?","Meu?","Nome?"],"Gabarito":[2,3,5]}
# respostas={"id_aluno":id_aluno,"id_avaliaca":id_avaliacao,"respostas":[2,3,4]}
if __name__ == "__main__":
    # criando alguns dados para testes
    _, a1 = add_avaliacao(
        "P1", 1, [1, 2, 3], ["Pergunta 1", "Pergunta 2", "Pergunta 3"]
    )
    _, a2 = add_avaliacao(
        "P2", 2, [3, 2, 1], ["Pergunta A", "Pergunta B", "Pergunta C"]
    )
    _, a3 = add_avaliacao(
        "PF", 3, [2, 2, 1], ["Pergunta X", "Pergunta Y", "Pergunta Z"]
    )

    print(get_avaliacao(a1))
    print(get_avaliacoes())

    del_avaliacao(a1)
    del_avaliacao(a2)
    del_avaliacao(a3)

    print(get_avaliacoes())
