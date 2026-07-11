---
name: IMP-0025-distribuicao-vertical-percentual-fracao-corpo
description: "Relatorio de implementacao do H-0024 — distribuicao vertical da altura do corpo (igual/percentual/fracao). Implementacao interrompida: bloqueio arquitetural (ARCHITECTURE_REVIEW_REQUIRED)."
metadata:
  type: relatorio_implementacao
  status: BLOCKED
  handoff_origem: H-0024
  data: 2026-07-11
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_composicao_corpo.md"
  adr_relacionadas:
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
    - docs/adr/ADR-0017-redimensionamento-reativo-tui.md
  bugs_abertos: []
---

# IMP-0025 — Relatorio de Implementacao

## Handoff executado

`H-0024 — Distribuicao vertical da altura do corpo: modos percentual e por fracao`

Autoridade operacional imediata: `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
(QA final `H1_HANDOFF_APPROVED`, proxima categoria `IMPLEMENTAR`).

## Status final

`BLOCKED` — `ARCHITECTURE_REVIEW_REQUIRED`.

A implementacao **nao** foi concluida. Durante a execucao, a semantica
normativa exigida pelo handoff, quando aplicada ao modelo real
`config/telas/orquestrador.json`, entrou em contradicao direta com uma
regressao imutavel obrigatoria (`tela/teste_demo.py`). A contradicao nao pode
ser resolvida dentro do escopo autorizado sem uma decisao arquitetural nao
documentada. Conforme as condicoes de bloqueio do handoff (secao 19) e do
prompt de implementacao, o executor **parou**, **reverteu** as alteracoes de
codigo e registrou o bloqueio.

## Estado Git inicial

Verificado antes da implementacao (conforme secao 2.1/2.2 do handoff):

```text
git branch --show-current      -> master
git rev-parse HEAD             -> 3332773a3f10e716115a164148af323fa86e608f
git log -1 --oneline           -> 3332773 feat: implementa redimensionamento reativo da TUI
git stash list                 -> stash@{0}: On master: pre-H-0022
git status --short:
  ?? docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
  ?? docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md
  ?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md
```

O estado inicial confere integralmente com o esperado. Stage vazio, nenhum
arquivo rastreado modificado, stash preservado. **Nenhuma divergencia de estado**
(portanto o bloqueio **nao** e `BLOCKED_REPOSITORY_STATE`).

## Autoridades utilizadas

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md` (integral);
- `docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md` (integral);
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md` (integral);
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` (Decisoes 5, 6, 7, 8, 9, 10);
- `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md` (evidencia de localizacao);
- `docs/templates/TEMPLATE_RELATORIO_IMPL.md` (estrutura deste relatorio, somente leitura);
- codigo real: `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`,
  `tela/teste_renderizador.py`, `tela/teste_demo.py`.

## Arquivos alterados

Nenhum arquivo rastreado permanece alterado. As alteracoes de codigo feitas
durante a tentativa de implementacao foram **revertidas** (`git checkout --`)
apos a deteccao do bloqueio, para preservar o estado esperado do repositorio.

| Arquivo | Situacao final |
|---|---|
| `tela/loader.py` | revertido a HEAD (sem alteracao) |
| `tela/modelo.py` | revertido a HEAD (sem alteracao) |
| `tela/renderizador.py` | revertido a HEAD (sem alteracao) |
| `tela/teste_loader.py` | nao alterado |
| `tela/teste_modelo.py` | nao alterado |
| `tela/teste_renderizador.py` | nao alterado |
| `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md` | criado (este relatorio) |

## Descricao da implementacao tentada (por camada) — revertida

A implementacao a seguir foi construida, executada e depois **revertida**. E
registrada aqui como evidencia tecnica para a revisao arquitetural. Nenhuma
parte dela permanece no worktree.

### Loader (`tela/loader.py`)

- constante `MODOS_DISTRIBUICAO_CORPO_VALIDOS = {"igual", "percentual", "fracao"}`;
- helper `_eh_numero(valor)` (int/float, excluindo `bool`);
- funcao `_validar_distribuicao_corpo(distribuicao, n_elementos)` reproduzindo as
  validacoes normativas: objeto obrigatorio; `modo` em {igual, percentual, fracao};
  `igual` sem exigencia de `valores`; `percentual`/`fracao` com `valores` lista,
  `len(valores) == n_elementos` (filhos diretos; grupo = 1 slot), todos numericos
  e `> 0`; `percentual` com `sum(valores) == 100`; rejeicao via
  `TelaEstruturaInvalida` (padrao ja usado para `corpo.arranjo`), sem fallback
  silencioso;
