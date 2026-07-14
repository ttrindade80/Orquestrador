# Relatório de QA pós-patch 2 — H-0023 Handoff

## 1. Objetivo e escopo

Auditoria formal do handoff `docs/handoff/H-0023-redimensionamento-reativo-tui.md`
após o segundo patch, limitada a verificar os achados
`H0023-HANDOFF-POST-QA-001` e `H0023-HANDOFF-POST-QA-002`, a ausência de
regressões e a implementabilidade documental do H-0023.

Não houve correção do handoff, implementação, alteração de código ou testes,
alteração de ADRs, contratos ou nomenclatura, stage, commit, push ou alteração
de histórico Git. Este relatório é o único arquivo criado nesta etapa.

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

Lidos também como evidência técnica:

- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`

Consultados para preservações:

- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`
- `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`

Código, testes e relatórios históricos foram usados como evidência, não como
autoridade superior às ADRs e contratos ativos.

## 3. Arquivos examinados

O handoff sob QA tem 1216 linhas. O relatório de QA original tem 289 linhas. O
relatório pós-patch anterior tem 321 linhas. O código atual confirma a premissa
técnica: `tela/demo.py` ainda não possui `SIGWINCH`, `ioctl`, wakeup pipe ou
redimensionamento reativo; `tela/renderizador.py` já aceita `largura` e `altura`
e pode lançar `RenderizadorErro`.

## 4. Comandos executados

```bash
test -e docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md
git status --short
git log -1 --oneline
git diff --check
git diff --stat
git diff --name-only
git diff --cached --stat
git diff --cached --name-only
git diff --no-index /dev/null docs/handoff/H-0023-redimensionamento-reativo-tui.md
git diff --no-index /dev/null docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md
wc -l docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 6 'os\.set_blocking|O_NONBLOCK|BlockingIOError|EAGAIN|EWOULDBLOCK|pipe cheio|não bloqueante|nao bloqueante|os\.write|os\.read|resize_pendente|select\.select' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 5 '\[x\]|\[ \]|validação humana|validacao humana|TTY real|nenhum item|pseudo-TTY' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 5 'estado anterior|estado posterior|os\.pipe|_iniciar_sessao_tui|_instalar_handler_sigwinch|terminal pequeno|"\!"' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 3 'handler_anterior|atributos_originais|os\.close|finally|RenderizadorErro|ARCHITECTURE_REVIEW_REQUIRED|BLOCKED_EVIDENCE|IMP-0024|RELATORIO_QA_POS_PATCH_2|\[x\]' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 4 'redimensionamento|SIGWINCH|TIOCGWINSZ|últimas dimensões|ultimas dimensoes|terminal pequeno|80, 24|80,24' docs/contratos/contrato_tela_json.md docs/contratos/contrato_composicao_corpo.md docs/NOMENCLATURA.md
rg -n -C 4 'alternate screen|cbreak|autowrap|synchronized|Ctrl\+C|SIGWINCH|redimensionamento|tty|setraw|setcbreak|\x1b\[2J' docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md docs/contratos/contrato_console.md docs/contratos/contrato_barra_de_menus.md docs/contratos/contrato_lancador.md docs/contratos/contrato_estilo.md
rg -n 'RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF|IMP-0024-redimensionamento-reativo-tui|RELATORIO_QA_POS_PATCH_H-0023_HANDOFF' docs/relatorios docs/handoff
```

`git diff --no-index` retornou código 1 nos arquivos novos, como esperado para
diferenças contra `/dev/null`.

## 5. Estado Git

Antes da criação deste relatório:

```text
HEAD: de0f023 fix: corrige execução TTY em tela cheia
stage: vazio
git diff --check: sem saída
```

`git status --short`:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
?? docs/handoff/H-0023-redimensionamento-reativo-tui.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md
```

`git diff --stat`:

```text
 scripts/docs/NOMENCLATURA.md                       |  48 ++++++-
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 .../docs/contratos/contrato_composicao_corpo.md    |  56 ++++++--
 scripts/docs/contratos/contrato_tela_json.md       | 156 +++++++++++++++++++--
 4 files changed, 240 insertions(+), 21 deletions(-)
```

`git diff --name-only`:

```text
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_tela_json.md
```

`git diff --cached --stat` e `git diff --cached --name-only`: sem saída. O
stage está vazio. Após esta etapa, o arquivo produzido pelo QA atual é:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md
```

## 6. Resultado de H0023-HANDOFF-POST-QA-001

ID original: `H0023-HANDOFF-POST-QA-001`

resultado: `RESOLVIDO`

