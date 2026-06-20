import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    PRETO,
    BRANCO,
    CINZA,
)
from src.inimigos import gerar_inimigos, reposicionar_inimigo
from src.jogo import executar_jogo


def executar_mapa():
    """Executa o loop do mapa, onde o jogador clica em inimigos para duelar."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Mapa")


    """Carrega as imagens dos inimigos e redimensiona"""
    imagens_inimigos = [
    pygame.image.load("assets/imagens/inimigo1.png").convert_alpha(),
    pygame.image.load("assets/imagens/inimigo2.png").convert_alpha(),
    pygame.image.load("assets/imagens/inimigo3.png").convert_alpha(),
    pygame.image.load("assets/imagens/inimigo4.png").convert_alpha(),
    pygame.image.load("assets/imagens/inimigo5.png").convert_alpha(),
]
    for i in range(len(imagens_inimigos)):
        imagens_inimigos[i] = pygame.transform.scale(imagens_inimigos[i], (120, 120))


    f_inst = pygame.font.SysFont(None, 28)
    relogio = pygame.time.Clock()
    rodando = True

    inimigos = gerar_inimigos(imagens_inimigos)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for inimigo in inimigos:
                    if inimigo["rect"].collidepoint(evento.pos):
                        executar_jogo()
                        reposicionar_inimigo(inimigo, inimigos, imagens_inimigos)

        tela.fill((30, 30, 30))

        for inimigo in inimigos:
            tela.blit(inimigo["imagem"], inimigo["rect"])
            
        inst = f_inst.render("Clique em um inimigo para duelar", True, CINZA)
        tela.blit(inst, (LARGURA_TELA // 2 - inst.get_width() // 2, 560))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()