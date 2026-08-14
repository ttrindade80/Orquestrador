# Relatório de Enquadramento — Observações Manuais H-0063

```yaml
rastreabilidade:
  etapa: ENQUADRAR_OBSERVACOES_MANUAIS
  perfil: GERENTE_DE_ADR_IMPLEMENTACAO
  papel_agente: pesquisador_documental_normativo_focal
  contexto_agente: LIMPO
  objeto: H-0063
  item: ITEM-0010
  adr: ADR-0046
  predecessor: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0063.md
  handoff: docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  observacoes:
    - O-H0063-MANUAL-001
    - O-H0063-MANUAL-002
  estado_factual_gates:
    VM-H0063-001: APROVADO
    VM-H0063-002: APROVADO
    VM-H0063-003: APROVADO
  alteracoes_autorizadas: nenhuma
  escopo: somente_levantamento_e_classificacao_normativa

resultado:
  status: ENQUADRAMENTO_CONCLUIDO
  O-H0063-MANUAL-001:
    classificado_como: NAO_VIOLA_REGRA_VIGENTE_APLICAVEL_AO_H0063
    e_defeito_do_h0063: false
    destino_normativo: ITEM-0024
  O-H0063-MANUAL-002:
    classificado_como: POLITICA_FUTURA_JA_DEFERIDA_SEM_ITEM_NUMERADO
    e_defeito_do_h0063: false
    destino_normativo: deferimento_H-0054_secao_10_1
    item_backlog_especifico: NAO_EXISTE
```

## 1. Objetivo e limites

Determinar, apenas por levantamento documental/normativo:

1. se `O-H0063-MANUAL-001` viola regra vigente aplicável ao H-0063;
2. se `O-H0063-MANUAL-002` é defeito do H-0063 ou já pertence a item/política futura.

Não houve alteração de código, handoff, backlog ou normativos. Os gates
`VM-H0063-001`–`003` permanecem aprovados conforme o predecessor; este
relatório não reabre a validação manual nem fecha a classificação final do
handoff.

## 2. Fatos das observações (predecessor)

Fonte: `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0063.md`.

| ID | Fato observado (síntese) |
|---|---|
| `O-H0063-MANUAL-001` | Ao paginar, a implementação não tenta manter um pai junto com todos os seus filhos quando o conjunto pai+filhos caberia em uma página; dúvida se existe regra vigente equivalente a “não iniciar o conjunto no fim da página se ele não couber inteiro no restante”. |
| `O-H0063-MANUAL-002` | Organização/exibição da Barra de Menus fora da expectativa visual; dúvida se já existe ITEM de backlog para criar/uniformizar regra de exibição/organização da barra. |

## 3. O-H0063-MANUAL-001 — paginação pai + filhos

### 3.1 Autoridades consultadas

