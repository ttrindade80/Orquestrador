---
name: relatorio-qa-h-0040-implementacao
description: QA independente da implementacao do H-0040 / ADR-0031
metadata:
  type: relatorio
  etapa: QA_IMPLEMENTACAO
  handoff: H-0040
  adr: ADR-0031
---

# Relatório de QA da Implementação H-0040

## 1. Identificação

```yaml
resultado:
  etapa: QA_IMPLEMENTACAO
  handoff: H-0040
  adr: ADR-0031
  arquivo_auditado: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
```

## 2. Objeto e escopo

Auditoria independente da implementação de navegação simples e seleção única em console de nível único. O QA leu as autoridades obrigatórias, inspecionou integralmente os sete arquivos de código/teste/relatório e os oito JSONs declarados, executou os testes e smoke checks prescritos. Não alterou código, testes, JSONs, demos, autoridades nem relatórios anteriores; não realizou validação visual em nome do usuário.

## 3. Estado processual

```yaml
handoff: H-0040
adr: ADR-0031
qa_final_handoff: H1_HANDOFF_APPROVED
implementacao_declarada: IMPLEMENTATION_COMPLETED_AWAITING_QA
qa_anterior_da_implementacao: nao
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
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
    - artefatos_documentais_acumulados_ADR-0031
    - 13_arquivos_declarados_da_implementacao_H-0040
```

Os documentos acumulados da ADR-0031 e os três `__pycache__` já estavam presentes antes do QA e não foram atribuídos à implementação H-0040.

## 5. Gate

```yaml
gate:
  H0040_existe: sim
  qa_final_handoff_existe: sim
  qa_final_handoff_termina_H1_HANDOFF_APPROVED: sim
  relatorio_implementacao_existe: sim
  relatorio_implementacao_ultima_linha_correta: sim
  treze_novos_existem: sim
  dois_modificados_existem: sim
  relatorio_QA_preexistente: nao
  conflito_git_impedindo_leitura: nao
  resultado: APROVADO
```

## 6. Autoridades

Lidas integralmente: H-0040, `RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md`, `RELATORIO_IMPLEMENTACAO_H-0040.md` e ADR-0031. Os relatórios históricos de patch/QA anteriores foram usados somente para rastreabilidade da autoridade aprovada.

## 7. Método

Inventário Git sem escrita; inspeção de delta e conteúdo integral; validação sintática/carregamento dos JSONs; reprodução do comportamento de renderer e demo; busca de escopo indevido; execução dos comandos de teste prescritos. A reprodução do indicador usou `h0040_nav_console_grade_2x3.json`, largura 60 e cursores 0 a 4, sem avaliação visual subjetiva.

## 8. Limite nominal de arquivos

```yaml
arquivos_da_implementacao:
  modificados:
    esperados: 2
    encontrados:
      - demo/demo.py
      - tela/renderizador.py
  novos:
    esperados: 13
    encontrados: 13
  fora_da_lista: []
```

Os demais arquivos não rastreados/documentais são anteriores ou externos ao delta atribuível pelo relatório de implementação; não compõem `fora_da_lista` do H-0040.

## 9. Auditoria do delta

`git diff -- demo/demo.py tela/renderizador.py` confirma as integrações de runtime/renderer. Os 13 arquivos novos passaram `git diff --no-index --check /dev/null <arquivo>`. Não houve erro de whitespace. O delta contém, entretanto, os defeitos materiais descritos nos achados QAI40-001 a QAI40-003.

## 10. Arquitetura

`tela/navegacao.py` é independente de TTY e não renderiza diretamente; `demo/demo.py` concentra captura/estado; `demo/demo_navegacao.py` delega ao runtime real; não há renderer alternativo, dispatcher novo, seleção múltipla nem paginação interativa. A separação é adequada, com duas exceções de materialidade: a geometria efetivamente entregue ao módulo não é a mesma do renderer (QAI40-002) e a camada de renderer não localiza o item em grade matricial (QAI40-001).

## 11. Matriz D1–D15

