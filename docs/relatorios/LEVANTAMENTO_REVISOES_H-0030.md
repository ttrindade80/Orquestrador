# Levantamento de revisoes futuras originadas na validacao manual do H-0030

```yaml
etapa: LEVANTAMENTO
resultado_geral: >
  Levantamento neutro concluido. Foram localizadas evidencias documentais,
  declarativas, tecnicas e executaveis sobre os cinco pontos registrados na
  validacao manual do H-0030. Nenhum achado reabre ou reclassifica o H-0030.
  Nenhuma solucao foi escolhida, nenhuma ADR foi criada e nenhum arquivo alem
  deste relatorio foi alterado.
```

## 1. Objetivo e limites

Objetivo: investigar individualmente cinco pontos registrados como revisao
futura durante a validacao manual do H-0030:

1. quebra da descricao do cabecalho;
2. truncamento da descricao do cabecalho com reticencias;
3. reorganizacao dos chips do lancador em colunas;
4. espaco entre dashboard e `barra_de_menus` em `destino_minimo`;
5. espaco entre dashboard e `barra_de_menus` em `grupo_minimo`.

Limites observados:

- nao houve implementacao;
- nao houve correcao de codigo, configuracao, contrato ou ADR;
- nao houve QA formal;
- nao houve criacao de handoff;
- nao houve escolha entre alternativas de comportamento;
- nao houve reabertura nem reclassificacao do H-0030;
- unico arquivo criado: `docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md`.

## 2. Artefatos consultados

Artefatos de origem do H-0030:

- `docs/handoff/H-0030-catalogo-telas-utilizaveis.md`
- `docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md`
- `docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0030.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0030_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0030.md`

Autoridades documentais e declarativas consultadas:

- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_json_cabecalho.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/adr/ADR-0001-menu-suporta-matriz.md`
- `docs/adr/ADR-0002-menu-sobra-direita.md`
- `docs/adr/ADR-0003-vaos-elasticos-menu.md`
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md`

Configuracoes permanentes consultadas:

- `config/elementos/cabecalho.json`
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- `config/telas/demo/destino_minimo.json`
- `config/telas/demo/grupo_minimo.json`
- `config/telas/demo/h0030_console_unico.json`
- `config/telas/demo/h0030_dashboard_unico.json`
- `config/telas/demo/h0030_matriz_2x2.json`
- `config/telas/demo/h0030_matriz_3x2.json`
- `config/telas/demo/h0030_matriz_2x4.json`

Implementacao, testes e comandos existentes consultados:

- `tela/renderizador.py`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `demo/demo.py`
- `demo/diagnostico.py`
- `demo/teste_explorar_barra_de_menus.py`

## 3. Comandos executados

Estado e descoberta:

```bash
git status --short
pwd
rg --files
rg -n "H-0030|0030|validacao manual|VALIDACAO|revis" docs/handoff docs/relatorios
rg -n "descri|cabecalho|cabeçalho|quebra|linha|retic|ellipsis|trunca" docs/contratos docs/adr docs/NOMENCLATURA.md tela demo config
rg -n "chip|lancador|lançador|coluna|respons|horizontal|distribu|destino_minimo|grupo_minimo" docs/contratos docs/adr docs/NOMENCLATURA.md tela demo config
rg -n "destino_minimo|grupo_minimo|h0030|catalogo|demo.py|diagnostico|render" docs/handoff docs/relatorios tela demo config
rg -n "retic|ellipsis|\\.\\.\\.|…|quebr|wrap|descricao|descrição|max_caracteres|trunc" docs/contratos docs/adr docs/NOMENCLATURA.md config/elementos config/telas/demo tela demo
rg -n "def _linha|def _linhas|cabecalho|descricao|descrição|trunc|retic|lancador|_colunar|_grade|_linhas_lancador|renderizar_tela|_linhas_barra|_preencher|altura|distribu" tela/renderizador.py
rg -n "cabecalho|descricao|descrição|trunc|retic|lancador|coluna|matriz|destino_minimo|grupo_minimo|linha vazia|linhas estruturais|sem linhas externas|fill externo" tela/teste_renderizador.py demo/teste_explorar_barra_de_menus.py demo/teste_demo.py demo/teste_diagnostico.py
test -e docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md; echo $?
rm -rf tela/__pycache__
git status --short
```