evidência: as seções 13.2, 13.3, 13.6, 13.8 e 19.2 do handoff agora exigem
`os.set_blocking(r_wakeup, False)` e `os.set_blocking(w_wakeup, False)` logo
após `os.pipe()` e antes de `_instalar_handler_sigwinch`; registram
`O_NONBLOCK`, `BlockingIOError`, `EAGAIN`/`EWOULDBLOCK`, pipe cheio sem bloqueio,
coalescência, flag definida antes de `os.write`, drenagem não bloqueante até
`BlockingIOError` e testes determinísticos sem encher pipe real indefinidamente.

impacto: a política de pipe não bloqueante e pipe cheio deixou de ser lacuna do
handoff. Resta um novo defeito de restauração em falha parcial, registrado como
achado separado.

## 7. Resultado de H0023-HANDOFF-POST-QA-002

ID original: `H0023-HANDOFF-POST-QA-002`

resultado: `RESOLVIDO`

evidência: a busca por `\[x\]` não encontrou caixa marcada no handoff. A seção
21.2 declara explicitamente: "Nenhum item abaixo foi validado"; usa caixas
`[ ]`; afirma que a aprovação humana só será registrada no `IMP-0024` após TTY
real; e distingue validação humana de testes automatizados e pseudo-TTY. As
seções 20.2 e 22.3 mantêm pseudo-TTY como não substituto universal e validação
humana obrigatória.

impacto: não há mais autoaprovação documental da validação humana.

## 8. Verificação dos quatro achados anteriores

`H23-QA-BLOQ-001`: não reintroduzido. A seção 2.1 distingue estado anterior à
criação do H-0023 e a seção 2.2 registra o handoff e o relatório de QA como
arquivos não rastreados adicionais.

`H23-QA-MED-001`: não reintroduzido quanto à ordem principal. As seções 13.2 e
13.8 usam a ordem `fd` → dimensões iniciais → `os.pipe()` → `os.set_blocking`
→ `_iniciar_sessao_tui` → `_instalar_handler_sigwinch`.

`H23-QA-MED-002`: não reintroduzido. `"!"` não aparece como mensagem normativa
suficiente; para largura menor que 9 o handoff assume limite físico e preenche
com espaços.

`H23-QA-NOTA-001`: não reintroduzido. O teste pedido na seção 19.2 fala em
chamadas efetivas a `_instalar_handler_sigwinch(...)`, excluindo a definição da
função.

## 9. Análise do pipe não bloqueante

Conforme. O handoff especifica `os.pipe()` antes da instalação do handler, ambos
os descritores não bloqueantes por `os.set_blocking(fd, False)`, compatibilidade
com POSIX via `O_NONBLOCK`, e nenhuma seção preserva o handler instalado antes
da configuração do pipe.

## 10. Análise do pipe cheio e coalescência

Conforme. O handler marca `resize_pendente[0] = True` antes de tentar
`os.write(w_wakeup, b'\x00')`, escreve somente um byte, captura `OSError`
incluindo `BlockingIOError`, não bloqueia, não encerra a aplicação, não limpa a
flag, não tenta drenar no handler e trata múltiplos `SIGWINCH` como
coalescência usando a dimensão mais recente disponível.

## 11. Análise da drenagem

Conforme. O fluxo normal usa `select.select([fd, r_wakeup], [], [])`; quando
`r_wakeup` está pronto, faz `os.read(r_wakeup, 64)` em laço, encerra em
`BlockingIOError`, `b""` ou `OSError`, não depende de número fixo de bytes, não
aguarda indefinidamente e consulta dimensões depois da notificação.

## 12. Análise da integração com a espera do loop

Conforme. O wakeup pipe participa da espera real da sessão por meio de
`select.select([fd, r_wakeup], [], [])`. O handoff distingue stdin de
`r_wakeup`, processa resize antes da tecla quando ambos estão prontos, chama
`_ler_tecla_sessao(fd=fd)` apenas para teclado, preserva a leitura de sequências
de escape no descritor de stdin e evita confundir bytes do pipe com entrada do
usuário.

## 13. Análise da restauração

Parcialmente conforme.

Conforme para saída por Esc e exceções dentro do loop: o `finally` restaura o
handler antes de fechar descritores, fecha `r_wakeup` e `w_wakeup`, e chama
`_encerrar_sessao_tui`. Isso impede nova escrita pelo handler próprio após o
fechamento do descritor de escrita.

Não conforme para falha parcial antes de entrar no `try/finally` principal. Na
estrutura completa da seção 13.8, `os.pipe()`, `os.set_blocking(...)`,
`_iniciar_sessao_tui(fd)` e `_instalar_handler_sigwinch(...)` ocorrem antes do
`try:` que contém o `finally`. Se falhar a segunda chamada de `os.set_blocking`,
`_iniciar_sessao_tui` ou `_instalar_handler_sigwinch`, o handoff não define uma
limpeza implementável dos descritores já abertos, nem a restauração do terminal
caso a sessão tenha sido parcialmente iniciada.

