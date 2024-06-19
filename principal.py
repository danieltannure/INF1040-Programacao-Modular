# bibliotecas
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

# biblioteca para montar cálculos de tempo de curso
from datetime import datetime, timedelta

# bibliotecas para montar o calendário
from tkinter import ttk
import calendar
import os
import json

# Módulos
# Apenas o mensagens fica nesse formato, pra não precisar do prefixo mensagens. nos erros
# Para o resto, use: from . import modulo
from .mensagens import *
from . import cadastro
from . import filial
from . import filialturma
from . import avaliacao
from . import criterio
from . import respostas

# Variáveis globais de registro da sessão
# Globais Aluno
aluno_da_sessao = ""
# Globais Professor
professor_da_sessao = ""
lista_perguntas_montagem = []
lista_gabarito_montagem = []
# Globais Admin
lista_cursos_formacao = []
lista_cursos_prequisito = []
lista_cursos_aptos = []
lista_filiais_aptas = []
# Globais de data
ano_atual = datetime.now().year
mes_atual = datetime.now().month
# Globais p/Calendário
label_mes_ano = None
combobox_filial = None
frame_calendario = None
turmas_do_mes = []


# Tela Inicial
def show_tela_login():
    for widget in root.winfo_children():
        widget.destroy()

    # desloga qualquer usuário que retornar para o login
    global aluno_da_sessao
    aluno_da_sessao = None
    global professor_da_sessao
    professor_da_sessao = None

    label_usuario = tk.Label(root, text="Usuário:")
    label_usuario.grid(row=0, column=0, padx=10, pady=10)

    entrada_usuario = tk.Entry(root)
    entrada_usuario.grid(row=0, column=1, padx=10, pady=10)

    label_senha = tk.Label(root, text="Senha:")
    label_senha.grid(row=1, column=0, padx=10, pady=10)

    entrada_senha = tk.Entry(root, show="*")
    entrada_senha.grid(row=1, column=1, padx=10, pady=10)

    botao_cadastro = tk.Button(root, text="Cadastrar", command=show_tela_cadastro)
    botao_cadastro.grid(row=2, column=0, columnspan=1, pady=10)

    botao_login = tk.Button(
        root,
        text="Login",
        command=lambda: get_credenciais(entrada_usuario.get(), entrada_senha.get()),
    )
    botao_login.grid(row=2, column=1, columnspan=1, pady=10)


# Tela de Cadastro
def show_tela_cadastro():

    for widget in root.winfo_children():
        widget.destroy()

    label_usuario = tk.Label(root, text="Novo Usuário:")
    label_usuario.grid(row=0, column=0, padx=10, pady=10)

    entrada_novo_usuario = tk.Entry(root, width=55)
    entrada_novo_usuario.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

    label_nova_senha = tk.Label(root, text="Nova Senha:")
    label_nova_senha.grid(row=1, column=0, padx=10, pady=10)

    entrada_nova_senha = tk.Entry(root, width=55, show="*")
    entrada_nova_senha.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

    # os bairros vão ter que se puxado de algum database do módulo filial

    caminho_bairros = os.path.join(
        os.path.dirname(__file__), "filial/data", "bairros.json"
    )

    with open(caminho_bairros, "r", encoding="utf-8") as f:
        data = json.load(f)
        bairros = ["(Selecione o Bairro)"] + data.get("bairros", [])

    bairros = [
        "(Selecione o Bairro)",
        "Centro",
        "Bela Vista",
        "Jardim Europa",
        "Vila Madalena",
        "Moema",
    ]
    bairro_var = tk.StringVar(root)
    bairro_var.set(bairros[0])  # Definir valor padrão como vazio

    label_bairro = tk.Label(root, text="Bairro:")
    label_bairro.grid(row=2, column=0, padx=10, pady=10)

    menu_bairros = tk.OptionMenu(root, bairro_var, *bairros)
    menu_bairros.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

    label_disponibilidade = tk.Label(root, text="Disponibilidade:  Das")
    label_disponibilidade.grid(row=3, column=0, padx=10, pady=10)

    entrada_horario_inicio = tk.Entry(root)
    entrada_horario_inicio.grid(row=3, column=1, padx=10, pady=10)

    label_fim = tk.Label(root, text="às")
    label_fim.grid(row=3, column=2, padx=10, pady=10)

    entrada_horario_fim = tk.Entry(root)
    entrada_horario_fim.grid(row=3, column=3, padx=10, pady=10)

    botao_criar_conta = tk.Button(
        root,
        text="Criar Conta",
        command=lambda: send_add_conta(
            entrada_novo_usuario.get(),
            entrada_nova_senha.get(),
            bairro_var.get(),
            entrada_horario_inicio.get(),
            entrada_horario_fim.get(),
        ),
    )
    botao_criar_conta.grid(row=4, column=1, columnspan=1, pady=10)

    botao_voltar_login = tk.Button(
        root, text="Voltar ao Login", command=show_tela_login
    )
    botao_voltar_login.grid(row=4, column=0, columnspan=1, pady=10)


def send_add_conta(usuario, senha, bairro, ini, fim):
    if bairro == "(Selecione o Bairro)":
        messagebox.showerror("Bairro Inválido", "Selecione um Bairro")
        show_tela_cadastro()
    else:
        # testa se ini é convertivel pra int
        try:
            valor_ini = int(ini)
            # testa se fim é convertivel pra int
            try:
                valor_fim = int(fim)
                if valor_ini < valor_fim:
                    # aqui deve ter do modulo aluno um add_aluno que pega bairro,ini,fim e cria um aluno e retorna uma id única
                    id_usuario = 1
                    erro = cadastro.add_cadastro(usuario, senha, id_usuario, "aluno")
                    if erro[0] != 0:
                        messagebox.showerror("Erro", f"{get_msg_status(erro[0])}")
                        show_tela_cadastro()
                    else:
                        messagebox.showinfo(
                            "Cadastro Concluido", "Sua conta foi criada."
                        )
                        show_tela_login()
                else:
                    messagebox.showerror(
                        "Intervalo Inválido",
                        "Insira o intervalo de disponibilidade corretamente",
                    )
                    show_tela_cadastro()
            except ValueError:
                messagebox.showerror(
                    "Numero Inválido", "Insira um número para o fim corretamente."
                )
                show_tela_cadastro()
        except ValueError:
            messagebox.showerror(
                "Numero Inválido", "Insira um número para o início corretamente."
            )
            show_tela_cadastro()


def get_credenciais(usuario, senha):
    # pega o id do usuário que está entrando numa sessão
    erro, id_usuario = cadastro.login(usuario, senha)
    if erro != 0:
        messagebox.showerror("Erro", f"{get_msg_status(erro)}")
        show_tela_login()
    else:

        # checa se ele é admin
        erro, check_admin = cadastro.is_admin(usuario)
        if erro != 0:
            messagebox.showerror("Erro", f"{get_msg_status(erro)}")
            show_tela_login()
        elif check_admin:
            show_tela_principal_admin()

        # checa se ele é aluno
        erro, check_aluno = cadastro.is_aluno(usuario)
        if erro != 0:
            messagebox.showerror("Erro", f"{get_msg_status(erro)}")
            show_tela_login()
        elif check_aluno:
            show_tela_principal_aluno()
            # guarda o id_aluno que está sendo usado
            global aluno_da_sessao
            aluno_da_sessao = id_usuario

        # checa se ele é professor
        erro, check_professor = cadastro.is_professor(usuario)
        if erro != 0:
            messagebox.showerror("Erro", f"{get_msg_status(erro)}")
            show_tela_login()
        elif check_professor:
            show_tela_principal_professor()
            # guarda o id_professor que está sendo usado
            global professor_da_sessao
            professor_da_sessao = id_usuario


# Sessão: Admin
def show_tela_principal_admin():
    for widget in root.winfo_children():
        widget.destroy()

    label_bem_vindo_admin = tk.Label(root, text="Sessão: Admin")
    label_bem_vindo_admin.grid(row=0, column=0, padx=10, pady=10)

    botao_formacoes = tk.Button(
        root, height=5, text="Gerir Formações", command=show_tela_formacoes_admin
    )
    botao_formacoes.grid(row=1, rowspan=2, column=0, padx=10, pady=10)

    botao_filiais = tk.Button(
        root, height=5, text="Gerir Filiais", command=show_tela_filiais_admin
    )
    botao_filiais.grid(row=1, rowspan=2, column=1, padx=10, pady=10)

    botao_formacao = tk.Button(
        root, height=5, text="Gerir Cursos", command=show_tela_cursos_admin
    )
    botao_formacao.grid(row=1, rowspan=2, column=2, padx=10, pady=10)

    botao_criterio = tk.Button(
        root, height=5, text="Gerir Critérios", command=show_tela_criterio_admin
    )
    botao_criterio.grid(row=1, rowspan=2, column=3, padx=10, pady=10)

    botao_cadastros = tk.Button(
        root, height=5, text="Gerir Cadastros", command=show_tela_cadastro_admin
    )
    botao_cadastros.grid(row=1, rowspan=2, column=4, padx=10, pady=10)

    botao_levantamentos = tk.Button(
        root,
        height=5,
        text="Mostrar Levantamentos",
        command=show_tela_levantamentos_admin,
    )
    botao_levantamentos.grid(row=1, rowspan=2, column=5, padx=10, pady=10)

    botao_logout = tk.Button(root, text="Logout", command=show_tela_login)
    # WARNING: na aplicação final não deve-se retornar para a tela login, e sim para uma função que feche o sistema e salve tudo
    botao_logout.grid(row=3, column=0, padx=10, pady=10)


def show_tela_cursos_admin():
    for widget in root.winfo_children():
        widget.destroy()

    label_curso = tk.Label(root, text="Gestão Cursos")
    label_curso.grid(row=0, column=0, padx=10, pady=10)

    label_criar_curso = tk.Label(root, text="Criar Curso:")
    label_criar_curso.grid(row=1, column=0, padx=10, pady=10)

    botao_criar = tk.Button(root, text="Criar", command=show_tela_cria_curso)
    botao_criar.grid(row=1, column=1, padx=10, pady=10)

    # os cursos devem ser puxadas pelo módulo curso via curso.get_cursos()
    cursos = [
        "(Selecione o Curso)",
        "Psicologia",
        "Programação",
        "Física",
        "Medicina",
        "História",
    ]
    cursos_var = tk.StringVar(root)
    cursos_var.set(cursos[0])  # Definir valor padrão como vazio

    label_cursos = tk.Label(root, text="Apagar Curso:")
    label_cursos.grid(row=2, column=0, padx=10, pady=10)

    menu_cursos = tk.OptionMenu(root, cursos_var, *cursos)
    menu_cursos.grid(row=2, column=1, padx=10, pady=10)

    botao_turmas = tk.Button(
        root, text="Deletar", command=lambda: send_del_curso(cursos_var.get())
    )
    botao_turmas.grid(row=3, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_admin)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_del_curso(id_curso):
    if id_curso == "(Selecione o Curso)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Curso.")
        show_tela_cursos_admin()
    else:
        resultado = messagebox.askyesno("Aviso", "Deseja deletar este Curso?")
        if resultado:
            # aqui deve ser inserido a função do modulo curso del_curso(id_curso)
            # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
            # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

            # AVISO: curso so deve ser apagado do módulo cursos, mesmo continuando existindo no módulo assuntos e criterioaprovacao
            # isso é importante para preservar o monitoramento do histórico mesmo de cursos extintos
            messagebox.showinfo("Deletado", f"O curso {id_curso} foi deletado.")
        else:
            show_tela_cursos_admin()


