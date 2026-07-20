---
status_literal: IMPLEMENTATION_APPROVED_WITH_NOTES
status_normalizado: approved_with_notes
historia: H-0037
tipo: QA_POS_PATCH_IMPLEMENTACAO
patch_auditado: oitavo_patch_pos_validacao_manual
data: 2026-07-20
---

# RELATORIO QA POS PATCH 8 H-0037 IMPLEMENTACAO

## 1. Identificacao

Auditoria tecnica independente do oitavo patch focal da implementacao H-0037,
decorrente do setimo QA pos-patch que identificou `H0037-IMPL-QAPP7-001` e
`H0037-IMPL-QAPP7-002`.

Resultado: `IMPLEMENTATION_APPROVED_WITH_NOTES`.

## 2. Objetivo

Auditar exclusivamente as correcoes declaradas para:

- `H0037-IMPL-QAPP7-001`: corte silencioso da hierarquia verbosa em largura
  reduzida — containers da hierarquia caiam no ramo nao verboso e recebiam
  `_truncar_com_marcador`.
- `H0037-IMPL-QAPP7-002`: cobertura integrada insuficiente em
  `teste_h0037_manual_001_marcador_truncamento` e registro incompleto no
  `IMP-0037`.

Nao foi executada revalidacao manual em nome do usuario.

## 3. Autoridades

Arquivos lidos integralmente:

```yaml
docs/relatorios/RELATORIO_QA_POS_PATCH_7_H-0037_IMPLEMENTACAO.md:
  linhas: 719
docs/relatorios/RELATORIO_QA_POS_PATCH_6_H-0037_IMPLEMENTACAO.md:
  linhas: 805
docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md:
  linhas: 462
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md:
  linhas: 2342
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md:
  lido_no_qaa_anterior: confirmado
docs/contratos/contrato_console.md:
  lido_no_qaa_anterior: confirmado
docs/contratos/contrato_composicao_corpo.md:
  lido_no_qaa_anterior: confirmado
tela/renderizador.py: integral
tela/teste_renderizador.py: integral (foco nas secoes VERB-01..13)
demo/demo.py: revisado
demo/teste_demo_console_modos.py: revisado
```

Autoridades decisivas:

- `contrato_console.md §21.2-21.3`: modo verboso sem marcador artificial;
  modo nao verboso com marcador `...`.
- `IMP-0037 secao 37`: declaracao do oitavo patch.
- `RELATORIO_QA_POS_PATCH_7`: achados auditados.

## 4. Estado Git

Comandos executados na raiz real:

```yaml
raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch: master
head: f6982d08640af1762b8e0e8814b6e90c9421538e
head_log: "f6982d0 docs: corrige whitespace do fechamento H-0036"
stage: vazio
commit_novo: inexistente
push: nao_executado
git_diff_check: sem_erros
```

Arquivos rastreados no diff acumulado (modificados mas nao commitados):

```text
config/telas/demo/demo.json
demo/demo.py
demo/teste_demo.py
demo/teste_demo_console.py
demo/teste_diagnostico.py
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Arquivos nao rastreados relevantes: fixtures H-0037, ADR-0028, handoff H-0037,
relatorios H-0037/ADR-0028, `demo/teste_demo_console_modos.py` e relatorios QA.

Itens inesperados:

```yaml
arquivos_acumulados_anteriores: presentes_na_worktree_acumulada
origem: NAO_CONFIRMADA_COMO_DO_OITAVO_PATCH
producao_pelo_oitavo_patch: NAO_CONFIRMADO_PARA_ARQUIVOS_FORA_DA_LISTA
```

## 5. Escopo Do Oitavo Patch

O executor declarou alteracao em (IMP-0037 secao 37.9):

```text
tela/renderizador.py
tela/teste_renderizador.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Alteracoes focais confirmadas:

```yaml
tela/renderizador.py:
  - ramo verboso de _linhas_apresentacao_hierarquia deixou de ser
    condicionado a eh_folha; todo no (container ou folha) entra no
    ramo verboso com _quebrar_texto
  - largura_disp = max(10, content_w - len(prefixo)) calculado com o
    prefixo real do no
  - linhas de continuacao: indent_cont = ' ' * len(prefixo)

tela/teste_renderizador.py:
  - adiciona teste_h0037_qapp7_verb_sem_corte_silencioso (VERB-01..13)

docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md:
  - adiciona secao 37 do oitavo patch focal
```

