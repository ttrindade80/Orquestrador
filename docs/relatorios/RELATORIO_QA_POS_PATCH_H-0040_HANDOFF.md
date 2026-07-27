---
name: relatorio-qa-pos-patch-h-0040-handoff
description: Relatorio de QA pos-patch independente do handoff H-0040
metadata:
  type: relatorio
  etapa: QA_POS_PATCH_HANDOFF
  handoff: H-0040
  status: H1_HANDOFF_APPROVED
---

# Relatório de QA Pós-Patch do Handoff H-0040

## 1. Identificação

```yaml
resultado:
  etapa: QA_POS_PATCH_HANDOFF
  handoff: H-0040
  status: H1_HANDOFF_APPROVED
  data: 2026-07-25
```

## 2. Objeto e escopo

Auditoria pós-patch independente do handoff `H-0040` (docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md) à luz do relatório de QA inicial (docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md) e do relatório de patch (docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md). Não há alteração de código, testes, ADRs, contratos ou implementações nesta etapa. O único limite material é a criação deste relatório.

## 3. Estado documental

```yaml
handoff:
  numero: H-0040
  status: HANDOFF_PATCH_COMPLETED_AWAITING_QA

origem:
  item_de_backlog: ITEM-0002
  adr: ADR-0031

qa_inicial:
  relatorio: docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
  classificacao: H2_HANDOFF_PATCH_REQUIRED

patch:
  relatorio: docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
  status: HANDOFF_PATCH_COMPLETED_AWAITING_QA

implementacao:
  iniciada: false
```

## 4. Estado Git acumulado

```yaml
estado_git_inicial:
  arquivos_staged: []
  arquivos_unstaged:
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
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

## 5. Gate

```yaml
gate_pos_patch:
  H-0040_existe: true
  H-0040_ultima_linha: HANDOFF_PATCH_COMPLETED_AWAITING_QA
  QA_inicial_existe: true
  QA_inicial_termina_REQUIRED: true
  Relatorio_patch_existe: true
  Relatorio_patch_ultima_linha: HANDOFF_PATCH_COMPLETED_AWAITING_QA
  Post_QA_preexistente: false
  conflitos_git_ativos: false
```

## 6. Autoridades lidas

Lidos na íntegra:
- `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`
- `docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md`
- `docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md`
- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`

Lidos seletivamente:
- `demo/demo.py`
- `demo/teste_demo.py`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/distribuicao_matricial.py`

## 7. Método

1. Confirmação dos gates e inventário de caminhos.
2. Análise detalhada do tratamento dado a cada achado (QAH40-001 a QAH40-008).
3. Verificação de consistência e suficiência de testes (AT/PN).
4. Verificação das proibições de Enter, escopo negativo, demonstração e validação manual.
5. Verificação das delimitações dos pontos NC e riscos de runtime.
6. Geração do relatório com classificação final.

## 8. QAH40-001 (Arquivos novos)

O H-0040 possui uma única lista canônica com exatamente 13 arquivos novos. Sem wildcards, sem ambiguidades e sem contradições numéricas entre as seções.

```yaml
arquivos_novos:
  total: 13
  caminhos_unicos: 13
  curingas: 0
  contradicoes_entre_secoes: 0
