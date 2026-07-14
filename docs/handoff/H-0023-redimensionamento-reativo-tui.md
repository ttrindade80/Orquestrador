---
name: H-0023-redimensionamento-reativo-tui
description: Handoff de implementação — redimensionamento reativo da TUI em tela/demo.py e tela/teste_demo.py conforme ADR-0017: SIGWINCH via pipe de wakeup, cadeia ioctl/TIOCGWINSZ, validação de par, fallback inicial, últimas dimensões válidas, redesenho em redução e ampliação, quadro mínimo de aviso, restauração do handler
metadata:
  type: handoff
  status: proposto
  data: 2026-07-11
rastreabilidade:
  adr_base: docs/adr/ADR-0017-redimensionamento-reativo-tui.md
  adrs_preservadas:
    - docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
  escopo_permitido:
    - tela/demo.py
    - tela/teste_demo.py
  relatorio_implementacao_esperado: docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
---

# H-0023 — Redimensionamento reativo da TUI

## 1. Identificação e objetivo

Implementar o redimensionamento reativo da TUI conforme a ADR-0017, em
`tela/demo.py` e `tela/teste_demo.py`, sem introduzir biblioteca de TUI, sem
alterar ADRs, contratos, nomenclatura, configuração ou schema JSON.

Capacidade coesa: a sessão TTY detecta alterações de tamanho da janela por
`SIGWINCH`, obtém novas dimensões pela cadeia `ioctl(TIOCGWINSZ) →
LINES/COLUMNS → últimas dimensões válidas`, valida o par, redesenha o quadro
quando o par muda, exibe quadro mínimo de aviso quando insuficiente, e recupera
automaticamente a tela normal quando as dimensões voltam a ser suficientes.

## 2. Estado comprovado

### 2.1 Estado anterior à criação do H-0023

Estado do repositório no momento em que este handoff foi criado, antes de o
próprio arquivo existir:

```text
HEAD: de0f023 fix: corrige execução TTY em tela cheia
branch: master
stage: vazio

Arquivos rastreados modificados (não commitados, ciclo documental ADR-0017):
  M docs/NOMENCLATURA.md
  M docs/adr/INDICE_ADR.md
  M docs/contratos/contrato_composicao_corpo.md
  M docs/contratos/contrato_tela_json.md

Arquivos não rastreados (ciclo documental ADR-0017):
  ?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
  ?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
  ?? docs/relatorios/RELATORIO_QA_ADR-0017.md
  ?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md

Último relatório de implementação numérico: IMP-0023-implementacao-h0022-tela-cheia-tty.md
Próximo identificador disponível: IMP-0024
```

### 2.2 Estado posterior à criação e aprovação documental do H-0023

Após a criação deste handoff e do relatório de QA, os seguintes arquivos
adicionais passam a existir como não rastreados:

```text
  ?? docs/handoff/H-0023-redimensionamento-reativo-tui.md
  ?? docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
```

O estado completo esperado no início da implementação é o estado da seção 2.1
acrescido desses dois arquivos adicionais. O stage permanece vazio. O worktree
contém arquivos modificados e não rastreados — não está limpo.

A condição de bloqueio da seção 24 compara o estado real encontrado no início
da implementação com este estado (seção 2.2), não com o estado anterior à
criação documental.

Status do QA da aplicação que autoriza este handoff:
`ADR_APPLICATION_APPROVED_WITH_NOTES`
(RELATORIO_QA_APLICACAO_ADR-0017.md, 2026-07-11)

## 3. Autoridades

Em ordem decrescente de precedência:

1. `docs/adr/ADR-0017-redimensionamento-reativo-tui.md` — autoridade primária
   deste handoff; define gatilho, cadeia de obtenção, validade, fallback,
   redesenho, quadro mínimo e preservações.
2. `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md` — preservada
   integralmente; define a política de sessão TTY que este handoff estende.
3. `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md` — define que
   `altura_disponivel` é dimensão explícita; o mecanismo de obtenção da altura
   durante a sessão está em ADR-0017.
4. `docs/contratos/contrato_tela_json.md` seção 24 — registra a política da
   ADR-0017 aplicada; referência normativa documental.
5. `docs/contratos/contrato_composicao_corpo.md` — regras R-23 e R-24
   registradas na aplicação da ADR-0017.
6. `docs/NOMENCLATURA.md` §6.2 — termos específicos do redimensionamento
   reativo; obrigatório para nomenclatura de funções e constantes.

## 4. Decisão fechada

O H-0023 implementa redimensionamento reativo sem biblioteca de TUI,
conforme ADR-0017.

**Gatilho:** `SIGWINCH` em sessão TTY ativa.

**Fonte primária:** `ioctl(fd, TIOCGWINSZ, ...)` via `fcntl.ioctl` +
`struct.unpack`. Largura e altura são sempre um par coerente.

**Par válido:** ambos presentes, ambos convertíveis em `int`, ambos > 0.

**Cadeia de inicialização:**
```
ioctl(TIOCGWINSZ) → LINES e COLUMNS → fallback fixo (80, 24)
```

**Cadeia após SIGWINCH:**
```
ioctl(TIOCGWINSZ) → LINES e COLUMNS → últimas dimensões válidas
```
O fallback `(80, 24)` não substitui as últimas dimensões válidas em sessão ativa.

**Mecanismo de SIGWINCH:** pipe de wakeup (descrito na seção 13).

**Redesenho:** somente quando o novo par válido difere do estado atual.

**Terminal pequeno demais:** quadro mínimo quando `largura < LARGURA_MINIMA_TELA`
ou `altura < ALTURA_MINIMA_TELA`; recuperação automática quando as dimensões
ficam suficientes; sem encerramento da sessão.

```text
LARGURA_MINIMA_TELA = 10   (derivado da guarda mínima do renderer)
ALTURA_MINIMA_TELA  = 6    (l_cab=3 + l_barra_mínimo=3)
```

## 5. Levantamento do estado atual

### 5.1 Onde a sessão TTY é iniciada e encerrada

`tela/demo.py`:

- `_iniciar_sessao_tui(fd_stdin)` — linha 265: salva `termios.tcgetattr`,
  chama `tty.setcbreak`, escreve `\x1b[?1049h\x1b[?25l\x1b[?7l\x1b[2J\x1b[H`
  para stdout. Retorna os atributos originais.
- `_encerrar_sessao_tui(fd_stdin, atributos_originais)` — linha 279: chama
  `termios.tcsetattr(fd, TCSADRAIN, atributos_originais)`, escreve
  `\x1b[?7h\x1b[?25h\x1b[?1049l`. Cada passo em bloco `try` separado.
- O bloco `finally` em `main()` (linha 357) chama `_encerrar_sessao_tui`
  garantindo restauração em qualquer saída do loop.

### 5.2 Onde largura e altura são lidas atualmente

- `main()` — linhas 334–336: `shutil.get_terminal_size(fallback=(80, 24))`;
  atribui `largura = .columns` e `altura = .lines` antes do bloco TTY.
- `_apresentar_quadro(conteudo)` — linha 305: relê
  `shutil.get_terminal_size(fallback=(80, 24)).columns` a cada chamada.
- Não há SIGWINCH, não há `ioctl`, não há atualização reativa de dimensões.

### 5.3 Onde o loop de entrada processa teclas

`main()` — linha 344: `while True:` com `ch = _ler_tecla_sessao()`. Dentro
do loop, `processar_comando(estado, ch, modelo)` atualiza o estado. Saída por
`break` quando `estado["saindo"]`.

`_ler_tecla_sessao(fd=None)` — linha 209: lê um caractere via
`os.read(fd, 1)` (bloqueante), distingue Esc isolado de sequência de escape
via `select.select([fd], [], [], 0.03)` em follow-up.

### 5.4 Onde o quadro é renderizado

`renderizar_estado(estado, modelo, largura=None, altura=None)` — linha 188:
delega a `renderizar_tela(modelo, tipo_borda=..., largura=largura, altura=altura)`.
`renderizar_tela` retorna string com exatamente `altura` linhas quando `altura`
é fornecida e suficiente.

### 5.5 Onde o quadro é apresentado

`_apresentar_quadro(conteudo)` — linha 296: formata com posicionamento
absoluto CSI n;1H linha a linha, preenche até `w` chars, envolve em
synchronized output (`\x1b[?2026h/l`), emite em uma única `write()` + `flush()`.

### 5.6 Como o `finally` protege a sessão

Bloco `try/finally` em `main()` (linhas 342–358): o `finally` cobre todo o
loop, chamando `_encerrar_sessao_tui(fd, atributos_originais)` em qualquer saída.

### 5.7 Como `KeyboardInterrupt` é tratado

`except KeyboardInterrupt: continue` dentro do loop (linha 355–356):
capturado silenciosamente, sessão continua. `captura_interrupcao_de_script`
(linha 249) para uso futuro em execução de scripts internos.

### 5.8 Como o fluxo não-TTY é separado

Bloco `else` em `main()` (linhas 359–370): leitura linha a linha de
`sys.stdin`, `print(..., end="")` sem sequências ANSI. Completamente separado
do bloco `if sys.stdin.isatty() and sys.stdout.isatty()`.

### 5.9 Como os testes simulam TTY

`tela/teste_demo.py`:
- Testes unitários usam `unittest.mock.patch` para `termios`, `tty`,
  `sys.stdout`, `shutil.get_terminal_size`.
- Testes de integração usam `subprocess.run` com `input=...` e
  `capture_output=True` (modo não-TTY, pipe).
- Testes de pipe real usam `os.pipe()` para validar `_ler_tecla_sessao`.
- Não há testes em pseudo-TTY real — lacuna a ser coberta pelo H-0023.

### 5.10 Quais módulos precisam ser alterados

Apenas `tela/demo.py` e `tela/teste_demo.py`. O renderer (`tela/renderizador.py`)
e o restante do pipeline não precisam de modificação: `renderizar_tela` já
aceita `largura` e `altura` como parâmetros; a lógica de preenchimento vertical
e o quadro mínimo são tratados em `demo.py`.

## 6. Capacidade coesa

