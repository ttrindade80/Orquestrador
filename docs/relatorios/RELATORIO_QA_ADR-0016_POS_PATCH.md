# Relatório de QA da ADR-0016 pós-PATCH_ADR

## 1. Identificação

```yaml
etapa: QA_ADR
projeto: Orquestrador
ciclo: H-0022 / ADR-0016
data: 2026-07-11
arquivo_auditado: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
relatorio_criado: docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
escopo: auditoria formal da ADR-0016 corrigida
```

Este relatório audita somente a versão corrigida da ADR-0016. Não corrige a
ADR, não aplica a decisão a contratos ou índice, não audita handoff, não audita
implementação, não altera relatórios históricos e não prepara commit.

## 2. Evidência de versão

Comandos exigidos antes da auditoria:

```text
wc -l docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
215 docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md

sha256sum docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7  docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
```

A versão auditada corresponde exatamente à versão autorizada para esta etapa:
215 linhas e SHA-256 `afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7`.

## 3. Estado Git Observado

```text
branch: master
HEAD: 0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf
```

Estado antes da criação deste relatório:

```text
 M docs/adr/INDICE_ADR.md
 M tela/demo.py
 M tela/teste_demo.py
?? docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
?? docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
?? docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
?? docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md
?? docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_CONSISTENCIA_H-0022.md
?? docs/relatorios/RELATORIO_QA_ADR-0016_POS_AJUSTES.md
?? docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md
```

O estado sujo já existia antes desta etapa. Nenhum arquivo foi alterado por
este QA além do relatório presente.

## 4. Autoridade Aplicada

A autoridade principal desta auditoria é a decisão explícita do usuário
reproduzida no prompt de execução de 2026-07-11. Essa decisão aprova o conteúdo
normativo da ADR-0016 e cobre expressamente:

- ativação TUI somente com stdin e stdout TTY;
- modo `cbreak`, preservando `OPOST` e `ISIG`;
- alternate screen, cursor ocultado/restaurado e autowrap restaurado;
- posicionamento absoluto linha a linha, preenchimento até a largura e escrita
  atômica por quadro;
- limpeza de tela uma única vez na entrada;
- synchronized output em cada quadro;
- Ctrl+C preservado por `ISIG`, capturado localmente em execução futura de
  script/processo interno, e ignorado silenciosamente no restante do loop;
- restauração protegida por `finally`;
- preservação não-TTY;
- itens fora de escopo;
- risco aceito de Esc permanecer como única saída normatizada.

O bloqueio histórico `BLOCKED_USER_DECISION` de
`RELATORIO_QA_ADR-0016_POS_AJUSTES.md` foi correto no momento em que foi
emitido e foi superado por essa decisão posterior. O relatório histórico não
foi alterado.

## 5. Documentos Lidos

Lidos integralmente para esta auditoria:

- `docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md`;
- `docs/relatorios/RELATORIO_QA_ADR-0016_POS_AJUSTES.md`;
- `docs/relatorios/RELATORIO_LEVANTAMENTO_CONSISTENCIA_H-0022.md`;
- `docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md`;
- `docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md`;
- `docs/contratos/contrato_tela_json.md`;
- `docs/contratos/contrato_console.md`;
- `docs/contratos/contrato_processo_desenvolvimento.md`;
- `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`;
- `docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md`;
- `docs/adr/ADR-0001-menu-suporta-matriz.md`;
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`;
- `docs/adr/INDICE_ADR.md`.

As ADRs aceitas ADR-0001 e ADR-0013 foram usadas somente para verificar
convenção estrutural e coerência de status.

## 6. Verificações Obrigatórias

### 6.1 Correspondência com a decisão

Resultado: **conforme**.

A seção `Decisão` da ADR-0016 possui 11 itens nas linhas 71-138 e corresponde
à decisão explícita do usuário:

- item 1: TUI somente com `sys.stdin.isatty() and sys.stdout.isatty()`;
- item 2: `cbreak`, não `raw`, com preservação de `OPOST` e `ISIG`;
- itens 3-4: alternate screen, cursor e autowrap;
- itens 5-8: posicionamento absoluto, preenchimento, escrita atômica, limpeza
  inicial única e synchronized output;
- itens 9-10: Ctrl+C escopado e restauração por `finally`;
- item 11: comportamento não-TTY preservado.

Não foi identificada omissão relevante da decisão explícita, acréscimo de
alternativa não aprovada, transformação de código em autoridade, nem ampliação
indevida para SIGWINCH, Windows, terminfo ou bibliotecas proibidas.

### 6.2 Status e rastreabilidade

Resultado: **conforme**.

- Frontmatter: `metadata.status: aceita` na linha 6.
- Corpo: seção `## Status` com literal `aceita` na linha 25.
- Ambos são coerentes e decorrem da decisão explícita do usuário, não de
  autoaprovação da ADR.