| Decisão | Evidência em código | Teste AT | Prova PN | Resultado |
| --- | --- | --- | --- | --- |
| D1 | filtros de tipo em `lista_foco` | AT-0004/0005 | PN-0001/0002/0003 | IMPLEMENTADA |
| D2 | `console_e_focalizavel` | AT-0001/0002/0003 | PN-0004 | IMPLEMENTADA |
| D3 | travessia depth-first | AT-0006/0007/0008 | PN-0001 | IMPLEMENTADA |
| D4 | ordem declarada dos filhos | AT-0009/0010 | — | IMPLEMENTADA |
| D5 | Tab e ambas Shift+Tab | AT-0011 a 0014 | PN-0005 | IMPLEMENTADA |
| D6 | entrada zera cursor | AT-0015/0016 | PN-0005 | IMPLEMENTADA |
| D7 | `grade_de_itens`/motor matricial | AT-0017 a 0021 | PN-0016 | IMPLEMENTADA_COM_NOTA |
| D8 | toroide por eixo | AT-0022 a 0027 | PN-0006/0007 | IMPLEMENTADA |
| D9 | eixos unitários sem movimento | AT-0028 a 0030 | PN-0006 | IMPLEMENTADA |
| D10 | cursor lógico preservado | AT-0031 a 0034 | PN-0011/0012 | IMPLEMENTADA_COM_NOTA |
| D11 | contexto de foco no renderer | AT-0035 | PN-0008 | CONTRADITORIA |
| D12 | indicador/coluna de estilo | AT-0036/0037 | PN-0010/0015 | CONTRADITORIA |
| D13 | item sob cursor; espaço inerte | AT-0038 | PN-0017 | IMPLEMENTADA |
| D14 | regras de existência dos chips | AT-0039/0040 | PN-0009 | IMPLEMENTADA |
| D15 | setas sem página; Enter preservado | — | PN-0013/0014 | IMPLEMENTADA |

## 12. Elegibilidade

A elegibilidade materializa `tipo == console`, `politica_navegacao.navegavel` e ao menos um item navegável. Grupo, lançador, dashboard, console não navegável e console sem item navegável são excluídos. A travessia é em profundidade e preserva a ordem fornecida pelo modelo.

## 13. Foco e teclado

`\t`, `\x1b[Z` e `\x1b\t` são reconhecidos. A captura TTY real (`_ler_tecla_sessao`) devolve sequências completas de escape; Tab/Shift+Tab e setas passam por `processar_comando`. Lista vazia não altera o estado e reentrada zera o cursor. Em modo não-TTY, `linha.strip()` não é usado como prova de Tab — os smoke checks limitaram-se a carga/renderização/saída.

## 14. Estado de runtime

`foco_console` e `cursores` estão apenas no estado de runtime e possuem defaults defensivos para estados legados. Os oito JSONs não os persistem e não há schema novo.

## 15. Geometria

Há divergência material. `demo/demo.py:409-417` passa a largura total a `largura_navegacao`; `tela/navegacao.py:233-255` usa `largura - 2`; `tela/renderizador.py:2779-2781` reduz primeiro a largura total para `content_w = total_w - 3` e `:2093-2100` reduz mais 2. Com largura 60: navegação usa área 58 e renderer usa 55. AT-0021 e PN-0016 reproduzem o cálculo do módulo, não a geometria efetivamente consumida pelo renderer.

## 16. Movimento

O movimento horizontal consulta somente ocupadas da mesma linha e o vertical somente ocupadas da mesma coluna; wraps e degenerados foram reproduzidos pelos testes. Não há salto diagonal, vizinho mais próximo, compensação de eixo, percurso linear ou mudança de página.

## 17. Seleção

Seleção é derivada do cursor; não há conjunto persistente, toggle de espaço ou indicador de inclusão. PN-0017 passou materialmente.

## 18. Indicador

O símbolo vem de `estilo.selecionado_simbolo`, sem hardcode de `→` em produção. Contudo, para grade 2×3, `tela/renderizador.py:471-497` mapeia cada célula sequencialmente para uma linha física, embora três células compartilhem a primeira linha física. Reprodução:

```text
cursor 0 -> seta antes de G00 (correto)
cursor 1 -> seta antes da linha G10/G11 (não marca G01)
cursor 2 -> seta em linha vazia
cursor 3 -> seta em linha vazia
cursor 4 -> seta em linha vazia
```

Assim, a primeira linha física do item corrente não é marcada para a maior parte da matriz, contrariando D11/D12.

## 19. Chips

`[⇆]` depende de dois ou mais consoles focalizáveis e `[✥]` de console focado com mais de um item navegável. As regras usam `regra_existencia`, não alteram schema e os testes/JSONs de um ou dois consoles demonstram o comportamento contratado.

## 20. Redimensionamento e modos

