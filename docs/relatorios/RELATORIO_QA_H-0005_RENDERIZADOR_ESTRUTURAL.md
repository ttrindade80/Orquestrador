# RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL

Status final: QA_REJECTED
Data: 2026-07-07
QA: Codex
Ciclo: H-0005 — Renderer estrutural mínimo da tela raiz

## 1. Identificacao do QA

QA pos-implementacao do ciclo H-0005, informado como `IMPLEMENTATION_COMPLETED`.
O objetivo foi verificar aderencia ao handoff, regressao dos ciclos anteriores,
escopo Git, ausencia de mutacao em JSON e ausencia de cache/bytecode residual.

## 2. Arquivos lidos

Leitura minima obrigatoria respeitada. Arquivos lidos:

- `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
- `docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `tela/diagnostico.py`
- `tela/teste_diagnostico.py`
- `config/telas/orquestrador.json`
- `tela/teste_loader.py` e `tela/teste_modelo.py` somente via execucao/verificacao de regressao

Nao foram lidos contratos, ADRs, `NOMENCLATURA.md`, indices ou configs fora de
`config/telas/orquestrador.json`.

## 3. Resumo da implementacao auditada

`tela/renderizador.py` evoluiu a saida para o formato estrutural H-0005:
regioes `REGIAO: cabecalho`, `REGIAO: corpo` e
`REGIAO: barra_de_menus`; componentes como `[{tipo}] {id}`; chips como
`[{id}] {texto}`.

Os testes `tela/teste_renderizador.py` e `tela/teste_diagnostico.py` foram
atualizados para o novo formato, mantendo igualdade estrita com a saida
esperada do handoff e regressao dos ciclos anteriores.

## 4. Escopo Git

Estado inicial observado pelo QA:

```text
$ git status --short
 M tela/renderizador.py
 M tela/teste_diagnostico.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
?? docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md
```

```text
$ git diff --name-only
scripts/tela/renderizador.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_renderizador.py
```

```text
$ git diff --stat
 scripts/tela/renderizador.py       |  46 +++++++++-------
 scripts/tela/teste_diagnostico.py  |  91 ++++++++++++++++---------------
 scripts/tela/teste_renderizador.py | 108 ++++++++++++++++++-------------------
 3 files changed, 128 insertions(+), 117 deletions(-)
```

Os arquivos modificados em diff sao permitidos pelo handoff. Porem, o estado
Git tambem contem arquivos nao rastreados fora da lista exaustiva de arquivos
permitidos pelo H-0005, em especial `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
e `docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md`. O proprio relatorio
IMP tambem aparece como nao rastreado, embora seja permitido criar.

Estado final apos criar este relatorio de QA acrescenta:

```text
?? docs/relatorios/RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL.md
```

Este arquivo e o artefato solicitado ao QA.

## 5. Verificacao item a item

### 5.1 Renderer

- `renderizar_tela(modelo: ModeloTela) -> str` mantida.
- Entrada validada como `ModeloTela`; entrada invalida lanca `RenderizadorErro`.
- Renderer importa apenas `ModeloTela` de `tela.modelo`.
- Nao importa `json`, `os`, `pathlib`, `tela.loader`, `subprocess`.
- Nao abre arquivos, nao le JSON bruto, nao acessa `config/telas/orquestrador.json`
  nem `config/estilo.json`.
- Nao usa biblioteca de UI, largura real de terminal, cores, molduras ou ANSI.
- Nao executa acoes, bindings, chips, filtros ou navegacao por `tela_destino`.
- Nao grava estado ou arquivos.
- Nao acessa `_campos_inertes`; usa `elemento.id` e `elemento.tipo`.
- Saida deterministica confirmada por teste.

### 5.2 Formato estrutural H-0005

Saida do executavel:

```text
TELA: orquestrador
SCHEMA: tela.v1

REGIAO: cabecalho
  titulo: Orquestrador
  descricao: Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de survey

REGIAO: corpo
  arranjo: sobreposto
  componentes:
    [console] console_principal
    [dashboard] dashboard_info
    [lancador] lancador_principal

REGIAO: barra_de_menus
  chips:
    [chip_esc] Sair
    [chip_paginas] Páginas
    [chip_colunas] Colunas
    [chip_grupos] Grupos
    [chip_alternar] Alternar
    [chip_navegar] Navegar
    [chip_selecionar] Selecionar
    [chip_enter] Todos
    [chip_estilo] Estilo
    [chip_verboso] Verboso
    [chip_ajuda] Ajuda
