# Fechamento H-0058 — ADR-0044

## Capacidade fechada

H-0058 — Pop-up com lista navegável e marcação `exclusiva`/`multipla`, com
foco por ID, navegação, recomposição física e saída por `Esc`.

## Status finais

- QA do handoff: `H1_HANDOFF_APPROVED`.
- Implementação pós-patch P01: runtime conforme; teste regressivo explícito
  de recomposição adicionado; nenhuma falha de implementação identificada.
- Verificação documental: `AMBIGUIDADE_DOCUMENTAL`, sem bloqueio ao
  fechamento; as três formações são obrigatórias e cobertas deterministicamente.
- Validação manual: `MANUAL_VALIDATION_APPROVED`.
- Patch P01: `runtime_alterado: false`, originado em `MV-H0058-01`.

## Testes finais

- Testes focais (`tela/teste_popup.py` e `demo/teste_demo_popup.py`):
  `60 passed`.
- Teste regressivo isolado de recomposição: `1 passed`.
- Suíte canônica: `1157 passed`.
- `git diff --check`: limpo.

## Arquivos do ciclo

- `tela/renderizacao/popup.py`
- `tela/teste_popup.py`
- `demo/demo.py`
- `demo/teste_demo_popup.py`
- `demo/fixtures/h0058_popup_lista_marcacao.py`
- `config/telas/demo/demo.json`
- `docs/handoff/H-0058-popup-lista-navegavel-marcacao.md`
- `docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0058.md`
- `docs/relatorios/RELATORIO_QA_HANDOFF_H-0058.md`
- `docs/relatorios/IMP-0058-popup-lista-navegavel-marcacao.md`
- `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0058.md`
- `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0058_P01.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0058_P01.md`
- `docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_H-0058_FORMACOES_TERMINAL_PEQUENO.md`
- `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0058.md`
- `docs/relatorios/RELATORIO_FECHAMENTO_H-0058_ADR-0044.md`

## Reconciliação focal

As referências a H-0058, os caminhos dos artefatos e os IDs demonstrativos
`popup_lista_exclusiva`, `popup_lista_multipla` e `opcao_1`–`opcao_6` foram
conferidos. O comportamento entregue é compatível com ADR-0044, contrato do
pop-up e nomenclatura vigente: a lista é plana, a política pertence à
configuração e cursor/marcações são preservados por ID na recomposição.

A fronteira de H-0059 permanece preservada. H-0058 não entrega confirmação por
`Enter`, `CONFIRMADO`, payload confirmado, binding, interpretação pelo chamador
ou ação de negócio; `Esc` permanece `ABORTADO` sem payload. H-0059 é o próximo
handoff funcional.

Não foi necessária alteração direta em ADR-0044, contrato, nomenclatura,
índice ou backlog. Não foram feitas correções mecânicas de whitespace/EOF.
Não foram encontrados resíduos temporários.

## Resize e deferimento

Na sessão TTY não foram observadas visualmente matriz e linha antes do quadro
de terminal pequeno. A observação é não bloqueante: a cobertura determinística
confirmou, na mesma instância, `coluna → matriz → linha → coluna`, preservando
identidade, envelope, ordem, cursor e marcações. A documentação não exige que
uma única sessão TTY atravesse as três formações antes do terminal pequeno.

Fica deferida exclusivamente para o fechamento documental final do
`ITEM-0017`, depois de H-0059, a criação de um novo item de backlog para fazer
o redimensionamento efetivamente atravessar as distribuições coluna, matriz e
linha antes de declarar terminal pequeno demais. Nenhum item foi criado e o
backlog não foi alterado neste fechamento.

## Stage

O stage nominal deve conter somente os 16 arquivos listados acima. Após a
auditoria, o estado esperado é `STAGE_PRONTO_PARA_COMMIT`; nenhum commit ou
push foi executado.

Mensagem de commit proposta para uso posterior pelo gerente:

`feat: implementa popup com lista navegavel e marcacao`
