# Relatório de QA — H-0023 Handoff

## 1. Identificação

```yaml
etapa: QA_HANDOFF
projeto: Orquestrador
handoff: docs/handoff/H-0023-redimensionamento-reativo-tui.md
data: 2026-07-11
relatorio: docs/relatorios/RELATORIO_QA_H-0023_HANDOFF.md
```

## Status final

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: o H-0023 está substancialmente alinhado à ADR-0017 e ao
mecanismo técnico escolhido, mas contém um achado bloqueante processual no
estado Git comprovado: a seção 2 do handoff omite o próprio
`docs/handoff/H-0023-redimensionamento-reativo-tui.md` como arquivo não
rastreado, enquanto o estado real verificado o contém. Pela taxonomia autorizada
de `QA_HANDOFF`, isso sustenta `H2_HANDOFF_PATCH_REQUIRED`: os defeitos podem
ser corrigidos no próprio handoff, sem decisão arquitetural adicional, e o
handoff deve retornar a novo QA antes da implementação.

## 3. Escopo executado

Foi executada exclusivamente auditoria formal do handoff H-0023. Não houve
correção do handoff, implementação, alteração de código ou testes, alteração de
ADR, contratos ou nomenclatura, stage, commit, push ou alteração de histórico
Git.

Este relatório é o único arquivo criado nesta etapa.

## 4. Estado Git verificado

Comandos executados:

```bash
git status --short
git rev-parse --short HEAD
git branch --show-current
git diff --cached --stat
```

Resultado observado:

```text
HEAD: de0f023
branch: master
stage: vazio

 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
?? docs/handoff/H-0023-redimensionamento-reativo-tui.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md
```

O `stage` está vazio, conforme informado pelo autor. O `HEAD` e a branch
também conferem. A divergência está na lista de arquivos não rastreados
registrada pela seção 2 do handoff, que não inclui o próprio H-0023.

## 5. Autoridades lidas

Lidos integralmente:

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

Lidos também como estado diretamente relacionado:

- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`

Consultados para preservação e contradições:

- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`

## 6. Verificação do handoff

### 6.1 Integridade mecânica

Conforme, com ressalva de estado Git.

`wc -l` confirmou:

```text
1084 docs/handoff/H-0023-redimensionamento-reativo-tui.md
```

O arquivo existe no caminho esperado e foi lido integralmente. O metadado
interno do handoff registra `status: proposto`; o estado recebido do autor
registra `status: CRIADO`. Essa diferença não é tratada como achado bloqueante,
pois o ciclo observado usa o arquivo como handoff criado e sob QA, enquanto o
status formal de aprovação depende deste relatório.

### 6.2 Aderência à ADR-0017

Conforme em termos substantivos.

O H-0023 materializa:

- gerenciamento próprio do resize, sem `ncurses`, `curses`, `textual` ou `rich`;
- plataforma POSIX, sinais, `ioctl` e terminal ANSI/VT/xterm;
- `SIGWINCH` como gatilho em sessão TTY ativa;
- `ioctl(fd, TIOCGWINSZ, ...)` como fonte primária;
- tratamento de largura e altura como par coerente;
- validação de par somente quando ambos existem, são inteiros e maiores que zero;
- cadeia inicial `ioctl → LINES/COLUMNS → (80, 24)`;
- cadeia pós-`SIGWINCH` `ioctl → LINES/COLUMNS → últimas dimensões válidas`;
- proibição de aplicar par inválido ou redesenhar como mudança sem novo par;
- redesenho em redução e ampliação;
- preservação de `corpo.arranjo`, `tiling`, chips e composição declarativa;
- quadro mínimo para terminal pequeno demais;
- preservação da ADR-0016.

O mecanismo escolhido de wakeup pipe é compatível com a ADR-0017, que delega ao
handoff a decisão técnica sobre executar o trabalho no handler ou diferi-lo
para o fluxo normal. O H-0023 escolhe handler mínimo, flag e pipe, com
processamento posterior no loop principal.

### 6.3 Aderência à ADR-0016 e ADR-0013

Conforme.

O handoff preserva as políticas da ADR-0016: ativação somente com stdin/stdout
TTY, `cbreak`, preservação de `ISIG`/`OPOST`, alternate screen, cursor,
autowrap, posicionamento absoluto, escrita atômica, synchronized output,
`\x1b[2J` somente na entrada, restauração em `finally`, Ctrl+C escopado e
comportamento não-TTY.

Também preserva a ADR-0013: altura é dimensão explícita da renderização e a
ocupação vertical não colapsa com `corpo.arranjo`.

### 6.4 Confronto com o código real

Conforme.

O levantamento técnico do H-0023 confere com `tela/demo.py`:

- `_ler_tecla_sessao` usa `os.read(fd, 1)` bloqueante e `select` curto para
  sequências de escape;
- `main()` lê `shutil.get_terminal_size(fallback=(80, 24))` antes do ramo TTY;
- o ramo TTY atual não possui `SIGWINCH`, `ioctl`, wakeup pipe nem atualização
  reativa;
- `_apresentar_quadro` relê largura via `shutil.get_terminal_size`;
- `_iniciar_sessao_tui` usa `tty.setcbreak`, alternate screen, cursor oculto,
  autowrap off e `\x1b[2J` na entrada;
