"""Funções de interface visual.

Este arquivo concentra telas e desenhos reutilizáveis: botões, ranking,
instruções, confirmação de voltar ao menu e entrada de nome.
"""

import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TAMANHO_DADO,
    PRETO,
    BRANCO,
    CINZA,
    AMARELO,
)
from src.regras import centralizar_dados

VERDE = (100, 220, 100)
VERMELHO = (220, 80, 80)
AZUL = (90, 160, 255)
LARANJA = (230, 150, 45)

NUM_PAGINAS_INSTRUCOES = 4


# ─────────────────────────────────────────────────────────────────────────────
# Botões do menu
# ─────────────────────────────────────────────────────────────────────────────

def criar_botao(texto, centro_y, largura=320, altura=48):
    """Cria um botão simples baseado em pygame.Rect."""
    rect = pygame.Rect(0, 0, largura, altura)
    rect.center = (LARGURA_TELA // 2, centro_y)
    return {"texto": texto, "rect": rect}


def desenhar_botao(tela, fonte, botao, mouse_pos):
    """Desenha o botão e retorna True se o mouse está sobre ele."""
    sobre = botao["rect"].collidepoint(mouse_pos)
    cor = AMARELO if sobre else BRANCO

    pygame.draw.rect(tela, cor, botao["rect"], border_radius=6)
    texto = fonte.render(botao["texto"], True, PRETO)
    tela.blit(texto, (
        botao["rect"].centerx - texto.get_width() // 2,
        botao["rect"].centery - texto.get_height() // 2,
    ))

    return sobre


# ─────────────────────────────────────────────────────────────────────────────
# Dados na tela
# ─────────────────────────────────────────────────────────────────────────────

def desenhar_dados(tela, fonte_dado, dados):
    """Desenha os dados e destaca os selecionados em amarelo."""
    centralizar_dados(dados)

    for d in dados:
        cor = AMARELO if d["selecionado"] else BRANCO
        pygame.draw.rect(tela, cor, d["rect"], border_radius=10)
        texto = fonte_dado.render(str(d["valor"]), True, PRETO)
        tela.blit(texto, (
            d["rect"].x + TAMANHO_DADO // 2 - texto.get_width() // 2,
            d["rect"].y + TAMANHO_DADO // 2 - texto.get_height() // 2,
        ))


# ─────────────────────────────────────────────────────────────────────────────
# Ranking e nome
# ─────────────────────────────────────────────────────────────────────────────

def desenhar_ranking(tela, fontes, ranking):
    """Desenha a tela de ranking sobre fundo escuro."""
    f_titulo, f_item, f_inst = fontes
    tela.fill(PRETO)

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
        medalhas = ["1.", "2.", "3.", "4.", "5."]

        for i, (nome, titulo_rank, pontos) in enumerate(ranking[:5]):
            cor = cores_pos[i]
            y = 140 + i * 55
            tela.blit(f_inst.render(medalhas[i], True, cor), (80, y + 8))
            tela.blit(f_item.render(nome[:14], True, cor), (140, y))
            tela.blit(f_item.render(titulo_rank, True, cor), (380, y))
            tela.blit(f_item.render(str(pontos), True, cor), (590, y))


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
                if evento.key == pygame.K_BACKSPACE:
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

        # Cursor piscando.
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = caixa.x + 10 + texto.get_width() + 2
            pygame.draw.line(tela, PRETO, (cursor_x, caixa.y + 8), (cursor_x, caixa.y + 42), 2)

        dica = f_inst.render("(max. 16 caracteres)", True, (150, 150, 150))
        tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, 375))

        pygame.display.flip()
        relogio.tick(FPS)


# ─────────────────────────────────────────────────────────────────────────────
# Confirmação de retorno ao menu
# ─────────────────────────────────────────────────────────────────────────────

