import random
from collections import Counter
import itertools  # Importe o módulo itertools
import numpy as np
import matplotlib.pyplot as plt

class Bot:
    def __init__(self, nome, marca, learning_rate=0.1, epsilon=0.1):
        self.nome = nome
        self.marca = marca
        self.q_table = {}
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
        self.sequencias_jogo = []
        self.learning_rate = learning_rate # Taxa de aprendizado
        self.epsilon = epsilon  # Taxa de exploração
        self.historico_partidas = []
        # Inicialize o tabuleiro com espaços em branco
        self.tabuleiro = np.empty((3, 3), dtype=str)
        self.tabuleiro[:] = ' '

    def treinar_com_historico(self):
        for partida in self.historico_partidas:
            estado = partida["estado"]
            movimento = partida["movimento"]
            recompensa = partida["recompensa"]
            proximo_estado = partida["proximo_estado"]

            self.atualizar_q_table(estado, movimento, recompensa, proximo_estado)


    def escolher_movimento(self, tabuleiro, movimentos):
        estado = tuple(tuple(row) for row in tabuleiro)
        if estado not in self.q_table:
            self.q_table[estado] = {movimento: 0 for movimento in movimentos}

        if random.random() < self.epsilon:
            melhor_movimento = random.choice(list(movimentos))
        else:
            melhor_movimento = max(self.q_table[estado], key=lambda movimento: self.q_table[estado][movimento])

        return melhor_movimento

    def atualizar_q_table(self, estado, movimento, recompensa, proximo_estado):
        if estado is not None and proximo_estado is not None:
            if estado not in self.q_table:
                self.q_table[estado] = {movimento: 0 for movimento in proximo_estado}

            self.q_table[estado][movimento] += self.learning_rate * (recompensa + max(self.q_table[proximo_estado].values()) - self.q_table[estado][movimento])
    def iniciar_sessaos_treinamento(self, sessoes):
        melhores_taxas = {
            'learning_rate': 0,
            'epsilon': 0,
            'vitorias_max': 0
        }

        for _ in range(sessoes):
            melhores_taxas = self.treinar_com_sessaos_treinamento(melhores_taxas)
            # Atualize learning_rate e epsilon com base nos resultados anteriores
            self.learning_rate = melhores_taxas['learning_rate']
            self.epsilon = melhores_taxas['epsilon']

    def treinar_com_sessaos_treinamento(self, melhores_taxas):
        # Experimente diferentes valores de learning_rate e epsilon
        learning_rates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        epsilons = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

        for learning_rate in learning_rates:
            for epsilon in epsilons:
                self.learning_rate = learning_rate
                self.epsilon = epsilon

                # Treina os bots
                jogo_bot_aprendizado(bot1, bot2)
                bot1.treinar_com_historico()
                bot2.treinar_com_historico()

                # Registre os resultados
                vitorias_bot1 = bot1.vitorias
                derrotas_bot1 = bot1.derrotas
                empates_bot1 = bot1.empates

                if vitorias_bot1 > melhores_taxas['vitorias_max']:
                    melhores_taxas['learning_rate'] = learning_rate
                    melhores_taxas['epsilon'] = epsilon
                    melhores_taxas['vitorias_max'] = vitorias_bot1

                print(f"Resultado para learning_rate={learning_rate}, epsilon={epsilon}:")
                print(f"Vitórias de {bot1.nome}: {vitorias_bot1}")
                print(f"Derrotas de {bot1.nome}: {derrotas_bot1}")
                print(f"Empates de {bot1.nome}: {empates_bot1}")
                print("\n")

        return melhores_taxas

def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" | ".join(linha))
        print("-" * 9)

def verificar_vitoria(tabuleiro, jogador):
    # Verifica linhas
    for linha in tabuleiro:
        if all(c == jogador for c in linha):
            return True

    # Verifica colunas
    for coluna in range(3):
        if all(tabuleiro[linha][coluna] == jogador for linha in range(3)):
            return True

    # Verifica diagonais
    if all(tabuleiro[i][i] == jogador for i in range(3)) or all(tabuleiro[i][2 - i] == jogador for i in range(3)):
        return True

    return False

