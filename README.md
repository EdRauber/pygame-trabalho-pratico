# Nome do Jogo

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

- Artur Sales Francisco
- Eduardo Rauber Silva
- Ian Poty Arandu Marques

## Estrutura do projeto

- `main.py`: inicia o jogo;
- `src/mapa.py`: contém o loop principal do mapa;
- `src/jogo.py`: contém o loop principal da partida;
- `src/config.py`: guarda configurações como tamanho da tela e cores;
- `src/funcoes.py`: contém funções auxiliares (antigo - abandonado);
- `src/dados.py`: contém funções de leitura e escrita de arquivos;
- `src/audio.py`: controla a música durante o jogo;
- `src/combinacoes.py`: calcula a pontuação dos lances;
- `src/inimigo.py`: controla como o computador joga;
- `src/inimigos.py`: controla a aparição de spirtes de oponentes no mapa;
- `src/jogo_mutiplayer.py`: controla o fluxo de jogo no modo multiplayer;
- `src/menu.py`: controla as opções de menu da tela principal;
- `src/regras.py`: monitora o funcionamento das regras do jogo para condições;
- `src/sprites.py`: arquivo abandonado;
- `src/transicoes.py`: gera transicoes de combate super radicais;
- `src/ui.py`: controla a interface do menu assim como o display das intruções;

## Descrição do jogo

Descreva brevemente a ideia principal do jogo.

> Tela do mapa onde o jogador pode movimentar e duelar oponentes, durante o duelo mostrar tela da partida do jogo de dados.
> Movimento durante exploração e controle das ações no jogo de dados
> Fazer combinações de dados e ganhar (opcional) - modelo de jogo inspirado em "farkle"
> Dados com baixas pontuações ou nenhuma, oponentes com sorte.

Exemplo:

> O jogo consiste em principalmente um jogo de dados onde o jogador consegue pontuar fazendo combinações especificas dea dados

## Objetivo do jogador

Explique o que o jogador precisa fazer para vencer ou avançar no jogo.

> Duelar oponentes (computadores ou jogadores reais) no jogo de dados e vencer, ou conseguir uma pontuação recordista e entrar no top 5 das maiores pontuações


Exemplo:

> O objetivo é fazer 1500 antes do seu adversário, ou tentar pontuar o mais alto possível

## Regras do jogo

Liste as principais regras do jogo.

- Regra 1: Vence quem conseguir marcar 1500 pontos primeiro
- Regra 2: O jogo consiste em turnos, com cada turno encerrando quando o jogador decidir parar de pontuar, ou quando os dados jogados pontuarem 0
- Regra 3: Cada jogador começa o turno com 6 dados
- Regra 4: Tabela de pontos:
|Dado||pontuação sozinho||pontuação com 2||pontuação com 3|
|:---||:---------------:||:-------------:||--------------:|
|Face 1|| 100 || 200||1000|
|Face 2|| 0 || 0||200|
|Face 3|| 0 || 0||300|
|Face 4|| 0 || 0||400|
|Face 5|| 50 || 100||500|
|Face 6|| 0 || 0||600|
Combinações especiais:
1 | 2 | 3 | 4 | 5 | 6 - 1500 pontos
1 | 2 | 3 | 4 | 5 - 750 pontos
2 | 3 | 4 | 5 | 6 - 750 pontos
Combinações com número repetido 3+ vezes:
a partir de 3 faces iguais a pontuação é multiplicada por 100 baseado no número da face, e para cada dado além de 3 essa pontução duplica:
3 faces 2 = 200
4 faces 2 = 400
5 faces 2 = 800 
- Regra 5: Quando pontuar o jogador pode escolher quais dados utilizar para pontuar
exemplo:
1 | 2 | 2 | 5 | 1 | 3 = pode pontuar - 50 (1 face 5) / 100 (1 face 1) / 150 (1 face 1 & 1 face 5) / 200 (2 face 1) / 250 (2 face 1 & 1 face 5)
- Regra 6: Depois de pontuar o jogador pode continuar jogando com os dados restantes (os que não foram utilizados para pontuar) ou guardar os pontos ganhos nesse turno
(caso queira mais instruções elas estão presentes no menu de "instrucoes" do pygame)


Exemplo:

- O jogador seleciona os dados com o click esquerdo
- Cada lance tem possibilidades diferentes de pontuação
- ao vencer é possível adicionar seu nome e pontuação ao placar
- A partida termina quando o jogador ou o inimigo pontuar pelo menos 1500 pontos

## Controles

Informe as teclas ou comandos utilizados no jogo.

Exemplo:

- W: mover para cima
- S: mover para baixo
- A: mover para esquerda
- D: mover para direita
- ENTER: duelar oponente
- ESC: sair do jogo
- click esquerdo durante partida: selecionar dado
- num_1: pontuar com os dados selecionados
- num_2: pontuar e encerrar o turno


## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
