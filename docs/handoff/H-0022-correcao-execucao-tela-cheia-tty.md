---
name: H-0022-correcao-execucao-tela-cheia-tty
description: Handoff de implementação — substituição completa da sessão TUI em tela/demo.py e tela/teste_demo.py conforme ADR-0016: modo cbreak, alternate screen, autowrap desativado, posicionamento absoluto linha a linha, escrita atômica, synchronized output, Ctrl+C escopado
metadata:
  type: handoff
  status: proposto
  data: 2026-07-10
rastreabilidade:
  adr_base: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
  escopo_permitido:
    - tela/demo.py
    - tela/teste_demo.py
  implementacao_anterior:
    - docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
---

# H-0022 — Correção da execução em tela cheia (TTY) conforme ADR-0016

## Objetivo

Implementar os itens 1–11 da seção Decisão da ADR-0016 em `tela/demo.py` e
`tela/teste_demo.py`, **substituindo por completo** a implementação anterior
registrada em
`docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md`.

Esta substituição não é um ajuste incremental — a implementação anterior é
declarada inválida pela ADR-0016 quanto ao modo de entrada (`tty.setraw()` em
vez de `cbreak`) e à política de redesenho (limpeza de tela repetida a cada
quadro, sem escrita atômica, sem autowrap/synchronized output normatizados).

## Relação com a implementação anterior

Este documento é a **primeira vez que um handoff cobre este escopo**. Quando a
tentativa anterior foi executada e registrada em
`docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md`, não havia
handoff precedente para aquele trabalho. Este H-0022 foi criado posteriormente
para formalizar a correção. A ADR-0016 aponta estruturalmente para o H-0022 no
campo `handoffs_bloqueados` de sua rastreabilidade — indicando o H-0022 como
handoff dependente da ADR, auditado separadamente; esse campo não confirma
inexistência anterior do H-0022.

`docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md` é citado
apenas como **evidência histórica do problema**: modo `raw` causando progressão
diagonal de linhas (efeito escada), e cintilação por limpeza de tela repetida
a cada quadro. Esse relatório não deve ser usado como base de código para este
handoff e não constitui autoridade normativa.

## Pré-requisito antes da implementação

`tela/demo.py` e `tela/teste_demo.py` contêm alterações não commitadas
resultantes da tentativa de implementação anterior (sem handoff). Antes de
iniciar a implementação deste handoff, essas alterações devem ser
**preservadas** via:

```bash
git stash push -m "pre-H-0022" -- tela/demo.py tela/teste_demo.py
```

Esse comando deixa a árvore de trabalho limpa nesses dois arquivos sem
descartar as alterações — elas ficam guardadas no stash e podem ser consultadas
como referência histórica, se necessário. **Este handoff não executa esse
comando** — é uma pré-condição documentada para a etapa de implementação, de
responsabilidade do engenheiro ou executor que iniciar este ciclo.

## Escopo permitido

Apenas os arquivos abaixo podem ser criados ou alterados na implementação deste
handoff:

```
tela/demo.py          — ALTERAR (substituição completa da sessão TUI)
tela/teste_demo.py    — ALTERAR (atualização dos critérios de teste)
```

A lista acima é exaustiva para código e testes da capacidade. O relatório de
implementação é um artefato processual obrigatório exigido pelo
`contrato_processo_desenvolvimento.md` seção 5 — sua criação não amplia o
escopo técnico da implementação e não está sujeita à cláusula exaustiva acima.
Nenhum outro arquivo técnico ou documental pode ser criado ou alterado. Se a
implementação exigir alterar qualquer outro arquivo além dos dois técnicos
acima, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

## Relatório de implementação esperado

Concluída a implementação técnica dos arquivos acima, o executor deve criar
exatamente um relatório em:

```
docs/relatorios/IMP-00NN-implementacao-h0022-tela-cheia-tty.md
```

onde `00NN` é o próximo número livre real em `docs/relatorios/`, verificado
no momento da criação — sem sobrescrever nem renomear relatório existente.

O relatório deve conter somente:

1. referência à ADR-0016 e ao H-0022;
2. identificação da versão implementada;
3. resumo técnico das alterações em `tela/demo.py` e `tela/teste_demo.py`;
4. comandos de teste executados e resultados literais;
5. lista dos arquivos técnicos alterados;
6. estado Git observado;
7. bloqueios, limitações e validações manuais ainda pendentes;
8. referência ao stash `pre-H-0022`, sem aplicá-lo ou removê-lo;
9. declaração de que a implementação permanece pendente de QA separado.

O relatório não pode:

- aprovar a implementação;
- classificar formalmente os itens 1–11 como conformes;
- substituir o QA;
- corrigir ADR, contratos ou handoff;
- preparar fechamento ou commit.