O H-0023 entrega uma única capacidade indivisível: a sessão TTY reage a
alterações de tamanho da janela do terminal durante sua execução, atualizando
as dimensões, redesenhando o quadro com as novas dimensões quando válidas, e
exibindo um quadro mínimo de aviso quando as dimensões são válidas mas
insuficientes para a tela normal — com recuperação automática quando as
dimensões voltam a ser suficientes. O fluxo não-TTY e toda a política de sessão
da ADR-0016 permanecem inalterados.

## 7. Arquivos futuros permitidos

Esta lista é exaustiva para código e testes:

```
tela/demo.py          — ALTERAR
tela/teste_demo.py    — ALTERAR
```

O relatório de implementação (`docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md`)
é artefato processual obrigatório; sua criação não amplia o escopo técnico.
Nenhum outro arquivo técnico ou documental pode ser criado ou alterado.

## 8. Arquivos futuros somente para leitura

```
docs/adr/ADR-0017-redimensionamento-reativo-tui.md
docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/NOMENCLATURA.md
tela/renderizador.py
tela/loader.py
tela/modelo.py
config/telas/orquestrador.json
config/telas/destino_minimo.json
config/telas/grupo_minimo.json
```

## 9. Arquivos futuros proibidos

Qualquer arquivo não listado nas seções 7 e 8 está proibido. Em particular:

```
docs/adr/          — nenhuma ADR pode ser criada ou alterada
docs/contratos/    — nenhum contrato pode ser alterado
docs/NOMENCLATURA.md — proibido
docs/relatorios/   — apenas IMP-0024 pode ser criado nesta pasta
docs/handoff/      — nenhum handoff pode ser criado ou alterado
config/            — nenhum JSON de configuração
tela/renderizador.py
tela/loader.py
tela/modelo.py
tela/diagnostico.py
```

## 10. Escopo positivo

O implementador deve:

1. Adicionar `import fcntl`, `import struct`, `import signal` em `tela/demo.py`.
2. Definir as constantes `LARGURA_MINIMA_TELA = 10` e `ALTURA_MINIMA_TELA = 6`
   em nível de módulo em `tela/demo.py`.
3. Implementar `_obter_dimensoes_ioctl(fd)` conforme especificação da seção 15.
4. Implementar `_par_dimensoes_valido(largura, altura)` conforme seção 15.
5. Implementar `_obter_dimensoes_env()` conforme seção 15.
6. Implementar `_obter_dimensoes_iniciais(fd)` conforme seção 15.
7. Implementar `_obter_dimensoes_apos_sigwinch(fd, ultimas_validas)` conforme
   seção 15.
8. Implementar `_instalar_handler_sigwinch(w_wakeup, resize_pendente)` conforme
   seção 13.
9. Implementar `_restaurar_handler_sigwinch(handler_anterior)` conforme seção 13.
10. Implementar `_tela_pequena_demais(largura, altura)` conforme seção 17.
11. Implementar `_quadro_minimo_aviso(largura, altura)` conforme seção 17.
12. Implementar `_resolver_conteudo(estado, modelo, largura, altura)` conforme
    seção 16.
13. Modificar `_apresentar_quadro` adicionando parâmetro `largura=None`
    conforme seção 13.
14. Modificar `main()` — ramo TTY — conforme seção 13: substituir leitura de
    dimensões por `_obter_dimensoes_iniciais`, criar wakeup pipe, instalar e
    restaurar handler de SIGWINCH, substituir `_ler_tecla_sessao()` direto por
    select duplo (`[fd, r_wakeup]`), processar resize no loop.
15. Ramo não-TTY de `main()` permanece com `shutil.get_terminal_size`; não
    instalar handler; não alterar comportamento.
16. Garantir restauração do handler e fechamento do wakeup pipe no `finally`.
17. Implementar todos os testes da seção 19 em `tela/teste_demo.py`.
18. Verificar que todos os testes existentes do H-0022 continuam passando.

## 11. Escopo negativo

O implementador **não deve**:

- Alterar ADRs, contratos, `NOMENCLATURA.md` ou qualquer documento normativo.
- Alterar o schema JSON de qualquer tela.
- Criar novos campos declarativos em `config/`.
- Alterar `corpo.arranjo`, `tiling` ou a composição declarada de qualquer tela.
- Criar fallback de composição baseado na dimensão.
- Inventar ou remover chips.
- Introduzir biblioteca de TUI (`ncurses`, `curses`, `textual`, `rich`).
- Usar `terminfo` ou detecção ampla de capacidades.
- Reintroduzir `\x1b[2J` por quadro ou por redimensionamento.
- Usar `tty.setraw()` ou desligar `ISIG` ou `OPOST`.
- Alterar a política de Ctrl+C (ADR-0016 item 9).
- Alterar a tecla de saída (Esc permanece).
- Modificar `tela/renderizador.py`, `tela/loader.py`, `tela/modelo.py`.
- Executar operações complexas diretamente dentro do handler de SIGWINCH.
- Instalar handler de SIGWINCH no fluxo não-TTY.
- Usar `shutil.get_terminal_size` como fonte primária da dimensão na sessão TTY
  após a inicialização (pode ser mantido como fallback interno de `_apresentar_quadro`
  quando `largura=None`, mas não como fonte normativa primária do ciclo reativo).
- Fazer stage, commit, push ou alteração de histórico Git.
- Refatorar código além do necessário para a capacidade.

## 12. Preservações obrigatórias

As seguintes políticas do H-0022 e da ADR-0016 devem ser preservadas
integralmente sem exceção:

| Política | Localização atual |
|---|---|
| Sessão somente quando stdin e stdout forem TTY | `main()` linha 339 |
| Modo `cbreak`, não `raw`; `ISIG` e `OPOST` preservados | `_iniciar_sessao_tui` linha 273 |
| Alternate screen `\x1b[?1049h/l` | `_iniciar_sessao_tui`, `_encerrar_sessao_tui` |
| Cursor oculto durante a sessão `\x1b[?25l/h` | `_iniciar_sessao_tui`, `_encerrar_sessao_tui` |
| Autowrap desativado durante a sessão `\x1b[?7l/h` | `_iniciar_sessao_tui`, `_encerrar_sessao_tui` |
| Posicionamento absoluto linha a linha `CSI n;1H` | `_apresentar_quadro` linha 311 |
| Preenchimento até a largura corrente | `_apresentar_quadro` linha 313–314 |
| Uma `write()` e um `flush()` por quadro (escrita atômica) | `_apresentar_quadro` linhas 317–318 |
| Synchronized output `\x1b[?2026h/l` em cada quadro | `_apresentar_quadro` linhas 310, 315 |
| `\x1b[2J` somente na entrada da sessão | `_iniciar_sessao_tui` linha 274 |
| Restauração em `finally` | `main()` linhas 357–358 |
| `KeyboardInterrupt` capturado silenciosamente no loop | `main()` linhas 355–356 |
| Saída por Esc | `processar_comando` linha 164 |
| Comportamento não-TTY inalterado | `main()` linhas 359–370 |
| Ausência de echo | preservado pelo `cbreak` |
| Ausência de cintilação perceptível | escrita atômica + synchronized output |

## 13. Mecanismo escolhido para integração de SIGWINCH

### 13.1 Fundamento da escolha

`_ler_tecla_sessao` começa com `os.read(fd, 1)` — chamada bloqueante. Com
PEP 475 (Python 3.5+), `os.read` é reiniciado automaticamente após delivery
de sinal, então um flag simples não desbloquearia a leitura. O mecanismo
escolhido é o **wakeup pipe**: o handler do sinal escreve um byte em um pipe;
o loop principal usa `select.select([fd_stdin, r_wakeup], [], [])` para
acordar ao receber o sinal sem depender do desbloqueio de `os.read`. Isso
permite que operações complexas (ioctl, renderização) permaneçam no loop
principal, fora do handler.

### 13.2 Wakeup pipe

Criado em `main()`, ramo TTY. A sequência normativa completa no ramo TTY é,
nesta ordem:

0. inicializar sentinelas de aquisição antes de qualquer operação que possa
   falhar: `r_wakeup = None`, `w_wakeup = None`, `sessao_iniciada = False`,
   `handler_instalado = False`, `handler_anterior = None`,
   `atributos_originais = None`;
1. obter descritor TTY (`fd = sys.stdin.fileno()`);
2. obter dimensões iniciais;
3. entrar em região protegida por `try/finally`;
4. criar o wakeup pipe (`os.pipe()`); imediatamente após, ambos os descritores
   são considerados recursos a fechar;
5. configurar ambos os descritores como não bloqueantes
   (`os.set_blocking(r_wakeup, False)` e `os.set_blocking(w_wakeup, False)`),
   imediatamente após a criação e antes da instalação do handler;
6. iniciar a sessão TUI (`_iniciar_sessao_tui`); marcar `sessao_iniciada = True`
   somente após retorno bem-sucedido; capturar `atributos_originais` do retorno;
7. instalar o handler (`_instalar_handler_sigwinch`); capturar `handler_anterior`
   do retorno e marcar `handler_instalado = True` somente após retorno
   bem-sucedido;
8. executar o loop;
9. no `finally` (condicional): restaurar o handler somente se
   `handler_instalado`; fechar `r_wakeup` se não for `None`; fechar `w_wakeup`
   se não for `None`; restaurar a sessão TUI somente se `sessao_iniciada`.

O handler somente é instalado depois que o pipe existe e está configurado como
não bloqueante (passo 7 após passos 4 e 5), garantindo que ele nunca escreva
em descritor inexistente nem fique suspenso por pipe cheio. A restauração e o
fechamento ocorrem no `finally` com verificação condicional, garantindo execução
mesmo após exceção em qualquer passo da inicialização.

```python
r_wakeup, w_wakeup = os.pipe()
os.set_blocking(r_wakeup, False)
os.set_blocking(w_wakeup, False)
```

`os.set_blocking(fd, False)` configura `O_NONBLOCK` na camada POSIX (via
`fcntl` internamente). Deve ser chamado para ambos os descritores imediatamente
após `os.pipe()` e antes da instalação do handler. O descritor de escrita não
bloqueante impede que o handler fique suspenso quando o pipe está cheio; o
descritor de leitura não bloqueante permite que a drenagem no loop principal
termine sem aguardar bytes adicionais.

`r_wakeup`: descritor de leitura — monitorado no select do loop principal.
`w_wakeup`: descritor de escrita — passado para o handler de SIGWINCH.

Fechamento condicional no `finally`:

