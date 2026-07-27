---
description: Segundo patch pos-validacao manual H-0040 para QAPOSTVM40-001 e QAPOSTVM40-002
---

# Relatorio de Segundo Patch Pos-Validacao Manual H-0040

## 1. Identificacao

```yaml
etapa: SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H0040
handoff: H-0040
adr: ADR-0031
data: 2026-07-26
relatorio: docs/relatorios/RELATORIO_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
```

## 2. Estado de entrada

```yaml
classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
achados:
  QAPOSTVM40-001: ABERTO
  QAPOSTVM40-002: ABERTO
preservados_como_corrigidos:
  - VM-07 roteiro
  - VM-07 override verboso
  - VM-07 item multilinha
  - VM-07 sobreposição
```

## 3. Matriz dos achados

| Achado | Causa | Correção | Evidência | Estado |
| --- | --- | --- | --- | --- |
| QAPOSTVM40-001 | `grupo_externo` vertical com dois descendentes visuais sem `distribuicao`; em altura ampliada (ex.: 120×35) o renderer levantava DA-02 por área vertical excedente | Declarar `distribuicao: {modo: igual}` em `grupo_externo`; roteiro VM-02 orienta ampliar janela se aparecer quadro mínimo | 100×30 e 120×35 renderizam normal sem DA-02; 80×24 cai em quadro mínimo tratado; AT-0008/AT-0011/AT-0012 | CORRIGIDO |
| QAPOSTVM40-002 | Fixture usava `matriz_fixa` 2×3; formação, vizinhos e coluna do indicador não mudavam ao redimensionar | Trocar para `preferencia_linhas` (min 2, max 3) com textos que forçam redistribuição observável (2×3 → 3×2); atualizar VM-10/VM-11 sem dimensões fixas | dimensao_A 80×24 = 2×3; dimensao_B 28×30 = 3×2; item `g11` preservado; AT-0031/AT-0032/PN-0012/PN-0016 | CORRIGIDO |

## 4. Diagnostico QAPOSTVM40-001

```yaml
arquivo: config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
causa_DA_02: >
  grupo_externo (arranjo vertical) contem grupo_interno_a e console_externo
  sem distribuicao; quando a altura disponivel excede a ocupacao minima,
  DA-02 rejeita multiplos descendentes sem politica de particao.
ajuste_da_fixture: "distribuicao: {modo: igual} em grupo_externo"
preservado:
  consoles_focalizaveis: 3
  grupos_aninhados: true
  descendentes_assimetricos: true
  ordem_depth_first: [console_a1, console_a2, console_externo]
```

## 5. Diagnostico QAPOSTVM40-002

```yaml
arquivo: config/telas/demo/h0040_nav_console_grade_2x3.json
politica_existente_usada: preferencia_linhas
formacao:
  minimo: 2
  maximo: 3
itens_navegaveis: 5
textos: [Alpha, Bravo, Charlie, Delta, Echo]
dimensao_A: 80x24
grade_A: 2x3
dimensao_B: 28x30
grade_B: 3x2
item_preservado: g11
posicao_alterada: "(1,1) -> (2,0)"
vizinhos_recalculados: true
estado_runtime_persistido: false
campos_schema_novos: false
```

## 6. Arquivos

```yaml
arquivos_modificados:
  - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
  - config/telas/demo/h0040_nav_console_grade_2x3.json
  - demo/teste_demo_navegacao.py
  - tela/teste_navegacao.py
  - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
arquivos_criados:
  - docs/relatorios/RELATORIO_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
arquivos_preservados:
  - codigo de producao (tela/navegacao.py, tela/renderizador.py)
  - demo/demo.py
  - demo/demo_navegacao.py
  - JSON linear verboso e demais JSONs
  - ADR, contratos, nomenclatura, backlog e indices
  - todos os relatorios de QA e patch anteriores
arquivos_fora_da_lista_alterados: []
relatorios_QA_alterados: []
```

## 7. Reproducoes

```yaml
tres_consoles:
  80x24: quadro_minimo_tratado
  100x30: renderizacao_normal
  120x35: renderizacao_normal
  DA_02_em_dimensao_ampliada: false

redistribuicao:
  dimensao_A: 80x24
  grade_A: 2x3
  dimensao_B: 28x30
  grade_B: 3x2
  item_preservado: g11
  posicao_alterada: true
```

## 8. Testes

```yaml
contagem:
  AT: 40
  PN: 17
  total: 57

testes_focais:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
  coletados: 57
  aprovados: 57
  falhas: 0
  erros: 0

regressao_direta:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py demo/teste_demo.py tela/teste_loader.py tela/teste_distribuicao_matricial.py -q
  coletados: 352
  aprovados: 352
  falhas: 0
  erros: 0

suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  coletados: 480
  aprovados: 480
  falhas: 0
  erros: 0
```

## 9. Smoke checks

| Cenario | Exit | STDERR bytes | Traceback | Observacao |
| --- | ---: | ---: | --- | --- |
| tres_consoles | 0 | 0 | false | non-TTY ~80x24: quadro minimo (nao prova funcional) |
| grade_2x3 | 0 | 0 | false | CARREGA_RENDERIZA_SAI_LIMPO |
| linear_verboso | 0 | 0 | false | CARREGA_RENDERIZA_SAI_LIMPO |

## 10. Historico documental

```yaml
qa_pos_primeiro_patch_pos_validacao:
  classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
  achados:
    - QAPOSTVM40-001
    - QAPOSTVM40-002

segundo_patch_pos_validacao:
  status: EXECUTADO_AGUARDANDO_QA
  nova_ADR: false
  validacao_manual_executada: false
```

Ultima linha de `RELATORIO_IMPLEMENTACAO_H-0040.md` preservada:

```text
IMPLEMENTATION_COMPLETED_AWAITING_QA
```

## 11. Controles

```yaml
operacoes_git_de_escrita_executadas: []
commit_executado: nao
QA_executado: nao
validacao_manual_executada: nao
nova_ADR: false
bloqueios: []
```

## 12. Encerramento

IMPLEMENTATION_PATCH_COMPLETED