def show_tela_cria_curso():
    for widget in root.winfo_children():
        widget.destroy()

    label_curso = tk.Label(root, text="Criação Curso")
    label_curso.grid(row=0, column=0, padx=10, pady=10)

    label_nome = tk.Label(root, text="Nome:")
    label_nome.grid(row=1, column=0, padx=10, pady=10)

    entrada_nome = tk.Entry(root)
    entrada_nome.grid(row=1, column=1, padx=10, pady=10)

    label_duracao = tk.Label(root, text="Duração (em Semanas):")
    label_duracao.grid(row=2, column=0, padx=10, pady=10)

    entrada_duracao = tk.Entry(root)
    entrada_duracao.grid(row=2, column=1, padx=10, pady=10)

    label_duracao_aula = tk.Label(root, text="Duração da Aula (em Horas):")
    label_duracao_aula.grid(row=3, column=0, padx=10, pady=10)

    entrada_duracao_aula = tk.Entry(root)
    entrada_duracao_aula.grid(row=3, column=1, padx=10, pady=10)

    global lista_cursos_prequisito
    lista_cursos_prequisito = []

    # os cursos vão ter que se puxado do database do módulo cursos
    cursos = [
        "(Selecione o Curso)",
        "Psicologia",
        "Programação",
        "Física",
        "Medicina",
        "História",
    ]
    cursos_var = tk.StringVar(root)
    cursos_var.set(cursos[0])  # Definir valor padrão como vazio

    label_cursos = tk.Label(root, text="Selecione um Curso:")
    label_cursos.grid(row=4, column=0, padx=10, pady=10)

    menu_cursos = tk.OptionMenu(root, cursos_var, *cursos)
    menu_cursos.grid(row=4, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(
        root,
        text="Adicionar Requisito",
        command=lambda: send_append_requisito(cursos_var.get()),
    )
    botao_voltar.grid(row=5, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_cursos_admin)
    botao_voltar.grid(row=6, column=0, padx=10, pady=10)

    botao_voltar = tk.Button(
        root,
        text="Criar Curso",
        command=lambda: send_add_curso(
            entrada_nome.get(),
            entrada_duracao.get(),
            entrada_duracao_aula.get(),
            lista_cursos_prequisito,
        ),
    )
    botao_voltar.grid(row=6, column=1, padx=10, pady=10)


def send_append_requisito(id_curso):
    if id_curso == "(Selecione o Curso)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou um Curso.")
        show_tela_cria_curso()
    else:
        global lista_cursos_prequisito
        lista_cursos_prequisito.append(id_curso)
        messagebox.showinfo("Concluido", "Requisito Adicionado.")
        show_tela_cria_curso()


def send_add_curso(nome, duracao, cargahoraria, prereqs):
    try:
        semanas = int(duracao)
        cargahoraria = semanas * 2
        try:
            carga = int(cargahoraria)
            # basta usar a função de acesso do módulo Curso
            # erro,id = curso.add_curso(nome,carga,prereqs,semanas)
            # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
            # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
            messagebox.showinfo("Concluido", f"Curso {nome} foi criado.")
            show_tela_cria_curso()
        except ValueError:
            messagebox.showerror(
                "Erro", "Por favor, insira um número inteiro válido nas duracao."
            )
            show_tela_cria_curso()
    except ValueError:
        messagebox.showerror(
            "Erro", "Por favor, insira um número inteiro válido nas duracao."
        )
        show_tela_cria_curso()


def show_tela_criterio_admin():
    for widget in root.winfo_children():
        widget.destroy()

    label_criterio = tk.Label(root, text="Gestão Critério")
    label_criterio.grid(row=0, column=0, padx=10, pady=10)

    # os cursos vão ter que se puxado do database do módulo cursos
    cursos = [
        "(Selecione o Curso)",
        "Psicologia",
        "Programação",
        "Física",
        "Medicina",
        "História",
    ]
    cursos_var = tk.StringVar(root)
    cursos_var.set(cursos[0])  # Definir valor padrão como vazio

    label_cursos = tk.Label(root, text="Selecione um Curso para Critério:")
    label_cursos.grid(row=1, column=0, padx=10, pady=10)

    menu_cursos = tk.OptionMenu(root, cursos_var, *cursos)
    menu_cursos.grid(row=1, column=1, padx=10, pady=10)

    # as avaliacoes devem ser puxadas do módulo avaliação

    erro = avaliacao.get_avaliacoes()

    avaliacoes = ["(Selecione Uma Avaliação)"] + [av["nome"] for av in erro[1]]
    avaliacoes_var = tk.StringVar(root)
    avaliacoes_var.set(avaliacoes[0])  # Definir valo padrão como vazio

    label_avaliacoes = tk.Label(root, text="Selecione uma Avaliacao para Critério:")
    label_avaliacoes.grid(row=2, column=0, padx=10, pady=10)

    menu_avaliacoes = tk.OptionMenu(root, avaliacoes_var, *avaliacoes)
    menu_avaliacoes.grid(row=2, column=1, padx=10, pady=10)

    botao_deletar = tk.Button(
        root,
        text="Adicionar Avaliação ao Critério",
        command=lambda: send_add_avaliacao_ao_criterio(
            cursos_var.get(), avaliacoes_var.get()
        ),
    )
    botao_deletar.grid(row=3, column=1, padx=10, pady=10)

    botao_deletar = tk.Button(
        root,
        text="Adicionar Avaliação Nova ao Critério",
        command=lambda: show_nova_avaliacao_ao_criterio(cursos_var.get()),
    )
    botao_deletar.grid(row=3, column=0, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_admin)
    botao_voltar.grid(row=4, column=0, padx=10, pady=10)


def send_add_avaliacao_ao_criterio(id_curso, id_avaliacao):
    if id_curso == "(Selecione o Curso)":
        messagebox.showinfo("Erro", "Você não selecionou Curso")
        show_tela_criterio_admin()
    elif id_avaliacao == "(Selecione Uma Avaliação)":
        messagebox.showinfo("Erro", "Você não selecionou Avaliação")
    else:
        # Aqui insira a funçao de acesso do módulo criterioaprovacao
        # erro= criterioaprovacao.add_avaliacao_ao_criterio(id_curso,id_avaliacao)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
        messagebox.showinfo(
            "Concluido", f"O critério do curso {id_curso}, foi atualizado."
        )
        show_tela_criterio_admin()


def show_nova_avaliacao_ao_criterio(id_curso):
    if id_curso == "(Selecione o Curso)":
        messagebox.showinfo("Erro", "Você não selecionou Curso")
        show_tela_criterio_admin()
    else:
        for widget in root.winfo_children():
            widget.destroy()

        label_criar_av = tk.Label(root, text="Criar Avaliação")
        label_criar_av.grid(row=0, column=0, padx=10, pady=10)

        label_nome = tk.Label(root, text="Nome:")
        label_nome.grid(row=1, column=0, padx=10, pady=10)

        entrada_nome = tk.Entry(root)
        entrada_nome.grid(row=1, column=1, padx=10, pady=10)

        label_tipo = tk.Label(root, text="Tipo:")
        label_tipo.grid(row=2, column=0, padx=10, pady=10)

        entrada_tipo = tk.Entry(root)
        entrada_tipo.grid(row=2, column=1, padx=10, pady=10)

        botao_criar = tk.Button(
            root,
            text="Criar ",
            command=lambda: send_novo_add_avaliacao_ao_criterio(
                entrada_nome.get(), entrada_tipo.get(), id_curso
            ),
        )
        botao_criar.grid(row=3, column=1, padx=10, pady=10)

        botao_voltar = tk.Button(root, text="Voltar", command=show_tela_criterio_admin)
        botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_novo_add_avaliacao_ao_criterio(nome, tipo, curso):
    try:
        tipo_prova = int(tipo)
        # chama a função de acesso do modulo avaliação add_avaliacao(nome,tipo_prova) #mudar parametros da função avaliação
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
        # pega o id dessa nova avaliação e chama a send_add_avaliacao_ao_criterio(id_curso,id_avaliacao_nova)
        erro = avaliacao.add_avaliacao(nome, tipo, [], [])
        id_avaliacao_nova = erro[1]
        send_add_avaliacao_ao_criterio(curso, id_avaliacao_nova)

        messagebox.showinfo(
            "Avaliação Incluida",
            f"Agora avaliação {nome}, faz parte do critério do curso {curso}.",
        )
    except ValueError:
        messagebox.showerror("Erro", "Você não inseriu o tipo corretamente.")


def show_tela_levantamentos_admin():
    for widget in root.winfo_children():
        widget.destroy()

    label_levantamentos = tk.Label(root, text="Levantamentos")
    label_levantamentos.grid(row=0, column=0, padx=10, pady=10)

    botao_formacoes = tk.Button(
        root, height=5, text="Turmas Lecionando", command=send_turmas_lecionando
    )
    botao_formacoes.grid(row=1, rowspan=2, column=0, padx=10, pady=10)

    botao_filiais = tk.Button(
        root, height=5, text="Equipe de Professores", command=show_equipe_professores
    )
    botao_filiais.grid(row=1, rowspan=2, column=1, padx=10, pady=10)

    botao_formacao = tk.Button(
        root, height=5, text="Média Avaliação", command=show_media_avaliacao
    )
    botao_formacao.grid(row=1, rowspan=2, column=2, padx=10, pady=10)

    botao_criterio = tk.Button(
        root, height=5, text="Turmas por Filiais", command=show_turma_por_filiais
    )
    botao_criterio.grid(row=1, rowspan=2, column=3, padx=10, pady=10)

    botao_criterio = tk.Button(
        root, height=5, text="Formações do Ano", command=lambda: send_formacoes_do_ano
    )
    botao_criterio.grid(row=1, rowspan=2, column=4, padx=10, pady=10)

    botao_criterio = tk.Button(
        root, height=5, text="Calendário", command=show_tela_calendario_admin
    )
    botao_criterio.grid(row=1, rowspan=2, column=5, padx=10, pady=10)

    botao_criterio = tk.Button(
        root, height=5, text="Cursos Ativos", command=send_cursos_ativos
    )
    botao_criterio.grid(row=1, rowspan=2, column=6, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_admin)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_cursos_ativos():
    # aqui deverá ser puxado do modulo cursos o cursos.get_cursos()
    # e roda para cada curso e id curso chega no modulo assunto assunto.get_assuntos() e pega as turmas
    # para cada turma q ta ativa (significa q ta sendo lecionada e existe um professor), crie um contador e incremente ele a cada turma ativa
    # crie uma mensagem do tipo parecida com a abaixo
    messagebox.showinfo("Curso:A\nProfessores:4\n\nCurso:B\nProfessores:5")
    show_tela_levantamentos_admin()


