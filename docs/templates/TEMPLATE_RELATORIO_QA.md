---
name: REL-QA-NNNN-descricao
description: "[preencher] Resultado factual da auditoria"
metadata:
  type: relatorio_qa
  etapa_qa: QA_ADR | QA_APLICACAO_ADR | QA_HANDOFF | QA_IMPLEMENTACAO | QA_POS_PATCH
  camada_auditada: ADR | APLICACAO_ADR | HANDOFF | IMPLEMENTACAO
  status: "[usar taxonomia aplicável]"
  data: YYYY-MM-DD
rastreabilidade:
  autorizacao_qa: null
  adr_auditada: null
  relatorio_aplicacao: null
  handoff_origem: null
  relatorio_impl: null
  relatorio_qa_anterior: null
  contrato_alvo: null
  adr_relacionadas: []
  issues_relacionadas: []
  cadeia_raiz: null
  predecessor_imediato: null
  achados_tratados: []
---

# REL-QA-NNNN — Relatório de QA

> Relatório sucinto, factual, assertivo e autocontido. Omitir seções e campos vazios.
>
> QA aprovado sem achados: máximo normal de 250 palavras. QA com achados materiais: máximo normal de 900 palavras.
>
> Este relatório não corrige a entrega, não gera a próxima etapa e nunca sobrescreve relatório de QA anterior.

## 1. Identificação e status

```yaml
revisao: [identificador e título da auditoria]
etapa_qa: QA_ADR | QA_APLICACAO_ADR | QA_HANDOFF | QA_IMPLEMENTACAO | QA_POS_PATCH
camada_auditada: ADR | APLICACAO_ADR | HANDOFF | IMPLEMENTACAO
status_literal:
status_normalizado:
proxima_categoria:
```

### Taxonomia de ADR

- `ADR_APPROVED`;
- `ADR_APPROVED_WITH_NOTES`;
- `ADR_REJECTED`;
- `BLOCKED_USER_DECISION`;
- `BLOCKED_DOCUMENTATION`.

### Taxonomia de aplicação da ADR

- `ADR_APPLICATION_APPROVED`;
- `ADR_APPLICATION_APPROVED_WITH_NOTES`;
- `ADR_APPLICATION_REJECTED`;
- `BLOCKED_DOCUMENTATION`.

### Taxonomia de handoff

- `H1_HANDOFF_APPROVED`;
- `H2_HANDOFF_PATCH_REQUIRED`;
- `H3_BLOCKED_DOCUMENTATION`;
- `H4_QA_EVIDENCE_INCOMPLETE`.

### Taxonomia de implementação

- `I1_IMPLEMENTATION_APPROVED`;
- `I2_IMPLEMENTATION_PATCH_REQUIRED`;
- `I3_HANDOFF_PATCH_REQUIRED`;
- `I4_BLOCKED_DOCUMENTATION`;
- `I5_MANUAL_VALIDATION_REQUIRED`.

Use somente a taxonomia da camada auditada. Em `QA_POS_PATCH`, reutilize a taxonomia da camada retestada; não invente status específico de pós-patch.

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado:
autoridades_materiais:
  - [caminho, decisão ou seção]
escopo:
  - [item auditado]
```

Não registre a lista completa de tudo que foi lido. Não repita status já transportados sem necessidade.

## 3. Verificações executadas

```yaml
verificacoes:
  - id:
    comando_ou_metodo:
    evidencia_focal:
    resultado: OK | FALHA | INCOMPLETA | NAO_VERIFICADO
```

Em QA aprovado, registre apenas os grupos materiais de verificações; não crie matriz completa de itens conformes.

## 4. Achados

[Use `nenhum` quando não houver achados.]

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| [ID] | bloqueante/alto/médio/baixo/observação | | | | |

Não aplique patch nem proponha mudança fora do achado comprovado.

## 5. Delta de QA pós-patch

[Omitir fora de `QA_POS_PATCH`. Não repetir a descrição completa dos achados anteriores.]

```yaml
raiz:
predecessor_imediato:
achados_tratados: []
achados_resolvidos: []
achados_pendentes: []
novos_achados: []
```

## 6. Testes, demonstração e validação manual

[Omitir itens não aplicáveis.]

```yaml
testes_ou_metodos:
  - comando_ou_metodo:
    resultado_compacto:
    prova_semantica:
demonstracao:
  resultado:
  evidencia:
validacao_manual:
  necessaria:
  metodo_reproduzivel:
  resultado:
  criterios_pendentes: []
```

Código de saída zero, isoladamente, não basta.

Use `VALIDACAO_MANUAL_INCONCLUSIVA` quando faltar método reproduzível. Reserve `MANUAL_VALIDATION_FAILED` para comportamento reproduzido e incorreto.

## 7. Evidências separadas

[Omitir quando toda a evidência material estiver contida neste relatório.]

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```

Nenhuma evidência material pode permanecer somente em `/tmp`.

## 8. Estado Git e itens inesperados

Registre somente divergências ou fatos materiais:

```yaml
estado_git_compacto:
  branch:
  HEAD:
  staged:
  unstaged:
  nao_rastreados:
itens_inesperados:
  - item:
    origem: NAO_CONFIRMADA | CONFIRMADA
    evidencia:
```

Não copie a saída Git completa quando o estado estiver conforme.

## 9. Conclusão

[Justifique o status em uma síntese curta, usando somente as evidências registradas. Não repita as seções anteriores.]
