# IMP-0024 — Relatório de Implementação: Redimensionamento Reativo da TUI

## Metadados

| Campo | Valor |
|---|---|
| ID | IMP-0024 |
| Handoff de origem | H-0023-redimensionamento-reativo-tui.md |
| ADR de referência | ADR-0017-redimensionamento-reativo-tui.md |
| Status do handoff na entrada | H1_HANDOFF_APPROVED |
| Status desta implementação | IMPLEMENTACAO_CONCLUIDA_PENDENTE_VALIDACAO_HUMANA |
| Branch | HEAD |
| Commit base | de0f023 |
| Stage na entrada | vazio |
| Arquivos alterados pela implementação H-0023 | tela/demo.py, tela/teste_demo.py, docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md |
| Data | 2026-07-11 |

> **Nota de precisão (PATCH_IMPLEMENTACAO).** Uma versão anterior deste relatório
> descrevia o worktree como contendo apenas os arquivos da implementação e
> afirmava que `docs/contratos/` e `docs/NOMENCLATURA.md` não estavam
> modificados. Isso confundia o **escopo da implementação H-0023** com o
> **estado global do worktree**, que já continha alterações documentais
> preexistentes do ciclo ADR-0017/H-0023. As seções 8 e 9 abaixo registram o
> estado Git integral e distinguem claramente: (a) alterações preexistentes ao
> patch; (b) a entrega global da implementação H-0023; (c) as alterações feitas
> pelo `PATCH_IMPLEMENTACAO`. Ver H0023-IMPL-QA-002.

---

## 1. Escopo da implementação

Esta implementação executa exclusivamente o passo `IMPLEMENTAR` do ciclo H-0023, conforme delimitado pelo handoff aprovado e pelo ADR-0017. Os arquivos alterados pela implementação H-0023 foram:

- `tela/demo.py` — reescrito integralmente para adicionar redimensionamento reativo
- `tela/teste_demo.py` — expandido com seção 8 (testes H-0023) e adaptações na seção 7H
- `docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md` — este arquivo

A implementação H-0023 **não alterou** `tela/renderizador.py` nem `tela/teste_renderizador.py`. Também **não alterou** nenhum documento em `docs/` além deste relatório: os arquivos `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_composicao_corpo.md` e `docs/contratos/contrato_tela_json.md` **já apareciam modificados no worktree** por etapas documentais anteriores do ciclo ADR-0017/H-0023; a implementação H-0023 não os tocou. O estado Git integral que sustenta essa distinção está na seção 8.

---

## 2. Mecanismo implementado

### 2.1 Importações adicionadas

```python
import fcntl
import signal
import struct
from tela.renderizador import renderizar_tela, RenderizadorErro
```

### 2.2 Constantes

```python
LARGURA_MINIMA_TELA = 10
ALTURA_MINIMA_TELA = 6
```

### 2.3 Funções novas

| Função | Responsabilidade |
|---|---|
| `_restaurar_efeitos_visuais_tui()` | Sequência de restauração visual compartilhada por rollback e encerramento normal |
| `_par_dimensoes_valido(largura, altura)` | Valida que o par (largura, altura) é inteiro positivo |
| `_obter_dimensoes_ioctl(fd)` | Lê dimensões via `ioctl(TIOCGWINSZ)` + `struct.unpack('HHHH', ...)` |
| `_obter_dimensoes_env()` | Lê dimensões de `LINES`/`COLUMNS` do ambiente |
| `_obter_dimensoes_iniciais(fd)` | Cadeia ioctl → env → fallback (80, 24) na inicialização |
| `_obter_dimensoes_apos_sigwinch(fd, ultimas_validas)` | Cadeia ioctl → env → ultimas_validas após SIGWINCH |
| `_instalar_handler_sigwinch(w_wakeup, resize_pendente)` | Instala handler async-signal-safe; escreve no pipe; retorna handler anterior |
| `_restaurar_handler_sigwinch(handler_anterior)` | Restaura handler anterior; silencia exceções internas |
| `_tela_pequena_demais(largura, altura)` | Testa se largura < 10 ou altura < 6 |
| `_quadro_minimo_aviso(largura, altura)` | Gera quadro de aviso com exatamente `altura` linhas, nenhuma excedendo `largura` |
| `_resolver_conteudo(estado, modelo, largura, altura)` | Resolve conteúdo: tela pequena → quadro mínimo; RenderizadorErro → quadro mínimo; normal → renderizar_estado |

