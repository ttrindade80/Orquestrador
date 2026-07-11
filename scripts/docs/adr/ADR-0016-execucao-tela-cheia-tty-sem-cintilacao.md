---
name: ADR-0016-execucao-tela-cheia-tty-sem-cintilacao
description: Sistema passa a executar em modo tela cheia via alternate screen quando stdin/stdout são TTY — entrada cbreak, desenho por posicionamento absoluto linha a linha, autowrap desativado, escrita atômica com synchronized output, e Ctrl+C escopado à execução de script interno
metadata:
  type: adr
  status: aceita
  data: 2026-07-10
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas:
    - docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_processo_desenvolvimento.md
  handoffs_bloqueados:
    - docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
---

# ADR-0016 — Execução em tela cheia (TTY) sem cintilação, com Ctrl+C escopado

## Status

`aceita`

## Data

2026-07-10

## Contexto

O handoff H-0009 estabeleceu detecção de TTY isolada (`sys.stdin.isatty()`) com
leitura tecla a tecla sem Enter e sem echo, mas sem controle de sessão completa
(sem alternate screen, sem modo de entrada normatizado).

A implementação registrada em
`docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md` avançou
para sessão TUI completa — alternate screen (`\x1b[?1049h/l`), cursor oculto,
redesenho por substituição de quadro — **sem que uma ADR precedesse a
implementação** e **sem que um handoff formal precedesse aquela tentativa**.
Naquele estado anterior, havia apenas o relatório de implementação; o rótulo
"H-0022" aparecia somente nos metadados internos do próprio relatório, sem
documento de handoff correspondente. Isso violou a seção 5 (ciclo padrão,
item 3: "Registrar ADR se houver decisão arquitetural") e a seção 6 ("nenhuma
mudança de contrato pode ser escondida em implementação") do
`contrato_processo_desenvolvimento.md` — em grau duplo: faltou tanto a ADR
quanto o handoff precedentes.

Essa implementação apresentou falha funcional observada em uso real:

1. **Modo de entrada `tty.setraw()` é amplo demais.** `setraw()` desliga
   `ICANON`, `ECHO`, `ISIG` **e** `OPOST` de uma vez. Sem `OPOST`, o driver do
   terminal deixa de converter `\n` em "retorno de coluna + avanço de linha"
   automaticamente — cada linha nova nasce na coluna onde a anterior parou,
   produzindo uma progressão diagonal ("escada") em vez de quadro alinhado.
2. **Limpeza de tela (`\x1b[2J`) a cada quadro** produz cintilação perceptível
   — o terminal fica em branco por um instante antes do conteúdo novo chegar.
3. **Ausência de política de autowrap (DECAWM)** deixa em aberto o risco de
   scroll acidental quando uma linha do quadro atinge a última coluna do
   terminal.
4. **Ausência de escopo definido para Ctrl+C** — a sessão não define se
   `SIGINT` deve encerrar a aplicação, ser ignorado, ou ser tratado de forma
   diferente durante a execução de um script interno disparado pela própria
   aplicação.

Esta ADR fecha essas lacunas normativas antes de qualquer nova tentativa de
implementação. Ela **não corrige código** — define a política que um handoff
corretivo deve seguir.

## Decisão

**1. Ativação da sessão TUI** ocorre somente quando
`sys.stdin.isatty() and sys.stdout.isatty()` (mantido de H-0009 e da
implementação registrada em IMP-0022).

**2. Modo de entrada: `cbreak`, não `raw`.**
`tty.setcbreak()` (ou `termios` seletivo manual com resultado equivalente)
desliga apenas `ICANON` e `ECHO`. `OPOST` e `ISIG` permanecem preservados dos
atributos originais do terminal. `tty.setraw()` é rejeitado nesta política.

**3. Alternate screen buffer.**
Entrada de sessão: `\x1b[?1049h` (alternate screen) + `\x1b[?25l` (oculta
cursor). Saída de sessão: `\x1b[?25h` (mostra cursor) + `\x1b[?1049l` (sai do
alternate screen). Mantido da implementação registrada em IMP-0022.

**4. Autowrap (DECAWM) desativado durante a sessão.**
`\x1b[?7l` emitido na entrada da sessão; `\x1b[?7h` emitido na saída,
garantindo que nenhuma linha do quadro provoque scroll automático por atingir
a última coluna do terminal.

**5. Desenho de quadro por posicionamento absoluto linha a linha.**
Cada linha lógica do quadro é precedida por `CSI <linha>;1H` (posicionamento
absoluto) antes de ser escrita. O desenho não depende do comportamento de
`\n` para retorno de coluna — mesmo mecanismo usado por aplicações de tela
cheia como `nano`/`vi`.

**6. Preenchimento de linha até a largura total.**
Cada linha escrita é preenchida com espaços até a largura do terminal
(`shutil.get_terminal_size`), garantindo que conteúdo de um quadro anterior
nunca fique visível atrás do conteúdo novo, mesmo quando a linha nova é mais
curta.

**7. Escrita atômica por quadro.**
Todas as sequências de posicionamento e o conteúdo de todas as linhas de um
quadro são concatenados em uma única string e emitidos em uma única chamada
de `write()` seguida de uma única `flush()`. A limpeza de tela (`\x1b[2J`)
ocorre **uma única vez**, na entrada da sessão — nunca é repetida a cada
quadro.

**8. Synchronized output mode.**
`\x1b[?2026h` é emitido antes do conteúdo do quadro e `\x1b[?2026l` depois,
em toda atualização de quadro durante a sessão TUI. Terminais sem suporte a
essa sequência a ignoram sem efeito colateral; nenhuma detecção de
capacidade é realizada.

**9. Ctrl+C (SIGINT) permanece habilitado, com escopo definido.**
`ISIG` não é desligado (decorrência de `cbreak`, item 2). Comportamento
normativo:

- **Durante execução de script/processo interno** disparado pela aplicação:
  `KeyboardInterrupt` é capturado no escopo dessa chamada — interrompe
  apenas o script em execução; a sessão TUI permanece ativa.
- **Fora desse escopo** (navegação entre telas, menus): `KeyboardInterrupt`
  é capturado e **ignorado silenciosamente** — não encerra a aplicação. A
  única saída normatizada da sessão TUI continua sendo Esc.

**10. Restauração garantida do terminal.**
Atributos `termios` originais, autowrap, cursor e alternate screen são
restaurados em `finally` que protege lexicalmente o loop completo da sessão
TUI. Ctrl+C fora do escopo de script continua sendo capturado e ignorado no
loop (item 9), mantendo a sessão ativa e sem executar imediatamente a
restauração; o `finally` executa quando o loop efetivamente termina, por Esc
ou por exceção não tratada.

**11. Comportamento não-TTY preservado sem alteração.**
Mantido de H-0009/H-0021: leitura linha a linha de `sys.stdin`, `print(...,
end="")`, nenhuma sequência ANSI de sessão emitida.

## Consequências

### Obrigatórias

- **A implementação registrada em IMP-0022 é tratada como inválida** quanto a
  modo de entrada (`raw` em vez de `cbreak`) e política de redesenho (limpeza
  de tela a cada quadro, sem escrita atômica, sem autowrap/synchronized
  output normatizados). Permanece como evidência histórica da tentativa
  anterior e não deve ser usada como base sem correção.
- `contrato_tela_json.md` passa a registrar a política completa de execução
  TTY (itens 1–11 desta ADR) como seção normativa. `contrato_console.md`
  passa a registrar apenas o item 9 (escopo de Ctrl+C durante execução de
  script interno), por ser este o único item de sua alçada — conforme
  detalhado na tabela de artefatos abaixo.
- O H-0022 foi posteriormente criado em
  `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md` para materializar
  a correção definida por esta ADR. Esta menção não aprova o handoff, não
  aprova implementação e não transforma relatórios ou código em autoridade
  normativa.
- A ausência de saída de emergência alternativa a Esc (Ctrl+C ignorado fora
  de escopo de script) é um risco aceito por esta ADR — se o terminal travar
  por outro motivo, o usuário depende de mecanismos externos (fechar a aba,
  `kill` do processo).

### Artefatos a atualizar em tarefa subsequente

| Arquivo | Atualização mínima |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar ADR-0016 |
| `docs/contratos/contrato_tela_json.md` | Registrar seção normativa de modo de execução TTY (itens 1–11 desta ADR) |
| `docs/contratos/contrato_console.md` | Registrar escopo de Ctrl+C durante execução de script interno |
| `docs/contratos/contrato_processo_desenvolvimento.md` | Registrar a implementação de IMP-0022 como caso de violação dupla do ciclo padrão (sem ADR e sem handoff precedentes), para referência processual futura |

### Arquivos que NÃO devem ser alterados por esta ADR

| Arquivo ou grupo | Motivo |
|---|---|
| `tela/demo.py` e demais módulos de código | Implementação pertence ao handoff corretivo, não a esta ADR |
| `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md` | Artefato histórico não é reescrito nem apagado; permanece como evidência da tentativa anterior supersedida |
| `config/` | Não afetado por decisão de modo de execução TTY |

### Pendências derivadas

- O H-0022 existente materializa a correção documentalmente dependente desta
  ADR e deve referenciar IMP-0022 apenas como evidência histórica do problema,
  sem transformar a tentativa anterior em autoridade normativa.
- Handoff futuro de redimensionamento reativo (`SIGWINCH`) permanece fora do
  escopo desta ADR. Não há número reservado para ele; sua numeração será
  atribuída somente no momento em que for de fato criado.

## Fora do escopo

- Redimensionamento reativo da janela do terminal (`SIGWINCH`) — tratado em
  handoff futuro, sem número reservado. A numeração de handoffs segue a
  ordem real de execução no momento da criação, não reserva antecipada; a
  menção anterior a "H-0023" para este tema (originada em IMP-0022) não
  constitui reserva válida.
- Suporte a terminais não compatíveis com ANSI/VT/xterm, e suporte Windows.
- Detecção de capacidade de terminal via `terminfo` — a política assume
  compatibilidade ANSI/VT/xterm, mantendo a política estreita já implícita
  desde H-0009 (uso direto de `termios`/`tty` sem guarda de `ImportError`).
- Biblioteca `curses`/`textual`/`rich` — permanece proibida, conforme H-0009.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar |
|---|---|
| `tty.setraw()` para a sessão inteira | Desliga `OPOST` junto com `ICANON`/`ECHO`; causa progressão diagonal de linhas (falha observada na implementação registrada em IMP-0022) |
| Quadro integral com `\r\n` (sem posicionamento absoluto) | Não resolve o risco de autowrap na última coluna da última linha; menos defensivo que posicionamento absoluto |
| Manter autowrap ativo | Risco de scroll acidental quando uma linha atinge a largura total do terminal |
| Limpar tela (`\x1b[2J`) a cada quadro | Causa cintilação perceptível (tela em branco entre quadros); causa raiz do problema relatado nesta ADR |
| Múltiplas chamadas de `write()` por quadro (uma por linha) | Permite redesenho parcial visível entre chamadas, produzindo cintilação mesmo sem erro de posicionamento |
| Não usar synchronized output | Abre mão de redução adicional de cintilação em terminais compatíveis, sem custo de compatibilidade (fallback seguro em terminais sem suporte) |
| Ctrl+C sempre mata o processo (ISIG padrão sem escopo) | Não atende ao requisito de permitir interromper apenas um script em execução, mantendo a sessão TUI viva |
| Desligar `ISIG` e tratar `SIGINT` manualmente em baixo nível | Complexidade desnecessária — `cbreak` já preserva `ISIG`, e escopar a captura de `KeyboardInterrupt` no código resolve o requisito sem tocar em flags adicionais |
| `curses` | Muda a arquitetura da renderização (deixa de ser função pura que retorna string); desproporcional ao estágio atual do projeto, conforme já rejeitado em H-0009 |
