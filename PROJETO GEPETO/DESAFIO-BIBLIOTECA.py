import json
from datetime import datetime, timedelta

# FUNÇÃO DE CRIAR USUÁRIO MESTRE
def criar_usuario_mestre():
    usuarios = {
        "admin": {
            "cpf": "12345678901",
            "senha": "007"
        }
    }
    salvar_usuarios(usuarios)

# FUNÇÃO PARA SALVAR USUÁRIOS
def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as arquivo_usuarios:
        json.dump(usuarios, arquivo_usuarios, indent=4)

#FUNÇÃO PARA CARREGAR USUÁRIOS
def carregar_usuarios():
    try:
        with open("usuarios.json", "r") as arquivo_usuarios:
            return json.load(arquivo_usuarios)
    except FileNotFoundError:
        return {}

# FUNÇÃO PARA REALIZAR LOGIN
def realizar_login(usuarios):
    tentativas = 3

    if not usuarios:
        print("Nenhum usuário cadastrado. Encerrando o programa.")
        return False

    while tentativas > 0:
        usuario = input("Digite o nome de usuário: ")
        senha = input("Digite a senha: ")

        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            print("Login bem-sucedido!")
            return True
        else:
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")

    print("Número máximo de tentativas excedido. Encerrando o programa.")
    return False

# FUNÇÃO PARA VIZUALIZAR TODOS OS USUÁRIOS CADASTRADOS
def visualizar_usuarios(usuarios):
    print("\nInformações dos Usuários Cadastrados:")
    if usuarios:
        for nome, detalhes in usuarios.items():
            print("\nNome de Usuário:", nome)
            print("CPF:", detalhes["cpf"])
            print("Senha:", detalhes["senha"])
    else:
        print("Não há usuários cadastrados.")

# FUNÇÃO PARA ALUGAR LIVRO (MENU ALUGUEL, DATA, ETC)

def alugar_livro(usuario, biblioteca, usuarios):
    if usuario not in usuarios:
        print("Usuário não encontrado.")
        return

    if "livros_alugados" not in usuarios[usuario]:
        usuarios[usuario]["livros_alugados"] = {}

    if len(usuarios[usuario]["livros_alugados"]) >= 3:
        print("Você já atingiu o limite de livros alugados (máximo: 3).")
        return

    visualizar_biblioteca(biblioteca)

    livro_escolhido = input("Digite o título do livro que deseja alugar: ")

    if livro_escolhido not in biblioteca:
        print("Livro não encontrado.")
        return

    if biblioteca[livro_escolhido]["quantidade"] <= 0:
        print("Este livro está fora de estoque no momento.")
        return

    dias_aluguel = int(input("Escolha a quantidade de dias para alugar (10, 15 ou 30): "))
    data_devolucao = datetime.now() + timedelta(days=dias_aluguel)

    usuarios[usuario]["livros_alugados"][livro_escolhido] = {
        "data_devolucao": data_devolucao.strftime("%Y-%m-%d"),
        "atrasado": False
    }

    biblioteca[livro_escolhido]["quantidade"] -= 1
    salvar_usuarios(usuarios)
    salvar_livros(biblioteca)

    print(f"Você alugou '{livro_escolhido}' por {dias_aluguel} dias. Devolução até {data_devolucao.strftime('%Y-%m-%d')}.")

#FUNÇÃO PARA VERIFICAR SE HÁ ATRASOS NA DEVOLUÇÃO DO LIVRO

def verificar_atrasos(usuario, usuarios):
    if "livros_alugados" not in usuarios[usuario]:
        return False

    hoje = datetime.now()

    for livro, detalhes in usuarios[usuario]["livros_alugados"].items():
        data_devolucao = datetime.strptime(detalhes["data_devolucao"], "%Y-%m-%d")

        if hoje > data_devolucao and not detalhes["atrasado"]:
            dias_atraso = (hoje - data_devolucao).days
            detalhes["atrasado"] = True
            print(f"Você está {dias_atraso} dias atrasado na devolução do livro '{livro}'.")