### 2.4 Modificações em funções existentes

**`_iniciar_sessao_tui(fd_stdin)`** — adicionado rollback em caso de falha no `write`/`flush`:
- Se `sys.stdout.write` ou `sys.stdout.flush` lançarem, executa `_restaurar_efeitos_visuais_tui()` + `termios.tcsetattr` + re-raise da exceção original.
- `atributos_originais` obtidos antes de qualquer modificação visual.

**`_encerrar_sessao_tui(fd_stdin, atributos_originais)`** — delega restauração visual para `_restaurar_efeitos_visuais_tui()`, garantindo coerência com rollback.

**`_apresentar_quadro(conteudo, largura=None)`** — adicionado parâmetro opcional `largura`; quando fornecido, `shutil.get_terminal_size` não é chamado.

**`main()`** (ramo TTY) — reestruturado com:
- Flags sentinela: `r_wakeup`, `w_wakeup`, `sessao_iniciada`, `handler_instalado`, `handler_anterior`, `atributos_originais`
- `resize_pendente = [False]`
- `os.pipe()` com descritores não bloqueantes via `os.set_blocking(..., False)`
- SIGWINCH handler instalado via `_instalar_handler_sigwinch`
- Loop principal com `select.select([fd, r_wakeup], [], [])` (select duplo)
- Drenagem não bloqueante do pipe ao receber wakeup
- `_obter_dimensoes_apos_sigwinch` para atualizar dimensões
- `_resolver_conteudo` para resolver conteúdo (com suporte a tela pequena e RenderizadorErro)
- `finally` com cleanup condicional: handler → pipes → sessão TUI

### 2.5 Ordem de cleanup no `finally`

1. `if handler_instalado: _restaurar_handler_sigwinch(handler_anterior)`
2. `if r_wakeup is not None: os.close(r_wakeup)`
3. `if w_wakeup is not None: os.close(w_wakeup)`
4. `if sessao_iniciada: _encerrar_sessao_tui(fd, atributos_originais)`

Handler restaurado antes do fechamento do pipe, conforme especificação H-0023 §18.

---

## 3. Políticas ADR-0016 preservadas

| Política | Status |
|---|---|
| Alternate screen `\x1b[?1049h/l` | Preservada |
| Cursor oculto `\x1b[?25l/h` | Preservada |
| Autowrap `\x1b[?7l/h` | Preservada |
| `\x1b[2J` apenas na entrada (exatamente 1 ocorrência) | Verificado: count=1 |
| Synchronized output | Preservada |
| Escrita atômica via `sys.stdout.write` + `flush` | Preservada |
| Sem `\x1b[2J` em redraw por resize | Implementado |
| Python stdlib apenas (sem curses, textual, rich) | Verificado |

---

## 4. Resultados dos testes

### 4.1 `tela/teste_demo.py`

Comando executado: `python tela/teste_demo.py` — código de saída `0`.

```
Total de verificacoes: 303
Passaram: 303
Falharam: 0
```

> Contagem atualizada após o `PATCH_IMPLEMENTACAO` (era 297 antes do patch;
> +6 verificações pseudo-TTY na seção 8.16, ver seção 5.1).

Seções cobertas:
- **Seções 1–7** (H-0010A / H-0022): todas preservadas
- **Seção 8** (H-0023): 8.1–8.16 implementadas integralmente

### 4.2 `tela/teste_renderizador.py`

