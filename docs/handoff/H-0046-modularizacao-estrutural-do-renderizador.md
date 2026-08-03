---
name: H-0046-modularizacao-estrutural-do-renderizador
description: "Handoff 1/3 da ADR-0039 — modularizacao estrutural de tela/renderizador.py para tela/renderizacao/, preservando a fachada publica e o comportamento observavel"
metadata:
  type: handoff
  id: H-0046
  ADR: ADR-0039
  item: ITEM-0022
  sequencia: "1/3"
  status: criado
---

# H-0046 — Modularização estrutural de `tela/renderizador.py`

## 0. Estado transportado (herdado, não reaberto)

```yaml
ADR: ADR-0039 (aceita)
QA_aplicacao_ADR: ADR_APPLICATION_APPROVED_WITH_NOTES (sem bloqueios materiais)
sequencia: 1 de 3 — próximos: modularizacao_de_tela_loader; reorganizacao_dos_testes_do_renderizador
```

Este handoff não reabre ADR-0038 (paginação) nem redefine qualquer contrato. É
estritamente estrutural (D-MOD-02).

---

## 1. Capacidade coesa

Modularizar estruturalmente `tela/renderizador.py` (4547 linhas) em módulos
internos coesos sob `tela/renderizacao/`, preservando `tela/renderizador.py`
como fachada pública compatível que delega a essas implementações, sem
alterar comportamento observável, schema, política, API pública ou resultado
visual.

Este handoff **não** toca `tela/loader.py`, **não** cria `tela/carregamento/`
e **não** reorganiza `tela/teste_renderizador.py` de forma geral — apenas
autoriza os ajustes focais de compatibilidade estritamente necessários,
identificados nominalmente na seção 5.

---

## 2. Diagnóstico estrutural factual

### 2.1 Tamanho e forma atual

`tela/renderizador.py` tem 4547 linhas, ~90 funções de nível superior, 1
classe de exceção (`RenderizadorErro`), e ~15 constantes/estruturas de módulo.
Único import de terceiros do próprio pacote: `copy` (stdlib),
`tela.modelo.ModeloTela`, `tela.distribuicao_matricial.{calcular_distribuicao,
alinhar_na_celula}`. O arquivo não importa `tela.loader`, `tela.paginacao`,
`tela.navegacao`, `tela.selecao` nem `tela.estilo` (este último não existe
como arquivo — não há `tela/estilo.py` no código atual; parâmetros de estilo
chegam ao renderer como objeto `EstiloResolvido` já materializado, passado
por parâmetro).

### 2.2 Responsabilidades concretas encontradas

Levantamento AST (símbolos e intervalos de linha) identificou blocos coesos
distintos, na ordem em que aparecem no arquivo:

1. **Excesso/alinhamento do lançador** — `_split_excesso_lancador` (L94-106).
2. **Primitivas de caixa/borda** — `_borda_de_estilo`, `_linha_topo`,
   `_linha_base`, `_linha_conteudo`, `_caixa`, `_contar_linhas` (L195-293).
3. **Distribuição genérica de área (igual/percentual/fração + maiores
   restos)** — `_pesos_distribuicao`, `_distribuir_alturas`,
   `_distribuir_larguras` (L296-382).
4. **Contexto de navegação/seleção/paginação por console** (leem o estado de
   runtime `_navegacao_atual`) — `_mesmo_console_de_contexto` até
   `_participante_eh_selecionavel` (L390-546), `_item_corrente_de_contexto`,
   `_itens_navegaveis_do_elemento` (L672-700), `_console_tem_paginacao`,
   `_algum_console_paginado_no_corpo`, `_pagina_atual_de_contexto`
   (L2888-2923), `_preparar_contexto_navegacao` (L4053-4112).
5. **Indicador de item corrente (`ec`) e grade de itens** —
   `_aplicar_indicador_linhas`, `_largura_indicador_do_elemento`,
   `largura_util_itens_console`, `_linhas_fisicas_por_item`,
   `_grade_de_itens_para_indicador` (L549-755).
6. **Renderização de itens de `console`** — `_linhas_console` (L758-774),
   `mapa_fisico_de_itens` (L2834-2885), constante pública
   `DESCONTO_ESTRUTURAL_CONSOLE` (L669).
7. **Designadores de conteúdo multinível** — `_romano`, `_alfabetico`,
   `_texto_designador`, `_texto_no_conteudo` (L789-865).
8. **Apresentações de conteúdo externo multinível** (hierarquia, tabela,
   conjuntos de campos) — `_linhas_conteudo_externo`, `_quebrar_texto`,
   `_truncar_com_marcador`, `_linhas_apresentacao_hierarquia`,
   `_linhas_apresentacao_tabela`, `_texto_valor_campo`,
   `_linhas_apresentacao_conjuntos`, `_participantes_de_conteudo_externo`
   (L868-1272).
9. **`dashboard`** — `_linhas_dashboard` (L1275-1290).
10. **`lancador`** — `_itens_lancador_normalizados`, `_chip_sub_w`,
    `_distribuir_excesso_total`, `_linhas_lancador` (L1293-1605).
11. **`barra_de_menus` e chips** (ANSI, distribuição responsiva ADR-0014,
    âncoras, regra de ativo/inativo) — `_avaliar_regra_ativo` até
    `_linhas_barra` (L1608-2490).
12. **Distribuição matricial de participantes dentro de um elemento**
    (ADR-0025) — `_contar_elementos_visuais` até
    `_larguras_mapa_fisico_matricial` (L2493-2831).
13. **Fragmentação de elementos para paginação física** (distinto de
    `tela/paginacao.py`, que faz o planejamento lógico de páginas) —
    `_fragmentos_e_total_paginacao` até `_linhas_distribuicao_matricial`
    (L2926-3368).
14. **Montagem de containers da árvore de composição** (vertical, horizontal,
    matriz, caixa de elemento) — `_caixa_de_elemento` até
    `_montar_corpo_horizontal` (L3371-4023).
15. **Orquestração de topo** — `_quadro_minimo_global` (L4026-4050),
    `_geometria_por_console`, `geometria_console`,
    `altura_interna_disponivel`, `renderizar_tela` (L4115-4547).

### 2.3 Acoplamento crítico: estado de runtime compartilhado

Dois nomes de módulo são mutados e lidos por **quase todos** os grupos acima,
não apenas pelo grupo 4:

- `_navegacao_atual` (dict, L125-152): populado por
  `_preparar_contexto_navegacao` e lido por dezenas de funções em quase
  todos os grupos (contexto de console, indicador, `_linhas_barra`,
  paginação). É mutado por **atribuição de chave** (`_navegacao_atual["x"] =
  ...`), nunca reatribuído inteiro — por isso pode ser importado como objeto
  partilhado por múltiplos módulos internos sem quebrar identidade.
- `_quadro_minimo_lancador_ativo` (bool, L115): mutado via `global` dentro de
  `_linhas_lancador` (L1440-1441) e `_linhas_distribuicao_matricial`
  (L3248-3249), e lido/reiniciado dentro de `renderizar_tela`
  (L4079-4080, L4386-4387, L4544). Diferente do dict, esta é uma
  **reatribuição de nome** — `global` só afeta o módulo onde a instrução
  `global` está escrita. Se `_linhas_lancador` for movida para um módulo
  diferente daquele em que a variável é definida, `global
  _quadro_minimo_lancador_ativo` passa a criar/mutar uma variável **nova**
  nesse outro módulo, quebrando a coordenação entre lançador, paginação
  interna e o quadro mínimo global lido no fim de `renderizar_tela`. Isto é
  tratado explicitamente na arquitetura-alvo (seção 3, nota da fachada
  `contexto_execucao.py`).

### 2.4 Consumidores públicos confirmados (via busca focal)

Busca `rg` por `tela\.renderizador` em `tela/`, `demo/`, `tests/` e
`orquestrador.py` (não há `tests/` neste repositório; não há
`orquestrador.py` na raiz ainda — ausência confirmada, não presumida)
confirma consumidores em `demo/*.py` e `tela/teste_*.py`. Símbolos
efetivamente importados de `tela.renderizador` por código fora do arquivo:

```text
renderizar_tela, RenderizadorErro, DESCONTO_ESTRUTURAL_CONSOLE,
mapa_fisico_de_itens, geometria_console, altura_interna_disponivel,
_largura_sem_ansi, _ANSI_RESET_FG, _codigo_ansi_de_cor, _ljust_sem_ansi,
_linhas_barra, _avaliar_regra_ativo, _texto_chip_barra,
_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT,
_normalizar_distribuicao, _validar_distribuicao, _garantir_esc_primeiro,
_distribuir_alturas, _distribuir_larguras, _pesos_distribuicao,
_linhas_console, _texto_designador, _romano, _alfabetico,
_truncar_com_marcador, _quebrar_texto, _texto_valor_campo,
_montar_corpo_horizontal,
_renderizar_container_horizontal, _larguras_mapa_fisico_matricial,
_participantes_distribuicao_matricial, _largura_indicador_do_elemento,
_renderizar_participante_na_celula, _linhas_distribuicao_matricial,
_linhas_lancador, _preparar_contexto_navegacao, _navegacao_atual (atributo
de módulo mutável, lido diretamente), calcular_distribuicao (reexportado de
tela.distribuicao_matricial, ver §2.5)
```

Consumidores externos concretos: `tela/paginacao.py` (import local, sob
demanda, de `mapa_fisico_de_itens`); `demo/demo.py`, `demo/diagnostico.py`,
`demo/demo_distribuicao.py`, `demo/explorar_barra_de_menus.py`,
`demo/casos_validacao_paginacao.py`; `tela/teste_navegacao.py`,
`tela/teste_paginacao.py`, `tela/teste_renderizador.py`,
`demo/teste_demo*.py`, `demo/teste_diagnostico.py`,
`demo/teste_explorar_barra_de_menus.py`.

### 2.5 Riscos de compatibilidade identificados nominalmente (não hipotéticos)

Estes três riscos foram confirmados lendo o texto real dos testes — não são
especulação — e devem ser tratados no manifesto de implementação (seção 5):

**(a) Testes de inspeção whitebox do texto-fonte do arquivo.** Três funções de
`tela/teste_renderizador.py` leem `tela/renderizador.py` como texto puro
(`Path(...).read_text()`) e verificam presença/ausência de substrings
literais:

- `teste_proibicoes_importacao` (define-se em L704): a maioria das
  asserções é de **ausência** (`"import json" not in texto_mod`, etc.) e
  permanece válida trivialmente após a modularização, pois a fachada não
  ganhará esses imports. Porém a asserção **de presença**
  `"_campos_inertes" in texto_mod` (L742) vai falhar, pois o acesso a
  `elemento._campos_inertes` está espalhado pelas funções que serão
  extraídas, não na fachada.
- `teste_inspecao_fonte_hardcoded` (L746): asserções de presença
  `"_campos_inertes" in texto_mod` (L796) e `"barra_de_menus" in texto_mod`
  (L800) — mesma causa; `"barra_de_menus"` como string literal só aparece
  hoje dentro de `_linhas_barra` e `_normalizar_distribuicao`, ambas movidas
  para `tela/renderizacao/barra_menus.py`.
- `teste_alternancia_borda` (L848): asserções de presença
  `"estilo.cor_texto" in texto_mod` (L1093) e `"estilo.cor_fundo" in
  texto_mod` (L1097) — o acesso literal a esses atributos ocorre hoje só
  dentro de `_texto_chip_barra` (L1784-1785), que move para
  `tela/renderizacao/barra_menus.py`.

**(b) Testes que fazem monkeypatch de nomes privados via o módulo
`tela.renderizador`, esperando que a chamada interna enxergue o patch.**
Python resolve nomes globais no namespace do módulo onde a função **chamadora**
está definida — não no namespace de onde o símbolo foi originalmente
importado. Se chamador e chamado migrarem juntos para o mesmo módulo interno,
um patch aplicado em `tela.renderizador.<nome>` deixa de alcançar a chamada
interna:

- `TestDistribuicaoMatricialH0035.test_minimo_fixo_nao_cresce` (classe em
  L10003, método em L10277): faz
  `_mod._renderizar_participante_na_celula = _espiao` (L10298) sobre
  `import tela.renderizador as _mod`, espera que a chamada feita de dentro de
  `_renderizar_participante_com_indicador` (chamador, mesmo arquivo hoje)
  invoque o espião.
- `test_h0045_ph07_coerencia_renderer_mapa_fisico` (def em L13282): faz
  `_rend.calcular_distribuicao = _espiao` (L13343) sobre
  `import tela.renderizador as _rend` — `calcular_distribuicao` é hoje
  importado em `tela/renderizador.py` de `tela.distribuicao_matricial`
  (L74) e chamado de dentro de `_larguras_mapa_fisico_matricial`.

Após a extração, chamador e chamado (`_renderizar_participante_com_indicador`
+ `_renderizar_participante_na_celula`; `_larguras_mapa_fisico_matricial` +
`calcular_distribuicao`) permanecem **juntos** no mesmo módulo interno
(`tela/renderizacao/matriz_participantes.py`, seção 3), então o patch
aplicado em `tela.renderizador.<nome>` (fachada) não alcança mais a chamada
interna, que resolve o nome no namespace de
`tela.renderizacao.matriz_participantes`. É um ajuste **focal e nominal** de
teste (retargetar o `patch`/atribuição para o módulo interno), não uma
reorganização geral da suíte — autorizado no manifesto (seção 5).

**(c) Caso já compatível, registrado para não ser reaberto por engano.**
`unittest.mock.patch("tela.renderizador.mapa_fisico_de_itens")` é usado em
`demo/teste_demo_paginacao.py` (L2695 e seguintes) e funciona porque (i)
`mapa_fisico_de_itens` é consumido de fora do pacote `tela.renderizacao` via
`tela.paginacao._mapa`, que faz `from tela.renderizador import
mapa_fisico_de_itens` **dentro da função**, a cada chamada — resolvendo
sempre o atributo corrente da fachada — e (ii) a fachada continuará
reexportando `mapa_fisico_de_itens`. Nenhum ajuste é necessário aqui.

### 2.6 Pontos que não podem ser extraídos isoladamente

- `_navegacao_atual` e `_quadro_minimo_lancador_ativo` (seção 2.3) precisam
  de um único módulo interno proprietário; qualquer outro módulo que precise
  alterar `_quadro_minimo_lancador_ativo` deve fazê-lo por meio de uma função
  de acesso desse módulo proprietário, nunca por `global` local (ver §3).
- `RenderizadorErro` é levantada em 52 pontos espalhados por quase todos os
  grupos — precisa de um módulo próprio, sem dependências, importável por
  todos os demais sem risco de ciclo.
- `_borda_de_estilo` e `_contar_linhas` são usados tanto pela montagem de
  containers quanto pela orquestração de topo (`geometria_console`,
  `renderizar_tela`) — pertencem a um módulo de geometria de baixo nível
  comum a ambos.
- `_codigo_ansi_de_cor`, `_largura_sem_ansi`, `_cortar_sem_ansi` e
  `_ljust_sem_ansi` são usados tanto pela geometria de caixa (`_linha_conteudo`,
  hoje L251-252) quanto pela barra de menus (`_texto_chip_barra`,
  `_montar_coluna_a_coluna`, `_linhas_barra`) — pertencem a um módulo comum de
  baixo nível (`texto_ansi.py`), sem dependência de nenhum dos dois
  consumidores, evitando o acoplamento cruzado entre eles.

Nenhum ciclo de importação é introduzido por essas dependências: o desenho da
seção 3 mantém direção única (baixo nível → alto nível), com
`tela/renderizacao/tela.py` como único módulo que importa de praticamente
todos os demais, sem que nenhum deles importe de volta `tela.py` nem a
fachada `tela/renderizador.py`.

---

## 3. Arquitetura-alvo nominal

### 3.1 Novos arquivos em `tela/renderizacao/`

```text
tela/renderizacao/__init__.py
tela/renderizacao/erros.py
tela/renderizacao/contexto_execucao.py
tela/renderizacao/texto_ansi.py
tela/renderizacao/geometria_caixa.py
tela/renderizacao/designadores.py
tela/renderizacao/conteudo_externo.py
tela/renderizacao/dashboard.py
tela/renderizacao/lancador.py
tela/renderizacao/barra_menus.py
tela/renderizacao/matriz_participantes.py
tela/renderizacao/console.py
tela/renderizacao/paginacao_interna.py
tela/renderizacao/composicao_corpo.py
tela/renderizacao/tela.py
```

`tela/renderizacao/__init__.py` fica vazio (apenas marca o pacote) — nenhuma
lógica nem reexportação nele; a reexportação pública vive exclusivamente em
`tela/renderizador.py` (D-MOD-04).

### 3.2 Responsabilidade e símbolos de cada módulo

**`erros.py`** — exceção do domínio, sem dependências internas.
- `RenderizadorErro` (classe, hoje L80-81).

**`contexto_execucao.py`** — estado de runtime do render corrente e as
funções que o consultam para resolver console/foco/seleção/página. Único
lugar autorizado a definir e mutar `_navegacao_atual` e
`_quadro_minimo_lancador_ativo`. Também autoridade única de
`DESCONTO_ESTRUTURAL_CONSOLE` (ver nota de ciclo em `console.py`, abaixo).
- Estado: `_navegacao_atual` (hoje L125-152), `_quadro_minimo_lancador_ativo`
  (hoje L115).
- Constante: `DESCONTO_ESTRUTURAL_CONSOLE` (hoje L669) — relocada para este
  módulo (releitura focal: nenhuma função de `console.py` a consome
  diretamente; os consumidores reais são `matriz_participantes.py` (L652,
  L754), `barra_menus.py` (L2268, L2281), `paginacao_interna.py` (L2930,
  L2936, L2955, L2958) e `composicao_corpo.py` (L3455) — todos já
  dependentes de `contexto_execucao.py` ou aptos a depender dele sem criar
  ciclo; ver §3.3).
- Funções de acesso ao estado (adicionadas apenas como reformulação mecânica
  do `global` cross-módulo, sem alterar comportamento observável):
  `_ativar_quadro_minimo_lancador()`, `_quadro_minimo_lancador_esta_ativo()`,
  `_reiniciar_quadro_minimo_lancador()`.
  - `_ativar_quadro_minimo_lancador()` substitui `global
    _quadro_minimo_lancador_ativo; ... = True` em `lancador.py` (hoje
    L1440-1441) e `paginacao_interna.py` (hoje L3248-3249).
  - `_quadro_minimo_lancador_esta_ativo()` substitui a leitura direta em
    `tela.py` (hoje L4544, dentro de `renderizar_tela`).
  - `_reiniciar_quadro_minimo_lancador()` substitui `global
    _quadro_minimo_lancador_ativo; ... = False` em `tela.py` (hoje
    L4386-4387, dentro de `renderizar_tela`). O outro ponto de reset (hoje
    L4079-4080, dentro de `_preparar_contexto_navegacao`) permanece
    atribuição direta: essa função já pertence a `contexto_execucao.py`,
    portanto não há `global` cross-módulo a reformular ali. Nenhuma
    temporalidade ou precedência de reset é alterada — apenas o mecanismo de
    acesso ao nome cross-módulo.
- Funções de contexto (hoje L390-546, L672-700, L2888-2923, L4053-4112):
  `_mesmo_console_de_contexto`, `_console_focalizavel_de_contexto`,
  `_console_focado_de_contexto`, `_console_original_de_contexto`,
  `_console_declarou_selecao_multipla`, `_selecao_do_console_de_contexto`,
  `_ids_selecionaveis_do_elemento`, `_participante_eh_selecionavel`,
  `_item_corrente_de_contexto`, `_itens_navegaveis_do_elemento`,
  `_console_tem_paginacao`, `_algum_console_paginado_no_corpo`,
  `_pagina_atual_de_contexto`, `_preparar_contexto_navegacao`.
- Sem dependência de outro módulo interno.

**`texto_ansi.py`** — primitivas transversais e de baixo nível para largura
física, corte, preenchimento e códigos ANSI, sem dependência dos componentes
de barra, geometria ou composição.
- Constantes: `_ANSI_POR_NOME_SEMANTICO` (hoje L1670-1676), `_ANSI_RESET_FG`
  (hoje L1677).
- Funções (hoje L1680-1754): `_codigo_ansi_de_cor`, `_largura_sem_ansi`,
  `_cortar_sem_ansi`, `_ljust_sem_ansi`.
