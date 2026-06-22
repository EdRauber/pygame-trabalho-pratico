"""Controle centralizado de áudio/música do jogo."""

import pygame

from src.config import VOLUME_MUSICA


def tocar_musica(caminho, repeticoes=-1, volume=VOLUME_MUSICA):
    """Carrega e toca uma música usando o volume padrão do projeto.

    Mantemos o volume em um único lugar para facilitar ajustes futuros.
    O volume padrão atual é 0.5, ou seja, metade do volume máximo.
    """
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(repeticoes)


def parar_musica():
    """Para a música atual."""
    pygame.mixer.music.stop()
