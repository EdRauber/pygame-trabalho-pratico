"""Animações de transição entre telas."""

import pygame

from src.config import LARGURA_TELA, ALTURA_TELA


def _suavizar_saida(t):
    """Curva simples para animações começarem rápidas e terminarem suaves."""
    return 1 - (1 - t) ** 3


def transicao_batalha(tela, imagem_player, imagem_inimigo, duracao_ms=1800):
    """Animação de entrada para a batalha."""
    T_FLASH_INI = 750
    T_FLASH_FIM = 900
    T_LINHA_INI = 900
    T_LINHA_FIM = 1100
    T_CORTE_INI = 1100
    T_CORTE_FIM = 1800

    relogio = pygame.time.Clock()
    inicio = pygame.time.get_ticks()
    W, H = LARGURA_TELA, ALTURA_TELA
    CX, CY = W // 2, H // 2
    SPRITE_BASE = 160

    img_player = pygame.transform.scale(imagem_player, (SPRITE_BASE, SPRITE_BASE))
    img_inimigo = pygame.transform.scale(imagem_inimigo, (SPRITE_BASE, SPRITE_BASE))

    flash_surf = pygame.Surface((W, H))
    flash_surf.fill((255, 255, 255))

    snapshot = None

    while True:
        agora = pygame.time.get_ticks()
        elapsed = agora - inicio
        progresso = min(elapsed / duracao_ms, 1.0)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        tela.fill((0, 0, 0))

        # Fase 1: barras pretas entrando.
        ALTURA_BARRA = 90
        t1 = min(elapsed / 200, 1.0)
        barra_y = int(_suavizar_saida(t1) * ALTURA_BARRA)
        pygame.draw.rect(tela, (0, 0, 0), (0, 0, W, barra_y))
        pygame.draw.rect(tela, (0, 0, 0), (0, H - barra_y, W, barra_y))

        # Fase 2: exclamação piscando.
        if 120 <= elapsed < 380:
            t_ex = (elapsed - 120) / 65
            if int(t_ex) % 2 == 0:
                f_ex = pygame.font.SysFont(None, 120)
                ex_surf = f_ex.render("!", True, (220, 40, 40))
                tela.blit(ex_surf, (CX - ex_surf.get_width() // 2, CY - ex_surf.get_height() // 2))

        # Fase 3: sprites entram com zoom.
        if elapsed >= 200:
            t2 = min((elapsed - 200) / 350, 1.0)
            t2e = _suavizar_saida(t2)
            sprite_y = CY - SPRITE_BASE // 2
            player_x = int((-SPRITE_BASE - 60) + (CX - SPRITE_BASE - 40 - (-SPRITE_BASE - 60)) * t2e)
            inimigo_x = int((W + 60) + (CX + 40 - (W + 60)) * t2e)
            zoom = 0.4 + 0.6 * t2e
            tam_atual = int(SPRITE_BASE * zoom)

            if tam_atual > 0:
                sp = pygame.transform.scale(img_player, (tam_atual, tam_atual))
                si = pygame.transform.scale(img_inimigo, (tam_atual, tam_atual))
                offset_y = (SPRITE_BASE - tam_atual) // 2
                tela.blit(sp, (player_x, sprite_y + offset_y))
                tela.blit(si, (inimigo_x, sprite_y + offset_y))

        # Fase 4: VS aparece.
        if elapsed >= 550:
            t3 = min((elapsed - 550) / 200, 1.0)
            tam_vs = int(120 * _suavizar_saida(t3))
            if tam_vs > 10:
                f_vs = pygame.font.SysFont(None, tam_vs)
                vs_surf = f_vs.render("VS", True, (230, 180, 40))
                tela.blit(vs_surf, (CX - vs_surf.get_width() // 2, CY - vs_surf.get_height() // 2))

        if T_FLASH_INI <= elapsed and snapshot is None:
            snapshot = tela.copy()

        # Flash branco.
        if T_FLASH_INI <= elapsed < T_FLASH_FIM:
            t4 = (elapsed - T_FLASH_INI) / (T_FLASH_FIM - T_FLASH_INI)
            alpha_flash = int((t4 if t4 <= 0.5 else 1.0 - t4) / 0.5 * 255)
            flash_surf.set_alpha(max(0, min(255, alpha_flash)))
            tela.blit(flash_surf, (0, 0))

        # Linha vermelha corta a tela.
        if T_LINHA_INI <= elapsed < T_LINHA_FIM:
            t_a = (elapsed - T_LINHA_INI) / (T_LINHA_FIM - T_LINHA_INI)
            largura_linha = int(_suavizar_saida(t_a) * W)
            pygame.draw.rect(tela, (220, 40, 40), (W - largura_linha, CY - 3, largura_linha, 6))

        # Tela se parte em duas fatias.
        if elapsed >= T_CORTE_INI and snapshot is not None:
            t_b = min((elapsed - T_CORTE_INI) / (T_CORTE_FIM - T_CORTE_INI), 1.0)
            deslocamento = int(_suavizar_saida(t_b) * H)
            tela.fill((0, 0, 0))

            fatia_cima = snapshot.subsurface(pygame.Rect(0, 0, W, CY)).copy()
            tela.blit(fatia_cima, (0, -deslocamento))

            fatia_baixo = snapshot.subsurface(pygame.Rect(0, CY, W, H - CY)).copy()
            tela.blit(fatia_baixo, (0, CY + deslocamento))

            y_linha_cima = CY - deslocamento - 3
            y_linha_baixo = CY + deslocamento
            if y_linha_cima + 6 >= 0:
                pygame.draw.rect(tela, (220, 40, 40), (0, y_linha_cima, W, 6))
            if y_linha_baixo <= H:
                pygame.draw.rect(tela, (220, 40, 40), (0, y_linha_baixo, W, 6))

        pygame.display.flip()
        relogio.tick(60)

        if progresso >= 1.0:
            break
