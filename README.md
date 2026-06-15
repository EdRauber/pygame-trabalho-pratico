# Nome do Jogo

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

- Artur Sales Francisco
- Eduardo Rauber Silva
- Ian Poty Arandu Marques
- Nome do integrante 4

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

Descreva brevemente a ideia principal do jogo.

Exemplo:

> O jogo consiste em principalmente um jogo de dados onde o jogador consegue pontuar fazendo combinações especificas dea dados

## Objetivo do jogador

Explique o que o jogador precisa fazer para vencer ou avançar no jogo.

Exemplo:

> O objetivo é fazer 1500 antes do seu adversário, ou tentar pontuar o mais alto possível

## Regras do jogo

Liste as principais regras do jogo.

Exemplo:

- O jogador seleciona os dados com o click esquerdo
- Cada lance tem possibilidades diferentes de pontuação
- ao vencer é possível adicionar seu nome e pontuação ao placar
- A partida termina quando o jogador ou o inimigo pontuar pelo menos 1500 pontos

## Controles

Informe as teclas ou comandos utilizados no jogo.

Exemplo:

- click esquerdo: escolher inimigo/dados
- number pad 1: guardar e continuar turno
- number pad 2: guardar e encerrar turno

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
