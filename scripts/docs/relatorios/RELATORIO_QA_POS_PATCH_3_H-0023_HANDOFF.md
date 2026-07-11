# Relatório de QA pós-patch 3 — H-0023 Handoff

## 1. Objetivo e escopo

Auditoria formal do handoff `docs/handoff/H-0023-redimensionamento-reativo-tui.md`
após o terceiro patch, limitada a verificar o achado
`H0023-HANDOFF-POST2-QA-001`, a ausência de regressões e a implementabilidade
documental do H-0023.

Não houve correção do handoff, implementação, alteração de código ou testes,
alteração de ADRs, contratos ou nomenclatura, stage, commit, push ou alteração
de histórico Git. Este relatório é o único arquivo criado nesta etapa.

## 2. Autoridades e evidências lidas

Lidos integralmente e usados como autoridade:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `docs/handoff/H-0023-redimensionamento-reativo-tui.md`
- `docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md`

Lidos também como evidência técnica:

- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`

Consultados para preservações:

- `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`

Código, testes e relatórios históricos foram usados como evidência, não como
autoridade superior às ADRs e contratos ativos.

## 3. Integridade do arquivo-alvo

Antes da criação deste relatório, o caminho abaixo foi verificado como
inexistente:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md
```

O handoff sob QA tem 1485 linhas. O código 1 de `git diff --no-index` contra
`/dev/null` foi observado nos arquivos novos inspecionados, como esperado.

## 4. Estado Git

Comandos executados:

```bash
git status --short
git log -1 --oneline
git diff --check
git diff --stat
git diff --name-only
git diff --cached --stat
git diff --cached --name-only
git diff --no-index /dev/null docs/handoff/H-0023-redimensionamento-reativo-tui.md
git diff --no-index /dev/null docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md
wc -l docs/handoff/H-0023-redimensionamento-reativo-tui.md
```

Resultado observado antes deste relatório:

```text
HEAD: de0f023 fix: corrige execução TTY em tela cheia
stage: vazio
git diff --check: sem saída
```

Arquivos rastreados modificados:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
```

Arquivos não rastreados:

```text
?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
?? docs/handoff/H-0023-redimensionamento-reativo-tui.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md
```

`git diff --stat` aponta somente as quatro alterações rastreadas documentais
acima. `git diff --cached --stat` e `git diff --cached --name-only` não
produziram saída. Após esta etapa, o relatório criado é:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md
```

## 5. Buscas mínimas

Executadas buscas equivalentes às solicitadas para:

- falha parcial, rollback, cleanup, sentinelas, `r_wakeup`, `w_wakeup`,
  `os.pipe`, `os.set_blocking`, `_iniciar_sessao_tui`,
  `_encerrar_sessao_tui`, `_instalar_handler_sigwinch` e `finally`;
- `H0023-HANDOFF-POST2-QA-001`, preservação da exceção original, erro
  secundário, duplo close e idempotência;
- `os.set_blocking`, `BlockingIOError`, `EAGAIN`, `EWOULDBLOCK`,
  `select.select`, caixas de validação humana, terminal pequeno e `"!"`.

Também foram feitas buscas adicionais nos contratos, nomenclatura e H-0022 para
preservações de ADR-0016, ADR-0017 e composição declarativa.

## 6. Resultado do achado original

ID original: `H0023-HANDOFF-POST2-QA-001`

resultado: `PARCIALMENTE_RESOLVIDO`

evidência: as seções 13.2 e 13.8 agora inicializam sentinelas antes da
aquisição e colocam `os.pipe()`, as duas chamadas de `os.set_blocking(...)`,
`_iniciar_sessao_tui`, `_instalar_handler_sigwinch`, apresentação inicial e
loop sob a mesma região `try/finally`. As seções 13.10, 18.1 e 18.2 definem
cleanup condicional para descritores, sessão e handler, com restauração do
handler antes do fechamento de `w_wakeup`, fechamento independente dos dois
descritores, restauração da sessão apenas quando `sessao_iniciada = True` e
preservação da exceção original contra erros secundários de cleanup.

