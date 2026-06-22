# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

Portugueses

## 2. Integrantes do grupo

Liste os integrantes do grupo.

- Nome 1: Artur Sales Francisco
- Nome 2: Eduardo Rauber Silva
- Nome 3: Ian Poty Arandu Marques

## 3. Tipo de jogo

Indique o tipo de jogo que será desenvolvido.

Exemplos:
- jogo de desviar de obstáculos;
- jogo de coleta de itens;
- labirinto simples;
- jogo de perguntas e respostas;
- jogo de memória;
- Pong;
- Snake;
- Breakout;
- nave desviando de meteoros;
- corrida simples com obstáculos;
- jogo de clique rápido;
- jogo de sobrevivência simples.

Tipo escolhido pelo grupo:

> Jogo de dados inspirado em farlke

## 4. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará.

Procure responder:

- O que aparece na tela?
- O que o jogador controla?
- O que o jogador precisa fazer?
- Quais desafios aparecem durante a partida?

Descrição:

> Tela do mapa onde o jogador pode movimentar e duelar oponentes, durante o duelo mostrar tela da partida do jogo de dados.
> Movimento durante exploração e controle das ações no jogo de dados
> Fazer combinações de dados e ganhar (opcional) - modelo de jogo inspirado em "farkle"
> Dados com baixas pontuações ou nenhuma, oponentes com sorte.

## 5. Objetivo do jogador

Explique qual é o objetivo principal do jogador.

Exemplos:

- coletar o maior número possível de itens;
- sobreviver pelo maior tempo possível;
- chegar até o final do labirinto;
- acertar alvos;
- responder perguntas corretamente;
- evitar obstáculos;
- quebrar todos os blocos.

Objetivo:

> Duelar oponentes (computadores ou jogadores reais) no jogo de dados e vencer, ou conseguir uma pontuação recordista e entrar no top 5 das maiores pontuações

## 6. Regras principais

Liste as principais regras do jogo.

Exemplo:

- O jogador começa com 3 vidas.
- Cada moeda coletada vale 10 pontos.
- Cada colisão com obstáculo remove 1 vida.
- A partida termina quando as vidas chegam a zero.
- O jogador vence se alcançar 100 pontos.

Regras do grupo:

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


## 7. Condição de vitória

Explique como o jogador vence ou conclui o jogo.

Exemplos:

- atingir determinada pontuação;
- chegar ao final da fase;
- sobreviver até o tempo acabar;
- responder uma quantidade mínima de perguntas;
- quebrar todos os blocos.

Condição de vitória:

> 1500 pontos em um jogo

## 8. Condição de derrota ou encerramento

Explique como o jogador perde ou quando a partida termina.

Exemplos:

- perder todas as vidas;
- acabar o tempo;
- colidir com determinado obstáculo;
- errar muitas perguntas;
- deixar a bola cair, no caso de Breakout ou Pong.

Condição de derrota ou encerramento:

> oponente pontuar 1500 pontos antes do jogador

## 9. Elementos previstos no jogo

Descreva os principais elementos que farão parte do jogo.

## Jogador ou elemento principal

Descrição:

> Um personagem controlado por WASD.
> Jogo de dados controlado por mouse

## Obstáculos, inimigos ou desafios

Exemplo:

> Obstáculos aparecem em posições aleatórias e devem ser evitados.

Descrição:

> inimigos aparecem aleatóriamente no mapa

## Itens, alvos ou objetos de interação

Exemplo:

> Moedas aparecem na tela e aumentam a pontuação quando coletadas.

Descrição:

> Duelar oponentes que aparecem & encontrar as melhores combinações de dados disponíveis

## Pontuação, vidas, tempo ou progresso

Exemplo:

> O jogador começa com 3 vidas e ganha 10 pontos por item coletado.

Descrição:

> pontuação muda durante partida, começando com 0 e com mínimo de vítoria de 1500

## 10. Controles previstos

Informe os comandos que serão utilizados pelo jogador.

Exemplo:

- W: mover para cima
- S: mover para baixo
- A: mover para esquerda
- D: mover para direita
- ENTER: realizar ação
- ESC: sair do jogo

Controles do grupo:

- W: mover para cima
- S: mover para baixo
- A: mover para esquerda
- D: mover para direita
- ENTER: duelar oponente
- ESC: sair do jogo
- click esquerdo durante partida: selecionar dado
- num_1: pontuar com os dados selecionados
- num_2: pontuar e encerrar o turno

## 11. Organização inicial do código

Explique como o grupo pretende organizar o código.

Exemplo:

- `main.py`: inicia o jogo;
- `src/jogo.py`: contém o loop principal;
- `src/config.py`: guarda configurações como tamanho da tela e cores;
- `src/funcoes.py`: contém funções auxiliares;
- `src/dados.py`: contém funções de leitura e escrita de arquivos.

Organização planejada:

> 
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


## 12. Recursos externos previstos

Informe se o grupo pretende utilizar imagens, sons, fontes, tutoriais ou códigos externos.

Exemplo:

- imagens obtidas de banco gratuito;
- sons gratuitos;
- tutorial usado apenas como referência;
- fonte personalizada.

Recursos previstos:

> biblioteca random
> imagens & fontes para estilizar assim como modelos originais
> biblioteca combinations

Caso não pretenda utilizar recursos externos, escreva:

> Não pretendemos utilizar recursos externos.

## 13. Principais dificuldades esperadas

Liste as dificuldades que o grupo acredita que poderá enfrentar.

Exemplos:

- movimentação do jogador;
- colisão entre objetos;
- controle de tempo;
- criação do ranking;
- organização do código;
- uso do GitHub;
- testes;
- exibição de textos na tela.

Dificuldades previstas:

- Dificuldade 1: organização do código
- Dificuldade 2: interface funcional
- Dificuldade 3: IA básica do oponente

## 14. Escopo mínimo para a entrega final

Descreva qual será a versão mínima aceitável do jogo.

Esta seção é importante para evitar que o grupo escolha uma ideia grande demais.

Exemplo:

> A versão mínima do jogo terá um personagem controlado pelo teclado, obstáculos aparecendo na tela, sistema de vidas, sistema de pontuação e tela de fim de jogo.

Escopo mínimo:

> A versão mínima do jogo terá um sitema de streak para cada vitória, um mapa pequeno para andar e duelar oponentes, e um sistema de dados funcional, com uma tela mostrando a streak mais alta quando for fechar o jogo.

## 15. Possíveis melhorias, caso haja tempo

Liste funcionalidades extras que o grupo poderá implementar se conseguir concluir o escopo mínimo.

Exemplos:

- tela inicial;
- sons;
- fases;
- aumento de dificuldade;
- ranking;
- animações;
- novos tipos de obstáculos;
- diferentes personagens;
- menu de pausa.

Melhorias possíveis:

- Melhoria 1: Dados especiais
- Melhoria 2: Modo História (beta)
- Melhoria 3: Nomes de ranque
- Melhoria 4: moeda de jogo
- Melhoria 5: menu de pausa