O cursor lógico é mantido no estado e a navegação recalcula a grade por largura. Porém, os AT-0032–0034 não comprovam mudança material de grade/modo. Além disso, a demo declarada com `--verboso` não aplica a opção: o JSON fornece `politica_exibicao`, o modelo do console apresenta `politica_modo=None`, e `demo/demo.py:777` ainda redefine `modo_verboso` pelo modelo. As saídas não-TTY normal e `--verboso` foram idênticas (2.908 bytes cada).

## 21. Paginação

Nenhum tratamento novo para `<`, `>`, `proxima_pagina` ou `pagina_anterior` foi introduzido. PN-0014 preserva `pagina_atual` ausente/inalterada após setas.

## 22. Enter

Não há dispatcher, registry novo, contador de ação em produção, troca de tela ou resposta nova para Enter. PN-0013 preserva estado de navegação e não introduz infraestrutura de ações.

## 23. Matriz dos oito JSONs

| JSON | Carrega | Finalidade contratada presente | Campos não autorizados | Resultado |
| --- | ---: | ---: | ---: | --- |
| `h0040_nav_console_unico_linear.json` | sim | sim, quatro itens e texto longo | não | APROVADO |
| `h0040_nav_dois_consoles.json` | sim | sim, dois consoles | não | APROVADO |
| `h0040_nav_tres_consoles_em_grupo.json` | sim | sim, grupos assimétricos | não | APROVADO |
| `h0040_nav_console_grade_2x3.json` | sim | sim, 2×3 incompleta | não | APROVADO_COM_DEFEITO_DE_RENDERER |
| `h0040_nav_console_nao_focalizavel.json` | sim | sim, não focalizáveis | não | APROVADO |
| `h0040_nav_degenere_um_item.json` | sim | sim, um item | não | APROVADO |
| `h0040_nav_degenere_uma_linha.json` | sim | sim, uma linha | não | APROVADO |
| `h0040_nav_degenere_uma_coluna.json` | sim | sim, uma coluna | não | APROVADO |

Todos passaram `python -m json.tool` e `carregar_tela`/`construir_modelo`; nenhum contém `foco_console` ou `cursores`.

## 24. Demo

`demo/demo_navegacao.py` contém `main`, `--tela`, delegação ao runtime/renderer reais, EOF seguro e saída não-TTY limpa. O requisito funcional de `--verboso`, contudo, não foi materializado (QAI40-003); por isso a demo não está integralmente aprovada.

## 25. Matriz dos 40 AT