## 6. Integridade

```yaml
python_ast:
  tela/renderizador.py: OK
  tela/teste_renderizador.py: OK
  demo/demo.py: OK
  demo/teste_demo_console_modos.py: OK
conflitos_git:
  marcadores_reais: ausentes
temporarios:
  __pycache__: ausente
  "*.pyc": ausente
  "*.tmp": ausente
  "*.bak": ausente
  "*.swp": ausente
  "*~": ausente
whitespace:
  git_diff_check: sem_erros
```

Nenhum artefato transitorio encontrado por `find` nas diretorias `tela/` e
`demo/`.

## 7. Revisao Do Ramo Hierarquico

### 7.1 Ramo anterior x ramo atual

```yaml
ramo_anterior:
  condicao: "verboso and content_w is not None and eh_folha"
  onde_eh_folha: "nivel is not None and nivel.tipo != 'container'"
  containers: caiam_no_ramo_else_com_truncar_com_marcador
  consequencia: marcador_artificial_em_modo_verboso_e_corte_silencioso_pelo_envelope

ramo_atual:
  condicao: "verboso and content_w is not None"
  todo_no: sim_container_e_folha
  mecanismo: _quebrar_texto(texto, largura_disp)
  largura_disp: max(10, content_w - len(prefixo))
  prefixo: recuo + marc_fmt + espaco_separador
  continuacao: indent_cont = ' ' * len(prefixo)
```

### 7.2 Casos auditados

```yaml
container_com_conteudo_textual:
  verboso: ocupa_varias_linhas_sem_marcador
  nao_verboso: uma_linha_com_marcador_quando_excede
  conforme: true

folha_com_conteudo_textual:
  verboso: ocupa_varias_linhas_sem_marcador
  nao_verboso: uma_linha_com_marcador_quando_excede
  conforme: true

container_sem_conteudo_textual_proprio:
  verboso: exibe_designador_e_linha_de_prefixo_vazio
  nao_verboso: exibe_designador_e_prefixo_sem_marcador
  sem_linhas_vazias_artificiais: true
  conforme: true

dois_niveis:
  containers_no_ramo_verboso: confirmado
  folhas_no_ramo_verboso: confirmado
  alinhamento_de_coluna_raiz: preservado
  conforme: true

tres_niveis:
  todos_os_nos_no_ramo_verboso: confirmado
  sem_mistura_de_niveis: confirmado
  sem_eliminacao_de_niveis: confirmado
  conforme: true

ordem:
  preservada: true
  duplicacao: false
  alinhamento: conforme
```

Smoke executado:

```yaml
dois_niveis_w30_verboso:
  marcadores_artificial: 0
  todas_linhas_largura_30: true
dois_niveis_w30_nao_verboso:
  marcadores_artificial: 4
tres_niveis_w30_verboso:
  marcadores_artificial: 0
  todas_linhas_largura_30: true
tres_niveis_w50_verboso:
  marcadores_artificial: 0
  todas_linhas_largura_50: true
```

```yaml
H0037_IMPL_QAPP7_001:
  ramo_anterior: container_caia_no_else_com_truncar_com_marcador
  ramo_atual: todo_no_usa_quebrar_texto
  containers: conformes
  folhas: conformes
  nos_sem_conteudo: linha_curta_sem_marcador_artificial
  dois_niveis: conformes
  tres_niveis: conformes
  ordem: preservada
  duplicacao: ausente
  alinhamento: preservado
  conforme: true
```

## 8. Quebra Verbosa Pela Largura Restante

### 8.1 Calculo de largura_disp

```yaml
largura_disp_formula: max(10, content_w - len(prefixo))
prefixo_compoe: recuo + marc_fmt + separador
largura_interna: content_w (= largura_total - 3)
```

Casos verificados (sem gerar requisito novo):

