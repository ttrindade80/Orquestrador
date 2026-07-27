---
description: QA pos-patch independente da implementacao do H-0040 / ADR-0031
---

# Relatorio de QA Pos-Patch da Implementacao H-0040

## 1. Identificacao

```yaml
etapa: QA_POS_PATCH_IMPLEMENTACAO
handoff: H-0040
adr: ADR-0031
data: 2026-07-26
relatorio_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md
```

## 2. Objeto e escopo

Auditoria independente do patch da implementacao de H-0040, sem alterar codigo,
testes, demos, JSONs ou relatorios preexistentes. O QA executou somente
inspecao, testes automatizados e smoke checks nao interativos; validacao manual
permanece exclusiva do usuario.

## 3. Estado processual

```yaml
handoff:
  numero: H-0040
  adr: ADR-0031
  qa_handoff: H1_HANDOFF_APPROVED
implementacao_inicial:
  encerramento: IMPLEMENTATION_COMPLETED_AWAITING_QA
qa_inicial_da_implementacao:
  relatorio: docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
  classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
  achados: [QAI40-001, QAI40-002, QAI40-003, QAI40-004]
patch:
  relatorio: docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
  encerramento: IMPLEMENTATION_PATCH_COMPLETED
implementacao_atualizada:
  relatorio: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  encerramento: IMPLEMENTATION_COMPLETED_AWAITING_QA
validacao_manual:
  executada: false
  liberada: false
```

## 4. Estado Git inicial

```yaml
estado_git_inicial:
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
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - .zcode/plans/plan-sess_ee8ccabe-374c-4847-962f-8bbe4df3c60f.md
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - config/telas/demo/h0040_nav_console_nao_focalizavel.json
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_degenere_um_item.json
    - config/telas/demo/h0040_nav_degenere_uma_coluna.json
    - config/telas/demo/h0040_nav_degenere_uma_linha.json
    - config/telas/demo/h0040_nav_dois_consoles.json
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
    - tela/navegacao.py
    - tela/teste_navegacao.py
```

O worktree acumulado nao foi usado como bloqueio.

## 5. Gate

```yaml
gate:
  handoff_H0040_existe: sim
  qa_inicial_existe: sim
  qa_inicial_ultima_linha: I2_IMPLEMENTATION_PATCH_REQUIRED
  relatorio_patch_existe: sim
  relatorio_patch_ultima_linha: IMPLEMENTATION_PATCH_COMPLETED
  relatorio_implementacao_atualizado_existe: sim
  relatorio_implementacao_ultima_linha: IMPLEMENTATION_COMPLETED_AWAITING_QA
  relatorio_QA_pos_patch_preexistente: nao
  conflito_git_bloqueante: nao
```

## 6. Autoridades

Lidos e usados como autoridade: H-0040, QA inicial da implementacao, relatorio
do patch, relatorio atualizado de implementacao, QA pos-segundo-patch do
handoff e ADR-0031. Foram inspecionados `demo/demo.py`, `tela/renderizador.py`,
`tela/navegacao.py`, `demo/demo_navegacao.py`, `demo/teste_demo_navegacao.py`,
`tela/teste_navegacao.py` e os oito JSONs nominais H-0040.

## 7. Limite material do patch

```yaml
delta_do_patch:
  arquivos_modificados_esperados: 7
  arquivos_modificados_confirmados:
    - demo/demo.py
    - tela/renderizador.py
    - tela/navegacao.py
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - tela/teste_navegacao.py
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  arquivos_criados_esperados: 1
  arquivos_criados_confirmados:
    - docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
  arquivos_fora_da_lista: []
  JSONs_alterados: []
  relatorios_de_QA_alterados: []
```

O inventario Git acumulado contem documentacao ADR-0031 e `__pycache__`
preexistentes; esses itens nao foram atribuidos ao patch.

## 8. Matriz dos achados iniciais

| Achado | Resultado pos-patch | Evidencia material |
| -- | -- | -- |
| QAI40-001 | CORRIGIDO | `tela/renderizador.py::_renderizar_participante_com_indicador`; cursores 0-4 na grade 2x3 com um unico simbolo na celula correta. |
| QAI40-002 | CORRIGIDO | `DESCONTO_ESTRUTURAL_CONSOLE=3` com repasse explicito; renderer importa `LARGURA_INDICADOR_COLUNA`; larguras 60/80 e mudanca 18->25 correspondem. |
| QAI40-003 | CORRIGIDO | `modo_verboso_forcado` propaga ao runtime; CLI normal e `--verboso` tem saidas semanticamente diferentes. |
| QAI40-004 | CORRIGIDO | Relatorio atualizado preserva QA I2 historico, patch, contagens pos-correcao e ausencia de validacao manual. |

