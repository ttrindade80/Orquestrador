---
status_literal: IMPLEMENTATION_APPROVED_WITH_NOTES
status_normalizado: approved_with_notes
historia: H-0037
tipo: QA_POS_PATCH_IMPLEMENTACAO
patch_auditado: sexto_patch_pos_QA
data: 2026-07-19
---

# RELATORIO QA POS PATCH 6 H-0037 IMPLEMENTACAO

## 1. Identificacao

Auditoria tecnica independente do sexto patch focal da implementacao H-0037.

Resultado: `IMPLEMENTATION_APPROVED_WITH_NOTES`.

## 2. Objetivo

Determinar se o sexto patch resolveu integralmente:

- `H0037-IMPL-QAPP5-001`
- `H0037-IMPL-QAPP5-002`

O QA concentrou-se na compatibilidade historica da variante 2 do envelope
pre-ADR-0028, ausencia de bypass por `regra_geracao_itens`, preservacao das
fixtures corrigidas, V-13 por `nivel` e `campo`, compatibilidade estrutural dos
dados externos e suite canonica final.

## 3. Autoridades

Arquivos obrigatorios lidos:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_5_H-0037_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0037_IMPLEMENTACAO.md
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
tela/loader.py
tela/teste_loader.py
demo/demo.py
demo/teste_demo.py
demo/teste_demo_console_modos.py
config/telas/demo/demo.json
```

Autoridades decisivas:

- `contrato_console.md` secao 3: `itens` ou regra de geracao de itens sao
  alternativas de fonte, dentro do envelope minimo do console.
- `contrato_json_console.md` secoes 12 e 13: documento externo multinivel,
  V-01, V-13, V-14 e D23.
- ADR-0028 D23: telas novas ou revisadas consumidoras de conteudo multinivel
  devem declarar `politica_modo`; telas legadas preservadas nao recebem politica
  por inferencia.
- QA POS PATCH 5: a chave `regra_geracao_itens` nao pode ser isencao generica e
  V-13 precisava cobrir `campo`.

## 4. Decisoes Explicitas Do Usuario

Decisoes reproduzidas no `IMP-0037` e aplicadas nesta auditoria:

```yaml
regra_geracao_itens:
  alternativa_contratual_a_itens: true
  schema_interno_fechado: inexistente
  inventar_schema: proibido

variante_2_historica:
  fonte_de_itens: regra_geracao_itens
  campos_base: 6
  itens: ausente
  compatibilidade: restrita_a_configuracao_historica_comprovada
  telas_novas: nao_podem_obter_compatibilidade
  consumidores_multinivel: nao_podem_obter_compatibilidade
```

## 5. Estado Git

Comandos iniciais obrigatorios confirmaram a raiz real:

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

Arquivos modificados rastreados no diff acumulado:

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
relatorios H-0037/ADR-0028 e `demo/teste_demo_console_modos.py`.

Itens inesperados:

```yaml
arquivo: "arquivos acumulados alem dos tres declarados para o sexto patch"
origem: NAO_CONFIRMADA
produzido_pelo_sexto_patch: NAO_CONFIRMADO
```

Artefatos transitorios: nenhum encontrado por `find` para `__pycache__`, `*.pyc`,
`*.tmp`, `*.bak`, `*.swp` ou `*~`.

## 6. Escopo Do Sexto Patch

O executor declarou alteracao em:

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

O diff acumulado da worktree e maior que essa lista, mas nao ha commit novo que
permita separar mecanicamente alteracoes anteriores das do sexto patch. Nao
atribuo origem sem evidencia.

Alteracoes focais confirmadas:

```yaml
- arquivo: tela/loader.py
  alteracao: "_console_em_escopo_d23 passa a classificar variantes 1/2 do envelope, rejeitar hibridos e restringir variante 2 a _TELAS_VARIANTE2_LEGADAS"
  autorizacao: "H0037-IMPL-QAPP5-001"
  necessidade: sim
  impacto: "elimina isencao generica por regra_geracao_itens"
  classificacao: JUSTIFICADA

- arquivo: tela/loader.py
  alteracao: "validar_conteudo_externo deriva catalogo de campo de formato.niveis[].conteudo e aplica V-13 para campo"
  autorizacao: "H0037-IMPL-QAPP5-002"
  necessidade: sim
  impacto: "separa campo sem origem (V-14) de campo declarado mas inexistente (V-13)"
  classificacao: JUSTIFICADA

