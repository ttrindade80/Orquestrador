# Relatorio de Auditoria do Handoff H-0004

## Status final

HANDOFF_REQUIRES_ADJUSTMENT

## Escopo auditado

Auditoria do handoff `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
quanto a prontidao para orientar uma implementacao minima do H-0004:

`config/telas/orquestrador.json` -> `tela/loader.py` -> `tela/modelo.py` ->
`tela/renderizador.py` -> diagnostico textual deterministico.

A auditoria verificou se o handoff limita o ciclo a integracao executavel
minima, preserva os invariantes de H-0001, H-0002 e H-0003, evita escopo
interativo/dinamico e oferece criterios observaveis para implementacao e QA.

## Arquivos lidos

- `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/handoff/H-0001-loader-validador-tela-json.md`
- `docs/handoff/H-0002-modelo-interno-tela.md`
- `docs/handoff/H-0003-renderizador-textual-estatico.md`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `config/telas/orquestrador.json`

## Arquivos nao lidos por decisao de escopo

- Demais contratos em `docs/contratos/`
- ADRs em `docs/adr/`
- `docs/NOMENCLATURA.md`
- `docs/INDICE.md`
- Demais arquivos de documentacao e configuracao nao listados no pedido
- Relatorios IMP/QA anteriores, pois nao foi necessario confirmar escopo ou
  regressao fora dos handoffs e arquivos autorizados

## Metodologia

1. Leitura limitada aos arquivos autorizados.
2. Comparacao do H-0004 contra o contrato de processo.
3. Comparacao do H-0004 contra os limites e invariantes herdados de H-0001,
   H-0002 e H-0003.
4. Verificacao textual dos pontos de entrada, arquivos permitidos, proibicoes,
   criterios de aceite, comandos esperados e condicoes de bloqueio.
5. Registro dos comandos de verificacao solicitados.

## Achados bloqueantes

### BLOQUEANTE 1 - Ambiguidade entre arquivos permitidos e arquivos que poderiam ser alterados com justificativa

O H-0004 afirma que o executor pode criar ou alterar somente:

- `tela/diagnostico.py`
- `tela/teste_diagnostico.py`
- `docs/relatorios/IMP-0004-diagnostico-executavel-tela-raiz.md`

Em seguida, a secao "Preferir nao alterar" lista `tela/loader.py`,
`tela/modelo.py`, `tela/renderizador.py`, `tela/__init__.py` e testes
anteriores, dizendo que se uma alteracao for estritamente necessaria deve ser
justificada objetivamente no relatorio.

Isso cria ambiguidade operacional: os arquivos sao ao mesmo tempo fora da lista
"somente" permitida e mencionados como possivelmente alteraveis mediante
justificativa. Pela regra de classificacao da auditoria, ambiguidade em arquivo
permitido/proibido e bloqueante.

Impacto: GLM/OpenCode poderia decidir localmente alterar modulo herdado sob
justificativa, enquanto outra leitura do handoff bloquearia qualquer alteracao.

### BLOQUEANTE 2 - Instrucao tecnicamente inconsistente sobre `sys.dont_write_bytecode`

O H-0004 exige que `sys.dont_write_bytecode = True` seja definido antes de
qualquer import. A estrutura esperada mostra essa atribuicao antes de
`import sys`, o que nao e executavel em Python, pois o nome `sys` nao existe
antes da importacao.

O proprio handoff tambem mostra, em outro trecho, um exemplo em que a atribuicao
ocorre dentro do bloco `if __name__ == "__main__":`, apos imports de `tela.*`.
Assim, ha conflito entre a intencao de prevenir bytecode antes dos imports do
pacote e os exemplos de implementacao.

Impacto: o executor precisaria escolher uma interpretacao local, por exemplo
`import sys` primeiro e definir `sys.dont_write_bytecode = True` antes dos
imports de `tela.*`. Como o handoff exige estrutura objetiva e verificavel, a
redacao atual precisa ajuste antes da implementacao.

## Achados nao bloqueantes

### NAO BLOQUEANTE 1 - Verificacao do modo executavel no teste integrado pode ser mais direta

A tabela de verificacoes obrigatorias de `tela/teste_diagnostico.py` diz que
`python tela/diagnostico.py` imprime a mesma string, mas descreve a verificacao
como "via importacao". Mais adiante, os criterios de aceite e comandos esperados
exigem executar `python tela/diagnostico.py`.

Nao impede a implementacao, porque os criterios posteriores sao observaveis,
mas recomenda-se alinhar a tabela para exigir verificacao real por subprocesso
ou deixar claro que a verificacao via importacao e apenas complementar.

### NAO BLOQUEANTE 2 - H-0004 poderia explicitar que `config/estilo.json` nao integra o fluxo minimo

O H-0004 inclui verificacao de `config/estilo.json` "se consultado no ciclo" e
nos comandos esperados herdados. Isso nao contradiz a cadeia principal, mas o
objetivo do H-0004 esta centrado em `config/telas/orquestrador.json`.

Recomenda-se explicitar que `config/estilo.json` e uma regressao documental
herdada/auxiliar, nao dependencia do diagnostico integrado.

## Observacoes

### OBSERVACAO 1 - Objetivo tecnico esta claro

O handoff define de forma direta a funcao publica
`gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str`, o modo
executavel `python tela/diagnostico.py` e o encadeamento
`carregar_tela(None, id_tela)` -> `construir_modelo(tela_raw)` ->
`renderizar_tela(modelo)`.

### OBSERVACAO 2 - Escopo interativo e dinamico esta bem proibido

O handoff proibe loop de aplicacao, navegacao, acoes, bindings ativos,
filtros funcionais, paginacao, selecao, registries, execucao de chips,
navegacao por `tela_destino`, dashboard dinamico, mudanca de estilo em runtime,
interface interativa, bibliotecas de UI e renderer visual final.

### OBSERVACAO 3 - Criterios de aceite sao majoritariamente observaveis

Os criterios cobrem ponto de entrada, saida deterministica, modo executavel,
teste integrado, regressao H-0001/H-0002/H-0003, ausencia de bytecode,
integridade de JSON, integridade documental e relatorio IMP-0004.

## Verificacao de aderencia ao H-0004

| Item auditado | Resultado |
|---|---|
| Objetivo tecnico definido | Conforme |
| Integracao executavel minima | Conforme |
| Cadeia loader -> modelo -> renderizador explicita | Conforme |
| Loop de aplicacao proibido | Conforme |
| Navegacao proibida | Conforme |
| Acoes proibidas | Conforme |
| Bindings ativos proibidos | Conforme |
| Filtros funcionais proibidos | Conforme |
| Paginacao funcional proibida | Conforme |
| Selecao proibida | Conforme |
| Registry de acoes ou tipos proibido | Conforme |
| Execucao de chips proibida | Conforme |
| Navegacao por `tela_destino` proibida | Conforme |
| Dashboard dinamico proibido | Conforme |
| Mudanca de estilo em runtime proibida | Conforme |
| Interface interativa proibida | Conforme |
| `curses`, `textual`, `rich` e bibliotecas de UI proibidas | Conforme |
| Renderer visual final proibido | Conforme |
| Ponto de entrada objetivo | Conforme |
| stdout/retorno textual definidos | Conforme |
| Saida deterministica e testavel exigida | Conforme |
| Arquivos permitidos definidos | Requer ajuste por ambiguidade local |
| Alteracoes normativas proibidas | Conforme |
| Alteracao de modulos herdados desencorajada | Requer ajuste por ambiguidade local |
| Relatorio IMP-0004 exigido | Conforme |
| Teste/evidencia integrada exigida | Conforme |
| Regressao H-0001/H-0002/H-0003 exigida | Conforme |
| Validacao de `config/telas/orquestrador.json` exigida | Conforme |
| Ausencia de `__pycache__` e `.pyc` exigida | Conforme |
| `git status` e diff final exigidos | Conforme |
| Implementacao sem decisao arquitetural | Requer ajuste por inconsistencia de `sys.dont_write_bytecode` |
| Criterios observaveis e verificaveis | Requer ajuste pontual |
| Sem nova regra normativa disfarçada | Conforme |

## Verificacao de aderencia ao contrato de processo

O contrato de processo exige handoff fechado, criterios verificaveis, limites
claros de arquivos permitidos/proibidos e bloqueio quando criterio nao for
verificavel ou decisao arquitetural estiver faltando.

O H-0004 atende ao objetivo geral do contrato, pois possui escopo pequeno,
criterios de aceite, arquivos proibidos, relatorio obrigatorio e condicoes de
bloqueio. Entretanto, os dois achados bloqueantes indicam que o handoff ainda
nao esta plenamente fechado: ha ambiguidade de arquivos alteraveis e uma
instrucao tecnicamente inconsistente sobre a ordem de `sys.dont_write_bytecode`.

Esses problemas parecem corrigiveis localmente no proprio texto do H-0004, sem
necessidade de revisao arquitetural.

## Verificacao de aderencia a cadeia H-0001 -> H-0002 -> H-0003

O H-0004 respeita a cadeia estabelecida:

- H-0001: usa `carregar_tela(None, id_tela)` e preserva validacao macro do
  loader.
- H-0002: usa `construir_modelo(tela_raw)` sem chamar loader internamente no
  modelo.
- H-0003: usa `renderizar_tela(modelo)` e reaproveita a saida textual estatica
  deterministica.

O H-0004 nao autoriza reimplementacao de loader, modelo ou renderizador e
mantem inertes DOC-B008, DOC-B009, `bindings`, `referencias_de_acoes`,
`filtros`, `tela_destino`, chips e campos pendentes.

Nao foi identificada contradicao material com H-0001, H-0002 ou H-0003, exceto
a necessidade de ajustar a redacao local do H-0004 sobre arquivos herdados e
bytecode antes da implementacao.

## Comandos de verificacao

### `git status --short`

Saida registrada apos a criacao deste relatorio:

```text
?? docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md
```

Observacao: o handoff auditado aparece como nao rastreado no estado atual do
repositorio. A auditoria nao alterou esse arquivo. O unico arquivo criado pela
auditoria foi este relatorio.

### `git diff --stat -- docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`

Saida registrada:

```text
```

### `git diff --stat -- docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md`

Saida registrada apos criacao deste relatorio:

```text
```

Observacao: a saida e vazia porque o arquivo do relatorio ainda esta nao
rastreado; `git diff --stat` nao inclui arquivos untracked por padrao.

## Conclusao

O H-0004 esta tecnicamente bem orientado para provar a integracao minima
H-0001 -> H-0002 -> H-0003, mas ainda nao deve seguir para implementacao sem
ajuste textual local.

Os bloqueios encontrados nao indicam lacuna normativa nem contradicao
arquitetural ampla. Eles podem ser corrigidos no proprio handoff:

1. tornar absoluta a proibicao de alterar `tela/loader.py`, `tela/modelo.py`,
   `tela/renderizador.py`, `tela/__init__.py` e testes anteriores, ou mover
   esses arquivos para uma lista explicitamente permitida com condicao formal;
2. corrigir a regra de `sys.dont_write_bytecode` para algo executavel, por
   exemplo: `import sys` deve ocorrer primeiro; em seguida
   `sys.dont_write_bytecode = True`; depois disso podem ocorrer imports de
   `tela.*`.

## Recomendacao objetiva

Ajustar o handoff no Claude Code antes de entregar ao GLM/OpenCode para
implementacao.

---

## Reauditoria apos ajuste

### Data da reauditoria

2026-07-07

### Arquivos lidos

Leitura obrigatoria e limitada conforme pedido da reauditoria:

- `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`

Nao foram lidos ADRs, NOMENCLATURA, indice, demais contratos, arquivos de
codigo ou configuracoes. Nao houve necessidade de confirmar contradicao em
codigo-fonte.

### Resumo dos ajustes verificados

O handoff ajustado tornou exaustiva a lista de arquivos permitidos e incluiu
secao explicita de proibicao absoluta de alteracao dos modulos herdados:

- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/__init__.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`

