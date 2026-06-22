"""Testes automatizados da lógica do jogo Portugeses.

Organização dos testes:
- Casos normais: situações esperadas do jogo.
- Casos de borda: limites, empates, listas vazias e valores nos extremos.
- Casos de domínio: regras específicas do jogo de dados, ranking e inimigos.

Para executar a partir da raiz do projeto:
    pytest tests/test_logica.py

Ou, se este arquivo estiver na raiz:
    pytest test_logica.py
"""

import os

# Ajuda o Pygame a rodar em ambientes sem janela gráfica, como CI/pytest.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from src.combinacoes import definir_combinacoes
from src.dados import carregar_ranking, salvar_ranking
from src.inimigos import gerar_inimigos, reposicionar_inimigo
from src.regras import (
    centralizar_dados,
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    pontos_para_entrar_no_ranking,
    rolar_dados,
    tem_pontuacao,
    titulo_por_pontuacao,
    verificar_colisao,
)


# ─────────────────────────────────────────────────────────────────────────────
# Casos normais: utilidades básicas
# ─────────────────────────────────────────────────────────────────────────────


def test_calcular_pontos_soma_corretamente():
    """Caso normal: deve somar os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Caso de borda: zero vidas já significa derrota."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas_positivas():
    """Caso normal: vidas positivas indicam que o jogador continua vivo."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Caso de borda: valor menor que o mínimo deve ser travado no mínimo."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Caso de borda: valor maior que o máximo deve ser travado no máximo."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Caso normal: valor dentro do intervalo deve ser mantido."""
    assert limitar_valor(50, 0, 100) == 50


def test_verificar_colisao_entre_rects():
    """Caso normal: rects sobrepostos devem indicar colisão."""
    r1 = pygame.Rect(0, 0, 50, 50)
    r2 = pygame.Rect(25, 25, 50, 50)
    assert verificar_colisao(r1, r2) is True


def test_verificar_ausencia_de_colisao_entre_rects():
    """Caso de borda: rects separados não devem indicar colisão."""
    r1 = pygame.Rect(0, 0, 50, 50)
    r2 = pygame.Rect(100, 100, 50, 50)
    assert verificar_colisao(r1, r2) is False


# ─────────────────────────────────────────────────────────────────────────────
# Casos de domínio: regras de pontuação dos dados
# ─────────────────────────────────────────────────────────────────────────────


def test_pontuacao_faces_individuais_1_e_5():
    """Domínio: face 1 sozinha vale 100 e face 5 sozinha vale 50."""
    assert definir_combinacoes([1]) == 100
    assert definir_combinacoes([5]) == 50
    assert definir_combinacoes([1, 5]) == 150


def test_pontuacao_duas_faces_1_e_duas_faces_5():
    """Domínio: duas faces 1 valem 200 e duas faces 5 valem 100."""
    assert definir_combinacoes([1, 1]) == 200
    assert definir_combinacoes([5, 5]) == 100


def test_pontuacao_trincas_basicas():
    """Domínio: três faces iguais seguem a tabela de pontos."""
    assert definir_combinacoes([1, 1, 1]) == 1000
    assert definir_combinacoes([2, 2, 2]) == 200
    assert definir_combinacoes([3, 3, 3]) == 300
    assert definir_combinacoes([4, 4, 4]) == 400
    assert definir_combinacoes([5, 5, 5]) == 500
    assert definir_combinacoes([6, 6, 6]) == 600


def test_pontuacao_dobra_a_partir_do_quarto_dado_igual():
    """Domínio: cada dado extra além do terceiro dobra a pontuação da trinca."""
    assert definir_combinacoes([2, 2, 2, 2]) == 400
    assert definir_combinacoes([2, 2, 2, 2, 2]) == 800
    assert definir_combinacoes([6, 6, 6, 6]) == 1200
    assert definir_combinacoes([6, 6, 6, 6, 6]) == 2400


def test_combinacoes_especiais_de_sequencia():
    """Domínio: sequências especiais devem ter pontuação fixa."""
    assert definir_combinacoes([1, 2, 3, 4, 5, 6]) == 1500
    assert definir_combinacoes([1, 2, 3, 4, 5]) == 750
    assert definir_combinacoes([2, 3, 4, 5, 6]) == 750


def test_combinacoes_especiais_com_repeticao_de_1_ou_5():
    """Domínio: sequências com repetição de 1 ou 5 têm pontuação própria."""
    assert definir_combinacoes([1, 1, 2, 3, 4, 5]) == 850
    assert definir_combinacoes([2, 3, 4, 5, 5, 6]) == 800


def test_combinacao_invalida_nao_pontua():
    """Domínio: faces 2, 3, 4 e 6 sozinhas ou em dupla não pontuam."""
    assert definir_combinacoes([2]) == 0
    assert definir_combinacoes([2, 2]) == 0
    assert definir_combinacoes([3, 4, 6]) == 0


def test_tem_pontuacao_detecta_rolagem_sem_pontos_da_imagem():
    """Regressão: 6,4,2,3,4,6 não tem 1, 5 nem trinca; deve ser derrota."""
    assert tem_pontuacao([6, 4, 2, 3, 4, 6]) is False


def test_tem_pontuacao_detecta_1_5_e_trinca():
    """Domínio: rolagens com 1, 5 ou trinca devem ser jogáveis."""
    assert tem_pontuacao([1, 2, 3, 4, 6, 6]) is True
    assert tem_pontuacao([2, 3, 4, 5, 6, 6]) is True
    assert tem_pontuacao([2, 2, 2, 3, 4, 6]) is True