Leituras por trechos, sempre a partir da raiz:

```bash
nl -ba docs/contratos/contrato_cabecalho.md | sed -n '1,260p'
nl -ba docs/contratos/contrato_json_cabecalho.md | sed -n '1,260p'
nl -ba docs/contratos/contrato_lancador.md | sed -n '1,320p'
nl -ba docs/NOMENCLATURA.md | sed -n '535,575p'
nl -ba docs/NOMENCLATURA.md | sed -n '780,930p'
nl -ba config/elementos/cabecalho.json | sed -n '1,220p'
nl -ba config/elementos/lancador.json | sed -n '1,220p'
nl -ba tela/renderizador.py | sed -n '120,195p'
nl -ba tela/renderizador.py | sed -n '292,345p'
nl -ba tela/renderizador.py | sed -n '755,850p'
nl -ba tela/renderizador.py | sed -n '1158,1385p'
nl -ba config/telas/demo/destino_minimo.json | sed -n '1,120p'
nl -ba config/telas/demo/grupo_minimo.json | sed -n '1,120p'
nl -ba docs/adr/ADR-0001-menu-suporta-matriz.md | sed -n '1,140p'
nl -ba docs/adr/ADR-0002-menu-sobra-direita.md | sed -n '1,130p'
nl -ba docs/adr/ADR-0003-vaos-elasticos-menu.md | sed -n '1,150p'
nl -ba docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md | sed -n '60,145p'
nl -ba docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md | sed -n '130,245p'
nl -ba docs/contratos/contrato_composicao_corpo.md | sed -n '235,335p'
nl -ba docs/contratos/contrato_composicao_corpo.md | sed -n '635,690p'
nl -ba docs/contratos/contrato_barra_de_menus.md | sed -n '520,570p'
nl -ba tela/teste_renderizador.py | sed -n '5720,5768p'
nl -ba tela/teste_renderizador.py | sed -n '5796,6180p'
nl -ba docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0030.md | sed -n '1,220p'
nl -ba docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md | sed -n '1,240p'
nl -ba docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md | sed -n '1,220p'
nl -ba docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md | sed -n '1,220p'
nl -ba docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0030_IMPLEMENTACAO.md | sed -n '1,260p'
```

Evidencias executaveis textuais:

```bash
python -c 'from tela.loader import carregar_tela; from tela.modelo import construir_modelo; from tela.renderizador import renderizar_tela
for idt in ("destino_minimo","grupo_minimo"):
    raw=carregar_tela(None,idt,"config/telas/demo"); modelo=construir_modelo(raw); print("===",idt,"==="); print("arquivo=config/telas/demo/%s.json"%idt); print("raw_id=%s modelo_id=%s titulo=%s arranjo=%s dist=%r"%(raw.get("id"),modelo.id,modelo.cabecalho.get("titulo"),modelo.corpo.arranjo,modelo.corpo.distribuicao)); print("filhos_corpo=",[(e.id,e.tipo,e._campos_inertes.get("titulo"),e._campos_inertes.get("distribuicao")) for e in modelo.corpo.elementos]);
    for largura,altura in ((42,20),(80,30)):
        s=renderizar_tela(modelo,largura=largura,altura=altura); linhas=s.splitlines(); topo=[i for i,l in enumerate(linhas) if l.startswith("╭")]; base=[i for i,l in enumerate(linhas) if l.startswith("╰")]; barra=topo[-1]; dash_topo=topo[1] if len(topo)>1 else None; dash_base=next((i for i in base if dash_topo is not None and i>dash_topo),None); vazias=[i for i,l in enumerate(linhas) if l==" "*largura]; internas=[i for i,l in enumerate(linhas) if l.startswith("│") and l.endswith("│") and not l.strip("│ ")]; print("dim=%sx%s total_linhas=%s topo_caixas=%s base_caixas=%s dash_topo=%s dash_base=%s barra_topo=%s vazias_totais=%s vazias_entre_dash_barra=%s internas_vazias=%s"%(largura,altura,len(linhas),topo,base,dash_topo,dash_base,barra,vazias,[i for i in vazias if dash_base is not None and dash_base<i<barra],internas));
        ini=max(0,(dash_base or 0)-1); fim=min(len(linhas),barra+3); print("janela_linhas_%s_%s:"%(ini,fim-1));
        for i in range(ini,fim): print("%02d:%r"%(i,linhas[i]));
'
```

