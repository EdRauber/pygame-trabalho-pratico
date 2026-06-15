import random
import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    TAMANHO_DADO,
    ESPACO_DADO,
    PRETO,
    BRANCO,
    CINZA,
    AMARELO,
)

VERDE    = (100, 220, 100)
VERMELHO = (220, 80, 80)


def rolar_dados(quantidade):
    dados = []
    for _ in range(quantidade):
        dados.append({
            "valor": random.randint(1, 6),
            "selecionado": False
        })
    return dados


def tem_pontuacao(valores):
    """Retorna True se ao menos uma combinação pontuável existe nos valores rolados."""
    contagem = [0] * 7
    for v in valores:
        contagem[v] += 1
    if contagem[1] > 0 or contagem[5] > 0:
        return True
    for v in range(2, 7):
        if contagem[v] >= 3:
            return True
    return False


def titulo_por_pontuacao(pontuacao):
    """Retorna o título colonial conforme a pontuação acumulada."""
    if pontuacao >= 4000:
        return "Capitao-Geral"
    elif pontuacao >= 3000:
        return "Capitao"
    elif pontuacao >= 2000:
        return "Bandeirante"
    elif pontuacao >= 1500:
        return "Colono"
    else:
        return "Grumete"


def centralizar_dados(dados):
    """Calcula e atribui os rects dos dados, centralizados horizontalmente."""
    n = len(dados)
    total_w = n * TAMANHO_DADO + (n - 1) * ESPACO_DADO
    x0 = (LARGURA_TELA - total_w) // 2
    for i, d in enumerate(dados):
        d["rect"] = pygame.Rect(x0 + i * (TAMANHO_DADO + ESPACO_DADO), 220, TAMANHO_DADO, TAMANHO_DADO)


def desenhar_ranking(tela, fontes, ranking):
    """Desenha a tela de ranking sobre um fundo escuro."""
    f_titulo, f_item, f_inst = fontes
    tela.fill((0, 0, 0))

    titulo = f_titulo.render("RANKING DOS COLONIZADORES", True, AMARELO)
    tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 30))

    cab_cor = (180, 180, 180)
    tela.blit(f_inst.render("#", True, cab_cor), (80, 105))
    tela.blit(f_inst.render("NOME", True, cab_cor), (140, 105))
    tela.blit(f_inst.render("TITULO", True, cab_cor), (380, 105))
    tela.blit(f_inst.render("PONTOS", True, cab_cor), (590, 105))

    pygame.draw.line(tela, cab_cor, (70, 125), (700, 125), 1)

    if not ranking:
        s = f_item.render("Nenhuma pontuacao registrada ainda.", True, CINZA)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 250))
    else:
        cores_pos = [AMARELO, CINZA, (205, 127, 50), BRANCO, BRANCO]
        medalhas  = ["1.", "2.", "3.", "4.", "5."]

        for i, (nome, titulo_rank, pontos) in enumerate(ranking):
            cor = cores_pos[i]
            y   = 140 + i * 55

            tela.blit(f_inst.render(medalhas[i], True, cor), (80, y + 8))
            tela.blit(f_item.render(nome[:14], True, cor), (140, y))
            tela.blit(f_item.render(titulo_rank, True, cor), (380, y))
            tela.blit(f_item.render(str(pontos), True, cor), (590, y))

    instrucao = f_inst.render("Pressione qualquer tecla para jogar novamente", True, CINZA)
    tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, 540))


def pedir_nome(tela, f_medio, f_inst):
    """Tela de entrada de nome; retorna a string digitada."""
    nome = ""
    relogio = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return nome or "Jogador"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome.strip():
                    return nome.strip()
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif len(nome) < 16 and evento.unicode.isprintable():
                    nome += evento.unicode

        tela.fill(PRETO)
        titulo = f_medio.render("VOCE VENCEU!", True, VERDE)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 180))

        instrucao = f_inst.render("Digite seu nome e pressione ENTER:", True, CINZA)
        tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, 260))

        caixa = pygame.Rect(LARGURA_TELA // 2 - 160, 310, 320, 50)
        pygame.draw.rect(tela, BRANCO, caixa, border_radius=8)
        texto = f_medio.render(nome, True, PRETO)
        tela.blit(texto, (caixa.x + 10, caixa.y + 8))

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = caixa.x + 10 + texto.get_width() + 2
            pygame.draw.line(tela, PRETO, (cursor_x, caixa.y + 8), (cursor_x, caixa.y + 42), 2)

        dica = f_inst.render("(max. 16 caracteres)", True, (150, 150, 150))
        tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, 375))

        pygame.display.flip()
        relogio.tick(60)


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