## 14. Auditoria dos testes

Conforme quanto aos achados originais: há testes previstos para descritores não
bloqueantes, escrita normal, pipe cheio por mock de `os.write`, captura de
`BlockingIOError`, coalescência, flag preservada, drenagem completa, término sem
bloqueio, integração com a espera do loop, atualização após drenagem, restauração
após Esc, restauração após exceção e ausência de travamento. O handoff proíbe
encher um pipe real indefinidamente.

Lacuna vinculada ao novo achado: os testes não exigem explicitamente falha
parcial durante criação/configuração/início/instalação com limpeza dos recursos
já obtidos.

## 15. Auditoria do pseudo-TTY

Conforme. A seção 20 cobre `pty.openpty()`, dimensão inicial via `TIOCSWINSZ`,
alteração real de winsize, envio de `SIGWINCH`, processo ainda ativo, captura
de saída, Esc, código de saída 0 e restauração. O procedimento reconhece que
pseudo-TTY não substitui validação visual humana.

## 16. Auditoria da validação humana

Conforme. Nenhuma caixa `[x]` permanece. A validação humana continua obrigatória
em TTY real, separada de testes automatizados e pseudo-TTY. O implementador deve
registrar pendência, execução e resultado no relatório de implementação, sem
autoaprovação.

## 17. Verificação de ausência de regressões

O handoff preserva ADR-0017, ADR-0016 e ADR-0013; não introduz decisão
arquitetural nova; não converte relatório ou código em autoridade normativa; e
permanece limitado ao H-0023. Não foram encontradas nova navegação, alteração de
schema, nova taxonomia, refatoração ampla, mudança de composição declarativa,
threads, event loop externo, biblioteca de TUI ou funcionalidade futura alheia
ao resize.

As fontes de dimensão estão coerentes:

```text
inicialização: ioctl(TIOCGWINSZ) → LINES/COLUMNS → (80, 24)
após SIGWINCH: ioctl(TIOCGWINSZ) → LINES/COLUMNS → últimas dimensões válidas
```

O redesenho exige recálculo integral, redução e ampliação, preservação de
`corpo.arranjo`, `tiling`, chips e presença declarativa, escrita atômica,
synchronized output e ausência de `\x1b[2J` a cada resize. Terminal pequeno é
tratado como quadro seguro limitado à área, sem encerramento e com recuperação
automática.

## 18. Suficiência dos arquivos permitidos

Parcialmente conforme.

A implementação normal do wakeup pipe, loop, dimensões, quadro mínimo e testes é
suficiente em:

```text
tela/demo.py
tela/teste_demo.py
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
```

Nenhum outro arquivo de código parece indispensável. Porém o handoff precisa
detalhar, ainda dentro desses mesmos arquivos, a limpeza em falhas parciais
antes do `try/finally` principal.

## 19. Novos achados

### H0023-HANDOFF-POST2-QA-001

severidade: alto

evidência: a seção 13.8 cria `r_wakeup, w_wakeup = os.pipe()`, chama
`os.set_blocking(...)`, inicia a sessão e instala o handler antes do `try:` cujo
`finally` restaura handler, fecha pipe e restaura terminal. A seção 18 garante
restauração após exceção no loop, mas não define limpeza para falha parcial
durante criação/configuração dos recursos. O prompt de QA exige confirmar que
falha parcial durante criação/configuração também possui limpeza definida.

impacto: se `os.set_blocking(w_wakeup, False)`, `_iniciar_sessao_tui` ou
`_instalar_handler_sigwinch` falhar, descritores podem vazar; se a sessão TUI
tiver sido parcialmente iniciada, a restauração do terminal pode não estar
garantida. O defeito é corrigível no handoff atual sem nova ADR, mas impede
aprovação do handoff como implementável.

## 20. Limitações

Não executei a suíte de testes nem validação humana em TTY real, pois esta etapa
é QA documental do handoff. Não alterei código, testes, ADRs, contratos,
nomenclatura ou relatórios anteriores.

## 21. Classificação final

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: os dois achados originais do relatório pós-patch anterior estão
resolvidos e os quatro achados anteriores não foram reintroduzidos, mas resta
defeito corrigível no próprio handoff sobre limpeza/restauração em falha parcial
antes do `try/finally` principal.

## 22. Próxima categoria permitida

```text
PATCH_HANDOFF
```

Não gerar prompt seguinte.
