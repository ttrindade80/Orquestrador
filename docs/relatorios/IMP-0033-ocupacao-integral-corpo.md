# IMP-0033 — Ocupação integral do corpo

**Handoff:** H-0033
**ADR de referência:** ADR-0024 (Proibição de preenchimento externo vazio no corpo)
**Data:** 2026-07-16
**Status:** PATCH_APLICADO — VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

---

## 1. Campos mínimos obrigatórios

```yaml
handoff: H-0033
adr: ADR-0024

arquivos_alterados:
  obrigatorios:
    - tela/renderizador.py
    - tela/teste_renderizador.py
    - docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
  condicionais_preservados:
    - tela/modelo.py
    - tela/loader.py
    - demo/demo.py
    - demo/diagnostico.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - demo/teste_demo.py
    - demo/teste_diagnostico.py
    - demo/teste_explorar_barra_de_menus.py
    - config/telas/demo/demo.json
    - config/telas/demo/destino_minimo.json
    - config/telas/demo/grupo_minimo.json
    - config/telas/demo/stub_b.json
    - config/telas/demo/h0029_dashboard_fracao.json
    - config/telas/demo/h0029_dashboard_igual.json
    - config/telas/demo/h0029_dashboard_percentual.json
    - config/telas/demo/h0029_grupo_fracao.json
    - config/telas/demo/h0029_grupo_igual.json
    - config/telas/demo/h0029_grupo_percentual.json
    - config/telas/demo/h0029_grupo_pai_distribuido.json
    - config/telas/demo/h0030_console_unico.json
    - config/telas/demo/h0030_dashboard_unico.json
    - config/telas/demo/h0030_matriz_2x2.json
    - config/telas/demo/h0030_matriz_2x4.json
    - config/telas/demo/h0030_matriz_3x2.json

implementacao:
  DA_01: >
    Implementado em _renderizar_container_vertical. Quando distribuicao=None e
    altura_disponivel e fornecida e n_visual==1, o unico descendente visual
    recebe altura_alvo=altura_disponivel, ocupando integralmente toda a area.
    Grupos transparentes (DA-03) repassam a area via _renderizar_container
    recursivo. Funcao auxiliar _contar_elementos_visuais foi adicionada para
    detectar cardinalidade.
  DA_02: >
    Implementado em _renderizar_container_vertical e _renderizar_container_horizontal.
    Vertical: quando n_visual > 1 e ha area residual nao coberta (l_fill > 0)
    apos renderizacao natural, levanta RenderizadorErro com prefixo "DA-02 (ADR-0024)".
    Horizontal (patch QA-H0033-IMP-HIGH-001): quando N > 1 e distribuicao is None,
    rejeita imediatamente com RenderizadorErro "DA-02 (ADR-0024)"; ausencia de
    distribuicao nunca equivale a particionamento uniforme implicito.
    Composicoes com distribuicao explicita seguem caminho pre-existente e nao sao afetadas.
  DA_03: >
    Implementado via propagacao de altura_disponivel para grupos transparentes
    (sem distribuicao, arranjo vertical, sem estrutura=matriz). Esses grupos
    repassam integralmente sua area aos descendentes visuais via chamada
    recursiva _renderizar_container com altura_disponivel. Grupos com gestao
    propria contam como 1 unidade visual.
  DA_04: >
    Implementado em dois pontos: (1) em _renderizar_container_vertical, quando
    n_visual==0 e ha area residual, levanta RenderizadorErro com prefixo
    "DA-04 (ADR-0024)"; (2) em renderizar_tela, o bloco de fill externo
    pre-ADR-0024 foi substituido por guarda de seguranca que tambem levanta
    RenderizadorErro caso area residual chegue a esse ponto inesperadamente.

inventario_jsons:
  quantidade_real_em_config_telas_demo: 16
  registrados_no_relatorio: 16
  verificacao_conjunto: CONFIRMADO

jsons_atualizados: []

jsons_revisados_e_preservados:
  quantidade: 16
  lista:
    - config/telas/demo/demo.json
    - config/telas/demo/destino_minimo.json
    - config/telas/demo/grupo_minimo.json
    - config/telas/demo/stub_b.json
    - config/telas/demo/h0029_dashboard_fracao.json
    - config/telas/demo/h0029_dashboard_igual.json
    - config/telas/demo/h0029_dashboard_percentual.json
    - config/telas/demo/h0029_grupo_fracao.json
    - config/telas/demo/h0029_grupo_igual.json
    - config/telas/demo/h0029_grupo_percentual.json
    - config/telas/demo/h0029_grupo_pai_distribuido.json
    - config/telas/demo/h0030_console_unico.json
    - config/telas/demo/h0030_dashboard_unico.json
    - config/telas/demo/h0030_matriz_2x2.json
    - config/telas/demo/h0030_matriz_2x4.json
    - config/telas/demo/h0030_matriz_3x2.json

jsons_invalidos_de_teste:
  descricao: >
    Fixture invalida nominal para o Caso C (DA-02/DA-04) definida dentro de
    tela/teste_renderizador.py, classe TestOcupacaoIntegralCorpoH0033,
    metodos test_DA02_dois_visuais_sem_dist_erro,
    test_DA02_tres_visuais_sem_dist_erro e test_DA04_zero_visuais_com_area_erro.
    As fixtures sao construidas inline nos testes, nao como JSONs permanentes,
    e nao transformam configuracao permanente valida em invalida.

testes_focais:
  classe: TestOcupacaoIntegralCorpoH0033
  arquivo: tela/teste_renderizador.py
  testes:
    - test_DA01_visual_direto_ocupa_area_integral
    - test_DA01_visual_via_grupo_transparente
    - test_DA01_fill_interno_preservado
    - test_DA01_equivalencia_com_distribuicao
    - test_DA02_dois_visuais_sem_dist_erro
    - test_DA02_tres_visuais_sem_dist_erro
    - test_DA02_com_distribuicao_ok
    - test_DA02_sem_area_residual_ok
    - test_DA03_grupo_com_dist_repassa_area
    - test_DA03_grupo_transparente_repassa_area_integral
    - test_DA04_zero_visuais_com_area_erro
    - test_inventario_16_jsons_altura_natural
    - test_inventario_15_jsons_com_altura_20
    - test_inventario_15_jsons_com_altura_30_largura_80
    - test_destino_minimo_sem_fill_externo
    - test_grupo_minimo_sem_fill_externo
    - test_H1_horizontal_um_participante_sem_dist
    - test_H2_horizontal_dois_sem_dist_rejeita
    - test_H3_horizontal_grupo_multiplos_sem_dist_rejeita
    - test_H4_horizontal_aninhado_nao_bypassa_DA02
    - test_H5_horizontal_com_distribuicao_valido
    - test_H6_matriz_nao_e_rejeitada

suite_canonica:
  tela_teste_renderizador:
    comando: python tela/teste_renderizador.py
    verificacoes: 1126
    aprovacoes: 1126
    falhas: 0
    codigo_saida: 0
  tela_teste_loader:
    comando: python tela/teste_loader.py
    verificacoes: 283
    aprovacoes: 283
    falhas: 0
    codigo_saida: 0
  tela_teste_modelo:
    comando: python tela/teste_modelo.py
    verificacoes: 163
    aprovacoes: 163
    falhas: 0
    codigo_saida: 0
  demo_teste_demo:
    comando: python demo/teste_demo.py
    verificacoes: 358
    aprovacoes: 358
    falhas: 0
    codigo_saida: 0
  demo_teste_diagnostico:
    comando: python demo/teste_diagnostico.py
    verificacoes: 30
    aprovacoes: 30
    falhas: 0
    codigo_saida: 0
  demo_teste_explorar_barra_de_menus:
    comando: python demo/teste_explorar_barra_de_menus.py
    verificacoes: 38
    aprovacoes: 38
    falhas: 0
    codigo_saida: 0
  total_verificacoes: 1998
  total_aprovacoes: 1998
  total_falhas: 0
  baseline_handoff: 1937
  incremento_por_testes_focais: 54
  incremento_por_patch_QA-H0033-IMP-HIGH-001: 7

demonstracao_real:
  pipeline_nao_interativo: EXECUTADO
  destino_minimo_42x20: CONFIRMADO_SEM_FILL_EXTERNO
  destino_minimo_80x30: PENDENTE_TTY_REAL
  grupo_minimo_42x20: CONFIRMADO_SEM_FILL_EXTERNO
  grupo_minimo_80x30: PENDENTE_TTY_REAL
  demo_json: CONFIRMADO_PELA_SUITE

identidades_confirmadas:
  destino_minimo:
    id_tela: destino_minimo
    cabecalho_titulo: Destino Minimo
    corpo_arranjo: sobreposto
    corpo_distribuicao: null
    dashboard: dashboard_teste
    dashboard_titulo: Teste
    ausencia_faixa_externa_42x20: CONFIRMADA
    busca_fill_externo_42x20: "indices com fill externo: []"
  grupo_minimo:
    id_tela: grupo_minimo
    cabecalho_titulo: Grupo Minimo
    corpo_distribuicao: null
    grupo: grupo_principal
    dashboard: dashboard_conteudo
    dashboard_titulo: Conteudo
    ausencia_dashboard_TESTE: CONFIRMADA
    ausencia_faixa_externa_42x20: CONFIRMADA
    busca_fill_externo_42x20: "indices com fill externo: []"
    busca_TESTE_na_saida: false
  demo:
    id_tela: demo
    cabecalho_titulo: Orquestrador
    corpo_arranjo: vertical
    distribuicao_modo: fracao
    distribuicao_valores: [2, 1, 2]
    n_elementos: 3
    elementos:
      - {id: console_principal, tipo: console}
      - {id: dashboard_info, tipo: dashboard}
      - {id: lancador_principal, tipo: lancador}

dimensoes_testadas:
  - 42x20
  - 80x30

validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

excecoes_operacionais_autorizadas: []

git:
  raiz: /home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador
  git_diff_check: LIMPO
  git_diff_name_only:
    documentos_adr_0024_acumulados:
      - docs/NOMENCLATURA.md
      - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
      - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
      - docs/adr/INDICE_ADR.md
      - docs/contratos/contrato_composicao_corpo.md
      - docs/contratos/contrato_json_tela_minima.md
      - docs/contratos/contrato_tela_json.md
    arquivos_implementacao_h0033:
      - tela/renderizador.py
      - tela/teste_renderizador.py
  git_status_short:
    modificados_rastreados:
      - " M docs/NOMENCLATURA.md"
      - " M docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md"
      - " M docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md"
      - " M docs/adr/INDICE_ADR.md"
      - " M docs/contratos/contrato_composicao_corpo.md"
      - " M docs/contratos/contrato_json_tela_minima.md"
      - " M docs/contratos/contrato_tela_json.md"
      - " M tela/renderizador.py"
      - " M tela/teste_renderizador.py"
    nao_rastreados:
      - "?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md"
      - "?? docs/handoff/H-0033-ocupacao-integral-corpo.md"
      - "?? docs/relatorios/IMP-0033-ocupacao-integral-corpo.md"
      - "?? docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md"
      - "?? docs/relatorios/RELATORIO_QA_ADR-0024.md"
      - "?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0024.md"
      - "?? docs/relatorios/RELATORIO_QA_H-0033_HANDOFF.md"
      - "?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md"
      - "?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0033_HANDOFF.md"
      - "?? tela/__pycache__/"
  arquivos_inesperados: []

bloqueios: []
```