def show_tela_calendario_admin():
    for widget in root.winfo_children():
        widget.destroy()

    # Label para exibir o mês e ano atual
    global label_mes_ano
    label_mes_ano = tk.Label(root, text=f"{calendar.month_name[mes_atual]} {ano_atual}")
    label_mes_ano.grid(row=0, column=1, columnspan=3)

    # Botões para navegação do calendário
    botao_anterior = tk.Button(root, text="<", command=send_mes_anterior)
    botao_anterior.grid(row=0, column=0)

    botao_proximo = tk.Button(root, text=">", command=send_proximo_mes)
    botao_proximo.grid(row=0, column=4)

    # Combobox para selecionar a filial
    global combobox_filial, turmas_do_mes
    turmas_do_mes = send_obter_turmas()
    filiais = list(set(turma["filial"] for turma in turmas_do_mes))

    combobox_filial = ttk.Combobox(root, values=filiais)

    if filiais:
        combobox_filial.current(0)
    combobox_filial.grid(row=0, column=5)
    combobox_filial.bind(
        "<<ComboboxSelected>>", lambda event: send_atualizar_calendario()
    )

    # Frame para o calendário
    global frame_calendario
    frame_calendario = tk.Frame(root)
    frame_calendario.grid(row=1, column=0, columnspan=6, sticky="nsew")

    # Botão para voltar à tela principal
    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_levantamentos_admin)
    botao_voltar.grid(row=2, column=0, columnspan=6, pady=10)

    # Criar o calendário inicial
    send_atualizar_calendario()


def send_mes_anterior():
    global ano_atual, mes_atual
    if mes_atual == 1:
        mes_atual = 12
        ano_atual -= 1
    else:
        mes_atual -= 1
    send_atualizar_calendario()


def send_proximo_mes():
    global ano_atual, mes_atual
    if mes_atual == 12:
        mes_atual = 1
        ano_atual += 1
    else:
        mes_atual += 1
    send_atualizar_calendario()


def send_atualizar_calendario():
    global ano_atual, mes_atual
    filtro_filial = int(combobox_filial.get())
    global turmas_do_mes
    turmas_do_mes = send_obter_turmas()

    # Limpa o frame do calendário
    for widget in frame_calendario.winfo_children():
        widget.destroy()

    # Obter a matriz do calendário
    cal = calendar.monthcalendar(ano_atual, mes_atual)

    # Cabeçalhos dos dias da semana
    dias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    for col, dia in enumerate(dias):
        tk.Label(
            frame_calendario,
            text=dia,
            borderwidth=1,
            relief="solid",
            width=15,
            height=2,
        ).grid(row=0, column=col)

    # Inserir os dias na grade do calendário
    for row, week in enumerate(cal, start=1):
        for col, dia in enumerate(week):
            if dia == 0:
                cell_text = ""
            else:
                data = datetime(ano_atual, mes_atual, dia)
                cell_text = f"{dia}\n"
                for turma in turmas_do_mes:
                    data_fim = turma["data_ini"] + timedelta(
                        weeks=turma["duracao_semanas"]
                    )
                    if (
                        turma["filial"] == filtro_filial
                        and turma["data_ini"] <= data <= data_fim
                    ):
                        if (data - turma["data_ini"]).days % 7 == 0:
                            cell_text += f"Turma {turma['id']}\n"
            cell = tk.Text(
                frame_calendario, width=15, height=8, borderwidth=1, relief="solid"
            )  # Altura ajustada
            cell.insert(tk.END, cell_text.strip())
            cell.config(state=tk.DISABLED)  # Desabilita a edição do texto
            cell.grid(row=row, column=col, sticky="nsew")

    label_mes_ano.config(text=f"{calendar.month_name[mes_atual]} {ano_atual}")


def send_obter_turmas():
    # futuramente aqui você deve puxar do módulo  o dicionário = turma.get_turmas()
    # e ai pega do módulo aulas o dicionario = filialturma.get_aulas()
    # junte os dois dicionários pra ficar igual a do exemplo abaixo:
    return [
        {
            "id": 1,
            "is_online": False,
            "data_ini": datetime(2024, 6, 1),
            "duracao_semanas": 4,
            "horario": {"ini": 9, "fim": 11},
            "filial": 1,
        },
        {
            "id": 2,
            "is_online": True,
            "data_ini": datetime(2024, 6, 5),
            "duracao_semanas": 6,
            "horario": {"ini": 14, "fim": 16},
            "filial": 2,
        },
        {
            "id": 3,
            "is_online": False,
            "data_ini": datetime(2024, 6, 8),
            "duracao_semanas": 3,
            "horario": {"ini": 10, "fim": 12},
            "filial": 1,
        },
        {
            "id": 4,
            "is_online": True,
            "data_ini": datetime(2024, 6, 10),
            "duracao_semanas": 2,
            "horario": {"ini": 15, "fim": 17},
            "filial": 2,
        },
        {
            "id": 5,
            "is_online": False,
            "data_ini": datetime(2024, 6, 12),
            "duracao_semanas": 5,
            "horario": {"ini": 8, "fim": 10},
            "filial": 3,
        },
        {
            "id": 6,
            "is_online": True,
            "data_ini": datetime(2024, 6, 15),
            "duracao_semanas": 7,
            "horario": {"ini": 13, "fim": 15},
            "filial": 1,
        },
        {
            "id": 7,
            "is_online": False,
            "data_ini": datetime(2024, 6, 18),
            "duracao_semanas": 4,
            "horario": {"ini": 11, "fim": 13},
            "filial": 2,
        },
    ]


def send_formacoes_do_ano():
    # aqui chama a função do módulo formatura e guarde numa lista alunos_formandos = formatura.get_formaturas()
    # percorra num for e fazer o seguinte algoritmo para cada aluno nessa lista:
    # puxe a formação que ele está inscrito e puxa os requisitos de formatura no módulo formacao cursos_necessarios= formacao.get_formacao(aluno_formandos[i]["id_formacao"])
    # rode um for nos cursos_necessarios e compare com o atributo cursos concluidos do aluno (alunos_formados[i]["cursos_concluidos"])
    # retire do cursos_necessarios os cursos que se encontram no cursos concluidos
    # depois, procure no módulo assuntos se existem turmas deste tal curso que falta, se não tiver, passe para o proximo aluno de aluno_formandos
    # se tiver, procure em matrícula se esse aluno está matriculado em quaisquer turmas de todos os cursos que tenham turmas ativas que faltam
    # se ele não estiver, passe para o proximo aluno de alunos_formandos, se ele estiver, crie uma label com o nome da formação
    # caso estas turmas , pegando no modulo turma, tenham dado inicio e baseado na duração terminem ainda no ano desejado, eles serão formandos deste tal ano
    # se a turma terminar no ano seguinte, este aluno deve ser descontabilizado para formação
    # se a label já tive sido criada para tal formacao que um aluno está se formando, não crie outra

    # ex:
    # todos os gets necessários (não é pra ser feito nesta ordem):
    dicionario_formaturas = [
        {"id_formatura": 1, "id_aluno": 9, "cursos_concluidos": [3, 4]},
        {"id_formatura": 2, "id_aluno": 4, "cursos_concluidos": [3]},
        {"id_formatura": 1, "id_aluno": 3, "cursos_concluidos": [3, 4]},
    ]
    dicionario_formacao = [
        {"id": 1, "nome": "Fisiculturismo Avançado", "cursos": [3, 4, 5]},
        {"id": 2, "nome": "Fisiculturismo Intermediário", "cursos": [3, 4]},
    ]
    turmas_cursos = [
        {"id_curso": 3, "id_turma": 50},
        {"id_curso": 4, "id_turma": 51},
        {"id_curso": 3, "id_turma": 59},
        {"id_curso": 5, "id_turma": 40},
    ]
    alunos_turmas = [
        {"id_turma": 40, "id_aluno": 3},
        {"id_turma": 51, "id_aluno": 4},
        {"id_turma": 30, "id_aluno": 3},
        {"id_turma": 14, "id_aluno": 9},
    ]
    dicionario_turmas = [
        {
            "id": 40,
            "is_online": False,
            "max_alunos": 10,
            "data_ini": datetime(2024, 6, 14),
            "duracao_semanas": 3,
            "horario": {"ini": 4, "fim": 5},
        },
        {
            "id": 51,
            "is_online": False,
            "max_alunos": 10,
            "data_ini": datetime(2024, 10, 14),
            "duracao_semanas": 10,
            "horario": {"ini": 2, "fim": 6},
        },
        {
            "id": 14,
            "is_online": True,
            "max_alunos": None,
            "data_ini": datetime(2024, 1, 2),
            "duracao_semanas": 30,
            "horario": {"ini": 1, "fim": 2},
        },
        {
            "id": 30,
            "is_online": False,
            "max_alunos": 10,
            "data_ini": datetime(2024, 4, 9),
            "duracao_semanas": 7,
            "horario": {"ini": 3, "fim": 4},
        },
    ]

    # o aluno 9 está cursando a matéria 5 que falta pra ele completar a formação 1 dele então ele é formando na turma 40 e vai terminar antes do fim de 2024
    # o aluno 4 também está cursando a materia 4 que falta para sua formação 2 então ele é formando na turma 51 e vai terminar antes do fim de 2024

    # dica para calculo de se vai terminar depois de 2024
    # data_ini = datetime(2023, 6, 13)
    # duracao_semanas= 10
    # nova_data = data_ini + timedelta(weeks=duracao_semanas)
    # if nova_data.year > 2024 , então não é formando deste ano

    messagebox.showinfo("Possuimos formando de : A , B  e C para 2024.")


def send_turmas_lecionando():
    # chama a função do módulo turma turma.get.turmas();
    # guarda a lista e roda num for e verifica quais delas dão true para turma.isativa(lista[i])
    # para cada uma que der true conte 1
    # retorne esse valor
    messagebox.showinfo(
        "Turmas Lecionando", "Neste momento, possuem-se x turmas lecionando."
    )
    show_tela_levantamentos_admin()


