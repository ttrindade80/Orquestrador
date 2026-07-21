---
name: nomenclatura-lancador
description: Terminologia do lançador — tipo de elemento do corpo para navegação, itens, fila, matriz, grandezas de largura mínima funcional
metadata:
  type: nomenclatura
  scope: lancador
  fase_de_aplicacao: VIGENTE
---

# Lançador

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário dos termos de:
- lançador como tipo de elemento do corpo;
- tela de destino;
- item do lançador e suas partes;
- fila (modo de uma linha);
- matriz do lançador (modo de múltiplas colunas);
- coluna do lançador;
- vão do lançador;
- largura mínima funcional;
- `area_lancador_w`;
- `lancador_caixa_min_w`;
- `coluna_minima_content_w`;
- fallback específico do lançador (quadro mínimo por insuficiência de área).

Histórico da mudança `menu` para `lancador` está no módulo `90` e no relatório
histórico.

## 3. Termos proprietários

- `lancador` (tipo de elemento)
- `tela_destino`
- item do lançador: `chip`, `texto`, `tela_destino`
- fila (modo `distribuicao_lancador = "fila"`)
- matriz do lançador (modo `distribuicao_lancador = "matriz"`)
- `distribuicao_lancador`
- vão (no contexto do lançador)
- coluna do lançador
- `area_lancador_w`
- `lancador_caixa_min_w`
- `coluna_minima_content_w`
- `content_w` (domínio de conteúdo do lançador)
- `quadro mínimo global acionado por inviabilidade do lancador`
- `fallback local do lancador` (proibido)
- `recuperação automática por redesenho`

## 4. Definições

### 4.1 Lançador como tipo de elemento

O `lancador` é um tipo de elemento do corpo. Cada instância tem título e uma
lista de itens. Aciona navegação para outra tela via `tela_destino`. Não executa
processo, não filtra dado, não altera estado.

**Termo canônico**: `lancador`. Substituiu `menu` em 2026-07-06.
Ver módulo `90` para o histórico da substituição.

### 4.2 Estrutura mínima do item

| Parte | Descrição |
|---|---|
| `chip` | Identificador visual de ação (ex.: `[A]`) |
| `texto` | Rótulo do item — máximo 15 caracteres |
| `tela_destino` | Campo formal que identifica a tela a ser aberta |

**Regra do texto**: texto acima de 15 caracteres é **rejeitado em verificação**
— não é truncado nem abreviado. A regra normativa completa está em
`contrato_lancador.md`.

### 4.3 Modos de distribuição

| Modo | Descrição |
|---|---|
| fila | Linha única horizontal — todos os itens em uma linha |
| matriz | Múltiplas colunas — calculado automaticamente pela largura real do terminal |

O modo é calculado automaticamente (ADR-0001); não é declarado pela classe nem
ajustável manualmente via chip.

**Coluna do lançador**: a largura de cada coluna é definida pelo maior item
daquela coluna específica (não pelo maior item do lançador inteiro).

### 4.4 Grandezas de largura (ADR-0023)

| Termo | Definição normativa |
|---|---|
| `area_lancador_w` | Largura total efetivamente alocada ao elemento `lancador` pela composição — inclui bordas e padding externos da caixa completa |
| `lancador_caixa_min_w` | Largura mínima total da caixa do `lancador`; inclui as unidades estruturais obrigatórias (bordas e padding externos). Relação: `lancador_caixa_min_w = coluna_minima_content_w + largura_estrutural_da_caixa` |
| `coluna_minima_content_w` | Largura mínima do conteúdo necessária para representar integralmente uma coluna válida completa, sem bordas nem padding externo da caixa |
| `coluna válida completa` | Coluna cujo conteúdo — chip, vão e texto — cabe integralmente na largura disponível, com todos os itens visíveis e sem truncamento, overflow, omissão ou paginação |
| `content_w` | Largura de conteúdo do `lancador`, obtida descontando bordas e padding externos de `area_lancador_w`; é o domínio de comparação com `coluna_minima_content_w` |
| `quadro mínimo global acionado por inviabilidade do lancador` | O mesmo `quadro mínimo de terminal pequeno` (ADR-0017) acionado quando `area_lancador_w < lancador_caixa_min_w`, mesmo que `terminal_w` seja maior |
| `fallback local do lancador` | **Proibido.** Nenhum estado visual, mensagem, truncamento ou variante restrita à caixa do `lancador` é permitido |
| `recuperação automática por redesenho` | A cada redesenho, quando `area_lancador_w >= lancador_caixa_min_w`, o quadro mínimo desaparece e a tela normal é reconstruída |

