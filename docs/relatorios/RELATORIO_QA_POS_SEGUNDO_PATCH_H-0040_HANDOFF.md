---
name: relatorio-qa-pos-segundo-patch-h-0040-handoff
description: Relatorio de auditoria pos-segundo-patch independente do handoff H-0040
metadata:
  type: relatorio
  etapa: QA_POS_SEGUNDO_PATCH_HANDOFF
  handoff: H-0040
  status: H1_HANDOFF_APPROVED
---

# Relatório de QA Pós-Segundo-Patch do Handoff H-0040

## 1. Identificação

```yaml
resultado:
  etapa: QA_POS_SEGUNDO_PATCH_HANDOFF
  handoff: H-0040
  status: H1_HANDOFF_APPROVED
  data: 2026-07-25
```

## 2. Objeto e escopo

Auditoria independente do segundo patch do handoff `H-0040` (`docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`) à luz do relatório do segundo patch (`docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md`) e do histórico acumulado de QA e patches anteriores do ciclo. Esta etapa não altera código, testes, JSONs ou o artefato do handoff. O único arquivo criado nesta etapa é este relatório.

## 3. Estado documental

```yaml
handoff:
  numero: H-0040
  status: HANDOFF_PATCH_COMPLETED_AWAITING_QA

qa_inicial:
  classificacao: H2_HANDOFF_PATCH_REQUIRED

primeiro_patch:
  resultado: HANDOFF_PATCH_COMPLETED_AWAITING_QA

qa_pos_primeiro_patch:
  resultado_literal: H1_HANDOFF_APPROVED
  aceite_gerencial: REJEITADO_POR_INCONSISTENCIA_MATERIAL

segundo_patch:
  relatorio: docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
  achados_declarados:
    SPH40-001: CORRIGIDO
    SPH40-002: CORRIGIDO
    SPH40-003: CORRIGIDO

implementacao:
  iniciada: false
  liberada: false
```

## 4. Estado Git inicial

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
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

## 5. Gate

```yaml
gate_pos_segundo_patch:
  handoff_H0040_existe: true
  handoff_H0040_ultima_linha_COMPLETED: true
  qa_inicial_existe: true
  primeiro_relatorio_patch_existe: true
  primeiro_qa_pos_patch_existe: true
  relatorio_segundo_patch_existe: true
  relatorio_segundo_patch_ultima_linha_COMPLETED: true
  RELATORIO_QA_POS_SEGUNDO_PATCH_preexistente: false
  conflitos_git_impedindo_leitura: false
  autoridades_ausentes: false
```

## 6. Autoridades

