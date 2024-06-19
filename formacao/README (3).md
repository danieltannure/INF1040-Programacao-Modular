# Como utilizar

No diretório imediatamente acima do seu módulo, execute:

`git clone https://github.com/Danielbano1/formacao`

Depois você pode utilizar as funções de formacao com o import:

```Python
from .. import formacao

formacao.get_formacao(25)
```

**OBS:** Para utilizar imports relativos, seu módulo também precisa fazer parte de um package, ou seja, o diretório do módulo deve possuir um arquivo `__init__.py` assim como o nosso.

Alternativamente, se o diretório acima do seu módulo também for um repositório, como o principal, você pode adicionar formacao como submódulo:

`git submodule add https://github.com/Danielbano1/formacao`

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

## get_formacao

Esta função recebe um valor de inteiro em seu parâmetro e busca na base de dados do módulo um formacao cujo "id" corresponda ao valor. Esta função retorna uma tupla com uma mensagem de erro seguida de um dicionário com as informações da formacao buscado na base de dados caso encontrado ou seguida de None caso contrário.

### Requisitos

- Retorna uma tupla com a mensagem FORMACAO_NAO_ENCONTRADO e None, em seqência, caso não encontre um formacao cujo "id" corresponda ao valor em parametro
- Retorna uma tupla com a mensagem FORMACAO_NAO_ATIVO e um dicionário com as informações da base de dados referentes aa formacao cuja "id" corresponda ao valor em parâmetro, caso tal formacao seja encontrado e esteja listado como um formacao desativado
- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e um dicionário com as informações da base de dados referentes aa formacao cuja "id" corresponda ao valor em parâmetro, caso tal formacao seja encontrado e não esteja listado como um formacao desativado

### Acoplamento

- id: int
  Variável a ser buscada na base de dados como "id" da formacao

## get_formacoes

Esta função retorna uma tupla com uma mensagem de erro seguida de uma lista de dicionários com todas as informações de todos as formacoes ativas no banco de dados do módulo.

### Requisitos

- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e uma lista de dicionários com todas as informações de todos as formacoes registradas na base de dados como formacoes ativas

## add_formacao

Esta função recebe em seus parâmetros um nome e uma lista de ids de cursos, em sequência. Esta função busca na base de dados do módulo se existe já um formacao com o nome solicitado. Caso encontre retorna uma tupla com uma mensagem de erro seguida por None, caso contrário é gerado um novo "id" para formacao e um nova formacao é registrado com tal "id" e com as informações fornecidas nos parâmetros na base de dados do módulo, retornando uma tupla com uma mensagem de erro seguida pelo id do nova formacao.

### Requisitos

- Retorna uma tupla com a mensagem FORMACAO_JA_EXISTE e None, em sequência, caso encontre um formacao registrado no banco de dados do módulo com "nome" como o informado no primeiro valor dos parâmetros
- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e um inteiro correspondente do "id" gerado para o nova formacao registrado
- Não é realizada nenhuma avaliação dos cursos informados nos parâmetros e seus possíveis efeitos no uso da aplicação

### Acoplamento

- nome: str
  Nome para a nova formacao. É único para as formacoes e é usado na busca por repetição nesta função
- cursos: list[int]
  Lista com inteiros que correspondem aos "id"s dos cursos componentes desta formacao

## del_formacao

Esta função recebe como parâmetro um inteiro e busca, então, na base de dados um formacao ativo com um "id" correspondente. Caso encontre a formacao é registrado como inativo. Retorna uma mensagem de erro o inteiro fornecido nos parâmetros.

### Requisitos

- Retorna uma tupla com a mensagem FORMACAO_NAO_ENCONTRADO e o "id" fornecido nos parâmetros caso não haja um formacao com o "id" informado registrado na base de dados do módulo
- Retorna uma tupla com a mensagem FORMACAO_NAO_ATIVO e o "id" fornecido nos parâmetros caso haja um formacao com o "id" informado registrado na base de dados do módulo como inativo
- Retorna uma tupla com a mensagem OPERACAO_REALIZADA_COM_SUCESSO e o "id" fornecido nos parâmetros caso haja um formacao com o "id" informado registrado na base de dados do módulo como ativo

### Acoplamento

- id: int
  "id" da formacao a ser desativado




