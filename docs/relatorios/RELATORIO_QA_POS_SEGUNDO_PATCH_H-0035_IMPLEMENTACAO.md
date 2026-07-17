---
id: RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO
tipo: qa_implementacao
handoff: H-0035
rodada: POS_SEGUNDO_PATCH
data: 2026-07-16
status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: MANUAL_VALIDATION_REQUIRED
---

# RELATORIO QA POS SEGUNDO PATCH H-0035 IMPLEMENTACAO

## 1. Identificacao

Etapa executada: `QA_POS_PATCH`.

Rodada auditada: `POS_SEGUNDO_PATCH`.

Relatorio criado nesta etapa:

```text
docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO.md
```

Este QA nao corrigiu codigo, testes, JSONs, demos, contratos, ADRs, handoff,
relatorios anteriores ou relatorio de implementacao. Nenhum commit foi preparado
ou executado.

## 2. Objetivo

Reavaliar exclusivamente:

```text
QA-H0035-IMP-ALTO-001
QA-H0035-IMP-MEDIO-001
QA-H0035-POS-PATCH-BAIXO-001
```

Tambem foi confirmada a preservacao de:

```text
QA-H0035-IMP-BAIXO-001
```

## 3. Rodada

```yaml
rodada: POS_SEGUNDO_PATCH
retorno_declarado_do_patch:
  arquivos_alterados:
    - tela/renderizador.py
    - tela/teste_renderizador.py
    - docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
  arquivos_criados: []
  pytest_renderizador: 288 passed, 3 warnings
  script_renderizador: 1191 verificacoes
  suite_canonica_total: 2158
```

As declaracoes foram reavaliadas por leitura de codigo, instrumentacao e
execucao das provas obrigatorias.

## 4. Handoff

Handoff auditado:

```text
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Regra material aplicada: `minimo_fixo` excedido usa
`TRATAMENTO_INTERNO_DO_PARTICIPANTE`; a distribuicao externa nao pode selecionar,
reduzir ou descartar conteudo do participante. A area calculada e entregue ao
participante; a protecao fisica da area nao autoriza a camada matricial a criar
substring ou escolher caracteres sobreviventes.

## 5. QAs anteriores

QAs lidos integralmente:

```text
docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_IMPLEMENTACAO.md
```

O QA pos-primeiro-patch terminou com:

```yaml
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
achados_originais:
  QA-H0035-IMP-ALTO-001: NAO_CORRIGIDO
  QA-H0035-IMP-MEDIO-001: NAO_CORRIGIDO
  QA-H0035-IMP-BAIXO-001: CORRIGIDO
fluxo_do_conteudo:
  texto_integral_recebido_pelo_participante: false
  camada_que_descarta_caracteres: tela.renderizador._linhas_distribuicao_matricial
  truncamento_externo_equivalente: true
teste_minimo_fixo:
  prova_comportamental: false
  detecta_truncamento_equivalente: false
proxima_categoria: PATCH_IMPLEMENTACAO
```

## 6. Relatorio de implementacao

Relatorio auditado:

```text
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

A secao `43. Segundo patch de implementacao (SEGUNDO_PATCH)` registra a criacao
do helper `_renderizar_participante_na_celula`, a passagem de conteudo integral,
a reconciliacao do pytest focal (`288 passed`) e o total canonico de `2158`
verificacoes. A leitura do codigo e as execucoes atuais confirmam essas
declaracoes materiais.

## 7. Autoridades

Arquivos lidos e usados como criterio:

```text
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_HANDOFF.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_IMPLEMENTACAO.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_lancador.md
```

Dashboard fecha a regra de `minimo_fixo`; console e lancador remetem a essa
regra sem excecao.

## 8. Estado Git inicial

Comandos executados antes da criacao deste relatorio:

```text
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff --cached --name-only
```

Resultado material:

```yaml
arquivos_rastreados_modificados:
  - demo/teste_diagnostico.py
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_dashboard.md
  - docs/contratos/contrato_json_lancador.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
  - tela/loader.py
  - tela/modelo.py
  - tela/renderizador.py
  - tela/teste_loader.py
  - tela/teste_modelo.py
  - tela/teste_renderizador.py
arquivos_nao_rastreados_do_ciclo_H0035:
  - config/telas/demo/h0035_*.json
  - demo/demo_distribuicao.py
  - demo/teste_demo_distribuicao.py
  - docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
  - docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
  - docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_IMPLEMENTACAO.md
  - tela/distribuicao_matricial.py
  - tela/teste_distribuicao_matricial.py
arquivos_preexistentes_ou_origem_nao_confirmada:
  - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_H-0035_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
stage: vazio
git_diff_check: limpo
git_diff_cached: vazio
```

