---
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_required
historia: H-0037
tipo: QA_POS_PATCH_IMPLEMENTACAO
patch_auditado: quarto_patch_pos_QA
data: 2026-07-19
---

# RELATORIO QA POS PATCH 4 H-0037 IMPLEMENTACAO

## 1. Identificacao

Auditoria tecnica independente do quarto patch focal da implementacao H-0037.

Resultado: `IMPLEMENTATION_PATCH_REQUIRED`.

## 2. Objetivo

Determinar se o quarto patch resolveu integralmente:

- `H0037-IMPL-QAPP3-001`
- `H0037-IMPL-QAPP3-002`

A regra prioritaria auditada foi: envelope parcial sem marcadores D23 retorna
fora do escopo somente se isso nao permitir a uma tela consumidora multinivel
contornar a obrigacao de declarar `politica_modo`.

## 3. Autoridades

Artefatos obrigatorios consultados:

- `docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0037_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0037_IMPLEMENTACAO.md`
- `docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
- `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md`
- `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`

Autoridades decisivas:

- ADR-0028 D23: telas novas/revisadas consumidoras de conteudo multinivel devem
  declarar `politica_modo`; nao ha default implicito por ausencia do bloco.
- `contrato_json_console.md`: envelope historico tem forma contratual propria;
  V-14 invalida coluna de tabela sem nivel ou campo de origem.
- QA anterior: o patch so pode ser aprovado se a isencao de envelope nao
  permitir bypass D23 por consumidor multinivel.

## 4. Estado Git

```yaml
branch: master
head: f6982d08640af1762b8e0e8814b6e90c9421538e
head_log: "f6982d0 docs: corrige whitespace do fechamento H-0036"
stage: vazio
commit_novo: inexistente
push: inexistente
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

Arquivos nao rastreados incluem os JSONs H-0037, `demo/teste_demo_console_modos.py`,
ADR/handoff/relatorios H-0037/ADR-0028 e artefatos transitorios `__pycache__`.

Itens inesperados/transitorios:

```yaml
arquivo: tela/__pycache__/
origem: NAO_CONFIRMADA
produzido_pelo_quarto_patch: NAO_CONFIRMADO
arquivo: demo/__pycache__/
origem: NAO_CONFIRMADA
produzido_pelo_quarto_patch: NAO_CONFIRMADO
```

## 5. Escopo do Quarto Patch

A secao 33 do relatorio IMP declara alteracao no quarto patch em:

```text
tela/loader.py
tela/teste_loader.py
demo/demo.py
demo/teste_demo_console_modos.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

O diff acumulado contem outros arquivos tecnicos e documentais de H-0037/ADR-0028.
Nao ha base suficiente, so pelo estado Git, para atribuir todos eles ao quarto
patch. Classificacao dos adicionais: `origem: NAO_CONFIRMADA`;
`produzido_pelo_quarto_patch: NAO_CONFIRMADO`.

## 6. Integridade

```yaml
python_ast_parse:
  arquivos: 7
  resultado: OK
json_loads:
  arquivos: 8
  resultado: OK
conflitos:
  marcadores_git_reais: ausentes
  observacao: "rg encontrou linhas separadoras ======= em comentarios/relatorios, nao marcadores de conflito completos"
temporarios:
  __pycache__: presentes
  pyc: presentes
  tmp_bak_swp_tilde: ausentes
whitespace:
  git_diff_check: sem_erros
```

## 7. Funcao de Validacao do Envelope

`_validar_valores_envelope_pre_adr_0028(elemento)` fica em `tela/loader.py` e e
chamada por `_console_em_escopo_d23` apenas quando os sete campos do envelope
estao presentes.

Parametros: `elemento`.

Retorno: sem retorno material; levanta `TelaEstruturaInvalida` em invalidade.

Excecoes: `TelaEstruturaInvalida`.

Momento de chamada: antes de `_console_em_escopo_d23` retornar `False` para
envelope completo e conceder isencao D23.

## 8. Sete Campos

```yaml
itens:
  tipo_aceito: list