- Sem dependência de outro módulo interno de `tela/renderizacao/`; não pode
  importar `geometria_caixa.py` nem `barra_menus.py` (são consumidores, não
  dependências — a direção esperada é `texto_ansi.py → geometria_caixa.py` e
  `texto_ansi.py → barra_menus.py`, nunca o inverso).

**`geometria_caixa.py`** — primitivas físicas de caixa/borda e distribuição
genérica de área entre filhos diretos de um container (algoritmo de maiores
restos, ADR-0015).
- Constantes: `TOTAL_WIDTH`, `INNER_WIDTH`, `CONTENT_WIDTH`, `_LABEL_MAX`
  (hoje L84-87), `_PLACEHOLDER_CONSOLE` (L89), `_LABEL_BARRA` (L90).
- Funções (hoje L195-382): `_borda_de_estilo`, `_linha_topo`, `_linha_base`,
  `_linha_conteudo`, `_caixa`, `_contar_linhas`, `_pesos_distribuicao`,
  `_distribuir_alturas`, `_distribuir_larguras`.
- Depende de: `erros.py` (`RenderizadorErro` levantado em
  `_distribuir_alturas`/`_distribuir_larguras`, hoje L335 e L370);
  `texto_ansi.py` (`_cortar_sem_ansi` e `_ljust_sem_ansi`, consumidas em
  `_linha_conteudo`, hoje L251-252 — releitura focal confirmou que esta
  dependência já existia e não estava registrada nominalmente).

**`designadores.py`** — numeração/rotulagem de nós de conteúdo multinível
(romano, alfabético, designador composto).
- Constante: `_ROMANOS` (hoje L782-786).
- Funções (hoje L789-865): `_romano`, `_alfabetico`, `_texto_designador`,
  `_texto_no_conteudo`.
- Sem dependência de outro módulo interno.

**`conteudo_externo.py`** — apresentações de conteúdo multinível externo
(hierarquia, tabela, conjuntos de campos), truncamento e quebra de texto
associados a essas apresentações.
- Constante: `_VALOR_CAMPO_AUSENTE_TEXTO` (hoje L1139).
- Funções (hoje L868-1272): `_linhas_conteudo_externo`, `_quebrar_texto`,
  `_truncar_com_marcador`, `_linhas_apresentacao_hierarquia`,
  `_linhas_apresentacao_tabela`, `_texto_valor_campo`,
  `_linhas_apresentacao_conjuntos`, `_participantes_de_conteudo_externo`.
- Depende de: `designadores.py`, `erros.py` (`RenderizadorErro` levantado em
  `_linhas_conteudo_externo`, hoje L883).

**`dashboard.py`** — renderização do elemento `dashboard`.
- Função (hoje L1275-1290): `_linhas_dashboard`.
- Sem dependência de outro módulo interno.

**`lancador.py`** — renderização do elemento `lancador` (fila/matriz
automáticos, excesso, vãos).
- Funções (hoje L94-106, L1293-1605): `_split_excesso_lancador`,
  `_itens_lancador_normalizados`, `_chip_sub_w`, `_distribuir_excesso_total`,
  `_linhas_lancador`.
- Depende de: `contexto_execucao.py` (chama `_ativar_quadro_minimo_lancador()`
  no ponto que hoje é `global _quadro_minimo_lancador_ativo; ... = True`,
  L1440-1441), `erros.py` (`RenderizadorErro` levantado hoje em L1308, L1382
  e L1407).

**`barra_menus.py`** — chips, ANSI, distribuição horizontal responsiva
(ADR-0014), âncoras, regra de ativo/inativo.
- Constantes: `_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT` (hoje L158-190),
  `_PREENCHIMENTOS_MULTILINHA_VALIDOS` (L192).
- Funções (hoje L1608-1670, L1755-2490): `_avaliar_regra_ativo`,
  `_texto_chip_barra`, `_normalizar_distribuicao`, `_eh_int_nao_bool`,
  `_validar_distribuicao`, `_validar_ancoras`, `_montar_coluna_a_coluna`,
  `_montar_linha_a_linha`, `_garantir_esc_primeiro`, `_linhas_barra`.
- Depende de: `texto_ansi.py` (`_codigo_ansi_de_cor` e `_ANSI_RESET_FG`,
  consumidas em `_texto_chip_barra`, hoje L1799, L1802, L1804 e L1807;
  `_largura_sem_ansi`, consumida em `_montar_coluna_a_coluna` e
  `_linhas_barra`, hoje L2104, L2462 e L2479; `_ljust_sem_ansi`, consumida em
  `_montar_coluna_a_coluna`, hoje L2111 — releitura focal confirmou que esta
  dependência já existia e não estava registrada nominalmente),
  `contexto_execucao.py` (leitura de `_navegacao_atual` para estado de
  destaque/ativo dos chips, hoje L2217-2439, chama `_console_tem_paginacao`
  hoje L2258, e consome `DESCONTO_ESTRUTURAL_CONSOLE`, hoje L2268 e L2281),
  `erros.py` (`RenderizadorErro` levantado em múltiplos pontos de validação
  de distribuição, hoje L1826-L2483). Importa localmente, sob demanda
  (dentro de `_linhas_barra`): `tela.paginacao` (externo, hoje L2259),
  `tela.selecao` (externo, hoje L2308 e L2379), `tela.navegacao` (externo,
  hoje L2309).

**`matriz_participantes.py`** — distribuição matricial de participantes
dentro de um elemento (ADR-0025), indicador de item corrente (`ec`) e grade
física de itens do console.
- Funções (hoje L549-662, L703-755, L2493-2831): `_aplicar_indicador_linhas`,
  `_largura_indicador_do_elemento`, `largura_util_itens_console`,
  `_linhas_fisicas_por_item`, `_grade_de_itens_para_indicador`,
  `_contar_elementos_visuais`, `_participantes_distribuicao_matricial`,
  `_renderizar_participante_na_celula`, `_renderizar_participante_com_indicador`,
  `_altura_quebra_item`, `_item_console_e_navegavel`, `_politica_quebra_item`,
  `_itens_visiveis_console`, `_larguras_mapa_fisico_matricial`.
- Depende de: `contexto_execucao.py` (inclui `DESCONTO_ESTRUTURAL_CONSOLE`,
  hoje L652 e L754), `conteudo_externo.py` (`_quebrar_texto`, chamada em
  `_renderizar_participante_na_celula` e `_altura_quebra_item`, hoje L2649 e
  L2690; `_participantes_de_conteudo_externo`, chamada em
  `_participantes_distribuicao_matricial`, hoje L2566 — releitura focal
  confirmou esta segunda dependência, antes não registrada nominalmente),
  `tela.distribuicao_matricial` (externo ao pacote `renderizacao`,
  já existente — `calcular_distribuicao`, `alinhar_na_celula`, reexportados
  aqui para que a fachada os repasse), `tela.navegacao` (externo, import
  local sob demanda, hoje L615-618, L660 e L752).

**`console.py`** — geração de linhas de itens de `console` e mapa físico de
itens (autoridade pública consumida por `tela/paginacao.py`).
- Funções (hoje L758-774, L2834-2885): `_linhas_console`,
  `mapa_fisico_de_itens`.
- Depende de: `matriz_participantes.py`, `conteudo_externo.py`,
  `contexto_execucao.py`. Não consome `DESCONTO_ESTRUTURAL_CONSOLE`
  diretamente (releitura focal: nenhuma ocorrência dentro de L758-774 ou
  L2834-2885) — a constante é definida e reexportada por
  `contexto_execucao.py` (ver acima), não por este módulo, justamente para
  evitar o ciclo `console.py ↔ matriz_participantes.py` que existiria se
  `matriz_participantes.py` precisasse importar a constante de volta de
  `console.py` (que já depende de `matriz_participantes.py`).

**`paginacao_interna.py`** — fragmentação física de elementos para paginação
dentro da área alocada (distinto de `tela/paginacao.py`, que planeja páginas
lógicas e importa `mapa_fisico_de_itens` da fachada sob demanda).
- Funções (hoje L2926-3368): `_fragmentos_e_total_paginacao`,
  `_recortar_linhas_paginadas`, `_texto_base_paginacao`,
  `_linhas_texto_item_para_pagina`, `_elemento_fragmentado_para_pagina`,
  `_linhas_distribuicao_matricial`.
- Depende de: `console.py`, `matriz_participantes.py`,
  `contexto_execucao.py` (chama `_ativar_quadro_minimo_lancador()` no ponto
  que hoje é `global _quadro_minimo_lancador_ativo; ... = True`, L3248-3249,
  consome `DESCONTO_ESTRUTURAL_CONSOLE`, hoje L2930, L2936, L2955 e L2958, e
  chama `_console_tem_paginacao`, hoje L2975), `conteudo_externo.py`
  (`_quebrar_texto`, chamada em `_linhas_texto_item_para_pagina`, hoje
  L2992). Importa localmente, sob demanda: `tela.paginacao` (externo, dentro
  de `_fragmentos_e_total_paginacao`, hoje L2927 — mesmo padrão de import
  tardio já usado por `tela/paginacao.py` para importar a fachada (§2.5(c)),
  sem ciclo de carregamento); `tela.navegacao` (externo, dentro de
  `_linhas_distribuicao_matricial`, hoje L3307 —
  `LARGURA_INDICADOR_COLUNA`/`LARGURA_INDICADOR_INCLUSAO` — releitura focal
  confirmou esta dependência, antes não registrada nominalmente).

**`composicao_corpo.py`** — montagem da árvore de composição do corpo
(containers vertical/horizontal/matriz, caixa de elemento, corpo horizontal
completo).
- Funções (hoje L3371-4023): `_caixa_de_elemento`,
  `_renderizar_container_vertical`, `_renderizar_container_horizontal`,
  `_renderizar_container_matriz`, `_renderizar_container`,
  `_montar_corpo_horizontal`.
- Depende de: `geometria_caixa.py`, `console.py`, `dashboard.py`,
  `lancador.py`, `paginacao_interna.py`, `matriz_participantes.py` (para
  `largura_util_itens_console`, hoje usada em L3456), `contexto_execucao.py`
  (`DESCONTO_ESTRUTURAL_CONSOLE`, hoje L3455, e `_console_tem_paginacao`,
  hoje L3434 e L3463), `erros.py` (`RenderizadorErro` levantado em múltiplos
  pontos, hoje L3605-L3957).

