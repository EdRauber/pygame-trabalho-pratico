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
    ESPACO_DADO,
    X_INICIAL_DADOS,
    Y_INICIAL_DADOS,
)
from src.funcoes import rolar_dados, tem_pontuacao
from src.combinacoes import definir_combinacoes

VERDE    = (100, 220, 100)
VERMELHO = (220, 80, 80)

def centralizar_dados(dados):
    """Calcula e atribui os rects dos dados, centralizados horizontalmente."""
    n = len(dados)
    total_w = n * TAMANHO_DADO + (n - 1) * ESPACO_DADO
    x0 = (LARGURA_TELA - total_w) // 2
    for i, d in enumerate(dados):
        d["rect"] = pygame.Rect(x0 + i * (TAMANHO_DADO + ESPACO_DADO), 220, TAMANHO_DADO, TAMANHO_DADO)


def executar_jogo():
    """Executa o loop principal do jogo com exibição e rolagem dos dados."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    f_grande = pygame.font.SysFont(None, 72)
    f_medio  = pygame.font.SysFont(None, 52)
    f_dado   = pygame.font.SysFont(None, 64)
    f_inst   = pygame.font.SysFont(None, 30)
    relogio = pygame.time.Clock()

 # ── Variáveis de estado ─────────────────────────────────────────────────
    dados           = rolar_dados(6)
    pontos_rodada   = 0   # acumulado no turno atual, ainda não guardado
    pontuacao_total = 0   # pontos definitivamente guardados
    ultimo_ganho    = 0   # usado só para exibir na tela "guardou"
 
    # "selecionando" → jogador escolhe dados
    # "decisao"      → seleção válida, espera [1] ou [2]
    # "derrota"       → jogada sem pontos possíveis, perdeu a rodada
    # "guardou"      → pontos guardados, aguarda tecla para novo turno
    # "inicio"      →  tela inicial da partida
    # "vitoria"      → jogador vence com 1500 pontos
    # "vitoria_rodada" → jogador faz 1500 pontos em uma única rolagem
    estado = "inicio"

    pontuacao_vitoria = 1500

    rodando = True

    dados = rolar_dados(6)

    while rodando:

        # ── Calcula combo da seleção atual ──────────────────────────────────
        valores_sel  = [d["valor"] for d in dados if d["selecionado"]]
        pontos_combo = definir_combinacoes(valores_sel) if valores_sel else 0
 
        # Transição automática conforme validade da seleção
        if estado == "selecionando" and pontos_combo > 0:
            estado = "decisao"
        elif estado == "decisao" and pontos_combo == 0:
            estado = "selecionando"
 
        # ── Eventos ─────────────────────────────────────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:

                # Qualquer tecla reinicia o turno depois de derrota ou guardar
                if estado in ("derrota", "guardou"):
                    dados         = rolar_dados(6)
                    pontos_rodada = 0
                    estado        = "selecionando"

                elif estado in ("inicio"):
                    dados = rolar_dados(6)
                    estado = "selecionando"

                elif estado in ("vitoria", "vitoria_rodada"):
                    pontuacao_total = 0
                    pontos_rodada = 0
                    dados = rolar_dados(6)
                    estado = "inicio"
                
                elif estado == "decisao":
                   if evento.key == pygame.K_1:          # ── [1] Continuar
                       pontos_rodada += pontos_combo
                       n_rest = sum(1 for d in dados if not d["selecionado"])
                       # Se pontuou todos os 6, ganha dados novos
                       dados = rolar_dados(n_rest if n_rest > 0 else 6)
                       if tem_pontuacao([d["valor"] for d in dados]):
                           estado = "selecionando"
                       else:
                           pontos_rodada = 0
                           estado = "derrota"

                elif evento.key == pygame.K_2:        # ── [2] Guardar
                    ultimo_ganho     = pontos_rodada + pontos_combo
                    pontuacao_total += ultimo_ganho

                    valores_sel_ordenados = sorted(valores_sel)

                    if valores_sel_ordenados == [1, 2, 3, 4, 5, 6]:
                        estado = "vitoria_rodada"
                    elif pontuacao_total >= pontuacao_vitoria:
                        estado = "vitoria"
                    else:
                        estado           = "guardou"

                    pontos_rodada    = 0

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if estado in ("selecionando", "decisao"):
                    for d in dados:
                        if "rect" in d and d["rect"].collidepoint(evento.pos):
                            d["selecionado"] = not d["selecionado"]

                        
        # ── Renderização ────────────────────────────────────────────────────
        tela.fill(PRETO)
        centralizar_dados(dados)
 
        # Pontuação total (topo)
        s = f_grande.render(f"Total: {pontuacao_total}", True, BRANCO)
        tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 25))
 
        # Pontos acumulados no turno atual
        s = f_medio.render(f"Rodada: {pontos_rodada}", True, CINZA)
        tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 110))
 
        # Dados
        for d in dados:
            cor = AMARELO if d["selecionado"] else BRANCO
            pygame.draw.rect(tela, cor, d["rect"], border_radius=10)
            t = f_dado.render(str(d["valor"]), True, PRETO)
            tela.blit(t, (
                d["rect"].x + TAMANHO_DADO//2 - t.get_width()//2,
                d["rect"].y + TAMANHO_DADO//2 - t.get_height()//2,
            ))
 
        # Mensagem principal + instrução conforme estado
        if estado == "selecionando":
            msg  = "Combinação inválida" if valores_sel else "Clique nos dados para selecionar"
            cor  = VERMELHO if valores_sel else CINZA
            inst = ""
        elif estado == "decisao":
            msg  = f"Combo: {pontos_combo} pts"
            cor  = VERDE
            inst = "[1] Continuar jogando   [2] Guardar pontos"
        elif estado == "derrota":
            msg  = "DERROTA!  Pontos da rodada perdidos."
            tela.fill(VERMELHO)
            cor  = BRANCO
            inst = "Pressione qualquer tecla para continuar"
        elif estado == "inicio":
            msg = "PARTIDA INICIADA!"
            cor = BRANCO
            inst = "Pressione qualquer tecla para iniciar"
        elif estado == "vitoria":
            msg = "VOCÊ VENCEU!"
            tela.fill(VERDE)
            cor = BRANCO
            inst = "Pressione qualquer tecla para jogar novamente"
        elif estado == "vitoria_rodada":
            msg = "INCRÍVEL! PONTUAÇÃO ESPECIAL!"
            tela.fill(AMARELO)
            cor = BRANCO
            inst = "Pressione qualquer tecla para jogar novamente"
        else:  # guardou
            msg  = f"+{ultimo_ganho} pts guardados!"
            cor  = VERDE
            inst = "Pressione qualquer tecla para continuar"
 
        s = f_medio.render(msg, True, cor)
        tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 350))
 
        if inst:
            s = f_inst.render(inst, True, CINZA)
            tela.blit(s, (LARGURA_TELA//2 - s.get_width()//2, 420))
 
        pygame.display.flip()
        relogio.tick(FPS)
 
    pygame.quit()