import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    PRETO,
    BRANCO,
    CINZA,
    AMARELO,
    TAMANHO_DADO,
    CAMINHO_RANKING,
    CAMINHO_MUSICA_LUTA,
)
from src.funcoes import (
    rolar_dados,
    tem_pontuacao,
    titulo_por_pontuacao,
    centralizar_dados,
    desenhar_ranking,
    pedir_nome,
)
from src.combinacoes import definir_combinacoes
from src.dados import salvar_ranking, carregar_ranking
from src.inimigo import jogar_turno as inimigo_jogar

VERDE    = (100, 220, 100)
VERMELHO = (220, 80, 80)


def executar_jogo(tela=None):
    """Executa o loop principal do jogo com exibição e rolagem dos dados."""
    pygame.init()

    if tela is None:
        tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    f_grande = pygame.font.SysFont(None, 42)
    f_medio  = pygame.font.SysFont(None, 36)
    f_dado   = pygame.font.SysFont(None, 48)
    f_inst   = pygame.font.SysFont(None, 24)
    relogio  = pygame.time.Clock()

    dados                = rolar_dados(6)
    pontos_rodada        = 0
    pontuacao_total      = 0
    ultimo_ganho         = 0
    pontuacao_inimigo    = 0
    ultimo_ganho_inimigo = 0
    desc_inimigo         = ""

    estado = "inicio"
    pontuacao_vitoria = 1500
    rodando = True

    # Fade in de preto para a tela dos dados
    dados_temp = rolar_dados(6)
    centralizar_dados(dados_temp)
    fade_surf = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    fade_surf.fill((0, 0, 0))
    inicio_fade = pygame.time.get_ticks()
    DURACAO_FADE = 400
    while True:
        elapsed_fade = pygame.time.get_ticks() - inicio_fade
        alpha = max(0, int((1 - elapsed_fade / DURACAO_FADE) * 255))

        tela.fill(PRETO)

        # Placar
        s = f_grande.render(f"Voce: 0", True, BRANCO)
        tela.blit(s, (30, 25))
        s = f_grande.render(f"Inimigo: 0", True, VERMELHO)
        tela.blit(s, (LARGURA_TELA - s.get_width() - 30, 25))
        s = f_medio.render(f"Rodada: 0", True, CINZA)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 100))

        # Dados
        for d in dados_temp:
            pygame.draw.rect(tela, BRANCO, d["rect"], border_radius=10)
            t = f_dado.render(str(d["valor"]), True, PRETO)
            tela.blit(t, (
                d["rect"].x + TAMANHO_DADO // 2 - t.get_width() // 2,
                d["rect"].y + TAMANHO_DADO // 2 - t.get_height() // 2,
            ))

        # Mensagem de estado inicial
        s = f_medio.render("PARTIDA INICIADA!", True, BRANCO)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 350))
        s = f_inst.render("Pressione qualquer tecla para iniciar", True, CINZA)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 420))

        fade_surf.set_alpha(alpha)
        tela.blit(fade_surf, (0, 0))
        pygame.display.flip()
        relogio.tick(FPS)
        if alpha == 0:
            break
    dados = dados_temp

    while rodando:

        valores_sel  = [d["valor"] for d in dados if d["selecionado"]]
        pontos_combo = definir_combinacoes(valores_sel) if valores_sel else 0

        if estado == "selecionando" and pontos_combo > 0:
            estado = "decisao"
        elif estado == "decisao" and pontos_combo == 0:
            estado = "selecionando"

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:

                if estado in ("derrota", "guardou"):
                    # Vez do inimigo
                    ganho, desc          = inimigo_jogar(pontuacao_inimigo, pontuacao_vitoria)
                    pontuacao_inimigo    += ganho
                    ultimo_ganho_inimigo  = ganho
                    desc_inimigo          = desc
                    dados         = rolar_dados(6)
                    pontos_rodada = 0
                    if pontuacao_inimigo >= pontuacao_vitoria:
                        estado = "inimigo_vitoria"
                    else:
                        estado = "inimigo_resultado"

                elif estado == "inimigo_resultado":
                    estado = "selecionando"

                elif estado == "inimigo_vitoria":
                    pontuacao_total   = 0
                    pontuacao_inimigo = 0
                    pontos_rodada     = 0
                    dados  = rolar_dados(6)
                    estado = "inicio"

                elif estado == "inicio":
                    dados  = rolar_dados(6)
                    estado = "selecionando"

                elif estado == "ranking":
                    pontuacao_total   = 0
                    pontuacao_inimigo = 0
                    pontos_rodada     = 0
                    dados  = rolar_dados(6)
                    estado = "inicio"

                elif estado == "decisao":
                    if evento.key == pygame.K_1:
                        pontos_rodada += pontos_combo
                        n_rest = sum(1 for d in dados if not d["selecionado"])
                        dados  = rolar_dados(n_rest if n_rest > 0 else 6)
                        if tem_pontuacao([d["valor"] for d in dados]):
                            estado = "selecionando"
                        else:
                            pontos_rodada = 0
                            estado        = "derrota"

                    elif evento.key == pygame.K_2:
                        ultimo_ganho     = pontos_rodada + pontos_combo
                        pontuacao_total += ultimo_ganho
                        pontos_rodada    = 0

                        valores_sel_ord = sorted(valores_sel)

                        if valores_sel_ord == [1, 2, 3, 4, 5, 6]:
                            estado = "vitoria_rodada"
                        elif pontuacao_total >= pontuacao_vitoria:
                            estado = "vitoria"
                        else:
                            estado = "guardou"

                        if estado in ("vitoria", "vitoria_rodada"):
                            titulo = titulo_por_pontuacao(pontuacao_total)
                            nome   = pedir_nome(tela, f_medio, f_inst)
                            salvar_ranking(CAMINHO_RANKING, nome, titulo, pontuacao_total)
                            estado = "ranking"

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado in ("selecionando", "decisao"):
                    for d in dados:
                        if "rect" in d and d["rect"].collidepoint(evento.pos):
                            d["selecionado"] = not d["selecionado"]

        # ── Renderização ────────────────────────────────────────────────────
        if estado == "ranking":
            ranking = carregar_ranking(CAMINHO_RANKING)
            desenhar_ranking(tela, (f_grande, f_medio, f_inst), ranking)
            pygame.display.flip()
            relogio.tick(FPS)
            continue

        # ── Renderização especial: turno do inimigo ─────────────────────────
        if estado in ("inimigo_resultado", "inimigo_vitoria"):
            tela.fill(VERMELHO if estado == "inimigo_vitoria" else PRETO)

            titulo_msg = "INIMIGO VENCEU!" if estado == "inimigo_vitoria" else "TURNO DO INIMIGO"
            s = f_grande.render(titulo_msg, True, BRANCO)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 80))

            cor_desc = AMARELO if ultimo_ganho_inimigo > 0 else VERMELHO
            if estado == "inimigo_vitoria":
                cor_desc = BRANCO
            s = f_medio.render(desc_inimigo, True, cor_desc)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 200))

            placar = f"Voce: {pontuacao_total}   Inimigo: {pontuacao_inimigo}"
            s = f_medio.render(placar, True, CINZA)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 290))

            s = f_inst.render("Pressione qualquer tecla para continuar", True, CINZA)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 420))

            pygame.display.flip()
            relogio.tick(FPS)
            continue

        tela.fill(PRETO)
        centralizar_dados(dados)

        # Placar: jogador (esquerda) e inimigo (direita)
        s = f_grande.render(f"Voce: {pontuacao_total}", True, BRANCO)
        tela.blit(s, (30, 25))

        s = f_grande.render(f"Inimigo: {pontuacao_inimigo}", True, VERMELHO)
        tela.blit(s, (LARGURA_TELA - s.get_width() - 30, 25))

        s = f_medio.render(f"Rodada: {pontos_rodada}", True, CINZA)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 100))

        for d in dados:
            cor = AMARELO if d["selecionado"] else BRANCO
            pygame.draw.rect(tela, cor, d["rect"], border_radius=10)
            t = f_dado.render(str(d["valor"]), True, PRETO)
            tela.blit(t, (
                d["rect"].x + TAMANHO_DADO // 2 - t.get_width() // 2,
                d["rect"].y + TAMANHO_DADO // 2 - t.get_height() // 2,
            ))

        if estado == "selecionando":
            msg  = "Combinacao invalida" if valores_sel else "Clique nos dados para selecionar"
            cor  = VERMELHO if valores_sel else CINZA
            inst = ""
        elif estado == "decisao":
            msg  = f"Combo: {pontos_combo} pts"
            cor  = VERDE
            inst = "[1] Continuar jogando   [2] Guardar pontos"
        elif estado == "derrota":
            tela.fill(VERMELHO)
            msg  = "DERROTA!  Pontos da rodada perdidos."
            cor  = BRANCO
            inst = "Pressione qualquer tecla para vez do inimigo"
        elif estado == "inicio":
            msg  = "PARTIDA INICIADA!"
            cor  = BRANCO
            inst = "Pressione qualquer tecla para iniciar"
        else:  # guardou
            msg  = f"+{ultimo_ganho} pts guardados!"
            cor  = VERDE
            inst = "Pressione qualquer tecla para vez do inimigo"

        s = f_medio.render(msg, True, cor)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 350))

        if inst:
            s = f_inst.render(inst, True, CINZA)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 420))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()