- `_encerrar_sessao_tui` restaura atributos, autowrap, cursor e alternate
  screen;
- o ramo não-TTY permanece separado e usa `print(..., end="")`;
- `renderizar_estado` já repassa `largura` e `altura` para `renderizar_tela`.

O levantamento também confere com `tela/renderizador.py`: `renderizar_tela`
aceita `altura`; quando suficiente, retorna exatamente `altura` linhas; e pode
levantar `RenderizadorErro` em largura/altura insuficiente ou chips que não
cabem.

## 7. Achados

### H23-QA-BLOQ-001 — Estado Git comprovado diverge do estado real

Severidade: bloqueante.

Evidência:

- H-0023 seção 2 lista como não rastreados apenas:
  `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`,
  `docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md`,
  `docs/relatorios/RELATORIO_QA_ADR-0017.md`,
  `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md`.
- `git status --short` real inclui também:
  `?? docs/handoff/H-0023-redimensionamento-reativo-tui.md`.
- H-0023 seção 24 determina parar com `BLOCKED_EVIDENCE` se o estado Git real
  divergir do estado comprovado na seção 2.

Impacto: um executor que siga o próprio handoff deve bloquear antes da
implementação. O handoff precisa ajustar o estado comprovado para refletir o
arquivo de handoff não rastreado, ou esclarecer explicitamente que a seção 2
representa o estado anterior à criação do H-0023. Sem isso, a etapa seguinte
fica contradita pelo próprio critério de bloqueio.

### H23-QA-MED-001 — Contradição interna sobre a ordem de criação do wakeup pipe

Severidade: média.

Evidência:

- H-0023 seção 13.2 afirma que `r_wakeup, w_wakeup = os.pipe()` é criado antes
  de `_iniciar_sessao_tui`.
- H-0023 seção 13.8 mostra a estrutura completa de `main()` com
  `_iniciar_sessao_tui(fd)` antes de `os.pipe()`.

Impacto: a ordem não parece alterar a decisão arquitetural principal, pois o
handler só é instalado depois da criação do pipe. Ainda assim, o handoff dá duas
instruções incompatíveis ao implementador em uma área sensível de restauração e
fechamento de recursos. Deve ser harmonizado no patch.

### H23-QA-MED-002 — Quadro mínimo com `"!"` pode não preservar significado inequívoco

Severidade: média.

Evidência:

- ADR-0017 exige aviso equivalente a "terminal pequeno demais" e permite
  adequar a formulação à largura disponível, preservando inequivocamente esse
  significado.
- H-0023 seção 17.2 define que, para largura menor que 9 e maior ou igual a 1,
  a mensagem será apenas `"!"`.
- H-0023 seção 19.3 transforma esse comportamento em teste obrigatório para
  `_quadro_minimo_aviso(5, 2)`.

Impacto: `"!"` cabe no terminal, mas não comunica inequivocamente "terminal
pequeno demais". O problema é especialmente relevante porque o handoff eleva
essa forma a critério de teste. Uma forma abreviada mais semântica para larguras
estreitas, ou uma justificativa explícita para o limite físico de representação,
deveria ser registrada.

### H23-QA-NOTA-001 — Teste por ocorrência textual do handler pode ser frágil

Severidade: nota.

Evidência: a seção 19.2 pede "inspecionar texto de `demo.py` para confirmar que
`_instalar_handler_sigwinch` aparece apenas dentro do bloco
`if sys.stdin.isatty()`".

Impacto: o nome da função necessariamente aparecerá na própria definição em
nível de módulo, fora do bloco TTY. O critério é recuperável se interpretado
como "chamadas a `_instalar_handler_sigwinch` aparecem apenas dentro do bloco
TTY", mas a redação literal pode produzir falso negativo em teste textual.

## 8. Não achados relevantes

- Não foi encontrada autorização para alterar arquivos fora de
  `tela/demo.py`, `tela/teste_demo.py` e o relatório de implementação esperado.
- Não foi encontrada autorização para modificar ADRs, contratos, nomenclatura,
  `config/`, `renderizador.py`, `loader.py` ou `modelo.py`.
- Não foi encontrada introdução de biblioteca de TUI, `terminfo` ou suporte
  Windows.
- Não foi encontrada autorização para repetir `\x1b[2J` por quadro ou por
  resize.
- Não foi encontrada autorização para alterar `corpo.arranjo`, `tiling`, chips
  ou presença declarativa de elementos.
- O status `ADR_APPLICATION_APPROVED_WITH_NOTES` foi encontrado no relatório
  `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0017.md`.

## 9. Testes

Não executei a suíte de testes nesta etapa. A auditoria de QA do handoff foi
documental e por inspeção de código/testes existentes, conforme o escopo
recebido. Também não realizei validação manual em TTY real.

## 10. Conclusão

O H-0023 é tecnicamente implementável e traduz a política central da ADR-0017,
mas não está pronto para implementação enquanto o achado bloqueante
H23-QA-BLOQ-001 permanecer aberto. Após patch documental do estado Git e
harmonização das notas acima, o handoff deve retornar a QA antes de qualquer
implementação.

## Próxima categoria permitida

```text
PATCH_HANDOFF
```

Nenhuma etapa posterior foi executada por este relatório.