---

## 2. Alterações em `tela/renderizador.py`

### 2.1 Nova função `_contar_elementos_visuais`

Inserida antes de `_caixa_de_elemento`. Conta descendentes visuais
(`console`/`dashboard`/`lancador`) atravessando a hierarquia de grupos.

Grupos **sem gestão própria** (sem `distribuicao`, arranjo vertical, sem `estrutura=matriz`)
são containers estruturais transparentes: a contagem percorre seus filhos.
Grupos **com gestão própria** (com `distribuicao`, arranjo horizontal ou matriciais)
contam como 1 unidade visual — eles resolvem a área internamente.

Utilizada para aplicar DA-01 e detectar DA-02/DA-04.

### 2.2 Modificação de `_renderizar_container_vertical`

Adicionado ramo `elif distribuicao is None and altura_disponivel is not None:`
que implementa DA-01/DA-02/DA-04:

- **DA-01** (`n_visual == 1`): único descendente visual recebe `altura_alvo=altura_disponivel`.
  Grupos transparentes (DA-03) repassam a área integralmente via `_renderizar_container`.
- **DA-02/DA-04** (`n_visual != 1`): renderização natural; se `l_fill > 0`:
  - `n_visual == 0` → `RenderizadorErro` com prefixo `"DA-04"`.
  - `n_visual > 1` → `RenderizadorErro` com prefixo `"DA-02"`.

O ramo `else` (sem `altura_disponivel`) permanece inalterado — renderização natural
orientada pelo conteúdo (ADR-0018 D2).

### 2.3 Guarda pós-renderização em `renderizar_tela`

O bloco de preenchimento externo de H-0015 (linhas de espaços entre corpo e barra)
foi substituído por uma guarda de segurança DA-04:

```python
l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
if l_corpo_fill > 0 and arranjo_corpo != "horizontal" and not _corpo_vertical_distribuido:
    raise RenderizadorErro("DA-04 (ADR-0024): preenchimento externo vazio detectado ...")
```

Essa guarda protege contra estados inesperados: em operação normal, DA-02/DA-04 são
detectados antes, dentro de `_renderizar_container_vertical`.

---

## 3. Alterações em `tela/teste_renderizador.py`

### 3.1 Testes atualizados (comportamento antigo → ADR-0024)

