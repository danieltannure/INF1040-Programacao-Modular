# Como utilizar

### Clonando

`git clone --recurse-submodules https://github.com/danieltannure/principal`

### Atualizando submódulos

`git submodule update --init --recursive`

`git submodule update --remote --merge`

### Executando

`cd (...)/principal`

`python -m principal`

### Adicionando um submódulo

`git submodule add (link do repo)`

### Importando um submódulo no principal

```Python
from . import módulo

módulo.func()
```

# Fluxo de telas

![Diagrama do Projeto](Diagrama.png)
