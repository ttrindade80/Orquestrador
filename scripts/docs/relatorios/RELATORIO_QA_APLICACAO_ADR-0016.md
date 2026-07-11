# Relatório de QA da Aplicação da ADR-0016

## 1. Identificação da etapa

```yaml
etapa: QA_APLICACAO_ADR
projeto: Orquestrador
ciclo: H-0022 / ADR-0016
data: 2026-07-11
relatorio_criado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0016.md
```

Este relatório audita somente a aplicação documental da ADR-0016. Não corrige
documentos, não altera contratos, não altera ADR, não altera handoff, não lê
código como autoridade normativa, não prepara commit e não executa etapa
posterior.

## 2. Versão da ADR aplicada

Comandos obrigatórios executados antes da auditoria:

```text
wc -l docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
215 docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md

sha256sum docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7  docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
```

Versão auditada:

```yaml
arquivo: docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
linhas: 215
sha256: afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7
status: aceita
```

## 3. Relatórios de autoridade e execução

Relatório de QA autorizador lido integralmente:

```text
docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
```

Evidência: o relatório autoriza a ADR-0016 corrigida para aplicação documental
após validar a versão de 215 linhas e SHA-256
`afa961fc63d56a02108a8a5b30b8af4ee25668587d0a7907c00e42b824d8faa7`
(linhas 19-32) e conclui `QA_ADR_APROVADO` (linhas 241-250).

Relatório de aplicação lido integralmente:

```text
docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
```

Verificação do relatório de aplicação:

| Item obrigatório | Resultado | Evidência |
|---|---|---|
| etapa `APLICAR_ADR` | conforme | linhas 3-10 |
| versão e hash corretos da ADR | conforme | linhas 12-19 |
| referência ao QA autorizador | conforme | linhas 21-28 |
| lista dos arquivos alterados | conforme como declaração do executor | linhas 29-37 |
| seções modificadas | conforme | linhas 39-53 |
| decisões propagadas | conforme | linhas 55-68 |
| decisões não propagadas | conforme | linhas 70-81 |
| verificações locais | conforme como declaração do executor | linhas 83-103 |
| estado Git | conforme como declaração do executor, com limitação de proveniência | linhas 105-135 |
| pendência de `QA_APLICACAO_ADR` | conforme | linhas 143-147 |
| ausência de autoaprovação | conforme | não há status de aprovação da própria aplicação |

## 4. Documentos e versões auditados

Lidos integralmente:

```text
docs/adr/ADR-0016-execucao-tela-cheia-tty-sem-cintilacao.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/relatorios/RELATORIO_QA_ADR-0016_POS_PATCH.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
```

Lidos por necessidade limitada de renumeração/referências:

```text
docs/INDICE.md
docs/build_docs/to_do.md
docs/relatorios/anexos/orquestrador_stub_b_validacao.json
```

## 5. Matriz da aplicação

### Índice de ADRs

Resultado: conforme.

- ADR-0016 aparece exatamente uma vez em `docs/adr/INDICE_ADR.md`, linha 46.
- Caminho implícito, número, título, data e status estão coerentes com a ADR:
  `ADR-0016`, "Execução em tela cheia (TTY) sem cintilação, com Ctrl+C escopado",
  `aceita`, `2026-07-10`.
- O formato é coerente com as entradas ADR-0001 a ADR-0015.
- Não foi encontrada entrada concorrente de ADR-0016 como `proposta`.

### Contrato de tela JSON

Resultado geral: propagado fielmente, sem omissão material.

```text
item_adr: 1. Guarda dupla de TTY
linhas_adr: 73-75
linhas_contrato: 655-659, 663
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 2. cbreak, não raw
linhas_adr: 77-80
linhas_contrato: 664-666
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 3. Preservação de OPOST e ISIG
linhas_adr: 77-80, 117-119
linhas_contrato: 664-665, 683
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 4. Alternate screen e cursor
linhas_adr: 82-85
linhas_contrato: 667-670
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 5. DECAWM desativado/restaurado
linhas_adr: 87-90
linhas_contrato: 671-672
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 6. Posicionamento absoluto linha a linha
linhas_adr: 92-96
linhas_contrato: 673-674
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 7. Preenchimento até a largura
linhas_adr: 98-102
linhas_contrato: 675-676
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 8. Única write e flush por quadro; limpeza única na entrada
linhas_adr: 104-109
linhas_contrato: 677-680
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 9. Synchronized output por atualização
linhas_adr: 111-115
linhas_contrato: 681-682
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 10. Ctrl+C escopado e restauração não imediata
linhas_adr: 117-134
linhas_contrato: 683-693
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma

item_adr: 11. Comportamento não-TTY preservado e limites
linhas_adr: 136-138, 190-201
linhas_contrato: 657-659, 694-699
resultado: PROPAGADO_FIELMENTE
omissao: nenhuma
ampliacao: nenhuma
contradicao: nenhuma
```

