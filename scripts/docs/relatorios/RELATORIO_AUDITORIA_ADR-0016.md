---
name: RELATORIO_AUDITORIA_ADR-0016
description: Relatório de auditoria da ADR-0016 (execução em tela cheia TTY sem cintilação) — verificação de existência de artefatos, checklist estrutural e achados; segunda iteração sobre versão revisada da ADR
metadata:
  type: relatorio
  subtipo: auditoria
  data: 2026-07-10
  auditado: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
---

# Relatório de Auditoria — ADR-0016 (segunda iteração)

**Data:** 2026-07-10
**Artefato auditado:** `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`
**Auditor:** Claude Sonnet 4.6 (sessão de auditoria somente leitura)
**Nota de iteração:** Existe uma versão anterior deste relatório, gerada para
uma revisão anterior da ADR que continha o achado bloqueante B-01 (ADR
presupunha existência de `docs/handoff/H-0022-*.md`). A versão atual da ADR
corrigiu esse ponto; este relatório audita a versão atual e substitui o anterior.

---

## 1. Status Final

**APROVADO_COM_RESSALVAS**

Motivo: A ADR não apresenta achados bloqueantes na versão atual. Os achados
bloqueantes identificados na auditoria anterior foram corrigidos: (a) a ADR
afirma explicitamente que H-0022 não existe como documento de handoff; (b) a
seção `## Data` está presente no corpo. Restam cinco ressalvas não bloqueantes
documentadas na seção 4.

---

## 2. Resultado item a item da ETAPA B (checklist completa)

---

### Item 1 — Frontmatter contém todos os campos presentes em ADRs aceitas?

**PARCIAL**

Campos verificados no frontmatter da ADR-0016 e comparados com ADR-0011 e
ADR-0014 (ADRs aceitas de referência):

| Campo | ADR-0011 | ADR-0014 | ADR-0016 |
|---|---|---|---|
| `name` | ✓ | ✓ | ✓ |
| `description` | ✓ | ✓ | ✓ |
| `metadata.type` | ✓ | ✓ | ✓ |
| `metadata.status` | ✓ | ✓ | ✓ |
| `metadata.data` | ✓ | ✓ | ✓ |
| `metadata.substitui` | ✓ | ✓ | ✓ |
| `rastreabilidade.rfc_origem` | ✓ | ✓ | ✓ |
| `rastreabilidade.issues_relacionadas` | ✓ | ✓ | ✓ |
| `rastreabilidade.contratos_afetados` | ✓ | ✓ | ✓ |
| `rastreabilidade.handoffs_bloqueados` | `[]` | `[]` | texto longo |

Todos os campos estão presentes. Ressalva: o campo `handoffs_bloqueados`
nos ADRs aceitos de referência contém lista de caminhos de arquivo (ou lista
vazia `[]`). Na ADR-0016, o campo contém um parágrafo explicativo longo:

```yaml
handoffs_bloqueados:
  - Nenhum handoff H-0022 existe no repositório. A implementação anterior
    está registrada apenas em docs/relatorios/IMP-0022-...
```

O conteúdo é correto e útil, mas o uso do campo como texto narrativo desvia
da convenção do template (lista de paths ou lista vazia). Ressalva
não-bloqueante; ver NB-01.

---

### Item 2 — O número ADR-0016 realmente não colide com nenhuma ADR existente no diretório?

**SIM**

Verificação executada via `ls docs/adr/`. O diretório lista ADR-0001 a
ADR-0016 (16 arquivos únicos). O INDICE_ADR.md confirma ADR-0016 com status
`proposta` e data `2026-07-10`. Nenhum outro arquivo inicia com `ADR-0016`.
Sem colisão.

---

### Item 3 — Todas as seções obrigatórias estão presentes na ordem usada pelas ADRs aceitas?

**SIM**

Seções obrigatórias verificadas nas ADRs de referência (ADR-0011, ADR-0014):
`Status → Data → Contexto → Decisão → Consequências → Fora do escopo →
Alternativas consideradas`

Seções presentes em ADR-0016:
`Status → Data → Contexto → Decisão → Consequências → Fora do escopo →
Alternativas consideradas`