def gerar_combinacoes_jogos():
    movimentos = [(i + 1, j + 1) for i in range(3) for j in range(3)]
    return set(combinacao for combinacao in itertools.permutations(movimentos, 9))

def jogo_bot_aprendizado(bot1, bot2):
    combinacoes_jogos = gerar_combinacoes_jogos()
    vitorias_bot1 = 0
    vitorias_bot2 = 0
    sequencias_bot1 = []
    sequencias_bot2 = []
    vitorias_consecutivas_bot1 = 0
    vitorias_consecutivas_bot2 = 0
    jogo_atual = 0
    sequencia_jogo = []
    combinacoes_jogadas_bot1 = set()
    combinacoes_jogadas_bot2 = set()

    while combinacoes_jogos:
        combinacao_jogo = combinacoes_jogos.pop()
        tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
        movimentos = set(combinacao_jogo)
        jogo_ativo = True
        ultimo_estado = None

        while movimentos and jogo_ativo:
            jogador1 = bot1
            jogador2 = bot2

            #imprimir_tabuleiro(tabuleiro)

            # Movimentos do jogador1 (bot1)
            if jogador1 == bot1:
                estado = tuple(tuple(row) for row in tabuleiro)
                movimento = jogador1.escolher_movimento(tabuleiro, movimentos)
                ultimo_estado = estado

            linha, coluna = movimento
            if (linha, coluna) in movimentos:
                tabuleiro[linha - 1][coluna - 1] = jogador1.marca
                movimentos.remove((linha, coluna))

            if verificar_vitoria(tabuleiro, jogador1.marca):
                jogador1.atualizar_q_table(ultimo_estado, movimento, 1, None)
                jogador2.atualizar_q_table(ultimo_estado, movimento, -1, None)
                jogo_ativo = False
                jogador1.vitorias += 1
                vitorias_bot1 += 1
                vitorias_consecutivas_bot1 += 1
                sequencias_bot1.extend(sequencia_jogo)
                sequencia_jogo = []
                combinacoes_jogadas_bot1.add(combinacao_jogo)
                jogador2.derrotas += 1  # Adicione a contagem de derrotas ao jogador 2 sempre que o jogador 1 ganhar
                break

            if not movimentos or not jogo_ativo:
                jogador1.empates += 1
                break

            #imprimir_tabuleiro(tabuleiro)

            # Movimentos do jogador2 (bot2)
            if jogador2 == bot2:
                estado = tuple(tuple(row) for row in tabuleiro)
                movimento = jogador2.escolher_movimento(tabuleiro, movimentos)
                ultimo_estado = estado

            linha, coluna = movimento
            if (linha, coluna) in movimentos:
                tabuleiro[linha - 1][coluna - 1] = jogador2.marca
                movimentos.remove((linha, coluna))

            if verificar_vitoria(tabuleiro, jogador2.marca):
                jogador1.atualizar_q_table(ultimo_estado, movimento, -1, None)
                jogador2.atualizar_q_table(ultimo_estado, movimento, 1, None)
                jogo_ativo = False
                jogador2.vitorias += 1
                vitorias_bot2 += 1
                vitorias_consecutivas_bot2 += 1
                sequencias_bot2.extend(sequencia_jogo)
                sequencia_jogo = []
                combinacoes_jogadas_bot2.add(combinacao_jogo)
                jogador1.derrotas += 1  # Adicione a contagem de derrotas ao jogador 1 sempre que o jogador 2 ganhar
                break

            if not movimentos:
                jogador1.atualizar_q_table(ultimo_estado, movimento, 0, None)
                jogador2.atualizar_q_table(ultimo_estado, movimento, 0, None)
                jogador1.empates += 1

        jogo_atual += 1

    #imprimir_tabuleiro(tabuleiro)       # ESSA CHAMADA SE ABERTA PERMITE IMPRIMIR JOGO A JOGO DO TABULEIRO

    # Cálculo de vitórias em porcentagem
    total_jogos = jogo_atual
    porcentagem_vitorias_bot1 = (vitorias_bot1 / total_jogos) * 100
    porcentagem_vitorias_bot2 = (vitorias_bot2 / total_jogos) * 100

    # Sequência de jogo mais utilizada por cada bot ( aberturas de jogos )
    sequencia_mais_utilizada_bot1 = Counter(sequencias_bot1).most_common(1)
    sequencia_mais_utilizada_bot2 = Counter(sequencias_bot2).most_common(1)

    print(f"Placar: {bot1.nome} (Vitórias: {bot1.vitorias}, Derrotas: {bot1.derrotas}, Empates: {bot1.empates})")
    print(f"Placar: {bot2.nome} (Vitórias: {bot2.vitorias}, Derrotas: {bot2.derrotas}, Empates: {bot2.empates}")
    print(f"Combinacoes de jogos diferentes: {len(combinacoes_jogos)}")
    print(f"Porcentagem de vitórias de {bot1.nome}: {porcentagem_vitorias_bot1}%")
    print(f"Porcentagem de vitórias de {bot2.nome}: {porcentagem_vitorias_bot2}%")

    if sequencia_mais_utilizada_bot1:
        print(f"Sequência de jogo mais utilizada por {bot1.nome}: {sequencia_mais_utilizada_bot1[0][0]}")
    else:
        print(f"Não há sequências de jogo mais utilizadas por {bot1.nome}")

    if sequencia_mais_utilizada_bot2:
        print(f"Sequência de jogo mais utilizada por {bot2.nome}: {sequencia_mais_utilizada_bot2[0][0]}")
    else:
        print(f"Não há sequências de jogo mais utilizadas por {bot2.nome}")