def test_tem_pontuacao_lista_vazia_retorna_falso():
    """Caso de borda: sem dados, não existe pontuação possível."""
    assert tem_pontuacao([]) is False


# ─────────────────────────────────────────────────────────────────────────────
# Casos normais e de borda: geração/posicionamento de dados
# ─────────────────────────────────────────────────────────────────────────────


def test_rolar_dados_cria_quantidade_correta_e_valores_validos():
    """Caso normal: rolar_dados deve criar dados de 1 a 6 não selecionados."""
    dados = rolar_dados(6)

    assert len(dados) == 6
    for dado in dados:
        assert 1 <= dado["valor"] <= 6
        assert dado["selecionado"] is False


def test_rolar_zero_dados_retorna_lista_vazia():
    """Caso de borda: rolar 0 dados deve retornar lista vazia."""
    assert rolar_dados(0) == []


def test_centralizar_dados_adiciona_rects_validos():
    """Caso normal: centralizar_dados deve adicionar um Rect em cada dado."""
    dados = [
        {"valor": 1, "selecionado": False},
        {"valor": 5, "selecionado": True},
    ]

    centralizar_dados(dados)

    assert "rect" in dados[0]
    assert "rect" in dados[1]
    assert isinstance(dados[0]["rect"], pygame.Rect)
    assert dados[0]["rect"].y == 220
    assert dados[1]["rect"].x > dados[0]["rect"].x


# ─────────────────────────────────────────────────────────────────────────────
# Casos de domínio: títulos e ranking
# ─────────────────────────────────────────────────────────────────────────────


def test_titulo_por_pontuacao_nos_limites():
    """Casos de borda: títulos devem mudar exatamente nos limites definidos."""
    assert titulo_por_pontuacao(1499) == "Grumete"
    assert titulo_por_pontuacao(1500) == "Colono"
    assert titulo_por_pontuacao(2000) == "Bandeirante"
    assert titulo_por_pontuacao(3000) == "Capitao"
    assert titulo_por_pontuacao(4000) == "Capitao-Geral"


def test_ranking_com_menos_de_5_entradas_aceita_pontuacao():
    """Caso de borda: ranking incompleto aceita nova pontuação."""
    ranking = [
        ("Ana", "Colono", 1500),
        ("Bia", "Colono", 1700),
    ]
    assert pontos_para_entrar_no_ranking(1500, ranking) == 0


def test_ranking_precisa_superar_o_quinto_colocado():
    """Domínio: com ranking cheio, precisa superar o 5º colocado."""
    ranking = [
        ("A", "Capitao", 3000),
        ("B", "Capitao", 2500),
        ("C", "Bandeirante", 2100),
        ("D", "Colono", 1800),
        ("E", "Colono", 1500),
    ]

    assert pontos_para_entrar_no_ranking(1501, ranking) == 0
    assert pontos_para_entrar_no_ranking(1500, ranking) == 1
    assert pontos_para_entrar_no_ranking(1490, ranking) == 11


def test_salvar_ranking_mantem_top_5_ordenado(tmp_path):
    """Domínio: salvar_ranking deve ordenar e manter apenas as 5 maiores pontuações."""
    caminho = tmp_path / "ranking.txt"

    entradas = [
        ("A", "Colono", 1500),
        ("B", "Colono", 1600),
        ("C", "Bandeirante", 2000),
        ("D", "Capitao", 3000),
        ("E", "Colono", 1700),
        ("F", "Capitao-Geral", 4000),
    ]

    for nome, titulo, pontos in entradas:
        salvar_ranking(caminho, nome, titulo, pontos)

    ranking = carregar_ranking(caminho)

    assert len(ranking) == 5
    assert ranking[0] == ("F", "Capitao-Geral", 4000)
    assert ranking[-1][2] == 1600
    assert all(pontos >= 1600 for _, _, pontos in ranking)


def test_carregar_ranking_arquivo_inexistente_retorna_lista_vazia(tmp_path):
    """Caso de borda: arquivo de ranking inexistente não deve quebrar o jogo."""
    assert carregar_ranking(tmp_path / "nao_existe.txt") == []


# ─────────────────────────────────────────────────────────────────────────────
# Casos de domínio: inimigos no mapa
# ─────────────────────────────────────────────────────────────────────────────


def test_gerar_inimigos_cria_dicionarios_com_rect_e_imagem():
    """Caso normal: inimigos devem ter as chaves usadas pelo mapa."""
    imagens = [object(), object(), object(), object()]
    inimigos = gerar_inimigos(imagens, n=3)

    assert len(inimigos) == 3
    for inimigo in inimigos:
        assert set(inimigo.keys()) == {"rect", "imagem"}
        assert isinstance(inimigo["rect"], pygame.Rect)
        assert inimigo["imagem"] in imagens


def test_gerar_inimigos_nao_cria_mais_que_imagens_disponiveis():
    """Caso de borda: se pedir mais inimigos que imagens, limita pelo total de imagens."""
    imagens = [object(), object()]
    inimigos = gerar_inimigos(imagens, n=5)
    assert len(inimigos) == 2


def test_reposicionar_inimigo_nao_usa_chave_antiga_imagens_inimigos():
    """Regressão: reposicionar_inimigo não deve acessar a chave inexistente imagens_inimigos."""
    imagens = [object(), object(), object(), object()]
    inimigos = gerar_inimigos(imagens, n=3)
    alvo = inimigos[0]

    reposicionar_inimigo(alvo, inimigos, imagens)

    assert "imagem" in alvo
    assert "imagens_inimigos" not in alvo
    assert alvo["imagem"] in imagens
    assert 50 <= alvo["rect"].x <= 700
    assert 50 <= alvo["rect"].y <= 500
