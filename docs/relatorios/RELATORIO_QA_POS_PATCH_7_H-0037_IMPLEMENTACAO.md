---
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_required
historia: H-0037
tipo: QA_POS_PATCH_IMPLEMENTACAO
patch_auditado: setimo_patch_pos_validacao_manual
data: 2026-07-20
---

# RELATORIO QA POS PATCH 7 H-0037 IMPLEMENTACAO

## 1. Identificacao

Auditoria tecnica independente do patch focal decorrente da validacao manual
reprovada de H-0037.

Resultado: `IMPLEMENTATION_PATCH_REQUIRED`.

## 2. Objetivo

Auditar exclusivamente as correcoes declaradas para:

- `H0037-MANUAL-001`: marcador `...` ausente no truncamento.
- `H0037-MANUAL-002`: chip `[Esc]` fora da primeira posicao.
- `H0037-MANUAL-003`: tecla `v` minuscula nao alternava.

Nao foi executada revalidacao manual em nome do usuario.

## 3. Autoridades

Arquivos obrigatorios lidos integralmente:

```yaml
docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md:
  linhas: 461
  sha256: d0ca640316b3a703d582da6098bea17c69ce140b374c9b90b7764256965d157f
docs/relatorios/RELATORIO_QA_POS_PATCH_6_H-0037_IMPLEMENTACAO.md:
  linhas: 804
  sha256: 7b7fb65e29b4342cf1a871ba66c67c5aae5537efa6c90ed18d3b85c98bc2e76a
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md:
  linhas: 1975
  sha256: edffa690dc5c657a625dd58330ea78f8c54215b7a50e0e57349f96f8e2dae872
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md:
  linhas: 1718
  sha256: 09ead8c9ea740f606caa4dfcf199f1321c8baffe7ed83803d7ceaa6250d7159d
docs/contratos/contrato_console.md:
  linhas: 839
  sha256: de79c1a3b3986ea6af8c8b8b590c6cbe233dfb61d024735d9471be218a786733
docs/contratos/contrato_barra_de_menus.md:
  linhas: 827
  sha256: 7dfc62f7d0bbfcfb38eefdaa4b115629533ab1be32817762b9d2bf67f45c91e9
docs/contratos/contrato_json_console.md:
  linhas: 1258
  sha256: cacba69f9e29ee60a42470e6f6b283ed1a4c3546615b33f8578874ca6013096b
docs/contratos/contrato_composicao_corpo.md:
  linhas: 1947
  sha256: df3a25df0a10e7761c8a2738825cc57cfe226cf9e96a605c0baf553a7f6e807b
tela/renderizador.py:
  linhas: 2590
  sha256: 41f1f2bfc1228e452e000ed08b933a78c9c8fed37bd3e3a41f9f39156538170a
tela/teste_renderizador.py:
  linhas: 10667
  sha256: cff2261baa61e027277212610d9197ca9ba3e61af778995a9e48a86d8dfff86b
demo/demo.py:
  linhas: 773
  sha256: c4bf7012462bcc7b144746ce7526bc6eb03f11639135f34c1df2d3fa1ef1c38d
demo/teste_demo.py:
  linhas: 3303
  sha256: df6a02e45f238abe37ab0c64278dd8513ccde5a1dd6c79c69cc747141e9ea3a0
demo/teste_demo_console_modos.py:
  linhas: 549
  sha256: 78dcfac78473194ae47c2ddfc1593b8623c206bbb8fa1428b1b90ec19af7dfda
demo/teste_explorar_barra_de_menus.py:
  linhas: 610
  sha256: 649e8841bfa16914071542703b0e5fe2b63f8227bf03f5ff7a7017bcefec8669
```

Autoridades decisivas nesta rodada:

- `RELATORIO_VALIDACAO_MANUAL_H-0037.md`: tres achados manuais em TTY real.
- `contrato_console.md`: modo nao verboso com truncamento marcado e modo
  verboso sem marcador artificial.
- `contrato_barra_de_menus.md`: `[Esc]` primeiro quando declarado.
- `IMP-0037`, secao 36: patch focal e suite declarada.

