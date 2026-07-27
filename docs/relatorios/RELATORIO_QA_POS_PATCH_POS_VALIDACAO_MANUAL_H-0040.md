---
description: QA pos-patch independente do patch pos-validacao manual do H-0040
---

# Relatorio de QA Pos-Patch Pos-Validacao Manual H-0040

## 1. Identificacao

```yaml
etapa: QA_POS_PATCH_POS_VALIDACAO_MANUAL_H0040
handoff: H-0040
adr: ADR-0031
data: 2026-07-26
relatorio_patch: docs/relatorios/RELATORIO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
relatorio_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
```

## 2. Objeto

Auditoria independente do patch realizado apos a validacao manual inicial nao
aprovada do H-0040. Este QA nao altera codigo, testes, JSONs, handoff ou
relatorios anteriores, nao aplica correcoes e nao executa a validacao manual em
nome do usuario.

## 3. Estado processual

```yaml
handoff: H-0040
adr: ADR-0031
qa_tecnico_anterior:
  classificacao: I1_IMPLEMENTATION_APPROVED
  natureza: HISTORICO_ANTERIOR_A_VALIDACAO_MANUAL
validacao_manual_inicial:
  resultado_global: NAO_APROVADA
  VM_02: INCONCLUSIVO
  VM_07: FALHOU
  VM_10: APROVADO_COM_COBERTURA_FRACA
  VM_11: APROVADO_COM_COBERTURA_FRACA
levantamento:
  classificacao: NO_NEW_ADR_PATCH_EXISTING_CYCLE
patch_pos_validacao:
  encerramento: IMPLEMENTATION_PATCH_COMPLETED
nova_ADR:
  necessaria: false
validacao_manual_repetida:
  executada: false
  liberada: false
```

As declaracoes do patch foram tratadas como insumo historico, nao como
aprovacao.

## 4. Estado Git

Comandos de inventario executados:

```yaml
git_diff_cached_name_only: []
git_diff_name_only:
  - demo/demo.py
  - docs/adr/INDICE_ADR.md
  - docs/backlog.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
  - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  - tela/renderizador.py
arquivos_nao_rastreados_relevantes:
  - config/telas/demo/h0040_nav_console_grade_2x3.json
  - config/telas/demo/h0040_nav_console_unico_linear.json
  - config/telas/demo/h0040_nav_degenere_uma_coluna.json
  - config/telas/demo/h0040_nav_degenere_uma_linha.json
  - config/telas/demo/h0040_nav_dois_consoles.json
  - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
  - demo/demo_navegacao.py
  - demo/teste_demo_navegacao.py
  - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
  - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md
  - docs/relatorios/RELATORIO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md
  - tela/navegacao.py
  - tela/teste_navegacao.py
observacao: worktree acumulado nao foi tratado como bloqueio automatico.
```

## 5. Gate

```yaml
gate:
  levantamento_ultima_linha: NO_NEW_ADR_PATCH_EXISTING_CYCLE
  relatorio_patch_existe: true
  relatorio_patch_ultima_linha: IMPLEMENTATION_PATCH_COMPLETED
  relatorio_implementacao_ultima_linha: IMPLEMENTATION_COMPLETED_AWAITING_QA
  relatorio_QA_pos_patch_pos_validacao_preexistente: false
  prosseguir: true
```

## 6. Autoridades

Lidos integralmente:

- `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md`
- `docs/relatorios/RELATORIO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md`
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md`
- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`

Inspecionados:

- `demo/demo.py`
- `demo/demo_navegacao.py`
- `demo/teste_demo_navegacao.py`
- `tela/renderizador.py`
- `tela/teste_navegacao.py`
- `config/telas/demo/h0040_nav_console_unico_linear.json`
- `config/telas/demo/h0040_nav_tres_consoles_em_grupo.json`
- `config/telas/demo/h0040_nav_console_grade_2x3.json`
- `config/telas/demo/h0040_nav_degenere_uma_linha.json`
- `config/telas/demo/h0040_nav_degenere_uma_coluna.json`