impacto: o defeito estrutural principal do relatório anterior foi corrigido:
não permanece a forma antiga em que a aquisição inteira precedia o `try`.
Contudo, a solução de rollback interno para falha parcial de
`_iniciar_sessao_tui` restaura apenas `termios`. Se `sys.stdout.write` emitir
parcialmente alternate screen, cursor oculto, autowrap desativado ou limpeza de
tela e depois `write`/`flush` falhar, o handoff não exige desfazer esses efeitos
visuais antes de propagar a exceção. Assim, a garantia de restauração da sessão
parcial ainda não está completa.

## 7. Verificações principais

### Região protegida

Conforme. O handoff exige sentinelas antes de qualquer operação que possa
falhar: `r_wakeup = None`, `w_wakeup = None`, `sessao_iniciada = False`,
`handler_instalado = False`, `handler_anterior = None` e
`atributos_originais = None`. A estrutura completa do ramo TTY entra em
`try/finally` antes de `os.pipe()` e mantém pipe, configuração não bloqueante,
sessão, handler, apresentação inicial e loop dentro da mesma política de
cleanup.

### Sentinelas e estados

Conforme. O handoff distingue descritores inexistentes/adquiridos, sessão não
iniciada/iniciada, handler não instalado/instalado, handler anterior ainda
desconhecido/obtido e atributos originais inexistentes/válidos. Os estados são
locais à sessão e não alteram JSON, modelo declarativo ou arquitetura externa.

### Falhas de pipe

Conforme. Se `os.pipe()` falhar, nenhum descritor é fechado. Se qualquer
`os.set_blocking` falhar após `os.pipe()` retornar, ambos os descritores são
fechados no `finally`; o loop não começa; sessão e handler inexistentes não são
restaurados; a exceção original propaga.

### Falha de `_iniciar_sessao_tui`

Parcialmente conforme. O handoff escolhe rollback interno: capturar atributos
antes de alterações, executar `tty.setcbreak`, envolver `write`/`flush` em
`try/except`, restaurar `termios.tcsetattr` quando `write`/`flush` falhar e
propagar a exceção original. O chamador não é obrigado a restaurar um valor que
nunca recebeu.

Não conforme para efeitos visuais: o rollback descrito não restaura alternate
screen, cursor oculto, autowrap desativado, limpeza/posição inicial ou qualquer
efeito visual parcialmente emitido antes da falha.

### Falha da instalação do handler

Conforme com ressalva documental. O handoff define que `handler_instalado` só
passa a `True` após `_instalar_handler_sigwinch` retornar; em exceção, permanece
`False` e o `finally` não restaura handler não instalado. Pipe e sessão já
adquiridos seguem para cleanup. A justificativa menciona atomicidade de
`signal.signal` em CPython, mas também define estados observáveis suficientes
para o código futuro saber quando o handler novo foi efetivamente instalado.

### Falha depois da instalação e antes do loop

Conforme. A apresentação inicial e o loop estão dentro do mesmo `try`; exceção
após instalação bem-sucedida restaura handler anterior antes de fechar
descritores, fecha o pipe, restaura a sessão e preserva a exceção original.

### Ordem do cleanup

Conforme. A ordem normativa é:

```text
restaurar handler próprio, quando instalado
→ fechar descritores adquiridos
→ restaurar sessão TUI iniciada
```

O handler é restaurado antes do fechamento de `w_wakeup`. Ambos os descritores
são fechados condicionalmente e de modo independente. Esc e exceções percorrem
a mesma política de cleanup.

### Preservação da exceção original

Conforme. O handoff especifica mecanismos implementáveis: `_restaurar_handler`
silencia erros próprios, cada `os.close` é protegido por `try/except OSError`,
`_encerrar_sessao_tui` já usa blocos independentes, e não há `return` em
`finally` no pseudocódigo. Erros secundários não substituem a exceção original.

### Idempotência

Conforme. Cada recurso é restaurado ou fechado no máximo uma vez pelo
`finally`, condicionado por sentinelas locais. Não há exigência de função nova
de gerenciamento amplo.

### Testes de falhas parciais

Parcialmente conforme. A seção 19.6 cobre falha de `os.pipe`, primeiro e
segundo `os.set_blocking`, falha de `_iniciar_sessao_tui`, rollback interno,
falha de `_instalar_handler_sigwinch`, exceções antes e durante o loop, saída
por Esc, falhas de cleanup, preservação da exceção original, ausência de duplo
close e ausência de restauração com estado inválido. A lacuna acompanha o
achado novo: os testes de rollback interno confirmam `termios.tcsetattr`, mas
não exigem restauração dos efeitos visuais parcialmente emitidos.

