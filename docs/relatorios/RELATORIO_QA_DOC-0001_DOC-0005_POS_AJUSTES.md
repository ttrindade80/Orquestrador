---
name: REL-DOC-DOC-0001-DOC-0005-POS-AJUSTES
description: Auditoria pós-ajustes de consistência documental entre DOC-0001 e DOC-0005
metadata:
  type: relatorio_qa
  status: APROVADO
  data: 2026-07-05
rastreabilidade:
  auditoria_anterior: docs/relatorios/RELATORIO_QA_DOC-0001_DOC-0005.md
  auditoria: "DOC-0001 a DOC-0005 pós-ajustes"
  contratos_alvo:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_estilo.md
  adr_relacionadas:
    - docs/adr/ADR-0001-menu-suporta-matriz.md
    - docs/adr/ADR-0002-menu-sobra-direita.md
    - docs/adr/ADR-0003-vaos-elasticos-menu.md
    - docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md
  bugs_abertos: []
---

# Relatório QA pós-ajustes — DOC-0001 a DOC-0005

## Status anterior

`APROVADO COM AJUSTES`

## Status pós-ajustes

`APROVADO`

## Achados anteriores e estado atual

| Achado | Severidade original | Estado atual | Evidencia atual | Observacao |
|---|---|---|---|---|
| ACHADO-001 — Residuo de "alinhado a direita" | alta | resolvido | `grep -RInE 'alinhado à direita\|alinhamento à direita\|alinhamento do \`menu\` \(direita\)\|menu.*muda.*direita' ...` sem saida. `docs/adr/ADR-0001-menu-suporta-matriz.md:85` referencia ADR-0002 como "bloco a esquerda com sobra a direita"; `docs/NOMENCLATURA.md:325`, `:606` e `:727` usam formulacao equivalente. | Nao restou formulacao de alinhamento do `menu` a direita. |
| ACHADO-002 — Decisoes ja aceitas ainda tratadas como pendentes de ADR | media | resolvido | `grep -RInE 'ADR-000X-menu-suporta-matriz\|pendente de ADR\|Mudança pendente de ADR\|a atualizar por ADR' ...` sem saida. `docs/NOMENCLATURA.md:207`, `:453`, `:514` e secao 12 referenciam ADR-0001, ADR-0002, ADR-0003 e ADR-0004 aceitas. | As decisoes de DOC-0001 a DOC-0004 aparecem como formalizadas. |
| ACHADO-003 — DOC-0001 concluido, mas com proxima acao ativa | baixa | resolvido | `docs/build_docs/to_do.md:34` marca DOC-0001 como `concluido`; `docs/build_docs/to_do.md:41` registra proxima acao como concluida e aponta para `docs/adr/ADR-0001-menu-suporta-matriz.md`. | Nao ha instrucao ativa para criar `ADR-000X-menu-suporta-matriz.md`. |
| ACHADO-004 — `contrato_estilo.md` dizia que contratos separados ainda nao foram escritos | baixa | resolvido | `grep -RInE 'ainda não escritos' docs/contratos/contrato_estilo.md` sem saida. `docs/contratos/contrato_estilo.md:23-25` informa que `contrato_composicao_corpo.md` ja cobre composicao do corpo e que demais dominios serao tratados quando formalizados. | A frase foi corrigida sem ampliar escopo contratual. |

## Verificacoes sem achados

| Verificacao | Evidencia | Resultado |
|---|---|---|
| Ausencia de residuos de "alinhado a direita" | Comando grep obrigatorio executado nos arquivos alvo, sem saida. | OK |
| Ausencia de pendencias de ADR ja resolvidas | Comando grep obrigatorio para `ADR-000X-menu-suporta-matriz`, `pendente de ADR`, `Mudança pendente de ADR` e `a atualizar por ADR`, sem saida. | OK |
| DOC-0001 sem proxima acao ativa incompatível | `docs/build_docs/to_do.md:34-41` mostra status concluido e proxima acao encerrada com referencia a `docs/adr/ADR-0001-menu-suporta-matriz.md`. | OK |
| Frase de `contrato_estilo.md` corrigida | `docs/contratos/contrato_estilo.md:23-25` reconhece `contrato_composicao_corpo.md` como existente; grep por "ainda nao escritos" nao retornou ocorrencias. | OK |
| `scripts/config/estilo.json` valido | `python -m json.tool config/estilo.json >/dev/null && echo "JSON OK"` retornou `JSON OK`. | OK |
| Ausencia de arquivos de codigo alterados | `git status --short --untracked-files=all` listou apenas arquivos em `docs/` e `config/`; nenhum arquivo de codigo apareceu. | OK |

## Comandos executados

Os comandos foram executados a partir de `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`; por isso, os caminhos foram usados sem o prefixo externo `scripts/`.

```bash
grep -RInE 'alinhado à direita|alinhamento à direita|alinhamento do `menu` \(direita\)|menu.*muda.*direita' \
  docs/adr/ADR-0001-menu-suporta-matriz.md \
  docs/NOMENCLATURA.md \
  docs/contratos/contrato_estilo.md \
  docs/build_docs/to_do.md
```

Saida observada: sem ocorrencias.

```bash
grep -RInE 'ADR-000X-menu-suporta-matriz|pendente de ADR|Mudança pendente de ADR|a atualizar por ADR' \
  docs/NOMENCLATURA.md \
  docs/build_docs/to_do.md
```

Saida observada: sem ocorrencias.

```bash
grep -RInE 'ainda não escritos' \
  docs/contratos/contrato_estilo.md
```

Saida observada: sem ocorrencias.

```bash
python -m json.tool config/estilo.json >/dev/null && echo "JSON OK"
```

Saida observada: `JSON OK`.

```bash
git status --short --untracked-files=all
```

Saida observada antes deste relatorio: alteracoes/untracked apenas em `docs/` e `config/`; nenhum arquivo de codigo listado.

## Conclusao

A documentação DOC-0001 a DOC-0005 está aprovada após os ajustes locais. Os achados da auditoria anterior foram encerrados.