Para os itens de origem nao confirmada:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

## 9. Diff focal

Diff focal inspecionado integralmente:

```text
git diff -- tela/renderizador.py
git diff -- tela/teste_renderizador.py
```

Pontos materiais:

```yaml
tela/renderizador.py:
  helper_novo: _renderizar_participante_na_celula
  limite_cel_x_fim: localizado_no_helper
  funcao_matricial_percorre_caracteres: false
  funcao_matricial_cria_substring: false
  funcao_matricial_escreve_canvas_diretamente: false
  funcao_matricial_chama_helper: true
tela/teste_renderizador.py:
  teste_minimo_fixo_usa_espiao: true
  captura_conteudo_integral: true
  captura_largura_altura: true
  teste_direto_helper: true
  inspect_getsource: presente_com_papel_suplementar
```

## 10. Escopo

Escopo declarado do segundo patch:

```yaml
arquivos_alterados_declarados:
  - tela/renderizador.py
  - tela/teste_renderizador.py
  - docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
arquivos_criados_declarados: []
```

Confirmacao operacional: no estado Git atual ha muitos arquivos preexistentes
do ciclo H-0035 ja registrados pelos QAs anteriores. Nenhum arquivo novo
atribuivel ao segundo patch foi detectado. O novo relatorio deste QA nao conta
como arquivo do patch.

## 11. Reavaliacao do achado alto

```yaml
achado_original: QA-H0035-IMP-ALTO-001
resultado: CORRIGIDO
evidencia: >
  tela/renderizador.py:1259-1273 mostra _linhas_distribuicao_matricial
  chamando _renderizar_participante_na_celula com
  texto_integral=participantes[celula["participante"]] e largura/altura da
  celula. A funcao matricial nao itera caracteres, nao produz substring e nao
  escreve diretamente no canvas.
```

## 12. Fluxo do conteudo

Fluxo real observado:

```yaml
conteudo_original: ABCDEFGH
funcao_matricial: tela.renderizador._linhas_distribuicao_matricial
funcao_interna: tela.renderizador._renderizar_participante_na_celula
conteudo_passado_a_fronteira: ABCDEFGH
area_passada:
  largura: 5
  altura: 1
resultado_visual_fisico: ABCDE
celula_vizinha_inalterada: true
```

O resultado visual fisico nao equivale a descarte pela camada matricial: o
conteudo integral chega ao helper junto com a area calculada.

## 13. Fronteira de responsabilidade

```yaml
funcao_matricial:
  recebe_participante: true
  recebe_conteudo_integral: true
  percorre_caracteres: false
  produz_substring: false
  descarta_caracteres: false
  escreve_diretamente_no_canvas: false
  chama_fronteira_interna: true
fronteira_interna:
  recebe_participante_ou_identidade: true
  recebe_conteudo_integral: true
  recebe_x: true
  recebe_y: true
  recebe_largura: true
  recebe_altura: true
  limita_escrita_a_area: true
  altera_geometria_externa: false
```

## 14. Analise semantica do helper

`_renderizar_participante_na_celula` nao e apenas extracao cosmetica. A
fronteira e observavel porque:

- a camada matricial entrega a string integral;
- o helper recebe area completa (`cel_x`, `cel_y`, `cel_w`, `cel_h`);
- a decisao de escrita fisica ocorre depois da distribuicao externa;
- o helper nao devolve substring a camada matricial;
- a camada matricial nao decide quais caracteres sobrevivem;
- o helper foi testado diretamente com canvas concreto.

```yaml
extracao_cosmetica: false
fronteira_semantica: true
```

## 15. Politica interna

O helper reutiliza a convencao existente do renderer: canvas de caracteres,
`alinhar_na_celula` e limite fisico de escrita. Ele nao cria quebra, rolagem,
paginacao, fallback interno, crescimento externo ou alteracao de conteudo.

```yaml
politica_nova_criada: false
protecao_fisica_contra_invasao: true
exige_I4_BLOCKED_DOCUMENTATION: false
```

## 16. Instrumentacao

Instrumentacao independente executada sem alterar arquivos:

```yaml
conteudo_passado_a_linhas_distribuicao: ABCDEFGH
conteudo_passado_a_fronteira_interna: ABCDEFGH
largura_passada: 5
altura_passada: 1
quantidade_de_chamadas: 1
participante_correspondente: c1 / ABCDEFGH
celula_vizinha_inalterada: true
formacao_valida: true
dimensao_externa_final:
  largura: 5
  altura: 1
saida_material:
  linha_conteudo: "ABCDE                                  "
```