### 4.5 Distinções de largura obrigatórias

| Termo | Significado | Não confundir com |
|---|---|---|
| `area_lancador_w` | Largura total da caixa alocada ao `lancador` (inclui bordas/padding) | `coluna_minima_content_w` (grandeza de conteúdo, exclui bordas/padding) |
| `lancador_caixa_min_w` | Largura mínima da caixa (inclui bordas/padding) | `coluna_minima_content_w` (largura de conteúdo) |
| `coluna_minima_content_w` | Largura mínima do conteúdo para coluna válida (exclui bordas/padding) | `area_lancador_w` ou `lancador_caixa_min_w` (são larguras de caixa) |
| `terminal_w` | Largura total do terminal | Qualquer grandeza interna do `lancador` — não comparável diretamente |

### 4.6 Parametrização — `config/elementos/lancador.json`

Os valores de vão, alinhamento e linhas mínimas do lançador vivem em
`config/elementos/lancador.json`, não hardcoded. A especificação normativa
completa está em `contrato_lancador.md`.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `lancador` × `barra_de_menus` | Lançador: elemento do corpo para navegação; barra: região fixa inferior da tela — não são intercambiáveis |
| `lancador` × `console` | Lançador aciona navegação; console é container interativo de dados |
| modo fila × modo matriz | Fila: linha única; matriz: múltiplas colunas — calculados automaticamente pela largura |
| matriz do lançador × `distribuição matricial` (ADR-0025) | Matriz do lançador é modo de layout interno do tipo de elemento lançador; distribuição matricial (módulo `41`) é capacidade genérica configurável de elementos |
| `fallback local do lancador` × `quadro mínimo global` | O fallback local é **proibido**; somente o quadro mínimo global é permitido |

## 6. Relação com contratos

- `contrato_lancador.md`: autoridade do comportamento normativo completo.
- `contrato_composicao_corpo.md`: composição do corpo que inclui o lançador.

## 7. Relação com ADRs

- ADR-0001: lançador suporta modo matriz.
- ADR-0002: sobra à direita no lançador.
- ADR-0003: vãos elásticos.
- ADR-0005: lançador não é corpo navegável por `[✥]`.
- ADR-0023: largura mínima funcional; grandezas de largura.

## 8. Aliases ou termos descontinuados relacionados

- `menu` (corpo) → descontinuado; substituído por `lancador` (decisão 2026-07-06).
  Ver módulo `90` e relatório histórico.
- `config/lancador.json` → caminho inicial histórico, migrado para
  `config/elementos/lancador.json` (ADR-0021). Ver módulo `90`.

## 9. Conteúdo que não pertence a este módulo

- Largura de tela em geral → módulo `21`.
- `quadro mínimo de terminal pequeno` (definição geral) → módulo `21`.
- Algoritmo de cálculo de colunas (regra comportamental completa) →
  `contrato_lancador.md`.
- Distribuição matricial genérica → módulo `41`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§8 (linhas 893-986), §13 (linhas 1146-1215), §6.3 (linhas 786-823)"
  intervalo_ou_bloco: "NOM-LEV-014, NOM-LEV-020, NOM-LEV-012 (parcial)"
origem_normativa: ADR-0001, ADR-0002, ADR-0003, ADR-0005, ADR-0023
contratos_relacionados:
  - contrato_lancador.md
  - contrato_composicao_corpo.md
adrs_relacionadas:
  - ADR-0001
  - ADR-0002
  - ADR-0003
  - ADR-0005
  - ADR-0023
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
  - CLASSIFICADO_COMO_HISTORICO
partes_NAO_CONFIRMADAS: []
```
