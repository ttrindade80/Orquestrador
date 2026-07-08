# Relatório de Implementação — H-0009 Layout por dimensão do terminal e entrada sem echo

## Status

IMPLEMENTATION_COMPLETED

## Arquivos alterados

Somente arquivos autorizados pelo handoff H-0009 ("Arquivos permitidos"):

- `tela/renderizador.py` — ALTERADO
- `tela/teste_renderizador.py` — ALTERADO
- `tela/demo.py` — ALTERADO
- `tela/teste_demo.py` — ALTERADO
- `tela/teste_diagnostico.py` — ALTERADO
- `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md` — CRIADO (este arquivo)

`git diff --name-only` confirma exatamente os cinco arquivos de código acima:

```
scripts/tela/demo.py
scripts/tela/renderizador.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_renderizador.py
```

`git diff --stat`:

```
 scripts/tela/demo.py               | 103 +++++++++++++++-------
 scripts/tela/renderizador.py       | 114 ++++++++++++++++---------
 scripts/tela/teste_demo.py         | 171 +++++++++++++++++++++++++++++++++----
 scripts/tela/teste_diagnostico.py  |   2 -
 scripts/tela/teste_renderizador.py |  78 +++++++++++++++--
 5 files changed, 376 insertions(+), 92 deletions(-)
```

## Arquivos não alterados (confirmação dos proibidos)

Confirmados intocados (não lidos para reinterpretação, não alterados):

- `tela/loader.py` (H-0001)
- `tela/modelo.py` (H-0002)
- `tela/diagnostico.py` (H-0004 — permanece não interativo, sem `sys.stdin`, sem `input(`)
- `tela/teste_loader.py` (H-0001)
- `tela/teste_modelo.py` (H-0002)
- `tela/__init__.py`
- `config/telas/orquestrador.json` (inalterado após execução da demo — verificado)
- `config/` (qualquer arquivo)
- `docs/contratos/`, `docs/adr/`, `docs/NOMENCLATURA.md`, `docs/INDICE.md`,
  `docs/backlog.md`, `docs/issues.md`, `docs/handoff/` (qualquer arquivo).

## Resumo da implementação

Implementação estrita do H-0009, sem decisões de arquitetura próprias e sem
ampliação de escopo. Foram corrigidos os quatro problemas apontados pelo handoff:

1. **Largura dinâmica no renderer** — `renderizar_tela` passou a aceitar
   `largura` opcional; `largura=None` usa o fallback determinístico
   `TOTAL_WIDTH = 42` (compatível com H-0006/H-0007/H-0008 e com
   `tela/diagnostico.py`). Quando `largura=W` é fornecida, cada linha
   não-vazia da saída tem exatamente `W` caracteres Python.
2. **Remoção da linha em branco entre caixas** — os separadores `"\n\n"`
   entre caixas/regiões visuais em `renderizar_tela` foram substituídos por
   `"\n"`. As caixas ficam consecutivas. Nenhum espaçamento interno foi
   adicionado ou removido (R-10 permanece fora de escopo).
3. **Entrada por tecla direta na demo (sem Enter, sem echo)** — `main()`
   detecta TTY com `sys.stdin.isatty()`; em TTY, usa `termios`/`tty` em modo
   raw para ler um caractere por vez com `sys.stdin.read(1)`, restaurando o
   terminal em `finally`. Fora de TTY (pipe/testes), preserva a leitura
   linha a linha.
4. **Esc real saindo da demo** — `processar_comando` aceita `"\x1b"` como
   comando de saída (define `saindo=True`, preserva `tipo_borda`). `"s"`
   permanece como atalho auxiliar para pipe/testes. Em TTY, Esc sai sem
   Enter e sem echo.

A largura real do terminal é lida na demo com
`shutil.get_terminal_size(fallback=(80, 24)).columns`. O renderer em si não
lê terminal, não lê config e não lê JSON — somente a demo lê a dimensão do
terminal e a repassa via parâmetro.

## API implementada

### `tela/renderizador.py` — `renderizar_tela`

```python
def renderizar_tela(
    modelo: ModeloTela, tipo_borda: str = "curva", largura: int | None = None
) -> str:
```

Derivação interna (a partir de `total_w = TOTAL_WIDTH if largura is None else largura`):

