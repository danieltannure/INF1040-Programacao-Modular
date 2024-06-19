import json
import os
from typing import Tuple, List

__all__ = ["add_aula", "del_aula", "get_turmas_por_filial","get_filial_por_turma"]

# Variáveis Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))  # Caminho do diretório do script atual
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")  # Caminho do diretório 'data' dentro do diretório do script
_TURMAS_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "aula.json")  # Caminho completo para o arquivo 'turmas.json'

# Códigos de Erro
OPERACAO_REALIZADA_COM_SUCESSO = 0  # Código de retorno para operação bem-sucedida
ARQUIVO_NAO_ENCONTRADO = 30  # Código de retorno para arquivo não encontrado
ARQUIVO_EM_FORMATO_INVALIDO = 31  # Código de retorno para arquivo em formato inválido
ERRO_NA_ESCRITA_DO_ARQUIVO = 32  # Código de retorno para erro na escrita do arquivo
TURMA_JA_EXISTE = 36  # Código de retorno para tentativa de adicionar uma turma que já existe
TURMA_NAO_ENCONTRADA = 1  # Código de retorno para tentativa de excluir uma turma que não existe
ERRO_DESCONHECIDO = 34  # Código de retorno para erro desconhecido

def add_aula(id_turma: int, filial_id: int) -> int:
    """
    Adiciona uma turma ao arquivo JSON de turmas.

    Args:
        id_turma (int): ID da turma a ser adicionada.
        filial_id (int): ID da filial à qual a turma será vinculada.

    Returns:
        int: Código de retorno indicando o resultado da operação.
    """
    try:
        with open(_TURMAS_JSON_FILE_PATH, 'r') as file:
            turmas = json.load(file)

        if str(filial_id) not in turmas:
            turmas[str(filial_id)] = []

        if id_turma in turmas[str(filial_id)]:
            return TURMA_JA_EXISTE

        turmas[str(filial_id)].append(id_turma)

        with open(_TURMAS_JSON_FILE_PATH, 'w') as file:
            json.dump(turmas, file, indent=4)

        return OPERACAO_REALIZADA_COM_SUCESSO
    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO
    except Exception as e:
        return ERRO_DESCONHECIDO

def del_aula(id_turma: int) -> int:
    """
    Exclui uma turma do arquivo JSON de turmas.

    Args:
        id_turma (int): ID da turma a ser excluída.

    Returns:
        int: Código de retorno indicando o resultado da operação.
    """
    try:
        with open(_TURMAS_JSON_FILE_PATH, 'r') as file:
            turmas = json.load(file)

        turma_encontrada = False
        for filial_id in turmas:
            if id_turma in turmas[filial_id]:
                turmas[filial_id].remove(id_turma)
                turma_encontrada = True
                break

        if not turma_encontrada:
            return TURMA_NAO_ENCONTRADA

        with open(_TURMAS_JSON_FILE_PATH, 'w') as file:
            json.dump(turmas, file, indent=4)

        return OPERACAO_REALIZADA_COM_SUCESSO
    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO
    except Exception as e:
        return ERRO_DESCONHECIDO

def get_turmas_por_filial(filial_id: int) -> Tuple[int, List[int]]:
    """
    Retorna todas as turmas de uma filial específica do arquivo JSON de turmas.

    Args:
        filial_id (int): ID da filial para buscar as turmas.

    Returns:
        Tuple[int, List[int]]: Tupla contendo um código de erro ou sucesso
        e uma lista de IDs das turmas encontradas.
    """
    try:
        with open(_TURMAS_JSON_FILE_PATH, 'r') as file:
            turmas = json.load(file)

        if str(filial_id) in turmas:
            return OPERACAO_REALIZADA_COM_SUCESSO, turmas[str(filial_id)]
        return TURMA_NAO_ENCONTRADA, []
    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO, []
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO, []
    except Exception as e:
        return ERRO_DESCONHECIDO, []

def get_filial_por_turma(turma_id: int) -> tuple:
    """
    Retorna todas as filiais que possuem uma determinada turma do arquivo JSON de turmas.

    Args:
        turma_id (int): ID da turma para buscar as filiais.

    Returns:
        Tuple[int, List[int]]: Tupla contendo um código de erro ou sucesso e uma lista de IDs das filiais encontradas.
    """
    try:
        with open(_TURMAS_JSON_FILE_PATH, 'r') as file:
            turmas = json.load(file)

        filiais_com_turma = []
        for filial_id, turmas_da_filial in turmas.items():
            if turma_id in turmas_da_filial:
                filiais_com_turma.append(int(filial_id))

        if filiais_com_turma:
            return OPERACAO_REALIZADA_COM_SUCESSO, filiais_com_turma
        else:
            return TURMA_NAO_ENCONTRADA, []

    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO, []
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO, []
    except Exception as e:
        return ERRO_DESCONHECIDO,[]

print(get_turmas_por_filial(1))