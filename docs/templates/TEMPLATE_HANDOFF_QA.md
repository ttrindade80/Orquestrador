---
name: QA-NNNN-descricao
description: "[preencher] Objetivo verificável da revisão"
metadata:
  type: handoff_qa
  status: READY_FOR_QA
  id: QA-NNNN
  etapa_qa: QA_ADR | QA_APLICACAO_ADR | QA_HANDOFF | QA_IMPLEMENTACAO | QA_POS_PATCH
  camada_auditada: ADR | APLICACAO_ADR | HANDOFF | IMPLEMENTACAO
  data_criacao: YYYY-MM-DD
rastreabilidade:
  adr_alvo: null
  relatorio_aplicacao: null
  handoff_origem: null
  relatorio_impl: null
  relatorio_qa_anterior: null
  contrato_alvo: null
  adr_relacionadas: []
  issues_relacionadas: []
---

# QA-NNNN — Revisar [artefato ou implementação]

## 1. Etapa única

Este handoff executa exclusivamente uma das etapas:

`QA_ADR` | `QA_APLICACAO_ADR` | `QA_HANDOFF` | `QA_IMPLEMENTACAO` | `QA_POS_PATCH`

Não autoriza correção, implementação, commit ou próxima etapa.

## 2. Papel

Atue como auditor independente.

Crie somente o relatório solicitado.
Não corrija durante o QA.
Não aprove a própria produção anterior.

## 3. Manifesto fechado de leitura

```yaml
leitura_integral:
  - [artefato indispensável]
leitura_focal:
  - arquivo: [arquivo ou relatório]
    comando_busca: [comando exato]
    objetivo: [critério, achado ou evidência necessária]
buscas_autorizadas:
  - [caminho, termo e limite exatos]
nao_ler:
  - docs/relatorios/**, salvo item nominalmente autorizado acima
  - [outros caminhos fora do contexto]
```

Status aprovado, IDs de achados, notas materiais e deltas devem ser transportados no prompt sempre que isso evitar leitura de relatório.

Para leitura focal, execute o comando indicado e leia somente sua saída. Não abra o arquivo inteiro por conveniência. Se a saída for insuficiente, pare e solicite expansão focal.

## 4. Autoridades e objetos auditados

Selecione somente os itens aplicáveis:

- `[decisões fechadas, para QA_ADR]`;
- `[ADR auditada ou ADR aplicada]`;
- `[contratos, índices e módulos alterados, para QA_APLICACAO_ADR]`;
- `[handoff auditado]`;
- `[implementação e relatório correspondente]`;
- `[relatório de QA anterior, somente para reteste ou delta]`.

## 5. Escopo da revisão

### Para `QA_ADR`

- fidelidade às decisões fechadas;
- coerência interna;
- autoridade e compatibilidade;
- ausência de decisão, arquitetura, schema ou política inventada;
- critérios de aplicação e fora de escopo.

### Para `QA_APLICACAO_ADR`

- propagação completa da ADR;
- contratos especializados e documentos diretamente afetados;
- índices, backlog e módulos de nomenclatura aplicáveis;
- ausência de contradições normativas ativas;
- conformidade factual do relatório de aplicação;
- preservação do escopo documental e ausência de implementação indevida.

### Para `QA_HANDOFF`, `QA_IMPLEMENTACAO` e `QA_POS_PATCH`

Verificar somente os itens aplicáveis e materialmente necessários:

- autoridade e coerência interna;
- critérios de aceite;
- diff real e escopo autorizado;
- arquivos e diretórios criados, alterados ou não rastreados;
- entradas reais, fixtures, temporários e saídas;
- testes e demonstração operacional;
- prova semântica;
- escopo negativo e autorizações focais;
- estado Git;
- suficiência factual do relatório da etapa;
- validação manual.

## 6. Critérios de QA

| ID | Item | Evidência exigida |
|---|---|---|
| QA-01 | [Item] | [Evidência objetiva] |

## 7. Taxonomia obrigatória

### Para `QA_ADR`

- `ADR_APPROVED`;
- `ADR_APPROVED_WITH_NOTES`;
- `ADR_REJECTED`;
- `BLOCKED_USER_DECISION`;
- `BLOCKED_DOCUMENTATION`.

### Para `QA_APLICACAO_ADR`

- `ADR_APPLICATION_APPROVED`;
- `ADR_APPLICATION_APPROVED_WITH_NOTES`;
- `ADR_APPLICATION_REJECTED`;
- `BLOCKED_DOCUMENTATION`.

### Para `QA_HANDOFF`

- `H1_HANDOFF_APPROVED`;
- `H2_HANDOFF_PATCH_REQUIRED`;
- `H3_BLOCKED_DOCUMENTATION`;
- `H4_QA_EVIDENCE_INCOMPLETE`.

### Para `QA_IMPLEMENTACAO`

- `I1_IMPLEMENTATION_APPROVED`;
- `I2_IMPLEMENTATION_PATCH_REQUIRED`;
- `I3_HANDOFF_PATCH_REQUIRED`;
- `I4_BLOCKED_DOCUMENTATION`;
- `I5_MANUAL_VALIDATION_REQUIRED`.

Em `QA_POS_PATCH`, use a taxonomia da camada retestada. Use em `status_literal` exatamente um valor aplicável.

## 8. Relatório de QA

Criar novo relatório em:

```text
docs/relatorios/<nome-canonico>.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_QA.md
```

Regras:

- cada QA produz relatório próprio e nunca sobrescreve QA anterior;
- QA aprovado sem achados: máximo normal de 250 palavras;
- QA com achados materiais: máximo normal de 900 palavras;
- não criar matriz completa de itens conformes;
- achado deve registrar ID estável, requisito violado, evidência focal, impacto e correção necessária;
- QA pós-patch registra somente achados tratados, resolvidos, pendentes e novos, referenciando raiz e predecessor imediato;
- evidência separada, quando indispensável, permanece em `docs/relatorios/`;
- o relatório não corrige a entrega nem gera a etapa seguinte.

## 9. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/<arquivo>.md
bloqueios:
  - <somente quando houver>
proxima_acao: <somente quando objetivamente determinada>
```

Omitir campos vazios. Não copiar o relatório nem acrescentar conclusão narrativa.

## 10. Limite de encerramento

Concluído o relatório, pare.

Não corrija.
Não implemente.
Não gere o prompt da etapa seguinte.
Não prepare nem execute commit.
Não inicie outro ciclo.
