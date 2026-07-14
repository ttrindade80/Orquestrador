# RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025

## 1. Escopo

Este levantamento documenta a transição operacional entre o handoff **H-0024**
(`H-0024-distribuicao-vertical-percentual-fracao-corpo.md`) e o handoff
**H-0025** (`H-0025-distribuicao-vertical-explicita-area-corpo.md`), passando
pela **ADR-0018** (`ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`)
e pelo relatório de implementação bloqueada **IMP-0025**.

Objeto do levantamento: reconstruir, com base exclusivamente nos artefatos
presentes no repositório, a sequência histórica de:

1. criação e aprovação do H-0024;
2. tentativa de implementação e bloqueio;
3. reversão das alterações técnicas;
4. criação e aplicação da ADR-0018;
5. criação e aprovação do H-0025;
6. implementação bem-sucedida via IMP-0026;
7. relação de substituição entre H-0024 e H-0025.

Síntese conversacional verificada: foi fornecida pelo usuário a seguinte
confirmação prévia: _"H-0024 foi criado, corrigido e aprovado como handoff, mas
a tentativa de implementação foi bloqueada por lacuna documental ou semântica. As
alterações de código e testes foram revertidas, e o H-0024 ficou preservado como
histórico. H-0025 foi o handoff substituto, criado depois da ADR-0018. Ele foi
implementado, com IMP-0026, testes aprovados e QA final
I1_IMPLEMENTATION_APPROVED."_ Esta síntese foi tratada como
`CONFIRMAÇÃO_EXPLÍCITA_DO_USUÁRIO` e verificada contra os artefatos de
repositório.

Este levantamento **não autoriza e não executou**:

- correção de documentação;
- alteração de H-0024, H-0025 ou ADR-0018;
- registro formal de substituição entre handoffs;
- QA de qualquer artefato;
- implementação de código;
- restauração ou reversão de arquivos;
- preparação ou execução de commit;
- início de qualquer etapa posterior.

## 2. Método

Protocolo executado:

1. Detectar raiz Git, branch, HEAD e estado do worktree.
2. Buscar todos os artefatos relacionados a H-0024, H-0025, ADR-0018, IMP-0025
   e IMP-0026 por `rg` e `find`.
3. Ler integralmente cada artefato encontrado em ordem cronológica de criação
   inferida.
4. Reconstruir a sequência de etapas de H-0024 (criação → QA → patch → QA
   pós-patch → implementação → bloqueio → reversão).
5. Verificar a necessidade de ADR-0018 e reconstruir o ciclo da ADR.
6. Reconstruir a sequência de etapas de H-0025 (criação → QA → implementação
   → QA → fechamento → commit).
7. Comparar H-0024 e H-0025 textualmente.
8. Verificar a relação de substituição.
9. Identificar contradições e evidências ausentes.
10. Produzir exclusivamente este relatório.

## 3. Estado Git inicial

Estado do repositório no momento em que o levantamento foi iniciado:

| Parâmetro | Valor |
|---|---|
| Branch | `master` |
| HEAD | `c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos` |
| Stage | vazio |
| Worktree | limpo (sem arquivos rastreados modificados, sem arquivos não rastreados relevantes) |
| Stash | ausente no momento do levantamento |

O HEAD `c003f3e` é o segundo commit após `1cc0dff feat: implementa distribuicao
vertical explicita do corpo`, que foi o commit que selou o ciclo H-0024 →
ADR-0018 → H-0025. Os commits intermediários foram:

