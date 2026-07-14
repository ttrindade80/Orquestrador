# Relatório de QA pós-patch — H-0023 Handoff

## 1. Objetivo e escopo

Auditoria formal pós-patch do handoff
`docs/handoff/H-0023-redimensionamento-reativo-tui.md`, limitada a verificar se
os achados do relatório anterior foram resolvidos e se o patch não introduziu
regressões.

Escopo respeitado: não houve correção do handoff, implementação, alteração de
código ou testes, alteração de ADRs, contratos ou nomenclatura, stage, commit,
push ou alteração de histórico Git. Este relatório é o único arquivo criado por
esta etapa.

## 2. Autoridades

Lidas e usadas como autoridade:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/relatorios/RELATORIO_QA_ADR-0017.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `docs/handoff/H-0023-redimensionamento-reativo-tui.md`
- `docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md`

Lidos também como estado técnico diretamente relacionado:

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

## 3. Arquivos examinados

O handoff corrigido tem 1132 linhas e foi lido integralmente. O relatório
anterior de QA tem 289 linhas e foi inspecionado como arquivo novo não
rastreado. O código atual confirma a premissa técnica do handoff: ainda não há
`SIGWINCH`, `ioctl`, wakeup pipe nem redimensionamento reativo em `tela/demo.py`;
`renderizar_tela` já aceita largura e altura.

## 4. Comandos executados

```bash
git status --short
git log -1 --oneline
git diff --check
git diff --stat
git diff --name-only
git diff --cached --stat
git diff --cached --name-only
git diff --no-index /dev/null docs/handoff/H-0023-redimensionamento-reativo-tui.md
git diff --no-index /dev/null docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
wc -l docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n -C 5 'estado anterior|estado posterior|seção 2\.2|secao 2\.2|os\.pipe|_iniciar_sessao_tui|_instalar_handler_sigwinch|terminal pequeno|aviso mínimo|aviso minimo|"\!"' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n 'H23-QA-BLOQ-001|H23-QA-MED-001|H23-QA-MED-002|H23-QA-NOTA-001' docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
rg -n 'nonblock|bloqueante|pipe cheio|EAGAIN|EWOULDBLOCK|O_NONBLOCK|set_blocking|setblocking|fcntl' docs/handoff/H-0023-redimensionamento-reativo-tui.md docs/adr/ADR-0017-redimensionamento-reativo-tui.md docs/contratos/contrato_tela_json.md
rg -n 'RenderizadorErro|exceção|excecao|classe|aprovad|\[x\]|validação humana|validacao humana|pseudo-TTY|pty\.openpty|SIGWINCH|select\.select|os\.read\(r_wakeup|os\.write\(w_wakeup|os\.pipe\(\)' docs/handoff/H-0023-redimensionamento-reativo-tui.md
rg -n 'IMP-0024-redimensionamento-reativo-tui|RELATORIO_QA_POS_PATCH_H-0023_HANDOFF' docs/relatorios docs/handoff
```

`git diff --no-index` retornou código 1 nos dois arquivos novos, como esperado
para diferenças contra `/dev/null`.

## 5. Estado Git

```text
HEAD: de0f023 fix: corrige execução TTY em tela cheia
stage: vazio
git diff --check: sem saída
```

`git status --short` antes da criação deste relatório:

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
```

`git diff --stat` e `git diff --name-only` apontam somente alterações
rastreadas do ciclo documental da ADR-0017:

```text
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_tela_json.md
```

Não há diff staged. O patch do handoff não modificou `tela/`, `config/`,
`docs/adr/`, `docs/contratos/`, `docs/NOMENCLATURA.md` nem
`docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md`; o handoff e o relatório
anterior aparecem como arquivos não rastreados.

Após esta etapa, o arquivo produzido adicionalmente é:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md
```

## 6. Estado dos achados originais

### H23-QA-BLOQ-001

resultado: RESOLVIDO

