# Como utilizar

### Clonando

`git clone --recurse-submodules https://github.com/danieltannure/principal`

### Atualizando submódulos

`git submodule update --init --recursive`

`git submodule update --remote --merge`

### Executando

Seu **diretório** no terminal deve ser **um acima do principal**:

`cd (pasta parente do principal)/`

`python -m principal.principal`

### Adicionando um submódulo

`git submodule add (link do repo)`

### Importando um submódulo no principal

```Python
from . import módulo

módulo.func()
```

# Fluxo de telas

![Diagrama do Projeto](Diagrama.png)
