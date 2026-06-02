def definir_combinacoes(dados_escolhidos):
    if {1 , 2 , 3 , 4 , 5 , 6}.issubset(dados_escolhidos):
        return 1500

    if {1 , 2 , 3 , 4 , 5}.issubset(dados_escolhidos) or {2 , 3 , 4 , 5, 6}.issubset(dados_escolhidos):
        if dados_escolhidos.count(1) == 2:
            return 850
        if dados_escolhidos.count(5) == 2:
            return 800
        return 750
    
    face_1 , face_2 , face_3 , face_4, face_5, face_6 = 0 , 0 , 0 , 0 , 0 , 0
    for i in dados_escolhidos:
        if i == 1:
            face_1 += 1
        
        elif i == 2:
            face_2 += 1

        elif i == 3:
            face_3 += 1
        
        elif i == 4:
            face_4 += 1
        
        elif i == 5:
            face_5 += 1

        elif i == 6:
            face_6 += 1
    
    if not {1 , 2}.isdisjoint([face_2 , face_3 , face_4 , face_6]):
        return 0
    
    valor = 0

    if 3 > face_1 > 0:
        valor += face_1 * 100
    
    elif face_1 >= 3:
        valor += 1000 * (2**(face_1 - 3))
    
    if face_2 >= 3:
        valor += 200 * (2**(face_2 - 3))
    
    if face_3 >= 3:
        valor += 300 * (2**(face_3 - 3))
    
    if face_4 >= 3:
        valor += 400 * (2**(face_4 - 3))
    
    if 3 > face_5 > 0:
        valor += face_5 * 50

    elif face_5 >= 3:
        valor += 500 * (2**(face_5 - 3))

    if face_6 >= 3:
        valor += 600 * (2**(face_6 - 3))
    
    return valor

lista = [1,2,3,4,1,1]
print(definir_combinacoes(lista))