evidência: o handoff agora distingue a seção 2.1 como estado anterior à
criação do H-0023 e a seção 2.2 como estado posterior. A seção 2.2 registra
`docs/handoff/H-0023-redimensionamento-reativo-tui.md` e
`docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md` como arquivos não rastreados
adicionais, preserva `HEAD de0f023`, stage vazio e declara explicitamente que
o worktree não está limpo. A condição de bloqueio da seção 24 compara a futura
implementação com o estado da seção 2.2.

impacto: o executor não fica mais bloqueado por contradição temporal no estado
Git comprovado.

### H23-QA-MED-001

resultado: RESOLVIDO

evidência: as seções 13.2 e 13.8 usam a mesma ordem: obter `fd`, obter
dimensões iniciais, criar `os.pipe()`, iniciar sessão TUI, instalar handler,
executar loop, restaurar handler, fechar descritores e restaurar terminal.
Não foi encontrada preservação da ordem antiga.

impacto: a sequência normativa deixou de concorrer internamente.

### H23-QA-MED-002

resultado: RESOLVIDO

evidência: a seção 17.2 removeu `"!"` como mensagem suficiente. O handoff
distingue mensagem completa (`terminal pequeno demais`), abreviação inequívoca
(`tela peq.`) e limite físico para largura menor que 9, quando a linha é
preenchida com espaços. Os casos `1x1`, `1xN`, `Nx1` e `5x2` permanecem dentro
da área; alturas ou larguras zero continuam inválidas pela seção 15.1.

impacto: o aviso mínimo deixa de normatizar um símbolo ambíguo como mensagem
semanticamente suficiente.

### H23-QA-NOTA-001

resultado: RESOLVIDO

evidência: a seção 19.2 agora pede inspeção de chamadas efetivas a
`_instalar_handler_sigwinch(...)`, excluindo a definição da função em nível de
módulo, e exige instalação somente no bloco TTY.

impacto: o teste não deve falhar apenas porque a função foi definida fora do
ramo TTY.

## 7. Ordem do wakeup pipe

A sequência corrigida garante que o pipe exista antes da instalação do handler:
`os.pipe()` aparece antes de `_instalar_handler_sigwinch`. A restauração do
handler aparece antes do fechamento de `r_wakeup` e `w_wakeup`; a restauração
do terminal fica por último. Esc e exceções atravessam o `finally`, que restaura
handler, fecha descritores e encerra a sessão TUI.

Há, porém, um novo achado sobre bloqueio do descritor de escrita do pipe; ver
`H0023-HANDOFF-POST-QA-001`.

## 8. Aviso mínimo

O handoff agora é implementável para dimensões positivas extremamente pequenas:
`_quadro_minimo_aviso` gera exatamente `altura` linhas e cada linha tem no
máximo `largura` caracteres antes do `\n`. Para `1x1`, `1xN`, `Nx1` e `5x2`,
a saída fica limitada ao retângulo disponível e não inventa encerramento,
tecla ou ação do usuário. Zero e negativos continuam par inválido, não
terminal pequeno válido.

## 9. Teste do handler

O critério corrigido permite definição em nível de módulo, examina chamadas
efetivas do instalador, exige instalação apenas no fluxo TTY e preserva o fluxo
não-TTY sem handler. A formulação deixou de depender de contagem textual simples
do nome da função.

## 10. Ausência de regressões

Conforme quanto à autoridade, capacidade coesa, dimensões, redesenho,
apresentação, escopo de arquivos, testes, pseudo-TTY e relatório de
implementação, com duas exceções registradas em novos achados.

O handoff continua limitado ao H-0023: não introduz navegação nova, mudança de
schema, nova taxonomia, refatoração ampla, mudança de composição declarativa ou
capacidade futura alheia ao resize. Preserva ADR-0017, ADR-0016 e ADR-0013, e
não usa relatório ou código como autoridade normativa superior às ADRs e
contratos ativos.

## 11. Suficiência dos arquivos permitidos

A lista permanece suficiente e mínima:

```text
tela/demo.py
tela/teste_demo.py
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
```

