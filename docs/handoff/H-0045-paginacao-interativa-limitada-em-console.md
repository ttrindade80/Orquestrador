---
name: H-0045-paginacao-interativa-limitada-em-console
description: "Implementa a paginação interativa limitada do console (ITEM-0003) conforme ADR-0038 D-PAG-01 a D-PAG-14 — página como quarta camada de estado de runtime independente por console, calculada sobre o conteúdo efetivamente renderizado (itens navegáveis e não navegáveis, modo normal e verboso, políticas de quebra por item), sem wrap entre páginas, cursor reposicionado no primeiro item navegável da página de destino, integração com [✥], foco, redimensionamento, modo, seleção múltipla e o protocolo focal da ADR-0037"
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0045
  data_criacao: "2026-07-30"
rastreabilidade:
  contrato_alvo:
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_chip.md
  adr_relacionadas:
    - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
    - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
    - docs/adr/ADR-0034-selecao-multipla-e-fluxo-focal-de-processamento.md
    - docs/adr/ADR-0037-integracao-do-fluxo-focal-com-dry-run-e-restauracao-da-origem.md
  issues_relacionadas:
    - ITEM-0003
  handoffs_anteriores: []
---

# H-0045 — Implementar paginação interativa limitada do console

## 1. Etapa única

Este handoff autoriza exclusivamente:

`IMPLEMENTAR`

Ele não autoriza QA, aprovação, commit ou início de outro ciclo.

## 2. Ordem de autoridade

1. decisão explícita do usuário;
2. ADRs aprovadas e aplicadas (ADR-0038, e as ADRs 0031/0034/0037 que ela especializa);
3. contratos ativos (`contrato_console.md` §12, §22, §23, §24; `contrato_barra_de_menus.md` §24; `contrato_chip.md` §8-9);
4. este handoff.

Se houver falta, divergência ou decisão nova necessária, bloquear com `LEITURA_ADICIONAL_NECESSARIA`.

## 3. Estado comprovado

```yaml
branch: master
head: b88e49bd65ee21c6e1024ad17c1bc3a2fa6f9d96
stage: vazio
adr_0038:
  status: aceita
  qa_da_adr: ADR_APPROVED
  aplicacao_documental: executada
  qa_aplicacao_adr: ADR_APPLICATION_APPROVED  # informado pelo estado transportado ao autor deste handoff
  handoff_criado_no_frontmatter_da_adr: false  # campo da ADR ainda não atualizado; fora do escopo deste handoff
item_0003_no_backlog:
  status: em_andamento
  proxima_acao_registrada: "criar handoff apos QA_APLICACAO_ADR"
h_0045_numeracao: livre  # nenhum arquivo docs/handoff/H-0045-*, nenhuma ocorrência em README/INDICE_ADR/backlog
paginacao_interativa_no_codigo_atual: ausente
  # tela/navegacao.py e tela/renderizador.py declaram explicitamente
  # "sem paginação"; grade_de_itens/mover_* operam sobre o console inteiro,
  # sem noção de página; renderizar_tela não aceita parâmetro de página.
capacidade_fisica_multilinha_ja_existente_no_renderer:
  local: "tela/renderizador.py — _altura_quebra_item, _linhas_distribuicao_matricial, _linhas_fisicas_por_item, _aplicar_indicador_linhas"
  fato: >
    O renderer já calcula, hoje, ocupação física variável por item (modo
    verboso quebra texto em múltiplas linhas dentro da própria célula da
    grade matricial; a altura de cada linha da grade é redistribuída por
    _distribuir_alturas quando algum item excede a altura mínima estimada).
    A paginação não pode presumir "um item = uma linha física": essa
    premissa já é falsa para o renderer atual em modo verboso.
loader_politica_paginacao:
  campo: "politica_paginacao"
  tipo_aceito: string
  vocabulario_fechado: ["sem", "com"]
  local: "tela/loader.py — _POLITICA_PAGINACAO_VALIDOS e _validar_valores_envelope_pre_adr_0028"
  formato_objeto_draft_ja_rejeitado: true  # isinstance(pol_pag, str) já é exigido; objeto já causa TelaEstruturaInvalida
campo_legado_pagina_singular:
  local: "tela/fluxo_execucao.py (self._pagina_suspensa) e estado.get('pagina') em tela/teste_fluxo_execucao.py"
  natureza: inteiro único, não indexado por console
  relacao_com_adr_0038: NAO_CONFIRMADO — não é a representação de página independente por console
    exigida por D-PAG-13; nenhum contrato ou nomenclatura documenta esse campo. Tratado como campo
    de compatibilidade histórico a preservar (não remover, não redefinir sua semântica atual) — ver §6.2.
barra_de_menus_json_documental:
  chip_paginas_ja_especificado: true
  local: "config/elementos/barra_de_menus.json"
  campos: "simbolo [<][>], existencia.eixo_composicao=paginacao/valor_requerido=com, estado_dinamico.condicao_inativo=numero_de_paginas<=1"
layout_console_json_documental:
  bloco_navegacao_ja_preve: "paginacao independente da navegacao; cada pagina e seu proprio toroide; selecao persiste entre paginas"
qa_handoff_anterior:
  relatorio: docs/relatorios/RELATORIO_QA_HANDOFF_H-0045.md
  status: H2_HANDOFF_PATCH_REQUIRED
  achados_corrigidos_por_este_patch:
    - QAH45-001  # §9 substituída por "Decisões técnicas"; sem tabela canônica
    - QAH45-002  # redução técnica incompatível com contrato_console.md §12 (item de uma linha, quebra ignorada, verboso multilinha fora de escopo)
```

## 4. Objetivo

Entregar, em uma única implementação coesa, a paginação interativa limitada
do console (`ITEM-0003`), fechando as 14 decisões da ADR-0038 (D-PAG-01 a
D-PAG-14): cálculo e manutenção de página atual por console, paginação sem
wrap entre extremos, comandos `,`/`<` (anterior) e `.`/`>` (próxima)
dirigidos ao console focado, cursor restrito à página atual, indicador
`página X/Y`, estados contextuais de `[<]`, `[>]` e `[✥]`, e integração com
seleção, foco, redimensionamento, modo e o protocolo focal da ADR-0037.

A paginação é calculada sobre o **conteúdo efetivamente renderizado** do
console (`contrato_console.md` §12): itens navegáveis e itens visíveis não
navegáveis, considerando que modo normal e modo verboso alteram o número de
linhas físicas por item, e que cada item pode declarar política própria de
quebra de página (`evitar_quebra`, `permitir_quebra`,
`permitir_quebra_somente_se_maior_que_pagina`). Renderer e navegação
consomem uma única autoridade de planejamento físico — nunca dois cálculos
paralelos de página (ver §10, D-TEC-04).

## 5. Manifesto fechado de leitura

```yaml
leitura_integral:
  - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  - docs/contratos/contrato_console.md   # secoes 3,4,6,7,8,11,12,14,21,22,23,24
  - docs/contratos/contrato_chip.md      # secoes 4,5,8,9,10,14
  - docs/contratos/contrato_barra_de_menus.md  # secoes 7,8,11,19,20,23,24
  - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - tela/navegacao.py
  - tela/modelo.py
  - tela/selecao.py
  - tela/fluxo_execucao.py
  - demo/demo.py
  - tela/teste_navegacao.py
  - tela/teste_selecao.py
  - tela/teste_fluxo_execucao.py
  - demo/teste_demo_navegacao.py
  - demo/teste_demo_selecao.py

leitura_focal:
  - arquivo: tela/renderizador.py
    comando_busca: "rg -n 'def renderizar_tela|_navegacao_atual|_linhas_barra|regra_existencia|regra_ativo|_linha_base|_caixa_de_elemento|largura_util_itens_console|DESCONTO_ESTRUTURAL_CONSOLE' tela/renderizador.py"
    objetivo: "assinatura de renderizar_tela; mecanismo de _navegacao_atual (dict de módulo, reiniciado por chamada); avaliação de regra_existencia/regra_ativo em _linhas_barra (~2034-2255); autoridade única de geometria em largura_util_itens_console (545-582); ponto de composição da borda inferior em _linha_base (226) e _caixa/_caixa_de_elemento (246, 2756-2830) onde o indicador 'página X/Y' deve ser inserido"
  - arquivo: tela/renderizador.py
    comando_busca: "rg -n '_altura_quebra_item|_linhas_distribuicao_matricial|_linhas_fisicas_por_item|_aplicar_indicador_linhas|_item_corrente_de_contexto|_escrever_item_com_indicador' tela/renderizador.py"
    objetivo: "confirmar a capacidade física JÁ EXISTENTE de item multilinha em modo verboso dentro da grade matricial (_altura_quebra_item, redistribuição de altura por linha da grade); confirmar o mapeamento índice-de-linha-física -> id-do-item (_linhas_fisicas_por_item) e a regra de que somente a PRIMEIRA linha física do item corrente recebe o símbolo de cursor (_aplicar_indicador_linhas) — esta é a base para definir, sem inventar regra nova, a qual página pertence um item navegável fragmentado (D-TEC-17)"
  - arquivo: tela/loader.py
    comando_busca: "rg -n 'politica_paginacao|_POLITICA_PAGINACAO_VALIDOS|_validar_valores_envelope_pre_adr_0028|_console_em_escopo_d23|politica_quebra' tela/loader.py"
    objetivo: "confirmar que politica_paginacao já é validada como string 'sem'/'com' (linha ~1644, ~1717-1722) e que o formato objeto antigo já é rejeitado; verificar se politica_quebra por item já possui alguma validação de vocabulário fechado no loader — se não possuir, decidir se a ausência de validação é aceitável para este ciclo (leitura obrigatória e explícita antes de decidir; não presumir)"
  - arquivo: tela/fluxo_execucao.py
    comando_busca: "rg -n '_pagina_suspensa|_capturar_estado_suspensao|_retorno_dry_run|_retorno_real|_reconciliar_foco_cursor|_retornar_de_resultado|_limpar_refs_proprias|_ids_cursor_suspensos' tela/fluxo_execucao.py"
    objetivo: "localizar exatamente onde estender a captura/restauração/reconciliação com um novo campo self._paginas_suspensas, seguindo o MESMO padrão já usado por self._cursores_suspensos e self._ids_cursor_suspensos (captura ~331-352, retorno dry-run ~384-400, retorno real ~402-428, reconciliação ~430-469, limpeza ~471-483, chaves preservadas em _retornar_de_resultado ~358-382)"
  - arquivo: tela/teste_fluxo_execucao.py
    comando_busca: "rg -n 'def teste_retorno_dry_run|def teste_retorno_real_preserva_cursor|def teste_retorno_real_fallback_cursor|pagina' tela/teste_fluxo_execucao.py"
    objetivo: "localizar o par canônico de testes de preservação/fallback de cursor (teste_retorno_dry_run_zero_recargas, teste_retorno_real_preserva_cursor_por_id, teste_retorno_real_fallback_cursor) como modelo estrutural para os testes equivalentes de página"
  - arquivo: config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
    comando_busca: "cat config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json"
    objetivo: "confirmar estrutura de distribuicao_matricial.formacao (politica preferencia_linhas, linhas.maximo) para calibrar um cenário h0045_* com teto de itens por linha que force overflow em 3+ páginas em 80x24"
  - arquivo: config/telas/demo/h0044_fluxo_execucao_integrado.json
    comando_busca: "cat config/telas/demo/h0044_fluxo_execucao_integrado.json"
    objetivo: "usar como esqueleto do novo cenário h0045_fluxo_execucao_paginado.json (mesmos campos de console/chip_dry_run), sem alterar o arquivo original"

buscas_autorizadas:
  - "rg -n 'pagina|página|paginacao|paginação|pagina_atual|cursores|foco_console|selecoes|\\[<\\]|\\[>\\]|\\[✥\\]|redimension|verboso|filtro|politica_quebra|evitar_quebra|permitir_quebra' tela/navegacao.py tela/renderizador.py tela/loader.py tela/modelo.py tela/selecao.py tela/fluxo_execucao.py demo/demo.py tela/teste_navegacao.py tela/teste_renderizador.py tela/teste_loader.py tela/teste_selecao.py tela/teste_fluxo_execucao.py demo/teste_demo_navegacao.py demo/teste_demo_selecao.py demo/teste_demo.py"
    limite: "somente dentro dos arquivos listados; sem busca recursiva ampla"

nao_ler:
  - docs/relatorios/**, salvo os relatórios da cadeia ADR-0038/H-0045 já verificados por `test -f` (RELATORIO_QA_ADR-0038.md, RELATORIO_APLICACAO_ADR-0038.md, RELATORIO_QA_APLICACAO_ADR-0038.md, RELATORIO_QA_HANDOFF_H-0045.md, RELATORIO_PATCH_HANDOFF_H-0045_P01.md) — mesmo estes, apenas como evidência de existência/cadeia, não de conteúdo integral
  - outros handoffs (docs/handoff/H-0001..H-0044*)
  - outras ADRs além de 0038/0031/0034/0037
  - outros contratos além de console/chip/barra_de_menus
  - outros módulos de nomenclatura além de 21/31/32
  - config/telas/demo/demo.json (rascunho histórico com formato draft antigo — não é fonte de schema)
  - qualquer outro arquivo de config/telas/demo/*.json não citado nominalmente acima
```

Para leitura focal, execute o comando indicado e leia somente sua saída. Se a
saída for insuficiente, pare com `LEITURA_ADICIONAL_NECESSARIA`; não amplie
autonomamente o contexto.

## 6. Escopo da implementação

### 6.1 Arquivos e diretórios autorizados

```yaml
arquivos_a_criar:
  - caminho: tela/paginacao.py
    finalidade: >
      API pura (sem estado de módulo, sem I/O) de cálculo de páginas e
      transição de página, seguindo o padrão de tela/navegacao.py e
      tela/selecao.py. Consome exclusivamente navegacao.grade_de_itens (para
      identidade/topologia lógica do cursor) e o mapa físico de conteúdo
      exposto por tela/renderizador.py (para ocupação real de linhas —
      D-TEC-04); nenhuma grade paralela.
    motivo_da_inclusao_ou_preservacao: >
      Autoridade única de planejamento físico de paginação, reutilizável por
      navegação, renderer e fluxo focal (D-TEC-03/04). Preservado do
      handoff original; escopo revisto para conteúdo multilinha e políticas
      de quebra (correção do achado QAH45-002).
  - caminho: tela/teste_paginacao.py
    finalidade: Testes unitários puros da API de tela/paginacao.py.
    motivo_da_inclusao_ou_preservacao: >
      Prova nominal de cálculo de páginas, extremos, conjunto vazio,
      fragmentação por política de quebra e identidade de fragmento —
      cobertura ampliada em relação ao handoff original (§11).
  - caminho: demo/teste_demo_paginacao.py
    finalidade: >
      Testes ponta-a-ponta via demo.py (carregar_tela -> construir_modelo ->
      processar_comando -> renderizar_estado), no padrão de
      demo/teste_demo_navegacao.py e demo/teste_demo_selecao.py.
    motivo_da_inclusao_ou_preservacao: >
      Prova semântica de integração sem TTY real; ampliado para repaginação
      material por mudança de modo e para as três políticas de quebra.
  - caminho: config/telas/demo/h0045_paginacao_console_unico.json
    finalidade: >
      Console único, coluna única, com itens suficientes para produzir 3 ou
      mais páginas em 80x24 (geometria controlada — ver §18.3; a quantidade
      exata de páginas é derivada da capacidade física efetiva, não fixada
      por este handoff), misturando itens navegáveis e não navegáveis de
      modo que uma página intermediária fique sem item navegável;
      politica_selecao "multipla" para provar seleção persistente entre
      páginas e Todos sobre todas as páginas no mesmo cenário.
    motivo_da_inclusao_ou_preservacao: >
      Cenário principal de paginação limitada, extremos, cursor, página sem
      navegáveis e seleção. Preservado do handoff original.
  - caminho: config/telas/demo/h0045_paginacao_conjunto_vazio.json
    finalidade: >
      Console único com politica_paginacao "com" e zero itens navegáveis
      (itens: [] ou todos navegavel:false), não focalizável (ADR-0031 D2).
    motivo_da_inclusao_ou_preservacao: >
      Prova D-PAG-12 (indicador "página 1/1" na própria borda, independente
      de foco) e D-PAG-13 ([<][>] inativos sem console focado). Preservado
      do handoff original.
  - caminho: config/telas/demo/h0045_dois_consoles_paginas_independentes.json
    finalidade: >
      Dois consoles focalizáveis lado a lado (ou empilhados), cada um
      paginado com estado próprio.
    motivo_da_inclusao_ou_preservacao: >
      Prova D-PAG-13 (independência de página por console) e D-PAG-05
      (retorno por Tab/Shift+Tab preserva a página anterior do console).
      Preservado do handoff original.
  - caminho: config/telas/demo/h0045_fluxo_execucao_paginado.json
    finalidade: >
      Console paginado (2+ páginas) integrado ao protocolo focal (esqueleto
      análogo a h0044_fluxo_execucao_integrado.json).
    motivo_da_inclusao_ou_preservacao: >
      Prova retorno de dry-run preservando página e retorno de execução real
      reconciliando a página que contém o item pelo ID preservado, com
      fallback para a primeira página quando o ID deixa de existir.
      Preservado do handoff original.
  - caminho: config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
    finalidade: >
      Console único paginado cujos itens produzem, em modo verboso, mais de
      uma linha física por item (texto acima da largura útil da célula),
      forçando limites de página diferentes em modo normal e em modo
      verboso.
    motivo_da_inclusao_ou_preservacao: >
      NOVO — corrige a exclusão indevida de "modo verboso multi-linha +
      paginação" apontada por QAH45-002. Prova D-PAG-06 (repaginação
      material por mudança de modo) e conteúdo multilinha em página.
  - caminho: config/telas/demo/h0045_paginacao_politicas_quebra.json
    finalidade: >
      Console único paginado cujos itens declaram, respectivamente,
      evitar_quebra, permitir_quebra e permitir_quebra_somente_se_maior_que_pagina;
      inclui ao menos um item cujo conteúdo excede sozinho a capacidade
      física de uma página vazia.
    motivo_da_inclusao_ou_preservacao: >
      NOVO — corrige a leitura-e-ignora silenciosa de politica_quebra
      apontada por QAH45-002. Prova as três políticas com efeito real e o
      caso de item maior que uma página inteira.

arquivos_a_alterar:
  - caminho: tela/navegacao.py
    finalidade: >
      1) mover_direita/mover_esquerda/mover_baixo/mover_cima (e os núcleos
      _mover_horizontal/_mover_vertical) passam a aceitar um intervalo
      opcional de linhas (inicio, fim) que restringe o domínio de wrap de
      _linha_com_itens/_coluna_com_itens à página atual; default (None)
      preserva integralmente o comportamento H-0040 sem paginação.
      _posicao_do_item_logico/item_logico_de_posicao NÃO mudam de
      assinatura nem de semântica (continuam operando sobre a grade LÓGICA
      completa retornada por grade_de_itens, preservando a identidade global
      do item lógico já usada por cursores[console.id] desde a ADR-0031—
      D-TEC-02).
      2) exibir_chip_navegar (D14/D-PAG-04) passa a restringir a contagem de
      itens navegáveis à página atual do console focado quando este declara
      politica_paginacao "com".
      Import de tela.paginacao feito LOCALMENTE dentro das funções que
      precisam dele (mesmo padrão já usado em tela/renderizador.py para
      evitar import circular).
    motivo_da_inclusao_ou_preservacao: >
      Restringe o domínio de wrap toroidal à página atual sem duplicar
      cálculo de geometria (D-TEC-05). Preservado do handoff original.
  - caminho: tela/teste_navegacao.py
    finalidade: >
      Novos testes cobrindo o intervalo de linhas restrito e a extensão de
      exibir_chip_navegar; nenhum teste existente é alterado.
    motivo_da_inclusao_ou_preservacao: Regressão e cobertura de D-PAG-04.
  - caminho: tela/teste_loader.py
    finalidade: >
      Novo teste de regressão explícito confirmando que o loader rejeita o
      formato objeto antigo {"politica_paginacao": {"paginacao": "com"}}
      (comportamento já existente — apenas fixado por teste nominal).
    motivo_da_inclusao_ou_preservacao: Regressão nominal de D-TEC-13.
  - caminho: tela/fluxo_execucao.py
    finalidade: >
      Novo campo self._paginas_suspensas (dict id_console -> int), seguindo
      EXATAMENTE o padrão de self._cursores_suspensos e
      self._ids_cursor_suspensos: capturado em _capturar_estado_suspensao a
      partir de estado.get("pagina_atual", {}); copiado 1:1 em
      _retorno_dry_run; incluído na tupla de chaves preservadas de
      _retornar_de_resultado; reconciliado por ID em _retorno_real via nova
      função companheira de _reconciliar_foco_cursor que usa
      tela.paginacao.pagina_do_item_logico para recalcular a página que
      contém o item preservado (fallback: página 1); zerado em
      _limpar_refs_proprias. O campo legado singular self._pagina_suspensa
      é preservado sem alteração de comportamento.
    motivo_da_inclusao_ou_preservacao: Integração com o protocolo focal (D-TEC-14).
  - caminho: tela/teste_fluxo_execucao.py
    finalidade: >
      Novos testes espelhando teste_retorno_dry_run_zero_recargas,
      teste_retorno_real_preserva_cursor_por_id e
      teste_retorno_real_fallback_cursor para a página; nenhum teste
      existente é alterado.
    motivo_da_inclusao_ou_preservacao: Regressão e cobertura de D-TEC-14.
  - caminho: demo/demo.py
    finalidade: >
      1) criar_estado_inicial ganha a chave "pagina_atual": {} (dict
      runtime, paralelo a "cursores"/"selecoes"; nunca persiste em JSON).
      2) processar_comando reconhece as entradas "," "<" "." ">" no MESMO
      bloco condicional que hoje trata Tab/Shift+Tab/setas/Espaço/Enter,
      delegando a tela.paginacao.pagina_anterior/pagina_proxima.
      3) renderizar_estado repassa estado.get("pagina_atual", {}) como novo
      argumento paginas_atuais de renderizar_tela.
    motivo_da_inclusao_ou_preservacao: Integração de runtime (D-TEC-09).

arquivos_a_preservar:
  - tela/renderizador.py  # REMOVIDO DO ESCOPO ATIVO [PATCH_HANDOFF P05] — ver §6.2 e §19.6; nenhuma nova alteração autorizada
  - tela/teste_renderizador.py  # mesma condição do item acima — ver §6.2 e §19.6
  - docs/adr/ADR-0038-paginacao-interativa-limitada-em-console.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/backlog.md
  - docs/adr/INDICE_ADR.md
  - config/telas/demo/h0040_nav_matriz_26_itens_redimensionamento.json
  - config/telas/demo/h0040_nav_dois_consoles.json
  - config/telas/demo/h0041_selecao_multipla_oito_itens.json
  - config/telas/demo/h0044_fluxo_execucao_integrado.json
  - config/telas/demo/resultado_execucao.json
  - config/telas/demo/demo.json
  - config/elementos/barra_de_menus.json
  - config/layouts/layout_console.json
  - config/estilo.json
  - tela/selecao.py  # sem alteração: seleção já é independente de página

diretorios_a_criar: []
```

