---
name: relatorio-patch-aplicacao-adr-0049-p02
description: Relatório do patch P02 aplicado ao contrato de composição textual para tratar o resíduo QA-APP-0049-02
metadata:
  type: relatorio
  scope: tui_composicao_textual
---

# Relatório — Patch de aplicação ADR-0049 (P02)

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0049.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0049_POS_P01.md
achados_tratados:
  - QA-APP-0049-02
```

## Trechos corrigidos

### §5 — Resultado (linha 78 original)

Antes:

> preservar a ordem e o conteúdo textual, sem perda, duplicação, condensação
> ou inserção de conteúdo, salvo as transformações expressamente admitidas
> neste contrato;

Depois:

> preservar a ordem e o conteúdo textual, sem perda, duplicação ou inserção
> de conteúdo, salvo as transformações expressamente admitidas neste
> contrato;

Removida a palavra `condensação`, que escolhia implicitamente uma política de
não condensação de espaços/separadores.

### §12 — Critérios de aceite para handoffs futuros (linha 189 original)

Removido o item de lista:

> - ausência de normalização incidental de espaços e separadores;

Esse item prescrevia diretamente uma política de preservação de
espaços/separadores não decidida pela ADR-0049.

## Política normativa removida

- Exigência de ausência de `condensação` de conteúdo em §5.
- Exigência de `ausência de normalização incidental de espaços e
  separadores` em §12.

## Confirmação de que nenhuma política substituta foi criada

Nenhum texto novo foi introduzido em §5 ou §12. As duas remoções apenas
suprimiram prescrição existente; não foi adicionada preservação literal,
normalização, compactação, trimming ou qualquer outra política de
whitespace/separadores. A indefinição já registrada em §6 permanece
inalterada e continua sendo a única declaração normativa sobre o tema.

## Busca focal de resíduos (pós-patch)

Comando executado:

```zsh
rg -n -i \
  'condens|normaliz|espaços|espacos|separador|whitespace|trim|remov|acrescent|preserv' \
  docs/contratos/contrato_composicao_textual.md
```

Ocorrências remanescentes e classificação:

- L50–51: definição de `vão interno`/`separador` — assunto terminológico
  distinto (elegibilidade para justificação), não é política de whitespace.
- L78: integridade geral de conteúdo (perda/duplicação/inserção), sem
  determinar política de espaços/separadores.
- L84: preservação de informação ANSI — segurança ANSI, assunto distinto.
- L91: ausência de hífen/marcador de quebra — não é política de whitespace.
- L94–99 (§6): declara explicitamente a política de espaços/separadores como
  indefinida — preservado sem alteração.
- L104: limite de largura ao repartir segmento — não é política de
  whitespace.
- L134: preservação de estado visual ANSI — segurança ANSI, assunto
  distinto.
- L187: preservação de ordem e conteúdo (critério geral de aceite) — não
  determina política de whitespace/separadores.
- L195: preservação de responsabilidades e fronteiras do consumidor —
  assunto distinto.

Nenhuma ocorrência remanescente prescreve política de whitespace/separadores;
todas apenas declaram a indefinição (§6) ou tratam de assunto não
equivalente.

## Verificações

```zsh
git diff --check -- \
  docs/contratos/contrato_composicao_textual.md \
  docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0049_P02.md
```

Sem saída (sem conflitos de whitespace). O contrato permanece como arquivo
não rastreado (`??`) no git, portanto `git diff` não produz saída de
comparação para ele; a ausência de erro do `--check` foi confirmada.

```zsh
test -f docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0049_P02.md
```

Confirmado: arquivo presente.

## Bloqueios

Nenhum. A remoção das prescrições não exigiu escolher nova política de
espaços/separadores.
