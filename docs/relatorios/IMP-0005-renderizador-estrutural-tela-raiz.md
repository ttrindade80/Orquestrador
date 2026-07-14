# IMP-0005 — Renderer estrutural mínimo da tela raiz

Status: APROVADO
Handoff: `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
Auditoria prévia: `docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md`
(status `HANDOFF_APPROVED_WITH_NOTES`, sem bloqueantes pendentes)
Data: 2026-07-07
Executor: implementador GLM/OpenCode (executor estrito)

---

## 1. Identificação do ciclo H-0005

Ciclo **H-0005 — Renderer estrutural mínimo da tela raiz**. Evolui o
renderer textual estático (H-0003) para uma representação **estrutural**
com regiões nomeadas (`REGIAO: cabecalho`, `REGIAO: corpo`,
`REGIAO: barra_de_menus`) e componentes tipados na forma `[{tipo}] {id}`
e chips na forma `[{id}] {texto}`. A função pública
`renderizar_tela(modelo: ModeloTela) -> str` mantém assinatura, contrato
de entrada (`ModeloTela`) e determinismo. Sem dependência de terminal,
sem execução de ação, sem ativação de binding, sem consulta a JSON.

---

## 2. Resumo do que foi implementado

**Especificado**: evoluir `tela/renderizador.py` para o formato estrutural
H-0005, atualizar `tela/teste_renderizador.py` para verificar o novo
formato, atualizar `tela/teste_diagnostico.py` para substituir as
verificações de formato H-0003 pelos equivalentes H-0005, e criar este
relatório.

**Implementado**: exatamente o especificado.

- `tela/renderizador.py` — reescrito para emitir regiões nomeadas
  (`REGIAO:`) em vez de rótulos planos; componentes do corpo listados
  como `    [{tipo}] {id}`; chips listados como `    [{id}] {texto}`;
  campos ausentes renderizados como `(ausente)` / `(não declarado)`;
  saída termina com `\n`.
- `tela/teste_renderizador.py` — `_EXPECTED_ORQUESTRADOR` atualizada
  para o formato H-0005; verificações de substring substituídas
  (`CABECALHO`→`REGIAO: cabecalho`, `id: ... | tipo: ...`→`[{tipo}] {id}`,
  `id: chip_esc`→`[chip_esc]`, etc.); modelo fabricado verifica
  `[console] e1` e `[c1] Ok`; demais verificações (erros, proibições de
  importação, inércia, não-vazamento de campos inertes) preservadas.
- `tela/teste_diagnostico.py` — `_EXPECTED_ORQUESTRADOR` atualizada para
  H-0005; tabela de substituição de formato aplicada integralmente;
  pré-condição `H-0003`→`H-0005` no loop de subprocess; demais
  verificações (determinismo, igualdade estrita, modo executável,
  proibições de import, campos inertes) preservadas.

---

## 3. Arquivos alterados

- `tela/renderizador.py` — ALTERADO (novo formato estrutural H-0005).
- `tela/teste_renderizador.py` — ALTERADO (verificações H-0005).
- `tela/teste_diagnostico.py` — ALTERADO (verificações de formato H-0005).
- `docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md` — CRIADO
  (este relatório).

## 4. Confirmação de arquivos não alterados

Conforme "Arquivos proibidos de alterar" do handoff, os arquivos abaixo
**não foram tocados** (confirmado por `git status --short` / `git diff --stat`
na seção 11.8):

- `tela/loader.py` (H-0001)
- `tela/modelo.py` (H-0002)
- `tela/diagnostico.py` (H-0004 — cadeia não muda)
- `tela/__init__.py`
- `tela/teste_loader.py` (H-0001)
- `tela/teste_modelo.py` (H-0002)
- `config/telas/orquestrador.json`
- `config/estilo.json` (e demais `config/*.json`)
- `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md`,
  `docs/issues.md`
- todos os arquivos em `docs/contratos/`, `docs/adr/`, `docs/handoff/`,
  `docs/templates/`

---

## 5. Aderência ao handoff

| Critério do handoff | Status |
|---|---|
| Somente arquivos listados em "Arquivos permitidos" alterados | OK |
| Assinatura `renderizar_tela(modelo: ModeloTela) -> str` mantida | OK |
| `RenderizadorErro(Exception)` mantida | OK |
| Renderer não importa `json`/`os`/`pathlib` nem chama `carregar_tela` | OK |
| Renderer não executa ação, não ativa binding, não altera estado | OK |
| Renderer não acessa campos inertes internos de `ElementoCorpo` | OK |
| Renderer usa exclusivamente `id` e `tipo` dos elementos do corpo | OK |
| `renderizar_tela(None)` lança `RenderizadorErro` | OK |
| Saída começa com `TELA: orquestrador` | OK |
| Segunda linha é `SCHEMA: tela.v1` | OK |
| Regiões `cabecalho`, `corpo`, `barra_de_menus` presentes | OK |
| Componentes como `    [{tipo}] {id}` | OK |
| Chips como `    [{id}] {texto}` | OK |
| Saída determinística (duas chamadas idênticas) | OK |
| Modelo fabricado `id="teste_fabricado"` usa dados do modelo | OK |
| Saída bate com expected output literal (igualdade estrita) | OK |
| `python tela/teste_loader.py` retorna 0 (37 verificações) | OK |
| `python tela/teste_modelo.py` retorna 0 (30 verificações) | OK |
| `python tela/teste_renderizador.py` retorna 0 (formato H-0005) | OK |
| `python tela/teste_diagnostico.py` retorna 0 (verificações atualizadas) | OK |
| `python tela/diagnostico.py` imprime saída H-0005 e encerra com 0 | OK |
| Nenhum `__pycache__`/`.pyc` em `tela/` após os testes | OK |
| `config/telas/orquestrador.json` válido e inalterado | OK |
| `config/estilo.json` válido e inalterado (não carregado pelo renderer) | OK |
| Saída não contém `origem_dados`/`bindings`/`filtros`/`tela_destino`/`regra_existencia` | OK |
| Sem dependência de biblioteca de UI (`curses`/`textual`/`rich`) | OK |
| Commit não realizado | OK |

Notas da auditoria do Codex respeitadas:
1. `config/estilo.json` aparece apenas na verificação documental de JSON
   válido (regressão herdada); o renderer do H-0005 **não** carrega,
   interpreta ou aplica estilo.
2. A ordem de autoridade cita ADRs/H-0001/H-0002 mas não foram lidos para
   reinterpretar arquitetura; nenhuma divergência detectada.

---

## 6. Formato final da saída estrutural

### 6.1 Assinatura da função e módulos importados

`tela/renderizador.py`:

```python
from tela.modelo import ModeloTela


class RenderizadorErro(Exception):
    """Erro de renderizacao estrutural de tela."""


def renderizar_tela(modelo: ModeloTela) -> str:
    ...
```

Único import de terceiro nível: `from tela.modelo import ModeloTela`.
Não importa `json`, `os`, `pathlib`, nem `tela.loader`. Não usa
`subprocess`/`exec`/`eval`. Não abre nem lê arquivos.

### 6.2 Saída real do pipeline para `orquestrador.json`

Reprodução literal da string retornada por
`renderizar_tela(construir_modelo(carregar_tela(None, "orquestrador")))`,
idêntica ao stdout de `python tela/diagnostico.py` (termina com `\n`
após `[chip_ajuda] Ajuda`; 643 bytes; MD5
`e63f5160b0dc07561dc2fc8d5e1037e4`):

```
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

Saída bate byte a byte com o expected output literal definido na seção
"Saída esperada" do handoff H-0005 (igualdade estrita verificada por
`saida == _EXPECTED_ORQUESTRADOR` em ambos os testes).

---

## 7. Invariantes de H-0001 e H-0002

Confirmados por execução direta e também reconfirmados como subprocess
pelo próprio `teste_diagnostico.py` (pré-condição obrigatória):

| Ciclo | Script | Total | Passaram | Falharam | Exit |
|---|---|---|---|---|---|
| H-0001 | `python tela/teste_loader.py` | 37 | 37 | 0 | 0 |
| H-0002 | `python tela/teste_modelo.py` | 30 | 30 | 0 | 0 |

---

## 8. Resultado dos testes do H-0005

`python tela/teste_renderizador.py` — 39 verificações, todas passando:

```
Diagnostico H-0005 - renderer estrutural de tela
Base padrao: /home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
Python: 3.14.6

== Renderer sobre modelo de config/telas/orquestrador.json ==
[PASSOU] renderizar_tela aceita ModeloTela valido sem excecao
[PASSOU] saida e str - tipo=str
[PASSOU] saida comeca com 'TELA: orquestrador'
[PASSOU] saida contem 'SCHEMA: tela.v1'
[PASSOU] saida contem 'REGIAO: cabecalho'
[PASSOU] saida contem 'titulo: Orquestrador'
[PASSOU] saida contem 'descricao:'
[PASSOU] saida contem 'REGIAO: corpo'
[PASSOU] saida contem 'arranjo: sobreposto'
[PASSOU] saida contem '[console] console_principal'
[PASSOU] saida contem '[dashboard] dashboard_info'
[PASSOU] saida contem '[lancador] lancador_principal'
[PASSOU] saida contem 'REGIAO: barra_de_menus'
[PASSOU] saida contem '[chip_esc]'
[PASSOU] saida contem '[chip_ajuda]'
[PASSOU] saida e deterministica (duas chamadas identicas)
[PASSOU] saida bate com expected output literal do handoff H-0005

== Modelo fabricado: renderer usa dados do modelo, nao do JSON ==
[PASSOU] saida fabricada comeca com 'TELA: teste_fabricado' - prefixo='TELA: teste_fabricado\nSCHEMA: tela.v0\n\nR'
[PASSOU] saida fabricada contem 'SCHEMA: tela.v0'
[PASSOU] saida fabricada contem 'arranjo: linear'
[PASSOU] saida fabricada contem '[console] e1'
[PASSOU] saida fabricada contem '[c1] Ok'
[PASSOU] saida fabricada nao menciona orquestrador

== Casos de erro do renderer ==
[PASSOU] renderizar_tela(None) lanca RenderizadorErro - RenderizadorErro: renderizar_tela exige ModeloTela; recebido: NoneType
[PASSOU] renderizar_tela(<dict>) lanca RenderizadorErro - RenderizadorErro: renderizar_tela exige ModeloTela; recebido: dict

== Proibicoes de import/leitura no modulo do renderer ==
[PASSOU] renderer nao importa 'json'
[PASSOU] renderer nao importa 'os'
[PASSOU] renderer nao importa 'pathlib'
[PASSOU] renderer nao importa tela.loader (nao chama carregar_tela)
[PASSOU] renderer nao abre nem le arquivos (open/read_text/read_bytes)
[PASSOU] renderer nao usa subprocess/exec/eval
[PASSOU] renderer nao acessa _campos_inertes dos elementos

== Inercia: renderer nao executa/resolve/ativa ==
[PASSOU] renderizar_tela nao altera modelo._raw
[PASSOU] renderizar_tela nao altera modelo.cabecalho
[PASSOU] renderizar_tela nao altera corpo.elementos
[PASSOU] renderizar_tela nao altera barra_de_menus.chips
[PASSOU] console._campos_inertes preserva origem_dados.referencia == 'pendente' (inerte)
[PASSOU] lancador._campos_inertes['itens'] == [] preservado (inerte)
[PASSOU] saida nao vaza campos inertes (origem_dados/bindings/filtros/tela_destino/regra_existencia)

== Resumo ==
Total de verificacoes: 39
Passaram: 39
Falharam: 0
```

---

## 9. Resultado dos testes do diagnóstico atualizados

`python tela/teste_diagnostico.py` — 27 verificações, todas passando:

```
Diagnostico H-0004 - ponto de entrada executavel da tela raiz
Base padrao: /home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
Python: 3.14.6

== Invariantes dos ciclos anteriores (subprocess) ==
[PASSOU] invariantes H-0001 preservados (tela/teste_loader.py retorna 0) - returncode=0
[PASSOU] invariantes H-0002 preservados (tela/teste_modelo.py retorna 0) - returncode=0
[PASSOU] invariantes H-0005 preservados (tela/teste_renderizador.py retorna 0) - returncode=0

== gerar_diagnostico_tela sobre orquestrador.json ==
[PASSOU] gerar_diagnostico_tela() nao lanca excecao
[PASSOU] retorno e str - tipo=str
[PASSOU] resultado comeca com 'TELA: orquestrador'
[PASSOU] resultado contem 'SCHEMA: tela.v1'
[PASSOU] resultado contem 'REGIAO: cabecalho'
[PASSOU] resultado contem 'titulo: Orquestrador'
[PASSOU] resultado contem 'REGIAO: corpo'
[PASSOU] resultado contem 'arranjo: sobreposto'
[PASSOU] resultado contem '[console] console_principal'
[PASSOU] resultado contem '[dashboard] dashboard_info'
[PASSOU] resultado contem '[lancador] lancador_principal'
[PASSOU] resultado contem 'REGIAO: barra_de_menus'
[PASSOU] resultado contem '[chip_esc]'
[PASSOU] resultado contem '[chip_ajuda]'
[PASSOU] resultado e deterministico (duas chamadas identicas)
[PASSOU] resultado bate com saida esperada do H-0005 (igualdade estrita)
[PASSOU] campos inertes nao vazam na saida (origem_dados/bindings/filtros/tela_destino/regra_existencia)
[PASSOU] gerar_diagnostico_tela('orquestrador') == gerar_diagnostico_tela()

== Modo executavel: python tela/diagnostico.py ==
[PASSOU] modo executavel encerra com codigo de saida 0 - returncode=0
[PASSOU] 'python tela/diagnostico.py' stdout == gerar_diagnostico_tela()

== Proibicoes de import no modulo tela/diagnostico.py ==
[PASSOU] diagnostico nao importa 'json'
[PASSOU] diagnostico nao importa 'os'
[PASSOU] diagnostico nao importa 'pathlib'
[PASSOU] diagnostico nao usa subprocess/exec/eval

== Resumo ==
Total de verificacoes: 27
Passaram: 27
Falharam: 0
```

## 9.b Resultado do modo executável

`python tela/diagnostico.py` — EXIT=0, imprime a string literal da
seção 6.2 (643 bytes; MD5 `e63f5160b0dc07561dc2fc8d5e1037e4`).

---

## 10. Comportamento fora de escopo — preservado como inerte

Todos os itens abaixo permanecem **não implementados**, conforme
"Fora de escopo" do handoff. O H-0005 apenas evolui o formato da saída
estática; nenhum deles é ativado, resolvido ou executado:

- loop de aplicação;
- navegação real entre telas;
- execução de ações declaradas em chips ou itens de lancador;
- registry de ações (`referencias_de_acoes`);
- resolução de `bindings`;
- ativação de filtros funcionais (`filtros[]`);
- paginação funcional;
- seleção funcional;
- registry de tipos de elemento;
- execução de chips;
- navegação por `tela_destino`;
- dashboard dinâmico com dados reais;
- mudança de estilo em runtime;
- carregamento ou aplicação de `config/estilo.json`;
- bordas, molduras ou qualquer primitiva de borda;
- cores ou escape codes ANSI;
- chips visuais finais com aparência definitiva;
- cálculo de largura de terminal ou layout responsivo;
- interface interativa;
- `curses`, `textual`, `rich` ou qualquer biblioteca de UI;
- renderer visual final;
- pop-up;
- tela de processamento;
- seleção de item por cursor;
- qualquer estado de runtime (cursor, página, filtro ativo, seleção, foco);
- leitura direta de `config/telas/orquestrador.json` pelo renderer;
- alteração de JSON em runtime.

Razão de cada um ser mantido inerte: o handoff H-0005 proíbe
explicitamente todos eles e autoriza apenas a evolução do formato da
saída estrutural a partir de `ModeloTela`. Os módulos subjacentes (loader,
modelo) já preservam esses campos como declaração inerte em `_raw` /
campos inertes internos; o renderer apenas atravessa sem toque, usando
exclusivamente `id` e `tipo` dos elementos do corpo.

## 10.b Pendências preservadas

Confirmadas inertes (sem execução, sem resolução, sem erro):

- **DOC-B008**: tipos internos de item de `console` permanecem
  indefinidos; `regra_geracao_itens` do console permanece
  `tipo: "pendente"`.
- **DOC-B009**: `referencias_de_acoes.status` permanece
  `"pendente_DOC-B009"`; nenhuma ação é executada.
- `lancador_principal.itens` permanece `[]`; `tela_destino` do
  `chip_estilo.acao` permanece `"pendente"`.
- `bindings`, `filtros`, `origem_dados.referencia` ("pendente") e
  `regra_existencia` permanecem declarados sem ativação.
- Verificação objetiva: nenhum dos tokens `origem_dados`, `bindings`,
  `filtros`, `tela_destino`, `regra_existencia` aparece na string de
  saída (teste "saida nao vaza campos inertes" — PASSOU em ambos os
  diagnósticos).

---

## 11. Saída real de todos os comandos de verificação

Executados a partir de
`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`.

### 11.1 Integridade dos JSONs

```
$ python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
orquestrador.json OK
$ python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"
estilo.json OK
```

### 11.2 `python tela/teste_loader.py`

```
EXIT=0
== Resumo ==
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

### 11.3 `python tela/teste_modelo.py`

```
EXIT=0
== Resumo ==
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

### 11.4 `python tela/teste_renderizador.py`

```
EXIT=0
== Resumo ==
Total de verificacoes: 39
Passaram: 39
Falharam: 0
```

(Saída integral na seção 8.)

### 11.5 `python tela/teste_diagnostico.py`

```
EXIT=0
== Resumo ==
Total de verificacoes: 27
Passaram: 27
Falharam: 0
```

(Saída integral na seção 9.)

### 11.6 `python tela/diagnostico.py`

```
EXIT=0
(saída: a string literal da seção 6.2; 643 bytes; MD5 e63f5160b0dc07561dc2fc8d5e1037e4)
```

### 11.7 Verificação de bytecode

```
$ find tela -type d -name '__pycache__' -print
(saída vazia)

$ find tela -type f -name '*.pyc' -print
(saída vazia)
```

Ausência confirmada. `sys.dont_write_bytecode = True` está definido em
todos os módulos de teste e em `tela/diagnostico.py` antes dos imports
`tela.*`; os subprocessos herdam o flag em seus próprios processos.

### 11.8 Estado do repositório

```
$ git status --short
 M tela/renderizador.py
 M tela/teste_diagnostico.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md
```

Os dois arquivos untracked (`docs/handoff/H-0005-...` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md`) **não foram
criados por esta implementação** — já estavam presentes no repositório
antes do início do H-0005 (são, respectivamente, o handoff aprovado e o
relatório de auditoria prévia que aprova o handoff). Os arquivos
alterados por esta implementação são apenas `tela/renderizador.py`,
`tela/teste_renderizador.py` e `tela/teste_diagnostico.py` (mais este
relatório IMP-0005, recém-criado).

```
$ git diff --stat
 scripts/tela/renderizador.py       |  46 +++++++++-------
 scripts/tela/teste_diagnostico.py  |  91 ++++++++++++++++---------------
 scripts/tela/teste_renderizador.py | 108 ++++++++++++++++++-------------------
 3 files changed, 128 insertions(+), 117 deletions(-)
```

`git diff --stat` confirma que somente os três arquivos autorizados foram
modificados. Nenhum arquivo fora do escopo foi alterado.

---

## 12. Status final

H-0005 implementado conforme o handoff aprovado
(`HANDOFF_APPROVED_WITH_NOTES`). Cadeia H-0001 → H-0002 → H-0005 →
diagnóstico executável funcionando de ponta a ponta, com saída estrutural
determinística idêntica ao expected output literal do handoff. Todos os
invariantes dos ciclos anteriores preservados (37 + 30 = 67 verificações),
mais 39 verificações próprias do H-0005 e 27 do diagnóstico integrado
(134 verificações no total, todas passando). Nenhum arquivo fora do
escopo autorizado foi criado ou alterado. Nenhum `__pycache__`/`.pyc`
residual. Commit não realizado (responsabilidade do engenheiro, conforme
handoff).

Resultado final: **APROVADO**
