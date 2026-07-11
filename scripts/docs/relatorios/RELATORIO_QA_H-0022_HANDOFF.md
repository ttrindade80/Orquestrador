# Relatório de QA — auditoria do handoff H-0022

## 1. Status final

**BLOQUEADO**

Motivo determinante: o critério de aceite do Item 7 permite que a sequência de
limpeza de tela `\x1b[2J` não seja emitida, enquanto a ADR-0016 determina que
ela ocorra uma única vez, na entrada da sessão. Assim, o handoff não traduz
integralmente o Item 7 da Decisão da ADR e pode aprovar uma implementação não
conforme.

## 2. Evidências da coleta

- A ADR-0016 foi lida integralmente: 212 linhas.
- O H-0022 foi lido integralmente: 216 linhas.
- O H-0009 foi lido integralmente: 1053 linhas, incluindo seu formato de
  checklist de critérios de aceite. O H-0022 segue o mesmo padrão geral de
  critérios agrupados, caixas de seleção, verificações por inspeção/comando e
  marcação explícita de verificações manuais.
- `ls -la docs/handoff/` mostrou H-0022 como o handoff de maior numeração e o
  arquivo mais recente da pasta, posterior a H-0021. Não há H-0023 nem handoff
  de numeração superior.
- A busca `find docs/handoff -maxdepth 1 -type f -name 'H-0022*' -print`
  retornou somente
  `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`. Não existe outro
  H-0022 duplicado ou conflitante na pasta.
- A consulta ao histórico Git de `docs/handoff/` não encontrou H-0022 anterior
  rastreado. O H-0022 atual está não rastreado, coerentemente com sua criação
  como primeiro handoff desse número no estado observado.
- O relatório referenciado
  `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md` existe e
  foi inspecionado. Ele se identifica como relatório de implementação, atribui
  internamente o rótulo “Handoff: H-0022” e documenta a tentativa anterior com
  `tty.setraw`, sem constituir arquivo de handoff.
- No `git status` inicial, `tela/demo.py` e `tela/teste_demo.py` constavam como
  modificados e não commitados. Logo, o stash específico descrito no
  “Pré-requisito antes da implementação” não havia sido executado sobre esses
  arquivos no momento da auditoria.

## 3. Resultado item a item da Etapa B

### 3.1. Correspondência entre os itens 1–11 da ADR e os critérios do handoff

**PARCIAL**

Mapeamento explícito:

| Item da Decisão da ADR-0016 | Critério correspondente no H-0022 | Resultado |
|---|---|---|
| 1 — ativação somente com stdin e stdout TTY | “Item 1 — Ativação da sessão TUI somente com stdin e stdout TTY” | SIM |
| 2 — `cbreak`, não `raw`, preservando `OPOST` e `ISIG` | “Item 2 — Modo de entrada: cbreak, não raw” | SIM |
| 3 — alternate screen e cursor oculto/restaurado | “Item 3 — Alternate screen buffer com cursor oculto e restaurado” | SIM |
| 4 — autowrap desativado e restaurado | “Item 4 — Autowrap (DECAWM) desativado e restaurado” | SIM |
| 5 — posicionamento absoluto linha a linha | “Item 5 — Desenho por posicionamento absoluto linha a linha” | SIM |
| 6 — preenchimento até a largura do terminal | “Item 6 — Preenchimento de linha até a largura do terminal” | SIM |
| 7 — escrita atômica; uma única limpeza na entrada | “Item 7 — Escrita atômica por quadro; limpeza de tela apenas na entrada” | PARCIAL |
| 8 — synchronized output em cada quadro | “Item 8 — Synchronized output em cada atualização de quadro” | SIM |
| 9 — Ctrl+C escopado | “Item 9 — Ctrl+C escopado: interrompe script interno, ignorado fora desse escopo” | SIM |
| 10 — restauração garantida em `finally` | “Item 10 — Restauração garantida do terminal em finally” | SIM |
| 11 — comportamento não-TTY preservado | “Item 11 — Comportamento não-TTY preservado sem alteração” | SIM |