- arquivo: tela/teste_loader.py
  alteracao: "remove mascaras regra_geracao_itens:{} de fixtures macro e adiciona matriz RGI-P6/V13-P6"
  autorizacao: "H0037-IMPL-QAPP5-001/002"
  necessidade: sim
  impacto: "preserva testes macro com envelope variante 1 completo"
  classificacao: JUSTIFICADA

- arquivo: docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  alteracao: "secao 35 documenta Resultado B, variantes, fixtures e suite 2694"
  autorizacao: "relatorio de implementacao"
  necessidade: sim
  impacto: "rastreabilidade do sexto patch"
  classificacao: JUSTIFICADA
```

## 7. Integridade

`ast.parse`:

```yaml
tela/loader.py: OK
tela/teste_loader.py: OK
demo/demo.py: OK
demo/teste_demo.py: OK
demo/teste_demo_console_modos.py: OK
```

`json.loads`:

```yaml
config/telas/demo/demo.json: OK
config/telas/demo/h0037_console_nao_verboso.json: OK
config/telas/demo/h0037_console_verboso_dois_niveis.json: OK
config/telas/demo/h0037_console_alternavel_tres_niveis.json: OK
config/telas/demo/h0037_console_tabela_alternavel.json: OK
config/telas/demo/h0037_dois_niveis_conteudo.json: OK
config/telas/demo/h0037_tres_niveis_conteudo.json: OK
config/telas/demo/h0037_tabela_conteudo.json: OK
```

Conflitos: sem marcadores reais `<<<<<<<`/`>>>>>>>`. O `rg` encontrou linhas
`=======` em relatorios e comentarios, nao um bloco de conflito.

Temporarios: ausentes.

## 8. Duas Variantes Do Envelope

```yaml
variantes_envelope:
  variante_1:
    fonte_de_itens: itens
    campos_base: [origem_dados, politica_composicao, politica_navegacao, politica_selecao, politica_paginacao, politica_exibicao]
    regra_geracao_itens: ausente
    conforme: true
  variante_2:
    fonte_de_itens: regra_geracao_itens
    campos_base: [origem_dados, politica_composicao, politica_navegacao, politica_selecao, politica_paginacao, politica_exibicao]
    itens: ausente
    compatibilidade: historica_restrita
    conforme: true
  exclusividade_das_fontes: true
  completude_externa: true
  schema_interno_inventado: false
```

O loader rejeita `itens` + `regra_geracao_itens`, rejeita variantes incompletas
e nao valida schema interno de `regra_geracao_itens`.

## 9. Variante Historica 2

Matriz executada pelo carregador publico:

```yaml
variante_2:
  configuracao_real_demo_json: ACEITO
  mesma_estrutura_e_mesma_identidade_demo: ACEITO
  mesma_estrutura_outro_id: REJEITADO
  prefixos_semelhantes:
    demo_novo: REJEITADO
    demo_copia: REJEITADO
    h0037_demo: REJEITADO
  consumidor_multinivel_com_id_demo: REJEITADO_D23
  variante2_com_marcador_D23: REJEITADO
  variante2_incompleta_sem_cada_campo_base: REJEITADO
  variante2_mais_itens: REJEITADO
  variante2_nova_com_regra_vazia: REJEITADO
  variante2_nova_com_valor_historico_copiado: REJEITADO
  nova_tela_consegue_bypass: false
  compatibilidade_restrita: true
  conforme: true