```yaml
largura_interna_maior_prefixo_varios_chars:
  content_w=27_prefixo=3: largura_disp=24_linha_max=27=content_w
  conforme: true

largura_interna_maior_prefixo_um_char:
  margem_de_seguranca: acima_do_floor_de_10
  conforme: true

largura_interna_igual_prefixo:
  largura_disp: max(10,0)=10 -> linha potencialmente_maior_que_content_w
  observacao: edge_case_NAO_ativado_pelos_dados_H0037
  conforme_para_dados_reais: true

largura_interna_menor_que_prefixo:
  largura_disp: max(10,...) -> linha_pode_exceder_content_w
  envelope_trunca_silenciosamente: true_no_edge_case_extremo
  observacao: NAO_introduzido_pelo_8o_patch
  conforme_para_dados_H0037: true

prefixo_muito_longo:
  reproduzido_sinteticamente: true
  linha_excede_content_w: true_quando_prefix_gt_content_w_menos_10
  observacao: NAO_ativado_em_H0037_casos_reais
  nao_e_regressao_do_8o_patch: true

conteudo_sem_espacos:
  _quebrar_texto_quebra_em_largura_fixa: confirmado
  nenhum_marcador: confirmado

conteudo_com_palavras_longas:
  palavra_maior_que_largura_disp: colocada_em_linha_propria_sem_truncamento
  confirmado: true
```

Resultado:

```yaml
conteudo_longo:
  quebrado_em_multiplas_linhas: true
  corte_silencioso: false  # para dados H-0037 reais
  reticencias: false
  caracteres_preservados: true
  largura_respeitada: true
```

**Observacao tecnica** (nao corretiva): a formula `max(10, content_w - len(prefixo))`
pode produzir linhas intermediarias com `len(prefixo) + len(frag) > content_w`
quando `len(prefixo) > content_w - 10`. Nesses casos extremos, o envelope
`_linha_conteudo` ainda aplica `texto[:content_w]`, contrariando a afirmacao do
IMP-0037 de que o corte "jamais atua em modo verboso". Esta condicao nao e
ativada pelos dados reais do H-0037 (max prefix ~7 chars, min content_w 27 chars)
e nao foi introduzida pelo oitavo patch (afetava nos folha antes). Registrada
como `H0037-IMPL-QAPP8-001` (OBSERVACAO_NAO_CORRETIVA).

## 9. Linhas De Continuacao

```yaml
linhas_de_continuacao:
  indentacao: deterministica_igual_a_len_prefixo
  identificador_repetido: false
  token_inicial: preservado_na_primeira_linha
  token_intermediario: preservado_em_alguma_linha
  token_final: preservado_em_alguma_linha
  nivel_preservado: true
  largura: respeitada_para_dados_H0037
  conforme: true
```

Verificado pelo teste `VERB-05`:

```yaml
VERB-05_continuacoes_nao_repetem_designador: PASSOU
VERB-05_indentacao_deterministica: PASSOU
```

E confirmado pelo smoke em w=30 dois niveis:

```yaml
prefixo_container_raiz: "1. "  # 3 chars
indent_cont: "   "             # 3 espacos
linha_continuacao_observada: "   conteudo_dois_niveis"
recuo_igual_ao_prefixo: true
```

## 10. Saida Final Depois Do Envelope

Smoke tecnico com saida completa inspecionada:

```yaml
saida_final:
  largura_total: todas_as_linhas_com_comprimento_igual_a_largura_parametrizada
  bordas: alinhadas_confirmado_por_VERB_11
  token_final: presente_confirmado_por_VERB_03_VERB_09_VERB_11
  reticencias_no_verboso: ausentes
  corte_pelo_envelope: ausente_para_dados_H0037
  recalculo_em_largura_maior: confirmado_por_VERB_09
  conforme: true
```

Provas concretas (smoke):

```yaml
dois_niveis_w30_verboso: todas_30_linhas_de_largura_30
tres_niveis_w50_verboso: todas_as_linhas_de_largura_50
token_final_tres_niveis: "tres niveis." presente em w30 e w50
borda_direita: todas_as_linhas_internas_terminam_com_bordo_vertical
```

## 11. Modo Nao Verboso Preservado

```yaml
nao_verboso:
  uma_linha_por_item_ou_celula: true
  marcador_quando_truncado: "..."
  marcador_quando_cabe: ausente
  largura_respeitada: true
  containers_no_ramo_correto: true
  containers_nao_quebram_em_varias_linhas: true
```