origem_dados:
  tipo_aceito: dict ou null
politica_composicao:
  tipo_aceito: dict
politica_navegacao:
  tipo_aceito: dict
politica_selecao:
  tipo_aceito: string
  valores: [multipla, nenhuma, unica]
politica_paginacao:
  tipo_aceito: string
  valores: [com, sem]
politica_exibicao:
  tipo_aceito: dict
```

Observacao normativa: `origem_dados: null` e aceito pelo contrato local e pela
funcao. Portanto o caso "cada campo null" nao rejeita esse campo isoladamente.

## 9. Envelope Completo

Matriz executada pelo carregador real:

```yaml
validacao_envelope:
  sete_chaves_validas: aceita
  sete_chaves_null: rejeita
  cada_campo_null:
    itens: rejeita
    origem_dados: aceita
    politica_composicao: rejeita
    politica_navegacao: rejeita
    politica_selecao: rejeita
    politica_paginacao: rejeita
    politica_exibicao: rejeita
  cada_tipo_incorreto: rejeita
  politicas_desconhecidas: rejeita
  objetos_incompletos: nao_comprovado_completamente
  sete_chaves_invalidas_recebem_isencao: false
  conforme: parcial
```

O defeito anterior dos sete campos todos invalidos foi corrigido para o caso
`all_null`, tipos incorretos e politicas desconhecidas.

## 10. Envelope Parcial

Resultado adversarial independente pelo carregador real:

```yaml
envelope_parcial:
  significado_de_false: "fora do D23 e sem validacao posterior do envelope parcial"
  validacao_posterior_existe: false
  consumidor_pode_contornar_D23: true
  envelope_incompleto_pode_ser_aceito: true
  demo_json_excluido_por_tipo_real: false
  exclusao_depende_apenas_de_cardinalidade: true
  bypass_remanescente: true
  conforme: false
```

Evidencia:

- consumidor puro sem `politica_modo`: rejeitado por D23;
- mesmo consumidor com cada um dos sete campos isolados: aceito;
- mesmo consumidor com 2, 3, 4, 5 ou 6 campos: aceito;
- parcial + `politica_modo`: rejeitado como hibrido.

Isso refuta a regra prioritaria do prompt: uma tela consumidora nova consegue
contornar D23 apenas acrescentando campo de envelope parcial e omitindo
`politica_modo`.

## 11. Estrutura Hibrida

```yaml
envelope_completo_mais_politica_modo: rejeita
campo_isolado_mais_politica_modo: rejeita
seis_campos_mais_politica_modo: rejeita
conforme: true
```

## 12. demo.json

`config/telas/demo/demo.json` carrega integralmente pelo loader real.

```yaml
elementos_corpo: 3
lancador_itens: 11
entradas_H_0037:
  - h0037_console_nao_verboso
  - h0037_console_verboso_dois_niveis
  - h0037_console_alternavel_tres_niveis
  - h0037_console_tabela_alternavel
console_principal:
  tipo: console
  campos_envelope_presentes:
    - origem_dados
    - politica_composicao
    - politica_navegacao
    - politica_selecao
    - politica_paginacao
    - politica_exibicao
  itens: ausente
  formato: ausente