- `docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md` (§5, §8, §9, §16)
- `docs/contratos/contrato_console.md` §12 (`politica_quebra`), §22.16–§22.17
- `docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md`
- `docs/adr/ADR-0042-navegacao-multinivel-do-console.md` §4.8, §8
- `docs/backlog.md` — `ITEM-0024`, `ITEM-0025`
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` (`politica_paginacao: com`)

### 3.2 Achados normativos

1. **H-0063 não exige “manter pai+filhos juntos”.** O handoff exige reutilizar
   `dois_niveis_por_foco`, resize/redesenho e paginação pela infraestrutura
   canônica; não define política de agrupamento visual de blocos pai+filhos
   entre páginas. Critérios de aceite (§16) e validação manual (§15) cobrem
   estrutura, navegação e resize — não continuidade de grupo na paginação.

2. **A frase “mantém junto quando possível” existe, mas em outro objeto.** Em
   `contrato_console.md` §12, `permitir_quebra_somente_se_maior_que_pagina`
   descreve a quebra de **um item** (`politica_quebra` por item): se o item
   cabe no resto da página, fica; se não cabe no resto mas cabe em página
   vazia, começa na página seguinte; se for maior que uma página, quebra.
   Isso **não** é regra de unidade semântica “pai + todos os filhos”.

3. **Paginação multinível não cria regra concorrente de agrupamento.**
   `contrato_console.md` §22.17 e ADR-0042 §4.8 subordinam a paginação das
   políticas multinível integralmente à ADR-0041 (teclas/chips
   `PageUp`/`PageDown`, `[PgUp][PgDn]`). ADR-0041 não define “não iniciar
   conjunto pai+filhos no final da página”.

4. **A capacidade desejada já está reservada a trabalho futuro.** ADR-0042 §8
   exclui expressamente “nova distribuição geométrica de grupos, compactação
   ou otimização de layout, ou **nova política de quebra entre grupos**”,
   reservados a `ITEM-0024`. O backlog descreve `ITEM-0024` como distribuição
   visual de blocos de pais e filhos multinível, incluindo **compactação local
   de um único grupo** e **continuidade entre páginas** (status `bloqueado`).

5. **`ITEM-0025` não é o destino.** Trata integração futura de
   `arvore_colapsavel` com multiline e paginação, não a política de quebra
   entre grupos de `dois_niveis_por_foco`.

### 3.3 Classificação

```yaml
id: O-H0063-MANUAL-001
classificacao: NAO_VIOLA_REGRA_VIGENTE_APLICAVEL_AO_H0063
e_defeito_implementacional_do_h0063: false
e_violacao_de_paginacao_vigente: false
exige_patch_de_h0063: false
destino: ITEM-0024
nota: >
  O comportamento observado (não agrupar pai+filhos na paginação) não
  confronta requisito vigente do H-0063 nem regra aplicável de ADR-0041/
  contrato_console sobre conjuntos pai+filhos. A expectativa de “manter
  junto quando possível” no sentido de grupo enquadra-se na política futura
  de quebra/continuidade entre grupos (ITEM-0024), não na politica_quebra
  por item do §12.
```

## 4. O-H0063-MANUAL-002 — organização/exibição da Barra de Menus

### 4.1 Autoridades consultadas

- H-0063 §6.3, §13, §16 (Barra e chips)
- `docs/contratos/contrato_barra_de_menus.md` §7 (ordem canônica), §17
  (distribuição / ordem por declaração / âncoras)
- `docs/backlog.md` (busca por ITEM de organização/exibição/uniformização da
  barra)
- `docs/handoff/H-0054-selecao-multinivel.md` §10 / §10.1 (deferimentos)
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
- `config/telas/demo/h0055_dois_niveis_por_foco.json` (precedente da política
  reutilizada)
- `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0063.md` (DESVIO-PAG-H0063)

### 4.2 Achados normativos

1. **Não há ITEM numerado no backlog ativo** cujo título/descrição seja criar
   ou uniformizar regra de organização/exibição da Barra de Menus. Busca em
   `docs/backlog.md`: nenhum `ITEM-NNNN` com esse objeto. Itens próximos
   (`ITEM-0029` ajuda/chips; `ITEM-0031` mapa de teclas F) não cobrem
   organização visual da barra.

2. **Há política/trabalho futuro já deferido, sem ITEM.** Em H-0054 §10.1
   permanecem fora de escopo e deferidos, entre outros:
   - ordenação global dos itens canônicos da barra;
   - posição global de `[✥]`;
   - algoritmo futuro que preserve ordem canônica independentemente da
     declaração.
   Relatórios de aplicação/QA da ADR-0042 P03 e patches de H-0054 reiteram
   “ordenação global da barra” como fora daquele ciclo.

3. **H-0063 não inventa barra própria.** §6.3 exige infraestrutura normal,
   ordem canônica aplicável, chips estruturais
   `[Esc]` → `[✥]` → `[␣]` → `[?]` (Ajuda último), sem Aplicar/F1–F11. O JSON
   H-0063 inclui também `[PgUp][PgDn] Páginas` (paginação `com`), na ordem
   declarada `Esc → Navegar → Páginas → Selecionar → Ajuda` — **idêntica** à
   fixture canônica `h0055_dois_niveis_por_foco.json` da política reutilizada.

4. **Ordem canônica §7 × ordem por declaração.** O contrato fixa a sequência
   semântica `[Esc] → [PgUp][PgDn] → … → [✥] → [␣] → … → [?]`, mas §17 também
   fixa que, com `ordem.politica = "declaracao"`, o renderer usa
   `barra_de_menus.chips[]` e **não reordena** para corrigir; âncoras são
   validação, não auto-correção. O algoritmo que faria a ordem canônica
   prevalecer sobre a declaração é exatamente o deferimento de H-0054 §10.1.

5. **QA de implementação não tratou a barra H-0063 como defeito.**
   `DESVIO-PAG-H0063` foi classificado Caso A: presença de `[PgUp][PgDn]
   Páginas` compatível com a infraestrutura canônica.

6. **Texto residual em contrato ≠ ITEM de backlog.** `contrato_barra_de_menus.md`
   §17 ainda menciona “pendência de handoff futuro” para a implementação da
   distribuição horizontal responsiva; os ciclos H-0016/H-0017/H-0018 já
   fecharam essa implementação. Isso não constitui ITEM ativo de
   organização/exibição no `docs/backlog.md`.

### 4.3 Classificação

```yaml
id: O-H0063-MANUAL-002
classificacao: POLITICA_FUTURA_JA_DEFERIDA_SEM_ITEM_NUMERADO
e_defeito_implementacional_do_h0063: false
pertence_a_item_especifico_do_backlog: false
item_backlog_encontrado: null
destino: >
  Deferimento documental H-0054 §10.1 (ordenação global da barra / algoritmo
  futuro de preservação da ordem canônica independentemente da declaração),
  ainda sem ITEM-NNNN no backlog ativo.
