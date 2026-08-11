# QA pós-patch de implementação — H-0056 P01

```yaml
item: ITEM-0017
handoff: H-0056
patch: P01
status: I5_MANUAL_VALIDATION_REQUIRED
```

## Resultado

`QA-H0056-IMP-002` foi corrigido. `validar_popups` distingue a ausência da
chave `popups` de sua presença com valor `None`: `{}` e `{"popups": {}}` são
válidos e resultam em mapa vazio; `{"popups": None}` gera `PopupErro`; valores
não-mapa continuam inválidos. A causa é comportamentalmente corrigida, sem
conversão silenciosa de `null` em ausência.

O teste `test_popups_null_presente_e_invalido`, com `pytest.raises(PopupErro)`,
exerce diretamente o caso que passava sob o comportamento anterior baseado em
`.get` e passa com a implementação atual.

## Validações

- **Teste focal direto:** `17 passed in 0.03s`, código de saída `0`.
- **Conjunto focal H-0056:** `21 passed in 0.11s`, código de saída `0`.
- **Suíte canônica:** `1118 passed in 30.50s`, código de saída `0`.
- **Diff focal:** `git diff --check -- tela/renderizacao/popup.py tela/teste_popup.py` sem erros. Os dois arquivos aparecem como não rastreados, sem delta Git disponível para atribuição histórica; a inspeção focal não revelou expansão semântica além da distinção ausência/null e do teste correspondente.

As validações cobrem e mantêm ausência válida, mapa vazio, declaração e
resolução de `popup_basico`, rejeição de tipos não-mapa e as demais validações
estruturais exercidas pelo módulo. Não foi identificado novo defeito material,
nem alteração material em conteúdo runtime, chip `[Esc] Voltar`, geometria,
centralização, modalidade, captura de teclas, `ABORTADO` ou demonstração.

`QA-H0056-IMP-001` e `QA-H0056-IMP-003` não foram reabertos. `.pytest_cache/`
permanece fora do critério desta etapa.

## Encaminhamento

O patch está conforme para automação. Permanece exclusivamente a validação
visual/interativa final em TTY pelo usuário; portanto, o H-0056 deve seguir
para validação manual, sem declaração de aprovação humana.