**`tela.py`** — orquestração de topo: geometria pública por console, quadro
mínimo global, ponto de entrada `renderizar_tela`.
- Funções (hoje L4026-4050, L4115-4547): `_quadro_minimo_global`,
  `_geometria_por_console`, `geometria_console`, `altura_interna_disponivel`,
  `renderizar_tela`.
- Depende de: `erros.py`, `contexto_execucao.py`, `geometria_caixa.py`,
  `composicao_corpo.py`, `barra_menus.py`, `tela.modelo` (externo — tipo
  `ModeloTela` na assinatura de `renderizar_tela`/`_geometria_por_console`).

### 3.3 Direção de dependências (acíclica)

A ordem abaixo é uma ordem topológica válida: cada módulo depende apenas de
módulos listados ANTES dele. `contexto_execucao.py` concentra as
dependências transversais (estado de runtime e a constante
`DESCONTO_ESTRUTURAL_CONSOLE`) justamente por ser base — isso é o que
resolve o ciclo potencial `console.py ↔ matriz_participantes.py` descrito em
`console.py` (§3.2): a constante não é mais propriedade de um módulo que
`matriz_participantes.py` precisaria importar de volta. Da mesma forma,
`texto_ansi.py` concentra as primitivas ANSI de baixo nível (largura física,
corte, preenchimento, código de cor) justamente por ser base — isso resolve
o acoplamento que existiria se `geometria_caixa.py` precisasse depender de
`barra_menus.py` (ou vice-versa) apenas para reaproveitar essas primitivas:
nenhum dos dois é mais propriedade delas, e `texto_ansi.py` não importa
nenhum dos dois consumidores de volta.

```text
erros.py                (base, sem deps)
designadores.py         (base, sem deps)
contexto_execucao.py    (base, sem deps de outro módulo interno)
texto_ansi.py           (base, sem deps de outro módulo interno; não importa
                          geometria_caixa.py nem barra_menus.py)
        │
        ▼
geometria_caixa.py      ← erros.py, texto_ansi.py
        │
        ▼
conteudo_externo.py     ← designadores.py, erros.py
dashboard.py            (sem deps)
lancador.py             ← contexto_execucao.py, erros.py
barra_menus.py          ← texto_ansi.py, contexto_execucao.py, erros.py,
                          tela.paginacao (externo), tela.selecao (externo),
                          tela.navegacao (externo)
matriz_participantes.py ← contexto_execucao.py, conteudo_externo.py,
                          tela.distribuicao_matricial (externo),
                          tela.navegacao (externo)
        │
        ▼
console.py              ← matriz_participantes.py, conteudo_externo.py,
                          contexto_execucao.py
        │
        ▼
paginacao_interna.py    ← console.py, matriz_participantes.py,
                          contexto_execucao.py, conteudo_externo.py,
                          tela.paginacao (externo, import tardio — §2.5(c)),
                          tela.navegacao (externo, import tardio)
        │
        ▼
composicao_corpo.py     ← geometria_caixa.py, console.py, dashboard.py,
                          lancador.py, paginacao_interna.py,
                          matriz_participantes.py, contexto_execucao.py,
                          erros.py
        │
        ▼
tela.py                 ← erros.py, contexto_execucao.py, geometria_caixa.py,
                          composicao_corpo.py, barra_menus.py,
                          tela.modelo (externo)
```

Dependências externas ao subpacote `tela/renderizacao/` (todas em módulos já
existentes fora do escopo deste handoff, nenhuma delas importa de volta
`tela.renderizacao.*` nem `tela.renderizador`): `tela.distribuicao_matricial`
(carregamento normal, topo de `matriz_participantes.py`); `tela.navegacao`
(import local sob demanda em `matriz_participantes.py`, `barra_menus.py` e
`paginacao_interna.py` — este último confirmado na releitura focal, dentro
de `_linhas_distribuicao_matricial`, hoje L3307); `tela.selecao` (import
local sob demanda em `barra_menus.py`);
`tela.paginacao` (import local sob demanda em `barra_menus.py` e
`paginacao_interna.py` — o mesmo módulo `tela/paginacao.py` já importa a
fachada de volta de forma tardia, dentro de função, conforme §2.5(c); isso
não cria ciclo de carregamento porque nenhuma das duas pontas resolve o
import no momento em que o módulo é carregado, apenas quando a função é
chamada); `tela.modelo` (carregamento normal, topo de `tela.py`, para o tipo
`ModeloTela` usado na assinatura pública).

Ausência de ciclos: a lista acima é uma ordem topológica (cada seta aponta
de um módulo para outro módulo listado estritamente antes dele nesta lista,
ou para um módulo externo ao subpacote); não há aresta de volta de nenhum
módulo mais alto (`tela.py`, `composicao_corpo.py`, `paginacao_interna.py`,
`console.py`) para um módulo mais baixo que dependa dele, e nenhum módulo
interno importa `tela.renderizador` (a fachada) — condição obrigatória de
D-MOD-08 item 9.

### 3.4 Conteúdo que permanece em `tela/renderizador.py` (fachada)

Apenas: docstring de módulo (adaptada para descrever a fachada e apontar para
`tela/renderizacao/`); imports de reexportação dos módulos internos listados
acima; no máximo atribuições simples de alias necessárias à reexportação
(ex.: `renderizar_tela = tela.renderizar_tela` quando o import direto não
bastar); `__all__`, quando usado, apenas como lista literal nominal de
exportações. Nenhum caso desta análise exige um wrapper de função: todos os
símbolos públicos consumidos (§3.5) mapeiam diretamente para um símbolo
interno de mesmo nome, importável por `from tela.renderizacao.<modulo>
import <nome>`. A prova normativa (§7, comando 6) exige **zero funções, zero
funções assíncronas, zero lambdas e zero classes definidas na fachada, em
qualquer profundidade** — nenhuma alternativa permissiva de wrapper é
admitida nesta versão do handoff. Se a implementação, durante a extração,
encontrar um caso concreto em que a assinatura pública não possa ser
preservada por reexportação direta ou por alias simples, deve **parar antes
de criar o wrapper** e solicitar a exceção operacional focal (§11),
incluindo pedido de patch documental deste handoff antes de prosseguir — a
necessidade de wrapper não pode ser resolvida unilateralmente pela
implementação.

### 3.5 Pontos reexportados pela fachada (lista nominal completa)

```text
RenderizadorErro                                 ← erros
_navegacao_atual                                 ← contexto_execucao
_preparar_contexto_navegacao                     ← contexto_execucao
_distribuir_alturas                              ← geometria_caixa
_distribuir_larguras                             ← geometria_caixa
_pesos_distribuicao                              ← geometria_caixa
_texto_designador                                ← designadores
_romano                                          ← designadores
_alfabetico                                      ← designadores
_truncar_com_marcador                            ← conteudo_externo
_quebrar_texto                                   ← conteudo_externo
_texto_valor_campo                               ← conteudo_externo
_linhas_lancador                                 ← lancador
_linhas_barra                                    ← barra_menus
_avaliar_regra_ativo                             ← barra_menus
_texto_chip_barra                                ← barra_menus
_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT      ← barra_menus
_normalizar_distribuicao                         ← barra_menus
_validar_distribuicao                            ← barra_menus
_garantir_esc_primeiro                           ← barra_menus
_largura_sem_ansi                                ← texto_ansi
_ANSI_RESET_FG                                   ← texto_ansi
_codigo_ansi_de_cor                              ← texto_ansi
_ljust_sem_ansi                                  ← texto_ansi
_larguras_mapa_fisico_matricial                  ← matriz_participantes
_participantes_distribuicao_matricial            ← matriz_participantes
_largura_indicador_do_elemento                   ← matriz_participantes
_renderizar_participante_na_celula               ← matriz_participantes
calcular_distribuicao                            ← matriz_participantes (reexportado de tela.distribuicao_matricial)
DESCONTO_ESTRUTURAL_CONSOLE                      ← contexto_execucao
_linhas_console                                  ← console
mapa_fisico_de_itens                             ← console
_linhas_distribuicao_matricial                   ← paginacao_interna
_montar_corpo_horizontal                         ← composicao_corpo
_renderizar_container_horizontal                 ← composicao_corpo
geometria_console                                ← tela
altura_interna_disponivel                        ← tela
renderizar_tela                                  ← tela
```

Todo símbolo interno não listado acima permanece acessível apenas via seu
módulo interno (`tela.renderizacao.<modulo>.<simbolo>`) e **não** é
reexportado pela fachada, salvo se a implementação encontrar, durante a
extração, outro consumidor externo real não capturado nesta busca — nesse
caso, o símbolo adicional deve ser reexportado e registrado no relatório de
implementação (seção 9), não descartado silenciosamente.

---

## 4. Manifesto da implementação

### 4.1 Arquivos autorizados para criação

```text
tela/renderizacao/__init__.py
tela/renderizacao/erros.py
tela/renderizacao/contexto_execucao.py
tela/renderizacao/texto_ansi.py
tela/renderizacao/geometria_caixa.py
tela/renderizacao/designadores.py
tela/renderizacao/conteudo_externo.py
tela/renderizacao/dashboard.py
tela/renderizacao/lancador.py
tela/renderizacao/barra_menus.py
tela/renderizacao/matriz_participantes.py
tela/renderizacao/console.py
tela/renderizacao/paginacao_interna.py
tela/renderizacao/composicao_corpo.py
tela/renderizacao/tela.py
docs/relatorios/IMP-0046-modularizacao-estrutural-do-renderizador.md
```

### 4.2 Arquivos autorizados para alteração

```text
tela/renderizador.py
```

### 4.3 Arquivos de teste autorizados para ajuste focal

```text
tela/teste_renderizador.py
```

Ajustes autorizados **exclusivamente** nas três funções e nos dois métodos
identificados na seção 2.5(a)-(b):

- `teste_proibicoes_importacao` (asserção da L742: `"_campos_inertes" in
  texto_mod`);
- `teste_inspecao_fonte_hardcoded` (asserções das L796 e L800);
- `teste_alternancia_borda` (asserções das L1093 e L1097);
- `TestDistribuicaoMatricialH0035.test_minimo_fixo_nao_cresce` (monkeypatch da
  L10298 e restauração da L10357);
