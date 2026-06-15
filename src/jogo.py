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

VERDE    = (100, 220, 100)
VERMELHO = (220, 80, 80)


def executar_jogo():
    """Executa o loop principal do jogo com exibição e rolagem dos dados."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    f_grande = pygame.font.SysFont(None, 42)
    f_medio  = pygame.font.SysFont(None, 36)
    f_dado   = pygame.font.SysFont(None, 48)
    f_inst   = pygame.font.SysFont(None, 24)
    relogio  = pygame.time.Clock()

    dados           = rolar_dados(6)
    pontos_rodada   = 0
    pontuacao_total = 0
    ultimo_ganho    = 0

    estado = "inicio"
    pontuacao_vitoria = 1500
    rodando = True

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
                    dados         = rolar_dados(6)
                    pontos_rodada = 0
                    estado        = "selecionando"

                elif estado == "inicio":
                    dados  = rolar_dados(6)
                    estado = "selecionando"

                elif estado == "ranking":
                    pontuacao_total = 0
                    pontos_rodada   = 0
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

        tela.fill(PRETO)
        centralizar_dados(dados)

        s = f_grande.render(f"Total: {pontuacao_total}", True, BRANCO)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 25))

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
            inst = "Pressione qualquer tecla para continuar"
        elif estado == "inicio":
            msg  = "PARTIDA INICIADA!"
            cor  = BRANCO
            inst = "Pressione qualquer tecla para iniciar"
        else:
            msg  = f"+{ultimo_ganho} pts guardados!"
            cor  = VERDE
            inst = "Pressione qualquer tecla para continuar"

        s = f_medio.render(msg, True, cor)
        tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 350))

        if inst:
            s = f_inst.render(inst, True, CINZA)
            tela.blit(s, (LARGURA_TELA // 2 - s.get_width() // 2, 420))

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()