```python
if r_wakeup is not None:
    try:
        os.close(r_wakeup)
    except OSError:
        pass
if w_wakeup is not None:
    try:
        os.close(w_wakeup)
    except OSError:
        pass
```

O teste `is not None` garante que descritores não criados não sejam fechados
como se existissem. Se `os.pipe()` falhar, nenhum fechamento é tentado. Se
`os.pipe()` tiver sucesso mas um `os.set_blocking` falhar, ambos os descritores
já existem e ambos são fechados.

### 13.3 Handler de SIGWINCH

Criado como closure dentro de `_instalar_handler_sigwinch`:

```python
def _instalar_handler_sigwinch(w_wakeup, resize_pendente):
    def _handler(signum, frame):
        resize_pendente[0] = True
        try:
            os.write(w_wakeup, b'\x00')
        except OSError:
            pass
    handler_anterior = signal.signal(signal.SIGWINCH, _handler)
    return handler_anterior
```

- `resize_pendente` é uma lista de um elemento `[False]` criada em `main()`,
  permitindo mutação a partir do closure.
- O handler executa somente operações async-signal-safe: atribuição simples e
  `os.write`. Nenhuma chamada a `ioctl`, renderização, impressão ou loading.
- A flag `resize_pendente[0] = True` é atribuída **antes** da tentativa de
  escrita, garantindo que o estado de resize pendente esteja registrado mesmo
  que a escrita falhe.
- O descritor `w_wakeup` é não bloqueante (configurado na seção 13.2). Se o
  pipe estiver cheio, `os.write` lança `BlockingIOError` (`EAGAIN`/`EWOULDBLOCK`).
  Como `BlockingIOError` é subclasse de `OSError`, o `except OSError: pass`
  já a captura. O handler retorna imediatamente sem bloquear, sem repetir a
  escrita em loop e sem encerrar a aplicação.
- Pipe cheio representa coalescência de notificações, não perda definitiva:
  múltiplos `SIGWINCH` são agrupados em uma única atualização usando o tamanho
  mais recente disponível. A flag `resize_pendente[0]` permanece suficiente
  para indicar que uma atualização deve ocorrer.
- `OSError` diferente de `BlockingIOError` (e.g., pipe fechando durante
  restauração) é igualmente silenciada sem encerrar a aplicação.

### 13.4 Restauração do handler

```python
def _restaurar_handler_sigwinch(handler_anterior):
    try:
        signal.signal(signal.SIGWINCH, handler_anterior)
    except Exception:
        pass
```

Chamado no `finally` de `main()`, antes de `_encerrar_sessao_tui`. Restaura
o handler que existia antes da sessão (tipicamente `signal.SIG_DFL`).

### 13.5 Instalação e restauração somente em TTY

`_instalar_handler_sigwinch` e `_restaurar_handler_sigwinch` são chamados
**apenas dentro do ramo** `if sys.stdin.isatty() and sys.stdout.isatty()`.
O ramo `else` (não-TTY) não toca em `SIGWINCH`.

### 13.6 Select duplo no loop principal

O loop principal substitui a chamada direta a `_ler_tecla_sessao()` por um
`select.select` que monitora simultaneamente stdin e o wakeup pipe. A drenagem
do pipe usa um laço não bloqueante: consome todos os bytes disponíveis e
encerra ao receber `BlockingIOError` (EAGAIN — sem mais dados disponíveis),
`b""` (pipe fechado) ou outro `OSError`, sem aguardar bytes adicionais.

```python
while True:
    try:
        prontos, _, _ = select.select([fd, r_wakeup], [], [])

        if r_wakeup in prontos:
            while True:
                try:
                    dados = os.read(r_wakeup, 64)
                    if not dados:
                        break
                except BlockingIOError:
                    break
                except OSError:
                    break
            resize_pendente[0] = False
            nova_l, nova_a = _obter_dimensoes_apos_sigwinch(fd, (largura, altura))
            if nova_l != largura or nova_a != altura:
                largura, altura = nova_l, nova_a
                _apresentar_quadro(
                    _resolver_conteudo(estado, modelo, largura, altura), largura
                )
            if fd not in prontos:
                continue

        ch = _ler_tecla_sessao(fd=fd)
        tela_antes = estado["tela_atual"]
        estado = processar_comando(estado, ch, modelo)
        if estado["saindo"]:
            break
        if estado["tela_atual"] != tela_antes:
            modelo = _carregar_modelo_por_id(estado["tela_atual"])
        if ch == "b" or estado["tela_atual"] != tela_antes:
            _apresentar_quadro(
                _resolver_conteudo(estado, modelo, largura, altura), largura
            )
    except KeyboardInterrupt:
        continue
```

Quando `r_wakeup` e `fd` estão prontos simultaneamente: processa o resize
primeiro (com redesenho), depois lê e processa a tecla nessa mesma iteração.

### 13.7 Modificação de `_apresentar_quadro`

Adicionar parâmetro `largura=None` com backward-compatibility:

```python
def _apresentar_quadro(conteudo, largura=None):
    w = largura if largura is not None else shutil.get_terminal_size(fallback=(80, 24)).columns
    ...
```

Todas as chamadas de `main()` no ramo TTY passam `largura` explicitamente.
Chamadas existentes sem `largura` continuam funcionando via fallback.

### 13.8 Estrutura completa de `main()` — ramo TTY

```python
if sys.stdin.isatty() and sys.stdout.isatty():
    fd = sys.stdin.fileno()
    largura, altura = _obter_dimensoes_iniciais(fd)
    resize_pendente = [False]
    r_wakeup = None
    w_wakeup = None
    sessao_iniciada = False
    handler_instalado = False
    handler_anterior = None
    atributos_originais = None
    try:
        r_wakeup, w_wakeup = os.pipe()
        os.set_blocking(r_wakeup, False)
        os.set_blocking(w_wakeup, False)
        atributos_originais = _iniciar_sessao_tui(fd)
        sessao_iniciada = True
        handler_anterior = _instalar_handler_sigwinch(w_wakeup, resize_pendente)
        handler_instalado = True
        _apresentar_quadro(
            _resolver_conteudo(estado, modelo, largura, altura), largura
        )
        while True:
            try:
                prontos, _, _ = select.select([fd, r_wakeup], [], [])
                if r_wakeup in prontos:
                    while True:
                        try:
                            dados = os.read(r_wakeup, 64)
                            if not dados:
                                break
                        except BlockingIOError:
                            break
                        except OSError:
                            break
                    resize_pendente[0] = False
                    nova_l, nova_a = _obter_dimensoes_apos_sigwinch(fd, (largura, altura))
                    if nova_l != largura or nova_a != altura:
                        largura, altura = nova_l, nova_a
                        _apresentar_quadro(
                            _resolver_conteudo(estado, modelo, largura, altura), largura
                        )
                    if fd not in prontos:
                        continue
                ch = _ler_tecla_sessao(fd=fd)
                tela_antes = estado["tela_atual"]
                estado = processar_comando(estado, ch, modelo)
                if estado["saindo"]:
                    break
                if estado["tela_atual"] != tela_antes:
                    modelo = _carregar_modelo_por_id(estado["tela_atual"])
                if ch == "b" or estado["tela_atual"] != tela_antes:
                    _apresentar_quadro(
                        _resolver_conteudo(estado, modelo, largura, altura), largura
                    )
            except KeyboardInterrupt:
                continue
    finally:
        if handler_instalado:
            _restaurar_handler_sigwinch(handler_anterior)
        if r_wakeup is not None:
            try:
                os.close(r_wakeup)
            except OSError:
                pass
        if w_wakeup is not None:
            try:
                os.close(w_wakeup)
            except OSError:
                pass
        if sessao_iniciada:
            _encerrar_sessao_tui(fd, atributos_originais)
```

### 13.9 Ramo não-TTY — inalterado

```python
else:
    tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
    largura = tamanho_terminal.columns
    altura = tamanho_terminal.lines
    print(renderizar_estado(estado, modelo, largura, altura=altura), end="")
    for linha in sys.stdin:
        ...
```

Sem `SIGWINCH`, sem wakeup pipe, sem `ioctl`, sem select duplo.

### 13.10 Políticas de falha parcial na aquisição

#### 13.10.1 Estado explícito de aquisição

Os sentinelas e indicadores inicializados antes do `try` distinguem o estado
de cada recurso:

- `r_wakeup = None` / `w_wakeup = None`: `None` indica descritor não criado;
  qualquer outro valor indica descritor existente e sujeito a fechamento.
- `sessao_iniciada = False`: `True` somente após `_iniciar_sessao_tui` retornar
  sem exceção.
- `handler_instalado = False`: `True` somente após `_instalar_handler_sigwinch`
  retornar sem exceção.
- `handler_anterior = None`: recebe o valor de retorno de
  `_instalar_handler_sigwinch` somente quando `handler_instalado = True`.
- `atributos_originais = None`: recebe o valor de retorno de
  `_iniciar_sessao_tui` somente quando a função conclui sem exceção; o estado
  `sessao_iniciada = True` garante que `atributos_originais` é válido quando
  `_encerrar_sessao_tui` é chamado no `finally`.

Esses estados pertencem exclusivamente à sessão. Não são campos do JSON de
configuração, não são estado declarativo da tela e não alteram a arquitetura
externa. Servem exclusivamente para cleanup idempotente e condicional.

#### 13.10.2 Falha em `os.pipe()` ou `os.set_blocking`

Se `os.pipe()` falhar, `r_wakeup` e `w_wakeup` permanecem `None`. O `finally`
não tenta fechar nenhum descritor. `sessao_iniciada` e `handler_instalado`
permanecem `False`; as etapas correspondentes do `finally` são ignoradas.

Se o primeiro `os.set_blocking` (`r_wakeup`) falhar, `os.pipe()` já retornou
com sucesso: ambos os descritores existem. O `finally` fecha ambos (via
`is not None`). `sessao_iniciada` e `handler_instalado` permanecem `False`.

Se o segundo `os.set_blocking` (`w_wakeup`) falhar, o mesmo se aplica: ambos
os descritores existem e são fechados pelo `finally`.

Em nenhum caso de falha de `os.pipe()` ou `os.set_blocking` o `finally` chama
`_encerrar_sessao_tui` ou `_restaurar_handler_sigwinch`.

