---
name: ADR-0033-separacao-backlog-historico-e-arquivo-documental
description: Separação entre backlog ativo, histórico compacto de encerramentos e área de documentos obsoletos sem autoridade vigente
metadata:
  type: adr
  status: aceita
  id: ADR-0033
  data: 2026-07-27
  substitui: null
rastreabilidade:
  decisao_usuario: "D-HIST-01 a D-HIST-14 — separação entre docs/backlog.md (planejamento ativo), docs/HISTORICO.md (histórico compacto de encerramentos) e docs/arquivo/ (documentos obsoletos preservados, sem autoridade vigente), incluindo migração nominal inicial de docs/build_docs/ e fechamento do ITEM-0002"
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados: []
  handoffs_bloqueados: []
---

# ADR-0033 — Separação entre backlog, histórico e arquivo documental

## 1. Status

`aceita`

## 2. Contexto

`docs/backlog.md` hoje mistura trabalho ainda ativo com itens já encerrados
(o próprio `ITEM-0002` permanece no backlog com estado factual de
implementação concluída, aguardando apenas fechamento Git). Não existe
nenhum artefato canônico para registrar de forma compacta o que já foi
encerrado, o que obriga a reconstrução do histórico a partir de ADRs,
handoffs e relatórios dispersos em `docs/relatorios/`.

Paralelamente, `docs/build_docs/instruction.md` já declara `docs/build_docs/`
como pasta temporária, "arquivada depois que a documentação estiver
fechada". O `to_do.md` legado dessa pasta acumulou itens `concluido`,
itens bloqueados sem decisão e itens cuja pendência foi superada por
decisões posteriores, sem que exista uma área documental para preservar
esses artefatos com o status explícito de não terem mais autoridade
normativa vigente.

Não existe hoje distinção formal entre documento vigente e documento
histórico, nem regra de onde e como preservar evidência de encerramento
sem duplicar o conteúdo detalhado que já vive em ADRs, handoffs, contratos
e commits.

## 3. Decisão explícita do usuário

- **D-HIST-01**: `docs/backlog.md` passa a conter somente trabalho ativo;
  `docs/HISTORICO.md` passa a conter itens encerrados; documentos obsoletos
  preservados integralmente ficam em `docs/arquivo/`; ADRs, handoffs,
  contratos, relatórios e commits continuam sendo as autoridades e
  evidências detalhadas — o histórico não os reproduz.
- **D-HIST-02**: os únicos estados permitidos no backlog passam a ser
  `planejado`, `bloqueado`, `em_andamento` e `pronto_para_handoff`. Estados
  de encerramento não permanecem no backlog.
- **D-HIST-03**: no mesmo fechamento documental em que um item for
  encerrado, ele é removido de `docs/backlog.md` e registrado em
  `docs/HISTORICO.md`, com resultado `CONCLUIDO`, `CANCELADO`,
  `SUBSTITUIDO` ou `INCOMPATIVEL`.
- **D-HIST-04**: o caminho canônico inicial do histórico é
  `docs/HISTORICO.md`, ao lado de `docs/backlog.md`; estrutura maior,
  divisão por períodos ou múltiplos arquivos só poderá ser adotada em
  decisão futura própria.
- **D-HIST-05**: as entradas de `docs/HISTORICO.md` são agrupadas em
  Concluídos, Cancelados, Substituídos e Incompatíveis, ordenadas
  crescentemente pelo identificador original dentro de cada seção, no
  formato mínimo definido no prompt (identificador, resultado, origem,
  data, referências, resumo e motivo quando aplicável), preservando
  identificadores originais e usando `NAO_CONFIRMADA` em vez de inventar
  dado ausente.
- **D-HIST-06**: o caminho canônico da área de documentos obsoletos é
  `docs/arquivo/`, preservando a estrutura de origem, com
  `docs/arquivo/README.md` declarando natureza histórica, ausência de
  autoridade normativa vigente, proibição de orientar trabalho atual,
  proibição de carregamento por padrão e leitura restrita a pesquisa
  histórica explicitamente autorizada.
- **D-HIST-07**: todo arquivo movido para `docs/arquivo/` deve começar com
  o aviso literal de documento histórico sem autoridade vigente definido
  no prompt.
- **D-HIST-08**: migração inicial nominal de `docs/build_docs/instruction.md`,
  `docs/build_docs/prompts.md` e `docs/build_docs/to_do.md` para
  `docs/arquivo/build_docs/`, preservando estrutura; após a migração,
  `docs/build_docs/` deixa de integrar a documentação ativa.
