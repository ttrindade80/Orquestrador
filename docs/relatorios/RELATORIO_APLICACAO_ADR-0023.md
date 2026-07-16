# Relatório de Aplicação da ADR-0023

```yaml
etapa: APLICAR_ADR
adr: ADR-0023
status: CONCLUIDA
data: 2026-07-15
executor: aplicacao_documental
```

---

## 1. Identificação da etapa

Etapa: `APLICAR_ADR`

Esta etapa propaga a decisão aprovada da ADR-0023 nos documentos normativos
ativos. Nenhum código foi implementado, nenhum teste foi alterado, nenhum
handoff foi corrigido, nenhum commit foi preparado.

---

## 2. ADR aplicada

```yaml
arquivo: docs/adr/ADR-0023-largura-minima-funcional-lancador.md
status_da_adr: aceita
data_da_adr: 2026-07-15
```

A ADR permaneceu inalterada durante toda a aplicação. O arquivo permanece
como item não rastreado (`??`) no Git — seu conteúdo não foi tocado.

---

## 3. QA que aprovou a ADR

```yaml
arquivo: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: APROVADA_COM_OBSERVACOES
achados_anteriores_corrigidos:
  - QA-ADR0023-BLOQUEANTE-001
  - QA-ADR0023-ALTO-001
  - QA-ADR0023-MEDIO-001
achado_remanescente:
  - QA-POS-ADR0023-BAIXO-001
```

O relatório QA pós-patch permaneceu inalterado durante a aplicação.

---

## 4. Decisão propagada

A ADR-0023 registra que, quando a área total alocada ao `lancador` não
comportar nem uma coluna válida completa:

1. Nenhuma representação válida do `lancador` deve ser renderizada.
2. O renderer deve acionar o quadro mínimo canônico global já existente
   (`quadro mínimo de terminal pequeno`, ADR-0017).
3. Toda a tela ou sessão TUI normal deve ser substituída integralmente.
4. Nenhum componente da tela normal permanece visível.
5. Não deve existir mensagem ou fallback local dentro da caixa do `lancador`.
6. Não deve ser criada mensagem específica.
7. Não deve haver truncamento, overflow, paginação, rolagem, omissão ou perda
   de itens.
8. O estado deve ser reavaliado em cada redesenho.
9. Quando uma coluna válida voltar a caber, a tela normal deve ser
   reconstruída automaticamente.
10. O `lancador` deve voltar à distribuição válida em `fila` ou `matriz`,
    conforme a largura atual.

A ADR distingue cinco grandezas de largura:

```text
terminal_w
area_lancador_w
lancador_caixa_min_w
content_w
coluna_minima_content_w
```

Comparações normativas compatíveis:

```text
content_w < coluna_minima_content_w     (domínio do conteúdo)
```

equivale, no domínio da caixa, a:

```text
area_lancador_w < lancador_caixa_min_w  (domínio da caixa completa)
```

---

## 5. Estado Git inicial

```text
 M docs/NOMENCLATURA.md         — (não existia)
 M docs/adr/INDICE_ADR.md       — (não existia)
 M docs/contratos/contrato_composicao_corpo.md  — (não existia)
 M docs/contratos/contrato_lancador.md          — (não existia)
 M docs/contratos/contrato_tela_json.md         — (não existia)
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? tela/__pycache__/
```

Na abertura da etapa, os cinco arquivos autorizados eram arquivos rastreados
(`M` = Modified in worktree). O stage estava vazio. A ADR, o handoff e os
relatórios de QA eram todos `??` (não rastreados, portanto não modificados
pelas etapas anteriores).

---

## 6. Lista nominal dos arquivos alterados

| Arquivo | Operação |
|---|---|
| `docs/contratos/contrato_lancador.md` | Alterado |
| `docs/contratos/contrato_tela_json.md` | Alterado |
| `docs/contratos/contrato_composicao_corpo.md` | Alterado |
| `docs/NOMENCLATURA.md` | Alterado |
| `docs/adr/INDICE_ADR.md` | Alterado |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md` | Criado |

---

## 7. Resumo das alterações por arquivo

### 7.1 `docs/contratos/contrato_lancador.md`

- Frontmatter: adicionado `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
  à lista `adrs_aplicadas`.
- Nova subseção **6.7 Largura mínima funcional e fallback global (ADR-0023)**:
  define as quatro grandezas de largura (`terminal_w`, `area_lancador_w`,
  `lancador_caixa_min_w`, `coluna_minima_content_w`); declara as comparações
  normativas em domínios compatíveis; registra a fórmula de
  `coluna_minima_content_w`; define a sequência normativa de decisão do
  renderer; lista as proibições de fallback local; declara a recuperação
  automática.
