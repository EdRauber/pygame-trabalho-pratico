import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    PRETO,
    BRANCO,
    AMARELO,
    CAMINHO_MUSICA_MAPA,
)
from src.mapa import executar_mapa

def executar_menu():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Menu")

    pygame.mixer.music.load(CAMINHO_MUSICA_MAPA)
    pygame.mixer.music.play(-1)

    f_titulo = pygame.font.SysFont(None, 64)
    f_botao = pygame.font.SysFont(None, 40)
    relogio = pygame.time.Clock()

    botao_rect = pygame.Rect(0, 0, 280, 55)
    botao_rect.center = (LARGURA_TELA // 2, ALTURA_TELA // 2)

    rodando = True
    
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        sobre_botao = botao_rect.collidepoint(mouse_pos)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if sobre_botao:
                    executar_mapa()
        tela.fill(PRETO)

        titulo = f_titulo.render(TITULO_JOGO, True, BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 150))

        cor_botao = AMARELO if sobre_botao else BRANCO
        pygame.draw.rect(tela, cor_botao, botao_rect)

        texto_botao = f_botao.render("INICIAR JOGO!", True, PRETO)
        tela.blit(texto_botao, (
            botao_rect.centerx - texto_botao.get_width() // 2,
            botao_rect.centery - texto_botao.get_height() // 2,
        ))

        pygame.display.flip()
        relogio.tick(FPS)
    pygame.quit()