- **D-HIST-09**: todos os itens marcados `concluido` no `to_do.md` legado
  são aceitos como realizados e registrados compactamente em
  `docs/HISTORICO.md`, sem exigência de commit individual quando ausente
  na entrada legada e sem inventar dado ausente; `DOC-0019` e `DOC-0022`
  também entram como concluídos.
- **D-HIST-10**: `DOC-B003`, `DOC-B004`, `DOC-B007`, `DOC-B008` e
  `DOC-B009` são registrados em `docs/HISTORICO.md` como `CANCELADO`, com
  os motivos compactos definidos no prompt para cada um.
- **D-HIST-11**: criação no backlog de `ITEM-0015` (aplicar ADR-0008 aos
  contratos de cabeçalho e estilo), `ITEM-0016` (reconciliar o
  comportamento de `tx` no console) e `ITEM-0017` (avaliar a necessidade
  de `popup_execucao`), todos com `status: bloqueado` e sem campo de
  origem legada, cada um com o motivo de bloqueio específico definido no
  prompt.
- **D-HIST-12**: fechamento do `ITEM-0002` — remoção de `docs/backlog.md`
  e registro em `docs/HISTORICO.md` como `CONCLUIDO`, com os dados
  comprovados fornecidos no prompt (ADR-0031, H-0040, commit
  `13d743d2def11ea4e32b936d9b5accb71346dc5c`, data 2026-07-26).
- **D-HIST-13**: os itens ativos `ITEM-0003` a `ITEM-0014` permanecem no
  backlog, sujeitos apenas à nova taxonomia de estados; nenhum deles é
  concluído, cancelado ou reescrito por inferência nesta ADR.
- **D-HIST-14**: `docs/INDICE.md` deve identificar `docs/backlog.md` como
  planejamento ativo, `docs/HISTORICO.md` como registro compacto de
  encerramentos e `docs/arquivo/` como área histórica sem autoridade
  vigente.

## 4. Decisão

Fica adotada a separação em três papéis documentais distintos e
mutuamente exclusivos:

**Planejamento ativo — `docs/backlog.md`.** Contém somente itens ainda não
encerrados. Os únicos estados permitidos são `planejado`, `bloqueado`,
`em_andamento` e `pronto_para_handoff` (D-HIST-02). Nenhum item em estado
de encerramento permanece neste arquivo.

**Histórico compacto — `docs/HISTORICO.md`.** Caminho canônico inicial, ao
lado de `docs/backlog.md` (D-HIST-04). Registra, em forma compacta, itens
encerrados com resultado `CONCLUIDO`, `CANCELADO`, `SUBSTITUIDO` ou
`INCOMPATIVEL`. As entradas são agrupadas nas quatro seções correspondentes
— Concluídos, Cancelados, Substituídos, Incompatíveis — ordenadas
crescentemente pelo identificador original dentro de cada seção, no formato
mínimo definido em D-HIST-05 (identificador e título, `Resultado`,
`Origem`, `Data`, `Referências`, `Resumo` e `Motivo` quando aplicável). O
histórico preserva identificadores originais, não inventa data, commit ou
referência ausente (usa `NAO_CONFIRMADA` quando necessário) e não copia
descrição extensa — a evidência detalhada permanece nos documentos de
origem (ADR, handoff, contrato, relatório, commit) ou em seu arquivo
histórico correspondente. O histórico não é autoridade nem evidência
detalhada; é apenas registro compacto de encerramento.

**Arquivo documental — `docs/arquivo/`.** Caminho canônico para documentos
obsoletos preservados integralmente, com a estrutura de origem mantida
(D-HIST-06). A área possui `docs/arquivo/README.md`, que declara que os
documentos ali contidos são históricos, não possuem autoridade normativa
vigente, não devem orientar trabalho atual, não devem ser carregados por
padrão e só podem ser lidos em pesquisa histórica explicitamente
autorizada. Todo arquivo movido para `docs/arquivo/` recebe, no início do
arquivo, o aviso literal definido em D-HIST-07.

**Movimentação no encerramento.** No mesmo fechamento documental em que um
item for encerrado, ele é removido de `docs/backlog.md` e registrado em
`docs/HISTORICO.md` (D-HIST-03). Não há estado intermediário em que um item
encerrado permaneça simultaneamente no backlog e no histórico.

