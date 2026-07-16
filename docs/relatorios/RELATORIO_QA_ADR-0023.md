# Relatorio de QA da ADR-0023

```yaml
etapa: QA_ADR
adr: ADR-0023
artefato_auditado: docs/adr/ADR-0023-largura-minima-funcional-lancador.md
status_literal: ARCHITECTURE_REVIEW_REQUIRED
status_normalizado: REVISAO_ARQUITETURAL_REQUERIDA
data: 2026-07-15
auditoria: independente
```

## 1. Identificacao

Este relatorio audita exclusivamente a ADR-0023:

`docs/adr/ADR-0023-largura-minima-funcional-lancador.md`

Nenhuma correcao foi aplicada a ADR. Nenhum contrato, nomenclatura, indice,
handoff, codigo, teste ou configuracao foi alterado por esta auditoria.

## 2. Artefato auditado

Artefato principal:

`docs/adr/ADR-0023-largura-minima-funcional-lancador.md`

A ADR declara status `aceita`, data 2026-07-15, origem no achado
`QA-H0034-HANDOFF-ALTO-003`, contratos afetados `contrato_lancador.md` e
`NOMENCLATURA.md`, e handoff bloqueado `H-0034`.

## 3. Decisao explicita do usuario

Decisao material auditada:

> Quando o lancador nao cabe em uma coluna, o sistema nao fica utilizavel. Deve
> ser mostrada a mensagem ou o estado ja usado nas outras situacoes em que o
> terminal fica pequeno demais.

A decisao autoriza registrar que:

- se nem uma coluna valida completa do `lancador` couber, a interface fica
  inutilizavel;
- o fallback deve reutilizar o estado canonico existente de terminal pequeno
  demais;
- nao devem ser inventados truncamento, overflow, paginacao, omissao ou perda
  de itens;
- a recuperacao deve ocorrer quando o espaco suficiente for restaurado.

A decisao nao fixa uma nova mensagem textual, nao autoriza uma variante local
do aviso e nao resolve, por si so, se a substituicao visual deve ocorrer na
tela inteira ou somente na area alocada ao `lancador`.

## 4. Autoridades consultadas

- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`, integralmente.
- `docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md`, especialmente status
  `H2_HANDOFF_PATCH_REQUIRED` e achado `QA-H0034-HANDOFF-ALTO-003`.
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`,
  especialmente secoes 3.1 a 3.8 e calculos de largura.
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`, especialmente secao 9.
- `docs/contratos/contrato_lancador.md`, especialmente secoes 4 a 9.
- `docs/contratos/contrato_json_lancador.md`, especialmente secoes 2, 5 e 7.
- `docs/NOMENCLATURA.md`, especialmente secoes 6.2 e 8.1 a 8.4.
- `docs/adr/INDICE_ADR.md`.
- `docs/contratos/contrato_tela_json.md`, secao 24, apenas para confirmar a
  aplicacao contratual do quadro minimo da ADR-0017.
- `docs/contratos/contrato_composicao_corpo.md`, trechos sobre terminal pequeno
  e area insuficiente, apenas para confirmar escopo arquitetural.
- `demo/demo.py` e `demo/teste_demo.py`, somente para rastreabilidade do estado
  implementado de quadro minimo.
- `tela/renderizador.py`, somente para rastreabilidade do estado atual do
  `lancador`.
- `config/elementos/lancador.json`, para confirmar parametros normativos de vao.

## 5. Estado Git inicial e final

### Inicial

Comando executado a partir da raiz:

```bash
git status --short
```

Resultado:

```text
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? tela/__pycache__/
```

Comando executado a partir da raiz:

```bash
git diff --no-index /dev/null docs/adr/ADR-0023-largura-minima-funcional-lancador.md
```

Resultado: retornou codigo 1 porque comparou `/dev/null` com um arquivo novo.
Esse comportamento e esperado para `git diff --no-index` nessa situacao. O
diff exibiu a ADR inteira como arquivo novo.

### Final

Comando executado a partir da raiz:

```bash
git status --short
```

Resultado:

```text
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? tela/__pycache__/
```

Comando executado a partir da raiz:

```bash
git diff --no-index /dev/null docs/adr/ADR-0023-largura-minima-funcional-lancador.md
```

Resultado: retornou codigo 1 novamente porque comparou `/dev/null` com o
arquivo novo da ADR. Esse comportamento e esperado para este comando; o diff
exibiu a ADR inteira como arquivo novo. O conteudo auditado da ADR nao foi
alterado por esta auditoria.

## 6. Proveniencia dos itens nao rastreados

```yaml
docs/adr/ADR-0023-largura-minima-funcional-lancador.md:
  presente_no_status_atual: CONFIRMADO
  estado: "?? nao rastreado"
  origem: CONFIRMADO
  produzido_pelo_autor_da_adr: CONFIRMADO

docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  presente_no_status_atual: CONFIRMADO
  estado: "?? nao rastreado"
  origem: CONFIRMADO
  produzido_pelo_autor_da_adr: NAO_CONFIRMADO

docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md:
  presente_no_status_atual: CONFIRMADO
  estado: "?? nao rastreado"
  origem: CONFIRMADO
  produzido_pelo_autor_da_adr: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md:
  presente_no_status_atual: CONFIRMADO
  estado: "?? nao rastreado"
  origem: CONFIRMADO
  produzido_pelo_autor_da_adr: NAO_CONFIRMADO

demo/__pycache__/:
  presente_no_status_atual: CONFIRMADO
  estado: "?? nao rastreado"
  origem: NAO_CONFIRMADA
  produzido_pelo_autor_da_adr: NAO_CONFIRMADO

tela/__pycache__/:
  presente_no_status_atual: CONFIRMADO
  estado: "?? nao rastreado"
  origem: NAO_CONFIRMADA
  produzido_pelo_autor_da_adr: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_ADR-0023.md:
  presente_no_status_atual: CONFIRMADO
  estado: "?? nao rastreado"
  origem: CONFIRMADO
  produzido_pelo_autor_da_adr: NAO_CONFIRMADO
```

Observacao: os caches nao foram removidos.

## 7. Resumo executivo

A ADR-0023 registra corretamente a intencao material de nao truncar, nao
paginar, nao omitir itens e usar o estado canonico de terminal pequeno demais
quando nenhuma coluna completa do `lancador` couber. Tambem identifica
corretamente a lacuna aberta pelo QA do H-0034.

Entretanto, a ADR ainda nao pode ser aprovada sem revisao arquitetural. A
autoridade existente define `quadro minimo de terminal pequeno` como substituto
do quadro da sessao/tela quando as dimensoes do terminal sao insuficientes para
a tela normal. A ADR-0023 estende esse gatilho para uma area interna alocada ao
`lancador`, mas nao define sem ambiguidade o escopo visual do fallback: tela
inteira, corpo, area alocada ao `lancador` ou caixa do proprio `lancador`.

Ha tambem risco de mistura entre `content_w`, largura da caixa do `lancador`,
area alocada ao elemento e largura total do terminal. Essa distincao e
necessaria para aplicar corretamente a formula de coluna minima.

## 8. Auditoria das treze areas

### 8.1 Fidelidade a decisao do usuario

Parcialmente conforme.

A ADR registra que, se `content_w < coluna_minima_content_w`, o fallback e o
estado canonico de quadro minimo, proibindo truncamento, overflow, omissao,
duplicacao, reordenacao, paginacao e rolagem especifica. Tambem declara
recuperacao automatica quando o espaco volta.

Nao foi identificada invencao de texto fixo para a mensagem. A lacuna esta no
escopo visual do estado reutilizado, nao na fidelidade material da decisao.

### 8.2 Existencia e autoridade do estado canonico

Conforme quanto a existencia; insuficiente quanto a extensao.

Autoridade confirmada:

- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`, secao 9, define
  terminal pequeno demais quando dimensoes validas sao insuficientes para a
  tela normal.
- `docs/NOMENCLATURA.md`, secao 6.2, registra `quadro mínimo de terminal pequeno`.
- `docs/contratos/contrato_tela_json.md`, secao 24, aplica a regra como quadro
  minimo da sessao TUI.

Nome canonico exato confirmado: `quadro mínimo de terminal pequeno`.

Nao ha mensagem textual normativa fixa; a ADR-0017 exige preservar
inequivocamente o significado "terminal pequeno demais" e permite adequacao a
largura disponivel.

### 8.3 Extensao do gatilho para area alocada

Nao conforme.

A decisao do usuario aponta para reutilizar o estado existente quando o
`lancador` torna o sistema inutilizavel. A ADR afirma que o mesmo estado pode
ser acionado quando a area renderizavel do `lancador` e insuficiente mesmo com
terminal fisico maior.