## 4. Estado Git

Comandos obrigatorios executados na raiz real:

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

Arquivos declarados pelo patch:

```text
tela/renderizador.py
tela/teste_renderizador.py
demo/demo.py
demo/teste_demo_console_modos.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Arquivos fora do escopo presentes na worktree acumulada:

```text
config/telas/demo/demo.json
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
tela/teste_loader.py
tela/teste_modelo.py
arquivos H-0037/ADR-0028 nao rastreados acumulados
```

Nao ha evidencia suficiente para atribuir origem dessas alteracoes acumuladas
ao patch focal auditado.

## 5. Escopo Do Patch

O diff dos cinco arquivos declarados foi inspecionado. Em arquivos nao
rastreados, a inspecao foi feita pelo conteudo integral do arquivo, pois
`git diff` normal nao mostra arquivos untracked.

Alteracoes focais confirmadas:

```yaml
tela/renderizador.py:
  - adiciona _truncar_com_marcador
  - integra truncamento em hierarquia, tabela e conjuntos
  - adiciona _garantir_esc_primeiro
  - chama _garantir_esc_primeiro dentro de _linhas_barra
demo/demo.py:
  - processar_comando passa a aceitar comando in ("V", "v")
tela/teste_renderizador.py:
  - adiciona teste_h0037_manual_001_marcador_truncamento
  - adiciona teste_h0037_manual_002_esc_primeiro
demo/teste_demo_console_modos.py:
  - adiciona teste_h0037_manual_003_tecla_v_minuscula
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md:
  - adiciona secao 36 do patch focal
```

## 6. Integridade

```yaml
python_ast:
  tela/renderizador.py: OK
  tela/teste_renderizador.py: OK
  demo/demo.py: OK
  demo/teste_demo_console_modos.py: OK
  demo/teste_explorar_barra_de_menus.py: OK
conflitos_git:
  marcadores: ausentes
temporarios:
  __pycache__: presente_apos_smoke_tecnico_QA
  "*.pyc": presente_apos_smoke_tecnico_QA
  "*.tmp": ausente
  "*.bak": ausente
  "*.swp": ausente
  "*~": ausente
whitespace:
  git_diff_check: sem_erros
```

## 7. H0037-MANUAL-001

Implementacao auditada:

- `_truncar_com_marcador(texto, largura)` retorna texto integral quando cabe.
- Para texto maior que a largura e `largura >= 3`, retorna sufixo visivel
  `...`, com comprimento final igual a largura.
- Para `largura < 3`, aplica truncamento silencioso conforme regra vigente.
- O marcador e aplicado antes do envelope da caixa em caminhos nao verbosos.

Evidencias positivas:

```yaml
texto_que_cabe: conforme
texto_exatamente_na_largura: conforme
texto_truncado: conforme
hierarquia_nao_verbosa: conforme
tabela_nao_verbosa: conforme
conjuntos_nao_verbosos: conforme
larguras_minimas:
  largura_3: conforme
  largura_menor_que_3: conforme_regra_vigente
largura_respeitada: conforme
bordas_e_separadores: preservados
```

Provas executadas:

```yaml
helper:
  _truncar_com_marcador("abc", 5): "abc"
  _truncar_com_marcador("abcde", 5): "abcde"
  _truncar_com_marcador("abcdef", 5): "ab..."
  _truncar_com_marcador("abcdef", 3): "..."
  _truncar_com_marcador("abcdef", 2): "ab"
render_hierarquia_nao_verbosa:
  largura: 50
  exemplo: "Politica somente_nao_verboso aplicada quan...|"
render_tabela_nao_verbosa:
  largura: 50
  exemplo: "Grupo                     Campo            V...|"
render_conjuntos_nao_verbosos:
  largura: 26
  exemplos:
    - "Modo : conjuntos_c...|"
    - "Fonte: documento e...|"
