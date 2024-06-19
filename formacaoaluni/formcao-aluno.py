__all__ = ['inicializar', 'finalizar', 'add_formatura', 'notify_curso_concluido', 'get_formaturas_by_aluno', 'get_formaturas', 'get_alunos_by_formatura', 'is_concluida']

import json, atexit, formacao

# Variáveis globais
lista_formatura = list()
formaturas_deletadas = list()

PATH = "data/formacao-aluno.json"

# Códigos de erro
OPERACAO_REALIZADA_COM_SUCESSO = 0
ALUNO_NAO_ENCONTRADO = 16
ARQUIVO_NAO_ENCONTRADO = 30
ARQUIVO_EM_FORMATO_INVALIDO = 31
ERRO_NA_ESCRITA_DO_ARQUIVO = 32
FORMATURA_NAO_ENCONTRADA = 40
FORMATURA_JA_EXISTE = 41
FORMATURA_NAO_ATIVA = 42
CURSO_NAO_CONCLUIDO = 51

# Funções para leitura de Json
def inicializar() -> int:
    global lista_formaturas

    try:
        with open(PATH, 'r') as arquivo:
            try:
                lista_formaturas = json.load(arquivo)
            except json.JSONDecodeError: return ARQUIVO_EM_FORMATO_INVALIDO
    except FileNotFoundError: return ARQUIVO_NAO_ENCONTRADO

    return OPERACAO_REALIZADA_COM_SUCESSO

def finalizar() -> int:
    try:
        with open(PATH, 'w') as arquivo:
            json.dump(obj=lista_formaturas, fp=arquivo, indent=4)
    except OSError: return ERRO_NA_ESCRITA_DO_ARQUIVO

    return OPERACAO_REALIZADA_COM_SUCESSO

# Funções de acesso

# adiciona uma nova formatura para um aluno em formação específica
def add_formatura(id_aluno: int, id_formacao: int) -> tuple[int, dict]:
    global lista_formaturas
    formatura = {"id_aluno": id_aluno, "id_formacao": id_formacao, "cursos_concluidos": list()}
    lista_formatura.append(formatura)
    return OPERACAO_REALIZADA_COM_SUCESSO, formatura

# verifica se um curso foi concluído por um aluno
def notify_curso_concluido(id_aluno: int, id_curso: int) -> int:
    global lista_formatura
    for formatura in lista_formatura:
        if(formatura["id_aluno"] == id_aluno):
            formatura["cursos_concluidos"].append(id_curso)
            return OPERACAO_REALIZADA_COM_SUCESSO
    return FORMATURA_NAO_ENCONTRADA


# retorna uma lista com as formaturas associadas a um aluno
def get_formaturas_by_aluno(id_aluno: int)-> tuple[int, list[dict]]:
    global lista_formatura
    formatura_by_aluno = list()
    for formatura in lista_formatura:
        if(formatura["id_aluno"] == id_aluno):
            formatura_by_aluno.append(formatura["id_formacao"])
    return OPERACAO_REALIZADA_COM_SUCESSO, formatura_by_aluno

# retorna uma lista de todas as formaturas
def get_formaturas() -> tuple[int, list[dict]]:
    return OPERACAO_REALIZADA_COM_SUCESSO, lista_formatura

# retorna uma lista com os IDs de alunos associados a uma formação específica
def get_alunos_by_formatura(id_formacao) -> tuple[int, list[int]]:
    global lista_formatura
    alunos_by_formacao = list()
    for formatura in lista_formatura:
        if(formatura["id_formacao"] == id_formacao):
            alunos_by_formacao.append(formatura["id_aluno"])
    return OPERACAO_REALIZADA_COM_SUCESSO, alunos_by_formacao

# verifica se um aluno concluiu uma formação (NAO CONCLUIDA)
def is_concluida(id_aluno: int, id_formacao: int) -> tuple[int, bool]:
    for formatura in lista_formaturas:
        if formatura.get("id_aluno") == id_aluno and formatura.get("id_formacao") == id_formacao:
            # Verifica se todos os cursos da formação foram concluídos
            _, formacao = formacao.get_formacao(id_formacao)
            cursos_formacao = formacao.get("cursos", [])
            cursos_concluidos = formatura.get("cursos_concluidos", [])

            if set(cursos_formacao).issubset(set(cursos_concluidos)):
                return OPERACAO_REALIZADA_COM_SUCESSO, True
            else:
                return OPERACAO_REALIZADA_COM_SUCESSO, False
    return FORMATURA_NAO_ENCONTRADA, False


# Funções internas
def exibe_formaturas():
    status, formaturas_ativas = get_formaturas()
    if status == OPERACAO_REALIZADA_COM_SUCESSO:
        for formatura in lista_formaturas:
            print(formatura)
    else:
        print("Código de erro: {status}")

# main
erro = inicializar()
if erro != 0:
    print(erro)


# Salvar turmas ao final do programa
atexit.register(finalizar)