Tambem corrigiu a estrutura esperada de `tela/diagnostico.py`: o modulo deve
fazer `import sys` como primeiro import, definir
`sys.dont_write_bytecode = True` imediatamente a seguir e somente depois
importar `tela.loader`, `tela.modelo` e `tela.renderizador`.

O teste do modo executavel passou a exigir verificacao por
`subprocess.run(["python", "tela/diagnostico.py"], capture_output=True)`, com
comparacao de `stdout` contra a string retornada por
`gerar_diagnostico_tela()`.

`config/estilo.json` foi declarado explicitamente como fora da cadeia
funcional do diagnostico H-0004; sua validacao permanece apenas como regressao
documental herdada e auxiliar.

### Status dos bloqueantes anteriores

| Bloqueante anterior | Status na reauditoria | Evidencia |
|---|---|---|
| BLOQUEANTE 1 - Ambiguidade entre arquivos permitidos e alteraveis com justificativa | Resolvido | O handoff declara que somente tres arquivos podem ser criados/alterados e que a lista e exaustiva, sem excecao. Os modulos herdados e testes anteriores aparecem em "Proibicao absoluta de alteracao de modulos herdados". |
| BLOQUEANTE 2 - Instrucao inconsistente sobre `sys.dont_write_bytecode` | Resolvido | A estrutura esperada de `tela/diagnostico.py` exige `import sys`, depois `sys.dont_write_bytecode = True`, depois imports de `tela.*`. Nao exige decisao arquitetural local. |