```

Caminhos nominais verificados na seção 8 do H-0040:
1. `tela/navegacao.py`
2. `demo/demo_navegacao.py`
3. `demo/teste_demo_navegacao.py`
4. `tela/teste_navegacao.py`
5. `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md`
6. `config/telas/demo/h0040_nav_console_unico_linear.json`
7. `config/telas/demo/h0040_nav_dois_consoles.json`
8. `config/telas/demo/h0040_nav_tres_consoles_em_grupo.json`
9. `config/telas/demo/h0040_nav_console_grade_2x3.json`
10. `config/telas/demo/h0040_nav_console_nao_focalizavel.json`
11. `config/telas/demo/h0040_nav_degenere_um_item.json`
12. `config/telas/demo/h0040_nav_degenere_uma_linha.json`
13. `config/telas/demo/h0040_nav_degenere_uma_coluna.json`

## 9. Arquivos modificáveis

Os únicos arquivos existentes com modificação autorizada são exatamente:
- `demo/demo.py`
- `tela/renderizador.py`

Eles são materialmente e estruturalmente suficientes para implementar teclado (Tab, Shift+Tab, setas), foco, cursor, chips dinamizados, indicadores visuais e reatividades a Sigwinch/modos sem precisar alterar outro arquivo preexistente.

## 10. Arquivos preservados

A seção 9 do H-0040 lista explicitamente 22 arquivos existentes a serem preservados. Não há arquivos classificados simultaneamente como modificáveis, novos e preservados.

## 11. QAH40-002 (Testes e coleta)

O comando canônico e o de coleta foram perfeitamente unificados. A contagem de 423 testes foi devidamente classificada como uma fotografia histórica no momento da autoria, permitindo explicitamente o crescimento da suíte de testes após a implementação do H-0040.

```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  comando_coleta: PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q
  coleta_inicial: 423
  natureza: COLETA_NO_MOMENTO_DA_AUTORIA
  contagem_pos_implementacao_fixa: false
  crescimento_permitido: true
  resultado_exigido:
    falhas: 0
    erros: 0
```

## 12. QAH40-003 (Relatório futuro de implementação)

O template e o caminho do relatório futuro estão perfeitamente documentados na seção 24 de H-0040. O arquivo nominal preservado é `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md` e os campos obrigatórios estão integrados. O marcador de encerramento exigido é estritamente `IMPLEMENTATION_COMPLETED_AWAITING_QA`.

## 13. Critérios de aceitação (AT)

A seção 19 de H-0040 define exatamente 40 critérios de aceitação automatizados (AT-0001 a AT-0040). Todos são exequíveis, possuem identificadores únicos, sem lacunas ou duplicidades.

```yaml
AT:
  primeiro: AT-0001
  ultimo: AT-0040
  identificadores_unicos: 40
  lacunas: 0
  duplicatas: 0
