---
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
objeto: H-0045 / VM-H0045-R06-001
patch: P22
achado_tratado: QA-H0045-P21-001
rastreabilidade:
  cadeia_raiz: VM-H0045-R06-001
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P21.md
  arquivos_alterados:
    - demo/teste_demo_paginacao.py
---

# P22 — Prova ponta a ponta da sequência de Esc em tela aninhada

## Achado tratado

QA-H0045-P21-001: inexistia prova ponta a ponta da sequência de Esc em
tela aninhada (seleção ativa → `[Esc] Limpar` → primeiro Esc limpa e
permanece → `[Esc] Voltar` → segundo Esc retorna à tela anterior).

## Teste acrescentado

`test_h0045_p22_esc_aninhada_primeiro_limpa_segundo_volta`, acrescentado a
`demo/teste_demo_paginacao.py` (aditivo, após os testes P21 existentes).
Helper local `_p22_modelos_tela_aninhada()` reutiliza o padrão de modelo em
memória já adotado pelos testes P06/P07
(`_console_paginado_selecionavel_h0045`) e o helper `_barra_esc_p21`.

## Construção da tela aninhada (caminho funcional real)

O estado aninhado é construído sem manipulação manual de pilha ou seleção:

1. Tela raiz com lançador cujo `chip` "x" dispara o empilhamento real
   (`processar_comando` reconhece o chip, empilha `tela_atual` e troca para
   `tela_destino`) — produz `pilha_telas == ["tela_raiz_p22"]`.
2. `Tab` estabelece foco no console aninhado (seleção múltipla, paginado).
3. `Espaço` marca o item sob o cursor.

O console aninhado declara `politica_selecao: multipla` e chip Esc com
`forma_exibicao: "rotulo_dinamico_esc"` e `texto: "Voltar"` — condição
exigida pelo cenário inicial (item 7) para que o rótulo dinâmico exiba
`[Esc] Voltar` quando a seleção está vazia em tela aninhada.

## Antes do primeiro Esc

Tela aninhada é a tela atual; pilha contém a tela anterior; seleção do
console focado não vazia; quadro contém `[Esc] Limpar` e não contém
`[Esc] Voltar` nem `[Esc] Sair`; `saindo` falso; foco, cursor e página
válidos.

## Depois do primeiro Esc

Seleção esvaziada (`[]`); tela aninhada permanece a tela atual; pilha
inalterada (mesma quantidade de entradas, sem retorno); `saindo` falso;
foco, cursor e página preservados. Quadro passa a conter `[Esc] Voltar` e
não contém `[Esc] Limpar`.

## Depois do segundo Esc (mesmo objeto de estado)

Fluxo normal de Voltar executado pelo próprio processamento funcional de
Esc: tela anterior (`tela_raiz_p22`) volta a ser a tela atual; pilha
reduzida exatamente uma vez (`[]`); `saindo` permanece falso (sem saída
global).

## Resultados

- Teste nominal (P22): passed.
- Suíte focal (`teste_selecao`, `teste_renderizador`,
  `teste_demo_paginacao`, `teste_demo_navegacao`): 483 passed.
- Suíte completa (`python -m pytest`): 897 passed.
- `git diff --check` sobre os arquivos preservados/autorizados: limpo
  (exit 0).

## Bloqueios

Nenhum. Código produtivo, configurações JSON e demais testes permanecem
intactos. A alteração é estritamente aditiva em `demo/teste_demo_paginacao.py`.
