# Gerenciamento de Formaturas

Este módulo em Python gerencia as formaturas de alunos em formações específicas, permitindo adicionar, notificar conclusão de cursos, e consultar formaturas. Os dados são persistidos em um arquivo JSON.

## Funcionalidades

O módulo expõe as seguintes funções:

- `inicializar()`
- `finalizar()`
- `add_formatura(id_aluno, id_formacao)`
- `notify_curso_concluido(id_aluno, id_curso)`
- `get_formaturas_by_aluno(id_aluno)`
- `get_formaturas()`
- `get_alunos_by_formatura(id_formacao)`
- `is_concluida(id_aluno, id_formacao)`

## Variáveis Globais

- `lista_formatura`: Lista de formaturas ativas.
- `formaturas_deletadas`: Lista de formaturas deletadas.
- `PATH`: Caminho do arquivo JSON onde os dados são armazenados.

## Códigos de Erro

- `OPERACAO_REALIZADA_COM_SUCESSO = 0`
- `ALUNO_NAO_ENCONTRADO = 16`
- `ARQUIVO_NAO_ENCONTRADO = 30`
- `ARQUIVO_EM_FORMATO_INVALIDO = 31`
- `ERRO_NA_ESCRITA_DO_ARQUIVO = 32`
- `FORMATURA_NAO_ENCONTRADA = 40`
- `FORMATURA_JA_EXISTE = 41`
- `FORMATURA_NAO_ATIVA = 42`
- `CURSO_NAO_CONCLUIDO = 51`

## Funções

### `inicializar() -> int`

Carrega os dados do arquivo JSON para a variável global `lista_formaturas`.

**Retorna:**
- `OPERACAO_REALIZADA_COM_SUCESSO` (0) se a operação foi bem-sucedida.
- `ARQUIVO_NAO_ENCONTRADO` (30) se o arquivo não foi encontrado.
- `ARQUIVO_EM_FORMATO_INVALIDO` (31) se o arquivo JSON está em formato inválido.

### `finalizar() -> int`

Salva os dados da variável global `lista_formaturas` no arquivo JSON.

**Retorna:**
- `OPERACAO_REALIZADA_COM_SUCESSO` (0) se a operação foi bem-sucedida.
- `ERRO_NA_ESCRITA_DO_ARQUIVO` (32) se houve erro na escrita do arquivo.

### `add_formatura(id_aluno: int, id_formacao: int) -> tuple[int, dict]`

Adiciona uma nova formatura para um aluno em uma formação específica.

**Parâmetros:**
- `id_aluno`: Identificador do aluno.
- `id_formacao`: Identificador da formação.

**Retorna:**
- Tupla contendo o código de erro e a formatura adicionada.

### `notify_curso_concluido(id_aluno: int, id_curso: int) -> int`

Notifica que um curso foi concluído por um aluno.

**Parâmetros:**
- `id_aluno`: Identificador do aluno.
- `id_curso`: Identificador do curso.

**Retorna:**
- Código de erro.

### `get_formaturas_by_aluno(id_aluno: int) -> tuple[int, list[dict]]`

Retorna uma lista com as formaturas associadas a um aluno.

**Parâmetros:**
- `id_aluno`: Identificador do aluno.

**Retorna:**
- Tupla contendo o código de erro e a lista de formaturas do aluno.

### `get_formaturas() -> tuple[int, list[dict]]`

Retorna uma lista de todas as formaturas.

**Retorna:**
- Tupla contendo o código de erro e a lista de formaturas.

### `get_alunos_by_formatura(id_formacao: int) -> tuple[int, list[int]]`

Retorna uma lista com os IDs de alunos associados a uma formação específica.

**Parâmetros:**
- `id_formacao`: Identificador da formação.

**Retorna:**
- Tupla contendo o código de erro e a lista de alunos.

### `is_concluida(id_aluno: int, id_formacao: int) -> tuple[int, bool]`

Verifica se um aluno concluiu uma formação específica.

**Parâmetros:**
- `id_aluno`: Identificador do aluno.
- `id_formacao`: Identificador da formação.

**Retorna:**
- Tupla contendo o código de erro e um booleano indicando se a formação foi concluída.

## Funções Internas

### `exibe_formaturas()`

Exibe todas as formaturas ativas.

## Inicialização e Finalização Automática

O programa carrega os dados ao iniciar e salva os dados ao finalizar utilizando `atexit.register(finalizar)`.

## Exemplo de Uso

```python
# Inicializar o sistema
erro = inicializar()
if erro != OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Erro na inicialização: {erro}")

# Adicionar uma formatura
erro, formatura = add_formatura(1, 101)
if erro == OPERACAO_REALIZADA_COM_SUCESSO:
    print(f"Formatura adicionada: {formatura}")

# Notificar curso concluído
erro = notify_curso_concluido(1, 201)
if erro == OPERACAO_REALIZADA_COM_SUCESSO:
    print("Curso concluído notificado")

# Exibir formaturas ativas
exibe_formaturas()

# Verificar se formação foi concluída
erro, concluida = is_concluida(1, 101)
if erro == OPERACAO_REALIZADA_COM_SUCESSO and concluida:
    print("Formação concluída")
elif erro == OPERACAO_REALIZADA_COM_SUCESSO:
    print("Formação não concluída")

Estrutura do JSON
O arquivo JSON (formacao-aluno.json) deve ter a seguinte estrutura:
[
    {
        "id_aluno": 1,
        "id_formacao": 101,
        "cursos_concluidos": [201, 202]
    }
]