```bash
python -c 'from tela.loader import carregar_tela; from tela.modelo import construir_modelo; from tela.renderizador import renderizar_tela
for idt in ("destino_minimo","demo"):
    raw=carregar_tela(None,idt,"config/telas/demo"); modelo=construir_modelo(raw); print("===",idt,"largura=24===");
    try:
        s=renderizar_tela(modelo,largura=24); linhas=s.splitlines(); print("id=%s titulo=%s descricao=%r"%(modelo.id,modelo.cabecalho.get("titulo"),modelo.cabecalho.get("descricao"))); print("linha0=%r"%linhas[0]); print("linha1=%r"%linhas[1]); print("linha2=%r"%linhas[2]); print("tem_reticencias=%s tem_quebra_desc=%s"%(("..." in linhas[1] or "…" in linhas[1]), False))
    except Exception as exc: print("erro=%s: %s"%(type(exc).__name__,exc))
'
```

Nenhum temporario externo ao repositorio foi criado.

## 4. Estado Git

Antes das verificacoes:

```yaml
comando: git status --short
resultado: limpo
stage: vazio
arquivos_modificados: []
arquivos_nao_rastreados: []
```

Durante as observacoes executaveis com Python, foi gerado `tela/__pycache__/`
como cache local. O cache foi removido com `rm -rf tela/__pycache__` para
restaurar o escopo final.

Depois das verificacoes, da criacao deste relatorio e da remocao do cache
gerado:

```yaml
comando: git status --short
resultado_observado:
  - "?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md"
arquivos_alterados:
  - docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
nenhum_outro_arquivo_alterado: true
```

## 5. Origem das revisoes futuras

O registro manual do H-0030 esta em
`docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0030.md`.

Evidencias:

- linhas 58-64: para o orquestrador, foram registradas observacoes sobre
  redimensionamento da descricao do cabecalho, reticencias e chips do lancador
  que nao se reorganizam em colunas;
- linhas 109-118: em `destino_minimo_d`, foi registrado espaco entre o dashboard
  `TESTE` e a `barra_de_menus`;
- linhas 120-129: em `grupo_minimo_g`, foi registrado o mesmo tipo de espaco;
- linhas 165-176: os itens foram explicitamente marcados como revisoes futuras
  nao bloqueantes, sem reabrir automaticamente o H-0030.

## 6. Ponto 1 - Quebra da descricao do cabecalho

Evidencia documental:

- `docs/contratos/contrato_cabecalho.md`, linhas 126-143: a descricao e
  renderizada abaixo da borda superior e possui `max_caracteres`,
  `alinhamento`, `recuo` e `capitalizacao`.
- `docs/contratos/contrato_cabecalho.md`, linhas 183-186: ha truncamento por
  `max_caracteres` antes de alinhamento/capitalizacao.
- `docs/contratos/contrato_json_cabecalho.md`, linhas 71-74 e 122-126:
  parametros de apresentacao pertencem a `config/elementos/cabecalho.json`.
- `config/elementos/cabecalho.json`, linhas 8-13: existem `max_caracteres`,
  `alinhamento`, `recuo` e `capitalizacao`, sem campo de numero de linhas ou
  politica de quebra por largura.

Nao foi localizada regra normativa ativa que determine ou permita quebrar a
descricao do cabecalho em duas linhas quando faltar largura horizontal.

Evidencia de implementacao:

- `tela/renderizador.py`, linhas 162-169: `_linha_conteudo` corta o texto com
  `texto[:content_w]` e monta uma unica linha.
- `tela/renderizador.py`, linhas 1241-1248: `renderizar_tela` passa a descricao
  como lista de uma linha (`[descricao]`) para `_caixa`.

Evidencia de testes:

- Foram encontradas verificacoes gerais de cabecalho e snapshots em
  `tela/teste_renderizador.py` e `tela/teste_demo.py`, mas nao foi localizada
  prova direta de quebra da descricao do cabecalho em duas linhas.

