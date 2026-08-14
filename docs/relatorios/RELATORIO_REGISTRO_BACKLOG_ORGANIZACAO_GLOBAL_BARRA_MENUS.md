# Relatório — Registro de backlog: organização global da Barra de Menus

```yaml
rastreabilidade:
  perfil: GERENTE_DE_ADR_IMPLEMENTACAO
  etapa: REGISTRAR_ITEM_BACKLOG
  papel: executor_documental_focal
  contexto_agente: LIMPO
  objeto: organizacao_global_barra_de_menus
  item_criado: ITEM-0032
  origens:
    - H-0054 §10.1
    - O-H0063-MANUAL-002
    - RELATORIO_CLASSIFICACAO_FINAL_VALIDACAO_MANUAL_H-0063.md
  premissas:
    h0063: VALIDACAO_MANUAL_APROVADA_FINAL
    item_numerado_preexistente: false
```

## Baseline Git observada

- Branch: `master`.
- HEAD: `77bd8bf3772985325bc51a850f7c6d76d61ad573`.
- Stage: vazio no início desta etapa.

## Objetivo da etapa

Materializar no backlog ativo uma entrada própria para a organização/ordenação
global da Barra de Menus, de modo que o trabalho deixe de existir apenas como
deferimento histórico (H-0054 §10.1) e como observação enquadrada
(`O-H0063-MANUAL-002` → `TRABALHO_FUTURO_DEFERIDO`).

## Escopo autorizado e exclusões

Autorizado:

- criar `ITEM-NNNN` novo em `docs/backlog.md`;
- produzir este relatório.

Fora desta etapa (não executado):

- alterar H-0063;
- implementar a funcionalidade;
- criar ADR;
- fechar ITEM-0010;
- commit ou push.

## Verificação de ID

Busca por `ITEM-0032` no repositório: nenhum resultado prévio.
Maior identificador ativo em `docs/backlog.md` antes do registro: `ITEM-0031`.
Identificador atribuído: `ITEM-0032`.

## Item registrado

### ITEM-0032 — Organização global da Barra de Menus

| Campo | Valor |
|---|---|
| Tipo | `implementacao` |
| Prioridade | `media` |
| Status | `planejado` |
| Cobertura | ordenação global dos itens canônicos; posição global de `[✥]`; algoritmo que preserve a ordem canônica independentemente da declaração |
| Origem | H-0054 §10.1; `O-H0063-MANUAL-002` |
| Próxima ação | levantamento focal e especificação própria, sem ADR nem implementação nesta etapa |

Relações explícitas de não-cobertura:

- não altera H-0063;
- não fecha ITEM-0010;
- não cobre `ITEM-0029` (Ajuda/F1);
- não cobre `ITEM-0031` (mapa de teclas F).

## Preservações

- H-0063: não tocado.
- ITEM-0010: permanece `em_andamento`; não fechado.
- Demais itens do backlog: sem alteração de conteúdo nesta etapa, além da
  inserção do bloco `ITEM-0032` ao final da lista ativa.
- Nenhuma ADR, handoff, contrato, nomenclatura, código ou configuração foi
  criada ou alterada.

## Arquivos efetivamente tocados

- `docs/backlog.md` — inserção de `ITEM-0032`.
- `docs/relatorios/RELATORIO_REGISTRO_BACKLOG_ORGANIZACAO_GLOBAL_BARRA_MENUS.md`
  — este relatório.

## Validação

- `git diff --check` nos arquivos desta etapa: passou (exit 0).

## Resultado

```yaml
resultado:
  status: BACKLOG_ITEM_REGISTERED
  item: ITEM-0032
  titulo: Organização global da Barra de Menus
  status_item: planejado
  deferimento_historico_promovido_a_item: true
  h0063_alterado: false
  item_0010_fechado: false
  adr_criada: false
  implementacao_executada: false
```
