# Relatório de criação do handoff H-0058

## Registro

O handoff `docs/handoff/H-0058-popup-lista-navegavel-marcacao.md` foi criado
para a terceira capacidade da `ADR-0044`, sobre a baseline `master` em
`f8064df`.

## Autoridades usadas

Foram usadas a ADR-0044, o contrato `docs/contratos/contrato_popup.md), a
nomenclatura `docs/nomenclatura/35_POPUP.md`, o renderer
`tela/renderizacao/popup.py`, os testes `tela/teste_popup.py` e
`demo/teste_demo_popup.py`, a fixture
`demo/fixtures/h0057_popup_texto_dinamico.py`, os trechos materiais de
`demo/demo.py` e as declarações/acionamentos de pop-up em
`config/telas/demo/demo.json`.

## Capacidade materializada

O handoff delimita lista plana de marcação, foco por ID, navegação toroidal,
marcação exclusiva/múltipla, recomposição por resize, coexistência com o
conteúdo e chips existentes, preservação da modalidade e `Esc` com
`ABORTADO` sem payload. Mantém explícita a fronteira sem `Enter`,
`CONFIRMADO`, payload confirmado ou ação de negócio.

## Arquivos autorizados

O handoff autoriza somente os componentes diretamente envolvidos do renderer,
integração da tela, testes focais, demo, configuração demonstrativa e a nova
fixture específica de H-0058. Exige, para a implementação futura, o relatório
`docs/relatorios/IMP-0058-popup-lista-navegavel-marcacao.md`.

## Verificações internas

Foi confirmada a existência dos diretórios de handoff e relatórios, a árvore
inicial estava limpa, e o baseline local correspondia a `master`/`f8064df`.
Também foi conferida a separação operacional de H-0058 em relação a H-0059,
sem depender de confirmação ou payload para executar a capacidade.

Não há bloqueio material de autoridade; nenhum arquivo de implementação foi
alterado nesta etapa.