```

A regressao do `demo.json` foi removida, mas por regra ampla de cardinalidade
1..6 e nao por prova estrutural robusta de que o elemento real nao e consumidor
multinivel.

## 13. Classificacao D23

```yaml
classificacao_separada_da_validacao: parcial
identifica_forma_candidata: "conta campos do envelope e detecta marcadores D23"
validacao: "valida valores somente quando os 7 campos estao presentes"
decisao_D23: "retorna False para 1..6 campos sem D23 antes de validacao estrutural posterior"
conforme: false
```

## 14. Modo somente_verboso

```yaml
somente_nao_verboso: false
somente_verboso: true
alternavel_com_modo_inicial_nao_verboso: false
alternavel_com_modo_inicial_verboso: true
```

Ponto de entrada/smoke tecnico:

```yaml
h0037_console_nao_verboso: nao_verboso
h0037_console_verboso_dois_niveis: verboso
h0037_console_alternavel_tres_niveis: nao_verboso
h0037_console_tabela_alternavel: verboso
```

`V` e inerte nas telas fixas; chip ausente nas fixas; troca de tela recalcula o
modo inicial do modelo. O teste focal agora espera `True` para
`h0037_console_verboso_dois_niveis`.

## 15. V-14

Matriz independente:

```yaml
origem_ausente: rejeita_V_14
campo_null: rejeita_V_14
campo_vazio: rejeita_V_14
campo_whitespace: rejeita_V_14
campo_tipo_incorreto: rejeita_V_14
nivel_null: rejeita_V_14
nivel_vazio: rejeita_V_14
nivel_whitespace: rejeita_V_14
nivel_tipo_incorreto: rejeita_V_14
origem_incompativel_com_estrutura:
  observado: aceita
  conforme: false
campo_valido: aceita
nivel_valido: aceita
duas_colunas_validas: aceita
titulo_valido_com_origem_vazia: rejeita_V_14
causa_distinta_de_V_01: true
ultrapassa_V_01: true
conforme: parcial
```

A causa para nulos/vazios/whitespace/tipo incorreto e V-14, nao V-01.

## 16. Lista Mista

```yaml
lista_mista:
  comportamento: "entrada invalida + coluna valida em formato.tabela.colunas rejeita na primeira entrada invalida"
  autoridade: "contrato_json_console.md V-14; ADR-0028 V-14"
  conforme: true
```

Observacao: a lista mista em `formato.tabela.cabecalho` permanece aceita quando
ha ao menos uma coluna reconhecivel, conforme comportamento ja registrado no QA
anterior como observacao de risco sem bloqueio independente.

## 17. Testes Modificados

```yaml
- teste: "D23-P3-05/06 campo isolado sem marcadores D23 aceito"
  arquivo: tela/teste_loader.py
  regra: envelope parcial
  entrada: consumidor sem politica + um campo de envelope
  esperado_pelo_teste: aceita
  observado_QA: aceita
  passa_pelo_carregador_real: true
  testa_apenas_funcao_privada: false
  conforme: false

- teste: "D23-P3-09 envelope parcial 6/7 sem marcadores D23 aceito"
  arquivo: tela/teste_loader.py
  regra: envelope incompleto
  entrada: seis campos de envelope sem politica_modo
  esperado_pelo_teste: aceita
  observado_QA: aceita
  passa_pelo_carregador_real: true
  testa_apenas_funcao_privada: false
  conforme: false

- teste: "D23-P4-01..04 validacao de envelope completo"
  arquivo: tela/teste_loader.py
  regra: valores dos sete campos
  entrada: all_null, tipo errado, politica desconhecida
  esperado: rejeita
  observado: rejeita
  passa_pelo_carregador_real: true
  testa_apenas_funcao_privada: false
  conforme: true

- teste: "D23-P4-05/06 hibridos"
  arquivo: tela/teste_loader.py
  regra: envelope parcial/completo + D23
  entrada: campos de envelope + politica_modo
  esperado: rejeita
  observado: rejeita
  passa_pelo_carregador_real: true
  testa_apenas_funcao_privada: false
  conforme: true

- teste: "V-14 semantica"
  arquivo: tela/teste_loader.py
  regra: origem semanticamente vazia
  entrada: null, vazio, whitespace
  esperado: rejeita
  observado: rejeita
  passa_pelo_carregador_real: true
  testa_apenas_funcao_privada: false
  conforme: parcial
  lacunas: "nao cobre tipo incorreto nem origem incompativel"

- teste: "teste_modo_verboso_inicial cenario 2"
  arquivo: demo/teste_demo_console_modos.py
  regra: somente_verboso abre verboso
  entrada: h0037_console_verboso_dois_niveis
  esperado: true
  observado: true
  passa_pelo_carregador_real: true
  testa_apenas_funcao_privada: false
  conforme: true