- `test_h0045_ph07_coerencia_renderer_mapa_fisico` (monkeypatch da L13343 e
  restauração da L13361).

Nenhum outro teste, fixture, caso, docstring ou asserção de
`tela/teste_renderizador.py` pode ser alterado. Nenhuma reordenação, divisão
em arquivos ou renumeração é permitida.

### 4.4 Arquivos preservados (leitura apenas, sem alteração)

```text
tela/paginacao.py
tela/teste_paginacao.py
tela/loader.py
tela/modelo.py
tela/navegacao.py
tela/selecao.py
tela/distribuicao_matricial.py
demo/demo.py
demo/casos_validacao_paginacao.py
demo/diagnostico.py
demo/demo_distribuicao.py
demo/explorar_barra_de_menus.py
tela/teste_navegacao.py
demo/teste_demo*.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
```

### 4.5 Relatório de implementação

```text
docs/relatorios/IMP-0046-modularizacao-estrutural-do-renderizador.md
```

---

## 5. Compatibilidade pública

### 5.1 Método reproduzível — imports públicos e consumidores existentes

```zsh
# Nenhum consumidor externo foi migrado para tela.renderizacao.*
# A exclusao cobre a fachada E todo o subpacote interno (tela/renderizacao/),
# cujos imports internos entre modulos sao esperados e nao contam como
# consumo externo.
rg -n 'from tela\.renderizacao|import tela\.renderizacao' tela demo \
  | grep -v '^tela/renderizador.py:' \
  | grep -v '^tela/renderizacao/'
# saída esperada: vazia
```

```zsh
# Todos os símbolos hoje importados de tela.renderizador continuam
# resolvendo, com o mesmo comportamento, através da fachada.
python3 - <<'PY'
import tela.renderizador as f
nomes = [
    "renderizar_tela", "RenderizadorErro", "DESCONTO_ESTRUTURAL_CONSOLE",
    "mapa_fisico_de_itens", "geometria_console", "altura_interna_disponivel",
    "_largura_sem_ansi", "_ANSI_RESET_FG", "_codigo_ansi_de_cor",
    "_ljust_sem_ansi", "_linhas_barra", "_avaliar_regra_ativo",
    "_texto_chip_barra",
    "_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT", "_normalizar_distribuicao",
    "_validar_distribuicao", "_garantir_esc_primeiro", "_distribuir_alturas",
    "_distribuir_larguras", "_pesos_distribuicao", "_linhas_console",
    "_texto_designador", "_romano", "_alfabetico", "_truncar_com_marcador",
    "_quebrar_texto", "_texto_valor_campo",
    "_montar_corpo_horizontal", "_renderizar_container_horizontal",
    "_larguras_mapa_fisico_matricial", "_participantes_distribuicao_matricial",
    "_largura_indicador_do_elemento", "_renderizar_participante_na_celula",
    "_linhas_distribuicao_matricial", "_linhas_lancador",
    "_preparar_contexto_navegacao", "_navegacao_atual",
    "calcular_distribuicao",
]
faltando = [n for n in nomes if not hasattr(f, n)]
assert not faltando, faltando
print("OK: todos os", len(nomes), "simbolos publicos preservados")
PY
```

```zsh
# hasattr negativos que ja eram verdadeiros continuam verdadeiros
python3 -c "
import tela.renderizador as f
assert not hasattr(f, '_BORDAS')
assert not hasattr(f, '_TEXTO_ITEM_MAX')
print('OK')
"
```

### 5.2 Ausência de importação inversa

```zsh
rg -n 'from tela\.renderizador import|import tela\.renderizador' \
  tela/renderizacao
# saída esperada: vazia
```

### 5.3 Identidade do estado de runtime mutável

```zsh
python3 -c "
import tela.renderizador as f
import tela.renderizacao.contexto_execucao as ctx
assert f._navegacao_atual is ctx._navegacao_atual
print('OK: mesma identidade de objeto')
"
```

### 5.4 Monkeypatches focais retargetados (equivalência funcional)

Após o ajuste focal da seção 4.3, os dois testes que hoje fazem
`import tela.renderizador as _mod; _mod.<nome> = espiao` devem monkeypatchar
`tela.renderizacao.matriz_participantes.<nome>` (o módulo onde chamador e
chamado passam a coexistir) e continuar produzindo os mesmos resultados de
asserção que produziam antes da extração — comprovado pela execução da
suíte completa (seção 6).

---

## 6. Equivalência comportamental — testes focais e suíte completa

Comandos nominais, executados nesta ordem:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_resultado_execucao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_console.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_console_modos.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_navegacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_paginacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_selecao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_diagnostico.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_explorar_barra_de_menus.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

A suíte canônica completa (`python -m pytest`, sem filtro) é condição
necessária, mas não suficiente (D-MOD-08) — os critérios de aceite da
seção 10 e as verificações estruturais da seção 7 também devem ser
satisfeitos.

---

## 7. Integridade estrutural

```zsh
# 1. Importação de todos os módulos internos, isoladamente
python3 -c "
import importlib
for m in [
    'tela.renderizacao.erros', 'tela.renderizacao.contexto_execucao',
    'tela.renderizacao.texto_ansi',
    'tela.renderizacao.geometria_caixa', 'tela.renderizacao.designadores',
    'tela.renderizacao.conteudo_externo', 'tela.renderizacao.dashboard',
    'tela.renderizacao.lancador', 'tela.renderizacao.barra_menus',
    'tela.renderizacao.matriz_participantes', 'tela.renderizacao.console',
    'tela.renderizacao.paginacao_interna', 'tela.renderizacao.composicao_corpo',
    'tela.renderizacao.tela',
]:
    importlib.import_module(m)
print('OK: todos os modulos internos importam isoladamente')
"
```

```zsh
# 2. Ausencia de ciclos de importacao (checagem estatica por grafo)
#
# Politica adotada (§3.1): imports relativos (level > 0) dentro de
# tela/renderizacao/ sao PROIBIDOS. A forma `from tela.renderizacao import
# <modulo>` TAMBEM E PROIBIDA — o no ImportFrom resultante tem
# `module == "tela.renderizacao"` (o pacote, nao o submodulo efetivamente
# consumido), o que ocultaria a aresta real do grafo e permitiria que um
# ciclo escapasse da deteccao. Toda dependencia interna entre modulos do
# subpacote usa uma das duas formas abaixo, absolutas e nominais, ambas
# normalizadas para o mesmo no de grafo "tela.renderizacao.<modulo>":
#
#   import tela.renderizacao.<modulo>
#   from tela.renderizacao.<modulo> import <simbolo>
#
# A prova roda verificacoes SINTETICAS primeiro (comprovando que o proprio
# analisador rejeita as formas proibidas e aceita/normaliza as formas
# autorizadas), e so entao analisa o pacote real.
python3 - <<'PY'
import ast, pathlib, sys

PREFIXO = "tela.renderizacao"


def analisar_arquivo(src, origem="<sintetico>"):
    """Devolve (deps_internas, violacoes) para o codigo-fonte de um modulo.

    ``deps_internas``: conjunto de nos de grafo ("tela.renderizacao.X")
    normalizados a partir de ast.Import/ast.ImportFrom absolutos e
    autorizados. ``violacoes``: lista de (motivo, linha) para toda forma
    proibida — import relativo de qualquer forma, ou import (via
    ast.Import/ast.ImportFrom) que referencie o pacote "tela.renderizacao"
    sem nomear o submodulo.
    """
    arv = ast.parse(src, filename=origem)
    deps, violacoes = set(), []
    for no in ast.walk(arv):
        if isinstance(no, ast.ImportFrom):
            if no.level and no.level > 0:
                violacoes.append(("import relativo (level > 0)", no.lineno))
            elif no.module == PREFIXO:
                violacoes.append((
                    "from tela.renderizacao import <modulo> oculta o "
                    "submodulo real no grafo", no.lineno,
                ))
            elif no.module and no.module.startswith(PREFIXO + "."):
                deps.add(no.module)
        elif isinstance(no, ast.Import):
            for alias in no.names:
                if alias.name == PREFIXO:
                    violacoes.append((
                        "ast.Import simples de tela.renderizacao (sem "
                        "submodulo) oculta o submodulo real no grafo{0}".format(
                            " com alias local {0!r}".format(alias.asname)
                            if alias.asname else ""
                        ), no.lineno,
                    ))
                elif alias.name.startswith(PREFIXO + "."):
                    deps.add(alias.name)
    return deps, violacoes


# --- Verificacoes sinteticas (falham ruidosamente se o analisador regredir)

_, v1 = analisar_arquivo("from .modulo import simbolo\n")
assert v1, "REGRESSAO: import relativo deveria ser rejeitado"

_, v2 = analisar_arquivo("from tela.renderizacao import modulo\n")
assert v2, "REGRESSAO: 'from tela.renderizacao import modulo' deveria ser rejeitado"

_, v3 = analisar_arquivo("import tela.renderizacao\n")
assert len(v3) == 1 and v3[0][0].startswith("ast.Import simples"), (
    "REGRESSAO: 'import tela.renderizacao' deveria ser rejeitado por ast.Import"
)

_, v4 = analisar_arquivo("import tela.renderizacao as renderizacao\n")
assert len(v4) == 1 and "alias local" in v4[0][0], (
    "REGRESSAO: 'import tela.renderizacao as renderizacao' deveria ser "
    "rejeitado por ast.Import com resultado distinguivel"
)

d5, v5 = analisar_arquivo("import tela.renderizacao.modulo\n")
assert not v5 and d5 == {"tela.renderizacao.modulo"}, (
    "REGRESSAO: 'import tela.renderizacao.modulo' deveria ser aceito e normalizado"
)

d6, v6 = analisar_arquivo("import tela.renderizacao.modulo as alias\n")
assert not v6 and d6 == d5 == {"tela.renderizacao.modulo"}, (
    "REGRESSAO: alias nao deveria alterar a normalizacao de ast.Import"
)

d7, v7 = analisar_arquivo("from tela.renderizacao.modulo import simbolo\n")
assert not v7 and d7 == {"tela.renderizacao.modulo"}, (
    "REGRESSAO: 'from tela.renderizacao.modulo import simbolo' deveria ser "
    "aceito e normalizado"
)