#FUNÇÃO QUE ADMINISTRA O MENU DE ALUGUEL DE LIVROS

def menu_aluguel(usuario, biblioteca, usuarios):
    verificar_atrasos(usuario, usuarios)

    print("\nOpções do Menu de Aluguel:")
    print("1. Alugar livro")
    print("2. Visualizar livros alugados")
    print("3. Devolver livro")
    print("4. Voltar ao Menu Inicial")

    escolha_menu_aluguel = input("Escolha a opção desejada (1/2/3/4): ")

    if escolha_menu_aluguel == "1":
        alugar_livro(usuario, biblioteca, usuarios)
    elif escolha_menu_aluguel == "2":
        visualizar_livros_alugados(usuario, usuarios)
    elif escolha_menu_aluguel == "3":
        devolver_livro(usuario, biblioteca, usuarios)
    elif escolha_menu_aluguel == "4":
        salvar_livros(biblioteca)
        salvar_usuarios(usuarios)
        print("Retornando ao Menu Inicial.")
    else:
        print("Opção inválida. Tente novamente.")

#FUNÇÃO PARA VERIFICAR LIVROS ALUGADOS

def visualizar_livros_alugados(usuario, usuarios):
    if "livros_alugados" not in usuarios[usuario] or not usuarios[usuario]["livros_alugados"]:
        print("Você não tem livros alugados no momento.")
        return

    print("\nLivros Alugados:")
    for livro, detalhes in usuarios[usuario]["livros_alugados"].items():
        status = "Atrasado" if detalhes["atrasado"] else "Em dia"
        print(f"\nTítulo: {livro}")
        print(f"Data de Devolução: {detalhes['data_devolucao']} ({status})")

#FUNÇÃO PARA DEVOLVER LIVROS ALUGADOS

def devolver_livro(usuario, biblioteca, usuarios):
    visualizar_livros_alugados(usuario, usuarios)

    if "livros_alugados" not in usuarios[usuario] or not usuarios[usuario]["livros_alugados"]:
        print("Você não tem livros alugados para devolver.")
        return

    livro_devolver = input("Digite o título do livro que deseja devolver: ")

    if livro_devolver not in usuarios[usuario]["livros_alugados"]:
        print("Você não alugou esse livro.")
        return

    hoje = datetime.now()
    data_devolucao = datetime.strptime(usuarios[usuario]["livros_alugados"][livro_devolver]["data_devolucao"], "%Y-%m-%d")

    if hoje > data_devolucao:
        dias_atraso = (hoje - data_devolucao).days
        print(f"Você está {dias_atraso} dias atrasado na devolução do livro '{livro_devolver}'.")
        usuarios[usuario]["livros_alugados"][livro_devolver]["atrasado"] = True

    biblioteca[livro_devolver]["quantidade"] += 1
    del usuarios[usuario]["livros_alugados"][livro_devolver]

    salvar_livros(biblioteca)
    salvar_usuarios(usuarios)
    print(f"Livro '{livro_devolver}' devolvido com sucesso.")


#FUNÇÃO PARA CADASTRAR NOVO USUÁRIO

def cadastrar_novo_usuario(usuarios):


    print("\nCadastro de Novo Usuário:")
    novo_usuario = input("Digite o nome de usuário: ")

    if novo_usuario in usuarios:
        print(f"Usuário '{novo_usuario}' já existe. Escolha outro nome de usuário.")
        return

    novo_cpf = input("Digite o CPF (apenas números): ")
    if not novo_cpf.isdigit() or len(novo_cpf) != 11:
        print("CPF inválido. Certifique-se de inserir 11 dígitos numéricos.")
        return

    nova_senha = input("Digite a senha (8 a 12 caracteres): ")
    if not (8 <= len(nova_senha) <= 12):
        print("Senha inválida. Certifique-se de que a senha tenha entre 8 e 12 caracteres.")
        return

    usuarios[novo_usuario] = {
        "cpf": novo_cpf,
        "senha": nova_senha
    }

    salvar_usuarios(usuarios)
    print(f"Usuário '{novo_usuario}' cadastrado com sucesso!")