## 9. Auditoria de QAI40-001

O indicador agora e escrito dentro da celula fisica, antes do texto, por
`_renderizar_participante_com_indicador`. Cada celula navegavel recebe coluna
indicadora propria; somente o item corrente do console focado recebe
`selecionado_simbolo` na primeira linha fisica. Demais itens e continuacoes
recebem `selecionado_off`; console nao focado e console sem foco nao exibem o
simbolo. Linhas vazias nao foram marcadas.

## 10. Reproducao matricial

Fonte: `config/telas/demo/h0040_nav_console_grade_2x3.json`, largura total 60.

| Cursor | Item | Linha da grade | Coluna da grade | Simbolos encontrados | Celula correta | Resultado |
| --: | -- | --: | --: | --: | --: | -- |
| 0 | g00 | 0 | 0 | 1 | true | APROVADO |
| 1 | g01 | 0 | 1 | 1 | true | APROVADO |
| 2 | g02 | 0 | 2 | 1 | true | APROVADO |
| 3 | g10 | 1 | 0 | 1 | true | APROVADO |
| 4 | g11 | 1 | 1 | 1 | true | APROVADO |

```yaml
para_cada_cursor:
  simbolos_encontrados: 1
  simbolo_na_celula_correta: true
  simbolo_em_linha_vazia: false
```

## 11. Continuacao fisica

Item longo em modo verboso produziu tres linhas fisicas reais:

```yaml
primeira_linha_do_item_corrente:
  indicador: selecionado_simbolo
linhas_de_continuacao:
  indicador: selecionado_off
  simbolo_em_continuacao: false
linhas_item_longo_verboso:
  - "Gamma Delta Epsilon Zeta"
  - "Eta Theta Iota Kappa"
  - "Lambda Mu"
```

## 12. Auditoria de QAI40-002

O desconto estrutural nominal esta em `tela/renderizador.py` como
`DESCONTO_ESTRUTURAL_CONSOLE = 3`. A navegacao nao usa literal implicito para
esse desconto; recebe `desconto_estrutural` explicitamente quando o runtime
precisa da mesma geometria do renderer. A largura da coluna indicadora tem
autoridade unica em `tela/navegacao.py` (`LARGURA_INDICADOR_COLUNA = 2`) e o
renderer importa esse valor. `grade_de_itens()` nao desconta duas vezes: aplica
o desconto estrutural na area e inclui a coluna indicadora nos `min_ws`.

## 13. Autoridade da largura

Ocorrencias classificadas:

| Simbolo/termo | Arquivo | Contexto |
| -- | -- | -- |
| `DESCONTO_ESTRUTURAL_CONSOLE` | `tela/renderizador.py` | autoridade nominal do desconto estrutural e repasse para grade. |
| `DESCONTO_ESTRUTURAL_CONSOLE` | `demo/demo.py` | consumo explicito pelo runtime ao popular estado de navegacao. |
| `LARGURA_INDICADOR_COLUNA` | `tela/navegacao.py` | autoridade unica da coluna indicadora. |
| `LARGURA_INDICADOR_COLUNA` | `tela/renderizador.py` | importacao da autoridade, sem duplicar literal. |
| `desconto_estrutural` | `tela/navegacao.py` | parametro explicito com default 0 para compatibilidade. |

## 14. Correspondencia em larguras fixas

| Largura total | Util da navegacao | Util do renderer | Linhas | Colunas | Correspondencia |
| --: | --: | --: | --: | --: | -- |
| 60 | 57 | 57 | 2 | 3 | true |
| 80 | 77 | 77 | 2 | 3 | true |

## 15. Mudanca material de grade

A grade fixa 2x3 nominal nao muda de formacao por definicao. A busca
programatica usou cenario autorizado equivalente ao AT-0032, com
`preferencia_linhas`.

```yaml
mudanca_material_de_grade:
  largura_A: 18
  grade_A: "3 linhas x 2 colunas"
  posicao_item_f_A: [2, 0]
  largura_B: 25
  grade_B: "2 linhas x 3 colunas"
  posicao_item_f_B: [1, 1]
  mesmo_item_logico_preservado: true
  posicao_recalculada: true
  vizinhos_recalculados: true
  renderer_corresponde_a_navegacao: true
```