```python
total_w = TOTAL_WIDTH if largura is None else largura
inner_w = total_w - 2
content_w = total_w - 3
label_max = total_w - 4
```

Retorno (caixas consecutivas, sem `"\n\n"`):

```python
return (
    caixa_cabecalho + "\n"
    + caixa_dashboard + "\n"
    + caixa_menu + "\n"
)
```

As funções auxiliares privadas `_linha_topo`, `_linha_base`, `_linha_conteudo`
e `_caixa` foram refatoradas para receber as dimensões derivadas
(`label_max`, `inner_w`, `content_w`). `TOTAL_WIDTH = 42` permanece como
constante pública de fallback; `INNER_WIDTH`, `CONTENT_WIDTH` e `_LABEL_MAX`
permanecem como marcadores do fallback (sem caráter normativo).

### `tela/demo.py`

```python
def processar_comando(estado, comando):
    novo = {"tipo_borda": estado["tipo_borda"], "saindo": estado["saindo"]}
    if comando == "b":
        novo["tipo_borda"] = "reta" if estado["tipo_borda"] == "curva" else "curva"
    elif comando == "s" or comando == "\x1b":
        novo["saindo"] = True
    return novo


def renderizar_estado(estado, modelo, largura=None):
    return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"], largura=largura)


def _ler_tecla_unica():
    fd = sys.stdin.fileno()
    config_original = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, config_original)
    return ch
```

`main()` (trecho relevante):

```python
estado = criar_estado_inicial()
largura = shutil.get_terminal_size(fallback=(80, 24)).columns
print(renderizar_estado(estado, modelo, largura), end="")

if sys.stdin.isatty():
    while True:
        ch = _ler_tecla_unica()
        estado = processar_comando(estado, ch)
        if estado["saindo"]:
            break
        if ch == "b":
            print(renderizar_estado(estado, modelo, largura), end="")
else:
    for linha in sys.stdin:
        comando = linha.strip()
        estado = processar_comando(estado, comando)
        if estado["saindo"]:
            break
        if comando == "b":
            print(renderizar_estado(estado, modelo, largura), end="")
return 0
```

Importações novas em `tela/demo.py`: `import shutil`, `import termios`,
`import tty` (biblioteca padrão; sem `try/except` — Linux/macOS). Permanece
proibido `json`, `os`, `pathlib`, `curses`, `textual`, `rich`, `subprocess`.

## Decisões não tomadas

Este ciclo **não implementa** explicitamente:

- dashboard real;
- lançador;
- abertura de tela de teste;
- navegação;
- registry;
- bindings declarativos;
- execução real de chips;
- resize reativo completo (sem SIGWINCH);
- layout responsivo complexo;
- leitura de configs de estilo/layout (`config/estilo.json`,
  `config/layout_console.json`, `config/lancador.json`);
- alterações normativas (contratos, ADRs, NOMENCLATURA, índice, backlog, issues);
- espaçamento interno às caixas (conformidade com R-10 do
  `contrato_composicao_corpo.md`) — fora de escopo, conforme nota do handoff.

Nenhuma decisão de arquitetura foi tomada por conta própria. Toda a
implementação segue estritamente o H-0009 e o relatório de auditoria
(`AUDIT_APPROVED_WITH_NOTES`).

## Verificações executadas

