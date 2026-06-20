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

    largura_player = 120
    altura_player = 120

    sprites_player = {
        "parado_baixo": pygame.transform.scale(
            pygame.image.load("assets/imagens/player_frente_1.png").convert_alpha(),(largura_player, altura_player)
        ),
        "parado_cima": pygame.transform.scale(
            pygame.image.load("assets/imagens/player_costas_1.png").convert_alpha(),(largura_player, altura_player)
        ),
        "parado_direita": pygame.transform.scale(
            pygame.image.load("assets/imagens/player_direita_1.png").convert_alpha(),(largura_player, altura_player)
        ),
        "parado_esquerda": pygame.transform.scale(
            pygame.image.load("assets/imagens/player_esquerda_1.png").convert_alpha(),(largura_player, altura_player)
        ),

        "andando_baixo": [
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_frente_2.png").convert_alpha(),(largura_player, altura_player)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_frente_3.png").convert_alpha(),(largura_player, altura_player)
            ),
        ],
        "andando_cima": [
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_costas_2.png").convert_alpha(),(largura_player, altura_player)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_costas_3.png").convert_alpha(),(largura_player, altura_player)
            ),
        ],
        "andando_direita": [
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_direita_2.png").convert_alpha(),(largura_player, altura_player)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_direita_3.png").convert_alpha(),(largura_player, altura_player)
            ),
        ],
        "andando_esquerda": [
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_esquerda_2.png").convert_alpha(),(largura_player, altura_player)
            ),
            pygame.transform.scale(
                pygame.image.load("assets/imagens/player_esquerda_3.png").convert_alpha(),(largura_player, altura_player)
            ),
        ]
    }

    player = {"rect": pygame.Rect(0, 0, largura_player, altura_player)}
    player["rect"].midbottom = (LARGURA_TELA//2, ALTURA_TELA - 20)
    velocidade = 5
    direcao = "baixo"
    frame = 0
    contador_movimento = 0
    imagem_player = sprites_player["parado_baixo"]

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and inimigo_proximo:
                    executar_jogo()
                    reposicionar_inimigo(inimigo, inimigos, imagens_inimigos)

        """Movimenta o player no espaço da tela"""
        teclas = pygame.key.get_pressed()
        movendo = False

        if teclas[pygame.K_w]:
            player["rect"].y -= velocidade
            direcao = "cima"
            movendo = True
        if teclas[pygame.K_s]:
            player["rect"].y += velocidade
            direcao = "baixo"
            movendo = True
        if teclas[pygame.K_a]:
            player["rect"].x -= velocidade
            direcao = "esquerda"
            movendo = True
        if teclas[pygame.K_d]:
            player["rect"].x += velocidade
            direcao = "direita"
            movendo = True

        if movendo:
            contador_movimento += 1
            if contador_movimento >= 10:
                contador_movimento = 0
                frame = (frame + 1)%2
                
                if direcao == "baixo":
                    imagem_player = sprites_player["andando_baixo"][frame]
                if direcao == "cima":
                    imagem_player = sprites_player["andando_cima"][frame]
                if direcao == "direita":
                    imagem_player = sprites_player["andando_direita"][frame]
                if direcao == "esquerda":
                    imagem_player = sprites_player["andando_esquerda"][frame]
        else:
            if direcao == "baixo":
                imagem_player = sprites_player["parado_baixo"]
            if direcao == "cima":
                imagem_player = sprites_player["parado_cima"]
            if direcao == "direita":
                imagem_player = sprites_player["parado_direita"]
            if direcao == "esquerda":
                imagem_player = sprites_player["parado_esquerda"]

        player["rect"].x = max(0, min(player["rect"].x, LARGURA_TELA - largura_player))
        player["rect"].y = max(0, min(player["rect"].y, ALTURA_TELA - altura_player))

        """Detecta colisão do player com algum inimigo"""
        inimigo_proximo = None
        for inimigo in inimigos:
            if player["rect"].colliderect(inimigo["rect"]):
                inimigo_proximo = inimigo
                break

        tela.fill((30, 30, 30))

        for inimigo in inimigos:
            tela.blit(inimigo["imagem"], inimigo["rect"])

        tela.blit(imagem_player, player["rect"])

        """Exibe mensagem na tela quando puder iniciar a batalha"""
        if inimigo_proximo:
            inst = f_inst.render("Pressione ENTER para duelar", True, CINZA)
            tela.blit(inst, (LARGURA_TELA // 2 - inst.get_width() // 2, 560))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()