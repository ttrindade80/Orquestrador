---
name: ADR-0032-uso-obrigatorio-de-templates-canonicos
description: Uso obrigatório de templates canônicos depositados em docs/templates/ para artefatos e relatórios de agentes
metadata:
  type: adr
  status: aceita
  id: ADR-0032
  data: 2026-07-26
  substitui: null
rastreabilidade:
  decisao_usuario: "D-TPL-CICLO-01 a D-TPL-07 — pacote canônico de templates em docs/templates/ passa a ser uso obrigatório para artefatos e relatórios de agentes, após aplicação e QA aprovados"
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_processo_desenvolvimento.md
  handoffs_bloqueados: []
---

# ADR-0032 — Uso obrigatório de templates canônicos

## 1. Status

`aceita`

## 2. Contexto

O Orquestrador acumulou múltiplos padrões de relatório e de artefato documental
sem um pacote único e resolvido de templates. `docs/relatorios/README.md` é
legado: define uma matriz reduzida de tipos (`IMP-NNNN`, `REL-QA-NNNN`,
`REL-DOC-NNNN`) e trata auditoria documental como adaptação do template de QA,
em vez de template próprio. `docs/adr/INDICE_ADR.md` já referencia
`docs/templates/TEMPLATE_ADR.md` como fonte de criação de ADR, mas não há
regra geral que estenda a obrigatoriedade a todos os artefatos e relatórios
produzidos por agentes.

Um levantamento prévio (`docs/relatorios/RELATORIO_LEVANTAMENTO_TEMPLATES_RELATORIOS.md`)
identificou o pacote hoje depositado em `docs/templates/`. Esta ADR formaliza
a decisão já fechada de tornar esse pacote de uso obrigatório, sem redesenhar
seu conteúdo e sem aplicar a mudança nos documentos afetados.

## 3. Decisão explícita do usuário

- Ciclo puramente documental: após `QA_APLICACAO_ADR` aprovado, o fluxo segue
  para análise documental final e fechamento manual, sem handoff,
  implementação, QA de handoff ou QA de implementação.
- O pacote canônico é exatamente o conjunto depositado em `docs/templates/`
  no momento desta ADR (índice, 5 artefatos documentais, 9 templates de
  relatórios e evidências).
- A obrigatoriedade entra em vigor somente após a aprovação da aplicação
  (`QA_APLICACAO_ADR`); a própria criação, QA, aplicação e QA da aplicação
  desta ADR não ficam sujeitas retroativamente a ela.
- Não há reescrita retroativa de relatórios ou artefatos históricos.
- Ausência de template aplicável, ou conflito material entre template e
  regra vigente, bloqueia a produção do artefato — sem adaptação por
  proximidade e sem estrutura improvisada.
- Durante a aplicação, `docs/templates/00_INDICE_TEMPLATES_RELATORIOS.md`
  será renomeado para `docs/templates/00_INDICE_TEMPLATES_DOCUMENTAIS_E_RELATORIOS.md`,
  com atualização de todas as referências materiais e sem alias permanente.
- `docs/relatorios/README.md` será substituído durante a aplicação por
  roteamento conciso ao índice canônico e regras gerais vigentes, removendo
  a matriz antiga e a adaptação do template de QA para auditoria documental.

## 4. Decisão

Fica adotado como pacote canônico de templates documentais e de relatórios o
conjunto atualmente depositado em `docs/templates/`:

**Índice**
- `docs/templates/00_INDICE_TEMPLATES_RELATORIOS.md` (a ser renomeado na
  aplicação — ver §"Compatibilidade e transição")

**Artefatos documentais**
- `TEMPLATE_ADR.md`
- `TEMPLATE_BUG.md`
- `TEMPLATE_HANDOFF_IMPLEMENTACAO.md`
- `TEMPLATE_HANDOFF_QA.md`
- `TEMPLATE_RFC.md`

**Relatórios e evidências**
- `TEMPLATE_RELATORIO_CRIACAO_DOCUMENTAL.md`
- `TEMPLATE_RELATORIO_APLICACAO_ALTERACAO.md`
- `TEMPLATE_RELATORIO_IMPL.md`
- `TEMPLATE_RELATORIO_PATCH.md`
- `TEMPLATE_RELATORIO_QA.md`
- `TEMPLATE_RELATORIO_BUSCA_LEVANTAMENTO_VERIFICACAO.md`
- `TEMPLATE_RELATORIO_ANALISE_DOCUMENTAL_FINAL.md`
- `TEMPLATE_RELATORIO_BLOQUEIO.md`
- `TEMPLATE_EVIDENCIA_MATERIAL.md`

O baseline factual do depósito, para fins de rastreabilidade, está registrado
por hash SHA-256 no relatório de criação desta ADR. Os hashes documentam o
estado no momento da decisão; não exigem que uma correção material
autorizada preserve o mesmo hash.

**Obrigatoriedade de resolução prévia de um único template.** Todo novo
artefato ou relatório produzido por agente deve, antes de sua produção, ter
exatamente um template canônico resolvido pelo gerente. Não é permitido
produzir o artefato sem essa resolução prévia, nem combinar mais de um
template no mesmo artefato.