def show_equipe_professores():
    for widget in root.winfo_children():
        widget.destroy()

    label_equipe = tk.Label(root, text=f"Nossa Equipe")
    label_equipe.grid(row=0, column=0, padx=10, pady=10)
    # chama a função do módulo professor professor.get_professores()
    # rode um for e monte uma label para cada professor da lista mostrando seu nome e cursos q leciona

    professores = [
        {
            "id": 1,
            "nome": "A",
            "cursos": [1, 2],
            "filiais": [4, 2],
            "horarios": {"ini": 5, "fim": 8},
        },
        {
            "id": 2,
            "nome": "B",
            "cursos": [5, 2],
            "filiais": [9, 2],
            "horarios": {"ini": 9, "fim": 10},
        },
    ]
    indice_fileira = 1
    for i in range(len(professores)):
        nome = professores[i]["nome"]
        label_professor_nome = tk.Label(root, text=f"Nome: {nome}")
        label_professor_nome.grid(row=indice_fileira, column=0, padx=10, pady=10)
        indice_fileira = indice_fileira + 1
        for j, curso in enumerate(professores[i]["cursos"]):
            label_professor_cursos = tk.Label(root, text=f"Curso: {curso}")
            label_professor_cursos.grid(row=indice_fileira, column=0, padx=10, pady=10)
            indice_fileira = indice_fileira + 1

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_levantamentos_admin)
    botao_voltar.grid(row=indice_fileira + 1, column=0, padx=10, pady=10)


def show_media_avaliacao():
    for widget in root.winfo_children():
        widget.destroy()

    label_media = tk.Label(root, text=f"Media Avaliações")
    label_media.grid(row=0, column=0, padx=10, pady=10)

    # tem q ser puxado do módulo avaliações

    erro = avaliacao.get_avaliacoes()

    avaliacoes = ["(Selecione Uma Avaliação)"] + [av["nome"] for av in erro[1]]
    avaliacoes_var = tk.StringVar(root)
    avaliacoes_var.set(avaliacoes[0])  # Definir valor padrão como vazio

    label_avaliacoes = tk.Label(root, text="Selecione uma Avaliação:")
    label_avaliacoes.grid(row=1, column=0, padx=10, pady=10)

    menu_avaliacoes = tk.OptionMenu(root, avaliacoes_var, *avaliacoes)
    menu_avaliacoes.grid(row=1, column=1, padx=10, pady=10)

    botao_ver_media = tk.Button(
        root, text="Ver Média", command=lambda: send_media(avaliacoes_var.get())
    )
    botao_ver_media.grid(row=2, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_levantamentos_admin)
    botao_voltar.grid(row=2, column=0, padx=10, pady=10)


def send_media(id_avaliacao):
    if id_avaliacao == "(Selecione uma Avaliação)":
        messagebox.showerror("Error", "Nenhuma Avaliação foi selecionada.")
        show_media_avaliacao()
    else:
        codigo_retorno, lista_respostas= respostas.get_respostas_by_avaliacao(id_avaliacao)

        if codigo_retorno == 0:
            notas = [resp["nota"] for resp in lista_respostas]
            media = sum(notas) / len(notas)
            messagebox.showinfo("Média da Avaliação", f"A media da avaliação {id_avaliacao} foi de {media}")
            show_media_avaliacao()
        else:
            messagebox.showerror("Error", "Nenhuma resposta foi encontrada para esta avaliação.")
            show_media_avaliacao()

def show_turma_por_filiais():
    for widget in root.winfo_children():
        widget.destroy()

    label_turmasfil = tk.Label(root, text=f"Turmas Por Filiais")
    label_turmasfil.grid(row=0, column=0, padx=10, pady=10)

    # as filiais devem ser puxadas pelo módulo filial via filial.get_filiais()
    codigo_retorno, filiais = filial.get_filiais()

    if codigo_retorno == 0:  # Verifica se a operação foi realizada com sucesso
        nomes_filiais = [filial["nome"] for filial in filiais]
        nomes_filiais.insert(0, "(Selecione uma Filial)")
    else:
        nomes_filiais = ["Filiais não encontradas"]
    filiais_var = tk.StringVar(root)
    filiais_var.set(nomes_filiais[0])  # Definir valor padrão como vazio

    label_turmasfil = tk.Label(root, text=f"Selecione uma Filial:")
    label_turmasfil.grid(row=1, column=0, padx=10, pady=10)

    menu_filiais = tk.OptionMenu(root, filiais_var, *nomes_filiais)
    menu_filiais.grid(row=1, column=1, padx=10, pady=10)

    botao_ver_media = tk.Button(
        root,
        text="Ver Turmas",
        command=lambda: send_turmas_por_filiais(filiais_var.get()),
    )
    botao_ver_media.grid(row=2, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_levantamentos_admin)
    botao_voltar.grid(row=2, column=0, padx=10, pady=10)


def send_turmas_por_filiais(nome_filial):
    if nome_filial == "(Selecione uma Filial)":
        messagebox.showerror("Erro", "Nenhuma Filial selecionada.")
        show_turma_por_filiais()
    else:
        # Obter o código e a lista de filiais
        codigo, filiais = filial.get_filiais()
        if codigo != 0:
            messagebox.showerror("Erro", f"Código de erro: {codigo}")
            return

        id_filial = None
        for f in filiais:
            if f["nome"] == nome_filial:
                id_filial = f["id"]
                break

        if id_filial is None:
            messagebox.showerror(
                "Erro",
                f"Não foi possível encontrar a filial com o nome '{nome_filial}'.",
            )
            return

        # Obter turmas da filial através do módulo aula
        codigo_turmas, turmas = filialturma.get_turmas_por_filial(id_filial)
        if codigo_turmas != 0:
            messagebox.showerror("Erro", f"Código de erro: {codigo_turmas}")
            return

        # Contar turmas ativas PRECISA DA AJUDA PARA COMPLETAR AQUI DO MODULO TURMA
        turmas_ativas = 0
        # for turma_id in turmas:
        #     if is_ativa(turma_id):  # Verifica se a turma está ativa
        #         turmas_ativas += 1

        messagebox.showinfo(
            "Turmas na Filial",
            f"Existem {turmas_ativas} turmas ativas na filial '{nome_filial}'.",
        )
        show_turma_por_filiais()