## 16. Auditoria de QAI40-003

`demo/demo_navegacao.py` injeta `modo_verboso_forcado=True` quando `--verboso`
e usado. `demo/demo.py::_verboso_efetivo` da precedencia a esse override antes
da politica do modelo, de modo que `politica_modo=None` nao sobrescreve a
escolha. Nenhum campo novo foi persistido nos JSONs e a tecla `V` continua
condicionada a telas com politica `alternavel`.

## 17. Reproducao normal versus verboso

| Modo | Exit | STDERR bytes | STDOUT bytes | Linhas | Observacao |
| -- | --: | --: | --: | --: | -- |
| normal | 0 | 0 | 2908 | 24 | item `Gamma...Mu` em uma linha fisica. |
| verboso | 0 | 0 | 2908 | 24 | item quebrado em duas linhas: `Gamma...Theta` e `Iota...Mu`. |

```yaml
comparacao:
  saidas_materialmente_diferentes: true
  item_longo_quebrado_em_multiplas_linhas: true
  diferenca_explica_modo_verboso: true
```

## 18. Auditoria de QAI40-004

O relatorio atualizado preserva o resultado bruto inicial e a rejeicao
independente: `I2_IMPLEMENTATION_PATCH_REQUIRED` com `QAI40-001` a `QAI40-004`.
As contagens historicas aparecem como `testes_focais.aprovados_brutos: 57` e
`suite_canonica.aprovados_brutos: 480`; as contagens pos-patch aparecem como
57 focais, 352 regressao direta e 480 suite canonica. O texto separa historico
inicial, rejeicao independente, correcoes do patch, resultados pos-correcao,
QA pos-patch ainda pendente e validacao manual nao executada. Nao ha declaracao
de `I1_IMPLEMENTATION_APPROVED`, implementacao aprovada ou validacao manual
aprovada. A ultima linha e `IMPLEMENTATION_COMPLETED_AWAITING_QA`.

## 19. Prova negativa anterior a correcao

```yaml
prova_negativa_do_patch:
  executada: sim
  total_de_falhas: 10
  testes_nominais:
    - AT-0021
    - AT-0032
    - AT-0033
    - AT-0034
    - AT-0035
    - AT-0036
    - AT-0037
    - PN-0010
    - PN-0011
    - PN-0016
  falhas_coerentes_com_os_defeitos: true
  evidencia_suficiente: true
```

## 20. Matriz dos AT reformulados

| AT | Preparacao material | Observacao real | Usa renderer real | Passou | Resultado |
| -- | -- | -- | --: | --: | -- |
| AT-0021 | grade e modelo renderizado | compara grade navegacao e linhas reais | sim | sim | APROVADO |
| AT-0032 | duas larguras com grades diferentes | posicao e vizinhos mudam para mesmo item | sim | sim | APROVADO |
| AT-0033 | item longo e modo alternado | saida muda e cursor logico permanece | sim | sim | APROVADO |
| AT-0034 | modo normal/verboso | apresentacao fisica recalculada | sim | sim | APROVADO |
| AT-0035 | cursores 0-4 na matriz 2x3 | simbolo unico na celula correta | sim | sim | APROVADO |
| AT-0036 | matriz 1x3 e estilo customizado | simbolo do estilo e texto estavel | sim | sim | APROVADO |
| AT-0037 | item longo multilinha real | simbolo so na primeira linha | sim | sim | APROVADO |

## 21. Matriz das PN reformuladas

| PN | Preparacao | Estimulo | Condicao de falha | Passou | Resultado |
| -- | -- | -- | -- | --: | -- |
| PN-0010 | item longo, largura pequena, verboso | renderizar console focado | simbolo em continuacao | sim | APROVADO |
| PN-0011 | cursor no item 2 e override verboso | render normal/verboso e ponto CLI | modo ignorado, cursor 0 ou identidade trocada | sim | APROVADO |
| PN-0016 | grade 2x3 e renderer integrado | comparar grade, linhas e indicador | coordenada/linha/celula divergente | sim | APROVADO |

## 22. Reconciliacao completa de AT e PN

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
testes_novos:
  esperados: 57
  coletados: 57
```

## 23. Testes focais

```yaml
testes_focais:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
  coletados: 57
  aprovados: 57
  ignorados: 0
  falhas: 0
  erros: 0
