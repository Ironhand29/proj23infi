# main.py

from tarefas import criar_tarefa, adicionar_tarefa, listar_tarefas, marcar_como_concluida, exibir_por_prioridade, exibir_por_categoria

while True:
    print("\n==== Menu de Tarefas ====")
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Marcar Tarefa como Concluída")
    print("4. Exibir Tarefas por Prioridade")
    print("5. Exibir Tarefas por Categoria")
    print("6. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        nome = input("Nome da tarefa: ")
        descricao = input("Descrição da tarefa: ")
        prioridade = input("Prioridade da tarefa: ")
        categoria = input("Categoria da tarefa: ")

        nova_tarefa = criar_tarefa(nome, descricao, prioridade, categoria)
        adicionar_tarefa(nova_tarefa)

        print("Tarefa adicionada com sucesso!")

    elif escolha == "2":
        listar_tarefas()

    elif escolha == "3":
        listar_tarefas()
        indice = int(input("Digite o índice da tarefa a ser marcada como concluída: "))
        marcar_como_concluida(indice)

    elif escolha == "4":
        prioridade = input("Digite a prioridade a ser filtrada: ")
        exibir_por_prioridade(prioridade)

    elif escolha == "5":
        categoria = input("Digite a categoria a ser filtrada: ")
        exibir_por_categoria(categoria)

    elif escolha == "6":
        print("Saindo do programa. Até mais!")
        break

    else:
        print("Opção inválida. Tente novamente.")
