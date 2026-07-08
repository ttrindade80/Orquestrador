# Relatório de QA — H-0009 Layout por dimensão do terminal e entrada sem echo

## Status

QA_APPROVED_WITH_NOTES

## Escopo auditado

Foi auditada a implementação do ciclo H-0009, limitada a:

- largura opcional em `renderizar_tela`;
- uso da largura calculada do terminal na demo;
- entrada por tecla única em TTY com `termios`/`tty`, sem Enter e sem echo;
- saída por Esc real (`"\x1b"`);
- preservação do modo pipe/subprocess;
- remoção das linhas em branco entre regiões visuais;
- preservação do diagnóstico não interativo;
- ausência de avanço para dashboard real, lançador, navegação, registry, bindings ativos, pop-up, processamento, filtros, paginação funcional, seleção ou UI externa.

Nenhum arquivo fora da leitura autorizada foi consultado.

## Arquivos lidos

- `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0009_HANDOFF.md`
- `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/diagnostico.py`
- `tela/teste_diagnostico.py`
- `config/telas/orquestrador.json`

## Comandos executados

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
python tela/diagnostico.py
printf 'b\ns\n' | python tela/demo.py
printf 'b\n\x1b\n' | python tela/demo.py
grep -R "config/estilo.json\|config/barra_de_menus.json\|config/layout_console.json\|config/lancador.json" -n tela docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md || true
grep -R "curses\|textual\|rich\|SIGWINCH\|layout_console\|lancador" -n tela || true
grep -R "registry\|binding\|bindings\|tela_destino\|naveg" -n tela/demo.py tela/teste_demo.py || true
grep -R "termios\|tty\|get_terminal_size\|isatty\|read(1)\|\\x1b" -n tela/demo.py tela/teste_demo.py || true
grep -R "\"\\n\\n\"" -n tela/renderizador.py tela/teste_renderizador.py tela/demo.py tela/teste_demo.py tela/teste_diagnostico.py || true
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --stat
git diff --name-only
```

Também foi feita uma verificação adicional em pseudo-TTY via sessão interativa do executor: `python tela/demo.py`, envio de `b` sem Enter e envio de Esc sem Enter.

## Resultado dos testes

- `orquestrador.json OK`
- `python tela/teste_loader.py`: 37 passaram, 0 falharam, código 0.
- `python tela/teste_modelo.py`: 30 passaram, 0 falharam, código 0.
- `python tela/teste_renderizador.py`: 65 passaram, 0 falharam, código 0.
- `python tela/teste_diagnostico.py`: 26 passaram, 0 falharam, código 0.
- `python tela/teste_demo.py`: 69 passaram, 0 falharam, código 0.
- `python tela/diagnostico.py`: encerrou com código 0 e imprimiu a tela curva de fallback 42, sem `"\n\n"` entre caixas.
- `find tela -type d -name '__pycache__' -print`: sem saída.
- `find tela -type f -name '*.pyc' -print`: sem saída.

## Demonstração por pipe/subprocess

`printf 'b\ns\n' | python tela/demo.py` encerrou com código 0 e imprimiu render inicial curvo seguido do render reto após `b`, ambos com largura 80, sem linha vazia entre caixas.

`printf 'b\n\x1b\n' | python tela/demo.py` encerrou com código 0 e produziu saída visual idêntica à execução com `b\ns\n`. Isso confirma que Esc real (`"\x1b"`) marca saída e que `s` permanece apenas como atalho auxiliar de pipe/teste.

## Verificação TTY / sem echo

A inspeção de `tela/demo.py` confirma:

- detecção de TTY com `sys.stdin.isatty()`;
- leitura de terminal com `sys.stdin.read(1)`;
- uso de `termios.tcgetattr`, `tty.setraw` e `termios.tcsetattr(..., termios.TCSADRAIN, ...)`;
- restauração do terminal em `finally`;
- ausência de `input(`;
- ausência de `curses`, `textual` e `rich`.

Em pseudo-TTY, `b` alternou a borda sem Enter e não apareceu ecoado; Esc encerrou sem Enter e sem saída adicional. A confirmação visual humana em terminal real não foi realizada neste QA, portanto permanece como nota.

## Verificação de largura dinâmica

`renderizar_tela` tem assinatura:

```python
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva", largura: int | None = None) -> str
```

Chamadas antigas continuam compatíveis:

- `renderizar_tela(modelo)`
- `renderizar_tela(modelo, tipo_borda="curva")`
- `renderizar_tela(modelo, tipo_borda="reta")`

`largura=None` usa `TOTAL_WIDTH = 42`. Largura explícita ajusta cada linha não vazia para o valor informado; os testes cobrem `largura=42` e `largura=60`. A demo calcula largura com:

```python
shutil.get_terminal_size(fallback=(80, 24)).columns
```

O renderer não lê terminal diretamente e não lê configuração de layout.

## Verificação de ausência de linhas em branco entre regiões

`renderizar_tela` concatena `caixa_cabecalho`, `caixa_dashboard` e `caixa_menu` com separadores simples `"\n"`, não `"\n\n"`.

As saídas de `python tela/diagnostico.py`, `printf 'b\ns\n' | python tela/demo.py` e `printf 'b\n\x1b\n' | python tela/demo.py` não apresentam linha vazia entre cabeçalho, dashboard placeholder e barra/menu inferior.

A remoção ficou limitada às linhas entre regiões visuais. Não houve tentativa de resolver R-10 de espaçamento interno neste ciclo.

## Verificação de escopo Git

Antes da criação deste relatório, `git status --short` mostrava:

```text
 M tela/demo.py
 M tela/renderizador.py
 M tela/teste_demo.py
 M tela/teste_diagnostico.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md
?? docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0009_HANDOFF.md
```

`git diff --stat`:

```text
 scripts/tela/demo.py               | 103 +++++++++++++++-------
 scripts/tela/renderizador.py       | 114 ++++++++++++++++---------
 scripts/tela/teste_demo.py         | 171 +++++++++++++++++++++++++++++++++----
 scripts/tela/teste_diagnostico.py  |   2 -
 scripts/tela/teste_renderizador.py |  78 +++++++++++++++--
 5 files changed, 376 insertions(+), 92 deletions(-)
```

`git diff --name-only`:

```text
scripts/tela/demo.py
scripts/tela/renderizador.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_renderizador.py
```

Após este QA, espera-se também a presença de:

```text
docs/relatorios/RELATORIO_QA_H-0009_LAYOUT_TERMINAL_ENTRADA_SEM_ECHO.md
```

Não foi identificado arquivo implementado fora do escopo do H-0009. Os arquivos de handoff, auditoria e implementação aparecem como não rastreados por pertencerem aos artefatos do ciclo.

## Verificação de aderência ao handoff

A implementação adere ao H-0009 nos pontos auditados:

- assinatura nova do renderer preserva compatibilidade;
- fallback 42 permanece determinístico;
- largura explícita funciona;
- demo usa largura calculada do terminal;
- renderer não lê terminal nem configs;
- separação `"\n\n"` entre caixas foi removida;
- diagnóstico permanece não interativo e determinístico;
- `processar_comando(..., "b")` alterna borda;
- `processar_comando(..., "\x1b")` marca saída;
- `processar_comando(..., "s")` é mantido como atalho auxiliar;
- comandos desconhecidos e maiúsculos não têm efeito;
- `renderizar_estado(..., largura=...)` delega para `renderizar_tela(..., largura=...)`;
- modo pipe/subprocess foi preservado;
- estado de borda permanece apenas em memória;
- não há escrita em arquivo pela demo;
- `config/telas/orquestrador.json` permanece válido e sem alteração observada;
- não há uso de biblioteca externa de UI.

## Achados

### Bloqueantes

Nenhum.

### Não bloqueantes

1. A confirmação visual humana em TTY real não foi realizada neste QA. A simulação em pseudo-TTY corroborou `b` sem Enter/echo e Esc sem Enter/echo, mas não substitui a validação manual visual exigida como nota pelo próprio ciclo.
2. Os comandos `grep` recomendados retornaram ocorrências em docstrings, comentários e testes de ausência para termos proibidos como `curses`, `textual`, `rich`, `layout_console`, `lancador`, `registry` e `bindings`. Não foram identificados usos funcionais fora de escopo.

## Avaliação dos pontos críticos

### Nova assinatura do renderer

A assinatura implementada é compatível com `renderizar_tela(modelo, tipo_borda="curva", largura=None)`. Chamadas antigas continuam cobertas por testes e execução.

### Largura dinâmica com fallback determinístico

`largura=None` usa `TOTAL_WIDTH = 42`; `largura=60` produz todas as linhas não vazias com 60 caracteres; a demo usa `shutil.get_terminal_size(fallback=(80, 24)).columns`.

### Entrada sem Enter e sem echo

O caminho TTY usa `tty.setraw` e `sys.stdin.read(1)`. Em pseudo-TTY, `b` alternou sem Enter e não apareceu ecoado.

### Esc real

`"\x1b"` define `saindo=True`, preserva `tipo_borda` e encerra a demo em pipe e pseudo-TTY. Não depende apenas de `s`.

### TTY vs pipe

TTY e pipe estão separados por `sys.stdin.isatty()`. Em pipe, a leitura linha a linha foi preservada e os comandos obrigatórios com `s` e Esc passaram.

### Preservação do diagnóstico

`tela/diagnostico.py` não foi alterado para modo interativo, não lê `sys.stdin`, não usa `input(` e encerra sem entrada do usuário.

### Comandos locais vs ações declarativas

`b`, `s` e Esc permanecem comandos locais da demo. Não há ativação de bindings declarativos do JSON, registry ou navegação.

### Ausência de funcionalidades fora de escopo

Não foi encontrado dashboard real, dados de dashboard, lançador funcional, abertura de tela de teste, navegação entre telas, registry, bindings ativos, execução real de chips, pop-up, tela de processamento, filtros, paginação funcional, seleção, resize reativo completo, layout responsivo complexo nem uso de `curses`, `textual`, `rich` ou biblioteca externa de UI.

## Conclusão

A implementação do H-0009 está aprovada com notas. Todos os testes e inspeções obrigatórios passaram, a demo deixou de ficar presa ao comportamento principal de 42 caracteres, Esc real funciona, a separação `"\n\n"` entre regiões foi removida e os ciclos anteriores não apresentaram regressão.

O status não é `QA_APPROVED` apenas porque a confirmação visual humana em TTY real permanece pendente.

## Recomendação

Manter o ciclo como `QA_APPROVED_WITH_NOTES` até uma execução manual em terminal real confirmar visualmente:

- `b` alterna sem Enter;
- `b` não aparece como echo;
- Esc sai sem Enter;
- Esc não aparece como echo;
- caixas ocupam a largura calculada do terminal;
- não há linha em branco entre caixas.