Essa extensao nao decorre diretamente das autoridades existentes, que falam em
dimensoes da sessao/tela normal. A extensao pode ser arquiteturalmente correta,
mas exige esclarecer se a insuficiencia de um componente deve substituir todo o
quadro da TUI ou renderizar algum estado local. A ADR nao fecha essa escolha.

### 8.4 Escopo visual do estado

Nao conforme.

A ADR usa expressoes como "renderer do `lancador` deve entrar no estado" e
"mesmo estado canonico", mas nao declara onde o estado aparece. As autoridades
atuais definem quadro substituto da sessao/tela, nao uma variante local dentro
da caixa do elemento.

Essa ambiguidade obriga a implementacao futura a escolher entre pelo menos duas
leituras incompatíveis:

- substituir o quadro inteiro pelo aviso canonico;
- substituir apenas a area/caixa do `lancador` por uma variante local.

### 8.5 Definicao de coluna minima valida

Parcialmente conforme.

A formula da ADR considera chip, vao minimo chip-texto, texto, maiores
subcolunas e margens horizontais do bloco. Os parametros de vao batem com
`config/elementos/lancador.json`: `chip_texto.minimo = 1` e
`entre_itens_colunas_margem.minimo = 2`.

Problema: a ADR compara em alguns pontos a "area alocada ao `lancador`" com
`coluna_minima_content_w`. Se "area alocada" significar largura total da caixa
do elemento, faltam bordas e padding. Se significar area renderizavel de
conteudo, a ADR deve usar esse termo de modo consistente.

### 8.6 Formula e nivel de detalhe

Parcialmente conforme.

A formula e necessaria para verificar quando uma coluna valida cabe e nao fixa
nome de funcao interna. Entretanto, a ADR ainda precisa separar melhor:

- largura minima do conteudo da coluna;
- largura minima da caixa do `lancador`;
- largura minima da area alocada ao elemento;
- largura total da tela.

Sem essa separacao, a futura aplicacao pode cristalizar um detalhe de caixa
atual ou comparar grandezas diferentes.

### 8.7 Ordem de decisao

Conforme.

A ADR define a sequencia:

```text
calcular largura util
-> testar fila
-> testar matrizes validas
-> testar coluna minima
-> acionar quadro minimo quando nenhuma coluna valida couber
```

Nao ha fallback para coluna invalida, truncamento, paginacao ou perda de itens.
Ausencia de itens e tratada como 0 linhas de conteudo sem erro.

### 8.8 Recuperacao reativa

Conforme.

A ADR determina reavaliacao a cada redesenho, recuperacao automatica quando a
largura volta, retorno para fila ou matriz conforme a largura atual, ausencia
de reinicio e ausencia de estado invalido persistente. Isso e compativel com a
ADR-0017 quanto ao comportamento reativo.

### 8.9 Compatibilidade e escopo negativo

Conforme.

A ADR declara que nao altera textos, limite de caracteres, chips, acoes,
destinos, barra_de_menus, cabecalho, `destino_minimo`, `grupo_minimo`, H-0030,
H-0033, paginacao, rolagem, navegacao, selecao ou algoritmo completo de
fila/matriz.

Nao foi identificada contradicao direta nesses itens.

### 8.10 Relacao com ADRs anteriores

Parcialmente conforme.

A ADR identifica corretamente ADR-0001, ADR-0002, ADR-0003, ADR-0013,
ADR-0016 e ADR-0017 como relacionadas e nao declara substituicao indevida.

Ressalva: ao chamar a ADR-0017 de autoridade primaria do estado e simultaneamente
estender o gatilho para area interna do `lancador`, a ADR cria uma relacao nova
que precisa de revisao arquitetural ou redacao normativa mais explicita.

### 8.11 Documentos afetados

Parcialmente conforme.

Correto:

- `docs/contratos/contrato_lancador.md` precisa ser atualizado futuramente.
- `docs/NOMENCLATURA.md` precisa registrar o novo termo ou regra.
- `docs/adr/INDICE_ADR.md` precisa registrar a ADR.
- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
  deve ser tratado separadamente por `PATCH_HANDOFF`.
- `docs/contratos/contrato_json_lancador.md` nao precisa ser alterado, pois nao
  cria campo JSON novo e regras de layout pertencem ao contrato do tipo.

Condicionalmente incompleto:

- se o fallback continuar sendo o quadro minimo global de sessao/tela, a
  semantica de `docs/contratos/contrato_tela_json.md` e possivelmente
  `docs/contratos/contrato_composicao_corpo.md` pode precisar ser atualizada
  para aceitar gatilho por area interna alocada ao componente.

