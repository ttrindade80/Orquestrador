---
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_required
historia: H-0037
tipo: QA_POS_PATCH_IMPLEMENTACAO
patch_auditado: quinto_patch_pos_QA
data: 2026-07-19
---

# RELATORIO QA POS PATCH 5 H-0037 IMPLEMENTACAO

## 1. Identificacao

Auditoria tecnica independente do quinto patch focal da implementacao H-0037.

Resultado: `IMPLEMENTATION_PATCH_REQUIRED`.

## 2. Objetivo

Determinar se o quinto patch resolveu integralmente:

- `H0037-IMPL-QAPP4-001` -- bypass do D23 por campos parciais de envelope.
- `H0037-IMPL-QAPP4-002` -- origem declarada, mas incompativel.

Regra prioritaria: `regra_geracao_itens` nao pode transformar por mera presenca
uma tela consumidora multinivel, estrutura hibrida ou objeto invalido em console
de geracao interna fora do D23.

## 3. Autoridades

Arquivos obrigatorios consultados:

- `docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0037_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0037_IMPLEMENTACAO.md`
- `docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
- `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md`
- `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `tela/loader.py`
- `tela/teste_loader.py`
- `demo/demo.py`
- `demo/teste_demo.py`
- `demo/teste_demo_console_modos.py`
- `config/telas/demo/demo.json`

Autoridades materiais:

- `contrato_console.md` secao 3 exige instancia minima de `console` com
  `origem_dados` ou `binding`, `itens` ou regra de geracao de itens, e politicas
  de composicao, navegacao, selecao, paginacao e exibicao.
- O mesmo contrato registra como invalida instancia sem `origem_dados`,
  `binding` ou regra de geracao de itens, e sem cada politica obrigatoria.
- `demo.json` declara `regra_geracao_itens` como pendencia DOC-B008, com
  `tipo: "pendente"` e `nota`; isso nao define schema geral para aceitar `{}`.
- ADR-0028 / `contrato_json_console.md` D23 exigem politica de modo para telas
  novas ou revisadas consumidoras de console multinivel, sem default implicito.
- ADR-0028 V-13 invalida dados incompativeis com a estrutura declarada.
- ADR-0028 V-14 invalida coluna de tabela sem nivel ou campo de origem.

## 4. Estado Git

Comandos executados a partir da raiz real:

```text
pwd
/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
branch
master
HEAD
f6982d08640af1762b8e0e8814b6e90c9421538e
git log -1
f6982d0 docs: corrige whitespace do fechamento H-0036
```

```yaml
branch: master
head: f6982d08640af1762b8e0e8814b6e90c9421538e
stage: vazio
commit_novo: inexistente
push: nao_executado
diff_check: sem_erros
```

Arquivos modificados rastreados:

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

Arquivos nao rastreados relevantes:

```text
config/telas/demo/h0037_console_alternavel_tres_niveis.json
config/telas/demo/h0037_console_nao_verboso.json
config/telas/demo/h0037_console_tabela_alternavel.json
config/telas/demo/h0037_console_verboso_dois_niveis.json
config/telas/demo/h0037_dois_niveis_conteudo.json
config/telas/demo/h0037_tabela_conteudo.json
config/telas/demo/h0037_tres_niveis_conteudo.json
demo/teste_demo_console_modos.py
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0037_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0037_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md
```

```yaml
documentacao_acumulada: presente
arquivos_tecnicos: presentes
relatorios: presentes
whitespace: sem_erros
artefatos_transitorios: nenhum_encontrado
arquivos_inesperados:
  - arquivo: "multiplos arquivos acumulados modificados/nao rastreados alem dos tres declarados para o quinto patch"
    origem: NAO_CONFIRMADA
    produzido_pelo_quinto_patch: NAO_CONFIRMADO
```

## 5. Escopo Do Quinto Patch

O relatorio de implementacao declara como arquivos alterados no quinto patch:

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

O diff acumulado da worktree e maior que essa lista. Como nao ha commit novo, nao
e possivel separar com certeza absoluta o quinto patch das alteracoes acumuladas.
Nao atribuo origem sem evidencia.