```

## 10. Identidade `demo`

`_TELAS_VARIANTE2_LEGADAS = frozenset({"demo"})` compara contra `id_tela`
derivado do JSON carregado e validado contra o basename do arquivo. Portanto
`demo` representa a identidade da tela/arquivo `config/telas/demo/demo.json`
cujo `id` interno tambem e `demo`; nao e o id do elemento `console_principal`,
catalogo externo ou prefixo de path.

Observacao: a restricao e nominal por `id_tela`; nao e uma comparacao byte a
byte do elemento historico. Isso nao gerou bypass para telas novas, prefixos,
copias renomeadas ou consumidores multinivel.

## 11. Matriz Adversarial Da Variante 2

```yaml
V2_01_configuracao_historica_real: ACEITO
V2_02_mesma_estrutura_mesma_identidade: ACEITO
V2_03_mesma_estrutura_outro_id: REJEITADO_SEM_COMPATIBILIDADE_HISTORICA
V2_04_prefixos_semelhantes: SEM_COMPATIBILIDADE_AUTOMATICA
V2_05_consumidor_multinivel_com_id_demo: REJEITADO
V2_06_variante2_com_marcador_D23: REJEITADA_COMO_MISTURA_DE_FORMAS
V2_07_variante2_incompleta: REJEITADA
V2_08_variante2_mais_itens: REJEITADA_POR_DUAS_FONTES
V2_09_variante2_nova_com_regra_vazia: REJEITADA
V2_10_variante2_nova_com_valor_historico: REJEITADA_SE_IDENTIDADE_NAO_FOR_A_HISTORICA
```

## 12. Ausencia De Bypass D23

```yaml
D23:
  regra_geracao_itens_usada_como_isencao_generica: false
  consumidor_sem_politica_consegue_bypass: false
  consumidor_sem_politica_com_regra_vazia: rejeitado
  consumidor_sem_politica_com_regra_historica_copiada: rejeitado
  consumidor_com_politica_e_regra_geracao: rejeitado_como_hibrido
  consumidor_com_um_a_seis_campos_de_envelope: rejeitado
  consumidor_com_variante_2_completa_e_id_novo: rejeitado
  envelope_variante_1_incompleto: rejeitado
  envelope_variante_2_incompleto: rejeitado
  cinco_legados_preservados: true
  bypass_remanescente: false
  conforme: true
```

## 13. 26 Fixtures

O diff de `tela/teste_loader.py` mostra remocao da mascara conceitual
`regra_geracao_itens:{}` dos placeholders macro e substituicao por envelope
variante 1 completo (`itens` + seis campos-base). O arquivo tambem adiciona
testes RGI-P6 e V13-P6, por isso o diff acumulado tem mais linhas do que as 26
fixtures declaradas.

Agrupamento das 26 fixtures corrigidas:

```yaml
grupo_1:
  fixture: _tela_minima
  teste: testes macro de loader que precisam de tela valida
  objetivo_original: tela minima valida sem foco em D23
  forma_incorreta_anterior: regra_geracao_itens:{} como mascara
  forma_corrigida: envelope variante 1 completo
  variante_usada: variante_1
  campos_obrigatorios_presentes: true
  objetivo_preservado: true
  resultado: JUSTIFICADA

grupo_2:
  fixture: _run_tipos_validos
  teste: taxonomia de tipos validos
  objetivo_original: aceitar console/lancador/dashboard
  forma_incorreta_anterior: console placeholder insuficiente para nova regra
  forma_corrigida: _ENVELOPE_CONSOLE_COMPLETO
  variante_usada: variante_1
  campos_obrigatorios_presentes: true
  objetivo_preservado: true
  resultado: JUSTIFICADA

grupo_3:
  fixture: grupos, hierarquia de grupos, distribuicao de corpo e matriz
  teste: validacoes de arranjo/distribuicao/grupo nao relacionadas a D23
  objetivo_original: manter console valido como filho/irmao em cenarios macro
  forma_incorreta_anterior: regra_geracao_itens:{} ou console parcial
  forma_corrigida: envelope variante 1 completo
  variante_usada: variante_1
  campos_obrigatorios_presentes: true
  objetivo_preservado: true
  resultado: JUSTIFICADA
```

Confirmacoes:

```yaml
regra_geracao_itens_vazia_removida_das_fixtures_macro: true
fixture_corrigida_representa_envelope_variante_1_completo: true
teste_de_consumidor_convertido_em_envelope: false
teste_invalido_transformado_em_valido_sem_intencao: false
expectativas_originais_preservadas: true
numero_26: compativel_com_declaracao_do_executor_e_com_grupos_do_diff
contagem_manual_mascaradora: nao_evidenciada
classificacao: JUSTIFICADA
```

## 14. V-13 Por Nivel

```yaml
nivel:
  ausente: V_14
  null: V_14
  vazio: V_14
  whitespace: V_14
  tipo_incorreto: V_14
  sintaticamente_valido_mas_inexistente: V_13
  existente_e_compativel: aceito
```

A coluna ultrapassa V-01 antes de V-13/V-14 quando existe coluna reconhecivel.

## 15. Catalogo Estrutural De Campos

Implementacao auditada em `validar_conteudo_externo`:

```yaml
catalogo_de_campos:
  origem: formato.niveis[].conteudo
  entradas:
    container: conteudo string
    conteudo: conteudo string
    nome_valor: conteudo.nome e conteudo.valor
  extracao: strings nao vazias
  duplicados: colapsados_por_set
  valores_vazios: rejeitados_antes_ou_ignorados_na_coleta
  niveis_inexistentes_contaminam_catalogo: false
  documento_estrutural_correto: documento_externo_multinivel
  conteudo_externo_altera_catalogo_indevidamente: false
  escopo: colunas_de_tabela
  generalizacao_indevia: false
  conforme: true