- `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- `c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos`

## 4. Artefatos de H-0024

Artefatos encontrados e examinados relacionados ao H-0024:

| Artefato | Caminho | Status final |
|---|---|---|
| Handoff H-0024 | `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md` | `proposto` (frontmatter; operacionalmente: histórico bloqueado) |
| QA do handoff | `docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md` | `H2_HANDOFF_PATCH_REQUIRED` |
| QA pós-patch | `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md` | `H1_HANDOFF_APPROVED` |
| Implementação bloqueada | `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md` | `BLOCKED / ARCHITECTURE_REVIEW_REQUIRED` |
| Levantamento do bloqueio | `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md` | `LEVANTAMENTO_CONCLUIDO / BLOCKED_USER_DECISION` |

Todos os artefatos acima foram commitados em `1cc0dff` e estão presentes no
repositório.

Artefato periférico observado (não examinado neste levantamento):

| Artefato | Caminho |
|---|---|
| Levantamento de feature | `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md` |

Este artefato aparece nos registros de arquivos não rastreados durante o ciclo
(`RELATORIO_QA_ADR-0018.md` §17) e foi commitado em `1cc0dff`, mas antecede a
criação do H-0024 e não integra a cadeia de transição investigada.

## 5. Etapas comprovadas de H-0024

| Etapa | Evidência | Status/Resultado |
|---|---|---|
| `CRIAR_HANDOFF` | H-0024 existe em `docs/handoff/` | Criado com 8 arquivos autorizados; autoridade ADR-0015 |
| `QA_HANDOFF` | `RELATORIO_QA_H-0024_HANDOFF.md` | `H2_HANDOFF_PATCH_REQUIRED` (2 achados médios: H2-001, H2-002) |
| `PATCH_HANDOFF` | inferido da existência do relatório pós-patch | sem relatório de patch dedicado; confirmado por completude da sequência |
| `QA_POS_PATCH_HANDOFF` | `RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md` | `H1_HANDOFF_APPROVED` → próxima: `IMPLEMENTAR` |
| `IMPLEMENTAR` | `IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md` | `BLOCKED / ARCHITECTURE_REVIEW_REQUIRED` |

**Achados do QA do H-0024 (H2_HANDOFF_PATCH_REQUIRED):**

- **H2-001** (médio): a semântica de `modo=igual` era tratada de forma
  inconsistente — o handoff admitia ambiguidade entre comportamento local e
  divisão normativa.
- **H2-002** (médio): `docs/templates/TEMPLATE_RELATORIO_IMPL.md`, exigido como
  arquivo de leitura, não estava listado na seção de arquivos autorizados.

**Resolução pós-patch:**

- H2-001 resolvido: ausência de `distribuicao` ≡ `igual` explicitamente
  especificada com divisão igual obrigatória.
- H2-002 resolvido: template adicionado à seção somente leitura.

Estado Git no momento da aprovação H1: HEAD `3332773a` (feat: implementa
redimensionamento reativo da TUI), stage vazio, stash `stash@{0}: On master:
pre-H-0022` (SHA `21f98d0f4a479d72e6df21b1dca1511c3ad38937`).

## 6. Bloqueio da implementação de H-0024

### 6.1. Descrição do bloqueio

Durante a execução de `IMPLEMENTAR`, a tentativa de implementação da distribuição
vertical no `renderizador.py` foi bloqueada pela condição
`ARCHITECTURE_REVIEW_REQUIRED`.

**Causa primária:** conflito irreconciliável entre as semânticas normativas do
H-0024 e o comportamento exigido pela suíte de regressão imutável.

**Raciocínio:**

O H-0024 (conforme pós-patch) especificava: ausência de `corpo.distribuicao` ≡
`modo=igual` ≡ divisão igual do espaço disponível entre todos os filhos diretos.

O `config/telas/orquestrador.json` possui `corpo.arranjo = "vertical"` e **sem**
`corpo.distribuicao`. Com altura total `h=15`, as cotas são:

- `cabeçalho`: 3 linhas
- `barra_de_menus`: 3 linhas
- `corpo` disponível: 15 - 3 - 3 = **9 linhas**

Com 3 filhos diretos e `modo=igual`, a distribuição normativa geraria `[3, 3, 3]`
(maiores restos). O filho `lancador`, porém, exige **4 linhas** de conteúdo
natural mínimo, tornando a cota de 3 linhas inválida → `RenderizadorErro`.

O teste `tela/teste_demo.py` height=15 é imutável (regressão de integração) e
afirmava o comportamento antigo de preenchimento externo (H-0015), não divisão
igual.

As duas exigências eram mutuamente exclusivas: implementar a divisão igual
conforme H-0024 quebra o teste imutável; preservar o teste imutável contradiz a
norma pós-patch do H-0024.

### 6.2. Documentação do bloqueio

- `IMP-0025`: status `BLOCKED / ARCHITECTURE_REVIEW_REQUIRED`; confirmação dos
  algoritmos corretos (exemplos `[1,1,1]→[23,23,22]` e `[2,1,2]→[27,14,27]`
  verificados a h=68); declaração explícita das restrições conflitantes.
- `RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`: status
  `LEVANTAMENTO_CONCLUIDO / BLOCKED_USER_DECISION`; documenta que
  `config/telas/orquestrador.json` possui `corpo.arranjo="vertical"` sem
  `distribuicao`; demonstra o conflito cota × conteúdo; registra que a decisão
  sobre modo/valores pertence ao usuário.

### 6.3. Classificação do bloqueio

```text
BLOQUEIO_COMPROVADO
Causa: lacuna semântica entre H-0024 (ausência ≡ igual) e comportamento
       exigido pela regressão imutável (preenchimento externo, não divisão)