Alteracoes focalmente confirmadas:

```yaml
- arquivo: tela/loader.py
  alteracao: "_console_em_escopo_d23 passa a retornar fora de D23 quando a chave regra_geracao_itens existe"
  autorizacao: "relacionada ao achado H0037-IMPL-QAPP4-001"
  necessidade: "sim, mas implementada sem validacao estrutural suficiente"
  impacto: "bypass por mera presenca da chave"
  classificacao: DEFEITO_IMPLEMENTACAO

- arquivo: tela/teste_loader.py
  alteracao: "testes D23-P5 adicionados e fixtures antigas recebem regra_geracao_itens"
  autorizacao: "relacionada ao achado H0037-IMPL-QAPP4-001"
  necessidade: "parcial"
  impacto: "testes aceitam forma vazia/pendente nao comprovada"
  classificacao: TESTE_INCORRETO

- arquivo: docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  alteracao: "secao 34 declara resolucao e isencao por regra_geracao_itens"
  autorizacao: "relatorio de implementacao"
  necessidade: "sim"
  impacto: "declara conforme o que a matriz adversarial refuta"
  classificacao: RELATORIO_INCORRETO
```

## 6. Integridade

Validacao por `ast.parse`:

```yaml
tela/loader.py: OK
tela/teste_loader.py: OK
demo/demo.py: OK
demo/teste_demo.py: OK
demo/teste_demo_console_modos.py: OK
```

Validacao por `json.loads`:

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

Buscas:

```yaml
conflitos_git:
  marcadores: ausentes
temporarios:
  __pycache__: ausente
  pyc: ausente
  tmp_bak_swp_til: ausentes
```

## 7. Autoridade De `regra_geracao_itens`

```yaml
regra_geracao_itens:
  mera_presenca_identifica_forma: nao
  objeto_vazio_valido: nao_comprovado_pela_autoridade
  campos_internos_obrigatorios: nao_definidos_em_contrato_fechado
  tipos_e_valores_permitidos: nao_definidos_em_contrato_fechado
  mutuamente_exclusiva_com_itens: "sim como fonte concorrente: contrato diz itens OU regra"
  mutuamente_exclusiva_com_origem_dados: "nao como conceito geral: contrato exige origem_dados/binding ou regra, mas demo combina origem_dados pendente com regra pendente"
  compativel_com_campos_politica_envelope: "somente se a instancia inteira for contratualmente valida; nao por chave avulsa"
  pode_coexistir_com_consumidor_multinivel: nao
  objeto_incompleto_deve_ser_rejeitado: sim
  etapa_validacao: "loader/camada equivalente antes de conceder isencao D23"
```

Conclusao normativa: a autoridade permite tratar uma regra de geracao de itens
como alternativa a `itens`, mas nao autoriza que qualquer valor sob a chave
`regra_geracao_itens` seja uma regra valida. A implementacao concede isencao
antes de validar se existe uma forma estrutural valida.

## 8. Matriz Adversarial Da Geracao Interna

Casos executados pelo carregador publico `carregar_tela`, com JSONs temporarios
em `/tmp`.

```yaml
RGI-01_geracao_interna_historica_valida: ACEITA
RGI-02_objeto_vazio: ACEITA_INCORRETAMENTE
RGI-03_null: ACEITA_INCORRETAMENTE
RGI-04_string: ACEITA_INCORRETAMENTE
RGI-04_lista: ACEITA_INCORRETAMENTE
RGI-04_booleano: ACEITA_INCORRETAMENTE
RGI-04_numero: ACEITA_INCORRETAMENTE
RGI-05_objeto_sem_tipo: ACEITA_INCORRETAMENTE
RGI-05_objeto_sem_ids: ACEITA_INCORRETAMENTE
RGI-06_consumidor_sem_politica_mais_objeto_vazio: ACEITA_INCORRETAMENTE
RGI-07_consumidor_sem_politica_mais_regra_sintatica: ACEITA_INCORRETAMENTE
RGI-08_consumidor_com_politica_mais_regra: REJEITA
RGI-09_regra_mais_itens: ACEITA_INCORRETAMENTE
RGI-10_regra_mais_origem_dados: ACEITA
RGI-11_regra_mais_1_a_6_campos_envelope: ACEITA_INCORRETAMENTE
RGI-12_regra_mais_envelope_completo: ACEITA_INCORRETAMENTE
RGI-13_copia_renomeada_consumidor_mais_objeto_vazio: ACEITA_INCORRETAMENTE
RGI-14_demo_json:
  tipo_estrutural_real: "console_principal com origem_dados pendente, regra_geracao_itens pendente e 5/7 campos de envelope historico"
  forma_contratualmente_valida: nao_comprovada_por_contrato_fechado
  fica_fora_do_D23: "pela implementacao, por mera presenca de regra_geracao_itens"
  valor_regra_geracao_itens_valido: nao_comprovado
  depende_apenas_da_chave: sim_no_loader
```

