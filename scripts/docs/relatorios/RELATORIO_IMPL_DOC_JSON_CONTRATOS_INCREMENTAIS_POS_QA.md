# Relatório de Implementação — Correção pós-QA contratos JSON incrementais

## Status

IMPLEMENTATION_COMPLETED

## Achado corrigido

**Achado bloqueante 1** (`contrato_json_tela_minima.md` tornava `corpo.arranjo`
obrigatório, contradizendo a regra ativa que permite `arranjo` não declarado e
uso de `tiling` do estilo como default).

Evidência do achado (fonte: `RELATORIO_AUDITORIA_DOC_JSON_CONTRATOS_INCREMENTAIS.md`):

- `contrato_json_tela_minima.md` seção 5 listava `corpo.arranjo` como campo obrigatório.
- `contrato_composicao_corpo.md` seção 4.2 admite `arranjo` como
  `sobreposto | lado_a_lado | (não declarado)`.
- `contrato_composicao_corpo.md` seção 5.6 define que, quando `tela.json` não
  declara `arranjo`, o renderer consulta `tiling` do estilo ativo.
- `NOMENCLATURA.md` seção 1.4 também preserva `tiling` como default quando a
  classe não especifica arranjo fixo.

## Arquivos alterados

- `docs/contratos/contrato_json_tela_minima.md`

## Arquivos preservados

- `docs/contratos/contrato_json_cabecalho.md` — inalterado
- `docs/contratos/contrato_json_barra_de_menus.md` — inalterado
- `docs/contratos/contrato_json_lancador.md` — inalterado
- `docs/contratos/contrato_json_dashboard.md` — inalterado
- `docs/contratos/contrato_json_console.md` — inalterado
- `docs/INDICE.md` — inalterado
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` — inalterado
- `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` — inalterado
- `docs/NOMENCLATURA.md` — inalterado
- `docs/contratos/contrato_composicao_corpo.md` — inalterado
- `docs/contratos/contrato_tela_json.md` — inalterado
- `docs/contratos/contrato_estilo.md` — inalterado
- `tela/` — não tocado
- `config/` — não tocado
- Qualquer arquivo Python — não tocado

## Regra antes

**Seção 4 — JSON mínimo**: o exemplo JSON apresentava `"arranjo": "sobreposto"`
dentro de `corpo`, tratando o campo como parte obrigatória do envelope mínimo.

**Seção 5 — Campos obrigatórios**: a tabela continha a linha:

```
| `corpo.arranjo` | string | Valor de arranjo dos elementos do corpo.
`"sobreposto"` é o valor mínimo quando há um único elemento; `"lado_a_lado"`
quando há dois ou mais que se dispõem horizontalmente. |
```

Isso tornava `corpo.arranjo` obrigatório e eliminava, para o JSON mínimo, a
alternativa ativa de omitir `arranjo` e usar `tiling` do estilo como default.

## Regra depois

**Seção 4 — JSON mínimo**: o exemplo JSON apresenta apenas `corpo.elementos[]`,
sem `arranjo`. Observação explicita que `corpo.arranjo` é campo permitido mas
opcional; quando ausente, o renderer usa `tiling` do estilo ativo (seção 5.6
de `contrato_composicao_corpo.md`); o renderer não inventa arranjo nem decide
composição por largura de terminal.

Uma subseção `4.1 Exemplo com arranjo explícito (opcional)` exibe o JSON com
`arranjo` declarado, deixando claro que essa é uma fixação explícita da tela,
não requisito do envelope mínimo.

**Seção 5 — Campos obrigatórios**: a linha de `corpo.arranjo` foi removida da
tabela de campos obrigatórios. Uma subseção `5.1 Campo opcional corpo.arranjo`
foi adicionada, contendo:

- tabela com valores permitidos e regra das duas camadas de decisão;
- regra de que `arranjo` é relevante apenas para 2+ elementos `console`/`lancador`;
- regra de que `arranjo` não decide posição do `dashboard`;
- regra de que o renderer não inventa arranjo nem cria fallback próprio.

## Evidência de aderência contratual

| Contrato / ADR | Regra | Aderência após correção |
|---|---|---|
| `contrato_composicao_corpo.md` seção 4.2 | `arranjo` aceita `sobreposto`, `lado_a_lado` ou *(não declarado)* | Aderente — JSON mínimo não declara `arranjo` |
| `contrato_composicao_corpo.md` seção 5.6 | Quando `tela.json` não declara `arranjo`, renderer usa `tiling` do estilo ativo | Aderente — explicitado nas seções 4 e 5.1 |
| `contrato_composicao_corpo.md` R-12 | Renderer não consulta `tiling` quando `tela.json` já declarou `arranjo` explicitamente | Aderente — seção 4.1 e 5.1 descrevem a prioridade |
| `contrato_estilo.md` seção 3.4 | `tiling` é preferência manual do usuário; renderer não sobrescreve por largura de terminal | Aderente — seção 5.1 proíbe explicitamente fallback por largura |
| `contrato_tela_json.md` seção 8 | `corpo` contém "tiling ou arranjo equivalente" + `elementos[]` | Aderente — envelope mínimo preserva `elementos[]`; `arranjo` é equivalente declarativo, não obrigatório |
| `contrato_composicao_corpo.md` seções 4.3 e R-9 | `arranjo`/`tiling` não afetam posição do `dashboard` | Aderente — seção 5.1 afirma explicitamente |
| ADR-0008 ponto 3 | JSON da tela é fonte de composição; renderer não hardcoda | Aderente — nenhum fallback por código é autorizado |

## Comandos executados

```bash
git status --short
git diff --stat
git diff -- docs/contratos/contrato_json_tela_minima.md
```

Nota: `contrato_json_tela_minima.md` é arquivo não rastreado (`??`), portanto
`git diff` não exibe seu conteúdo. O diff efetivo está nas alterações descritas
nas seções "Regra antes" e "Regra depois" acima.

## Conclusão

O achado bloqueante foi corrigido exclusivamente em `docs/contratos/contrato_json_tela_minima.md`.
Nenhum outro arquivo foi alterado. O envelope mínimo agora é compatível com os
contratos ativos: `corpo.arranjo` é campo permitido/opcional; quando não
declarado, o renderer usa `tiling` do estilo ativo; o renderer não inventa
arranjo nem decide composição por largura de terminal.

O achado não bloqueante (`contrato_json_barra_de_menus.md`, ambiguidade de
`acao` como string) não foi corrigido nesta tarefa — a instrução de escopo
proibiu alteração dos demais contratos, e o achado não bloqueante não é
impedimento para aprovação.