Evidencia executavel:

- Para `destino_minimo` em `largura=24`, a linha da descricao observada foi
  `'│ Tela de destino para │'`, seguida imediatamente pela base do cabecalho.
- Para `demo` em `largura=24`, a linha da descricao observada foi
  `'│ Tela raiz do sistema │'`, seguida imediatamente pela base do cabecalho.
- `tem_quebra_desc=False` na observacao textual.

```yaml
ponto: 1
descricao: "quebra da descricao do cabecalho"
autoridade_normativa: REGRA_AUSENTE
comportamento_normativo: "NAO_CONFIRMADO para quebra por largura; contrato so confirma uma linha de descricao e max_caracteres"
comportamento_observado: "descricao renderizada em uma unica linha e cortada por content_w"
implementacao: "tela/renderizador.py::_linha_conteudo; renderizar_tela passa [descricao]"
testes: "sem teste direto localizado para quebra de descricao do cabecalho"
evidencia_executavel: "largura=24 em destino_minimo e demo nao gerou segunda linha de descricao"
causa: "ausencia de politica normativa de quebra; implementacao atual usa corte por largura"
classificacao: REGRA_AUSENTE
bloqueio: NAO_CONFIRMADO
proxima_categoria_recomendada: BLOCKED_DOCUMENTATION
```

## 7. Ponto 2 - Truncamento da descricao com reticencias

Evidencia documental:

- `docs/contratos/contrato_cabecalho.md`, linhas 132-135: `max_caracteres`
  define numero maximo e texto que exceder esse limite e truncado antes da
  renderizacao.
- `docs/contratos/contrato_cabecalho.md`, linhas 183-186: truncamento ocorre
  antes de alinhamento/capitalizacao.
- `docs/NOMENCLATURA.md`, linhas 828-835: repete `max_caracteres` e truncamento
  da descricao.
- Nenhum desses trechos define reticencias, forma (`...` ou caractere unico),
  posicao das reticencias, nem precedencia entre reticencias e quebra de linha
  por largura.
- `docs/contratos/contrato_console.md` contem truncamento com reticencias para
  `console`, mas essa regra pertence a outro componente e nao pode ser
  transferida ao `cabecalho`.

Evidencia de implementacao:

- `tela/renderizador.py`, linhas 162-169: corte por `content_w` sem reticencias.
- `tela/renderizador.py`, linhas 1241-1248: descricao do cabecalho segue o mesmo
  caminho de `_linha_conteudo`.

Evidencia de testes:

- Nao foi localizado teste direto exigindo reticencias na descricao do
  cabecalho.

Evidencia executavel:

- Para `destino_minimo` em `largura=24`, a descricao foi cortada para
  `'Tela de destino para'`, sem `...` ou `…`.
- Para `demo` em `largura=24`, a descricao foi cortada para
  `'Tela raiz do sistema'`, sem `...` ou `…`.

Comparacao entre pontos 1 e 2:

- Quebra em duas linhas: nenhuma autoridade ativa localizada.
- Reticencias por falta de largura: nenhuma autoridade ativa localizada.
- Truncamento por `max_caracteres`: existe, mas nao decide overflow horizontal
  por largura nem define reticencias.
- Implementacao atual observa corte por largura sem reticencias e sem quebra,
  mas isso nao equivale a decisao normativa entre as alternativas.
- Nao foi localizada contradicao direta entre autoridades; foi localizada
  ausencia de decisao para a escolha quebra vs reticencias no cabecalho.

```yaml
ponto: 2
descricao: "truncamento da descricao do cabecalho com reticencias"
autoridade_normativa: "PARCIALMENTE_COMPROVADO para truncamento por max_caracteres; REGRA_AUSENTE para reticencias por largura"
comportamento_normativo: "truncar por max_caracteres antes da renderizacao; reticencias e precedencia com quebra NAO_CONFIRMADO"
comportamento_observado: "corte por content_w sem reticencias e sem segunda linha"
implementacao: "tela/renderizador.py::_linha_conteudo usa texto[:content_w]"
testes: "sem teste direto localizado para reticencias no cabecalho"
evidencia_executavel: "largura=24 em destino_minimo e demo: tem_reticencias=False"
causa: "decisao normativa ausente para overflow horizontal do cabecalho"
classificacao: REGRA_AUSENTE
bloqueio: BLOCKED_USER_DECISION
proxima_categoria_recomendada: CORRECAO_DOCUMENTAL_LOCALIZADA
```