- Novas regras **R-11** (grandezas no mesmo domínio), **R-12** (fallback
  global quando coluna mínima não couber), **R-13** (proibição absoluta de
  fallback local) e **R-14** (recuperação automática por redesenho).
- Novos critérios de validação correspondentes às regras R-11 a R-14.

### 7.2 `docs/contratos/contrato_tela_json.md`

- Frontmatter: adicionado `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
  à lista `adrs_aplicadas`.
- Nova subseção **"Área do `lancador` insuficiente por composição (ADR-0023)"**
  dentro da seção 24, após "Terminal pequeno demais": declara que
  `area_lancador_w < lancador_caixa_min_w` é gatilho independente do mesmo
  quadro mínimo canônico global; explicita que o resultado é global (toda a
  tela normal substituída); confirma que nenhum campo JSON novo é introduzido;
  descreve a recuperação pelo mesmo mecanismo reativo; restringe a regra ao
  `lancador`.

### 7.3 `docs/contratos/contrato_composicao_corpo.md`

- Frontmatter: adicionado `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
  à lista `adrs_aplicadas`.
- Novo parágrafo **"Área do `lancador` insuficiente como gatilho global
  (ADR-0023)"** na seção 5.10, após o parágrafo "Terminal pequeno demais
  (ADR-0017)": declara que a insuficiência de `area_lancador_w` torna a
  composição inválida para produzir tela normal; eleva o resultado ao quadro
  mínimo global; proíbe truncamento, estado local e mensagem local; descreve
  a recuperação automática; restringe a regra ao `lancador`.
- Nova regra **R-33** na seção 7: registra o gatilho por `area_lancador_w`,
  o alcance global, a proibição de estado local e a recuperação automática.
- Três novos critérios de validação na seção 8, correspondentes à R-33.

### 7.4 `docs/NOMENCLATURA.md`

- Nova subseção **6.3 Grandezas de largura do `lancador` e gatilho por área
  interna (ADR-0023)**: tabela de termos com definições de `area_lancador_w`,
  `lancador_caixa_min_w`, `coluna_minima_content_w`, `coluna válida completa`,
  `content_w`, `quadro mínimo global acionado por inviabilidade do lancador`,
  `fallback local do lancador` (proibido) e `recuperação automática por
  redesenho`; tabela de distinções obrigatórias entre as grandezas; regras
  normativas derivadas da ADR-0023.

### 7.5 `docs/adr/INDICE_ADR.md`

- Nova linha na tabela de decisões registradas para ADR-0023: ID, título,
  estado `aceita`, data `2026-07-15`, resumo da decisão com referência ao
  quadro mínimo global e ao `lancador`.

---

## 8. Trechos e seções afetadas

| Arquivo | Seção afetada |
|---|---|
| `contrato_lancador.md` | Frontmatter `adrs_aplicadas`; nova seção 6.7; regras R-11 a R-14; critérios de validação |
| `contrato_tela_json.md` | Frontmatter `adrs_aplicadas`; seção 24 (nova subseção após "Terminal pequeno demais") |
| `contrato_composicao_corpo.md` | Frontmatter `adrs_aplicadas`; seção 5.10 (novo parágrafo); seção 7 (nova R-33); seção 8 (três novos critérios) |
| `NOMENCLATURA.md` | Seção 6 (nova subseção 6.3 após 6.2) |
| `INDICE_ADR.md` | Tabela "Decisoes registradas" (nova linha ADR-0023) |

---

## 9. Distinção das grandezas de largura

As seguintes grandezas foram introduzidas e são distintas:

```text
terminal_w          : largura total do terminal ou viewport
area_lancador_w     : largura total da caixa alocada ao lancador (inclui bordas e padding)
lancador_caixa_min_w: largura mínima total da caixa do lancador (inclui bordas e padding)
content_w           : largura de conteúdo (area_lancador_w menos bordas e padding)
coluna_minima_content_w: largura mínima do conteúdo para uma coluna válida (exclui bordas e padding)
```

Comparação normativa correta:

```text
content_w < coluna_minima_content_w     (mesmo domínio — conteúdo)
area_lancador_w < lancador_caixa_min_w  (mesmo domínio — caixa completa)
```

Comparações proibidas:

```text
terminal_w < coluna_minima_content_w          (domínios diferentes)
area_lancador_w < coluna_minima_content_w     (domínios diferentes sem conversão)
```

Nenhuma dessas grandezas é confundida com as demais em nenhum dos documentos
alterados.

---

## 10. Tratamento global do quadro mínimo

