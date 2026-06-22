import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    PRETO,
    BRANCO,
    CINZA,
    AMARELO,
    TAMANHO_DADO,
)
from src.regras import (
    rolar_dados,
    tem_pontuacao,
    centralizar_dados,
)
from src.ui import confirmar_voltar_menu
from src.combinacoes import definir_combinacoes

VERDE = (100, 220, 100)
VERMELHO = (220, 80, 80)
AZUL = (90, 160, 255)


NOMES_JOGADORES = ("Jogador 1", "Jogador 2")


def trocar_jogador(jogador_atual):
    """Alterna entre Jogador 1 e Jogador 2."""
    return 1 - jogador_atual


def cor_jogador(indice):
    """Retorna uma cor visual para cada jogador."""
    return AZUL if indice == 0 else VERMELHO


def iniciar_novo_turno():
    """Cria os dados e zera a pontuacao temporaria do turno."""
    return rolar_dados(6), 0


def desenhar_placar_multiplayer(tela, fontes, pontuacoes, jogador_atual, pontos_rodada):
    """Desenha o placar dos dois jogadores e destaca de quem e a vez."""
    f_grande, f_medio, f_inst = fontes

    cor_j1 = AMARELO if jogador_atual == 0 else BRANCO
    cor_j2 = AMARELO if jogador_atual == 1 else BRANCO

    s = f_grande.render(f"J1: {pontuacoes[0]}", True, cor_j1)
    tela.blit(s, (30, 25))

    s = f_grande.render(f"J2: {pontuacoes[1]}", True, cor_j2)
    tela.blit(s, (LARGURA_TELA - s.get_width() - 30, 25))

    s = f_medio.render(f"Rodada: {pontos_rodada}", True, CINZA)
    tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 90))

    nome = NOMES_JOGADORES[jogador_atual]
    s = f_inst.render(f"Vez de {nome}", True, cor_jogador(jogador_atual))
    tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 135))


def desenhar_dados(tela, f_dado, dados):
    """Desenha os dados na tela com destaque para os selecionados."""
    centralizar_dados(dados)

    for d in dados:
        cor = AMARELO if d["selecionado"] else BRANCO
        pygame.draw.rect(tela, cor, d["rect"], border_radius=10)
        t = f_dado.render(str(d["valor"]), True, PRETO)
        tela.blit(t, (
            d["rect"].x + TAMANHO_DADO // 2 - t.get_width() // 2,
            d["rect"].y + TAMANHO_DADO // 2 - t.get_height() // 2,
        ))


