# Relatorio de QA do handoff H-0034

```yaml
etapa: QA_HANDOFF
handoff: H-0034
artefato_auditado: docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: PATCH_REQUERIDO
data: 2026-07-15
auditoria: independente
```

## 1. Identificacao

Este relatorio audita exclusivamente o handoff
`docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`.

Nenhuma correcao foi aplicada ao handoff. Nenhum codigo, teste, contrato, ADR,
configuracao ou nomenclatura foi alterado por esta auditoria.

## 2. Autoridades consultadas

- `docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_json_lancador.md`
- secoes aplicaveis de `docs/NOMENCLATURA.md`
- `docs/adr/ADR-0001-menu-suporta-matriz.md`, apenas como rastreabilidade historica
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `demo/demo.py`
- estado operacional disponivel no repositorio

## 3. Estado Git

Estado inicial:

```text
?? demo/__pycache__/
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? tela/__pycache__/
```

Diff inicial solicitado:

```text
git diff -- docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
```

Resultado: vazio, porque o handoff auditado esta nao rastreado.

Estado final verificado apos esta auditoria:

```text
?? demo/__pycache__/
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? tela/__pycache__/
```

Diff final solicitado:

```text
git diff -- docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
```

Resultado verificado: vazio, pelo mesmo motivo.

## 4. Proveniencia dos itens nao rastreados

```yaml
levantamento_h0030:
  preexistente_a_criacao_do_handoff: CONFIRMADO_POR_DECLARACAO_DO_USUARIO
  produzido_pelo_autor_do_handoff: false

pycache:
  preexistente_a_criacao_do_handoff: CONFIRMADO_POR_DECLARACAO_DO_USUARIO
  origem: NAO_CONFIRMADA
  produzido_pelo_autor_do_handoff: NAO_CONFIRMADO
```

Nao houve remocao de cache durante esta auditoria.

## 5. Resumo executivo

O H-0034 se apoia em regra ativa real: o `lancador` deve alternar entre
`fila` e `matriz`, calcular colunas automaticamente, preservar ordem
coluna-a-coluna e nao paginar. A configuracao demonstrativa `demo` existe,
possui identidade correta e contem os sete itens usados nos calculos.

Entretanto, o handoff precisa de patch antes de seguir para implementacao. O
principal defeito e tratar a linha focal `python -m pytest
tela/teste_renderizador.py -q` / `217 passed` como suite canonica completa,
contradizendo a linha de base anterior de seis scripts diretos e `1803/1803`.
Tambem ha ambiguidade na demonstracao por `python demo/demo.py`, pois esse
comando sozinho depende da largura fisica do terminal e nao reproduz
deterministicamente os limiares 80 e 110.

## 6. Verificacao das doze areas obrigatorias

### 6.1 Autoridade e decisao fechada

Conforme.

Autoridades:

- `contrato_lancador.md` secao 6.1 define `fila`, `matriz`, calculo automatico pela largura real e ausencia de paginacao.
- `contrato_lancador.md` secoes 6.2 e 6.3 definem largura por maior item da propria coluna e sub-colunas independentes.
- `contrato_lancador.md` secoes 6.4 e R-10 definem que alinhamento horizontal e regra da instancia.
- `NOMENCLATURA.md` secoes 8.1 a 8.3 definem vaos, sobra a direita, matriz, algoritmo em duas etapas e ausencia de teto absoluto.
- `config/elementos/lancador.json` fornece parametros transicionais concretos de vaos, sobra, colunas, matriz e vertical.
- `ADR-0001-menu-suporta-matriz.md` confirma a rastreabilidade historica do antigo `menu`, sem superar contratos ativos.

Ressalva: o handoff deve tomar cuidado para nao transformar a ADR historica do
antigo `menu` em autoridade superior ao contrato ativo do `lancador`, sobretudo
onde `contrato_lancador.md` declara alinhamento por instancia.

### 6.2 Formula de largura util

Parcialmente conforme.

O renderer atual calcula:

- `inner_w = total_w - 2`
- `content_w = total_w - 3`
- `_linha_conteudo`: `{v} {texto:<content_w}{v}`

Logo, as tres unidades subtraidas sao:

- 1 caractere da borda esquerda;
- 1 caractere de padding esquerdo fixo;
- 1 caractere da borda direita.

Isso corresponde estruturalmente a caixa real atual. Contudo, a formula esta
comprovada pela implementacao vigente, nao por regra contratual textual. O
handoff deve explicitar que `content_w = largura_total_da_area - 3` deriva da
API atual de `_caixa`/`_caixa_de_elemento` e nao da tela inteira em abstrato,
especialmente em renderizacao horizontal/grupos, onde `total_w` pode ser a
largura da area alocada ao elemento.

