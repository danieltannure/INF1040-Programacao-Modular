# Gerenciamento de Cursos

Este módulo em Python gerencia uma lista de cursos, permitindo adicionar, deletar e consultar cursos. Os dados são persistidos em um arquivo JSON.

## Funcionalidades

O módulo expõe as seguintes funções:

- `inicializar()`
- `finalizar()`
- `get_curso(id)`
- `get_cursos()`
- `add_curso(nome, carga_horaria, prereqs, duracao_semanas)`
- `del_curso(id)`

## Variáveis Globais

- `lista_cursos`: Lista de cursos ativos.
- `cursos_deletados`: Lista de cursos deletados.
- `PATH`: Caminho do arquivo JSON onde os dados são armazenados.

## Códigos de Erro

- `OPERACAO_REALIZADA_COM_SUCESSO = 0`
- `ARQUIVO_NAO_ENCONTRADO = 30`
- `ARQUIVO_EM_FORMATO_INVALIDO = 31`
- `ERRO_NA_ESCRITA_DO_ARQUIVO = 32`
- `CURSO_NAO_ENCONTRADO = 5`
- `CURSO_JA_EXISTE = 38`
- `CURSO_NAO_ATIVO = 39`

## Funções

### `inicializar() -> int`

Carrega os dados do arquivo JSON para as variáveis globais `lista_cursos` e `cursos_deletados`.

**Retorna:**
- `OPERACAO_REALIZADA_COM_SUCESSO` (0) se a operação foi bem-sucedida.
- `ARQUIVO_NAO_ENCONTRADO` (30) se o arquivo não foi encontrado.
- `ARQUIVO_EM_FORMATO_INVALIDO` (31) se o arquivo JSON está em formato inválido.

### `finalizar() -> int`

Salva os dados das variáveis globais `lista_cursos` e `cursos_deletados` no arquivo JSON.

**Retorna:**
- `OPERACAO_REALIZADA_COM_SUCESSO` (0) se a operação foi bem-sucedida.
- `ERRO_NA_ESCRITA_DO_ARQUIVO` (32) se houve erro na escrita do arquivo.

### `get_curso(id: int) -> tuple[int, dict]`

Recupera um curso pelo seu ID.

**Parâmetros:**
- `id`: Identificador do curso.

**Retorna:**
- Tupla contendo o código de erro e o curso (ou `None` se não encontrado).

### `get_cursos() -> tuple[int, list[dict]]`

Recupera todos os cursos ativos.

**Retorna:**
- Tupla contendo o código de erro e a lista de cursos ativos.

### `add_curso(nome: str, carga_horaria: int, prereqs: list[int], duracao_semanas: int) -> tuple[int, int]`

Adiciona um novo curso.

**Parâmetros:**
- `nome`: Nome do curso.
- `carga_horaria`: Carga horária do curso.
- `prereqs`: Lista de IDs de cursos pré-requisitos.
- `duracao_semanas`: Duração do curso em semanas.

**Retorna:**
- Tupla contendo o código de erro e o ID do novo curso.

### `del_curso(id: int) -> tuple[int, int]`

Deleta um curso pelo seu ID.

**Parâmetros:**
- `id`: Identificador do curso.

**Retorna:**
- Tupla contendo o código de erro e o ID do curso deletado.

## Funções Internas

### `exibe_curso(id)`

Exibe detalhes de um curso pelo ID.

### `exibe_cursos() -> int`

Exibe todos os cursos ativos.

## Inicialização e Finalização Automática

O programa carrega os dados ao iniciar e salva os dados ao finalizar utilizando `atexit.register(finalizar)`.

## Exemplo de Uso

```python
# Inicializar o sistema
erro = inicializar()
if erro != OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Erro na inicialização: {erro}")

# Adicionar um curso
erro, id_curso = add_curso("Curso de Python", 40, [], 4)
if erro == OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Curso adicionado com ID: {id_curso}")

# Exibir cursos ativos
exibe_cursos()

# Deletar um curso
erro, id_curso = del_curso(id_curso)
if erro == OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Curso com ID {id_curso} deletado")


Estrutura do JSON
O arquivo JSON (curso.json) deve ter a seguinte estrutura:
{
    "lista_cursos": [
        {
            "id": 1,
            "nome": "Curso Exemplo",
            "carga_horaria": 40,
            "prereqs": [],
            "duracao_semanas": 4
        }
    ],
    "cursos_deletados": []
}