| Função/método | Mudança |
|---|---|
| `teste_altura_explicita` | `altura=21/24` com 3 visuais sem dist → espera DA-02 |
| `TestH0016.test_renderizar_tela_preserva_altura_h0015` | Verifica DA-02 em vez de fill externo |
| `TestPreenchimentoVerticalH0020.test_vertical_preserva_comportamento_atual` | Verifica `fill_ext==0` (DA-01) em vez de `fill_ext>0` |
| `TestComposicaoH0021.test_vertical_nao_regride_apos_h0021` | Segunda parte: espera DA-02 em vez de fill externo |
| `TestDistribuicaoVerticalH0025.test_ausencia_preserva_altura_natural_sem_cota` | `altura=24` com 3 visuais → espera DA-02 |
| `TestCardinalidadeUnitariaH0029.test_M01_ausencia_funcional_preserva_natural` | `corpo_alts==[14]`, `fill_ext==0` (DA-01) |
| `TestCardinalidadeUnitariaH0029.test_M05_igual_grupo_sem_dist_1filho` | `corpo_alts==[14]` (DA-01 dentro do grupo) |
| `TestCardinalidadeUnitariaH0029.test_M07_ausencia_corpo_grupo_igual_1filho` | `corpo_alts==[14]`, `fill_ext==0` (DA-01+DA-03) |
| `TestCardinalidadeUnitariaH0029.test_integracao_json_grupo_minimo` | `corpo_alts[0]==14`, `fill_ext==0` |
| `TestTelasPermanentesH0029.test_geometria_grupo_pai_distribuido_natural` | Dashboard expande (DA-01); `base==altura-4` |
| `TestTelasPermanentesH0029.test_area_adicional_absorvida` | `h0029_grupo_pai_distribuido` segue padrão geral (`base20==16`, `base30==26`) |

### 3.2 Nova classe `TestOcupacaoIntegralCorpoH0033`

Testes focais adicionados antes de `main()`:

| Teste | DA coberta |
|---|---|
| `test_DA01_visual_direto_ocupa_area_integral` | DA-01 |
| `test_DA01_visual_via_grupo_transparente` | DA-01 + DA-03 |
| `test_DA01_fill_interno_preservado` | DA-01 (fill interno válido) |
| `test_DA01_equivalencia_com_distribuicao` | DA-01 (equivalência sem/com dist) |
| `test_DA02_dois_visuais_sem_dist_erro` | DA-02 |
| `test_DA02_tres_visuais_sem_dist_erro` | DA-02 (mensagem "distribuicao") |
| `test_DA02_com_distribuicao_ok` | DA-02 (sem erro com dist) |
| `test_DA02_sem_area_residual_ok` | DA-02 (l_fill==0 → sem erro) |
| `test_DA03_grupo_com_dist_repassa_area` | DA-03 |
| `test_DA03_grupo_transparente_repassa_area_integral` | DA-03 |
| `test_DA04_zero_visuais_com_area_erro` | DA-04 |
| `test_inventario_16_jsons_altura_natural` | Inventário (13 JSONs, altura natural) |
| `test_inventario_15_jsons_com_altura_20` | Inventário (15 JSONs × 42×20) |
| `test_inventario_15_jsons_com_altura_30_largura_80` | Inventário (15 JSONs × 80×30) |
| `test_destino_minimo_sem_fill_externo` | DA-01 (`destino_minimo.json`) |
| `test_grupo_minimo_sem_fill_externo` | DA-01 + DA-03 (`grupo_minimo.json`) |

---

## 4. Inventário nominal dos 16 JSONs

Verificação executada confirmou que `config/telas/demo/` contém exatamente 16 arquivos JSON,
correspondendo ao inventário abaixo.