### 6.3 Algoritmo em duas etapas

Parcialmente conforme.

O algoritmo de tentar fila e depois matriz maximizando colunas esta amparado em
`NOMENCLATURA.md` secao 8.3, `config/elementos/lancador.json` e ADR-0001.
O handoff define universo de candidatos por `n_rows = 2..n_itens`, criterio de
validade por largura minima, desempate pelo primeiro candidato que couber,
numero de linhas, preenchimento coluna-a-coluna e calculo de colunas.

Defeito: quando nenhuma matriz valida cabe, o handoff manda usar `n_col = 1`,
`n_rows = n_itens`, mas nao define o que acontece se a coluna unica ainda for
maior que `content_w`. Como o renderer atual trunca linhas em `_linha_conteudo`,
isso deixa politica operacional nao documentada: erro, overflow visual,
largura minima funcional ou outra solucao.

### 6.4 Limiares da demonstracao

Conforme quanto aos calculos.

Itens reais de `config/telas/demo/demo.json`:

| idx | chip | texto | item_w_min |
|---:|---|---|---:|
| 0 | d | Destino | 11 |
| 1 | g | Grupo Min. | 14 |
| 2 | 1 | Console | 11 |
| 3 | 2 | Dashboard | 13 |
| 4 | 3 | Matriz 2x2 | 14 |
| 5 | 4 | Matriz 3x2 | 14 |
| 6 | 5 | Matriz 2x4 | 14 |

Calculo independente da fila:

```text
sum itens = 91
vaos internos = 6 * 2 = 12
margens = 2 + 2 = 4
fila_content_w_min = 91 + 12 + 4 = 107
largura_total_min = 107 + 3 = 110
```

Calculo independente de matriz 4 x 2 em largura 80:

```text
content_w = 80 - 3 = 77
colunas:
  c0: Destino, Grupo Min. -> 3 + 1 + 10 = 14
  c1: Console, Dashboard -> 3 + 1 + 9 = 13
  c2: Matriz 2x2, Matriz 3x2 -> 3 + 1 + 10 = 14
  c3: Matriz 2x4 -> 3 + 1 + 10 = 14
sum colunas = 55
vaos colunas = 3 * 2 = 6
margens = 2 + 2 = 4
matriz_4x2_content_w_min = 65
77 >= 65, portanto 4 x 2 cabe
```

Como a fila exige `content_w >= 107`, largura 80 nao cabe em fila e seleciona
4 x 2 antes de 3 x 3.

### 6.5 Separacao de escopos

Conforme, com ressalva.

O handoff distingue o arquivo criado pelo autor do handoff dos tres arquivos da
futura implementacao:

- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md`

Esses tres arquivos sao suficientes para implementar, testar no foco, demonstrar
por API com largura explicita e relatar. A leitura de `config/telas/demo/demo.json`
e `demo/demo.py` nao exige permissao de escrita.

Ressalva: se o patch documental corrigir a exigencia da suite canonica completa,
a implementacao futura precisara executar os seis scripts diretos, mas isso nao
exige ampliar arquivos autorizados para escrita.

### 6.6 Configuracao demonstrativa

Conforme.

`config/telas/demo/demo.json` existe, tem `id = "demo"`, contem
`lancador_principal`, possui exatamente os sete itens usados nos calculos, nao
precisa ser alterado e permite observar `fila` e `matriz` pelo renderer com
larguras explicitas.

Nao foi identificada dependencia de alias ou fallback entre raizes para provar
a identidade da tela, desde que a demonstracao semantica valide `modelo.id`.

### 6.7 Demonstracao deterministica

Nao conforme.

`python demo/demo.py`, sozinho, nao fixa largura 80 nem 110. Em TTY real, o
programa obtem dimensoes do terminal por ioctl/env/fallback; fora de TTY, usa
`shutil.get_terminal_size(fallback=(80, 24))`. Portanto, o comando isolado nao
reproduz de modo exato e repetivel:

- largura 80;
- largura 110;
- transicao fila -> matriz;
- retorno matriz -> fila;
- ordem das celulas em ambas as larguras.

O handoff inclui bons smokes por `renderizar_tela(modelo, largura=N, altura=30)`,
mas deve separar explicitamente:

- teste automatizado deterministico com largura explicita;
- smoke do ponto de entrada;
- pseudo-TTY;
- validacao humana em TTY real com redimensionamento e criterios de aceitacao.

### 6.8 Testes obrigatorios

Parcialmente conforme.

Os treze testes declarados cobrem fila, matriz, ordem coluna-a-coluna,
cardinalidade zero, cardinalidade um, limite exato, unidade abaixo, reducao e
ampliacao, identidade da configuracao demonstrativa, ausencia de paginacao e
preservacao de outros componentes.

Defeitos:

- T-07 promete provar largura de coluna independente, mas usa um cenario de uma
  unica coluna; nao prova que uma coluna larga nao afeta outra coluna.
- T-08 declara que todos os itens aparecem "a qualquer content_w positivo",
  o que reabre a lacuna operacional de larguras menores que o minimo de uma
  coluna.
- Os exemplos de demonstracao T-10/T-11 verificam relacoes de linhas, mas nao
  exigem larguras completas de coluna e vaos como valores esperados
  independentes.
- A prova da tela correta nao pode se limitar a codigo de saida zero; o handoff
  acerta ao exigir `modelo.id == "demo"`, mas precisa manter isso como criterio
  obrigatorio em todos os smokes relevantes.

### 6.9 Suite canonica

Nao conforme.

O handoff chama `python -m pytest tela/teste_renderizador.py -q` / `217 passed`
de linha de base e tambem de "suite canonica completa". Isso contradiz a
autoridade operacional anterior informada para este QA:

```text
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
demo/teste_demo.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
```

Linha de base comprovada anterior:

```text
1803/1803
6/6 codigos de saida zero
```

`217 passed` pode permanecer como suite focal por pytest, mas nao pode
substituir a suite canonica completa nem ser chamado de "suite canonica".

### 6.10 Escopo negativo e preservacoes

Conforme.

O handoff mantem fora do H-0034: cabecalho, quebra de descricao, reticencias,
`destino_minimo`, `grupo_minimo`, H-0033, `orquestrador.py`, contratos, ADRs,
nomenclatura, `barra_de_menus`, navegacao, selecao, acoes, paginacao,
persistencia e refatoracao ampla.

Nao foram encontrados residuos autorizando alteracao substantiva desses temas.

### 6.11 Relatorio de implementacao

Parcialmente conforme.

O caminho esperado esta correto:

```text
docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
```

O conteudo exigido cobre arquivos, algoritmo, autoridades, calculos, testes,
demonstracao, identidade da tela, Git, itens nao rastreados, caches, excecoes e
validacao manual pendente.

Defeito: o relatorio futuro e orientado a registrar como "suite canonica"
`python -m pytest tela/teste_renderizador.py -q`; deve exigir tambem a suite
canonica completa dos seis scripts diretos.

### 6.12 Condicoes de bloqueio e excecao operacional

Conforme.

O handoff manda parar antes de alterar arquivo fora da lista nominal, exige
autorizacao focal com arquivo, motivo, escopo e mudanca esperada, e nao permite
usar a excecao para criar arquitetura ou semantica nova.

## 7. Achados

### QA-H0034-HANDOFF-ALTO-001

Evidencia: secoes 10.1, 10.5, 11 e saida final do handoff chamam
`python -m pytest tela/teste_renderizador.py -q` / `217 passed` de suite
canonica ou suite canonica completa.

Regra violada: a suite canonica comprovada anterior e a execucao direta dos
seis scripts, com `1803/1803` e `6/6` codigos de saida zero.

Impacto: futura implementacao pode ser aprovada sem regressao completa do
projeto.

Correcao necessaria: renomear `217 passed` para suite focal e exigir, no IMP
futuro, a execucao dos seis scripts canonicos diretos.

Secao afetada: 9.1, 10.1, 10.5, 11, 12, 14 e saida final.

### QA-H0034-HANDOFF-ALTO-002

Evidencia: secao 5 declara `comando: python demo/demo.py`; secao 14 confirma
demonstracao por esse comando. `demo/demo.py` usa dimensoes reais do terminal
em TTY e `shutil.get_terminal_size` fora de TTY.

Regra violada: a demonstracao precisa reproduzir largura 80, largura 110,
transicao, retorno e ordem de celulas de modo exato e repetivel, ou declarar
preparacao do terminal e criterios humanos.

Impacto: o comando isolado nao comprova os limiares do handoff.

Correcao necessaria: separar comando TTY de validacao humana, smoke do ponto de
entrada e provas automatizadas deterministicas com `renderizar_tela(...,
largura=80/110, altura=30)`.

Secao afetada: 5, 9, 14 e saida final.

### QA-H0034-HANDOFF-ALTO-003

Evidencia: secao 3.4 define fallback `n_col = 1`, `n_rows = n_itens` quando
nenhuma distribuicao couber, mas nao define comportamento se uma coluna unica
ainda exceder `content_w`.

Regra violada: o executor futuro nao pode ter de escolher politica nao
documentada. O `lancador` nao pagina e nao deve perder itens.

Impacto: em larguras muito estreitas, a implementacao pode truncar, estourar,
errar ou inventar largura minima sem criterio aprovado.

Correcao necessaria: declarar o comportamento para `content_w` menor que a
menor coluna possivel, incluindo relacao com `_linha_conteudo` e com erro de
layout ou largura minima funcional.

Secao afetada: 3.4, 3.8, 10.3, 11.

### QA-H0034-HANDOFF-MEDIO-001

Evidencia: secao 3.1 apresenta `content_w = largura_total_da_tela - 3` como
formula do lancador.

Regra violada: a auditoria deve distinguir largura da tela, largura da caixa e
largura do conteudo.

Impacto: em areas aninhadas ou horizontais, a formula correta e sobre a largura
alocada ao elemento/caixa, nao necessariamente sobre a tela inteira.

Correcao necessaria: reescrever como `content_w = largura_total_da_area_do_elemento - 3`
e registrar que a base estrutural atual vem de `_linha_conteudo` e
`renderizar_tela`.

Secao afetada: 3.1.

### QA-H0034-HANDOFF-MEDIO-002

Evidencia: T-07 pretende provar largura de colunas independentes, mas o caso
descrito termina em uma unica coluna.

Regra violada: os testes obrigatorios devem cobrir larguras independentes.

Impacto: uma implementacao que usa largura global para todas as colunas pode
passar por essa prova.

Correcao necessaria: trocar T-07 por cenario de pelo menos duas colunas em que
uma coluna tenha texto maior e outra menor, com esperados independentes por
coluna.

Secao afetada: 10.3.

### QA-H0034-HANDOFF-MEDIO-003

Evidencia: T-10/T-11 validam relacoes entre chips na mesma linha ou em linhas
diferentes, mas nao exigem valores esperados completos de larguras de coluna,
vaos e margens no render final.

Regra violada: testes devem ter valores esperados independentes e nao depender
somente da mesma propriedade generica que a implementacao calcula.

Impacto: defeitos em vaos, largura de coluna e sobra horizontal podem escapar.

Correcao necessaria: incluir esperados literais ou medicoes independentes de
posicoes/intervalos para os sete itens da demo em largura 80 e largura 110.

Secao afetada: 9.2, 9.3, 10.4.

### QA-H0034-HANDOFF-BAIXO-001

Evidencia: o handoff afirma que nenhuma decisao nova foi criada, mas tambem
traduz detalhes da implementacao atual de `_caixa` como instrucao tecnica de
assinatura.

Regra violada: detalhe atual de implementacao nao deve virar regra normativa
sem autoridade ou justificativa estrutural.

Impacto: baixo, pois a mudanca e implementavel e localizada, mas a linguagem
deve ser mais precisa.

Correcao necessaria: declarar que a assinatura sugerida e caminho de
implementacao recomendado, nao norma independente.

Secao afetada: 3.1.

### QA-H0034-HANDOFF-OBS-001

Evidencia: `config/telas/demo/demo.json` tem `layout.alinhamento = "esquerda"`;
`config/elementos/lancador.json` declara sobra excedente a direita; o contrato
ativo tambem diz que alinhamento horizontal e regra da instancia.

Observacao: para a demo especifica nao ha conflito pratico, porque a instancia
declara esquerda. O handoff deve evitar generalizar esse valor para qualquer
instancia sem passar pela regra declarada.

## 8. Escopo necessario do eventual patch

O patch necessario e documental e deve se limitar ao proprio handoff H-0034.
Nao ha indicacao de necessidade de alterar contratos, ADRs, nomenclatura,
configuracoes, renderer ou testes nesta etapa.

Conteudo minimo do patch:

- corrigir a nomenclatura de suite focal versus suite canonica completa;
- exigir os seis scripts diretos e registrar a linha de base `1803/1803`;
- tornar a demonstracao deterministica por largura explicita;
- declarar criterio para largura menor que uma coluna minima;
- ajustar `content_w` para largura da area/caixa do elemento;
- fortalecer T-07, T-10 e T-11 com provas independentes.

## 9. Status

```yaml
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: PATCH_REQUERIDO
achados_bloqueantes: 0
achados_altos: 3
achados_medios: 3
achados_baixos: 1
observacoes: 1
proxima_categoria: PATCH_HANDOFF
```

## 10. Testes

Nao foram executados testes automatizados nesta etapa. A auditoria foi
documental e por leitura de fontes, para evitar criar novos caches ou alterar
estado operacional alem deste relatorio.

## 11. Validacao manual

Nao executada. A validacao manual em TTY real permanece uma atividade futura da
implementacao, depois que o handoff for corrigido para declarar dimensoes,
preparacao e criterios humanos.