Lidos na íntegra:
- `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`
- `docs/relatorios/RELATORIO_QA_H-0040_HANDOFF.md`
- `docs/relatorios/RELATORIO_PATCH_H-0040_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md`
- `docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md`
- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`

Lidos seletivamente:
- `demo/demo.py`
- `tela/renderizador.py`
- `tela/distribuicao_matricial.py`

## 7. Método

1. Verificação dos gates de integridade e existência dos arquivos.
2. Análise minuciosa de cada um dos achados declarados corrigidos pelo segundo patch (`SPH40-001`, `SPH40-002`, `SPH40-003`).
3. Avaliação da cobertura material e detecção de falha das 17 proibições negativas (PN).
4. Auditoria específica dos critérios materiais de `PN-0005` e `PN-0008` diretamente no H-0040.
5. Verificação da consistência de roteiro, comandos literais e separação de teclas na validação manual (VM-01 a VM-11).
6. Execução de pesquisa no codebase para conformidade taxonômica de termos como `HANDOFF_QA_APPROVED` ou declarações de aprovação presumida.
7. Varredura focal contra regressão de achados de QAs anteriores.
8. Geração de relatórios e de matrizes de reconciliação.

## 8. Auditoria de `SPH40-001`

A reorganização das proibições negativas foi confirmada com rigor. O H-0040 traz uma única seção canônica de 17 proibições, sem lacunas e sem duplicatas. Cada prova negativa contém os atributos obrigatórios de identificação, proibição, preparação, estímulo, observação, condição de falha e teste nominal. As provas são formalmente coerentes com as decisões D1 a D15 da ADR-0031 e do fluxo.

## 9. Matriz das 17 PN

| PN | Preparação suficiente | Estímulo observável | Condição de falha detectável | Teste nominal | Resultado |
|---|---|---|---|---|---|
| PN-0001 | grupo com filhos focalizáveis | construir lista | tipo grupo retornado | `prova_grupo_nunca_na_lista_foco` | APROVADA |
| PN-0002 | lançador no corpo | construir lista | lançador retornado | `prova_lancador_nunca_na_lista_foco` | APROVADA |
| PN-0003 | dashboard no corpo | construir lista | dashboard retornado | `prova_dashboard_nunca_na_lista_foco` | APROVADA |
| PN-0004 | um console com navegável false e outro com navegável true sem itens navegáveis | construir lista | qualquer dos dois consoles aparece na lista de foco | `prova_console_nao_navegavel_ou_sem_itens_nunca_na_lista_foco` | APROVADA |
| PN-0005 | pelo menos dois consoles focalizáveis; cursor do primeiro fora do item 0; foco muda de console; retorno por Tab/Shift+Tab | Tab ou Shift+Tab de volta ao primeiro | cursor anterior restaurado ou diferente do item lógico 0 | `prova_retorno_nao_restaura_cursor_anterior` | APROVADA |
| PN-0006 | matriz incompleta com None entre itens | seta horizontal e vertical com wrap | cursor em None ou movimento conta None como passo | `prova_celula_vazia_nao_recebe_cursor_nem_participa_toroide` | APROVADA |
| PN-0007 | item no fim da linha e item no fim da coluna | seta direita e seta baixo | linha mudou na horizontal ou coluna mudou na vertical | `prova_eixo_nao_cruza_linha_nem_coluna` | APROVADA |
| PN-0008 | pelo menos dois consoles focalizáveis; ambos renderizados simultaneamente; um focado | renderizar tela | qualquer console não focado exibe selecionado_simbolo | `prova_indicador_nao_aparece_em_console_nao_focado` | APROVADA |
| PN-0009 | console focado com um item | renderizar barra | [✥] aparece | `prova_chip_navegar_nao_aparece_com_um_item` | APROVADA |
| PN-0010 | item multilinha em modo verboso | renderizar console focado | símbolo indicador em linha de continuação | `prova_indicador_nao_aparece_em_linha_de_continuacao` | APROVADA |
| PN-0011 | cursor no item 2 | alternar modo | cursor posterior reinicia no item 0 | `prova_mudanca_modo_nao_reinicia_item_zero` | APROVADA |
| PN-0012 | cursor em item com grade larga | recalcular grade estreita | id do item lógico muda ou vira 0 | `prova_redimensionamento_nao_perde_identidade_logica` | APROVADA |
| PN-0013 | estado com item selecionado e contador de ações | processar Enter | ação registrada ou dispatcher chamado | `prova_enter_nao_executa_acao` | APROVADA |
| PN-0014 | página_atual observável antes da seta | quatro setas | página muda | `prova_setas_nao_mudam_pagina` | APROVADA |
| PN-0015 | estilo com símbolo X | renderizar cursor | aparece símbolo diferente do estilo | `prova_indicador_nao_hardcoded` | APROVADA |
| PN-0016 | mesmo console e largura | calcular navegação e renderizar | coordenadas de navegação divergem da grade visual | `prova_grade_navegacao_nao_diverge_grade_visual` | APROVADA |
| PN-0017 | estado com cursor | processar espaço | espaço altera seleção ou cria conjunto | `prova_space_nao_togla_inclusao` | APROVADA |

## 10. Auditoria específica de `PN-0005`

A prova `PN-0005` foi auditada detalhadamente e considerada correta:
- **Preparação:** Ao menos dois consoles focalizáveis; cursor do primeiro posicionado fora do item lógico `0`; o foco é alterado para o segundo console; o retorno ao primeiro console ocorre através das teclas Tab ou Shift+Tab.
- **Estímulo:** Tab ou Shift+Tab de volta ao primeiro console.
- **Observação:** O cursor do console focado após o reingresso.
- **Condição de falha:** O cursor anterior do console reentrado ser restaurado ao invés de reiniciar no item lógico `0`.
- **Comportamento esperado:**
```yaml
comportamento_esperado:
  cursor_apos_retorno: ITEM_LOGICO_0

condicao_de_falha:
  - cursor_anterior_restaurado
  - cursor_apos_retorno_diferente_de_0
