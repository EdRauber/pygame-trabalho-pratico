# pontuacao = []
# salvo = [False] * 6
# dados = [0] * 6


# import random

# def rolar_dados():
#     for i in range(6):
#         if not salvo[i]:
#             dados[i] = random.randint(1, 6)

# def salvar_pontos(indice):
#     salvo[indice] = True


# SELECIONAR AÇÃO

turno = True
contador = 0

while turno:
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:  # aperta 1
                rolar_dados()
            elif evento.key == pygame.K_2:  # aperta 2
                pnts_jogador += calcular_pontuacao()
                turno = False
contador += 1