```yaml
inventario_jsons:

  - caminho: config/telas/demo/demo.json
    id_da_tela: demo
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao fracao:[2,1,2] explicita, 3 visuais
    compatibilidade_DA_02: CONFORME — distribuicao obrigatoria presente
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo transparente no nivel do corpo
    compatibilidade_DA_04: CONFORME — toda area distribuida entre elementos visuais
    acao: PRESERVADO
    justificativa: >
      3 elementos visuais com distribuicao fracao:[2,1,2] explícita. Toda area do corpo
      alocada por cotas. Caminho _corpo_vertical_distribuido=True; DA-01 nao se aplica.
      Sem fill externo. Suite confirma: 358 verificacoes passam.

  - caminho: config/telas/demo/destino_minimo.json
    id_da_tela: destino_minimo
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: CONFORME — 1 dashboard (dashboard_teste, titulo Teste), sem dist, DA-01 aplicado; ocupa area integral
    compatibilidade_DA_02: NAO_APLICAVEL — cardinalidade unitaria
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo
    compatibilidade_DA_04: CONFORME — 0 linhas de fill externo (prova: indices=[])
    acao: PRESERVADO
    justificativa: >
      Corpo arranjo=sobreposto, distribucao=None, 1 dashboard_teste.
      Prova executada: fill_externo=[] em 42x20. Nenhuma linha vazia entre dashboard e
      barra_de_menus. Sem alteracao necessaria.

  - caminho: config/telas/demo/grupo_minimo.json
    id_da_tela: grupo_minimo
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: CONFORME — dashboard_conteudo (titulo Conteudo) ocupa area integral via DA-01+DA-03
    compatibilidade_DA_02: NAO_APLICAVEL — cardinalidade unitaria
    compatibilidade_DA_03: CONFORME — grupo_principal repassa area integralmente a dashboard_conteudo
    compatibilidade_DA_04: CONFORME — 0 linhas de fill externo (prova: indices=[])
    acao: PRESERVADO
    justificativa: >
      Corpo vertical, distribucao=None, 1 grupo_principal (sem dist) contendo 1 dashboard_conteudo.
      DA-01 e DA-03 aplicados conjuntamente. Prova: fill_externo=[] em 42x20.
      Nao existe dashboard TESTE nesta tela (confirmado: busca TESTE na saida = false).

  - caminho: config/telas/demo/stub_b.json
    id_da_tela: stub_b
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: CONFORME — 1 dashboard (dashboard_teste), sem dist, DA-01 aplicado
    compatibilidade_DA_02: NAO_APLICAVEL — cardinalidade unitaria
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo
    compatibilidade_DA_04: CONFORME — cardinalidade unitaria sem area residual
    acao: PRESERVADO
    justificativa: >
      Corpo sobreposto, distribucao=None, 1 dashboard_teste. Identica em estrutura
      a destino_minimo. Coberta por test_inventario_15_jsons_com_altura_20/30.

  - caminho: config/telas/demo/h0029_dashboard_fracao.json
    id_da_tela: h0029_dashboard_fracao
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao fracao:[1] explicita
    compatibilidade_DA_02: CONFORME — distribuicao presente, 1 visual
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo transparente
    compatibilidade_DA_04: CONFORME — cota garante area integral ao dashboard
    acao: PRESERVADO
    justificativa: Distribuicao fracao:[1] explicita. Caminho _corpo_vertical_distribuido=True.

  - caminho: config/telas/demo/h0029_dashboard_igual.json
    id_da_tela: h0029_dashboard_igual
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao igual explicita
    compatibilidade_DA_02: CONFORME — distribuicao presente
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo transparente
    compatibilidade_DA_04: CONFORME — area integral ao dashboard
    acao: PRESERVADO
    justificativa: Distribuicao igual explicita.

  - caminho: config/telas/demo/h0029_dashboard_percentual.json
    id_da_tela: h0029_dashboard_percentual
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao percentual:[100] explicita
    compatibilidade_DA_02: CONFORME — distribuicao presente
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo transparente
    compatibilidade_DA_04: CONFORME — area integral ao dashboard
    acao: PRESERVADO
    justificativa: Distribuicao percentual:[100] explicita.

  - caminho: config/telas/demo/h0029_grupo_fracao.json
    id_da_tela: h0029_grupo_fracao
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao fracao:[1] no corpo e no grupo
    compatibilidade_DA_02: CONFORME — distribuicao explicita em ambos os niveis
    compatibilidade_DA_03: CONFORME — grupo com dist propria (auto-gerenciado)
    compatibilidade_DA_04: CONFORME — toda area alocada
    acao: PRESERVADO
    justificativa: Corpo fracao:[1] e grupo com fracao:[1]. Grupo auto-gerenciado conta como 1 unidade visual.

  - caminho: config/telas/demo/h0029_grupo_igual.json
    id_da_tela: h0029_grupo_igual
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao igual no corpo e no grupo
    compatibilidade_DA_02: CONFORME — distribuicao explicita
    compatibilidade_DA_03: CONFORME — grupo com dist propria
    compatibilidade_DA_04: CONFORME
    acao: PRESERVADO
    justificativa: Distribuicao igual em ambos os niveis.

  - caminho: config/telas/demo/h0029_grupo_percentual.json
    id_da_tela: h0029_grupo_percentual
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao percentual:[100] no corpo e no grupo
    compatibilidade_DA_02: CONFORME — distribuicao explicita
    compatibilidade_DA_03: CONFORME — grupo com dist propria
    compatibilidade_DA_04: CONFORME
    acao: PRESERVADO
    justificativa: Distribuicao percentual:[100] em ambos os niveis.

  - caminho: config/telas/demo/h0029_grupo_pai_distribuido.json
    id_da_tela: h0029_grupo_pai_distribuido
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: CONFORME — grupo sem dist, 1 dashboard interno; DA-01 aplicado pelo grupo
    compatibilidade_DA_02: NAO_APLICAVEL — grupo tem 1 filho visual
    compatibilidade_DA_03: CONFORME — grupo transparente repassa area ao dashboard
    compatibilidade_DA_04: CONFORME — toda area alocada; sem fill externo
    acao: PRESERVADO
    justificativa: >
      Corpo fracao:[1] (1 elemento: grupo sem dist). Grupo transparente com 1 filho dashboard.
      DA-01 aplicado dentro do grupo: dashboard ocupa area integral. Avaliacao inicial
      POTENCIALMENTE_INCOMPATIVEL foi resolvida: compativel confirmado apos implementacao.
      Suite confirma: test_geometria_grupo_pai_distribuido_natural e
      test_area_adicional_absorvida passam.

  - caminho: config/telas/demo/h0030_console_unico.json
    id_da_tela: h0030_console_unico
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao igual explicita
    compatibilidade_DA_02: CONFORME — distribuicao presente
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo
    compatibilidade_DA_04: CONFORME
    acao: PRESERVADO
    justificativa: Distribuicao igual com 1 console.

  - caminho: config/telas/demo/h0030_dashboard_unico.json
    id_da_tela: h0030_dashboard_unico
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — distribuicao igual explicita
    compatibilidade_DA_02: CONFORME — distribuicao presente
    compatibilidade_DA_03: NAO_APLICAVEL — sem grupo
    compatibilidade_DA_04: CONFORME
    acao: PRESERVADO
    justificativa: Distribuicao igual com 1 dashboard.

  - caminho: config/telas/demo/h0030_matriz_2x2.json
    id_da_tela: h0030_matriz_2x2
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — corpo tem dist igual; grupo matricial auto-gerenciado
    compatibilidade_DA_02: CONFORME — dist igual no corpo; grupo matricial gerencia internamente
    compatibilidade_DA_03: CONFORME — grupo matricial (estrutura=matriz) conta como 1 unidade
    compatibilidade_DA_04: CONFORME — toda area alocada via dist explicita do corpo
    acao: PRESERVADO
    justificativa: >
      Corpo igual, 1 grupo matricial (estrutura=matriz, 4 dashboards). Grupo matricial tem
      gestao propria (nao transparente): conta como 1 unidade visual. Avaliacao inicial
      POTENCIALMENTE_INCOMPATIVEL foi resolvida: compativel confirmado. Requer
      altura_disponivel para distribuicao de linhas (comportamento pre-existente).
      Suite: test_inventario_15_jsons_com_altura_20/30 passam.

  - caminho: config/telas/demo/h0030_matriz_2x4.json
    id_da_tela: h0030_matriz_2x4
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — grupo matricial auto-gerenciado
    compatibilidade_DA_02: CONFORME — dist igual no corpo; grupo gerencia internamente
    compatibilidade_DA_03: CONFORME — grupo matricial conta como 1 unidade
    compatibilidade_DA_04: CONFORME
    acao: PRESERVADO
    justificativa: Idem h0030_matriz_2x2. Grupo matricial 2x4 (8 dashboards).

  - caminho: config/telas/demo/h0030_matriz_3x2.json
    id_da_tela: h0030_matriz_3x2
    resultado_da_revisao: COMPATIVEL_CONFIRMADO
    compatibilidade_DA_01: NAO_APLICAVEL — grupo matricial auto-gerenciado
    compatibilidade_DA_02: CONFORME — dist igual no corpo; grupo gerencia internamente
    compatibilidade_DA_03: CONFORME — grupo matricial conta como 1 unidade
    compatibilidade_DA_04: CONFORME
    acao: PRESERVADO
    justificativa: Idem h0030_matriz_2x2. Grupo matricial 3x2 (6 dashboards).
```

---

## 5. Provas semânticas

### `destino_minimo`

Evidência executada pelo pipeline diagnóstico (`largura=42, altura=20`):

- `m.id = destino_minimo`
- `m.cabecalho['titulo'] = Destino Minimo`
- `m.corpo.distribuicao = None`
- `m.corpo.elementos = [('dashboard_teste', 'dashboard')]`
- `total_linhas = 21` (20 linhas + `\n` final)
- `linha4 = '╭ TESTE ─────────────────────────────────╮'` — borda superior do dashboard
- `linha6 = '│                                        │'` — conteúdo interno (espaço interno válido, não externo)
- `linha17 = '╰────────────────────────────────────────╯'` — borda inferior da barra de menus
- `indices_fill_externo = []` — confirmação de ausência de fill externo

Código de saída zero não é a prova. A prova é a lista de índices vazia.

### `grupo_minimo`

Evidência executada pelo pipeline diagnóstico (`largura=42, altura=20`):

- `m.id = grupo_minimo`
- `m.cabecalho['titulo'] = Grupo Minimo`
- `m.corpo.distribuicao = None`
- `m.corpo.elementos = [('grupo_principal', 'grupo')]`
- `grupo_principal.elementos = [('dashboard_conteudo', 'dashboard')]`
- `dashboard_conteudo._campos_inertes['titulo'] = Conteudo`
- `total_linhas = 21`
- `linha4 = '╭ CONTEUDO ──────────────────────────────╮'` — borda superior do dashboard
- `linha6 = '│                                        │'` — espaço interno válido
- `linha17 = '╰────────────────────────────────────────╯'` — barra de menus
- `indices_fill_externo = []`
- `'TESTE' in saida = False` — ausência de dashboard TESTE confirmada
- `'Conteudo' in saida = False` (título renderizado como maiúsculas: CONTEUDO)