def executar_multiplayer(tela=None):
    """Executa uma batalha local de dados para dois jogadores.

    Os dois jogadores jogam no mesmo computador, revezando turnos.
    O jogador ativo seleciona dados com o mouse e usa:
      - 1 para continuar rolando
      - 2 para guardar os pontos
      - ESC para perguntar se volta ao menu principal
    """
    pygame.init()

    if tela is None:
        tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    pygame.display.set_caption("Multiplayer")

    f_grande = pygame.font.SysFont(None, 42)
    f_medio = pygame.font.SysFont(None, 36)
    f_dado = pygame.font.SysFont(None, 48)
    f_inst = pygame.font.SysFont(None, 24)
    relogio = pygame.time.Clock()

    pontuacao_vitoria = 1500
    pontuacoes = [0, 0]
    jogador_atual = 0
    dados, pontos_rodada = iniciar_novo_turno()
    ultimo_ganho = 0
    mensagem_resultado = ""
    estado = "inicio"

    while True:
        valores_dados = [d["valor"] for d in dados]
        valores_sel = [d["valor"] for d in dados if d["selecionado"]]
        pontos_combo = definir_combinacoes(valores_sel) if valores_sel else 0

        # Derrota automática da rodada quando nenhum dado da mão atual
        # pode pontuar. Isso corrige casos como 6,4,2,3,4,6.
        if estado == "selecionando" and not tem_pontuacao(valores_dados):
            nome = NOMES_JOGADORES[jogador_atual]
            mensagem_resultado = f"{nome} perdeu os pontos da rodada."
            ultimo_ganho = 0
            pontos_rodada = 0
            estado = "resultado_turno"

        if estado == "selecionando" and pontos_combo > 0:
            estado = "decisao"
        elif estado == "decisao" and pontos_combo == 0:
            estado = "selecionando"

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE and estado != "vitoria":
                    escolha_menu = confirmar_voltar_menu(tela, f_medio, f_inst)
                    if escolha_menu == "sim":
                        return "menu_principal"
                    if escolha_menu == "sair":
                        return "sair"
                    continue

                if estado == "inicio":
                    estado = "selecionando"

                elif estado == "resultado_turno":
                    jogador_atual = trocar_jogador(jogador_atual)
                    dados, pontos_rodada = iniciar_novo_turno()
                    ultimo_ganho = 0
                    mensagem_resultado = ""
                    estado = "selecionando"

                elif estado == "vitoria":
                    if evento.key == pygame.K_RETURN:
                        return "menu_principal"

                elif estado == "decisao":
                    if evento.key == pygame.K_1:
                        pontos_rodada += pontos_combo
                        n_rest = sum(1 for d in dados if not d["selecionado"])
                        dados = rolar_dados(n_rest if n_rest > 0 else 6)

                        if tem_pontuacao([d["valor"] for d in dados]):
                            estado = "selecionando"
                        else:
                            nome = NOMES_JOGADORES[jogador_atual]
                            mensagem_resultado = f"{nome} perdeu os pontos da rodada."
                            ultimo_ganho = 0
                            pontos_rodada = 0
                            estado = "resultado_turno"

                    elif evento.key == pygame.K_2:
                        nome = NOMES_JOGADORES[jogador_atual]
                        ultimo_ganho = pontos_rodada + pontos_combo
                        pontuacoes[jogador_atual] += ultimo_ganho
                        pontos_rodada = 0

                        if pontuacoes[jogador_atual] >= pontuacao_vitoria:
                            estado = "vitoria"
                        else:
                            mensagem_resultado = f"{nome} guardou +{ultimo_ganho} pts."
                            estado = "resultado_turno"

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado in ("selecionando", "decisao"):
                    for d in dados:
                        if "rect" in d and d["rect"].collidepoint(evento.pos):
                            d["selecionado"] = not d["selecionado"]

        # ── Renderizacao ───────────────────────────────────────────────────
        tela.fill(PRETO)

        if estado == "vitoria":
            vencedor = NOMES_JOGADORES[jogador_atual]
            s = f_grande.render(f"{vencedor} venceu!", True, cor_jogador(jogador_atual))
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 105))

            placar = f"J1: {pontuacoes[0]}   J2: {pontuacoes[1]}"
            s = f_medio.render(placar, True, BRANCO)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 210))

            s = f_inst.render("ENTER: voltar ao menu principal", True, CINZA)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 340))

            pygame.display.flip()
            relogio.tick(FPS)
            continue

        desenhar_placar_multiplayer(
            tela,
            (f_grande, f_medio, f_inst),
            pontuacoes,
            jogador_atual,
            pontos_rodada,
        )
        desenhar_dados(tela, f_dado, dados)

        if estado == "inicio":
            msg = "MULTIPLAYER INICIADO!"
            cor = BRANCO
            inst = "Pressione qualquer tecla para o Jogador 1 comecar"

        elif estado == "selecionando":
            msg = "Combinacao invalida" if valores_sel else "Clique nos dados para selecionar"
            cor = VERMELHO if valores_sel else CINZA
            inst = ""

        elif estado == "decisao":
            msg = f"Combo: {pontos_combo} pts"
            cor = VERDE
            inst = "[1] Continuar jogando   [2] Guardar pontos"

        else:  # resultado_turno
            msg = mensagem_resultado
            cor = VERDE if ultimo_ganho > 0 else VERMELHO
            proximo = NOMES_JOGADORES[trocar_jogador(jogador_atual)]
            inst = f"Pressione qualquer tecla para a vez de {proximo}"

        s = f_medio.render(msg, True, cor)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 350))

        if inst:
            s = f_inst.render(inst, True, CINZA)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 420))

        s = f_inst.render("ESC: voltar ao menu", True, CINZA)
        tela.blit(s, (15, 560))

        pygame.display.flip()
        relogio.tick(FPS)