A ordem é idêntica. Todas as seções obrigatórias estão presentes.

Nota: A versão anterior da ADR não tinha a seção `## Data` no corpo. A versão
atual incluiu essa seção (linha 27 do documento: `## Data` / `2026-07-10`),
corrigindo a ressalva NB-01 do relatório anterior.

---

### Item 4 — Cada arquivo citado no texto existe de fato no repositório?

**SIM** (com observação sobre H-0023)

Verificação realizada via `ls` nos diretórios relevantes:

| Referência no texto da ADR | Caminho verificado | Resultado |
|---|---|---|
| "handoff H-0009" | `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md` | **EXISTE** |
| "H-0009/H-0021" (item 11) | `docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md` | **EXISTE** |
| H-0022 | Explicitamente afirmado como inexistente pela ADR | **CONFIRMADO AUSENTE** (ver item 5) |
| IMP-0022 | `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md` | **EXISTE** |
| `contrato_tela_json.md` | `docs/contratos/contrato_tela_json.md` | **EXISTE** |
| `contrato_console.md` | `docs/contratos/contrato_console.md` | **EXISTE** |
| `contrato_processo_desenvolvimento.md` | `docs/contratos/contrato_processo_desenvolvimento.md` | **EXISTE** |
| `INDICE_ADR.md` | `docs/adr/INDICE_ADR.md` | **EXISTE** |
| `tela/demo.py` | `tela/demo.py` | **EXISTE** (modificado; confirmado por git status) |
| `config/` | `config/` (diretório) | **EXISTE** |

**Observação sobre H-0023:** A ADR menciona "Handoff futuro de
redimensionamento reativo (SIGWINCH) permanece sob H-0023, conforme já
registrado em IMP-0022" (Pendências derivadas) e "Redimensionamento reativo
da janela do terminal (SIGWINCH) — H-0023" (Fora do escopo). O documento
`docs/handoff/H-0023-*.md` não existe (o diretório vai até H-0021). A
referência é a um número reservado para handoff futuro, não a um documento
existente. A frase "permanece sob H-0023" pode ser interpretada
ambiguamente como "já está documentado em H-0023", o que seria falso. O
contexto deixa claro que é referência futura, mas a redação é potencialmente
ambígua; ver NB-02.

---

### Item 5 — A ADR afirma corretamente que H-0022 NÃO existe como documento de handoff no repositório (apenas o relatório IMP-0022 existe)?

**SIM**

A ADR afirma explicitamente, em múltiplos pontos, que H-0022 não existe como
documento de handoff:

1. **Frontmatter (`handoffs_bloqueados`):** "Nenhum handoff H-0022 existe no
   repositório. A implementação anterior está registrada apenas em
   `docs/relatorios/IMP-0022-...`, sem handoff que a precedesse."

2. **Seção Contexto:** "não há arquivo `docs/handoff/H-0022-*.md` no
   repositório, apenas o relatório de implementação. O rótulo 'H-0022' aparece
   somente nos metadados internos do próprio relatório, sem documento de handoff
   correspondente."

3. **Seção Consequências (Obrigatórias):** "Não existe handoff H-0022 a ser
   cancelado ou revisado — apenas o relatório de implementação."

4. **Seção Pendências derivadas:** "Como não existe handoff H-0022 a ser
   revisado ou cancelado, a pendência se resume a abrir um handoff novo..."

5. **Tabela "Arquivos que NÃO devem ser alterados":** lista
   `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md` como
   artefato histórico — sem mencionar `docs/handoff/H-0022-*.md`, que de fato
   não existe.

Verificação confirma: `ls docs/handoff/` vai de H-0001 a H-0021; nenhum
arquivo com prefixo `H-0022`. A ADR está correta em todas as suas afirmações
sobre H-0022.

**Nota histórica:** O relatório de auditoria anterior (versão anterior da ADR)
identificou este como achado bloqueante B-01, pois a ADR então presumia H-0022
existente. A versão atual corrigiu integralmente esse ponto.

---

