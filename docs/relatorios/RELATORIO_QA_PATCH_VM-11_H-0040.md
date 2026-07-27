# Relatório de QA do Patch VM-11 H-0040

## 1. Identificação

```yaml
etapa: QA_PATCH_VM11_H0040
handoff: H-0040
adr: ADR-0031
origem: VALIDACAO_MANUAL
data: 2026-07-26
relatorio_criado: docs/relatorios/RELATORIO_QA_PATCH_VM-11_H-0040.md
```

## 2. Gate

```yaml
handoff:
  QA: H1_HANDOFF_APPROVED

relatorio_patch:
  existe: true
  ultima_linha: IMPLEMENTATION_PATCH_COMPLETED

relatorio_implementacao:
  ultima_linha: IMPLEMENTATION_COMPLETED_AWAITING_QA

validacao_manual:
  VM_01_a_VM_10: APROVADOS
  VM_11: FALHOU
```

## 3. Limite material do patch

Confirmado que o delta de modificações foi estritamente circunscrito aos arquivos autorizados. O worktree acumulado não bloqueia o QA.

```yaml
arquivos_modificados:
  - demo/demo.py
  - demo/teste_demo_navegacao.py
  - tela/navegacao.py
  - tela/teste_navegacao.py
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md

arquivos_criados:
  - config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  - docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md

arquivos_preservados:
  - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
  - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  - docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md
  - todos_os_relatorios_de_QA_anteriores
  - tela/renderizador.py
  - tela/distribuicao_matricial.py
  - tela/teste_renderizador.py
  - tela/teste_distribuicao_matricial.py
  - demo/demo_navegacao.py
```

## 4. Reprodução independente da falha original

Usando o cenário `config/telas/demo/h0040_nav_console_grade_2x3.json` sob a fronteira declarada de largura redimensionada para 32 (com `desconto_estrutural=3`), a primeira seta DOWN recalculou a geometria utilizando a formação `3×2` vigente, movendo `g11` diretamente para `g00` (e não para `g01`, que seria o vizinho na formação anterior `2×3` com desconto 0).

```yaml
reproducao_VM11:
  formacao_renderer: 3x2
  formacao_navegacao: 3x2
  item_antes: g11
  primeiro_DOWN: g00
  resultado_esperado: g11 → g00
  resultado_observado: g11 → g00
  divergencia_residual: nenhuma
```

## 5. Preservação da geometria atual

O runtime preserva no estado as chaves de geometria durante `processar_comando`. A navegação é pura e recalcula a geometria dinamicamente de forma correta sem reutilizar nenhum estado cacheado anterior.

```yaml
preservacao_geometria:
  largura: preservada
  altura: preservada
  altura_interna: preservada
  desconto_estrutural: preservado
  modo_atual: preservado
  pagina_atual: preservada
  item_logico: preservado
  console_focado: preservado

descarte_memoria_anterior:
  formacao_anterior: descartada
  linha_anterior: descartada
  coluna_anterior: descartada
  vizinhos_anteriores: descartada

tempo_recalculo: imediato (primeira seta, sem comandos intermediarios)
```

## 6. Auditoria do JSON de 26 itens

O arquivo `config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json` foi auditado e está totalmente correto.

```yaml
auditoria_JSON_26_itens:
  quantidade_itens: 26
  ids: item_01_a_item_26
  todos_navegaveis: true
  estado_runtime_persistido: false
  ordem_semantica: linha (Lima a Cascata)
  configuracao_canonical:
    formacao:
      politica: preferencia_linhas
      linhas: {minimo: 1, maximo: 26}
    distribuicao_horizontal: {politica: uniforme}
    espacamento:
      margem_superior: {minimo: 1, maximo: 1}
      vao_horizontal: {minimo: 2}
      vao_vertical: {minimo: 1, maximo: 1}
    dimensionamento:
      colunas: {politica: maior_da_coluna}
      linhas: {politica: maior_da_linha}
```

## 7. Formações obrigatórias

Varredura empírica confirmou que o JSON de 26 itens assume as formações automáticas cabíveis de acordo com a largura da tela.

