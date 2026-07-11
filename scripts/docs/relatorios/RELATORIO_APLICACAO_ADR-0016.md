# Relatório de Aplicação da ADR-0016

## 1. Identificação

```yaml
etapa: APLICAR_ADR
projeto: Orquestrador
ciclo: H-0022 / ADR-0016
data: 2026-07-11
```

## 2. Versão da ADR aplicada

```text
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 215
sha256: afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7
status: aceita
```

## 3. Relatório de QA autorizador

```text
docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
```

Usado somente como evidência de aprovação da ADR para aplicação documental.

## 4. Arquivos alterados

```text
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
```

## 5. Seções adicionadas ou modificadas

- `docs/adr/INDICE_ADR.md`: entrada da ADR-0016 atualizada para status
  `aceita`.
- `docs/contratos/contrato_tela_json.md`: adicionada a seção
  `## 23. Execução TTY da sessão TUI (ADR-0016)`; seções posteriores
  renumeradas.
- `docs/contratos/contrato_console.md`: adicionada a seção
  `## 10. Ctrl+C em execução interna (ADR-0016)`; seções posteriores
  renumeradas.
- `docs/contratos/contrato_processo_desenvolvimento.md`: adicionada a seção
  `## 7. Precedente de violação dupla do ciclo`; seções posteriores
  renumeradas.
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md`: criado este relatório de
  aplicação.

## 6. Decisões propagadas

- Índice registra a ADR-0016 como aceita.
- `contrato_tela_json.md` registra a política de execução TTY da ADR-0016:
  ativação somente com stdin/stdout TTY, `cbreak`, preservação de `OPOST` e
  `ISIG`, alternate screen, cursor, autowrap/DECAWM, posicionamento absoluto,
  preenchimento de linhas, escrita atômica, limpeza inicial única,
  synchronized output, Ctrl+C escopado, restauração em `finally`, preservação
  não-TTY e limites fora de escopo.
- `contrato_console.md` registra somente o recorte de Ctrl+C/`KeyboardInterrupt`
  do item 9 da ADR-0016 para execução interna futura.
- `contrato_processo_desenvolvimento.md` registra o precedente processual de
  `IMP-0022` como violação dupla do ciclo padrão: implementação sem ADR
  precedente e sem handoff precedente.

## 7. Decisões explicitamente não propagadas

- `contrato_tela_json.md`: não foram propagados SIGWINCH, reserva de handoff
  futuro, `terminfo`, Windows, `curses`, `textual`, `rich`, política nova de
  navegação por setas ou detalhes derivados de código.
- `contrato_console.md`: não foram propagados os itens 1-8, 10 ou 11 como
  política própria do console; regras de renderização terminal, escape codes,
  buffer, refresh, alternate screen, autowrap e desenho de quadro foram
  mantidas fora deste contrato.
- `contrato_processo_desenvolvimento.md`: não foi propagada cronologia extensa,
  lista de ferramentas, atribuição pessoal de culpa, regra por nome de agente
  ou aprovação de handoff/implementação.

## 8. Resultado das verificações locais

```text
git diff --check
resultado: sem saída

rg -n 'ADR-0016|execução TTY|sessão TUI|cbreak|setraw|OPOST|ISIG|alternate screen|DECAWM|2026h|2026l|KeyboardInterrupt|IMP-0022|H-0023|SIGWINCH' \
  docs/adr/INDICE_ADR.md \
  docs/contratos/contrato_tela_json.md \
  docs/contratos/contrato_console.md \
  docs/contratos/contrato_processo_desenvolvimento.md
resultado: termos localizados nos pontos aplicados; H-0023 e SIGWINCH não aparecem.
```

Inspeção textual registrada:

- `setraw` aparece apenas como comportamento rejeitado.
- `H-0023` não foi reservado.
- `contrato_console.md` não recebeu a política completa de renderização.
- `contrato_processo_desenvolvimento.md` contém regra processual curta e
  referência histórica a `IMP-0022`.

## 9. Estado Git observado

Antes da aplicação:

```text
branch: master
HEAD: 0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf
status: havia alterações pré-existentes em índice, código, ADR, handoff e relatórios históricos não alterados por esta etapa.
```

Após a aplicação:

```text
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
 M tela/demo.py
 M tela/teste_demo.py
?? docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
?? docs/handoff/H-0022-correcao-execucao-tela-cheia-tty.md
?? docs/relatorios/IMP-0022-controle-tela-cheia-terminal-sem-echo.md
?? docs/relatorios/IMP-0023-implementacao-h0022-tela-cheia-tty.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
?? docs/relatorios/RELATORIO_AUDITORIA_ADR-0016.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_CONSISTENCIA_H-0022.md
?? docs/relatorios/RELATORIO_QA_ADR-0016_POS_AJUSTES.md
?? docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
?? docs/relatorios/RELATORIO_QA_H-0022_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0022_IMPLEMENTACAO.md
```

## 10. Confirmação de escopo

Nenhum arquivo fora do escopo permitido foi alterado por esta etapa. As
alterações pré-existentes em código, handoff, ADR e relatórios históricos
foram preservadas sem edição.

## 11. Pendência

```text
QA_APLICACAO_ADR
```