```

Nao conformidade encontrada:

```yaml
modo_verboso:
  marcador_artificial: presente_em_larguras_reduzidas
  exemplos:
    - tela: h0037_console_verboso_dois_niveis
      largura: 30
      linha: "| 1. H-0037 conteudo_dois_...|"
    - tela: h0037_console_alternavel_tres_niveis
      largura: 50
      linha: "|   1.1. Politica alternavel com modo inicial ...|"
  causa_provavel:
    - containers da hierarquia seguem ramo com _truncar_com_marcador mesmo quando verboso=True
  conforme: false
```

Resultado:

```yaml
H0037_MANUAL_001:
  texto_que_cabe: conforme
  texto_exatamente_na_largura: conforme
  texto_truncado: conforme_no_modo_nao_verboso
  hierarquia: nao_conforme_no_modo_verboso_reduzido
  tabela: conforme
  conjuntos: conforme_no_modo_nao_verboso
  modo_verboso: nao_conforme
  alternancia: parcialmente_bloqueada_por_defeito_no_verbose
  larguras_minimas: conforme_para_helper
  largura_respeitada: conforme
  conforme: false
```

## 8. H0037-MANUAL-002

Implementacao auditada:

- `_garantir_esc_primeiro(chips)` move o primeiro chip com `tecla == "Esc"`
  para a primeira posicao.
- `_linhas_barra` chama essa funcao em ponto central, sem condicao por ID de
  tela.
- A ordem relativa dos demais chips e preservada.
- Quando `Esc` nao esta presente, nenhum chip e inventado.

Provas executadas:

```yaml
Esc_primeiro:
  esc_meio: ["Esc", "V", "?", "X"]
  esc_final: ["Esc", "V", "?", "X"]
  esc_ja_primeiro: ["Esc", "V", "?"]
barra_sem_Esc:
  resultado: ["V", "?", "X"]
somente_Esc:
  resultado: ["Esc"]
duplicacao:
  helper_nao_cria_Esc_novo: true
  observacao: "segunda ocorrencia indevida e materia de validacao contratual separada"
aplicacao_central:
  funcao: _linhas_barra
  condicao_por_id: ausente
barras_historicas:
  demo: preservada
  h0036_console_hierarquia: preservada
  h0036_console_tabela: preservada
  h0036_console_conjuntos: preservada
cenarios_H0037:
  h0037_console_alternavel_tres_niveis: "[Esc] antes de [V]"
  h0037_console_tabela_alternavel: "[Esc] antes de [V]"
conforme: true
```

## 9. H0037-MANUAL-003

Implementacao auditada em `demo/demo.py`:

```python
if comando in ("V", "v") and modelo is not None:
```

Provas executadas:

```yaml
V_alternaveis:
  h0037_console_alternavel_tres_niveis: alterna
  h0037_console_tabela_alternavel: alterna
v_alternaveis:
  h0037_console_alternavel_tres_niveis: alterna
  h0037_console_tabela_alternavel: alterna
V_fixas:
  h0037_console_nao_verboso: inerte
  h0037_console_verboso_dois_niveis: inerte
v_fixas:
  h0037_console_nao_verboso: inerte
  h0037_console_verboso_dois_niveis: inerte
reversibilidade: conforme
alternancia_mista: conforme_por_tratamento_nominal
isolamento: conforme
recarregamento: conforme
eco: ausente
outras_teclas:
  B: continua_inerte_para_borda
  b: continua_alternando_borda
  normalizacao_global: ausente
conforme: true
```

## 10. Testes Adicionados

```yaml
- teste: teste_h0037_manual_001_marcador_truncamento
  arquivo: tela/teste_renderizador.py
  regra: H0037-MANUAL-001
  casos: helper, hierarquia_nao_verbosa, tabela_nao_verbosa, tabela_verbosa, redimensionamento
  resultado: passou
  prova_comportamento_real: parcial
  apenas_testa_helper: false
  conforme: false
  motivo: "nao cobre hierarquia verbosa em largura reduzida, onde o marcador artificial aparece"

- teste: teste_h0037_manual_002_esc_primeiro
  arquivo: tela/teste_renderizador.py
  regra: H0037-MANUAL-002
  casos: helper, barras H-0037 renderizadas, barras historicas
  resultado: passou
  prova_comportamento_real: true
  apenas_testa_helper: false
  conforme: true

