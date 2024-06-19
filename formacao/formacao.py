__all__ = [ 'inicializar', 'finalizar', 'get_formacao', 'get_formacoes', 'add_formacao', 'del_formacao' ]

import json, atexit

# Variaveis globais
lista_formacoes = list()
formacoes_deletadas = list()

PATH = "data/formacao.json"


# Códigos de erro
OPERACAO_REALIZADA_COM_SUCESSO = 0

ARQUIVO_NAO_ENCONTRADO = 30
ARQUIVO_EM_FORMATO_INVALIDO = 31
ERRO_NA_ESCRITA_DO_ARQUIVO = 32

FORMACAO_NAO_ENCONTRADO = 40
FORMACAO_JA_EXISTE = 41
FORMACAO_NAO_ATIVO = 42

# Funções para leitura de Json
def inicializar() -> int:
    global lista_formacoes, formacoes_deletadas

    try:
        with open(PATH, 'r') as arquivo:
            try:
                dados = json.load(arquivo) ### verificar nos 2 arquivos
            except json.JSONDecodeError: return ARQUIVO_EM_FORMATO_INVALIDO
    except FileNotFoundError: return ARQUIVO_NAO_ENCONTRADO

    lista_formacoes = dados["lista_formacoes"]
    formacoes_deletadas = dados["formacoes_deletadas"]

    return OPERACAO_REALIZADA_COM_SUCESSO

def finalizar() -> int:
    global lista_formacoes, formacoes_deletadas

    dados = {"lista_formacoes": lista_formacoes, "formacoes_deletadas": formacoes_deletadas}

    try:
        with open(PATH, 'w') as arquivo:
            json.dump(obj = dados, fp = arquivo, indent = 4) ### verificar nos 2 arquivos
    except OSError: return ERRO_NA_ESCRITA_DO_ARQUIVO

    return OPERACAO_REALIZADA_COM_SUCESSO


# Funcoes de acesso
def get_formacao(id: int) -> tuple[int, dict]:
    for formacao in lista_formacoes:
        if(formacao.get("id") == id):
            if formacao in formacoes_deletadas:
                return FORMACAO_NAO_ATIVO, formacao
            else:
                return OPERACAO_REALIZADA_COM_SUCESSO, formacao
    return FORMACAO_NAO_ENCONTRADO, None    
    

def get_formacoes() -> tuple[int, list[dict]]:
    formacoes_ativas = []
    for formacao in lista_formacoes:
        if formacao not in formacoes_deletadas:
            formacoes_ativas.append(formacao)
    return OPERACAO_REALIZADA_COM_SUCESSO, formacoes_ativas

def add_formacao(nome: str, cursos: list[int]) -> tuple[int, int]:
    global lista_formacoes

    formacao = {
        "id": len(lista_formacoes)+1,
        "nome": nome,
        "cursos": cursos
    }

    for formacao in lista_formacoes:
        if formacao["nome"] == nome:
            return 41, None
        
    lista_formacoes.append(formacao)
    return OPERACAO_REALIZADA_COM_SUCESSO, id

def del_formacao(id: int) -> tuple[int, int]:
    global formacoes_deletadas

    sinal, formacao = get_formacao(id)      # sinal é o codigo do erro
    
    if sinal == OPERACAO_REALIZADA_COM_SUCESSO:
        formacoes_deletadas.append(formacao)

    return sinal, id

# Funcoes internas
def exibe_formacao(id):
    print(get_formacao(id))   

def exibe_formacoes():
    erro, lista = get_formacoes()
    for formacao in lista:
        print(formacao)
        print("\n")
    return erro

# main
erro = inicializar()
if erro != 0:
    print(erro)


# Salvar turmas ao final do programa
atexit.register(finalizar)