### 8.12 Ausencia de aplicacao prematura

Conforme.

A ADR nao altera contratos, nomenclatura, indice ou handoff. Ela lista
consequencias e criterios futuros, separa `APLICAR_ADR` de `PATCH_HANDOFF`,
nao afirma testes executados e nao declara que os contratos ja foram atualizados.

### 8.13 Exequibilidade da futura aplicacao

Nao conforme ate revisao arquitetural.

A decisao e aplicavel quanto a coluna minima, proibicoes e recuperacao. Contudo,
a futura aplicacao ainda exigiria decidir ou explicitar o escopo visual do
fallback e a relacao entre insuficiencia de area interna e quadro minimo global.
Sem isso, `APLICAR_ADR` nao pode propagar a regra sem nova escolha.

## 9. Analise do estado canonico

O estado canonico existe e esta normativamente definido:

- ADR-0017, secao 9: quando dimensoes atuais sao validas mas insuficientes para
  representar a tela normal, a aplicacao deve exibir quadro minimo equivalente
  a "terminal pequeno demais".
- `NOMENCLATURA.md`, secao 6.2: o termo canonico e
  `quadro mínimo de terminal pequeno`.
- `contrato_tela_json.md`, secao 24: a sessao TUI substitui o quadro anterior
  por quadro minimo, sem scroll, sem residuo e com recuperacao automatica.

Condicoes atuais de ativacao: dimensoes validas da janela/sessao TUI
insuficientes para a tela normal. Comportamento durante redimensionamento:
recalculo e redesenho apos novo par valido. Recuperacao: substituicao
automatica pela tela normal quando dimensoes suficientes forem restauradas.

Nao ha texto visual exato fixo. A implementacao atual em `demo/demo.py` usa
`terminal pequeno demais`, `tela peq.` ou string vazia conforme a largura, o que
confirma apenas a rastreabilidade operacional, nao cria autoridade normativa.

## 10. Analise do escopo visual do fallback

As autoridades atuais descrevem o quadro minimo como substituicao do quadro da
sessao/tela. A ADR-0023, por outro lado, fala no `renderer do lancador` entrando
no estado quando a area renderizavel alocada ao elemento e insuficiente.

Essa formulacao nao permite saber se o comportamento esperado e:

- substituir a tela inteira pelo quadro minimo;
- substituir o corpo inteiro;
- substituir apenas a area alocada ao `lancador`;
- substituir apenas a caixa interna do `lancador`.

A decisao do usuario manda reutilizar o comportamento existente, mas nao
autoriza inventar uma variante local. Como a ADR nao fixa que a reutilizacao e
global, nem cria uma nova autoridade para variante local, a aplicacao posterior
ficaria bloqueada por escolha arquitetural.

## 11. Analise das grandezas de largura

Grandezas distintas identificadas:

```text
largura minima do conteudo da coluna
largura minima da caixa do lancador
largura minima da area alocada ao elemento
largura total da tela
```

A ADR define `coluna_minima_content_w`, que e largura minima do conteudo
renderizavel para uma coluna completa, incluindo margens internas horizontais
do bloco de itens. Essa grandeza nao e automaticamente igual a largura total da
caixa do `lancador`, pois a caixa inclui bordas e eventual padding.

O H-0034 usava `content_w = largura_total_da_tela - 3` como traducao da
implementacao atual. A ADR-0023 evita repetir essa formula como regra central,
mas ainda mistura termos quando fala em "area alocada ao `lancador`" abaixo de
`coluna_minima_content_w`.

Para aplicacao futura, a regra precisa declarar explicitamente qual largura e
comparada:

- `content_w < coluna_minima_content_w`, para area de conteudo; ou
- `largura_caixa_lancador < coluna_minima_content_w + bordas/padding`, para
  area total da caixa.

## 12. Documentos afetados

Classificacao auditada:

```yaml
docs/contratos/contrato_lancador.md:
  classificacao_da_adr: afetado
  avaliacao_qa: correta

docs/NOMENCLATURA.md:
  classificacao_da_adr: afetado
  avaliacao_qa: correta

docs/adr/INDICE_ADR.md:
  classificacao_da_adr: afetado
  avaliacao_qa: correta

docs/contratos/contrato_json_lancador.md:
  classificacao_da_adr: nao_afetado
  avaliacao_qa: correta
  justificativa: decisao nao cria campo JSON novo e trata comportamento calculado pelo renderer

docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  classificacao_da_adr: PATCH_HANDOFF posterior
  avaliacao_qa: correta

docs/contratos/contrato_tela_json.md:
  classificacao_da_adr: nao_listado
  avaliacao_qa: possivelmente afetado se a extensao do quadro minimo global for mantida

docs/contratos/contrato_composicao_corpo.md:
  classificacao_da_adr: nao_listado
  avaliacao_qa: possivelmente afetado se a regra passar a tratar area interna insuficiente como gatilho global
```

