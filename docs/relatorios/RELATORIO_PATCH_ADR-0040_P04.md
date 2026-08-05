---
name: RELATORIO_PATCH_ADR-0040_P04
description: "Relatório do patch documental que incorpora D-DRY-12 (reconciliação dos rótulos visuais Real/Simulação) à ADR-0040"
metadata:
  type: relatorio
---

# Relatório — Patch ADR-0040 (P04)

```yaml
rastreabilidade:
  etapa: PATCH_ADR
  objeto: ADR-0040
  artefato_principal: docs/adr/ADR-0040-padronizacao-universal-do-controle-de-execucao-real-e-dry-run.md
  decisao_aplicada:
    - D-DRY-12

execucao:
  status: ADR_PATCHED_AWAITING_QA
```

## Decisão incorporada

D-DRY-12 foi acrescentada à seção 3 como nova decisão fechada, posterior a
D-DRY-01–D-DRY-11, originada da decisão explícita do usuário após a
validação manual R03 do `H-0050` (`MANUAL_VALIDATION_APPROVED`, 7/7
critérios conformes). Ela reconcilia exclusivamente os rótulos visuais do
modo corrente do controle universal, sem tocar identificadores internos,
schema, tecla ou qualquer outra decisão vigente.

## Trechos reconciliados

- **D-DRY-02**: rótulos originais marcados como históricos/substituídos;
  rótulos vigentes registrados como definidos por D-DRY-12.
- **D-DRY-06**: tabela de destaque visual passou a referenciar os rótulos
  vigentes por estado interno (`executar` → `[Ins] Real`; `dry_run` →
  `[Ins] Simulação`), preservando a regra de destaque por `cor_alerta`.
- **Seção 4 (Decisão)**: texto consolidado passou a citar `[Ins]
  Real`/`[Ins] Simulação`, com nota de substituição de D-DRY-02 e
  parágrafo dedicado a D-DRY-12.
- **Seção 5 (Consequências)**: nova consequência positiva (fim da colisão
  lexical com `[⏎] Executar`) e novo custo (atualizar documentação,
  configurações demonstrativas, testes e roteiro de validação manual).
- **Seção 5 (Artefatos afetados)**: linha de `contrato_barra_de_menus.md`
  atualizada; nova subseção "Escopo de aplicação de D-DRY-12" lista as
  camadas afetadas pela aplicação futura.
- **Seção 6**: parágrafo novo registra que D-DRY-12 está fechada mas ainda
  não aplicada, e que os rótulos antigos seguem em uso literal até lá.
- **Seção 9**: dez novos itens de verificação cobrindo rótulos, tecla,
  destaque, `[⏎] Executar`, valores internos, ausência de
  `real`/`simulacao` e preservação do H-0044.

## Rótulos substituídos

`[Ins] Executar` → `[Ins] Real` (modo `executar`); `[Ins] Dry-Run` →
`[Ins] Simulação` (modo `dry_run`). Toda ocorrência normativa vigente foi
atualizada; as menções remanescentes aos rótulos antigos estão
explicitamente marcadas como histórico substituído, exceto as referências
ao `[Ins] Dry-Run` focal da ADR-0037/H-0044 — instância distinta, não
afetada por D-DRY-12, preservada sem alteração.

## Valores internos preservados

`executar` e `dry_run` continuam os únicos valores aceitos por
`controle_execucao.modo_inicial`, pela requisição e pelo registro de
ações. Nenhum valor `real` ou `simulacao` foi criado em schema, config ou
requisição.

## Distinção entre modo e ação

A ADR passa a registrar explicitamente que `[⏎] Executar` (ação que inicia
o processamento do lote) e `[Ins] Real`/`[Ins] Simulação` (modo da futura
execução) são conceitos distintos — motivo declarado da reconciliação.

## Consequências e critérios atualizados

Consequências (positivas e custos) e os critérios de aplicação (seção 9)
foram estendidos conforme acima, sem remover nenhum item preexistente.

## Verificações

- D-DRY-12 explícita na seção 3: confirmado.
- `[Ins] Real` como rótulo de `executar`: confirmado.
- `[Ins] Simulação` como rótulo de `dry_run`: confirmado.
- `[⏎] Executar` inalterado: confirmado.
- `cor_alerta` associado a `dry_run`/`Simulação`: confirmado.
- `executar` e `dry_run` como únicos valores internos: confirmado.
- Nenhum valor `real` ou `simulacao` criado: confirmado.
- Sem contradição normativa entre rótulos antigos e novos (antigos sempre
  marcados como substituídos): confirmado.
- D-DRY-01 e D-DRY-03 a D-DRY-11 inalteradas: confirmado.
- Somente `ADR-0040...md` foi alterado; `RELATORIO_PATCH_ADR-0040_P04.md`
  foi criado: confirmado (`git status` restrito a esses dois caminhos).
- Sem espaços em branco finais no arquivo alterado: confirmado.

## Bloqueios

nenhum

## Próxima ação

`QA_ADR` sobre a ADR-0040 patched.