```

| AT | Decisão | Teste nominal | Superfície observável | Exequível | Resultado |
| -- | ------- | ------------- | --------------------- | --------- | --------- |
| AT-0001 | D2 | `teste_console_focalizavel_com_itens_navegaveis` | lista de foco | sim | APROVADO |
| AT-0002 | D2 | `teste_console_nao_focalizavel_politica_false` | lista de foco | sim | APROVADO |
| AT-0003 | D2 | `teste_console_nao_focalizavel_sem_itens_navegaveis` | lista de foco | sim | APROVADO |
| AT-0004 | D1 | `teste_lancador_nao_entra_lista_foco` | lista de foco | sim | APROVADO |
| AT-0005 | D1 | `teste_dashboard_nao_entra_lista_foco` | lista de foco | sim | APROVADO |
| AT-0006 | D3 | `teste_grupo_estrutural_percorre_filhos` | lista de foco | sim | APROVADO |
| AT-0007 | D3 | `teste_lista_foco_dois_consoles_planos_ordem_declarada` | lista de foco | sim | APROVADO |
| AT-0008 | D3 | `teste_lista_foco_grupo_com_consoles_depth_first` | lista de foco | sim | APROVADO |
| AT-0009 | D4 | `teste_lista_foco_irmaos_horizontais_esquerda_direita` | lista de foco | sim | APROVADO |
| AT-0010 | D4 | `teste_lista_foco_irmaos_em_matriz_row_major` | lista de foco | sim | APROVADO |
| AT-0011 | D5 | `teste_tab_avanca_circular` | foco_console | sim | APROVADO |
| AT-0012 | D5 | `teste_shift_tab_recua_circular_duas_sequencias` | foco_console | sim | APROVADO |
| AT-0013 | D5 | `teste_tab_sem_foco_foca_primeiro` | foco_console | sim | APROVADO |
| AT-0014 | D5 | `teste_shift_tab_sem_foco_foca_ultimo` | foco_console | sim | APROVADO |
| AT-0015 | D6 | `teste_entrada_tab_cursor_item_zero` | cursores | sim | APROVADO |
| AT-0016 | D6 | `teste_entrada_shift_tab_cursor_item_zero` | cursores | sim | APROVADO |
| AT-0017 | D7 | `teste_grade_linear_uma_coluna_n_linhas` | grade de navegacao | sim | APROVADO |
| AT-0018 | D7 | `teste_grade_distribuicao_matricial_row_major` | posicoes renderizadas | sim | APROVADO |
| AT-0019 | D8 | `teste_grade_celula_vazia_none` | grade de navegacao | sim | APROVADO |
| AT-0020 | D7 | `teste_itens_console_linear_preserva_ordem` | itens navegaveis | sim | APROVADO |
| AT-0021 | D7 | `teste_grade_navegacao_equivale_grade_visual_vigente` | renderizacao e grade | sim | APROVADO |
| AT-0022 | D8 | `teste_seta_direita_toroide` | cursor | sim | APROVADO |
| AT-0023 | D8 | `teste_seta_esquerda_toroide` | cursor | sim | APROVADO |
| AT-0024 | D8 | `teste_seta_baixo_toroide` | cursor | sim | APROVADO |
| AT-0025 | D8 | `teste_seta_cima_toroide` | cursor | sim | APROVADO |
| AT-0026 | D8 | `teste_celula_vazia_excluida_toroide_horizontal` | cursor | sim | APROVADO |
| AT-0027 | D8 | `teste_celula_vazia_excluida_toroide_vertical` | cursor | sim | APROVADO |
| AT-0028 | D9 | `teste_um_item_qualquer_seta_sem_movimento` | cursor | sim | APROVADO |
| AT-0029 | D9 | `teste_uma_linha_seta_vertical_sem_movimento` | cursor | sim | APROVADO |
| AT-0030 | D9 | `teste_uma_coluna_seta_horizontal_sem_movimento` | cursor | sim | APROVADO |
| AT-0031 | D10 | `teste_redimensionamento_preserva_item_logico` | cursores e grade | sim | APROVADO |
| AT-0032 | D10 | `teste_redimensionamento_recalcula_linha_coluna_vizinhos` | linha coluna e vizinhos | sim | APROVADO |
| AT-0033 | D10 | `teste_mudanca_modo_preserva_item_logico` | cursores e renderizacao | sim | APROVADO |
| AT-0034 | D10 | `teste_mudanca_modo_recalcula_grade_atual` | grade e renderizacao | sim | APROVADO |
| AT-0035 | D11 | `teste_indicador_apenas_console_focado` | renderizacao | sim | APROVADO |
| AT-0036 | D12 | `teste_indicador_simbolo_do_estilo_coluna_estavel` | coluna indicadora | sim | APROVADO |
| AT-0037 | D12 | `teste_continuacoes_recebem_selecionado_off` | renderizacao verbosa | sim | APROVADO |
| AT-0038 | D13 | `teste_selecao_unica_cursor_eh_selecionado` | item selecionado | sim | APROVADO |
| AT-0039 | D14 | `teste_chip_alternar_presente_dois_focalizaveis_ausente_um` | barra de menus | sim | APROVADO |
| AT-0040 | D14 | `teste_chip_navegar_presente_mais_de_um_item_ausente_um_item` | barra de menus | sim | APROVADO |

## 14. Provas negativas (PN)

A seção 20 do H-0040 define exatamente 17 provas negativas automatizadas (PN-0001 a PN-0017).

```yaml
PN:
  primeiro: PN-0001
  ultimo: PN-0017
  identificadores_unicos: 17
  lacunas: 0
  duplicatas: 0