## 13. Achados

### QA-ADR0023-BLOQUEANTE-001

Severidade: bloqueante.

Evidencia:

- ADR-0023, secao 3.2, declara que o `renderer do lancador` deve entrar no
  estado canonico quando `content_w < coluna_minima_content_w`.
- ADR-0023, secao 5.1, estende o estado para area renderizavel alocada ao
  `lancador`, mesmo quando a largura total do terminal e maior.
- ADR-0017, secao 9, `NOMENCLATURA.md` secao 6.2 e `contrato_tela_json.md`
  secao 24 definem quadro minimo para insuficiencia da tela normal/sessao TUI,
  nao como variante local de elemento.

Regra violada: a ADR nao pode deixar a implementacao escolher entre substituir
toda a tela e substituir somente a area do `lancador`.

Impacto: a futura aplicacao documental e o patch do H-0034 podem implementar
comportamentos visualmente incompatíveis, ambos alegando reutilizar o estado
canonico.

Correcao ou decisao necessaria: realizar revisao arquitetural e registrar, na
ADR, se a insuficiencia do `lancador` aciona o quadro minimo global da sessao ou
se sera criado outro estado local por nova decisao normativa. Se a opcao for o
quadro global, explicitar que o quadro inteiro e substituido.

Secao afetada: 3.2, 5.1, 5.2, 9, 10 e 11.

### QA-ADR0023-ALTO-001

Severidade: alto.

Evidencia:

- ADR-0023 define `coluna_minima_content_w` como formula de conteudo.
- A mesma ADR usa "area alocada ao `lancador`" e "area renderizavel alocada" em
  pontos que podem ser lidos como largura da caixa do elemento.
- O H-0034 distingue `content_w` da largura total usada pela caixa atual.

Regra violada: a ADR nao deve misturar largura minima do conteudo da coluna,
largura minima da caixa do `lancador`, largura minima da area alocada ao
elemento e largura total da tela.

Impacto: a futura implementacao pode comparar `coluna_minima_content_w` contra
a largura errada, gerando fallback cedo ou tarde demais.

Correcao ou decisao necessaria: explicitar as grandezas e declarar a formula
equivalente para a caixa/area alocada quando bordas e padding participarem do
cabimento.

Secao afetada: 3.1, 3.2, 5.1, 8, 10.

### QA-ADR0023-MEDIO-001

Severidade: medio.

Evidencia:

- ADR-0023 lista `contrato_lancador.md`, `NOMENCLATURA.md` e `INDICE_ADR.md`
  para futura aplicacao.
- A extensao do quadro minimo pode alterar a semantica aplicada em
  `contrato_tela_json.md` secao 24 e em `contrato_composicao_corpo.md`, caso o
  fallback seja global por insuficiencia de area interna.

Regra violada: documentos afetados devem identificar corretamente todos os
contratos que receberao consequencia normativa.

Impacto: uma futura `APLICAR_ADR` pode deixar a politica global de terminal
pequeno contraditoria com a nova condicao de gatilho por componente.

Correcao ou decisao necessaria: apos resolver o achado bloqueante, revisar a
lista de documentos afetados para incluir ou justificar explicitamente a nao
inclusao de `contrato_tela_json.md` e `contrato_composicao_corpo.md`.

Secao afetada: 9 e 10.

## 14. Status literal e normalizado

```yaml
status_literal: ARCHITECTURE_REVIEW_REQUIRED
status_normalizado: REVISAO_ARQUITETURAL_REQUERIDA
achados_bloqueantes: 1
achados_altos: 1
achados_medios: 1
achados_baixos: 0
observacoes: 0
```

Justificativa: a decisao material esta registrada, mas a ADR exige revisao
normativa/arquitetural antes de aprovacao porque estende um estado global
existente para insuficiencia de area interna sem definir o escopo visual do
fallback.

## 15. Proxima categoria

```yaml
proxima_categoria: REVISAO_ARQUITETURAL_ADR
gerar_prompt: false
```
