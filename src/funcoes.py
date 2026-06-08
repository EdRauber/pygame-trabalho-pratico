import random


def rolar_dados(quantidade):
    dados = []
    for _ in range(quantidade):
        dados.append({
            "valor": random.randint(1, 6),
            "selecionado": False
        })
    return dados


def tem_pontuacao(valores):
    """Retorna True se ao menos uma combinação pontuável existe nos valores rolados.
    Usado para detectar derrota: se retornar False, o jogador perdeu a rodada.
    """
    contagem = [0] * 7          # índice 1–6
    for v in valores:
        contagem[v] += 1
    if contagem[1] > 0 or contagem[5] > 0:   # 1s e 5s sempre pontuam
        return True
    for v in range(2, 7):                     # qualquer trinca pontua
        if contagem[v] >= 3:
            return True
    return False


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