| AT | Teste coletado | Assertiva material | Passou | Resultado |
| --- | --- | --- | ---: | --- |
| AT-0001 | `teste_console_focalizavel_com_itens_navegaveis` | console entra | sim | APROVADO |
| AT-0002 | `teste_console_nao_focalizavel_politica_false` | política false exclui | sim | APROVADO |
| AT-0003 | `teste_console_nao_focalizavel_sem_itens_navegaveis` | sem item exclui | sim | APROVADO |
| AT-0004 | `teste_lancador_nao_entra_lista_foco` | lançador ausente | sim | APROVADO |
| AT-0005 | `teste_dashboard_nao_entra_lista_foco` | dashboard ausente | sim | APROVADO |
| AT-0006 | `teste_grupo_estrutural_percorre_filhos` | filhos sem grupo | sim | APROVADO |
| AT-0007 | `teste_lista_foco_dois_consoles_planos_ordem_declarada` | ordem | sim | APROVADO |
| AT-0008 | `teste_lista_foco_grupo_com_consoles_depth_first` | depth-first | sim | APROVADO |
| AT-0009 | `teste_lista_foco_irmaos_horizontais_esquerda_direita` | esquerda-direita | sim | APROVADO |
| AT-0010 | `teste_lista_foco_irmaos_em_matriz_row_major` | row-major | sim | APROVADO |
| AT-0011 | `teste_tab_avanca_circular` | wrap direto | sim | APROVADO |
| AT-0012 | `teste_shift_tab_recua_circular_duas_sequencias` | ambas sequências | sim | APROVADO |
| AT-0013 | `teste_tab_sem_foco_foca_primeiro` | foco 0 | sim | APROVADO |
| AT-0014 | `teste_shift_tab_sem_foco_foca_ultimo` | último | sim | APROVADO |
| AT-0015 | `teste_entrada_tab_cursor_item_zero` | cursor 0 | sim | APROVADO |
| AT-0016 | `teste_entrada_shift_tab_cursor_item_zero` | cursor 0 | sim | APROVADO |
| AT-0017 | `teste_grade_linear_uma_coluna_n_linhas` | N×1 | sim | APROVADO |
| AT-0018 | `teste_grade_distribuicao_matricial_row_major` | row-major | sim | APROVADO |
| AT-0019 | `teste_grade_celula_vazia_none` | vazio None | sim | APROVADO |
| AT-0020 | `teste_itens_console_linear_preserva_ordem` | ordem lógica | sim | APROVADO |
| AT-0021 | `teste_grade_navegacao_equivale_grade_visual_vigente` | compara motor simulado, não renderer | sim | INSUFICIENTE |
| AT-0022 | `teste_seta_direita_toroide` | wrap linha | sim | APROVADO |
| AT-0023 | `teste_seta_esquerda_toroide` | wrap linha | sim | APROVADO |
| AT-0024 | `teste_seta_baixo_toroide` | wrap coluna | sim | APROVADO |
| AT-0025 | `teste_seta_cima_toroide` | wrap coluna | sim | APROVADO |
| AT-0026 | `teste_celula_vazia_excluida_toroide_horizontal` | pula None | sim | APROVADO |
| AT-0027 | `teste_celula_vazia_excluida_toroide_vertical` | sem movimento | sim | APROVADO |
| AT-0028 | `teste_um_item_qualquer_seta_sem_movimento` | quatro setas | sim | APROVADO |
| AT-0029 | `teste_uma_linha_seta_vertical_sem_movimento` | vertical inerte | sim | APROVADO |
| AT-0030 | `teste_uma_coluna_seta_horizontal_sem_movimento` | horizontal inerte | sim | APROVADO |
| AT-0031 | `teste_redimensionamento_preserva_item_logico` | mesma identidade | sim | APROVADO |
| AT-0032 | `teste_redimensionamento_recalcula_linha_coluna_vizinhos` | não exige mudança nem vizinhos | sim | INSUFICIENTE |
| AT-0033 | `teste_mudanca_modo_preserva_item_logico` | não muda modo | sim | INSUFICIENTE |
| AT-0034 | `teste_mudanca_modo_recalcula_grade_atual` | não muda modo/grade | sim | INSUFICIENTE |
| AT-0035 | `teste_indicador_apenas_console_focado` | contradito no 2×3 | sim | CONTRADITORIO |
| AT-0036 | `teste_indicador_simbolo_do_estilo_coluna_estavel` | só uma coluna, sem grade | sim | INSUFICIENTE |
| AT-0037 | `teste_continuacoes_recebem_selecionado_off` | não prepara continuação | sim | INSUFICIENTE |
| AT-0038 | `teste_selecao_unica_cursor_eh_selecionado` | item sob cursor | sim | APROVADO |
| AT-0039 | `teste_chip_alternar_presente_dois_focalizaveis_ausente_um` | limiar 2 | sim | APROVADO |
| AT-0040 | `teste_chip_navegar_presente_mais_de_um_item_ausente_um_item` | limiar item/foco | sim | APROVADO |

## 26. Matriz das 17 PN

