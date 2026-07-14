# Relatório de QA — H-0007 Alternância de bordas em memória

## Status

QA_APPROVED

## Escopo auditado

QA pós-implementação do ciclo:

```text
H-0007 — Alternância de bordas em memória
```

Foram auditados somente os arquivos autorizados pela solicitação. Não houve
implementação, correção de código, alteração de testes, alteração de
configuração nem alteração documental fora deste relatório de QA.

## Arquivos lidos

```text
docs/handoff/H-0007-alternancia-bordas-memoria.md
docs/relatorios/RELATORIO_AUDITORIA_H-0007_HANDOFF.md
docs/relatorios/IMP-0007-alternancia-bordas-memoria.md
tela/modelo.py
tela/renderizador.py
tela/teste_renderizador.py
tela/diagnostico.py
tela/teste_diagnostico.py
config/telas/orquestrador.json
```

Arquivo adicional lido:

```text
/home/tiago/.codex/attachments/a888e93d-f164-4a98-a019-22ce56dfb890/pasted-text.txt
```

Justificativa: continha a solicitação desta auditoria, a lista restrita de
leitura, os comandos obrigatórios e o formato exigido para este relatório.

Não foram lidos contratos, ADRs, `NOMENCLATURA.md`, `config/estilo.json`,
`config/barra_de_menus.json`, `config/layout_console.json` nem
`config/lancador.json`.

## Comandos executados

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/diagnostico.py
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --stat
git diff --name-only
grep -R "config/estilo.json\|config/barra_de_menus.json\|config/layout_console.json\|config/lancador.json" -n tela docs/relatorios/IMP-0007-alternancia-bordas-memoria.md || true
grep -R "curses\|textual\|rich\|get_terminal_size\|shutil.get_terminal_size\|resize\|terminal" -n tela || true
grep -R "tipo_borda\|_BORDAS\|RenderizadorErro" -n tela/renderizador.py tela/teste_renderizador.py
```

## Resultado dos testes

`python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"`:

```text
orquestrador.json OK
```

`python tela/teste_loader.py`:

```text
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

`python tela/teste_modelo.py`:

```text
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

`python tela/teste_renderizador.py`:

```text
Total de verificacoes: 58
Passaram: 58
Falharam: 0
```

O teste do renderizador confirmou a preservação do expected H-0006 por
igualdade estrita, a equivalência entre default e `tipo_borda="curva"`, a
saída congelada de `tipo_borda="reta"`, linhas visuais com 42 caracteres
Python, alteração restrita aos quatro cantos e erro `RenderizadorErro` para
`"invalida"` e `"CURVA"`.

`python tela/teste_diagnostico.py`:

```text
Total de verificacoes: 26
Passaram: 26
Falharam: 0
```

`python tela/diagnostico.py`:

```text
╭ ORQUESTRADOR ──────────────────────────╮
│ Tela raiz do sistema — ponto de entrada│
╰────────────────────────────────────────╯

╭ DASHBOARD ─────────────────────────────╮
│ Dashboard de teste                     │
│ Sem dados carregados                   │
╰────────────────────────────────────────╯

╭ Menu ──────────────────────────────────╮
│ [Esc] Sair    [B] Borda                │
╰────────────────────────────────────────╯
```

Verificação de cache/bytecode:

```text
find tela -type d -name '__pycache__' -print
(vazio)

find tela -type f -name '*.pyc' -print
(vazio)
```

Nenhum `__pycache__` ou `.pyc` precisou ser removido.

## Verificação de escopo Git

`git status --short`:

```text
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0007-alternancia-bordas-memoria.md
?? docs/relatorios/IMP-0007-alternancia-bordas-memoria.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0007_HANDOFF.md
```

O status corresponde ao esperado para o ciclo: dois arquivos de implementação
modificados e três artefatos H-0007 não rastreados dentro do escopo informado.
O relatório `IMP-0007` existe.

`git diff --stat`:

```text
 scripts/tela/renderizador.py       | 108 +++++++++++++++------
 scripts/tela/teste_renderizador.py | 189 ++++++++++++++++++++++++++++++++++++-
 2 files changed, 267 insertions(+), 30 deletions(-)
```