## 17. Reavaliacao do achado medio

```yaml
achado_original: QA-H0035-IMP-MEDIO-001
resultado: CORRIGIDO
evidencia: >
  tela/teste_renderizador.py:10034-10114 usa espiao substituindo
  _renderizar_participante_na_celula, captura argumentos reais da chamada de
  producao e exige que o conteudo recebido seja exatamente "ABCDEFGH" e que a
  largura da celula seja 5.
```

A prova comportamental detecta o truncamento equivalente que escapou do primeiro
patch: se a camada matricial passar `texto[:5]` ou `"ABCDE"`, a assercao de
conteudo integral falha.

## 18. Teste com spy

```yaml
usa_spy_ou_equivalente: true
intercepta_funcao_realmente_chamada: true
captura_argumentos_reais: true
exige_exatamente_ABCDEFGH: true
falha_se_receber_ABCDE: true
exige_largura_5: true
exige_altura_1: true
falha_se_fronteira_nao_for_chamada: true
falha_se_bypass_substituir_helper: true
confirma_formacao_valida: true
confirma_ausencia_de_crescimento_externo: true
confirma_ausencia_de_invasao_vizinha: true
observacao: >
  O teste usa len(chamadas) >= 1; uma segunda chamada identica e idempotente
  nao seria detectada por esse criterio isolado, mas a instrumentacao atual
  observou exatamente 1 chamada e nao ha duplicacao visivel.
```

## 19. Teste direto do helper

`test_fronteira_interna_celula` usa canvas concreto 10x1, conteudo
`ABCDEFGH`, celula `x=0`, largura `5`, e confirma:

```yaml
canvas_concreto: true
coordenadas_verificadas: true
limite_fisico_verificado: true
celula_vizinha_verificada: true
nao_afirma_todo_conteudo_visivel: true
distingue_conteudo_recebido_de_conteudo_exibido: true
saida_material:
  primeira_celula: "ABCDE     "
  segunda_celula: "     XY   "
```

## 20. Mutacoes detectaveis

Avaliacao mental apoiada nas assercoes reais:

```yaml
mutacoes_detectadas:
  substring: true
  literal_reduzido: true
  bypass_da_fronteira: true
  escrita_direta_substitutiva: true
  crescimento_da_area: true
  invalidacao_da_formacao: true
  duplicacao:
    detecta_chamada_extra_idempotente: false
    detecta_duplicacao_visivel_de_participantes: true
  troca_de_participante:
    caso_minimo_1_participante: nao_aplicavel
    casos_multiplos_existentes: true
```

## 21. Papel do inspect.getsource

```yaml
inspect_getsource_presente: true
papel: suplementar
prova_principal: false
```

A prova principal e o spy comportamental. A inspecao textual de `[:cel_w]`
permanece apenas como protecao auxiliar.

## 22. Reavaliacao do achado baixo da rodada

```yaml
achado_original: QA-H0035-POS-PATCH-BAIXO-001
resultado: CORRIGIDO
evidencia: >
  O relatorio de implementacao registra o pytest focal atual como 288 passed,
  3 warnings. A execucao deste QA confirmou 288 passed, 3 warnings.
```

## 23. Preservacao da contagem de 31

```yaml
achado_original: QA-H0035-IMP-BAIXO-001
resultado: CORRIGIDO
arquivos_criados_reais: 31
composicao:
  codigo_demo_testes: 4
  configuracoes_json: 26
  relatorio_implementacao: 1
arquivo_adicional: nenhum
declaracao_material_atual_de_32_arquivos: ausente
```

## 24. Busca de residuos

Busca executada em `tela/renderizador.py`, `tela/teste_renderizador.py` e no
relatorio de implementacao para:

```text
[:cel_w]
cel_x_fim
cx <
break
continue
islice
texto[
substring
recorte
trunc
corte
ABCDEFGH
ABCDE
inspect.getsource
289 passed
288 passed
287 passed
1184
1186
1191
31 arquivos
32 arquivos
```

Classificacao material:

```yaml
distribuicao_matricial_externa:
  - "_linhas_distribuicao_matricial contem chamada ao helper e nao contem [:cel_w], cx <, substring ou loop de caracteres."
fronteira_interna:
  - "_renderizar_participante_na_celula contem cel_x_fim e cx < cel_x_fim como protecao fisica."
prova_comportamental:
  - "ABCDEFGH, ABCDE e inspect.getsource aparecem nos testes H0035."
protecao_suplementar:
  - "inspect.getsource e [:cel_w] aparecem como guarda auxiliar."
resultado_atual:
  - "288 passed e 1191 verificacoes aparecem na secao 43 do relatorio de implementacao e foram confirmados."
registro_historico:
  - "287 passed, 1184, 1186, 32 arquivos, texto[:cel_w] e cx < cel_x_fim aparecem no historico do primeiro patch/QA."
residuo_contraditorio: nenhum_material
```