## Critérios de aceite

Os critérios abaixo traduzem cada um dos itens 1–11 da Decisão da ADR-0016 em
verificações observáveis e testáveis.

### Item 1 — Ativação da sessão TUI somente com stdin e stdout TTY

- [ ] `demo.py` contém guarda `sys.stdin.isatty() and sys.stdout.isatty()` (ou
      estrutura equivalente) como condição de ativação da sessão TUI.
- [ ] Executado via pipe (`printf 'b\ns\n' | python tela/demo.py`), o processo
      não emite sequências de alternate screen nem ativa modo cbreak.
- [ ] Executado via pipe, o processo encerra com código 0 sem erro.

### Item 2 — Modo de entrada: cbreak, não raw

- [ ] `demo.py` contém `tty.setcbreak` (ou configuração `termios` equivalente
      que preserve `OPOST` e `ISIG`).
- [ ] `demo.py` **não contém** `tty.setraw` em nenhuma parte do código
      (inspeção: ausência da string `setraw` no arquivo).
- [ ] Em sessão TTY real, linhas desenhadas não produzem progressão diagonal
      (cada linha inicia na coluna 1).

### Item 3 — Alternate screen buffer com cursor oculto e restaurado

- [ ] `demo.py` contém a sequência de entrada `\x1b[?1049h` (alternate screen)
      e `\x1b[?25l` (oculta cursor).
- [ ] `demo.py` contém a sequência de saída `\x1b[?25h` (restaura cursor) e
      `\x1b[?1049l` (sai do alternate screen).
- [ ] Ao sair da sessão (Esc), o terminal retorna ao conteúdo pré-sessão e o
      cursor está visível (verificação manual de QA).

### Item 4 — Autowrap (DECAWM) desativado e restaurado

- [ ] `demo.py` contém `\x1b[?7l` emitido na entrada da sessão (desativa
      autowrap).
- [ ] `demo.py` contém `\x1b[?7h` emitido na saída da sessão (restaura
      autowrap).
- [ ] Nenhuma linha do quadro provoca scroll automático ao atingir a última
      coluna do terminal durante a sessão (verificação manual de QA).

### Item 5 — Desenho por posicionamento absoluto linha a linha

- [ ] Cada linha lógica do quadro é precedida por sequência `\x1b[<n>;1H`
      (posicionamento absoluto na coluna 1) antes de ser escrita.
- [ ] `demo.py` **não depende de `\n`** para retorno de coluna durante o
      desenho de quadro em modo TTY (inspeção de código: ausência de `\n` como
      mecanismo de quebra de linha no loop de desenho).
- [ ] Em sessão TTY real, o quadro é desenhado corretamente alinhado à esquerda
      independentemente da posição anterior do cursor (verificação manual de QA).

### Item 6 — Preenchimento de linha até a largura do terminal

- [ ] Cada linha escrita é preenchida com espaços até a largura do terminal
      reportada por `shutil.get_terminal_size`.
- [ ] `demo.py` contém `shutil.get_terminal_size` (inspeção de código).
- [ ] Após atualização de quadro, nenhum conteúdo de quadro anterior permanece
      visível em posições que o conteúdo novo não alcança (verificação manual
      de QA).

### Item 7 — Escrita atômica por quadro; limpeza de tela apenas na entrada

- [ ] Todo o conteúdo de um quadro (posicionamentos + linhas preenchidas) é
      concatenado e emitido em uma única chamada `write()` seguida de uma única
      `flush()` por atualização.
- [ ] A sequência de limpeza de tela (`\x1b[2J`) ocorre **exatamente uma vez**
      em `demo.py`, na inicialização da sessão TTY — nunca dentro do loop de
      redesenho (inspeção: a string `\x1b[2J` aparece exatamente uma vez no
      arquivo, fora da lógica de loop; ausência total da sequência é não
      conformidade, não conformidade parcial).
- [ ] Em sessão TTY real, não há flash de tela em branco entre quadros
      (verificação manual de QA ao pressionar `b` para alternar borda).

### Item 8 — Synchronized output em cada atualização de quadro

- [ ] `demo.py` contém `\x1b[?2026h` (synchronized output on) emitido antes
      do conteúdo de cada quadro no loop de redesenho.
- [ ] `demo.py` contém `\x1b[?2026l` (synchronized output off) emitido após
      o conteúdo de cada quadro no loop de redesenho.
- [ ] As sequências de synchronized output estão dentro do loop de atualização,
      não apenas na entrada/saída da sessão.

### Item 9 — Ctrl+C escopado: mecanismo de captura preparado para uso futuro, ignorado fora desse escopo

