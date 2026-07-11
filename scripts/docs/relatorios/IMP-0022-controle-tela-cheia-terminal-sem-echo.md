# IMP-0022 — Controle de tela cheia do terminal sem echo

**Handoff:** H-0022
**Status:** IMPLEMENTADO — PENDENTE_QA_MANUAL
**Data:** 2026-07-10

---

## Arquivos alterados

| Arquivo | Tipo de alteração |
|---|---|
| `tela/demo.py` | Alterado — adicionadas funções de sessão TUI e `main()` reescrito |
| `tela/teste_demo.py` | Alterado — adicionada Seção 7 com 26 novos testes; novos imports |

## Arquivo criado

```
docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
```

---

## Funções criadas ou modificadas

### Novas funções em `tela/demo.py`

**`_ler_tecla_sessao()`**
Lê exatamente um caractere de `sys.stdin` sem gerenciar raw mode. Deve ser chamada somente quando a sessão TUI já estiver ativa (raw mode ativo por `_iniciar_sessao_tui`).

**`_iniciar_sessao_tui(fd_stdin)`**
Salva os atributos originais do terminal via `termios.tcgetattr`, ativa raw mode via `tty.setraw`, emite as sequências ANSI de entrada na sessão TUI e retorna os atributos originais para restauração posterior.

**`_encerrar_sessao_tui(fd_stdin, atributos_originais)`**
Restaura atributos do terminal via `termios.tcsetattr`, emite as sequências ANSI de saída da sessão TUI e executa flush. Cada passo é envolvido em `try/except` independente para garantir execução máxima mesmo em caso de falha parcial.

**`_apresentar_quadro(conteudo)`**
Apresenta um quadro completo da TUI no mesmo espaço visual: move o cursor ao topo via `ESC[H`, escreve o conteúdo sem quebra terminal final e executa flush.

### Função modificada em `tela/demo.py`

**`main()`**
A condição de detecção TTY passou de `sys.stdin.isatty()` para `sys.stdin.isatty() and sys.stdout.isatty()`. O branch TTY agora usa sessão completa: `_iniciar_sessao_tui` → loop com `_ler_tecla_sessao` e `_apresentar_quadro` → `_encerrar_sessao_tui` em `finally`. O branch não-TTY é preservado sem alteração.

---

## Política de detecção TTY

A sessão TUI controlada é ativada somente quando:

```python
sys.stdin.isatty() and sys.stdout.isatty()
```

Quando qualquer uma das condições for falsa:
- `termios.tcgetattr` não é chamado;
- `tty.setraw` não é chamado;
- nenhuma sequência ANSI de sessão é emitida;
- o fluxo não-TTY anterior (leitura linha a linha, `print`) é preservado.

---

## Sequências ANSI utilizadas

### Entrada na sessão

```
\x1b[?1049h   alternate screen
\x1b[?25l     ocultar cursor
\x1b[2J       limpar tela
\x1b[H        cursor no topo (início da sessão)
```

Emitidas em uma única chamada `write`, seguida de `flush`.

### Início de cada quadro

```
\x1b[H        cursor no topo
```

Prefixado ao conteúdo do quadro em cada chamada a `_apresentar_quadro`.

### Saída da sessão

```
\x1b[?25h     mostrar cursor
\x1b[?1049l   sair do alternate screen
```

Emitidas em uma única chamada `write`, seguida de `flush`.

---

## Estratégia de raw/noecho

Raw mode é ativado uma vez na abertura da sessão via `tty.setraw(fd_stdin)` e permanece ativo durante toda a execução do loop de entrada. Não é ativado e desativado a cada tecla (comportamento anterior de `_ler_tecla_unica`, que foi preservada mas não é mais usada no branch TTY).

A função `_ler_tecla_unica` permanece definida no módulo para compatibilidade e uso fora do contexto de sessão.

---

## Estratégia de apresentação de quadros

