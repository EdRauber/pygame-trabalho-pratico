import random
import pygame

def gerar_inimigos(n=3):
    inimigos = []
    for inimigo in range(n):
        x = random.randint(50, 700)
        y = random.randint(50, 700)
        inimigos.append({
            "rect": pygame.Rect(x, y, 60, 60),
            "cor": (220, 80, 80)
        })
    return inimigos