## 7. Limite material do patch

```yaml
delta_do_patch:
  arquivos_modificados_esperados: 7
  arquivos_modificados_confirmados_por_relatorio_patch:
    - demo/demo.py
    - demo/teste_demo_navegacao.py
    - tela/renderizador.py
    - tela/teste_navegacao.py
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  arquivos_modificados_confirmados_por_git_diff_atual:
    - demo/demo.py
    - tela/renderizador.py
  arquivos_criados_esperados: 1
  arquivos_criados_confirmados_por_relatorio_patch:
    - docs/relatorios/RELATORIO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
  arquivos_fora_da_lista_no_inventario_atual:
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  relatorios_QA_alterados: []
```

O inventario atual nao permite isolar sozinho o delta do patch dentro do
worktree acumulado. Essa limitacao foi registrada como nota, sem bloquear por
si so este QA.

## 8. Matriz dos cinco pontos

| Ponto | Resultado pos-patch | Evidencia |
|---|---|---|
| VM-02 | NAO_CORRIGIDO | Roteiro usa tres consoles e sequencias corretas, mas o cenario cai em quadro minimo em 80x24 e tambem em 120x35 por DA-02; o roteiro nao informa dimensao segura. |
| VM-07 roteiro | CORRIGIDO | Handoff usa `h0040_nav_console_unico_linear.json --verboso`, nao pede `V` e verifica item multilinha/continuacoes. |
| VM-07 override | CORRIGIDO | `modo_verboso_forcado` permaneceu apos seta, Tab, Shift+Tab, espaco e Enter; nao foi persistido no JSON. |
| VM-07 sobreposicao | CORRIGIDO | Larguras 33, 34 e 35 com altura suficiente renderizaram sem sobreposicao; alturas insuficientes cairam no quadro minimo. |
| VM-10/VM-11 | NAO_CORRIGIDO | Roteiro usa grade fixa 2x3; dimensoes comuns preservam mesma grade, mesma linha/coluna, mesmos vizinhos e mesma coluna do indicador. |

## 9. VM-02

O roteiro revisado usa:

```text
config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
```

Inspecao tecnica da ordem:

```yaml
lista_foco_depth_first:
  - console_a1
  - console_a2
  - console_externo
Tab:
  sequencia:
    - console_a1
    - console_a2
    - console_externo
    - console_a1
Shift_Tab:
  sequencia:
    - console_a1
    - console_externo
    - console_a2
    - console_a1
circularidade: true
entrada_no_item_logico_0: true
linguagem_simples_no_roteiro: true
resposta_passou_falhou: true
```

A logica de navegacao foi corrigida, mas a executabilidade manual do cenario
permanece insuficiente porque dimensoes comuns podem exibir apenas quadro
minimo.

## 10. Usabilidade do cenario de tres consoles

Inspecao mecanica com dimensoes controladas:

| Dimensao | Renderizacao normal | Quadro minimo | Sobreposicao | Utilizavel manualmente |
|---|---:|---:|---:|---:|
| 80x24 | nao | sim | nao observavel | nao |
| 100x30 | sim | nao | nao | sim |
| 120x35 | nao | sim | nao observavel | nao |

Classificacao da causa:

```yaml
80x24: ALTURA_OU_LARGURA_INSUFICIENTE
100x30: RENDERIZACAO_NORMAL
120x35: DEFEITO_DE_RENDERIZACAO
detalhe_120x35: "RenderizadorErro DA-02 por area vertical extra em grupo com dois elementos visuais sem distribuicao"
dimensao_segura_encontrada: 100x30
roteiro_informa_dimensao_segura: false
```

`exit 0` com quadro minimo em non-TTY foi registrado como
`CARREGA_MAS_NAO_COMPROVA_CENARIO`.

## 11. VM-07 roteiro