# FUNÇÃO PARA SALVAR LIVROS ( SALVA OS LIVROS ADICIONADOS)
def salvar_livros(biblioteca):
    with open("livros.json", "w") as arquivo_livros:
        json.dump(biblioteca, arquivo_livros, indent=4)
    print("Livros salvos com sucesso!")

# CARREGAR LIVROS DA BIBLIOTECA
def carregar_livros():
    try:
        with open("livros.json", "r") as arquivo_livros:
            return json.load(arquivo_livros)
    except FileNotFoundError:
        return {}

# FUNÇÃO PARA ADICIONAR LIVROS A BIBLIOTECA, LIVROS COLOCADOS AQUI SÃO SALVOS PELO MENU DA BIBLIOTECA EM UM TERMINAL JSON
def adicionar_livros(biblioteca):
    livros_para_adicionar = {
        # ... adicione os outros livros aqui
    }

    for livro, detalhes in livros_para_adicionar.items():
        biblioteca[livro] = detalhes

    print("Livros adicionados com sucesso!")
    salvar_livros(biblioteca)

# FUNÇÃO PARA VISUALIZAR OS LIVROS NA BIBLIOTECA
def visualizar_biblioteca(biblioteca):
    print("\nInformações da Biblioteca Virtual:")
    print(f"Total de livros armazenados: {len(biblioteca)}")

    if biblioteca:
        print("\nDetalhes dos Livros:")
        for titulo, info in biblioteca.items():
            print(f"\nTítulo: {titulo}")
            print(f"Autor: {info['autor']}")
            print(f"Quantidade em estoque: {info['quantidade']}")
    else:
        print("A biblioteca está vazia.")

# FUNÇÃO QUE CONTROLA O MENU INICIAL DA GEPETO (MENU DE SELEÇÃO SAÍDA USUÁRIO)
def menu_inicial():
    print("\nOpções do Menu Inicial:")
    print("1. Visualizar informações da biblioteca virtual")
    print("2. Adicionar novo livro")
    print("3. Realizar logout")
    print("4. Cadastrar novo usuário")
    print("5. Visualizar usuários cadastrados")
    print("6. Menu de Aluguel de Livros")
    return input("Escolha a opção desejada: ")

# FUNÇÃO DE ESCOLHA DAS OPÇÕES DE MENU - CONTROLE DE MENU
def main():
    # CARREGA OU CRIA O USUÁRIO MESTRE
    usuarios = carregar_usuarios()
    if not usuarios:
        criar_usuario_mestre()
        usuarios = carregar_usuarios()

    # REALIZA LOGIM
    if realizar_login(usuarios):
        usuario = input("Digite o nome de usuário: ")
        print("Bem-vindo ao PROJETO GEPETO!")

        # INICIALIZA A BIBLIOTECA VIRTUAL
        biblioteca_virtual = carregar_livros()

        while True:
            escolha_menu = menu_inicial()

            if escolha_menu == "1":
                visualizar_biblioteca(biblioteca_virtual)

            elif escolha_menu == "2":
                adicionar_livros(biblioteca_virtual)

            elif escolha_menu == "3":
                salvar_livros(biblioteca_virtual)
                print("Logout realizado. Encerrando o programa.")
                break

            elif escolha_menu == "4":
                cadastrar_novo_usuario(usuarios)
            elif escolha_menu == "5":
                visualizar_usuarios(usuarios)
            elif escolha_menu == "6":
                menu_aluguel(usuario, biblioteca_virtual, usuarios)
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