- `handoffs_bloqueados` é estrutural e aponta o H-0022 atual nas linhas 17-18.
- H-0022 é mencionado como criado posteriormente, sem aprovação automática do
  handoff ou da implementação, nas linhas 154-158.
- IMP-0022 é mantido como evidência histórica e tentativa supersedida nas
  linhas 144-148 e 177-178.
- Não há instrução para criar outro handoff.
- Não há reserva antecipada de número para SIGWINCH; a ADR declara que não há
  número reservado nas linhas 186-188 e 192-196.

### 6.3 Temporalidade do contexto

Resultado: **conforme**.

A ADR distingue:

- a tentativa anterior sem ADR e sem handoff formal precedente nas linhas
  37-48;
- a criação posterior do H-0022 nas linhas 154-158;
- o estado presente em que H-0022 existe, mas não é automaticamente aprovado
  pela ADR, nas linhas 154-158 e 181-185.

Foram procurados resíduos de afirmações presentes falsas. A versão auditada
não contém as formulações bloqueantes `não existe handoff H-0022`, `Nenhum
handoff H-0022`, `abrir um handoff novo` ou `próximo número livre`.

### 6.4 Itens 9 e 10

Resultado: **conforme**.

A ADR agora distingue corretamente:

- Ctrl+C durante execução futura de script/processo interno: captura local de
  `KeyboardInterrupt`, interrupção apenas do escopo interno e permanência da
  sessão TUI, linhas 121-123;
- Ctrl+C fora desse escopo: captura e ignorância silenciosa, com a sessão ativa
  e Esc como saída normatizada, linhas 124-126;
- proteção lexical do loop completo por `finally`, linhas 128-131;
- execução efetiva do `finally` apenas quando o loop termina por Esc ou por
  exceção não tratada, linhas 131-134.

A redação não sugere mais que o mesmo Ctrl+C seja simultaneamente ignorado e
cause encerramento/restauração imediata.

### 6.5 Consequências e aplicação futura

Resultado: **conforme**.

A ADR identifica como aplicação posterior:

- `docs/adr/INDICE_ADR.md`;
- `docs/contratos/contrato_tela_json.md`;
- `docs/contratos/contrato_console.md`;
- `docs/contratos/contrato_processo_desenvolvimento.md`.

A ausência atual da política nos contratos e o índice ainda não atualizado são
aplicação pendente de etapa futura `APLICAR_ADR`, não defeitos desta ADR e não
evidência de aplicação prematura. Nenhum desses arquivos foi alterado nesta
etapa.

## 7. Convenção Estrutural

Resultado: **conforme**.

Comparada a ADRs aceitas, a ADR-0016 preserva a convenção essencial:

- frontmatter com `metadata.type: adr`, `metadata.status`, `data` e
  `substitui`;
- rastreabilidade com `issues_relacionadas`, `contratos_afetados` e
  `handoffs_bloqueados`;
- título, `## Status`, `## Data`, `## Contexto`, `## Decisão`,
  `## Consequências` e `## Alternativas consideradas`;
- status literal coerente entre frontmatter e corpo.

O uso de `handoffs_bloqueados` com um caminho existente é aceitável nesta ADR,
pois indica o handoff dependente/bloqueado pela regularização documental e não
ordena a criação de novo handoff.

## 8. Aplicação Pendente

Os seguintes fatos devem permanecer registrados como pendências de aplicação,
não como rejeição da ADR:

- `docs/adr/INDICE_ADR.md` ainda registra ADR-0016 como `proposta`;
- os três contratos afetados ainda não incorporam a política normativa da
  ADR-0016;
- H-0022, implementação e QAs próprios não são aprovados por este relatório.

Esses pontos pertencem a etapas posteriores explicitamente fora do escopo
deste QA.

## 9. Achados

Nenhum achado bloqueante, alto, médio ou baixo foi identificado na versão
auditada.

Observação não bloqueante:

```text
id: QA-ADR16-POSPATCH-OBS-01
tipo: aplicacao_pendente
evidencia: docs/adr/INDICE_ADR.md e contratos afetados ainda não refletem a ADR-0016 aceita.
impacto: nenhum para a aprovação da ADR nesta etapa; a aplicação pertence a APLICAR_ADR.
acao: executar etapa posterior autorizada de aplicação e QA próprio.
```

## 10. Status Final

```text
QA_ADR_APROVADO
```

A ADR-0016 corrigida está aprovada para seguir para a etapa posterior de
aplicação documental, quando autorizada. Esta conclusão não aprova o handoff
H-0022, a implementação, relatórios posteriores, fechamento do ciclo, commit,
numeração do IMP-0023 ou início de qualquer nova etapa.

## 11. Arquivos Alterados Nesta Etapa

Somente:

```text
docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
```