Em todos os documentos alterados, o quadro mínimo é tratado como substituto
integral de toda a tela ou sessão TUI normal. O alcance visual é descrito
como idêntico ao da ADR-0017: cabeçalho, corpo, `lancador`, dashboards e
`barra_de_menus` não são exibidos. Nenhum texto nos documentos alterados
permite interpretar o quadro mínimo como restrito à área ou caixa do
`lancador`.

---

## 11. Proibições preservadas

As seguintes proibições foram explicitamente propagadas e verificadas:

- Fallback local restrito ao `lancador`: proibido em todos os documentos.
- Truncamento de textos ou chips para forçar encaixe: proibido.
- Overflow horizontal: proibido.
- Omissão de itens: proibida.
- Duplicação de itens: proibida.
- Reordenação de itens: proibida.
- Paginação do `lancador`: proibida.
- Rolagem específica: proibida.
- Mensagem nova específica para o `lancador`: proibida.
- Variante visual local: proibida.
- Comparação de grandezas de domínios diferentes: proibida.
- Generalização da regra para outros componentes: proibida.

---

## 12. Recuperação automática

A recuperação automática foi propagada em todos os documentos relevantes:

- A cada redesenho, o renderer recalcula `area_lancador_w` e `content_w`.
- Quando `area_lancador_w >= lancador_caixa_min_w` (equivalente:
  `content_w >= coluna_minima_content_w`), o quadro mínimo desaparece.
- A tela normal é reconstruída integralmente.
- O `lancador` volta à distribuição válida (`fila` ou `matriz`, conforme
  couber), recalculada a partir da largura atual.
- Não é necessária ação do usuário.
- Não é necessário reiniciar a aplicação.
- Não há persistência do estado de quadro mínimo entre redesenhos.

---

## 13. Ausência de novo campo JSON

Confirmado: nenhum campo JSON foi introduzido em nenhum dos documentos
alterados. O gatilho é calculado pelo renderer a partir da composição e das
dimensões disponíveis. O `contrato_json_lancador.md` não foi alterado.

---

## 14. Tratamento da nota do frontmatter (QA-POS-ADR0023-BAIXO-001)

O achado `QA-POS-ADR0023-BAIXO-001` registra que o frontmatter da ADR possui
uma lista resumida de `contratos_afetados` (apenas `contrato_lancador.md` e
`NOMENCLATURA.md`), enquanto a seção 9 da ADR contém a lista normativa
completa (incluindo `contrato_tela_json.md`, `contrato_composicao_corpo.md` e
`INDICE_ADR.md`).

Durante esta aplicação:

- A ADR aprovada não foi alterada; o frontmatter permaneceu inalterado.
- A seção 9 da ADR foi usada como lista normativa completa de propagação.
- Todos os cinco contratos listados na seção 9 foram atualizados, incluindo
  `contrato_tela_json.md` e `contrato_composicao_corpo.md`, que não constam
  no frontmatter resumido.
- O achado baixo é registrado como observação não bloqueante; não impediu a
  aplicação.

---

## 15. Buscas de resíduos executadas

### 15.1 Formulações que limitam o quadro mínimo à largura total do terminal

Buscas executadas nos documentos alterados por:
- "dimensões do terminal"
- "largura do terminal"
- "terminal pequeno demais" (sem complemento de área interna)

Resultado: as seções preexistentes que mencionam o gatilho por terminal
fisicamente pequeno foram preservadas e complementadas — não sobrescritas.
Não há texto remanescente nos documentos alterados que impeça o novo gatilho
por `area_lancador_w`.

### 15.2 Ocorrências de fallback local

Buscas por "fallback local", "mensagem local", "estado local", "variante local"
nos documentos alterados.

Resultado: todas as ocorrências são negativas (proibições explícitas) ou
definições do termo como proibido. Nenhuma ocorrência permite interpretar
fallback como local.

### 15.3 Truncamento ou paginação

Buscas por "truncar", "paginar", "omitir", "overflow".

Resultado: todas as ocorrências nos trechos novos são proibições. Nenhuma
ocorrência nova permite truncamento ou paginação do `lancador`.

### 15.4 Mistura de grandezas de largura

Buscas por comparações diretas entre grandezas de domínios diferentes.

Resultado: não encontradas comparações proibidas. As seções novas declaram
explicitamente que `terminal_w` não deve ser comparado com
`coluna_minima_content_w`, e que `area_lancador_w` não deve ser comparado
com `coluna_minima_content_w` sem converter bordas e padding.

### 15.5 Criação de campo JSON

Nenhum campo JSON foi criado. O `contrato_json_lancador.md` não foi alterado.

### 15.6 Generalização para outros componentes

Buscas por formulações genéricas aplicadas a outros componentes sem autoridade.

