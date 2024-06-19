import json, atexit
from .. import curso, avaliacao

# from mockAvaliacaoCurso import get_curso, get_avaliacao #type: ignore

__all__ = ["add_avaliacao_ao_criterio", "del_avaliacao_do_criterio", "get_criterio"]

FILE_NAME = "criterios.json"

criterios: list[dict] = []  # lista para armazenar os criterios
"""
[
  {
    'curso': id_curso, 
    'avaliacoes': [id_avaliacao]
  },
  ...

]
"""

"""
Códigos de ERRO do Módulo

53 - avaliação já existe no criterio
54 - avaliação não encontrada no criterio
55 - criterio não encontrado
"""


# ----------funcoes de acesso-------------
def add_avaliacao_ao_criterio(id_curso: int, id_avaliacao: int) -> int:
    """
    Adiciona uma avaliação (em uma instância de dicionário) de um criterio (atrelado ao id_curso)

    Caso o id_avaliacao já exista no criterio -> retorna o código de erro 53

    Caso a instância de dicionário referente ao criterio não exista -> cria uma nova instância de dicionário e adiciona o id_avaliacao no criterio
    """

    # checa_curso_e_avaliacao = existe_curso_e_avaliacao(id_curso, id_avaliacao)
    # if checa_curso_e_avaliacao != 0:
    #  return checa_curso_e_avaliacao

    for criterio in criterios:
        if criterio["curso"] == id_curso:
            for avaliacao in criterio["avaliacoes"]:
                if avaliacao == id_avaliacao:
                    return 53  # ERRO: avaliação já existe no criterio

            criterio["avaliacoes"].append(id_avaliacao)
            return 0

    novoCriterio: dict = {
        "curso": id_curso,
        "avaliacoes": [id_avaliacao],
    }  # se o criterio não existir, cria um novo
    criterios.append(novoCriterio)
    return 0


def del_avaliacao_do_criterio(id_curso: int, id_avaliacao: int) -> int:
    """
    Deleta uma avaliação (de uma instância de dicionário) de um criterio (atrelado ao id_curso)

    Se, após a operação, a lista de avaliações do criterio estiver vazia -> deleta o criterio da lista de criterios

    Caso o id_avaliacao não exista no criterio -> retorna o código de erro 54

    Caso o criterio não exista -> retorna o código de erro 55
    """

    # checa_curso_e_avaliacao = existe_curso_e_avaliacao(id_curso, id_avaliacao)
    # if checa_curso_e_avaliacao != 0:
    #  return checa_curso_e_avaliacao

    for criterio in criterios:
        if criterio["curso"] == id_curso:

            for avaliacao in criterio["avaliacoes"]:
                if avaliacao == id_avaliacao:

                    criterio["avaliacoes"].remove(id_avaliacao)
                    if (
                        len(criterio["avaliacoes"]) == 0
                    ):  # se criterio nao tem mais avaliaçoes, o mesmo é excluido
                        criterios.remove(criterio)
                    return 0

            return 54  # ERRO: avaliação não encontrada no criterio

    return 55  # ERRO: criterio não encontrado


def get_criterio(id_curso: int) -> tuple[int, list[int]]:
    """
    Retorna uma copia da lista de avaliações (de uma instância de dicionário) de um criterio (atrelado ao id_curso)

    Caso o criterio não exista, retorna o código de erro 55
    """

    # curso = get_curso(id_curso)
    # if (curso != 0):
    #  return (curso,[]) #ERRO: curso nao encontrado

    for criterio in criterios:
        if criterio["curso"] == id_curso:
            return (0, criterio["avaliacoes"].copy())  # criterio encontrado

    return (55, [])  # ERRO: criterio não encontrado


# ----------funcoes auxiliares de arquivo-------------
def carregar_criterios() -> None:
    global criterios
    try:
        with open(FILE_NAME, "r") as file:
            criterios = json.load(file)
    except FileNotFoundError:
        criterios = []


def salvar_criterios() -> None:
    with open(FILE_NAME, "w") as file:
        json.dump(criterios, file, indent=4)


# ----------funcoes auxiliares-------------
def existe_curso_e_avaliacao(id_curso: int, id_avaliacao: int) -> int:
    curso = curso.get_curso(id_curso)
    avaliacao = avaliacao.get_avaliacao(id_avaliacao)

    if curso != 0:
        return curso

    if avaliacao != 0:
        return avaliacao

    return 0


# ----------SETUP-------------
# Popular lista de criterios
carregar_criterios()

# Salvar turmas ao final do programa
atexit.register(salvar_criterios)

# ----------testes-------------
if __name__ == "__main__":

    carregar_criterios()

    id_av = 100
    id_curso = 8

    # add
    print(
        "add avaliaçao id:("
        + str(id_av)
        + ") ao curso id:("
        + str(id_curso)
        + ") -> "
        + str(add_avaliacao_ao_criterio(id_curso, id_av))
    )
    print(
        "add avaliaçao id:("
        + str(id_av + 1)
        + ") ao curso id:("
        + str(id_curso)
        + ") -> "
        + str(add_avaliacao_ao_criterio(id_curso, id_av + 1))
    )

    # get
    print(
        "get criterio do curso id:("
        + str(id_curso)
        + ") -> "
        + str(get_criterio(id_curso))
    )
    print(
        "get criterio do curso id:("
        + str(id_curso + 1)
        + ") -> "
        + str(get_criterio(id_curso + 1))
    )  # curso inexistente

    # del
    print(
        "del avaliaçao id:("
        + str(id_av)
        + ") do curso id:("
        + str(id_curso)
        + ") -> "
        + str(del_avaliacao_do_criterio(id_curso, id_av))
    )
    print(
        "del avaliaçao id:("
        + str(id_av - 1)
        + ") do curso id:("
        + str(id_curso)
        + ") -> "
        + str(del_avaliacao_do_criterio(id_curso, id_av - 1))
    )  # avaliacao inexistente
    print(
        "del avaliaçao id:("
        + str(id_av)
        + ") do curso id:("
        + str(id_curso + 1)
        + ") -> "
        + str(del_avaliacao_do_criterio(id_curso + 1, id_av))
    )  # curso inexistente

    # get
    print(
        "get criterio do curso id:("
        + str(id_curso)
        + ") -> "
        + str(get_criterio(id_curso))
    )

    # del
    print(
        "del avaliaçao id:("
        + str(id_av + 1)
        + ") do curso id:("
        + str(id_curso)
        + ") -> "
        + str(del_avaliacao_do_criterio(id_curso, id_av + 1))
    )

    # get
    print(
        "get criterio do curso id:("
        + str(id_curso)
        + ") -> "
        + str(get_criterio(id_curso))
    )

    salvar_criterios()