Resultado obrigatorio:

```yaml
regra_geracao_itens:
  mera_presenca_concede_isencao: true
  objeto_vazio_valido: false
  valor_null_aceito: true
  tipos_incorretos_aceitos: true
  objeto_incompleto_aceito: true
  consumidor_sem_politica_consegue_bypass: true
  consumidor_com_regra_valida_aceito_como_hibrido: true
  coexistencia_com_itens: aceita_incorretamente
  coexistencia_com_origem_dados: aceita
  coexistencia_com_envelope: aceita_incorretamente
  demo_json_conforme: nao_comprovado
  bypass_remanescente: true
  conforme: false
```

## 9. Campos Parciais De Envelope

Sem `regra_geracao_itens`, o quinto patch corrigiu o bypass por cardinalidade
parcial de envelope.

```yaml
consumidor_sem_politica:
  zero_campos_envelope: rejeitado_D23
  um_campo_envelope: rejeitado_D23
  dois_campos_envelope: rejeitado_D23
  tres_campos_envelope: rejeitado_D23
  quatro_campos_envelope: rejeitado_D23
  cinco_campos_envelope: rejeitado_D23
  seis_campos_envelope: rejeitado_D23

envelope_historico:
  completo_valido: aceito
  incompleto: rejeitado_D23
  valores_invalidos: rejeitado
```

Essa conformidade e anulada como fechamento do achado porque a mesma estrutura
passa a ser aceita se receber `regra_geracao_itens` vazia, nula ou invalida.

## 10. Fixtures Alteradas

Ocorrencias literais em `tela/teste_loader.py`:

```yaml
arquivo: tela/teste_loader.py
ocorrencias_regra_geracao_itens_objeto_vazio: 27
linhas_representativas:
  - 141
  - 723
  - 901
  - 1080
  - 1096
  - 1115
  - 1135
  - 1157
  - 1183
  - 1225
  - 1244
  - 1261
  - 1279
  - 1293
  - 1309
  - 1332
  - 1351
  - 1370
  - 1387
  - 1434
  - 1550
  - 1556
  - 1564
  - 1688
  - 1703
  - 2075
  - 2173
forma_anterior: "{ itens: [], origem_dados: null } em fixtures de console placeholder"
forma_atual: "{ itens: [], origem_dados: null, regra_geracao_itens: {} }"
regra_geracao_itens_valida_pelo_contrato: nao_comprovado
mudanca_preserva_objetivo_original: nao_comprovado
mudanca_mascara_erro: sim
resultado: REGRESSAO_MASCARADA
```

Classificacao: `REGRESSAO_MASCARADA`. Os testes passaram porque receberam a
chave de isencao, nao porque a forma de geracao interna vazia tenha sido
validada contratualmente.

## 11. V-13 Por Nivel

Casos executados por `validar_conteudo_externo`:

```yaml
nivel_ausente: V_14
nivel_null: V_14
nivel_vazio: V_14
nivel_whitespace: V_14
nivel_tipo_incorreto: V_14
nivel_sintaticamente_valido_mas_inexistente: V_13
nivel_existente: aceito
```

A coluna com `titulo` ultrapassa V-01 e falha em V-14 quando a origem nao tem
valor semantico. A coluna com `nivel` string nao vazia mas inexistente falha em
V-13, com mensagem distinta de V-14.

## 12. V-13 Por Campo

