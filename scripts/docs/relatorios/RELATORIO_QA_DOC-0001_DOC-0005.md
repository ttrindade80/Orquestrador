---
name: REL-DOC-DOC-0001-DOC-0005
description: Auditoria documental final de consistência entre DOC-0001 e DOC-0005
metadata:
  type: relatorio_qa
  status: APROVADO_COM_AJUSTES
  data: 2026-07-05
rastreabilidade:
  auditoria: "DOC-0001 a DOC-0005"
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

# REL-DOC — Auditoria DOC-0001 a DOC-0005

## Revisao executada

Auditoria final de consistência documental entre DOC-0001, DOC-0002, DOC-0003, DOC-0004 e DOC-0005.

## Status final

`APROVADO COM AJUSTES`

## Achados

### ACHADO-001 — Resíduo de "alinhado à direita"

Severidade: alta

Arquivos:

- `scripts/docs/adr/ADR-0001-menu-suporta-matriz.md:85`
- `scripts/docs/NOMENCLATURA.md:325`
- `scripts/docs/NOMENCLATURA.md:607`
- `scripts/docs/NOMENCLATURA.md:729`

Descrição:

Ainda há formulações dizendo que o menu foi "alinhado à direita" ou que ADR-0002 é "alinhamento à direita", em conflito com DOC-0002.

Ação recomendada:

Substituir por "bloco à esquerda com sobra à direita" ou equivalente.

Classificação: correção local.

### ACHADO-002 — NOMENCLATURA.md ainda trata decisões como pendentes de ADR

Severidade: média

Arquivos:

- `scripts/docs/NOMENCLATURA.md:207`
- `scripts/docs/NOMENCLATURA.md:453`
- `scripts/docs/NOMENCLATURA.md:514`
- `scripts/docs/NOMENCLATURA.md:720`

Descrição:

O documento mantém linguagem de pendência para decisões já formalizadas em ADR-0001 a ADR-0004.

Ação recomendada:

Atualizar os trechos para referenciar as ADRs aceitas ou remover a seção de ADRs necessárias já cumpridas.

Classificação: correção local.

### ACHADO-003 — to_do.md marca DOC-0001 concluído, mas mantém próxima ação ativa

Severidade: baixa

Arquivos:

- `scripts/docs/build_docs/to_do.md:34`
- `scripts/docs/build_docs/to_do.md:41`

Descrição:

DOC-0001 está concluído, mas ainda instrui criar ADR genérica `ADR-000X-menu-suporta-matriz.md`.

Ação recomendada:

Trocar a próxima ação por "concluído" e apontar para `docs/adr/ADR-0001-menu-suporta-matriz.md`.

Classificação: correção local.

### ACHADO-004 — contrato_estilo.md diz que contratos separados ainda não foram escritos

Severidade: baixa

Arquivos:

- `scripts/docs/contratos/contrato_estilo.md:22`

Descrição:

O texto afirma que composição de corpo, barra_de_menus e layout são contratos separados "ainda não escritos", mas `contrato_composicao_corpo.md` já existe.

Ação recomendada:

Atualizar a frase para refletir os contratos já existentes e os que ainda faltam.

Classificação: correção local.

## Verificações sem achados

- `scripts/config/estilo.json` existe e é JSON válido.
- Não há resíduo do nome antigo `ADR-0002-alinhamento-menu-direita` / `alinhamento-menu-direita`.
- `contrato_composicao_corpo.md` está consistente sobre fila, matriz, preenchimento coluna-a-coluna, ausência de paginação, vãos elásticos e sobra à direita.
- `INDICE_ADR.md` lista ADR-0001, ADR-0002, ADR-0003 e ADR-0004, e os arquivos correspondentes existem com nomes compatíveis.
- `contrato_estilo.md` não mantém tabelas de valores concretos de presets; aponta para `scripts/config/estilo.json`.
- `NOMENCLATURA.md` não mantém tabelas concretas de presets de estilo; mantém referências ao JSON.
- A relação entre schema obrigatório, valores concretos em `scripts/config/estilo.json` e ausência temporária de `cor_inativo` / `cor_alerta` está explicada adequadamente.
- `git status --short --untracked-files=all` mostra alterações/untracked em documentação e config, sem arquivos de código alterados.

## Verificação de escopo

| Item | Resultado |
|---|---|
| Relatório QA formal criado | OK |
| Contratos preservados sem correção nesta rodada | OK |
| ADRs preservadas sem correção nesta rodada | OK |
| `NOMENCLATURA.md` preservado sem correção nesta rodada | OK |
| `to_do.md` preservado sem correção nesta rodada | OK |
| `config/estilo.json` preservado sem correção nesta rodada | OK |

## Conclusão

A auditoria DOC-0001 a DOC-0005 foi registrada com status `APROVADO COM AJUSTES`. Os quatro achados são correções locais em documentação, sem exigência de ADR/RFC nova neste relatório.