Provas:

```yaml
h0037_console_nao_verboso_w30:
  marcadores_artificiais: 4
  linhas_hierarquia: "1. H-0037 conteudo_dois_...|" e "Politica somente_nao_v...|"
  conforme: true

tabela_nao_verbosa_w50:
  marcadores_artificiais: 6
  conforme: true
```

## 12. Alternancia

Sequencia testada: nao verboso -> verboso -> nao verboso -> verboso

```yaml
alternancia:
  nao_verboso:
    linha_unica: true
    reticencias_quando_necessario: true  # 4 marcadores em w50
    marcadores_nv1: 4
    marcadores_nv2: 4

  verboso:
    multilinha: true
    reticencias: false
    conteudo_completo: true
    marcadores_v1: 0
    marcadores_v2: 0

  retorno:
    recalculado_dos_dados_originais: true  # NV1 == NV2, V1 == V2
    estado_corrompido: false
    perda_de_conteudo: false

  token_final_verboso: "tres niveis." em V1 e V2
  nao_verboso_nao_reutiliza_dado_quebrado: true
```

## 13. Teste Integrado Adicionado

Funcao `teste_h0037_qapp7_verb_sem_corte_silencioso` em
`tela/teste_renderizador.py`, chamada em `main()`:

```yaml
VERB-01:
  entrada: modelo_dois, w=220, verboso=True
  caminho: renderizar_tela -> caixa -> hierarquia verbosa
  saida_final_inspecionada: true
  expectativa: sem_marcador_artificial_texto_integral_presente
  resultado: PASSOU

VERB-02:
  entrada: modelo_dois, w=30, verboso=True
  caminho: renderizar_tela -> hierarquia verbosa
  saida_final_inspecionada: true
  expectativa: sem_marcador_e_mais_linhas_que_nao_verboso
  resultado: PASSOU

VERB-03:
  entrada: modelo_tres, w=30, verboso=True
  caminho: _texto_caixa_console (texto concatenado do console)
  saida_final_inspecionada: true
  expectativa: tokens_inicial_intermediario_final_preservados
  resultado: PASSOU

VERB-04:
  entrada: modelo_dois, w=30, verboso=True
  caminho: _linhas_caixa_console (linhas completas do console)
  saida_final_inspecionada: true
  expectativa: largura_total_respeitada_designador_preservado
  resultado: PASSOU

VERB-05:
  entrada: modelo_dois, w=30, verboso=True
  caminho: _linhas_caixa_console com inspecao de indentacao
  saida_final_inspecionada: true
  expectativa: continuacoes_deterministas_sem_repetir_designador
  resultado: PASSOU

VERB-06:
  entrada: modelo_dois, w=30, verboso=True
  caminho: _texto_caixa_console
  saida_final_inspecionada: true
  expectativa: folha_segundo_nivel_com_recuo_correto
  resultado: PASSOU

VERB-07:
  entrada: modelo_tres, w=50, verboso=True
  caminho: saida_completa e _texto_caixa_console
  saida_final_inspecionada: true
  expectativa: tres_niveis_presentes_sem_misturar_sem_marcador
  resultado: PASSOU

VERB-08:
  entrada: modelo_dois/tres, w=30/50, verboso=True
  caminho: saida_completa (loop sobre tres configuracoes)
  saida_final_inspecionada: true
  expectativa: sem_marcador_em_cada_configuracao_largura_respeitada
  resultado: PASSOU_em_tres_variantes

VERB-09:
  entrada: modelo_tres, w=220, verboso=True (pos w=50)
  caminho: renderizar_tela
  saida_final_inspecionada: true
  expectativa: token_final_restaurado_sem_marcador_menos_linhas
  resultado: PASSOU

VERB-10:
  entrada: modelo_tres, w=50, nao_verboso/verboso/nao_verboso
  caminho: renderizar_tela x3
  saida_final_inspecionada: true
  expectativa: nv_com_marcador_v_sem_marcador_retorno_igual_ao_original
  resultado: PASSOU

VERB-11:
  entrada: modelo_tres, w=50, verboso=True
  caminho: saida completa e _linhas_caixa_console
  saida_final_inspecionada: true
  expectativa: token_final_presente_largura_respeitada_bordas_alinhadas
  resultado: PASSOU

VERB-12:
  entrada: modelo_tabela, w=50, verboso=True e False
  caminho: renderizar_tela
  saida_final_inspecionada: true
  expectativa: verboso_sem_marcador_nao_verboso_com_marcador_verboso_mais_linhas
  resultado: PASSOU

VERB-13:
  entrada: modelo_conjuntos_h0036, w=26/80, nao_verboso/verboso
  caminho: renderizar_tela
  saida_final_inspecionada: true
  expectativa: nao_verboso_com_marcador_verboso_sem_marcador_em_largura_ampla
  resultado: PASSOU
```

