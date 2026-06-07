import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    PRETO,
    BRANCO,
    AMARELO,
    TAMANHO_DADO,
    ESPACO_DADO,
    X_INICIAL_DADOS,
    Y_INICIAL_DADOS,
)
from src.funcoes import rolar_dados


def executar_jogo():
    """Executa o loop principal do jogo com exibição e rolagem dos dados."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    fonte = pygame.font.SysFont(None, 48)
    relogio = pygame.time.Clock()
    rodando = True

    dados = rolar_dados(6)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    dados = rolar_dados(6)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for dado in dados:
                    if dado["rect"].collidepoint(evento.pos):
                        dado["selecionado"] = not dado["selecionado"]

                        
        tela.fill(PRETO)

        for i in range(2):
            for j in range(3):
                x = X_INICIAL_DADOS + j * (TAMANHO_DADO + ESPACO_DADO)
                y = Y_INICIAL_DADOS + i * (TAMANHO_DADO + ESPACO_DADO)
                dados[i*3+j]["rect"] = pygame.Rect(x, y, TAMANHO_DADO, TAMANHO_DADO)
                if dados[i*3+j]["selecionado"]:
                    pygame.draw.rect(tela, AMARELO, (x, y, TAMANHO_DADO, TAMANHO_DADO))
                else:
                    pygame.draw.rect(tela, BRANCO, (x, y, TAMANHO_DADO, TAMANHO_DADO))
                texto = fonte.render(f"{dados[i*3+j]['valor']}", True, PRETO)
                tela.blit(texto, (x, y))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()