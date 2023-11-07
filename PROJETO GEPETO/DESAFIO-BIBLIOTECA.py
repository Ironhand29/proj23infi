import pickle  # importa a bibli pickle
from datetime import datetime  # importa date
import pandas as pd # importa bibli panda
senhas_por_usuario = {}
usuarios_admin = {"admin": True}
biblioteca = {
    "Livro 1": {"autor": "Autor 1", "quantidade": 5},
    "Livro 2": {"autor": "Autor 2", "quantidade": 3},
}
alugueis = {}

def verificar_senha(senha):
    if len(senha) >= 8 and len(senha) <= 12:
        return True
    return False

def listar_usuarios():
    for usuario, senhas in senhas_por_usuario.items():
        print(f"Usuário: {usuario}")
        for senha in senhas:
            print(f"  - {senha}")

def excluir_usuario(usuario):
    if usuario == "admin":
        print("Você não pode excluir o usuário admin.")
    elif usuario in senhas_por_usuario:
        if usuarios_admin.get(conta_logada, False) or usuario == conta_logada:
            del senhas_por_usuario[usuario]
            usuarios_admin.pop(usuario, None)
            print(f"Usuário {usuario} excluído.")
        else:
            print("Você não tem permissão para excluir este usuário.")
    else:
        print("Usuário não encontrado.")

def tornar_admin(usuario):
    if usuario in senhas_por_usuario:
        usuarios_admin[usuario] = True
        print(f"Usuário {usuario} promovido a administrador.")
    else:
        print("Usuário não encontrado.")

def logoff():
    print(f"{conta_logada} desconectado.")
    return None

def tentar_alterar_senha(usuario):
    senha_atual = input("Digite sua senha atual: ")
    if senha_atual in senhas_por_usuario[usuario]:
        nova_senha = input("Digite uma nova senha: ")
        if verificar_senha(nova_senha):
            senhas_por_usuario[usuario].append(nova_senha)
            print("Senha alterada com sucesso.")
        else:
            print("A nova senha não atende aos critérios. Tente novamente.")
    else:
        print("Senha atual incorreta. Tente novamente.")

def logoff_admin():
    print("Admin desconectado.")
    return None

def importar_livros_excel():
    if conta_logada is not None and usuarios_admin.get(conta_logada, False):
        arquivo_excel = input("Digite o nome do arquivo Excel com a lista de livros: ")
        try:
            # Leia os dados do arquivo Excel
            dados_excel = pd.read_excel(arquivo_excel)
            for _, row in dados_excel.iterrows():
                titulo = row['Título']
                autor = row['Autor']
                quantidade = int(row['Quantidade'])
                # Adicione os livros à biblioteca
                if titulo not in biblioteca:
                    biblioteca[titulo] = {"autor": autor, "quantidade": quantidade}
                else:
                    # Se o livro já existe na biblioteca, atualize a quantidade
                    biblioteca[titulo]["quantidade"] += quantidade
                print(f"Livros importados com sucesso.")
        except Exception as e:
            print(f"Erro ao importar livros do arquivo Excel: {str(e)}")
    else:
        print("Você não tem permissão para importar livros do Excel.")

# exporta a lista de livros da biblioteca
def exportar_livros_excel():  
    if conta_logada is not None and usuarios_admin.get(conta_logada, False):
        nome_arquivo_excel = input("Digite o nome do arquivo Excel para exportar a lista de livros: ")
        try:
            dados_exportacao = []
            for titulo, info in biblioteca.items():
                dados_exportacao.append({"Título": titulo, "Autor": info["autor"], "Quantidade": info["quantidade"]})
            
            df = pd.DataFrame(dados_exportacao)
            df.to_excel(nome_arquivo_excel, index=False)
            print(f"Lista de livros exportada com sucesso para o arquivo {nome_arquivo_excel}.")
        except Exception as e:
            print(f"Erro ao exportar lista de livros para o Excel: {str(e)}")
    else:
        print("Você não tem permissão para exportar a lista de livros para o Excel.")

def dar_baixa_livro():
    if conta_logada is not None and usuarios_admin.get(conta_logada, False):
        usuario_devolver = input("Digite o nome de usuário que está devolvendo o livro: ")
        livro_devolvido = input("Digite o título do livro que está sendo devolvido: ")
        if usuario_devolver in alugueis and livro_devolvido in alugueis[usuario_devolver]:
            # Devolver o livro ao estoque
            biblioteca[livro_devolvido]["quantidade"] += 1
            # Remover o registro de aluguel
            del alugueis[usuario_devolver][livro_devolvido]
            print(f"Livro '{livro_devolvido}' devolvido por {usuario_devolver}.")
        else:
            print("Livro não encontrado nos registros de aluguel deste usuário.")
    else:
        print("Você não tem permissão para dar baixa em livros.")

try:
    with open("senhas.pkl", "rb") as arquivo:
        senhas_por_usuario = pickle.load(arquivo)