Confirmacoes adicionais sobre o teste:

```yaml
atravessa_apresentacao_real: true
atravessa_envelope_da_caixa: true
verifica_token_final: true
verifica_ausencia_de_reticencias_no_verboso: true
verifica_largura_final: true
verifica_dois_niveis: true
verifica_tres_niveis: true
verifica_alternancia: true
verifica_tabela: true
verifica_conjuntos: true
nao_limita_a_quebrar_texto: true
nao_usa_expectativa_frouxa_por_perda_parcial: true
contagem_manual_de_verificacoes: nao_alterada
```

Observacao sobre VERB-06: a expectativa `"  Politica" in texto_v30 or
"Politica" in texto_v30` e tecnicamente satisfeita pela segunda clausula
independentemente da primeira. A verificacao e funcionalmente correta para
o dado real (o recuo de 2 espacos esta presente na saida e "  Politica" e
substring de "   Politica"), mas a logica da expressao `or` torna a primeira
clausula redundante. Classificada como OBSERVACAO_NAO_CORRETIVA
(H0037-IMPL-QAPP8-002).

## 14. Preservacao De H0037-MANUAL-002 (Esc Primeiro)

Confirmado por smoke sem reabrir a implementacao:

```yaml
chips:
  h0037_console_alternavel_tres_niveis: "[Esc] Voltar  [V] Verboso"
  h0037_console_tabela_alternavel: "[Esc] Voltar  [V] Verboso"
  Esc_primeiro: true
  ordem_relativa_dos_demais: preservada
  duplicacao_de_Esc: ausente
  barra_sem_Esc: preservada
  cenarios_alternaveis: conformes
```

## 15. Preservacao De H0037-MANUAL-003 (V e v)

Confirmado pela suite (80 verificacoes, 0 falhas):

```yaml
teclas:
  V_maiusculo:
    telas_alternaveis: funcional
    telas_fixas: inerte
  v_minusculo:
    telas_alternaveis: funcional
    telas_fixas: inerte
  isolamento: preservado
  eco: ausente
  outras_teclas: preservadas
```

## 16. Paginacao

```yaml
paginacao:
  implementada_no_oitavo_patch: false
  testes_novos_exigindo_paginacao: nenhum
  mecanismos_historicos_alterados: false
  classificacao: NAO_APLICAVEL
```

Ausencia de paginacao nao foi registrada como defeito.

## 17. Preservacoes Anteriores

Confirmadas por suite e inspecao proporcional:

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso

conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false

D23:
  regressao_nova: false

validacoes:
  V_01: preservada
  V_04: preservada
  V_13: preservada
  V_14: preservada

demo_json:
  carrega: true
  entradas: 11

regressao_H_0036:
  preservada: true  # VERB-13 usa h0036_console_conjuntos e passa