def confirmar_voltar_menu(tela, f_medio, f_inst):
    """Pergunta se o jogador deseja voltar ao menu principal.

    ENTER confirma e reinicia o fluxo do jogo.
    ESC cancela e continua onde estava.
    """
    relogio = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return "sim"
                if evento.key == pygame.K_ESCAPE:
                    return "nao"

        tela.fill(PRETO)

        titulo = f_medio.render("Voltar ao menu principal?", True, BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 180))

        aviso = f_inst.render("Isso reinicia o mapa e a partida atual.", True, CINZA)
        tela.blit(aviso, (LARGURA_TELA // 2 - aviso.get_width() // 2, 245))

        opcao_sim = f_medio.render("ENTER: voltar ao menu", True, AMARELO)
        tela.blit(opcao_sim, (LARGURA_TELA // 2 - opcao_sim.get_width() // 2, 330))

        opcao_nao = f_medio.render("ESC: continuar", True, CINZA)
        tela.blit(opcao_nao, (LARGURA_TELA // 2 - opcao_nao.get_width() // 2, 380))

        pygame.display.flip()
        relogio.tick(FPS)


# ─────────────────────────────────────────────────────────────────────────────
# Instruções
# ─────────────────────────────────────────────────────────────────────────────

def _texto(tela, fonte, texto, x, y, cor=BRANCO):
    """Atalho para renderizar uma linha e retornar a próxima posição y."""
    surf = fonte.render(texto, True, cor)
    tela.blit(surf, (x, y))
    return y + surf.get_height() + 8


def _linhas(tela, fonte, linhas, x, y, cor_padrao=CINZA, espacamento=25):
    """Desenha uma sequência de linhas curtas.

    Use tuplas (texto, cor) para destacar uma linha específica.
    """
    for linha in linhas:
        if linha == "":
            y += espacamento // 2
            continue
        texto, cor = linha if isinstance(linha, tuple) else (linha, cor_padrao)
        surf = fonte.render(texto, True, cor)
        tela.blit(surf, (x, y))
        y += espacamento
    return y


def _cabecalho_instrucoes(tela, f_titulo, f_subtitulo, subtitulo, pagina):
    """Desenha o título fixo da tela de instruções."""
    titulo = f_titulo.render("INSTRUCOES", True, AMARELO)
    tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 18))

    sub = f_subtitulo.render(subtitulo, True, BRANCO)
    tela.blit(sub, (55, 75))

    pag = pygame.font.SysFont(None, 22).render(
        f"Pagina {pagina + 1}/{NUM_PAGINAS_INSTRUCOES}", True, CINZA
    )
    tela.blit(pag, (LARGURA_TELA - pag.get_width() - 35, 32))


def desenhar_instrucoes(tela, fontes, pagina=0):
    """Desenha as instruções em páginas separadas para evitar texto espremido."""
    f_titulo, f_subtitulo, f_texto, f_pequena = fontes
    tela.fill(PRETO)

    if pagina == 0:
        _cabecalho_instrucoes(tela, f_titulo, f_subtitulo, "Controles e objetivo", pagina)
        _linhas(tela, f_texto, [
            ("Objetivo", AMARELO),
            "Vence quem marcar 1500 pontos primeiro.",
            "No modo campanha, voce enfrenta a maquina.",
            "No multiplayer, dois jogadores se revezam localmente.",
            "",
            ("Menu", AMARELO),
            "Mouse: clicar nos botoes.",
            "ESC ou ENTER: voltar quando estiver no ranking.",
            "",
            ("Mapa", AMARELO),
            "W/A/S/D: movimentar o personagem.",
            "ENTER: iniciar duelo ao encostar em um inimigo.",
            "ESC: confirmar volta ao menu principal.",
        ], 60, 120, CINZA, 25)

    elif pagina == 1:
        _cabecalho_instrucoes(tela, f_titulo, f_subtitulo, "Como funciona um turno", pagina)
        _linhas(tela, f_texto, [
            "1. Cada turno comeca com 6 dados.",
            "2. O turno acaba quando voce guarda pontos ou rola 0 pontos.",
            "3. Quando pontua, voce escolhe quais dados usar no combo.",
            "4. Se continuar, rola apenas os dados que nao foram usados.",
            "5. Se usar todos os dados para pontuar, volta a rolar 6 dados.",
            "6. Se uma nova rolagem nao tiver pontuacao, perde os pontos da rodada.",
            "",
            ("Controles na batalha", AMARELO),
            "Mouse: selecionar ou desselecionar dados.",
            "1: continuar jogando com os dados restantes.",
            "2: guardar os pontos da rodada.",
            "ESC: confirmar volta ao menu principal.",
        ], 60, 120, CINZA, 25)

    elif pagina == 2:
        _cabecalho_instrucoes(tela, f_titulo, f_subtitulo, "Tabela de pontuacao", pagina)

        x_face, x_um, x_dois, x_tres = 85, 220, 370, 535
        y = 130
        cabecalhos = [
            ("Face", x_face),
            ("1 dado", x_um),
            ("2 dados", x_dois),
            ("3 dados", x_tres),
        ]
        for texto, x in cabecalhos:
            tela.blit(f_texto.render(texto, True, AMARELO), (x, y))
        y += 38

        tabela = [
            ("1", "100", "200", "1000"),
            ("2", "0", "0", "200"),
            ("3", "0", "0", "300"),
            ("4", "0", "0", "400"),
            ("5", "50", "100", "500"),
            ("6", "0", "0", "600"),
        ]
        for face, um, dois, tres in tabela:
            tela.blit(f_texto.render(face, True, BRANCO), (x_face + 12, y))
            tela.blit(f_texto.render(um, True, BRANCO), (x_um + 18, y))
            tela.blit(f_texto.render(dois, True, BRANCO), (x_dois + 18, y))
            tela.blit(f_texto.render(tres, True, BRANCO), (x_tres + 18, y))
            y += 35

        _linhas(tela, f_pequena, [
            ("Regra das repeticoes com 3+ dados", AMARELO),
            "A partir de 3 faces iguais, valor face x 100.",
            "Cada dado extra alem do terceiro dobra a pontuacao.",
            "Exemplo: 3 faces 2 = 200, 4 faces 2 = 400, 5 faces 2 = 800.",
        ], 60, 390, CINZA, 24)

    else:
        _cabecalho_instrucoes(tela, f_titulo, f_subtitulo, "Combinacoes especiais e exemplo", pagina)
        _linhas(tela, f_texto, [
            ("Combinacoes especiais", AMARELO),
            "1 | 2 | 3 | 4 | 5 | 6 = 1500 pontos",
            "1 | 2 | 3 | 4 | 5 = 750 pontos",
            "2 | 3 | 4 | 5 | 6 = 750 pontos",
            "",
            ("Exemplo de escolha", AMARELO),
            "Rolagem: 1 | 2 | 2 | 5 | 1 | 3",
            "O jogador pode escolher o que quer pontuar:",
            "- 50 pontos usando uma face 5",
            "- 100 pontos usando uma face 1",
            "- 150 pontos usando uma face 1 e uma face 5",
            "- 200 pontos usando duas faces 1",
            "- 250 pontos usando duas faces 1 e uma face 5",
        ], 60, 120, CINZA, 25)

    rodape = "ENTER: proxima pagina    ESC: voltar ao menu"
    pygame.draw.rect(tela, PRETO, (0, 552, LARGURA_TELA, 48))
    instrucao = f_pequena.render(rodape, True, CINZA)
    tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, 565))
