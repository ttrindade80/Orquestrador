---
name: RELATORIO_QA_ADR-0043
description: "Resultado factual da auditoria normativa da ADR-0043"
metadata:
  type: relatorio_qa
  etapa_qa: QA_ADR
  camada_auditada: ADR
  status: BLOCKED_USER_DECISION
  data: 2026-08-08
rastreabilidade:
  autorizacao_qa: "QA_ADR ADR-0043"
  adr_auditada: docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
  adr_relacionadas:
    - docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
    - docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
    - docs/adr/ADR-0042-navegacao-multinivel-do-console.md
---

# RELATORIO_QA_ADR-0043 — Relatório de QA

## 1. Identificação e status

```yaml
revisao: ADR-0043 — Ajuda universal e chip contextual de expandir/recolher
etapa_qa: QA_ADR
camada_auditada: ADR
status_literal: BLOCKED_USER_DECISION
status_normalizado: BLOCKED_USER_DECISION
proxima_categoria: DECISAO_USUARIO
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/adr/ADR-0043-ajuda-universal-e-chip-contextual-de-expandir-recolher.md
autoridades_materiais:
  - ADR-0012; contrato_barra_de_menus; contrato_chip
  - nomenclatura 31_BARRA_DE_MENUS_E_CHIPS e 32_CONSOLE
  - ADR-0041 e ADR-0042, em leitura focal
escopo:
  - Ajuda universal, identidade contextual de Espaço e estados do chip
  - ordem, rastreabilidade, limites de aplicação e H-0053
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: V-01
    comando_ou_metodo: preflight Git e leitura integral do manifesto
    evidencia_focal: branch master; HEAD 0bf6c51; stage vazio; ADR existente; relatório ausente
    resultado: OK
  - id: V-02
    comando_ou_metodo: comparação com decisões D-CHIP-01 a D-CHIP-12 e gramática vigente
    evidencia_focal: Ajuda obrigatória, última, persistente e sujeita a erro de layout; restante declarativo
    resultado: OK
  - id: V-03
    comando_ou_metodo: comparação com ADR-0042 e contrato do chip
    evidencia_focal: ramo/folha e separação de seleção preservados; D-CHIP-09 não fecha ausência de item corrente
    resultado: FALHA
  - id: V-04
    comando_ou_metodo: comparação da ordem canônica e dos exemplos D-CHIP-05/D-CHIP-06
    evidencia_focal: posição do contextual só é definida como “antes de Ajuda”; `acao:` usa forma de campo técnico
    resultado: FALHA
  - id: V-05
    comando_ou_metodo: auditoria dos §§6–9, 10 e 12
    evidencia_focal: aplicação documental, reconciliação H-0053, demonstração multilinha e backlog estão separados
    resultado: OK
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| ADR-0043-A | bloqueante | D-CHIP-09 deve fechar ou impedir a transferência de decisão normativa | §§3.8–3.9: para console sem item corrente, remete à gramática vigente ou manda bloquear; as autoridades não definem o estado deste chip nesse caso, embora páginas sem item/console sem cursor sejam possíveis | A aplicação pode precisar decidir se o chip é ausente, inativo ou tratado de outra forma | Decisão do usuário sobre o estado/escopo sem item corrente, ou regra normativa explícita que mantenha o bloqueio sem declarar a ADR aplicável |
| ADR-0043-B | alto | Não criar identificador técnico não decidido | D-CHIP-05/D-CHIP-06, §§3.4–3.5, usam `acao: recolher_ramo_corrente` e `acao: expandir_ramo_corrente` em YAML sob o rótulo “estado semântico”; `contrato_chip` usa `acao` como referência a ação registrada | A aplicação pode interpretar os valores como IDs de schema/registry e criar contrato funcional antecipado | Marcar inequivocamente esses valores como descrição semântica, sem campo `acao` técnico nem identificador registrável |
| ADR-0043-C | alto | Preservar a ordem relativa canônica dos chips simultâneos | D-CHIP-03 e critério §9 só exigem contextual antes de Ajuda; a gramática vigente fixa relações adicionais entre `[␣]`, `[⏎]`, específicos, `[V]` e `[?]` | Instâncias com outros chips podem receber duas ordenações compatíveis com o texto da ADR | Fixar a posição do contextual na gramática existente, sem redefinir a ordem completa |
| ADR-0043-D | médio | Rastreabilidade operacional verdadeira | Frontmatter declara `handoffs_bloqueados: []`, enquanto §7 registra H-0053 pendente de reconciliação e validação manual suspensa; o contexto operacional mantém H-0053 interrompido | A cadeia não identifica o handoff que impede a retomada operacional | Corrigir a rastreabilidade para refletir H-0053 como bloqueado/interrompido, ou declarar explicitamente a distinção operacional adotada |

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: leitura documental e comparação normativa; sem execução de código
    resultado_compacto: achados materiais registrados acima
    prova_semantica: tabelas e critérios da ADR confrontados com as autoridades vigentes
demonstracao:
  resultado: NAO_APLICAVEL
validacao_manual:
  necessaria: NAO_APLICAVEL_NESTA_ETAPA
```

## 8. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 0bf6c51ea67b66f9d3f990048e7c24fd01b8fe2d
  staged: vazio
  unstaged: alterações preexistentes do ciclo H-0053, preservadas
  nao_rastreados: ADR-0043 e artefatos do ciclo H-0053, preservados
```

## 9. Conclusão

A ADR preserva as decisões fechadas principais, mas não pode seguir para
aplicação enquanto a ausência de item corrente permanecer sem decisão
normativa inferível. Os demais achados também exigem correção antes da
aplicação para impedir criação de identificador técnico, ambiguidade de ordem
e rastreabilidade falsa. Próxima ação: `DECISAO_USUARIO`.