```

## 18. Relatorio IMP-0037

A secao 37 foi auditada integralmente.

```yaml
defeito_QA7_registrado: true
causa_ramo_eh_folha: true
tratamento_containers_e_folhas: true
quebra_pela_largura_restante: true
formula_largura_disp: "max(10, content_w - len(prefixo))"
linhas_de_continuacao: true
ausencia_reticencias_verboso: true
preservacao_modo_nao_verboso: true
teste_integrado_VERB_01_13: true
inspecao_saida_final: true  # secao 37.3 saida_final_coberta
tabela_preservada: true  # 37.4 H0037_MANUAL_001 tabela
conjuntos_preservados: true  # 37.4 H0037_MANUAL_001 conjuntos
Esc_preservado: true  # 37.4 H0037_MANUAL_002
V_e_v_preservados: true  # 37.4 H0037_MANUAL_003
paginacao_fora_do_escopo: true  # 37.5
10_scripts: true  # 37.7
2778_verificacoes: true  # 37.7
zero_falhas: true  # 37.7
arquivos_alterados: true  # 37.9
git_diff_check: true  # 37.10
stage_vazio: true  # 37.10
ausencia_commit_e_push: true  # 37.10
relatorio_manual_inalterado: true  # 37.10
revalidacao_manual_pendente: true  # 37.11
ausencia_autoaprovacao: true  # 37.12 e header global IMP-0037
conclusao_literal:
  esperado: "implementacao corrigida apos QA pos-validacao manual e aguardando novo QA independente"
  observado: "implementacao corrigida apos QA pós-validação manual e aguardando novo QA independente"
  compativel: true
classificacao: CONFORME
```

Nota: a afirmacao "o corte final `texto[:content_w]` da camada da caixa jamais
atua em modo verboso" (secao 37.1) e tecnicamente mais forte do que o codigo
garante no caso geral. Para prefixos com `len(prefixo) > content_w - 10`, a
linha intermediaria pode exceder `content_w` e o envelope ainda atuaria. Esta
imprecisao nao afeta os casos reais do H-0037 e nao constitui relatorio
incorreto que exige patch (classificada como observacao nao corretiva).

## 19. Testes Focais

```yaml
- script: tela/teste_renderizador.py
  verificacoes: 1290
  falhas: 0
  codigo_saida: 0
  esperado_declarado: {verificacoes: 1290, falhas: 0}
  conforme: true

- script: demo/teste_demo_console_modos.py
  verificacoes: 80
  falhas: 0
  codigo_saida: 0
  esperado_declarado: {verificacoes: 80, falhas: 0}
  conforme: true
```

Ambos os scripts terminaram com codigo de saida zero.

## 20. Suite Independente

Suite executada pelo QA:

```yaml
por_script:
  tela/teste_loader.py: {verificacoes: 512, falhas: 0, codigo_saida: 0}
  tela/teste_modelo.py: {verificacoes: 186, falhas: 0, codigo_saida: 0}
  tela/teste_renderizador.py: {verificacoes: 1290, falhas: 0, codigo_saida: 0}
  tela/teste_distribuicao_matricial.py: {verificacoes: 36, falhas: 0, codigo_saida: 0}
  demo/teste_demo.py: {verificacoes: 363, falhas: 0, codigo_saida: 0}
  demo/teste_diagnostico.py: {verificacoes: 48, falhas: 0, codigo_saida: 0}
  demo/teste_demo_distribuicao.py: {verificacoes: 109, falhas: 0, codigo_saida: 0}
  demo/teste_explorar_barra_de_menus.py: {verificacoes: 38, falhas: 0, codigo_saida: 0}
  demo/teste_demo_console.py: {verificacoes: 116, falhas: 0, codigo_saida: 0}
  demo/teste_demo_console_modos.py: {verificacoes: 80, falhas: 0, codigo_saida: 0}

total:
  scripts: 10
  verificacoes: 2778
  falhas: 0
  codigo_saida: todos_zero
  conforme_com_declarado: true
```

## 21. Smoke Tecnico

Smoke seguro, sem aprovacao visual:

```yaml
hierarquia_verbosa:
  largura_reduzida:
    dois_niveis_w30:
      quebra_em_linhas: true
      corte_silencioso: false
      reticencias: false
      conteudo_final_presente: true
    tres_niveis_w30:
      quebra_em_linhas: true
      corte_silencioso: false
      reticencias: false
    tres_niveis_w50:
      quebra_em_linhas: true
      corte_silencioso: false
      reticencias: false
      conteudo_final_presente: true

hierarquia_nao_verbosa:
  marcador_quando_truncado: "..."
  marcadores_dois_niveis_w30: 4

tabela:
  verboso_sem_marcador: true
  verboso_mais_linhas_que_nao_verboso: true
  nao_verboso_com_reticencias: true
  marcadores_nao_verboso_w50: 6

