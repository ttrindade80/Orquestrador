# IMP-0060 — Resize responsivo das formações do pop-up de marcação — R02

## Identificação

- Item: `ITEM-0028`
- ADR: `ADR-0045`
- Handoff: `H-0060`
- Patch de handoff: `P01`
- Origem: `MV-H0060-001`
- Etapa executada: `IMPLEMENTAR`

## Causa transportada

`renderizar_tela` já calculava `l_corpo_disponivel`, mas, com pop-up aberto,
entregava à sobreposição a altura natural excedente do corpo materializado.
O pop-up escolhia a formação contra esse espaço fictício e a verificação final
rejeitava o excesso contra a cota física real.

## Alteração aplicada

No ramo focal `popup is not None` de `renderizar_tela`, quando existe altura
física definida, o bloco subjacente usado pela sobreposição passa a ser uma
projeção com exatamente `l_corpo_disponivel` linhas. Linhas naturais excedentes
do corpo não são apresentadas ao pop-up como capacidade vertical; eventual
complemento físico usa linhas vazias da largura do corpo. A mesma
`l_corpo_disponivel` é passada como `altura` à sobreposição.

Nenhum conteúdo do pop-up, instrução, chip ou item é cortado. A verificação
final de geometria permanece ativa e continua rejeitando uma composição final
maior que a região reservada. O caminho sem pop-up não recebeu especialização:
em `80x18`, ele continua materializando o corpo natural com 14 linhas e
rejeitando-o contra as 12 linhas disponíveis.

`tela/renderizacao/popup.py` permaneceu intacto nesta execução; a implementação
aprovada das formações foi apenas exercitada pelos testes.

## Arquivos alterados nesta execução

- `tela/renderizacao/tela.py`
- `tela/testes_renderizador/integracao.py`
- `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao-R02.md`

Mudanças já existentes no diretório de trabalho foram preservadas sem edição
nesta execução.

## Regressões de integração adicionadas

- Matriz em `80x18`, para marcação exclusiva e múltipla: a sobreposição recebe
  bloco e cota de 12 linhas, os seis itens são materializados em matriz, o
  quadro tem 80 colunas por 18 linhas e não produz terminal pequeno.
- Linha em `77x14`, para marcação exclusiva e múltipla: a sobreposição recebe
  bloco e cota de 8 linhas, os seis itens são materializados em linha, o quadro
  tem 77 colunas por 14 linhas e não produz terminal pequeno.
- Terminal pequeno real em `23x6`, para marcação exclusiva e múltipla: o fluxo
  runtime completo preserva por igualdade o quadro consolidado, sem itens
  parciais e sem substituir a instância aberta.
- Não regressão sem pop-up em `80x18`: preservada a rejeição do corpo natural de
  14 linhas contra a área física de 12 linhas.
- Os casos de matriz e linha também verificam identidade da instância, cursor,
  marcações por ID, dimensões finais e presença integral dos seis itens.

## Resultados dos comandos obrigatórios

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/testes_renderizador/integracao.py`:
  23 aprovados em 0,22 s.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py`:
  63 aprovados em 0,13 s.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_popup.py`:
  15 aprovados em 0,13 s.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest`:
  1175 aprovados em 30,95 s.
- `git diff --check`: código de saída 0, sem ocorrências.

## Bloqueios e desvios

Nenhum bloqueio e nenhum desvio de escopo. Não houve alteração normativa,
validação manual, QA independente, stage, commit ou push.