d8, v8 = analisar_arquivo(
    "from tela.renderizacao.modulo import simbolo as alias\n"
)
assert not v8 and d8 == d7 == {"tela.renderizacao.modulo"}, (
    "REGRESSAO: alias nao deveria alterar a normalizacao de ast.ImportFrom"
)

print("OK: verificacoes sinteticas do detector (rejeicao de formas proibidas "
      "e normalizacao das formas autorizadas)")

# --- Analise real do pacote: todos os arquivos .py, travessia transitiva,
# ciclos de qualquer comprimento, dependencias externas ignoradas no calculo
# de ciclos (so entram no grafo arestas que comecam com PREFIXO + ".").

pkg = pathlib.Path("tela/renderizacao")
grafo, todas_violacoes = {}, []

for arq in pkg.glob("*.py"):
    nome = f"{PREFIXO}.{arq.stem}"
    deps, violacoes = analisar_arquivo(arq.read_text(encoding="utf-8"), str(arq))
    grafo[nome] = deps
    todas_violacoes.extend((nome, linha, motivo) for motivo, linha in violacoes)

if todas_violacoes:
    print("FALHA: forma de import proibida dentro de tela/renderizacao/:", todas_violacoes)
    sys.exit(1)

visitado, pilha = set(), set()

def dfs(n, caminho):
    if n in pilha:
        raise SystemExit(
            "CICLO detectado: {0}".format(" -> ".join(caminho + [n]))
        )
    if n in visitado:
        return
    pilha.add(n)
    for d in sorted(grafo.get(n, ())):
        dfs(d, caminho + [n])
    pilha.discard(n)
    visitado.add(n)

for n in sorted(grafo):
    dfs(n, [])
print("OK: nenhum ciclo de importacao entre modulos de tela/renderizacao")
PY
```

```zsh
# 3. Nenhum modulo interno importa a fachada (repete a secao 5.2)
rg -n 'from tela\.renderizador import|import tela\.renderizador' tela/renderizacao
```

```zsh
# 4. Nenhum consumidor externo migrado para caminhos internos (repete a secao 5.1)
rg -n 'from tela\.renderizacao|import tela\.renderizacao' tela demo \
  | grep -v '^tela/renderizador.py:' \
  | grep -v '^tela/renderizacao/'
# saída esperada: vazia
```

```zsh
# 5. Reducao material da concentracao de tela/renderizador.py
wc -l tela/renderizador.py
# esperado: modulo reduzido a fachada de reexportacao (ordem de dezenas de
# linhas, nao centenas) — nenhuma funcao com corpo de logica de dominio.
```

```zsh
# 6. Fachada sem funcoes, lambdas ou classes — prova normativa UNICA (§3.4).
# Nenhuma alternativa permissiva de wrapper e admitida nesta versao do
# handoff: se a implementacao encontrar necessidade concreta de
# funcao-wrapper, deve parar pela excecao operacional focal (§11) e
# solicitar patch documental antes de cria-la — nao ha comando alternativo
# a substituir esta prova.
python3 - <<'PY'
import ast, importlib

reexportacoes_autorizadas = {
    "tela.renderizacao.erros": {"RenderizadorErro"},
    "tela.renderizacao.contexto_execucao": {
        "_navegacao_atual", "_preparar_contexto_navegacao",
        "DESCONTO_ESTRUTURAL_CONSOLE",
    },
    "tela.renderizacao.geometria_caixa": {
        "_distribuir_alturas", "_distribuir_larguras", "_pesos_distribuicao",
    },
    "tela.renderizacao.designadores": {
        "_texto_designador", "_romano", "_alfabetico",
    },
    "tela.renderizacao.conteudo_externo": {
        "_truncar_com_marcador", "_quebrar_texto", "_texto_valor_campo",
    },
    "tela.renderizacao.lancador": {"_linhas_lancador"},
    "tela.renderizacao.barra_menus": {
        "_linhas_barra", "_avaliar_regra_ativo", "_texto_chip_barra",
        "_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT", "_normalizar_distribuicao",
        "_validar_distribuicao", "_garantir_esc_primeiro",
    },
    "tela.renderizacao.texto_ansi": {
        "_largura_sem_ansi", "_ANSI_RESET_FG", "_codigo_ansi_de_cor",
        "_ljust_sem_ansi",
    },
    "tela.renderizacao.matriz_participantes": {
        "_larguras_mapa_fisico_matricial", "_participantes_distribuicao_matricial",
        "_largura_indicador_do_elemento", "_renderizar_participante_na_celula",
        "calcular_distribuicao",
    },
    "tela.renderizacao.console": {"_linhas_console", "mapa_fisico_de_itens"},
    "tela.renderizacao.paginacao_interna": {"_linhas_distribuicao_matricial"},
    "tela.renderizacao.composicao_corpo": {
        "_montar_corpo_horizontal", "_renderizar_container_horizontal",
    },
    "tela.renderizacao.tela": {
        "geometria_console", "altura_interna_disponivel", "renderizar_tela",
    },
}
publicos_fachada = {
    simbolo: modulo
    for modulo, simbolos in reexportacoes_autorizadas.items()
    for simbolo in simbolos
}
assert len(publicos_fachada) == sum(
    len(simbolos) for simbolos in reexportacoes_autorizadas.values()
), "mapa nominal da fachada contem simbolos duplicados"


def eh_alias_simples(no):
    """True para Name ou cadeia de Attribute sobre Name."""
    if isinstance(no, ast.Name):
        return True
    if isinstance(no, ast.Attribute):
        return eh_alias_simples(no.value)
    return False


def eh_lista_literal_de_strings(no):
    return isinstance(no, (ast.List, ast.Tuple)) and all(
        isinstance(el, ast.Constant) and isinstance(el.value, str) for el in no.elts
    )


def analisar_fachada(fonte):
    """Aplica a politica fechada de imports e aliases da fachada."""
    arv = ast.parse(fonte, filename="<fachada-sintetica>")
    violacoes, importados, atribuicoes = [], {}, {}
    nomes_all = None

    for idx, stmt in enumerate(arv.body):
        if (
            idx == 0
            and isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Constant)
            and isinstance(stmt.value.value, str)
        ):
            continue
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                violacoes.append(
                    "ast.Import nao autorizado na fachada: {0}".format(alias.name)
                )
            continue
        if isinstance(stmt, ast.ImportFrom):
            if stmt.level:
                violacoes.append("ImportFrom relativo nao autorizado")
                continue
            if stmt.module == "__future__":
                violacoes.append(
                    "ImportFrom de __future__ nao previsto para esta fachada"
                )
                continue
            if stmt.module not in reexportacoes_autorizadas:
                violacoes.append(
                    "modulo nao autorizado na fachada: {0}".format(stmt.module)
                )
                continue
            permitidos = reexportacoes_autorizadas[stmt.module]
            for alias in stmt.names:
                if alias.name == "*":
                    violacoes.append("importacao curinga nao autorizada na fachada")
                    continue
                if alias.name not in permitidos:
                    violacoes.append(
                        "simbolo nao autorizado em {0}: {1}".format(
                            stmt.module, alias.name
                        )
                    )
                    continue
                local = alias.asname or alias.name
                importados[local] = (stmt.module, alias.name, alias.asname)
            continue
        if (
            isinstance(stmt, ast.Assign)
            and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)
        ):
            alvo = stmt.targets[0].id
            if alvo == "__all__":
                if not eh_lista_literal_de_strings(stmt.value):
                    violacoes.append("__all__ deve ser lista/tupla literal de strings")
                else:
                    nomes_all = [el.value for el in stmt.value.elts]
                continue
            if not eh_alias_simples(stmt.value):
                violacoes.append(
                    "atribuicao da fachada deve ser alias simples: {0}".format(alvo)
                )
                continue
            if alvo not in publicos_fachada or not isinstance(stmt.value, ast.Name):
                violacoes.append(
                    "alias nao autorizado ou sem nome canonico: {0}".format(alvo)
                )
                continue
            atribuicoes[alvo] = stmt.value.id
            continue
        violacoes.append(
            "instrucao nao autorizada no nivel de modulo: {0}".format(
                type(stmt).__name__
            )
        )

    for local, (modulo, origem, asname) in importados.items():
        if asname and asname != origem:
            if not any(
                alvo == origem and valor == local
                for alvo, valor in atribuicoes.items()
            ):
                violacoes.append(
                    "alias tecnico {0!r} nao recompõe o nome canonico {1!r}".format(
                        local, origem
                    )
                )

    for alvo, local in atribuicoes.items():
        origem = importados.get(local)
        esperado = publicos_fachada.get(alvo)
        if origem is None or origem[:2] != (esperado, alvo):
            violacoes.append(
                "alias {0!r} nao possui origem nominal autorizada".format(alvo)
            )
    return arv, violacoes, importados, atribuicoes, nomes_all


def all_fechado(nomes_all):
    return nomes_all is None or set(nomes_all) == set(publicos_fachada)


casos_fachada_rejeitados = {
    "import os": "import os\n",
    "import copy": "import copy\n",
    "import tela.renderizacao": "import tela.renderizacao\n",
    "simbolo nao autorizado de modulo permitido": (
        "from tela.renderizacao.console import simbolo_nao_autorizado\n"
    ),
    "simbolo correto do modulo errado": (
        "from tela.renderizacao.modulo_errado import renderizar_tela\n"
    ),
    "importacao generica do pacote": "from tela.renderizacao import console\n",
    "alias arbitrario": (
        "from tela.renderizacao.tela import renderizar_tela as arbitrario\n"
    ),
}
for descricao, fonte in casos_fachada_rejeitados.items():
    _, violacoes, _, _, _ = analisar_fachada(fonte)
    assert violacoes, "REGRESSAO: caso proibido da fachada passou ({0})".format(descricao)

casos_fachada_aceitos = {
    "reexportacao nominal de erro": (
        "from tela.renderizacao.erros import RenderizadorErro\n"
    ),
    "reexportacao nominal de tela": (
        "from tela.renderizacao.tela import renderizar_tela\n"
    ),
    "alias tecnico recompondo nome canonico": (
        "from tela.renderizacao.tela import renderizar_tela as _renderizar\n"
        "renderizar_tela = _renderizar\n"
    ),
}
for descricao, fonte in casos_fachada_aceitos.items():
    _, violacoes, _, _, _ = analisar_fachada(fonte)
    assert not violacoes, "REGRESSAO: caso permitido da fachada falhou ({0})".format(
        descricao
    )