```

## 16. V-13 Por Campo

Casos executados:

```yaml
campo:
  estrutural_existente: ACEITO
  estrutural_inexistente: V_13
  campo_no_nivel_errado_combo_nivel_grupo_campo_texto: ACEITO
  campo_ausente_nos_dados_com_dados_vazios: ACEITO
  campo_presente_nos_dados_mas_nao_declarado_na_estrutura: V_13_quando_referenciado_em_coluna
  vazio: V_14
  whitespace: V_14
  tipo_incorreto: V_14
  duas_colunas_validas: ACEITAS
  apresentacao_sem_catalogo_aplicavel: nao_generalizada
  conforme: true
```

Justificativa: a autoridade explicita usada pelo sexto patch define o catalogo
por `formato.niveis[].conteudo`. O contrato nao exige, de forma materialmente
bloqueante nesta auditoria, que uma coluna com `nivel` e `campo` valide o par
nivel-campo quando ambos sao declarados; V-14 fala em nivel **ou** campo de
origem. Tambem nao exige que todo campo estrutural declarado apareca nos dados
quando a propria lista `dados` e vazia. Nao criei requisito novo.

## 17. Compatibilidade Com Dados

```yaml
estrutura_declara_nivel_dados_nao_possuem:
  resultado: rejeitado_quando_no_referencia_nivel_inexistente_ou_no_viola_nivel

estrutura_declara_campo_dados_nao_possuem:
  resultado: rejeitado_quando_no_do_nivel_existe_sem_o_campo_de_conteudo

dados_possuem_campo_nao_declarado:
  resultado: aceito_como_campo_extra_de_no; rejeitado_se_coluna_referencia_campo_nao_declarado

estrutura_e_dados_compativeis:
  resultado: aceito
```

Conclusao: V-13 cobre a incompatibilidade entre dados e estrutura declarada pelas
validacoes 12-17 e cobre `campo` de coluna contra o catalogo estrutural. Nao
identifiquei exigencia normativa para rejeitar campos extras nos nos.

## 18. Separacao V-01/V-13/V-14

```yaml
V_01:
  condicao: nenhuma_coluna_reconhecivel
  caso_executado: cabecalho_sem_coluna_reconhecivel
  falha: V_01

V_14:
  condicao: origem_ausente_ou_sem_valor_semantico
  coluna_reconhecida: true
  origem_sem_valor: true
  falha: V_14

V_13_nivel:
  condicao: origem_declarada_mas_incompativel_com_estrutura
  coluna_reconhecida: true
  nivel_declarado: true
  nivel_existe: false
  falha: V_13

V_13_campo:
  condicao: campo_declarado_mas_incompativel_com_catalogo_estrutural
  coluna_reconhecida: true
  campo_declarado: true
  campo_existe: false
  falha: V_13
```

## 19. Lista Mista

```yaml
lista_mista:
  comportamento: aceita_quando_ha_ao_menos_uma_coluna_reconhecivel_valida
  alterada_no_sexto_patch: false
  classificacao: OBSERVACAO_NAO_CORRETIVA
```

Nao reclassifiquei como bloqueio sem nova autoridade.

## 20. Itens Preservados

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso

tecla_V:
  telas_fixas: inerte
  telas_alternaveis: reversivel

V_01:
  conforme: true

V_04:
  folha_sem_filhos: aceita
  folha_com_filhos_vazio: rejeitada
  folha_com_filho_real: rejeitada

V_14:
  origem_ausente: rejeitada
  origem_null: rejeitada
  origem_vazia: rejeitada
  origem_whitespace: rejeitada
  tipo_incorreto: rejeitado

conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false

demo_json:
  carrega: true
  entradas: 11

inventario_legado_D23:
  total: 5

recalibracoes_launcher:
  preservadas: true

regressao_H_0036:
  preservada: true
```

## 21. Relatorio IMP-0037

A secao 35 registra corretamente:

```yaml
qa_de_origem: true
portao_documental_resultado_B: true
ausencia_schema_interno_fechado: true
decisao_de_nao_inventar_schema: true
duas_variantes_externas_do_envelope: true
variante_2_restrita_ao_historico_demo: true
significado_de_demo: "parcialmente explicito; no codigo e id_tela"
rejeicao_de_copia_renomeada: true
rejeicao_de_consumidor_hibrido: true
correcao_das_26_fixtures: true
catalogo_de_campos: true
V_13_por_nivel: true
V_13_por_campo: true
separacao_V_13_V_14: true
compatibilidade_com_dados_conforme_autoridade: true
lista_mista_observacao: true
10_scripts: true
2694_verificacoes: true
zero_falhas: true
git_diff_check: true
stage_vazio: true
ausencia_commit_push: true
validacao_manual_pendente: true
ausencia_autoaprovacao: true
```

O relatorio nao fecha schema interno novo para `regra_geracao_itens`.

## 22. Testes Focais

```yaml
- script: tela/teste_loader.py
  verificacoes: 512
  falhas: 0
  codigo_saida: 0

- script: demo/teste_demo.py
  verificacoes: 363
  falhas: 0
  codigo_saida: 0

- script: demo/teste_demo_console_modos.py
  verificacoes: 63
  falhas: 0
  codigo_saida: 0
```

## 23. Suite Independente

```yaml
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2694
  falhas: 0
  codigo_saida: todos_zero

por_script:
  tela/teste_loader.py: {verificacoes: 512, falhas: 0, codigo_saida: 0}
  tela/teste_modelo.py: {verificacoes: 186, falhas: 0, codigo_saida: 0}
  tela/teste_renderizador.py: {verificacoes: 1223, falhas: 0, codigo_saida: 0}
  tela/teste_distribuicao_matricial.py: {verificacoes: 36, falhas: 0, codigo_saida: 0}
  demo/teste_demo.py: {verificacoes: 363, falhas: 0, codigo_saida: 0}
  demo/teste_diagnostico.py: {verificacoes: 48, falhas: 0, codigo_saida: 0}
  demo/teste_demo_distribuicao.py: {verificacoes: 109, falhas: 0, codigo_saida: 0}
  demo/teste_explorar_barra_de_menus.py: {verificacoes: 38, falhas: 0, codigo_saida: 0}
  demo/teste_demo_console.py: {verificacoes: 116, falhas: 0, codigo_saida: 0}
  demo/teste_demo_console_modos.py: {verificacoes: 63, falhas: 0, codigo_saida: 0}
```

## 24. Smoke Tecnico

Smoke seguro, sem aprovacao visual:

```yaml
h0037_console_nao_verboso: nao_verboso
h0037_console_verboso_dois_niveis: verboso
h0037_console_alternavel_tres_niveis: nao_verboso
h0037_console_tabela_alternavel: verboso
```

## 25. Validacao Manual

Permanece:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Nao simulei usuario, nao declarei aprovacao visual, nao criei relatorio de
validacao manual e nao preparei fechamento.

## 26. Achados

```yaml
- id: H0037-IMPL-QAPP6-001
  arquivo: tela/loader.py
  funcao_ou_teste: _console_em_escopo_d23 / _TELAS_VARIANTE2_LEGADAS
  evidencia: "A compatibilidade da variante 2 e restrita nominalmente a id_tela == 'demo'. Cópias renomeadas, prefixos e consumidores multinivel com id demo foram rejeitados; uma variante 2 completa em arquivo temporario tambem chamado demo e aceita por essa identidade nominal."
  autoridade: "decisoes explicitas do usuario: nao inventar schema interno e restringir variante 2 ao historico demo"
  severidade: BAIXA
  tipo: OBSERVACAO_NAO_CORRETIVA
  impacto: "Nao ha bypass para telas novas nem consumidores multinivel; a restricao e nominal, nao comparacao integral de snapshot historico."
  correcao_exigida: "Nenhuma nesta etapa, salvo decisao futura para inventario por elemento/snapshot."

- id: H0037-IMPL-QAPP6-002
  arquivo: tela/loader.py
  funcao_ou_teste: validar_conteudo_externo / lista mista de cabecalho
  evidencia: "Comportamento de lista mista permanece inalterado e ja havia sido classificado como observacao nao bloqueante."
  autoridade: "QA POS PATCH 5; ausencia de nova autoridade proibitiva"
  severidade: BAIXA
  tipo: OBSERVACAO_NAO_CORRETIVA
  impacto: "Nenhum bloqueio para os achados H0037-IMPL-QAPP5-001/002."
  correcao_exigida: "Nenhuma."
```

