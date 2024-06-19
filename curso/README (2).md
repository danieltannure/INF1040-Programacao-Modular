# Como utilizar

No diretório imediatamente acima do seu módulo, execute:

`git clone https://github.com/Danielbano1/curso`

Depois você pode utilizar as funções de curso com o import:

```Python
from .. import curso

curso.get_curso(25)
```

**OBS:** Para utilizar imports relativos, seu módulo também precisa fazer parte de um package, ou seja, o diretório do módulo deve possuir um arquivo `__init__.py` assim como o nosso.

Alternativamente, se o diretório acima do seu módulo também for um repositório, como o principal, você pode adicionar curso como submódulo:

`git submodule add https://github.com/Danielbano1/curso`

## Dependências

Python 3.9+

# Documentação adicional

O módulo possui um endereço de um arquivo fixo para registro da base de dados em memória persistente, inacessivel ao cliente.
O módulo usa um espaço em memória de acesso rápido para guardar o banco de dados para o uso das funcionalidades do módulo. Esta posição de memória também é inacessível ao cliente.

## inicializar

Esta função realiza a leitura da base de dados na memória persistente para um espaço de acesso rápido a ser usado pelas outras funções. A memória de acesso rápido acessada é fixa e qualquer informação previamente armazenada será perdida.

### Requisitos

- Retorna ARQUIVO_NAO_ENCONTRADO caso não encontre o arquivo de leitura
- Retorna ARQUIVO_EM_FORMATO_INVALIDO caso encontre o arquivo de leitura, mas não seja capaz de fazer a leitura
- Retorna OPERACAO_REALIZADA_COM_SUCESSO caso faça a leitura com sucesso
- Não avalia a integridade do conteudo lido e sua compatibilidade com as aplicações que o usarão

## finalizar

Esta função realiza o registro da base de dados em memória de acesso rápido sendo usada pelo módulo no arquivo resignado pelo módulo. Qualquer conteudo prévio no arquivo será sobrescrito.

### Requisitos

- Retorna ERRO_NA_ESCRITA_DO_ARQUIVO caso não seja capaz de fazer a escrita
- Retorna OPERACAO_REALIZADA_COM_SUCESSO caso faça a escrita com sucesso

## get_curso

Esta função recebe um valor de inteiro em seu parâmetro e busca na base de dados do módulo um curso cujo "id" corresponda ao valor. Esta função retorna uma tupla com uma mensagem de erro seguida de um dicionário com as informações do curso buscado na base de dados caso encontrado ou seguida de None caso contrário.

### Requisitos

- Retorna uma tupla com a mensagem CURSO_NAO_ENCONTRADO e None, em seqência, caso não encontre um curso cujo "id" corresponda ao valor em parametro
- Retorna uma tupla com a mensagem CURSO_NAO_ATIVO e um dicionário com as informações da base de dados referentes ao curso cuja "id" corresponda ao valor em parâmetro, caso tal curso seja encontrado e esteja listado como um curso desativado
- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e um dicionário com as informações da base de dados referentes ao curso cuja "id" corresponda ao valor em parâmetro, caso tal curso seja encontrado e não esteja listado como um curso desativado

### Acoplamento

- id: int
  Variável a ser buscada na base de dados como "id" do curso

## get_cursos

Esta função retorna uma tupla com uma mensagem de erro seguida de uma lista de dicionários com todas as informações de todos os cursos ativos no banco de dados do módulo.

### Requisitos

- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e uma lista de dicionários com todas as informações de todos os cursos registrados na base de dados como cursos ativos

## add_curso

Esta função recebe em seus parâmetros um nome, uma carga horaria, uma lista dos ids dos prerequisitos e uma duração em semanas, em sequência. Esta função busca na base de dados do módulo se existe já um curso com o nome solicitado. Caso encontre retorna uma tupla com uma mensagem de erro seguida por None, caso contrário é gerado um novo "id" para curso e um novo curso é registrado com tal "id" e com as informações fornecidas nos parâmetros na base de dados do módulo, retornando uma tupla com uma mensagem de erro seguida pelo id do novo curso.

### Requisitos

- Retorna uma tupla com a mensagem CURSO_JA_EXISTE e None, em sequência, caso encontre um curso registrado no banco de dados do módulo com "nome" como o informado no primeiro valor dos parâmetros
- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e um inteiro correspondente do "id" gerado para o novo curso registrado
- Não é realizada nenhuma avaliação dos prerequisitos informados nos parâmetros e seus possíveis efeitos no uso da aplicação

### Acoplamento

- nome: str
  Nome do novo curso. É único para os cursos e é usado na busca por repetição nesta função
- carga_horaria: int
  Inteiro correspondente às horas semanais do curso
- prereqs: list[int]
  Lista com inteiros que correspondem aos "id"s dos cursos que são prerequisitos para este curso
- duracao_semanas: int
  Inteiro correspondente à duração do curso em semanas

### Condições de acoplamento

- "carga_horaria" não deve exceder 168

## del_curso

Esta função recebe como parâmetro um inteiro e busca, então, na base de dados um curso ativo com um "id" correspondente. Caso encontre o curso é registrado como inativo. Retorna uma mensagem de erro o inteiro fornecido nos parâmetros.

### Requisitos

- Retorna uma tupla com a mensagem CURSO_NAO_ENCONTRADO e o "id" fornecido nos parâmetros caso não haja um curso com o "id" informado registrado na base de dados do módulo
- Retorna uma tupla com a mensagem CURSO_NAO_ATIVO e o "id" fornecido nos parâmetros caso haja um curso com o "id" informado registrado na base de dados do módulo como inativo
- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e o "id" fornecido nos parâmetros caso haja um curso com o "id" informado registrado na base de dados do módulo como ativo

### Acoplamento

- id: int
  "id" do curso a ser desativado