Verificações específicas:

- Ctrl+C durante futura execução interna: propagado em `contrato_tela_json.md`,
  linhas 683-686.
- Ctrl+C ignorado no restante do loop: propagado nas linhas 687-690.
- Distinção entre Ctrl+C ignorado e execução do `finally`: propagada nas linhas
  689-693.
- Restauração quando o loop efetivamente termina: propagada nas linhas 691-693.
- Comportamento não-TTY: propagado nas linhas 657-659.
- Limites e fora de escopo: propagados nas linhas 694-699.
- "navegação por setas" aparece em `contrato_tela_json.md` linhas 697-699 como
  exclusão de escopo fora das regras já contratadas. A autoridade correspondente
  é `contrato_console.md` seção 7, linhas 210-230, que já normatiza `[✥]` e
  setas do teclado. Não foi classificada como ampliação documental.

### Contrato do console

Resultado geral: recorte do item 9 propagado corretamente; há defeito de
renumeração interna em referências preexistentes.

Conforme:

- `ISIG` habilitado: linhas 284-289.
- Captura local de `KeyboardInterrupt` em futura execução interna: linhas
  286-289.
- Interrupção somente da execução interna e permanência da sessão TUI: linhas
  288-289.
- Ctrl+C ignorado fora desse escopo: linhas 291-292.
- Esc como saída normatizada: linhas 291-292.
- Mecanismo permitido antes de fluxo real e proibição de inventar fluxo apenas
  para consumi-lo: linhas 293-294.
- Política completa de renderização terminal não foi transferida para este
  contrato: linhas 296-298.
- A seção de pendências fora de escopo preserva que renderização final em
  terminal, caracteres, cores, escape codes e chamadas de sistema não pertencem
  ao contrato do console: linhas 486-510.

Não conformidade corrigível:

- `politica_paginacao` e `politica_quebra` continuam apontando "Ver seção 11"
  nas linhas 99 e 135. Após a inserção de `## 10. Ctrl+C em execução interna`,
  a paginação passou para `## 12. Paginação` nas linhas 324-348. Essas
  referências internas ficaram desatualizadas.

### Contrato de processo

Resultado: conforme.

- Implementação sem ADR como violação: linhas 66-69.
- Implementação sem handoff como violação: linhas 68-70.
- Ocorrência simultânea como violação dupla: linhas 72-76.
- Interrupção da aceitação: linhas 72-74.
- Exigência de ADR, handoff e QAs separados: linhas 72-76.
- Implementação e autoavaliação juntas não substituem QA: linhas 75-76.
- `IMP-0022` citado somente como precedente histórico: linha 78.
- Não há atribuição de culpa pessoal, regra dependente de ferramenta/chat ou
  narrativa extensa que transforme o contrato em relatório.
- A nova regra é compatível com ciclo, autoridade e bloqueio preexistentes
  (`contrato_processo_desenvolvimento.md`, linhas 19-39, 50-64 e 97-108).

## 6. Verificação da renumeração

Sequência interna de seções:

| Documento | Resultado |
|---|---|
| `contrato_tela_json.md` | sequência 1-28 sem salto ou duplicação após inserção da seção 23 |
| `contrato_console.md` | sequência 1-18 sem salto ou duplicação após inserção da seção 10 |
| `contrato_processo_desenvolvimento.md` | sequência 1-12 sem salto ou duplicação após inserção da seção 7 |

Referências internas e externas:

- `contrato_console.md`, linhas 99 e 135: referências internas desatualizadas
  para "Ver seção 11"; deveriam apontar para a seção 12 após a renumeração.