**Migração inicial nominal de `docs/build_docs/`.** Os três arquivos
`docs/build_docs/instruction.md`, `docs/build_docs/prompts.md` e
`docs/build_docs/to_do.md` são movidos para `docs/arquivo/build_docs/`,
preservando a estrutura, cada um recebendo o aviso de D-HIST-07 no início.
Após a migração, `docs/build_docs/` deixa de integrar a documentação ativa
(D-HIST-08).

**Tratamento dos itens do `to_do.md` legado.** Todos os itens marcados
`concluido` no `to_do.md` legado são aceitos como realizados e registrados
compactamente em `docs/HISTORICO.md`, incluindo `DOC-0019` e `DOC-0022`
como concluídos posteriormente; ausência de commit individual na entrada
legada não impede o registro, e dado ausente não é inventado (D-HIST-09).
`DOC-B003`, `DOC-B004`, `DOC-B007`, `DOC-B008` e `DOC-B009` são registrados
como `CANCELADO`, com os motivos compactos definidos em D-HIST-10.

**Novos itens de backlog derivados de pendências legadas.** `ITEM-0015`,
`ITEM-0016` e `ITEM-0017` são criados em `docs/backlog.md`, todos em
`status: bloqueado`, sem campo de origem legada, com os motivos de bloqueio
específicos de D-HIST-11.

**Fechamento do `ITEM-0002`.** `ITEM-0002` é removido de `docs/backlog.md`
e registrado em `docs/HISTORICO.md` como `CONCLUIDO`, com os dados
comprovados de D-HIST-12 (ADR-0031, H-0040, commit
`13d743d2def11ea4e32b936d9b5accb71346dc5c`, data 2026-07-26).

**Itens ativos preservados.** `ITEM-0003` a `ITEM-0014` permanecem em
`docs/backlog.md`, sujeitos apenas à nova taxonomia de estados definida em
D-HIST-02; nenhum deles é encerrado, cancelado ou reescrito por inferência
por esta ADR (D-HIST-13).

**Roteamento no índice.** `docs/INDICE.md` passa a identificar
`docs/backlog.md` como planejamento ativo, `docs/HISTORICO.md` como
registro compacto de encerramentos e `docs/arquivo/` como área histórica
sem autoridade vigente (D-HIST-14).

## 5. Consequências

### Positivas

- Elimina a ambiguidade entre item ainda ativo e item já encerrado dentro
  de `docs/backlog.md`.
- Dá lugar canônico e compacto para consulta rápida de encerramentos, sem
  exigir garimpo em `docs/relatorios/` para saber o que já foi concluído,
  cancelado, substituído ou tornado incompatível.
- Formaliza que documento preservado em `docs/arquivo/` não deve ser
  carregado por padrão nem confundido com fonte normativa vigente,
  reduzindo risco de trabalho futuro se apoiar em decisão superada.
- Resolve o estado pendente de `docs/build_docs/` (declarado desde sua
  criação como pasta temporária) e do `ITEM-0002` (já implementado e
  validado, aguardando apenas fechamento documental).

### Custos e restrições

- Exige aplicação documental subsequente para criar `docs/HISTORICO.md`,
  `docs/arquivo/README.md`, mover os três arquivos de `docs/build_docs/` e
  atualizar `docs/backlog.md` e `docs/INDICE.md` antes de a separação
  produzir efeito prático.
- Introduz um artefato novo (`docs/HISTORICO.md`) cuja estrutura de seções
  e ordenação precisa ser respeitada em todo fechamento futuro de item de
  backlog.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `docs/backlog.md` | remover `ITEM-0002`; adicionar `ITEM-0015`, `ITEM-0016`, `ITEM-0017` em `bloqueado`; reclassificar `ITEM-0003` a `ITEM-0014` pela taxonomia de D-HIST-02 |
| `docs/HISTORICO.md` | criar; registrar `ITEM-0002`, itens `concluido` do `to_do.md` legado (incluindo `DOC-0019` e `DOC-0022`) e `DOC-B003`, `DOC-B004`, `DOC-B007`, `DOC-B008`, `DOC-B009` como `CANCELADO` |
| `docs/arquivo/README.md` | criar, com as quatro declarações de D-HIST-06 |
| `docs/arquivo/build_docs/instruction.md` | criar por migração de `docs/build_docs/instruction.md`, com aviso de D-HIST-07 |
| `docs/arquivo/build_docs/prompts.md` | criar por migração de `docs/build_docs/prompts.md`, com aviso de D-HIST-07 |
| `docs/arquivo/build_docs/to_do.md` | criar por migração de `docs/build_docs/to_do.md`, com aviso de D-HIST-07 |
| `docs/build_docs/` | deixa de integrar a documentação ativa após a migração |
| `docs/INDICE.md` | identificar `docs/backlog.md`, `docs/HISTORICO.md` e `docs/arquivo/` conforme D-HIST-14 |