- teste: teste_h0037_manual_003_tecla_v_minuscula
  arquivo: demo/teste_demo_console_modos.py
  regra: H0037-MANUAL-003
  casos: V/v em cenarios 3 e 4, fixas, reversibilidade, isolamento, eco
  resultado: passou
  prova_comportamento_real: true
  apenas_testa_helper: false
  conforme: true
```

Os testes cobrem os tres achados humanos, mas a cobertura de
`H0037-MANUAL-001` e insuficiente para o requisito de modo verboso sem marcador.

## 11. Paginacao Nao Aplicavel

```yaml
paginacao:
  implementada_neste_patch: false
  testes_novos_de_paginacao: nenhum
  mecanismos_historicos_alterados: false
  classificacao: NAO_APLICAVEL
```

Ausencia de paginacao nao foi tratada como defeito.

## 12. Preservacoes

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso

conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false

alinhamento_dois_niveis:
  preservado: true

tabela:
  cabecalho: preservado
  celulas_multilinha_no_verboso: preservadas

D23:
  preservado: true

validacoes:
  V_01: preservada
  V_04: preservada
  V_13: preservada
  V_14: preservada

demo_json:
  carrega: true
  entradas: 11

regressao_H_0036:
  preservada: true
```

## 13. Relatorio IMP-0037

A secao 36 foi auditada.

```yaml
origem_manual: registrada
tres_achados: registrados
causas: registradas
arquivos_alterados: registrados
funcoes_centrais: registradas
comportamento_de_truncamento: registrado
regra_Esc_primeiro: registrada
suporte_V_e_v: registrado
paginacao_fora_do_escopo: registrado
testes_adicionados: registrados
10_scripts: registrado
2741_verificacoes: registrado
zero_falhas: registrado
git_diff_check: registrado
stage_vazio: registrado
ausencia_commit_push: registrada
relatorio_manual_preservado: registrado
revalidacao_manual_pendente: registrada
ausencia_autoaprovacao: registrada
conclusao_literal:
  esperado: "implementacao corrigida apos reprovacao manual e aguardando novo QA independente"
  observado: "implementacao corrigida apos reprovação manual e aguardando novo QA independente"
classificacao: RELATORIO_COM_INCOMPLETUDE_POR_NAO_REFLETIR_DEFEITO_ENCONTRADO_NESTE_QA
```

O relatorio de implementacao era coerente com a suite declarada, mas nao
captura a falha encontrada nesta auditoria em modo verboso estreito.

Observacao de higiene: os testes focais e a suite canonica foram executados com
`PYTHONDONTWRITEBYTECODE=1`, mas probes tecnicos adicionais de smoke foram
executados sem esse ambiente e geraram artefatos Python nao rastreados. Eles
foram registrados e nao removidos, conforme instrucao desta rodada.

## 14. Testes Focais

```yaml
- script: tela/teste_modelo.py
  verificacoes: 186
  falhas: 0
  codigo_saida: 0

- script: tela/teste_renderizador.py
  verificacoes: 1253
  falhas: 0
  codigo_saida: 0

- script: demo/teste_demo.py
  verificacoes: 363
  falhas: 0
  codigo_saida: 0

- script: demo/teste_demo_console_modos.py
  verificacoes: 80
  falhas: 0
  codigo_saida: 0

- script: demo/teste_explorar_barra_de_menus.py
  verificacoes: 38
  falhas: 0
  codigo_saida: 0
```

Todos terminaram com codigo zero.

## 15. Suite Independente

