"""Compatibilidade com versões antigas do projeto.

O código foi modularizado em arquivos menores:
  - regras.py: lógica dos dados, pontuação e utilidades;
  - ui.py: telas, botões, ranking, instruções e confirmação;
  - transicoes.py: animações.

Mantemos este arquivo reexportando as funções antigas para evitar quebrar imports
que ainda usam `from src.funcoes import ...`.
"""

from src.regras import *  
from src.ui import *  
from src.transicoes import *  
