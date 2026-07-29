---
name: REL-PATCH-H0041-P03-chips-estado-apresentacao
description: "Correção dos chips Espaço/Enter e sincronização após Todos, conectando estado lógico à apresentação"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
  data: 2026-07-28
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0041
  cadeia_raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
  predecessor_imediato: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0041.md
  achados_tratados:
    - H0041-MANUAL-001
    - H0041-MANUAL-002
    - H0041-MANUAL-003
---

# REL-PATCH-H0041-P03 — Chips Espaço/Enter e sincronização após Todos

> Relatório incremental. Apenas o delta desta execução. Não substitui QA nem
> revalidação TTY.

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCH_COMPLETED_AWAITING_QA
```

## 2. Cadeia

```yaml
raiz: docs/relatorios/IMP-0041-selecao-multipla-estado-comandos-e-apresentacao.md
predecessor_imediato: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0041.md
achados_tratados:
  - H0041-MANUAL-001
  - H0041-MANUAL-002
  - H0041-MANUAL-003
achados_resolvidos:
  - H0041-MANUAL-001
  - H0041-MANUAL-002
  - H0041-MANUAL-003
achados_pendentes: []
novos_achados: []
```

## 3. Delta aplicado

### Causa técnica

**H0041-MANUAL-001** (chip Espaço): a fixture declarava `chip_espaco` com
`regra_ativo: "sempre"`, e `_avaliar_regra_ativo` devolvia `True`
incondicionalmente para `"sempre"`. O estado ATIVO/INATIVO do chip Espaço
não derivava da selecionabilidade do item sob cursor — embora o comando
`Espaço` corretamente ignorasse itens não selecionáveis (via
`selecao.alternar`). A função `selecao.chip_espaco_ativo` já decidia
corretamente, mas não era consumida pelo renderer.

**H0041-MANUAL-002/003** (chip Enter e sincronização): o estado lógico
(`regra_ativo: "selecao_vazia"` → `estado_ativo_chips["chip_enter"]`) já
estava correto e se materializava na barra. A auditoria do fluxo
tecla→alteração→contexto→redraw confirmou que `renderizar_estado` lê
`estado["selecoes"]` em cada chamada, de modo que o contexto dos chips é
sempre recalculado sobre o estado vigente — nunca reutiliza contexto
anterior à alteração da seleção. O teste focalizado novo (MANUAL-003)
confirma a sincronização no mesmo quadro.

### Diferença estado lógico vs apresentação

O estado lógico (ATIVO/INATIVO) é propriedade distinta do rótulo e do
texto renderizado. A prova é `estado_ativo_chips` (avaliação de
`regra_ativo`); a caixa baixa é consequência material. O P03 garante que
ambos os chips de seleção (Espaço e Enter) derivam seu estado da mesma
fonte canônica (estado de runtime avaliado por `regra_ativo`), e não por
inferência de rótulo.

```yaml
delta_material:
  - id_achado: H0041-MANUAL-001
    alteracao: >
      regra_ativo do chip Espaço mudou de "sempre" para
      "item_focalizado_selecionavel"; _avaliar_regra_ativo reconhece a nova
      regra e o renderer calcula item_focalizado_selecionavel via
      selecao.chip_espaco_ativo, recalculado a cada render.
  - id_achado: H0041-MANUAL-002
    alteracao: >
      estado lógico do chip Enter (regra_ativo=selecao_vazia) confirmado e
      coberto por teste que percorre a sequência manual e verifica tanto o
      estado quanto a apresentação.
  - id_achado: H0041-MANUAL-003
    alteracao: >
      auditoria do fluxo confirmou sincronização; teste novo verifica que
      uma única renderização após Todos apresenta conjuntamente os 4 tg
      incluídos e o chip Enter INATIVO.
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_H-0041_P03.md
arquivos_alterados:
  - caminho: tela/renderizador.py
    delta: >
      _avaliar_regra_ativo reconhece "item_focalizado_selecionavel";
      _linhas_barra calcula item_focalizado_selecionavel (via
      selecao.chip_espaco_ativo) e repassa a _avaliar_regra_ativo.
  - caminho: config/telas/demo/h0041_selecao_multipla_oito_itens.json
    delta: chip_espaco regra_ativo "sempre" -> "item_focalizado_selecionavel".
  - caminho: tela/teste_renderizador.py
    delta: 7 testes H0041-MANUAL (estado lógico + apresentação + sincronização).
  - caminho: demo/teste_demo.py
    delta: 6 testes de integração percorrendo a sequência manual completa.
arquivos_removidos: []
```

## 4. Verificações locais

```yaml
verificacoes_executadas:
  - comando_ou_metodo: "pytest tela/teste_renderizador.py"
    resultado_compacto: 307 passed
  - comando_ou_metodo: "pytest demo/teste_demo_selecao.py demo/teste_demo.py"
    resultado_compacto: 42 passed
  - comando_ou_metodo: >
      pytest tela/teste_selecao.py tela/teste_renderizador.py
      demo/teste_demo_selecao.py demo/teste_demo.py
    resultado_compacto: 374 passed
  - comando_ou_metodo: "pytest (suíte completa)"
    resultado_compacto: 547 passed (baseline 534; +13 testes novos)
  - comando_ou_metodo: regressão focal (Enter resíduo, Executar inativo, Esc, seleção única, consoles sem seleção múltipla)
    resultado_compacto: 12 passed, 0 falhas
```

Regressões confirmadas preservadas: primeiro/segundo `Enter` sobre resíduo
(QA-H0041-001); `Enter` em `Executar` sem efeito; associação
participante→ID; seleção única; consoles sem seleção múltipla; `Esc`.

## 5. Bloqueios e evidências

```yaml
bloqueios: []
```

- Suporte visual inativo já existia (caixa baixa em `_texto_chip_barra`,
  consequência de `regra_ativo`); não houve necessidade de novo campo de
  estilo, schema ou `config/estilo.json`.
- `selecao.chip_espaco_ativo` já existia (Handoff 1); foi conectada ao
  renderer, sem duplicar lógica.
- Estado lógico preservado do P02 (QA-H0041-002): o P03 apenas conecta o
  estado já calculado à apresentação; não volta a inferir estado pelo texto.

Necessidade de novo QA e revalidação TTY: **sim**. A correção foi
verificada por reprodução do fluxo (não-TTY e PTY) e testes automatizados,
mas a confirmação final em TTY real é responsabilidade do usuário, fora
deste patch.

## 6. Estado Git

```yaml
branch: master
HEAD: 721f8f1
stage: vazio
diff_check: limpo
arquivos_alterados: somente autorizados
relatorio_P03: criado (este arquivo)
```