```yaml
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2741
  falhas: 0
  codigo_saida: todos_zero

por_script:
  tela/teste_loader.py: {verificacoes: 512, falhas: 0, codigo_saida: 0}
  tela/teste_modelo.py: {verificacoes: 186, falhas: 0, codigo_saida: 0}
  tela/teste_renderizador.py: {verificacoes: 1253, falhas: 0, codigo_saida: 0}
  tela/teste_distribuicao_matricial.py: {verificacoes: 36, falhas: 0, codigo_saida: 0}
  demo/teste_demo.py: {verificacoes: 363, falhas: 0, codigo_saida: 0}
  demo/teste_diagnostico.py: {verificacoes: 48, falhas: 0, codigo_saida: 0}
  demo/teste_demo_distribuicao.py: {verificacoes: 109, falhas: 0, codigo_saida: 0}
  demo/teste_explorar_barra_de_menus.py: {verificacoes: 38, falhas: 0, codigo_saida: 0}
  demo/teste_demo_console.py: {verificacoes: 116, falhas: 0, codigo_saida: 0}
  demo/teste_demo_console_modos.py: {verificacoes: 80, falhas: 0, codigo_saida: 0}
```

## 16. Smoke Tecnico

Smoke seguro, sem aprovacao visual:

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso

chips:
  alternavel_tres_niveis:
    Esc_primeiro: true
    V_presente: true
  tabela_alternavel:
    Esc_primeiro: true
    V_presente: true

teclas:
  V: funcional
  v: funcional
  telas_fixas: inertes

smoke_nao_visual:
  classificacao: tecnico
```

## 17. Revalidacao Manual

Permanece:

```text
REVALIDACAO_MANUAL_PENDENTE_USUARIO
```

Nao simulei usuario, nao declarei aprovacao visual, nao alterei o relatorio
manual anterior, nao criei novo relatorio manual e nao executei fechamento.

## 18. Achados

```yaml
- id: H0037-IMPL-QAPP7-001
  arquivo: tela/renderizador.py
  funcao_ou_teste: _linhas_apresentacao_hierarquia
  evidencia: "renderizar_tela(..., verboso=True, largura=30/50) produz linhas com '...|' em h0037_console_verboso_dois_niveis e h0037_console_alternavel_tres_niveis"
  autoridade: "contrato_console.md e roteiro QA_POS_PATCH_IMPLEMENTACAO: no modo verboso, marcador_artificial ausente e conteudo_multilinha preservado"
  severidade: MEDIA
  tipo: DEFEITO_IMPLEMENTACAO
  impacto: "O patch resolve o marcador ausente no modo nao verboso, mas aplica ou preserva marcador visual em modo verboso sob largura reduzida, reabrindo parte do requisito H0037-MANUAL-001."
  correcao_exigida: "Ajustar o caminho verboso da hierarquia para nao usar marcador artificial em containers/linhas verbosas e preservar conteudo por quebra quando aplicavel."

- id: H0037-IMPL-QAPP7-002
  arquivo: tela/teste_renderizador.py
  funcao_ou_teste: teste_h0037_manual_001_marcador_truncamento
  evidencia: "O teste afirma modo verboso sem marcador, mas valida apenas a tabela verbosa; nao cobre hierarquia verbosa estreita, caso que falha com '...|'."
  autoridade: "roteiro QA_POS_PATCH_IMPLEMENTACAO, secao 6: testes devem cobrir os tres achados humanos e atravessar comportamento real com expectativas semanticamente corretas"
  severidade: MEDIA
  tipo: TESTE_INCORRETO
  impacto: "A suite de 2741 verificacoes passa apesar do defeito de modo verboso no requisito H0037-MANUAL-001."
  correcao_exigida: "Adicionar teste de renderizacao real para hierarquia verbosa em largura reduzida, garantindo ausencia de marcador artificial e preservacao multilinha."
