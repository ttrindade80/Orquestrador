---
name: indice-texto
description: Índice de documentos de redação — regras gerais e blocos por texto produzido
metadata:
  type: indice
  scope: texto
---

# Índice — texto/

## Estrutura

```
texto/
├── docs/
│   ├── INDICE.md              ← este arquivo
│   ├── backlog.md             ← tarefas futuras de redação
│   ├── issues.md              ← impedimentos ativos
│   └── contratos/
│       └── contrato_redacao_geral.md   ← regras comuns a todos os textos
└── <nome_texto>/
    └── docs/
        ├── INDICE.md          ← índice específico do texto
        ├── backlog.md
        ├── issues.md
        └── contratos/
            └── contrato_<nome_texto>.md  ← seções, escopo, voz, restrições
```

## Textos registrados

| Pasta | Tipo | Estado |
|---|---|---|
| _(nenhum ainda)_ | — | — |

## Política

- `contrato_redacao_geral.md`: regras que valem para todos os textos (português
  acadêmico, política de estrangeirismos, uso de siglas, travessão vs. hífen, etc.)
- Contrato por texto: seções obrigatórias, escopo, restrições específicas do
  veículo (template PPGEE, journal, etc.)
- As críticas do qualificacao_v3.tex (Claude + GPT, 2026-07-02) são a base para o
  `contrato_redacao_geral.md` e para o contrato do texto de qualificação.