```

## 24. Regressao direta

```yaml
regressao_direta:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py demo/teste_demo.py tela/teste_loader.py tela/teste_distribuicao_matricial.py -q
  coletados: 352
  aprovados: 352
  ignorados: 0
  falhas: 0
  erros: 0
```

## 25. Suite canonica

```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  coletados: 480
  aprovados: 480
  ignorados: 0
  falhas: 0
  erros: 0
  duracao: 17.03s
```

## 26. Smoke checks

| Cenario | Exit | STDERR bytes | Traceback | Primeira renderizacao | Encerramento |
| -- | --: | --: | --: | --: | -- |
| dois_consoles | 0 | 0 | false | sim | limpo |
| grade_2x3 | 0 | 0 | false | sim | limpo |
| console_unico_normal | 0 | 0 | false | sim | limpo |
| console_unico_verboso | 0 | 0 | false | sim | limpo |

## 27. Compatibilidade retroativa

Chamadas sem parametros de navegacao continuam aceitas pelo renderer e deixam
o contexto inativo. Estados sem `foco_console`, `cursores` ou override sao
aceitos por defaults em `processar_comando`. Console nao focalizavel teve
`lista_foco: []`, zero simbolos e largura sem reserva indevida de indicador.
As suites de distribuicao horizontal, vertical e matricial, loader e telas
H-0037 com `conteudo_externo` passaram na suite canonica. Enter, espaco e
paginacao permaneceram sem nova funcao fora do H-0040. Nenhum JSON recebeu
campo runtime novo.

## 28. Busca de escopo indevido

Ocorrencias de `dispatcher`, `registry`, `toggle`, `proxima_pagina` e
`pagina_anterior` aparecem em comentarios/docstrings ou negacoes explicitas,
sem infraestrutura nova de acao, selecao multipla ou paginacao. Ocorrencias de
`modo_verboso_forcado`, `DESCONTO_ESTRUTURAL_CONSOLE` e
`LARGURA_INDICADOR_COLUNA` sao coerentes com o patch e nao indicam estado
persistido indevidamente.

## 29. Novos achados

```yaml
novos_achados: []
achados_bloqueantes: 0
achados_maiores: 0
achados_menores: 0
notas:
  - id: QAPOSTI40-OPS-001
    categoria: EVIDENCIA
    evidencia_material: scripts auxiliares de inspecao executados sem PYTHONDONTWRITEBYTECODE criaram arquivos __pycache__ novos
    impacto: efeito operacional do QA, sem alteracao de implementacao, testes, JSONs ou relatorios preexistentes
    acao: registrado; arquivos __pycache__ nao removidos por instrucao explicita
```

## 30. Classificacao final

```yaml
classificacao: I1_IMPLEMENTATION_APPROVED
justificativa:
  QAI40_001_a_QAI40_004_corrigidos: true
  testes_reformulados_materialmente_suficientes: true
  AT_40_e_PN_17_aprovados: true
  focais_regressao_e_suite_passaram: true
  regressao_corrigivel_encontrada: false
  pronta_para_validacao_manual: true
```

## 31. Validacao manual pendente

```yaml
validacao_manual:
  executada_pelo_QA: nao
  motivo: EXCLUSIVA_DO_USUARIO
  roteiro_disponivel: sim
  liberada_se_I1: sim
```

## 32. Arquivos criados pelo QA

```yaml
efeito_do_QA:
  arquivos_preexistentes_alterados: []
  arquivos_criados:
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md
  outros_arquivos_criados:
    - demo/__pycache__/demo_navegacao.cpython-314.pyc
    - tela/__pycache__/distribuicao_matricial.cpython-314.pyc
    - tela/__pycache__/loader.cpython-314.pyc
    - tela/__pycache__/modelo.cpython-314.pyc
    - tela/__pycache__/navegacao.cpython-314.pyc
    - tela/__pycache__/renderizador.cpython-314.pyc
  operacoes_git_de_escrita: []
  commit_executado: nao
  validacao_manual_executada: nao
```

## 33. Estado Git final

Este relatorio e o unico arquivo documental criado pelo QA. Scripts auxiliares
de inspecao executados sem `PYTHONDONTWRITEBYTECODE=1` criaram arquivos
`__pycache__` adicionais; eles foram preservados porque a instrucao operacional
proibiu remover `__pycache__`. O restante do worktree acumulado foi preservado
sem alteracao intencional por esta auditoria.

## 34. Encerramento

I1_IMPLEMENTATION_APPROVED
