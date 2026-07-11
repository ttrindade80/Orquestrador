# Relatorio de QA — ADR-0017

## 1. Objetivo e escopo

Auditoria formal da ADR-0017 (`docs/adr/ADR-0017-redimensionamento-reativo-tui.md`) contra a decisao explicita do usuario, autoridades documentais ativas e estado Git recebido.

Escopo executado: somente QA da ADR e criacao deste relatorio.

Fora do escopo respeitado: nao houve correcao da ADR, aplicacao aos contratos, alteracao de documentacao normativa, criacao de handoff, alteracao de codigo, alteracao de testes, stage, commit, push ou alteracao de historico Git.

## 2. Arquivos e trechos examinados

- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`: arquivo integral, 446 linhas; diff integral como arquivo novo.
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`: arquivo integral.
- `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`: arquivo integral.
- `docs/adr/INDICE_ADR.md`: arquivo integral.
- `docs/contratos/contrato_tela_json.md`: arquivo integral.
- `docs/contratos/contrato_composicao_corpo.md`: arquivo integral.
- `docs/contratos/contrato_processo_desenvolvimento.md`: arquivo integral.
- `docs/NOMENCLATURA.md`: trechos relacionados a dimensoes do terminal, largura, altura, ocupacao vertical, TTY/redimensionamento, composicao e `tiling`.

## 3. Comandos executados

```bash
git status --short
git rev-parse HEAD
git diff -- docs/adr/ADR-0017-redimensionamento-reativo-tui.md
git diff --no-index -- /dev/null docs/adr/ADR-0017-redimensionamento-reativo-tui.md
nl -ba docs/adr/ADR-0017-redimensionamento-reativo-tui.md
nl -ba docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
nl -ba docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
nl -ba docs/adr/INDICE_ADR.md
nl -ba docs/contratos/contrato_tela_json.md
nl -ba docs/contratos/contrato_composicao_corpo.md
nl -ba docs/contratos/contrato_processo_desenvolvimento.md
rg -n "dimens|largura|altura|ocupacao|ocupação|TTY|tty|redimension|composi|tiling|janela|terminal" docs/NOMENCLATURA.md
sed -n '1,320p' docs/contratos/contrato_composicao_corpo.md
sed -n '321,640p' docs/contratos/contrato_composicao_corpo.md
sed -n '641,960p' docs/contratos/contrato_composicao_corpo.md
sed -n '120,180p' docs/NOMENCLATURA.md
sed -n '648,672p' docs/NOMENCLATURA.md
sed -n '935,1005p' docs/NOMENCLATURA.md
git diff --check
git diff --no-index /dev/null docs/adr/ADR-0017-redimensionamento-reativo-tui.md
wc -l docs/adr/ADR-0017-redimensionamento-reativo-tui.md
git log -1 --oneline
```

Observacao: `git diff --no-index /dev/null ...` retornou codigo 1 por detectar diferenca em arquivo novo; isso e resultado esperado, nao falha de QA.

## 4. Estado Git

