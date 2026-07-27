# Relatorio de QA do Patch de Handoff H-0040

## 1. Identificacao

```yaml
etapa: QA_PATCH_HANDOFF_H0040
handoff: H-0040
adr: ADR-0031
data: 2026-07-26
relatorio_criado: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0040.md
```

## 2. Objeto

Auditar o patch documental aplicado em `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`, sem implementar, sem alterar o handoff, sem validacao manual e sem operacoes Git de escrita.

## 3. Estado processual

```yaml
ultima_linha_do_handoff: HANDOFF_PATCHED_AWAITING_QA
estado_esperado_confirmado: true
validacao_manual:
  VM_01_a_VM_10: APROVADOS
  VM_11: FALHOU
  resultado_global: FALHOU_PATCH_NECESSARIO
nova_ADR:
  necessaria: false
implementacao:
  executada_apos_patch_do_handoff: false
observacao:
  campos_equivalentes_no_handoff:
    - validacao_manual_consolidada
    - decisao_pos_validacao_manual.nova_ADR: nao
    - patch_handoff_VM11.implementacao_executada_neste_patch: false
```

## 4. Estado Git

```yaml
arquivos_staged: []
worktree_acumulado_bloqueia_QA: false
operacoes_git_de_escrita_executadas: []
commit_executado: nao
observacao: >
  O worktree atual contem arquivos modificados e nao rastreados historicos do ciclo.
  A auditoria nao atribui esses arquivos ao terceiro patch do handoff.
```

## 5. Gate

```yaml
relatorio_existia_antes: false
handoff_status: HANDOFF_PATCHED_AWAITING_QA
autoridades_lidas: true
validacao_manual_executada_pelo_QA: nao
implementacao_executada_pelo_QA: nao
gate_resultado: REPROVADO
classificacao: H2_HANDOFF_PATCH_REQUIRED
```

## 6. Autoridades

Lidos integralmente:

- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`
- `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`
- `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0040.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_POS_VALIDACAO_MANUAL_H-0040.md`

Lidos seletivamente para campos vigentes de distribuicao matricial:

- `docs/nomenclatura/41_DISTRIBUICAO_MATRICIAL.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_tela_json.md`
- `tela/loader.py`
- `tela/distribuicao_matricial.py`

## 7. Delta do patch

```yaml
delta_do_patch:
  arquivo_esperado:
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  arquivos_confirmados:
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  arquivos_fora_da_lista: []
  base_da_confirmacao:
    - handoff_secao_37_declara_limite_material_do_terceiro_patch
    - git_staged_vazio
```

## 8. Novo cenario

```yaml
novo_cenario:
  arquivo: config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  autorizado_nominalmente: true
  itens:
    quantidade: 26
    ids: item_01_a_item_26
    tamanho_das_palavras:
      minimo: 4
      maximo: 10
    variacao_de_tamanho: true
  matriz:
    formacao: automatica_por_preferencia_linhas
    ordem: por_linha
    linhas_minimas: 1
    linhas_maximas: 26
    colunas_minimas: 1
    colunas_maximas: 26
  espacamento:
    margem_superior: 1
    entre_linhas: 1
    entre_colunas:
      minimo: 2
      dinamico: true
  distribuicao_horizontal:
    uniforme: true
    recalculada_com_a_largura: true
  runtime_no_JSON_autorizado: false
  ressalva_bloqueante: distribuicao_horizontal.politica_permanece_com_placeholder_a_definir
```

## 9. Capacidade documental

```yaml
capacidade_documental:
  formacao_matricial_automatica: EQUIVALENTE_CANONICO
  preferencia_horizontal: EQUIVALENTE_CANONICO
  minimo_e_maximo_de_linhas: VIGENTE
  minimo_e_maximo_de_colunas: VIGENTE
  margem_superior: VIGENTE
  espacamento_entre_linhas: EQUIVALENTE_CANONICO
  espacamento_entre_colunas: EQUIVALENTE_CANONICO
  distribuicao_horizontal_uniforme: VIGENTE
  dimensionamento_pelo_maior_elemento_da_linha_ou_coluna: VIGENTE
  alinhamento_dentro_da_celula: VIGENTE
  capacidades_nao_suportadas: []
  contradicoes:
    - distribuicao_horizontal_uniforme_descrita_sem_valor_canonico_no_bloco_JSON
```

O valor canonico `distribuicao_horizontal.politica: uniforme` esta vigente no loader e nos contratos. O handoff, contudo, deixa o bloco normativo do JSON com `a_definir_pela_implementacao_conforme_NC-007`.

## 10. Formacoes

```yaml
formacoes:
  extremos:
    "1x26": definido
    "26x1": definido
  intermediarias:
    obrigatorias: true
    exemplos_confirmados:
      - "2x13"
      - "4x7"
      - "7x4"
      - "13x2"
  dimensoes_hardcoded: false
  dependem_do_espaco_disponivel: true
  matriz_incompleta_permitida: true
  todos_os_26_itens_presentes: true
  ordem_semantica_por_linha_preservada: true