#### 13.10.3 Falha em `_iniciar_sessao_tui`

`_iniciar_sessao_tui` é responsável por realizar rollback interno completo quando
falhar antes de retornar com sucesso. O chamador observa somente dois resultados:

- **Sucesso:** a sessão foi integralmente iniciada; `atributos_originais` foi
  retornado; `sessao_iniciada` passa a `True` no chamador.
- **Falha:** a função já executou rollback interno best effort; a exceção original
  é propagada; `sessao_iniciada` permanece `False`; o `finally` externo não chama
  `_encerrar_sessao_tui`.

Não há escolha entre rollback interno e rollback pelo chamador. O rollback
interno é a política única e obrigatória.

##### Emissão potencialmente parcial

A sequência de entrada pode ter sido emitida total ou parcialmente antes de
uma falha de `write` ou `flush`:

```text
\x1b[?1049h   alternate screen
\x1b[?25l     cursor oculto
\x1b[?7l      autowrap desativado
\x1b[2J       limpeza
\x1b[H        posicionamento inicial
```

Uma chamada de `write()` pode escrever toda a sequência, escrever parte dela,
lançar exceção após emissão parcial, ou ser seguida por falha de `flush()`
depois que dados já foram aceitos pelo stream. Portanto, não é permitido
presumir que uma exceção de `write` ou `flush` significa que nenhuma sequência
visual alcançou o terminal.

##### Função auxiliar `_restaurar_efeitos_visuais_tui`

Para evitar duas políticas visuais concorrentes entre o rollback de
`_iniciar_sessao_tui` e o encerramento normal de `_encerrar_sessao_tui`, o
handoff exige uma função auxiliar local e mínima definida em `tela/demo.py`:

```python
def _restaurar_efeitos_visuais_tui():
    try:
        sys.stdout.write("\x1b[?7h\x1b[?25h\x1b[?1049l")
    except Exception:
        pass
    try:
        sys.stdout.flush()
    except Exception:
        pass
```

Essa função:
- usa as mesmas sequências normatizadas pela ADR-0016: autowrap ativo
  (`\x1b[?7h`), cursor visível (`\x1b[?25h`), saída do alternate screen
  (`\x1b[?1049l`);
- separa `write` e `flush` em blocos `try` independentes, garantindo que falha
  em `write` não impede a tentativa de `flush`;
- não lança exceção própria — erros são silenciados internamente;
- é reutilizada tanto no rollback de `_iniciar_sessao_tui` quanto em
  `_encerrar_sessao_tui`, eliminando divergência entre as duas políticas visuais.

Não cria módulo novo. Não altera a interface de nenhuma outra função. Não
introduz protocolo de terminal novo.

##### `_encerrar_sessao_tui` atualizada

```python
def _encerrar_sessao_tui(fd_stdin, atributos_originais):
    try:
        termios.tcsetattr(fd_stdin, termios.TCSADRAIN, atributos_originais)
    except Exception:
        pass
    _restaurar_efeitos_visuais_tui()
```

A semântica permanece: `termios` primeiro, restauração visual depois. A função
auxiliar substitui a duplicação da sequência sem alterar a ordem nem o
comportamento observável.

##### `_iniciar_sessao_tui` com rollback interno completo

```python
def _iniciar_sessao_tui(fd_stdin):
    atributos_originais = termios.tcgetattr(fd_stdin)
    tty.setcbreak(fd_stdin)
    try:
        sys.stdout.write("\x1b[?1049h\x1b[?25l\x1b[?7l\x1b[2J\x1b[H")
        sys.stdout.flush()
    except Exception:
        _restaurar_efeitos_visuais_tui()
        try:
            termios.tcsetattr(fd_stdin, termios.TCSADRAIN, atributos_originais)
        except Exception:
            pass
        raise
    return atributos_originais
```

Ordem do rollback interno quando qualquer operação falhar depois de
`tty.setcbreak`:

```text
1. tentar restaurar efeitos visuais (_restaurar_efeitos_visuais_tui)
2. tentar flush da sequência de restauração (encapsulado na auxiliar)
3. tentar restaurar atributos termios originais (termios.tcsetattr)
4. propagar a exceção original (raise)
```

A restauração de `termios` é tentada mesmo quando a restauração visual falhar:
`_restaurar_efeitos_visuais_tui` silencia erros internamente e sempre retorna
sem exceção. A falha de `termios.tcsetattr` durante o rollback não substitui a
exceção primária: está capturada pelo `try/except Exception: pass` interno. Não
há `return` no bloco `except`. O `raise` ao final propaga a exceção original.

Não há captura ampla que transforme falha de inicialização em sucesso. Quando
não houver exceção primária, a política normal da função permanece inalterada.

##### Falhas de `termios.tcgetattr` ou `tty.setcbreak`

Se `termios.tcgetattr` ou `tty.setcbreak` falharem antes de qualquer sequência
visual ser emitida, nenhuma modificação foi aplicada ao terminal. A exceção
propaga diretamente sem tentativa de rollback visual ou de `termios`.
`sessao_iniciada` permanece `False`.

##### Cobertura de falhas parciais

| Ponto de falha | Rollback visual tentado | Termios restaurado | Exceção preservada |
|---|---|---|---|
| `tcgetattr` ou `setcbreak` falham | Não (nenhuma emissão anterior) | Não (não modificado) | Sim |
| `write` falha antes de qualquer emissão visual | Sim (best effort) | Sim (best effort) | Sim |
| `write` falha após `\x1b[?1049h` parcial | Sim (best effort) | Sim (best effort) | Sim |
| `write` falha após `\x1b[?25l` | Sim (best effort) | Sim (best effort) | Sim |
| `write` falha após `\x1b[?7l` | Sim (best effort) | Sim (best effort) | Sim |
| `write` falha após `\x1b[2J\x1b[H` | Sim (best effort) | Sim (best effort) | Sim |
| `flush` falha após `write` bem-sucedido | Sim (best effort) | Sim (best effort) | Sim |
| Rollback visual falha | — (silenciado em `_restaurar_efeitos_visuais_tui`) | Sim (best effort) | Sim |
| `tcsetattr` falha durante rollback | — | — (silenciado) | Sim |

Em todos os casos onde `_iniciar_sessao_tui` falha:
- `sessao_iniciada` permanece `False`.
- O `finally` externo não chama `_encerrar_sessao_tui` com estado inexistente.
- Pipe e demais recursos externos continuam sendo limpos pelas sentinelas da
  seção 13.10.2.

#### 13.10.4 Falha em `_instalar_handler_sigwinch`

`signal.signal` é atômico em CPython: ou substitui o handler e retorna o
anterior, ou lança exceção sem alterar o estado do sinal. Se
`_instalar_handler_sigwinch` lançar exceção, o handler de `SIGWINCH` permanece
inalterado. `handler_instalado` permanece `False` e `handler_anterior`
permanece `None`.

O `finally` não chama `_restaurar_handler_sigwinch` quando
`handler_instalado = False`. O pipe (já criado e configurado) e a sessão TUI
(já iniciada, se `sessao_iniciada = True`) continuam sujeitos a cleanup pelos
seus respectivos sentinelas.

`handler_anterior` passa a ser responsabilidade do cleanup exclusivamente após
`_instalar_handler_sigwinch` retornar com sucesso — ou seja, quando
`handler_instalado = True`.

#### 13.10.5 Cleanup idempotente e não duplicado

- Nenhum descritor é fechado duas vezes: o teste `is not None` garante que
  cada descritor é fechado no máximo uma vez pelo `finally`.
- A sessão TUI não é encerrada duas vezes: o `finally` verifica
  `sessao_iniciada`.
- Nenhum handler é restaurado quando nunca foi substituído: o `finally` verifica
  `handler_instalado`.
- Falha em uma etapa de cleanup não autoriza abandonar os recursos restantes:
  cada etapa do `finally` é independente e protegida individualmente (ver
  seção 18.2).
- A exceção original é preservada: toda a lógica de cleanup em `finally`,
  `_restaurar_handler_sigwinch` e `_encerrar_sessao_tui` suprime erros
  secundários internamente; a exceção que alcança o chamador é sempre a do
  corpo do `try`.

## 14. Importações adicionais em `tela/demo.py`

```python
import fcntl
import struct
import signal
```

`fcntl` e `struct` são necessários para `ioctl(TIOCGWINSZ)`.
`signal` é necessário para `signal.signal` e `signal.SIGWINCH`.

## 15. Regras de obtenção e validação das dimensões

### 15.1 `_par_dimensoes_valido(largura, altura)`

Retorna `True` se e somente se:
- `largura` existe (não é `None`);
- `altura` existe (não é `None`);
- ambos são convertíveis em `int` (teste: `isinstance(largura, int)` ou
  conversão segura de string);
- `largura > 0`;
- `altura > 0`.

Retorna `False` para qualquer condição não satisfeita. Não lança exceção.

```python
def _par_dimensoes_valido(largura, altura):
    try:
        l = int(largura)
        a = int(altura)
        return l > 0 and a > 0
    except (TypeError, ValueError):
        return False
```

### 15.2 `_obter_dimensoes_ioctl(fd)`

Usa `fcntl.ioctl(fd, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))`.
A struct `winsize` tem layout `(ws_row, ws_col, ws_xpixel, ws_ypixel)`, todos
`unsigned short` (`H`). Desempacota como `struct.unpack('HHHH', buf)`;
`cols = resultado[1]`, `rows = resultado[0]`.

Retorna `(cols, rows)` como `(largura, altura)` quando o par é válido.
Retorna `None` quando `ioctl` lança exceção ou o par não é válido.

```python
def _obter_dimensoes_ioctl(fd):
    try:
        buf = struct.pack('HHHH', 0, 0, 0, 0)
        buf = fcntl.ioctl(fd, termios.TIOCGWINSZ, buf)
        rows, cols, _, _ = struct.unpack('HHHH', buf)
        if _par_dimensoes_valido(cols, rows):
            return int(cols), int(rows)
        return None
    except (OSError, struct.error):
        return None
```

### 15.3 `_obter_dimensoes_env()`

Lê `os.environ.get("LINES")` e `os.environ.get("COLUMNS")` como par.
Aceita somente quando **ambas** estão presentes e formam um par válido.
Uma variável ausente invalida o par.