- integracao no fluxo de `carregar_tela` e inclusao de `distribuicao` no dict
  `corpo` retornado.

### Modelo (`tela/modelo.py`)

- campo `distribuicao: dict | None = None` no dataclass `Corpo` (apenas
  transporte do dado ja validado; sem calculo, sem revalidacao);
- `construir_modelo` passando `distribuicao=corpo_raw.get("distribuicao")`.

### Distribuicao de altura (`tela/renderizador.py`)

- `_pesos_distribuicao(distribuicao, n_slots)`: ausencia/`igual` -> pesos
  unitarios; `percentual`/`fracao` -> `valores` como pesos;
- `_distribuir_alturas(altura_disponivel, pesos)`: metodo dos maiores restos
  (ADR-0015 D8), soma exata, empates por ordem declarada.

Verificacao isolada do algoritmo (antes da reversao), confirmando os exemplos
normativos do handoff (secao 5.4):

```text
_distribuir_alturas(68, [1, 1, 1])       -> [23, 23, 22]   (exemplo normativo OK)
_distribuir_alturas(68, [2, 1, 2])       -> [27, 14, 27]   (exemplo normativo OK)
_distribuir_alturas(68, [40, 20, 40])    -> [27, 14, 27]   (percentual OK)
_distribuir_alturas(66, [1, 1, 1])       -> [22, 22, 22]   (divisao exata OK)
sum(_distribuir_alturas(101,[3,5,7,11])) -> 101            (invariante de soma OK)
```

### Renderizacao (`tela/renderizador.py`)

- `altura_alvo` propagado por `_caixa_de_elemento` para `_caixa` (default `None`);
- `_montar_corpo_vertical(...)` repartindo a altura util entre os filhos diretos,
  aplicando `altura_alvo` a cada caixa (grupo = 1 slot, altura aplicada ao unico
  interno);
- no ramo vertical de `renderizar_tela`, quando `altura is not None` e ha filhos:
  pre-computa `linhas_barra`, deriva `l_corpo_disponivel`, distribui e empilha as
  caixas dimensionadas; flag `_corpo_vertical_distribuido = True`;
- guarda no fill externo H-0015: nao inserir preenchimento externo quando a
  distribuicao vertical esta ativa;
- `altura is None`: preserva o empilhamento sequencial e o fill externo H-0015.

## Ponto de bloqueio

### Semantica de ausencia e `igual`

O handoff (secoes 5.8, 11.4, 14.6) e o QA pos-patch (achado H2-001 "resolvido")
determinam explicitamente:

```text
ausencia de corpo.distribuicao ≡ modo = "igual" ≡ divisao igual da area
```

e, textualmente (handoff 5.8):

> o comportamento anterior de empilhamento sequencial com preenchimento vertical
> externo (H-0015) **nao** e mais o resultado de ausencia/igual em corpo vertical
> com altura definida: ele e **substituido** pela divisao igual da area.

Portanto o algoritmo de distribuicao **deve** ser ativado para o modelo real
`orquestrador.json` (que declara `corpo.arranjo = "vertical"` e **nao** declara
`corpo.distribuicao`) sempre que `altura` for fornecida.

### Contradicao com a regressao imutavel `tela/teste_demo.py`

Medida real das alturas naturais das caixas do orquestrador (largura 42):

```text
console_principal  (console)   -> 3 linhas
dashboard_info     (dashboard) -> 2 linhas
lancador_principal (lancador)  -> 4 linhas
soma natural                    = 9 linhas
```

Para `altura = 15` (o `n_minimo` usado pela regressao): `l_cab = 3`, `l_barra = 3`,
`l_corpo_disponivel = 9`. A divisao igual normativa entre 3 filhos e:

```text
_distribuir_alturas(9, [1, 1, 1]) = [3, 3, 3]
```

O `lancador_principal` tem altura natural **4**, mas recebe cota **3**. Como
`_caixa` nao trunca (politica existente, handoff 11.4), a caixa ocupa 4 linhas;
a soma renderizada passa a `3 + 3 + 4 = 10 > 9`, e a verificacao determinista
existente (`l_corpo_conteudo > l_corpo_disponivel`) levanta `RenderizadorErro`:

```text
RenderizadorErro: altura insuficiente: corpo requer 10 linhas mas area
disponivel e 9 linhas (altura=15, cabecalho=3, barra=3)
```

