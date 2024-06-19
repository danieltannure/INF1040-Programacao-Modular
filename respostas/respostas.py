import os, stat, sys, json, subprocess, atexit, copy, datetime
from .. import avaliacao

# Exportando funções de acesso
__all__ = [
    "add_resposta",
    "get_resposta",
    "get_respostas_by_aluno",
    "get_respostas_by_avaliacao",
]

# Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")
_ID_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "proximo_id.txt")
_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "respostas.json")
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


_respostas: list[dict] = []


# Funões internas
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

def _read_respostas() -> None:
    """
    Descompacta o arquivo .bin em _BIN_FILE_PATH, lê o arquivo .json resultante em _JSON_FILE_PATH
    e armazena o conteúdo em _respostas, uma lista de dicionários

    Se não existir, chama _write_respostas parar criar um novo vazio
    """
    global _respostas

    if not os.path.exists(_BIN_FILE_PATH):
        _write_respostas()
        return

    # Descompactação
    subprocess.run([_COMPACTADOR_PATH, _BIN_FILE_PATH])

    try:
        with open(_JSON_FILE_PATH, "r") as file:
            _respostas = json.load(file, object_hook=_str_para_datetime)
    except Exception as e:
        print(f"Erro de I/O em _read_avaliacoes: {e}")

    # Aqui deveríamos deletar o .json, mas vamos manter para fins de debug
    # os.remove(_JSON_FILE_PATH)

def _write_respostas() -> None:
    """
    Realiza o dump da lista _respostas para um arquivo json, definido em _JSON_FILE_PATH,
    e depois o compacta para um arquivo .bin usando o compactador em _COMPACTADOR_PATH

    Cria os arquivos necessários caso não existam, gerando uma lista vazia de avaliacoes
    """
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    try:
        with open(_JSON_FILE_PATH, "w") as file:
            json.dump(_respostas, file, indent=2, default=_datetime_para_str)
    except Exception as e:
        print(f"Erro de I/O em _write_respostas: {e}")

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

def _str_para_datetime(resposta_dict: dict) -> dict:
    """
    Converte uma string de datetime para um objeto datetime

    Chamada pelo json.load quando ele não sabe como desserializar um objeto
    """
    for key, value in resposta_dict.items():
        if key == "data_ini" and isinstance(value, str):
            try:
                resposta_dict[key] = datetime.datetime.fromisoformat(value)
            except ValueError:
                print(f"Erro ao converter {value} para datetime")

    return resposta_dict

def _calcular_notas(respostas_aluno, avaliacao):
    for resposta in respostas_aluno:
        nota = 0
        for resposta_aluno, resposta_correta in zip(resposta["respostas"], avaliacao["gabarito"]):
            if resposta_aluno == resposta_correta:
                nota += 1
        resposta["nota"] = nota


# Funções de acesso
def add_resposta(id_aluno, id_avaliacao, respostas_aluno):
    novo_id = _gera_novo_id()
    if novo_id == -1:
        # Erro ao gerar o ID
        return 8, None  # type: ignore
    
    avaliacoes = avaliacao.get_avaliacoes()
    avaliacao = avaliacoes.get(id_avaliacao)

    if avaliacao is None:
        # Avaliação não encontrada
        return 52, None
    
    nova_resposta = {
        "id": novo_id,
        "id_aluno": id_aluno,
        "id_avaliacao": id_avaliacao,
        "respostas": respostas_aluno,
        "nota": 0 
    }

    _respostas.append(nova_resposta)
    _calcular_notas([nova_resposta], avaliacao)
    return 0, nova_resposta


def get_resposta(id_aluno, id_avaliacao):
    for resposta in _respostas:
        if resposta["id_aluno"] == id_aluno and resposta[
                "id_avaliacao"] == id_avaliacao:
            return 0, resposta
        
    # Nenhuma resposta foi achada para estes ids (avaliação com este id e/ou aluno com este id).
    erro = 13
    return 13, None


def get_respostas_by_aluno(id_aluno):
    respostas_aluno = []
    for resposta in _respostas:
        if resposta["id_aluno"] == id_aluno:
            respostas_aluno.append(resposta)

    if respostas_aluno == []:
        # Nenhuma resposta foi achada para este aluno (aluno com este id).
        return 14, None
    else:
        return 0, respostas_aluno


def get_respostas_by_avaliacao(id_avaliacao):
    respostas_avaliacao = []
    
    for resposta in _respostas:
        if resposta["id_avaliacao"] == id_avaliacao:
            respostas_avaliacao.append(resposta)

    if respostas_avaliacao == []:
        # Nenhuma resposta foi achada para esta avaliação (avaliação com este id)
        return 15, None
    else:
        return 0, respostas_avaliacao



# Setup
_read_respostas()

atexit.register(_write_respostas)



if __name__ == "__main__":
    print("Retorno add_resposta:\n")

    print("Resposta de avaliação criada com sucesso:")
    print(add_resposta(1, 101, [1, 2, 3]))
    print("\n")
    print(add_resposta(1, 102, [4, 5, 6]))
    print("\n")
    print(add_resposta(2, 101, [1, 2, 0]))
    print("\n")
    print(add_resposta(2, 101, [1, 0, 0]))
    print("\n")
    print(add_resposta(2, 101, [0, 0, 0]))
    print("\n")
    print(add_resposta(3, 102, [4, 0, 0]))
    print("\n")
    print(add_resposta(3, 102, [4, 5, 0]))
    print("\n")

    print("Avaliação com id que não existe (não encontrado):")
    print(add_resposta(3, 103, [4, 5, 0]))
    print("\n")

    #obtendo uma resposta específica
    print("Retorno get_resposta:\n")
    print(get_resposta(1, 101))
    print(get_resposta(3, 102))
    print(get_resposta(3, 101))
    print("\n")

    #obtendo todas as respostas de um aluno
    print("Retorno get_respostas_by_aluno:\n")
    print(get_respostas_by_aluno(1))
    print("\n")

    #obtendo todas as respostas de uma avaliação
    print("Retorno get_respostas_by_avaliacao:\n")
    print(get_respostas_by_avaliacao(101))
    print("\n")