Casos executados por `validar_conteudo_externo`:

```yaml
campo:
  ausente: V_14
  null: V_14
  vazio: V_14
  whitespace: V_14
  tipo_incorreto: V_14
  inexistente_na_estrutura: ACEITA_INCORRETAMENTE
  inexistente_nos_dados: rejeitado_por_TelaCampoObrigatorioAusente_no_no_nome_valor
  incompativel_com_apresentacao: ACEITA_INCORRETAMENTE
  valido: aceito
  duas_colunas_validas: aceito
```

O loader implementa V-13 para `nivel`, mas nao valida `campo` equivalente. Uma
coluna com `campo: "nao_existe"` e aceita quando os dados possuem os campos
exigidos pelo nivel, mesmo que a coluna declare campo nao disponivel.

## 13. Compatibilidade Com Dados

```yaml
estrutura_declara_nivel:
  dados_nao_possuem_nivel: rejeitado
  causa: V_13_ou_validacao_12_17

estrutura_declara_campo:
  dados_nao_possuem_campo: rejeitado_quando_o_campo_e_parte_do_contrato_do_nivel
  coluna_declara_campo_nao_existente: aceita_incorretamente

estrutura_e_dados_compativeis:
  resultado: aceito
```

Conclusao: a compatibilidade estrutural dos dados por nivel foi melhorada, mas a
origem por `campo` declarada em coluna ainda nao e confrontada com os campos
disponiveis/esperados.

## 14. Separacao V-13/V-14

```yaml
V_14:
  condicao: origem_ausente_ou_sem_valor_semantico
  coluna_reconhecida: true
  falha: V_14
  V_01_disparou: false

V_13_nivel:
  condicao: origem_declarada_mas_incompativel_com_estrutura
  coluna_reconhecida: true
  nivel_declarado: true
  nivel_existe: false
  falha: V_13
  V_14_disparou: false

V_13_campo:
  condicao: campo_declarado_mas_incompativel_com_estrutura_ou_dados
  coluna_reconhecida: true
  campo_declarado: true
  campo_compativel: false
  falha_observada: nenhuma
  V_14_disparou: false
```

Separacao conforme para `nivel`; incompleta para `campo`.

## 15. Lista Mista

```yaml
lista_mista:
  entrada_invalida: null
  coluna_valida: {identificador: x, titulo: X, campo: campo}
  comportamento_observado: aceita
  comportamento_normativo: nao_determinado_expressamente
  autoridade: "ADR-0028/contrato_json_console: V-01 rejeita tabela sem cabecalho; V-14 rejeita coluna sem origem"
  conforme: nao_bloqueante_para_QAPP5
```

Nao encontrei autoridade expressa que proiba lista de cabecalho contendo uma
entrada invalida quando ha ao menos uma coluna reconhecivel valida. Registro como
observacao nao corretiva nesta auditoria, pois os dois achados em escopo sao
decididos por evidencias independentes.

## 16. Itens Preservados

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

conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false

inventario_legado:
  total: 5

demo_json:
  carrega: true
  entradas: 11

recalibracoes_launcher:
  preservadas: true

regressao_H_0036:
  preservada: true
```

Nao reabri itens aprovados sem evidencia nova.

## 17. Relatorio IMP-0037

A secao 34 do relatorio de implementacao registra:

```yaml
qa_de_origem: sim
dois_achados_tratados: sim
autoridade_de_regra_geracao_itens: parcial
forma_interna_obrigatoria: nao
validade_de_objeto_vazio: declara_por_uso_em_fixtures_mas_nao_demonstra
exclusividades_estruturais: parcial
razao_demo_json_fora_D23: "presenca de regra_geracao_itens"
rejeicao_consumidores_hibridos: parcial
rejeicao_envelopes_incompletos: sim_sem_regra
V_13_por_nivel: sim
V_13_por_campo: declara_nao_implementado
compatibilidade_com_dados: parcial
separacao_V_13_V_14: parcial
decisao_lista_mista: nao_suficiente
fixtures_alteradas: sim
10_scripts: sim
2658_verificacoes: sim
zero_falhas: sim
git_diff_check: sim
stage_vazio: sim
ausencia_commit_push: sim
validacao_manual_pendente: sim
ausencia_autoaprovacao: sim
```

Conclusao: `RELATORIO_IMP_0037` e incorreto ao declarar o bypass eliminado e a
implementacao corrigida, pois a matriz adversarial refuta a isencao por
`regra_geracao_itens` e a completude de V-13 para `campo`.

## 18. Testes Focais

```yaml
- script: tela/teste_loader.py
  verificacoes: 476
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