Contudo, `tela/teste_demo.py` (arquivo **imutavel**, executavel apenas como
regressao — handoff secoes 8.1, 10, 15) exige, na linha 699:

```text
renderizar_estado(estado_curva, modelo, largura=42, altura=15) -> 15 linhas
(sem fill), identico a renderizar_estado(..., largura=42) [sem altura]
```

ou seja, exige exatamente a **semantica H-0015 antiga** (empilhamento sequencial
+ fill externo) para o orquestrador vertical com `altura`. A execucao com a
semantica nova **aborta a suite** (`teste_demo.py`, exit=1). Verificado tambem
que `tela/teste_renderizador.py::teste_altura_explicita` falha por depender do
fill externo (esse arquivo seria modificavel, mas o de `demo` nao).

### Por que e um bloqueio, e nao um erro de implementacao

O algoritmo esta correto e conforme a norma (exemplos normativos conferem). O
conflito e **entre autoridades**:

1. O handoff **manda** substituir o fill externo H-0015 por divisao igual em
   corpo vertical com altura definida, inclusive para ausencia de `distribuicao`
   (secoes 5.8, 11.4, 14.6; achado H2-001 marcado como resolvido).
2. O proprio handoff tambem **exige** (secao 14.8) que "os testes de altura
   explicita e preenchimento vertical externo H-0015 passam", e preserva
   `tela/teste_demo.py` como regressao imutavel (secoes 8.1, 15) que codifica a
   semantica H-0015 **antiga** para o orquestrador real com altura.

Esses dois requisitos sao **mutuamente exclusivos** para o modelo real. O QA de
handoff registrou explicitamente que **nao executou** as suites (RELATORIO_QA_
POS_PATCH secao 13: "Testes executados nesta etapa: nenhum"), logo a colisao com
`teste_demo.py` nao foi detectada na aprovacao do handoff.

Resolver exigiria uma **decisao arquitetural nao documentada**, entre opcoes que
o executor **nao** esta autorizado a escolher:

- **(a)** isentar ausencia/`igual` no orquestrador real da distribuicao —
  contradiz diretamente o handoff (secao 5.8) e reabre o achado H2-001;
- **(b)** definir **altura minima por elemento** (o `lancador` precisa de >= 4)
  para que a divisao igual nao estoure a cota — **explicitamente fora de escopo**
  (handoff secao 7; ADR-0015 Decisao 11) e condicao de bloqueio direta do prompt:
  "o tratamento de algum caso depender de altura minima ainda nao definida";
- **(c)** alterar `tela/teste_demo.py` para refletir a nova semantica —
  **proibido** (handoff secoes 8.1, 10; prompt).

Todas as saidas caem em condicoes de bloqueio declaradas. Enquadramento:
`ARCHITECTURE_REVIEW_REQUIRED` (autoridade contradiz o handoff; e o caso depende
de altura minima ainda nao normatizada).

## Testes

### Testes automatizados adicionados

Nenhum. O bloqueio foi identificado antes da escrita dos testes obrigatorios
(secao 14 do handoff); nao houve alteracao em `tela/teste_loader.py`,
`tela/teste_modelo.py` nem `tela/teste_renderizador.py`.

### Suites executadas (sobre a implementacao tentada, antes da reversao)

| Suite | Codigo de saida | Resultado |
|---|---|---|
| `python tela/teste_loader.py` | 0 | passou |
| `python tela/teste_modelo.py` | 0 | passou |
| `python tela/teste_renderizador.py` | 1 | falhou (`teste_altura_explicita`, fill externo) |
| `python tela/teste_demo.py` | 1 | falhou (crash em `altura=15`, `RenderizadorErro`) |

As falhas de `teste_renderizador.py` e `teste_demo.py` sao a manifestacao direta
do bloqueio descrito acima, nao defeitos do algoritmo.

### Verificacoes Git (estado final, apos reversao)

| Comando | Resultado | Verificacoes | Codigo de saida |
|---|---|---|---|
| `git diff --check` | sem saida (limpo) | 0 conflitos/espacos | 0 |
| `git diff --stat` | sem saida | 0 arquivos rastreados alterados | 0 |
| `git diff --name-only` | sem saida | 0 arquivos | 0 |
| `git status --short` | 4 arquivos `??` (docs esperados + este relatorio apos criacao) | — | 0 |

## Semantica de ausencia e `igual`

