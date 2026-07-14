# Relatorio de QA pos-patch 4 — H-0023 Handoff

## 1. Objetivo e escopo

Auditoria formal do handoff `docs/handoff/H-0023-redimensionamento-reativo-tui.md`
apos o quarto patch, limitada a verificar o achado
`H0023-HANDOFF-POST3-QA-001`, a ausencia de regressões e a implementabilidade
documental do H-0023.

Nao houve correcao do handoff, implementacao, alteracao de codigo ou testes,
alteracao de ADRs, contratos ou nomenclatura, stage, commit, push ou alteracao
de historico Git. Este relatorio e o unico arquivo criado nesta etapa.

Antes da criacao deste relatorio, foi confirmado que o caminho
`docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0023_HANDOFF.md` nao existia.

## 2. Autoridades

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
- `docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md`

Consultados para preservacoes:

- `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`

Codigo, testes e relatorios historicos foram usados como evidencia, nao como
autoridade superior as ADRs e contratos ativos.

## 3. Arquivos examinados

Evidencia tecnica lida:

- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`

O handoff sob QA tem 1680 linhas. O codigo atual confirma o estado
pre-implementacao: `tela/demo.py` ainda nao contem resize reativo, wakeup pipe,
`SIGWINCH` ou `ioctl`; a alteracao segue descrita apenas no handoff.

## 4. Comandos executados

```bash
test ! -e docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0023_HANDOFF.md
git status --short
git log -1 --oneline
git diff --check
git diff --stat
git diff --name-only
git diff --cached --stat
git diff --cached --name-only
git diff --no-index /dev/null docs/handoff/H-0023-redimensionamento-reativo-tui.md
git diff --no-index /dev/null docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md
wc -l docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 8 '_restaurar_efeitos_visuais_tui|rollback visual|restauracao visual|alternate screen|cursor oculto|autowrap|1049l|25h|7h|synchronized|termios|tcsetattr|_iniciar_sessao_tui|_encerrar_sessao_tui|write|flush|excecao original|erro secundario' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 5 'H0023-HANDOFF-POST3-QA-001|emissao parcial|falha.*rollback|sessao_iniciada|atributos_originais|finally|raise|return' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 4 'os\.set_blocking|BlockingIOError|select\.select|\[x\]|\[ \]|terminal pequeno|"\!"|\\x1b\[2J' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n 'H23-QA-BLOQ-001|H23-QA-MED-001|H23-QA-MED-002|H23-QA-NOTA-001|H0023-HANDOFF-POST-QA-001|H0023-HANDOFF-POST-QA-002|H0023-HANDOFF-POST2-QA-001|H0023-HANDOFF-POST3-QA-001' docs/handoff/H-0023-redimensionamento-reativo-tui.md docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md
rg -n -C 4 'redimensionamento|SIGWINCH|TIOCGWINSZ|ultimas dimensoes|terminal pequeno|80, 24|cbreak|alternate screen|autowrap|synchronized|\\x1b\[2J' docs/contratos/contrato_tela_json.md docs/contratos/contrato_composicao_corpo.md docs/NOMENCLATURA.md
rg -n 'tty\.setraw|tty\.setcbreak|\?1049h|\?1049l|\?25l|\?25h|\?7l|\?7h|\?2026h|\?2026l|\x1b\[2J|KeyboardInterrupt|isatty|finally' tela/demo.py tela/teste_demo.py
```

`git diff --no-index` retornou codigo 1 nos arquivos novos inspecionados, como
esperado para diff contra `/dev/null`.

## 5. Estado Git

Estado antes da criacao deste relatorio:

```text
HEAD: de0f023 fix: corrige execucao TTY em tela cheia
stage: vazio
git diff --check: sem saida
```

Arquivos rastreados modificados previamente:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
```

Arquivos nao rastreados previamente:

```text
?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
?? docs/handoff/H-0023-redimensionamento-reativo-tui.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md
```

`git diff --stat`:

```text
 scripts/docs/NOMENCLATURA.md                    |  48 ++++++-
 scripts/docs/adr/INDICE_ADR.md                  |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md |  56 ++++++--
 scripts/docs/contratos/contrato_tela_json.md    | 156 +++++++++++++++++++--
 4 files changed, 240 insertions(+), 21 deletions(-)
```