```yaml
usa_json_correto: true
usa_verboso: true
nao_pede_tecla_V: true
nao_afirma_tela_alternavel: true
verifica_item_duas_ou_mais_linhas: true
verifica_indicador_primeira_linha: true
verifica_continuacoes_sem_indicador: true
pede_navegacao_por_tecla: true
confirma_modo_verboso_permanece: true
confirma_item_logico_correto: true
resultado: CORRIGIDO
```

## 12. Override verboso

```yaml
modo_verboso_forcado:
  estado_inicial: true
  preservado_apos_seta: true
  preservado_apos_Tab: true
  preservado_apos_Shift_Tab: true
  preservado_apos_espaco: true
  preservado_apos_Enter: true
  persistido_no_JSON: false
  tecla_V_adicionada: false
  chamadas_sem_override_preservam_comportamento_anterior: true
```

Auditoria dos testes associados:

| ID | Classificacao | Evidencia |
|---|---|---|
| AT-0033 | APROVADO | Executa comandos reais e verifica override/estado efetivo apos cada comando. |
| AT-0034 | APROVADO | Renderiza modo normal/verboso, confirma continuacao real e persistencia apos comandos. |
| PN-0011 | APROVADO | Usa CLI real com/sem `--verboso`, cursor fora do item 0 e diferenca semantica. |

## 13. Fixture multilinha

```yaml
fixture_multilinha:
  arquivo: config/telas/demo/h0040_nav_console_unico_linear.json
  console_nivel_unico: true
  quantidade_itens: 4
  item_longo: i3
  dimensao_comum_testada: 80x24
  linhas_fisicas_observadas: 3
  politica_alternavel_adicionada: false
  foco_console_no_JSON: false
  cursores_no_JSON: false
  campos_nao_autorizados: []
```

Em 80x24 com cursor no item `i3`, o item longo produziu tres linhas fisicas:
`Gamma texto-longo-demonstrativo`, `Delta Epsilon Zeta Eta Theta Iota` e
`Kappa`; `Omega` apareceu em linha propria sem sobreposicao.

## 14. Larguras estreitas

Com modo verboso, cursor no item longo e altura suficiente:

| Largura | Classificacao |
|---:|---|
| 33 | RENDERIZACAO_SEM_SOBREPOSICAO |
| 34 | RENDERIZACAO_SEM_SOBREPOSICAO |
| 35 | RENDERIZACAO_SEM_SOBREPOSICAO |

Com altura 24 ou 30, as larguras 33-35 cairam corretamente em
`TERMINAL_PEQUENO_TRATADO`. Nenhuma largura aceita produziu sobreposicao.

```yaml
largura_aceita:
  sobreposicao: false
  item_seguinte_apos_continuacoes: true
  indicador_na_primeira_linha: true
  indicador_nas_continuacoes: false
renderer_considera_altura_fisica_real_do_item: true
```

## 15. Testes de continuacao

| ID | Classificacao | Evidencia |
|---|---|---|
| AT-0037 | APROVADO | Prepara item longo, largura pequena, modo verboso e item seguinte; confirma simbolo unico e ausencia de sobreposicao. |
| PN-0010 | APROVADO | Prepara continuacao fisica real; falha se simbolo aparece em continuacao ou se item seguinte sobrepoe. |

## 16. VM-10 e VM-11

Ambos usam:

```text
config/telas/demo/h0040_nav_console_grade_2x3.json
PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json
```

O roteiro evita exigir indices internos, coordenadas ou objetos Python. Pede
item diferente do primeiro, reducao/redimensionamento, matriz incompleta,
celula vazia e ausencia de sobreposicao.

Defeito remanescente: o JSON manual e `matriz_fixa` 2x3 com alinhamento
`inicio`. Nas dimensoes testadas, a formacao, os vizinhos e a coluna textual do
indicador nao mudaram. Para cursor em `g11`, a coluna do simbolo permaneceu 9
em larguras 25, 30, 35, 40, 50, 60 e 80.

## 17. Cobertura material de redimensionamento