```python
def _obter_dimensoes_env():
    try:
        cols = int(os.environ["COLUMNS"])
        rows = int(os.environ["LINES"])
        if _par_dimensoes_valido(cols, rows):
            return cols, rows
        return None
    except (KeyError, ValueError):
        return None
```

### 15.4 `_obter_dimensoes_iniciais(fd)`

Cadeia: `ioctl → env → (80, 24)`.

```python
def _obter_dimensoes_iniciais(fd):
    par = _obter_dimensoes_ioctl(fd)
    if par is not None:
        return par
    par = _obter_dimensoes_env()
    if par is not None:
        return par
    return 80, 24
```

### 15.5 `_obter_dimensoes_apos_sigwinch(fd, ultimas_validas)`

Cadeia: `ioctl → env → ultimas_validas`. O fallback `(80, 24)` não aparece aqui.

```python
def _obter_dimensoes_apos_sigwinch(fd, ultimas_validas):
    par = _obter_dimensoes_ioctl(fd)
    if par is not None:
        return par
    par = _obter_dimensoes_env()
    if par is not None:
        return par
    return ultimas_validas
```

`ultimas_validas` é `tuple[int, int]` com par válido da última atualização bem-
sucedida (ou da inicialização). Sempre retorna um par de inteiros positivos.

## 16. Regras de redesenho

### 16.1 `_resolver_conteudo(estado, modelo, largura, altura)`

Função auxiliar chamada antes de cada `_apresentar_quadro` no ramo TTY:

```python
def _resolver_conteudo(estado, modelo, largura, altura):
    if _tela_pequena_demais(largura, altura):
        return _quadro_minimo_aviso(largura, altura)
    return renderizar_estado(estado, modelo, largura, altura=altura)
```

### 16.2 Condição de redesenho após SIGWINCH

Redesenho ocorre **somente** quando `nova_l != largura or nova_a != altura`.
Se `_obter_dimensoes_apos_sigwinch` retornar as mesmas últimas dimensões
válidas (porque todas as fontes falharam), não há redesenho — as dimensões
não mudaram.

### 16.3 Resultado visual obrigatório

Após cada redesenho com par válido:
- Nenhum resíduo do quadro anterior permanece visível.
- Nenhuma linha excede a largura atual.
- O número de linhas escritas não excede a altura atual.
- Nenhuma linha adicional é emitida após o quadro.
- `\x1b[2J` **não** é emitido durante redesenho por resize.
- Escrita atômica e synchronized output preservados.

Esses requisitos são satisfeitos porque `renderizar_tela` retorna exatamente
`altura` linhas quando `altura` é fornecida e suficiente, e `_apresentar_quadro`
usa posicionamento absoluto linha a linha sem emitir `\n` de quebra.

## 17. Terminal pequeno demais

### 17.1 `_tela_pequena_demais(largura, altura)`

```python
def _tela_pequena_demais(largura, altura):
    return largura < LARGURA_MINIMA_TELA or altura < ALTURA_MINIMA_TELA
```

`LARGURA_MINIMA_TELA = 10`: derivado da guarda explícita em
`_montar_corpo_horizontal` e do comportamento indefinido documentado em
`renderizar_tela` para `largura < 10`.

`ALTURA_MINIMA_TELA = 6`: `l_cab_mínimo(3) + l_barra_mínimo(3)`.

### 17.2 `_quadro_minimo_aviso(largura, altura)`

Retorna string com exatamente `altura` linhas terminadas por `\n`
(`conteudo.count("\n") == altura`), cada linha com exatamente `largura`
caracteres antes do `\n`. Formato compatível com `renderizar_tela`.

Algoritmo:
- `msg_completa = "terminal pequeno demais"` (23 chars) — dimensão suficiente
  para mensagem completa e inequívoca.
- `msg_breve = "tela peq."` (9 chars) — dimensão suficiente apenas para
  mensagem abreviada mas ainda inequívoca.
- Para `largura < 9` (limite físico): nenhuma mensagem com significado
  inequívoco de "terminal pequeno demais" cabe em 1 a 8 chars. A linha é
  preenchida com espaços. A sessão permanece ativa e a recuperação automática
  continua funcionando quando as dimensões voltarem a ser suficientes.
- Linha do aviso: `msg_completa` se `largura >= 23`; `msg_breve` se
  `largura >= 9`; `""` (preenchida com espaços) se `largura < 9`.
- Linha do aviso truncada a `largura` chars e preenchida com espaços à direita
  até `largura` chars.
- Linhas restantes (`altura - 1`): `" " * largura` cada uma.
- Resultado: `"\n".join(linhas) + "\n"` onde `len(linhas) == altura`.

```python
def _quadro_minimo_aviso(largura, altura):
    if largura >= 23:
        msg = "terminal pequeno demais"
    elif largura >= 9:
        msg = "tela peq."
    else:
        msg = ""  # limite físico: nenhuma mensagem inequívoca cabe em largura < 9
    linha_aviso = msg[:largura].ljust(largura)
    linha_vazia = " " * largura
    linhas = [linha_aviso] + [linha_vazia] * (altura - 1)
    return "\n".join(linhas) + "\n"
```

### 17.3 Comportamento durante sessão com terminal pequeno

- A sessão TUI permanece ativa (não encerra, não propaga exceção como
  encerramento).
- O quadro mínimo substitui completamente o quadro anterior, sem resíduos.
- Esc, navegação e demais teclas continuam sendo processados normalmente
  (o `processar_comando` funciona independente do que é exibido).
- Quando uma atualização posterior de dimensões produzir `not _tela_pequena_demais(nova_l, nova_a)`:
  a tela normal é redesenhada automaticamente sem ação do usuário.

### 17.4 Caso não coberto pelas constantes pré-definidas

Se o renderer levantar `RenderizadorErro` durante um resize com `not _tela_pequena_demais(largura, altura)`,
isso indica conteúdo que não cabe mesmo com largura/altura acima dos mínimos (e.g., chips da
barra_de_menus que não cabem em `largura = 10`). Para H-0023, esse caso é mapeado para o quadro
mínimo de aviso — `_resolver_conteudo` pode capturar `RenderizadorErro` e retornar
`_quadro_minimo_aviso(largura, altura)`. Esta captura não conflita com ADR-0017 §9: evita
que `RenderizadorErro` seja encerramento normal.

```python
def _resolver_conteudo(estado, modelo, largura, altura):
    if _tela_pequena_demais(largura, altura):
        return _quadro_minimo_aviso(largura, altura)
    try:
        return renderizar_estado(estado, modelo, largura, altura=altura)
    except RenderizadorErro:
        return _quadro_minimo_aviso(largura, altura)
```

O import de `RenderizadorErro` em `demo.py` já existe via
`from tela.renderizador import renderizar_tela` — adicionar
`RenderizadorErro` ao import.

## 18. Tratamento de restauração

### 18.1 Ordem no `finally`

1. Se `handler_instalado`: `_restaurar_handler_sigwinch(handler_anterior)` —
   primeiro, para que o handler não dispare após o pipe ser fechado.
2. Se `r_wakeup is not None`: fechar `r_wakeup` em bloco `try/except OSError`.
3. Se `w_wakeup is not None`: fechar `w_wakeup` em bloco `try/except OSError`.
4. Se `sessao_iniciada`: `_encerrar_sessao_tui(fd, atributos_originais)` — último.

A condicionalidade de cada etapa garante que recursos não adquiridos não sejam
restaurados ou fechados como se existissem. A ordem permanece coerente com a
regra de restaurar o handler antes de fechar o descritor de escrita usado por
ele (etapa 1 precede etapa 3).

### 18.2 Robustez individual

Cada passo do `finally` é protegido: uma falha em qualquer etapa não impede
as seguintes. `_encerrar_sessao_tui` já usa blocos `try` separados
internamente. `_restaurar_handler_sigwinch` usa `try/except Exception`.

### 18.3 Garantia após exceção

Se uma exceção não tratada ocorrer em qualquer ponto dentro do `try` — durante
a inicialização (criação do pipe, configuração não bloqueante, início da sessão
TUI, instalação do handler) ou durante o loop —, o `finally` executa com
verificação condicional: somente os recursos efetivamente adquiridos são
restaurados ou fechados. A exceção original não é substituída por erro
secundário de cleanup.

## 19. Testes automatizados obrigatórios

Adicionar seção 8 em `tela/teste_demo.py`: `teste_redimensionamento_reativo_h0023()`.

### 19.1 Obtenção e validação de dimensões

| Caso | Descrição |
|---|---|
| `_par_dimensoes_valido(80, 24)` | `True` |
| `_par_dimensoes_valido(0, 24)` | `False` (zero) |
| `_par_dimensoes_valido(80, 0)` | `False` (zero) |
| `_par_dimensoes_valido(-1, 24)` | `False` (negativo) |
| `_par_dimensoes_valido("abc", 24)` | `False` (não inteiro) |
| `_par_dimensoes_valido(None, 24)` | `False` (ausente) |
| `_par_dimensoes_valido(80, None)` | `False` (ausente) |
| `_par_dimensoes_valido("80", "24")` | `True` (string inteira válida) |

**`_obter_dimensoes_ioctl`:**
- Com mock de `fcntl.ioctl` retornando `struct.pack('HHHH', 24, 80, 0, 0)`:
  retorna `(80, 24)`.
- Com mock de `fcntl.ioctl` retornando `struct.pack('HHHH', 0, 0, 0, 0)`:
  retorna `None` (par inválido).
- Com mock de `fcntl.ioctl` levantando `OSError`: retorna `None`.

**`_obter_dimensoes_env`:**
- Com `LINES=24, COLUMNS=80`: retorna `(80, 24)`.
- Com `LINES=24` ausente `COLUMNS`: retorna `None`.
- Com `COLUMNS=0, LINES=24`: retorna `None` (zero inválido).
- Com `LINES="abc"`: retorna `None` (não inteiro).

**`_obter_dimensoes_iniciais`:**
- ioctl válido prevalece sobre env: com ioctl retornando `(100, 50)` e
  `COLUMNS=80, LINES=24` presentes, retorna `(100, 50)`.
- ioctl None, env válido: retorna par de env.
- ioctl None, env inválido (só LINES): retorna `(80, 24)`.
- ioctl None, env None: retorna `(80, 24)`.