| Formação | Dimensão | Formação obtida | Tela normal | Sobreposição |
| -------- | -------- | --------------- | ----------: | -----------: |
| 1×26     | 282x80   | 1x26            | sim         | nao          |
| 2×13     | 151x80   | 2x13            | sim         | nao          |
| 4×7      | 85x80    | 4x7             | sim         | nao          |
| 7×4      | 52x80    | 7x4             | sim         | nao          |
| 13×2     | 28x80    | 13x2            | sim         | nao          |
| 26×1     | 20x80    | 26x1            | sim         | nao          |

## 8. Preservação e primeira seta

As transições de redimensionamento de janela preservam a identidade do item selecionado e recalculam os vizinhos imediatamente.

```yaml
transicoes_item_11_marmore:
  - transicao:
      formacao_origem: 1x26
      formacao_destino: 4x7
      item: item_11
      posicao_origem: [0, 10]
      posicao_destino: [1, 3]
      identidade_preservada: true
      primeira_seta: RIGHT
      vizinho_esperado: item_12
      vizinho_observado: item_12
  - transicao:
      formacao_origem: 4x7
      formacao_destino: 13x2
      item: item_11
      posicao_origem: [1, 3]
      posicao_destino: [5, 0]
      identidade_preservada: true
      primeira_seta: DOWN
      vizinho_esperado: item_13
      vizinho_observado: item_13
  - transicao:
      formacao_origem: 13x2
      formacao_destino: 26x1
      item: item_11
      posicao_origem: [5, 0]
      posicao_destino: [10, 0]
      identidade_preservada: true
      primeira_seta: DOWN
      vizinho_esperado: item_12
      vizinho_observado: item_12
  - transicao:
      formacao_origem: 26x1
      formacao_destino: 2x13
      item: item_11
      posicao_origem: [10, 0]
      posicao_destino: [0, 10]
      identidade_preservada: true
      primeira_seta: RIGHT
      vizinho_esperado: item_12
      vizinho_observado: item_12

transicoes_item_17_cometa:
  - transicao:
      formacao_origem: 1x26
      formacao_destino: 4x7
      item: item_17
      posicao_origem: [0, 16]
      posicao_destino: [2, 2]
      identidade_preservada: true
      primeira_seta: RIGHT
      vizinho_esperado: item_18
      vizinho_observado: item_18
  - transicao:
      formacao_origem: 4x7
      formacao_destino: 13x2
      item: item_17
      posicao_origem: [2, 2]
      posicao_destino: [8, 0]
      identidade_preservada: true
      primeira_seta: DOWN
      vizinho_esperado: item_19
      vizinho_observado: item_19
  - transicao:
      formacao_origem: 13x2
      formacao_destino: 26x1
      item: item_17
      posicao_origem: [8, 0]
      posicao_destino: [16, 0]
      identidade_preservada: true
      primeira_seta: DOWN
      vizinho_esperado: item_18
      vizinho_observado: item_18
  - transicao:
      formacao_origem: 26x1
      formacao_destino: 2x13
      item: item_17
      posicao_origem: [16, 0]
      posicao_destino: [1, 3]
      identidade_preservada: true
      primeira_seta: RIGHT
      vizinho_esperado: item_18
      vizinho_observado: item_18
```

## 9. Toroide

```yaml
toroide:
  formacao_1x26:
    cima_baixo: mantem_mesmo_item (no_movement)
    esquerda_direita: circula_pelos_26_itens
  formacao_26x1:
    esquerda_direita: mantem_mesmo_item (no_movement)
    cima_baixo: circula_pelos_26_itens
  matrizes_incompletas:
    celulas_vazias_ignoradas: sim
    salto_diagonal: nao (impedida)
    horizontal_permanece_na_linha: sim
    vertical_permanece_na_coluna: sim
    retorno_circular: considera_apenas_celulas_ocupadas
```

## 10. Distribuição horizontal