Reproduzida corretamente no algoritmo (pesos unitarios; ausencia == `igual`).
Nao pode ser **entregue** por colidir com a regressao imutavel, conforme o
bloqueio.

## Percentual, fracao e algoritmo de maiores restos

Implementados e verificados isoladamente (exemplos normativos `[1,1,1]`->`[23,23,22]`
e `[2,1,2]`->`[27,14,27]` em 68 linhas conferem; invariante de soma exata; empate
por ordem declarada). Tratamento de linhas residuais: unidades restantes atribuidas
aos maiores restos fracionarios. Preenchimento da area: `altura_alvo` via `_caixa`
(linhas internas bordeadas). Integracao com redimensionamento: funcao pura da
`altura` recebida por `renderizar_tela`, sem cache. Todos revertidos junto com o
restante da implementacao.

## Regressoes verificadas

- `tela/teste_loader.py`: passa com a implementacao (compatibilidade preservada);
- `tela/teste_modelo.py`: passa com a implementacao;
- `tela/teste_renderizador.py`: **falha** em `teste_altura_explicita` (fill externo H-0015);
- `tela/teste_demo.py`: **falha/crash** em `altura=15` (imutavel) — nucleo do bloqueio.

## Validacao manual

1. **Testes automatizados** — executados; resultado acima.
2. **Pseudo-TTY** — nao aplicavel (handoff secao 16.2).
3. **Validacao humana em TTY real** — **nao realizada** e nao aplicavel nesta
   etapa: a implementacao nao foi concluida. Permanece **pendente** para um
   eventual ciclo posterior, apos resolucao arquitetural, a verificacao visual
   de (a) distribuicao percentual/fracao ocupando integralmente a altura util;
   (b) ausencia de sobra/rasgo entre molduras; (c) recomputacao ao redimensionar.
   Nenhuma evidencia de usuario foi fornecida; nada e declarado validado.

## Bloqueios

`ARCHITECTURE_REVIEW_REQUIRED`. Detalhado na secao "Ponto de bloqueio".

Sintese: a semantica normativa mandada pelo handoff (ausencia/`igual` ->
divisao igual substituindo o fill externo H-0015 em corpo vertical com altura),
aplicada ao `orquestrador.json` real, quebra a regressao imutavel
`tela/teste_demo.py` (que codifica a semantica H-0015 antiga) e, no caso-limite
`altura=15`, so poderia ser conciliada definindo **altura minima por elemento**
— conceito fora de escopo e nao normatizado. A resolucao exige decisao
arquitetural/documental que o executor nao esta autorizado a tomar.

## Divergencias entre o handoff e o repositorio

- **Divergencia normativa interna do handoff**: secao 14.8 ("os testes de altura
  explicita e preenchimento vertical externo H-0015 passam") e incompativel com
  as secoes 5.8/11.4/14.6 (substituir o fill externo H-0015 por divisao igual em
  corpo vertical com altura) para o modelo real.
- **Divergencia handoff x regressao imutavel**: `tela/teste_demo.py` (proibido de
  alterar, executavel so como regressao) afirma a semantica H-0015 antiga para o
  orquestrador vertical com `altura`, contradizendo a semantica nova exigida.
- **Lacuna de altura minima**: o orquestrador real (com `lancador` de altura
  natural 4) so distribui igualmente sem erro se houver altura minima por
  elemento — conceito registrado como futuro (ADR-0015 Decisao 11) e fora de
  escopo (handoff secao 7).

Nenhuma dessas divergencias foi resolvida por este executor: o handoff nao pode
ser alterado, ADR/contrato nao podem ser criados/corrigidos e `teste_demo.py`
nao pode ser modificado.

## Observacoes para o revisor arquitetural

Decisoes possiveis a serem tomadas pela autoridade competente (nenhuma escolhida
aqui):

1. redefinir a semantica de ausencia/`igual` em corpo vertical com altura para o
   modelo real (ex.: manter H-0015 quando `distribuicao` ausente), com o
   respectivo patch normativo e atualizacao do handoff; ou
2. normatizar **altura minima por elemento** (ex.: cada area >= altura natural do
   elemento) e o comportamento quando a soma dos minimos excede a area util; ou
3. autorizar a atualizacao de `tela/teste_demo.py`/`teste_altura_explicita` para
   a nova semantica H-0015-substituida, com registro normativo explicito de que
   o fill externo antigo deixa de valer para corpo vertical com altura.

A escolha entre elas altera contrato/ADR e/ou o handoff e esta fora da autoridade
do executor de implementacao.
