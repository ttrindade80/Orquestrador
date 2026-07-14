# Relatório de QA da Aplicação — ADR-0017

## 1. Identificação

```yaml
etapa: QA_APLICACAO_ADR
projeto: Orquestrador
adr: ADR-0017
data: 2026-07-11
artefato_principal: docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
```

## 2. Escopo

Auditoria formal da aplicação documental da ADR-0017, limitada a verificar se
os documentos alterados aplicam a decisão normativa aceita sem propagar os
achados do QA anterior e sem contrariar ADRs ou contratos ativos.

Fora do escopo respeitado: não foram corrigidos documentos avaliados, não foi
alterada a ADR-0017, não foram alterados contratos, código, testes, handoffs,
índice ou nomenclatura, e não houve stage, commit, push ou alteração de
histórico Git.

Este relatório é o único arquivo criado por esta etapa.

## 3. Estado Git Verificado

Estado verificado diretamente, não aceito apenas a partir do relatório de
aplicação:

```text
HEAD: de0f023 fix: corrige execução TTY em tela cheia
stage: vazio
```

`git status --short` mostrou:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0017-redimensionamento-reativo-tui.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md
?? docs/relatorios/RELATORIO_QA_ADR-0017.md
```

`git diff --stat` confirmou:

```text
4 files changed, 240 insertions(+), 21 deletions(-)
```

O resumo mecânico declarado pela etapa `APLICAR_ADR` confere com o estado
observado: quatro arquivos rastreados modificados, três arquivos não rastreados
relacionados ao ciclo, e stage vazio.

## 4. Autoridades Lidas

Lidos integralmente:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/relatorios/RELATORIO_QA_ADR-0017.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0017.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`

Consultados para contradições:

- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`

## 5. Verificação da Aplicação

### `docs/adr/INDICE_ADR.md`

Conforme. A ADR-0017 foi registrada como aceita, datada de 2026-07-11, com
menção a `SIGWINCH`, `ioctl(TIOCGWINSZ)`, cadeia de dimensões válidas, quadro
mínimo de aviso e relação complementar com ADR-0013 e ADR-0016.

### `docs/contratos/contrato_tela_json.md`

Conforme. A seção 23 preserva a política da ADR-0016 e direciona o
redimensionamento reativo para a nova seção 24. A seção 24 registra:

- aplicação somente em sessão TTY ativa e comportamento não-TTY preservado;
- `SIGWINCH` como gatilho;
- `ioctl(fd, TIOCGWINSZ, ...)` como fonte primária;
- par coerente de largura/altura, sem misturar fontes;
- validade apenas com largura e altura presentes, inteiras e maiores que zero;
- inicialização por `ioctl → LINES/COLUMNS → (80, 24)`;
- pós-`SIGWINCH` por `ioctl → LINES/COLUMNS → últimas dimensões válidas`;
- não aplicação de par inválido e não redesenho como mudança quando não há novo
  par válido;
- redesenho completo após novo par válido, para redução e ampliação;
- preservação de `corpo.arranjo`, `tiling`, chips e composição declarativa;
- quadro mínimo para terminal pequeno demais, sem nome de classe normativo;
- preservação da seção 23, incluindo protocolo de tela cheia, escrita atômica,
  synchronized output e não repetição de `\x1b[2J`;
- exclusão de Windows, `terminfo`, `ncurses`, `curses`, `textual` e `rich`.

### `docs/contratos/contrato_composicao_corpo.md`

Conforme. A aplicação registra a ADR-0017 nos metadados, referencia a cadeia de
dimensões na seção de ocupação vertical, preserva `corpo.arranjo` e `tiling`,
define terminal pequeno demais como quadro mínimo com recuperação automática,
e adiciona regras/critério de validação para:

- redimensionamento sem alteração de composição declarativa;
- recálculo de áreas, paginação e distribuições apenas com novo par válido;
- conservação das últimas dimensões válidas sem redesenho quando o par é
  inválido.

### `docs/NOMENCLATURA.md`

Conforme. A nomenclatura atualiza a data, expande o termo de
redimensionamento reativo e cria a seção 6.2 com termos específicos:
`SIGWINCH`, `ioctl(TIOCGWINSZ)`, `par de dimensões válido`, `últimas dimensões
válidas` e `quadro mínimo de terminal pequeno`.

As distinções terminológicas preservam `corpo.arranjo`, `tiling` e
`ocupacao_vertical_terminal` como conceitos independentes. O texto não cria
fallback de composição por dimensão.

## 6. Verificações Específicas Obrigatórias

### ADR17-QA-001

Resultado: conforme.

Os documentos aplicados não transformaram `RenderizadorErro` nem outra classe
concreta em requisito normativo. A busca por `RenderizadorErro` nos documentos
alterados não retornou ocorrência. `contrato_tela_json.md` declara
expressamente que nenhuma classe ou nome de exceção é normativo para o quadro
mínimo de terminal pequeno.

### ADR17-QA-002

Resultado: conforme.

Os documentos aplicados não autorizam redesenho usando dimensões antigas quando
`ioctl` e `LINES`/`COLUMNS` falham. A regra propagada é a decisória: conservar
as últimas dimensões válidas, não aplicar par inválido e não redesenhar como se
o tamanho tivesse mudado.

Busca por formulações como "redesenho pode ocorrer com as dimensões" ou
"redesenhar estado anterior" nos documentos alterados não encontrou propagação
da frase ambígua da seção de riscos da ADR-0017.

## 7. Compatibilidade com ADR-0013 e ADR-0016

Conforme.

A aplicação complementa a ADR-0013 ao tratar largura e altura como dimensões da
janela do terminal, sem colapsar `ocupacao_vertical_terminal` com
`corpo.arranjo`.

A aplicação preserva a ADR-0016: sessão apenas com stdin/stdout TTY, `cbreak`
em vez de `raw`, `ISIG` e `OPOST`, alternate screen, cursor oculto, autowrap
desativado, posicionamento absoluto, preenchimento até a largura atual, escrita
atômica com um flush por quadro, synchronized output, `\x1b[2J` apenas na
entrada, restauração em `finally`, política de Ctrl+C e comportamento não-TTY.

## 8. Contradições Consultivas

Não foram encontradas contradições bloqueantes em:

- `contrato_estilo.md`: preserva `tiling` como escolha/preferência não forçada
  por largura de terminal.
- `contrato_barra_de_menus.md`: mantém chips declarativos, não inventados e
  não reordenados por largura; detalhes específicos da barra permanecem no
  contrato próprio.
- `contrato_lancador.md`: mantém cálculo visual por largura real sem alterar
  composição declarada.
- `contrato_console.md`: mantém paginação, colunas e estado de runtime no
  escopo da instância declarada; não contradiz a cadeia de dimensões.
- `contrato_processo_desenvolvimento.md`: a aplicação respeita a autoridade de
  ADRs aceitas acima de contratos de módulo e não iniciou etapa posterior.

## 9. Achados

Nenhum achado bloqueante.

Nenhuma correção é exigida para a aplicação documental da ADR-0017 nesta etapa
de QA.

Observação não bloqueante: `contrato_composicao_corpo.md` resume a cadeia como
`ioctl(TIOCGWINSZ) → LINES/COLUMNS → fallback ou últimas dimensões válidas`.
O detalhamento normativo correto está delegado a `contrato_tela_json.md` seção
24, que distingue inicialização de sessão pós-`SIGWINCH`. Como a delegação está
explícita e as regras R-24/critério de validação repetem a conservação correta,
isso não constitui contradição.

## Status final

ADR_APPLICATION_APPROVED_WITH_NOTES

Justificativa: a aplicação documental cobre os artefatos previstos pela
ADR-0017, preserva ADR-0013 e ADR-0016, não propaga os achados anteriores,
mantém o escopo documental e não introduz contradição normativa bloqueante.

## Próxima categoria permitida

RETOMAR_OU_RECRIAR_HANDOFF

Nenhuma etapa posterior é executada por este relatório.