**`_obter_dimensoes_apos_sigwinch`:**
- ioctl válido retorna par ioctl (ignora últimas_validas).
- ioctl None, env válido: retorna par env.
- ioctl None, env None: retorna `ultimas_validas` passado como argumento.
- Confirmação: `(80, 24)` não aparece como resultado quando `ultimas_validas=(120, 40)` e todas as fontes falham.

### 19.2 Sinal e ciclo de atualização

**Handler e instalação:**
- `_instalar_handler_sigwinch(w_wakeup, resize_pendente)` com mock de
  `signal.signal`: confirma que `signal.signal` foi chamado com `signal.SIGWINCH`
  e que retornou o handler anterior.
- Handler instalado somente em TTY: inspecionar o código-fonte de `demo.py`
  para confirmar que chamadas a `_instalar_handler_sigwinch` — excluindo a
  definição da função em nível de módulo — ocorrem apenas dentro do bloco
  `if sys.stdin.isatty() and sys.stdout.isatty()`. Usar inspeção de chamadas
  efetivas (`_instalar_handler_sigwinch(...)`) em vez de contagem textual do
  nome da função.
- Fluxo não-TTY via subprocess: `subprocess.run` com pipe não contém referência
  a handler de SIGWINCH nos efeitos observáveis.

**Flag e pipe:**
- Chamar diretamente o handler com `signum=28, frame=None` (após instalar com
  `w_wakeup` real e `resize_pendente=[False]`): confirma `resize_pendente[0] is True`
  e que um byte foi escrito no pipe.
- `os.read(r_wakeup, 64)` após chamar o handler: retorna pelo menos um byte.

**Processamento no loop (via mock):**
- Usar `unittest.mock.patch` em `tela.demo.processar_comando`,
  `tela.demo._ler_tecla_sessao`, `tela.demo._apresentar_quadro`,
  `tela.demo._iniciar_sessao_tui`, `tela.demo._encerrar_sessao_tui`,
  `tela.demo._carregar_modelo_por_id`, `tela.demo.renderizar_estado`,
  `sys.stdin`, `sys.stdout` para simular sessão TTY:
  - Primeiro evento: wakeup pipe ativo com nova dimensão → `_apresentar_quadro`
    chamado com nova largura.
  - Par inválido: `_obter_dimensoes_apos_sigwinch` retorna últimas válidas →
    `_apresentar_quadro` não chamado como redesenho de resize (dimensões iguais).
  - Handler anterior restaurado: `signal.signal` chamado com `signal.SIGWINCH`
    e handler anterior ao final.

**Restore após Esc:**
- Simular saída via Esc (estado `saindo = True`): confirmar que
  `signal.signal` é chamado com o handler anterior, que `os.close` é chamado
  para `r_wakeup` e `w_wakeup`, e que `_encerrar_sessao_tui` é chamado (via
  mocks).

**Restore após exceção:**
- Simular `RuntimeError` dentro do loop: confirmar que handler é restaurado
  e pipe é fechado (via mocks).

**Pipe não bloqueante e pipe cheio:**
- Confirmar que `os.get_blocking(r_wakeup)` retorna `False` após a
  configuração inicial com `os.set_blocking(r_wakeup, False)`.
- Confirmar que `os.get_blocking(w_wakeup)` retorna `False` após a
  configuração inicial com `os.set_blocking(w_wakeup, False)`.
- Chamar diretamente o handler com `w_wakeup` real não bloqueante e
  `resize_pendente=[False]`: confirmar que retorna sem bloquear,
  `resize_pendente[0]` é `True` e pelo menos um byte está disponível em
  `r_wakeup`.
- Simular pipe cheio com mock de `os.write` levantando `BlockingIOError`:
  confirmar que o handler retorna imediatamente, `resize_pendente[0]`
  permanece `True` e nenhuma exceção não tratada é propagada.
- Confirmar que `BlockingIOError`/`EAGAIN`/`EWOULDBLOCK` na escrita do
  handler não encerram a aplicação (o `except OSError: pass` já cobre
  `BlockingIOError` como subclasse).
- Confirmar coalescência: chamar o handler múltiplas vezes sem drenar o pipe
  (mock de `os.write` aceita na primeira chamada e lança `BlockingIOError`
  nas seguintes); após a drenagem, apenas um redesenho é executado usando a
  dimensão mais recente disponível.
- Confirmar que a drenagem consome os bytes disponíveis e termina ao receber
  `BlockingIOError` sem bloquear: usar pipe real não bloqueante com número
  limitado de bytes escritos e verificar que o laço de drenagem encerra
  corretamente.
- Confirmar que uma atualização válida de dimensões ocorre após a drenagem
  (via mock de `_obter_dimensoes_apos_sigwinch` retornando par novo).

Os testes não devem encher um pipe real de forma indefinida nem correr risco
de travamento. Podem usar mocks controlados de `os.write` e `os.read` para
simular condições de pipe cheio de forma determinística.

### 19.3 Renderização e apresentação

**`_quadro_minimo_aviso`:**
- `_quadro_minimo_aviso(80, 24)`: resultado tem `count("\n") == 24`;
  primeira linha começa com "terminal pequeno demais".
- `_quadro_minimo_aviso(9, 3)`: primeira linha começa com "tela peq.".
- `_quadro_minimo_aviso(5, 2)`: primeira linha tem exatamente 5 chars antes do
  `\n` e é preenchida com espaços (limite físico — `largura < 9`; nenhuma
  mensagem inequívoca cabe); `"!"` não aparece como texto normativo.
- `_quadro_minimo_aviso(23, 1)`: resultado tem `count("\n") == 1`; única linha
  tem exatamente 23 chars antes do `\n`.
- Para qualquer `(largura, altura)` com `largura > 0` e `altura > 0`:
  `conteudo.count("\n") == altura`.
- Nenhuma linha do resultado excede `largura` chars antes do `\n`.

**`_tela_pequena_demais`:**
- `(9, 24)` → `True`; `(10, 24)` → `False`.
- `(80, 5)` → `True`; `(80, 6)` → `False`.
- `(10, 6)` → `False`.

**`_apresentar_quadro` com parâmetro `largura`:**
- Chamada com `largura=20`: preenche linhas a 20 chars sem consultar
  `shutil.get_terminal_size` (mock de `shutil.get_terminal_size` não é chamado).
- Chamada sem `largura`: comportamento existente preservado (mock de
  `shutil.get_terminal_size` é chamado).

**Redesenho por redução e ampliação:**
- Reducer de conteúdo: `renderizar_estado(..., largura=60, altura=20)` retorna
  string com `count("\n") == 20` e cada linha não-vazia com 60 chars.
- Amplification: `renderizar_estado(..., largura=120, altura=40)` retorna
  string com `count("\n") == 40` e cada linha não-vazia com 120 chars.
- Composição declarativa: após cada chamada, `modelo.corpo.arranjo` permanece
  inalterado.

### 19.4 Terminal pequeno

- `_tela_pequena_demais(9, 6)` → `True`; aviso retornado por `_resolver_conteudo`.
- `_tela_pequena_demais(10, 5)` → `True`; aviso retornado por `_resolver_conteudo`.
- `_tela_pequena_demais(10, 6)` → `False`; render normal tentado por `_resolver_conteudo`.
- Aviso cabe: para qualquer `(largura, altura)` positivos, `_quadro_minimo_aviso(largura, altura)`
  não excede `largura × altura` caracteres úteis.
- Recuperação: `_resolver_conteudo` retorna render normal quando `not _tela_pequena_demais(...)`.

### 19.5 Regressões obrigatórias (seções existentes)

Todas as seções 1–7 de `teste_demo.py` devem continuar passando sem alteração
de seus critérios. Verificar especialmente:
- Seção 7A: `setraw` ausente, `setcbreak` presente, `\x1b[2J` exatamente uma
  vez, synchronized output, finally.
- Seção 7B: `_iniciar_sessao_tui` com sequências obrigatórias.
- Seção 7C: `_encerrar_sessao_tui` com restauração completa.
- Seção 7D: `_apresentar_quadro` com escrita atômica, posicionamento absoluto,
  synchronized output — chamada sem `largura` deve continuar funcionando.
- Seção 7G: saída pipe não contém sequências TUI.
- Seção 4: subprocess com pipe (`b\ns\n`) encerra com código 0, stdout
  determinístico.

### 19.6 Falhas parciais na inicialização e cleanup

Todos os testes desta seção devem usar mocks determinísticos. Nenhum teste
deve provocar corrupção real do terminal nem vazamento intencional de
descritores no processo de teste.

**Pipe — falha em `os.pipe()`:**
- Mockar `os.pipe` para lançar `OSError`: confirmar que `os.close` não é
  chamado com nenhum argumento (nenhum descritor existe).

**Pipe — falha no primeiro `os.set_blocking` (`r_wakeup`):**
- Mockar `os.set_blocking` para lançar na primeira chamada: confirmar que
  `os.close` é chamado para ambos os descritores retornados por `os.pipe()`.

**Pipe — falha no segundo `os.set_blocking` (`w_wakeup`):**
- Mockar `os.set_blocking` para lançar na segunda chamada: confirmar que
  `os.close` é chamado para ambos os descritores.

**Pipe — cleanup não fecha duas vezes:**
- Usar pipe real e confirmar que cada descritor é passado a `os.close`
  exatamente uma vez durante o cleanup normal (saída por Esc ou exceção).

**Sessão TUI — `_iniciar_sessao_tui` falha antes de concluir:**
- Mockar `_iniciar_sessao_tui` para lançar `RuntimeError` antes de retornar:
  confirmar que `sessao_iniciada` permanece `False`, que `_encerrar_sessao_tui`
  não é chamado, que o pipe criado é fechado e que a exceção original é
  propagada ao chamador.

**Sessão TUI — rollback interno quando `write`/`flush` falha após `setcbreak`:**
- Mockar `sys.stdout.write` para lançar na chamada de `_iniciar_sessao_tui`:
  confirmar que `_restaurar_efeitos_visuais_tui` é chamada (ou que
  `sys.stdout.write` é invocado com `"\x1b[?7h\x1b[?25h\x1b[?1049l"`) antes de
  a exceção propagar.
- Confirmar que `termios.tcsetattr` é chamado com os atributos originais após
  a tentativa de restauração visual e antes de a exceção propagar.