```
Total de verificacoes: 331
Passaram: 331
Falharam: 0
```

Sem regressões no renderizador.

### 4.3 Seção 8 — cobertura detalhada

| Subsecção | Descrição | Verificações |
|---|---|---|
| 8.1 | `_par_dimensoes_valido` (8 casos) | pass |
| 8.2 | `_obter_dimensoes_ioctl` (3 casos) | pass |
| 8.3 | `_obter_dimensoes_env` (4 casos) | pass |
| 8.4 | `_obter_dimensoes_iniciais` (4 casos: ioctl prevalece, env fallback, só linhas, nada) | pass |
| 8.5 | `_obter_dimensoes_apos_sigwinch` (4 casos: ioctl, env, ultimas_validas, negativo) | pass |
| 8.6 | Handler: instalação, retorno anterior, chamada única no ramo TTY | pass |
| 8.7 | Pipe não bloqueante, flag, pipe cheio, coalescência, drenagem | pass |
| 8.8 | Select duplo: resize com nova largura, handler restaurado, handler antes do pipe | pass |
| 8.9 | `_quadro_minimo_aviso`: múltiplas dimensões, altura exata, sem overflow | pass |
| 8.10 | `_tela_pequena_demais`: fronteiras L=10 / A=6, constantes | pass |
| 8.11 | `_apresentar_quadro` com/sem `largura`: shutil não chamado quando fornecido | pass |
| 8.12 | `_resolver_conteudo`: tela pequena, normal, RenderizadorErro | pass |
| 8.13 | Falhas parciais: write/flush/tcgetattr/restaurar/pipe/set_blocking/init/handler | pass |
| 8.14 | Regressão não-TTY: subprocess encerra com código 0, sem sequências TUI | pass |
| 8.15 | Inspeção de código: `\x1b[2J` único, imports, constantes, select duplo | pass |
| 8.16 | Pseudo-TTY: normal → redução (redraw + quadro mínimo) → ampliação (redraw + conteúdo normal) → Esc → cleanup | pass |

---

## 5. Validação humana

```
VALIDACAO_HUMANA_TTY_REAL: PENDENTE
```

Critérios pendentes de validação em TTY real:

1. Redução de janela: quadro mínimo aparece imediatamente, sem artefatos
2. Ampliação de janela: conteúdo normal restaurado sem residuos
3. Resize rápido (múltiplos SIGWINCH): coalescência funciona, sem travamento
4. Linha adicional após resize: não aparece linha extra abaixo do quadro
5. Flicker visual: ausente ou mínimo durante resize
6. Quadro de aviso: texto correto para dimensões abaixo dos mínimos
7. Recuperação automática: sem intervenção do usuário após ampliar
8. Echo suprimido: teclas digitadas durante a sessão não aparecem como texto bruto
9. Navegação preservada: teclas de navegação continuam funcionando após resize
10. Restauração após Esc: terminal retorna ao estado normal (cursor visível, tela normal)
11. Estado final: nenhum artefato visual residual após encerramento

### 5.1 Pseudo-TTY (executado automaticamente)

O teste 8.16 executa validação via `pty.openpty()` cobrindo uma sequência
completa: **normal → redução → redraw reduzido → ampliação → redraw normal →
Esc → cleanup**.

**Dimensões deterministas:**

| Fase | Dimensões (colunas × linhas) | Apresentação esperada |
|---|---|---|
| Normal inicial | 40 × 20 | Tela normal (contém `ORQUESTRADOR`) |
| Reduzida | 30 × 5 | Quadro mínimo (`terminal pequeno demais`); altura 5 < `ALTURA_MINIMA_TELA` (6) |
| Ampliada | 40 × 20 | Tela normal restaurada |

Cada resize é aplicado por `fcntl.ioctl(master_fd, TIOCSWINSZ, ...)` seguido de
`os.kill(pid, SIGWINCH)`.