### Distribuição válida (`demo.json`)

Evidência do JSON lido diretamente:

- `id = demo`
- `cabecalho.titulo = Orquestrador`
- `corpo.arranjo = vertical`
- `distribuicao = {"modo": "fracao", "valores": [2, 1, 2]}`
- `n_elementos = 3`
- `elementos = [console_principal/console, dashboard_info/dashboard, lancador_principal/lancador]`

---

## 6. Suíte canônica — resultados observados

```
python tela/teste_renderizador.py  →  1126/1126  código 0
python tela/teste_loader.py        →   283/283   código 0
python tela/teste_modelo.py        →   163/163   código 0
python demo/teste_demo.py          →   358/358   código 0
python demo/teste_diagnostico.py   →    30/30    código 0
python demo/teste_explorar_barra_de_menus.py → 38/38 código 0
─────────────────────────────────────────────────────
Total                              →  1998/1998  0 falhas
```

Baseline declarada no handoff: 1937.
Incremento por testes focais H-0033 (implementação): 54 verificações.
Incremento por patch QA-H0033-IMP-HIGH-001: 7 verificações (H1-H6 + T-NR01 reescrito).
Total: 61 verificações acima do baseline.

---

## 7. Estado Git

```
git diff --check    → LIMPO (sem whitespace errors)

git diff --name-only:
  docs/NOMENCLATURA.md                                   ← ADR-0024 (acumulado)
  docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md  ← ADR-0024
  docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md ← ADR-0024
  docs/adr/INDICE_ADR.md                                ← ADR-0024
  docs/contratos/contrato_composicao_corpo.md           ← ADR-0024
  docs/contratos/contrato_json_tela_minima.md           ← ADR-0024
  docs/contratos/contrato_tela_json.md                  ← ADR-0024
  tela/renderizador.py                                  ← H-0033
  tela/teste_renderizador.py                            ← H-0033

git status --short:
   M docs/NOMENCLATURA.md
   M docs/adr/ADR-0013-...
   M docs/adr/ADR-0018-...
   M docs/adr/INDICE_ADR.md
   M docs/contratos/contrato_composicao_corpo.md
   M docs/contratos/contrato_json_tela_minima.md
   M docs/contratos/contrato_tela_json.md
   M tela/renderizador.py
   M tela/teste_renderizador.py
  ?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
  ?? docs/handoff/H-0033-ocupacao-integral-corpo.md
  ?? docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
  ?? docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
  ?? docs/relatorios/RELATORIO_QA_ADR-0024.md
  ?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0024.md
  ?? docs/relatorios/RELATORIO_QA_H-0033_HANDOFF.md
  ?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md
  ?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0033_HANDOFF.md
  ?? tela/__pycache__/
```

`tela/__pycache__/` é cache Python gerado automaticamente pela execução dos testes.
Não pertence ao H-0033 nem à ADR-0024.

Arquivos inesperados: nenhum.

---

## 8. Validação pendente

**VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO**

A validação visual em terminal TTY real não foi executada pelo implementador.
Deve ser realizada pelo usuário com o procedimento abaixo:

```bash
# Cenário 42×20
stty size           # deve retornar: 20 42
python demo/demo.py
# pressionar 'd' para destino_minimo, 'g' para grupo_minimo

# Cenário 80×30
stty size           # deve retornar: 30 80
python demo/demo.py
```

Critérios: ausência de faixa vazia entre os elementos visuais e a `barra_de_menus`
em cada dimensão; espaço interno das molduras continua presente; `barra_de_menus`
posicionada corretamente; redimensionamento físico não recria fill externo.

Aprovação visual não pode ser declarada por este relatório.

---

## 9. Patch pós-QA — QA-H0033-IMP-HIGH-001

```yaml
patch:
  achado_corrigido: QA-H0033-IMP-HIGH-001
  titulo: "DA-02 nao e aplicada a containers horizontais sem distribuicao"
  status_pre_patch: NAO_CONFORME
  status_pos_patch: CONFORME

  alteracoes:
    tela/renderizador.py:
      funcao: _renderizar_container_horizontal
      descricao: >
        O ramo else (distribuicao is None e larguras is None) foi substituido
        por logica DA-01/DA-02: N==1 recebe largura integral (DA-01); N>1
        sem distribuicao levanta RenderizadorErro com prefixo "DA-02 (ADR-0024)".
        Comentario na docstring de renderizar_tela atualizado para descrever
        a semantica ADR-0024 (achado QA-H0033-IMP-LOW-001 corrigido
        simultaneamente).

    tela/teste_renderizador.py:
      testes_adaptados:
        - TestArranjoH0019: 9 testes com horizontal+N>1 recebem distribuicao=igual
        - TestPreenchimentoVerticalH0020: 6 testes adaptados; _modelo aceita
          distribuicao=None; test_horizontal_sem_altura_preserva_h0019 usa
          modelo_legado para _montar_corpo_horizontal e modelo com dist para
          renderizar_tela; test_barra_de_menus_preservada_apos_h0020 recebe
          distribuicao=igual
        - TestDistribuicaoHorizontalH0026.test_ausencia_distribuicao_preserva_uniforme:
          reescrito para verificar rejeicao DA-02 (2 e 3 elementos) em vez de
          particionamento uniforme; identificador de achado QA-H0033-IMP-HIGH-001
          presente no comentario
        - TestHierarquiaGruposH0027: 6 testes com grupos horizontais+N>1 recebem
          distribuicao=igual; _modelo_hierarquico ampliado com corpo_distribuicao=None;
          test_corpo_horizontal_com_grupos_filhos usa corpo_distribuicao=igual
      testes_adicionados:
        - test_H1_horizontal_um_participante_sem_dist (DA-01 horizontal)
        - test_H2_horizontal_dois_sem_dist_rejeita (QA-H0033-IMP-HIGH-001)
        - test_H3_horizontal_grupo_multiplos_sem_dist_rejeita (DA-02 via grupo)
        - test_H4_horizontal_aninhado_nao_bypassa_DA02 (DA-02 aninhado)
        - test_H5_horizontal_com_distribuicao_valido (caminho valido)
        - test_H6_matriz_nao_e_rejeitada (caminho matricial distinto)

  suite_canonica_pos_patch:
    tela_teste_renderizador: 1126/1126
    tela_teste_loader: 283/283
    tela_teste_modelo: 163/163
    demo_teste_demo: 358/358
    demo_teste_diagnostico: 30/30
    demo_teste_explorar_barra_de_menus: 38/38
    total: 1998/1998
    falhas: 0

  excecoes_operacionais: []
  arquivos_proibidos_alterados: []
  stage_ou_commit: NAO_EXECUTADO
```

---

## 10. Rastreamento de patches pós-QA

