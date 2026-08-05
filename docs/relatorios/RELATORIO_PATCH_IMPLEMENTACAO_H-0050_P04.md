---
name: RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P04
description: "Patch visual D-DRY-12 do controle universal H-0050"
metadata:
  type: relatorio_patch_implementacao
  etapa: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED_AWAITING_QA
---

# Relatório do patch de implementação H-0050 — P04

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0050-controle-universal-execucao-real-dry-run.md
  predecessor_documental: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0050_P06.md

decisao_implementada:
  - D-DRY-12

patch:
  id: P04
```

## Implementação

A autoridade concreta dos rótulos é `tela/controle_execucao.py`, em
`ROTULOS_EXECUCAO`; `tela/renderizacao/barra_menus.py` apenas materializa a
representação fornecida pela instância. O mapeamento passou a ser
`executar → Real` e `dry_run → Simulação`. Os textos-base das duas
configurações H-0050 foram alinhados, sem alteração do schema.

Arquivos alterados nesta execução:

- `tela/controle_execucao.py`
- `config/telas/demo/h0050_controle_execucao_universal.json`
- `config/telas/demo/h0050_controle_execucao_universal_dry_run_inicial.json`
- `tela/teste_controle_execucao.py`
- `tela/testes_renderizador/barra_menus.py`
- `demo/teste_demo.py`
- este relatório

Os valores internos `executar`, `dry_run`, `modo_inicial`, a enumeração fechada,
Insert, captura, registro, executor, resultado, seleção, Enter, retorno,
reinicialização e redimensionamento não foram reimplementados. `Real` mantém
aparência ativa normal (`destacado=False`); `Simulação` mantém `destacado=True`,
resolvido pela barra como `cor_alerta`. Ambos permanecem ativos. `[⏎] Executar`
continua sendo o chip separado de ação. H-0044 não recebeu delta.

As provas foram ajustadas para os dois rótulos, alternância nos dois sentidos,
aparência normal/alerta, ausência dos rótulos universais antigos, separação de
modo e ação e preservação dos rótulos em terminal estreito.

## Verificações

- Testes focais: **268 passed**.
- Suíte completa: **1037 passed**.
- Demonstração principal: comando executado com sucesso; abriu em `[Ins] Real`.
- Demonstração `dry_run` inicial: comando executado com sucesso; abriu em
  `[Ins] Simulação` com `cor_alerta`. Os testes integrados provaram alternância,
  execução, retorno e reinicialização nas duas configurações.
- Verificação de literais: nenhuma ocorrência vigente de `[Ins] Executar` ou
  `[Ins] Dry-Run` no escopo universal. `TESTE_HISTORICO`: nenhuma ocorrência
  exata. `ESPECIALIZACAO_FOCAL_H0044`: referências `Dry-Run` próprias do H-0044
  permaneceram sem alteração. `DEFEITO_REMANESCENTE`: nenhum.
- Desvios: nenhum. Bloqueios: nenhum.
- Nenhum arquivo foi staged e nenhum commit foi realizado.

A validação manual complementar em TTY real permanece pendente e é de
responsabilidade do usuário; não foi declarada neste patch.

```yaml
status: IMPLEMENTATION_PATCHED_AWAITING_QA
relatorio: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P04.md
artefatos:
  - tela/controle_execucao.py
  - config/telas/demo/h0050_controle_execucao_universal.json
  - config/telas/demo/h0050_controle_execucao_universal_dry_run_inicial.json
  - tela/teste_controle_execucao.py
  - tela/testes_renderizador/barra_menus.py
  - demo/teste_demo.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0050_P04.md
proxima_acao: QA_POS_PATCH_IMPLEMENTACAO_P04
```