| PN | Teste coletado | Preparação | Estímulo | Condição de falha | Passou | Resultado |
| --- | --- | --- | --- | --- | ---: | --- |
| PN-0001 | `teste_prova_grupo_nunca_na_lista_foco` | grupo com filho | lista | grupo retornado | sim | APROVADO |
| PN-0002 | `teste_prova_lancador_nunca_na_lista_foco` | lançador | lista | lançador retornado | sim | APROVADO |
| PN-0003 | `teste_prova_dashboard_nunca_na_lista_foco` | dashboard | lista | dashboard retornado | sim | APROVADO |
| PN-0004 | `teste_prova_console_nao_navegavel_ou_sem_itens_nunca_na_lista_foco` | dois excluídos | lista | inclusão | sim | APROVADO |
| PN-0005 | `teste_prova_retorno_nao_restaura_cursor_anterior` | dois consoles/cursor 2 | Tab | restaura 2 | sim | APROVADO |
| PN-0006 | `teste_prova_celula_vazia_nao_recebe_cursor_nem_participa_toroide` | 2×3 incompleta | seta | cursor None | sim | APROVADO |
| PN-0007 | `teste_prova_eixo_nao_cruza_linha_nem_coluna` | 2×3 | direita/baixo | troca eixo | sim | APROVADO |
| PN-0008 | `teste_prova_indicador_nao_aparece_em_console_nao_focado` | dois consoles | render | símbolo no não focado | sim | APROVADO |
| PN-0009 | `teste_prova_chip_navegar_nao_aparece_com_um_item` | um item | render | `[✥]` | sim | APROVADO |
| PN-0010 | `teste_prova_indicador_nao_aparece_em_linha_de_continuacao` | sem continuação real | render | símbolo em continuação | sim | INSUFICIENTE |
| PN-0011 | `teste_prova_mudanca_modo_nao_reinicia_item_zero` | modo não alternável | V | cursor 0 após alternância | sim | INSUFICIENTE |
| PN-0012 | `teste_prova_redimensionamento_nao_perde_identidade_logica` | cursor item 2 | resize | identidade muda | sim | APROVADO |
| PN-0013 | `teste_prova_enter_nao_executa_acao` | cursor/sentinela | Enter | ação | sim | APROVADO |
| PN-0014 | `teste_prova_setas_nao_mudam_pagina` | página observável | quatro setas | página muda | sim | APROVADO |
| PN-0015 | `teste_prova_indicador_nao_hardcoded` | estilo X | render | símbolo divergente | sim | APROVADO |
| PN-0016 | `teste_prova_grade_navegacao_nao_diverge_grade_visual` | cálculo duplicado | comparar | coordenadas divergentes | sim | INSUFICIENTE |
| PN-0017 | `teste_prova_space_nao_togla_inclusao` | cursor | espaço | conjunto/toggle | sim | APROVADO |

## 27. Reconciliação numérica

```yaml
AT:
  esperados: 40
  encontrados: 40
  unicos: 40
  aprovados: 33
  insuficientes: 6
  ausentes: 0
  contraditorios: 1
PN:
  esperadas: 17
  encontradas: 17
  unicas: 17
  aprovadas: 14
  insuficientes: 3
  ausentes: 0
testes_novos:
  declarados: 57
  coletados: 57
  correspondencia_identificador_por_teste: sim
```

## 28. Testes focais

```yaml
testes_focais:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_navegacao.py -q
  coletados: 57
  aprovados: 57
  ignorados: 0
  falhas: 0
  erros: 0
```

## 29. Regressão direta

```yaml
regressao_direta:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py demo/teste_demo.py tela/teste_loader.py tela/teste_distribuicao_matricial.py -q
  coletados: 352
  aprovados: 352
  ignorados: 0
  falhas: 0
  erros: 0
```

## 30. Suíte canônica

```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  coletados: 480
  aprovados: 480
  ignorados: 0
  falhas: 0
  erros: 0
  duracao: 17.00s
```

## 31. Smoke checks

Entrada não-TTY controlada: `printf 's\\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao ...`; `s` garante encerramento limpo após a primeira renderização. Nenhum resultado é validação visual.

```yaml
smoke_checks:
  dois_consoles:
    comando: "printf 's\\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json"
    stdout_linhas: 24
    stderr_bytes: 0
    exit: 0
  grade_2x3:
    comando: "printf 's\\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json"
    stdout_linhas: 24
    stderr_bytes: 0
    exit: 0
  console_unico_linear_verboso:
    comando: "printf 's\\n' | PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso"
    stdout_linhas: 24
    stderr_bytes: 0
    exit: 0
```

## 32. Compatibilidade retroativa

As 352 regressões diretamente relacionadas e a suíte de 480 passaram. Assinaturas públicas receberam parâmetros opcionais e estados legados são aceitos. Isto não remove os defeitos novos de indicador/geometria/demo; o comportamento H-0040 continua a exigir patch.

## 33. Relatório de implementação

O relatório é correto sobre a existência dos arquivos, comandos executados, contagens brutas e ausência de operações Git de escrita. É factualmente divergente ao declarar as 40 AT e 17 PN materialmente aprovadas, D11/D12 implementadas e suporte de demo a `--verboso`, pois a auditoria independente encontrou a contradição e lacunas descritas.

## 34. Validação manual pendente

```yaml
validacao_manual:
  executada_pelo_QA: nao
  motivo: EXCLUSIVA_DO_USUARIO
  roteiro_disponivel: sim
  necessaria_apos_aprovacao_tecnica: sim
```

## 35. Busca de escopo indevido

