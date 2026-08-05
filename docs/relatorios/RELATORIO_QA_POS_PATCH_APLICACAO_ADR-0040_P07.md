---
name: REL-QA-POS-PATCH-APLICACAO-0040-P07
description: QA independente da aplicação documental de D-DRY-12 no P07
metadata:
  type: relatorio_qa
  status: ADR_APPLICATION_REJECTED
  data: 2026-08-05
---

# Relatório QA pós-patch de aplicação — ADR-0040 P07

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
  patch_auditado: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P07.md
  regularizacao_previa: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0040_P08.md

decisao_auditada:
  - D-DRY-12
```

## Resultado material

Aplicação material **APROVADA**. O P07 propagou somente os rótulos visuais
universais de D-DRY-12: `[Ins] Real` para `executar` e `[Ins] Simulação` para
`dry_run`. A distinção com `[⏎] Executar` como ação está explícita.

Por arquivo:

- `contrato_barra_de_menus.md`: rótulos vigentes, modo corrente, `Insert`,
  atividade nos dois estados, aparência ativa normal em `Real` e
  `cor_alerta` em `Simulação` estão corretos; `[⏎] Todos` e `[⏎] Executar`
  permanecem preservados.
- `contrato_chip.md`: o controle continua chip específico de tipo
  `alternancia`, sem tipo ou tecla novos; os rótulos não são valores internos.
- `31_BARRA_DE_MENUS_E_CHIPS.md`: registra rótulos, distinção modo/ação,
  `cor_alerta` e a classificação do rótulo antigo.
- `INDICE_ADR.md`: descrição compacta da ADR-0040 usa os rótulos novos e
  preserva identidade, status, data e ITEM relacionado.
- `contrato_tela_json.md`: sem delta material P07; o schema continua usando
  somente `executar` e `dry_run`.
- `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`: sem delta terminológico P07;
  sua alteração visível no diff autorizado é anterior, associada ao P06,
  e preserva a separação configuração/runtime.

Não foram identificados `real` ou `simulacao` como valores internos. Permanecem
inalterados `controle_execucao.modo_inicial`, `dry_run_ativo`, os contratos de
console e o código, configurações concretas e testes fora do escopo. A
especialização focal `[Ins] Dry-Run` do ADR-0037/H-0044 permanece inalterada.

## Ocorrências antigas

O reteste nos seis arquivos autorizados confirmou:

- `HISTORICA_SUBSTITUIDA`: `INDICE_ADR.md:72`; `31_BARRA_DE_MENUS_E_CHIPS.md:142-143`;
  `contrato_barra_de_menus.md:977`; `contrato_chip.md:345-346`.
- `ESPECIALIZACAO_FOCAL_H0044`: `INDICE_ADR.md:69`;
  `31_BARRA_DE_MENUS_E_CHIPS.md:49,113,152,209,227`;
  `contrato_barra_de_menus.md:932,935,986`; `contrato_chip.md:323,352`.
- `DEFEITO_REMANESCENTE`: nenhum.

As ocorrências correntes `[Ins] Real`/`[Ins] Simulação` estão nos trechos
universais esperados. Não há ocorrência normativa universal antiga sem
classificação.

## Delta e cadeia

O delta terminológico do P07 é fiel e limitado aos quatro módulos declarados;
não há termos simultaneamente adicionados e alterados, nem conteúdo material
do P06 ou do P08 incorporado. P06 é aplicação substantiva anterior de
D-DRY-10/D-DRY-11, e o P08 regularizou o relatório do P06 com QA aprovado;
ambos foram preservados. O P07 permanece exclusivo de D-DRY-12.

Há, contudo, o achado `QA-P07-NEW-01`: o relatório P07 declara
`baseline_aprovada` como `...P05.md` e `predecessor_imediato` como `...P04.md`.
Após a existência substantiva do P06 e sua regularização pelo P08, essa cadeia
não é documentalmente fiel. O P07 deveria registrar nominalmente o P06 como
aplicação substantiva anterior, o P08 como regularização prévia aprovada e o
próprio P07 como patch auditado.

```yaml
achado:
  id: QA-P07-NEW-01
  natureza: DEFEITO_RELATORIO_P07
  impacto_material_na_aplicacao: false
  exige_correcao: true
aplicacao_material: APROVADA
relatorio_P07: REQUER_CORRECAO
```

`git diff --check` não apontou problemas. Não há bloqueios. O achado exige
correção do relatório, sem alteração do conteúdo material aplicado.

```yaml
status: ADR_APPLICATION_REJECTED
proxima_acao: PATCH_APLICACAO_ADR
```