### Item 6 — Os itens 1–11 da seção Decisão são internamente consistentes entre si?

**SIM**

Análise de consistência par a par:

- **Item 2 (cbreak) → Item 9 (Ctrl+C/ISIG):** `tty.setcbreak()` preserva
  `ISIG`, o que é pré-condição lógica do item 9 ("ISIG não é desligado —
  decorrência de cbreak, item 2"). Consistentes.
- **Item 2 (cbreak/OPOST) → Item 5 (posicionamento absoluto):** O motivo de
  rejeitar `setraw()` (item 2) é que desliga `OPOST`, quebrando conversão de
  `\n`. O item 5 (posicionamento absoluto `CSI <linha>;1H`) contorna o problema
  de outra forma, sem contradizer o item 2 — são medidas complementares.
- **Item 3 (alternate screen) → Item 10 (restauração):** Entrada `\x1b[?1049h`
  tem saída espelhada `\x1b[?1049l` no item 10. Consistentes.
- **Item 4 (DECAWM desativado) → Item 10 (restauração):** `\x1b[?7l` na
  entrada tem `\x1b[?7h` na saída. Consistentes.
- **Item 7 (limpeza única de tela) → Alternativas consideradas:** A limpeza
  a cada quadro está explicitamente rejeitada nas Alternativas consideradas, e o
  item 7 é a consequência direta dessa rejeição. Consistentes.
- **Item 8 (synchronized output) → Item 7 (escrita atômica):** O item 8 é
  camada adicional sobre o item 7; não o substitui nem contradiz.
- **Item 11 (não-TTY) → Item 1 (guarda isatty):** O item 11 descreve o ramo
  `isatty()` falso do item 1. Consistentes.

Nenhum dos 11 itens contradiz outro.

---

### Item 7 — A seção Decisão contradiz alguma regra ativa em algum contrato vigente?

**SIM (PARCIAL) — Ressalva não bloqueante**

Verificação em duas etapas:

**Etapa 7a — Grep por termos técnicos de sessão TTY em todos os contratos:**

Termos buscados: `tty`, `isatty`, `alternate`, `cbreak`, `setraw`, `setcbreak`,
`termios`, `1049h`, `1049l`, `echo`, `raw`, `OPOST`, `ICANON`, `ISIG`, `sigint`,
`ctrl+c`, `ctrl`

Resultado: **zero ocorrências de termos de sessão TTY** em qualquer contrato
no diretório `docs/contratos/`. A ADR-0016 introduz política em área onde não
há norma vigente alguma. Não há contradição direta com nenhuma regra escrita.

**Etapa 7b — Leitura dos contratos em `contratos_afetados`:**

- **`contrato_processo_desenvolvimento.md`:** lido integralmente. A ADR cita
  corretamente as seções 5 (item 3: "Registrar ADR se houver decisão
  arquitetural") e 6 ("Nenhuma mudança de contrato pode ser escondida em
  implementação"). A ADR é consistente com ambas.
- **`contrato_console.md`:** lido integralmente. A seção 17 ("Pendências fora
  de escopo") lista "Renderização final em terminal: caracteres, cores, escape
  codes e chamadas de sistema não pertencem a este contrato." Esta é uma
  exclusão de escopo atual (pendência futura), não uma proibição permanente.
  A ADR quer adicionar a política de Ctrl+C ao contrato, o que é expansão
  legítima de escopo via ADR.

  **Ressalva:** A prosa das Consequências (Obrigatórias) diz "contrato_tela_json.md
  e contrato_console.md passam a registrar esta política como seção normativa
  de modo de execução TTY (itens 1–11 desta ADR)", implicando que ambos os
  contratos receberão todos os 11 itens. Mas a tabela "Artefatos a atualizar"
  especifica apenas "Registrar escopo de Ctrl+C durante execução de script
  interno" para `contrato_console.md`. Há tensão entre a amplitude da prosa
  ("itens 1–11") e o escopo menor da tabela (apenas item 9). Ver NB-03.

- **`contrato_tela_json.md`:** não lido integralmente, mas o grep exaustivo não
  encontrou nenhum termo de sessão TTY. O arquivo trata de declarações de schema
  JSON para tela; a probabilidade de conflito com política de sessão terminal é
  baixa. Risco residual existe mas não é eliminável sem leitura completa; ver
  NB-04.

---

### Item 8 — "Fora do escopo" e "Alternativas consideradas" cobrem as mesmas alternativas descartadas, sem contradição?

**SIM**

Mapeamento de cobertura:

| Alternativa | Em "Alternativas consideradas"? | Em "Fora do escopo"? |
|---|---|---|
| `tty.setraw()` | Sim ("causa progressão diagonal") | Não (correto — é alternativa, não escopo) |
| Quadro com `\r\n` sem posicionamento absoluto | Sim | Não |
| Manter autowrap ativo | Sim | Não |
| `\x1b[2J` a cada quadro | Sim ("cintilação") | Não |
| Múltiplas chamadas `write()` por quadro | Sim | Não |
| Não usar synchronized output | Sim | Não |
| Ctrl+C sempre encerra (ISIG padrão sem escopo) | Sim | Não |
| Desligar ISIG e tratar SIGINT manualmente | Sim | Não |
| `curses` | Sim | **Também** (referência a H-0009) |
| SIGWINCH reativo | Não | Sim (correto — é escopo futuro, não alternativa) |
| Terminais não-ANSI / Windows | Não | Sim (correto — é exclusão de escopo) |
| `terminfo` | Não | Sim (correto — é decisão de arquitetura excluída) |

`curses` aparece em ambas as seções. "Fora do escopo" aponta para proibição
herdada de H-0009 ("permanece proibida, conforme H-0009"). "Alternativas
consideradas" rejeita `curses` pelos critérios desta ADR especificamente. A
duplicação é redundante mas não conflitante — ambas as seções apontam à mesma
conclusão por caminhos diferentes.

Nenhuma alternativa descartada na Decisão está ausente de "Alternativas
consideradas". Nenhuma exclusão de escopo contradiz uma alternativa aceita.

---

### Item 9 — A tabela "Artefatos a atualizar" lista arquivos que de fato existem e são os corretos para a mudança descrita?

**SIM**

**Tabela "Artefatos a atualizar em tarefa subsequente":**

| Arquivo | Existe? | Correto para a mudança? |
|---|---|---|
| `docs/adr/INDICE_ADR.md` | **EXISTE** ✓ | Sim. ADR-0016 já consta como `proposta`; tarefa subsequente troca para `aceita` |
| `docs/contratos/contrato_tela_json.md` | **EXISTE** ✓ | Sim — local natural para seção normativa de modo de execução TTY |
| `docs/contratos/contrato_console.md` | **EXISTE** ✓ | Sim — escopo de Ctrl+C durante execução de script pertence ao comportamento de ação do console |
| `docs/contratos/contrato_processo_desenvolvimento.md` | **EXISTE** ✓ | Sim — registro de IMP-0022 como caso de violação dupla do ciclo padrão é coerente com seção 5 do contrato |

**Tabela "Arquivos que NÃO devem ser alterados":**

| Arquivo ou grupo | Existe? |
|---|---|
| `tela/demo.py` e demais módulos | **EXISTE** (confirmado por git status) |
| `docs/relatorios/IMP-0022-...` | **EXISTE** ✓ |
| `config/` | **EXISTE** ✓ (verificado via `ls`) |

Todos os arquivos das duas tabelas existem. Não há proteção de arquivo
inexistente (o achado B-01 do relatório anterior, que protegia
`docs/handoff/H-0022-*.md` inexistente, foi corrigido na versão atual).

---

### Item 10 — A ADR evita prescrever código/implementação diretamente?

**PARCIAL — Ressalva não bloqueante**

A ADR declara explicitamente no Contexto: "Ela **não corrige código** — define
a política que um handoff corretivo deve seguir." E em Consequências:
"Um handoff corretivo de implementação é necessário antes de qualquer nova
tentativa de QA manual da sessão TUI."

No entanto, a seção Decisão contém:

- Sequências de escape VT100/xterm específicas: `\x1b[?1049h`, `\x1b[?25l`,
  `\x1b[?25h`, `\x1b[?1049l`, `\x1b[?7l`, `\x1b[?7h`, `CSI <linha>;1H`,
  `\x1b[?2026h`, `\x1b[?2026l`, `\x1b[2J`
- Nomes de função Python reais: `tty.setcbreak()`, `termios.tcgetattr`,
  `sys.stdin.isatty()`, `sys.stdout.isatty()`, `shutil.get_terminal_size`,
  `write()`, `flush()`
- Constantes de sistema operacional: `ICANON`, `ECHO`, `OPOST`, `ISIG`
- Padrão comportamental em Python: `KeyboardInterrupt` e escopo de captura

Avaliação: O precedente do projeto (ADR-0014, aceita) inclui "Algoritmo
normativo mínimo" com 10 passos e uma estrutura JSON canônica completa. O nível
de especificidade técnica da ADR-0016 é consistente com esse precedente. A
diferença é que a ADR-0016 usa nomes de função Python reais em vez de
pseudocódigo, o que a posiciona ligeiramente mais próxima da implementação.
Isso cria potencial rigidez: se a plataforma não disponibilizar `tty.setcbreak()`
diretamente, o handoff precisará interpretar o espírito da prescrição, não a
letra. Esta ressalva deve ser registrada no handoff corretivo; ver NB-05.

---

## 3. Lista de achados bloqueantes

**Nenhum.**

A versão atual da ADR não apresenta achados bloqueantes. O achado B-01 do
relatório anterior (ADR presumia H-0022 existente) foi corrigido na versão atual,
que agora declara explicitamente — no frontmatter, no Contexto, nas Consequências
e nas Pendências derivadas — que H-0022 não existe como documento de handoff.

---

## 4. Lista de achados não bloqueantes / ressalvas

### RESSALVA NB-01

**Título:** Campo `handoffs_bloqueados` contém texto narrativo em vez de lista
de paths (uso não-convencional do campo).

**Localização:** Frontmatter da ADR-0016, campo `rastreabilidade.handoffs_bloqueados`.

**Detalhes:** As ADRs aceitas de referência (ADR-0011, ADR-0014) têm
`handoffs_bloqueados: []` (lista vazia) ou lista de caminhos de arquivo. Na
ADR-0016, o campo contém um parágrafo de 60+ palavras explicando a ausência de
H-0022 e a pendência processual. O conteúdo é correto e útil, mas o uso do
campo como texto narrativo desvia da convenção de template. O template parece
projetado para listar `docs/handoff/H-XXXX-*.md` como paths a bloquear, não
para narrar situações.

**Impacto:** Baixo. Não viola nenhuma regra escrita. Potencial problema se
ferramentas de automação parsearem o campo como lista de paths.

---

### RESSALVA NB-02

**Título:** Referência a H-0023 usa "permanece sob H-0023" quando H-0023 não
existe, o que pode ser lido como se o documento já existisse.

**Localização:** Seção "Pendências derivadas": "Handoff futuro de
redimensionamento reativo (SIGWINCH) permanece sob H-0023, conforme já
registrado em IMP-0022"; seção "Fora do escopo": "Redimensionamento reativo
da janela do terminal (SIGWINCH) — H-0023."

**Detalhes:** O arquivo `docs/handoff/H-0023-*.md` não existe (o diretório de
handoffs vai até H-0021). A frase "permanece sob H-0023" usa presente
indicativo e pode ser lida como "está documentado em H-0023", o que seria
incorreto. O contexto deixa claro que é uma reserva de número para handoff
futuro (IMP-0022 também usa a mesma referência: "O tratamento de SIGWINCH e
redesenho após redimensionamento da janela pertence ao H-0023"), mas a
redação é potencialmente ambígua.

**Impacto:** Baixo. O contexto é suficiente para interpretar corretamente.
Nenhuma rastreabilidade quebrada.

---

### RESSALVA NB-03

**Título:** Tensão entre prosa e tabela nas Consequências — amplitude da política
TTY a ser adicionada a `contrato_console.md`.

**Localização:** Seção Consequências, subseção "Obrigatórias" (prosa) versus
tabela "Artefatos a atualizar".

**Detalhes:** A prosa diz: "contrato_tela_json.md e contrato_console.md passam
a registrar esta política como seção normativa de modo de execução TTY (itens
1–11 desta ADR)." A tabela, para `contrato_console.md`, diz apenas "Registrar
escopo de Ctrl+C durante execução de script interno" (item 9). A amplitude da
prosa ("itens 1–11") é maior que o escopo da tabela (apenas item 9).

A adição de todos os 11 itens ao `contrato_console.md` também entra em tensão
com a seção 17 desse contrato, que lista "escape codes e chamadas de sistema"
como "fora do escopo" do contrato. A tabela (somente Ctrl+C) é mais coerente
com o escopo natural de `contrato_console.md` do que a prosa.

**Impacto:** A tabela é a especificação operacional da tarefa subsequente; a
prosa é explicação contextual. Na prática, o executor do handoff usará a tabela.
Mas a prosa pode induzir à interpretação de que itens 1–10 também devem ser
adicionados ao `contrato_console.md`. Recomenda-se que o handoff corretivo
seja explícito sobre qual seção de qual contrato recebe cada item.

---

### RESSALVA NB-04

**Título:** `contrato_tela_json.md` não foi lido integralmente nesta auditoria.

**Detalhes:** O grep exaustivo por termos de sessão TTY em todos os contratos
retornou zero ocorrências. Entretanto, `contrato_tela_json.md` é o maior contrato
do repositório (700+ linhas conforme tamanho inferido do grep) e não foi lido
integralmente. O grep cobre termos técnicos específicos; não substitui leitura
completa. O risco de que o contrato contenha alguma regra sobre comportamento de
execução ou sessão que conflite com ADR-0016 foi mitigado mas não eliminado.

**Impacto:** Residual. O contrato cobre declarações de schema JSON para tela;
sessões de terminal não são domínio esperado. Auditoria posterior com leitura
integral pode eliminar este risco residual.

---

### RESSALVA NB-05

**Título:** A seção Decisão especifica nomes de função Python reais, criando
rigidez de implementação.

**Localização:** Itens 2, 7, 9, 10, 11 da seção Decisão.

**Detalhes:** A Decisão usa `tty.setcbreak()`, `write()`, `flush()`,
`shutil.get_terminal_size`, `sys.stdin.isatty()`, `sys.stdout.isatty()`,
`KeyboardInterrupt`, `termios.tcsetattr` como nomes de função Python reais
(não pseudocódigo). Se a plataforma alvo não disponibilizar o módulo `tty`
diretamente (ex.: implementação Python sem stdlib completa), o handoff
precisará usar equivalentes de `termios` manual sem poder invocar
`tty.setcbreak()` literalmente. A ADR menciona isso de passagem no item 2:
"`tty.setcbreak()` (ou `termios` seletivo manual com resultado equivalente)".

O precedente de ADR-0014 (aceita) inclui pseudocódigo normativo mas não nomes
de função reais de biblioteca específica, o que a mantém mais agnóstica de
plataforma. ADR-0016 está ligeiramente mais prescritiva.

**Impacto:** O handoff corretivo deve interpretar as prescrições como "resultado
equivalente" (como a ADR mesmo abre margem no item 2), não como chamadas
literais obrigatórias. Não é bloqueio à aceitação da ADR, mas é ponto de
atenção ao escrever o handoff.

---

## 5. Confirmação de escopo desta auditoria

Esta auditoria realizou **somente leitura** dos seguintes artefatos:

- `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_console.md`
- `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md` (versão anterior)
- `ls docs/adr/`, `ls docs/relatorios/`, `ls docs/contratos/`, `ls docs/handoff/`
- `ls config/`
- `grep` por termos TTY técnicos em `docs/contratos/contrato_tela_json.md` e
  em `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`

**Nenhum arquivo foi criado ou alterado além deste relatório.**

O único arquivo criado/sobrescrito nesta tarefa é:
`docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md`

Nenhuma ADR, contrato, handoff, índice ou arquivo de código foi modificado.