Escopo: decisão arquitetural não coberta por ADR vigente
```

## 7. Reversão das alterações técnicas

### 7.1. Evidências de reversão

A reversão das alterações técnicas é comprovada por **declaração formal no
relatório do executor** (`IMP-0025`, seção "Arquivos alterados"):

| Arquivo | Estado declarado em IMP-0025 |
|---|---|
| `tela/loader.py` | revertido a HEAD (`git checkout --`) |
| `tela/modelo.py` | revertido a HEAD (`git checkout --`) |
| `tela/renderizador.py` | revertido a HEAD (`git checkout --`) |
| `tela/teste_loader.py` | não alterado |
| `tela/teste_modelo.py` | não alterado |
| `tela/teste_renderizador.py` | não alterado |

### 7.2. Corroboração indireta

O `RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`
(produzido após a reversão) confirma que `git diff --stat` e `git diff
--name-only` retornaram saída vazia para arquivos rastreados — coerente com
worktree limpo pós-reversão.

As suítes base foram confirmadas como íntegras pós-reversão:

| Suíte | Resultado |
|---|---|
| loader | 89/89 |
| modelo | 56/56 |
| renderizador | 331/331 |
| demo | 303/303 |

### 7.3. Limitação da evidência

Não há `git diff` histórico que comprove a diferença entre o estado de código
durante a implementação e o estado pós-reversão, pois as alterações foram
revertidas antes de qualquer commit rastreado. A comprovação é documental
(declaração formal do executor) e indireta (worktree limpo confirmado).

### 7.4. Artefatos documentais preservados

Os seguintes artefatos foram criados durante o ciclo do H-0024 e **não foram
revertidos** — são registros históricos, não código:

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`
- `docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md`

### 7.5. Classificação da reversão

```text
REVERSÃO_INTEGRAL_COMPROVADA_POR_DECLARAÇÃO_FORMAL
Arquivos de código revertidos: loader.py, modelo.py, renderizador.py
Arquivos de teste: não alterados (não exigiram reversão)
Artefatos documentais: preservados intencionalmente como histórico
```

## 8. ADR-0018 e resolução da lacuna

### 8.1. Motivação

A ADR-0018 foi criada em resposta direta ao bloqueio do H-0024. A própria ADR
declara explicitamente: _"Durante a tentativa de implementação do H-0024
(registrada em IMP-0025 e no RELATORIO_LEVANTAMENTO_BLOQUEIO...), ficou
evidenciado que a especificação normativa vigente era insuficiente para resolver
o conflito entre..."_

### 8.2. Decisões normativas (D1-D10)

As decisões mais relevantes para a transição H-0024→H-0025:

| Decisão | Conteúdo |
|---|---|
| D1 | `arranjo` ≠ `distribuição`: são conceitos distintos |
| D2 | Ausência de `distribuicao` **preserva** construção orientada a conteúdo (NÃO equivale a `igual`) |
| D3 | Distribuição explícita reparte a altura útil integral entre os filhos diretos |
| D4 | Preenchimento interno (dentro da área alocada ao filho), não externo (H-0015) |
| D5 | `igual` é modo explícito, não fallback implícito |
| D9 | Mudanças JSON necessárias para o handoff pertencem ao próprio handoff |

D2 representa a inversão direta da norma que causou o bloqueio do H-0024.

### 8.3. Ciclo de aprovação da ADR-0018