- Mockar `sys.stdout.flush` para lançar após `write` bem-sucedido: confirmar
  que o mesmo rollback visual e `termios` são tentados.
- Confirmar que a exceção original de `write` ou `flush` é a exceção recebida
  pelo chamador, não um erro do rollback.

**Sessão TUI — exceção de `_iniciar_sessao_tui` não é suprimida:**
- Confirmar que a exceção lançada por `_iniciar_sessao_tui` alcança o chamador
  de `main()` sem ser capturada pelo `finally`.

**Sessão TUI — `_encerrar_sessao_tui` não chamado com estado inválido:**
- Após falha de `_iniciar_sessao_tui`, confirmar via mock que
  `_encerrar_sessao_tui` não é chamado.

**Falha da entrada visual — cenários por ponto de falha:**

Para cada cenário abaixo, usar mocks de `sys.stdout`, `tty` e `termios`. Não
alterar o terminal real. Confirmar em cada caso:

  (a) tentativa de emissão da sequência visual de restauração
      (`"\x1b[?7h\x1b[?25h\x1b[?1049l"`);
  (b) tentativa de flush da restauração;
  (c) tentativa de `termios.tcsetattr` com os atributos originais;
  (d) propagação da exceção original;
  (e) `sessao_iniciada` permanece `False`;
  (f) `_encerrar_sessao_tui` não é chamado.

- Falha de `tcgetattr`: confirmar que rollback visual e `termios` **não** são
  tentados (nenhuma modificação foi aplicada antes do ponto de falha); a exceção
  propaga diretamente.
- Falha de `setcbreak`: confirmar que rollback visual e `termios` **não** são
  tentados; a exceção propaga diretamente.
- Falha de `write` antes de qualquer byte emitido: confirmar (a)–(f).
- Falha de `write` com `IOError`: confirmar (a)–(f).
- Falha de `flush` após `write` bem-sucedido: confirmar (a)–(f).

**Falha durante rollback — resiliência do rollback interno:**

- `write` da restauração visual falha: confirmar que a tentativa de `flush` da
  restauração ainda ocorre e que `termios.tcsetattr` ainda é tentado após a
  falha de `write` do rollback.
- `flush` da restauração visual falha: confirmar que `termios.tcsetattr` ainda
  é tentado após a falha de `flush` do rollback.
- `termios.tcsetattr` falha durante rollback: confirmar que a exceção original
  de inicialização é preservada (não substituída pelo erro de `tcsetattr`).
- `write` visual e `termios.tcsetattr` falham sequencialmente durante rollback:
  confirmar que a exceção original de inicialização é a exceção recebida pelo
  chamador.
- Cleanup externo ainda fecha pipe quando `_iniciar_sessao_tui` falha e o
  rollback interno também falha parcialmente: confirmar via mocks que o `finally`
  externo fecha descritores.

**Coerência das sequências entre rollback e encerramento normal:**

- Confirmar que a sequência emitida pelo rollback de `_iniciar_sessao_tui` e
  a sequência emitida por `_encerrar_sessao_tui` são idênticas
  (`"\x1b[?7h\x1b[?25h\x1b[?1049l"`): ambas chamam
  `_restaurar_efeitos_visuais_tui`.
- Confirmar que `_restaurar_efeitos_visuais_tui` ativa autowrap (`\x1b[?7h`),
  mostra cursor (`\x1b[?25h`) e sai do alternate screen (`\x1b[?1049l`).
- Confirmar que a sequência de entrada (`\x1b[?1049h\x1b[?25l\x1b[?7l\x1b[2J\x1b[H`)
  não é emitida durante o rollback.
- Confirmar que `\x1b[2J` não aparece na sequência de restauração do rollback.
- Confirmar que `_restaurar_efeitos_visuais_tui` não lança exceção própria
  quando `write` e `flush` falham (erros silenciados internamente).

**Handler — `_instalar_handler_sigwinch` falha:**
- Mockar `signal.signal` para lançar `OSError` dentro de
  `_instalar_handler_sigwinch`: confirmar que `handler_instalado` permanece
  `False`, que `_restaurar_handler_sigwinch` não é chamado no `finally`, que
  o pipe é fechado e que, se `sessao_iniciada = True`, `_encerrar_sessao_tui`
  é chamado.

**Handler — nenhum handler não instalado é restaurado:**
- Usando o mock acima: confirmar que `signal.signal` não é chamado novamente
  no `finally` com o propósito de restauração (verificar que o número de
  chamadas a `signal.signal` após a falha é zero).

**Handler — falha após instalação bem-sucedida:**
- Após instalação bem-sucedida, mockar o loop para lançar `RuntimeError`:
  confirmar que `_restaurar_handler_sigwinch` é chamado com `handler_anterior`
  e que o `finally` completa todos os recursos.

**Handler — restaurado antes do fechamento do descritor de escrita:**
- Registrar a ordem das chamadas usando `unittest.mock.call_args_list` ou
  `side_effect` com lista: confirmar que `signal.signal` (restauração do
  handler) ocorre antes de `os.close(w_wakeup)`.

**Loop — exceção antes da primeira iteração:**
- Mockar `select.select` para lançar `OSError` na primeira chamada: confirmar
  que o `finally` executa cleanup completo de todos os recursos adquiridos.

**Loop — exceção durante o loop:**
- Mockar `processar_comando` para lançar `RuntimeError` na segunda chamada:
  confirmar cleanup completo.

**Loop — saída normal por Esc:**
- Simular `estado["saindo"] = True` em `processar_comando`: confirmar que o
  `finally` executa cleanup condicional com todos os recursos adquiridos.

**Cleanup — falha na restauração do handler não bloqueia os demais passos:**
- Mockar `signal.signal` (dentro de `_restaurar_handler_sigwinch`) para
  lançar; `_restaurar_handler_sigwinch` silencia via `try/except Exception`:
  confirmar que `os.close` e `_encerrar_sessao_tui` ainda são chamados após
  o retorno de `_restaurar_handler_sigwinch`.

**Cleanup — falha ao fechar um descritor não bloqueia os demais recursos:**
- Mockar `os.close` para lançar `OSError` na chamada de `r_wakeup`: confirmar
  que o bloco `try/except OSError` captura o erro, que a chamada `os.close`
  para `w_wakeup` ainda ocorre e que `_encerrar_sessao_tui` ainda é chamado.

**Cleanup — exceção original preservada:**
- Quando o loop lança `RuntimeError` e o mock de `signal.signal` também lança
  internamente: confirmar que a exceção recebida pelo chamador de `main()` é
  a `RuntimeError` original, pois `_restaurar_handler_sigwinch` a silencia
  internamente e não propaga erro secundário.

## 20. Validação em pseudo-TTY

### 20.1 Cenário automatizado com `pty.openpty()`

O teste deve:

1. Abrir um par master/slave PTY com `pty.openpty()`.
2. Iniciar a aplicação em subprocess com `stdin=slave_fd, stdout=slave_fd`
   (ou equivalente que apresente TTY real para a aplicação).
3. Enviar dimensões iniciais ao master PTY via `fcntl.ioctl(master_fd, termios.TIOCSWINSZ, ...)`.
4. Ler a saída inicial da aplicação pelo master e confirmar que contém
   sequências esperadas (alternate screen, synchronized output).
5. Alterar as dimensões via `fcntl.ioctl(master_fd, termios.TIOCSWINSZ, ...)` com novo valor.
6. Enviar `SIGWINCH` ao processo filho (`os.kill(pid, signal.SIGWINCH)`).
7. Ler saída do master e confirmar atualização (presença de novo conteúdo com
   nova dimensão ou posicionamento absoluto coerente).
8. Enviar Esc (`\x1b`) ao master para encerrar a aplicação.
9. Aguardar término do processo.
10. Confirmar código de saída 0.
11. Confirmar que a restauração ocorreu (ausência de alternate screen na saída
    posterior ao encerramento, ou código de saída 0).

### 20.2 Pseudo-TTY não substitui validação visual humana

O pseudo-TTY confirma atividade e resposta ao sinal. Não confirma ausência de
resíduos visuais, ausência de cintilação perceptível nem qualidade visual da
tela. Esses aspectos requerem validação humana em TTY real.

## 21. Validação manual em TTY real

### 21.1 Procedimento reproduzível

```bash
# Terminal com pelo menos 40×20 chars
cd /caminho/para/scripts
python tela/demo.py
```

Executar a sequência abaixo e registrar o resultado de cada passo:

| Passo | Ação | Critério de aprovação |
|---|---|---|
| 1 | Iniciar a aplicação | Tela renderizada sem resíduos; cursor oculto; alternate screen ativo |
| 2 | Reduzir a janela gradualmente | Tela redesenhada a cada redimensionamento; sem resíduos; sem scroll |
| 3 | Continuar reduzindo até < 10 ou < 6 linhas | Aviso "terminal pequeno demais" (ou variante) exibido; sem scroll; sem linha adicional abaixo |
| 4 | Ampliar a janela de volta | Tela normal restaurada automaticamente sem pressionar tecla; sem resíduos |
| 5 | Ampliar além da dimensão inicial | Tela normal com dimensões novas; sem resíduos do quadro anterior |
| 6 | Redimensionar repetidamente rápido | Sem cintilação perceptível; sem acúmulo de artefatos; último estado coerente |
| 7 | Pressionar `b` durante ou após resize | Borda alternada com as novas dimensões |
| 8 | Navegar via chip `d` durante resize | Navegação funciona; tela destino renderizada com dimensões atuais |
| 9 | Pressionar Esc | Saída limpa; terminal restaurado (cursor visível, tela normal, autowrap ativo) |
| 10 | Encerrar por exceção (kill externo, se possível) | Terminal restaurado; sem alternate screen residual |

### 21.2 Critérios objetivos de aprovação para validação humana

**Nenhum item abaixo foi validado.** Esta seção registra os critérios
pendentes para aprovação humana futura. O executor da implementação apenas
registra a pendência; não marca itens como concluídos antes da validação. A
aprovação humana será registrada exclusivamente no relatório de implementação
`IMP-0024`, após execução em TTY real, separada dos testes automatizados e
dos testes em pseudo-TTY.

Todos os seguintes devem ser verificados e aprovados em TTY real:

- [ ] Tela redesenhada ao redimensionar sem ação manual.
- [ ] Sem resíduos visíveis do quadro anterior após resize.
- [ ] Sem scroll acidental.
- [ ] Sem linhas adicionais abaixo do quadro após resize.
- [ ] Aviso de terminal pequeno exibido automaticamente quando dimensões insuficientes.
- [ ] Tela normal restaurada automaticamente sem ação quando dimensões ficam suficientes.
- [ ] Navegação (`b`, chips) funcional durante e após resize.
- [ ] Esc restaura terminal completamente (cursor, autowrap, alternate screen).
- [ ] Sem cintilação perceptível durante redimensionamento.
- [ ] Sem echo de teclas durante a sessão.

A validação humana deve ser registrada no relatório de implementação IMP-0024.

## 22. Critérios de aceite

### 22.1 Automáticos (verificáveis por testes)

- [ ] `SIGWINCH` instala handler somente em sessão TTY.
- [ ] Fluxo não-TTY não instala handler de SIGWINCH.
- [ ] Handler de SIGWINCH escreve no pipe e seta flag; não chama ioctl nem renderiza.
- [ ] `ioctl(TIOCGWINSZ)` é a primeira fonte consultada.
- [ ] ioctl válido prevalece sobre LINES/COLUMNS.
- [ ] LINES e COLUMNS somente aceitos como par; uma variável ausente invalida.
- [ ] String não convertível invalida o par.
- [ ] Zero ou negativo invalida o par.
- [ ] Inicialização sem fontes válidas usa `(80, 24)`.
- [ ] Após início da sessão, falha de todas as fontes retorna últimas dimensões válidas.
- [ ] Par inválido não substitui estado dimensional válido.
- [ ] Par inválido não aciona redesenho.
- [ ] Par válido diferente das dimensões atuais aciona redesenho.
- [ ] Par válido igual às dimensões atuais não aciona redesenho adicional.
- [ ] Largura e altura atualizadas como par coerente.
- [ ] Redução válida gera quadro com linhas de `nova_largura` chars e `nova_altura` linhas.
- [ ] Ampliação válida gera quadro com linhas de `nova_largura` chars e `nova_altura` linhas.
- [ ] `corpo.arranjo` não é alterado por resize.
- [ ] `tiling` não é alterado por resize.
- [ ] `_quadro_minimo_aviso(largura, altura)` tem exatamente `altura` linhas.
- [ ] Nenhuma linha de `_quadro_minimo_aviso` excede `largura` chars.
- [ ] `_tela_pequena_demais(9, 24)` → `True`; `(10, 24)` → `False`.
- [ ] `_tela_pequena_demais(80, 5)` → `True`; `(80, 6)` → `False`.
- [ ] Handler anterior restaurado ao final (saída normal e exceção no loop).
- [ ] Wakeup pipe fechado ao final (saída normal e exceção no loop).
- [ ] Falha em `os.pipe()` não tenta fechar descritores inexistentes.
- [ ] Falha em `os.set_blocking` fecha ambos os descritores do pipe.
- [ ] Falha em `_iniciar_sessao_tui` fecha o pipe e não chama `_encerrar_sessao_tui`.
- [ ] `_iniciar_sessao_tui` realiza rollback interno completo quando `write`/`flush`
      falha após `setcbreak`: restauração visual tentada antes de `termios`.
- [ ] Falha parcial da entrada TUI não deixa alternate screen ativo.
- [ ] Falha parcial não deixa cursor oculto.
- [ ] Falha parcial não deixa autowrap desativado.
- [ ] Restauração visual é tentada antes da restauração de `termios` no rollback interno.
- [ ] Restauração de `termios` é tentada mesmo quando rollback visual falhar.
- [ ] Exceção original de `_iniciar_sessao_tui` é preservada quando rollback visual falhar.
- [ ] Exceção original de `_iniciar_sessao_tui` é preservada quando `tcsetattr` de rollback falhar.
- [ ] `sessao_iniciada` somente passa a `True` após inicialização completa bem-sucedida.
- [ ] Cleanup externo não recebe estado inexistente quando `_iniciar_sessao_tui` falha.
- [ ] Testes cobrem falha de `write` antes de qualquer emissão, após alternate screen,
      após cursor oculto, após autowrap desativado, após limpeza/posicionamento e
      durante `flush`.
- [ ] Testes simulam emissão parcial e falha de flush com mocks de `sys.stdout`.
- [ ] Encerramento normal e rollback de inicialização usam a mesma sequência visual
      (via `_restaurar_efeitos_visuais_tui`).
- [ ] `_restaurar_efeitos_visuais_tui` não lança exceção própria.
- [ ] Falha em `_instalar_handler_sigwinch` fecha o pipe e restaura a sessão TUI.
- [ ] Handler não instalado não é restaurado no cleanup.
- [ ] Handler é restaurado antes do fechamento de `w_wakeup`.
- [ ] Falha em etapa de cleanup não interrompe as etapas seguintes.
- [ ] Exceção original do `try` é preservada em face de erros secundários de cleanup.
- [ ] `\x1b[2J` não presente em redesenho por resize (inspeção de código).
- [ ] Escrita atômica e synchronized output preservados.
- [ ] `_apresentar_quadro` aceita `largura` como parâmetro; sem `largura`, fallback a `shutil.get_terminal_size`.
- [ ] Todos os testes das seções 1–7 de `teste_demo.py` continuam passando.

### 22.2 Por pseudo-TTY

- [ ] Aplicação iniciada em pseudo-TTY responde a SIGWINCH com saída coerente.
- [ ] Aplicação continua ativa após SIGWINCH.
- [ ] Aplicação encerra com código 0 após Esc em pseudo-TTY.
- [ ] Restauração de terminal verificável após encerramento.

### 22.3 Por validação humana (obrigatória e separada)

- [ ] Validação humana realizada em TTY real conforme seção 21.
- [ ] Todos os critérios da tabela da seção 21.1 aprovados.
- [ ] Resultado registrado no IMP-0024.

## 23. Relatório de implementação esperado

Identificador: `docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md`

O relatório deve registrar:

- Arquivos alterados (`tela/demo.py`, `tela/teste_demo.py`).
- Funções adicionadas e modificadas, com localização de linha.
- Ordem de aquisição dos recursos e sentinelas/flags usados (`r_wakeup`,
  `w_wakeup`, `sessao_iniciada`, `handler_instalado`, `handler_anterior`).
- Alteração em `_iniciar_sessao_tui`: rollback interno completo implementado —
  localização do `try/except`, função auxiliar `_restaurar_efeitos_visuais_tui`
  introduzida e usada por `_iniciar_sessao_tui` e `_encerrar_sessao_tui`.
- Mecanismo de rollback visual: sequências emitidas na restauração; ordem entre
  restauração visual e `termios` no rollback interno; cobertura de emissão parcial
  da sequência de entrada.
- Sequências reutilizadas: confirmação de que rollback e `_encerrar_sessao_tui`
  usam a mesma função auxiliar e as mesmas sequências visuais.
- Preservação da exceção primária: como erros de rollback visual e `tcsetattr`
  são silenciados sem substituir a exceção original de inicialização.
- Testes de escrita parcial: como foi simulada a emissão parcial da sequência
  de entrada nos testes automatizados.
- Testes de falha de flush na inicialização TUI.
- Testes de falha durante rollback (rollback visual e `tcsetattr`).
- Confirmação de que o terminal real não foi modificado pelos testes automatizados
  (uso de mocks de `sys.stdout`, `termios` e `tty`).
- Validação humana ainda pendente (ver seção 21).
- Mecanismo de wakeup pipe: como o pipe foi criado, configurado e fechado.
- Cleanup em falha de `os.pipe()`: comportamento confirmado.
- Cleanup em falha de `os.set_blocking()`: comportamento confirmado.
- Cleanup em falha de início da sessão TUI: comportamento confirmado.
- Cleanup em falha de instalação do handler: comportamento confirmado.
- Ordem de restauração no `finally` (condicional): correspondência com a
  seção 18.1 confirmada.
- Mecanismo de ioctl: struct format, campos lidos, conversão.
- Validação e fallback: como `_par_dimensoes_valido` foi aplicado em cada
  ponto da cadeia.
- Integração com o loop: como o select duplo substitui a chamada direta a
  `_ler_tecla_sessao`.
- Handler anterior: como foi salvo e restaurado.
- Comportamento em resize válido: evidência de redesenho.
- Comportamento em resize inválido: evidência de não redesenho.
- Quadro mínimo: como foi gerado e quando foi exibido.
- Testes executados: lista e resultado (passou/falhou), incluindo testes de
  falhas parciais da seção 19.6.
- Resultado do pseudo-TTY: como foi executado, saída observada.
- Itens que dependem de validação humana (seção 21): registrar que a validação
  foi ou não realizada.
- Estado Git ao final da implementação.
- Limitações e bloqueios identificados durante a implementação.

O relatório **não** deve ser criado neste handoff. Será criado pelo implementador
ao concluir a implementação.

## 24. Condições de bloqueio

Parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

- A integração do select duplo exigir nova decisão arquitetural não coberta
  por este handoff.
- O mecanismo de wakeup pipe conflitar com alguma política da ADR-0016.
- O `_quadro_minimo_aviso` não puder ser gerado de forma coerente para
  alguma combinação de `largura >= 1, altura >= 1`.
- `fcntl`, `struct` ou `signal` não estiverem disponíveis no ambiente
  (violação de escopo POSIX).
- A lista de arquivos permitidos não for suficiente para a implementação.

Parar com `BLOCKED_EVIDENCE` se:

- `RELATORIO_QA_APLICACAO_ADR-0017.md` não contiver status
  `ADR_APPLICATION_APPROVED_WITH_NOTES`.
- Alguma autoridade obrigatória da seção 3 não existir.
- O estado Git real divergir do estado comprovado na seção 2.2 (estado
  posterior à criação e aprovação documental do H-0023).

## 25. Proibição de commit

O implementador **não** deve fazer `git add`, `git commit`, `git push` ou
qualquer alteração de histórico Git. A preparação de commit é etapa posterior,
separada da implementação.

## 26. Limite de encerramento

Concluída a implementação e os testes, pare. Não faça QA do próprio trabalho,
não crie relatório de implementação neste handoff, não prepare commit, não gere
prompt para a etapa seguinte.