Cada quadro é apresentado por `_apresentar_quadro(conteudo)`:

1. Cursor movido ao topo: `\x1b[H`
2. Conteúdo do quadro sem quebra terminal final
3. Flush imediato

Quadros sucessivos substituem o espaço anterior. Não há acumulação de quadros no terminal.

---

## Tratamento da quebra terminal final

O renderer retorna strings que terminam com `\n`. Escrever esse `\n` na última linha física do terminal causa scroll.

`_apresentar_quadro` remove exatamente um `\n` terminal antes de escrever:

```python
quadro = conteudo[:-1] if conteudo.endswith("\n") else conteudo
```

Regras respeitadas:
- Remove somente um `\n` final;
- Não usa `strip()` nem `rstrip()` genérico;
- Não remove espaços de linhas de preenchimento;
- Não altera a string retornada pelo renderer;
- Não afeta o branch não-TTY (que continua usando `print(..., end="")`).

---

## Ordem de restauração

`_encerrar_sessao_tui` executa na seguinte ordem:

1. `termios.tcsetattr(fd_stdin, termios.TCSADRAIN, atributos_originais)` — restaura atributos do TTY
2. `sys.stdout.write("\x1b[?25h\x1b[?1049l")` — mostra cursor e sai do alternate screen
3. `sys.stdout.flush()`

Cada bloco é envolvido em `try/except Exception: pass` para garantir execução máxima mesmo que um passo falhe.

A restauração é garantida pelo `finally` em `main()` para:
- saída normal por Esc;
- exceção durante o loop;
- qualquer erro ocorrido após a ativação da sessão TUI.

---

## Comportamento não-TTY

Preservado sem alteração em relação ao H-0021:
- leitura linha a linha de `sys.stdin`;
- `print(renderizar_estado(...), end="")`;
- nenhuma sequência ANSI de sessão;
- compatível com pipe, subprocess, redirecionamento.

---

## Testes executados

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
```

### Resultados

| Suite | Verificações | Passaram | Falharam |
|---|---|---|---|
| teste_loader.py | (incluído em teste_demo) | — | — |
| teste_modelo.py | 28 | 28 | 0 |
| teste_renderizador.py | 331 | 331 | 0 |
| teste_demo.py | 143 | 143 | 0 |
| teste_diagnostico.py | (incluído em teste_demo) | — | — |

Todos os testes passaram. Os 26 novos testes da Seção 7 cobrem:
- 2.1: entrada no modo TUI (7 verificações)
- 2.2: redesenho de quadros (5 verificações)
- 2.3: quebra terminal final (4 verificações)
- 2.4: restauração normal (3 verificações)
- 2.5: restauração por exceção (3 verificações)
- 2.6: fallback não-TTY (4 verificações)

---

## Verificação manual

**PENDENTE_QA_MANUAL**

O ambiente de execução deste ciclo não permitiu verificação em terminal interativo real. Os critérios manuais a verificar são:

```
1. o conteúdo anterior do shell some ao iniciar;
2. o prompt não aparece durante a execução;
3. as teclas não produzem echo;
4. mudanças de tela permanecem no mesmo espaço;
5. a última linha não faz a interface subir;
6. Esc encerra a aplicação;
7. o conteúdo anterior do shell reaparece;
8. o cursor volta a aparecer;
9. o shell volta a ecoar normalmente;
10. um comando digitado depois da saída funciona normalmente.
```

---

## Limitações conhecidas

Este ciclo não garante recuperação em:
- `SIGKILL` ou queda do processo pelo sistema operacional;
- fechamento abrupto do emulador de terminal;
- falha externa que impeça a execução do `finally`.

---

## Redimensionamento reativo

Não implementado neste ciclo, conforme escopo do H-0022.

O tratamento de `SIGWINCH` e redesenho após redimensionamento da janela pertence ao H-0023.

---

## Próximo ciclo

**H-0023 — Redimensionamento reativo da TUI**