## 8. Ponto 3 - Reorganizacao dos chips do lancador

Evidencia documental:

- `docs/contratos/contrato_lancador.md`, linhas 195-205: o renderer calcula
  automaticamente `fila` ou `matriz` a partir da largura real do terminal.
- `docs/contratos/contrato_lancador.md`, linhas 197-200: `fila` e linha unica;
  `matriz` e grade de multiplas colunas preenchida coluna-a-coluna.
- `docs/contratos/contrato_lancador.md`, linhas 206-207: o `lancador` nunca
  pagina.
- `docs/contratos/contrato_lancador.md`, linhas 311-317: largura de coluna pelo
  maior elemento da propria coluna; sub-colunas independentes.
- `docs/NOMENCLATURA.md`, linhas 855-917: confirma modos `fila` e `matriz`,
  algoritmo em duas etapas e ausencia de teto absoluto de colunas.
- `config/elementos/lancador.json`, linhas 15-21 e 55-72: `distribuicao_lancador`
  tem valores `fila`/`matriz`, origem calculada pelo renderer, e matriz
  coluna-a-coluna.
- `docs/adr/ADR-0001-menu-suporta-matriz.md`, linhas 29-34 e 49-68: origem
  historica da decisao para o antigo `menu`, hoje migrada para `lancador`.
- `docs/contratos/contrato_barra_de_menus.md`, linhas 526-566, e
  `docs/NOMENCLATURA.md`, linhas 546-571: a distribuicao da `barra_de_menus`
  e independente, e chips do `lancador` nao seguem regra da barra.

Evidencia de implementacao:

- `tela/renderizador.py`, linhas 315-338: `_linhas_lancador` renderiza cada item
  como uma linha separada `"[{chip}] {texto}"`; nao foi localizado calculo de
  `fila`/`matriz` para o `lancador`.
- `tela/renderizador.py`, linhas 782-787: `lancador` e passado para `_caixa`
  com as linhas de `_linhas_lancador`.

Evidencia de testes:

- `tela/teste_renderizador.py`, linhas 532-562: ha teste para rejeicao de texto
  de item acima de 15 caracteres.
- `tela/teste_renderizador.py`, linhas 1422-1475: ha testes de colunas para
  `barra_de_menus`, nao para `lancador`.
- Nao foi localizado teste direto que prove `lancador` em `fila` ou `matriz`.

Diferenciacao:

- Regra obrigatoria para `lancador`: localizada.
- Regra apenas permitida: nao; o contrato usa "calcula automaticamente".
- Comportamento atual nao normativo: localizado na implementacao, que renderiza
  um item por linha.
- Regra de outro componente: a `barra_de_menus` tambem possui distribuicao
  horizontal responsiva, mas a propria documentacao proibe transferir essa regra
  automaticamente ao `lancador`.

```yaml
ponto: 3
descricao: "reorganizacao dos chips do lancador em colunas quando faltar espaco horizontal"
autoridade_normativa: REGRA_ATIVA_EXISTENTE
comportamento_normativo: "lancador calcula fila se couber; se nao couber, matriz de multiplas colunas coluna-a-coluna"
comportamento_observado: "validacao manual informou que chips do lancador nao se reorganizam; implementacao atual gera um item por linha"
implementacao: "tela/renderizador.py::_linhas_lancador"
testes: "cobertura localizada para limite de texto; sem prova direta de fila/matriz do lancador"
evidencia_executavel: "NAO_CONFIRMADO por execucao especifica do lancador em matriz; evidencia tecnica por leitura de codigo"
causa: "regra ativa existe, mas implementacao/testes diretos de fila/matriz do lancador nao foram localizados"
classificacao: REGRA_ATIVA_EXISTENTE
bloqueio: NAO_CONFIRMADO
proxima_categoria_recomendada: CRIAR_HANDOFF
```