## 27. Conclusao

O sexto patch resolveu integralmente os achados de origem. A chave
`regra_geracao_itens` nao concede mais isencao D23 por mera presenca; a variante
2 exige os seis campos-base, ausencia de `itens` e identidade historica `demo`.
Telas novas, copias renomeadas, prefixos e consumidores multinivel nao obtiveram
compatibilidade.

V-13 agora cobre `nivel` e `campo` com causa distinta de V-14. A suite canonica
executada pelo QA tem 10 scripts, 2694 verificacoes, 0 falhas.

Restam apenas observacoes nao corretivas.

## 28. Status Literal

```text
IMPLEMENTATION_APPROVED_WITH_NOTES
```

## 29. Status Normalizado

```text
approved_with_notes
```

## 30. Proxima Categoria

```yaml
proxima_categoria: VALIDACAO_MANUAL_USUARIO
```

## Saida Final Canonica

```yaml
status_literal: IMPLEMENTATION_APPROVED_WITH_NOTES
status_normalizado: approved_with_notes
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_6_H-0037_IMPLEMENTACAO.md
qa_anterior: docs/relatorios/RELATORIO_QA_POS_PATCH_5_H-0037_IMPLEMENTACAO.md
handoff: docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
relatorio_implementacao: docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md

git:
  raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
  stage: vazio
  diff_check: sem_erros
  commit_novo: inexistente
  push: nao_executado
  arquivos_do_sexto_patch:
    - tela/loader.py
    - tela/teste_loader.py
    - docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  arquivos_inesperados: presentes_na_worktree_acumulada_origem_NAO_CONFIRMADA

integridade:
  python: OK
  json: OK
  conflitos: sem_marcadores_git_reais
  temporarios: ausentes

variantes_envelope:
  variante_1: conforme
  variante_2: conforme
  exclusividade: conforme
  completude: conforme
  schema_interno_inventado: false

variante_2:
  identidade_historica: id_tela_demo
  configuracao_real: aceita
  copia_renomeada: rejeitada
  prefixos_semelhantes: rejeitados
  consumidor_com_id_historico: rejeitado
  marcador_D23: rejeitado
  incompleta: rejeitada
  coexistencia_com_itens: rejeitada
  nova_tela: rejeitada
  compatibilidade_restrita: true
  conforme: true

D23:
  consumidor_sem_politica: rejeitado
  regra_vazia: rejeitada
  regra_historica_copiada: rejeitada
  consumidor_hibrido: rejeitado
  campos_parciais: rejeitados
  envelope_incompleto: rejeitado
  cinco_legados: preservados
  bypass_remanescente: false
  conforme: true

fixtures_corrigidas:
  quantidade: 26
  removidas_mascaras: true
  objetivos_preservados: true
  classificacao: JUSTIFICADA

V_01:
  preservado: true

V_13:
  nivel_inexistente: rejeitado
  campo_inexistente: rejeitado
  campo_no_nivel_errado: aceito_sem_autoridade_bloqueante_para_par_nivel_campo
  incompatibilidade_com_estrutura: rejeitada
  incompatibilidade_com_dados: coberta_pelas_validacoes_12_17_quando_no_viola_nivel
  incompatibilidade_com_apresentacao: rejeitada_para_bloco_especifico_incompativel
  causa_distinta: true
  conforme: true

V_14:
  origem_sem_valor: rejeitada
  causa_distinta: true
  conforme: true

catalogo_de_campos:
  origem: formato.niveis[].conteudo
  escopo: colunas_de_tabela
  conforme: true

lista_mista: OBSERVACAO_NAO_CORRETIVA
itens_preservados: true
relatorio_IMP_0037: conforme_com_notas

testes_focais:
  scripts: 3
  verificacoes: 938
  falhas: 0
suite_declarada:
  scripts: 10
  verificacoes: 2694
  falhas: 0
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2694
  falhas: 0
smoke_tests: conforme_sem_aprovacao_visual
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

achados_bloqueantes: []
achados_altos: []
achados_medios: []
achados_baixos:
  - H0037-IMPL-QAPP6-001
  - H0037-IMPL-QAPP6-002
observacoes:
  - compatibilidade_variante2_nominal_por_id_tela_demo
  - lista_mista_preservada_como_observacao_nao_corretiva
regressoes: []

implementacao_aprovada: true
proxima_categoria: VALIDACAO_MANUAL_USUARIO
```
