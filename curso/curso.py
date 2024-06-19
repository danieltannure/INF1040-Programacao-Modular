__all__ = [ 'inicializar', 'finalizar', 'get_curso', 'get_cursos', 'add_curso', 'del_curso']

import json, atexit

# Variaveis globais
lista_cursos = list()
cursos_deletados = list()

PATH = "data/curso.json"


# Códigos de erro
OPERACAO_REALIZADA_COM_SUCESSO = 0

ARQUIVO_NAO_ENCONTRADO = 30
ARQUIVO_EM_FORMATO_INVALIDO = 31
ERRO_NA_ESCRITA_DO_ARQUIVO = 32

CURSO_NAO_ENCONTRADO = 5
CURSO_JA_EXISTE = 38
CURSO_NAO_ATIVO = 39

# Funções para leitura de Json
def inicializar() -> int:
    global lista_cursos, cursos_deletados

    try:
        with open(PATH, 'r') as arquivo:
            try:
                dados = json.load(arquivo)
            except json.JSONDecodeError: return ARQUIVO_EM_FORMATO_INVALIDO
    except FileNotFoundError: return ARQUIVO_NAO_ENCONTRADO

    lista_cursos = dados["lista_cursos"]
    cursos_deletados = dados["cursos_deletados"]

    return OPERACAO_REALIZADA_COM_SUCESSO

def finalizar() -> int:
    global lista_cursos, cursos_deletados

    dados = {"lista_cursos": lista_cursos, "cursos_deletados": cursos_deletados}

    try:
        with open(PATH, 'w') as arquivo:
            json.dump(obj = dados, fp = arquivo, indent = 4)
    except OSError: return ERRO_NA_ESCRITA_DO_ARQUIVO

    return OPERACAO_REALIZADA_COM_SUCESSO


# Funcoes de acesso
def get_curso(id: int) -> tuple[int, dict]:
    for curso in lista_cursos:
        if(curso.get("id") == id):
            if curso in cursos_deletados:
                return CURSO_NAO_ATIVO, curso
            else:
                return OPERACAO_REALIZADA_COM_SUCESSO, curso
    return CURSO_NAO_ENCONTRADO, None    
    

def get_cursos() -> tuple[int, list[dict]]:
    cursos_ativos =[]
    for curso in lista_cursos:
        if curso not in cursos_deletados:
            cursos_ativos.append(curso)
    return OPERACAO_REALIZADA_COM_SUCESSO, cursos_ativos

def add_curso(nome: str, carga_horaria: int, prereqs: list[int], duracao_semanas: int) -> tuple[int, int]:
    global lista_cursos

    curso = {
        "id": len(lista_cursos) + 1,
        "nome": nome,
        "carga_horaria": carga_horaria,
        "prereqs": prereqs,
        "duracao_semanas": duracao_semanas
    }

    for curso in lista_cursos:
        if curso["nome"] == nome:
            return 38, None

    lista_cursos.append(curso)
    return OPERACAO_REALIZADA_COM_SUCESSO, id
    

def del_curso(id: int) -> tuple[int, int]:
    global cursos_deletados

    sinal, curso = get_curso(id)        # sinal é o codigo do erro
    
    if sinal == OPERACAO_REALIZADA_COM_SUCESSO:
        cursos_deletados.append(curso)

    return sinal, id    
    

# Funcoes internas
def exibe_curso(id):
    print(get_curso(id))   

def exibe_cursos():
    erro, lista = get_cursos()
    for curso in lista:
        print(curso)
        print("\n")
    return erro


# main
erro = inicializar()
if erro != 0:
    print(erro)


# Salvar turmas ao final do programa
atexit.register(finalizar)