| Etapa | Artefato | Resultado |
|---|---|---|
| `QA_ADR` | `RELATORIO_QA_ADR-0018.md` | `ADR_APPROVED_WITH_NOTES` (A-001 baixo) |
| `APLICAR_ADR` | `RELATORIO_APLICACAO_ADR-0018.md` | 6 documentos modificados |
| `QA_APLICACAO_ADR` | `RELATORIO_QA_APLICACAO_ADR-0018.md` | `ADR_APPLICATION_REJECTED` (APL-001 alto, APL-002 médio) |
| `PATCH_DOCUMENTACAO` | sem relatório dedicado | R-17 e NOMENCLATURA.md itens 12-13 corrigidos |
| `QA_POS_PATCH_APLICACAO_ADR` | `RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md` | `ADR_APPLICATION_APPROVED_WITH_NOTES` → `RETOMAR_OU_RECRIAR_HANDOFF` |

**Achados da aplicação rejeitada:**

- **APL-001** (alto): R-17 em `contrato_composicao_corpo.md:837` ainda declarava
  que `arranjo` define "eixo de distribuição"; itens 12-13 da `NOMENCLATURA.md`
  afirmavam que `arranjo` horizontal/vertical "aloca colunas/linhas" — residual
  de confusão arranjo/distribuição.
- **APL-002** (médio): busca de resíduos no relatório de aplicação estava
  incompleta.

### 8.4. Documentos modificados pela ADR-0018

| Documento | Alteração principal |
|---|---|
| `docs/contratos/contrato_composicao_corpo.md` | R-17 corrigido (arranjo ≠ distribuição) |
| `docs/contratos/contrato_tela_json.md` | distinção arranjo/distribuição aplicada |
| `docs/contratos/contrato_json_tela_minima.md` | §6.2 e §6.3: removidas formulações "ausência equivale a igual" |
| `docs/contratos/contrato_processo_desenvolvimento.md` | distinção distribuição explicitada |
| `docs/NOMENCLATURA.md` | itens 12-13 corrigidos (arranjo ≠ distribuição) |
| `docs/adr/INDICE_ADR.md` | ADR-0018 registrada como `aceita` |

### 8.5. Discrepância de status da ADR-0018

O frontmatter da ADR-0018 permanece com `status: proposta`, enquanto o
`INDICE_ADR.md` registra `aceita`. O `RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018`
registrou a aplicação como aprovada, mas o frontmatter da ADR nunca foi
atualizado para refletir isso. Esta divergência foi identificada em relatórios
posteriores (ciclo H-0027) como divergência histórica de status pré-existente.

## 9. Artefatos de H-0025

| Artefato | Caminho | Status final |
|---|---|---|
| Handoff H-0025 | `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md` | `proposto` (frontmatter; operacionalmente: implementado e commitado) |
| QA do handoff | `docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md` | `H1_HANDOFF_APPROVED` |
| Implementação | `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md` | `IMPLEMENTED` |
| QA da implementação | `docs/relatorios/RELATORIO_QA_H-0025_IMPLEMENTACAO.md` | `I1_IMPLEMENTATION_APPROVED` |
| Verificação de fechamento | `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md` | `CLOSURE_READY_FOR_COMMIT_PREPARATION` (com RSS-002/WS-001 pendente) |
| QA pós-patch WS-001 | `docs/relatorios/RELATORIO_QA_POS_PATCH_WS-001_H-0025.md` | `QA_POS_PATCH_APPROVED` |
| Verificação de fechamento pós-patch | `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_POS_PATCH_H-0025.md` | `CLOSURE_READY_FOR_COMMIT_PREPARATION` |

Todos os artefatos acima foram commitados em `1cc0dff`.

## 10. Etapas comprovadas de H-0025