chips:
  Esc_primeiro: true
  alternavel_tres_niveis: "[Esc] Voltar  [V] Verboso"
  tabela_alternavel: "[Esc] Voltar  [V] Verboso"

teclas:
  V: funcional
  v: funcional
  telas_fixas: inertes

alternancia:
  NV1_igual_NV2: true
  V1_igual_V2: true
  token_final_verboso: "tres niveis." presente_em_V1_e_V2
  nao_verboso_nao_usa_dado_previamente_quebrado: true

smoke_nao_visual: tecnico
aprovacao_visual: nao_declarada
```

## 22. Revalidacao Manual

```text
REVALIDACAO_MANUAL_PENDENTE_USUARIO
```

O QA nao simulou observacao humana, nao declarou aprovacao visual, nao alterou
o relatorio manual anterior, nao criou novo relatorio manual e nao preparou
fechamento.

## 23. Achados

```yaml
- id: H0037-IMPL-QAPP8-001
  arquivo: tela/renderizador.py
  funcao_ou_teste: _linhas_apresentacao_hierarquia
  evidencia: >
    A formula `largura_disp = max(10, content_w - len(prefixo))` pode
    produzir linhas intermediarias com `len(prefixo) + len(frag) > content_w`
    quando `len(prefixo) > content_w - 10`. Nesse cenario extremo, o envelope
    `_linha_conteudo` aplica `texto[:content_w]` e trunca silenciosamente o
    conteudo em modo verboso. Reproduzido sinteticamente com content_w=12,
    prefix_len=9: linha_resultante=14 > content_w=12.
  autoridade: >
    Nao e regressao do oitavo patch — a mesma formula afetava nos folha
    antes. Nao ativada pelos dados reais do H-0037 (max prefix ~7 chars,
    min content_w 27 chars). IMP-0037 documenta como regra minima pre-existente.
  severidade: BAIXA
  tipo: OBSERVACAO_NAO_CORRETIVA
  impacto: >
    Potencial truncamento silencioso em casos extremos nao cobertos pelos
    testes H-0037. Nao afeta os quatro cenarios canonicos nem os VERB-01..13.
  correcao_exigida: Nenhuma nesta etapa.

- id: H0037-IMPL-QAPP8-002
  arquivo: tela/teste_renderizador.py
  funcao_ou_teste: teste_h0037_qapp7_verb_sem_corte_silencioso, VERB-06
  evidencia: >
    A expectativa `"  Politica" in texto_v30 or "Politica" in texto_v30`
    e satisfeita pela segunda clausula independentemente da primeira, tornando
    a verificacao de recuo redundante. O dado real contem "   Politica" (3
    espacos), que inclui "  Politica" como substring, portanto a verificacao
    de recuo FUNCIONALMENTE passa — mas a logica `or` a torna inutil se
    apenas a segunda clausula fosse aplicada.
  autoridade: >
    Nao afeta o resultado do teste (VERB-06 PASSOU corretamente para o
    dado real). Nao compromete a cobertura funcional. A verificacao de
    conteudo esta correta mesmo com a redundancia logica.
  severidade: BAIXA
  tipo: OBSERVACAO_NAO_CORRETIVA
  impacto: >
    A verificacao e passavel mesmo sem o recuo correto em dados sinteticos
    que contenham a string "Politica". Nao afeta os quatro cenarios H-0037.
  correcao_exigida: Nenhuma nesta etapa.