```

## 19. Conclusao

`H0037-MANUAL-002` e `H0037-MANUAL-003` estao resolvidos no patch auditado.
`H0037-MANUAL-001` esta resolvido para truncamento real no modo nao verboso,
incluindo hierarquia, tabela e conjuntos, mas nao esta integralmente resolvido
porque o modo verboso ainda pode exibir marcador `...` em hierarquia quando a
largura diminui.

A implementacao exige novo patch focal. A revalidacao manual permanece pendente
e nao deve ser iniciada ate a correcao tecnica.

## 20. Status Literal

```text
IMPLEMENTATION_PATCH_REQUIRED
```

## 21. Status Normalizado

```text
patch_required
```

## 22. Proxima Categoria

```yaml
proxima_categoria: PATCH_IMPLEMENTACAO
```

## Saida Final Canonica

```yaml
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_required
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_7_H-0037_IMPLEMENTACAO.md
qa_anterior: docs/relatorios/RELATORIO_QA_POS_PATCH_6_H-0037_IMPLEMENTACAO.md
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
  arquivos_do_patch:
    - tela/renderizador.py
    - tela/teste_renderizador.py
    - demo/demo.py
    - demo/teste_demo_console_modos.py
    - docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  arquivos_inesperados: presentes_na_worktree_acumulada_origem_NAO_CONFIRMADA

integridade:
  python: OK
  conflitos: ausentes
  temporarios:
    - demo/__pycache__/demo.cpython-314.pyc
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/distribuicao_matricial.cpython-314.pyc
    - tela/__pycache__/loader.cpython-314.pyc
    - tela/__pycache__/modelo.cpython-314.pyc
    - tela/__pycache__/renderizador.cpython-314.pyc

H0037_MANUAL_001:
  helper: conforme
  texto_que_cabe: conforme
  texto_truncado: conforme_no_modo_nao_verboso
  hierarquia: nao_conforme_no_modo_verboso_reduzido
  tabela: conforme
  conjuntos: conforme_no_modo_nao_verboso
  alternancia: parcialmente_bloqueada
  largura: respeitada
  conforme: false

H0037_MANUAL_002:
  helper: conforme
  Esc_primeiro: conforme
  ordem_dos_demais: preservada
  barra_sem_Esc: preservada_sem_inventar_Esc
  duplicacao: helper_nao_duplica
  aplicacao_central: conforme
  barras_historicas: preservadas
  conforme: true

H0037_MANUAL_003:
  V_alternaveis: conforme
  v_alternaveis: conforme
  V_fixas: inerte
  v_fixas: inerte
  reversibilidade: conforme
  isolamento: conforme
  eco: ausente
  outras_teclas: preservadas
  conforme: true

testes_adicionados:
  teste_h0037_manual_001_marcador_truncamento: nao_conforme_cobertura_insuficiente
  teste_h0037_manual_002_esc_primeiro: conforme
  teste_h0037_manual_003_tecla_v_minuscula: conforme
paginacao:
  implementada_neste_patch: false
  testes_novos_de_paginacao: nenhum
  mecanismos_historicos_alterados: false
  classificacao: NAO_APLICAVEL
preservacoes: conforme_exceto_defeito_H0037_MANUAL_001_modo_verboso_reduzido
relatorio_IMP_0037: incompleto_frente_ao_defeito_encontrado_pelo_QA

testes_focais:
  - {script: tela/teste_modelo.py, verificacoes: 186, falhas: 0, codigo_saida: 0}
  - {script: tela/teste_renderizador.py, verificacoes: 1253, falhas: 0, codigo_saida: 0}
  - {script: demo/teste_demo.py, verificacoes: 363, falhas: 0, codigo_saida: 0}
  - {script: demo/teste_demo_console_modos.py, verificacoes: 80, falhas: 0, codigo_saida: 0}
  - {script: demo/teste_explorar_barra_de_menus.py, verificacoes: 38, falhas: 0, codigo_saida: 0}
suite_declarada:
  scripts: 10
  verificacoes: 2741
  falhas: 0
suite_executada_pelo_QA:
  scripts: 10
  verificacoes: 2741
  falhas: 0
  codigo_saida: todos_zero
smoke_tests:
  tecnico: executado
  visual: nao_executado
revalidacao_manual: REVALIDACAO_MANUAL_PENDENTE_USUARIO

achados_bloqueantes: []
achados_altos: []
achados_medios:
  - H0037-IMPL-QAPP7-001
  - H0037-IMPL-QAPP7-002
achados_baixos: []
observacoes: []
regressoes:
  - H0037-IMPL-QAPP7-001

implementacao_aprovada: false
proxima_categoria: PATCH_IMPLEMENTACAO
```