def show_tela_cadastro_admin():
    for widget in root.winfo_children():
        widget.destroy()

    label_media = tk.Label(root, text=f"Criar Cadastro (Professores)")
    label_media.grid(row=0, column=0, padx=10, pady=10)

    label_usuario = tk.Label(root, text="Novo Usuario:")
    label_usuario.grid(row=1, column=0, padx=10, pady=10)

    entrada_usuario = tk.Entry(root)
    entrada_usuario.grid(row=1, column=1, padx=10, pady=10)

    label_senha = tk.Label(root, text="Nova Senha:")
    label_senha.grid(row=2, column=0, padx=10, pady=10)

    entrada_senha = tk.Entry(root, show="*")
    entrada_senha.grid(row=2, column=1, padx=10, pady=10)
    # WARNING: so cadastros de PROFESSORES podem ser criados

    # os cursos devem ser puxadas pelo módulo cadastro via curso.get_cursos()

    # limpa as listas para receberem os cursos e filiais que o professor que está sendo criado pode lecionar/estar
    global lista_cursos_aptos, lista_filiais_aptas
    lista_cursos_aptos = []
    lista_filiais_aptas = []

    cursos = ["(Selecione um Curso)", "Curso1", "Curso2", "Curso3", "Curso4", "Curso5"]
    cursos_var = tk.StringVar(root)
    cursos_var.set(cursos[0])  # Definir valor padrão como vazio

    label_cursos = tk.Label(root, text="Cursos Aptos:")
    label_cursos.grid(row=3, column=0, padx=10, pady=10)

    menu_cursos = tk.OptionMenu(root, cursos_var, *cursos)
    menu_cursos.grid(row=3, column=1, padx=10, pady=10)

    botao_adicionar_curso = tk.Button(
        root, text="Adicionar", command=lambda: send_append_curso_prof(cursos_var.get())
    )
    botao_adicionar_curso.grid(row=4, column=1, padx=10, pady=10)

    codigo_retorno, filiais = filial.get_filiais()

    if codigo_retorno == 0:  # Verifica se a operação foi realizada com sucesso
        nomes_filiais = [filial["nome"] for filial in filiais]
        nomes_filiais.insert(0, "(Selecione uma Filial)")

    else:
        nomes_filiais = ["Filiais não encontradas"]

    filiais_var = tk.StringVar(root)
    filiais_var.set(nomes_filiais[0])  # Definir valor padrão como vazio

    label_filiais = tk.Label(root, text="Filiais Possíveis:")
    label_filiais.grid(row=5, column=0, padx=10, pady=10)

    menu_filiais = tk.OptionMenu(root, filiais_var, *nomes_filiais)
    menu_filiais.grid(row=5, column=1, padx=10, pady=10)

    botao_adicionar_filial = tk.Button(
        root,
        text="Adicionar",
        command=lambda: send_append_filial_prof(filiais_var.get()),
    )
    botao_adicionar_filial.grid(row=6, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(
        root,
        text="Criar Cadastro",
        command=lambda: send_cria_cadastro_admin(
            entrada_usuario.get(),
            entrada_senha.get(),
            lista_cursos_aptos,
            lista_filiais_aptas,
        ),
    )
    botao_voltar.grid(row=7, column=1, padx=10, pady=10)

    label_alt = tk.Label(root, text=f"Alterar Cadastro")
    label_alt.grid(row=8, column=0, padx=10, pady=10)
    # os users devem ser puxadas pelo módulo cadastro via cadastro.get_users()
    # os users com flag "professor" devem aparecer, o restante não
    users = ["(Selecione um Usuário)", "User1", "User2", "User3", "User4", "User5"]
    users_var = tk.StringVar(root)
    users_var.set(users[0])  # Definir valor padrão como vazio

    label_user = tk.Label(root, text="Selecione um Usuário:")
    label_user.grid(row=9, column=0, padx=10, pady=10)

    menu_users = tk.OptionMenu(root, users_var, *users)
    menu_users.grid(row=9, column=1, padx=10, pady=10)

    label_senhaalt = tk.Label(root, text="Nova Senha:")
    label_senhaalt.grid(row=10, column=0, padx=10, pady=10)

    entrada_senhaalt = tk.Entry(root, show="*")
    entrada_senhaalt.grid(row=10, column=1, padx=10, pady=10)

    botao_alterar = tk.Button(
        root,
        text="Alterar Senha",
        command=lambda: send_altera_senha_cadastro(
            users_var.get(), entrada_senhaalt.get()
        ),
    )
    botao_alterar.grid(row=11, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_admin)
    botao_voltar.grid(row=11, column=0, padx=10, pady=10)


def send_append_curso_prof(id_curso):
    if id_curso == "(Selecione um Curso)":
        messagebox.showerror("Erro", "Você não selecionou um Curso.")
        show_tela_cadastro_admin()
    else:
        global lista_cursos_aptos
        lista_cursos_aptos.append(id_curso)
        show_tela_cadastro_admin()


def send_append_filial_prof(id_filial):
    if id_filial == "(Selecione Uma Filial)":
        messagebox.showerror("Erro", "Você não selecionou uma Filial.")
        show_tela_cadastro_admin()
    else:
        global lista_filiais_aptas
        lista_filiais_aptas.append(id_filial)
        show_tela_cadastro_admin()


def send_cria_cadastro_admin(usuario, senha, cursos, filiais, ini, fim):
    if not cursos:
        messagebox.showerror("Sem Cursos", "Professor não tem cursos aptos.")
        show_tela_criacadastro_admin()
    else:
        if not filiais:
            messagebox.showerror("Sem Filial.", "Professor não tem filial disponível.")
            show_tela_criacadastro_admin()
        else:
            try:
                valor_ini = int(ini)
                try:
                    valor_fim = int(fim)
                    if valor_ini < valor_fim:
                        # cursos e filiais é pra adicionar na entidade professor correspondente o id que sera relacionado
                        # teste do append apenas (pode excluir no final)
                        print(f"{cursos}")
                        print(f"{filiais}")
                        horario = {"ini": valor_ini, "fim": valor_fim}
                        # aqui deve ser iniciado o add_professor do modulo professor onde ele pegaria cursos filiais horario e geraria um id novo
                        id_usuario = 2
                        erro = cadastro.add_cadastro(
                            usuario, senha, id_usuario, "professor"
                        )
                        if erro[0] != 0:
                            messagebox.showerror(
                                "Erro", f"Erro: {get_msg_status(erro[0])}"
                            )
                            show_tela_criacadastro_admin()
                        else:
                            messagebox.showinfo(
                                "Cadastro Concluido",
                                "Novo Professor já foi credenciado.",
                            )

                            # limpa as listas para receberem os cursos e filiais que o professor que está sendo criado pode lecionar/estar
                            global lista_cursos_aptos, lista_filiais_aptas
                            lista_cursos_aptos = []
                            lista_filiais_aptas = []

                            show_tela_criacadastro_admin()
                    else:
                        messagebox.showerror(
                            "Error", "Intervalo de disponibilidade inválido"
                        )
                except ValueError:
                    messagebox.showerror(
                        "Numero Inválido", "Numero de horário final incorreto."
                    )
            except ValueError:
                messagebox.showerror(
                    "Numero Inválido", "Numero de horário inicial incorreto."
                )


def send_altera_senha_cadastro(user, senha):
    # basicamente vai chama a função do módulo cadastro e usa cadastro.set_senha(user,senha)
    # serve para caso alguem esqueça ou pare de trabalhar e precisa ser retirado do acesso a conta
    messagebox.showinfo("Senha Alterada", f"A senha do usuario {user} foi alterada.")
    show_tela_cadastro_admin()


def show_tela_filiais_admin():
    for widget in root.winfo_children():
        widget.destroy()

    label_filiais = tk.Label(root, text="Gestão Filiais")
    label_filiais.grid(row=0, column=0, padx=10, pady=10)

    label_criar_filial = tk.Label(root, text="Criar Filial:")
    label_criar_filial.grid(row=1, column=0, padx=10, pady=10)

    botao_criar = tk.Button(root, text="Criar", command=show_tela_criar_filial)
    botao_criar.grid(row=1, column=1, padx=10, pady=10)

    label_apagar_filial = tk.Label(root, text="Apagar Filial:")
    label_apagar_filial.grid(row=2, column=0, padx=10, pady=10)

    # as filiais devem ser puxadas pelo módulo filial via filial.get_filiais()
    codigo_retorno, filiais = filial.get_filiais()

    if codigo_retorno == 0:  # Verifica se a operação foi realizada com sucesso
        nomes_filiais = [filial["nome"] for filial in filiais]
        nomes_filiais.insert(0, "(Selecione uma Filial)")
    else:
        nomes_filiais = ["Filiais não encontradas"]
    filiais_var = tk.StringVar(root)
    filiais_var.set(nomes_filiais[0])  # Definir valor padrão como vazio

    menu_filiais = tk.OptionMenu(root, filiais_var, *nomes_filiais)
    menu_filiais.grid(row=2, column=1, padx=10, pady=10)

    botao_deletar = tk.Button(
        root, text="Deletar", command=lambda: send_del_filial(filiais_var.get())
    )
    botao_deletar.grid(row=3, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_admin)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def show_tela_criar_filial():
    for widget in root.winfo_children():
        widget.destroy()

    label_criar = tk.Label(root, text="Criar Filial")
    label_criar.grid(row=0, column=0, padx=10, pady=10)

    label_nome = tk.Label(root, text="Nome:")
    label_nome.grid(row=1, column=0, padx=10, pady=10)

    entrada_nome = tk.Entry(root)
    entrada_nome.grid(row=1, column=1, padx=10, pady=10)

    label_bairro = tk.Label(root, text="Bairro:")
    label_bairro.grid(row=2, column=0, padx=10, pady=10)

    entrada_bairro = tk.Entry(root)
    entrada_bairro.grid(row=2, column=1, padx=10, pady=10)

    botao_criar = tk.Button(
        root,
        text="Criar",
        command=lambda: send_add_filial(entrada_nome.get(), entrada_bairro.get()),
    )
    botao_criar.grid(row=3, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_filiais_admin)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_add_filial(nome, bairro):
    try:
        erro = filial.add_filial(nome, bairro)

        if erro == 0:  # Assumindo que 0 indica sucesso
            messagebox.showinfo("Concluído", f"A filial {nome} foi criada.")
            show_tela_principal_admin()
        else:
            messagebox.showerror(
                "Erro", f"Erro ao adicionar a filial. Código de erro: {erro}"
            )

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar a filial: {str(e)}")


def send_del_filial(nome_filial):
    if nome_filial == "(Selecione uma Filial)":
        messagebox.showinfo(
            "Informação Inválida", "Você não selecionou uma Filial válida."
        )
        show_tela_filiais_admin()
    else:
        codigo, filiais = filial.get_filiais()
        if codigo == 0:
            id_filial = None
            for f in filiais:
                if f["nome"] == nome_filial:
                    id_filial = f["id"]
                    break
        else:
            messagebox.showerror("Erro", "Código:", codigo)
            return

        if id_filial is None:
            messagebox.showerror(
                "Erro",
                f"Não foi possível encontrar a filial com o nome '{nome_filial}'.",
            )
        else:
            resultado = messagebox.askyesno(
                "Aviso", f"Deseja deletar a filial '{nome_filial}' com ID {id_filial}?"
            )
            if resultado:
                status = filial.del_filial(
                    id_filial
                )  # Chama a função del_filial do módulo filial.py
                if status == 0:  # Operação realizada com sucesso
                    show_tela_filiais_admin()
                    messagebox.showinfo(
                        "Filial Deletada", f"A filial '{nome_filial}' foi deletada."
                    )
                else:
                    messagebox.showerror(
                        "Erro", "Ocorreu um erro deletar a filial.", status
                    )
            else:
                show_tela_filiais_admin()


def show_tela_formacoes_admin():
    for widget in root.winfo_children():
        widget.destroy()

    label_formacoes = tk.Label(root, text="Gestão Formações")
    label_formacoes.grid(row=0, column=0, padx=10, pady=10)

    label_criar_formacao = tk.Label(root, text="Criar Formação:")
    label_criar_formacao.grid(row=1, column=0, padx=10, pady=10)

    botao_criar = tk.Button(root, text="Criar", command=show_tela_cria_formacao)
    botao_criar.grid(row=1, column=1, padx=10, pady=10)

    label_apagar_formacao = tk.Label(root, text="Apagar Formação:")
    label_apagar_formacao.grid(row=2, column=0, padx=10, pady=10)

    # as formações deve ser puxadas pelo módulo formação via formacao.get_formacoes()
    formacoes = [
        "(Selecione uma Formação)",
        "Engenheiro de Software",
        "Análise de Dados",
        "Paisagismo",
        "Pesquisa Laboratorial",
        "Pintura em Aquarela",
    ]
    formacoes_var = tk.StringVar(root)
    formacoes_var.set(formacoes[0])  # Definir valor padrão como vazio

    menu_formacoes = tk.OptionMenu(root, formacoes_var, *formacoes)
    menu_formacoes.grid(row=2, column=1, padx=10, pady=10)

    botao_deletar = tk.Button(
        root, text="Deletar", command=lambda: send_del_formacao(formacoes_var.get())
    )
    botao_deletar.grid(row=3, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_admin)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_del_formacao(id_formacao):
    if id_formacao == "(Selecione uma Formação)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Formação.")
        show_tela_formacoes_admin()
    else:
        resultado = messagebox.askyesno("Aviso", "Deseja deletar esta Formação?")
        if resultado:
            # aqui será adicionado a função de acesso do módulo formacao
            # erro= formacao.del_formacao(id_formacao)
            # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
            # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

            # AVISO: formacao SO é apagado do modulo FORMACAO, por mais que ele exista em outros modulos como o Formatura
            # é necessário que ele continue existindo lá por questões de monitoramento do histórico, mesmo de formações extintas
            messagebox.showinfo("Concluido", "Esta Formação foi Deletada.")
            show_tela_formacoes_admin()
        else:
            show_tela_formacoes_admin()


def show_tela_cria_formacao():
    for widget in root.winfo_children():
        widget.destroy()

    global lista_cursos_formacao
    lista_cursos_formacao = []

    label_formacoes = tk.Label(root, text="Criação Formação")
    label_formacoes.grid(row=0, column=0, padx=10, pady=10)

    label_nome = tk.Label(root, text="Nome:")
    label_nome.grid(row=1, column=0, padx=10, pady=10)

    entrada_nome = tk.Entry(root)
    entrada_nome.grid(row=1, column=1, padx=10, pady=10)

    # os cursos vão ter que se puxado do database do módulo cursos
    cursos = [
        "(Selecione o Curso)",
        "Psicologia",
        "Programação",
        "Física",
        "Medicina",
        "História",
    ]
    cursos_var = tk.StringVar(root)
    cursos_var.set(cursos[0])  # Definir valor padrão como vazio

    label_matricula = tk.Label(root, text="Selecione Cursos para Formação:")
    label_matricula.grid(row=2, column=0, padx=10, pady=10)

    menu_cursos = tk.OptionMenu(root, cursos_var, *cursos)
    menu_cursos.grid(row=2, column=1, padx=10, pady=10)

    botao_criar = tk.Button(
        root, text="Adicionar", command=lambda: send_append_curso(cursos_var.get())
    )
    botao_criar.grid(row=3, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_formacoes_admin)
    botao_voltar.grid(row=4, column=0, padx=10, pady=10)

    botao_voltar = tk.Button(
        root,
        text="Criar Formação",
        command=lambda: send_add_formacao(entrada_nome.get(), lista_cursos_formacao),
    )
    botao_voltar.grid(row=4, column=1, padx=10, pady=10)


def send_append_curso(id_curso):
    if id_curso == "(Selecione o Curso)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Curso.")
        show_tela_cria_formacao()
    else:
        global lista_cursos_formacao
        lista_cursos_formacao.append(id_curso)
        messagebox.showinfo(
            "Curso Adicionado", f"O curso {id_curso} foi adicionado a formação."
        )
        show_tela_cria_formacao()


def send_add_formacao(nome, cursos):
    # aqui será adicionado a chamada da função de acesso do módulo formacao
    # erro, id = formacao.add_formacao(nome,cursos)
    # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
    # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

    messagebox.showinfo("Concluido", f"A Formação {nome} foi criada.")
    show_tela_cria_formacao()


