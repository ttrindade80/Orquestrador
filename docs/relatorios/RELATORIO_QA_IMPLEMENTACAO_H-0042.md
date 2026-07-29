---
name: RELATORIO_QA_IMPLEMENTACAO_H-0042
description: "Auditoria independente da implementação do protocolo focal H-0042"
metadata:
  type: relatorio_qa
  etapa_qa: QA_IMPLEMENTACAO
  camada_auditada: IMPLEMENTACAO
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  data: 2026-07-29
rastreabilidade:
  handoff_origem: docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
  relatorio_impl: docs/relatorios/IMP-0042-protocolo-focal-execucao-sintetica-reversivel.md
  contrato_alvo: docs/contratos/contrato_json_console.md
---

# RELATORIO_QA_IMPLEMENTACAO_H-0042 — Relatório de QA

## 1. Identificação e status

```yaml
revisao: H-0042 — protocolo focal de execução sintética reversível
etapa_qa: QA_IMPLEMENTACAO
camada_auditada: IMPLEMENTACAO
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: H-0042
autoridades_materiais:
  - docs/handoff/H-0042-protocolo-focal-execucao-sintetica-reversivel.md
  - docs/contratos/contrato_json_console.md §§12.1–12.5 e 14
escopo:
  - motor focal, executor, demonstração, fixtures e testes nominais
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V-01
    comando_ou_metodo: gate Git e manifesto nominal
    evidencia_focal: master; f4b5df1; stage vazio; arquivos preservados sem delta
    resultado: OK
  - id: V-02
    comando_ou_metodo: leitura integral autorizada e inspeção estática
    evidencia_focal: protocolo, schema multinível, canais, controles e limpeza conferidos
    resultado: FALHA
  - id: V-03
    comando_ou_metodo: pytest focal, regressivo e completo
    evidencia_focal: 58 passed; 35 passed; 617 passed
    resultado: OK
  - id: V-04
    comando_ou_metodo: sete demonstrações nominais
    evidencia_focal: baseline intacta e temporários removidos em todos os cenários
    resultado: FALHA
```

Critérios CA-01 a CA-18: `OK` quanto às evidências automatizadas e aos cenários nominais executados. Os achados abaixo violam requisitos mandatórios do motor e da demonstração que não são isolados por um CA próprio.

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| ACH-H0042-01 | MATERIAL | Motor não pode executar programa arbitrário sem restrição focal verificável. | `executar_protocolo_focal(..., argv_executor=[sys.executable, '-c', 'import sys; sys.exit(0)'])` invocou o processo (`invocou: True`). | Chamador Python pode substituir o executor autorizado por qualquer executável. | Remover ou encapsular a injeção de `argv_executor` para que o caminho produtivo aceite somente o executor focal autorizado. |
| ACH-H0042-02 | MATERIAL | Contrato §14.5: resultado semanticamente inválido não pode ser classificado como sucesso. | `classificar_processo(0, '{}')` retornou `sucesso`; a função só aplica `json.loads`, sem validar envelope/schema. | Um resultado JSON válido, porém semântico inválido, atravessa a classificação externa como sucesso. | Validar o envelope multinível e o schema de resultado antes de classificar código 0 como sucesso. |
| ACH-H0042-03 | MATERIAL | A demonstração deve tratar como êxito demonstrativo falha operacional e interrupção esperadas. | As invocações nominais retornaram respectivamente `1` e `130`, pois `main` propaga `resultado['codigo_saida']`. | Automação da demonstração interpreta cenários esperados como falha do próprio demonstrador. | Após comprovar o resultado esperado, retornar êxito do demonstrador mantendo o código observado no resumo humano. |

## 6. Testes e demonstração

```yaml
testes_ou_metodos:
  - comando_ou_metodo: pytest focal
    resultado_compacto: 58 passed
  - comando_ou_metodo: pytest regressivo H-0041
    resultado_compacto: 35 passed
  - comando_ou_metodo: pytest completo
    resultado_compacto: 617 passed
demonstracao:
  resultado: cenários semanticamente observados; dois códigos do demonstrador divergentes do requisito
  evidencia: dry-run, real, aviso, parcial, falha, JSON inválido e interrupção
validacao_manual:
  necessaria: false
```

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: f4b5df1
  staged: []
  divergencias_materiais: []
```

## 9. Conclusão

Os testes, cenários nominais, baseline e limpeza estão conformes, mas os três defeitos materiais de fronteira e classificação exigem patch antes da aprovação da implementação.