`git diff --name-only` aponta somente os quatro arquivos rastreados acima.
`git diff --cached --stat` e `git diff --cached --name-only` nao produziram
saida. O handoff, os relatorios anteriores e este relatorio permanecem como
arquivos nao rastreados. O unico arquivo criado por esta etapa e:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0023_HANDOFF.md
```

## 6. Resultado de H0023-HANDOFF-POST3-QA-001

ID original: `H0023-HANDOFF-POST3-QA-001`

resultado: `RESOLVIDO`

evidencia: a secao 13.10.3 agora reconhece emissao potencialmente parcial da
sequencia de entrada, proibe presumir que falha de `write` ou `flush` signifique
ausencia de saida, introduz a auxiliar local `_restaurar_efeitos_visuais_tui`,
usa essa auxiliar no rollback interno de `_iniciar_sessao_tui` e em
`_encerrar_sessao_tui`, define a sequencia `\x1b[?7h\x1b[?25h\x1b[?1049l`,
exige restauracao visual antes de `termios` no rollback interno, preserva a
excecao original com `raise` e cobre os pontos de falha em tabela e testes.

impacto: uma falha parcial de inicializacao nao fica mais documentalmente capaz
de deixar alternate screen ativo, cursor oculto ou autowrap desativado sem
tentativa defensiva de restauracao. O chamador nao precisa encerrar sessao
inexistente, e o cleanup externo continua cuidando apenas dos recursos que
adquiriu.

## 7. Politica unica de rollback

Conforme. O handoff determina que `_iniciar_sessao_tui` e responsavel pelo
rollback interno quando falha antes de retornar. O chamador so marca
`sessao_iniciada = True` apos retorno bem-sucedido e, em falha, nao chama
`_encerrar_sessao_tui` com estado invalido.

Nao foram encontradas duas politicas concorrentes: o rollback de inicializacao
fica dentro de `_iniciar_sessao_tui`; o encerramento normal fica em
`_encerrar_sessao_tui`. Ambas compartilham a mesma auxiliar visual.

## 8. Auxiliar visual

Conforme. `_restaurar_efeitos_visuais_tui` permanece local a `tela/demo.py`,
nao cria modulo novo nem arquitetura nova, e usa somente sequencias ja
autorizadas pela ADR-0016:

```text
\x1b[?7h    autowrap ativado
\x1b[?25h   cursor visivel
\x1b[?1049l saida do alternate screen
```

A auxiliar nao introduz `\x1b[2J`, nao emite posicionamento ou limpeza
desnecessarios, separa `write` e `flush` em blocos independentes, e e
reutilizada tanto pelo rollback interno quanto pelo encerramento normal.

## 9. Sequencias ANSI

Conforme. A ordem `autowrap -> cursor -> alternate screen` e definida,
coerente e defensiva para rollback. Nao ha sequencia de entrada durante
rollback, e `\x1b[2J` aparece apenas na entrada da sessao e em verificacoes de
ausencia no rollback/redesenho.

A ADR-0016 usa synchronized output por quadro, com `\x1b[?2026h` antes e
`\x1b[?2026l` depois de cada atualizacao. O handoff preserva essa politica em
`_apresentar_quadro`; a politica de entrada da sessao nao deixa synchronized
output aberto que precise ser finalizado pelo rollback de inicializacao.

## 10. Emissao parcial

Conforme. O handoff cobre falha antes de qualquer emissao visual, apos entrada
no alternate screen, apos ocultar cursor, apos desativar autowrap, apos limpeza
ou posicionamento, durante `flush` e apos emissao parcial nao mensuravel. Em
todos esses casos, exige tentativa de restauracao visual defensiva completa e
restauracao de `termios` quando atributos originais ja existem.

## 11. Ordem do rollback

Conforme. A ordem unica definida e:

```text
falha primaria de inicializacao
-> tentar restauracao visual
-> tentar flush da restauracao
-> tentar restauracao de termios
-> propagar a excecao primaria
```

Falha visual nao impede `tcsetattr`, falha de `tcsetattr` nao substitui a
excecao primaria, nao ha `return` em `except` ou `finally`, e a funcao nao
transforma falha de inicializacao em sucesso.

## 12. Falhas da propria restauracao

Conforme. O handoff distingue rollback durante excecao primaria de encerramento
normal sem excecao primaria. Durante rollback, `write` da restauracao visual,
`flush` da restauracao, ou ambos, sao erros secundarios silenciados pela
auxiliar, e a tentativa de `termios.tcsetattr` ainda ocorre.

No encerramento normal, a politica de silenciar erros de restauracao visual nao
e regressao: a implementacao atual ja usa blocos `try/except` para restauracao
de terminal, e a ADR-0016 exige restauracao garantida em `finally`, sem
determinar propagacao de falhas secundarias de cleanup.

## 13. Termios

Conforme. `termios.tcgetattr` ocorre antes de `tty.setcbreak`; `tty.setcbreak`
continua sendo a politica, preservando `ISIG` e `OPOST` conforme ADR-0016.
Atributos originais sao restaurados quando disponiveis. Falha em `tcgetattr` ou
`setcbreak`, antes de emissao visual, propaga diretamente sem tentar restaurar
estado inexistente. Falha de `setcbreak` nao permite ao chamador marcar sessao
como iniciada. As responsabilidades visual e `termios` ficam separadas.

## 14. Cleanup externo

Conforme. Quando `_iniciar_sessao_tui` falha, `sessao_iniciada` permanece
`False`; `_encerrar_sessao_tui` nao e chamada com `None`; pipe ja criado e
fechado pelas sentinelas; handler ainda nao instalado nao e restaurado; a
excecao primaria atravessa o `finally`; e nao ha restauracao visual duplicada
pelo chamador.

Quando a inicializacao termina com sucesso, o encerramento normal continua
responsavel pela restauracao. A auxiliar visual e chamada no caminho apropriado,
sem duas sequencias divergentes de saida do alternate screen.

## 15. Auditoria dos testes

Conforme. O handoff exige testes deterministas com mocks para falha de
`tcgetattr`, falha de `setcbreak`, falha de `write` antes da saida visual,
falha depois de emissao parcial, falha de `flush`, tentativa de restauracao
visual, falha do `write` de rollback, falha do `flush` de rollback, falha de
`tcsetattr`, falha visual seguida de tentativa de `termios`, preservacao da
excecao primaria, ausencia de chamada invalida a `_encerrar_sessao_tui`,
fechamento de recursos externos, igualdade da politica visual usada no rollback
e no encerramento normal, ausencia de `\x1b[2J` no rollback e terminal real nao
modificado durante testes automatizados.

## 16. Achados anteriores

Nao foram reintroduzidos:

- `H23-QA-BLOQ-001`: estado Git anterior e posterior continuam distinguidos.
- `H23-QA-MED-001`: ha uma unica ordem de aquisicao, com aquisicao dentro da
  regiao protegida.
- `H23-QA-MED-002`: `"!"` nao e mensagem normativa de terminal pequeno.
- `H23-QA-NOTA-001`: teste do handler se baseia em chamadas efetivas.
- `H0023-HANDOFF-POST-QA-001`: pipe nao bloqueante, `BlockingIOError`, pipe
  cheio, coalescencia, drenagem nao bloqueante e `select.select` estao
  especificados.
- `H0023-HANDOFF-POST-QA-002`: validacao humana permanece pendente, sem `[x]`.
- `H0023-HANDOFF-POST2-QA-001`: aquisicao e cleanup parcial estao sob
  `try/finally`, com sentinelas e fechamento condicional.

Tambem permanecem preservados: handler restaurado antes do fechamento do pipe,
pipe nao bloqueante, quadro minimo sem `"!"`, validacao humana pendente e
estado Git descrito como worktree nao limpo.

## 17. Ausencia de regressoes

Conforme. O handoff permanece limitado a H-0023 — redimensionamento reativo da
TUI. Nao introduz modulo novo, biblioteca nova, thread, event loop externo,
mudanca de schema, mudanca de composicao, nova navegacao ou refatoracao ampla
alheia ao resize.

As politicas da sessao permanecem: sessao apenas com stdin/stdout TTY, `cbreak`
e nao `raw`, `ISIG` e `OPOST`, alternate screen, cursor oculto durante sessao,
autowrap desativado durante sessao, synchronized output, escrita atomica,
`\x1b[2J` somente na entrada, Esc, Ctrl+C escopado, ausencia de echo,
restauracao em saida/excecoes e fluxo nao-TTY inalterado.

As politicas de redimensionamento permanecem: `SIGWINCH`, wakeup pipe, handler
minimo, consulta por `ioctl`, fallback por `LINES`/`COLUMNS`, fallback inicial
`(80, 24)`, ultimas dimensoes validas, nao redesenho sem novo par, reducao e
ampliacao, quadro minimo, recuperacao automatica e ausencia de residuos, scroll
e linha adicional.

## 18. Suficiencia dos arquivos permitidos

Conforme. Continuam suficientes:

```text
tela/demo.py
tela/teste_demo.py
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
```

A auxiliar visual pode ser implementada em `tela/demo.py` e testada em
`tela/teste_demo.py`, sem modulo novo e sem alteracao de `tela/renderizador.py`.

## 19. Novos achados

Nenhum novo achado.

## 20. Limitacoes

Nao executei a suite de testes nem validacao humana em TTY real, pois esta
etapa e QA documental do handoff. Nao corrigi o handoff e nao alterei codigo,
testes, ADRs, contratos, nomenclatura ou relatorios anteriores.

## 21. Classificacao final

```text
H1_HANDOFF_APPROVED
```

Justificativa: `H0023-HANDOFF-POST3-QA-001` esta resolvido; achados anteriores
nao foram reintroduzidos; nao ha nova correcao necessaria; o rollback visual e
implementavel; rollback e encerramento normal nao possuem politicas visuais
concorrentes; excecoes primarias e erros de cleanup estao corretamente
tratados; os arquivos permitidos sao suficientes; e os testes/criterios sao
verificaveis.

## 22. Proxima categoria permitida

```text
H1_HANDOFF_APPROVED → IMPLEMENTAR
```