```

## 11. Auditoria específica de `PN-0008`

A prova `PN-0008` foi auditada detalhadamente e considerada correta:
- **Preparação:** Ao menos dois consoles focalizáveis; ambos são renderizados simultaneamente na mesma tela; somente um console é marcado como focado; o estilo ativo possui um símbolo identificável (`selecionado_simbolo`).
- **Estímulo:** Renderizar a tela inteira.
- **Observação:** Presença ou ausência do símbolo do indicador em cada console.
- **Condição de falha:** Qualquer console não focado exibe o indicador (`selecionado_simbolo`).
- **Comportamento esperado:**
```yaml
console_focado:
  indicador: presente_no_item_corrente

consoles_nao_focados:
  indicador: ausente
```

## 12. Auditoria de `SPH40-002`

A validação manual foi totalmente revisada e não contém nenhuma das ocorrências proibidas (`comando do cenario`, `comando do cenário` ou `matriz completa`). Todos os roteiros manuais de teste (`VM-01` a `VM-11`) usam estritamente comandos de abertura reais, literais e completos, apontando diretamente para os JSONs reais de testes criados especificamente para a demonstração e preservando a separação exata de ações de teclado e redimensionamento.

## 13. Matriz da validação manual

| VM | Tela ou cenário | Comando literal | Tecla ou ação | Resultado visual | Executável nominalmente |
|---|---|---|---|---|---|
| VM-01 | dois consoles | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json` | Tab | Seta visual muda de quadro | Sim |
| VM-02 | dois consoles | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_dois_consoles.json` | Shift+Tab | Seta visual volta ao quadro anterior | Sim |
| VM-03 | matriz incompleta 2x3 | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json` | seta esquerda | Aponta item da mesma linha | Sim |
| VM-04 | matriz incompleta 2x3 | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json` | seta direita | Aponta item da mesma linha | Sim |
| VM-05 | matriz incompleta 2x3 | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json` | seta para cima | Aponta item da mesma coluna | Sim |
| VM-06 | matriz incompleta 2x3 | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_grade_2x3.json` | seta para baixo | Aponta item da mesma coluna | Sim |
| VM-07 | item multilinha | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json --verboso` | V | Mesmo item continua apontado | Sim |
| VM-08 | redimensionamento | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json` | maximizar janela | Mesmo item continua apontado | Sim |
| VM-09 | redimensionamento | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json` | restaurar janela | Mesmo item continua apontado | Sim |
| VM-10 | redimensionamento | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json` | reduzir janela | Mesmo item continua apontado | Sim |
| VM-11 | redimensionamento | `PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0040_nav_console_unico_linear.json` | redimensionar livremente | Mesmo item continua apontado e posição recalcula | Sim |

O H-0040 descreve formalmente as propriedades e definições da validação manual:
```yaml
validacao_manual:
  executante: USUARIO
  exclusiva_do_usuario: true
  executada_na_autoria_do_handoff: false
  executada_na_implementacao_automatica: false
  registro_posterior_previsto: true
```
A validação manual não instrui ou solicita que o usuário avalie índices internos de vetores, funções do código Python, estruturas de dados de memória ou nomes de símbolos internos da aplicação.

## 14. Auditoria de `SPH40-003`

A busca total pelo termo `HANDOFF_QA_APPROVED` resultou em 0 ocorrências ativas no H-0040. A aprovação foi descrita de forma estritamente canônica como um resultado de auditoria independente e externa, e não como uma conclusão antecipada ou presumida.

O H-0040 declara:
```yaml
resultado_possivel_apos_QA_independente:
  classificacao_de_aprovacao: H1_HANDOFF_APPROVED
  classificacao_nao_presumida_antes_do_QA: true
```

Não há declarações prévias e ativas de:
- `classificacao_esperada: H1_HANDOFF_APPROVED`
- `resultado_esperado: H1_HANDOFF_APPROVED`
- `handoff_aprovado`

## 15. Histórico do primeiro QA pós-patch

O H-0040 preservou adequadamente o histórico do primeiro QA pós-patch sem alteração semântica ou exclusão de registro, tratando-o unicamente como registro de progresso:
```yaml
qa_pos_primeiro_patch:
  relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
  resultado_literal: H1_HANDOFF_APPROVED
  aceite_gerencial: REJEITADO_POR_INCONSISTENCIA_MATERIAL
  motivos:
    - provas_negativas_ainda_incompletas
    - validacao_manual_com_comandos_nao_executaveis
    - taxonomia_nao_canonica_residual