`git diff --name-only`:

```text
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
```

Não há alteração rastreada em `config/`, JSON de tela, contratos, ADRs,
`NOMENCLATURA.md`, índice, backlog, issues, loader, modelo, diagnóstico,
teste de loader ou teste de modelo.

## Verificação de aderência ao handoff

A assinatura implementada é:

```python
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

`renderizar_tela(modelo)` continua válido, produz exatamente a saída default
H-0006 e é igual a `renderizar_tela(modelo, tipo_borda="curva")`.

A estrutura `_BORDAS` em `tela/renderizador.py` define exatamente os conjuntos
`"curva"` e `"reta"`. A borda curva usa `╭╮╰╯`; a borda reta usa `┌┐└┘`; `│`
e `─` permanecem iguais nos dois conjuntos.

`tipo_borda` inválido lança `RenderizadorErro`, conforme especificado no
handoff. A regra é testada para `"invalida"` e `"CURVA"`.

A saída `"reta"` bate com o expected congelado do handoff. A troca de borda
altera somente os quatro cantos, preservando conteúdo textual, cabeçalho,
dashboard placeholder e menu inferior.

`[B] Borda` permanece apenas texto inerte. Não há captura real da tecla `B`,
loop de aplicação, persistência de estado, ações genéricas, registry,
navegação, `tela_destino`, pop-up, filtros, paginação funcional ou seleção.

Não há leitura operacional de `config/estilo.json`,
`config/barra_de_menus.json`, `config/layout_console.json` ou
`config/lancador.json`. As ocorrências encontradas são declarações negativas
no código/relatório de implementação.

Não há uso de `curses`, `textual`, `rich`, `get_terminal_size`, resize ou
largura real do terminal. As ocorrências de `terminal` são comentários
negativos/descritivos.

Todas as linhas visuais verificadas pelos testes continuam com 42 caracteres
Python. A largura fixa aparece preservada como herança técnica provisória,
com declaração explícita de que não é regra normativa final de layout.

## Achados

### Bloqueantes

Nenhum.

### Não bloqueantes

Nenhum.

## Avaliação dos pontos críticos

### API `tipo_borda`

A API foi implementada com o parâmetro opcional `tipo_borda: str = "curva"`.
Os únicos valores aceitos são `"curva"` e `"reta"`. Valores inválidos lançam
`RenderizadorErro`, com validação case-sensitive.

### Compatibilidade com H-0006

A compatibilidade foi preservada. A chamada default continua válida e bate com
o expected H-0006 por igualdade estrita, incluindo `\n` final. O diagnóstico
continua usando `renderizar_tela(modelo)` sem argumento adicional.

### Borda curva e borda reta

A borda curva usa os cantos `╭`, `╮`, `╰`, `╯`. A borda reta usa `┌`, `┐`,
`└`, `┘`. As bordas vertical e horizontal (`│`, `─`) são comuns aos dois
conjuntos. A saída reta foi validada contra o literal congelado do handoff.

### Tipo de borda inválido

O handoff especifica `RenderizadorErro` para valores fora de `"curva"` e
`"reta"`, incluindo case sensitivity. A implementação cumpre e os testes
cobrem `"invalida"` e `"CURVA"`.

### Chips inertes

`[B] Borda` permanece texto hardcoded inerte no menu inferior. Não há binding,
captura de teclado, alteração de estado nem persistência associada.

### Separação borda × layout

O ciclo ficou restrito à troca de caracteres de borda. Não foram introduzidos
layout responsivo, largura dinâmica, resize, leitura de largura real do
terminal nem leitura de `config/layout_console.json` ou `config/lancador.json`.

### Ausência de funcionalidades fora de escopo

Não foram identificadas ações genéricas, registry, navegação entre telas,
navegação por `tela_destino`, pop-up, filtros, paginação funcional, seleção,
UI interativa, uso de biblioteca de UI, cores ou escape codes ANSI.

## Conclusão

A implementação adere estritamente ao handoff H-0007, preserva os invariantes
H-0001 a H-0006 e mantém o escopo restrito à alternância de bordas em memória.

## Recomendação

Aprovar o ciclo H-0007.