```

## 11. Recalculo da navegacao

```yaml
recalculo_apos_redimensionamento:
  preservar:
    - item_logico
    - console_focado
    - pagina_atual
    - modo_atual
  descartar:
    - formacao_anterior
    - linha_anterior
    - coluna_anterior
    - vizinhos_anteriores
    - largura_anterior
    - altura_anterior
  recalcular:
    - formacao_atual
    - linha
    - coluna
    - esquerda
    - direita
    - cima
    - baixo
    - toroide
  primeira_seta_usa_nova_formacao: true
  exige_Tab_troca_console_ou_reinicio: false
```

## 12. Distribuicao espacial

```yaml
espacamento_vertical:
  linha_fisica_vazia_entre_linhas_da_matriz: true
  proibicoes_confirmadas:
    - itens_ficticios
    - textos_vazios
    - celulas_falsas
    - quebras_artificiais_no_conteudo
    - inflacao_desnecessaria_da_altura_de_todos_os_itens

espacamento_horizontal:
  intervalo_minimo_entre_colunas: true
  intervalo_cresce_quando_janela_aumenta: true
  intervalo_diminui_quando_janela_reduz: true
  colunas_usam_espaco_disponivel: true
  nenhuma_palavra_sobreposta: true
  nenhuma_palavra_dividida_sem_necessidade: true
```

## 13. Arquivos autorizados

```yaml
arquivos_autorizados_nominalmente:
  confirmados:
    - demo/demo.py
    - demo/demo_navegacao.py
    - demo/teste_demo_navegacao.py
    - tela/navegacao.py
    - tela/renderizador.py
    - tela/distribuicao_matricial.py
    - tela/teste_navegacao.py
    - tela/teste_renderizador.py
    - tela/teste_distribuicao_matricial.py
    - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
    - config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  nao_confirmados_como_autorizacao_material_clara:
    - docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md
  lista_nao_obriga_alteracao_de_todos_os_arquivos: true
  alteracao_somente_quando_materialmente_necessaria: true
  implementacao_por_nome_da_fixture: proibida
  solucao_generica_dirigida_por_JSON: obrigatoria
```

O relatorio `RELATORIO_PATCH_VM-11_H-0040.md` e citado nominalmente na Secao 8 como "autorizado na Secao 33", mas a Secao 33 nao o autoriza materialmente.

## 14. AT e PN

```yaml
AT:
  total_declarado: 40
  menor: AT-0001
  maior: AT-0040
  lacunas_observadas: 0
  duplicatas_observadas: 0
PN:
  total_declarado: 17
  menor: PN-0001
  maior: PN-0017
  lacunas_observadas: 0
  duplicatas_observadas: 0
auditoria_focal:
  AT-0031: cobre_JSON_26_itens_multiplas_formacoes_extremos_preservacao_item
  AT-0032: cobre_primeira_seta_vizinhos_toroide_formacao_atual
  PN-0012: cobre_identidade_logica_e_primeira_seta_pos_redimensionamento
  PN-0016: cobre_renderer_vs_navegacao_espacamento_sobreposicao_linha_em_branco
```

## 15. VM-11

```yaml
VM_11:
  roteiro_substituido: true
  usa_novo_JSON: true
  acompanha_item_distante_do_primeiro: true
  passa_por_varias_formacoes: true
  busca_menor_quantidade_de_linhas: true
  busca_menor_quantidade_de_colunas: true
  testa_quatro_setas: true
  verifica_primeira_seta_apos_cada_redimensionamento: true
  verifica_toroide: true
  verifica_linha_vazia_entre_linhas_da_matriz: true
  verifica_distribuicao_horizontal_uniforme: true
  verifica_ausencia_de_sobreposicao: true
  verifica_ausencia_de_indicador_em_celula_vazia: true
  repeticao_futura_exclusiva: true
VM_01_a_VM_10:
  permanecem_aprovados: true
```

## 16. Contagens

```yaml
contagens:
  cenarios:
    declarado_em_checks: 9
    lista_canonica_de_JSONs: 9
    linhas_na_tabela_de_demonstracao: 10
    reconciliado: false
  AT:
    declarado: 40
    secoes_AT_0001_a_AT_0040: 40
    reconciliado: true
  PN:
    declarado: 17
    secoes_PN_0001_a_PN_0017: 17
    reconciliado: true
