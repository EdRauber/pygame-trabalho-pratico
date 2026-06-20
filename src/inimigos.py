import random
import pygame

def gerar_inimigos(imagens_inimigos, n=3):
    """Gera uma lista de inimigos em posições aleatórias no mapa."""
    inimigos = []
    imagens_sorteadas = random.sample(imagens_inimigos, n)

    for i in range(n):
        x = random.randint(50, 700)
        y = random.randint(50, 500)
        inimigos.append({
            "rect": pygame.Rect(x, y, 120, 120),
            "imagem": imagens_sorteadas[i]
        })
    return inimigos


def reposicionar_inimigo(inimigo, inimigos, imagens_inimigos):
    """Move o inimigo para uma nova posição aleatória e troca a imagem após ser derrotado."""
    inimigo["rect"].x = random.randint(50, 700)
    inimigo["rect"].y = random.randint(50, 500)

    imagens_usadas = [
        i["imagens_inimigos"]
        for i in inimigos
        if i is not inimigo 
    ]

    imagens_disponiveis = [
        i["imagens_inimigos"]
        for i in imagens_inimigos
        if i is not imagens_usadas
    ]

    inimigo["imagem"] = random.choice(imagens_disponiveis)