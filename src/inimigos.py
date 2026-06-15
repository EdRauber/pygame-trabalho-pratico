import random
import pygame


def gerar_inimigos(n=3):
    """Gera uma lista de inimigos em posições aleatórias no mapa."""
    inimigos = []
    for _ in range(n):
        x = random.randint(50, 700)
        y = random.randint(50, 500)
        inimigos.append({
            "rect": pygame.Rect(x, y, 60, 60),
            "cor": (220, 80, 80)
        })
    return inimigos


def reposicionar_inimigo(inimigo):
    """Move o inimigo para uma nova posição aleatória após ser derrotado."""
    inimigo["rect"].x = random.randint(50, 700)
    inimigo["rect"].y = random.randint(50, 500)