## 19. Suite Independente

```yaml
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2658
  falhas: 0
  codigo_saida: todos_zero

scripts:
  tela/teste_loader.py: 476
  tela/teste_modelo.py: 186
  tela/teste_renderizador.py: 1223
  tela/teste_distribuicao_matricial.py: 36
  demo/teste_demo.py: 363
  demo/teste_diagnostico.py: 48
  demo/teste_demo_distribuicao.py: 109
  demo/teste_explorar_barra_de_menus.py: 38
  demo/teste_demo_console.py: 116
  demo/teste_demo_console_modos.py: 63
```

A suite verde nao substitui conformidade semantica.

## 20. Smoke Tecnico

Smoke tecnico seguro, sem aprovacao visual:

```yaml
h0037_console_nao_verboso: nao_verboso
h0037_console_verboso_dois_niveis: verboso
h0037_console_alternavel_tres_niveis: nao_verboso
h0037_console_tabela_alternavel: verboso
```

## 21. Validacao Manual

Permanece:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Nao simulei usuario, nao declarei aprovacao visual e nao criei relatorio de
validacao manual.

## 22. Achados

```yaml
- id: H0037-IMPL-QAPP5-001
  arquivo: tela/loader.py; tela/teste_loader.py
  funcao_ou_teste: _console_em_escopo_d23 / D23-P5 / fixtures com regra_geracao_itens={}
  evidencia: "tela/loader.py:1519-1530 retorna fora do D23 quando a chave regra_geracao_itens existe, sem validar tipo, campos internos, objeto vazio, null, coexistencia com itens ou envelope. Matriz adversarial pelo carregar_tela aceitou {}, null, string, lista, bool, numero, objetos incompletos, consumidor sem politica mais regra, regra+itens e regra+1..6 campos de envelope."
  autoridade: "contrato_console.md secao 3 e criterios de validacao; ADR-0028 D23; regra prioritaria desta auditoria"
  severidade: ALTA
  tipo: DEFEITO_IMPLEMENTACAO
  impacto: "Consumidor multinivel novo ainda contorna D23 adicionando uma chave regra_geracao_itens invalida ou vazia; testes mascaram o defeito ao adicionar {} em fixtures."
  correcao_exigida: "Validar a forma contratual de geracao interna antes de conceder isencao D23; rejeitar valores null/tipos incorretos/objetos incompletos e estruturas hibridas com itens, envelope ou consumidor multinivel."

- id: H0037-IMPL-QAPP5-002
  arquivo: tela/loader.py; docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  funcao_ou_teste: validar_conteudo_externo / V-13 de colunas por campo
  evidencia: "tela/loader.py:2139-2146 valida V-13 apenas para nivel. Matriz adversarial aceitou coluna com campo='nao_existe' e coluna com nivel valido + campo inexistente, apesar de origem declarada e incompativel."
  autoridade: "ADR-0028 V-13: dados incompativeis com a estrutura declarada sao invalidos; V-14 separa ausencia/sem valor da origem declarada"
  severidade: MEDIA
  tipo: DEFEITO_IMPLEMENTACAO
  impacto: "Origem por campo sintaticamente valida mas incompativel ainda passa; o achado H0037-IMPL-QAPP4-002 nao foi resolvido integralmente."
  correcao_exigida: "Implementar validacao V-13 equivalente para campo, distinguindo campo ausente/nulo/vazio (V-14) de campo declarado mas incompativel com estrutura/dados (V-13), ou registrar autoridade documental suficiente se a referencia livre for intencional."
```

## 23. Conclusao