nomes_all_ok = list(publicos_fachada)
assert all_fechado(nomes_all_ok)
assert not all_fechado(nomes_all_ok + ["simbolo_extra"]), (
    "REGRESSAO: __all__ aceitou simbolo extra"
)
assert not all_fechado(nomes_all_ok[:-1]), "REGRESSAO: __all__ aceitou simbolo ausente"
print("OK: casos sinteticos da fachada e __all__ respeitam a lista nominal fechada")


src = open("tela/renderizador.py", encoding="utf-8").read()
arv, violacoes, importados, atribuicoes, nomes_all = analisar_fachada(src)
assert not violacoes, "fachada possui import/alias fora da politica nominal: {0}".format(
    violacoes
)
assert all_fechado(nomes_all), (
    "__all__ da fachada deve conter exatamente a lista nominal publica, sem "
    "simbolos ausentes ou extras"
)
for simbolo, modulo in publicos_fachada.items():
    direto = importados.get(simbolo)
    via_alias = atribuicoes.get(simbolo)
    assert (
        (direto is not None and direto[:2] == (modulo, simbolo))
        or (
            via_alias is not None
            and importados.get(via_alias) is not None
            and importados[via_alias][:2] == (modulo, simbolo)
        )
    ), "reexportacao nominal ausente ou incorreta: {0}".format(simbolo)

fachada = importlib.import_module("tela.renderizador")
for simbolo, modulo in publicos_fachada.items():
    proprietario = importlib.import_module(modulo)
    assert hasattr(proprietario, simbolo), (
        "proprietario nominal nao expoe {0}: {1}".format(modulo, simbolo)
    )
    assert hasattr(fachada, simbolo), "fachada nao reexporta: {0}".format(simbolo)
    assert getattr(fachada, simbolo) is getattr(proprietario, simbolo), (
        "reexportacao nao preserva identidade do proprietario: {0}".format(simbolo)
    )

# Zero FunctionDef/AsyncFunctionDef/Lambda/ClassDef em QUALQUER profundidade.
# A mesma politica fechada acima tambem verifica os imports da fachada; nao
# ha caminho permissivo para import generico, simbolo extra ou alias arbitrario.
proibidos = [
    n for n in ast.walk(arv)
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef))
]
assert not proibidos, (
    "fachada nao pode conter FunctionDef/AsyncFunctionDef/Lambda/ClassDef em "
    "nenhuma profundidade; encontrados: {0}"
).format([getattr(n, "name", "<lambda>") for n in proibidos])

print(
    "OK: fachada contem somente imports nominais fechados, aliases simples e "
    "__all__ fechado — zero FunctionDef, AsyncFunctionDef, Lambda e ClassDef"
)
PY
```

```zsh
# 7. Mapa estrutural dos modulos internos — derivado da autoridade nominal do
# comando 6 (D-MOD-08 item 10):
# (a) existencia fisica de __init__.py e de todos os modulos previstos,
#     incluindo `texto_ansi.py`; __init__.py importavel, sem logica e sem
#     reexportar a API publica da fachada;
# (b) para cada simbolo cuja propriedade e atribuida a um modulo interno,
#     confirmacao POR AST de que o nome e MATERIALIZADO nesse arquivo
#     (FunctionDef/AsyncFunctionDef/ClassDef/atribuicao de nivel superior),
#     nao apenas presente via `hasattr` (que aceitaria import acidental de
#     outro modulo) — exceto os aliases tecnicos nominalmente autorizados
#     (ex.: `calcular_distribuicao`, reexportado de
#     `tela.distribuicao_matricial`), verificados por import nominal
#     explicito. A lista publica, seus proprietarios, a identidade da
#     reexportacao, a origem AST da fachada e o confronto de `__all__` sao
#     validados pelo mapa unico `reexportacoes_autorizadas` no comando 6;
#     este comando nao mantem uma segunda lista de reexportacoes.
python3 - <<'PY'
import ast, importlib, pathlib

pkg = pathlib.Path("tela/renderizacao")

esperados = {
    "tela.renderizacao.erros": {
        "definidos": ["RenderizadorErro"],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.contexto_execucao": {
        "definidos": [
            "_navegacao_atual", "_quadro_minimo_lancador_ativo",
            "DESCONTO_ESTRUTURAL_CONSOLE", "_ativar_quadro_minimo_lancador",
            "_quadro_minimo_lancador_esta_ativo",
            "_reiniciar_quadro_minimo_lancador", "_preparar_contexto_navegacao",
        ],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.texto_ansi": {
        "definidos": [
            "_ANSI_POR_NOME_SEMANTICO", "_ANSI_RESET_FG",
            "_codigo_ansi_de_cor", "_largura_sem_ansi", "_cortar_sem_ansi",
            "_ljust_sem_ansi",
        ],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.geometria_caixa": {
        "definidos": [
            "TOTAL_WIDTH", "INNER_WIDTH", "CONTENT_WIDTH", "_caixa",
            "_contar_linhas", "_distribuir_alturas", "_distribuir_larguras",
            "_pesos_distribuicao",
        ],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.designadores": {
        "definidos": ["_romano", "_alfabetico", "_texto_designador"],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.conteudo_externo": {
        "definidos": [
            "_linhas_conteudo_externo", "_quebrar_texto", "_truncar_com_marcador",
            "_texto_valor_campo", "_participantes_de_conteudo_externo",
        ],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.dashboard": {
        "definidos": ["_linhas_dashboard"],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.lancador": {
        "definidos": ["_linhas_lancador"],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.barra_menus": {
        "definidos": [
            "_avaliar_regra_ativo", "_texto_chip_barra", "_linhas_barra",
            "_normalizar_distribuicao", "_validar_distribuicao",
            "_garantir_esc_primeiro",
            "_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT",
        ],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.matriz_participantes": {
        "definidos": [
            "_larguras_mapa_fisico_matricial", "_participantes_distribuicao_matricial",
            "_largura_indicador_do_elemento", "_renderizar_participante_na_celula",
            "largura_util_itens_console",
        ],
        "aliases_autorizados": {
            "calcular_distribuicao": {
                "modulo": "tela.distribuicao_matricial",
                "nome_origem": "calcular_distribuicao",
            },
            "alinhar_na_celula": {
                "modulo": "tela.distribuicao_matricial",
                "nome_origem": "alinhar_na_celula",
            },
        },
    },
    "tela.renderizacao.console": {
        "definidos": ["mapa_fisico_de_itens", "_linhas_console"],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.paginacao_interna": {
        "definidos": ["_linhas_distribuicao_matricial"],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.composicao_corpo": {
        "definidos": [
            "_montar_corpo_horizontal", "_renderizar_container_horizontal",
        ],
        "aliases_autorizados": {},
    },
    "tela.renderizacao.tela": {
        "definidos": [
            "geometria_console", "altura_interna_disponivel", "renderizar_tela",
        ],
        "aliases_autorizados": {},
    },
}


def materializado_no_proprietario(nome_simbolo, caminho_arquivo):
    """True se `nome_simbolo` e definido no ARQUIVO por FunctionDef,
    AsyncFunctionDef, ClassDef ou atribuicao de nivel superior — nao apenas
    acessivel via `hasattr` por import acidental de outro modulo."""
    arv = ast.parse(caminho_arquivo.read_text(encoding="utf-8"), filename=str(caminho_arquivo))
    for stmt in arv.body:
        if (
            isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and stmt.name == nome_simbolo
        ):
            return True
        if isinstance(stmt, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == nome_simbolo for t in stmt.targets):
                return True
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            if stmt.target.id == nome_simbolo:
                return True
    return False


def alias_tecnico_na_arvore(nome_simbolo, arv, origem):
    """True somente para a origem AST exata e o nome local esperado."""
    for no in ast.walk(arv):
        if isinstance(no, ast.ImportFrom):
            if no.level != 0 or no.module != origem["modulo"]:
                continue
            for alias in no.names:
                if (
                    alias.name == origem["nome_origem"]
                    and (alias.asname or alias.name) == nome_simbolo
                ):
                    return True
    return False


def eh_alias_tecnico_autorizado(nome_simbolo, caminho_arquivo, origem):
    """Valida o alias usando modulo, nome de origem e nome local exatos."""
    arv = ast.parse(
        caminho_arquivo.read_text(encoding="utf-8"), filename=str(caminho_arquivo)
    )
    return alias_tecnico_na_arvore(nome_simbolo, arv, origem)


def alias_tecnico_em_fonte(nome_simbolo, fonte, origem):
    return alias_tecnico_na_arvore(nome_simbolo, ast.parse(fonte), origem)


origem_calcular = {
    "modulo": "tela.distribuicao_matricial",
    "nome_origem": "calcular_distribuicao",
}
casos_alias_rejeitados = {
    "modulo incorreto": "from pacote_incorreto import calcular_distribuicao\n",
    "nome de origem incorreto": (
        "from tela.distribuicao_matricial import outro as calcular_distribuicao\n"
    ),
    "nome local incorreto": (
        "from tela.distribuicao_matricial import calcular_distribuicao as nome_incorreto\n"
    ),
    "origem relativa": (
        "from .distribuicao_matricial import calcular_distribuicao\n"
    ),
}
for descricao, fonte in casos_alias_rejeitados.items():
    assert not alias_tecnico_em_fonte("calcular_distribuicao", fonte, origem_calcular), (
        "REGRESSAO: alias tecnico rejeitado deveria falhar ({0})".format(descricao)
    )
assert alias_tecnico_em_fonte(
    "calcular_distribuicao",
    "from tela.distribuicao_matricial import calcular_distribuicao\n",
    origem_calcular,
)
assert alias_tecnico_em_fonte(
    "calcular_distribuicao",
    "from tela.distribuicao_matricial import calcular_distribuicao as calcular_distribuicao\n",
    origem_calcular,
)
print("OK: casos sinteticos de alias tecnico validam origem, simbolo e nome local")