**Nota de escopo:** `tela/demo.py` hoje não executa nenhum script ou processo
interno. Este critério exige apenas que o **mecanismo** de captura escopada
exista e seja testável isoladamente — não exige, e o executor não deve
inventar, nenhum fluxo de execução de script real só para satisfazer este
item. A funcionalidade de fato executar scripts é escopo futuro, fora deste
handoff.

- [ ] `ISIG` não é desligado na configuração `termios` (decorrência de `cbreak`;
      verificável por inspeção: ausência de `ISIG` em operação de mascaramento
      no código de configuração do terminal).
- [ ] `demo.py` fornece um mecanismo reutilizável (função ou context manager,
      ex.: `with captura_interrupcao_de_script():`) que captura
      `KeyboardInterrupt` localmente ao redor de um bloco de execução,
      preparado para uso futuro por uma funcionalidade de execução de
      script/processo que ainda não existe. Este mecanismo pode estar
      implementado sem estar em uso em nenhum ponto da UI atual.
- [ ] Fora desse mecanismo (ou seja, no restante do loop principal da sessão
      TUI), `KeyboardInterrupt` é capturado e ignorado silenciosamente — a
      sessão TUI permanece ativa.
- [ ] `demo.py` contém pelo menos um bloco `except KeyboardInterrupt` fora do
      `finally` de restauração do terminal (inspeção de código),
      correspondendo tanto ao mecanismo reutilizável quanto à captura
      silenciosa do loop principal.
- [ ] `teste_demo.py` testa o mecanismo reutilizável isoladamente (chamando-o
      diretamente e simulando `KeyboardInterrupt` dentro do bloco protegido),
      sem depender de nenhuma funcionalidade de execução de script real
      existir na UI.

### Item 10 — Restauração garantida do terminal em finally

- [ ] A restauração de atributos `termios` originais, autowrap (`\x1b[?7h`),
      cursor (`\x1b[?25h`) e alternate screen (`\x1b[?1049l`) está em bloco
      `finally` que cobre lexicalmente o loop principal da sessão TUI.
- [ ] O bloco `finally` de restauração executa quando o loop principal
      efetivamente termina — por Esc ou por exceção não tratada. Ctrl+C
      capturado e ignorado no loop (conforme Item 9) mantém a sessão ativa
      e não dispara imediatamente o `finally`; o `finally` não é executado
      enquanto o loop continua em execução. Exceção não tratada continua
      exigindo restauração antes da propagação.
- [ ] Após encerramento normal da demo, o terminal está em estado idêntico ao
      anterior à execução (sem alternate screen, autowrap e cursor restaurados,
      sem modo cbreak) — verificação manual de QA.

### Item 11 — Comportamento não-TTY preservado sem alteração

- [ ] Executado via pipe, `demo.py` lê `sys.stdin` linha a linha, sem emitir
      sequências ANSI de sessão TUI.
- [ ] `printf 'b\ns\n' | python tela/demo.py` encerra com código 0 e stderr
      vazio.
- [ ] `printf 'b\n\x1b\n' | python tela/demo.py` encerra com código 0 e produz
      saída idêntica à do comando anterior.
- [ ] Saída capturada em modo pipe não contém nenhuma das sequências
      `\x1b[?1049h`, `\x1b[?25l`, `\x1b[?7l`, `\x1b[?2026h`.

### Testes automatizados

- [ ] `python tela/teste_demo.py` retorna código 0 com cobertura mínima dos 11
      itens acima.
- [ ] Os testes cobrem: guarda TTY (inspeção de `isatty`), ausência de `setraw`
      (inspeção de código), presença das sequências de sessão (inspeção de
      código), escrita atômica com `\x1b[2J` presente exatamente uma vez e
      fora do loop (inspeção de código), synchronized output dentro do loop
      (inspeção de código), presença de `except KeyboardInterrupt` fora do
      `finally` (inspeção de código), presença de bloco `finally` de
      restauração (inspeção de código), e comportamento não-TTY correto via
      subprocess.

### Escopo e ausências

- [ ] Somente `tela/demo.py` e `tela/teste_demo.py` foram criados ou alterados.
- [ ] Nenhum outro arquivo foi modificado.
- [ ] Nenhum contrato, ADR, índice de ADR, handoff anterior, relatório anterior
      nem qualquer arquivo em `config/` foi alterado.

## Fora de escopo

- **Redimensionamento reativo da janela do terminal (`SIGWINCH`)** — declarado
  explicitamente como fora do escopo da ADR-0016. Receberá handoff próprio com
  numeração atribuída no momento de criação (sem número reservado antecipado).
- Suporte a terminais não compatíveis com ANSI/VT/xterm.
- Suporte Windows.
- Detecção de capacidade de terminal via `terminfo`.
- Bibliotecas `curses`, `textual`, `rich` — permanecem proibidas conforme H-0009.
- Qualquer outro tema listado como "Fora do escopo" na ADR-0016.
