---
name: relatorio-qa-aplicacao-adr-0049-pos-p01
description: Reteste QA do patch P01 da aplicação da ADR-0049
metadata:
  type: relatorio
  item: ITEM-0027
  adr: ADR-0049
---

# QA pós-P01 — aplicação da ADR-0049

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0049.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0049_P01.md
```

## Reteste

- `QA-APP-0049-01`: **resolvido**. §7 exige justificação somente quando solicitada, expansão entre vãos internos e distinção de padding/alinhamento, deixando indeterminados uniformidade, resto, ausência de vãos e última linha. §12 não reintroduz essas regras.
- `QA-APP-0049-02`: **pendente**. Embora §6 deixe a política histórica indefinida, §5 ainda prescreve não haver “condensação” de conteúdo e §12 exige “ausência de normalização incidental de espaços e separadores”. Semanticamente, essas formulações continuam proibindo condensação/normalização de espaços e separadores sem requisito de consumidor ou decisão posterior.
- `QA-APP-0049-03`: **resolvido**. §11 limita-se a exigir determinismo no domínio válido e remete validação, rejeição, exceção, fallback, texto vazio, ANSI inválido e limites técnicos à definição executiva posterior.

Não foi identificado novo defeito material separado; o problema de `QA-APP-0049-02` permanece residual. A busca focal foi executada e as ocorrências materiais foram verificadas nos §§3, 5–7, 11 e 12. Não há política substituta inventada para justificação ou entradas inválidas, e as decisões comportamentais da ADR permanecem preservadas.

## Status final

`ADR_APPLICATION_REJECTED`
