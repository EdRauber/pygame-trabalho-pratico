"""Menu principal do jogo.

Fluxo deste arquivo:
  1. mostra os botões principais;
  2. chama o mapa, o multiplayer, o ranking ou as instruções;
  3. quando algum modo retorna ao menu, a música do mapa/menu volta a tocar.
"""

import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    PRETO,
    BRANCO,
    CINZA,
    CAMINHO_MUSICA_MAPA,
    CAMINHO_RANKING,
)
from src.mapa import executar_mapa
from src.jogo_multiplayer import executar_multiplayer
from src.dados import carregar_ranking
from src.audio import tocar_musica
from src.ui import (
    NUM_PAGINAS_INSTRUCOES,
    criar_botao,
    desenhar_botao,
    desenhar_ranking,
    desenhar_instrucoes,
)


def tocar_musica_menu():
    """Garante que a música do menu/mapa esteja tocando com volume reduzido."""
    tocar_musica(CAMINHO_MUSICA_MAPA)


def executar_menu():
    """Loop principal do menu."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Menu")
    tocar_musica_menu()

    # Fontes usadas pelo menu e telas internas.
    f_titulo = pygame.font.SysFont(None, 64)
    f_botao = pygame.font.SysFont(None, 36)
    f_ranking_titulo = pygame.font.SysFont(None, 42)
    f_ranking_item = pygame.font.SysFont(None, 36)
    f_inst = pygame.font.SysFont(None, 24)
    f_instr_titulo = pygame.font.SysFont(None, 48)
    f_instr_subtitulo = pygame.font.SysFont(None, 34)
    f_instr_texto = pygame.font.SysFont(None, 26)
    f_instr_pequena = pygame.font.SysFont(None, 22)

    relogio = pygame.time.Clock()

    # Botões do menu principal.
    botoes = [
        ("jogar", criar_botao("INICIAR JOGO", ALTURA_TELA // 2 - 120)),
        ("multiplayer", criar_botao("MULTIPLAYER", ALTURA_TELA // 2 - 60)),
        ("ranking", criar_botao("VER RANKING", ALTURA_TELA // 2)),
        ("instrucoes", criar_botao("INSTRUCOES", ALTURA_TELA // 2 + 60)),
    ]

    estado = "menu"
    pagina_instrucoes = 0
    rodando = True

    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        botoes_hover = {nome: botao["rect"].collidepoint(mouse_pos) for nome, botao in botoes}

        # ── Entrada/eventos ────────────────────────────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif estado == "ranking" and evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    estado = "menu"

            elif estado == "instrucoes" and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = "menu"
                elif evento.key == pygame.K_RETURN:
                    pagina_instrucoes = (pagina_instrucoes + 1) % NUM_PAGINAS_INSTRUCOES

            elif estado == "menu" and evento.type == pygame.MOUSEBUTTONDOWN:
                if botoes_hover["jogar"]:
                    resultado = executar_mapa()
                    pygame.display.set_caption("Menu")
                    if resultado == "sair":
                        rodando = False
                    else:
                        tocar_musica_menu()

                elif botoes_hover["multiplayer"]:
                    resultado = executar_multiplayer(tela)
                    pygame.display.set_caption("Menu")
                    if resultado == "sair":
                        rodando = False
                    else:
                        tocar_musica_menu()

                elif botoes_hover["ranking"]:
                    estado = "ranking"

                elif botoes_hover["instrucoes"]:
                    pagina_instrucoes = 0
                    estado = "instrucoes"

        # ── Renderização das telas internas ────────────────────────────────
        if estado == "ranking":
            ranking = carregar_ranking(CAMINHO_RANKING)
            desenhar_ranking(tela, (f_ranking_titulo, f_ranking_item, f_inst), ranking)

            instrucao = f_inst.render("ENTER ou ESC: voltar ao menu", True, CINZA)
            tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, 540))

            pygame.display.flip()
            relogio.tick(FPS)
            continue

        if estado == "instrucoes":
            desenhar_instrucoes(
                tela,
                (f_instr_titulo, f_instr_subtitulo, f_instr_texto, f_instr_pequena),
                pagina_instrucoes,
            )
            pygame.display.flip()
            relogio.tick(FPS)
            continue

        # ── Renderização do menu principal ─────────────────────────────────
        tela.fill(PRETO)

        titulo = f_titulo.render(TITULO_JOGO, True, BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 75))

        for _, botao in botoes:
            desenhar_botao(tela, f_botao, botao, mouse_pos)

        dica = f_inst.render("ESC durante o jogo abre a confirmacao para voltar ao menu", True, CINZA)
        tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, 535))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