| Etapa | Evidência | Status/Resultado |
|---|---|---|
| `CRIAR_HANDOFF` | H-0025 existe em `docs/handoff/` | Criado pós ADR-0018 aprovada; autoridade ADR-0018; referencia H-0024 como histórico bloqueado |
| `QA_HANDOFF` | `RELATORIO_QA_H-0025_HANDOFF.md` | `H1_HANDOFF_APPROVED` (sem achados; sem patch necessário) |
| `IMPLEMENTAR` | `IMP-0026-distribuicao-vertical-explicita-area-corpo.md` | `IMPLEMENTED` (8 arquivos modificados) |
| `QA_IMPLEMENTACAO` | `RELATORIO_QA_H-0025_IMPLEMENTACAO.md` | `I1_IMPLEMENTATION_APPROVED` |
| `VERIFICAR_FECHAMENTO` | `RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md` | `CLOSURE_READY_FOR_COMMIT_PREPARATION` (WS-001 pendente) |
| `PATCH_WS-001` | sem relatório dedicado; inferido pelo QA pós-patch | linha vazia excedente no EOF de `RELATORIO_QA_ADR-0018.md` removida |
| `QA_POS_PATCH_WS-001` | `RELATORIO_QA_POS_PATCH_WS-001_H-0025.md` | `QA_POS_PATCH_APPROVED` |
| `REFAZER_VERIFICACAO_FECHAMENTO` | `RELATORIO_VERIFICACAO_FECHAMENTO_POS_PATCH_H-0025.md` | `CLOSURE_READY_FOR_COMMIT_PREPARATION` → `PREPARAR_COMMIT` |
| `COMMIT` | SHA `1cc0dff` | `feat: implementa distribuicao vertical explicita do corpo` (32 arquivos, 9.322 inserções) |

Estado Git no momento da aprovação H1 do H-0025: HEAD `3332773a`, branch
`master`, 6 arquivos rastreados modificados (aplicação ADR-0018), stage vazio,
stash `21f98d0f4a479d72e6df21b1dca1511c3ad38937`.

## 11. IMP-0026, testes e QA final

### 11.1. Arquivos modificados em IMP-0026

| Arquivo | Categoria | Alteração principal |
|---|---|---|
| `tela/loader.py` | código | leitura de `distribuicao` do JSON |
| `tela/modelo.py` | código | campo `distribuicao` no modelo de corpo |
| `tela/renderizador.py` | código | funções `_pesos_distribuicao`, `_distribuir_alturas` |
| `tela/teste_loader.py` | teste | cobertura de `distribuicao` no loader |
| `tela/teste_modelo.py` | teste | cobertura de `distribuicao` no modelo |
| `tela/teste_renderizador.py` | teste | 54 verificações em `TestDistribuicaoVerticalH0025` |
| `tela/teste_demo.py` | teste | fixture height=15 adaptada (helper `_modelo_orquestrador_sem_distribuicao`) |
| `config/telas/orquestrador.json` | configuração | `"distribuicao": {"modo": "fracao", "valores": [2, 1, 2]}` adicionado |

### 11.2. Resultados dos testes

| Suíte | Resultado pré-H-0025 | Resultado pós-IMP-0026 |
|---|---|---|
| loader | 89/89 | 105/105 |
| modelo | 56/56 | 58/58 |
| renderizador | 331/331 | 385/385 |
| demo | 303/303 | 303/303 |

### 11.3. Exemplos normativos confirmados

| Exemplo | Entrada | Saída esperada | Resultado |
|---|---|---|---|
| D7 (fracao) | h=68, pesos=[1,1,1] | [23, 23, 22] | confirmado |
| D7 (fracao) | h=68, pesos=[2,1,2] | [27, 14, 27] | confirmado |

### 11.4. QA final

- Status: `I1_IMPLEMENTATION_APPROVED`
- 14 arquivos rastreados modificados (6 ADR-0018 + 8 H-0025)
- Evidência suplementar do usuário: "A tela inicial ficou ótima" (OBS-H0025-001:
  cobre somente estado inicial, não resize nem todos os modos)

### 11.5. Tratamento do teste de regressão height=15

O teste `tela/teste_demo.py` que bloqueou o H-0024 foi adaptado conforme
H-0025 §11.5 item 1: a fixture de height=15 passou a usar um modelo construído
**sem** o campo `distribuicao` (helper `_modelo_orquestrador_sem_distribuicao()`).
Isso preserva a cobertura do comportamento "altura sem distribuição = saída
natural" sem contradizer a nova semântica de ausência definida pela ADR-0018.

## 12. Comparação entre H-0024 e H-0025