nota: >
  A expectativa de organização/exibição uniforme da Barra de Menus não se
  enquadra como defeito do escopo estrutural do H-0063: a barra segue o
  precedente H-0055 da política dois_niveis_por_foco e os critérios locais do
  handoff. A lacuna sistêmica (ordem canônica §7 vs ordem declarada, sem
  reordenação automática) já estava deferida antes do H-0063. A recordação de
  “ITEM de backlog” corresponde a trabalho futuro documentado, mas não a um
  ITEM-NNNN presente em docs/backlog.md.
```

## 5. Síntese para o gerente

| Observação | Viola regra vigente do H-0063? | É defeito do H-0063? | Destino |
|---|---|---|---|
| `O-H0063-MANUAL-001` | Não | Não | `ITEM-0024` (quebra/continuidade entre grupos multinível) |
| `O-H0063-MANUAL-002` | Não (no enquadramento deste levantamento) | Não | Política futura já deferida em H-0054 §10.1; **sem** ITEM numerado no backlog ativo |

Implicação gerencial sugerida (sem executar): as duas observações **não
bloqueiam** a aprovação do H-0063 por violação de regra aplicável a este
handoff; podem ser registradas como fora de escopo / trabalho futuro nos
destinos acima na etapa de classificação final.

## 6. Buscas executadas

```yaml
buscas:
  - padrao: O-H0063-MANUAL-00[12]|VM-H0063
  - padrao: manter junto|quebra entre grupos|continuidade entre paginas|compactacao local
  - padrao: politica_quebra|permitir_quebra_somente_se_maior_que_pagina
  - padrao: ITEM-0023|ITEM-0024|ITEM-0025|DEFINICOES_DIFERIDAS
  - padrao: organiza.*barra|barra.*organiza|ordenação global da barra|ordem canônica independentemente
  - padrao: Barra de Menus|barra_de_menus (backlog.md e HISTORICO.md)
  - artefatos_lidos_integrais_ou_focais:
      - RELATORIO_VALIDACAO_MANUAL_H-0063.md
      - H-0063 (seções de escopo, barra, fora de escopo, aceite)
      - contrato_console.md §12 e §22.16–22.17
      - ADR-0042 §4.8 e §8
      - backlog ITEM-0024/0025
      - contrato_barra_de_menus.md §7 e §17
      - H-0054 §10.1
      - h0063 e h0055 JSON (chips)
```

## 7. Bloqueios

Nenhum. Classificação normativa das duas observações concluída sem alteração
de artefatos operacionais.