```

| PN | Proibição | Preparação | Estímulo | Observação | Falha detectável | Resultado |
| -- | --------- | ---------- | -------- | ---------- | ---------------- | --------- |
| PN-0001 | grupo focado | grupo com filhos | construir lista | tipo retornado | tipo grupo na lista | APROVADO |
| PN-0002 | lancador focado | lancador no corpo | construir lista | ids na lista | lancador na lista | APROVADO |
| PN-0003 | dashboard focado | dashboard no corpo | construir lista | ids na lista | dashboard na lista | APROVADO |
| PN-0004 | politica false | console com navegavel false | construir lista | lista de foco | console aparece | APROVADO |
| PN-0005 | console vazio focado | console sem itens navegaveis | construir lista | lista de foco | console focado | APROVADO |
| PN-0006 | celula vazia no toroide | grade com vazias | mover cursor e wrap | cursor e vizinhos | cursor em None ou toroidal pulando errado | APROVADO |
| PN-0007 | horizontal muda linha | item no fim da linha | seta direita/esquerda | linha do cursor | linha mudou | APROVADO |
| PN-0008 | vertical muda coluna | item no fim da coluna | seta baixo/cima | coluna do cursor | coluna mudou | APROVADO |
| PN-0009 | [✥] com um item | console com um item | renderizar barra | texto renderizado | [✥] aparece | APROVADO |
| PN-0010 | indicador na continuacao | multilinha verboso | renderizar console | linhas fisicas | indicador na linha de continuacao | APROVADO |
| PN-0011 | modo reinicia cursor | cursor no item 2 | alternar modo | cursor posterior | cursor vira 0 | APROVADO |
| PN-0012 | redim. perde identidade | cursor em item | grade estreita | id do item focado | id mudou ou vira 0 | APROVADO |
| PN-0013 | Enter executa acao | item focalizado | processar Enter | estado e log de acoes | acao disparada ou dispatcher acionado | APROVADO |
| PN-0014 | setas mudam pagina | console paginado | quatro setas | pagina_atual | pagina mudou | APROVADO |
| PN-0015 | indicador hardcoded | estilo com X | renderizar console | texto renderizado | aparece '→' em vez de X | APROVADO |
| PN-0016 | grade divergente | grade de navegacao e renderer | calcular e renderizar | coordenadas | coordenadas divergentes | APROVADO |
| PN-0017 | espaco alterna selecao | cursor posicionado | processar tecla Espaco | estado de selecao | toggle executado ou alteracao | APROVADO |

## 15. Reconciliação AT/PN

A matriz de reconciliação de testes do H-0040 está correta e preserva integralmente:

```yaml
AT:
  total: 40
  unicos: 40
  lacunas: 0
  duplicatas: 0

PN:
  total: 17
  unicos: 17
  lacunas: 0
  duplicatas: 0
```

Todas as reformulações necessárias mapeadas no QA inicial foram adequadamente consolidadas e integradas na matriz (Seção 21 do H-0040).

## 16. Demonstração fechada

O roteiro de demonstração na seção 22 do H-0040 está nominal, exato e fechado. O arquivo nominal é `demo/demo_navegacao.py`. Mapeamento dos 8 cenários com seus respectivos comandos e JSONs vigentes:

| JSON | Finalidade | Comando | Comportamentos cobertos |
| ---- | ---------- | ------- | ----------------------- |
| `h0040_nav_dois_consoles.json` | dois consoles focalizaveis | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json` | Tab/Shift+Tab alternam foco; [⇆] ativo; indicador so no focado |
| `h0040_nav_console_nao_focalizavel.json` | console nao focalizavel | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_nao_focalizavel.json` | Tab nao foca; [⇆] e [✥] ausentes |
| `h0040_nav_tres_consoles_em_grupo.json` | grupos aninhados assimetricos | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_tres_consoles_em_grupo.json` | Ordem de foco DFS por Tab/Shift+Tab |
| `h0040_nav_console_grade_2x3.json` | matriz incompleta | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json` | Seta move cursor; None nao foca nem participa do toroide |
| `h0040_nav_degenere_um_item.json` | um item | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_degenere_um_item.json` | Setas nao movem; [✥] ausente |
| `h0040_nav_degenere_uma_linha.json` | uma linha | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_degenere_uma_linha.json` | Seta vertical inativa; horizontal toroidal |
| `h0040_nav_degenere_uma_coluna.json` | uma coluna | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_degenere_uma_coluna.json` | Seta horizontal inativa; vertical toroidal |
| `h0040_nav_console_unico_linear.json` | item multilinha e redimensionamento | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso` | Indicador so na primeira linha em verboso; Sigwinch preserva item |

## 17. Enter

```yaml
Enter:
  alteracao_autorizada_neste_handoff: false
  nova_resposta_demonstrativa: proibida
  execucao_de_acao: proibida
  comportamento_preexistente: preservar