| Aspecto | H-0024 | H-0025 |
|---|---|---|
| Autoridade normativa principal | ADR-0015 | ADR-0018 |
| Semântica de ausência de `distribuicao` | ausência ≡ `igual` (divisão igual, normativa) | ausência preserva construção orientada a conteúdo |
| Mudança em `orquestrador.json` | não incluída (violação de D9, causa de processo) | incluída: `{"modo": "fracao", "valores": [2, 1, 2]}` |
| `tela/teste_demo.py` nos arquivos autorizados | não (fora do escopo declarado) | sim (com adaptação autorizada por §11.5) |
| Total de arquivos autorizados | 7 | 9 |
| Relatório de implementação esperado | `IMP-0025` | `IMP-0026` |
| Referência histórica | — | `rastreabilidade.handoff_historico: H-0024` |
| Estado final do handoff (frontmatter) | `proposto` (histórico bloqueado) | `proposto` (implementado e commitado) |
| Substituição formal declarada | não aplicável | §2.3: "substitui operacionalmente o H-0024" |

**Convergência:** ambos têm o mesmo objetivo funcional — implementar distribuição
vertical do corpo entre os filhos diretos, com suporte a `igual`, `percentual` e
`fracao`.

**Divergência central:** a especificação semântica da ausência de `distribuicao`
é oposta. H-0024 exigia que a ausência fosse tratada como `igual`; H-0025 exige
que a ausência preserve o comportamento pré-existente de construção orientada a
conteúdo.

## 13. Relação de substituição

### 13.1. Declaração formal no H-0025

A relação de substituição está formalmente documentada em H-0025 §2.3:

> "Este handoff **substitui operacionalmente** o H-0024 para a implementação."
>
> "O H-0024 **permanece preservado** como evidência histórica e **não deve ser
> alterado, renomeado ou removido**."

### 13.2. Corroboração em outros artefatos

- `IMP-0026` §5: "Tanto o H-0024 quanto o IMP-0025 permanecem preservados como
  evidência histórica, sem autoridade normativa superior, e não foram alterados."
- `RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md` §7: categoriza H-0024 como
  "histórico bloqueado".
- `H-0025` frontmatter `rastreabilidade.handoff_historico`: aponta explicitamente
  para H-0024.

### 13.3. Natureza da substituição

| Dimensão | Classificação |
|---|---|
| Tipo | operacional (H-0025 executa o que H-0024 deveria executar) |
| Escopo | restrito à implementação (H-0024 permanece como evidência histórica válida) |
| Autoridade de declaração | H-0025 §2.3, aprovada pelo QA sem ressalvas (H1_HANDOFF_APPROVED) |
| Status de H-0024 após substituição | histórico preservado, sem autoridade normativa operacional |

### 13.4. Classificação

```text
SUBSTITUIÇÃO_FORMALMENTE_DOCUMENTADA
Evidência primária:    H-0025 §2.3
Evidência secundária:  IMP-0026 §5; RELATORIO_VERIFICACAO_FECHAMENTO_H-0025 §7
```

## 14. Contradições e evidências ausentes

### 14.1. H-0024 frontmatter status não atualizado

O frontmatter de `H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
permanece com `status: proposto`. Nenhum artefato formal registra uma transição
de status de H-0024 para `bloqueado`, `histórico` ou equivalente. A preservação
histórica é declarada por H-0025 §2.3 e IMP-0026 §5, mas não há documento de
fechamento dedicado ao próprio H-0024.

Esta divergência não compromete a reconstrução histórica, pois o estado
funcional está estabelecido pelos artefatos de bloqueio (IMP-0025,
RELATORIO_LEVANTAMENTO_BLOQUEIO) e pela declaração de substituição (H-0025 §2.3).

### 14.2. ADR-0018 frontmatter status divergente do INDICE_ADR.md

O frontmatter da ADR-0018 contém `status: proposta`, enquanto o `INDICE_ADR.md`
registra `aceita`. O processo de aplicação foi aprovado
(`ADR_APPLICATION_APPROVED_WITH_NOTES`), mas o frontmatter da ADR nunca foi
atualizado. Esta divergência foi identificada em relatórios posteriores (ciclo
H-0027, OBS-001 em `RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md`) como
divergência histórica de status.

### 14.3. Ausência de relatório dedicado de patch do H-0024

A etapa `PATCH_HANDOFF` de H-0024 não possui relatório de patch dedicado. A
existência do patch é inferida pela presença do
`RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md`, que valida a resolução de H2-001 e
H2-002. Não há evidência de que um relatório de patch tenha sido formalmente
criado.

### 14.4. Ausência de relatório dedicado do PATCH_DOCUMENTACAO da ADR-0018

O `PATCH_DOCUMENTACAO` que corrigiu APL-001 (R-17 em
`contrato_composicao_corpo.md` e itens 12-13 em `NOMENCLATURA.md`) não possui
relatório de patch dedicado. A resolução é confirmada pelo
`RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`.

### 14.5. Artefato periférico não examinado

O arquivo `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`
esteve presente no workspace durante o ciclo e foi commitado em `1cc0dff`, mas
não foi examinado neste levantamento. Ele antecede a criação do H-0024 e não
integra a cadeia de transição investigada.

## 15. Conclusões

```yaml
levantamento: RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025
data: "2026-07-12"
classificacao_final: LEVANTAMENTO_CONCLUSIVO

