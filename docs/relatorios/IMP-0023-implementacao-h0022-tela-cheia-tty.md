---
name: IMP-0023-implementacao-h0022-tela-cheia-tty
description: Relatório de implementação do handoff H-0022 — substituição completa da sessão TUI em tela/demo.py conforme ADR-0016
metadata:
  type: relatorio_implementacao
  handoff: docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
  adr_base: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
  data: 2026-07-10
---

# IMP-0023 — Implementação do H-0022: Correção da execução em tela cheia (TTY)

## Referências

- **Handoff normativo:** `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`
- **ADR base:** `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`
- **Implementação anterior (evidência histórica, inválida):**
  `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md`

## Arquivos alterados

Somente os dois arquivos listados no escopo permitido do H-0022 foram criados
ou alterados:

- `tela/demo.py` — substituição completa da sessão TUI
- `tela/teste_demo.py` — atualização dos critérios de teste (seção 7 reescrita)

Nenhum outro arquivo foi modificado.

## Pré-requisito executado

O stash da ETAPA B foi realizado com o comando:

```bash
git stash push -m "pre-H-0022" -- tela/demo.py tela/teste_demo.py
```

O stash `pre-H-0022` está disponível no repositório para consulta das
alterações anteriores não commitadas, caso necessário.

## Verificação dos critérios de aceite (Itens 1–11 da ADR-0016)

### Item 1 — Ativação da sessão TUI somente com stdin e stdout TTY

**Verificado automaticamente** por `python tela/teste_demo.py` (seção 7A e 7G):

- Inspeção: `"isatty" in texto_mod` → PASSOU
- Subprocess pipe `printf 'b\ns\n' | python tela/demo.py`:
  - Encerra com código 0 → PASSOU
  - Saída não contém `\x1b[?1049h`, `\x1b[?25l`, `\x1b[?7l`, `\x1b[?2026h` → PASSOU

Implementação: guarda `sys.stdin.isatty() and sys.stdout.isatty()` em `main()`.

### Item 2 — Modo de entrada: cbreak, não raw

**Verificado automaticamente** por `python tela/teste_demo.py` (seção 7A e 7B) e
por `grep -c 'setraw' tela/demo.py` (retorna 0):

- Inspeção: `"setcbreak" in texto_mod` → PASSOU
- Inspeção: `"setraw" not in texto_mod` → PASSOU
- `grep -c 'setraw' tela/demo.py` → `0`
- Teste funcional: mock verifica que `tty.setcbreak` é chamado (não `setraw`) → PASSOU

Implementação: `_iniciar_sessao_tui` usa `tty.setcbreak(fd_stdin)`.

### Item 3 — Alternate screen buffer com cursor oculto e restaurado

**Verificado automaticamente** por `python tela/teste_demo.py` (seções 7A, 7B, 7C):

- Inspeção: `\x1b[?1049h`, `\x1b[?25l`, `\x1b[?25h`, `\x1b[?1049l` presentes → PASSOU
- Teste funcional de `_iniciar_sessao_tui`: conteúdo contém `\x1b[?1049h` e `\x1b[?25l` → PASSOU
- Teste funcional de `_encerrar_sessao_tui`: conteúdo contém `\x1b[?25h` e `\x1b[?1049l` → PASSOU

**Pendente de verificação manual de QA (Fase 6):** ao sair via Esc, o terminal
retorna ao conteúdo pré-sessão e o cursor está visível.

### Item 4 — Autowrap (DECAWM) desativado e restaurado

**Verificado automaticamente** por `python tela/teste_demo.py` (seções 7A, 7B, 7C, 7F):

- Inspeção: `\x1b[?7l` e `\x1b[?7h` presentes no código → PASSOU
- Teste funcional de `_iniciar_sessao_tui`: contém `\x1b[?7l` → PASSOU
- Teste funcional de `_encerrar_sessao_tui`: contém `\x1b[?7h` → PASSOU
- Teste de restauração após exceção: contém `\x1b[?7h` → PASSOU

**Pendente de verificação manual de QA (Fase 6):** nenhuma linha do quadro
provoca scroll automático ao atingir a última coluna do terminal.

### Item 5 — Desenho por posicionamento absoluto linha a linha

**Verificado automaticamente** por `python tela/teste_demo.py` (seção 7D):

- `\x1b[1;1H` presente no quadro → PASSOU
- `\x1b[2;1H` presente no quadro → PASSOU
- `"\n" not in conteudo_quadro` (sem newline para quebra de linha) → PASSOU

**Pendente de verificação manual de QA (Fase 6):** em sessão TTY real, o quadro
é desenhado alinhado à esquerda independentemente da posição anterior do cursor.

### Item 6 — Preenchimento de linha até a largura do terminal

**Verificado automaticamente** por `python tela/teste_demo.py` (seções 7A e 7D):

- Inspeção: `shutil.get_terminal_size` presente → PASSOU
- Teste funcional com largura=10: `"AB        "` presente no quadro → PASSOU
- Teste funcional com largura=10: `"CD        "` presente no quadro → PASSOU

**Pendente de verificação manual de QA (Fase 6):** após atualização de quadro,
nenhum conteúdo de quadro anterior permanece visível.

### Item 7 — Escrita atômica por quadro; limpeza de tela apenas na entrada

**Verificado automaticamente** por `python tela/teste_demo.py` (seção 7A e 7D)
e por `grep -c '\x1b\[2J' tela/demo.py` (retorna 1):