```

Qualquer autorização para exibir ID, texto ou executar ações através da tecla Enter foi devidamente removida de H-0040, garantindo o isolamento do escopo do Bloco 2.

## 18. Escopo negativo

O escopo negativo foi integralmente consolidado. Foram explicitamente proibidos novos comportamentos ou alterações funcionais para: paginação interativa por setas, registro e dispatcher de ações, abertura de outra tela, retorno por pilha, seleção múltipla (toggle por espaço), indicador de inclusão, navegação multinível, colapsamento, tiling, cabeçalho estreito, alteração de dashboard e lançador, e alteração de cores de alerta e inativo.
Foram preservados os itens futuros de backlog `ITEM-0003` a `ITEM-0009`.

## 19. Validação manual

A validação manual na seção 23 do H-0040 está em conformidade total.

```yaml
validacao_manual:
  executante: USUARIO
  exclusiva_do_usuario: true
  executada_na_autoria_do_handoff: false
  executada_na_implementacao_automatica: false
```

Não há solicitações técnicas indevidas ao usuário. Os testes cobrem explicitamente e separadamente: Tab, Shift+Tab, setas direcionais, troca de modo verboso/não verboso e as variações de redimensionamento (maximizar, restaurar, reduzir, livremente), finalizando com a obrigação de registro posterior do resultado pelo usuário.

## 20. Regra operacional de exceção

A regra operacional de exceção foi adicionada com sucesso no H-0040 (seção 11):

```yaml
arquivo_fora_da_lista:
  acao: PARAR_ANTES_DA_ALTERACAO
  informar:
    - caminho_exato
    - responsabilidade_atual
    - motivo_da_necessidade
    - risco_de_nao_alterar
    - alteracao_minima_proposta
    - se_cria_nova_semantica
  aguardar_autorizacao_do_usuario: true
  alteracao_sem_autorizacao: proibida