confirmacao_sintese_usuario:
  status: CONFIRMADA_COM_VERIFICACAO
  divergencias_materiais: nenhuma
  nota: >
    A síntese fornecida pelo usuário é integralmente corroborada pelos artefatos
    do repositório. Todos os pontos — criação, correção, aprovação, bloqueio,
    reversão, preservação histórica, ADR-0018, H-0025 substituto, IMP-0026,
    testes aprovados e QA final I1_IMPLEMENTATION_APPROVED — foram comprovados
    por artefatos rastreados no repositório.

h0024:
  criado: comprovado
  qa_reprovado: comprovado  # H2_HANDOFF_PATCH_REQUIRED, 2 achados médios
  patched: inferido  # sem relatório dedicado; confirmado por QA pós-patch
  qa_aprovado: comprovado  # H1_HANDOFF_APPROVED
  implementacao_bloqueada: comprovado  # ARCHITECTURE_REVIEW_REQUIRED
  status_frontmatter: "proposto"  # não atualizado formalmente (DIV-001)

adr0018:
  criada: comprovado
  motivacao: bloqueio_do_H-0024
  qa: comprovado  # ADR_APPROVED_WITH_NOTES, A-001 baixo
  aplicacao_rejeitada: comprovado  # ADR_APPLICATION_REJECTED, APL-001 alto
  repatch: comprovado  # APL-001 e APL-002 resolvidos
  aplicacao_aprovada: comprovado  # ADR_APPLICATION_APPROVED_WITH_NOTES
  status_frontmatter: "proposta"  # diverge de INDICE_ADR.md "aceita" (DIV-002)

reversao_h0024:
  classificacao: REVERSÃO_INTEGRAL_COMPROVADA_POR_DECLARAÇÃO_FORMAL
  arquivos_codigo_revertidos:
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
  arquivos_teste: nao_alterados
  artefatos_documentais: preservados_intencionalmente

h0025:
  criado: comprovado
  qa_aprovado: comprovado  # H1_HANDOFF_APPROVED, sem achados
  implementado: comprovado  # IMP-0026 IMPLEMENTED, 8 arquivos modificados
  qa_implementacao: comprovado  # I1_IMPLEMENTATION_APPROVED
  fechamento: comprovado  # WS-001 resolvido, verificacao pós-patch aprovada
  commitado: comprovado  # SHA 1cc0dff, 2026-07-11T20:37:25-0300

substituicao:
  classificacao: SUBSTITUIÇÃO_FORMALMENTE_DOCUMENTADA
  evidencia_primaria: "H-0025 §2.3"
  evidencia_secundaria:
    - "IMP-0026 §5"
    - "RELATORIO_VERIFICACAO_FECHAMENTO_H-0025 §7"

divergencias_documentais:
  - id: DIV-001
    artefato: "docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md"
    divergencia: "frontmatter status 'proposto'; estado operacional é 'histórico bloqueado'"
    impacto: nenhum_sobre_a_reconstrucao_historica
  - id: DIV-002
    artefato: "docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md"
    divergencia: "frontmatter status 'proposta' vs. INDICE_ADR.md 'aceita'"
    impacto: nenhum_sobre_a_reconstrucao_historica
    nota: "divergência conhecida, documentada no ciclo H-0027"