- `HEAD`: `de0f023 fix: corrige execução TTY em tela cheia`
- `git rev-parse HEAD`: `de0f02324337170ddacda73a24e413840f349615`
- `git status --short` antes deste relatorio: somente `?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- Arquivos rastreados modificados antes do QA: nenhum.
- Arquivos nao rastreados antes do QA: `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`.
- Stage: vazio.
- `git diff --check`: sem saida; nenhuma falha de whitespace detectada nos diffs rastreados.
- Relatorio criado pelo QA: `docs/relatorios/RELATORIO_QA_ADR-0017.md`.

## 5. Comparacao item a item com a decisao do usuario

| Item da decisao | Resultado | Evidencia |
|---|---|---|
| Gerenciamento proprio; sem `ncurses`, `curses`, `textual`, `rich` ou biblioteca de TUI | Conforme | ADR-0017:75-79, 365, 376-377 |
| TTY ativa usa `SIGWINCH` como gatilho | Conforme | ADR-0017:81-90 |
| Sinal leva a nova consulta/redesenho com novo par valido sem fixar handler/loop | Conforme com nota | ADR-0017:87-90, 151-159, 165-174; ver ADR17-QA-002 |
| Fonte primaria `ioctl(fd, TIOCGWINSZ, ...)` | Conforme | ADR-0017:92-104 |
| Par coerente; nao misturar largura de uma fonte com altura de outra | Conforme | ADR-0017:103-104, 289-290, 411-412 |
| Par valido exige largura e altura presentes, inteiras e maiores que zero | Conforme | ADR-0017:106-116 |
| Inicializacao: `ioctl` -> `LINES`/`COLUMNS` -> `(80, 24)` | Conforme | ADR-0017:118-138 |
| `LINES`/`COLUMNS` aceitas somente juntas e nao prevalecem sobre `ioctl` valido | Conforme | ADR-0017:128-132 |
| Apos `SIGWINCH`: `ioctl` -> `LINES`/`COLUMNS` -> ultimas dimensoes validas | Conforme | ADR-0017:140-163 |
| Se fontes invalidas, conservar ultimas dimensoes, nao aplicar invalido, nao redesenhar como mudanca | Conforme com nota | ADR-0017:154-159; ver ADR17-QA-002 |
| Fallback `(80, 24)` nao substitui dimensoes validas ja estabelecidas | Conforme | ADR-0017:161-163, 296-297 |
| Novo par valido atualiza dimensoes, recalcula tela/regioes/paginacao/distribuicao e redesenha reducao/ampliacao | Conforme | ADR-0017:165-196 |
| Redimensionamento nao altera `corpo.arranjo`, `tiling`, chips ou composicao declarada | Conforme | ADR-0017:176-184, 298-299, 418-419 |
| Resultado visual sem residuos, scroll, linhas fora da altura, dimensoes antigas ou recorte superficial | Conforme | ADR-0017:190-196, 416-417 |
| Terminal pequeno demais: nao encerra, nao quadro antigo, nao desenha alem; exibe aviso minimo e recupera automaticamente | Conforme com nota | ADR-0017:198-228; ver ADR17-QA-001 |
| Preservar ADR-0016 e nao reintroduzir `\x1b[2J` por quadro | Conforme | ADR-0017:230-250, 424-426 |
| Plataforma POSIX/ANSI; Windows e `terminfo` fora do escopo | Conforme | ADR-0017:263-270, 363-364 |
| Nao-TTY sem handler reativo e sem sequencias de sessao | Conforme | ADR-0017:252-261, 427 |

## 6. Compatibilidade com ADR-0013 e ADR-0016

ADR-0013 exige que a tela ocupe largura e altura disponiveis do terminal, que `altura_disponivel` seja dimensao explicita futura e que ocupacao vertical nao se confunda com `corpo.arranjo` (`ADR-0013`:66-79, 102-125, 148-164). A ADR-0017 complementa essa decisao ao definir como obter e atualizar largura/altura durante a sessao TTY (`ADR-0017`:272-280) e preserva `corpo.arranjo`/`tiling` (`ADR-0017`:176-184).

ADR-0016 preserva sessao TTY apenas quando stdin/stdout sao TTY, `cbreak`, `ISIG`, `OPOST`, alternate screen, cursor oculto, autowrap desativado, posicionamento absoluto, preenchimento ate a largura, escrita atomica, synchronized output, `\x1b[2J` apenas na entrada, restauracao em `finally`, Ctrl+C escopado e comportamento nao-TTY (`ADR-0016`:73-138). A ADR-0017 declara expressamente que complementa a ADR-0016 e lista essas preservacoes (`ADR-0017`:230-250), sem substituir a ADR anterior.

Nao foi encontrada contradicao bloqueante com decisoes anteriores.

## 7. Verificacao de autoridade

A ADR-0017 respeita a ordem de autoridade do `contrato_processo_desenvolvimento.md` (`contrato_processo_desenvolvimento.md`:28-40). Ela se apresenta como politica normativa da ADR (`ADR-0017`:71-73), referencia ADR-0013 e ADR-0016 como autoridades superiores sobre os temas ja aceitos, e trata codigo/testes/handoff como etapas futuras (`ADR-0017`:50-52, 343-352, 354-369, 429-446).

Nao apresenta nano, ncurses, relatorio historico ou codigo como fonte normativa superior. A mencao a `nano` aparece apenas na ADR-0016 como analogia de posicionamento absoluto, nao como autoridade arquitetural (`ADR-0016`:92-96). `ncurses`/`curses` aparecem como alternativas rejeitadas ou proibicoes (`ADR-0017`:77-79, 365, 376).

## 8. Verificacao de coerencia interna

Conforme:

- distingue inicializacao (`ADR-0017`:118-138) de sessao apos `SIGWINCH` (`ADR-0017`:140-163);
- define precedencia das fontes nas duas fases;
- exige par coerente largura/altura (`ADR-0017`:103-104);
- define validade de dimensoes (`ADR-0017`:106-116);
- restringe fallback `(80, 24)` ao estado inicial sem fontes validas (`ADR-0017`:161-163);
- conserva ultimas dimensoes validas quando fontes novas forem invalidas (`ADR-0017`:154-159);
- condiciona redesenho a novo par valido (`ADR-0017`:165-174);
- cobre reducao e ampliacao (`ADR-0017`:186-196);
- preserva nao-TTY (`ADR-0017`:252-261).

Notas de coerencia: ha uma formulacao em riscos que pode ser lida em tensao com a regra de nao redesenhar quando nao ha novo par valido (ADR17-QA-002). Ha tambem uma mencao a classe concreta de erro em terminal pequeno demais (ADR17-QA-001).

## 9. Verificacao de consequencias documentais

A ADR identifica corretamente os artefatos afetados para futura etapa `APLICAR_ADR`:

- `docs/adr/INDICE_ADR.md` (`ADR-0017`:305);
- `docs/contratos/contrato_tela_json.md` (`ADR-0017`:306);
- `docs/contratos/contrato_composicao_corpo.md` (`ADR-0017`:307);
- `docs/NOMENCLATURA.md` (`ADR-0017`:308).

A exclusao de `docs/contratos/contrato_processo_desenvolvimento.md` e aceitavel porque a ADR nao introduz consequencia processual nova (`ADR-0017`:310-311). Nao identifiquei outro documento obrigatoriamente afetado nesta etapa. `contrato_barra_de_menus.md` pode ser referenciado futuramente se a aplicacao quiser explicitar apenas recalcule visual sem mudar distribuicao, mas a ADR corretamente deixa detalhes especificos da barra no contrato proprio (`ADR-0017`:367-369); isso nao torna o contrato da barra afetado obrigatorio.

## 10. Verificacao do escopo negativo

Confirmado que a ADR nao altera codigo, nao altera testes, nao aplica contratos, nao cria handoff, nao reserva numero de handoff, nao escolhe execucao pesada dentro do handler, nao introduz suporte Windows, nao introduz `terminfo` e nao autoriza biblioteca de TUI.

Evidencias principais: `ADR-0017`:50-52, 87-90, 343-352, 354-369, 429-446.

## 11. Achados

### ADR17-QA-001

- Severidade: medio
- Categoria: detalhe interno de implementacao normatizado sem decisao explicita
- Evidencia: `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`:198-206
- Descricao: a decisao do usuario exige que terminal pequeno demais nao encerre a sessao, nao mantenha quadro antigo e nao desenhe alem da area. A ADR acrescenta a proibicao especifica de "propagar `RenderizadorErro` como encerramento normal".
- Impacto: a mencao a uma classe/nome concreto de erro pode amarrar a futura implementacao a um detalhe interno nao decidido pelo usuario. Nao contradiz a politica funcional, mas amplia o texto normativo com artefato tecnico especifico.

### ADR17-QA-002

- Severidade: medio
- Categoria: coerencia interna / condicao para nao redesenho
- Evidencia: `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`:154-159 e 332-335
- Descricao: a secao decisoria determina que, se `ioctl` e variaveis forem invalidos, o sistema deve conservar as ultimas dimensoes validas e "nao redesenhar como se o tamanho tivesse mudado". Em "Riscos", a ADR afirma que "o redesenho pode ocorrer com as dimensoes do estado anterior ate que `ioctl` retorne valores consistentes".
- Impacto: a segunda formulacao pode ser lida como autorizacao para redesenhar mesmo sem novo par valido, enfraquecendo a regra de nao redesenho em dimensoes invalidas. A decisao normativa principal permanece correta, mas a ambiguidade deveria ser removida em revisao.

### ADR17-QA-003

- Severidade: observacao
- Categoria: forma documental / classificacao de artefatos
- Evidencia: `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`:12-16
- Descricao: o metadado `contratos_afetados` inclui `docs/NOMENCLATURA.md` e `docs/adr/INDICE_ADR.md`, que nao sao contratos de modulo, embora sejam artefatos documentais afetados.
- Impacto: nao bloqueia, pois o padrao ja aparece em ADR anterior e a tabela de consequencias deixa claro que se trata de artefatos a atualizar. E apenas uma nota de nomenclatura de metadados.

## 12. Limitacoes da auditoria

- Auditoria documental; nao houve execucao de testes nem inspecao de implementacao como fonte normativa.
- Codigo, testes, handoffs e relatorios historicos nao foram usados como autoridade superior.
- O diff de arquivo novo foi verificado por `git diff --no-index`; o codigo 1 foi tratado corretamente como diferenca esperada.
- Este relatorio nao corrige os achados, por restricao explicita do prompt.

## 13. Status final

`ADR_APPROVED_WITH_NOTES`

Justificativa: a ADR registra a politica solicitada de forma substancialmente aderente e implementavel, preserva as ADRs anteriores e respeita o escopo documental. Os achados identificados sao correcoes de precisao/limpeza normativa, sem bloqueio arquitetural e sem exigir nova decisao do usuario.

## 14. Proxima categoria permitida

`APLICAR_ADR`

Sem gerar prompt para a proxima etapa.
