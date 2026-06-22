"""Regras e pequenas funções de lógica do jogo.

Este arquivo fica sem telas grandes ou loops principais. A ideia é deixar aqui
funções puras ou quase puras: rolar dados, verificar pontuação, calcular títulos,
posicionar dados etc.
"""

import random
import pygame

from src.config import (
    LARGURA_TELA,
    TAMANHO_DADO,
    ESPACO_DADO,
)


# ─────────────────────────────────────────────────────────────────────────────
# Dados
# ─────────────────────────────────────────────────────────────────────────────

def rolar_dados(quantidade):
    """Cria uma lista de dados.

    Cada dado é um dicionário com:
      - valor: número sorteado de 1 a 6
      - selecionado: se o jogador clicou nele ou não

    O rect é criado depois por centralizar_dados(), porque depende da tela.
    """
    dados = []
    for _ in range(quantidade):
        dados.append({
            "valor": random.randint(1, 6),
            "selecionado": False,
        })
    return dados


def tem_pontuacao(valores):
    """Retorna True se a rolagem tem pelo menos uma pontuação possível.

    Pontua se houver:
      - pelo menos um 1;
      - pelo menos um 5;
      - três ou mais números iguais de qualquer face 2 a 6.
    """
    contagem = [0] * 7
    for v in valores:
        contagem[v] += 1

    if contagem[1] > 0 or contagem[5] > 0:
        return True

    for face in range(2, 7):
        if contagem[face] >= 3:
            return True

    return False


def centralizar_dados(dados):
    """Cria/atualiza o Rect de cada dado centralizando a fileira na tela."""
    n = len(dados)
    total_w = n * TAMANHO_DADO + (n - 1) * ESPACO_DADO
    x0 = (LARGURA_TELA - total_w) // 2

    for i, d in enumerate(dados):
        d["rect"] = pygame.Rect(
            x0 + i * (TAMANHO_DADO + ESPACO_DADO),
            220,
            TAMANHO_DADO,
            TAMANHO_DADO,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Pontuação/ranking
# ─────────────────────────────────────────────────────────────────────────────

def titulo_por_pontuacao(pontuacao):
    """Retorna o título colonial conforme a pontuação acumulada."""
    if pontuacao >= 4000:
        return "Capitao-Geral"
    if pontuacao >= 3000:
        return "Capitao"
    if pontuacao >= 2000:
        return "Bandeirante"
    if pontuacao >= 1500:
        return "Colono"
    return "Grumete"


def pontos_para_entrar_no_ranking(pontuacao, ranking, limite=5):
    """Retorna quanto faltou para entrar no ranking.

    Se retornar 0, a pontuação entra no Top 5.
    Se retornar mais que 0, esse é o valor que faltou.
    """
    ranking_ordenado = sorted(ranking, key=lambda entrada: entrada[2], reverse=True)

    # Se ainda não há 5 entradas, qualquer vitória entra no ranking.
    if len(ranking_ordenado) < limite:
        return 0

    menor_pontuacao_top = ranking_ordenado[limite - 1][2]

    # Precisa superar o 5º colocado, por isso +1 quando empata ou fica abaixo.
    if pontuacao > menor_pontuacao_top:
        return 0

    return menor_pontuacao_top - pontuacao + 1


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades simples
# ─────────────────────────────────────────────────────────────────────────────

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)
