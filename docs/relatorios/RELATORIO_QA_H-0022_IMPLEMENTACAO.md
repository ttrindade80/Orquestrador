# Relatório de QA — implementação do H-0022

## 1. Status final

**APROVADO_COM_RESSALVAS**

Não foram encontrados achados bloqueantes. A implementação satisfaz todos os critérios verificáveis automaticamente. Permanecem sete critérios expressamente não verificáveis por este agente, pendentes de teste manual humano antes da aceitação final. Há ainda uma ressalva processual: o IMP-0023 fez classificação item a item reservada à Fase 6.

## 2. Verificação item a item dos critérios de aceite

### Item 1 — Ativação somente com stdin e stdout TTY

1. **SIM.** A guarda exata `sys.stdin.isatty() and sys.stdout.isatty()` está em `tela/demo.py:302`.
2. **SIM.** O ramo não-TTY está em `tela/demo.py:322-333`, lê `sys.stdin` linha a linha e não chama as rotinas de sessão. `python tela/teste_demo.py`, seção 7G, confirmou ausência de `\x1b[?1049h`, `\x1b[?25l`, `\x1b[?7l` e `\x1b[?2026h` na saída via pipe.
3. **SIM.** `printf 'b\ns\n' | python tela/demo.py ; echo "EXIT: $?"` produziu `EXIT: 0`.

**Resultado do item: SIM.**

### Item 2 — cbreak, não raw

1. **SIM.** `_iniciar_sessao_tui` chama `tty.setcbreak(fd_stdin)` em `tela/demo.py:236`; o teste funcional da seção 7B passou.
2. **SIM.** `grep -c 'setraw' tela/demo.py` retornou exatamente `0`.
3. **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano.** A ausência de progressão diagonal precisa ser observada em TTY interativo real.

**Resultado do item: PARCIAL**, exclusivamente pelo critério manual pendente.

### Item 3 — Alternate screen e cursor

1. **SIM.** `\x1b[?1049h` e `\x1b[?25l` são emitidos na entrada em `tela/demo.py:237`; o teste funcional da seção 7B passou.
2. **SIM.** `\x1b[?25h` e `\x1b[?1049l` são emitidos na saída em `tela/demo.py:253`; o teste funcional da seção 7C passou.
3. **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano.** O retorno ao conteúdo pré-sessão e a visibilidade efetiva do cursor após Esc exigem TTY real.

**Resultado do item: PARCIAL**, exclusivamente pelo critério manual pendente.

### Item 4 — Autowrap desativado e restaurado

1. **SIM.** `\x1b[?7l` é emitido na entrada em `tela/demo.py:237`.
2. **SIM.** `\x1b[?7h` é emitido na saída em `tela/demo.py:253`.
3. **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano.** A ausência de scroll ao atingir a última coluna requer observação em terminal real.

**Resultado do item: PARCIAL**, exclusivamente pelo critério manual pendente.

### Item 5 — Posicionamento absoluto linha a linha

1. **SIM.** `_apresentar_quadro` precede cada linha com `\x1b[{0};1H` em `tela/demo.py:274-277`. A seção 7D confirmou `\x1b[1;1H` e `\x1b[2;1H`.
2. **SIM.** Embora `split("\n")` separe as linhas lógicas, a saída é montada com `"".join(partes)` e não contém newline (`tela/demo.py:269-281`); a seção 7D confirmou `"\n" not in conteudo_quadro`.
3. **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano.** O alinhamento visual independentemente da posição anterior do cursor exige TTY real.

**Resultado do item: PARCIAL**, exclusivamente pelo critério manual pendente.

### Item 6 — Preenchimento até a largura do terminal

1. **SIM.** A largura vem de `shutil.get_terminal_size(...).columns`, e cada linha recebe espaços calculados por `pad = w - len(linha)` em `tela/demo.py:268-277`. O teste da seção 7D, com largura 10, confirmou `AB` e `CD` preenchidos até 10 caracteres.
2. **SIM.** `shutil.get_terminal_size` está presente em `tela/demo.py:268` e `tela/demo.py:297`.
3. **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano.** A ausência visual de resíduos de quadro anterior requer atualização observada em TTY real.