O quinto patch corrigiu a rejeicao de 1 a 6 campos de envelope quando
`regra_geracao_itens` nao esta presente, preservou os modos iniciais e manteve a
suite canonica verde. Contudo, nao resolveu integralmente os dois achados de
origem.

O defeito central permanece: `regra_geracao_itens` e usada como discriminador por
mera presenca, sem validacao de forma e sem rejeicao de varias combinacoes
hibridas. Alem disso, a validacao V-13 foi adicionada para `nivel`, mas nao para
`campo`.

## 24. Status Literal

```text
IMPLEMENTATION_PATCH_REQUIRED
```

## 25. Status Normalizado

```text
patch_required
```

## 26. Proxima Categoria

```yaml
proxima_categoria: PATCH_IMPLEMENTACAO
```

## Saida Final Canonica

```yaml
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_required
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_5_H-0037_IMPLEMENTACAO.md
qa_anterior: docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0037_IMPLEMENTACAO.md
handoff: docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
relatorio_implementacao: docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md

git:
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
  stage: vazio
  diff_check: sem_erros
  commit_novo: inexistente
  push: nao_executado
  arquivos_do_quinto_patch:
    - tela/loader.py
    - tela/teste_loader.py
    - docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  arquivos_inesperados: presentes_na_worktree_acumulada_origem_NAO_CONFIRMADA

integridade:
  python: OK
  json: OK
  conflitos: ausentes
  temporarios: ausentes

regra_geracao_itens:
  forma_contratual: alternativa_a_itens_mas_schema_interno_nao_fechado
  objeto_vazio: aceito_incorretamente
  valor_null: aceito_incorretamente
  tipos_incorretos: aceitos_incorretamente
  objeto_incompleto: aceito_incorretamente
  consumidor_sem_politica: consegue_bypass
  consumidor_com_regra_valida: aceito_como_hibrido
  coexistencia_com_itens: aceita_incorretamente
  coexistencia_com_origem_dados: aceita
  coexistencia_com_envelope: aceita_incorretamente
  demo_json: carrega_mas_conformidade_da_regra_nao_comprovada
  bypass_remanescente: true
  conforme: false

D23:
  consumidor_sem_politica: rejeitado_sem_regra
  campos_isolados: rejeitados_sem_regra
  combinacoes_parciais: rejeitadas_sem_regra
  envelope_valido: aceito
  envelope_incompleto: rejeitado_sem_regra
  envelope_invalido: rejeitado_quando_completo
  cinco_legados: preservados
  conforme: false_por_bypass_com_regra

fixtures_modificadas: REGRESSAO_MASCARADA
V_01:
  preservado: true

V_13:
  nivel_inexistente: rejeitado
  campo_inexistente: aceito_incorretamente
  incompatibilidade_com_dados: parcial
  incompatibilidade_com_apresentacao: aceita_incorretamente
  causa_distinta: parcial
  conforme: false

V_14:
  origem_ausente: rejeitada
  origem_nula: rejeitada
  origem_vazia: rejeitada
  origem_whitespace: rejeitada
  tipo_incorreto: rejeitado
  causa_distinta: true
  conforme: true_para_origem_sem_valor

lista_mista: aceita_observacao_nao_bloqueante
itens_preservados: true
relatorio_IMP_0037: incorreto_por_declarar_resolucao_integral

testes_focais:
  scripts: 3
  verificacoes: 902
  falhas: 0
suite_declarada:
  scripts: 10
  verificacoes: 2658
  falhas: 0
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2658
  falhas: 0
smoke_tests: conforme_sem_aprovacao_visual
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

achados_bloqueantes:
  - H0037-IMPL-QAPP5-001
  - H0037-IMPL-QAPP5-002
achados_altos:
  - H0037-IMPL-QAPP5-001
achados_medios:
  - H0037-IMPL-QAPP5-002
achados_baixos: []
observacoes:
  - lista_mista_aceita_sem_autoridade_expressa_proibitiva
regressoes:
  - bypass_D23_por_regra_geracao_itens_invalida_ou_vazia
  - testes_com_regra_geracao_itens_objeto_vazio_mascaram_categoria_estrutural

implementacao_aprovada: false
proxima_categoria: PATCH_IMPLEMENTACAO
```