```yaml
distribuicao_horizontal:
  formacao: 13x2
  largura_A: 28
  intervalo_A_observado: 2
  largura_B: 39
  intervalo_B_observado: 6
  recuperacao_espaco: sim (recalculo toroidal dinâmico dos vaos)
  acumulo_esquerda_apenas: nao
  sobreposicao: nao
  conteudo_cortado: nao
  politica_uniforme: atendida
```

## 11. Separação vertical

```yaml
separacao_vertical:
  margem_superior: 1
  linhas_vazias_entre_linhas_da_matriz: 1
  origem_exclusiva: vao_vertical (da distribuicao_matricial)
  itens_falsos_ou_celulas_vazias: nao
  sobreposicao_de_linhas: nao
```

## 12. Correspondência entre renderer e navegação

```yaml
renderer_e_navegacao:
  linhas_iguais: sim
  colunas_iguais: sim
  posicoes_iguais: sim
  celulas_vazias_iguais: sim
  item_indicado_igual: sim
  desconto_estrutural_igual: sim
```

## 13. AT e PN

```yaml
AT:
  esperados: 40
  encontrados: 40
  unicos: 40
  aprovados: 40
  insuficientes: 0
  contraditorios: 0
  ausentes: 0

PN:
  esperadas: 17
  encontradas: 17
  unicas: 17
  aprovadas: 17
  insuficientes: 0
  contraditorias: 0
  ausentes: 0
```

Auditoria material dos testes focais do patch:

| ID | JSON real | Múltiplas formações | Primeira seta | Vizinhos | Toroide | Espaçamento | Resultado |
| -- | --------: | ------------------: | ------------: | -------: | ------: | ----------: | --------- |
| AT-0031 | sim | sim | sim | sim | sim | sim | APROVADO |
| AT-0032 | sim | sim | sim | sim | sim | sim | APROVADO |
| PN-0012 | sim | sim | sim | sim | sim | sim | APROVADO |
| PN-0016 | sim | sim | sim | sim | sim | sim | APROVADO |

## 14. Testes focais

```yaml
testes_focais:
  coletados: 57
  aprovados: 57
  ignorados: 0
  falhas: 0
  erros: 0
```

## 15. Regressão direta

```yaml
regressao_direta:
  coletados: 352
  aprovados: 352
  ignorados: 0
  falhas: 0
  erros: 0
```

## 16. Suíte canônica

```yaml
suite_canonica:
  coletados: 480
  aprovados: 480
  ignorados: 0
  falhas: 0
  erros: 0
  duracao: 16.64s
```

## 17. Smoke checks

```yaml
smoke_checks:
  matriz_26:
    exit: 0
    STDERR: vazio
    traceback: ausente
    primeira_renderizacao: perfeita
    encerramento: limpo (s)
  grade_2x3:
    exit: 0
    STDERR: vazio
    traceback: ausente
    primeira_renderizacao: perfeita
    encerramento: limpo (s)
  linear_verboso:
    exit: 0
    STDERR: vazio
    traceback: ausente
    primeira_renderizacao: perfeita
    encerramento: limpo (s)
```

## 18. Compatibilidade

```yaml
compatibilidade:
  VM_01_a_VM_10: preservados
  Tab_e_Shift_Tab: inalterados
  modo_verboso_forcado: inalterado
  Enter_preservado: inalterado
  espaco_preservado: inalterado
  paginacao_preservada: inalterada
  JSONs_anteriores: aceitos
  distribuicoes_anteriores: validas
  sem_estado_runtime_no_JSON: sim
```

## 19. Achados

Nenhum achado bloqueante, maior ou menor foi detectado.

```yaml
achados: []
```

## 20. Validação manual

```yaml
validacao_manual:
  executada_pelo_QA: nao
  liberada_se_I1:
    - VM-11
  VM_01_a_VM_10:
    preservar_resultados: true
```

## 21. Efeito do QA

```yaml
efeito_do_QA:
  arquivos_preexistentes_alterados: []
  arquivos_criados:
    - docs/relatorios/RELATORIO_QA_PATCH_VM-11_H-0040.md
  implementacao_executada: nao
  validacao_manual_executada: nao
  operacoes_git_de_escrita: []
  commit_executado: nao
```

I1_IMPLEMENTATION_APPROVED