# Sessão: Aluno
def show_tela_principal_aluno():
    for widget in root.winfo_children():
        widget.destroy()

    label_bem_vindo_aluno = tk.Label(root, text="Sessão: Aluno")
    label_bem_vindo_aluno.grid(row=0, column=0, padx=10, pady=10)

    botao_matricula = tk.Button(
        root, height=5, text="Matricular-se", command=show_tela_matricula_aluno
    )
    botao_matricula.grid(row=1, rowspan=2, column=0, padx=10, pady=10)

    botao_cursos = tk.Button(
        root, height=5, text="Turmas", command=show_tela_turmas_aluno
    )
    botao_cursos.grid(row=1, rowspan=2, column=1, padx=10, pady=10)

    botao_certificado = tk.Button(
        root, height=5, text="Cancelar Turma", command=show_tela_cancelamento_aluno
    )
    botao_certificado.grid(row=1, rowspan=2, column=2, padx=10, pady=10)

    botao_formacao = tk.Button(
        root, height=5, text="Formacoes", command=show_tela_formacoes_aluno
    )
    botao_formacao.grid(row=1, rowspan=2, column=3, padx=10, pady=10)

    botao_logout = tk.Button(root, text="Logout", command=show_tela_login)
    # WARNING: na aplicação final não deve-se retornar para a tela login, e sim para uma função que feche o sistema e salve tudo
    botao_logout.grid(row=3, padx=10, pady=10)


def show_tela_matricula_aluno():
    for widget in root.winfo_children():
        widget.destroy()

    label_matricula = tk.Label(root, text="Matrícular-se Em Um Curso")
    label_matricula.grid(row=0, column=0, padx=10, pady=10)

    # os cursos vão ter que se puxado do database do módulo cursos
    cursos = [
        "(Selecione o Curso)",
        "Psicologia",
        "Programação",
        "Física",
        "Medicina",
        "História",
    ]
    cursos_var = tk.StringVar(root)
    cursos_var.set(cursos[0])  # Definir valor padrão como vazio

    label_matricula = tk.Label(root, text="Selecione um Curso:")
    label_matricula.grid(row=1, column=0, padx=10, pady=10)

    menu_cursos = tk.OptionMenu(root, cursos_var, *cursos)
    menu_cursos.grid(row=1, column=1, padx=10, pady=10)

    formato_aula = ["(Selecione um Formato)", "Presencial", "À Distância"]
    formato_aula_var = tk.StringVar(root)
    formato_aula_var.set(formato_aula[0])  # Definir valor padrão como vazio

    label_matricula = tk.Label(root, text="Selecione um Formato de Aula:")
    label_matricula.grid(row=2, column=0, padx=10, pady=10)

    menu_formato = tk.OptionMenu(root, formato_aula_var, *formato_aula)
    menu_formato.grid(row=2, column=1, padx=10, pady=10)

    botao_matricula = tk.Button(
        root,
        text="Matricular",
        command=lambda: send_add_matricula(
            aluno_da_sessao, cursos_var.get(), formato_aula_var.get()
        ),
    )
    botao_matricula.grid(row=3, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_aluno)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_add_matricula(id_aluno, id_curso, quer_online):

    if id_curso == "(Selecione o Curso)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Curso.")
        show_tela_matricula_aluno()

    elif quer_online == "(Selecione um Formato)":
        messagebox.showinfo(
            "Informação Inválida", "Você não selecionou Formato de Aula."
        )
        show_tela_matricula_aluno()
    else:
        # futuramente, a função do módulo matrícula vai ta aqui matricula.add_matricula(id_aluno,id_curso,quer_online)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

        messagebox.showinfo("Matrícula Concluida", "Você está foi matrículado.")

        show_tela_principal_aluno()


def show_tela_turmas_aluno():
    for widget in root.winfo_children():
        widget.destroy()

    label_turmas_aluno = tk.Label(root, text="Minhas Turmas")
    label_turmas_aluno.grid(row=0, column=0, padx=10, pady=10)

    # as turmas vão ter que se puxadas do database do módulo matrícula
    # turmas = matricula.get_turmas_by_aluno(aluno_da_sessao)
    turmas = ["(Selecione uma Turma)", "102A", "103A", "104A", "105A", "106A"]
    turmas_var = tk.StringVar(root)
    turmas_var.set(turmas[0])  # Definir valor padrão como vazio

    label_turmas = tk.Label(root, text="Selecione uma Turma:")
    label_turmas.grid(row=1, column=0, padx=10, pady=10)

    menu_turmas = tk.OptionMenu(root, turmas_var, *turmas)
    menu_turmas.grid(row=1, column=1, padx=10, pady=10)

    botao_faltas = tk.Button(
        root,
        height=5,
        text="Ver Faltas",
        command=lambda: send_get_faltas(turmas_var.get(), aluno_da_sessao),
    )
    botao_faltas.grid(row=2, column=0, padx=10, pady=10)

    botao_situacao = tk.Button(
        root,
        height=5,
        text="Ver Situação Acadêmica",
        command=lambda: send_situacao(turmas_var.get(), aluno_da_sessao),
    )
    botao_situacao.grid(row=2, column=1, padx=10, pady=10)

    botao_avaliacoes = tk.Button(
        root,
        height=5,
        text="Ver Avaliações",
        command=lambda: show_tela_avaliacoes_aluno(turmas_var.get()),
    )
    botao_avaliacoes.grid(row=2, column=2, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_aluno)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_get_faltas(id_turma, id_aluno):
    if id_turma == "(Selecione uma Turma)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Turma.")
        show_tela_turmas_aluno()
    else:
        # futuramente, a função do módulo matrícula vai ta aqui matricula.get_faltas(id_turma,id_aluno)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

        messagebox.showinfo("Faltas", f"Você possui x faltas na turma {id_turma}.")
        show_tela_turmas_aluno()


def send_situacao(id_turma, id_aluno):
    if id_turma == "(Selecione uma Turma)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Turma.")
        show_tela_turmas_aluno()

    # futuramente, iremos verificar no módulo turma se essa turma já se encerrou com if (turma.is_final(id_turma) == True) and (turma.is_ativa(id_turma) == False)
    # Depois, a função do módulo matrícula vai ta aqui  resultado = matricula.is_aprovado(id_aluno,id_turma)
    # Então , se o resultado for true mensagem de aprovação , se não de reprovação
    # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
    # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
    return


def show_tela_avaliacoes_aluno(id_turma):
    if id_turma == "(Selecione uma Turma)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Turma.")
        show_tela_turmas_aluno()
    else:
        for widget in root.winfo_children():
            widget.destroy()

        label_turmas_aluno = tk.Label(root, text=f"Avaliações Turma {id_turma}")
        label_turmas_aluno.grid(row=0, column=0, padx=10, pady=10)

        # primeiro teremos que achar o curso dessa turma por meio do módulo assunto assunto.get_curso_by_turma(id_turma)
        # disso, descobrir a lista de avalicoes pelo modulo criterioaprovacao sendo:
        # avaliacoes = crieterioaprovacao.get_criterio(assunto.get_curso_by_turma(id_turma))

        erro = avaliacao.get_avaliacoes()

        avaliacoes = ["(Selecione Uma Avaliação)"] + [av["nome"] for av in erro[1]]
        avaliacoes_var = tk.StringVar(root)
        avaliacoes_var.set(avaliacoes[0])  # Definir valor padrão como vazio

        label_avaliacoes = tk.Label(root, text="Selecione uma Avaliação:")
        label_avaliacoes.grid(row=1, column=0, padx=10, pady=10)

        menu_avaliacoes = tk.OptionMenu(root, avaliacoes_var, *avaliacoes)
        menu_avaliacoes.grid(row=1, column=1, padx=10, pady=10)

        botao_notas = tk.Button(
            root,
            height=5,
            text="Fazer Prova",
            command=lambda: show_tela_fazer_prova(
                avaliacoes_var.get(), aluno_da_sessao, id_turma
            ),
        )  # precisa do atributo turma para poder voltar a pagina que estava
        botao_notas.grid(row=2, column=0, padx=10, pady=10)

        botao_notas = tk.Button(
            root,
            height=5,
            text="Ver Nota",
            command=lambda: send_get_resposta_by_aluno(
                avaliacoes_var.get(), aluno_da_sessao, id_turma
            ),
        )  # precisa do atributo turma para poder voltar a pagina que estava
        botao_notas.grid(row=2, column=1, padx=10, pady=10)

        botao_gabarito = tk.Button(
            root,
            height=5,
            text="Ver Gabarito",
            command=lambda: show_tela_gabarito_aluno(
                avaliacoes_var.get(), aluno_da_sessao, id_turma
            ),
        )  # precisa do atributo turma para poder voltar a pagina que estava
        botao_gabarito.grid(row=2, column=2, padx=10, pady=10)

        botao_voltar = tk.Button(root, text="Voltar", command=show_tela_turmas_aluno)
        botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def show_tela_fazer_prova(id_avaliacao, id_aluno, id_turma):
    if id_avaliacao == "(Selecione uma Avaliação)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou uma Avaliação.")
        show_tela_avaliacoes_aluno(id_turma)
    else:
        for widget in root.winfo_children():
            widget.destroy()

        label_turmas_aluno = tk.Label(root, text=f"Avaliação: {id_avaliacao}")
        label_turmas_aluno.grid(row=0, column=0, padx=10, pady=10)

        # pega as perguntas do módulo avaliacao dic_avaliacao= avaliacao.get_avaliacao()
        # perguntas = dic_avaliacao("perguntas")
        respostas = []
        perguntas = [
            "Qual meu nome?\n 1.Daniel 2.Danie 3.Dani 4.Dan 5.Da",
            "Qual meu sobrenome?\n 1.Tannure 2.Tannur 3.Tannu 4.Tann 5.Tan",
        ]

        # Montagem da prova na Tela
        for i, pergunta in enumerate(perguntas):
            label_pergunta = tk.Label(root, text=pergunta)
            label_pergunta.grid(row=3 * i + 1, column=0, padx=10, pady=10)
            numero_escolhido = tk.IntVar()
            escala = tk.Scale(
                root, from_=1, to=5, orient=tk.HORIZONTAL, variable=numero_escolhido
            )
            escala.grid(row=3 * i + 2, column=0, columnspan=2, padx=10, pady=10)
            botao_resposta = tk.Button(
                root,
                text="Confirmar Resposta",
                command=lambda: respostas.append(numero_escolhido.get()),
            )
            # WARNING: não pode ficar apertando no botão confirmar resposta mais de uma vez, se não ele automaticamente guarda mais de 1 resposta
            # é como se ele "respondesse a questão seguinte"
            botao_resposta.grid(row=3 * i + 3, column=1, padx=10, pady=10)

        botao_concluir = tk.Button(
            root,
            text="Finalizar Prova",
            command=lambda: send_add_respostas(
                id_aluno, id_avaliacao, respostas, id_turma
            ),
        )  # precisa do atributo turma para poder voltar a pagina que estava
        botao_concluir.grid(row=3 * len(perguntas) + 1, column=1, padx=10, pady=10)


