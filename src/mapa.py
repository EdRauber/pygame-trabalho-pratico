import pygame
from src.inimigos import gerar_inimigos
from src.jogo import executar_jogo

def executar_mapa():
    pygame.init()
    
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mapa")
    
    relogio = pygame.time.Clock()
    rodando = True

    inimigos = gerar_inimigos()
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for inimigo in inimigos:
                    if inimigo["rect"].collidepoint(evento.pos):
                        executar_jogo()
                        inimigo["rect"].x = random.randint(50, 700)
                        inimigo["rect"].y = random.randint(50, 500)
        
        tela.fill((30, 30, 30))  # fundo cinza escuro provisório
        for inimigo in inimigos:
            pygame.draw.rect(tela, inimigo["cor"], inimigo["rect"], border_radius = 8)
        
        pygame.display.flip()
        relogio.tick(60)
    
    pygame.quit()