```yaml
redimensionamento_manual:
  dimensao_A: 80x24
  grade_A: 2 linhas x 3 colunas
  dimensao_B: 100x30
  grade_B: 2 linhas x 3 colunas
  item_logico_preservavel: true
  mudanca_visual_observavel: false
  roteiro_permite_verificacao: false
```

A suite automatizada cobre mudanca material em teste sintetico com
`preferencia_linhas`, mas VM-10/VM-11 devem ser aprovadas pela fixture e pelo
roteiro manual. A matriz manual fixa ainda sustenta cobertura fraca para
redimensionamento material.

## 18. Handoff atualizado

```yaml
validacao_manual_inicial:
  resultado: NAO_APROVADA
  VM_02: INCONCLUSIVO_POR_CENARIO
  VM_07: FALHOU_POR_ROTEIRO_E_OVERRIDE
  VM_10: APROVADO_COM_COBERTURA_FRACA
  VM_11: APROVADO_COM_COBERTURA_FRACA
levantamento_pos_validacao:
  classificacao: NO_NEW_ADR_PATCH_EXISTING_CYCLE
patch_pos_validacao:
  status: EXECUTADO_AGUARDANDO_QA
D1_D15_presentes: true
AT_PN_nao_renumerados: true
nova_validacao_declarada_aprovada: false
```

## 19. Relatorio de implementacao

O relatorio preserva o historico da validacao manual inicial nao aprovada,
registra o levantamento, registra o patch pos-validacao, declara QA ainda nao
executado e nova validacao manual ainda nao executada. A ultima linha permanece:

```text
IMPLEMENTATION_COMPLETED_AWAITING_QA
```

Nao foi encontrada aprovacao antecipada deste patch.

## 20. AT e PN

```yaml
AT:
  esperados: 40
  encontrados: 40
  unicos: 40
  aprovados: 40
  insuficientes: 0
  contraditorios: 0
  ausentes: []

PN:
  esperadas: 17
  encontradas: 17
  unicas: 17
  aprovadas: 17
  insuficientes: 0
  contraditorias: 0
  ausentes: []

total_testes_novos:
  esperado: 57
  coletado: 57
```

## 21. Testes focais

```yaml
testes_focais:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
  coletados: 57
  aprovados: 57
  ignorados: 0
  falhas: 0
  erros: 0
```

## 22. Regressao direta

```yaml
regressao_direta:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py demo/teste_demo.py tela/teste_loader.py tela/teste_distribuicao_matricial.py -q
  coletados: 352
  aprovados: 352
  ignorados: 0
  falhas: 0
  erros: 0
```

## 23. Suite canonica

```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  coletados: 480
  aprovados: 480
  ignorados: 0
  falhas: 0
  erros: 0
  duracao: 16.60s
```

## 24. Smoke checks

| Cenario | Exit | STDERR bytes | Traceback | Primeira renderizacao | Quadro minimo | Encerramento |
|---|---:|---:|---:|---:|---:|---|
| tres_consoles | 0 | 0 | false | sim | sim | limpo |
| grade_2x3 | 0 | 0 | false | sim | nao | limpo |
| linear_verboso | 0 | 0 | false | sim | nao | limpo |

```yaml
smoke_checks:
  tres_consoles: CARREGA_MAS_NAO_COMPROVA_CENARIO
  grade_2x3: CARREGA_RENDERIZA_SAI_LIMPO
  linear_verboso: CARREGA_RENDERIZA_SAI_LIMPO
```

## 25. Compatibilidade

```yaml
compatibilidade:
  estados_sem_override_continuam_aceitos: true
  H_0037_sem_alteracao_semantica_intencional: true
  conteudo_externo_preservado: true
  tecla_V_nao_ampliada: true
  Enter_sem_nova_funcao: true
  espaco_sem_toggle: true
  paginacao_inalterada: true
  loader_e_distribuicoes_regressao_passaram: true
  JSONs_sem_estado_runtime: true
```

## 26. Novos achados