```

O formato bate com o especificado no handoff H-0005, incluindo regioes,
componentes, chips, ausencia de moldura visual final, ausencia de cores e
ausencia de comportamento interativo.

### 5.3 Teste do renderer

`tela/teste_renderizador.py` continua sendo o teste principal da saida do
renderer. Ele valida o formato H-0005, igualdade literal com expected output,
modelo fabricado, determinismo, componentes por `id`/`tipo`, chips, erros de
tipo e proibicoes de import/leitura. Nao delega a validacao principal ao teste
de diagnostico e nao aceita o formato antigo H-0003 por acidente.

### 5.4 Teste de diagnostico

`tela/teste_diagnostico.py` foi atualizado para acompanhar as strings do novo
formato. Continua validando o ponto de entrada integrado, modo executavel,
determinismo, igualdade com expected output e invariantes H-0001, H-0002 e
H-0005 via subprocess. Nao substitui o teste principal do renderer.

### 5.5 Diagnostico executavel

`tela/diagnostico.py` nao aparece em `git diff --name-only`. Continua apenas
encadeando `carregar_tela -> construir_modelo -> renderizar_tela`, sem logica
especifica do novo formato, sem estilo e sem comportamento interativo.

### 5.6 JSON e mutacao

`config/telas/orquestrador.json` permanece valido. `git diff -- config/` nao
produziu saida, confirmando ausencia de alteracao em JSON.

### 5.7 Cache e bytecode

`find tela -type d -name '__pycache__' -print` nao produziu saida.
`find tela -type f -name '*.pyc' -print` nao produziu saida.
Nao houve cache/bytecode residual a remover.

### 5.8 Relatorio IMP-0005

O IMP contem identificacao do ciclo, resumo, arquivos alterados, formato final,
comandos, resultados, verificacao de cache/bytecode, pendencias e status final.

Inconsistencia bloqueante: o IMP afirma que arquivos em `docs/handoff/` nao
foram tocados e que os untracked `docs/handoff/H-0005-...` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md` ja estavam presentes
antes da implementacao. O QA nao recebeu uma linha de base anterior que permita
confirmar essa afirmacao, e o estado Git atual contem esses arquivos fora da
lista exaustiva de arquivos permitidos pelo H-0005.

## 6. Comandos executados e resultados

```text
$ python tela/teste_loader.py
EXIT=0
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

```text
$ python tela/teste_modelo.py
EXIT=0
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

```text
$ python tela/teste_renderizador.py
EXIT=0
Total de verificacoes: 39
Passaram: 39
Falharam: 0
Trecho relevante: saida contem REGIAO: cabecalho, REGIAO: corpo,
REGIAO: barra_de_menus; saida bate com expected output literal do handoff H-0005.
```

```text
$ python tela/teste_diagnostico.py
EXIT=0
Total de verificacoes: 27
Passaram: 27
Falharam: 0
Trecho relevante: invariantes H-0001, H-0002 e H-0005 preservados; modo executavel retorna 0.
```

```text
$ python tela/diagnostico.py
EXIT=0
Trecho relevante: imprime a saida estrutural H-0005 com as tres regioes e chips.
```

```text
$ python -m json.tool config/telas/orquestrador.json >/dev/null
EXIT=0
```

```text
$ git diff -- config/
EXIT=0
Saida vazia.
```

```text
$ find tela -type d -name '__pycache__' -print
EXIT=0
Saida vazia.
```

```text
$ find tela -type f -name '*.pyc' -print
EXIT=0
Saida vazia.
```

## 7. Achados

### BLOQUEANTE

1. Estado Git contem arquivos nao rastreados fora do escopo permitido pelo
   handoff H-0005:
   - `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
   - `docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md`

   O handoff declara a lista de arquivos permitidos como exaustiva e proibe
   criar/alterar arquivos em `docs/handoff/`. Sem uma linha de base Git
   anterior verificavel pelo QA, isso impede aprovar o ciclo.

2. O relatorio IMP-0005 esta incoerente com o estado Git atual ao declarar
   que nao ha arquivo fora do escopo e que `docs/handoff/` nao foi tocado,
   enquanto `git status --short` mostra arquivos nao rastreados fora do escopo.

### NAO_BLOQUEANTE

Nenhum achado nao bloqueante de implementacao funcional.

### OBSERVACAO

1. `git diff --name-only` e `git diff --stat` mostram apenas os tres arquivos
   de codigo/teste permitidos. A rejeicao decorre do estado Git completo visto
   por `git status --short`, nao do diff dos arquivos rastreados.

2. A implementacao funcional do renderer, os testes e o diagnostico passaram
   integralmente.

## 8. Decisao final

`QA_REJECTED`

Motivo: embora a implementacao funcional esteja aderente e todos os testes
obrigatorios passem, o criterio de aprovacao exige ausencia de alteracao/criacao
fora do escopo permitido. O estado Git atual contem arquivos nao rastreados fora
do escopo do H-0005 e o IMP nao representa esse estado com precisao verificavel.

## 9. Recomendacao objetiva

Nao seguir para commit do ciclo como aprovado. A proxima acao recomendada e
revisao humana do escopo Git para decidir se os arquivos untracked fora do
escopo pertencem a ciclo documental anterior e devem ser regularizados
separadamente. Depois disso, atualizar/corrigir o IMP se necessario e repetir
o QA de escopo.