lista_nominal_dos_nove_cenarios:
  - h0040_nav_console_unico_linear.json
  - h0040_nav_dois_consoles.json
  - h0040_nav_tres_consoles_em_grupo.json
  - h0040_nav_console_grade_2x3.json
  - h0040_nav_console_nao_focalizavel.json
  - h0040_nav_degenere_um_item.json
  - h0040_nav_degenere_uma_linha.json
  - h0040_nav_degenere_uma_coluna.json
  - h0040_nav_matriz_26_itens_redimensionamento.json
```

## 17. Escopo negativo

```yaml
fora_do_escopo_confirmado:
  - paginacao_interativa
  - selecao_multipla
  - acoes_por_Enter
  - registry_de_acoes
  - multinivel_colapsavel
  - foco_de_dashboard
  - navegacao_entre_paginas
  - estado_de_runtime_persistido_no_JSON
  - alteracao_nao_relacionada_das_decisoes_D1_D15
```

## 18. Exequibilidade

```yaml
exequibilidade:
  objetivo_claro: true
  arquivos_autorizados_suficientes: false
  criterios_testaveis: true
  roteiro_manual_executavel: true
  nomes_canonicos_reconciliados: false
  decisoes_de_produto_pendentes: false
```

## 19. Achados

```yaml
achado:
  id: QAH40P-001
  severidade: BLOQUEANTE
  arquivo: docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  secao: "33. Cenario matricial de 26 itens"
  evidencia: "distribuicao_horizontal: {politica: a_definir_pela_implementacao_conforme_NC-007}"
  comportamento_encontrado: >
    O bloco normativo do JSON deixa a politica horizontal a definir pela implementacao.
  comportamento_esperado: >
    O handoff deve usar nome canonico vigente ou declarar uma semantica sem campo pendente.
    O valor canonico uniforme ja existe em contrato e loader.
  correcao_necessaria: >
    Reconciliar o campo com valor canonico vigente, sem etapa adicional de definicao.
```

```yaml
achado:
  id: QAH40P-002
  severidade: MAIOR
  arquivo: docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  secao: "22. Demonstracao fechada / 35. Checks mecanicos esperados"
  evidencia: "Secao 22 lista 10 linhas de demonstracao; Secao 35 declara demonstracao.cenarios: 9."
  comportamento_encontrado: >
    A contagem de cenarios nao reconcilia com a tabela de demonstracao fechada.
  comportamento_esperado: >
    Todas as ocorrencias de cenarios: 9 devem reconciliar com lista nominal unica de nove cenarios.
  correcao_necessaria: >
    Remover, fundir ou reclassificar a linha excedente, preservando a lista nominal correta.
```

```yaml
achado:
  id: QAH40P-003
  severidade: MAIOR
  arquivo: docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  secao: "8. Lista canonica dos 14 arquivos novos / 26. Riscos e mecanismos / 29. Estado Git esperado apos implementacao"
  evidencia: >
    Secao 8 declara arquivos_novos.total: 14; Secao 35 declara total_nominal: 14;
    Secao 29 ainda declara arquivos_novos_autorizados: 13; Secao 26 cita lista canonica de 13.
  comportamento_encontrado: >
    Permanecem contagens antigas de arquivos novos depois da inclusao do novo JSON de 26 itens.
  comportamento_esperado: >
    As contagens de arquivos novos/autorizados devem ser unicas e consistentes.
  correcao_necessaria: >
    Atualizar as referencias residuais de 13 para a contagem reconciliada ou explicar formalmente a diferenca.
```

```yaml
achado:
  id: QAH40P-004
  severidade: MAIOR
  arquivo: docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  secao: "8. Lista canonica dos 14 arquivos novos / 33. Cenario matricial de 26 itens"
  evidencia: >
    Secao 8 afirma que docs/relatorios/RELATORIO_PATCH_VM-11_H-0040.md esta autorizado na Secao 33,
    mas a Secao 33 nao contem essa autorizacao material.
  comportamento_encontrado: >
    O arquivo e citado nominalmente, mas a autoridade apontada nao confirma permissao clara de criacao/alteracao.
  comportamento_esperado: >
    Arquivos futuros autorizados devem constar nominalmente na lista aplicavel ou em secao propria sem remissao falsa.
  correcao_necessaria: >
    Autorizar materialmente o relatorio de patch VM-11 na secao correta ou remover a afirmacao.
```

## 20. Classificacao

```yaml
classificacao: H2_HANDOFF_PATCH_REQUIRED
justificativa:
  achados_bloqueantes: 1
  achados_maiores: 3
  achados_menores: 0
  notas: 0
```

## 21. Efeito do QA

```yaml
efeito_do_QA:
  arquivos_preexistentes_alterados: []
  arquivos_criados:
    - docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0040.md
  implementacao_executada: nao
  validacao_manual_executada: nao
  operacoes_git_de_escrita: []
  commit_executado: nao
```

## 22. Encerramento

H2_HANDOFF_PATCH_REQUIRED
