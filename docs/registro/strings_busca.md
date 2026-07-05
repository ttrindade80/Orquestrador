---
name: registro-strings-busca
description: Log de buscas executadas — string exata, base, data, resultados e arquivo exportado
metadata:
  type: registro
  scope: referencias
---

# Log de Strings de Busca

Toda busca executada é registrada aqui antes de qualquer triagem.
Registrar antes de abrir o CSV — nunca reconstruir após o fato.

## Campos obrigatórios por entrada

| Campo | Descrição |
|---|---|
| `id` | Identificador sequencial (B001, B002, ...) |
| `hipotese` | H1 / H2 / H3 / H4 / geral |
| `base` | Scopus / IEEE / ACM / Springer / outro |
| `data` | Data de execução (YYYY-MM-DD) |
| `string` | String exata copiada do campo de busca |
| `filtros` | Período, tipo de documento, idioma, campo de busca |
| `n_resultados` | Número de registros retornados |
| `n_exportados` | Número de registros exportados (pode diferir se base limita) |
| `arquivo` | Nome do arquivo CSV exportado |
| `notas` | Decisões tomadas, refinamentos, motivo de descartar |

## Template

```markdown
### B001
- **Hipótese**: H1
- **Base**: Scopus
- **Data**: YYYY-MM-DD
- **String**: `TITLE( ) AND ...`
- **Filtros**: 2019–2026, Article + Conference Paper, inglês
- **Resultados**: N
- **Exportados**: N
- **Arquivo**: `scopus_H1_B001_YYYYMMDD.csv`
- **Notas**:
```

---

_Nenhuma busca registrada._
