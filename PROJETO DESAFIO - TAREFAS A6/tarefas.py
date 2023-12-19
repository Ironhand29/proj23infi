#tarefas.py
def criar_tarefa(nome, descricao, prioridade, categoria):
    return {
        'nome': nome,
        'descricao': descricao,
        'prioridade': prioridade,
        'categoria': categoria,
        'concluida': False
    }

tarefas = []

def adicionar_tarefa(tarefa):
    tarefas.append(tarefa)

def listar_tarefas():
    for i, tarefa in enumerate(tarefas, start=1):
        status = 'Concluída' if tarefa['concluida'] else 'Pendente'
        print(f"{i}. {tarefa['nome']} - {tarefa['descricao']} - {tarefa['prioridade']} - {tarefa['categoria']} - {status}")

def marcar_como_concluida(indice):
    if 1 <= indice <= len(tarefas):
        tarefas[indice - 1]['concluida'] = True
        print(f"Tarefa '{tarefas[indice - 1]['nome']}' marcada como concluída.")
    else:
        print("Índice inválido.")

def exibir_por_prioridade(prioridade):
    tarefas_prioridade = [tarefa for tarefa in tarefas if tarefa['prioridade'] == prioridade]
    if tarefas_prioridade:
        print(f"Tarefas com prioridade {prioridade}:")
        for tarefa in tarefas_prioridade:
            print(f"- {tarefa['nome']}")
    else:
        print(f"Nenhuma tarefa encontrada com prioridade {prioridade}.")

def exibir_por_categoria(categoria):
    tarefas_categoria = [tarefa for tarefa in tarefas if tarefa['categoria'] == categoria]
    if tarefas_categoria:
        print(f"Tarefas na categoria {categoria}:")
        for tarefa in tarefas_categoria:
            print(f"- {tarefa['nome']}")
    else:
        print(f"Nenhuma tarefa encontrada na categoria {categoria}.")