## 25. Testes focais

```yaml
pytest_renderizador:
  comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py -q --tb=short
  exit_code: 0
  collected: 288
  passed: 288
  failed: 0
  skipped: 0
  warnings: 3
  saida_material: "288 passed, 3 warnings in 0.27s"
focal_distribuicao:
  comando: PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
  exit_code: 0
  passed_ou_verificacoes: 36
  falhas: 0
  warnings: 0
  saida_material: "Total de verificacoes: 36; Passaram: 36; Falharam: 0"
renderizador_completo:
  comando: PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
  exit_code: 0
  passed_ou_verificacoes: 1191
  falhas: 0
  warnings: 0
  saida_material: "Total de verificacoes: 1191; Passaram: 1191; Falharam: 0"
```

## 26. Suite canonica

Oito scripts executados da raiz:

```yaml
tela/teste_loader.py: 303
tela/teste_modelo.py: 169
tela/teste_renderizador.py: 1191
tela/teste_distribuicao_matricial.py: 36
demo/teste_demo.py: 358
demo/teste_diagnostico.py: 41
demo/teste_demo_distribuicao.py: 22
demo/teste_explorar_barra_de_menus.py: 38
total: 2158
falhas: 0
```

## 27. Contagens

```yaml
pytest_renderizador:
  casos_pytest: 288
  warnings: 3
script_renderizador:
  verificacoes_internas: 1191
suite_canonica:
  scripts: 8
  verificacoes_internas: 2158
falhas_totais: 0
```

O pytest focal mede casos coletados; os scripts proprios medem verificacoes
internas registradas.

## 28. Smoke

Comando executado:

```text
PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
```

Resultado:

```yaml
exit_code: 0
identidade_material: "nome=h0035_catalogo familia=(sem distribuicao_matricial) formacao=(n/a) ordem=(n/a) consumidor=lancador estado=normal"
smoke: PASS
```

## 29. Identidade semantica

Confirmada no smoke e em `demo/teste_demo_distribuicao.py`:

```yaml
nome: h0035_catalogo
consumidor: lancador
estado: normal
familias_testadas:
  - preferencia_colunas
  - matriz_fixa
  - lancador
  - console
  - quadro_minimo
```

## 30. Regressoes

Suites e smoke confirmaram ausencia de regressao automatizada em:

```text
ausencia de distribuicao_matricial
dashboard
console
lancador
ordem dos participantes
formacao
margens
vaos
alinhamento
restos
fallback
recuperacao
pseudo-TTY
demo
diagnostico
JSONs existentes
separacao de H-0034
```

## 31. Validacao manual

```yaml
status: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
metodo_reproduzivel: PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
```

Este QA nao realizou validacao visual em nome do usuario. Como os achados
tecnicos da rodada foram corrigidos e a suite esta verde, a unica pendencia
remanescente e a observacao humana em TTY real.

## 32. Estado Git final

Comandos executados apos criar este relatorio:

```text
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff --cached --name-only
git diff --no-index --check /dev/null docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO.md
```

Resultado material:

```yaml
arquivo_criado_por_esta_etapa:
  - docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO.md
codigo_testes_jsons_demos_alterados_pelo_QA: false
relatorio_implementacao_alterado_pelo_QA: false
stage: vazio
commit: nao_realizado
git_diff_check: limpo
git_diff_cached: vazio
git_diff_no_index_check_relatorio:
  exit_code: 1
  saida_material: vazia
  interpretacao: diferenca_contra_dev_null_sem_erro_de_whitespace
temporarios_novos_no_status: nenhum
```

## 33. Achados

```yaml
achados_bloqueantes: []
achados_altos: []
achados_medios: []
achados_baixos: []
achados_originais:
  QA-H0035-IMP-ALTO-001:
    resultado: CORRIGIDO
    evidencia: "_linhas_distribuicao_matricial entrega conteudo integral e area ao helper, sem loop de caracteres ou substring."
  QA-H0035-IMP-MEDIO-001:
    resultado: CORRIGIDO
    evidencia: "teste com spy captura chamada real ao helper e exige ABCDEFGH, largura 5 e formacao valida."
  QA-H0035-POS-PATCH-BAIXO-001:
    resultado: CORRIGIDO
    evidencia: "pytest focal atual confirmado como 288 passed, 3 warnings."
  QA-H0035-IMP-BAIXO-001:
    resultado: CORRIGIDO
    evidencia: "contagem real preservada em 31 arquivos criados; nao ha declaracao material atual de 32."
```