As ocorrências de `dispatcher`, `registry`, `toggle`, `proxima_pagina` e `pagina_anterior` estão em comentários/docstrings preexistentes ou negações explícitas, não em infraestrutura nova. Não foi encontrado comportamento de página, ação ou seleção múltipla introduzido pelo H-0040.

## 36. Achados

```yaml
achados:
  - id: QAI40-001
    severidade: MAIOR
    categoria: [IMPLEMENTACAO, RENDERIZACAO, TESTE_AT, PROVA_PN]
    arquivo: tela/renderizador.py
    simbolo_ou_linha: "_linhas_fisicas_por_item (471-497) / _aplicar_indicador_linhas (415-429)"
    autoridade: "ADR-0031 D11/D12; H-0040 AT-0035/0037, PN-0010"
    evidencia_material: "No JSON 2x3 a seta marca G00 para cursor 0, a linha G10/G11 para cursor 1 e linhas vazias para cursores 2-4."
    comportamento_encontrado: "Células row-major são tratadas como linhas físicas sequenciais."
    comportamento_esperado: "Somente a primeira linha física do item corrente, no console focado, recebe o símbolo."
    correcao_necessaria: "Mapear a posição física real da célula/item e cobrir grade matricial e continuações reais."
  - id: QAI40-002
    severidade: MAIOR
    categoria: [GEOMETRIA, IMPLEMENTACAO, TESTE_AT, PROVA_PN]
    arquivo: demo/demo.py; tela/navegacao.py; tela/renderizador.py
    simbolo_ou_linha: "demo.py:409-417; navegacao.py:233-255; renderizador.py:2093-2100,2779-2781"
    autoridade: "ADR-0031 D7/D10/D12; H-0040 AT-0021, PN-0016"
    evidencia_material: "Para largura total 60, navegação usa area_w=58 e renderer usa area_w=55."
    comportamento_encontrado: "Parâmetros efetivos do mesmo motor divergem."
    comportamento_esperado: "Navegação e renderer devem consumir a mesma largura útil e resultado vigente."
    correcao_necessaria: "Centralizar/repassar a largura útil real e testar contra o renderer integrado."
  - id: QAI40-003
    severidade: MAIOR
    categoria: [DEMONSTRACAO, IMPLEMENTACAO, TESTE_AT]
    arquivo: demo/demo_navegacao.py; demo/demo.py
    simbolo_ou_linha: "demo_navegacao.py:150-158; demo.py:761-777"
    autoridade: "H-0040 seção 22; requisito de demo --verboso; D10"
    evidencia_material: "Modelo do JSON tem politica_modo=None; saída normal e --verboso foi idêntica (2.908 bytes)."
    comportamento_encontrado: "A opção é aceita, mas não estabelece modo verboso."
    comportamento_esperado: "--verboso deve iniciar o modo verboso contratado, preservando a integração real."
    correcao_necessaria: "Propagar a opção por estado/contrato efetivo e adicionar teste de efeito."
  - id: QAI40-004
    severidade: MAIOR
    categoria: [RELATORIO, EVIDENCIA]
    arquivo: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
    simbolo_ou_linha: "seções 4-10 e 15"
    autoridade: "Instrução QA seção 34"
    evidencia_material: "Declara 40 AT/17 PN aprovadas e suporte --verboso, contrariados por QAI40-001 a QAI40-003."
    comportamento_encontrado: "Relatório apresenta aprovação factual não sustentada."
    comportamento_esperado: "Contagens e afirmações devem refletir evidência material reproduzida."
    correcao_necessaria: "Atualizar o relatório junto do patch de implementação/testes."
```

## 37. Classificação final

```yaml
classificacao: I2_IMPLEMENTATION_PATCH_REQUIRED
motivo: "Achados maiores corrigíveis em renderer, geometria, demo, testes e relatório."
implementacao_tecnicamente_aprovada: nao
```

## 38. Arquivos criados pelo QA

```yaml
arquivos_criados:
  - docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
```

## 39. Estado Git final

```yaml
efeito_do_QA:
  arquivos_preexistentes_alterados: []
  arquivos_criados:
    - docs/relatorios/RELATORIO_QA_H-0040_IMPLEMENTACAO.md
  operacoes_git_de_escrita: []
  commit_executado: nao
  validacao_manual_executada: nao
```

O estado acumulado anterior foi preservado; o único arquivo novo do QA no worktree é este relatório.

## 40. Encerramento

I2_IMPLEMENTATION_PATCH_REQUIRED