```yaml
achados:
  - id: QAPOSTVM40-001
    origem:
      - VM_02
    severidade: MAIOR
    arquivo: docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    simbolo_ou_linha: VM-02
    autoridade: "criterio de usabilidade VM-02 e cenario de tres consoles em terminal real comum"
    evidencia_material: "80x24 exibiu quadro minimo por altura insuficiente; 120x35 exibiu quadro minimo por RenderizadorErro DA-02; somente 100x30 renderizou normal."
    comportamento_encontrado: "roteiro nao informa dimensao segura apesar de dimensoes comuns poderem nao renderizar o cenario."
    comportamento_esperado: "cenario executavel pelo usuario em terminal comum, ou roteiro com dimensao segura quando necessario."
    correcao_necessaria: "corrigir o cenario/renderizacao para dimensoes comuns ou registrar dimensao segura materialmente validada no roteiro."

  - id: QAPOSTVM40-002
    origem:
      - VM_10_VM_11
    severidade: MAIOR
    arquivo: docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    simbolo_ou_linha: VM-10/VM-11
    autoridade: "ADR-0031 D10 e criterio de cobertura material de redimensionamento"
    evidencia_material: "h0040_nav_console_grade_2x3.json e matriz_fixa 2x3; em larguras 25-80 o cursor g11 permaneceu na coluna textual 9 e a grade permaneceu 2x3."
    comportamento_encontrado: "roteiro manual nao produz mudanca observavel de linha, coluna, vizinhos, formacao ou posicao textual do indicador."
    comportamento_esperado: "duas dimensoes utilizaveis devem produzir mudanca fisica real verificavel pelo usuario."
    correcao_necessaria: "usar fixture/roteiro com redistribuicao material observavel ou explicitar dimensoes que alterem posicao fisica real."

notas:
  - id: QAPOSTVM40-NOTA-001
    categoria: INVENTARIO_GIT
    evidencia_material: "git diff --name-only contem documentacao preservada fora da lista declarada, mas o worktree acumulado foi explicitamente declarado nao bloqueante."
    impacto: "nao atribuido automaticamente ao patch; registrado para rastreabilidade."
```

## 27. Classificacao final

```yaml
classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
justificativa:
  testes_automatizados_passaram: true
  VM_07_corrigida: true
  VM_02_ainda_tem_defeito_corrigivel_de_roteiro_ou_cenario: true
  VM_10_VM_11_ainda_tem_cobertura_manual_fraca: true
  achados_bloqueantes: 0
  achados_maiores: 2
  achados_menores: 0
```

## 28. Validacao manual pendente

```yaml
validacao_manual:
  executada_pelo_QA: nao
  repeticao_liberada_se_I1:
    - VM-02
    - VM-07
    - VM-10
    - VM-11
  testes_anteriores_preservados:
    - VM-01
    - VM-03
    - VM-04
    - VM-05
    - VM-06
    - VM-08
    - VM-09
validacao_manual_liberada: false
```

## 29. Arquivos criados pelo QA

```yaml
efeito_do_QA:
  arquivos_preexistentes_alterados: []
  arquivos_criados:
    - docs/relatorios/RELATORIO_QA_POS_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
  operacoes_git_de_escrita: []
  commit_executado: nao
  validacao_manual_executada: nao
```

## 30. Estado Git final

```yaml
estado_git_final:
  git_diff_check: ok
  git_diff_cached_check: ok
  git_diff_no_index_check_relatorio_novo: "sem diagnosticos; exit 1 por diferenca esperada contra /dev/null"
  arquivos_staged: []
  arquivos_unstaged:
    - demo/demo.py
    - docs/adr/INDICE_ADR.md
    - docs/backlog.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_tela_json.md
    - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
    - tela/renderizador.py
  novo_relatorio_QA:
    - docs/relatorios/RELATORIO_QA_POS_PATCH_POS_VALIDACAO_MANUAL_H-0040.md
  arquivos_preexistentes_alterados_pelo_QA: []
  operacoes_git_de_escrita_executadas: []
```

## 31. Encerramento

I2_IMPLEMENTATION_PATCH_REQUIRED