```

## 18. Itens Preservados

```yaml
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
  ids:
    - h0035_console_com
    - h0035_console_sem
    - h0036_console_hierarquia
    - h0036_console_tabela
    - h0036_console_conjuntos
recalibracoes_launcher:
  preservadas: true
regressao_H_0036:
  preservada: true
```

## 19. Relatorio IMP-0037

A secao 33 registra corretamente a origem QA, os dois achados tratados, a funcao
nova, a correcao de `somente_verboso`, os testes adicionados, 10 scripts, 2.645
verificacoes, zero falhas, stage vazio e validacao manual pendente.

Nao esta conforme semanticamente porque declara que envelope parcial sem D23
"nao isenta D23" e "simplesmente nao e consumidor multinivel", mas o carregador
real aceita consumidor novo sem `politica_modo` quando recebe 1 a 6 campos de
envelope.

## 20. Testes Focais

```yaml
- script: tela/teste_loader.py
  verificacoes: 463
  falhas: 0
  codigo_saida: 0
- script: tela/teste_modelo.py
  verificacoes: 186
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

## 21. Suite Independente

```yaml
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2645
  falhas: 0
  codigo_saida: 0
por_script:
  tela/teste_loader.py: {verificacoes: 463, falhas: 0, codigo_saida: 0}
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

## 22. Smoke Tecnico

```yaml
h0037_console_nao_verboso: nao_verboso
h0037_console_verboso_dois_niveis: verboso
h0037_console_alternavel_tres_niveis: nao_verboso
h0037_console_tabela_alternavel: verboso
```

Nao houve aprovacao visual.

## 23. Validacao Manual

Permanece:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Nao foi executada validacao manual em nome do usuario.

## 24. Achados

```yaml
- id: H0037-IMPL-QAPP4-001
  arquivo: tela/loader.py
  funcao_ou_teste: "_console_em_escopo_d23 / carregar_tela / tela/teste_loader.py D23-P3-05..09"
  evidencia: "Consumidor novo sem politica_modo e sem campos de envelope e rejeitado; o mesmo consumidor com cada campo isolado de envelope e aceito; combinacoes de 2 a 6 campos tambem sao aceitas. A funcao retorna False em tela/loader.py:1526, e os testes em tela/teste_loader.py:3356 esperam essa aceitacao."
  autoridade: "ADR-0028 D23; contrato_json_console.md D23; QA_POS_PATCH_3 H0037-IMPL-QAPP3-001; regra prioritaria do prompt"
  severidade: ALTA
  tipo: DEFEITO_IMPLEMENTACAO
  impacto: "Tela consumidora multinivel nova consegue contornar a obrigacao de declarar politica_modo adicionando 1 a 6 campos de envelope, sem validacao posterior."
  correcao_exigida: "Separar o elemento real de demo.json por tipo/contrato estrutural efetivo, sem tornar 1..6 campos uma isencao generica; consumidor novo sem politica_modo deve continuar rejeitado."

- id: H0037-IMPL-QAPP4-002
  arquivo: tela/loader.py; tela/teste_loader.py
  funcao_ou_teste: "validar_conteudo_externo / V-14"
  evidencia: "A matriz adversarial rejeita null/vazio/whitespace/tipo incorreto por V-14, mas aceita coluna com nivel='inexistente'. Os testes modificados cobrem null/vazio/whitespace, mas nao tipo incorreto nem origem incompatível."
  autoridade: "ADR-0028 V-14: coluna de tabela sem nivel ou campo de origem e invalida; matriz obrigatoria deste QA"
  severidade: MEDIA
  tipo: DEFEITO_IMPLEMENTACAO
  impacto: "Origem declarada mas incompativel com a estrutura pode passar como valida."
  correcao_exigida: "Validar a compatibilidade de nivel/campo de coluna com a estrutura declarada, ou registrar autoridade documental expressa para aceitar referencia externa/livre."
