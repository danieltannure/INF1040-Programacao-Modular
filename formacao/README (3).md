# Gerenciamento de Formações

Este módulo em Python gerencia uma lista de formações, permitindo adicionar, deletar e consultar formações. Os dados são persistidos em um arquivo JSON.

## Funcionalidades

O módulo expõe as seguintes funções:

- `inicializar()`
- `finalizar()`
- `get_formacao(id)`
- `get_formacoes()`
- `add_formacao(nome, cursos)`
- `del_formacao(id)`

## Variáveis Globais

- `lista_formacoes`: Lista de formações ativas.
- `formacoes_deletadas`: Lista de formações deletadas.
- `PATH`: Caminho do arquivo JSON onde os dados são armazenados.

## Códigos de Erro

- `OPERACAO_REALIZADA_COM_SUCESSO = 0`
- `ARQUIVO_NAO_ENCONTRADO = 30`
- `ARQUIVO_EM_FORMATO_INVALIDO = 31`
- `ERRO_NA_ESCRITA_DO_ARQUIVO = 32`
- `FORMACAO_NAO_ENCONTRADO = 40`
- `FORMACAO_JA_EXISTE = 41`
- `FORMACAO_NAO_ATIVO = 42`

## Funções

### `inicializar() -> int`

Carrega os dados do arquivo JSON para as variáveis globais `lista_formacoes` e `formacoes_deletadas`.

**Retorna:**
- `OPERACAO_REALIZADA_COM_SUCESSO` (0) se a operação foi bem-sucedida.
- `ARQUIVO_NAO_ENCONTRADO` (30) se o arquivo não foi encontrado.
- `ARQUIVO_EM_FORMATO_INVALIDO` (31) se o arquivo JSON está em formato inválido.

### `finalizar() -> int`

Salva os dados das variáveis globais `lista_formacoes` e `formacoes_deletadas` no arquivo JSON.

**Retorna:**
- `OPERACAO_REALIZADA_COM_SUCESSO` (0) se a operação foi bem-sucedida.
- `ERRO_NA_ESCRITA_DO_ARQUIVO` (32) se houve erro na escrita do arquivo.

### `get_formacao(id: int) -> tuple[int, dict]`

Recupera uma formação pelo seu ID.

**Parâmetros:**
- `id`: Identificador da formação.

**Retorna:**
- Tupla contendo o código de erro e a formação (ou `None` se não encontrada).

### `get_formacoes() -> tuple[int, list[dict]]`

Recupera todas as formações ativas.

**Retorna:**
- Tupla contendo o código de erro e a lista de formações ativas.

### `add_formacao(nome: str, cursos: list[int]) -> tuple[int, int]`

Adiciona uma nova formação.

**Parâmetros:**
- `nome`: Nome da formação.
- `cursos`: Lista de IDs de cursos associados.

**Retorna:**
- Tupla contendo o código de erro e o ID da nova formação.

### `del_formacao(id: int) -> tuple[int, int]`

Deleta uma formação pelo seu ID.

**Parâmetros:**
- `id`: Identificador da formação.

**Retorna:**
- Tupla contendo o código de erro e o ID da formação deletada.

## Funções Internas

### `exibe_formacao(id)`

Exibe detalhes de uma formação pelo ID.

### `exibe_formacoes() -> int`

Exibe todas as formações ativas.

## Inicialização e Finalização Automática

O programa carrega os dados ao iniciar e salva os dados ao finalizar utilizando `atexit.register(finalizar)`.

## Exemplo de Uso

```python
# Inicializar o sistema
erro = inicializar()
if erro != OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Erro na inicialização: {erro}")

# Adicionar uma formação
erro, id_formacao = add_formacao("Formação Python", [1, 2, 3])
if erro == OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Formação adicionada com ID: {id_formacao}")

# Exibir formações ativas
exibe_formacoes()

# Deletar uma formação
erro, id_formacao = del_formacao(id_formacao)
if erro == OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Formação com ID {id_formacao} deletada")


Estrutura do JSON
O arquivo JSON (formacao.json) deve ter a seguinte estrutura:
{
    "lista_formacoes": [
        {
            "id": 1,
            "nome": "Formação Exemplo",
            "cursos": [1, 2, 3]
        }
    ],
    "formacoes_deletadas": []
}