## 9. Ponto 4 - Espaco em `destino_minimo`

Arquivo permanente usado como entrada:

- `config/telas/demo/destino_minimo.json`

Identidade semantica confirmada:

- `raw_id=destino_minimo`
- `modelo_id=destino_minimo`
- `cabecalho.titulo=Destino Minimo`
- `corpo.arranjo=sobreposto`
- `modelo.corpo.distribuicao=None`
- filho direto: `dashboard_teste`, tipo `dashboard`, titulo `Teste`

Evidencia declarativa:

- `config/telas/demo/destino_minimo.json`, linhas 3-7: id e cabecalho.
- `config/telas/demo/destino_minimo.json`, linhas 8-25: corpo com um dashboard
  `dashboard_teste`, titulo `Teste`, campo literal.
- `config/telas/demo/destino_minimo.json`, linhas 26-92: `barra_de_menus`
  horizontal responsiva com chips `Esc` e `?`.
- Nao ha `corpo.distribuicao` no JSON.

Evidencia normativa:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`, linhas 81-100:
  corpo ocupa a altura entre `cabecalho` e `barra_de_menus`; preenchimento e
  responsabilidade do renderer, nao do JSON.
- `docs/contratos/contrato_composicao_corpo.md`, linhas 314-330: o corpo deve
  poder ocupar altura disponivel com linhas em branco adicionadas pelo renderer.
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`,
  linhas 130-146: quando ha `corpo.distribuicao`, a sobra deve ser incorporada
  as caixas; por contraste, a ausencia de `distribuicao` nao e `igual`
  explicito.

Evidencia de implementacao:

- `tela/renderizador.py`, linhas 1275-1292: calcula `l_corpo_disponivel` e
  renderiza o container.
- `tela/renderizador.py`, linhas 1315-1360: quando `altura` e fornecida, insere
  linhas fisicas de preenchimento apos o ultimo box do corpo e antes da barra,
  se o corpo nao for horizontal e nao houver distribuicao vertical explicita.

Evidencia de testes:

- `tela/teste_renderizador.py`, linhas 5754-5768: `destino_minimo` sem
  distribuicao e preservado; render com altura 20 produz 20 linhas.
- `tela/teste_renderizador.py`, linhas 5796-5807: comentarios distinguem
  cabecalho, barra e linhas estruturais em branco.

Evidencia executavel:

Com dimensao `42x20`:

- total: 20 linhas;
- dashboard `Teste`: topo linha 3, base linha 5;
- `barra_de_menus`: topo linha 17;
- linhas vazias full-width entre dashboard e barra: 6 a 16, total 11;
- linhas vazias internas do dashboard: nenhuma;
- linhas vazias internas da barra: nenhuma.

Com dimensao `80x30`:

- total: 30 linhas;
- dashboard `Teste`: topo linha 3, base linha 5;
- `barra_de_menus`: topo linha 27;
- linhas vazias full-width entre dashboard e barra: 6 a 26, total 21;
- linhas vazias internas do dashboard: nenhuma;
- linhas vazias internas da barra: nenhuma.

Diferenciacao de origem:

- espaco exigido pelo contrato: ocupacao da altura do corpo por preenchimento
  quando ha altura disponivel;
- espaco produzido por distribuicao: nao confirmado; `corpo.distribuicao=None`;
- margem/separador/padding: nao confirmado para as linhas 6..16 ou 6..26;
- linha vazia pertencente ao dashboard: nao confirmado; as linhas sao externas
  e full-width;
- linha vazia pertencente a barra: nao confirmado;
- origem restante: preenchimento externo do corpo pelo renderer, comprovado.

```yaml
ponto: 4
descricao: "espaco entre dashboard TESTE e barra_de_menus em destino_minimo"
autoridade_normativa: COMPROVADO
comportamento_normativo: "altura do corpo deve ser preenchida pelo renderer; ausencia de distribuicao nao aloca a sobra dentro do dashboard"
comportamento_observado: "linhas fisicas vazias full-width entre base do dashboard Teste e topo da barra"
implementacao: "tela/renderizador.py::renderizar_tela, bloco de l_corpo_fill"
testes: "tela/teste_renderizador.py preserva destino_minimo sem distribuicao e altura=20"
evidencia_executavel: "42x20: 11 linhas vazias externas; 80x30: 21 linhas vazias externas"
causa: "preenchimento externo da area do corpo com corpo.distribuicao ausente"
classificacao: COMPROVADO
bloqueio: NENHUMA_ACAO_NECESSARIA
proxima_categoria_recomendada: NENHUMA_ACAO_NECESSARIA
```