def send_add_respostas(id_aluno, id_avaliacao, respostas, id_turma):
    print(respostas)  # só ta aqui para debugar pode tirar no final

    # Aqui será chamado o modulo respostas que adicionará a resposta do aluno por meio da função de acesso 
    codigo_retorno, dic = resposta.add_respostas(id_aluno,id_avaliacao, respostas)

    if codigo_retorno == 0:
        messagebox.showinfo("Concluido", "Suas Notas foram enviadas.")
    # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
    # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
    else:
        # tratar erro aqui
        pass
    show_tela_avaliacoes_aluno(id_turma)


def send_get_resposta_by_aluno(id_avaliacao, id_aluno, id_turma):
    if id_avaliacao == "(Selecione uma Avaliação)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou uma Avaliação.")
        show_tela_avaliacoes_aluno()
    else:
        codigo_retorno, dic_resposta= resposta.get_resposta(id_aluno,id_avaliacao)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
        if codigo_retorno == 0:
            nota = dic_resposta["nota"]
            messagebox.showinfo("Resultado", f"Sua nota é {nota}.")
        else:
            # tratar erro aqui
            pass
        show_tela_avaliacoes_aluno(id_turma)


def show_tela_gabarito_aluno(id_avaliacao, id_aluno, id_turma):
    if id_avaliacao == "(Selecione uma Avaliação)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou uma Avaliação.")
        show_tela_avaliacoes_aluno(id_turma)
    else:
        for widget in root.winfo_children():
            widget.destroy()

        label_turmas_aluno = tk.Label(root, text=f"Avaliação: {id_avaliacao}")
        label_turmas_aluno.grid(row=0, column=0, padx=10, pady=10)

        # Futuramente, ele acessará o módulo resposta: erro, dic_resposta= resposta.get_resposta(id_aluno,id_avaliacao)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
        # respostas = dic_resposta["respostas"]
        # Depois no módulo avaliação pegar as perguntas e gabarito
        # erro, dic_gabarito= avaliacao.get_avaliacao(id_avaliacao)
        # perguntas = dic_gabarito["perguntas"]
        # gabarito = dic_gabarito["gabarito"]

        # ex:
        avaliacao = {"Perguntas": ["Oi?", "Meu?", "Nome?"], "Gabarito": [2, 3, 5]}
        respostas = {
            "id_aluno": id_aluno,
            "id_avaliaca": id_avaliacao,
            "respostas": [2, 3, 4],
        }

        for i in range(len(avaliacao["Perguntas"])):
            pergunta = avaliacao["Perguntas"][i]
            label_pergunta = tk.Label(root, text=f"Pergunta: {pergunta}")
            label_pergunta.grid(row=i * 3 + 1, column=0, padx=10, pady=10)
            resposta = respostas["respostas"][i]
            label_repostas = tk.Label(root, text=f"Resposta:{resposta}")
            label_repostas.grid(row=i * 3 + 2, column=0, padx=10, pady=10)
            gabarito = avaliacao["Gabarito"][i]
            label_gabarito = tk.Label(root, text=f"Gabarito: {gabarito}")
            label_gabarito.grid(row=i * 3 + 3, column=0, padx=10, pady=10)

        botao_voltar = tk.Button(
            root, text="Voltar", command=lambda: show_tela_avaliacoes_aluno(id_turma)
        )
        botao_voltar.grid(row=len(pergunta) * 3, column=0, padx=10, pady=10)


def show_tela_cancelamento_aluno():
    for widget in root.winfo_children():
        widget.destroy()

    label_cancelamento_aluno = tk.Label(root, text=f"Cancelar Curso/Turma")
    label_cancelamento_aluno.grid(row=0, column=0, padx=10, pady=10)

    # as turmas vão ter que se puxadas do database do módulo matrícula
    # turmas = matricula.get_turmas_by_aluno(aluno_da_sessao)
    turmas = ["(Selecione uma Turma)", "102A", "103A", "104A", "105A", "106A"]
    turmas_var = tk.StringVar(root)
    turmas_var.set(turmas[0])  # Definir valor padrão como vazio

    label_turmas = tk.Label(root, text="Selecione uma Turma:")
    label_turmas.grid(row=1, column=0, padx=10, pady=10)

    menu_turmas = tk.OptionMenu(root, turmas_var, *turmas)
    menu_turmas.grid(row=1, column=1, padx=10, pady=10)

    botao_cancelar = tk.Button(
        root,
        text="Cancelar Matrícula",
        command=lambda: send_del_matricula(turmas_var.get(), aluno_da_sessao),
    )
    botao_cancelar.grid(row=2, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_aluno)
    botao_voltar.grid(row=2, column=0, padx=10, pady=10)


def send_del_matricula(id_turma, id_aluno):
    if id_turma == "(Selecione uma Turma)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Turma.")
        show_tela_cancelamento_aluno()

    # Futuramente, ele acessará o módulo matrícula: erro = matricula.del_aluno(id_turma,id_aluno)
    # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
    # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

    messagebox.showinfo("Cancelamento", "Sua nota matrícula foi cancelada nesta Turma")
    show_tela_cancelamento_aluno()


def show_tela_formacoes_aluno():
    for widget in root.winfo_children():
        widget.destroy()

    label_formacoes_aluno = tk.Label(root, text=f"Formações")
    label_formacoes_aluno.grid(row=0, column=0, padx=10, pady=10)

    # as formações deve ser puxadas pelo módulo formação via formacao.get_formacoes()
    formacoes = [
        "(Selecione uma Formação)",
        "Engenheiro de Software",
        "Análise de Dados",
        "Paisagismo",
        "Pesquisa Laboratorial",
        "Pintura em Aquarela",
    ]
    formacoes_var = tk.StringVar(root)
    formacoes_var.set(formacoes[0])  # Definir valor padrão como vazio

    label_formacoes = tk.Label(root, text="Selecione uma Formação:")
    label_formacoes.grid(row=1, column=0, padx=10, pady=10)

    menu_formacoes = tk.OptionMenu(root, formacoes_var, *formacoes)
    menu_formacoes.grid(row=1, column=1, padx=10, pady=10)

    botao_inscricao = tk.Button(
        root,
        height=5,
        text="Inscrever-se",
        command=lambda: send_add_formatura(formacoes_var.get(), aluno_da_sessao),
    )
    botao_inscricao.grid(row=2, column=1, padx=10, pady=10)

    botao_certificado = tk.Button(
        root,
        height=5,
        text="Gerar Certificado",
        command=lambda: send_gerar_certificado(formacoes_var.get(), aluno_da_sessao),
    )
    botao_certificado.grid(row=2, column=0, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_aluno)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_add_formatura(id_formacao, id_aluno):
    if id_formacao == "(Selecione uma Formação)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou uma Formação.")
        show_tela_formacoes_aluno()

    # Futuramente, ele acessará o módulo formatura: erro, forma_dic = formatura.add_formatura(id_aluno,id_formacao)
    # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
    # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

    messagebox.showinfo("Inscrição Concluida", "Você foi inscrito nesta formação.")
    show_tela_formacoes_aluno()


def send_gerar_certificado(id_formacao, id_aluno):
    if id_formacao == "(Selecione uma Formação)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Turma.")
        show_tela_formacoes_aluno()
    else:
        # Futuramente, ele acessará o módulo formatura: erro, forma_dic = formatura.gerar_Certificado(id_aluno,id_formacao)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

        # se puder gerar certificado, faz a reotnrar certificado retornar o texto do certificado

        # ex:
        messagebox.showinfo("Certificado", "Seu Certificado foi gerado.")
        text = gerar_certificado()
        show_tela_certificado(text)


def gerar_certificado():  # função criada meramente para ilustrar o exemplo acima
    return """
    ==================================================
                      CERTIFICADO DE FORMAÇÃO
    ==================================================

    Certificamos que:

                              [NOME DO ALUNO]

    Concluiu com sucesso o curso de:

                              [NOME DO CURSO]

    Local de Formação:

                              [NOME DA FILIAL]

    Data de Início: [DATA DE INÍCIO]
    Data de Conclusão: [DATA DE CONCLUSÃO]

    --------------------------------------------------

    A Direção

    [NOME DA INSTITUIÇÃO]
    [ENDEREÇO DA INSTITUIÇÃO]
    [CIDADE, ESTADO, PAÍS]

    ==================================================
    """


def show_tela_certificado(text):
    for widget in root.winfo_children():
        widget.destroy()

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    text_area.pack(padx=10, pady=10)

    text_area.insert(tk.INSERT, text)

    # Desabilitar a edição do texto
    text_area.config(state=tk.DISABLED)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_formacoes_aluno)
    botao_voltar.pack(pady=10)


# Sessão: Professor
def show_tela_principal_professor():
    for widget in root.winfo_children():
        widget.destroy()

    label_bem_vindo_professor = tk.Label(root, text="Sessão: Professor")
    label_bem_vindo_professor.grid(row=0, column=0, padx=10, pady=10)

    botao_matricula = tk.Button(
        root, height=5, text="Lecionar Turmas", command=show_tela_opcoes_professor
    )
    botao_matricula.grid(row=1, rowspan=2, column=0, padx=10, pady=10)

    botao_cursos = tk.Button(
        root, height=5, text="Turmas Ativas", command=show_tela_turmas_professor
    )
    botao_cursos.grid(row=1, rowspan=2, column=1, padx=10, pady=10)

    botao_logout = tk.Button(root, text="Logout", command=show_tela_login)
    # WARNING: na aplicação final não deve-se retornar para a tela login, e sim para uma função que feche o sistema e salve tudo
    botao_logout.grid(row=3, padx=10, pady=10)