O Item 7 é apenas parcial porque a ADR diz que `\x1b[2J` ocorre **uma única
vez**, na entrada da sessão, mas o handoff aceita que ocorra **no máximo uma
vez**. “No máximo uma vez” inclui zero ocorrências. O teste automatizado também
fala em “`\x1b[2J` único fora do loop”, mas não corrige inequivocamente o
critério normativo anterior nem exige de forma direta a presença da sequência
na inicialização. Este é achado bloqueante.

### 3.2. Critério que exige algo não presente na ADR-0016

**NÃO**, quanto a requisito funcional ou arquitetural novo.

Os comandos via pipe, inspeções de strings, exigência de testes automatizados
e verificações manuais detalham como observar as decisões da ADR; não criam
novo comportamento de produto. Os critérios de “Escopo e ausências” também
materializam a lista exaustiva de arquivos permitidos do próprio handoff.

Há uma prescrição estrutural estreita no Item 9 — “pelo menos um bloco `except
KeyboardInterrupt` fora do `finally`” — mas ela deriva diretamente da decisão
da ADR de capturar `KeyboardInterrupt`, não sendo classificada como invenção
de requisito. Ainda assim, a redação privilegia uma forma de implementação e
é registrada como ressalva não bloqueante.

### 3.3. Consistência do escopo permitido

**SIM**

A seção “Escopo permitido” autoriza exclusivamente `tela/demo.py` e
`tela/teste_demo.py`. Em “Critérios de aceite > Escopo e ausências”, o handoff
exige que somente esses dois arquivos tenham sido criados ou alterados e que
nenhum outro arquivo seja modificado. As duas seções são consistentes entre
si.

### 3.4. Consistência entre os Itens 9 e 10 sobre Ctrl+C

**PARCIAL**

Não há contradição operacional necessária se “o `finally` cobre o loop” for
entendido estruturalmente: o `KeyboardInterrupt` fora do escopo de script pode
ser capturado dentro do loop e ignorado, mantendo a sessão ativa; quando o
loop efetivamente termina por Esc ou por outra exceção, o `finally` restaura o
terminal. Nesse sentido, trata-se de redundância defensiva aceitável.

Entretanto, a frase do Item 10 segundo a qual o `finally` cobre “Ctrl+C fora de
escopo de script” é semanticamente ambígua: o mesmo evento que é capturado e
ignorado pelo Item 9 não pode, simultaneamente, provocar a saída e a execução
do `finally`. A ambiguidade já está na própria ADR-0016 e foi reproduzida pelo
handoff; portanto, não é invenção nem contradição nova do H-0022. É ressalva
não bloqueante, mas o teste deve distinguir “o loop está lexicalmente protegido
por `finally`” de “Ctrl+C ignorado dispara restauração e saída”.

### 3.5. Observabilidade e testabilidade dos critérios

**PARCIAL**

A grande maioria dos critérios é observável por comando concreto, inspeção de
string ou verificação explicitamente marcada como “verificação manual de QA”.
Não há formulação genérica como “deve funcionar bem”.

Há, porém, três limitações explícitas:

1. O Item 7 usa “no máximo uma vez”, teste observável, mas insuficiente para
   observar a obrigação exata da ADR de uma limpeza inicial.
2. No Item 9, o critério sobre o código que dispara script/processo interno não
   fornece comando, cenário, função ou processo concreto. A inspeção do
   repositório encontrou navegação e subprocessos nos testes, mas não encontrou
   em `tela/demo.py` uma execução de script/processo interno à qual esse
   critério possa ser aplicado no estado atual. A obrigação vem da ADR, porém
   sua verificação não está operacionalizada pelo handoff. Isso é ressalva de
   verificabilidade; caso não exista tal fluxo no momento da implementação, o
   critério deve ser registrado como não verificável, não presumido como
   atendido.
3. O critério do Item 10 que diz que o `finally` “cobre” Ctrl+C fora do escopo
   não define um cenário de teste que diferencie proteção lexical de execução
   efetiva do `finally`, em razão da captura silenciosa exigida pelo Item 9.