```yaml
patch_pos_QA:
  qa_de_origem: docs/relatorios/RELATORIO_QA_H-0033_IMPLEMENTACAO.md
  status_de_origem: I2_IMPLEMENTATION_PATCH_REQUIRED

  primeiro_patch:
    achados_tratados:
      - QA-H0033-IMP-HIGH-001
      - QA-H0033-IMP-LOW-001
    resultado: CONFORME_NO_CAMINHO_PUBLICO_COM_RESIDUO_EM_HELPER
    arquivos_alterados:
      - tela/renderizador.py
      - tela/teste_renderizador.py
    suite_canonica:
      tela_teste_renderizador: 1126/1126
      tela_teste_loader: 283/283
      tela_teste_modelo: 163/163
      demo_teste_demo: 358/358
      demo_teste_diagnostico: 30/30
      demo_teste_explorar_barra_de_menus: 38/38
      total: 1998/1998
      falhas: 0

  qa_pos_primeiro_patch:
    relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0033_IMPLEMENTACAO.md
    status: I2_IMPLEMENTATION_PATCH_REQUIRED
    achados_novos:
      - QA-H0033-POSPATCH-IMP-MED-001
      - QA-H0033-POSPATCH-IMP-MED-002
      - QA-H0033-POSPATCH-IMP-LOW-001
      - QA-H0033-POSPATCH-IMP-LOW-002

  segundo_patch:
    achados_tratados:
      - QA-H0033-POSPATCH-IMP-MED-001
      - QA-H0033-POSPATCH-IMP-MED-002
      - QA-H0033-POSPATCH-IMP-LOW-001
      - QA-H0033-POSPATCH-IMP-LOW-002
    resultado: PATCH_APLICADO_AGUARDA_QA_POS_PATCH
    arquivos_alterados:
      - tela/renderizador.py
      - tela/teste_renderizador.py
      - docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
    testes_adicionados_ou_atualizados:
      - _montar_corpo_horizontal: logica DA-01/DA-02 alinhada com _renderizar_container_horizontal
      - test_ausencia_distribuicao_preserva_uniforme: renomeado para
          test_ausencia_distribuicao_rejeita_multiplos_participantes
      - calls_montar_corpo_horizontal_N_gt_1: larguras explicitas fornecidas em todos os
          testes geometricos que chamavam o helper diretamente com N>1
      - TestHelperHorizontalH0033Patch2: classe focal adicionada (P1 a P10, 12 verificacoes)
      - docstrings: _montar_corpo_horizontal e _renderizar_container_horizontal atualizadas
    suite_canonica:
      tela_teste_renderizador:
        verificacoes: 1138
        aprovacoes: 1138
        falhas: 0
        codigo_saida: 0
      tela_teste_loader:
        verificacoes: 283
        aprovacoes: 283
        falhas: 0
        codigo_saida: 0
      tela_teste_modelo:
        verificacoes: 163
        aprovacoes: 163
        falhas: 0
        codigo_saida: 0
      demo_teste_demo:
        verificacoes: 358
        aprovacoes: 358
        falhas: 0
        codigo_saida: 0
      demo_teste_diagnostico:
        verificacoes: 30
        aprovacoes: 30
        falhas: 0
        codigo_saida: 0
      demo_teste_explorar_barra_de_menus:
        verificacoes: 38
        aprovacoes: 38
        falhas: 0
        codigo_saida: 0
      total_verificacoes: 2010
      total_aprovacoes: 2010
      total_falhas: 0
      incremento_em_relacao_ao_primeiro_patch: 12
    validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

  qa_pos_segundo_patch:
    relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0033_IMPLEMENTACAO.md
    status: I2_IMPLEMENTATION_PATCH_REQUIRED
    achados_novos:
      - QA-H0033-POSPATCH2-IMP-LOW-001

  terceiro_patch:
    qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0033_IMPLEMENTACAO.md
    status_de_origem: I2_IMPLEMENTATION_PATCH_REQUIRED
    achados_tratados:
      - QA-H0033-POSPATCH2-IMP-LOW-001
    defeito: >
      cardinalidade incoerente entre participantes e larguras explicitas
      nao era validada em _montar_corpo_horizontal. Lista com N !=
      len(larguras) causava IndexError (lista curta) ou descarte silencioso
      (lista longa), sem RenderizadorErro identificavel.
    comportamento_anterior: >
      _montar_corpo_horizontal aceitava larguras explicitas com qualquer
      cardinalidade. Lista curta causava IndexError list index out of range
      no loop de renderizacao. Lista longa podia ser ignorada incidentalmente
      ou disparar validacao de largura minima por acidente.
    comportamento_corrigido: >
      Quando larguras is not None, len(larguras) e comparado com N =
      len(elementos) antes de qualquer processamento. Se L != N, levanta
      RenderizadorErro com mensagem "cardinalidade horizontal incoerente:
      N participante(s) para L largura(s) explicita(s)". O erro ocorre
      antes do loop de renderizacao, garantindo ausencia de saida parcial.
      Casos validos (L == N) e caminhos larguras=None permanecem inalterados.
    arquivos_alterados:
      - tela/renderizador.py
      - tela/teste_renderizador.py
      - docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
    testes_adicionados_ou_atualizados:
      - TestCardinalidadeHorizontalH0033Patch3: classe focal adicionada
          (C1-C12, 14 verificacoes)
      - C1: N=0, L=0 -> retorna '' (coerente)
      - C2: N=0, L=1 -> rejeicao
      - C3: N=1, L=0 -> rejeicao
      - C4: N=1, L=1 -> sucesso
      - C5: N=1, L=2 -> rejeicao
      - C6: N=2, L=1 -> rejeicao
      - C7: N=2, L=2 -> sucesso
      - C8: N=2, L=3 -> rejeicao
      - C9: N=3, L=2 -> rejeicao
      - C10: prova instrumental que erro ocorre antes de renderizacao
      - C11: mensagem informa N e L (2 verificacoes)
      - C12a: larguras=None com N=1 preserva DA-01
      - C12b: larguras=None com N=2 preserva DA-02
    suite_canonica:
      tela_teste_renderizador:
        verificacoes: 1152
        aprovacoes: 1152
        falhas: 0
        codigo_saida: 0
      tela_teste_loader:
        verificacoes: 283
        aprovacoes: 283
        falhas: 0
        codigo_saida: 0
      tela_teste_modelo:
        verificacoes: 163
        aprovacoes: 163
        falhas: 0
        codigo_saida: 0
      demo_teste_demo:
        verificacoes: 358
        aprovacoes: 358
        falhas: 0
        codigo_saida: 0
      demo_teste_diagnostico:
        verificacoes: 30
        aprovacoes: 30
        falhas: 0
        codigo_saida: 0
      demo_teste_explorar_barra_de_menus:
        verificacoes: 38
        aprovacoes: 38
        falhas: 0
        codigo_saida: 0
      total_verificacoes: 2024
      total_aprovacoes: 2024
      total_falhas: 0
      incremento_em_relacao_ao_segundo_patch: 14
    validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

  qa_pos_terceiro_patch:
    relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0033_IMPLEMENTACAO.md
    status: I2_IMPLEMENTATION_PATCH_REQUIRED
    achados_novos:
      - QA-H0033-POSPATCH3-IMP-LOW-001

  quarto_patch:
    qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0033_IMPLEMENTACAO.md
    status_de_origem: I2_IMPLEMENTATION_PATCH_REQUIRED
    achados_tratados:
      - QA-H0033-POSPATCH3-IMP-LOW-001
    defeito: cardinalidade incoerente de larguras explicitas no caminho _renderizar_container_horizontal
    comportamento_anterior: >
      _renderizar_container_horizontal aceitava larguras explicitas sem validar
      len(larguras) == len(elementos). O bloco "if larguras is not None: pass"
      apenas registrava a intencao de usar as larguras, sem checar cardinalidade,
      e o "if N == 0: return ''" era executado antes de qualquer validacao,
      permitindo que listas nao vazias passassem para zero participantes. No loop
      de renderizacao, o acesso larguras[i] levantava IndexError (lista curta) ou
      iterava apenas os participantes existentes, descartando silenciosamente as
      larguras excedentes (lista longa/truncamento). Nao havia RenderizadorErro
      identificavel para esse helper, divergindo de _montar_corpo_horizontal.
    comportamento_corrigido: >
      Antes de "if N == 0: return ''", antes de qualquer ramo de distribuicao,
      e antes de qualquer indexacao/iteracao de larguras, _renderizar_container_horizontal
      agora compara L = len(larguras) com N = len(elementos) quando larguras
      is not None. Se L != N, levanta RenderizadorErro com a mesma mensagem de
      _montar_corpo_horizontal: "cardinalidade horizontal incoerente: N
      participante(s) para L largura(s) explicita(s)". N=0/L=0 retorna ''
      (coerente); N=0/L>0 e rejeitado; N>=1 com L!=N e rejeitado; lista curta
      nao produz IndexError; lista longa nao e truncada. Nenhuma saida parcial
      e produzida: o erro ocorre antes do primeiro efeito observavel. A politica
      agora e coerente entre _renderizar_container_horizontal e _montar_corpo_horizontal,
      sem refatoracao ampla e sem nova regra arquitetural.
    ponto_de_validacao: >
      tela/renderizador.py em _renderizar_container_horizontal: a guarda de
      cardinalidade fica posicionada imediatamente apos "N = len(elementos)",
      antes de "if N == 0: return ''", antes do bloco "if larguras is not None:
      pass", antes do loop "for i, w in enumerate(larguras)" e antes do loop
      "for i, elemento in enumerate(elementos)". Nenhum acesso a larguras[i]
      ou enumerate(larguras) precede a validacao.
    prova_sem_saida_parcial: >
      TestCardinalidadeHorizontalH0033Patch4.H13 (test_H13_erro_antes_de_renderizacao)
      usa dois participantes instrumentados cujo acesso a .tipo so ocorre dentro
      do loop de renderizacao; com N=2/L=1, RenderizadorErro de cardinalidade e
      levantado e tracker permanece [] — confirmando que nenhuma funcao
      descendente (_caixa_de_elemento/_renderizar_container) foi alcancada e
      nenhum participante foi renderizado. O mecanismo detecta o caminho que
      seria executado sem a correcao (o loop de renderizacao), distinguindo-se
      da mera ausencia de retorno. H12 confirma ainda que N=2/L=1 nao levanta
      IndexError e H11 confirma que N=2/L=3 nao produz saida truncada de largura 28.
    arquivos_alterados:
      - tela/renderizador.py
      - tela/teste_renderizador.py
      - docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
    testes_adicionados_ou_atualizados:
      - TestCardinalidadeHorizontalH0033Patch4: classe focal adicionada (H1-H16,
          18 verificacoes), atingindo diretamente _renderizar_container_horizontal.
      - H1: N=0, L=0 -> retorna ''
      - H2: N=0, L=1 -> rejeicao (lista nao vazia para zero participantes)
      - H3: N=1, L=0 -> rejeicao
      - H4: N=1, L=1 -> sucesso (largura 42)
      - H5: N=1, L=2 -> rejeicao
      - H6: N=2, L=1 -> rejeicao (sem IndexError)
      - H7: N=2, L=2 -> sucesso (largura total 42)
      - H8: N=2, L=3 -> rejeicao (sem truncamento)
      - H9: N=3, L=2 -> rejeicao
      - H10: N=3, L=3 -> sucesso (largura total 42)
      - H11: lista longa nao e truncada silenciosamente (sem saida de largura 28)
      - H12: lista curta nao produz IndexError
      - H13: erro antes de renderizacao (participantes instrumentados, tracker=[])
      - H14: mensagem informa contexto horizontal, N=2 e L=1 (2 verificacoes)
      - H15a: N=1, larguras=None -> DA-01 preservada
      - H15b: N=2, larguras=None -> DA-02 preservada
      - H16: N=2, distribuicao=igual -> sucesso sem regressao
    suite_canonica:
      tela_teste_renderizador:
        verificacoes: 1170
        aprovacoes: 1170
        falhas: 0
        codigo_saida: 0
      tela_teste_loader:
        verificacoes: 283
        aprovacoes: 283
        falhas: 0
        codigo_saida: 0
      tela_teste_modelo:
        verificacoes: 163
        aprovacoes: 163
        falhas: 0
        codigo_saida: 0
      demo_teste_demo:
        verificacoes: 358
        aprovacoes: 358
        falhas: 0
        codigo_saida: 0
      demo_teste_diagnostico:
        verificacoes: 30
        aprovacoes: 30
        falhas: 0
        codigo_saida: 0
      demo_teste_explorar_barra_de_menus:
        verificacoes: 38
        aprovacoes: 38
        falhas: 0
        codigo_saida: 0
      total_verificacoes: 2042
      total_aprovacoes: 2042
      total_falhas: 0
      incremento_em_relacao_ao_terceiro_patch: 18
    validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO

  quinto_patch:
    qa_de_origem: docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0033_IMPLEMENTACAO.md
    status_de_origem: I2_IMPLEMENTATION_PATCH_REQUIRED
    achados_tratados:
      - QA-H0033-POSPATCH4-IMP-MED-001
    escopo:
      - tela/teste_renderizador.py
      - docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
    codigo_de_producao_alterado: NAO
    defeito:
      descricao: prova H11 permissiva contra truncamento
    contexto: >
      O codigo do quarto patch permanece tecnicamente correto e confirmado pelo
      QA pos-quarto patch: _renderizar_container_horizontal rejeita cardinalidade
      explicita incoerente antes de qualquer renderizacao, sem IndexError e sem
      truncamento. O defeito tratado neste quinto patch e local ao teste e a
      fidelidade do relatorio — nao ao codigo de producao, que nao foi alterado.
    comportamento_anterior: >
      H11 (em TestCardinalidadeHorizontalH0033Patch4.test_H11_H12_sem_IndexError_e_sem_truncamento)
      era apresentado como prova contra truncamento de lista explicita maior
      (N=2, L=3). No entanto, o teste apenas verificava que a saida nao tinha
      linhas de largura 28 e silenciava tanto RenderizadorErro quanto qualquer
      Exception sem distinguir a classe de dominio. Ele nao exigia
      RenderizadorErro, aceitava sucesso (se a saida nao tivesse largura 28 por
      outro motivo) e aceitava excecao generica. A prova dependia somente da
      ausencia de uma largura especifica na saida, o que e insuficiente.
    comportamento_corrigido: >
      H11 foi fortalecido para exigir simultaneamente: (1) a chamada com
      N=2 e L=3 levanta RenderizadorErro; (2) IndexError reprova; (3) qualquer
      excecao generica diferente de RenderizadorErro reprova; (4) sucesso
      reprova; (5) a mensagem informa contexto horizontal, 2 participantes e
      3 larguras; (6) nenhum participante e renderizado; (7) nenhuma saida
      parcial e produzida. A prova de ausencia de saida parcial usa um tracker
      externo a funcao sob teste, populado pelo acesso a .tipo dentro do loop
      de renderizacao; com a guarda presente, o erro ocorre antes do loop e o
      tracker permanece []. A prova nao depende apenas da ausencia de uma
      largura ou texto especifico na saida. A rastreabilidade nominal H11 foi
      preservada (mesmo metodo test_H11_H12_sem_IndexError_e_sem_truncamento),
      agora subdividido em tres verificacoes estritas de H11 mais a verificacao
      H12.
    prova_H11:
      exige_RenderizadorErro: SIM
      rejeita_IndexError: SIM
      rejeita_excecao_generica: SIM
      rejeita_sucesso: SIM
      verifica_mensagem: "SIM (horizontal, 2 participante(s), 3 largura(s))"
      verifica_ausencia_saida_parcial: "SIM (tracker externo permanece [])"
    testes_adicionados_ou_atualizados:
      - TestCardinalidadeHorizontalH0033Patch4.test_H11_H12_sem_IndexError_e_sem_truncamento:
          H11 reescrito (3 verificacoes estritas) + H12 preservado (1 verificacao)
      - docstring da classe atualizada para refletir fielmente o que H11 prova
    superestimacao_corrigida_no_relatorio: >
      Este bloco registra expressamente que a descricao anterior da prova H11
      (no quarto_patch.prova_sem_saida_parcial) superestimava a garantia
      oferecida pelo teste real. A afirmacao anterior de que "H11 confirma que
      N=2/L=3 nao produz saida truncada de largura 28" descrevia um teste que
      nao exigia RenderizadorErro e silenciava excecoes genericas. A descricao
      anterior e preservada como historico; o quinto patch registra que a prova
      real somente agora atende a matriz obrigatoria exigida pelo QA pos-quarto
      patch. O codigo de producao nao foi alterado: a correcao tecnica ja
      existia desde o quarto patch.
    fidelidade_historica:
      codigo_do_quarto_patch_tecnicamente_correto: CONFIRMADO_PELO_QA_POS_QUARTO_PATCH
      prova_H11_original_insuficiente: CONFIRMADO
      quinto_patch_fortaleceu_o_teste: CONFIRMADO
      descricao_anterior_da_prova_corrigida: SIM (preservando o historico)
      codigo_de_producao_alterado: NAO
    suite_canonica:
      tela_teste_renderizador:
        verificacoes: 1172
        aprovacoes: 1172
        falhas: 0
        codigo_saida: 0
      tela_teste_loader:
        verificacoes: 283
        aprovacoes: 283
        falhas: 0
        codigo_saida: 0
      tela_teste_modelo:
        verificacoes: 163
        aprovacoes: 163
        falhas: 0
        codigo_saida: 0
      demo_teste_demo:
        verificacoes: 358
        aprovacoes: 358
        falhas: 0
        codigo_saida: 0
      demo_teste_diagnostico:
        verificacoes: 30
        aprovacoes: 30
        falhas: 0
        codigo_saida: 0
      demo_teste_explorar_barra_de_menus:
        verificacoes: 38
        aprovacoes: 38
        falhas: 0
        codigo_saida: 0
      total_verificacoes: 2044
      total_aprovacoes: 2044
      total_falhas: 0
      incremento_em_relacao_ao_quarto_patch: 2
    validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

---

## 11. Quinto patch — fortalecimento da prova H11

### 11.1 Origem

O QA pós-quarto patch
(`docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0033_IMPLEMENTACAO.md`,
`status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED`) registrou o achado
**QA-H0033-POSPATCH4-IMP-MED-001**: o teste H11, apresentado como prova contra
truncamento de lista explícita maior, era insuficiente. O QA confirmou
tecnicamente que o código do quarto patch estava correto
(`_renderizar_container_horizontal` rejeita cardinalidade explícita incoerente
antes de qualquer renderização), mas a prova H11 isoladamente:

- não exigia `RenderizadorErro`;
- aceitava exceção genérica;
- aceitava sucesso não truncado;
- dependia apenas da ausência de uma largura específica (28) na saída.

### 11.2 Escopo

Este quinto patch alterou exclusivamente:

- `tela/teste_renderizador.py` — fortalecimento do teste H11;
- `docs/relatorios/IMP-0033-ocupacao-integral-corpo.md` — este relatório.

**Nenhum código de produção foi alterado.** `tela/renderizador.py` permanece
exatamente como confirmado pelo QA pós-quarto patch.

### 11.3 Prova H11 fortalecida

O método `test_H11_H12_sem_IndexError_e_sem_truncamento` da classe
`TestCardinalidadeHorizontalH0033Patch4` foi reescrito. O cenário atinge
diretamente `_renderizar_container_horizontal` com `participantes: 2` e
`larguras_explicitas: 3`. A prova agora exige simultaneamente:

1. a chamada levanta `RenderizadorErro` (reprova `IndexError`, exceção genérica
   e sucesso);
2. a mensagem informa contexto `horizontal`, `2 participante(s)` e
   `3 largura(s)`;
3. ausência de saída parcial — comprovada por um tracker externo à função sob
   teste, populado pelo acesso a `.tipo` dentro do loop de renderização; com a
   guarda presente, o erro ocorre antes do loop e o tracker permanece `[]`.

A prova de ausência de saída parcial não depende apenas da ausência de uma
largura ou texto específico na saída: ela detecta o caminho de renderização
que seria executado sem a correção.

### 11.4 Fidelidade histórica

- O código do quarto patch já estava tecnicamente correto e o QA pós-quarto
  patch confirmou essa correção.
- A prova H11 original era insuficiente.
- O quinto patch fortaleceu o teste para atender à matriz obrigatória exigida
  pelo QA.
- A descrição anterior da prova H11 (no `quarto_patch.prova_sem_saida_parcial`)
  superestimava a garantia oferecida pelo teste real; essa superestimação é
  corrigida neste quinto patch, preservando o histórico anterior sem
  reescrevê-lo retroativamente.
- Não houve alteração no código de produção.

A aprovação formal não é declarada por este relatório. A validação manual em
TTY real permanece pendente (`VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO`).

### 11.5 Suíte canônica — resultados observados

```
python tela/teste_renderizador.py          →  1172/1172  código 0
python tela/teste_loader.py                →   283/283   código 0
python tela/teste_modelo.py                →   163/163   código 0
python demo/teste_demo.py                  →   358/358   código 0
python demo/teste_diagnostico.py           →    30/30    código 0
python demo/teste_explorar_barra_de_menus.py →  38/38   código 0
─────────────────────────────────────────────────────────────
Total                                      →  2044/2044  0 falhas
```

Incremento em relação ao quarto patch: +2 verificações em
`tela/teste_renderizador.py` (H11 passou de 1 verificação permissiva para 3
verificações estritas; H12 preservado como 1 verificação; o método registra
agora 4 verificações no lugar das 2 anteriores).