- `grep -c '\\x1b\[2J' tela/demo.py` → `1`
- Inspeção: `texto_mod.count("\\x1b[2J") == 1` → PASSOU (count=1)
- Teste funcional: exatamente uma chamada `write()` por quadro → PASSOU
- Teste funcional: exatamente uma chamada `flush()` por quadro → PASSOU
- Segundo quadro: também exatamente uma `write()` e uma `flush()` → PASSOU

**Pendente de verificação manual de QA (Fase 6):** em sessão TTY real, não há
flash de tela em branco entre quadros ao pressionar `b`.

### Item 8 — Synchronized output em cada atualização de quadro

**Verificado automaticamente** por `python tela/teste_demo.py` (seções 7A e 7D):

- Inspeção: `\x1b[?2026h` e `\x1b[?2026l` presentes no código → PASSOU
- Teste funcional: `conteudo_quadro.startswith("\x1b[?2026h")` → PASSOU
- Teste funcional: `conteudo_quadro.endswith("\x1b[?2026l")` → PASSOU

Implementação: as sequências estão em `_apresentar_quadro`, que é chamada dentro
do loop de redesenho e uma vez antes do loop para o quadro inicial.

### Item 9 — Ctrl+C escopado: mecanismo preparado para uso futuro, ignorado fora

**Verificado automaticamente** por `python tela/teste_demo.py` (seções 7A e 7E):

- Inspeção: `"captura_interrupcao_de_script" in texto_mod` → PASSOU
- Inspeção: `"except KeyboardInterrupt" in texto_mod` → PASSOU
- Teste funcional: `captura_interrupcao_de_script` suprime `KeyboardInterrupt` → PASSOU
- Teste funcional: não interfere em execução normal → PASSOU
- Teste funcional: não suprime outras exceções (`ValueError`) → PASSOU

Implementação: classe `captura_interrupcao_de_script` (context manager) definida
em `tela/demo.py`. Não está em uso em nenhum ponto da UI atual (nenhum fluxo de
execução de script existe ainda — correto e esperado conforme H-0022 item 9).
No loop principal de `main()`, `KeyboardInterrupt` é capturado por
`except KeyboardInterrupt: continue` (sessão permanece ativa).

### Item 10 — Restauração garantida do terminal em finally

**Verificado automaticamente** por `python tela/teste_demo.py` (seções 7A e 7F):

- Inspeção: `"finally:" in texto_mod` → PASSOU
- Teste de restauração por exceção: `tcsetattr` chamado após `RuntimeError` → PASSOU
- Teste de restauração por exceção: `\x1b[?25h` presente após exceção → PASSOU
- Teste de restauração por exceção: `\x1b[?1049l` presente após exceção → PASSOU
- Teste de restauração por exceção: `\x1b[?7h` presente após exceção → PASSOU

**Pendente de verificação manual de QA (Fase 6):** após encerramento normal, o
terminal está em estado idêntico ao anterior (sem alternate screen, autowrap e
cursor restaurados, sem modo cbreak).

### Item 11 — Comportamento não-TTY preservado sem alteração

**Verificado automaticamente** por `python tela/teste_demo.py` (seções 4, 7G) e
pelo comando `printf 'b\ns\n' | python tela/demo.py ; echo "EXIT: $?"`:

- `printf 'b\ns\n' | python tela/demo.py` → EXIT: 0 → PASSOU
- `printf 'b\n\x1b\n' | python tela/demo.py` → exit 0, saída idêntica → PASSOU
- Saída pipe sem `\x1b[?1049h`, `\x1b[?25l`, `\x1b[?7l`, `\x1b[?2026h` → PASSOU
- stderr vazio em modo pipe → PASSOU
- stdout bate com `renderizar_tela(...)` curva+reta → PASSOU (seção 4)

### Testes automatizados

`python tela/teste_demo.py` → código 0, **169/169 verificações passaram**.

## Resumo do estado dos critérios

| Item | Descrição resumida | Status |
|------|--------------------|--------|
| 1 | Ativação somente em TTY duplo | Verificado automaticamente |
| 2 | cbreak, não raw | Verificado automaticamente |
| 3 | Alternate screen + cursor | Verificado automaticamente (QA pendente para visual) |
| 4 | Autowrap desativado/restaurado | Verificado automaticamente (QA pendente para visual) |
| 5 | Posicionamento absoluto linha a linha | Verificado automaticamente (QA pendente para visual) |
| 6 | Preenchimento de linha até largura | Verificado automaticamente (QA pendente para visual) |
| 7 | Escrita atômica; \x1b[2J apenas uma vez | Verificado automaticamente |
| 8 | Synchronized output por quadro | Verificado automaticamente |
| 9 | captura_interrupcao_de_script + KI ignorado no loop | Verificado automaticamente |
| 10 | finally cobre restauração completa | Verificado automaticamente (QA pendente para visual) |
| 11 | Comportamento não-TTY preservado | Verificado automaticamente |

## Notas de implementação

- A `_ler_tecla_unica` foi removida: usava `tty.setraw` e não estava em uso
  no loop principal (apenas a `_ler_tecla_sessao` é usada na sessão TUI).
- O stash `pre-H-0022` preserva a implementação anterior para referência
  histórica sem descartá-la.
- Os contratos e a ADR-0016 estão marcados como pendentes de atualização
  em tarefa subsequente (conforme seção "Artefatos a atualizar" da ADR-0016);
  esses artefatos são fora do escopo do H-0022.
