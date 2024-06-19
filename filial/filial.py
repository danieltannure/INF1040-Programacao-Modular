import json
import os
from typing import Tuple, Union, List, Dict

__all__ = ["add_filial", "del_filial", "get_filial", "get_filiais", "get_filial_proxima"]

# Variáveis Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))  # Caminho do diretório do script atual
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")  # Caminho do diretório 'data' dentro do diretório do script 
_FILIAIS_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "filiais.json")  # Caminho completo para o arquivo 'filiais.json'

# Códigos de Erro
OPERACAO_REALIZADA_COM_SUCESSO = 0  # Código de retorno para operação bem-sucedida
ARQUIVO_NAO_ENCONTRADO = 30  # Código de retorno para arquivo não encontrado
ARQUIVO_EM_FORMATO_INVALIDO = 31  # Código de retorno para arquivo em formato inválido
ERRO_NA_ESCRITA_DO_ARQUIVO = 32  # Código de retorno para erro na escrita do arquivo
FILIAL_NAO_ENCONTRADA = 33  # Código de retorno para filial não encontrada
ERRO_DESCONHECIDO = 34  # Código de retorno para erro desconhecido
BAIRRO_NAO_ENCONTRADO = 35  # Código de retorno para bairro não encontrado

def add_filial(id: int, nome: str, bairro: str) -> int:
    """
    Cria uma nova filial e adiciona ao arquivo JSON de filiais.

    Args:
        id (int): ID da nova filial.
        nome (str): Nome da nova filial.
        bairro (str): Bairro da nova filial.

    Returns:
        int: Código de retorno indicando o resultado da operação.
    """
    try:
        # Carrega o arquivo de filiais existente
        with open(_FILIAIS_JSON_FILE_PATH, 'r') as file:
            filiais = json.load(file)

        # Verifica se o ID da filial já existe
        if any(f['id'] == id for f in filiais):
            return ERRO_DESCONHECIDO  # ou um código específico para ID duplicado

        # Adiciona a nova filial à lista de filiais
        filiais.append({
            'id': id,
            'nome': nome,
            'bairro': bairro
        })

        # Escreve de volta ao arquivo JSON
        with open(_FILIAIS_JSON_FILE_PATH, 'w') as file:
            json.dump(filiais, file, indent=4)

        return OPERACAO_REALIZADA_COM_SUCESSO  # Operação bem-sucedida
    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO  # Arquivo não encontrado
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO  # Arquivo em formato inválido
    except Exception as e:
        return ERRO_DESCONHECIDO  # Outro erro desconhecido

def del_filial(id_filial: int) -> int:
    """
    Remove uma filial do arquivo JSON de filiais com base no ID fornecido.

    Args:
        id_filial (int): ID da filial a ser removida.

    Returns:
        int: Código de retorno indicando o resultado da operação.
    """
    try:
        # Carrega o arquivo de filiais existente
        with open(_FILIAIS_JSON_FILE_PATH, 'r') as file:
            filiais = json.load(file)

        # Verifica se a filial com o ID especificado existe
        filial_encontrada = False
        for filial in filiais:
            if filial['id'] == id_filial:
                filiais.remove(filial)
                filial_encontrada = True
                break

        if not filial_encontrada:
            return ERRO_DESCONHECIDO  # ou um código específico para filial não encontrada

        # Escreve de volta ao arquivo JSON
        with open(_FILIAIS_JSON_FILE_PATH, 'w') as file:
            json.dump(filiais, file, indent=4)

        return OPERACAO_REALIZADA_COM_SUCESSO  # Operação bem-sucedida
    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO  # Arquivo não encontrado
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO  # Arquivo em formato inválido
    except Exception as e:
        return ERRO_DESCONHECIDO  # Outro erro desconhecido
        
def get_filial(id: int) -> Tuple[int, Union[Dict[str, str], None]]:
    """
    Consulta uma filial pelo seu ID no arquivo JSON correspondente.

    Args:
        id (int): ID da filial a ser consultada.

    Returns:
        Tuple[int, Union[Dict[str, str], None]]: Tupla contendo um código de erro ou sucesso
        e um dicionário com informações da filial se encontrada, ou None se não encontrada.
    """
    try:
        with open(_FILIAIS_JSON_FILE_PATH, 'r') as file:
            filiais = json.load(file)
        filial = next((f for f in filiais if f['id'] == id), None)
        if filial:
            return OPERACAO_REALIZADA_COM_SUCESSO, {'nome': filial['nome'], 'bairro': filial['bairro']}
        return FILIAL_NAO_ENCONTRADA, None
    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO, None
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO, None
    except Exception as e:
        return ERRO_DESCONHECIDO, None

def get_filiais() -> Tuple[int, List[Dict[str, str]]]:
    """
    Retorna todas as filiais presentes no arquivo JSON.

    Returns:
        Tuple[int, List[Dict[str, str]]]: Tupla contendo um código de erro ou sucesso
        e uma lista de dicionários representando todas as filiais encontradas.
    """
    try:
        with open(_FILIAIS_JSON_FILE_PATH, 'r') as file:
            filiais = json.load(file)
        return OPERACAO_REALIZADA_COM_SUCESSO, [{'nome': f['nome'], 'bairro': f['bairro']} for f in filiais]
    except FileNotFoundError:
        return ARQUIVO_NAO_ENCONTRADO, []
    except json.JSONDecodeError:
        return ARQUIVO_EM_FORMATO_INVALIDO, []
    except Exception as e:
        return ERRO_DESCONHECIDO, []

def get_filial_proxima(bairro: str) -> Tuple[int, Union[int, None]]:
    """
    Retorna o ID da filial mais próxima baseada no bairro informado.

    Args:
        bairro (str): Nome do bairro para buscar a filial mais próxima.

    Returns:
        Tuple[int, Union[int, None]]: Tupla contendo um código de erro ou sucesso
        e o ID da filial mais próxima encontrada, ou None se não encontrada.
    """
    filial_mais_proxima = [
        ("Tijuca", 1),
        ("Ipanema", 2),
        ("Andarai", 1),
        ("Leblon", 2),
        ("Grajau", 1),
        ("Gavea", 2),
        ("Vila Isabel", 1)
    ]
    for bairro_tuple in filial_mais_proxima:
        if bairro_tuple[0] == bairro:
            return OPERACAO_REALIZADA_COM_SUCESSO, bairro_tuple[1]
    else:
        return BAIRRO_NAO_ENCONTRADO, None  