### 6.2 Arquivos e diretórios preservados ou proibidos

- **`tela/renderizador.py` e `tela/teste_renderizador.py` estão fora do
  escopo ativo desta implementação [PATCH_HANDOFF P05, achado
  QA-H0045-P04-001].** A extensão de paginação do renderer (mapa físico de
  ocupação por item, recorte de conteúdo por página, indicador "página
  X/Y", regras de `[<]`/`[>]`) já foi aplicada em ciclo de implementação
  anterior; a análise causal
  (`RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md`, prova D)
  não encontrou defeito nele — `RENDERER_REGRESSION` permanece não
  classificada. Nenhuma nova alteração desses dois arquivos é autorizada por
  este handoff, nem por qualquer patch subsequente de paginação ou de
  harness de validação. Uma futura alteração do renderer só é autorizada
  se, cumulativamente: (1) surgir evidência nova e objetiva de defeito nele;
  (2) essa evidência for registrada em relatório; (3) houver autorização
  específica posterior do usuário/gerente — não esta autorização genérica.
  Nenhuma decisão técnica deste handoff (D-TEC-04, D-TEC-06, D-TEC-10,
  D-TEC-11, D-TEC-12) reabre essa autorização; elas descrevem extensões já
  aplicadas, preservadas como registro (ver nota de fechamento após
  D-TEC-12). **[PATCH_HANDOFF P07]** As três condições acima foram
  cumpridas para um achado específico e novo — `VM-H0045-R07-001` (largura
  horizontal do conteúdo do console,
  `RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_LARGURA_HORIZONTAL.md`). A
  autorização correspondente, estritamente limitada a esse achado, está em
  §20; fora dela, a exclusão geral acima permanece integralmente vigente.
  **[PATCH_HANDOFF P08]** A correção de `VM-H0045-R07-001` aplicada pelo
  `PATCH_IMPLEMENTACAO P17` (`tela/renderizador.py`,
  `tela/teste_renderizador.py`, dentro do escopo de §20) desatualizou cinco
  asserções numéricas em `demo/teste_demo_paginacao.py` e
  `demo/teste_demo_navegacao.py`, calibradas contra a geometria anterior ao
  patch (identificador gerencial `IMP-H0045-P17-001`). A autorização focal
  correspondente, restrita a esses dois arquivos e aos cinco testes
  nominalmente listados, está em §21; não autoriza nenhuma alteração
  adicional de `tela/renderizador.py`/`tela/teste_renderizador.py` além da
  já registrada em §20, nem de qualquer outro arquivo.
- Nenhum contrato, ADR, backlog, índice de ADR ou módulo de nomenclatura pode
  ser alterado por esta implementação.
- `tela/selecao.py` permanece intocado: a seleção já é um conjunto de IDs
  independente de posição/página (D-SEL-01/D-SEL-02); nenhuma mudança de
  comportamento de seleção é necessária para paginação.
- O campo legado `self._pagina_suspensa` (`tela/fluxo_execucao.py`) e a
  chave `estado.get("pagina")` (usada por `tela/teste_fluxo_execucao.py`)
  são preservados sem alteração de semântica — não é a representação por
  console exigida pela ADR-0038; um novo campo `self._paginas_suspensas`
  (dict) é adicionado ao lado dele, sem remover ou redefinir o legado.
- Nenhuma biblioteca `curses`, `ncurses`, `textual` ou `rich` pode ser
  introduzida.
- Nenhum mecanismo de alternate screen, SIGWINCH, cbreak, ISIG ou
  restauração de terminal em `demo/demo.py` pode ser alterado.
- `config/telas/demo/demo.json` permanece rascunho; seu formato antigo de
  `politica_paginacao` como objeto não é reativado nem usado como referência
  de schema.
- Consoles que declaram `conteudo_externo` hierárquico (H-0036: apresentação
  `hierarquia`, `tabela` ou `conjuntos`) permanecem **fora do universo
  paginado** deste ciclo — não porque item multilinha seja proibido (a
  ADR-0038 não distingue por tipo de apresentação), mas porque nenhuma das
  14 decisões D-PAG-01 a D-PAG-14 é fraseada nesses termos: todas operam
  sobre item navegável, cursor e console focado do modelo de
  `distribuicao_matricial` já coberto pela navegação de nível único
  (ADR-0031/H-0040). Estender paginação a `conteudo_externo` hierárquico é
  decisão de ciclo próprio (ver D-TEC-06); esta fronteira é preservação de
  um limite já existente desde a H-0036, não uma redução nova introduzida
  por este handoff.

### 6.3 Escopo positivo

- Cálculo e manutenção de página atual por console (`estado["pagina_atual"]`,
  dict `id_console -> int`).
- Paginação limitada sem wrap entre extremos (D-PAG-01).
- Comandos `,`/`<` (anterior) e `.`/`>` (próxima) sobre o console focado
  (D-PAG-14, D-PAG-13).
- Cursor restrito à página atual; reposicionado no primeiro item navegável
  da página de destino após troca explícita (D-PAG-02) ou retorno por foco
  (D-PAG-05).
- Página sem item navegável permanece acessível, sem cursor, com setas sem
  movimento (D-PAG-03).
- Indicador `página X/Y`, inclusive para uma única página e para conjunto
  vazio (D-PAG-11, D-PAG-12).
- Estados contextuais de `[<]`, `[>]` (D-PAG-01, D-PAG-13) e restrição de
  `[✥]` à página atual (D-PAG-04).
- Repaginação por redimensionamento e mudança de modo, preservando o item
  lógico corrente (D-PAG-06).
- Reconciliação de cursor/página por filtro (D-PAG-07 a D-PAG-09) e por
  atualização genérica dos dados (D-PAG-10), provadas por alteração
  controlada da lista de itens em memória — sem sistema genérico de filtro.
- Independência de página por console (D-PAG-13).
- Integração com seleção múltipla (persistência entre páginas, `Todos`
  sobre todas as páginas do conjunto filtrado).
- Integração com o protocolo focal da ADR-0037: preservação de página em
  retorno de `dry-run`; reconciliação de página por ID no retorno de
  execução real, com fallback à primeira página.
- **Paginação sobre o conteúdo efetivamente renderizado** (`contrato_console.md`
  §12): itens navegáveis, itens visíveis não navegáveis, uma ou várias
  linhas físicas por item, modo normal e modo verboso — calculada por uma
  autoridade única de planejamento físico compartilhada entre renderer e
  navegação (D-TEC-03/04).
- As três políticas de quebra de página (`evitar_quebra`, `permitir_quebra`,
  `permitir_quebra_somente_se_maior_que_pagina`, `contrato_console.md` §12)
  aplicadas com efeito real sobre a composição de páginas, inclusive o caso
  de item cujo conteúdo excede sozinho a capacidade física de uma página
  vazia (D-TEC-07).
- Repaginação material por mudança de modo (normal ↔ verboso) quando a
  ocupação física real muda — não apenas alternância de flag sem diferença
  física (D-PAG-06).

### 6.4 Escopo negativo

- `ITEM-0018` (limitar `Todos` à página atual) — permanece bloqueado/fora
  deste ciclo.
- Seleção compartilhada entre consoles (`ITEM-0019`).
- Toggle universal real/`dry-run` (`ITEM-0020`).
- Modos adicionais de tela de resultado (`ITEM-0021`).
- Registro genérico de ações (`ITEM-0004`) e pilha genérica de telas
  (`ITEM-0005`).
- Paginação multinível colapsável (`ITEM-0007`).
- Binding real com o Pipeline; persistência entre sessões; schema
  declarativo novo de `politica_paginacao`; cache ou renderização parcial;
  otimizações de desempenho sem necessidade comprovada.
- Paginação circular; alteração automática de página pelas setas; mudança
  de página de console não focado.
- Sistema genérico de filtros (ainda inexistente) — não criado por este
  ciclo.
- Paginação de consoles com `conteudo_externo` hierárquico (apresentação
  `hierarquia`/`tabela`/`conjuntos`, H-0036) — ver §6.2 e D-TEC-06;
  fronteira preservada, não redução nova.

## 7. Entradas, fixtures, temporários e saídas

```yaml
entradas_reais:
  - tela estrutural validada (config/telas/demo/h0045_*.json, novos)
  - itens do console (declarados nos JSONs novos, envelope pré-ADR-0028,
    incluindo o campo já contratado politica_quebra por item)
  - comando de teclado (",", "<", ".", ">", além dos já existentes)

fixtures:
  - config/telas/demo/h0045_paginacao_console_unico.json
  - config/telas/demo/h0045_paginacao_conjunto_vazio.json
  - config/telas/demo/h0045_dois_consoles_paginas_independentes.json
  - config/telas/demo/h0045_fluxo_execucao_paginado.json
  - config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
  - config/telas/demo/h0045_paginacao_politicas_quebra.json

configuracoes:
  - config/estilo.json (leitura, sem alteração)
  - config/elementos/barra_de_menus.json (leitura documental, sem alteração)

temporarios_operacionais:
  - nenhum arquivo temporário obrigatório; somente estruturas em memória
    (grade lógica de itens, mapa físico de linhas por item, intervalos de
    página) necessárias ao cálculo, descartadas ao final de cada chamada pura

saidas_geradas:
  - novo estado de runtime: estado["pagina_atual"] (dict id_console -> int)
  - página corrente renderizada (recorte do conteúdo físico do console,
    inclusive itens multilinha em modo verboso)
  - indicador "página X/Y" na borda do console paginado
  - estados contextuais de [<], [>] e [✥]
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0045.md (relatório desta execução)

politica_de_sobrescrita: nenhum arquivo de entrada real é sobrescrito; fixtures novas são criadas, não editadas depois de criadas neste ciclo
politica_de_limpeza: nenhuma — não há temporários em disco a limpar
```

Persistência em arquivo ou entre sessões é proibida. Nenhuma evidência
material pode permanecer somente em `/tmp`.

## 8. Tarefas

1. Criar `tela/paginacao.py` com a API pura descrita em §10 (Decisões
   técnicas D-TEC-01 a D-TEC-05, D-TEC-07, D-TEC-08, D-TEC-17), consumindo
   sem alterar a função física já exposta por `tela/renderizador.py`
   (D-TEC-04; renderer fora do escopo ativo — ver §6.2, §19.6).
2. Estender `tela/navegacao.py` (intervalo de linhas restrito nos
   movimentos da grade lógica; `exibir_chip_navegar` restrito à página
   atual) — D-TEC-05, D-TEC-15.
3. Estender `demo/demo.py` (`criar_estado_inicial`, `processar_comando`,
   `renderizar_estado`; remoção da reconstrução de modelo durante resize —
   §19.1) — D-TEC-09.
4. Estender `tela/fluxo_execucao.py` (`self._paginas_suspensas`, captura,
   retorno de `dry-run`, reconciliação por ID no retorno real, limpeza) —
   D-TEC-14.
5. Criar/ajustar os cenários `config/telas/demo/h0045_*.json` descritos em
   §6.1 e as três telas fixas de validação por política de §19.2, calibrados
   para permitir redimensionamento livre pelo usuário (3+ páginas no
   cenário principal; ao menos um cenário com multilinha em modo verboso;
   `H0045-VAL-VAZIO` e `H0045-VAL-CONTINUACAO` com conteúdo fixo — §19.3).
6. Criar `tela/teste_paginacao.py`, `demo/teste_demo_paginacao.py` e
   estender `tela/teste_navegacao.py`, `tela/teste_loader.py`,
   `tela/teste_fluxo_execucao.py` conforme §11 e §19.4.
7. Executar as verificações locais previstas (§11, §12, §19.4).
8. Criar o relatório desta execução usando o template canônico (§13).

## 9. Critérios de aceite

| ID | Critério | Evidência independente esperada |
|---|---|---|
| CA-H0045-01 | Paginação limitada: sem efeito ao recuar na primeira página nem ao avançar na última (D-PAG-01) | `tela/teste_paginacao.py`: teste nominal de `pagina_anterior`/`pagina_proxima` nos extremos, com estado antes/depois comparado campo a campo |
| CA-H0045-02 | Cursor reposicionado no primeiro item navegável da página de destino após troca explícita (D-PAG-02) | `demo/teste_demo_paginacao.py`: comparação de `cursores[console.id]` antes/depois de `"."`/`">"`/`","`/`"<"` via `processar_comando` |
| CA-H0045-03 | Página com conteúdo visível e zero itens navegáveis permanece acessível, sem cursor, setas sem movimento (D-PAG-03) | `demo/teste_demo_paginacao.py` sobre `h0045_paginacao_console_unico.json`: quadro renderizado da página intermediária comparado linha a linha; ausência de símbolo de cursor verificada textualmente |
| CA-H0045-04 | Conjunto vazio produz página lógica `1/1`, `[<]`/`[>]` inativos, sem cursor (D-PAG-12) | `tela/teste_paginacao.py` sobre `h0045_paginacao_conjunto_vazio.json`; regressão da cobertura já existente de `tela/teste_renderizador.py` executada sem alteração deste arquivo (§6.2, §19.6) |
| CA-H0045-05 | Conteúdo multilinha (modo verboso) é fatiado em páginas sem perda nem duplicação de linhas físicas | `tela/teste_paginacao.py` sobre `h0045_paginacao_modo_verboso_multilinha.json`: soma de linhas físicas por item across páginas comparada à contagem total calculada isoladamente; regressão da cobertura já existente de `tela/teste_renderizador.py` executada sem alteração deste arquivo (§6.2, §19.6) |
| CA-H0045-06 | Política `evitar_quebra`: item movido inteiro para a página seguinte quando possível; quebra permitida somente se não couber nem em página vazia | `tela/teste_paginacao.py` sobre `h0045_paginacao_politicas_quebra.json`, incluindo o caso do item maior que uma página |
| CA-H0045-07 | Política `permitir_quebra`: item pode atravessar páginas livremente | `tela/teste_paginacao.py` sobre o mesmo cenário, item declarado `permitir_quebra` |
| CA-H0045-08 | Política `permitir_quebra_somente_se_maior_que_pagina`: evita quebra salvo quando não cabe nem em página vazia | `tela/teste_paginacao.py` sobre o mesmo cenário, item declarado com essa política |
| CA-H0045-09 | Fragmentos de um item quebrado preservam identidade (mesmo `item_logico_ou_id`) e não perdem/duplicam linhas | `tela/teste_paginacao.py`: soma de `linhas_fisicas` de todos os fragmentos de um item == ocupação física total do item, calculada independentemente |
| CA-H0045-10 | Modo normal e modo verboso alteram materialmente o número de linhas por item e, portanto, os limites de página (contrato_console.md §12) | `demo/teste_demo_paginacao.py` sobre `h0045_paginacao_modo_verboso_multilinha.json`: `total_paginas`/limites de página comparados entre os dois modos, com diferença física comprovada (não apenas alternância de flag) |
| CA-H0045-11 | Repaginação por mudança de modo preserva o item lógico corrente; página recalculada sem preservar o número anterior (D-PAG-06) | mesmo teste acima, comparando o item lógico do cursor antes/depois da troca de modo |
| CA-H0045-12 | Repaginação por redimensionamento preserva o item lógico corrente | `demo/teste_demo_paginacao.py`: `renderizar_estado` chamado com larguras/alturas distintas sobre o mesmo modelo, item lógico do cursor comparado |
| CA-H0045-13 | Filtro que oculta o item corrente ou zera navegáveis reconcilia cursor/página por prioridade determinística (D-PAG-07 a D-PAG-09) | `demo/teste_demo_paginacao.py`: alteração controlada da lista de itens em memória, estado de cursor/página comparado antes/depois |
| CA-H0045-14 | Atualização genérica que remove o item corrente segue D-PAG-10 sem sobrescrever a reconciliação por ID da ADR-0037 | `tela/teste_fluxo_execucao.py` (extensão) + `demo/teste_demo_paginacao.py` |
| CA-H0045-15 | Dois consoles mantêm páginas independentes; comando de página afeta somente o console focado (D-PAG-13) | `demo/teste_demo_paginacao.py` sobre `h0045_dois_consoles_paginas_independentes.json` |
| CA-H0045-16 | Retorno por Tab/Shift+Tab preserva a página anterior do console; cursor reposicionado no primeiro navegável dessa página (D-PAG-05) | mesmo cenário acima, sequência Tab/Shift+Tab comparada |
| CA-H0045-17 | Seleção múltipla persiste entre páginas; `Todos` abrange o conjunto filtrado em todas as páginas | `demo/teste_demo_paginacao.py` sobre `h0045_paginacao_console_unico.json`, reaproveitando `tela/selecao.py` sem alteração |
| CA-H0045-18 | Retorno de `dry-run` preserva página; retorno de execução real reconcilia página por ID, com fallback à primeira página | `tela/teste_fluxo_execucao.py` (extensão) sobre `h0045_fluxo_execucao_paginado.json`, espelhando os testes canônicos de cursor |
| CA-H0045-19 | Indicador `página X/Y` correto em cada página, inclusive `1/1` para página única e conjunto vazio (D-PAG-11, D-PAG-12) | `tela/teste_renderizador.py`: cobertura já existente (comparação textual da borda inferior renderizada), executada para confirmar ausência de regressão — nenhuma extensão ou alteração deste arquivo é exigida ou autorizada (§6.2, §19.6) |
| CA-H0045-20 | Chips `[<]`/`[>]` refletem o estado da página do console focado; inativos sem console focado ou com console focado sem paginação (D-PAG-13) | `tela/teste_renderizador.py`: cobertura já existente, executada para confirmar ausência de regressão — nenhuma extensão ou alteração deste arquivo é exigida ou autorizada (§6.2, §19.6) |
| CA-H0045-21 | `[✥]` restrito à página atual do console focado (D-PAG-04) | `tela/teste_navegacao.py` (extensão) |
| CA-H0045-22 | Loader rejeita o formato objeto antigo de `politica_paginacao` (regressão fixada nominalmente) | `tela/teste_loader.py` (extensão): teste nominal com asserção de `TelaEstruturaInvalida` |
| CA-H0045-23 | Renderer e navegação usam o mesmo plano físico de paginação; página exibida é a mesma usada pelas setas; cursor nunca aponta item fora da página | `tela/teste_paginacao.py` + `demo/teste_demo_paginacao.py`: comparação cruzada entre o intervalo retornado por `tela.paginacao` e a página efetivamente recortada pelo renderer para o mesmo estado |
| CA-H0045-24 | Duas alturas de console (dois consoles, ou o mesmo console redimensionado) produzem planos de página independentes, sem divergência física/lógica | `demo/teste_demo_paginacao.py` |
| CA-H0045-25 | Regressão completa: nenhuma asserção pré-existente de `tela/teste_navegacao.py`, `tela/teste_renderizador.py`, `tela/teste_loader.py`, `tela/teste_selecao.py`, `tela/teste_fluxo_execucao.py`, `demo/teste_demo_navegacao.py`, `demo/teste_demo_selecao.py`, `demo/teste_demo.py` é alterada | Execução de `PYTHONDONTWRITEBYTECODE=1 python -m pytest` (suíte completa) sem falhas, registrada no relatório de implementação com contagem de casos antes/depois |
| CA-H0045-26 | Demonstração automatizada reproduz os seis cenários `h0045_*` via `renderizar_estado`/`processar_comando`, sem TTY real | `demo/teste_demo_paginacao.py` e execução de `python demo/demo.py h0045_*` para cada cenário, sem `RenderizadorErro` |
| CA-H0045-27 | Validação manual do roteiro operacional (§12) permanece pendente e reservada ao usuário em TTY real | Registro explícito no relatório de implementação; nenhuma execução automatizada pode declarar este item como comprovado |

O valor esperado não pode ser derivado da própria saída observada. Não é
evidência suficiente, isoladamente: "código implementado", "função criada",
"pytest retornou zero" ou inspeção visual não registrada.

## 10. Decisões técnicas fechadas por este handoff

As decisões abaixo são mínimas, focais e compatíveis com a arquitetura
vigente. Nenhuma cria framework, registry ou abstração genérica além do
necessário. Esta seção corrige o achado QAH45-002: nenhuma decisão abaixo
reduz item navegável a "sempre uma linha física", ignora `politica_quebra`
ou exclui modo verboso multilinha do universo já coberto pela paginação.

### D-TEC-01 — Representação de runtime

```yaml
campo: estado["pagina_atual"]
tipo: "dict[id_console: str, int]"  # 1-based
paralelo_a: "estado['cursores'] e estado['selecoes']"
persistencia_em_json: proibida
```

### D-TEC-02 — Duas camadas: grade lógica de navegação e conteúdo físico paginado

Há duas noções distintas, que este handoff mantém deliberadamente
separadas:

1. **Grade lógica de navegação** — `navegacao.grade_de_itens(elemento,
   largura, altura_interna, desconto_estrutural)`, autoridade já
   estabelecida pelo H-0040 (QAI40-002), usada exclusivamente para
   topologia toroidal do cursor (wrap por linha/coluna dentro de uma
   página) e para a identidade do **item lógico global** (o mesmo índice já
   usado por `cursores[console.id]` desde a ADR-0031). Esta camada **não
   muda** neste handoff.
2. **Conteúdo físico paginado** — o mapa de quantas linhas físicas cada
   item (navegável ou visível não navegável) efetivamente ocupa no canvas
   corrente, considerando modo normal/verboso (D-TEC-04). Página é um
   **intervalo contíguo desse mapa físico** — não um intervalo de linhas/
   `rows` da grade lógica, porque uma linha da grade lógica pode corresponder
   a mais de uma linha física quando o item é multilinha.

O item lógico corrente (cursor) é sempre identificado pela camada 1; a
página que o contém é sempre calculada pela camada 2 (D-TEC-04). As duas
camadas são reconciliadas por `pagina_do_item_logico`/
`primeiro_item_logico_da_pagina` (D-TEC-03, D-TEC-17), nunca calculadas
duas vezes de forma independente.

### D-TEC-03 — Fronteira: `tela/paginacao.py`

Módulo novo, API pura (sem estado de módulo, sem I/O), no padrão de
`tela/navegacao.py`/`tela/selecao.py`:

```yaml
geometria:
  - "plano_de_paginacao(elemento, largura, altura_interna, verboso, desconto_estrutural=0) -> PlanoFisico"
      # calcula UMA VEZ, a partir do mapa físico exposto por
      # tela/renderizador.py (D-TEC-04), a estrutura:
      #   pagina_atual: int
      #   total_paginas: int
      #   capacidade_fisica_da_pagina: int
      #   fragmentos_renderizados: list de
      #     {item_ou_bloco, pagina, linhas_fisicas, navegavel, item_logico_ou_id}
      #   navegaveis_por_pagina: dict[int pagina -> int contagem]
      #   pagina_por_item_logico: dict[int item_logico -> int pagina]
      # (nomes concretos ajustáveis pelo implementador; semântica não pode
      # ser reduzida — ver corpo do prompt de correção, seção "Autoridade
      # única de planejamento físico")
  - "total_paginas(elemento, largura, altura_interna, verboso, desconto_estrutural=0) -> int"
  - "intervalo_da_pagina(elemento, pagina, largura, altura_interna, verboso, desconto_estrutural=0) -> fragmentos da pagina"
      # clampa pagina a [1, total]
  - "primeiro_item_logico_da_pagina(elemento, pagina, largura, altura_interna, verboso, desconto_estrutural=0) -> int | None"
      # None quando a pagina nao contem nenhum item cuja PRIMEIRA linha
      # fisica esteja nesta pagina (D-TEC-17) — mesmo que a pagina exiba
      # conteudo de continuacao de um item cuja primeira linha esta em
      # pagina anterior (D-PAG-03 generalizado)
  - "pagina_do_item_logico(elemento, item_logico, largura, altura_interna, verboso, desconto_estrutural=0) -> int"
      # pagina que contem a PRIMEIRA linha fisica do item (D-TEC-17);
      # usado pela repaginacao (D-PAG-06/09/10) e pela reconciliacao da ADR-0037
transicoes_de_estado:
  - "pagina_atual(estado, console) -> int"
      # le estado['pagina_atual'].get(console.id, 1)
  - "ir_para_pagina(estado, console, pagina) -> novo_estado"
      # clampa; reposiciona cursores[console.id] no primeiro item navegavel
      # da pagina de destino (D-PAG-02) segundo primeiro_item_logico_da_pagina;
      # sem item navegavel, cursor permanece sem entrada visivel (D-PAG-03)
  - "pagina_anterior(estado, console) -> novo_estado"
      # D-PAG-01: sem efeito na primeira pagina
  - "pagina_proxima(estado, console) -> novo_estado"
      # D-PAG-01: sem efeito na ultima pagina
```

### D-TEC-04 — Autoridade única de planejamento físico compartilhada [ESCOPO DO RENDERER FECHADO — PATCH_HANDOFF P05]

`tela/paginacao.py` **não recalcula** ocupação física por conta própria:
consome exclusivamente a função pura e pública já exposta por
`tela/renderizador.py` em ciclo de implementação anterior (nome
concreto adotado pelo implementador, ex.:
`mapa_fisico_de_itens(elemento, largura, altura_interna, verboso)` — ver
relatório de implementação para o nome efetivo), que reaproveita — sem
duplicar — a lógica já existente no renderer para ocupação física variável
por item:

- `_altura_quebra_item` (número de linhas físicas reais de um texto na
  largura disponível, já usado em modo verboso);
- a redistribuição de altura por linha da grade matricial já feita em
  `_linhas_distribuicao_matricial` quando algum item excede a altura mínima
  estimada;
- `_linhas_fisicas_por_item` (mapeamento linha física -> item dono).

`tela/paginacao.py` importa essa função **localmente**, dentro de suas
próprias funções (nunca no nível de módulo), exatamente como
`tela/navegacao.py` já importa `tela/paginacao.py` localmente (D-TEC-05) —
evitando import circular, já que `tela/renderizador.py` precisa importar
`tela/paginacao.py` (também localmente, dentro de `_linhas_console`/
`_caixa_de_elemento`) para obter o intervalo de página a recortar. As duas
importações locais mútuas garantem que o mapa físico é calculado **uma
única vez por render** e consumido tanto pelo cálculo de páginas quanto
pelo recorte de conteúdo — nunca em cálculos paralelos divergentes.

É proibido:

- calcular páginas uma vez no renderer e novamente na navegação;
- usar somente `itens_navegaveis()` para definir conteúdo ou quantidade de
  páginas (itens visíveis não navegáveis também entram no mapa físico e no
  plano de paginação);
- criar grade física paralela incompatível com o conteúdo efetivamente
  renderizado;
- manter estado de módulo entre redesenhos;
- introduzir persistência em arquivo.

Esta função e a integração descrita acima já foram implementadas em ciclo
anterior; **nenhuma alteração de `tela/renderizador.py` está autorizada por
este item para expor, estender ou substituir essa função** — ver §6.2,
§19.6.

### D-TEC-05 — Grade lógica de navegação permanece intacta

`tela/navegacao.py` não ganha uma segunda noção de "grade da página": os
movimentos de cursor (`mover_direita/esquerda/baixo/cima`) continuam
operando sobre a grade lógica COMPLETA retornada por `grade_de_itens`
(preservando `_posicao_do_item_logico`/`item_logico_de_posicao` sem
alteração de assinatura ou semântica — D-TEC-02), mas
`_linha_com_itens`/`_coluna_com_itens` passam a aceitar um intervalo
opcional `(inicio, fim)` de linhas lógicas que restringe o domínio de wrap
à página atual — calculado uma única vez por
`paginacao.intervalo_da_pagina` (via `primeiro_item_logico_da_pagina`
mapeado de volta à posição lógica) e repassado pelo chamador
(`demo.py::processar_comando`). Sem esse intervalo (`None`), o
comportamento H-0040 é preservado integralmente (toróide sobre a grade
lógica inteira).

### D-TEC-06 — Universo de consoles e itens multilinha

O universo desta implementação é o mesmo já coberto pela navegação de
nível único: console com `distribuicao_matricial` declarada e itens
navegáveis (ADR-0031/H-0040). **Dentro desse universo**, um item PODE
ocupar mais de uma linha física quando o modo verboso efetivo
(`contrato_console.md` §6, §21.3) expande seu conteúdo — capacidade já
existente hoje no renderer (`_altura_quebra_item`,
`_linhas_distribuicao_matricial`) e agora considerada integralmente pelo
cálculo de páginas via D-TEC-04. **Não há exclusão de modo verboso
multilinha da paginação** — correção do achado QAH45-002.

Consoles com `conteudo_externo` hierárquico (H-0036: apresentação
`hierarquia`, `tabela` ou `conjuntos`) permanecem fora do universo paginado
deste ciclo (§6.2, §6.4): esse modelo de conteúdo não usa
`grade_de_itens`/cursor por item lógico, e nenhuma das 14 decisões da
ADR-0038 é fraseada nesses termos. Estender paginação a esse modelo — que a
própria ADR-0038 (§8) lista "algoritmo físico de quebra de páginas" e
"lista final de arquivos de implementação" como decisão de implementação
ainda em aberto — é candidato a ciclo próprio, não uma exclusão inventada
por este handoff.

### D-TEC-07 — Políticas de quebra por item (efeito real) [CORRIGIDO — PATCH_HANDOFF P04]

O campo `politica_quebra` do item (`contrato_console.md` §12, v0.2) passa a
ter **efeito real** sobre o plano de paginação, transcrito verbatim da
definição vigente do contrato — nenhuma reinterpretação. Esta tabela
substitui integralmente a transcrição anterior, que descrevia
`evitar_quebra` e `permitir_quebra_somente_se_maior_que_pagina` como
equivalentes; as três políticas são realmente distintas:

| Política | Efeito no plano de paginação |
|---|---|
| `permitir_quebra` — fluxo contínuo | O item começa na próxima linha disponível, inclusive na última linha útil de uma página; quando necessário, continua nas páginas seguintes. |
| `evitar_quebra` — começar em nova página | O item sempre começa na primeira linha útil de uma página nova, mesmo havendo espaço disponível na página anterior; se ocupar mais de uma página, continua nas páginas seguintes; o próximo item com a mesma política também espera uma página nova. |
| `permitir_quebra_somente_se_maior_que_pagina` — manter junto quando possível | O item pode começar depois do anterior; se couber inteiro no espaço restante, permanece na página atual; se não couber no espaço restante mas couber inteiro numa página vazia, começa inteiro na página seguinte; se for maior que uma página inteira, começa na primeira linha útil da página seguinte e continua nas posteriores. |

`evitar_quebra` nunca aproveita o espaço restante da página anterior —
sempre inicia em página nova, mesmo havendo espaço suficiente;
`permitir_quebra_somente_se_maior_que_pagina` aproveita esse espaço restante
sempre que o item cabe inteiro nele, só adiando o início para a página
seguinte quando não cabe. Não há ambiguidade textual remanescente entre as
duas políticas — a antiga afirmação de equivalência e a ambiguidade
registrada em §6.4 foram removidas por este patch (ver §19).

Quando um item excede sozinho a `capacidade_fisica_da_pagina` (item maior
que uma página inteira), ele é fragmentado em blocos contíguos que
preenchem páginas sequenciais, preservando `item_logico_ou_id` em cada
fragmento; a soma de `linhas_fisicas` de todos os fragmentos de um item é
sempre igual à sua ocupação física total (sem perda nem duplicação de
linha — CA-H0045-09).

Item sem `politica_quebra` declarada assume `evitar_quebra` como default —
escolha conservadora entre os três valores já contratados (nenhum valor
novo é introduzido); o implementador deve registrar esta escolha no
relatório de implementação como assunção explícita, não como fato
contratual.

### D-TEC-08 — Normalização quando a quantidade total diminui

Nenhum estado de página é validado preventivamente. A cada evento que pode
alterar o plano físico (troca de página, redimensionamento, mudança de
modo, atualização controlada da lista de itens em memória),
`paginacao.total_paginas`/`plano_de_paginacao` é recalculado a partir do
mapa físico corrente (D-TEC-04) e a página armazenada é clampada via
`paginacao.intervalo_da_pagina`/`pagina_do_item_logico`, nunca lida
diretamente sem validação.

### D-TEC-09 — Integração com `processar_comando`

`demo/demo.py::processar_comando` reconhece `","`, `"<"`, `"."`, `">"` no
mesmo bloco condicional que hoje trata Tab/Shift+Tab/setas/Espaço/Enter
(dirigidos exclusivamente ao console focado via `navegacao.console_focado`),
delegando a `paginacao.pagina_anterior`/`pagina_proxima`. O bloco já
preserva `foco_console`/`cursores`/`selecoes` no retorno; passa a preservar
também `pagina_atual` da mesma forma.

### D-TEC-10 — Parâmetros de `renderizar_tela`

Novo parâmetro opcional `paginas_atuais: dict | None = None` (paralelo a
`cursores`), despejado em `_navegacao_atual["paginas_atuais"]` no início de
`renderizar_tela`, reinicializado a cada chamada (preserva R-14 — renderer
puro, sem estado entre redesenhos).

### D-TEC-11 — Materialização do indicador `página X/Y` [ESCOPO DO RENDERER FECHADO — PATCH_HANDOFF P05]

`_linha_base` (ou função companheira) já passou a aceitar, em ciclo de
implementação anterior, um texto opcional ancorado à direita, para compor
`"─ página X/Y ─"` dentro de `inner_w`, conforme
`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` §4.4 ("a
última linha da própria borda do corpo exibe o indicador de página,
ancorado à direita"). Chamado apenas quando a instância declara
`politica_paginacao: "com"`, independentemente de o console estar focado —
o indicador pertence à borda do console, não à barra de menus (D-PAG-12 e
nomenclatura 21 §4.4).

### D-TEC-12 — Cálculo dinâmico dos controles da barra

Novo valor de `regra_existencia`: `"console_com_paginacao"` (existe quando o
console focalizável declara `politica_paginacao: "com"` em
`_campos_inertes`, propriedade estática — `contrato_barra_de_menus.md`
§8.1). Dois novos valores de `regra_ativo`: `"pagina_nao_e_primeira"` (chip
`[<]`) e `"pagina_nao_e_ultima"` (chip `[>]`), avaliados a partir da página
e do total de páginas do console FOCADO; sem console focado, ou com o
console focado sem paginação declarada, ambos ficam inativos (D-PAG-13).

**Nota de fechamento de escopo do renderer [PATCH_HANDOFF P05, achado
QA-H0045-P04-001]:** D-TEC-04, D-TEC-06, D-TEC-10, D-TEC-11 e D-TEC-12
descrevem extensões de `tela/renderizador.py` já aplicadas em ciclo de
implementação anterior a este patch. Nenhuma delas autoriza nova alteração
do renderer neste ou em qualquer patch subsequente de paginação — ver §6.2
(arquivos preservados) e §19.6 (condição de reautorização). Onde o texto
acima ainda usa tempo verbal prospectivo ("passa a", "ganha", "novo valor"),
deve ser lido como registro do que já foi implementado, não como tarefa
pendente.

### D-TEC-13 — Loader e formato declarativo

`politica_paginacao` permanece exatamente como já validado hoje —
`isinstance(pol_pag, str)` restrito a `{"sem", "com"}`
(`tela/loader.py:1644`, `:1717-1722`). **Nenhum novo campo JSON é
introduzido**: o número de páginas é 100% derivado em runtime a partir de
`distribuicao_matricial`, `politica_quebra` por item e da geometria
corrente (largura/altura/modo), análogo ao número de colunas ajustáveis
(`[-][+]`) já calculado dinamicamente sem campo declarativo próprio de
contagem. O loader já rejeita o formato objeto antigo
(`{"paginacao": "com"}`) por exigir `isinstance(..., str)` — nenhuma
alteração de schema de `politica_paginacao` é necessária. A leitura focal
de `tela/loader.py` (§5) deve confirmar se `politica_quebra` por item já
possui validação de vocabulário fechado; se não possuir, a implementação
pode adicionar validação estritamente restrita aos três valores já
contratados (não é schema novo, é fechamento de vocabulário já declarado em
`contrato_console.md` §12), registrando essa decisão no relatório de
implementação.

### D-TEC-14 — `FluxoExecucao`

Novo campo `self._paginas_suspensas` (dict `id_console -> int`), seguindo
exatamente o padrão de `self._cursores_suspensos`/`self._ids_cursor_suspensos`:

```yaml
captura: "em _capturar_estado_suspensao, no mesmo laço que popula _ids_cursor_suspensos; le estado.get('pagina_atual', {})"
retorno_dry_run: "copiado 1:1 (mesmo padrao do campo legado self._pagina_suspensa)"
retorno_real: "reconciliado por ID: nova funcao companheira de _reconciliar_foco_cursor usa paginacao.pagina_do_item_logico(elemento, item_logico_do_id_preservado, ...) para recalcular a pagina que contem o item apos a recarga; fallback pagina 1 quando o ID nao existe mais"
precedencia: "D-PAG-10 (regra generica) NAO substitui D-H4-09 (reconciliacao especializada por ID da ADR-0037); a reconciliacao de pagina aqui e um COROLARIO da reconciliacao de cursor por ID ja vigente, nao uma regra concorrente"
limpeza: "zerado em _limpar_refs_proprias, no mesmo ponto que zera self._pagina_suspensa"
```

### D-TEC-15 — `[✥]` restrito à página atual (D-PAG-04)

`navegacao.exibir_chip_navegar(estado)` passa a contar apenas os itens
navegáveis dentro do intervalo da página atual (fragmentos da página
retornados por `paginacao.intervalo_da_pagina`) do console focado (quando
este declara `politica_paginacao: "com"`), em vez do total de itens
navegáveis do console inteiro. Sem paginação declarada, comportamento
H-0040 preservado integralmente.

### D-TEC-16 — Campo legado `self._pagina_suspensa`

Não confundir com D-TEC-01/D-TEC-14: o campo singular pré-existente
(`tela/fluxo_execucao.py`, não indexado por console) é preservado sem
alteração de comportamento — nenhum teste que hoje depende dele
(`tela/teste_fluxo_execucao.py`) pode regredir. O novo campo
`self._paginas_suspensas` (plural, dict por console) coexiste com ele sem
sobrepor sua semântica.

### D-TEC-17 — Item navegável fragmentado: relação com cursor e indicador visual

Derivado diretamente de duas regras já vigentes — **D12**
(`contrato_console.md`/`tela/renderizador.py::_aplicar_indicador_linhas`:
apenas a **primeira linha física** do item corrente recebe o símbolo de
cursor; continuações recebem `selecionado_off`) e **D-PAG-03**
(página pode ter conteúdo visível sem item navegável) — sem introduzir
regra de interface nova:

- **Página que "contém" um item, para fins de `pagina_do_item_logico` e de
  cursor (D-PAG-02, D-PAG-05, D-PAG-06)**, é a página que contém a
  **primeira linha física** desse item, nunca uma página de continuação.
- Quando uma página começa por **continuação** de um item navegável cuja
  primeira linha física está na página anterior, essa continuação **não
  conta** como "primeiro item navegável desta página"
  (`primeiro_item_logico_da_pagina` avança para o próximo item cuja
  primeira linha física esteja nesta página).
- Se, depois de aplicada essa regra, a página não tiver nenhum item cuja
  primeira linha física esteja nela (por exemplo, uma página inteiramente
  preenchida pela continuação de um único item muito longo), essa página
  segue exatamente D-PAG-03: conteúdo visível, console focado, sem cursor
  visível, setas sem movimento — mesmo contendo, fisicamente, parte de um
  item navegável.
- Um item navegável fragmentado, quando é o item lógico corrente, tem seu
  símbolo de cursor visível somente na página que contém sua primeira
  linha física; nas páginas de continuação, suas linhas aparecem sem
  indicador, consistente com D12 já vigente para modo verboso não
  paginado.

Esta decisão não introduz semântica de interface nova: aplica D12 (regra já
existente sobre qual linha física de um item multilinha recebe o
indicador) à pergunta "a que página pertence este item", sem inventar
comportamento de UX adicional.

## 11. Testes obrigatórios

Execute a partir da raiz. A suíte canônica do Orquestrador é
`PYTHONDONTWRITEBYTECODE=1 python -m pytest`.

Comandos focais desta implementação:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  tela/teste_paginacao.py \
  tela/teste_navegacao.py \
  tela/teste_renderizador.py \
  tela/teste_loader.py \
  tela/teste_selecao.py \
  tela/teste_fluxo_execucao.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py \
  demo/teste_demo_selecao.py \
  demo/teste_demo.py \
  -v
```

Suíte completa (regressão integral):

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Cobertura nominal mínima a fechar (não fixar quantidade de testes
aprovados; declarar somente os casos materialmente necessários):

**Conteúdo físico e cálculo de páginas** (`tela/teste_paginacao.py`):

- item de uma linha; item multilinha (modo verboso); item visível não
  navegável; página formada por itens navegáveis e não navegáveis; página
  com conteúdo e nenhum navegável; conjunto vazio produz `total_paginas ==
  1`;
- `primeiro_item_logico_da_pagina` retorna `None` em página sem item cuja
  primeira linha física esteja nela (inclusive página de pura continuação —
  D-TEC-17);
- `pagina_do_item_logico` usado por repaginação e pela reconciliação da
  ADR-0037;
- as três políticas de quebra (`evitar_quebra`, `permitir_quebra`,
  `permitir_quebra_somente_se_maior_que_pagina`), inclusive item maior que
  uma página inteira;
- identidade de fragmento preservada; ausência de perda ou duplicação de
  linhas entre fragmentos.

**Navegação** (`tela/teste_navegacao.py`, extensão): setas restritas ao
intervalo de linhas lógicas da página atual, sem mudança de página (D15/
D-PAG mantidos); `exibir_chip_navegar` restrito à página atual (D-PAG-04);
regressão da navegação de nível único já existente (H-0040) permanece
intacta.

**Renderer** (`tela/teste_renderizador.py` — preservado, fora do escopo
ativo deste ciclo; ver §6.2, §19.6): a cobertura de indicador `página X/Y`
(inclusive `1/1` com página única e com conjunto vazio), `[<]`/`[>]`
contextuais (D-PAG-13), recorte de conteúdo por página com itens multilinha
e interação entre D12 e item navegável fragmentado (D-TEC-17) já existe de
ciclo anterior; nenhuma extensão nova é exigida por este handoff — apenas a
regressão da suíte existente permanece intacta.

**Loader** (`tela/teste_loader.py`, extensão): rejeição do formato objeto
antigo `{"politica_paginacao": {"paginacao": "com"}}`.

**Fluxo focal** (`tela/teste_fluxo_execucao.py`, extensão): retorno de
`dry-run` preserva `pagina_atual` (espelhando
`teste_retorno_dry_run_zero_recargas`); retorno de execução real reconcilia
a página pelo ID preservado (espelhando
`teste_retorno_real_preserva_cursor_por_id`); fallback para primeira página
quando o ID não existe mais (espelhando `teste_retorno_real_fallback_cursor`);
regressão dos testes existentes de preservação/fallback de cursor permanece
intacta.

**Integração via demo** (`demo/teste_demo_paginacao.py`): comandos
`,`/`<`/`.`/`>` via `processar_comando`; troca de página com cursor no
primeiro item navegável de destino; página sem item navegável; dois
consoles com páginas independentes; console focado × não focado; seleção
persistente entre páginas e `Todos` sobre todas as páginas do conjunto
filtrado; **mudança de modo/redimensionamento com diferença física real
comprovada** (não apenas alternância de flag sem efeito) preservando o item
lógico; retorno por foco (Tab/Shift+Tab) preservando página e reiniciando
cursor; as três políticas de quebra ponta-a-ponta sobre
`h0045_paginacao_politicas_quebra.json`.

**Coerência compartilhada**: renderer e navegação usam o mesmo plano físico
(comparação cruzada entre `tela.paginacao` e o conteúdo efetivamente
recortado pelo renderer); cursor nunca aponta item fora da página; itens
não navegáveis aparecem na página correta; duas alturas de console (dois
consoles, ou o mesmo console redimensionado) produzem planos independentes;
resize não gera divergência física/lógica.

**Regressão integral**: `tela/teste_navegacao.py`, `tela/teste_selecao.py`,
`tela/teste_fluxo_execucao.py`, `demo/teste_demo_navegacao.py`,
`demo/teste_demo_selecao.py`, `demo/teste_demo.py` continuam passando sem
nenhuma alteração de asserção pré-existente.

## 12. Demonstração operacional

```yaml
cwd: "."
comando:
  - "python demo/demo.py h0045_paginacao_console_unico"
  - "python demo/demo.py h0045_paginacao_conjunto_vazio"
  - "python demo/demo.py h0045_dois_consoles_paginas_independentes"
  - "python demo/demo.py h0045_fluxo_execucao_paginado"
  - "python demo/demo.py h0045_paginacao_modo_verboso_multilinha"
  - "python demo/demo.py h0045_paginacao_politicas_quebra"
entrada_ou_fixture: "config/telas/demo/h0045_*.json (novos, permanentes)"
configuracao: "config/estilo.json (leitura, sem alteração)"
saida_esperada: >
  Quadros com indicador "página X/Y" na borda do console, chips [<][>]
  refletindo o estado da página do console focado, [✥] restrito à página
  atual, cursor no primeiro item navegável após troca de página, conteúdo
  multilinha corretamente fatiado entre páginas em modo verboso, e itens
  quebrados conforme sua política declarada. 80x24 é a geometria de
  referência das fixtures permanentes (exemplo controlado, não critério
  universal — §18.1/§18.2); os fenômenos exigidos devem se sustentar nas
  geometrias adicionais exigidas por §18.5.
prova_semantica: >
  Testes não interativos em demo/teste_demo_paginacao.py que renderizam
  quadros de referência via renderizar_estado/processar_comando (sem TTY
  real) e comparam página, indicador, cursor, chips e conteúdo multilinha
  linha a linha — não dependem de inspeção visual nem usam screenshot como
  única evidência. 80x24 é usada como geometria canônica de regressão;
  §18.5 exige, adicionalmente, geometrias estreita, alta e redimensionada.
  Nenhuma fixture baseline pré-existente (h0040/h0041/h0044) é alterada.
arquivos_persistentes:
  - config/telas/demo/h0045_paginacao_console_unico.json
  - config/telas/demo/h0045_paginacao_conjunto_vazio.json
  - config/telas/demo/h0045_dois_consoles_paginas_independentes.json
  - config/telas/demo/h0045_fluxo_execucao_paginado.json
  - config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
  - config/telas/demo/h0045_paginacao_politicas_quebra.json
temporarios_operacionais: nenhum
limpeza_ou_restauracao: não aplicável (sem temporários, sem persistência de sessão)
validacao_manual:
  executor_exclusivo: USUARIO_EM_TTY_REAL
  estado_consolidado:
    aprovadas: "6/17..14/17 (preservadas — não reexecutar)"
    retomar_em: "15/17"
    reexecutar: ["15/17", "16/17", "17/17"]
    especificacao_vigente_para_retomada: "§18.6 substitui, para estas três etapas, os itens correspondentes deste roteiro_minimo (quebra/políticas, conjunto vazio e página somente de continuação), usando os casos separados de §18.4 em vez de uma fixture densa única"
  roteiro_minimo:
    - tecla: "."
      esperado: "avanca pagina"
    - tecla: ">"
      esperado: "avanca pagina (equivalente a '.')"
    - tecla: ","
      esperado: "recua pagina"
    - tecla: "<"
      esperado: "recua pagina (equivalente a ',')"
    - contexto: "primeira pagina"
      esperado: "[<] inativo"
    - contexto: "ultima pagina"
      esperado: "[>] inativo"
    - contexto: "pagina intermediaria"
      esperado: "[<] e [>] ambos ativos"
    - contexto: "apos troca de pagina"
      esperado: "cursor entra no primeiro item navegavel da pagina de destino"
    - contexto: "pagina sem item navegavel"
      esperado: "nenhum cursor visivel; setas sem movimento"
    - contexto: "pagina de continuacao de item multilinha fragmentado"
      esperado: "sem cursor visivel mesmo com conteudo do item presente (D-TEC-17)"
    - tecla: "V/v (modo verboso)"
      esperado: "conteudo multilinha aparece; limites de pagina podem mudar; item logico preservado"
    - tecla: "Tab / Shift+Tab"
      esperado: "pagina do console preservada; cursor reinicia no primeiro item navegavel dessa pagina"
    - contexto: "resize do terminal"
      esperado: "item logico preservado; pagina recalculada para conte-lo"
    - contexto: "selecao multipla entre paginas"
      esperado: "selecao permanece marcada ao mudar de pagina"
    - contexto: "item com evitar_quebra maior que uma pagina"
      esperado: "item fragmentado entre paginas consecutivas, sem conteudo perdido"
    - contexto: "indicador"
      esperado: "pagina X/Y correto em cada pagina"
    - contexto: "dois consoles"
      esperado: "paginas independentes; comando de pagina so afeta o console focado"
  gabarito_manual:
    - APROVADO
    - REPROVADO
    - "NÃO OBSERVADO"
  semantica_gabarito_manual:
    APROVADO: "o comportamento esperado foi observado integralmente"
    REPROVADO: "foi observado comportamento incompatível com o esperado"
    "NÃO OBSERVADO": "o cenário ou fenômeno não se materializou de forma verificável"
  observacao: >
    Roteiro para execução POSTERIOR pelo usuário. A implementação não pode
    declarar esta validação como executada. As etapas 6/17..14/17
    permanecem aprovadas (ver `estado_consolidado` acima) e não devem ser
    reexecutadas nem reclassificadas. Para as etapas 15/17..17/17, cada
    linha deve ser registrada pelo usuário usando exclusivamente o
    gabarito único `APROVADO` | `REPROVADO` | `NÃO OBSERVADO` acima,
    conforme os casos separados de §18.4 (§18.6); esta lista não é
    exaustiva — o usuário mantém apenas o que efetivamente observar.
```

Código de saída zero, isoladamente, não comprova a entrega.

## 13. Relatório da execução

Criar um novo relatório em:

```text
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0045.md
```

Usar obrigatoriamente:

```text
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

O relatório deve registrar: arquivos criados e alterados; decisões
técnicas concretas efetivamente aplicadas (incluindo eventuais desvios
justificados das decisões D-TEC-01 a D-TEC-17 deste handoff, com
justificativa — em particular o nome concreto escolhido para a função
física de D-TEC-04 e o default de `politica_quebra` ausente de D-TEC-07);
testes executados; demonstrações; estado Git; resíduos; bloqueios;
validação manual ainda pendente (sempre pendente — pertence ao usuário);
próxima ação `QA_IMPLEMENTACAO`.

Regras: cada execução material produz seu próprio relatório; não
sobrescrever relatório anterior; registrar somente fatos materiais; não
copiar código, diff completo, handoff, logs extensos ou metodologia
narrativa; omitir campos e seções vazios; teto normal de 600 palavras, até
900 quando houver conteúdo material que não possa ser reduzido; evidência
separada somente quando indispensável, sempre em `docs/relatorios/` e
referenciada no relatório; o relatório não aprova formalmente a
implementação.

## 14. Resposta terminal

Retorne somente:

```yaml
status: <STATUS_LITERAL>
relatorio: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0045.md
artefatos:
  - <somente arquivos criados ou alterados>
bloqueios:
  - <somente quando houver>
proxima_acao: <somente quando objetivamente determinada>
```

Omitir campos vazios. Não copiar o relatório nem acrescentar conclusão
narrativa.

## 15. Exceção operacional

Arquivo ou diretório fora da lista nominal de §6.1 não pode ser alterado
silenciosamente. Se um item externo for estritamente necessário — por
exemplo, um contrato concreto não enumerado, uma assinatura chamada
diretamente definida em arquivo não autorizado, ou um erro de teste que
aponte dependência material fora do manifesto:

1. pare antes da alteração;
2. informe item, motivo, escopo exato e mudança esperada;
3. peça autorização explícita ao usuário.

A implementação deve parar com `LEITURA_ADICIONAL_NECESSARIA`; não pode
ampliar o escopo silenciosamente. A autorização eventual não permite criar
semântica, arquitetura, schema, formato ou política nova além do já fechado
neste handoff.

## 16. Condições de bloqueio

Bloquear quando:

- faltar decisão;
- houver contradição documental;
- for necessário inventar formato ou schema (nenhum é necessário — ver
  D-TEC-13);
- diretório novo necessário não estiver autorizado (nenhum diretório novo é
  necessário — ver §6.1 `diretorios_a_criar: []`);
- houver risco de sobrescrever entrada real;
- o handoff for inexequível;
- a leitura focal autorizada for insuficiente;
- surgir, durante a implementação, um comportamento indispensável de item
  navegável fragmentado que D-TEC-17 e o contrato aplicado não resolvam —
  parar com `BLOCKED_USER_DECISION` em vez de inventar regra de interface
  nova.

Se o bloqueio ocorrer antes de qualquer resultado material, não criar
relatório. Se já houver leitura, verificação, alteração ou evidência que
precise sobreviver ao contexto, criar relatório factual do bloqueio.

## 17. Limite de encerramento

Ao concluir implementação, testes locais, demonstração e relatório, parar.

Não fazer QA formal. Não aprovar a própria entrega. Não preparar nem
executar commit. Não iniciar outro ciclo.

## 18. Correção do método de validação (PATCH_HANDOFF P02)

Esta seção corrige exclusivamente o **método** de implementação,
demonstração e validação das três etapas manuais ainda bloqueadas
(15/17–17/17, ver §12 `validacao_manual.estado_consolidado`). Ela não
reabre cursor, seleção, comandos de página, foco, integração dry-run/
execução real, as decisões da ADR-0038 ou as políticas contratuais de
quebra (§6.4). Onde houver conflito entre esta seção e uma redação anterior
deste handoff sobre geometria fixa ou prova por fixture única (§6.1, §12),
esta seção prevalece. Nenhum novo `PATCH_IMPLEMENTACAO` sobre 15/17–17/17
está autorizado antes de `QA_HANDOFF` aprovar esta correção.

**Nota de substituição [PATCH_HANDOFF P05, achado QA-H0045-P04-002]:** esta
seção 18 documenta o método adaptativo original (P02), posteriormente
identificado como causa de `HANDOFF_METHOD_DEFECT`
(`RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md`) e corrigido
pela seção 19 (P04/P05). Ficam explicitamente substituídos, sem vigência
onde incompatíveis com §19:

- **§18.2** (harness adaptativo: gera modelos/itens de validação em memória
  dependentes da geometria resolvida) — substituído por §19.1 (proibição de
  geração a partir de `W`/`C` e de reconstrução do modelo durante resize) e
  §19.2 (três telas fixas por política);
- **§18.3** (relações de `W`/`C` usadas para construir os quatro casos
  adaptativos removidos) — sem vigência para `H0045-VAL-LARGURA`,
  `H0045-VAL-PERMITIR`, `H0045-VAL-EVITAR` e `H0045-VAL-CONDICIONAL`; a
  relação de tamanho de `H0045-VAL-CONTINUACAO` é preservada apenas como
  registro histórico de uma construção única e fixa da fixture, nunca como
  geração em runtime (§19.1, §19.3);
- **§18.4** (os seis casos tratados como conjunto único, incluindo os
  quatro casos adaptativos) — substituído por §19.3: apenas
  `H0045-VAL-VAZIO` e `H0045-VAL-CONTINUACAO` permanecem vigentes, com
  conteúdo fixo, nunca reconstruído durante o resize;
- **§18.5** (testes automatizados que dependem do harness e dos quatro
  casos adaptativos) — as referências a "caso adaptativo" abaixo passam a
  designar exclusivamente o caso de conteúdo fixo `H0045-VAL-CONTINUACAO`
  (§19.3); nenhuma geração dependente de geometria é exigida ou permitida;
- **§18.6, etapa 15/17** — substituída por §19.5 (as três telas de §19.2 no
  lugar dos quatro casos adaptativos citados originalmente nesta etapa);
  16/17 e 17/17 permanecem, com a ressalva de conteúdo fixo de §19.1;
- **§18.7** (arquivos autorizados para o harness adaptativo, incluindo o
  helper que construía os seis casos "a partir da geometria efetivamente
  resolvida") — sem vigência [PATCH_HANDOFF P06, achado QA-H0045-P05-002];
  substituído integralmente por §19.6 (lista vigente de arquivos
  autorizados) e por §19.1 (proibição de construção de conteúdo dependente
  de `W`/`C`); mantido apenas como registro histórico do método revogado;
- **§18.8**, nos critérios que dependem exclusivamente dos quatro casos
  adaptativos removidos (`CA-H0045-PH-02` a `PH-05`, `PH-11`) — sem
  vigência; os fenômenos que descrevem continuam válidos, agora atestados
  pelos critérios `CA-H0045-PH-15`/`PH-16` (§19.8).

Nenhuma obrigação residual de gerar conteúdo a partir de `W`/`C`, de
reconstruir o modelo lógico durante o resize, ou de executar os quatro
casos adaptativos como conjunto obrigatório permanece vigente. A seção 19
substitui integralmente as obrigações incompatíveis desta seção 18. Onde
não houver conflito explícito com o exposto acima (§18.1 — fenômenos
distintos a provar, ainda válidos como conceito; §18.7 — registro
histórico do harness adaptativo revogado, sem vigência [PATCH_HANDOFF
P06] — ver §19.6 para a lista vigente de arquivos autorizados; §18.8 —
demais critérios não listados acima), a seção permanece válida como
registro histórico e complementar.

### 18.1 Fenômenos distintos de paginação a provar

Quatro fenômenos são independentes entre si. Nenhuma prova de um substitui
a prova dos demais.

**18.1.1 Quebra textual por largura** — uma única linha lógica cujo
conteúdo excede a largura útil efetiva e, por decisão do renderer,
transforma-se em duas ou mais linhas físicas. Prova mínima: a entrada
contém uma linha lógica única cujo comprimento excede a largura útil
calculada pela mesma autoridade usada pelo renderer (`largura_util_itens_
console`/geometria de célula, D-TEC-04); marcadores de início, meio e fim
identificam o conteúdo antes e depois da quebra; cada marcador aparece
exatamente uma vez; sem perda nem duplicação. Linhas curtas pré-separadas
não são aceitas como prova deste fenômeno (elas provam, no máximo,
fragmentação vertical — §18.1.2).

**18.1.2 Fragmentação vertical de item** — um item já materializado em
várias linhas físicas não cabe na capacidade restante ou total da página e
precisa ser transferido ou fragmentado conforme `politica_quebra`
(D-TEC-07). Provada separadamente para `evitar_quebra`, `permitir_quebra`
e `permitir_quebra_somente_se_maior_que_pagina`, com a altura física dos
itens calculada em função da capacidade real da página (`capacidade_
fisica_da_pagina`, D-TEC-03).

**18.1.3 Página somente de continuação** — página que contém
exclusivamente fragmento físico de item iniciado em página anterior e
nenhum início de item navegável (D-TEC-17). Prova mínima: conteúdo de
continuação visível; zero cursor; setas não movimentam o cursor; comandos
de página continuam funcionando; não ocorre salto automático; o cenário
permanece garantido em terminal alto porque sua dimensão é derivada da
capacidade física efetiva (§18.3), não de uma contagem estática de tokens.

**18.1.4 Conjunto paginado vazio** — console declara `politica_paginacao:
"com"` e possui zero itens reais (D-PAG-12). Prova mínima: indicador
"página 1/1"; `[<]` e `[>]` presentes e inativos; zero cursor; comandos de
página e setas sem efeito; nenhum conteúdo default ou fallback é
introduzido.

### 18.2 Infraestrutura de validação adaptativa (harness) [SUBSTITUÍDO — PATCH_HANDOFF P05]

Esta subseção autorizava, para as etapas 15/17–17/17, um **harness
adaptativo** que gerava modelos/itens de validação em memória a cada
geometria efetivamente resolvida (item 2 abaixo, preservado apenas como
registro do que causou o defeito):

> ~~2. gera modelos ou itens de validação em memória depois de conhecida a
> geometria efetivamente resolvida;~~

Essa autorização causou o defeito registrado em
`RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md`
(`HANDOFF_METHOD_DEFECT`) e está **revogada** por §19.1: nenhuma
implementação, presente ou futura, pode gerar ou reconstruir o modelo
lógico de validação a partir da geometria (`W`/`C`), nem reconstruí-lo
durante o redimensionamento — mesmo acionada pelo ponto de entrada real da
demo. O método vigente é exclusivamente o de §19.2/§19.3: três telas fixas
por política, mais os dois casos separados de conteúdo fixo `H0045-VAL-VAZIO`
e `H0045-VAL-CONTINUACAO` (§18.4).

As seis fixtures permanentes de §6.1/§7 continuam válidas para regressão e
demonstração geral, com o alcance probatório explicitamente delimitado:

```yaml
fixture_estatica:
  pode_provar: comportamento conhecido em geometria explicitamente controlada (80x24, conforme calibrado em P10/P11)
  nao_pode_provar_sozinha:
    - quebra textual em terminal externo arbitrário
    - existência de página somente de continuação em qualquer altura de terminal
    - equivalência material com validação humana em geometria não controlada
```

### 18.3 Dimensionamento adaptativo obrigatório [SEM VIGÊNCIA PARA OS CASOS REMOVIDOS — PATCH_HANDOFF P05]

Sem vigência para `H0045-VAL-LARGURA`, `H0045-VAL-PERMITIR`,
`H0045-VAL-EVITAR` e `H0045-VAL-CONDICIONAL` (removidos, §18.4). As
relações abaixo, para `H0045-VAL-CONTINUACAO`, são preservadas apenas como
registro histórico de uma construção única e fixa da fixture — nunca como
geração em runtime dependente de `W`/`C` (§19.1, §19.3):

```yaml
W: largura_util_efetiva_do_conteudo   # mesma autoridade do renderer, D-TEC-04
C: capacidade_fisica_efetiva_da_pagina   # idem
```

- **Quebra textual**: uma linha lógica com comprimento comprovadamente maior
  que `W` (preferencialmente entre `W + 1` e `2W`), contendo os marcadores
  `LARGURA_INICIO`, `LARGURA_MEIO`, `LARGURA_FIM` na mesma linha lógica de
  entrada.
- **`H0045-VAL-PERMITIR` (fragmentação vertical sob `permitir_quebra`)**:
  prova exclusivamente que o item pode usar a capacidade restante da
  página corrente, atravessar o limite entre duas páginas, com fragmentos
  contíguos, sem perda nem duplicação e com identidade preservada. O
  dimensionamento é o mínimo suficiente para atravessar ao menos um limite
  de página — não exige nem usa como critério uma página inteira de
  continuação pura. Uma relação admissível é equivalente a `altura_do_item
  > capacidade_restante_da_pagina`, com conteúdo anterior controlado para
  deixar um resíduo conhecido. Este caso não fixa nem depende de
  `2C + 1`.
- **`H0045-VAL-CONTINUACAO` (página somente de continuação)**: usa entrada
  própria, distinta de `H0045-VAL-PERMITIR`. Somente este caso exige uma
  relação suficiente para garantir uma página intermediária inteira de
  continuação — item cuja ocupação física seja pelo menos `2C + 1`, ou
  outra relação comprovadamente suficiente, independentemente de `C`. A
  prova inclui marcadores próprios `CONT_INICIO`/`CONT_MEIO`/`CONT_FIM`
  (ou equivalentes inequívocos).
- **`evitar_quebra`**: capacidade restante da página corrente menor que a
  altura do item, mas item menor ou igual a `C` — o item não usa o resíduo
  da página anterior e inicia inteiro na página seguinte.
- **Condicional**: provado em dois itens separados — um que cabe em página
  vazia (não fragmentado) e um maior que `C` (obrigatoriamente
  fragmentado).
- **Conjunto vazio**: zero itens reais; vazio nunca é simulado por itens não
  navegáveis.

Nenhum caso novo fixa `31 linhas`, `16 linhas por página` ou quantidade
equivalente como critério — esses valores concretos permanecem válidos
apenas como o resultado observado das fixtures permanentes calibradas para
80x24 (P10/P11), não como a regra geral.

### 18.4 Casos de validação separados [REVOGADO PARA OS QUATRO CASOS ADAPTATIVOS — PATCH_HANDOFF P05]

Os casos `H0045-VAL-LARGURA`, `H0045-VAL-PERMITIR`, `H0045-VAL-EVITAR` e
`H0045-VAL-CONDICIONAL`, originalmente listados nesta subseção como parte
de um conjunto de seis compartilhando o harness adaptativo de §18.2, estão
substituídos pelas três telas fixas de §19.2 (uma por política) e não são
mais exigidos nem autorizados como harness dependente de geometria (§19.1,
§19.3).

Apenas dois casos desta lista permanecem vigentes, com conteúdo fixo —
criado uma única vez, nunca gerado a partir de `W`/`C` nem reconstruído
durante o redimensionamento (§19.1):

```yaml
casos_vigentes:
  - id: H0045-VAL-VAZIO
    fenomeno: conjunto_paginado_vazio
  - id: H0045-VAL-CONTINUACAO
    fenomeno: pagina_somente_de_continuacao
```

Cada um deve continuar declarando, na sua documentação de implementação:
entrada fixa; geometria de referência; comando; resultado automatizado;
resultado manual simples; marcadores visuais; condição de falha. Nenhum dos
dois pode ser usado para provar o fenômeno do outro nem o fenômeno de
qualquer política de quebra (§19.2/§19.3 cobrem as políticas).

### 18.5 Testes automatizados obrigatórios (adicional a §11) [ver nota de substituição no início da seção 18]

**Geometrias múltiplas** — no mínimo: geometria canônica regular (80x24);
geometria estreita; geometria alta, escolhida de forma que a fixture
estática `h0045_paginacao_politicas_quebra.json` (calibrada para capacidade
16 em 80x24, RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P11.md) tenderia a perder
sua página de continuação pura, comprovando que o caso de conteúdo fixo
`H0045-VAL-CONTINUACAO` (§19.3) continua válido onde a fixture estática não
garante; redimensionamento entre pelo menos duas dessas geometrias.

**Propriedades materiais**, não apenas números finais de página: conteúdo
lógico completo preservado; marcadores aparecem exatamente uma vez;
fragmentos somam a ocupação física original; nenhum fragmento duplicado;
página somente de continuação com zero início navegável; conjunto vazio
mantém chips presentes e inativos; os casos vigentes (`H0045-VAL-VAZIO` e
`H0045-VAL-CONTINUACAO`, §19.3) continuam válidos após alteração de altura.

**PTY automatizado**, pelo ponto de entrada real (`python demo/demo.py
<caso>`), controlando explicitamente suas dimensões, exercitando abertura,
troca de página, página de continuação, conjunto vazio, redimensionamento
e retorno à dimensão inicial. PTY automatizado é evidência de integração,
não substituto da validação manual do usuário (§18.6).

### 18.6 Validação manual — retomada em 15/17

Não reabrir 6/17–14/17 (§12 `validacao_manual.estado_consolidado`). As três
etapas restantes são reespecificadas para usar os casos de §18.4 em vez de
uma única fixture densa, com rótulos inequívocos e gabarito curto:

```text
APROVADO | REPROVADO | NÃO OBSERVADO
```

- **15/17 — Quebra e políticas** [SUBSTITUÍDA — ver §19.5]: reespecificada
  por §19.5 para usar as três telas fixas de §19.2
  (`h0045_validacao_fluxo_continuo`, `h0045_validacao_nova_pagina`,
  `h0045_validacao_manter_junto`), uma por política, com redimensionamento
  livre pelo usuário. Os quatro casos adaptativos `H0045-VAL-LARGURA`,
  `H0045-VAL-PERMITIR`, `H0045-VAL-EVITAR` e `H0045-VAL-CONDICIONAL`
  citados originalmente nesta etapa não são mais exigidos (§19.3).
- **16/17 — Conjunto vazio**: `página 1/1` diretamente visível; `[<]` e
  `[>]` visíveis e inativos; nenhum cursor; comandos sem efeito; nenhum
  item artificial (`H0045-VAL-VAZIO`).
- **17/17 — Página somente de continuação**: entrada própria, distinta de
  `H0045-VAL-PERMITIR`; marcadores próprios `CONT_INICIO`/`CONT_MEIO`/
  `CONT_FIM` (ou equivalentes inequívocos) diretamente visíveis; nenhum
  início navegável; nenhum cursor; setas sem movimento; página anterior e
  próxima continuam acessíveis; conteúdo fixo, criado uma única vez no
  início da execução — o redimensionamento muda somente a forma como esse
  conteúdo aparece nas páginas, nunca o conteúdo em si; nenhuma geração a
  partir de `C` em runtime é exigida ou permitida (`H0045-VAL-CONTINUACAO`,
  §19.1) [CORRIGIDO — PATCH_HANDOFF P06, achado QA-H0045-P05-002].

### 18.7 Arquivos autorizados para implementação futura do harness [SUBSTITUÍDO — PATCH_HANDOFF P06, achado QA-H0045-P05-002]

Esta subseção documentava, para o harness adaptativo revogado por §19.1,
quais arquivos estariam autorizados e a finalidade de um helper que
construiria os seis casos de §18.4 "a partir da geometria efetivamente
resolvida". Essa construção dependente de `W`/`C` está revogada: nenhum
helper vigente pode receber `W` ou `C` para definir o tamanho do conteúdo,
criar quantidade de linhas conforme a geometria, recriar itens depois de
`SIGWINCH`, ou substituir textos, IDs, ordem ou políticas durante o resize
— helpers vigentes podem apenas construir modelos fixos (§19.1). A lista
vigente de arquivos autorizados para a implementação futura é
exclusivamente a de §19.6; o conteúdo abaixo permanece somente como
registro histórico do método revogado, sem vigência.

```yaml
historico_metodo_revogado:  # sem vigência — ver §19.6 para a lista vigente
  alteraveis:
    - demo/demo.py
    - demo/teste_demo_paginacao.py
    - tela/teste_paginacao.py
    # tela/teste_renderizador.py removido [PATCH_HANDOFF P05] — ver §6.2, §19.6
  fixtures_existentes_ajustaveis_por_ciclo_futuro:
    - config/telas/demo/h0045_paginacao_modo_verboso_multilinha.json
    - config/telas/demo/h0045_paginacao_politicas_quebra.json
    - config/telas/demo/h0045_paginacao_conjunto_vazio.json
  helper_antigo_a_partir_da_geometria:  # revogado — ver §19.1
    caminho_nominal_canonico: demo/casos_validacao_paginacao.py
    finalidade_historica: >
      Construía em memória, a partir da geometria efetivamente resolvida
      por tela/renderizador.py (geometria_console/largura_util_itens_
      console/mapa_fisico_de_itens), os seis casos de §18.4. Este padrão
      está revogado por §19.1; o arquivo permanece listado em §19.6 como
      alterável para a implementação futura, restrito a construir modelos
      fixos (§19.1), nunca dependentes de W/C.
```

Distinções obrigatórias, preservadas como registro histórico:

- fixture estática (`config/telas/demo/h0045_*.json`, dado de entrada real
  em disco) é distinta de
- modelo de validação em memória (`demo/casos_validacao_paginacao.py`,
  restrito a conteúdo fixo — §19.1), que é distinto de
- estado de runtime (`estado["pagina_atual"]`, D-TEC-01, nunca persistido em
  JSON), que é distinto de
- comportamento de produto (`tela/paginacao.py`, `tela/renderizador.py`),
  que é distinto de
- teste automatizado (`tela/teste_*.py`, `demo/teste_demo_paginacao.py`),
  que é distinto de
- validação humana (`§18.6`, executor exclusivo `USUARIO_EM_TTY_REAL`).

### 18.8 Critérios de aceite deste patch de método

| ID | Critério |
|---|---|
| CA-H0045-PH-01 | Nenhuma prova manual depende de 80x24, capacidade fixa ou quantidade absoluta de linhas como critério universal. |
| CA-H0045-PH-02 | Quebra textual por largura possui linha lógica única maior que a largura útil efetiva (`W`). |
| CA-H0045-PH-03 | Fragmentação vertical é provada separadamente da quebra textual. |
| CA-H0045-PH-04 | Página somente de continuação é garantida por relação com a capacidade física real (`C`) e continua existindo em terminal alto. |
| CA-H0045-PH-05 | Conjunto vazio contém zero itens reais e mantém controles de paginação presentes e inativos. |
| CA-H0045-PH-06 | Testes cobrem múltiplas geometrias e PTY pelo ponto de entrada real. |
| CA-H0045-PH-07 | Validação manual usa marcadores visíveis e não exige contagem extensa. |
| CA-H0045-PH-08 | Fixture estática não é tratada como prova universal de comportamento independente da geometria. |
| CA-H0045-PH-09 | As etapas 6/17..14/17 permanecem aprovadas e somente 15/17..17/17 são reexecutadas. |
| CA-H0045-PH-10 | Implementação futura não pode ser declarada pronta para validação manual sem demonstrar que cada caso de §18.4 realmente produz o fenômeno pretendido na geometria em uso. |
| CA-H0045-PH-11 | ~~`H0045-VAL-PERMITIR` e `H0045-VAL-CONTINUACAO` usam entrada, marcadores, condição de aceite e resultado manual próprios; nenhum dos dois prova nem substitui o fenômeno do outro.~~ Sem vigência ([PATCH_HANDOFF P05] `H0045-VAL-PERMITIR` removido, §18.4); o fenômeno de fluxo contínuo passa a ser provado pela Tela 1 de §19.2. |

`CA-H0045-PH-02` a `PH-05` dependem, na redação original, dos quatro casos
adaptativos removidos (§18.4); os fenômenos que descrevem continuam
válidos e passam a ser atestados pelos critérios `CA-H0045-PH-15`/`PH-16`
(§19.8), não mais pelo harness de §18.2.

## 19. Substituição do método adaptativo e telas de validação por política (PATCH_HANDOFF P04)

Esta seção corrige o achado de `RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md`
(`HANDOFF_METHOD_DEFECT`): o método autorizado por §18 permitia que o
harness recriasse o conteúdo lógico (itens, textos, IDs) a cada resize,
zerando foco/cursor/página no processo. Onde houver conflito entre esta
seção e §18 sobre geração de conteúdo dependente de geometria ou sobre
prova por caso adaptativo único, esta seção prevalece. Não reabre cursor,
seleção, comandos de página, foco, integração dry-run/execução real, as
decisões da ADR-0038 ou as políticas contratuais de quebra além da correção
de D-TEC-07 (§10). Nenhum `PATCH_IMPLEMENTACAO` sobre este método está
autorizado antes de `QA_HANDOFF` aprovar esta correção.

### 19.1 Proibição expressa da regeneração de conteúdo lógico

Para qualquer demonstração ou validação de paginação:

- o modelo (itens, textos, IDs, ordem, políticas de quebra) é criado **uma
  única vez por execução**;
- redimensionar altera somente geometria, quebras físicas, páginas, cursor
  reconciliado e quadro exibido — nunca o conteúdo lógico;
- o conteúdo nunca é ampliado, reduzido ou substituído para manter
  artificialmente um efeito visual;
- é proibido usar hífens, espaços ou tokens gerados em função de W ou C
  como conteúdo do item;
- é proibido reconstruir o modelo após `SIGWINCH`;
- é proibido zerar foco, cursor ou página por reconstrução do caso durante
  o resize;
- execuções em dimensões diferentes usam o mesmo conteúdo lógico.

Esta proibição revoga, para implementação futura, o padrão hoje presente em
`demo/demo.py::_aplicar_caso_validacao_adaptativo` (reconstrução de itens
via `casos_val.aplicar_caso_ao_modelo` e zeragem de `foco_console`/
`cursores`/`pagina_atual`, inclusive quando reinvocado a partir do
tratamento de `SIGWINCH`) e a geração de conteúdo dependente de W em
`demo/casos_validacao_paginacao.py` (`construir_caso_largura`,
`construir_caso_permitir`, `construir_caso_evitar`,
`construir_caso_condicional`). Nenhum desses pontos pode sobreviver como
está — ver §19.3 e §19.6.

### 19.2 Três telas de validação das políticas

A implementação futura deve criar três telas fixas separadas, uma por
política, cada uma provando **somente** a sua política. Textos fixos,
coerentes e fáceis de ler. Cada tela contém: um texto inicial não avaliado
(apenas para ocupar parte da página); quatro itens avaliados, com o início
de cada um marcado visivelmente por `1.`, `2.`, `3.` e `4.`; tamanhos
variados. Proibido em qualquer uma delas: linhas no formato `PERM_L01`,
`EVIT_L01` ou equivalente; preenchimento artificial com hífens; texto
escrito como relatório, YAML ou diagnóstico técnico.

**Tela 1 — Fluxo contínuo** (`h0045_validacao_fluxo_continuo`, todos os
itens `permitir_quebra`). A composição deve permitir observar, por
redimensionamento feito pelo usuário: vários itens na mesma página; um item
começando na última linha disponível; esse item continuando na página
seguinte; um item ocupando várias páginas; cada item começando
imediatamente depois do anterior. Não há obrigação de começar no topo.

**Tela 2 — Começar em nova página** (`h0045_validacao_nova_pagina`, todos
os itens `evitar_quebra`, quatro tamanhos claramente diferentes). Deve
permitir observar: cada item começando na primeira linha útil de uma
página; espaço restante da página anterior ficando vazio; item longo
continuando nas páginas seguintes; o item posterior esperando novamente uma
nova página.

**Tela 3 — Manter junto quando possível** (`h0045_validacao_manter_junto`,
todos os itens `permitir_quebra_somente_se_maior_que_pagina`, incluindo um
item muito curto, itens intermediários e um item longo o suficiente para
ocupar mais de uma página em alguma geometria normalmente alcançável pelo
redimensionamento). Deve permitir observar: dois ou três itens permanecendo
juntos quando há espaço; um item muito curto ocupando a última linha
quando o usuário ajustar o terminal para isso; um item sendo movido inteiro
para a próxima página quando não cabe no espaço restante; um item maior
que uma página começando no topo da página seguinte e continuando nas
posteriores.

Nenhuma das três telas fixa altura de terminal para produzir esses casos —
o usuário ajusta dinamicamente largura e altura.

**Redimensionamento nas três telas**: o número de páginas pode mudar; um
item pode mudar de página; a quebra de texto pode mudar; o texto e a
numeração não podem mudar; nenhuma frase pode desaparecer ou aparecer
repetida; a política da tela deve continuar sendo obedecida após cada
redimensionamento. Não se exige que o usuário conte linhas, nem dimensão
80x24, nem número fixo de páginas.

### 19.3 Casos anteriores — substituição e desativação

Os casos adaptativos antigos `H0045-VAL-LARGURA`, `H0045-VAL-PERMITIR`,
`H0045-VAL-EVITAR` e `H0045-VAL-CONDICIONAL` (`demo/casos_validacao_
paginacao.py`, entradas `h0045_validacao_largura`/`_permitir`/`_evitar`/
`_condicional` de `demo/demo.py`) são substituídos pelas três telas fixas
de §19.2. A implementação futura pode remover ou desativar esses quatro
casos e as entradas de catálogo correspondentes.

Os casos `H0045-VAL-VAZIO` (conjunto vazio) e `H0045-VAL-CONTINUACAO`
(página formada somente pela continuação de um item) continuam separados,
mas também devem usar conteúdo fixo e nunca reconstruir o modelo durante o
redimensionamento (§19.1). A tela estática existente de conteúdo verboso
multilinha (`h0045_paginacao_modo_verboso_multilinha.json`) pode permanecer
como prova separada de quebra de texto por largura, desde que seu conteúdo
seja fixo — ela já é uma fixture estática, não um caso adaptativo.

### 19.4 Testes automatizados futuros

Adicional a §11 — e não a §18.5 nas partes dependentes do harness
adaptativo e dos quatro casos substituídos (ver nota de substituição no
início da seção 18) —, a implementação futura deve fechar:

- teste independente para cada uma das três políticas;
- o mesmo modelo renderizado em múltiplas geometrias;
- hash ou comparação estrutural comprovando que o modelo não mudou entre
  geometrias;
- verificação de ausência de perda e de duplicação de conteúdo;
- teste de resize dentro da mesma execução;
- teste do ponto de entrada real (`python demo/demo.py <tela>`);
- suíte focal e suíte completa (`PYTHONDONTWRITEBYTECODE=1 python -m
  pytest`).

Os testes não podem gerar o conteúdo esperado a partir do resultado
observado — o valor esperado é fixado antes da execução.

### 19.5 Validação manual — nova especificação de 15/17

Não reabre 6/17–14/17 (`§12 validacao_manual.estado_consolidado`;
preservadas, não reexecutadas). A etapa 15/17 (quebra e políticas) é
reespecificada para usar as três telas de §19.2 em vez de uma fixture densa
ou do harness adaptativo de §18: cada tela recebe uma instrução curta e
pergunta somente se a sua regra foi obedecida, com o gabarito único já
fixado em §18.6 (`APROVADO | REPROVADO | NÃO OBSERVADO`). O redimensionamento
é feito livremente pelo usuário durante a execução de cada tela. 16/17
(conjunto vazio) e 17/17 (página somente de continuação) permanecem
especificadas por §18.6, com a ressalva de conteúdo fixo de §19.1. Qualquer
defeito observado durante essas execuções deve ser registrado, mesmo
quando não impeça a observação da regra principal da tela; um defeito não
pode ser descartado apenas com a justificativa de que "não invalida o
teste".

### 19.6 Arquivos autorizados para a implementação futura

Estende §6.1/§18.7. Nenhum destes arquivos é criado ou alterado neste
patch documental:

```yaml
implementacao_futura_p04:
  alteraveis:
    - tela/paginacao.py   # semantica real das tres politicas (D-TEC-07 corrigido)
    - demo/demo.py         # remove reconstrucao de modelo durante resize
    - demo/casos_validacao_paginacao.py
    - demo/teste_demo_paginacao.py
    - tela/teste_paginacao.py
  criaveis:
    - config/telas/demo/h0045_validacao_fluxo_continuo.json
    - config/telas/demo/h0045_validacao_nova_pagina.json
    - config/telas/demo/h0045_validacao_manter_junto.json
  removiveis_ou_substituiveis:
    - configuracoes h0045_validacao_* antigas que nao correspondam as tres
      telas acima (entradas de catalogo largura/permitir/evitar/condicional)
  fora_de_escopo:  # [PATCH_HANDOFF P05, achado QA-H0045-P04-001]
    - tela/renderizador.py
    - tela/teste_renderizador.py
```

A implementação futura deve corrigir apenas (1) a semântica real das três
políticas em `tela/paginacao.py` (hoje `evitar_quebra` e `permitir_quebra_
somente_se_maior_que_pagina` caem no mesmo ramo de código — ver prova em
`plano_de_paginacao`/`_fragmentar_entrada` — o que já não corresponde à
correção de D-TEC-07) e (2) o método de demonstração que hoje reconstrói o
modelo durante o resize (§19.1), dentro dos arquivos listados acima:
paginação, integração da demo, casos de validação, configurações (as três
telas fixas) e testes.

`tela/renderizador.py` e `tela/teste_renderizador.py` estão fora do escopo
ativo deste patch e de qualquer patch subsequente de paginação/harness —
a análise causal não encontrou regressão neles
(`RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_VALIDACAO_ADAPTATIVA.md`, prova D;
`RENDERER_REGRESSION` permanece não classificada). Nenhuma autorização
genérica ou condicional para alterar o renderer permanece aberta neste
handoff: uma nova alteração só é autorizada se, cumulativamente, (1) surgir
evidência nova e objetiva de defeito nele, (2) essa evidência for
registrada em relatório, e (3) houver autorização específica posterior do
usuário/gerente — não este handoff. **[PATCH_HANDOFF P07]** Essas três
condições foram cumpridas para o achado `VM-H0045-R07-001` (largura
horizontal, `RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_LARGURA_HORIZONTAL.md`); a
autorização correspondente, limitada a esse achado e às duas funções
identificadas, está em §20. Fora do escopo de §20, a exclusão geral
permanece vigente para qualquer outro achado ou alteração do renderer.

### 19.7 Achados preservados fora deste patch

Não são tratados nem declarados resolvidos por este patch, e não devem ser
misturados com a correção das políticas de §10/§19:

- `VM-H0045-R06-001` — chip `[Esc] Sair` quando o primeiro `Esc` limpa a
  seleção;
- `QA-H0045-P08-001` — classificação documental do relatório P08;
- qualquer outro defeito manual já comunicado e ainda não tratado
  nominalmente.

### 19.8 Critérios de aceite deste patch (método e telas)

| ID | Critério |
|---|---|
| CA-H0045-PH-12 | D-TEC-07 (§10) reflete as três políticas de `contrato_console.md` §12 v0.2, sem afirmação de equivalência entre `evitar_quebra` e `permitir_quebra_somente_se_maior_que_pagina`. |
| CA-H0045-PH-13 | §6.4 não contém mais a ambiguidade removida. |
| CA-H0045-PH-14 | O handoff proíbe expressamente reconstrução de modelo lógico, zeragem de foco/cursor/página por reconstrução, e conteúdo gerado a partir de W/C, durante resize. |
| CA-H0045-PH-15 | Três telas fixas, uma por política, estão especificadas com conteúdo fixo e critérios de observação próprios. |
| CA-H0045-PH-16 | Os quatro casos adaptativos antigos (LARGURA/PERMITIR/EVITAR/CONDICIONAL) têm substituição ou desativação autorizada; VAZIO e CONTINUACAO permanecem, com conteúdo fixo exigido. |
| CA-H0045-PH-17 | Arquivos necessários à implementação futura estão nominalmente autorizados, sem autorizar mudança no renderer. |
| CA-H0045-PH-18 | `VM-H0045-R06-001` e `QA-H0045-P08-001` permanecem registrados como não resolvidos por este patch. |
| CA-H0045-PH-19 | 6/17–14/17 não são reabertas; 15/17 é redirecionada às três telas; 16/17 e 17/17 permanecem, com exigência de conteúdo fixo. |

## 20. Autorização focal de largura horizontal no renderer (PATCH_HANDOFF P07)

Esta seção é a única exceção admitida, até aqui, pelas condições cumulativas
de §6.2 e §19.6 à exclusão geral de `tela/renderizador.py`/
`tela/teste_renderizador.py` do escopo ativo deste handoff. Não reabre
nenhuma outra decisão técnica, achado ou etapa de validação manual já
fechada. Nenhum patch subsequente pode invocar esta seção para justificar
alteração do renderer fora do achado abaixo — uma nova evidência exigiria
nova seção equivalente.

### 20.1 Achado novo

`VM-H0045-R07-001` — o conteúdo do console não utiliza toda a largura
horizontal útil disponível.

Evidência: `docs/relatorios/RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_LARGURA_HORIZONTAL.md`.
A largura externa do console e a área interna útil estão corretas; o
conteúdo recebe aproximadamente metade da largura disponível. A primeira
divergência ocorre em `tela/renderizador.py::_linhas_distribuicao_matricial`,
onde o ramo verboso limita `texto_min` a aproximadamente
`(area_w - ind_w) // 2`; o mesmo cálculo é reproduzido em
`tela/renderizador.py::_larguras_mapa_fisico_matricial`, que alimenta o mapa
físico consumido pela paginação — renderer e mapa físico concordam sobre
essa largura incorreta. Não há evidência de defeito em `demo/demo.py`,
`tela/paginacao.py` ou nas configurações JSON das telas. O defeito é
restrito ao ramo matricial verboso de itens internos; o console externo
anterior H-0037 não o reproduz.

O texto deve utilizar a largura interna disponível até a margem direita,
descontando somente bordas, margens, marcador e indicador realmente
consumidos. Não existe autorização para reservar arbitrariamente metade da
área.

### 20.2 Autorização nominal e limites

Autorizados, exclusivamente para este achado:

- `tela/renderizador.py`;
- `tela/teste_renderizador.py`.

Restrita a:

1. remover o teto arbitrário de metade da área no cálculo da largura da
   célula única ou da distribuição correspondente;
2. fazer a célula utilizar toda a largura horizontal que lhe foi atribuída;
3. manter coerentes: linhas exibidas, mapa físico e largura usada pela
   paginação;
4. preservar margens, bordas, marcador e indicador de página;
5. impedir overflow, truncamento indevido ou deslocamento do indicador;
6. preservar distribuições com múltiplas células e outros modos já
   corretos.

Não autorizada refatoração geral do renderer.

Não autorizada alteração de: `tela/paginacao.py`, `demo/demo.py`,
`demo/casos_validacao_paginacao.py`, configurações JSON, contratos, módulos
de nomenclatura.

Se a implementação provar objetivamente que outro arquivo é indispensável,
deve parar e solicitar nova autorização — não ampliar escopo silenciosamente
(§15).

### 20.3 Funções focais autorizadas

A implementação futura pode alterar, quando necessário:

- `_linhas_distribuicao_matricial`;
- `_larguras_mapa_fisico_matricial`;
- helpers imediatamente compartilhados por essas duas funções, somente se a
  correção não puder ser feita com segurança nos pontos já identificados.

Qualquer helper adicional deve ser justificado no relatório de
implementação.

### 20.4 Comportamento esperado

Para uma única célula que ocupe toda a linha:

- a largura textual cresce junto com a largura do terminal;
- o texto alcança aproximadamente a margem interna direita;
- somente descontos estruturais reais reduzem a área textual;
- renderer e mapa físico usam a mesma largura;
- redimensionar recalcula a largura sem alterar o conteúdo lógico;
- o número de páginas pode diminuir quando a largura aumenta;
- nenhuma linha lógica pode desaparecer ou ser duplicada.

### 20.5 Testes automatizados futuros exigidos

Larguras equivalentes a 80, 120, 160 e 200 colunas. Cobertura mínima:

1. as cinco telas H-0045 (`h0045_validacao_continuacao`,
   `h0045_validacao_fluxo_continuo`, `h0045_validacao_nova_pagina`,
   `h0045_validacao_manter_junto`, `h0045_paginacao_modo_verboso_multilinha`);
2. largura efetiva da célula;
3. maior linha física produzida;
4. igualdade entre largura usada pelo renderer e pelo mapa físico;
5. ausência de perda ou repetição de conteúdo;
6. resize;
7. preservação do indicador de página;
8. ausência de overflow;
9. regressão do console externo H-0037;
10. distribuições matriciais com mais de uma célula.

Não é exigida dimensão fixa para a validação manual.

### 20.6 Validação manual focal futura

Após o patch de implementação e seu QA, o usuário executa:

```
python demo/demo.py h0045_validacao_continuacao
```

Em terminal largo e durante redimensionamento, deve observar: texto
utilizando a largura até a margem interna direita; indicador de página
preservado; ausência de overflow ou truncamento; conteúdo invariável;
paginação recalculada conforme a largura atual.

As validações anteriormente aprovadas permanecem aprovadas. Não reabre
6/17–14/17, 15/17-A, 15/17-B, 15/17-C, 16/17 nem 17/17 (§12, §19.5). A
validação futura verifica somente o novo achado horizontal.

### 20.7 Achados preservados fora deste patch

Continuam abertos e não são declarados resolvidos por este patch:

- `VM-H0045-R06-001`;
- `QA-H0045-P08-001`.

### 20.8 Critérios de aceite deste patch

| ID | Critério |
|---|---|
| CA-H0045-PH-20 | `VM-H0045-R07-001` está registrado nominalmente com a evidência do relatório de causa raiz da largura horizontal. |
| CA-H0045-PH-21 | Renderer e teste do renderer estão autorizados nominalmente, restritos a este achado. |
| CA-H0045-PH-22 | A correção está limitada aos dois cálculos identificados em `_linhas_distribuicao_matricial` e `_larguras_mapa_fisico_matricial`. |
| CA-H0045-PH-23 | Não há autorização de refatoração geral do renderer. |
| CA-H0045-PH-24 | Coerência exigida entre renderer e mapa físico usado pela paginação. |
| CA-H0045-PH-25 | Uso de toda a largura útil exigido, com descontos apenas estruturais reais. |
| CA-H0045-PH-26 | Margens e indicador de página preservados. |
| CA-H0045-PH-27 | Regressão exigida nas cinco telas H-0045 e no caso H-0037. |
| CA-H0045-PH-28 | `VM-H0045-R06-001` e `QA-H0045-P08-001` permanecem registrados como não resolvidos. |

## 21. Autorização focal dos testes bloqueadores do P17 (PATCH_HANDOFF P08)

Esta seção trata exclusivamente o bloqueio transportado pelo
`RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P17.md` (identificador gerencial
`IMP-H0045-P17-001`). Não reabre nenhuma outra decisão técnica, achado ou
etapa de validação manual já fechada, nem amplia a autorização de §20.
Nenhum patch subsequente pode invocar esta seção para justificar alteração
de arquivo diferente dos dois nominados abaixo.

### 21.1 Bloqueio transportado

O `PATCH_IMPLEMENTACAO P17` corrigiu `VM-H0045-R07-001` em
`tela/renderizador.py` e `tela/teste_renderizador.py` (escopo de §20),
removendo o teto indevido de metade da largura no ramo verboso da grade
matricial, de modo que a célula única passa a usar toda a área horizontal
que lhe é atribuída. Essa correção reduz legitimamente o número de linhas
físicas por item e, por consequência, o número de páginas em cenários já
cobertos por teste automatizado.

A suíte completa revelou cinco asserções, em dois arquivos, calibradas
contra a geometria antiga (teto de metade da área):

- `demo/teste_demo_paginacao.py` — quatro testes com `total_paginas` fixo;
- `demo/teste_demo_navegacao.py` — um teste com contagem mínima de linhas
  físicas.

Nenhum dos dois arquivos estava autorizado pela lista de arquivos do
`PATCH_IMPLEMENTACAO P17` (restrita a `tela/renderizador.py`/
`tela/teste_renderizador.py` por §20); por isso permaneceram intocados e o
patch foi reportado como `IMPLEMENTATION_BLOCKED`.

### 21.2 Autorização nominal e limites

Autorizados, exclusivamente para este bloqueio, e adicionalmente aos
arquivos já autorizados para `VM-H0045-R07-001` (§20):

- `demo/teste_demo_paginacao.py` — restrita aos quatro testes de §21.3;
- `demo/teste_demo_navegacao.py` — restrita ao teste de §21.3.

Não autorizada alteração de código produtivo adicional: `tela/paginacao.py`,
`demo/demo.py`, `demo/casos_validacao_paginacao.py`,
`tela/renderizador.py` (além do já aplicado por P17), configurações JSON,
contratos, ADR, módulos de nomenclatura, ou qualquer outro teste além dos
cinco nominados. Se a implementação provar objetivamente que outro caminho
é indispensável, deve parar e solicitar nova autorização (§15) — não
ampliar escopo silenciosamente.

### 21.3 Testes autorizados

**`demo/teste_demo_paginacao.py`** — quatro testes, cujos totais
esperados foram calibrados para a largura limitada à metade e precisam
refletir a largura corrigida:

1. `test_demo_h0045_p10_fixture_real_verbosa_multilinha_paginada_sem_perdas`
   — 3 páginas passam a 2;
2. `test_demo_h0045_p10_dimensao_menor_repagina_sem_perda_e_cursor_correto`
   — 6 páginas passam a 4;
3. `test_demo_h0045_p11_politicas_quebra_fixture_real_seis_paginas_sem_perdas`
   — 6 páginas passam a 2;
4. `test_demo_h0045_p11_politicas_quebra_dimensao_menor_deriva_da_politica`
   — 11 páginas passam a 4.

A correção deve: atualizar as expectativas numéricas incompatíveis com a
largura corrigida; ajustar, quando necessário, as asserções dependentes da
distribuição de fragmentos por página (posição de cursor, conteúdo de cada
página, contagem de continuações); preservar integralmente a prova de
ausência de perda, ausência de repetição, ordem dos itens, política de
quebra, cursor e página reconciliados, e repaginação conforme a geometria.
Não remover verificação semântica apenas para obter suíte verde. Valores
numéricos exatos podem permanecer quando a geometria do teste é fixa e o
valor corrigido é parte da prova.

**`demo/teste_demo_navegacao.py`** — um teste:

5. `teste_prova_mudanca_modo_nao_reinicia_item_zero` — o item verboso
   ("Gamma...") agora cabe em menos linhas físicas na largura do cenário
   (antes exigia 2+). O objetivo do teste deve permanecer: alternar o modo
   não reinicia o primeiro item; o conteúdo verboso usado na prova ocupa
   mais de uma linha física; foco, item e navegação permanecem coerentes.
   A correção preferida é tornar o texto de teste suficientemente longo
   para continuar ocupando duas ou mais linhas físicas com a largura
   corrigida. É proibido enfraquecer a prova trocando
   `len(linhas_com_gamma) >= 2` por uma expectativa que aceite apenas uma
   linha.

### 21.4 Estado do delta do P17

A correção produtiva de largura já foi aplicada no worktree
(`tela/renderizador.py`, `tela/teste_renderizador.py`). O
`PATCH_IMPLEMENTACAO P17` permanece `IMPLEMENTATION_BLOCKED` até a
atualização dos cinco testes listados em §21.3. Não é necessário reverter
`tela/renderizador.py`. O próximo `PATCH_IMPLEMENTACAO` deve continuar
sobre o delta já aplicado por P17, não recriá-lo. Depois da atualização dos
testes, devem ser repetidas as suítes focal e completa (§21.5).

### 21.5 Suítes futuras obrigatórias

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_renderizador.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_renderizador.py \
  tela/teste_paginacao.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q
```

```bash
git diff --check -- \
  tela/renderizador.py \
  tela/teste_renderizador.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py
```

A suíte completa deve ficar integralmente verde antes de QA da
implementação.

### 21.6 Validação manual

Não executada nesta etapa documental. A validação focal futura permanece:

```
python demo/demo.py h0045_validacao_continuacao
```

As validações anteriormente aprovadas (§12, §19.5, §20.6) permanecem
aprovadas e não são reabertas por esta seção.

### 21.7 Achados preservados fora deste patch

Continuam abertos e não são declarados resolvidos por este patch:

- `VM-H0045-R06-001`;
- `QA-H0045-P08-001`.

`VM-H0045-R07-001` só poderá ser declarado resolvido após: (1) conclusão do
patch de implementação sobre os cinco testes de §21.3; (2) suíte completa
verde; (3) QA pós-patch; (4) validação manual focal do usuário (§21.6).

### 21.8 Critérios de aceite deste patch

| ID | Critério |
|---|---|
| CA-H0045-PH-29 | `IMP-H0045-P17-001` está registrado nominalmente com a origem do bloqueio (`RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P17.md`). |
| CA-H0045-PH-30 | Somente `demo/teste_demo_paginacao.py` e `demo/teste_demo_navegacao.py` estão autorizados nominalmente, adicionalmente aos arquivos já autorizados por §20. |
| CA-H0045-PH-31 | A autorização está restrita aos cinco testes nominados em §21.3. |
| CA-H0045-PH-32 | Nenhuma alteração de código produtivo adicional (além do já aplicado por P17) é autorizada. |
| CA-H0045-PH-33 | A intenção semântica de cada um dos cinco testes é preservada; nenhuma verificação pode ser removida apenas para obter suíte verde. |
| CA-H0045-PH-34 | O próximo `PATCH_IMPLEMENTACAO` continua sobre o delta já aplicado por P17, sem reversão de `tela/renderizador.py`. |
| CA-H0045-PH-35 | Suíte completa exigida verde antes de QA, com os comandos de §21.5. |
| CA-H0045-PH-36 | Validação manual focal permanece pendente ao usuário (§21.6); validações anteriores não são reabertas. |
| CA-H0045-PH-37 | `VM-H0045-R06-001` e `QA-H0045-P08-001` permanecem registrados como não resolvidos. |

## 22. Autorização focal para VM-H0045-R06-001 — chip Esc dinâmico (PATCH_HANDOFF P09)

Esta seção autoriza exclusivamente a implementação corretiva de
`VM-H0045-R06-001`. Ela prevalece sobre as exclusões anteriores de
`tela/renderizador.py` e `tela/teste_renderizador.py` somente para este
achado, nos limites nominais abaixo. Não declara o achado resolvido, não
autoriza QA, validação manual, stage, commit ou outro ciclo.

### 22.1 Achado e evidência transportada

`VM-H0045-R06-001` — o chip `[Esc]` apresenta a ação de saída quando existe
seleção ativa no console focado, embora o primeiro `Esc` apenas limpe a
seleção e mantenha a tela aberta.

O `PATCH_IMPLEMENTACAO P20`, registrado em
`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P20.md`, confirmou:

- o tratamento funcional já existente em `demo/demo.py` está correto: com
  seleção múltipla reconciliada não vazia, o primeiro `Esc` limpa a seleção
  e retorna sem sair; sem seleção, segue a ação normal de Sair/Voltar;
- o defeito está na composição estática de `_linhas_barra`, em
  `tela/renderizador.py`;
- `forma_exibicao` já materializa o rótulo dinâmico de `[Enter]` e pode ser
  estendido focalmente para `[Esc]`;
- `tela/selecao.py` já fornece a seleção reconciliada e a limpeza pura;
  ainda não existe função de rótulo para Esc.

### 22.2 Comportamento obrigatório

Quando o console atualmente focado declara seleção múltipla e sua seleção
reconciliada não está vazia, o chip deve exibir exatamente `[Esc] Limpar`.
O primeiro `Esc` deve limpar toda a seleção desse console, manter a tela
aberta, preservar foco, cursor e página válidos e atualizar a barra
imediatamente.

Quando não houver seleção ativa, o chip deve recuperar exatamente o texto
original configurado para Esc — `Sair`, `Voltar` ou outro rótulo original
válido — e o Esc seguinte deve executar essa ação normal. É proibido
substituir genericamente `Voltar` por `Sair` ou exibir `Limpar` e a ação
original simultaneamente.

Somente a seleção do console focado participa da decisão. Seleção em outro
console não altera o chip. Resize, troca de página e troca de foco devem
recalcular o rótulo; sem console de seleção múltipla focado, o rótulo
original deve ser preservado. O comportamento funcional de Esc em
`demo/demo.py` não deve ser alterado.

### 22.3 Autorização nominal e limites

São autorizados, exclusivamente para este achado:

- `tela/renderizador.py`: `_linhas_barra`, a interpretação focal de
  `forma_exibicao` para o chip Esc e helper imediatamente compartilhado se
  indispensável;
- `tela/teste_renderizador.py`: testes focais do rótulo, da atualização da
  barra e da ausência de regressão da composição;
- `tela/selecao.py`: função pura, por exemplo `rotulo_esc`, que determine o
  rótulo a partir do estado reconciliado do console focado;
- `tela/teste_selecao.py`: cobertura unitária da função pura e da limpeza;
- `demo/teste_demo_paginacao.py` e `demo/teste_demo_navegacao.py`: cobertura
  integrada do primeiro/segundo Esc, foco, página e resize;
- as configurações autorizadas para alteração, listadas em §22.3.1.

#### 22.3.1 Configurações autorizadas para alteração

São autorizadas para alteração da declaração existente de exibição do chip
Esc, exclusivamente por combinarem simultaneamente seleção múltipla, chip
Esc e rótulo estático que deve adotar a forma de exibição dinâmica:

- `config/telas/demo/h0045_fluxo_execucao_paginado.json` — configuração
  adicional encontrada pela busca focal, enumerada nominalmente antes da
  implementação;
- `config/telas/demo/h0044_fluxo_execucao_integrado.json`;
- `config/telas/demo/h0041_selecao_multipla_oito_itens.json`.

Na verificação deste handoff, as três configurações acima satisfazem
simultaneamente seleção múltipla, chip Esc e rótulo estático.

#### 22.3.2 Configurações preservadas e fora do escopo de alteração

`config/telas/demo/h0045_paginacao_console_unico.json` e
`config/telas/demo/h0045_dois_consoles_paginas_independentes.json` são
preservadas e não estão autorizadas para alteração por `VM-H0045-R06-001`:

- ambas declaram `politica_selecao: "unica"`;
- não precisam receber a nova forma de exibição dinâmica baseada em seleção
  múltipla;
- permanecem cobertas por testes de regressão, sem alteração de
  comportamento ou de rótulo do chip Esc;
- nenhuma seleção ou estado de outro console altera o chip Esc dessas
  configurações (§22.2).

É permitido alterar somente a declaração existente de exibição do chip Esc
nas configurações autorizadas em §22.3.1. Não criar campo
de configuração: `rotulo_dinamico_esc` pode ser apenas um valor específico
do mecanismo existente `forma_exibicao`. Não autorizar refatoração geral da
barra, renderer, seleção ou navegação; não alterar `demo/demo.py`, contratos,
ADR, backlog, nomenclatura ou outros arquivos.

### 22.4 Testes futuros obrigatórios

Exigir cobertura para:

1. sem seleção: rótulo original `Sair`;
2. sem seleção em tela aninhada: rótulo original `Voltar`;
3. uma seleção: `Limpar`;
4. várias seleções: `Limpar`;
5. seleção distribuída por páginas: `Limpar`;
6. primeiro Esc limpa e não sai;
7. depois da limpeza, retorna ao rótulo original;
8. segundo Esc executa Sair ou Voltar;
9. Limpar e Sair/Voltar nunca aparecem simultaneamente;
10. troca de página mantém o rótulo correto;
11. resize mantém o rótulo correto;
12. troca de foco entre dois consoles usa somente a seleção do console focal;
13. cursor, foco e página permanecem reconciliados;
14. Enter, Espaço, paginação e seleção múltipla não sofrem regressão.

Exigir, após a implementação:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_renderizador.py \
  tela/teste_selecao.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py
```

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q
```

`tela/teste_selecao.py` existe e é o arquivo real de cobertura da seleção;
nenhum arquivo de teste substituto deve ser criado arbitrariamente.

### 22.5 Validação manual futura e achados preservados

Depois do patch e do QA, o usuário validará em uma tela H-0045 com seleção
múltipla: (1) sem seleção, Sair ou Voltar conforme a tela; (2) ao selecionar
um item, `[Esc] Limpar`; (3) primeiro Esc limpa e mantém a tela aberta; (4) o
chip retorna ao rótulo original; (5) segundo Esc executa a saída ou retorno.

As validações anteriores permanecem aprovadas e não são reabertas, inclusive
`VM-H0045-R07-001`. `QA-H0045-P08-001` continua tratado separadamente por
correção factual manual e não é declarado resolvido por este patch.

### 22.6 Critérios de aceite desta autorização

| ID | Critério |
|---|---|
| CA-H0045-P09-01 | `VM-H0045-R06-001` está registrado com a evidência do P20. |
| CA-H0045-P09-02 | Renderer, seleção, testes e configurações necessárias estão autorizados nominalmente e focalmente. |
| CA-H0045-P09-03 | `demo/demo.py` permanece preservado; seu Esc funcional não é alterado. |
| CA-H0045-P09-04 | `Limpar` é distinto do rótulo original `Sair`/`Voltar` e depende somente do console focado. |
| CA-H0045-P09-05 | Não é criado campo de configuração nem autorizada refatoração geral. |
| CA-H0045-P09-06 | Primeiro Esc limpa; segundo Esc executa a ação original. |
| CA-H0045-P09-07 | Rótulo é atualizado após página, foco e resize, sem coexistência de Limpar e Sair/Voltar. |
| CA-H0045-P09-08 | Validações anteriores permanecem aprovadas e P08 permanece separado. |
| CA-H0045-P09-09 | As suítes focal e completa de §22.4 são obrigatórias antes do QA. |
| CA-H0045-P09-10 | O handoff passa em `git diff --check`. |

## 23. Autorização focal para VM-H0045-R08-001 — terminal insuficiente na barra de cinco chips (PATCH_HANDOFF P11)

Esta seção autoriza exclusivamente a implementação corretiva de
`VM-H0045-R08-001`. Ela prevalece sobre as exclusões anteriores de
`tela/renderizador.py` e `tela/teste_renderizador.py` somente para este
achado, nos limites nominais abaixo. Não declara o achado resolvido, não
autoriza QA, validação manual, stage, commit ou outro ciclo.

### 23.1 Achado e evidência transportada

`VM-H0045-R08-001` — ao reduzir o terminal durante `python demo/demo.py
h0045_fluxo_execucao_paginado`, a barra de cinco chips (`[Esc]`, `[<]`,
`[>]`, `[␣]`, `[⏎]`) deixa de caber no máximo efetivo de duas linhas;
`_linhas_barra` lança `RenderizadorErro` e a consulta de geometria feita
durante o resize não captura essa exceção; a demonstração termina com
traceback.

`RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_TERMINAL_ESTREITO.md` confirmou:

- o JSON declara apenas o alias `"horizontal"`, normalizado pelo renderer
  para o objeto canônico default (`_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT`),
  cujo `linhas.maximo` é `2` — comportamento normativo, não defeito;
- em `_geometria_por_console`, a chamada a `_linhas_barra` ocorre fora do
  bloco `try/except RenderizadorErro` que hoje só envolve
  `_renderizar_container`; a exceção escapa para `geometria_console` e, a
  partir daí, para `_com_geometria_real_do_console` e
  `_reconciliar_paginacao_apos_resize`;
- em `main`, o trecho de resize chama `_reconciliar_paginacao_apos_resize`
  antes de `_resolver_conteudo`; `_resolver_conteudo` já captura
  `RenderizadorErro` e produz um quadro mínimo de aviso
  (`_tela_pequena_demais`/`_quadro_minimo_aviso`), mas essa rede de
  segurança nunca é alcançada porque a exceção já escapou antes;
- o mesmo risco existe em qualquer comando que consulte geometria através de
  `_com_geometria_real_do_console` (paginação, setas) durante geometria
  inválida;
- os primeiros limites medidos para esta barra: 1 linha a partir de ~65
  colunas, 2 linhas a partir de ~41, 3 a partir de ~29, 4 a partir de ~28, 5
  a partir de ~17; considerando altura, `20x10` foi o menor quadro completo
  viável medido com até 5 linhas.

### 23.2 Solução combinada autorizada

1. configurar explicitamente esta tela para permitir até cinco linhas na
   barra;
2. escolher sempre a menor quantidade de linhas que comporte todos os
   chips;
3. quando a tela completa ainda não puder ser representada, entrar em
   estado controlado de terminal insuficiente;
4. impedir qualquer traceback;
5. preservar integralmente o estado lógico;
6. recuperar automaticamente a tela normal quando a geometria voltar a ser
   válida.

O limite global de duas linhas (`_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT`)
não é alterado por esta autorização.

### 23.3 Configuração autorizada

Autoriza-se alteração somente em
`config/telas/demo/h0045_fluxo_execucao_paginado.json`, substituindo o
alias `"distribuicao": "horizontal"` pelo objeto canônico já existente e já
validado por `_normalizar_distribuicao`/`_validar_distribuicao`
(`tela/renderizador.py`), com `linhas.maximo` elevado de `2` para `5`:
`modo: "horizontal_responsiva"`; `ordem.politica: "declaracao"`;
`preenchimento_multilinha: "coluna_a_coluna"`; `linhas: {minimo: 1, maximo:
5, preferir_menor_numero: true}`; `espacamentos` (margem horizontal, vãos
chip-texto, entre chips, entre colunas, vertical entre linhas) idênticos ao
default atual; `overflow: {quando_nao_couber: "erro_layout",
nao_omitir_chips: true, nao_truncar_texto: true, nao_reordenar: true}`.
Nenhum campo novo é criado — é a materialização explícita de um schema já
suportado pelo renderer. Não alterar chips, teclas, textos, ordem, regras
de existência/atividade ou cores; o rótulo dinâmico de `[Esc]` do P09/P20
permanece intacto. Nenhuma outra configuração é autorizada por este item.

### 23.4 Comportamento normal, estado controlado e recuperação

Enquanto houver largura e altura suficientes: usar a menor quantidade de
linhas (1 a 5) que comporte todos os chips sem omitir, truncar ou
reordenar; recalcular altura útil do console, capacidade e total de
páginas; reconciliar a página pelo item lógico atual; preservar seleção,
foco e cursor. Cada linha adicional pode reduzir a área do console e
aumentar o total de páginas — comportamento esperado, não perda de estado.

Quando nem cinco linhas permitirem representar a tela completa, a
demonstração deve: não lançar traceback; não encerrar a aplicação; não
manter um quadro antigo congelado; apresentar estado explícito de terminal
pequeno com a mensagem semântica `"Terminal pequeno demais" / "Aumente a
janela para continuar"` (adaptável/quebrável à largura disponível; saída
mínima segura em dimensões extremas, sem nova exceção); não renderizar
parcialmente a interface normal; não omitir chips silenciosamente; não
reconstruir o modelo lógico. A entrada e a saída desse estado não podem
alterar tela atual, pilha de telas, conteúdo lógico, identidade/ordem dos
itens, seleção, console focado, cursor lógico, página lógica reconciliada,
modo verboso, estado de execução ou rótulo dinâmico de Esc. O evento de
resize não é comando de navegação ou seleção.

Na recuperação (largura/altura voltam a ser suficientes): recalcular
geometria, paginação e indicador; relocalizar o item lógico atual;
restaurar a tela normal; preservar seleção, foco e cursor; sem repetição,
perda ou reinício da demonstração.

### 23.5 Autorização nominal — código produtivo

`demo/demo.py`, somente: `_reconciliar_paginacao_apos_resize`;
`_com_geometria_real_do_console`; `_resolver_conteudo`; trecho de resize em
`main`; helper mínimo para identificar erro de geometria insuficiente
(pode reaproveitar/estender o padrão já existente de
`_tela_pequena_demais`, distinguindo-o da insuficiência específica de barra
sinalizada por `RenderizadorErro`); helper mínimo para produzir o quadro
controlado de terminal pequeno (pode reaproveitar/estender
`_quadro_minimo_aviso`, hoje limitado a uma linha de aviso, para a mensagem
semântica de duas linhas exigida em §23.4). É permitido reorganizar
localmente a captura para evitar duplicação; não é autorizada refatoração
do ciclo geral da demo.

`tela/renderizador.py`, somente se necessário para cumprir a configuração
explícita de §23.3 ou para distinguir com segurança o erro de geometria
insuficiente: `_linhas_barra`; `_geometria_por_console` (hoje o
`try/except RenderizadorErro` cobre apenas a chamada a
`_renderizar_container`, não a chamada anterior a `_linhas_barra` — a
extensão mínima é ampliar essa mesma captura já existente); `geometria_console`;
helper imediatamente compartilhado. Não alterar: o default global de duas
linhas; funções de largura do P17; distribuição matricial de conteúdo;
paginação; composição semântica dos chips; rótulo dinâmico de Enter ou Esc.
Se a configuração explícita de cinco linhas já for integralmente suportada
sem essa extensão, o renderer não deve ser alterado apenas por
conveniência.

### 23.6 Autorização nominal — testes

Autoriza-se: `tela/teste_renderizador.py`; `demo/teste_demo_paginacao.py`;
`demo/teste_demo_navegacao.py`. Autoriza-se leitura e regressão, mas não
alteração produtiva, de `tela/paginacao.py` e `tela/navegacao.py`. Nenhum
outro arquivo é autorizado.

### 23.7 Tratamento de erros e comandos durante geometria inválida

A captura deve impedir que `RenderizadorErro` escape dos caminhos de
consulta de geometria usados por resize e por comandos (`_com_geometria_
real_do_console`, chamada por paginação e setas em `processar_comando`),
restrita a erros de layout causados por geometria insuficiente da tela
corrente — não a todo `RenderizadorErro` do renderer. Erros de modelo,
configuração inválida ou invariantes quebradas continuam visíveis nos
testes e não podem ser mascarados. Comandos dependentes de geometria não
devem corromper nem recalcular estado a partir de geometria inválida; o
`[Esc]` continua seguindo o comportamento funcional vigente quando
processável sem depender da geometria (limpar seleção quando houver
seleção múltipla ativa; sair ou voltar quando não houver). Não alterar
`demo/demo.py` além do tratamento focal autorizado em §23.5.

### 23.8 Contrato e default global

Registra-se expressamente: não é necessário patch de contrato; a
configuração explícita de até cinco linhas é local a esta tela; o default
normativo global de duas linhas permanece; `overflow.quando_nao_couber:
erro_layout` permanece válido; o erro continua sendo usado internamente
para detectar que a tela normal não pode ser composta; somente sua
apresentação não pode escapar como traceback ao usuário.

### 23.9 Testes futuros obrigatórios

Exigir cobertura para: abertura inicial em dimensão suficiente; barra em
uma, duas, três, quatro e cinco linhas; escolha da menor quantidade válida;
dimensão em que nem cinco linhas resolvem; altura insuficiente apesar da
largura; ausência de traceback no resize e em comandos que consultem
geometria; quadro explícito de terminal pequeno sem interface normal
parcialmente exibida; preservação de seleção, foco, cursor, item lógico,
página (ou sua reconciliação) e pilha de telas; recuperação automática ao
ampliar; ausência de perda, repetição, truncamento ou reordenação de chips;
rótulo dinâmico de Esc (primeiro Esc limpa sem sair; segundo Esc sai ou
volta); regressão das demais telas H-0045 e das configurações que
permanecem com máximo de duas linhas; suíte completa verde; `git diff
--check` limpo.

Exigir matriz técnica, sem TTY interativo, cobrindo pelo menos larguras 16,
17, 20, 28, 29, 40, 41, 64, 65, 120 e alturas 6, 8, 10, 15, 24, 40,
registrando para cada par material: quantidade de linhas da barra;
geometria válida ou insuficiente; altura consumida pela barra; capacidade
da página; página atual e total; estado controlado quando aplicável;
ausência de exceção não tratada.

### 23.10 Validação manual futura

Depois de implementação e QA, o usuário valida em TTY real: abrir
`h0045_fluxo_execucao_paginado` em tamanho normal; selecionar um item;
reduzir progressivamente a largura observando 2, 3, 4 e 5 linhas; reduzir
até o estado de terminal pequeno; confirmar ausência de traceback e a
mensagem controlada; ampliar novamente e confirmar recuperação automática
com seleção, foco, cursor, item e página preservados; confirmar `[Esc]
Limpar` com seleção, limpar e confirmar retorno a `[Esc] Sair`, sair com o
segundo Esc.

### 23.11 Pendências preservadas

`VM-H0045-R08-001` permanece aberto até implementação, QA técnico e
validação manual. `VM-H0045-R06-001` (implementação e QA técnico
aprovados; validação manual da tela raiz parcialmente aprovada) não é
reaberto por este patch — seu código não é reprocessado; seu comportamento
deve apenas ser preservado durante o resize. Não reabrir `VM-H0045-R07-001`,
`QA-H0045-P08-001`, nem as validações 6/17 a 17/17 já aprovadas.

### 23.12 Critérios de aceite desta autorização

| ID | Critério |
|---|---|
| CA-H0045-P11-01 | `VM-H0045-R08-001` está registrado com a evidência de `RELATORIO_ANALISE_CAUSA_RAIZ_H-0045_TERMINAL_ESTREITO.md`. |
| CA-H0045-P11-02 | Autoriza no máximo cinco linhas somente para `h0045_fluxo_execucao_paginado.json`, sem criar campo novo. |
| CA-H0045-P11-03 | O default global de duas linhas permanece intocado. |
| CA-H0045-P11-04 | Nenhuma omissão, truncamento ou reordenação de chips é autorizada. |
| CA-H0045-P11-05 | Estado controlado de terminal insuficiente é exigido, sem traceback e sem interface normal parcial. |
| CA-H0045-P11-06 | A captura de erro é restrita a geometria insuficiente da tela corrente; erros de modelo/configuração continuam visíveis. |
| CA-H0045-P11-07 | Todo o estado lógico (tela, pilha, itens, seleção, foco, cursor, página, modo, execução, rótulo de Esc) é preservado na entrada e saída do estado controlado. |
| CA-H0045-P11-08 | Recuperação automática é exigida ao voltar a geometria válida. |
| CA-H0045-P11-09 | Código, configuração e testes são autorizados nominal e focalmente, sem refatoração geral. |
| CA-H0045-P11-10 | `VM-H0045-R06-001`, `VM-H0045-R07-001`, `QA-H0045-P08-001` e as validações 6/17–17/17 não são reabertos. |
| CA-H0045-P11-11 | Testes futuros e matriz de dimensões (§23.9) são exigidos antes do QA. |
| CA-H0045-P11-12 | Validação manual futura (§23.10) está prevista e reservada ao usuário. |
| CA-H0045-P11-13 | O handoff passa em `git diff --check`. |

## 24. Autorização complementar nominal de `demo/teste_demo.py` — dois testes (PATCH_HANDOFF P12)

Esta seção trata exclusivamente o bloqueio transportado por
`RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P24.md` (identificador gerencial
`IMP-H0045-P24-001`). Não reabre nenhuma outra decisão técnica, achado ou
etapa de validação manual já fechada, nem amplia a autorização de §23. A
seção §23 permanece integralmente vigente e não é reescrita além do
necessário para registrar esta autorização adicional.

### 24.1 Bloqueio transportado

O `PATCH_IMPLEMENTACAO P24` confirmou que `erro_layout:` possui um produtor
real específico e exclusivo para a barra de menus, que `altura
insuficiente:` possui produtores geometricamente reais, e que `DA-02` e
`DA-04` são erros estruturais — nenhum código `DA` deve ser tratado
genericamente como insuficiência geométrica (achado sem bloqueio,
`QA-H0045-P23-001`). A classificação correspondente e a unificação do
quadro controlado podem ser corrigidas em `demo/demo.py`, sem alteração do
renderer.

O único bloqueio real decorre de duas expectativas vigentes em
`demo/teste_demo.py`, arquivo não autorizado pelo escopo do P24:

- `teste_redimensionamento_reativo_h0023`, seção 8.12 (`:2313-2317`) —
  injeta `RenderizadorErro("r")` sintético e espera quadro mínimo, quando
  `QA-H0045-P23-002` exige propagação do erro estrutural;
- `test_h0044_p01_redimensionamento_resolve_bloqueio_visual` (`:3984-3985`)
  — verifica apenas `"terminal pequeno demais"` em minúsculas para altura
  insuficiente, quando `QA-H0045-P23-003` exige o quadro controlado
  unificado do H-0045.

### 24.2 Autorização nominal e limites

Autorizado, exclusivamente para este bloqueio, e adicionalmente aos
arquivos já autorizados por §23 (`demo/demo.py`, `tela/teste_renderizador.py`,
`demo/teste_demo_paginacao.py`, `demo/teste_demo_navegacao.py`):

- `demo/teste_demo.py` — restrito aos dois testes de §24.3 e ao suporte
  local diretamente indispensável dentro deles.

Não autorizado: alteração de qualquer outro teste em `demo/teste_demo.py`;
refatoração geral do arquivo; alteração de helpers compartilhados, salvo
quando diretamente indispensável a estes dois testes e sem mudar sua
semântica para outros cenários; remoção de cobertura legada; alteração
produtiva de H-0023 ou H-0044; alteração do renderer; alteração de
contratos ou configurações. Se a implementação provar objetivamente que
outro caminho é indispensável, deve parar e solicitar nova autorização
(§15) — não ampliar escopo silenciosamente.

### 24.3 Testes autorizados e nova expectativa

**1. `teste_redimensionamento_reativo_h0023`** — seção 8.12 (`:2313-2317`):

`RenderizadorErro("r")` é um erro estrutural sintético, sem correspondência
a produtor geométrico autorizado. `_resolver_conteudo` deve relançá-lo; o
teste deve esperar explicitamente essa propagação — não deve esperar quadro
mínimo ou estado controlado. A cobertura de redimensionamento reativo do
H-0023 deve ser preservada; o subcaso não pode ser removido sem
substituição por uma prova explícita e equivalente de propagação.

**2. `test_h0044_p01_redimensionamento_resolve_bloqueio_visual`** (`:3984-3985`):

Altura insuficiente é insuficiência geométrica autorizada e deve usar o
mesmo quadro controlado do H-0045. Quando houver espaço, a saída deve
conter semanticamente `"Terminal pequeno demais"` e `"Aumente a janela para
continuar"`; o teste deve verificar as duas mensagens, sem depender apenas
da capitalização antiga. A prova de recuperação após aumentar a dimensão
deve ser preservada; a cobertura original do H-0044 não pode ser
enfraquecida.

### 24.4 Correção produtiva futura preservada

A continuação do `PATCH_IMPLEMENTACAO P24` deve: remover a classificação
ampla `startswith("DA-0")`, sem absorver `DA-02`, `DA-04`, `DA-01`,
`DA-099` ou códigos futuros; reconhecer apenas o formato específico do
`erro_layout` da barra; reconhecer somente os produtores reais de `altura
insuficiente`; relançar erros estruturais em `_resolver_conteudo`; unificar
o quadro controlado para insuficiência de largura e altura; mostrar as duas
mensagens em `80x8` quando couberem; preservar integralmente o P23. Esta
seção não reescreve a solução técnica de §23 além do necessário para
registrar esta autorização adicional.

### 24.5 Suítes futuras obrigatórias

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  demo/teste_demo.py \
  tela/teste_renderizador.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py \
  -k "P23 or p23 or P24 or p24 or redimensionamento_reativo_h0023 or h0044_p01"

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  demo/teste_demo.py \
  tela/teste_renderizador.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q
```

```bash
git diff --check -- \
  demo/demo.py \
  demo/teste_demo.py \
  tela/teste_renderizador.py \
  demo/teste_demo_paginacao.py \
  demo/teste_demo_navegacao.py
```

A suíte completa deve ficar integralmente verde antes de QA da
implementação.

### 24.6 Pendências preservadas

`VM-H0045-R08-001` permanece aberto até: continuação do P24; QA técnico;
validação manual. Não são reabertos: `VM-H0045-R06-001` (salvo preservação
durante resize, já prevista por §23); `VM-H0045-R07-001`;
`QA-H0045-P08-001`; as validações manuais 6/17–17/17 já aprovadas.

### 24.7 Critérios de aceite deste patch

| ID | Critério |
|---|---|
| CA-H0045-P12-01 | `IMP-H0045-P24-001` está registrado nominalmente com a origem do bloqueio (`RELATORIO_PATCH_IMPLEMENTACAO_H-0045_P24.md`). |
| CA-H0045-P12-02 | Somente `demo/teste_demo.py` é acrescentado ao escopo, adicionalmente aos arquivos já autorizados por §23. |
| CA-H0045-P12-03 | A autorização está restrita aos dois testes nominados em §24.3 e ao suporte local diretamente indispensável dentro deles. |
| CA-H0045-P12-04 | Nenhuma alteração produtiva de H-0023, H-0044 ou do renderer é autorizada. |
| CA-H0045-P12-05 | `teste_redimensionamento_reativo_h0023` passa a exigir propagação explícita do erro estrutural sintético, sem esperar quadro mínimo. |
| CA-H0045-P12-06 | `test_h0044_p01_redimensionamento_resolve_bloqueio_visual` passa a exigir as duas mensagens do quadro controlado unificado, preservando a prova de recuperação. |
| CA-H0045-P12-07 | A cobertura legada de H-0023 e H-0044 é preservada, sem remoção sem substituição equivalente. |
| CA-H0045-P12-08 | A correção produtiva futura (§24.4) permanece registrada e não é antecipada por esta etapa documental. |
| CA-H0045-P12-09 | Suíte completa exigida verde antes de QA, com os comandos de §24.5. |
| CA-H0045-P12-10 | `VM-H0045-R08-001` permanece aberto; `VM-H0045-R06-001`, `VM-H0045-R07-001`, `QA-H0045-P08-001` e as validações 6/17–17/17 não são reabertos. |
| CA-H0045-P12-11 | O handoff passa em `git diff --check`. |

## 25. Consolidação final do ciclo

Esta seção registra o estado final alcançado depois das autorizações,
implementações, patches, QAs e validações manuais documentados nas seções
anteriores. As declarações intermediárias de pendência permanecem como
registro histórico do estado de cada etapa no momento em que foram escritas;
não representam o estado operacional vigente após esta consolidação.

```yaml
data_da_consolidacao: 2026-08-03
estado_final: IMPLEMENTADO_E_VALIDADO
item:
  id: ITEM-0003
  resultado: CONCLUIDO
implementacao:
  handoff: H-0045
  resultado: CONCLUIDA
qa_tecnico_final:
  status: I5_MANUAL_VALIDATION_REQUIRED
  relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P25.md
  suite_completa: 970_passed
  matriz_dimensional: 60_de_60
validacao_manual:
  status: MANUAL_VALIDATION_APPROVED
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0045.md
  roteiro_base: 6/17..17/17
achados_encerrados:
  VM-H0045-R06-001: APROVADO
  VM-H0045-R07-001: APROVADO
  VM-H0045-R08-001: APROVADO
  QA-H0045-P08-001: TRATADO_POR_CORRECAO_FACTUAL
pendencias_tecnicas: []
pendencias_manuais: []
commit_do_ciclo: NAO_EXECUTADO
proxima_etapa: FECHAMENTO_MANUAL
```

### 25.1 Resultado funcional consolidado

A paginação limitada permanece sem wrap entre a primeira e a última página;
os comandos `,`/`<` e `.`/`>` atuam somente no console focado; páginas,
cursor e seleção são reconciliados por identidade lógica; consoles distintos
mantêm estado de página independente; `Todos`, seleção múltipla, retorno de
foco e fluxo focal permanecem integrados.

As três políticas de quebra foram validadas em telas separadas com conteúdo
fixo. O conjunto vazio permanece em `página 1/1`; páginas somente de
continuação permanecem acessíveis sem cursor; conteúdo verboso e multilinha
não perde, repete nem reordena linhas.

As correções focais posteriores também foram encerradas: o chip de Esc
apresenta `Limpar` quando o primeiro Esc limpa seleção; o conteúdo horizontal
usa a largura útil disponível; e dimensões insuficientes substituem a
interface normal pelo quadro controlado sem traceback, preservando estado e
recuperando automaticamente quando o terminal volta a comportar a tela.

O achado documental `QA-H0045-P08-001` foi tratado pela correção factual do
relatório P08 e não permanece como pendência do ciclo.

### 25.2 Convenção do metadado do handoff

O campo inicial `metadata.status: READY_FOR_IMPLEMENTATION` é preservado como
estado da autorização emitida pelo handoff, seguindo a convenção observada nos
handoffs anteriores do projeto. O estado final de execução e validação é o
registrado nesta seção, nos relatórios finais e no histórico do ITEM-0003.
