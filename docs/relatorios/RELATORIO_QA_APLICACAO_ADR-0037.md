---
name: REL-QA-ADR-0037-aplicacao
description: "Auditoria independente da aplicação documental da ADR-0037"
metadata:
  type: relatorio_qa
  etapa_qa: QA_APLICACAO_ADR
  camada_auditada: APLICACAO_ADR
  status: ADR_APPLICATION_REJECTED
  data: 2026-07-29
rastreabilidade:
  autorizacao_qa: ADR-0037
  adr_auditada: docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0037.md
  predecessor_imediato: APLICACAO_ADR-0037
  achados_tratados: []
---

# REL-QA-ADR-0037 — Aplicação documental

## 1. Identificação e status

```yaml
revisao: "ADR-0037 — integração do fluxo focal com dry-run e restauração da origem"
etapa_qa: QA_APLICACAO_ADR
camada_auditada: APLICACAO_ADR
status_literal: ADR_APPLICATION_REJECTED
status_normalizado: ADR_APPLICATION_REJECTED
proxima_categoria: PATCH_APLICACAO_ADR
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: aplicação documental da ADR-0037
autoridades_materiais:
  - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  - contratos, nomenclatura, índice e backlog autorizados
escopo:
  - fidelidade à decisão aprovada, limites de supersessão e ausência de implementação antecipada
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V-01
    comando_ou_metodo: baseline Git, diff autorizado e leitura integral do manifesto
    evidencia_focal: branch/HEAD/stage e caminhos conferem; somente o relatório atual foi acrescentado pela QA
    resultado: OK
  - id: V-02
    comando_ou_metodo: validação JSON e inspeção de config/estilo.json
    evidencia_focal: cor_inativo=cinza, cor_alerta=amarelo; pendência de tiling preservada; sem estado ou ANSI de dry-run
    resultado: OK
  - id: V-03
    comando_ou_metodo: confronto dos contratos e módulos com D-H4-01 a D-H4-10
    evidencia_focal: toggle focal, ativação cumulativa, transição, suspensão, retornos e limpeza estão distribuídos sem novo schema ou duplicação material
    resultado: OK
  - id: V-04
    comando_ou_metodo: leitura focal das ADRs 0034/0036 e contrato_json_console
    evidencia_focal: supersessão limitada a D-SEL-19, fronteira da barra e dois fora de escopo; contrato_json_console preserva documento/envelope e não exige alteração
    resultado: OK
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-APLICACAO-ADR0037-001 | alto | Aplicação deve decorrer de ADR aprovada e manter sua autoridade principal consistente com índice/backlog. | A própria ADR declara `metadata.status: proposta` e seção 1 `proposta`; o índice registra `QA da ADR: ADR_APPROVED` e `aceita`, e o ITEM-0006 declara a aplicação concluída. | Não é possível aprovar a aplicação como aplicação de uma decisão aprovada quando a fonte principal permanece proposta. | Conciliar a ADR-0037 com seu estado aprovado/aceito já registrado a jusante, ou corrigir as declarações a jusante se esse não for o estado oficial. |

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 8af243c336ca5eb3bdc7ae888009ab404c883ab6
  staged: vazio
  divergencia_material: nenhuma_fora_da_baseline_e_do_relatorio_QA
```

## 9. Conclusão

Os contratos, módulos, índice e backlog aplicam as decisões D-H4 sem antecipar
implementação; `ITEM-0011` e `ITEM-0020` permanecem abertos, e a ressalva ao
`contrato_json_console.md` é suficiente porque o envelope externo não muda.
Contudo, a contradição de status da autoridade principal exige patch antes do
aceite da aplicação.