- `docs/relatorios/anexos/orquestrador_stub_b_validacao.json`, linha 58,
  contém referência histórica/anexa a `contrato_console.md secao 12`; não foi
  atribuída automaticamente à aplicação e não foi classificada como defeito
  ativo do contrato principal nesta auditoria.
- Referências em handoffs e relatórios históricos foram tratadas como contexto
  histórico, não como norma ativa, salvo quando apontam para documentos
  normativos atuais.

## 7. Contradições e resíduos

Buscas contextuais executadas nos documentos aplicados e contratos diretamente
relacionados para:

```text
ADR-0016
proposta
aceita
IMP-0022
H-0022
H-0023
SIGWINCH
setraw
raw
cbreak
OPOST
ISIG
KeyboardInterrupt
finally
alternate screen
DECAWM
2026h
2026l
navegação por setas
```

Classificação:

| Termo/resíduo | Classificação | Evidência |
|---|---|---|
| ADR-0016 aceita no índice | norma ativa correta | `INDICE_ADR.md`, linha 46 |
| `raw` / `tty.setraw()` | comportamento rejeitado | `contrato_tela_json.md`, linhas 664-666 |
| `cbreak`, `OPOST`, `ISIG` | norma ativa correta | `contrato_tela_json.md`, linhas 664-665 e 683 |
| `KeyboardInterrupt` | norma ativa correta | `contrato_tela_json.md`, linhas 683-688; `contrato_console.md`, linhas 286-292 |
| `finally` | norma ativa correta | `contrato_tela_json.md`, linhas 691-693 |
| alternate screen / cursor / DECAWM | norma ativa correta em tela JSON; exclusão correta no console | `contrato_tela_json.md`, linhas 667-672; `contrato_console.md`, linhas 296-298 |
| `2026h` / `2026l` | norma ativa correta | `contrato_tela_json.md`, linhas 681-682 |
| limpeza `\x1b[2J` | norma ativa correta, única na entrada | `contrato_tela_json.md`, linhas 679-680 |
| `IMP-0022` | referência histórica correta | `contrato_processo_desenvolvimento.md`, linha 78 |
| `SIGWINCH` e `H-0023` | ausentes como norma ativa nos contratos aplicados; aparecem no relatório de aplicação como decisões não propagadas/verificação | `RELATORIO_APLICACAO_ADR-0016.md`, linhas 72-74 e 94-100 |
| "navegação por setas" | ocorrência relacionada e não ampliativa | `contrato_tela_json.md`, linhas 697-699; autoridade em `contrato_console.md`, linhas 210-230 |

Não foram encontradas, como norma ativa nos documentos aplicados:

- política concorrente de `raw`;
- Ctrl+C encerrando a sessão;
- limpeza de tela por quadro;
- autowrap ativo durante a sessão;
- múltiplas escritas normatizadas por quadro;
- H-0023 reservado;
- SIGWINCH incluído neste ciclo;
- política TTY completa atribuída ao console;
- IMP-0022 tratado como norma vigente;
- ADR-0016 registrada como proposta.

## 8. Ausência de implementação indevida

O relatório de aplicação declara que a etapa `APLICAR_ADR` alterou somente os
cinco arquivos previstos (`RELATORIO_APLICACAO_ADR-0016.md`, linhas 29-37) e
que alterações em código, handoff, ADR e relatórios históricos eram
preexistentes e foram preservadas (`RELATORIO_APLICACAO_ADR-0016.md`, linhas
137-141).

Evidência factual atual:

```text
git diff --name-only
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_console.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/contratos/contrato_tela_json.md
scripts/tela/demo.py
scripts/tela/teste_demo.py
```

Conclusão de proveniência: `NAO_CONFIRMADO` para código e testes. O workspace
já está sujo e há declaração explícita do relatório de aplicação de que essas
mudanças eram preexistentes; esta auditoria não encontrou evidência suficiente
para atribuí-las à aplicação documental.

Não foi encontrada evidência de schema executável criado, modificação de
`config/`, declaração de implementação/QA aprovados, fechamento, stage ou
commit pela etapa auditada.

## 9. Estado Git

Confirmação no início desta auditoria:

```text
branch: master
HEAD: 0b09fa6a99a6d0ed61e9488ecb7e78f16d37cfdf
```

`git status --short` antes da criação deste relatório:

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

`git diff --check`: sem saída.

`git diff --stat`:

```text
scripts/docs/adr/INDICE_ADR.md                     |   1 +
scripts/docs/contratos/contrato_console.md         |  34 +-
scripts/docs/contratos/contrato_processo_desenvolvimento.md |  24 +-
scripts/docs/contratos/contrato_tela_json.md       |  60 ++-
scripts/tela/demo.py                               | 200 ++++++--
scripts/tela/teste_demo.py                         | 525 ++++++++++++++++++++-
6 files changed, 783 insertions(+), 61 deletions(-)
```

Arquivos permitidos para a aplicação:

```text
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
```

Arquivos confirmados no diff atual e permitidos:

```text
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_processo_desenvolvimento.md
```

Arquivo criado nesta auditoria:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0016.md
```

Stage: não há evidência de arquivos staged no `git status --short`.

## 10. Achados por severidade

### Médios

```text
id: QA-APL-ADR16-MED-001
severidade: médio
arquivo: docs/contratos/contrato_console.md
linhas: 99, 135, 324
evidencia: as linhas 99 e 135 referenciam "Ver seção 11" para paginação/quebra de página; após a inserção da seção 10, "Paginação" está na seção 12, iniciada na linha 324.
regra_da_adr_ou_contrato: a aplicação declarou renumerar seções posteriores em RELATORIO_APLICACAO_ADR-0016.md, linhas 46-48; o prompt de QA exige verificar referências internas a números de seção.
impacto: referência normativa interna aponta para "Filtros" em vez de "Paginação", prejudicando rastreabilidade e leitura correta do contrato.
correcao_necessaria: atualizar as duas referências internas para apontarem à seção 12.
exige_decisao_do_usuario: não
```

### Observações

```text
id: QA-APL-ADR16-OBS-001
severidade: observação
arquivo: estado Git
linhas: n/a
evidencia: git diff atual inclui tela/demo.py e tela/teste_demo.py, enquanto RELATORIO_APLICACAO_ADR-0016.md declara que alterações em código eram preexistentes.
regra_da_adr_ou_contrato: escopo da aplicação documental limitado a índice, contratos e relatório de aplicação.
impacto: proveniência de código/testes permanece NAO_CONFIRMADO por workspace previamente sujo; não há evidência suficiente para atribuir essas alterações à aplicação.
correcao_necessaria: nenhuma nesta auditoria; preservar a limitação de proveniência em etapas posteriores.
exige_decisao_do_usuario: não
```

Não há achados bloqueantes, altos ou baixos.

## 11. Quadro final

```yaml
indice:
  resultado: conforme
  pendencias: []

contrato_tela_json:
  cobertura_itens_1_11: completa
  omissoes: []
  ampliacoes: []
  contradicoes: []

contrato_console:
  somente_item_9: conforme
  omissoes: []
  ampliacoes: []
  contradicoes: []
  defeitos_corrigiveis:
    - referencias internas desatualizadas para secao 11 onde a paginacao passou a ser secao 12

contrato_processo:
  precedente_processual: conforme
  omissoes: []
  ampliacoes: []
  contradicoes: []

relatorio_aplicacao:
  completo: sim
  autoaprovacao: ausente
  inconsistencias: []

escopo:
  arquivos_previstos:
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
  arquivos_confirmados:
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0016.md
  arquivos_externos:
    - tela/demo.py
    - tela/teste_demo.py
  limitacoes_de_proveniencia:
    - alteracoes em codigo/testes constam no diff atual, mas o relatorio de aplicacao as declara preexistentes; classificacao NAO_CONFIRMADO
```

## 12. Arquivos alterados nesta auditoria

Somente:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0016.md
```

## 13. Status final

```text
ADR_APPLICATION_REJECTED
```

Justificativa: a aplicação é materialmente fiel à ADR-0016 no índice e nas
novas seções normativas, mas deixou duas referências internas do
`contrato_console.md` apontando para seção renumerada incorreta. O defeito é
corrigível usando a ADR já aprovada e não exige nova decisão material.

## 14. Próxima categoria

```text
PATCH_DOCUMENTACAO
```