**Evidência de redraw (não apenas processo ativo):** a saída capturada após
cada `SIGWINCH` é validada separadamente (`saida_inicial`, `saida_reducao`,
`saida_ampliacao`) e deve conter um novo bloco de synchronized output
(`ESC[?2026h`). A leitura usa `select` com deadline explícito (timeout total de
3 s por fase, corte por 0,3 s de ociosidade) — não depende apenas de
`time.sleep`, é determinista e não fica pendurada.

**Evidência do quadro mínimo na redução:** `saida_reducao` contém
`terminal pequeno demais` e **não** contém `ORQUESTRADOR`. O último quadro
extraído (após remoção controlada das sequências ANSI) tem no máximo 5 linhas
e no máximo 30 colunas, e a redução não emite `ESC[2J`.

**Evidência de recuperação do conteúdo normal:** `saida_ampliacao` contém
`ORQUESTRADOR` e **não** contém `terminal pequeno demais`; o último quadro tem
no máximo 20 linhas e 40 colunas (novas dimensões).

**Esc e cleanup:** ao final envia-se `\x1b`; o processo encerra dentro do
timeout com código de saída `0`; os descritores master/slave são fechados e o
processo é finalizado caso ainda esteja ativo (registrado como
`PTY: cleanup concluido`). O cleanup executa também no `finally`, inclusive
quando uma asserção falha.

**Comando:** `python tela/teste_demo.py` — código de saída `0`.

**Verificações da seção 8.16 (12, todas PASSOU):**

```
[PASSOU] PTY: quadro inicial capturado (processo ativo, quadro TUI, conteudo normal)
[PASSOU] PTY: reducao produziu redraw (novo quadro apos SIGWINCH, nao apenas processo ativo)
[PASSOU] PTY: quadro minimo apareceu na reducao ('terminal pequeno demais')
[PASSOU] PTY: quadro reduzido respeita dimensoes (<= 30 colunas e <= 5 linhas, sem linha extra)
[PASSOU] PTY: redraw de resize sem clear total (ESC[2J ausente na reducao)
[PASSOU] PTY: ampliacao produziu redraw (novo quadro apos segundo SIGWINCH)
[PASSOU] PTY: conteudo normal retornou apos ampliacao ('ORQUESTRADOR' presente, quadro minimo ausente)
[PASSOU] PTY: quadro ampliado usa novas dimensoes (<= 40 colunas e <= 20 linhas)
[PASSOU] PTY: processo permaneceu ativo nos dois resizes
[PASSOU] PTY: Esc encerrou o processo dentro do timeout
[PASSOU] PTY: codigo de saida 0 apos Esc
[PASSOU] PTY: cleanup concluido (descritores fechados e processo finalizado)
```

**Limitações remanescentes do pseudo-TTY:** conforme H-0023 §20.2, o pseudo-TTY
confirma atividade, resposta ao sinal, redraw e coerência dimensional
automatizável, mas **não** confirma ausência de resíduos visuais, ausência de
cintilação perceptível, comportamento sob resize rápido nem qualidade visual.
Esses aspectos permanecem para validação humana em TTY real (ver seção 5 e
seção 9.4).

---

## 6. Arquivos não tocados pela implementação H-0023

A implementação H-0023 **não alterou** os arquivos abaixo. Para os documentos
que aparecem modificados no `git status`, a formulação precisa é: *a
implementação não alterou esses documentos; eles já apareciam modificados no
worktree por etapas documentais anteriores do ciclo ADR-0017/H-0023.*

