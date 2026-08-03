---
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
identificador: RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P21
achado: VM-H0045-R06-001
data: "2026-08-02"
rastreabilidade:
  cadeia_raiz: VM-H0045-R06-001
  achados_tratados:
    - VM-H0045-R06-001
---

# Relatório — Patch de Implementação H-0045 P21 (VM-H0045-R06-001)

## Causa confirmada

`VM-H0045-R06-001` corrige um defeito exclusivamente VISUAL do chip
`[Esc]`: enquanto a ação corrente (em console focado com seleção múltipla
não vazia) é limpar a seleção, o chip continuava exibindo o rótulo original
(`Sair`/`Voltar`). O tratamento FUNCIONAL de `Esc` em `demo/demo.py`
(limpar seleção e manter a tela aberta; só sair/voltar quando a seleção
está vazia) já está correto e foi preservado sem alteração — confirmado por
inspeção (`demo/demo.py:459-479`) e pela leitura focal autorizada.

A autoridade única de composição de chips da barra de menus vive em
`tela/renderizador.py::_linhas_barra`, que já interpreta o campo contratado
`forma_exibicao` para o chip `[Enter]` (`rotulo_dinamico_selecao`). O
mecanismo correto era, portanto, estender o MESMO campo com um novo valor
para o chip Esc — exatamente o caminho recomendado pelo P20 antes do
bloqueio.

## Solução implementada

Reutilizado o mecanismo existente `forma_exibicao` (nenhum campo novo de
configuração):

1. **`tela/selecao.py`** — função pura `rotulo_esc(estado, console,
   rotulo_original)`: devolve `"Limpar"` quando o console declara seleção
   múltipla E possui seleção reconciliada não vazia; devolve o
   `rotulo_original` nos demais casos (`None`, sem seleção múltipla,
   seleção vazia, rotulo ausente). Função privada
   `_console_declarou_selecao_multipla` espelha a leitura de
   `tela.navegacao`/`tela.renderizador`. `rotulo_enter`, `limpar`,
   `reconciliar` e demais políticas permanecem intocados.

2. **`tela/renderizador.py::_linhas_barra`** — duas alterações focais:
   (a) `console_foco` inicializado antes do bloco `if lista is not None`;
   (b) novo bloco de materialização, espelhando o de `[Enter]`, que substitui
   o `texto` do chip Esc por `rotulo_esc(...)` somente quando
   `tecla == "Esc"` E `forma_exibicao == "rotulo_dinamico_esc"`. Somente o
   texto exibido é substituído; tecla, ordem, atividade (`regra_ativo`),
   cores e demais propriedades do chip são preservados.

Funções de largura do P17, paginação, distribuição matricial, composição
geral da barra e comportamento de Enter permanecem inalterados.

## Arquivos alterados

- `tela/selecao.py` (+`rotulo_esc`, `_console_declarou_selecao_multipla`)
- `tela/renderizador.py` (somente `_linhas_barra`: inicialização de
  `console_foco` + bloco de materialização do chip Esc)
- `tela/teste_renderizador.py` (+`TestRotuloDinamicoEscP21`, 11 testes)
- `tela/teste_selecao.py` (+`TestRotuloEsc`, 14 testes)
- `demo/teste_demo_paginacao.py` (+duas classes de teste, 16 testes)

## Configurações atualizadas (3, seleção múltipla)

- `config/telas/demo/h0045_fluxo_execucao_paginado.json`
- `config/telas/demo/h0044_fluxo_execucao_integrado.json`
- `config/telas/demo/h0041_selecao_multipla_oito_itens.json`

Em cada uma, SOMENTE o chip `chip_esc` mudou de
`"forma_exibicao": "visivel_ativo"` para
`"forma_exibicao": "rotulo_dinamico_esc"`. O texto original `"Sair"`
permanece como fallback.

## Configurações preservadas (2, seleção única)

- `config/telas/demo/h0045_paginacao_console_unico.json`
  (`politica_selecao: "unica"`, `visivel_ativo`/`Sair` inalterados)
- `config/telas/demo/h0045_dois_consoles_paginas_independentes.json`
  (`politica_selecao: "unica"`, `visivel_ativo`/`Sair` inalterados)

Verificação focal confirmada: as três múltiplas usam `rotulo_dinamico_esc`;
as duas únicas permanecem `visivel_ativo`; nenhum campo novo introduzido.

## Comportamento do primeiro e segundo Esc

- **Primeiro Esc** (console focado com seleção não vazia): limpa toda a
  seleção reconciliada, mantém a tela aberta, preserva foco, cursor e
  página (caminho funcional já existente em `demo/demo.py`, não alterado).
- **Segundo Esc** (após seleção já limpa): executa a ação normal — Sair
  (pilha vazia) ou Voltar (pilha não vazia).

Prova ponta-a-ponta via `processar_comando` + `renderizar_estado`, sem
modificar `demo/demo.py`.

## Isolamento por console focal

Somente a seleção do console focado determina o rótulo (`rotulo_esc`
recebe `console_foco` do contexto). Seleção em outro console não produz
`[Esc] Limpar`. Ao trocar o foco, o rótulo reflete o novo console focal
(provado em `TestRotuloDinamicoEscP21`). Configurações de seleção única
não declaram `rotulo_dinamico_esc` e permanecem com o chip original.

## Testes focais

Cobertura dos 16 critérios exigidos: vazia exibe `Sair`; `Voltar`
preservado sem seleção; uma/varias seleções e seleção entre páginas exibem
`Limpar`; primeiro Esc limpa toda a seleção sem encerrar/retornar; após
limpeza reaparece o rótulo original; segundo Esc executa Sair; `Limpar` e
original nunca coexistem; mudança de página e resize mantêm coerência; troca
de foco considera somente o console focal; seleção única preserva o chip
original; cursor, foco e página reconciliados; Enter, Espaço, seleção e
paginação sem regressão.

## Suíte completa

Suíte focal autorizada → **482 passed**. Suíte completa
(`PYTHONDONTWRITEBYTECODE=1 python -m pytest -q`) → **896 passed**.

## `git diff --check`

Executado sobre os nove arquivos autorizados (código, testes, três
configurações). Resultado: **limpo** (código de saída 0; sem conflitos de
espaços em branco nem marcadores).

## Bloqueios

Nenhum. A implementação concluiu-se integralmente dentro dos arquivos
autorizados pelo patch. `demo/demo.py`, `tela/paginacao.py`,
`tela/navegacao.py`, funções de largura do renderer, contratos, ADRs e
demais documentos não foram alterados.

status: IMPLEMENTATION_PATCHED
proxima_acao: QA_POS_PATCH