**Alcance sobre artefatos, relatórios e evidências.** A obrigatoriedade
abrange:
- os relatórios e evidências produzidos por agentes dentro de
  `docs/relatorios/`;
- a criação de ADR, BUG, handoff de implementação, handoff de QA e RFC.

**Exclusão do relatório externo do gerente.** O relatório externo do
gerente permanece fora desta política e continua regido pelo sistema
externo do gerente.

**Bloqueio por ausência ou conflito de template.** Quando não existir
template canônico aplicável ao artefato ou relatório pretendido, ou houver
conflito material entre o template e a regra vigente, a execução deve
bloquear antes da produção do artefato ou relatório. Não é permitido:
adaptar outro template por proximidade; inventar estrutura ad hoc. O
bloqueio exige criação ou atualização documental formal do pacote antes de
prosseguir.

**Entrada em vigor.** A obrigatoriedade geral desta ADR entra em vigor
somente depois da aprovação de `QA_APLICACAO_ADR`. Até lá, o pacote está
depositado no worktree, mas não é normativamente exigível.

**Não retroatividade.** Relatórios e artefatos históricos não são
reescritos para adequação aos novos templates.
`docs/relatorios/RELATORIO_LEVANTAMENTO_TEMPLATES_RELATORIOS.md` permanece
no formato em que foi criado, como evidência prévia a esta ADR.

**Preservação estrutural do pacote.** O pacote depositado é adotado como
está. Durante a aplicação, somente incompatibilidades materiais comprovadas
com particularidades reais do Orquestrador podem ser corrigidas. Cada
correção deve ser focal e registrada; redesenho amplo do pacote é proibido.

## 5. Consequências

### Positivas

- Elimina a ambiguidade hoje existente entre a matriz legada de
  `docs/relatorios/README.md` e o pacote mais amplo depositado em
  `docs/templates/`.
- Dá cobertura explícita de template a tipos de relatório sem padrão prévio
  (busca/levantamento, análise documental final, bloqueio, evidência
  material, aplicação de alteração).
- Torna a ausência ou o conflito de template um estado de bloqueio explícito,
  em vez de improviso silencioso por agente.

### Custos e restrições

- Exige aplicação documental subsequente em múltiplos pontos de roteamento
  (`docs/INDICE.md`, `docs/adr/INDICE_ADR.md`, `docs/handoff/README.md`,
  `docs/contratos/contrato_processo_desenvolvimento.md`) antes de a regra
  produzir efeito.
- Introduz um ponto de bloqueio adicional no fluxo de trabalho de agentes
  quando o template resolvido não cobrir o caso real.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `docs/templates/00_INDICE_TEMPLATES_RELATORIOS.md` | renomear para `00_INDICE_TEMPLATES_DOCUMENTAIS_E_RELATORIOS.md` |
| `docs/relatorios/README.md` | substituir pelo roteamento conciso e regras gerais vigentes |
| `docs/INDICE.md` | atualizar referência ao índice de templates renomeado |
| `docs/adr/INDICE_ADR.md` | reconciliar com a obrigatoriedade geral de template |
| `docs/handoff/README.md` | reconciliar com a obrigatoriedade geral de template |
| `docs/contratos/contrato_processo_desenvolvimento.md` | reconciliar regras de relatório com o pacote canônico |

## 6. Compatibilidade e transição

O caminho `docs/templates/00_INDICE_TEMPLATES_RELATORIOS.md` é renomeado,
durante a aplicação, para
`docs/templates/00_INDICE_TEMPLATES_DOCUMENTAIS_E_RELATORIOS.md`. Todas as
referências materiais a esse caminho devem ser atualizadas na mesma
aplicação. Não há alias permanente para o caminho antigo: após a aplicação,
o caminho antigo deixa de existir.

## 7. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR: o pacote, seu alcance
e sua entrada em vigor já constituem decisão fechada fornecida ao autor
documental. Esta ADR não escolhe entre opções.

## 8. Itens fora de escopo

- Renomeação do índice, edição de templates, atualização de
  `docs/relatorios/README.md`, `docs/INDICE.md`, `docs/adr/INDICE_ADR.md`,
  `docs/handoff/README.md` e do contrato de processo — tudo isso pertence à
  aplicação desta ADR, não à sua criação.
- Handoff, implementação, QA de handoff e QA de implementação — este ciclo é
  puramente documental.
- Módulos de nomenclatura.
- Sistema externo do gerente e o relatório externo por ele produzido.

## 9. Critérios para aplicação

- [ ] A decisão foi propagada somente aos documentos afetados listados em
  §5 "Artefatos afetados".
- [ ] Não restaram contradições normativas ativas entre
  `docs/relatorios/README.md`, o índice renomeado e os pontos de roteamento
  atualizados.
- [ ] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] Diretórios previstos e criados foram distinguidos.
- [ ] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [ ] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [ ] Evidência material necessária foi preservada no relatório ou em
  arquivo referenciado dentro de `docs/relatorios/`.
- [ ] A aplicação foi submetida a QA independente (`QA_APLICACAO_ADR`).
- [ ] Após `QA_APLICACAO_ADR` aprovado, o ciclo seguiu para análise
  documental final e fechamento manual, sem handoff nem implementação.

## 10. Bloqueios

nenhum