itens_fora_de_escopo: []
proxima_etapa_autorizada: nenhuma_neste_levantamento
```

## 16. Arquivos examinados

| Arquivo | Lido integralmente | Propósito |
|---|---|---|
| `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md` | sim | handoff histórico H-0024 |
| `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md` | sim | handoff substituto H-0025 |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | sim | ADR resolvedora da lacuna semântica |
| `docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md` | sim | QA do H-0024 (H2_HANDOFF_PATCH_REQUIRED) |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md` | sim | QA pós-patch do H-0024 (H1_HANDOFF_APPROVED) |
| `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md` | sim | implementação bloqueada H-0024 |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md` | sim | levantamento do bloqueio (BLOCKED_USER_DECISION) |
| `docs/relatorios/RELATORIO_QA_ADR-0018.md` | sim | QA da ADR-0018 (ADR_APPROVED_WITH_NOTES) |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md` | sim | aplicação da ADR-0018 a 6 documentos |
| `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md` | sim | QA da aplicação (ADR_APPLICATION_REJECTED) |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md` | sim | QA pós-patch da aplicação (ADR_APPLICATION_APPROVED_WITH_NOTES) |
| `docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md` | sim | QA do H-0025 (H1_HANDOFF_APPROVED) |
| `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md` | sim | implementação bem-sucedida H-0025 (IMPLEMENTED) |
| `docs/relatorios/RELATORIO_QA_H-0025_IMPLEMENTACAO.md` | sim | QA da implementação (I1_IMPLEMENTATION_APPROVED) |
| `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md` | sim | verificação de fechamento (com WS-001) |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_WS-001_H-0025.md` | sim | QA pós-patch WS-001 (QA_POS_PATCH_APPROVED) |
| `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_POS_PATCH_H-0025.md` | sim | verificação de fechamento pós-patch (CLOSURE_READY_FOR_COMMIT_PREPARATION) |

## 17. Commits examinados

| SHA (abrev.) | SHA (completo) | Mensagem | Relevância |
|---|---|---|---|
| `3332773` | `3332773a3f10e716115a164148af323fa86e608f` | feat: implementa redimensionamento reativo da TUI | HEAD do repositório durante todo o ciclo H-0024/ADR-0018/H-0025 |
| `1cc0dff` | `1cc0dff88191630eae441e04ead4d3586afdd764` | feat: implementa distribuicao vertical explicita do corpo | commit que selou o ciclo completo (32 arquivos, 9.322 inserções, data 2026-07-11) |
| `40015b6` | (abreviado; completo não examinado) | feat: implementa distribuicao horizontal percentual e fracionaria | commit posterior ao ciclo H-0024/H-0025 |
| `c003f3e` | (abreviado; completo não examinado) | feat: implementa composicao hierarquica do corpo com tres niveis de grupos | HEAD no momento deste levantamento |

## 18. Comandos executados

| Ferramenta / Comando | Propósito |
|---|---|
| `git status --short` | estado do worktree |
| `git branch --show-current` | branch ativa |
| `git rev-parse HEAD` | SHA do HEAD |
| `git log --oneline -15` | commits recentes |
| `git show --stat 1cc0dff` | estatísticas do commit de fechamento |
| `git show --name-status 1cc0dff` | arquivos incluídos no commit |
| `rg -rl "H-0024"` | artefatos referenciando H-0024 |
| `rg -rl "H-0025"` | artefatos referenciando H-0025 |
| `rg -rl "ADR-0018"` | artefatos referenciando ADR-0018 |
| `find docs/ -name "*.md"` | listagem de todos os artefatos Markdown |
| `Read` (17 arquivos) | leitura integral de cada artefato da cadeia de transição |

## 19. Estado Git final

Após a criação deste relatório, o estado do repositório é:

| Parâmetro | Valor |
|---|---|
| Branch | `master` |
| HEAD | `c003f3e feat: implementa composicao hierarquica do corpo com tres niveis de grupos` |
| Stage | vazio |
| Arquivos rastreados modificados | nenhum |
| Arquivos não rastreados | `docs/relatorios/RELATORIO_LEVANTAMENTO_TRANSICAO_H-0024_H-0025.md` (este relatório) |

Este relatório não foi commitado pelo levantamento. O commit, se desejado,
pertence a etapa posterior não autorizada por este prompt.