```

## 16. Regressão dos achados anteriores

Não foram encontradas regressões materiais em relação aos achados de QAs passados:
- **QAH40-001 (13 arquivos novos canônicos):** A lista canônica unificada de 13 arquivos foi integralmente mantida de forma inequívoca (Seção 8 do H-0040).
- **QAH40-002 (suíte canônica):** Os comandos canônicos permanecem idênticos e o caráter puramente de referência para a contagem 423 de testes foi mantido.
- **QAH40-003 (relatório futuro):** O template e caminho do relatório de implementação futuro estão perfeitamente conservados.
- **QAH40-004 (40 AT e 17 PN):** A quantidade numérica e sua coerência com as decisões D1-D15 permanecem conservadas e preservadas de forma exata.
- **QAH40-005 (demonstração fechada e Enter preservado):** O roteiro de demonstração na Seção 22 continua com os comandos e cenários fechados de forma unívoca, mantendo a tecla Enter sem atribuição de comportamento interativo.
- **QAH40-006 (validação manual):** O roteiroVM-01 a VM-11 continua exclusivo do usuário e em linguagem não-técnica.
- **QAH40-007 (regra de exceção):** A regra operacional de parada antes de alterar arquivos fora da lista fechada permanece descrita de forma integral.
- **QAH40-008 (NC delimitados):** Os pontos NC continuam cobertos de forma adequada e classificados em correspondência com as diretrizes do QA inicial.

## 17. Arquivos autorizados

Os limites materiais de modificação e de criação de arquivos permanecem estritamente preservados e imutáveis nas seções do H-0040:
```yaml
arquivos_modificaveis:
  total: 2
  lista:
    - demo/demo.py
    - tela/renderizador.py

arquivos_novos:
  total: 13
```

A reorganização das provas negativas e dos roteiros manuais de teste preservou a integridade das listas de arquivos do H-0040.

## 18. Suíte canônica

O H-0040 declara e preserva a suíte canônica de testes de regressão automatizados:
```yaml
suite_canonica:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
  comando_coleta: PYTHONDONTWRITEBYTECODE=1 python -m pytest --collect-only -q
```
A contagem de 423 testes é tratada estritamente como uma fotografia de coleta no momento da autoria, permitindo o crescimento da suíte de testes de forma livre e natural após a implementação das decisões.

## 19. Relatório futuro

O template do relatório futuro de implementação, destinado à documentação da implementação de H-0040, encontra-se documentado na Seção 24 e encerra-se com o marcador de fim:
```text
IMPLEMENTATION_COMPLETED_AWAITING_QA
```
O relatório futuro não antecipa a própria aprovação.

## 20. Regra de exceção

A regra de exceção para arquivos fora da lista fechada permanece definida e descrita de forma estrita na Seção 11 de H-0040:
```yaml
arquivo_fora_da_lista:
  acao: PARAR_ANTES_DA_ALTERACAO
  aguardar_autorizacao_do_usuario: true
  alteracao_sem_autorizacao: proibida
```

## 21. Matriz dos três achados

| Achado | Resultado | Evidência |
|---|---|---|
| SPH40-001 | CORRIGIDO | Seção 20 do H-0040 reorganizou e consolidou as 17 PN canônicas materialmente suficientes e detectáveis, em correspondência inequívoca com as decisões D1-D15. |
| SPH40-002 | CORRIGIDO | Seção 23 do H-0040 substituiu todas as referências inespecíficas por comandos literais de execução exata para os cenários VM-01 a VM-11, cobrando todos os comportamentos de teclado e redimensionamento e não havendo ocorrências ativas dos termos proibidos. |
| SPH40-003 | CORRIGIDO | Seção 36 do H-0040 utiliza taxonomia canônica, apresentando H1_HANDOFF_APPROVED como resultado possível do QA independente e eliminando todas as menções prévias e ativas de aprovação presumida como `HANDOFF_QA_APPROVED`. |

## 22. Novos achados

```yaml
novos_achados: []
```

Nenhum novo defeito, lacuna técnica ou contradição estrutural foi introduzido pelas modificações deste segundo patch. O artefato documental está consistente e robusto.

## 23. Classificação final

A classificação final do processo é:
```yaml
classificacao: H1_HANDOFF_APPROVED
```
O handoff foi aprovado materialmente. A implementação do H-0040 está liberada para começar.

## 24. Arquivos criados pelo QA

```text
docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md
```

## 25. Estado Git final

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
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - docs/relatorios/RELATORIO_SEGUNDO_PATCH_H-0040_HANDOFF.md
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/teste_distribuicao_matricial.cpython-314-pytest-9.0.3.pyc
```

## 26. Encerramento

H1_HANDOFF_APPROVED