def show_tela_opcoes_professor():
    for widget in root.winfo_children():
        widget.destroy()

    label_matricula = tk.Label(root, text="Opções de Plano de Aulas")
    label_matricula.grid(row=0, column=0, padx=10, pady=10)

    # as turmas possíveis deverão ser puxadas baseada pelo horario,filiais,cursos do professor
    # que podem ser puxados por meio do modulo professor erro,dic_prof = professor.get_professor(id_professor)
    # depois disso basta caçar todas as turmas e suas respectivas informações
    # faz um for pra cada curso do professor e usa o módulo assunto pra pegar as turmas  possíveis assunto.get_turmas_by_curso(dic_prof["cursos"][i])
    # crie um item de lista para cada uma das turmas encontradas e guarde seu id e o id do curso, por fim guarde todos esse itens numa lista, formando uma matriz
    # para cada uma dessas turmas selecionada verifica quais filiais elas são a partir do módulo aula filialturma.get_filial_by_turma(id_turma)
    # percorra um for para verificar se a filial encontrada nao bate com nenhuma das filiais do professor, se nao bater descarte-a
    # caso seja, adicione em cada item de lista respectivo o id da filial
    # por fim, compare o horario de inicio e fim com o horario do professor, para acessar o de cada turma, basta usar o modulo turma erro,dic_turma= turma.get_turma(id_turma)
    # verifica se dic_turma["horario"]["ini"]<dic_prof["ini"] e dic_turma["horario"]["fim"]>dic_prof["fim"], caso nao seja , descarte-a da lista

    matriz_aulas = [
        ["id_turma1", "id_curso1", "Tijuca", {"ini": 1, "fim": 3}],
        ["id_turma2", "id_curso2", "Leme", {"ini": 1, "fim": 3}],
        ["id_turma3", "id_curso3", "Centro", {"ini": 1, "fim": 3}],
    ]

    for i, aula in enumerate(matriz_aulas):
        turma, curso, local, horario = aula
        texto_botao = f"Turma: {turma}, Curso: {curso}, Local: {local}, Inicio: {horario['ini']} Fim: {horario['fim']}"
        botao = tk.Button(
            root,
            text=texto_botao,
            command=lambda t=turma: send_add_leciona(t, professor_da_sessao),
        )
        botao.grid(row=i + 1, column=0, padx=10, pady=10)

    botao_cancelar = tk.Button(
        root, text="Cancelar", command=show_tela_principal_professor
    )
    botao_cancelar.grid(row=len(matriz_aulas) + 1, column=0, padx=10, pady=10)


def send_add_leciona(id_turma, id_professor):
    resultado = messagebox.askyesno("Aviso", "Deseja se inscrever nessa Turma?")
    if resultado:
        # aqui será adicionado a função de acesso do módulo leciona
        # erro= leciona.add_leciona(id_professor,id_turma)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
        # além disso deverá se chamado o módulo turma para abrir a turma chamando a função turma.abreturma(id_turma)
        messagebox.showinfo("Concluido", "Incrisção bem sucedida.")
        show_tela_opcoes_professor()
    else:
        show_tela_opcoes_professor()


def show_tela_turmas_professor():
    for widget in root.winfo_children():
        widget.destroy()

    label_matricula = tk.Label(root, text="Turmas Em Atividade")
    label_matricula.grid(row=0, column=0, padx=10, pady=10)

    label_turma = tk.Label(root, text="Turma:")
    label_turma.grid(row=1, column=0, padx=10, pady=10)

    # as turmas vão ter que se puxadas do database do módulo leciona
    # erro, turmas = leciona.get_turmas_by_prof(professor_da_sessao)
    # verificar quais delas estão de fato ativas

    turmas = ["(Selecione uma Turma)", "102A", "103A", "104A", "105A", "106A"]
    turmas_var = tk.StringVar(root)
    turmas_var.set(turmas[0])  # Definir valor padrão como vazio

    menu_turmas = tk.OptionMenu(root, turmas_var, *turmas)
    menu_turmas.grid(row=1, column=1, padx=10, pady=10)

    botao_presenca = tk.Button(
        root,
        height=5,
        text="Adicionar Presença",
        command=lambda: show_tela_presenca_professor(turmas_var.get()),
    )
    botao_presenca.grid(row=2, rowspan=2, column=0, padx=10, pady=10)

    botao_avaliacoes = tk.Button(
        root,
        height=5,
        text="Montar Avaliações",
        command=lambda: show_tela_montagem_professor(turmas_var.get()),
    )
    botao_avaliacoes.grid(row=2, rowspan=2, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_principal_professor)
    botao_voltar.grid(row=4, column=0, padx=10, pady=10)


def show_tela_presenca_professor(id_turma):
    for widget in root.winfo_children():
        widget.destroy()

    if id_turma == "(Selecione uma Turma)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Turma.")
        show_tela_turmas_professor()

    label_matricula = tk.Label(root, text="Marcar Presença")
    label_matricula.grid(row=0, column=0, padx=10, pady=10)

    # os alunos vão ter que se puxadas do database do módulo matricula
    # erro, alunos = matricula.get_alunos_by_turma(id_turma)
    alunos = ["(Selecione um Aluno)", "J.G.", "A.N.", "L.C.", "P.J.", "W.T."]
    alunos_var = tk.StringVar(root)
    alunos_var.set(alunos[0])  # Definir valor padrão como vazio

    label_aluno = tk.Label(root, text="Selecione um Aluno:")
    label_aluno.grid(row=1, column=0, padx=10, pady=10)

    menu_alunos = tk.OptionMenu(root, alunos_var, *alunos)
    menu_alunos.grid(row=1, column=1, padx=10, pady=10)

    botao_marcar = tk.Button(
        root,
        text="Marcar Falta",
        command=lambda: send_set_faltas(alunos_var.get(), id_turma),
    )
    botao_marcar.grid(row=3, column=1, padx=10, pady=10)

    botao_voltar = tk.Button(root, text="Voltar", command=show_tela_turmas_professor)
    botao_voltar.grid(row=3, column=0, padx=10, pady=10)


def send_set_faltas(id_aluno, id_turma):
    if id_aluno == "(Selecione um Aluno)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Aluno.")
        show_tela_presenca_professor()

    # primeiramente, chame o modulo matrícula e guarde em uma variavel erro, faltas= matricula.get_faltas(id_turma,id_aluno)
    # incremente este valor e em seguida chame o set_faltas para colocar o novo valor
    # erro = matricula.set_faltas(id_turma,id_aluno,faltas)
    # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
    # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

    messagebox.showinfo("Cadastro Concluido", "Faltas Registradas.")


def show_tela_montagem_professor(id_turma):
    for widget in root.winfo_children():
        widget.destroy()

    if id_turma == "(Selecione uma Turma)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Turma.")
        show_tela_turmas_professor()
    else:
        label_avaliacoes = tk.Label(root, text="Montar Avaliação")
        label_avaliacoes.grid(row=0, column=0, padx=10, pady=10)

        # para puxar as avaliações primeiramente tem que pegar de qual curso esta turma se insere
        # por meio do módulo assunto:  erro, curso= assunto.get_curso_by_turma(id_turma)
        # depois, puxe as avaliacoes possíveis por meio do módulo critério
        # erro, avaliacoes = criterio.get_criterio(curso)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado

        erro = avaliacao.get_avaliacoes()

        avaliacoes = ["(Selecione Uma Avaliação)"] + [av["nome"] for av in erro[1]]
        avaliacoes_var = tk.StringVar(root)
        avaliacoes_var.set(avaliacoes[0])  # Definir valor padrão como vazio

        label_avaliacao = tk.Label(root, text="Avaliação:")
        label_avaliacao.grid(row=1, column=0, padx=10, pady=10)

        menu_alunos = tk.OptionMenu(root, avaliacoes_var, *avaliacoes)
        menu_alunos.grid(row=1, column=1, padx=10, pady=10)

        botao_voltar = tk.Button(
            root, text="Voltar", command=show_tela_turmas_professor
        )
        botao_voltar.grid(row=2, column=0, padx=10, pady=10)

        botao_montar = tk.Button(
            root,
            text="Montar",
            command=lambda: show_tela_montar_professor(
                avaliacoes_var.get(), id_turma, professor_da_sessao
            ),
        )
        botao_montar.grid(row=2, column=1, padx=10, pady=10)


def show_tela_montar_professor(
    id_avaliacao, id_turma, id_prof
):  # rever os parametros necessários definidos na set_avaliacao
    for widget in root.winfo_children():
        widget.destroy()

    if id_avaliacao == "(Selecione uma Avaliação)":
        messagebox.showinfo("Informação Inválida", "Você não selecionou Avaliacao.")
        show_tela_montagem_professor(id_turma)

    global lista_perguntas_montagem
    lista_perguntas_montagem = []

    global lista_gabarito_montagem
    lista_gabarito_montagem = []

    label_avaliacoes = tk.Label(root, text="Estrutura da Prova")
    label_avaliacoes.grid(row=0, column=0, padx=10, pady=10)

    label_nome = tk.Label(root, text="Nome")
    label_nome.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    entrada_nome = tk.Entry(root)
    entrada_nome.grid(row=2, column=2, padx=10, pady=10)

    label_tipo = tk.Label(root, text="Tipo (em numero):")
    label_tipo.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    entrada_tipo = tk.Entry(root)
    entrada_tipo.grid(row=2, column=2, padx=10, pady=10)

    label_perguntas = tk.Label(root, text="Perguntas:")
    label_perguntas.grid(row=3, column=0, padx=10, pady=10)

    label_enunciado = tk.Label(root, text="Enunciado:")
    label_enunciado.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    entrada_enunciado = tk.Entry(root)
    entrada_enunciado.grid(row=4, column=2, padx=10, pady=10)

    label_resposta = tk.Label(root, text="Gabarito (em numero):")
    label_resposta.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    entrada_gabarito = tk.Entry(root)
    entrada_gabarito.grid(row=5, column=2, padx=10, pady=10)

    botao_adicionar = tk.Button(
        root,
        text="Adicionar Pergunta",
        command=lambda: send_pergunta(entrada_enunciado, entrada_gabarito),
    )
    botao_adicionar.grid(row=6, column=2, padx=10, pady=10)

    botao_voltar = tk.Button(
        root, text="Voltar", command=lambda: show_tela_montagem_professor(id_turma)
    )
    botao_voltar.grid(row=7, column=0, padx=10, pady=10)

    botao_concluir = tk.Button(
        root,
        text="Concluir Montagem",
        command=lambda: send_set_avaliacao(
            id_avaliacao,
            entrada_nome.get(),
            entrada_tipo.get(),
            id_turma,
            id_prof,
            lista_gabarito_montagem,
            lista_perguntas_montagem,
        ),
    )
    botao_concluir.grid(row=7, column=1, columnspan=2, padx=10, pady=10)


def send_pergunta(enunciado, gabarito):
    global lista_gabarito_montagem
    global lista_perguntas_montagem
    try:
        valor = int(gabarito)
        lista_gabarito_montagem.append(valor)
        lista_perguntas_montagem.append(enunciado)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")


def send_set_avaliacao(
    id_avaliacao, nome, tipo, id_turma, id_prof, gabarito, perguntas
):
    try:
        valor = int(tipo)
        # aqui caso de certo , coloque a chamada da função de acesso do modulo avaliacao
        # erro, dic_ava= avaliacao.set_avaliacao(id_avaliacao,nome,tipo,id_turma,id_prof,gabarito,perguntas)
        # baseado na conclusão da ação, se o status for OK, retornamos voltamos a tela de inicio normal
        # caso não, chamaremos futuramente a mensagem de erro do módulo de Erro coerente com o numero de erro retornado
        show_tela_montar_professor()

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")
        show_tela_montar_professor()


# Criar a janela principal
root = tk.Tk()
root.title("Plataforma de Ensino")

# Cria user admin
cadastro.add_cadastro("admin", "admin", -1, "admin")

# Mostra  a tela de login inicialmente
show_tela_login()

# Iniciar o loop principal da interface gráfica
root.mainloop()