Resultado: todos os trechos novos declaram explicitamente que a regra
aplica-se exclusivamente ao `lancador`. A seção 5.10 do
`contrato_composicao_corpo.md` especifica: "Esta regra aplica-se
exclusivamente ao `lancador`; não é criada regra genérica de falha global
para qualquer outro filho sem autoridade explícita."

### 15.7 Recuperação automática

Buscas por "redesenho", "recuperação", "automática".

Resultado: a recuperação automática está registrada em todos os documentos
relevantes — `contrato_lancador.md` seção 6.7 e R-14, `contrato_tela_json.md`
nova subseção, `contrato_composicao_corpo.md` seção 5.10 e R-33, e
`NOMENCLATURA.md` seção 6.3.

### 15.8 ADR e handoff

Verificado via `git status`: a ADR (`docs/adr/ADR-0023-largura-minima-funcional-lancador.md`)
e o handoff (`docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`)
permanecem como `??` (não rastreados) — seus conteúdos não foram alterados.

---

## 16. Estado Git final

Comandos executados a partir da raiz do projeto:

```bash
git status --short
git diff --name-only
git diff --check
git diff --cached --name-only
```

Resultado:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? tela/__pycache__/
```

`git diff --check`: sem whitespace errors.
`git diff --cached --name-only`: stage vazio.

---

## 17. Itens não rastreados

```yaml
demo/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: cache Python preexistente; não foi removido

tela/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: cache Python preexistente; não foi removido

docs/adr/ADR-0023-largura-minima-funcional-lancador.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: preexistente ao início da etapa; não alterado por esta etapa

docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: preexistente ao início da etapa; preservado sem alteração

docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: preexistente; não alterado

docs/relatorios/RELATORIO_QA_ADR-0023.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: preexistente; não alterado por esta etapa

docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: preexistente; não alterado

docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: preexistente; não alterado

docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md:
  origem: CONFIRMADA
  produzido_pelo_executor: CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: criado por esta etapa como artefato autorizado
```

---

## 18. Caches observados

Dois diretórios de cache Python foram observados:

- `demo/__pycache__/`
- `tela/__pycache__/`

Ambos eram preexistentes ao início da etapa. Nenhum foi removido. A origem
não pôde ser confirmada como produzida por esta etapa.

---

## 19. Fatos NAO_CONFIRMADO

```yaml
- item: demo/__pycache__/
  fato_nao_confirmado: origem do cache Python
- item: tela/__pycache__/
  fato_nao_confirmado: origem do cache Python
- item: docs/adr/ADR-0023-largura-minima-funcional-lancador.md
  fato_nao_confirmado: executor que criou o arquivo em etapa anterior
- item: docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
  fato_nao_confirmado: executor que criou o arquivo em etapa anterior
- item: docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
  fato_nao_confirmado: executor que criou o arquivo em etapa anterior
- item: docs/relatorios/RELATORIO_QA_ADR-0023.md
  fato_nao_confirmado: executor que criou o arquivo em etapa anterior
- item: docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
  fato_nao_confirmado: executor que criou o arquivo em etapa anterior
- item: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
  fato_nao_confirmado: executor que criou o arquivo em etapa anterior
```

---

## 20. Bloqueios

Nenhum bloqueio (`BLOCKED_DOCUMENTATION`) foi acionado durante a aplicação.

Motivos verificados:
- As autoridades aprovadas não são contraditórias entre si.
- A propagação não exigiu decidir novo comportamento.
- O quadro mínimo global foi distinguido do fallback local de forma inequívoca.
- As grandezas de largura foram reconciliadas sem mistura de domínios.
- Nenhum documento adicional fora da lista autorizada foi necessário.
- O `contrato_json_lancador.md` não exigiu alteração material.
- A lista nominal da seção 9 da ADR foi suficiente para aplicar integralmente
  a decisão.

---

## 21. Conclusão factual

Cinco documentos normativos foram alterados e um relatório foi criado:

1. `docs/contratos/contrato_lancador.md`: nova seção 6.7 e regras R-11 a R-14.
2. `docs/contratos/contrato_tela_json.md`: nova subseção na seção 24.
3. `docs/contratos/contrato_composicao_corpo.md`: novo parágrafo na seção 5.10,
   regra R-33 e três critérios.
4. `docs/NOMENCLATURA.md`: nova subseção 6.3.
5. `docs/adr/INDICE_ADR.md`: entrada ADR-0023.
6. `docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md`: este relatório (criado).

A ADR e o handoff H-0034 permaneceram inalterados. O stage Git permaneceu
vazio. Nenhum campo JSON foi introduzido. Nenhuma regra nova foi criada para
componentes além do `lancador`. Nenhum bloqueio foi acionado.

A aplicação documental da ADR-0023 está factualmente concluída.