| Arquivo | Situação no worktree | Tocado pela implementação H-0023? |
|---|---|---|
| `tela/renderizador.py` | limpo (`git diff` vazio) | Não |
| `tela/teste_renderizador.py` | limpo (`git diff` vazio) | Não |
| `docs/handoff/H-0023-redimensionamento-reativo-tui.md` | não rastreado (ciclo do handoff) | Não |
| `docs/adr/ADR-0017-redimensionamento-reativo-tui.md` | não rastreado (ciclo ADR) | Não |
| `docs/NOMENCLATURA.md` | modificado (preexistente, ciclo ADR-0017) | Não |
| `docs/adr/INDICE_ADR.md` | modificado (preexistente, ciclo ADR-0017) | Não |
| `docs/contratos/contrato_composicao_corpo.md` | modificado (preexistente, ciclo ADR-0017) | Não |
| `docs/contratos/contrato_tela_json.md` | modificado (preexistente, ciclo ADR-0017) | Não |

---

## 7. Estado Git integral

> **Observação de preservação de evidência.** O snapshot integral anterior à
> implementação original não foi preservado neste relatório. O estado abaixo
> rotulado "antes do PATCH_IMPLEMENTACAO" foi observado no início do patch
> atual; o estado "após o PATCH_IMPLEMENTACAO" foi observado ao final. Não se
> inventa aqui o estado histórico exato do início da implementação original.

### 7.1 Antes do `PATCH_IMPLEMENTACAO`

`git log -1 --oneline`:

```text
de0f023 fix: corrige execução TTY em tela cheia
```

`git status --short`:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
 M tela/demo.py
 M tela/teste_demo.py
?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
?? docs/handoff/H-0023-redimensionamento-reativo-tui.md
?? docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0023_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md
```

`git diff --stat`:

```text
 scripts/docs/NOMENCLATURA.md                       |   48 +-
 scripts/docs/adr/INDICE_ADR.md                     |    1 +
 scripts/docs/contratos/contrato_composicao_corpo.md|   56 +-
 scripts/docs/contratos/contrato_tela_json.md       |  156 ++-
 scripts/tela/demo.py                               |  289 ++++-
 scripts/tela/teste_demo.py                         | 1141 +++++++++++++++++++-
 6 files changed, 1639 insertions(+), 52 deletions(-)
```

`git diff --cached --stat` e `git diff --cached --name-only`: sem saída (stage vazio).

`sha256sum tela/demo.py`:

```text
d23c14c1551948a305bb9e52fb72667f283b54c587b79da35c672f6f703b61a6  tela/demo.py
```

### 7.2 Classificação dos arquivos preexistentes ao patch

Já estavam modificados/não rastreados quando o `PATCH_IMPLEMENTACAO` começou —
o patch não os criou nem os alterou:

- **ADR e índice:** `docs/adr/ADR-0017-redimensionamento-reativo-tui.md` (`??`),
  `docs/adr/INDICE_ADR.md` (` M`).
- **Contratos:** `docs/contratos/contrato_composicao_corpo.md` (` M`),
  `docs/contratos/contrato_tela_json.md` (` M`).
- **Nomenclatura:** `docs/NOMENCLATURA.md` (` M`).
- **Handoff:** `docs/handoff/H-0023-redimensionamento-reativo-tui.md` (`??`).
- **Relatórios de QA:** `RELATORIO_APLICACAO_ADR-0017.md`,
  `RELATORIO_QA_ADR-0017.md`, `RELATORIO_QA_APLICACAO_ADR-0017.md`,
  `RELATORIO_QA_H-0023_HANDOFF.md`, `RELATORIO_QA_H-0023_IMPLEMENTACAO.md`,
  `RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md` e os pós-patch 2, 3 e 4 (todos `??`).
- **Relatório de implementação já existente:** `IMP-0024-…` (`??`, criado pela
  implementação H-0023 e atualizado por este patch).
- **Código de implementação já modificado:** `tela/demo.py` (` M`),
  `tela/teste_demo.py` (` M`).

### 7.3 Entrega global da implementação H-0023

A implementação H-0023 (etapa `IMPLEMENTAR`, anterior a este patch) alterou:

```text
tela/demo.py
tela/teste_demo.py
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
```

Isso **não** significa que esses fossem os únicos arquivos presentes como
modificados/não rastreados no worktree global — os documentos listados em 7.2
já coexistiam por etapas documentais anteriores.

### 7.4 Após o `PATCH_IMPLEMENTACAO`

`git status --short`:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
 M tela/demo.py
 M tela/teste_demo.py
?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
?? docs/handoff/H-0023-redimensionamento-reativo-tui.md
?? docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0023_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_2_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_3_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_4_H-0023_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0023_HANDOFF.md
```