## 10. Ponto 5 - Espaco em `grupo_minimo`

Arquivo permanente usado como entrada:

- `config/telas/demo/grupo_minimo.json`

Identidade semantica confirmada:

- `raw_id=grupo_minimo`
- `modelo_id=grupo_minimo`
- `cabecalho.titulo=Grupo Minimo`
- `corpo.arranjo=vertical`
- `modelo.corpo.distribuicao=None`
- filho direto: `grupo_principal`, tipo `grupo`, sem `distribuicao`
- filho interno: dashboard `dashboard_conteudo`, titulo `Conteudo`

Observacao importante: a expressao "dashboard TESTE" nao foi confirmada em
`grupo_minimo`. O dashboard encontrado e `Conteudo`; o espaco entre esse
dashboard e a `barra_de_menus` foi confirmado.

Evidencia declarativa:

- `config/telas/demo/grupo_minimo.json`, linhas 3-7: id e cabecalho.
- `config/telas/demo/grupo_minimo.json`, linhas 8-31: corpo vertical com
  `grupo_principal`, que contem `dashboard_conteudo` titulo `Conteudo`.
- `config/telas/demo/grupo_minimo.json`, linhas 33-99: `barra_de_menus`
  horizontal responsiva com chips `Esc` e `?`.
- Nao ha `corpo.distribuicao` no JSON; nao ha `grupo.distribuicao`.

Evidencia normativa:

- Mesmas autoridades de ocupacao vertical e ausencia de distribuicao do ponto 4:
  `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`,
  `docs/contratos/contrato_composicao_corpo.md` e
  `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`.

Evidencia de implementacao:

- `tela/renderizador.py`, linhas 833-850: container vertical sem distribuicao
  renderiza filhos em altura natural.
- `tela/renderizador.py`, linhas 1315-1360: preenchimento externo e inserido
  antes da barra quando `altura` e fornecida e nao ha distribuicao vertical
  explicita.

Evidencia de testes:

- `tela/teste_renderizador.py`, linhas 5721-5751: `grupo_minimo.json` real tem
  `modelo.corpo.distribuicao is None`, altura 20 produz 20 linhas, filho natural
  e fill externo H-0015 presente.

Evidencia executavel:

Com dimensao `42x20`:

- total: 20 linhas;
- dashboard `Conteudo`: topo linha 3, base linha 5;
- `barra_de_menus`: topo linha 17;
- linhas vazias full-width entre dashboard e barra: 6 a 16, total 11;
- linhas vazias internas do dashboard: nenhuma;
- linhas vazias internas da barra: nenhuma.

Com dimensao `80x30`:

- total: 30 linhas;
- dashboard `Conteudo`: topo linha 3, base linha 5;
- `barra_de_menus`: topo linha 27;
- linhas vazias full-width entre dashboard e barra: 6 a 26, total 21;
- linhas vazias internas do dashboard: nenhuma;
- linhas vazias internas da barra: nenhuma.

Diferenciacao de origem:

- espaco exigido pelo contrato: ocupacao da altura do corpo por preenchimento
  quando ha altura disponivel;
- espaco produzido por distribuicao: nao confirmado; corpo e grupo sem
  `distribuicao`;
- margem/separador/padding: nao confirmado para as linhas externas;
- linha vazia pertencente ao dashboard: nao confirmado;
- linha vazia pertencente a barra: nao confirmado;
- origem restante: preenchimento externo do corpo pelo renderer, comprovado
  independentemente para `grupo_minimo`.

