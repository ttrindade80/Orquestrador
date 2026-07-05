---
name: indice-qualificacao
description: Índice de documentos específicos do texto de qualificação — contratos, backlog e issues
metadata:
  type: indice
  scope: texto-qualificacao
---

# Índice — texto/qualificacao/

## Carregar em toda sessão sobre este texto

1. `../../docs/contratos/contrato_redacao_geral.md` — regras universais
2. `docs/contratos/contrato_qualificacao.md` — estrutura e requisitos específicos
3. `docs/backlog.md` — tarefas abertas
4. `docs/issues.md` — impedimentos ativos

## Contratos vigentes

| Arquivo | Estado |
|---|---|
| `docs/contratos/contrato_qualificacao.md` | vigente |
| `qualificacao/docs/contratos_secoes.md` | vigente — migrar para cá |

## Arquivos fonte

| Arquivo | Localização atual |
|---|---|
| `qualificacao_v3.tex` | `qualificacao/texto/qualificacao_v3.tex` |
| `qualificacao.bib` | `qualificacao/texto/qualificacao.bib` |
| Makefile | `qualificacao/texto/Makefile` |

## Decisões estruturais fixadas

- Não duplicar objetivos: Cap. 1 é canônico; Cap. 5 usa referência cruzada
- Não usar travessão: ver `contrato_redacao_geral.md`
- Correção arquitetural: custo de ML irrelevante para WSN; modelar overhead de controle
