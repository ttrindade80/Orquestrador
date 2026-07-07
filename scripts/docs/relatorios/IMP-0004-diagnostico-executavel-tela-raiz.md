# IMP-0004 — Diagnóstico executável da tela raiz

Status: APROVADO_COM_RESSALVAS
Handoff: `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
Auditoria prévia: `docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md`
(status `HANDOFF_APPROVED_WITH_NOTES`, sem bloqueantes pendentes)
Data: 2026-07-07
Executor: implementador GLM/OpenCode (executor estrito)

---

## 1. Objetivo do H-0004

**Especificado**: criar um ponto de entrada mínimo e auditável que encadeie
integralmente o pipeline dos ciclos anteriores sobre a tela raiz
`"orquestrador"`:

```
config/telas/orquestrador.json
  -> carregar_tela(None, "orquestrador")   [tela/loader.py      — H-0001]
  -> dict (tela_raw)
  -> construir_modelo(tela_raw)            [tela/modelo.py      — H-0002]
  -> ModeloTela
  -> renderizar_tela(modelo)               [tela/renderizador.py — H-0003]
  -> str  (saída textual determinística)
```

Expor a função pública `gerar_diagnostico_tela(id_tela="orquestrador") -> str`,
um modo executável `python tela/diagnostico.py` que imprime a string no
stdout e encerra com código 0, e um teste integrado
`tela/teste_diagnostico.py` que valide a cadeia ponta a ponta. Nenhuma
lógica nova além do encadeamento.

**Implementado**: exatamente o especificado. A função
`gerar_diagnostico_tela` encadeia diretamente `carregar_tela` →
`construir_modelo` → `renderizar_tela`; o bloco `__main__` imprime e
termina com `sys.exit(0)`; o teste integrado cobre todas as verificações
obrigatórias da tabela do handoff.

---

## 2. Arquivos criados

- `tela/diagnostico.py` — ponto de entrada executável (função
  `gerar_diagnostico_tela` + bloco `__main__`).
- `tela/teste_diagnostico.py` — diagnóstico integrado (27 verificações).
- `docs/relatorios/IMP-0004-diagnostico-executavel-tela-raiz.md` — este
  relatório.

## 3. Arquivos alterados

Nenhum. `git diff --stat` retorna vazio (saída na seção 8). Nenhum arquivo
rastreado foi modificado.

## 4. Arquivos preservados explicitamente (somente leitura)

Conforme "Proibição absoluta de alteração de módulos herdados" do handoff,
os arquivos abaixo não foram tocados:

- `tela/loader.py` (H-0001)
- `tela/modelo.py` (H-0002)
- `tela/renderizador.py` (H-0003)
- `tela/__init__.py`
- `tela/teste_loader.py` (H-0001)
- `tela/teste_modelo.py` (H-0002)
- `tela/teste_renderizador.py` (H-0003)
- `config/telas/orquestrador.json`
- `config/estilo.json` (e demais `config/*.json`)
- `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md`,
  `docs/issues.md`
- todos os arquivos em `docs/contratos/`, `docs/adr/`, `docs/handoff/`,
  `docs/templates/`

---

## 5. Descrição objetiva da implementação

### 5.1 `tela/diagnostico.py`

Assinatura exata:

```python
def gerar_diagnostico_tela(id_tela: str = "orquestrador") -> str:
    tela_raw = carregar_tela(None, id_tela)
    modelo = construir_modelo(tela_raw)
    return renderizar_tela(modelo)
```

Módulos importados no topo:

```python
import sys

sys.dont_write_bytecode = True

# (bootstrap de sys.path restrito a __main__ — ver seção 10, ressalva 1)

from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
```

Bloco `__main__`:

```python
if __name__ == "__main__":
    resultado = gerar_diagnostico_tela()
    print(resultado, end="")
    sys.exit(0)
```

Comportamento:

- Sem efeitos colaterais: não altera JSON, não executa ação, não ativa
  binding, não navega por `tela_destino`, não aplica filtro, não grava
  arquivo.
- Determinismo: dada a mesma `id_tela` e o mesmo JSON em disco, retorna
  sempre a mesma string (verificado por MD5 na seção 8).
- Propagação de exceções: `TelaErro` e derivadas (H-0001),
  `ModeloTelaErro` (H-0002) e `RenderizadorErro` (H-0003) propagam
  naturalmente — não há `try/except`, relançamento ou transformação.
- Proibições de importação respeitadas: não importa `json`, `os`,
  `pathlib`, nem usa `subprocess`, `exec(` ou `eval(` (verificado pelos
  testes "Proibicoes de import").

### 5.2 `tela/teste_diagnostico.py`

- Define `sys.dont_write_bytecode = True` antes de qualquer import.
- Usa apenas stdlib + `tela.diagnostico` (+ subprocess da stdlib).
- Imprime `[PASSOU] <nome>` ou `[FALHOU] <nome>` para cada verificação.
- Imprime ao final `Total de verificacoes`, `Passaram`, `Falharam`.
- Retorna código 0 se todas passam, 1 se alguma falha.
- Sem `unittest`/`pytest`.
- **Pré-condição obrigatória**: antes de qualquer teste sobre o
  diagnóstico, executa via `subprocess.run` os três ciclos anteriores
  (`tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`)
  e confirma código de saída 0 em cada um.
- Verifica o modo executável `python tela/diagnostico.py` via
  `subprocess.run([sys.executable, "tela/diagnostico.py"], capture_output=True)`
  exigindo igualdade estrita entre o stdout e a string retornada por
  `gerar_diagnostico_tela()`.
- 27 verificações no total, todas cobertas pela tabela obrigatória do
  handoff mais as proibições de importação (também previstas nos critérios
  de aceite).

### 5.3 Saída real do pipeline para `orquestrador.json`

Reprodução literal da string retornada por `gerar_diagnostico_tela()`
(idêntica ao stdout de `python tela/diagnostico.py` e à saída validada no
H-0003; termina com `\n` após `chip_ajuda`):

```
TELA: orquestrador
SCHEMA: tela.v1

CABECALHO
  titulo: Orquestrador
  descricao: Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de survey

CORPO
  arranjo: sobreposto
  elementos:
    - id: console_principal | tipo: console
    - id: dashboard_info | tipo: dashboard
    - id: lancador_principal | tipo: lancador

BARRA_DE_MENUS
  chips:
    - id: chip_esc | texto: Sair
    - id: chip_paginas | texto: Páginas
    - id: chip_colunas | texto: Colunas
    - id: chip_grupos | texto: Grupos
    - id: chip_alternar | texto: Alternar
    - id: chip_navegar | texto: Navegar
    - id: chip_selecionar | texto: Selecionar
    - id: chip_enter | texto: Todos
    - id: chip_estilo | texto: Estilo
    - id: chip_verboso | texto: Verboso
    - id: chip_ajuda | texto: Ajuda
```

Determinismo confirmado por MD5 duplo (saída em arquivo + saída direta),
ambos `433bd34b400b71584ca802d575769b79`, 796 bytes.

---

## 6. Invariantes de H-0001, H-0002 e H-0003

Confirmados por execução direta e também reconfirmados como subprocess
pelo próprio `teste_diagnostico.py` (pré-condição obrigatória):

| Ciclo | Script | Total | Passaram | Falharam | Exit |
|---|---|---|---|---|---|
| H-0001 | `python tela/teste_loader.py` | 37 | 37 | 0 | 0 |
| H-0002 | `python tela/teste_modelo.py` | 30 | 30 | 0 | 0 |
| H-0003 | `python tela/teste_renderizador.py` | 39 | 39 | 0 | 0 |

---

## 7. Comportamento fora de escopo — preservado como inerte

Todos os itens abaixo permanecem **não implementados**, conforme
"Fora de escopo" do handoff. O H-0004 apenas encadeia o pipeline existente;
nenhum deles é ativado, resolvido ou executado:

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
- layout final responsivo completo;
- interface interativa;
- `curses`, `textual`, `rich` ou qualquer biblioteca de UI;
- escape codes ANSI / cores de terminal;
- alteração de JSON em runtime;
- qualquer estado de runtime (cursor, página, filtro ativo, seleção, foco);
- validação funcional de campos pendentes (DOC-B008 / DOC-B009).

Razão de cada um ser mantido inerte: o handoff H-0004 proíbe explicitamente
todos eles e autoriza apenas o encadeamento `carregar_tela` →
`construir_modelo` → `renderizar_tela`. Os módulos subjacentes (loader,
modelo, renderizador) já preservam esses campos como declaração inerte em
`_raw` / `_campos_inertes`; o diagnóstico apenas os atravessa sem toque.

## 7.b Pendências preservadas

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
  saída (teste "campos inertes nao vazam na saida" — PASSOU).

---

## 8. Saída real de todos os comandos de verificação

Executados a partir de
`/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`.

### 8.1 Integridade dos JSONs

```
$ python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
orquestrador.json OK
$ python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"
estilo.json OK
```

### 8.2 `python tela/teste_loader.py`

```
EXIT=0
== Resumo ==
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

### 8.3 `python tela/teste_modelo.py`

```
EXIT=0
== Resumo ==
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

### 8.4 `python tela/teste_renderizador.py`

```
EXIT=0
== Resumo ==
Total de verificacoes: 39
Passaram: 39
Falharam: 0
```

### 8.5 `python tela/teste_diagnostico.py`

```
Diagnostico H-0004 - ponto de entrada executavel da tela raiz
Base padrao: /home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
Python: 3.14.6

== Invariantes dos ciclos anteriores (subprocess) ==
[PASSOU] invariantes H-0001 preservados (tela/teste_loader.py retorna 0) - returncode=0
[PASSOU] invariantes H-0002 preservados (tela/teste_modelo.py retorna 0) - returncode=0
[PASSOU] invariantes H-0003 preservados (tela/teste_renderizador.py retorna 0) - returncode=0

== gerar_diagnostico_tela sobre orquestrador.json ==
[PASSOU] gerar_diagnostico_tela() nao lanca excecao
[PASSOU] retorno e str - tipo=str
[PASSOU] resultado comeca com 'TELA: orquestrador'
[PASSOU] resultado contem 'SCHEMA: tela.v1'
[PASSOU] resultado contem 'CABECALHO'
[PASSOU] resultado contem 'titulo: Orquestrador'
[PASSOU] resultado contem 'CORPO'
[PASSOU] resultado contem 'arranjo: sobreposto'
[PASSOU] resultado contem 'id: console_principal | tipo: console'
[PASSOU] resultado contem 'id: dashboard_info | tipo: dashboard'
[PASSOU] resultado contem 'id: lancador_principal | tipo: lancador'
[PASSOU] resultado contem 'BARRA_DE_MENUS'
[PASSOU] resultado contem 'id: chip_esc'
[PASSOU] resultado contem 'id: chip_ajuda'
[PASSOU] resultado e deterministico (duas chamadas identicas)
[PASSOU] resultado bate com saida esperada do H-0003 (igualdade estrita)
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
EXIT=0
```

### 8.6 `python tela/diagnostico.py`

```
EXIT=0
(saída: a string literal da seção 5.3; 796 bytes; MD5 433bd34b400b71584ca802d575769b79)
```

### 8.7 Verificação de bytecode

```
$ find tela -type d -name '__pycache__' -print
(saída vazia)

$ find tela -type f -name '*.pyc' -print
(saída vazia)
```

Ausência confirmada. `sys.dont_write_bytecode = True` está definido em
`tela/diagnostico.py` (antes dos imports `tela.*`) e em
`tela/teste_diagnostico.py` (antes de qualquer import); os subprocessos
herdam o flag em seus próprios processos.

### 8.8 Estado do repositório

```
$ git status --short
?? docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md
?? tela/diagnostico.py
?? tela/teste_diagnostico.py
```

Os dois primeiros arquivos untracked (`docs/handoff/H-0004-...` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0004_HANDOFF.md`) **não foram
criados por esta implementação** — já estavam presentes no repositório
antes do início do H-0004 (são, respectivamente, o handoff aprovado e o
relatório de auditoria prévia que aprova o handoff). Os arquivos criados
por esta implementação são apenas `tela/diagnostico.py` e
`tela/teste_diagnostico.py` (e este relatório IMP-0004, recém-criado).

```
$ git diff --stat
(saída vazia — nenhum arquivo rastreado modificado)
```

---

## 9. Validação de JSON

- `config/telas/orquestrador.json`: JSON válido (não alterado).
- `config/estilo.json`: JSON válido (não alterado, não consultado pelo
  diagnóstico — incluído por completude como regressão documental herdada
  dos ciclos anteriores).

## 10. Ressalvas objetivas

### Ressalva 1 — bootstrap de `sys.path` no módulo executável (necessário)

A estrutura de topo prescrita literalmente pelo handoff para
`tela/diagnostico.py`:

```
import sys
sys.dont_write_bytecode = True
from tela.loader import carregar_tela
...
```

**não é, por si só, suficiente** para que `python tela/diagnostico.py`
funcione. Em CPython, ao executar `python tela/diagnostico.py`, Python
coloca em `sys.path[0]` o diretório do script (`tela/`, absolutizado), e
**não** o diretório de trabalho corrente. Logo, `from tela.loader import
...` falha com `ModuleNotFoundError: No module named 'tela'`. Comportamento
verificado empiricamente neste ambiente (Python 3.14.6).

Isso cria uma tensão entre dois requisitos do próprio handoff:
- o critério de aceite exige `python tela/diagnostico.py` imprima e saia
  com código 0;
- a estrutura prescrita não contém bootstrap de `sys.path`.

O handoff resolve explicitamente essa classe de tensão ao autorizar, na
seção "Estrutura esperada de `tela/diagnostico.py`": *"O executor pode
ajustar a estrutura interna (ex.: adicionar docstrings), desde que o
comportamento externo seja exatamente o especificado."*

Sob essa autorização, foi adicionado um bootstrap mínimo, **restrito a
`if __name__ == "__main__":`**, que computa a raiz do repositório de
scripts (pai de `tela/`) a partir de `__file__` e a insere em `sys.path`
antes dos imports `tela.*`:

```python
if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)
```

Características do bootstrap:
- usa **apenas `sys`** (módulo já autorizado pelo handoff);
- **não importa** `os`, `pathlib`, `json`, nem usa `subprocess`/`exec`/
  `eval` — todas as proibições de importação do H-0004 permanecem
  satisfeitas (verificadas pelos testes "Proibicoes de import");
- **não adiciona lógica de negócio** alguma — apenas ajusta o caminho de
  importação para que os imports prescritos resolvam;
- é **idempotente e restrito ao modo script**: quando o módulo é importado
  como `tela.diagnostico` (pelo teste), `__name__ != "__main__"` e o
  bootstrap é pulado (o importador já colocou a raiz no `sys.path`);
- espelha a **mesma convenção** já adotada por `tela/teste_loader.py`,
  `tela/teste_modelo.py` e `tela/teste_renderizador.py` (que usam
  `pathlib` para o mesmo fim; aqui o bootstrap é ainda mais restrito por
  usar apenas `sys`).

Sem esse bootstrap, o critério de aceite "modo executável" seria
impossível. Esta é a única adaptação interna além de docstrings, e está
documentada no próprio código-fonte do módulo.

### Ressalva 2 — uso de `subprocess` no teste integrado

O handoff contém uma tensão de redação entre:
- a tabela de verificações (linha 17), que **exige** verificar o modo
  executável via
  `subprocess.run(["python", "tela/diagnostico.py"], capture_output=True)`;
- e o parágrafo posterior que diz que "o único uso autorizado de
  subprocess" seria para as três verificações de invariantes
  (H-0001/H-0002/H-0003).

O prompt de execução recebido pelo executor também explicita: *"O teste do
modo executável deve usar `subprocess.run(..., capture_output=True)`, se o
handoff assim especificar."* — confirmando `subprocess` para a verificação
do modo executável.

Interpretação adotada (não há decision nova, apenas reconciliação de
texto): "único uso autorizado de subprocess" restringe o uso de subprocess
para **invocar outros módulos de teste além dos três listados**; a
verificação do modo executável de `tela/diagnostico.py` é autorizada
separadamente pela linha explícita da tabela. `subprocess` é usado em
`tela/teste_diagnostico.py` exclusivamente para: (a) os três invariantes
H-0001/H-0002/H-0003, e (b) a anti-regressão do modo executável de
`tela/diagnostico.py`. Nenhum outro uso de subprocess.

---

## 11. Conclusão

H-0004 implementado conforme o handoff aprovado
(`HANDOFF_APPROVED_WITH_NOTES`). Cadeia H-0001 → H-0002 → H-0003 →
diagnóstico executável funcionando de ponta a ponta, com saída textual
determinística idêntica à validada no H-0003. Todos os invariantes dos
ciclos anteriores preservados (37 + 30 + 39 = 106 verificações), mais 27
verificações próprias do H-0004. Nenhum arquivo fora do escopo autorizado
foi criado ou alterado. Nenhum `__pycache__`/`.pyc` residual. Commit não
realizado (responsabilidade do engenheiro, conforme handoff).

Resultado final: **APROVADO_COM_RESSALVAS** — ressalvas 1 e 2 da seção 10,
objetivas e não bloqueantes, ambas decorrentes de tensões de redação
internas do handoff e resolvidas no menor escopo possível sem decision
nova de arquitetura.