### 3.6. Relação com a implementação anterior

**SIM**

A seção “Relação com a implementação anterior” é consistente com a ADR-0016 e
com o repositório observado: não há evidência de handoff H-0022 anterior no
histórico ou na pasta; há somente o relatório IMP-0022, que documenta a
implementação anterior e usa “H-0022” apenas como rótulo interno. O H-0022
atual é o primeiro documento de handoff desse número.

### 3.7. Pré-requisito de `git stash`

**SIM**

O handoff marca explicitamente que não executa o comando e que o stash é
responsabilidade do executor da implementação. O estado real é coerente com
essa declaração: `tela/demo.py` e `tela/teste_demo.py` permanecem modificados
e não commitados, logo o pré-requisito continua pendente no momento desta
auditoria.

### 3.8. Consistência do “Fora de escopo”

**SIM**

O handoff preserva todos os quatro grupos da ADR-0016:

- redimensionamento reativo via `SIGWINCH`, sem número reservado;
- terminais não ANSI/VT/xterm e Windows;
- detecção de capacidade via `terminfo`;
- proibição de `curses`, `textual` e `rich`.

O handoff apenas separa “Windows” em uma linha própria e acrescenta a cláusula
de cobertura “Qualquer outro tema listado como ‘Fora do escopo’ na ADR-0016”,
sem adicionar nem remover tema substantivo.

## 4. Achados bloqueantes

### ACH-BLOQ-01 — Item 7 aceita zero limpezas de tela

- **Referência exata no handoff:** “Critérios de aceite > Item 7 — Escrita
  atômica por quadro; limpeza de tela apenas na entrada”, segundo critério.
- **Texto problemático:** a sequência `\x1b[2J` ocorre “no máximo uma vez”.
- **Regra da ADR:** “Decisão > 7. Escrita atômica por quadro” determina que a
  limpeza ocorra “uma única vez, na entrada da sessão”.
- **Impacto:** uma implementação sem `\x1b[2J` poderia satisfazer literalmente
  o handoff, mas violaria a ADR. Portanto, o Item 7 não possui cobertura de
  aceite integral.

## 5. Ressalvas não bloqueantes

### RESS-01 — Ambiguidade defensiva entre Ctrl+C ignorado e `finally`

As seções “Critérios de aceite > Item 9” e “Critérios de aceite > Item 10”
reproduzem uma ambiguidade da ADR: Ctrl+C fora do escopo deve ser ignorado e
manter a sessão, enquanto o `finally` é descrito como cobrindo esse mesmo
evento. A leitura coerente é que o loop inteiro está protegido pelo `finally`,
não que todo Ctrl+C ignorado execute a restauração. Recomenda-se tornar essa
distinção testável em revisão futura do handoff/ADR; nenhum desses arquivos foi
alterado nesta auditoria.

### RESS-02 — Cenário de script/processo interno não concretizado

Em “Critérios de aceite > Item 9”, a captura local durante execução de
script/processo interno não aponta comando, função ou cenário concreto. No
estado atual inspecionado de `tela/demo.py`, não foi localizado fluxo de
execução de script/processo interno. O requisito vem da ADR e não deve ser
removido por suposição, mas sua verificação deve ser explicitamente registrada
como não verificável enquanto esse fluxo não puder ser identificado.

### RESS-03 — Critério estrutural mais estreito que o comportamento

Em “Critérios de aceite > Item 9”, exigir literalmente um bloco `except
KeyboardInterrupt` limita a forma de implementação, embora a ADR determine
principalmente o comportamento de captura. A exigência é compatível com a
redação da ADR, mas testes comportamentais seriam evidência mais robusta que a
mera presença da string ou do bloco.

## 6. Integridade desta auditoria

Nenhum handoff, ADR, contrato, relatório anterior ou arquivo de código foi
editado por esta auditoria. O único arquivo criado ou alterado por esta
auditoria foi:

`docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md`

As demais modificações e arquivos não rastreados exibidos pelo Git já estavam
presentes na coleta inicial e não foram produzidos nem alterados nesta
auditoria.