```yaml
ponto: 5
descricao: "espaco entre dashboard e barra_de_menus em grupo_minimo"
autoridade_normativa: COMPROVADO
comportamento_normativo: "altura do corpo deve ser preenchida pelo renderer; ausencia de distribuicao preserva filho natural e fill externo"
comportamento_observado: "linhas fisicas vazias full-width entre base do dashboard Conteudo e topo da barra"
implementacao: "tela/renderizador.py::_renderizar_container_vertical e renderizar_tela"
testes: "tela/teste_renderizador.py::test_integracao_json_grupo_minimo"
evidencia_executavel: "42x20: 11 linhas vazias externas; 80x30: 21 linhas vazias externas"
causa: "preenchimento externo da area do corpo com corpo.distribuicao e grupo.distribuicao ausentes"
classificacao: PARCIALMENTE_COMPROVADO
bloqueio: "NENHUMA_ACAO_NECESSARIA; dashboard TESTE em grupo_minimo = NAO_CONFIRMADO"
proxima_categoria_recomendada: NENHUMA_ACAO_NECESSARIA
```

## 11. Relacao ou independencia entre `destino_minimo` e `grupo_minimo`

Fatos comuns comprovados:

- ambos foram carregados de arquivos permanentes em `config/telas/demo/`;
- ambos possuem `modelo.corpo.distribuicao is None`;
- ambos produziram linhas fisicas vazias full-width entre o dashboard e a barra
  nas dimensoes observadas;
- ambos usam a mesma implementacao de preenchimento externo em
  `tela/renderizador.py::renderizar_tela`.

Independencia comprovada:

- `destino_minimo` tem dashboard direto `dashboard_teste`, titulo `Teste`;
- `grupo_minimo` tem grupo estrutural `grupo_principal` e dashboard interno
  `dashboard_conteudo`, titulo `Conteudo`;
- em `grupo_minimo`, a causa foi confirmada separadamente pela ausencia de
  `corpo.distribuicao` e de `grupo.distribuicao`, nao por analogia visual;
- a mencao a dashboard `TESTE` em `grupo_minimo` permanece `NAO_CONFIRMADO`.

## 12. Decisoes ausentes que devem retornar ao usuario

- Ponto 1: decidir se a descricao do cabecalho pode/deve quebrar em duas linhas
  por falta de largura, incluindo limite de linhas e comportamento em
  redimensionamento.
- Ponto 2: decidir se truncamento horizontal da descricao do cabecalho deve usar
  reticencias, qual forma (`...` ou outro caractere), posicao e precedencia
  frente a quebra.
- Ponto 3: nenhuma decisao de politica foi criada aqui; ha regra ativa para
  `lancador` em fila/matriz, mas a ausencia de implementacao/teste direto deve
  retornar como handoff tecnico, se o gerente assim decidir.
- Pontos 4 e 5: nenhuma decisao de comportamento foi identificada como ausente
  para o espaco observado nas dimensoes testadas; a origem normativa/tecnica do
  preenchimento externo foi comprovada. Para `grupo_minimo`, apenas a descricao
  "dashboard TESTE" permanece `NAO_CONFIRMADO`.

## 13. Proximas categorias processuais recomendadas

```yaml
ponto_1: BLOCKED_DOCUMENTATION
ponto_2: CORRECAO_DOCUMENTAL_LOCALIZADA
ponto_3: CRIAR_HANDOFF
ponto_4: NENHUMA_ACAO_NECESSARIA
ponto_5: NENHUMA_ACAO_NECESSARIA
```

## 14. Conclusao consolidada

O levantamento confirmou que os pontos do cabecalho ainda nao possuem autoridade
ativa suficiente para decidir quebra por largura ou reticencias. O ponto 2 fica
bloqueado por `BLOCKED_USER_DECISION` quanto a escolha entre alternativas de
overflow horizontal.

Para o `lancador`, existe regra ativa determinando calculo automatico entre
`fila` e `matriz`; a implementacao localizada ainda renderiza item por linha e
nao foi localizada cobertura direta desse comportamento normativo.

Para `destino_minimo` e `grupo_minimo`, o espaco observado foi reproduzido
textualmente e atribuido a preenchimento externo do corpo com `altura`
explicita e ausencia de `distribuicao`. Em `grupo_minimo`, a identidade
"dashboard TESTE" nao foi confirmada; o dashboard real observado e `Conteudo`.

Este relatorio nao propoe solucao e nao inicia etapa posterior.
