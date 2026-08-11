# Relatório de patch de implementação — H-0056 P01

- **Raiz da implementação:** `docs/relatorios/IMP-0056-popup-basico-exibicao-voltar.md`
- **Predecessor imediato:** `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0056.md`
- **Achado corrigido:** `QA-H0056-IMP-002 — popups: null aceito como ausência`.

## Correção

A causa técnica era o uso de `raw.get("popups")`, que retornava `None` tanto
para campo ausente quanto para campo presente com `null`. `validar_popups`
agora testa explicitamente a presença da chave e só retorna `{}` quando ela
está ausente. Campo presente com `None` ou qualquer valor não-mapa continua
gerando `PopupErro`; mapa vazio e declarações válidas permanecem aceitos.

Foi acrescentado o teste focal explícito
`test_popups_null_presente_e_invalido`, que exige `PopupErro` para
`validar_popups({"popups": None})`.

## Testes

- Focal direto: `17 passed in 0.03s`, código de saída `0`.
- Conjunto focal H-0056: `21 passed in 0.11s`, código de saída `0`.
- Suíte canônica: `1118 passed in 30.32s`, código de saída `0`.

## Diff focal

Alterados somente `tela/renderizacao/popup.py` (distinção explícita entre
chave ausente e valor `None`) e `tela/teste_popup.py` (teste de regressão do
`null`). Nenhuma semântica adicional do pop-up foi alterada.

`QA-H0056-IMP-001` não foi usado para modificar documentação. A higiene de
`.pytest_cache/` permanece deferida ao fechamento.

**Bloqueios:** nenhum.
