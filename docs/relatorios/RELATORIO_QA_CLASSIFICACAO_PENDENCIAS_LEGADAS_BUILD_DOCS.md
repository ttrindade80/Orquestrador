---
name: REL-QA-CLASSIFICACAO-PENDENCIAS-LEGADAS-BUILD-DOCS
description: "Auditoria independente da classificação factual das 10 pendências legadas de docs/build_docs/to_do.md"
metadata:
  type: relatorio_qa
  etapa_qa: QA_APLICACAO_ADR
  camada_auditada: APLICACAO_ADR
  status: QA_CLASSIFICACAO_APPROVED_WITH_NOTES
  data: "2026-07-27"
rastreabilidade:
  autorizacao_qa: null
  adr_auditada: null
  relatorio_aplicacao: docs/relatorios/RELATORIO_CLASSIFICACAO_PENDENCIAS_LEGADAS_BUILD_DOCS.md
  handoff_origem: null
  relatorio_impl: null
  relatorio_qa_anterior: null
  contrato_alvo: null
  adr_relacionadas: [ADR-0008, ADR-0028]
  issues_relacionadas: [DOC-0018, DOC-0019, DOC-0022, DOC-B001, DOC-B002, DOC-B003, DOC-B004, DOC-B007, DOC-B008, DOC-B009]
  cadeia_raiz: null
  predecessor_imediato: null
  achados_tratados: []
---

# REL-QA — Classificação de pendências legadas (build_docs)

## 1. Identificação e status

```yaml
revisao: QA_CLASSIFICACAO_PENDENCIAS_LEGADAS — auditoria de docs/relatorios/RELATORIO_CLASSIFICACAO_PENDENCIAS_LEGADAS_BUILD_DOCS.md
etapa_qa: QA_APLICACAO_ADR
camada_auditada: APLICACAO_ADR
status_literal: QA_CLASSIFICACAO_APPROVED_WITH_NOTES
status_normalizado: APPROVED_WITH_NOTES
proxima_categoria: nenhuma (sem correção obrigatória)
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: as 10 classificações do relatório de levantamento (DOC-0018, DOC-0019, DOC-0022, DOC-B001, DOC-B002, DOC-B003, DOC-B004, DOC-B007, DOC-B008, DOC-B009)
autoridades_materiais:
  - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
  - docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
  - docs/nomenclatura/32_CONSOLE.md, 34_DASHBOARD.md
  - docs/contratos/contrato_console.md, contrato_json_cabecalho.md, contrato_json_dashboard.md, contrato_composicao_corpo.md
  - config/telas/demo/demo.json (draft renomeado de config/telas/orquestrador.json, ver git log)
escopo:
  - reprodução de buscas focais por identificador em todos os 10 itens
  - reprodução do estado Git do arquivo de draft para confirmar proveniência
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V1
    comando_ou_metodo: "rg -n -i 'DOC-0018|DOC-B004|DOC-B007|DOC-B008|DOC-B009' config/telas/demo/demo.json"
    evidencia_focal: notas de pendência literais e vigentes no draft para os 5 itens ATIVO
    resultado: OK
  - id: V2
    comando_ou_metodo: "grep adrs_aplicadas em contrato_cabecalho.md e contrato_estilo.md"
    evidencia_focal: nenhum dos dois lista ADR-0008; contrato_json_cabecalho.md §3 confirma aplicação futura ('quando a ADR-0008 for aplicada')
    resultado: OK
  - id: V3
    comando_ou_metodo: "leitura de docs/nomenclatura/34_DASHBOARD.md e contrato_composicao_corpo.md (R-11)"
    evidencia_focal: tipo mínimo do dashboard fechado e vigente; 'antigo Info' registrado como draft da instância; pendência de alinhamento isolada e remetida a DOC-B004
    resultado: OK
  - id: V4
    comando_ou_metodo: "leitura de docs/INDICE.md linha 134"
    evidencia_focal: descrição de Config já reflete modelo por tela (ADR-0008/0021/0022), não modelo antigo por domínio/componente
    resultado: OK
  - id: V5
    comando_ou_metodo: "rg -i 'popup' e 'segunda pauta' nos alvos autorizados"
    evidencia_focal: DOC-B002 só aparece como 'fora de escopo' em ADR-0006/0007; DOC-B003 tem zero ocorrência vigente
    resultado: OK
  - id: V6
    comando_ou_metodo: "leitura de docs/nomenclatura/32_CONSOLE.md §9/§10 vs. contrato_console.md §5/§6/§21"
    evidencia_focal: divergência real confirmada — nomenclatura declara tx 'sem decisão vigente' (NOM-LEV-017); contrato_console.md descreve truncamento com reticências como comportamento disponível, condicionado à politica_exibicao da instância; ADR-0028 cobre apenas apresentação multinível, não a regra geral de tx
    resultado: OK
  - id: V7
    comando_ou_metodo: "git log --oneline --all -- config/telas/orquestrador.json"
    evidencia_focal: arquivo renomeado para config/telas/demo/demo.json (commit 5b10bc8); conteúdo textual preservado, citações do levantamento continuam válidas
    resultado: OK
  - id: V8
    comando_ou_metodo: "ls docs/HISTORICO.md"
    evidencia_focal: arquivo ainda não existe no repositório
    resultado: OK (observação registrada, não é erro de classificação)
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| N1 | observação | — | `docs/HISTORICO.md` (destino proposto para DOC-0019/DOC-0022) ainda não existe no repositório | Nenhum — destino permanece coerente como alvo a criar; não muda classificação nem exige ação | Nenhuma |
| N2 | observação | — | `contrato_console.md` (metadata) não lista ADR-0028 em `adrs_aplicadas`, embora a §21 a aplique extensamente | Nenhum sobre a classificação de DOC-B001, que permanece NAO_CONFIRMADO por divergência de conteúdo (não de metadado) | Nenhuma nesta auditoria |

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: "rg -n -i" (buscas focais por item, alvos autorizados do manifesto)
    resultado_compacto: 7 classificações confirmadas por evidência vigente fora do estado legado de to_do.md; 3 NAO_CONFIRMADO com ausência de evidência corretamente registrada
    prova_semantica: cada citação do relatório auditado foi reaberta e o trecho citado confere com o arquivo atual
```

## 8. Estado Git e itens inesperados

```yaml
itens_inesperados:
  - item: config/telas/orquestrador.json citado implicitamente pelo histórico do item DOC-B011 não existe mais como arquivo próprio
    origem: CONFIRMADA
    evidencia: git log mostra rename para config/telas/demo/demo.json (commit 5b10bc8); relatório auditado já cita corretamente o caminho atual (config/telas/demo/demo.json), não o caminho antigo
```

## 9. Conclusão

As dez classificações do relatório auditado resistem à reprodução de evidência focal: os cinco `ATIVO` (DOC-0018, DOC-B004, DOC-B007, DOC-B008, DOC-B009) têm pendência textual vigente e não duplicada no backlog atual; os dois `CONCLUIDO_POSTERIORMENTE` (DOC-0019, DOC-0022) têm entrega material completa, com a única pendência residual (alinhamento do dashboard) corretamente isolada em DOC-B004; os três `NAO_CONFIRMADO` (DOC-B001, DOC-B002, DOC-B003) carecem de evidência suficiente, incluindo a divergência real e explícita entre `32_CONSOLE.md` e `contrato_console.md` sobre `tx`. Nenhum destino documental proposto é incoerente. Cobertura dos dez itens confirmada. Status: `QA_CLASSIFICACAO_APPROVED_WITH_NOTES`, com duas observações que não alteram classificação nem destino.