**Resultado do item: PARCIAL**, exclusivamente pelo critério manual pendente.

### Item 7 — Escrita atômica e limpeza única

1. **SIM.** `_apresentar_quadro` concatena o quadro e realiza uma chamada a `write()` seguida de uma chamada a `flush()` em `tela/demo.py:273-281`. A seção 7D confirmou uma chamada de cada por quadro, inclusive no segundo quadro.
2. **SIM.** `grep -c '\\x1b\[2J' tela/demo.py` retornou exatamente `1`. A única ocorrência está na inicialização, em `tela/demo.py:237`, fora do loop de redesenho.
3. **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano.** A ausência de flash/cintilação ao pressionar `b` exige observação humana em TTY real.

**Resultado do item: PARCIAL**, exclusivamente pelo critério manual pendente.

### Item 8 — Synchronized output por atualização

1. **SIM.** `\x1b[?2026h` inicia o quadro em `tela/demo.py:273`.
2. **SIM.** `\x1b[?2026l` encerra o quadro em `tela/demo.py:278`.
3. **SIM.** As sequências pertencem a `_apresentar_quadro`, chamada para o quadro inicial em `tela/demo.py:306` e dentro do loop de atualização em `tela/demo.py:317`. A seção 7D confirmou que cada quadro começa e termina com essas sequências.

**Resultado do item: SIM.**

### Item 9 — Ctrl+C escopado

1. **SIM.** A configuração usa `tty.setcbreak` e não contém operação que mascare `ISIG` (`tela/demo.py:228-239`).
2. **SIM.** O context manager reutilizável `captura_interrupcao_de_script` está em `tela/demo.py:212-225` e suprime somente `KeyboardInterrupt`.
3. **SIM.** O `try/except KeyboardInterrupt` envolve leitura, processamento, carregamento, renderização e apresentação no corpo do loop em `tela/demo.py:307-319`; a interrupção é ignorada por `continue`.
4. **SIM.** Existe captura de `KeyboardInterrupt` fora do `finally`, em `tela/demo.py:318-319`, além da captura escopada pelo `__exit__` em `tela/demo.py:224-225`.
5. **SIM.** O mecanismo reutilizável é testado isoladamente em `tela/teste_demo.py:1446-1477`, com `KeyboardInterrupt`, execução normal e `ValueError`. A seção 7H (`tela/teste_demo.py:1583-1639`) também injeta `KeyboardInterrupt` durante `processar_comando` e confirma que o loop continua.

**Proibição de fluxo inventado: atendida.** `tela/demo.py` não contém `subprocess`, `Popen`, `exec(` ou `eval(` e o mecanismo não é ligado a fluxo fictício de execução. As ocorrências de `subprocess` em `tela/teste_demo.py` são infraestrutura de testes da própria demo.

**Resultado do item: SIM.**

### Item 10 — Restauração completa em finally

1. **SIM.** O `finally` de `tela/demo.py:305-321` cobre o loop principal e chama `_encerrar_sessao_tui`; essa função restaura os atributos originais em `tela/demo.py:248-250` e emite autowrap, cursor e alternate screen de saída em `tela/demo.py:253`.
2. **SIM.** Esc produz `break` dentro do `try`; exceções não tratadas atravessam o `finally`; Ctrl+C fora do mecanismo é capturado dentro do loop, que permanece sob o mesmo `try`. A seção 7F confirmou restauração simulada após exceção.
3. **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano.** A identidade efetiva do estado do terminal após encerramento normal exige TTY real.

**Resultado do item: PARCIAL**, exclusivamente pelo critério manual pendente.

### Item 11 — Comportamento não-TTY preservado