## 6. Compatibilidade e transição

Esta ADR não executa a migração nem altera nenhum dos artefatos afetados —
apenas registra a decisão fechada. Até a aplicação, `docs/backlog.md`
continua contendo `ITEM-0002`, `docs/HISTORICO.md` e `docs/arquivo/` ainda
não existem, e `docs/build_docs/` permanece no lugar atual.

Não há alias permanente para `docs/build_docs/`: após a aplicação, os três
arquivos passam a existir somente em `docs/arquivo/build_docs/` e a pasta
`docs/build_docs/` deixa de integrar a documentação ativa (D-HIST-08).

Rastreabilidade é preservada por construção: o histórico compacto sempre
referencia ADR, handoff e commit quando conhecidos, e nunca substitui a
evidência detalhada já registrada nesses documentos ou em `docs/relatorios/`.

## 7. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR: a separação entre
backlog, histórico e arquivo, a taxonomia de estados e resultados, e a
migração nominal inicial já constituem decisão fechada fornecida ao autor
documental. Esta ADR não escolhe entre opções.

## 8. Itens fora de escopo

- Execução da migração documental (criação de `docs/HISTORICO.md`,
  `docs/arquivo/README.md`, movimentação dos três arquivos de
  `docs/build_docs/`, edição de `docs/backlog.md` e `docs/INDICE.md`) —
  pertence à aplicação desta ADR, não à sua criação.
- Alteração de código, criação de handoff e implementação funcional.
- Revisão do conteúdo técnico dos itens `ITEM-0003` a `ITEM-0014`.
- Arquivamento de qualquer documento além dos três arquivos de
  `docs/build_docs/` nominados em D-HIST-08.
- Reorganização futura de `docs/HISTORICO.md` (divisão por período ou por
  múltiplos arquivos) — permanece como decisão futura própria (D-HIST-04).
- Solução técnica de `ITEM-0015`, `ITEM-0016` e `ITEM-0017`.
- Criação de changelog ou release notes.
- Push Git.

## 9. Critérios para aplicação

- [ ] `docs/backlog.md` contém somente `ITEM-0003` a `ITEM-0017`, nos
  estados `planejado | bloqueado | em_andamento | pronto_para_handoff`,
  sem `ITEM-0002`.
- [ ] `docs/HISTORICO.md` foi criado com as quatro seções (Concluídos,
  Cancelados, Substituídos, Incompatíveis), entradas ordenadas
  crescentemente pelo identificador original dentro de cada seção.
- [ ] `ITEM-0002` está registrado em `docs/HISTORICO.md` como `CONCLUIDO`
  com os dados comprovados de D-HIST-12.
- [ ] Itens `concluido` do `to_do.md` legado (incluindo `DOC-0019` e
  `DOC-0022`) estão registrados como `CONCLUIDO`; `DOC-B003`, `DOC-B004`,
  `DOC-B007`, `DOC-B008` e `DOC-B009` estão registrados como `CANCELADO`
  com os motivos compactos de D-HIST-10; nenhum dado ausente foi inventado.
- [ ] `ITEM-0015`, `ITEM-0016` e `ITEM-0017` foram criados em
  `docs/backlog.md` como `bloqueado`, sem campo de origem legada.
- [ ] `docs/arquivo/README.md` foi criado com as quatro declarações de
  D-HIST-06.
- [ ] Os três arquivos de `docs/build_docs/` foram migrados para
  `docs/arquivo/build_docs/` preservando a estrutura, cada um com o aviso
  de D-HIST-07 no início.
- [ ] `docs/build_docs/` deixou de integrar a documentação ativa após a
  migração.
- [ ] `docs/INDICE.md` foi atualizado identificando `docs/backlog.md`,
  `docs/HISTORICO.md` e `docs/arquivo/` conforme suas novas funções.
- [ ] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [ ] A aplicação foi submetida a QA independente.

## 10. Bloqueios

nenhum