# (a) __init__.py: existencia fisica, importabilidade, ausencia de logica e
# ausencia de reexportacao da API publica da fachada.
init_path = pkg / "__init__.py"
assert init_path.is_file(), "tela/renderizacao/__init__.py nao existe"
init_mod = importlib.import_module("tela.renderizacao")
init_arv = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
corpo_nao_docstring = [
    stmt for i, stmt in enumerate(init_arv.body)
    if not (
        i == 0 and isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str)
    )
]
assert not corpo_nao_docstring, (
    "__init__.py deve conter apenas docstring de pacote, sem logica: {0}"
).format([type(s).__name__ for s in corpo_nao_docstring])
_simbolos_fachada_amostra = {
    "RenderizadorErro", "renderizar_tela", "geometria_console",
    "altura_interna_disponivel", "mapa_fisico_de_itens",
}
assert not any(hasattr(init_mod, s) for s in _simbolos_fachada_amostra), (
    "__init__.py nao deve reexportar simbolos publicos da fachada"
)

# (a)/(b) demais modulos: existencia fisica, import isolado, e para cada
# simbolo esperado, materializacao (ou alias tecnico autorizado) no arquivo.
modulos = {}
for nome, spec in esperados.items():
    caminho = pkg / (nome.rsplit(".", 1)[-1] + ".py")
    assert caminho.is_file(), "arquivo previsto ausente: {0}".format(caminho)
    modulos[nome] = importlib.import_module(nome)
    for simbolo in spec["definidos"]:
        assert hasattr(modulos[nome], simbolo), "{0} nao define {1}".format(nome, simbolo)
        assert materializado_no_proprietario(simbolo, caminho), (
            "{0}.{1} nao e materializado por FunctionDef/AsyncFunctionDef/"
            "ClassDef/atribuicao de nivel superior nesse arquivo — pode ser "
            "import acidental de outro modulo".format(nome, simbolo)
        )
    for simbolo, origem in spec["aliases_autorizados"].items():
        assert hasattr(modulos[nome], simbolo), (
            "{0} nao expoe o alias tecnico autorizado {1}".format(nome, simbolo)
        )
        assert eh_alias_tecnico_autorizado(simbolo, caminho, origem), (
            "{0}.{1} deveria chegar por ImportFrom com modulo, nome de origem "
            "e nome local exatos: {2}".format(nome, simbolo, origem)
        )

print(
    "OK: __init__.py e todos os modulos previstos existem, importam e "
    "materializam (ou aliasam nominalmente) os simbolos esperados"
)

print(
    "OK: __init__.py e todos os modulos previstos materializam os simbolos "
    "proprietarios; aliases tecnicos possuem origem AST exata"
)
PY
```

---

## 8. Demonstração estrutural reproduzível

Não interativa, cobrindo renderização, paginação, dimensionamento e console
com navegação/seleção, comparando com fixtures já existentes (sem criar
validação manual nova):

```zsh
# demo/demo.py --help NAO e uma demonstracao material de renderizacao: o
# script ignora --help e renderiza a tela inicial normalmente (confirmado
# nesta correcao). Mantido apenas como smoke de CLI (o processo roda e
# termina sem excecao), nao como prova de dimensionamento/geometria.
PYTHONDONTWRITEBYTECODE=1 python demo/demo.py --help >/dev/null
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo.py -q -k "largura_explicita or altura_explicita"
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_paginacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_navegacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_selecao.py -q
```

```zsh
# Redimensionamento / calculo dimensional: geometria_console reproduz a
# mesma autoridade usada pelo render, antes e depois da extracao. Usa as
# assinaturas reais confirmadas nesta correcao: renderizar_tela exige
# `estilo` (tela.loader.carregar_estilo -> EstiloResolvido, sem default);
# geometria_console exige `console` (um ElementoCorpo real do modelo) para
# devolver geometria nao-None (sem cota fisica estavel, retorna None — ver
# docstring de geometria_console). altura=40 foi verificada como suficiente
# para o corpo da tela "demo" (config/telas/demo/demo.json) em largura 80 E
# 42 (verificacao material desta correcao: altura=24, usada na versao
# anterior deste exemplo, produzia RenderizadorErro de altura insuficiente
# em largura 42).
python3 - <<'PY'
from tela.loader import carregar_tela, carregar_estilo
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela, geometria_console

estilo = carregar_estilo()
tela_raw = carregar_tela(None, "demo", "config/telas/demo")
modelo = construir_modelo(tela_raw)
console = next(
    e for e in modelo.corpo.elementos if getattr(e, "tipo", None) == "console"
)

LARGURA_A, LARGURA_B, ALTURA = 80, 42, 40

saida_a = renderizar_tela(modelo, estilo, largura=LARGURA_A, altura=ALTURA)
saida_b = renderizar_tela(modelo, estilo, largura=LARGURA_B, altura=ALTURA)

# 1. Execucao valida (ambas as chamadas completam sem excecao — a asserção
#    esta implicita: se RenderizadorErro fosse levantado, o script pararia
#    aqui).

# 2. Diferenca fisica entre larguras: a saida muda e a largura de cada
#    linha fisica acompanha a largura solicitada.
assert saida_a != saida_b
assert max(len(l) for l in saida_a.split("\n")) == LARGURA_A
assert max(len(l) for l in saida_b.split("\n")) == LARGURA_B

# 3. geometria_console e efetivamente invocada, com um console real, para
#    as duas larguras.
geo_a = geometria_console(modelo, estilo, LARGURA_A, ALTURA, console=console)
geo_b = geometria_console(modelo, estilo, LARGURA_B, ALTURA, console=console)
assert geo_a is not None and geo_b is not None
assert geo_a["largura"] != geo_b["largura"]

# 4. Coerencia minima entre geometria_console e a renderizacao real: a
#    largura que a autoridade de geometria devolve para o console e a
#    mesma largura de linha fisica produzida pelo render, para cada largura
#    solicitada (o console desta tela e o unico descendente do corpo,
#    ocupando a largura total do corpo).
assert geo_a["largura"] == max(len(l) for l in saida_a.split("\n"))
assert geo_b["largura"] == max(len(l) for l in saida_b.split("\n"))

print("OK: renderizacao e geometria_console coerentes entre larguras 80 e 42")
PY
```

Não interativo (nenhum `input()`/TTY é aberto); a validação visual
interativa em TTY real, caso ainda necessária, fica reservada ao usuário e
não é parte deste handoff nem do relatório de implementação.

---

## 9. Relatório de implementação

**Arquivo:** `docs/relatorios/IMP-0046-modularizacao-estrutural-do-renderizador.md`

Deve registrar, em até 900 palavras: arquivos criados e alterados;
responsabilidades extraídas por módulo; conteúdo final da fachada;
compatibilidade pública comprovada (seção 5); testes focais e suíte completa
executados (seção 6) com resultado; verificação de ciclos e de importação
inversa (seção 7) com resultado; redução estrutural observada (linhas antes/
depois, funções por módulo); qualquer símbolo público adicional descoberto
durante a extração e reexportado além da lista da seção 3.5; defeitos
funcionais encontrados e **deferidos** (não corrigidos); bloqueios ou
desvios frente a este handoff, incluindo eventuais pedidos de exceção
operacional (seção 11) e sua resolução.

---

## 10. Critérios de aceite (D-MOD-08, materializados para H-0046)

| # | Critério | Prova reproduzível |
|---|---|---|
| 1 | API pública preservada | Comando da seção 5.1 (todos os símbolos presentes) |
| 2 | Comportamento observável preservado | Suíte completa da seção 6 verde |
| 3 | Testes focais do domínio aprovados | Comandos nominais da seção 6 (arquivos individuais) verdes |
| 4 | Suíte canônica completa aprovada | `PYTHONDONTWRITEBYTECODE=1 python -m pytest` verde, seção 6 |
| 5 | Concentração do arquivo original reduzida materialmente | Comando 5 da seção 7 (`wc -l`) + comando 6 da seção 7 (zero funções de domínio na fachada) |
| 6 | Fachada pequena e sem nova lógica substantiva | Comando 6 da seção 7 (zero funções, funções assíncronas, lambdas e classes na fachada, em qualquer profundidade; nenhum wrapper é admitido nesta versão — exceção operacional focal, §11, se necessário) |
| 7 | Módulos nomeados por responsabilidade | Lista nominal da seção 3.2, cada módulo com responsabilidade explícita de uma frase |
| 8 | Ausência de dependências circulares | Comando 2 da seção 7 (grafo de imports) |
| 9 | Ausência de importação inversa | Comandos da seção 5.2 e comando 3 da seção 7 |
| 10 | Localização mais direta das responsabilidades | Comandos 6 e 7 da seção 7 (autoridade nominal fechada para a fachada, existência física de `__init__.py` e de todos os módulos, materialização por AST no proprietário nominal — não apenas `hasattr` —, aliases técnicos com origem exata e origem AST da reexportação) + mapeamento completo da seção 3.2 |

---

## 11. Exceção operacional focal

Se a implementação identificar necessidade estrita de alterar um arquivo não
autorizado pelo manifesto (seção 4), a implementação deve **parar antes da
alteração** e solicitar autorização informando:

- caminho exato do arquivo;
- motivo da necessidade;
- mudança esperada;
- impacto de não alterar (o que fica quebrado, incompleto ou incorreto sem
  essa mudança);
- relação com o H-0046 (por que a modularização estrutural, por si só, exige
  esse arquivo).

Nenhuma alteração fora do manifesto pode ocorrer sem essa autorização
explícita registrada no relatório de implementação (seção 9).

## 12. Consolidação final do Handoff 1

Esta seção registra o estado documental final deste handoff após a aprovação
técnica definitiva. O status inicial do frontmatter permanece como registro
da autorização emitida; o estado vigente é o desta consolidação.

```yaml
estado_final: IMPLEMENTATION_APPROVED
handoff:
  id: H-0046
  sequencia: 1 de 3
  estado: concluido
item:
  id: ITEM-0022
  estado: em_andamento
  passo_1: concluido
  passo_2: proximo
  passo_3: futuro
  dependencia_passo_2: fechamento_validado_do_passo_1
  dependencia_passo_3: fechamento_validado_do_passo_2
ADR:
  id: ADR-0039
  status: aceita
implementacao:
  status_final: IMPLEMENTATION_APPROVED
  suite_completa: 970_passed
  validacao_manual: dispensada
  bloqueios: []
proximo_handoff: modularizacao_estrutural_de_tela_loader
atividade_global_concluida: false
```