`tela/renderizador.py` não precisa ser alterado porque já aceita `largura` e
`altura`; `tela/teste_renderizador.py` pode permanecer somente leitura. Não há
módulo novo necessário. `IMP-0024-redimensionamento-reativo-tui.md` não colide
com arquivo real existente.

## 12. Auditoria dos testes

O handoff mantém testes concretos para precedência do `ioctl`, fallback
ambiental, fallback inicial, últimas dimensões válidas, sinal e wakeup pipe,
instalação somente em TTY, não-TTY preservado, restauração do handler,
fechamento de descritores, resize inválido sem redraw, redução, ampliação,
quadro mínimo, recuperação automática, ausência de resíduos, scroll e linha
adicional, preservações do H-0022 e regressões anteriores.

Lacuna: os testes não exigem pipe não bloqueante nem cenário de pipe cheio; ver
`H0023-HANDOFF-POST-QA-001`.

## 13. Auditoria do pseudo-TTY

A seção 20 cobre `pty.openpty()`, dimensão inicial via `TIOCSWINSZ`, alteração
real de winsize, envio de `SIGWINCH`, confirmação por captura de saída, Esc,
código de saída 0 e limpeza. O procedimento reconhece que pseudo-TTY não
substitui validação visual humana.

## 14. Auditoria da validação manual

A validação humana permanece separada e obrigatória nas seções 21 e 22.3,
cobrindo redução, ampliação, resize rápido, resíduos, scroll, linhas novas,
flicker, aviso mínimo, recuperação, echo, navegação e restauração.

Regressão: a seção 21.2 usa caixas `[x]`, o que registra visualmente os itens
como já aprovados antes da implementação e da validação humana. Ver
`H0023-HANDOFF-POST-QA-002`.

## 15. Auditoria do relatório de implementação

O relatório esperado continua sendo:

```text
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
```

O conteúdo exigido é suficiente: arquivos alterados, funções, wakeup pipe,
`ioctl`, validação/fallback, integração do loop, handler anterior, resize
válido e inválido, quadro mínimo, testes, pseudo-TTY, validação humana, estado
Git e limitações. O handoff não autoaprova a implementação.

## 16. Novos achados

### H0023-HANDOFF-POST-QA-001

severidade: alto

evidência: a seção 13.3 instrui o handler a executar
`os.write(w_wakeup, b'\x00')` e silenciar `OSError`, mas nenhuma ocorrência no
handoff especifica `O_NONBLOCK`, `os.set_blocking(False)`, `EAGAIN`,
`EWOULDBLOCK` ou tratamento equivalente de pipe cheio. A busca direcionada por
termos de não bloqueio e pipe cheio não encontrou especificação.

impacto: um `os.write` em pipe bloqueante dentro do handler pode bloquear se o
pipe encher durante sequência rápida de `SIGWINCH`. Isso contraria a exigência
de ausência de deadlock/vazamento e enfraquece a premissa de handler mínimo. É
corrigível no handoff atual, sem nova ADR.

### H0023-HANDOFF-POST-QA-002

severidade: baixo

evidência: a seção 21.2 lista os critérios de validação humana com caixas já
marcadas `[x]`, embora o próprio handoff diga que a validação humana deve ser
registrada no `IMP-0024` e a seção 22.3 use caixas pendentes `[ ]`.

impacto: o texto pode ser lido como aprovação humana prévia de itens que ainda
devem ser executados após implementação. A correção é documental: trocar os
marcadores por critérios pendentes ou lista sem marcação de conclusão.

## 17. Limitações

Não executei a suíte de testes nem validação manual em TTY real, pois a etapa é
QA documental do handoff pós-patch. Código, testes e relatórios históricos foram
usados como evidência, não como autoridade superior às ADRs e contratos ativos.

## 18. Classificação final

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: os quatro achados originais foram resolvidos, mas restam dois
defeitos corrigíveis no próprio handoff: falta de especificação de pipe não
bloqueante/tratamento de pipe cheio no handler e marcação de validação humana
como já concluída.

## 19. Próxima categoria permitida

```text
PATCH_HANDOFF
```

Não gerar prompt seguinte.
