from src.combinacoes import definir_combinacoes
from src.funcoes import rolar_dados, tem_pontuacao
from itertools import combinations
 
# Inimigo guarda pontos quando acumula pelo menos esse valor na rodada
LIMIAR_GUARDAR = 300
 
 
def _melhor_selecao(valores):
    """Encontra o subconjunto de dados que maximiza a pontuação."""
    melhor_pts = 0
    melhor_sub = []
 
    for tamanho in range(1, len(valores) + 1):
        for sub in combinations(valores, tamanho):
            pts = definir_combinacoes(sub)
            if pts > melhor_pts:
                melhor_pts = pts
                melhor_sub = list(sub)
 
    return melhor_sub, melhor_pts
 
 
def jogar_turno(pontuacao_atual, pontuacao_vitoria=1500):
    """Simula o turno completo do inimigo.
 
    Estratégia simples:
      - Sempre seleciona o subconjunto de dados com maior pontuação.
      - Guarda quando acumulou LIMIAR_GUARDAR pts, restam <= 2 dados
        ou já pode vencer nessa rodada.
 
    Retorna (pontos_ganhos, descricao):
      - pontos_ganhos: 0 se perdeu a rodada, ou os pontos acumulados.
      - descricao:     string resumindo o resultado do turno.
    """
    pontos_rodada = 0
    dados = rolar_dados(6)
 
    while True:
        valores = [d["valor"] for d in dados]
 
        if not tem_pontuacao(valores):
            return 0, "Sem pontuacao! Perdeu os pontos."
 
        subset, pts_combo = _melhor_selecao(valores)
        pontos_rodada += pts_combo
 
        dados_restantes = len(valores) - len(subset)
        if dados_restantes == 0:
            dados_restantes = 6  # usou todos os dados, rola 6 novos
 
        # Guarda se acumulou o suficiente, restam poucos dados ou pode vencer
        if (pontos_rodada >= LIMIAR_GUARDAR
                or dados_restantes <= 2
                or pontuacao_atual + pontos_rodada >= pontuacao_vitoria):
            return pontos_rodada, f"Guardou +{pontos_rodada} pts!"
 
        dados = rolar_dados(dados_restantes)