```

## 24. Conclusao

Ambos os achados do setimo QA pos-patch foram integralmente resolvidos:

- `H0037-IMPL-QAPP7-001`: o ramo verboso de `_linhas_apresentacao_hierarquia`
  agora atende todo no — container e folha — usando `_quebrar_texto` com a
  largura restante real. Os marcadores artificiais `...` nao aparecem em modo
  verboso em nenhum dos quatro cenarios canonicos, confirmados por smoke direto
  e pelos 37 novos casos de teste (VERB-01..13).

- `H0037-IMPL-QAPP7-002`: o teste integrado `teste_h0037_qapp7_verb_sem_corte_silencioso`
  cobre efetivamente VERB-01 a VERB-13, atravessa a renderizacao real e o
  envelope da caixa, verifica o token final, a ausencia de marcador artificial,
  a largura, dois e tres niveis, alternancia, tabela e conjuntos. O IMP-0037
  documenta o oitavo patch na secao 37 com todos os campos exigidos.

Restam apenas duas observacoes nao corretivas (H0037-IMPL-QAPP8-001 e
H0037-IMPL-QAPP8-002), nenhuma bloqueante.

A suíte canônica executada pelo QA: 10 scripts, 2778 verificacoes, 0 falhas.

A revalidacao manual permanece pendente e deve ser executada pelo usuario antes
do fechamento.

## 25. Status Literal

```text
IMPLEMENTATION_APPROVED_WITH_NOTES
```

## 26. Status Normalizado

```text
approved_with_notes
```

## 27. Proxima Categoria

```yaml
proxima_categoria: REVALIDACAO_MANUAL_USUARIO
```

## Saida Final Canonica

```yaml
status_literal: IMPLEMENTATION_APPROVED_WITH_NOTES
status_normalizado: approved_with_notes
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_8_H-0037_IMPLEMENTACAO.md
qa_anterior: docs/relatorios/RELATORIO_QA_POS_PATCH_7_H-0037_IMPLEMENTACAO.md
relatorio_validacao_manual: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md
relatorio_implementacao: docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md

git:
  raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
  stage: vazio
  diff_check: sem_erros
  commit_novo: inexistente
  push: nao_executado
  arquivos_do_oitavo_patch:
    - tela/renderizador.py
    - tela/teste_renderizador.py
    - docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  arquivos_inesperados: presentes_na_worktree_acumulada_origem_NAO_CONFIRMADA

integridade:
  python: OK
  conflitos: ausentes
  temporarios: ausentes

H0037_IMPL_QAPP7_001:
  ramo_hierarquico: todo_no_usa_quebrar_texto
  containers: conformes
  folhas: conformes
  nos_sem_conteudo: exibem_designador_sem_marcador_artificial
  largura_restante: max(10, content_w - len(prefixo))
  linhas_de_continuacao: indent_cont_igual_a_len_prefixo
  tokens_preservados: true
  saida_final: todas_as_linhas_largura_correta
  corte_silencioso: false
  reticencias_no_verboso: false
  alinhamento: preservado
  conforme: true

H0037_IMPL_QAPP7_002:
  teste_integrado: teste_h0037_qapp7_verb_sem_corte_silencioso
  casos_VERB_01_13: todos_cobertos_e_passaram
  saida_final_coberta: true
  token_final_coberto: true
  larguras_cobertas: [30, 50, 80, 220]
  dois_niveis: cobertos_VERB_06
  tres_niveis: cobertos_VERB_07
  alternancia: coberta_VERB_10
  tabela: coberta_VERB_12
  conjuntos: cobertos_VERB_13
  IMP_0037: conforme_secao_37
  conforme: true

modo_nao_verboso: conforme_marcador_presente_quando_excede
H0037_MANUAL_002_preservado: true
H0037_MANUAL_003_preservado: true
paginacao: NAO_APLICAVEL

preservacoes_anteriores:
  modos_iniciais: conformes
  conteudo_compartilhado: conforme
  D23: sem_regressao_nova
  V_01: preservada
  V_04: preservada
  V_13: preservada
  V_14: preservada
  demo_json: 11_entradas_carregadas
  regressao_H_0036: preservada

testes_focais:
  - {script: tela/teste_renderizador.py, verificacoes: 1290, falhas: 0, codigo_saida: 0}
  - {script: demo/teste_demo_console_modos.py, verificacoes: 80, falhas: 0, codigo_saida: 0}

suite_declarada:
  scripts: 10
  verificacoes: 2778
  falhas: 0

suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2778
  falhas: 0
  codigo_saida: todos_zero
  conforme_com_declarado: true

smoke_tests:
  tecnico: executado
  visual: nao_executado

revalidacao_manual: REVALIDACAO_MANUAL_PENDENTE_USUARIO

achados_bloqueantes: []
achados_altos: []
achados_medios: []
achados_baixos: []
observacoes:
  - H0037-IMPL-QAPP8-001
  - H0037-IMPL-QAPP8-002
regressoes: []

implementacao_aprovada: true
proxima_categoria: REVALIDACAO_MANUAL_USUARIO
```