Comandos obrigatórios executados a partir da raiz do repositório de scripts
(`scripts/`), em estado limpo (sem `__pycache__`/`.pyc` em `tela/`):

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
printf '' | python tela/demo.py
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --stat
git diff --name-only
```

Resultado dos códigos de saída:

```
orquestrador.json OK
loader=0  modelo=0  render=0  diag=0  demo=0  diagrun=0
pipe_s=0  pipe_esc=0  demo_eof=0
find __pycache__ -> (vazio)
find *.pyc       -> (vazio)
```

## Resultado dos testes

| Suíte                          | Total | Passaram | Falharam | Código |
|--------------------------------|------:|---------:|---------:|-------:|
| `tela/teste_loader.py`         |    37 |       37 |        0 |      0 |
| `tela/teste_modelo.py`         |    30 |       30 |        0 |      0 |
| `tela/teste_renderizador.py`   |    65 |       65 |        0 |      0 |
| `tela/teste_diagnostico.py`    |    26 |       26 |        0 |      0 |
| `tela/teste_demo.py`           |    69 |       69 |        0 |      0 |

Totais acima dos mínimos exigidos pelo H-0009: renderer ≥ 65 (entregue 65);
demo ≥ 58 (entregue 69).

Novas verificações adicionadas:

- `teste_renderizador.py`: 7 de `largura` (`largura=42` igual ao fallback,
  `largura=42` reta, `largura=60` é str, linhas de 60 chars, começa com
  `╭ ORQUESTRADOR`, ausência de `"\n\n"`, `largura=None` equivalente).
- `teste_demo.py`: 4 de `"\x1b"` em `processar_comando`; 4 de `largura` em
  `renderizar_estado`; 3 de subprocess com `"\x1b"`; 1 de ausência de
  `"\n\n"` no stdout; 8 de inspeção de código (`termios`, `tty`,
  `shutil.get_terminal_size`, `isatty`, ausência de `input(`, `curses`,
  `textual`, `rich`).

Invariantes H-0001 a H-0008 preservados (confirmados via `teste_diagnostico.py`
que executa subprocess de `teste_loader.py`, `teste_modelo.py` e
`teste_renderizador.py`).

## Saída real de `python tela/diagnostico.py`

Determinístico, não interativo, sem `"\n\n"` entre caixas, fallback 42 chars:

```
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

Código de saída: `0`. `tela/diagnostico.py` não foi alterado e não contém
`sys.stdin` nem `input(`.

## Saída real de `printf 'b\ns\n' | python tela/demo.py`

Modo não-TTY: `shutil.get_terminal_size(fallback=(80,24))` retorna `columns=80`
(stdout/stderr/stdin são pipes; `COLUMNS` removido do env no teste). Cada linha
não-vazia tem exatamente 80 chars Python; sem `"\n\n"` entre caixas; render
curva inicial seguido do render reta após `b`:

```
╭ ORQUESTRADOR ────────────────────────────────────────────────────────────────╮
│ Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de su│
╰──────────────────────────────────────────────────────────────────────────────╯
╭ DASHBOARD ───────────────────────────────────────────────────────────────────╮
│ Dashboard de teste                                                           │
│ Sem dados carregados                                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
╭ Menu ────────────────────────────────────────────────────────────────────────╮
│ [Esc] Sair    [B] Borda                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
┌ ORQUESTRADOR ────────────────────────────────────────────────────────────────┐
│ Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de su│
└──────────────────────────────────────────────────────────────────────────────┘
┌ DASHBOARD ───────────────────────────────────────────────────────────────────┐
│ Dashboard de teste                                                           │
│ Sem dados carregados                                                         │
└──────────────────────────────────────────────────────────────────────────────┘
┌ Menu ────────────────────────────────────────────────────────────────────────┐
│ [Esc] Sair    [B] Borda                                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

Código de saída: `0`.

## Saída real de `printf 'b\n\x1b\n' | python tela/demo.py`

Em modo não-TTY, `linha.strip()` sobre `"\x1b\n"` produz `"\x1b"`, que
`processar_comando` trata como saída. A saída é **byte a byte idêntica** à
execução com `b\ns\n` (verificado por `diff`):

```
stdout de 'b\n\x1b\n' == stdout de 'b\ns\n': IDENTICAS
```

Código de saída: `0`.

## Ausência de persistência

- `config/telas/orquestrador.json` inalterado após execução da demo
  (verificado por comparação de conteúdo antes/depois em `teste_demo.py`).
- Estado de borda permanece somente em memória (`criar_estado_inicial` sempre
  inicia com `tipo_borda="curva"`; `processar_comando` não usa variável global
  mutável).
- Segunda execução da demo inicia com `tipo_borda="curva"`.

## Confirmação de ausência de `"\n\n"` entre caixas

- `renderizar_tela(modelo)` (fallback 42) não contém `"\n\n"`.
- `renderizar_tela(modelo, largura=60)` não contém `"\n\n"`.
- `python tela/diagnostico.py` não contém linha em branco entre caixas.
- Saída da demo via pipe (curva+reta) não contém `"\n\n"` (largura 80).
- `"\n\n" not in proc.stdout` verificado em `teste_demo.py`.

## Confirmação de largura dinâmica

- `renderizar_tela(modelo, largura=42)` == `renderizar_tela(modelo)`.
- `renderizar_tela(modelo, largura=None)` == `renderizar_tela(modelo)`.
- `renderizar_tela(modelo, largura=60)`: cada linha não-vazia tem 60 chars.
- Demo via pipe usa `largura=80` (fallback de `shutil.get_terminal_size` em
  pipe); cada linha não-vazia do stdout tem 80 chars.
- `tela/diagnostico.py` continua sem `largura` explícita → fallback 42.

## Demonstração manual

A demonstração manual interativa (`python tela/demo.py` em TTY real) depende
de um terminal real, conforme o handoff explicita ("não automatizável por
depender de TTY"). O agente executou `python tela/demo.py` (em contexto
não-TTY, imprime o render inicial e encerra com código 0) e, para obter
evidência automatizada do caminho TTY, executou uma **simulação com
pseudo-terminal (`pty` da stdlib, fora do repositório)** — spawn da demo com
stdin/stdout conectados a um `pty` com winsize 80×24, enviando `b` e `\x1b`
como bytes únicos (sem Enter).

Resultado da simulação pty (corrobora os 6 itens manuais):

| Item manual esperado | Evidência pty | Resultado |
|---|---|---|
| pressionar `b` alterna a borda sem Enter | envio de 1 byte `b` (sem `\n`) produziu saída == `renderizar_tela(modelo,"reta",largura=80)` | OK |
| o caractere `b` não aparece na tela | saída após `b` começa com `┌` (não com `b`); primeiro byte ≠ `0x62` | OK |
| pressionar Esc sai sem Enter | envio de 1 byte `\x1b` (sem `\n`) encerrou o processo | returncode == 0 |
| Esc não aparece na tela | saída após `\x1b` é vazia (sem echo, sem render extra) | OK |
| as caixas ocupam a largura calculada do terminal | render inicial == `renderizar_tela(modelo,"curva",largura=80)` (pty winsize 80) | OK |
| não há linha em branco entre caixas | `b"\n\n" not in` saída inicial | OK |

`TODOS OS CRITERIOS PTY OK: True`. A inspeção de código (Seção 6 de
`teste_demo.py`) confirma a presença de `termios`, `tty`,
`shutil.get_terminal_size`, `isatty` e a ausência de `input(`, `curses`,
`textual`, `rich` em `tela/demo.py`.

> Observação: a simulação pty não substitui a confirmação humana final em um
> terminal real (experiência visual), mas corrobora automaticamente o
> comportamento do caminho TTY exigido pelo H-0009. O modo raw por-leitura
> (`_ler_tecla_unica` restaura o terminal em `finally` a cada tecla) garante
> que o `print` entre leituras ocorra em modo cooked, preservando a
> tradução `\n` → CR+LF e a exibição correta das caixas.

## Nota sobre R-10

A seção 4.6 / R-10 de `contrato_composicao_corpo.md` trata de espaçamento
**interno** às caixas (entre a borda superior e a primeira linha de conteúdo).
O renderer atual é um placeholder que não implementa R-10 — não há linha em
branco interna às caixas. O H-0009 removeu somente as linhas em branco
**entre regiões visuais** (os `"\n\n"` que separavam caixas em
`renderizar_tela`). Nenhum espaçamento interno foi adicionado ou removido.
A conformidade com R-10 permanece tarefa futura (quando o body composer real
for implementado), fora do escopo deste ciclo.

## Observações

- Commit não realizado (responsabilidade do engenheiro, conforme handoff).
- `git status --short` mostra apenas os 5 arquivos autorizados como
  modificados (`M`). Os arquivos `docs/handoff/H-0009-...md` e
  `docs/relatorios/RELATORIO_AUDITORIA_H-0009_HANDOFF.md` aparecem como
  não-rastreados (`??`) por serem entradas do ciclo (handoff + auditoria),
  não criados nem alterados por esta implementação.
- Nenhum `__pycache__` nem `.pyc` em `tela/` após as verificações finais.
- Apenas biblioteca padrão do Python foi usada (`termios`, `tty`, `shutil`,
  `sys`). Nenhum uso de `curses`, `textual`, `rich` ou biblioteca externa.
- `tela/diagnostico.py` não foi alterado e permanece não interativo.

## Resultado final

IMPLEMENTATION_COMPLETED
