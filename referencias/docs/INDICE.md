---
name: indice-referencias
description: Índice de documentação de referências — decisões sobre bases, formatos e acervo
metadata:
  type: indice
  scope: referencias
---

# Índice — referencias/

## Estrutura

```
referencias/
├── docs/
│   ├── INDICE.md              ← este arquivo
│   ├── backlog.md             ← buscas planejadas, importações pendentes
│   ├── issues.md              ← problemas de acervo (acesso, duplicata, formato)
│   ├── contratos/
│   │   └── contrato_acervo.md   ← política de importação, formatos, organização
│   └── registro/
│       └── strings_busca.md     ← log de buscas (ver metodologia/docs/registro/)
└── <frente>/                    ← H1/, H2/, H3/, H4/
    ├── triagem/                 ← CSVs exportados + planilha de triagem
    └── ris/                     ← arquivos RIS dos artigos incluídos
```

## Decisões registradas

| Decisão | Resolução |
|---|---|
| Formato bulk de busca | CSV (Scopus) — BIB bulk não estrutura bem |
| Formato canônico de importação | RIS — universal entre bases |
| Formato para LaTeX | BIB — convertido de RIS |
| Base principal | Scopus — cobre IEEE, ACM, Elsevier, Springer |
| Bases complementares | IEEE Xplore, ACM, Springer Link (uso documentado) |

## Log de buscas

Ver `docs/registro/strings_busca.md` — log centralizado de todas as buscas
executadas, independente da frente.