Total de bloqueantes anteriores resolvidos: 2.

### Status dos achados nao bloqueantes anteriores

| Achado nao bloqueante anterior | Status na reauditoria | Evidencia |
|---|---|---|
| NAO BLOQUEANTE 1 - Verificacao do modo executavel poderia ser mais direta | Resolvido | A tabela de verificacoes obrigatorias exige subprocesso real para `python tela/diagnostico.py`, com `capture_output=True` e comparacao de stdout. |
| NAO BLOQUEANTE 2 - Explicitar que `config/estilo.json` nao integra o fluxo minimo | Resolvido | O criterio de aceite afirma que `config/estilo.json` nao faz parte da cadeia de diagnostico do H-0004 e que `tela/diagnostico.py` nao o consulta. |

Achados nao bloqueantes pendentes: 0.

### Observacoes anteriores

As tres observacoes anteriores continuam apenas informativas:

1. O objetivo tecnico permanece claro: funcao publica, modo executavel e
   encadeamento loader -> modelo -> renderizador.
2. O escopo interativo e dinamico permanece explicitamente proibido.
3. Os criterios de aceite permanecem observaveis, incluindo teste integrado,
   regressao H-0001/H-0002/H-0003, validacao de JSON, ausencia de bytecode e
   estado final do git.

