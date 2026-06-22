import random
import pygame


def gerar_inimigos(imagens_inimigos, n=3):
    """Gera uma lista de inimigos em posicoes aleatorias no mapa."""
    inimigos = []
    imagens_sorteadas = random.sample(imagens_inimigos, min(n, len(imagens_inimigos)))

    for imagem in imagens_sorteadas:
        x = random.randint(50, 700)
        y = random.randint(50, 500)
        inimigos.append({
            "rect": pygame.Rect(x, y, 120, 120),
            "imagem": imagem
        })

    return inimigos


def reposicionar_inimigo(inimigo, inimigos, imagens_inimigos):
    """Move o inimigo para uma nova posicao aleatoria e troca sua imagem.

    O bug anterior estava aqui: os inimigos possuem a chave "imagem",
    mas o codigo tentava acessar "imagens_inimigos" dentro de cada inimigo.
    """
    inimigo["rect"].x = random.randint(50, 700)
    inimigo["rect"].y = random.randint(50, 500)

    imagens_usadas = [
        outro["imagem"]
        for outro in inimigos
        if outro is not inimigo
    ]

    imagens_disponiveis = [
        imagem
        for imagem in imagens_inimigos
        if imagem not in imagens_usadas
    ]

    if imagens_disponiveis:
        inimigo["imagem"] = random.choice(imagens_disponiveis)
    else:
        inimigo["imagem"] = random.choice(imagens_inimigos)