1. **SIM.** O ramo de `tela/demo.py:322-333` usa `for linha in sys.stdin` e `print(..., end="")`, sem rotinas de sessão TUI.
2. **SIM.** O comando obrigatório produziu código 0; a seção 7G confirmou stderr vazio.
3. **SIM.** A seção 7G comparou `b\ns\n` com `b\n\x1b\n` e confirmou código 0 e stdout idêntico (`tela/teste_demo.py:1562-1579`).
4. **SIM.** A seção 7G confirmou ausência de `\x1b[?1049h`, `\x1b[?25l`, `\x1b[?7l` e `\x1b[?2026h` na saída capturada.

**Resultado do item: SIM.**

### Testes e comandos obrigatórios

- `python tela/teste_demo.py`: código **0**; **172/172** verificações passaram.
- `printf 'b\ns\n' | python tela/demo.py ; echo "EXIT: $?"`: `EXIT: 0`.
- `grep -c '\\x1b\[2J' tela/demo.py`: **1**.
- `grep -c 'setraw' tela/demo.py`: **0**.
- `git stash list`: contém `stash@{0}: On master: pre-H-0022`.

### Escopo observado

Antes da atualização deste relatório, `git status --short` mostrou somente arquivos autorizados pela lista especial desta auditoria: `docs/adr/INDICE_ADR.md`, `tela/demo.py`, `tela/teste_demo.py`, ADR-0016, H-0022, IMP-0022, IMP-0023, os relatórios das fases anteriores e este relatório. `git diff --stat` mostrou `docs/adr/INDICE_ADR.md`, `tela/demo.py` e `tela/teste_demo.py`. Conforme a instrução expressa da auditoria, `INDICE_ADR.md` e os artefatos das fases anteriores são ruído esperado do fluxo sem commits intermediários e não constituem violação bloqueante. Nenhum arquivo fora da lista permitida apareceu.

## 3. Conformidade processual do IMP-0023

**Achado processual confirmado, não bloqueante.** `docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md:41-179` contém classificação item a item, e `:181-195` contém tabela de status dos itens 1–11. Esse julgamento era escopo exclusivo da Fase 6 e não deveria ter sido feito na Fase 5.

As classificações técnicas dos itens 1–11 foram confrontadas com o código e os comandos e não se mostraram factualmente incorretas. Portanto, o achado permanece não bloqueante. Há uma imprecisão adicional não bloqueante em `IMP-0023:177`: o relatório registra 169/169 verificações, enquanto a versão auditada executou 172/172, incluindo a cobertura adicional da seção 7H.

## 4. Achados bloqueantes

**Nenhum.**

## 5. Ressalvas não bloqueantes

1. **ACH-NB-01 — julgamento indevido na Fase 5.** O IMP-0023 classifica os itens 1–11 e inclui tabela de status, invadindo o escopo de QA da Fase 6 (`docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md:41-195`).
2. **ACH-NB-02 — contagem de testes desatualizada no IMP-0023.** O relatório afirma 169/169 em `docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md:177`; a execução atual produziu 172/172. Isso não altera a conformidade dos critérios.

## 6. Critérios não verificáveis por este agente

Todos permanecem pendentes de teste manual humano antes da aceitação final:

1. Item 2, checkbox 3 — ausência de progressão diagonal em TTY real.
2. Item 3, checkbox 3 — conteúdo pré-sessão recuperado e cursor visível após Esc.
3. Item 4, checkbox 3 — ausência de scroll ao atingir a última coluna.
4. Item 5, checkbox 3 — quadro alinhado à esquerda independentemente da posição anterior do cursor.
5. Item 6, checkbox 3 — ausência visual de resíduos do quadro anterior.
6. Item 7, checkbox 3 — ausência de flash/cintilação entre quadros ao pressionar `b`.
7. Item 10, checkbox 3 — terminal efetivamente idêntico ao estado anterior após encerramento normal.

Para cada um deles, a classificação é: **NÃO VERIFICÁVEL POR ESTE AGENTE — requer teste manual humano**.

## 7. Integridade desta auditoria

Nenhum código, ADR, handoff ou outro relatório foi criado ou alterado por esta auditoria. O único arquivo alterado por este agente foi `docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md`.
