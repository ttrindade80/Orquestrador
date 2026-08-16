---
name: relatorio-aplicacao-adr-0047
description: Relatorio de aplicacao documental da ADR-0047 (formatacao dos filhos de dois_niveis_por_foco)
metadata:
  type: relatorio
  scope: orquestrador
  etapa: APLICAR_ADR
  status: ADR_APPLIED
---

# Relatório — Aplicação da ADR-0047

## 1. Identificação

- etapa: `APLICAR_ADR`
- status: `ADR_APPLIED`
- ADR aplicada: `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
- status transportado do QA: `ADR_APPROVED` (QA-ADR-0047-001 resolvido no P01;
  localização, cardinalidade e literais do schema fechados em §4.13)

## 2. Contratos alterados

- `docs/contratos/contrato_tela_json.md` — nova seção 36: materializa o
  schema literal do bloco `formato.dois_niveis_por_foco.filho` do elemento
  `console` (tabulação, designador, apresentação e tabela), no mesmo local
  estrutural do precedente `formato.excesso.politica_modo` (§33.6.1).
- `docs/contratos/contrato_console.md` — nova seção 25: propaga o
  comportamento (ordem física `tabulacao → ec → tg → designador →
  conteúdo`, deslocamento em unidade inteira, escolha do valor efetivo de
  tabulação e espaçamento pelo renderer, apresentação tabular local sem
  cabeçalho/borda/título, alinhamento global de colunas entre todos os
  filhos do console, quebra preservando o item lógico, resize).
- `docs/contratos/contrato_json_console.md` — nova seção 15: apenas
  clarificação de fronteira — o documento externo de conteúdo não declara
  tabulação, apresentação tabular, colunas nem espaçamento; os campos
  referenciados por `tabela.colunas[].campo` continuam pertencendo
  exclusivamente ao conteúdo. Nenhum schema estrutural foi introduzido
  nesta seção.

## 3. Módulos de nomenclatura alterados

- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` —
  nova subseção 4.6 com os termos de apresentação dos filhos de
  `dois_niveis_por_foco`, tabulação pai→filho, apresentação tabular local,
  colunas e espaçamento entre colunas; duas novas distinções obrigatórias
  (configuração de apresentação × conteúdo/dados; apresentação tabular
  local × `tabela` como política de navegação); remissão à ADR-0047 em §7.
- `docs/nomenclatura/32_CONSOLE.md` — nova subseção 4.11 com o termo
  proprietário "unidade inteira do filho deslocada", preservando `ec`,
  `tg` e item lógico sem redefinição; remissão à ADR-0047 em §7; uma nova
  linha na tabela de distinções (§5). Terminologia de apresentação
  (tabulação, tabela local, colunas, espaçamento) não foi movida para este
  módulo — permanece exclusiva do módulo `44`.

## 4. Arquivos avaliados e preservados

- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` —
  avaliado; nenhuma alteração necessária, pois a ADR reutiliza a regra
  vigente de resize que preserva o item lógico.
- `docs/nomenclatura/10_ESTILO.md`, `docs/contratos/contrato_estilo.md`,
  `config/estilo.json` — não avaliados para alteração, por instrução
  explícita do escopo; nenhuma semântica de Estilo foi tocada.
- `config/telas/demo/h0055_dois_niveis_por_foco.json`,
  `..._conteudo.json`, `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
  — não alterados; reconciliação pertence à implementação futura.
- `docs/backlog.md` — não alterado; ADR-0047 não possui ITEM canônico
  fechado.

## 5. Separação configuração × conteúdo

Propagada integralmente: o schema declarativo (tabulação, designador,
apresentação, colunas, espaçamento) pertence exclusivamente ao elemento
`console` do JSON estrutural da tela (`contrato_tela_json.md` §36); o
documento externo de conteúdo fornece somente dados semânticos
(`contrato_json_console.md` §15); o renderer calcula toda a geometria
física, sem persistência de resultado calculado em nenhum dos dois
documentos (`contrato_console.md` §25).

## 6. Schema literal materializado

`formato.dois_niveis_por_foco.filho` com `tabulacao{minimo,maximo}`,
`designador{tipo}`, `apresentacao("texto"|"tabela")` e, quando tabular,
`tabela.colunas[].campo` e `tabela.espacamento{minimo,maximo}` — idêntico
ao fechado por ADR-0047 §4.13, sem decisão nova.

## 7. Verificações

- Todo arquivo alterado pertence ao manifesto de arquivos permitidos.
- `git diff --check` executado sobre os sete arquivos alterados/criados.
- Existência material deste relatório confirmada.
- Nenhuma decisão D-DNF-01 a D-DNF-11 nem o schema fechado no P01 foi
  reaberta ou alterada.

## 8. Bloqueios

nenhum

## delta_terminologico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
    - docs/nomenclatura/32_CONSOLE.md
  termos_adicionados:
    - apresentação dos filhos de dois_niveis_por_foco
    - tabulação pai→filho
    - apresentação tabular local de filhos
    - colunas da apresentação tabular local
    - espaçamento entre colunas
    - unidade inteira do filho deslocada
  termos_alterados: []
  distincoes_adicionadas:
    - configuração de apresentação × conteúdo/dados
    - apresentação tabular local × tabela como política de navegação
    - unidade inteira do filho deslocada × ec/tg individualmente
  fronteiras_alteradas:
    - contrato_json_console.md §15 (documento externo não recebe schema de apresentação)
```
\n