```

A regra é explícita e intransigente para qualquer alteração fora da lista, sem brechas ou permissões genéricas.

## 21. NC-001 a NC-006

Todos os seis pontos foram adequadamente auditados e integrados com as classificações esperadas:

- **NC-001** (VERIFICACAO_TECNICA_NAO_BLOQUEANTE): Exige teste explícito de `\x1b[Z` e `\x1b\t` sem eleger uma única sequência como exclusiva.
- **NC-002** (VERIFICACAO_TECNICA_NAO_BLOQUEANTE): D23 atribuído à ADR-0028/nomenclatura, não como decisão de ADR-0031. `ElementoCorpo._campos_inertes` e ineligibilidade de console sem itens navegáveis estão corretas.
- **NC-003** (DELIMITADO_PELO_PATCH): `grade_de_itens()` autorizada como nova função, consumindo a mesma geometria visual vigente calculada pelo renderer em `distribuicao_matricial.py`. Proibição de grades paralelas.
- **NC-004** (VERIFICACAO_TECNICA_NAO_BLOQUEANTE): `regra_existencia` tratada como campo já contratado. Relaciona nominalmente os JSONs e chips.
- **NC-005** (VERIFICACAO_TECNICA_NAO_BLOQUEANTE): `foco_console` e `cursores` são estados de runtime e não devem ser persistidos. Mudanças em `demo/teste_demo.py` dependem da regra de exceção.
- **NC-006** (DELIMITADO_PELO_PATCH): Identidade lógica separada da visual; geometria dependente da largura atual. Grade independente proibida.

## 22. Riscos

Todos os 11 riscos mapeados na seção 21 estão associados a pelo menos um mecanismo correspondente (AT, PN, preservação, validação manual ou exceção), sem lacunas ou pontas soltas na segurança do runtime.

## 23. Matriz D1-D15

A avaliação das decisões D1 a D15 do H-0040 resultou em aprovação total:

| Decisão | Requisito | Arquivos | AT | PN | Resultado |
| ------- | --------- | -------- | -- | -- | --------- |
| D1 | Escopo de nível único | `demo/demo.py`, `renderizador.py` | AT-0004..AT-0005 | PN-0002..PN-0003 | COBERTA |
| D2 | Elegibilidade do console | `tela/navegacao.py` | AT-0001..AT-0003 | PN-0004..PN-0005 | COBERTA |
| D3 | Lista linear de foco | `tela/navegacao.py` | AT-0006..AT-0008 | PN-0001 | COBERTA |
| D4 | Ordem espacial row-major | `tela/navegacao.py` | AT-0009..AT-0010 | — | COBERTA |
| D5 | Tab/Shift+Tab circulares | `demo/demo.py`, `tela/navegacao.py` | AT-0011..AT-0014 | — | COBERTA |
| D6 | Entrada no item zero | `demo/demo.py`, `tela/navegacao.py` | AT-0015..AT-0016 | — | COBERTA |
| D7 | Ordem lógica row-major | `tela/navegacao.py` | AT-0017..AT-0018, AT-0020..AT-0021 | PN-0016 | COBERTA |
| D8 | Toroide estrito por eixo | `tela/navegacao.py` | AT-0022..AT-0027 | PN-0006..PN-0008 | COBERTA |
| D9 | Casos degenerados | `tela/navegacao.py` | AT-0028..AT-0030 | — | COBERTA |
| D10 | Preservação no redim./modo | `demo/demo.py`, `tela/navegacao.py` | AT-0031..AT-0034 | PN-0011..PN-0012 | COBERTA |
| D11 | Cursor só no console focado | `tela/renderizador.py` | AT-0035 | PN-0013 | COBERTA |
| D12 | Coluna indicadora estável | `tela/renderizador.py` | AT-0036..AT-0037 | PN-0010, PN-0015 | COBERTA |
| D13 | Seleção única sob cursor | `tela/navegacao.py` | AT-0038 | PN-0017 | COBERTA |
| D14 | Chips [⇆] e [✥] contextuais | `tela/renderizador.py` | AT-0039..AT-0040 | PN-0009, PN-0014 | COBERTA |
| D15 | Setas sem mudar página | `tela/navegacao.py` | — | PN-0014 | COBERTA |

## 24. Matriz dos achados iniciais

| Achado inicial | Resultado pós-patch | Evidência |
| -------------- | ------------------- | --------- |
| QAH40-001 | CORRIGIDO | Lista canônica unificada de 13 arquivos (Seção 8) |
| QAH40-002 | CORRIGIDO | Comandos Pytest e crescimento explícito unificados (Seção 18) |
| QAH40-003 | CORRIGIDO | Template de relatório futuro atualizado com encerramento (Seção 24) |
| QAH40-004 | CORRIGIDO | AT-0001..0040 e PN-0001..0017 completos e corrigidos (Seções 19-21) |
| QAH40-005 | CORRIGIDO | Demonstração com 8 cenários e commands exatos, sem Enter (Seção 22) |
| QAH40-006 | CORRIGIDO | Roteiro de validação manual exclusivo, não-técnico (Seção 23) |
| QAH40-007 | CORRIGIDO | Regra operacional de exceção ativada (Seção 11) |
| QAH40-008 | DELIMITADO | NC analisados e delimitados com precisão (Seção 25) |

## 25. Novos achados

```yaml
novos_achados: []
```

Não foram encontrados novos defeitos ou contradições introduzidos pelas correções do patch. O artefato documental está consistente e robusto.

## 26. Classificação final

```yaml
classificacao_final: H1_HANDOFF_APPROVED
```

## 27. Arquivos criados pelo QA nesta etapa

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
```

## 28. Estado Git final

```yaml
estado_git_final:
  arquivos_staged: []
  arquivos_unstaged:
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
  arquivos_staged_e_unstaged: []
  arquivos_nao_rastreados:
    - __pycache__/conftest.cpython-314-pytest-9.0.3.pyc
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
    - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

## 29. Encerramento

H1_HANDOFF_APPROVED