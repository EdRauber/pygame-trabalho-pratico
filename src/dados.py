def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if conteudo == "":
                return 0
            return int(conteudo)
    except FileNotFoundError:
        return 0


def salvar_ranking(caminho_arquivo, nome, titulo, pontuacao, limite=5):
    """Adiciona uma entrada ao ranking, mantendo os top 'limite' maiores."""
    entradas = carregar_ranking(caminho_arquivo)
    entradas.append((nome, titulo, pontuacao))
    entradas.sort(key=lambda x: x[2], reverse=True)
    entradas = entradas[:limite]
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        for n, t, p in entradas:
            arquivo.write(f"{n};{t};{p}\n")


def carregar_ranking(caminho_arquivo):
    """Carrega o ranking; retorna lista de tuplas (nome, titulo, pontuacao)."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            entradas = []
            for linha in arquivo:
                linha = linha.strip()
                partes = linha.split(";")
                if len(partes) == 3:
                    nome, titulo = partes[0], partes[1]
                    try:
                        pontuacao = int(partes[2])
                        entradas.append((nome, titulo, pontuacao))
                    except ValueError:
                        pass
            return entradas
    except FileNotFoundError:
        return []