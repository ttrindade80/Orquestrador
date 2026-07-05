---
name: indice-metodologia
description: Índice de documentos do sistema metodologia — ordem de carregamento e mapa de responsabilidades
metadata:
  type: indice
  scope: metodologia
---

# Índice — metodologia/

## Carregar em toda sessão

1. Este arquivo (`docs/INDICE.md`)
2. `docs/backlog.md` — trabalho futuro
3. `docs/issues.md` — impedimentos ativos

## Contratos vigentes

| Arquivo | Escopo | Estado |
|---|---|---|
| `docs/contratos/contrato_pesquisa.md` | Protocolo geral de busca e triagem | vigente |

## Registro

| Arquivo | Conteúdo |
|---|---|
| `docs/registro/strings_busca.md` | Log de buscas executadas — string, base, data, resultados |

## Estrutura de pastas

```
metodologia/
├── docs/               ← documentação do sistema metodologia
│   ├── contratos/      ← protocolos e regras
│   └── registro/       ← logs e histórico
├── texto/              ← textos produzidos (qualificacao, artigo1, tese, ...)
│   └── docs/           ← regras gerais de redação + bloco por texto
├── scripts/            ← scripts do pipeline
│   └── docs/           ← documentação de código (exportável)
└── referencias/        ← acervo de referências
    └── docs/           ← decisões sobre referências e log de buscas
```

## Política de documentos

- Todo `.md` tem frontmatter YAML com `name`, `description` e `metadata.type`
- Tipos: `indice`, `backlog`, `issues`, `contrato`, `registro`
- `backlog.md`: trabalho planejado, não urgente
- `issues.md`: impedimentos ativos com impacto identificável
- Contratos documentam decisões no padrão ADR: contexto → decisão → consequências
- Changelog: alterações em contratos vigentes são registradas no próprio documento