```

## 25. Conclusao

O quarto patch resolveu a validacao basica dos sete campos completos, a
regressao operacional do `demo.json`, o modo inicial `somente_verboso` e a
rejeicao V-14 de valores nulos/vazios/whitespace/tipos incorretos.

Porem nao resolveu integralmente `H0037-IMPL-QAPP3-001`: a regra nova de
envelope parcial cria bypass D23. A suite verde nao substitui a conformidade
semantica.

## 26. Status Literal

```text
IMPLEMENTATION_PATCH_REQUIRED
```

## 27. Status Normalizado

```text
patch_required
```

## 28. Proxima Categoria

```yaml
proxima_categoria: PATCH_IMPLEMENTACAO
```

## Saida Final

```yaml
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_required
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0037_IMPLEMENTACAO.md
qa_anterior: docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0037_IMPLEMENTACAO.md
handoff: docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
relatorio_implementacao: docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md

git:
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
  stage: vazio
  diff_check: sem_erros
  commit_novo: inexistente
  push: inexistente
  arquivos_do_quarto_patch:
    - tela/loader.py
    - tela/teste_loader.py
    - demo/demo.py
    - demo/teste_demo_console_modos.py
    - docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  arquivos_inesperados:
    - arquivo: tela/__pycache__/
      origem: NAO_CONFIRMADA
      produzido_pelo_quarto_patch: NAO_CONFIRMADO
    - arquivo: demo/__pycache__/
      origem: NAO_CONFIRMADA
      produzido_pelo_quarto_patch: NAO_CONFIRMADO

integridade:
  python: OK
  json: OK
  conflitos: sem_marcadores_git_reais
  temporarios: presentes

D23:
  classificacao_separada_da_validacao: parcial
  sete_campos: validados_quando_completos
  envelope_valido: aceita
  sete_campos_null: rejeita
  cada_campo_null: parcial_origem_dados_null_aceita_por_contrato
  cada_tipo_incorreto: rejeita
  politicas_desconhecidas: rejeita
  objetos_incompletos: nao_comprovado_completamente
  consumidor_sem_politica: rejeita_quando_sem_campos_envelope
  campos_isolados: aceita_incorretamente
  combinacoes_parciais: aceita_incorretamente
  envelope_incompleto: aceita_incorretamente
  estrutura_hibrida: rejeita
  demo_json: carrega
  elemento_demo_tipo_real: console_pre_ADR_0028_parcial_sem_formato
  elementos_fora_do_escopo: dependem_de_cardinalidade_1_a_6
  cinco_legados: preservados
  bypass_remanescente: true
  conforme: false

modo_inicial:
  somente_nao_verboso: false
  somente_verboso: true
  alternavel_tres_niveis: false
  tabela_alternavel: true
  tecla_V_fixas: inerte
  teste_focal: conforme

V_01:
  preservado: true

V_14:
  origem_ausente: rejeita_V_14
  origem_nula: rejeita_V_14
  origem_vazia: rejeita_V_14
  origem_whitespace: rejeita_V_14
  tipo_incorreto: rejeita_V_14
  causa_distinta: true
  ultrapassa_V_01: true
  lista_mista: rejeita_em_colunas
  conforme: parcial

testes_modificados: parcial
itens_preservados: true
relatorio_IMP_0037: incorreto_por_autoavaliar_regra_parcial

testes_focais:
  scripts: 4
  verificacoes: 1075
  falhas: 0
suite_declarada:
  scripts: 10
  verificacoes: 2645
  falhas: 0
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2645
  falhas: 0
smoke_tests: conforme
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

achados_bloqueantes:
  - H0037-IMPL-QAPP4-001
achados_altos:
  - H0037-IMPL-QAPP4-001
achados_medios:
  - H0037-IMPL-QAPP4-002
achados_baixos: []
observacoes:
  - "suite verde nao cobre o bypass parcial"
regressoes:
  - "bypass D23 por 1 a 6 campos de envelope"

implementacao_aprovada: false
proxima_categoria: PATCH_IMPLEMENTACAO
```