`git diff --stat` (parte de código/testes):

```text
 scripts/tela/demo.py       |  289 ++++-
 scripts/tela/teste_demo.py | 1270 +++++++++++++++++++-
```

`git diff --cached --name-only`: sem saída (stage permanece vazio).

`sha256sum tela/demo.py`:

```text
d23c14c1551948a305bb9e52fb72667f283b54c587b79da35c672f6f703b61a6  tela/demo.py
```

O hash de `tela/demo.py` é **idêntico** ao registrado em 7.1 — comprova que este
patch **não** alterou `tela/demo.py`.

> O bytecode `tela/__pycache__/` gerado pela execução obrigatória dos testes foi
> removido após a execução; não permanece no worktree como arquivo adicional.

---

## 8. Alterações realizadas por este `PATCH_IMPLEMENTACAO`

Este patch corrigiu os achados `H0023-IMPL-QA-001` e `H0023-IMPL-QA-002` do
`RELATORIO_QA_H-0023_IMPLEMENTACAO.md` e alterou **somente**:

```text
tela/teste_demo.py
docs/relatorios/IMP-0024-redimensionamento-reativo-tui.md
```

- **`tela/teste_demo.py`** — expandida exclusivamente a seção 8.16 (pseudo-TTY),
  preservando todos os demais testes. Adicionadas duas funções auxiliares de
  teste locais (`_ler_pty_ate_ocioso`, leitura de PTY com deadline por `select`;
  `_linhas_ultimo_quadro`, extração do último quadro synchronized-output para
  medir linhas e colunas). O cenário passou a cobrir a sequência completa
  normal → redução → redraw reduzido → ampliação → redraw normal → Esc →
  cleanup, com evidência semântica da saída (não apenas processo ativo).
- **`docs/relatorios/IMP-0024-…`** — este relatório, atualizado para registrar o
  estado Git integral, distinguir escopo da implementação × estado global,
  descrever o novo cenário pseudo-TTY e a contagem de testes.

Registre-se explicitamente que **`tela/demo.py` permaneceu inalterado por este
patch**, comprovado pelo hash idêntico antes/depois (seção 7.1 e 7.4). Não foram
alterados handoff, ADRs, contratos, nomenclatura nem relatórios de QA.

---

## 9. Classificação, próximo passo e ausência de autoaprovação

### 9.1 Natureza desta etapa

Este `PATCH_IMPLEMENTACAO` corrigiu testes e evidências. **Não houve QA formal
nesta etapa**: o executor do patch não audita nem aprova a própria correção.

### 9.2 Nenhuma aprovação emitida

Nenhuma aprovação foi emitida por esta etapa. Não foi gerado prompt de QA. O
resultado deve retornar ao gerente e a correção ainda deve passar por
`QA_POS_PATCH`.

### 9.3 Git

Não houve `git add`, `git commit`, `git push`, `stash`, `reset` ou qualquer
alteração de histórico. O stage permanece vazio.

### 9.4 Validação humana

```
VALIDACAO_HUMANA_TTY_REAL: PENDENTE
```

Permanece pendente e **não** foram declarados aprovados: redução visual real,
ampliação visual real, resize rápido, resíduos, scroll, linha adicional,
flicker, echo, restauração visual final. O pseudo-TTY (seção 5.1) não substitui
a validação humana.

### 9.5 Próximo passo

Retorno ao gerente para `QA_POS_PATCH` da implementação. Nenhuma etapa posterior
foi iniciada por este patch.
