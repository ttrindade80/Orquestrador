# Relatório de criação do handoff H-0060

## Identificação

- Item: `ITEM-0028`
- ADR: `ADR-0045`
- Handoff: `H-0060`
- Título: Resize responsivo das formações do pop-up de marcação

## Leitura realizada

Leitura integral:

- `docs/adr/ADR-0045-resize-responsivo-formacoes-popup-marcacao.md`
- `docs/contratos/contrato_popup.md`
- `docs/nomenclatura/35_POPUP.md`
- `tela/renderizacao/popup.py`

Leitura focal:

- `docs/backlog.md`, no registro do `ITEM-0028`;
- `tela/teste_popup.py`;
- `demo/teste_demo_popup.py`;
- `demo/fixtures/h0058_popup_lista_marcacao.py`.

## Buscas focais executadas

- `rg -n "popup|marcacao|formacao|geometria_popup|renderizar_popup|navegar_marcacao" tests`
  — o diretório `tests` não existe; a busca foi registrada com o erro de
  ausência do caminho.
- `rg -n "popup" demo config tests` — identificou os arquivos diretamente
  relacionados em `demo` e `config` e também registrou a ausência de
  `tests`.
- `rg --files` focal — identificou `tela/teste_popup.py`,
  `demo/teste_demo_popup.py` e a fixture H-0058.
- Buscas nominais nos símbolos de formação, grade, resize e navegação de
  `tela/renderizacao/popup.py` e nos testes H-0058 para confirmar os pontos de
  extensão.

## Arquivos identificados

Implementação:

- `tela/renderizacao/popup.py`, concentrando seleção de formação,
  particionamento, grade, materialização, navegação e geometria do pop-up.

Testes:

- `tela/teste_popup.py`, com helpers e testes unitários existentes de
  formações, navegação, estado, marcação e resize;
- `demo/teste_demo_popup.py`, com o fluxo runtime e os acionamentos das duas
  políticas de marcação.

Fixture/demonstração:

- `demo/fixtures/h0058_popup_lista_marcacao.py` existe e já é carregada pela
  demonstração. É aplicável e suficiente para reutilização; não foi incluída
  criação de fixture nova nem alteração de configuração.

## Decisões transportadas

O handoff transporta a prioridade `coluna → matriz → linha → quadro mínimo`,
a maximização de colunas fisicamente ocupadas, o mínimo de duas linhas para
matriz, o preenchimento vertical sem placeholders, a condição estrita de uma
linha para `linha`, o vão de dois espaços no cálculo e na saída, o desconto do
overhead real, a recomposição pelo fluxo geral de resize, a reversibilidade e
a preservação por ID do cursor e das marcações para as duas políticas.

Também foram transportadas as fronteiras negativas: não usar
`distribuicao_matricial`, não transformar o pop-up em console e não alterar
texto, abertura, envelope, resultados, chips, estilo, composição, paginação
ou política geral de terminal pequeno.

## Decisões novas e bloqueios

Nenhuma decisão nova foi introduzida. O handoff apenas converte a ADR-0045 e
os contratos já aplicados em instruções de implementação e testes.

Não foram identificados bloqueios de decisão, documentação ou decomposição.
