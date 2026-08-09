---
name: REL-QA-ADR-0043-P01
metadata:
  type: relatorio_qa
  etapa_qa: QA_POS_PATCH
  camada_auditada: ADR
  status: ADR_APPROVED
  data: 2026-08-08
rastreabilidade:
  adr_auditada: docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
  cadeia_raiz: RELATORIO_QA_ADR-0043
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_ADR-0043_P01.md
  achados_tratados: [ADR-0043-A, ADR-0043-B, ADR-0043-C, ADR-0043-D]
---

# REL-QA-ADR-0043-P01

## 1. Identificação e status

```yaml
revisao: ADR-0043 P01
etapa_qa: QA_POS_PATCH
camada_auditada: ADR
status_literal: ADR_APPROVED
status_normalizado: ADR_APPROVED
proxima_categoria: APLICAR_ADR
```

## 2. Escopo e autoridades

```yaml
objeto_auditado: ADR-0043, achados A-D e regressões diretas de P01
autoridades_materiais: [ADR-0042, nomenclaturas 31/32, contratos barra/chip]
```

## 3. Verificações

```yaml
preflight: OK — master, HEAD esperado, stage vazio, relatório QA ausente
reteste: OK — leitura prescrita e buscas focais confirmaram A-D
regressao_P01: OK — nenhuma material
```

## 4. Achados

| ID | Estado | Evidência focal |
|---|---|---|
| ADR-0043-A | RESOLVIDO | D-CHIP-09 exige cursor/item válido; sem nós visíveis, árvore não focalizável; reconciliação sem fallback novo. |
| ADR-0043-B | RESOLVIDO | Efeitos semânticos `[␣] Recolher`/`[␣] Expandir`; nenhum ID, registry ou schema técnico. |
| ADR-0043-C | RESOLVIDO | D-CHIP-03 usa a faixa vigente, antes de Ajuda, que permanece último chip; não cria segunda ordem. |
| ADR-0043-D | RESOLVIDO | Rastreabilidade contém ITEM-0007/H-0053; §7 mantém H-0053 interrompido até aplicação e reconciliação. |

Novos achados materiais: nenhum.

## 5. Delta de QA pós-patch

```yaml
raiz: RELATORIO_QA_ADR-0043
predecessor_imediato: RELATORIO_PATCH_ADR-0043_P01
achados_resolvidos: [ADR-0043-A, ADR-0043-B, ADR-0043-C, ADR-0043-D]
achados_pendentes: []
novos_achados: []
```

## 8. Estado Git

```yaml
branch: master
HEAD: 0bf6c51ea67b66f9d3f990048e7c24fd01b8fe2d
staged: vazio
nao_rastreados: ciclo ADR-0043/H-0053
```

## 9. Conclusão

A-D estão resolvidos; P01 não introduziu defeito material. Próxima ação:
`APLICAR_ADR`.