### Verificacao objetiva do handoff ajustado

| Item verificado | Resultado |
|---|---|
| Arquivos permitidos e proibidos sem ambiguidade | Conforme |
| `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`, `tela/__init__.py` e testes anteriores proibidos | Conforme |
| Estrutura esperada de `tela/diagnostico.py` dispensa decisao arquitetural | Conforme |
| `sys.dont_write_bytecode` posicionado antes dos imports de `tela.*` | Conforme |
| Teste do modo executavel especificado de modo verificavel | Conforme |
| `config/estilo.json` fora da cadeia funcional do diagnostico | Conforme |
| GLM/OpenCode pode implementar sem decidir arquitetura | Conforme |
| H-0004 restrito a integracao loader -> modelo -> renderizador | Conforme |
| Loop de aplicacao proibido | Conforme |
| Navegacao proibida | Conforme |
| Acoes proibidas | Conforme |
| Bindings ativos proibidos | Conforme |
| Filtros funcionais proibidos | Conforme |
| Paginacao funcional proibida | Conforme |
| Selecao proibida | Conforme |
| Registry de acoes proibido | Conforme |
| Registry de tipos proibido | Conforme |
| Execucao de chips proibida | Conforme |
| Navegacao por `tela_destino` proibida | Conforme |
| Dashboard dinamico proibido | Conforme |
| Mudanca de estilo em runtime proibida | Conforme |
| Interface interativa proibida | Conforme |
| `curses`, `textual`, `rich` ou biblioteca de UI proibidos | Conforme |
| Renderer visual final proibido | Conforme |
| Teste integrado novo exigido | Conforme |
| Regressao dos testes H-0001, H-0002 e H-0003 exigida | Conforme |
| Relatorio IMP-0004 exigido | Conforme |
| Validacao de JSON exigida | Conforme |
| Verificacao de ausencia de `__pycache__` e `.pyc` exigida | Conforme |
| `git status` final exigido | Conforme |

### Bloqueantes novos

Nao foram identificados bloqueantes novos introduzidos pelo ajuste.

### Comandos de verificacao

#### `git status --short`

Saida registrada:

```text
?? docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md
```

Observacao: o handoff e o relatorio de auditoria aparecem como nao rastreados
(`??`). Portanto, `git diff` normal nao mostra esses arquivos por padrao. Essa
condicao nao e falha.

#### `wc -l docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`

Saida registrada:

```text
631 docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
```

#### `wc -l docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md`

Saida registrada:

```text
429 docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md
```

#### `git diff --stat -- docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`

Nao executado como evidencia principal porque o handoff esta nao rastreado;
`git diff` normal nao inclui arquivos untracked por padrao.

#### `git diff --stat -- docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md`

Nao executado como evidencia principal porque o relatorio esta nao rastreado;
`git diff` normal nao inclui arquivos untracked por padrao.

### Conclusao final

HANDOFF_APPROVED_WITH_NOTES

O H-0004 ajustado esta pronto para implementacao pelo GLM/OpenCode. Os dois
bloqueantes anteriores foram resolvidos, os dois achados nao bloqueantes foram
incorporados, as tres observacoes anteriores permanecem apenas informativas e
nao ha bloqueantes novos.

### Recomendacao objetiva

Seguir para implementacao.