except FileNotFoundError:
    senhas_por_usuario = {}

conta_logada = None

while True:
    if conta_logada is None:
        usuario = input("Digite seu nome de usuário (ou 'sair' para encerrar o programa): ")

        if usuario.lower() == "sair":
            break

        if usuario == "admin":
            senha_admin = input("Digite a senha de administrador: ")
            if senha_admin == "007":
                print("Bem-vindo, James. ")
                conta_logada = "admin"
            else:
                print("Senha de administrador incorreta. Acesso negado.")
        else:
            if usuario in senhas_por_usuario:
                senha_atual = input("Digite sua senha: ")
                if senha_atual in senhas_por_usuario[usuario]:
                    print("Bem-vindo de volta, " + usuario + "!")
                    conta_logada = usuario
                else:
                    print("Senha incorreta. Acesso negado.")
            else:
                print("Usuário não encontrado. Deseja registrar um novo usuário? (sim/não)")
                registrar_usuario = input()
                if registrar_usuario.lower() == "sim":
                    nova_senha = input("Digite uma senha para o novo usuário: ")
                    if verificar_senha(nova_senha):
                        senhas_por_usuario[usuario] = [nova_senha]
                        print("Usuário registrado com sucesso.")
                        conta_logada = usuario
                    else:
                        print("A senha não atende aos critérios. Registro não realizado.")

    if conta_logada is not None:
        print("\nOpções disponíveis para " + conta_logada + ":")
        print(" 1. Alterar senha")
        print(" 2. Logoff")
        print(" 7. Listar livros disponíveis")
        print(" 8. Alugar livro")
        if usuarios_admin.get(conta_logada, False):
            print(" 3. Listar usuários e senhas")
            print(" 4. Excluir usuário")
            print(" 5. Tornar usuário administrador")
            print(" 6. Adicionar livro à biblioteca")
            print(" 9. Verificar aluguéis")
            print("10. Dar Baixa em Livro")
            print("11. Importar Livros do Excel")
            print("12. Exportar Lista de Livros para Excel")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            tentar_alterar_senha(conta_logada)
        elif opcao == "2":
            conta_logada = logoff()
        elif opcao == "3" and usuarios_admin.get(conta_logada, False):
            listar_usuarios()
        elif opcao == "4" and usuarios_admin.get(conta_logada, False):
            usuario_a_excluir = input("Digite o nome de usuário a ser excluído: ")
            excluir_usuario(usuario_a_excluir)
        elif opcao == "5" and usuarios_admin.get(conta_logada, False):
            usuario_a_promover = input("Digite o nome de usuário a ser promovido a administrador: ")
            tornar_admin(usuario_a_promover)
        elif opcao == "6" and usuarios_admin.get(conta_logada, False):
            titulo = input("Digite o título do livro: ")
            autor = input("Digite o autor do livro: ")
            quantidade = int(input("Digite a quantidade disponível: "))
            biblioteca[titulo] = {"autor": autor, "quantidade": quantidade}
            print(f"Livro '{titulo}' adicionado à biblioteca.")
        elif opcao == "7":
            for livro, info in biblioteca.items():
                print(f"Título: {livro}, Autor: {info['autor']}, Quantidade Disponível: {info['quantidade']}")
        elif opcao == "8":
            if conta_logada is not None:
                if conta_logada not in alugueis:
                    alugueis[conta_logada] = {}
                livro_a_alugar = input("Digite o título do livro que deseja alugar: ")
                if livro_a_alugar in biblioteca:
                    if biblioteca[livro_a_alugar]["quantidade"] > 0:
                        if len(alugueis[conta_logada]) < 3:
                            alugueis[conta_logada][livro_a_alugar] = datetime.now()
                            biblioteca[livro_a_alugar]["quantidade"] -= 1
                            print(f"{conta_logada} alugou '{livro_a_alugar}'.")
                        else:
                            print("Você já alugou o máximo de livros permitidos (3).")
                    else:
                        print("Este livro não está disponível no momento.")
                else:
                    print("Livro não encontrado na biblioteca.")
        elif opcao == "9" and usuarios_admin.get(conta_logada, False):
            for usuario, alugueis_usuario in alugueis.items():
                for livro_alugado, data_aluguel in alugueis_usuario.items():
                    dias_aluguel = (datetime.now() - data_aluguel).days
                    print(f"{usuario} alugou '{livro_alugado}' por {dias_aluguel} dias.")
        # ... (opção para alugar livro)
        elif opcao == "10":
            dar_baixa_livro()
        elif opcao == "11":
            importar_livros_excel()  # Chame a função de importação de livros do Excel
        elif opcao == "12":
            exportar_livros_excel()  # Chame a função de exportação para Excel
        else:
            print("Opção inválida. Tente novamente.")
            

with open("senhas.pkl", "wb") as arquivo:
    pickle.dump(senhas_por_usuario, arquivo)