## 8. Verificação dos achados anteriores

Não foram reintroduzidos:

- `H23-QA-BLOQ-001`: o handoff distingue estado Git anterior e posterior.
- `H23-QA-MED-001`: a ordem do pipe, sessão e handler está harmonizada.
- `H23-QA-MED-002`: `"!"` não é usado como mensagem suficiente.
- `H23-QA-NOTA-001`: o teste do handler fala em chamadas efetivas.
- `H0023-HANDOFF-POST-QA-001`: pipe não bloqueante, pipe cheio, coalescência,
  drenagem não bloqueante e integração com `select.select` estão especificados.
- `H0023-HANDOFF-POST-QA-002`: validação humana permanece pendente com `[ ]`,
  sem `[x]`.

## 9. Auditoria integral de regressões

O handoff permanece limitado a H-0023 — redimensionamento reativo da TUI. Não
introduz threads, event loop externo, módulo novo, biblioteca de TUI, mudança
de schema, mudança de composição, nova navegação ou refatoração ampla alheia ao
resize.

Os arquivos futuros permitidos continuam suficientes para a implementação
normal:

```text
tela/demo.py
tela/teste_demo.py
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
```

O rollback interno de `_iniciar_sessao_tui` pode ser implementado em
`tela/demo.py` e testado em `tela/teste_demo.py`, mas precisa cobrir também os
efeitos visuais parciais indicados no achado novo.

Preservadas as regras funcionais de `SIGWINCH`, wakeup pipe, handler mínimo,
processamento fora do handler, `ioctl(TIOCGWINSZ)`, fallback por `LINES` e
`COLUMNS`, fallback inicial `(80, 24)`, últimas dimensões válidas, não redesenho
sem novo par válido, resize em redução e ampliação, quadro mínimo, recuperação
automática, ausência de resíduos/scroll/linha adicional, políticas da ADR-0016
e fluxo não-TTY.

## 10. Relatório de implementação esperado

Conforme. O futuro
`docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md` deve registrar
ordem de aquisição, sentinelas, rollback da inicialização TUI, falhas de pipe,
falhas de configuração não bloqueante, falha de instalação do handler, ordem do
cleanup, testes de falhas parciais, pseudo-TTY, validação humana pendente,
estado Git, limitações e ausência de autoaprovação.

## 11. Novos achados

### H0023-HANDOFF-POST3-QA-001

severidade: alto

evidência: a seção 13.10.3 propõe rollback interno de `_iniciar_sessao_tui`
somente com `termios.tcsetattr(...)` quando `sys.stdout.write` ou
`sys.stdout.flush` falham após `tty.setcbreak`. A sequência escrita por
`_iniciar_sessao_tui` contém alternate screen (`\x1b[?1049h`), cursor oculto
(`\x1b[?25l`), autowrap desativado (`\x1b[?7l`), limpeza (`\x1b[2J`) e
posicionamento inicial (`\x1b[H`). O handoff não exige emitir a sequência de
saída/restauração visual nem testar esse caso quando a escrita tiver sido
parcialmente aplicada antes da falha.

impacto: uma falha parcial de inicialização pode deixar o terminal em alternate
screen, com cursor oculto ou autowrap desativado, apesar de
`sessao_iniciada = False` impedir `_encerrar_sessao_tui` no `finally` externo.
Isso contraria as preservações da ADR-0016 e a verificação solicitada de
restauração dos efeitos visuais parcialmente emitidos.

## 12. Limitações

Não executei a suíte de testes nem validação humana em TTY real, pois esta
etapa é QA documental do handoff. Não alterei código, testes, ADRs, contratos,
nomenclatura ou relatórios anteriores.

## 13. Classificação final

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: o terceiro patch resolveu a região protegida e a maior parte da
política de falhas parciais, mas ainda precisa corrigir o rollback interno de
`_iniciar_sessao_tui` para cobrir efeitos visuais parcialmente aplicados, além
dos atributos `termios`.

## 14. Próxima categoria permitida

```text
PATCH_HANDOFF
```
