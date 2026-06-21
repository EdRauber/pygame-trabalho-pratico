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


def _suavizar_saida(t):
    return 1 - (1 - t) ** 3


def transicao_batalha(tela, imagem_player, imagem_inimigo, duracao_ms=1800):
    # Mapa de tempos de cada fase (ms) — total 1800ms:
    #   0    – 200  : barras
    #   120  – 380  : exclamação piscando
    #   200  – 550  : sprites entram com zoom
    #   550  – 750  : VS aparece
    #   730         : snapshot tirado
    #   750  – 900  : flash branco
    #   900  – 1100 : linha vermelha atravessa a tela
    #   1100 – 1800 : tela se parte (fatias sobem/descem) → encerra direto
    T_FLASH_INI   = 750
    T_FLASH_FIM   = 900
    T_LINHA_INI   = 900
    T_LINHA_FIM   = 1100
    T_CORTE_INI   = 1100
    T_CORTE_FIM   = 1800

    relogio  = pygame.time.Clock()
    inicio   = pygame.time.get_ticks()
    W, H     = LARGURA_TELA, ALTURA_TELA
    CX, CY   = W // 2, H // 2
    SPRITE_BASE = 160

    img_player  = pygame.transform.scale(imagem_player,  (SPRITE_BASE, SPRITE_BASE))
    img_inimigo = pygame.transform.scale(imagem_inimigo, (SPRITE_BASE, SPRITE_BASE))

    flash_surf = pygame.Surface((W, H))
    flash_surf.fill((255, 255, 255))

    snapshot = None

    while True:
        agora     = pygame.time.get_ticks()
        elapsed   = agora - inicio
        progresso = min(elapsed / duracao_ms, 1.0)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        tela.fill((0, 0, 0))

        # Fase 1 — Barras (0–200ms)
        ALTURA_BARRA = 90
        t1  = min(elapsed / 200, 1.0)
        t1e = _suavizar_saida(t1)
        barra_y = int(t1e * ALTURA_BARRA)
        pygame.draw.rect(tela, (0, 0, 0), (0, 0, W, barra_y))
        pygame.draw.rect(tela, (0, 0, 0), (0, H - barra_y, W, barra_y))

        # Fase 1.5 — Exclamação piscando (120–380ms)
        if 120 <= elapsed < 380:
            t_ex = (elapsed - 120) / 65
            if int(t_ex) % 2 == 0:
                f_ex = pygame.font.SysFont(None, 120)
                ex_surf = f_ex.render("!", True, (220, 40, 40))
                tela.blit(ex_surf, (CX - ex_surf.get_width() // 2, CY - ex_surf.get_height() // 2))

        # Fase 2 — Sprites entram com zoom (200–550ms)
        if elapsed >= 200:
            t2  = min((elapsed - 200) / 350, 1.0)
            t2e = _suavizar_saida(t2)
            sprite_y  = CY - SPRITE_BASE // 2
            player_x  = int((-SPRITE_BASE - 60) + (CX - SPRITE_BASE - 40 - (-SPRITE_BASE - 60)) * t2e)
            inimigo_x = int((W + 60) + (CX + 40 - (W + 60)) * t2e)
            zoom      = 0.4 + 0.6 * t2e
            tam_atual = int(SPRITE_BASE * zoom)
            if tam_atual > 0:
                sp = pygame.transform.scale(img_player,  (tam_atual, tam_atual))
                si = pygame.transform.scale(img_inimigo, (tam_atual, tam_atual))
                offset_y = (SPRITE_BASE - tam_atual) // 2
                tela.blit(sp, (player_x,  sprite_y + offset_y))
                tela.blit(si, (inimigo_x, sprite_y + offset_y))

        # Fase 3 — VS aparece (550–750ms)
        if elapsed >= 550:
            t3     = min((elapsed - 550) / 200, 1.0)
            tam_vs = int(120 * _suavizar_saida(t3))
            if tam_vs > 10:
                f_vs    = pygame.font.SysFont(None, tam_vs)
                vs_surf = f_vs.render("VS", True, (230, 180, 40))
                tela.blit(vs_surf, (CX - vs_surf.get_width() // 2, CY - vs_surf.get_height() // 2))

        # Snapshot tirado depois de sprites e VS estarem na tela, antes do flash
        if T_FLASH_INI <= elapsed and snapshot is None:
            snapshot = tela.copy()

        # Fase 4 — Flash branco (1100–1300ms)
        if T_FLASH_INI <= elapsed < T_FLASH_FIM:
            t4 = (elapsed - T_FLASH_INI) / (T_FLASH_FIM - T_FLASH_INI)
            alpha_flash = int((t4 if t4 <= 0.5 else 1.0 - t4) / 0.5 * 255)
            flash_surf.set_alpha(max(0, min(255, alpha_flash)))
            tela.blit(flash_surf, (0, 0))

        if T_LINHA_INI <= elapsed < T_LINHA_FIM:
            t_a = (elapsed - T_LINHA_INI) / (T_LINHA_FIM - T_LINHA_INI)
            largura_linha = int(_suavizar_saida(t_a) * W)
            pygame.draw.rect(tela, (220, 40, 40), (W - largura_linha, CY - 3, largura_linha, 6))

        if elapsed >= T_CORTE_INI and snapshot is not None:
            t_b = min((elapsed - T_CORTE_INI) / (T_CORTE_FIM - T_CORTE_INI), 1.0)
            deslocamento = int(_suavizar_saida(t_b) * H)

            tela.fill((0, 0, 0))

            fatia_cima = snapshot.subsurface(pygame.Rect(0, 0, W, CY)).copy()
            tela.blit(fatia_cima, (0, -deslocamento))

            fatia_baixo = snapshot.subsurface(pygame.Rect(0, CY, W, H - CY)).copy()
            tela.blit(fatia_baixo, (0, CY + deslocamento))

            y_linha_cima  = CY - deslocamento - 3
            y_linha_baixo = CY + deslocamento
            if y_linha_cima + 6 >= 0:
                pygame.draw.rect(tela, (220, 40, 40), (0, y_linha_cima, W, 6))
            if y_linha_baixo <= H:
                pygame.draw.rect(tela, (220, 40, 40), (0, y_linha_baixo, W, 6))

        pygame.display.flip()
        relogio.tick(60)

        if progresso >= 1.0:
            break