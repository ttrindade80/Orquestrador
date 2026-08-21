---
name: RELATORIO_PATCH_ADR-0049_P02
description: "Relatório do patch P02 da ADR-0049, tratando exclusivamente QA-ADR-0049-03 (prescrição residual de fachada na tabela de artefatos afetados)"
metadata:
  type: relatorio
  item: ITEM-0027
  adr: ADR-0049
  patch: P02
---

```yaml
cadeia:
  raiz: docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0049_POS_P01.md
achados_tratados:
  - QA-ADR-0049-03
```

## Delta material

Reescrita a linha da tabela normativa de `Artefatos afetados` (§5) que
prescrevia existência e preservação de uma "fachada pública de
renderização". A linha passou a descrever, em nível puramente
comportamental, apenas os consumidores existentes que hoje acessam
capacidades de renderização compartilhadas, sem nomear fachada, camada
pública, adapter, gateway, interface central, módulo agregador, proxy ou
ponto único de exportação, e sem fixar módulo, API, helper ou caminho de
dependência.

## Trecho conceitualmente corrigido

Antes:

> `Fachada pública de renderização consumida pelos demais módulos` |
> `Migrar para o mecanismo canônico, preservando seu papel de fachada
> perante os consumidores existentes.`

Depois:

> `Consumidores existentes que hoje acessam capacidades de renderização
> compartilhadas` | `Migrar para o mecanismo canônico, garantindo que
> esses consumidores continuem recebendo, após a reconciliação, as
> capacidades de renderização de que dependem.`

## Busca focal de resíduos

Comando executado após a correção:

```zsh
rg -n -i \
  'fachada|reexport|re-export|interface central|módulo agregador|modulo agregador|gateway|adapter|proxy' \
  docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md
```

Ocorrências remanescentes e avaliação semântica:

- Linha 66 (D-0027-01): "não introduzir uma fachada sobre implementações
  divergentes que continuem a existir por baixo" — rejeita a fachada como
  abordagem insuficiente; não prescreve nem exige sua existência ou
  preservação. Fora do escopo do achado.
- Linha 180 (texto de fechamento de §5): "mecanismo de reexportação" surge
  apenas para afirmar que essa escolha pertence à aplicação/handoff futuro,
  não a esta ADR. Declaração de não-fixação, consistente com a correção.
- Linha 198 (§7, Alternativas consideradas): "Introduzir uma fachada
  pública única... sem unificá-las" é alternativa historicamente rejeitada
  por D-0027-01; não é prescrição normativa e não restringe a
  implementação futura.

Nenhuma das três ocorrências remanescentes exigiu edição.

## Verificações

- Significado de D-0027-01 a D-0027-09 preservado (nenhuma decisão fechada
  foi alterada; apenas a linha da tabela de artefatos afetados em §5 foi
  reescrita).
- Achados `QA-ADR-0049-01` e `QA-ADR-0049-02` não reintroduzidos (edição
  restrita à prescrição de fachada).
- Autoridade comportamental canônica, convergência de autoridades locais,
  contrato futuro `docs/contratos/contrato_composicao_textual.md`,
  fronteira comportamento comum/semântica dos consumidores, consistência
  medição/renderização e distinção wrap/truncamento permanecem intactos no
  texto da ADR.
- `git diff --check` e `test -f` sobre os dois artefatos alterados/criados
  executados sem apontar problemas.

## Bloqueios

Nenhum. A remoção da prescrição de fachada não exigiu escolher substituto
arquitetural: a linha corrigida permanece em nível comportamental, sem
fixar estrutura concreta.