if __name__ == "__main__":
    bot1 = Bot("BOT1", "X")
    bot2 = Bot("BOT2", "O")
    sessoes = 100  # Número de sessões de treinamento - LEMBRE DO WHILE

    # Inicia as sessões de treinamento
    bot1.iniciar_sessaos_treinamento(sessoes)

    total_jogos = 0  # Contador de número de jogos

    # Listas para armazenar os resultados
    vitorias_por_taxa = []
    derrotas_por_taxa = []
    empates_por_taxa = []

    while total_jogos < 100:  # while para número total de sessões de treino ( não confundir com número de jogos)
        # Treinamento dos bots
        jogo_bot_aprendizado(bot1, bot2)
        # Treino dos bots
        bot1.treinar_com_historico()
        bot2.treinar_com_historico()
        
        total_jogos += 1

        if total_jogos % 100 == 1:
            print(f"{total_jogos} jogos concluídos.")
            print(f"Melhores taxas encontradas:")
            print(f"Learning Rate: {bot1.learning_rate}")
            print(f"Epsilon: {bot1.epsilon}")

        # taxas de vitória, derrotas e empate
        porcentagem_vitorias_bot1 = (bot1.vitorias / total_jogos) * 100
        vitorias_por_taxa.append(porcentagem_vitorias_bot1)
        derrotas_por_taxa.append(100 - porcentagem_vitorias_bot1)
        empates_por_taxa.append((bot1.empates / total_jogos) * 100)

    # Plota Gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(vitorias_por_taxa, label='Vitórias', marker='o')
    plt.plot(derrotas_por_taxa, label='Derrotas', marker='x')
    plt.plot(empates_por_taxa, label='Empates', marker='s')
    plt.xlabel('Número de Jogos')
    plt.ylabel('Taxa (%)')
    plt.title('Impacto de Learning Rate e Epsilon nas Taxas de Vitória, Derrotas e Empates')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    
    # gráfico na tela
    plt.show()

    print("Treinamento concluído.")