## 34. Observacoes

```yaml
observacoes:
  - "A protecao cx < cel_x_fim permanece, mas agora esta na fronteira interna, que recebe conteudo integral e area calculada."
  - "O teste com spy usa len(chamadas) >= 1; a chamada extra idempotente nao e detectada isoladamente, mas a instrumentacao independente observou exatamente 1 chamada."
  - "Ocorrencias antigas de 287 passed, 1184, 1186, texto[:cel_w] e 32 arquivos estao no historico do relatorio de implementacao, nao como resultado atual."
decisoes_ausentes: 0
contradicoes_documentais: 0
```

## 35. Conclusao

O segundo patch corrigiu a fronteira material: a camada matricial nao seleciona
mais caracteres visiveis e nao escreve diretamente versao reduzida no canvas.
Ela chama a fronteira interna com o conteudo integral do participante e a area
calculada. A protecao de escrita fisica fica no helper, sem criar politica nova
de truncamento, quebra, rolagem, paginacao, crescimento externo ou fallback
interno.

Os testes focais, a suite canonica e o smoke passaram. A validacao manual em
TTY real permanece pendente do usuario.

## 36. Status literal

```text
I5_MANUAL_VALIDATION_REQUIRED
```

## 37. Status normalizado

```text
MANUAL_VALIDATION_REQUIRED
```

## 38. Proxima categoria

```text
VALIDACAO_MANUAL
```

## 39. Saida final consolidada

```yaml
etapa_executada: QA_POS_PATCH
rodada: POS_SEGUNDO_PATCH
handoff: H-0035
status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: MANUAL_VALIDATION_REQUIRED

qa_inicial: docs/relatorios/RELATORIO_QA_H-0035_IMPLEMENTACAO.md
qa_pos_primeiro_patch: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0035_IMPLEMENTACAO.md
relatorio_implementacao: docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
relatorio: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO.md

achados_originais:
  QA-H0035-IMP-ALTO-001:
    resultado: CORRIGIDO
    evidencia: conteudo integral entregue ao helper; camada matricial sem substring, sem loop de caracteres e sem escrita direta
  QA-H0035-IMP-MEDIO-001:
    resultado: CORRIGIDO
    evidencia: spy intercepta helper real e exige ABCDEFGH, largura 5 e formacao valida
  QA-H0035-POS-PATCH-BAIXO-001:
    resultado: CORRIGIDO
    evidencia: pytest focal atual confirmado como 288 passed, 3 warnings
  QA-H0035-IMP-BAIXO-001:
    resultado: CORRIGIDO
    evidencia: arquivos criados reais permanecem 31; nenhum arquivo adicional

fronteira:
  funcao_matricial: _linhas_distribuicao_matricial
  funcao_interna: _renderizar_participante_na_celula
  extracao_cosmetica: false
  conteudo_integral_recebido: true
  area_recebida:
    largura: 5
    altura: 1
  camada_que_limita_escrita: _renderizar_participante_na_celula
  politica_nova_criada: false

teste_comportamental:
  spy_realmente_intercepta_producao: true
  conteudo_esperado: ABCDEFGH
  conteudo_observado: ABCDEFGH
  area_observada:
    largura: 5
    altura: 1
  detecta_substring: true
  detecta_bypass: true
  detecta_escrita_direta: true
  detecta_duplicacao: parcial_para_chamada_extra_idempotente
  inspect_getsource_apenas_auxiliar: true

pytest_renderizador:
  collected: 288
  passed: 288
  failed: 0
  warnings: 3

suite_canonica:
  scripts_esperados: 8
  scripts_executados: 8
  total_verificacoes: 2158
  falhas: 0

contagem_arquivos_criados:
  real: 31
  relatorio_correto: true

smoke:
  exit_code: 0
  identidade: nome=h0035_catalogo consumidor=lancador estado=normal
identidade_semantica: confirmada
regressoes: nao_observadas_automaticamente

validacao_manual:
  status: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
  metodo_reproduzivel: PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py

achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes:
  - chamada extra idempotente do helper nao e detectada isoladamente pelo len(chamadas) >= 1
decisoes_ausentes: 0
contradicoes_documentais: 0
arquivos_criados_ou_alterados:
  - docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0035_IMPLEMENTACAO.md
git:
  stage: vazio
  commit: nao_realizado
proxima_categoria: VALIDACAO_MANUAL
```
