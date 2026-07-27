---
name: relatorio-qa-aplicacao-adr-0031
description: QA independente da aplicacao documental da ADR-0031 — navegacao simples e selecao unica em console de nivel unico
metadata:
  type: relatorio_qa
  etapa: QA_APLICACAO_ADR
  adr: ADR-0031
  item_de_backlog: ITEM-0002
  status: ADR_APPLICATION_QA_REJECTED
---

# Relatorio de QA da Aplicacao Documental — ADR-0031

## 1. Identificacao

```yaml
etapa: QA_APLICACAO_ADR
adr: ADR-0031
item_de_backlog: ITEM-0002
objeto: docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
adr_avaliada: docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
relatorio_criado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
data: 2026-07-25
```

## 2. Objeto e escopo

Este QA avaliou independentemente a aplicacao documental da ADR-0031 nos contratos, modulos de nomenclatura, indice e backlog declarados pela aplicacao.

O QA nao avaliou implementacao, nao leu conteudo de handoff, nao criou handoff, nao aplicou correcao, nao executou stage e nao executou commit.

## 3. Estado inicial

```yaml
adr: ADR-0031
item_de_backlog: ITEM-0002
qa_semantico_da_adr: ADR_QA_APPROVED_WITH_NOTES
aplicacao_documental: CONCLUIDA
qa_da_aplicacao: PENDENTE
implementacao: NAO_INICIADA
handoff: NAO_CRIADO
stage: VAZIO
commit_executado: nao
relatorio_qa_aplicacao_preexistente: nao
```

Gate inicial:

| Check | Resultado |
|---|---|
| ADR-0031 existe | PASSOU |
| `RELATORIO_QA_ADR-0031.md` existe | PASSOU |
| QA da ADR terminou como `ADR_QA_APPROVED_WITH_NOTES` | PASSOU |
| QA da ADR sem achados bloqueantes, maiores ou menores | PASSOU |
| `RELATORIO_APLICACAO_ADR-0031.md` existe | PASSOU |
| Stage vazio | PASSOU |
| `RELATORIO_QA_APLICACAO_ADR-0031.md` ainda nao existia | PASSOU |

## 4. Arquivos consultados

Leitura integral obrigatoria realizada:

```text
docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
docs/relatorios/RELATORIO_QA_ADR-0031.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
docs/backlog.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
docs/nomenclatura/32_CONSOLE.md
docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
```

Os levantamentos foram tratados como documentos de referencia opcional e nao foram necessarios para decidir os achados materiais deste QA.

## 5. Metodo

1. Conferencia do gate inicial e do stage.
2. Leitura integral dos documentos obrigatorios.
3. Execucao dos checks de estado material: `git status --short --untracked-files=all`, `git diff --cached --check`, `git diff --check`, `git diff --name-only` e `git diff --stat`.
4. Exame do diff completo de cada arquivo rastreado modificado.
5. Conferencia direta do diff de `contrato_tela_json.md` por `numstat`.
6. Comparacao entre ADR, relatorio de aplicacao, documentos alterados e criterios D1-D15.
7. Registro de achados sem aplicar correcao.

## 6. Estado material e diffs

Estado material observado antes da criacao deste relatorio:

```text
 M docs/adr/INDICE_ADR.md
 M docs/backlog.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_chip.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_tela_json.md
 M docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
 M docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
 M docs/nomenclatura/32_CONSOLE.md
 M docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
?? docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
?? docs/relatorios/RELATORIO_QA_ADR-0031.md
```

Checks de diff antes da criacao deste relatorio:

```yaml
git_diff_cached_check: PASSOU
git_diff_check: PASSOU
git_diff_name_only:
  - docs/adr/INDICE_ADR.md
  - docs/backlog.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
  - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
git_diff_stat: "12 files changed, 494 insertions(+), 36 deletions(-)"
```

`docs/contratos/contrato_tela_json.md` foi confirmado diretamente:

```yaml
contrato_tela_json:
  classificacao: ALTERADO
  numstat: "1 0"
  conteudo: inclusao_da_ADR_0031_em_adrs_aplicadas
  mudanca_estrutural_de_schema: nao
```

## 7. ADR-0031

A ADR-0031 esta coerente quanto ao estado processual:

```yaml
status_da_adr: aceita
qa_semantico:
  resultado: ADR_QA_APPROVED_WITH_NOTES
aplicacao_documental:
  executada: true
qa_da_aplicacao:
  executada: false
implementacao:
  executada: false
handoff:
  criado: false
ultima_linha: ADR_APPLICATION_COMPLETED_AWAITING_QA
```

A ADR nao declara implementacao concluida, nao declara QA da aplicacao aprovado, preserva as decisoes deferidas e contextualiza referencias historicas a `ADR_CREATED_AWAITING_QA`. Somente a ultima linha funciona como encerramento efetivo.

## 8. Indice

`docs/adr/INDICE_ADR.md` possui exatamente uma entrada para ADR-0031, com numero, titulo, status e data compativeis com ADR aceita. A entrada declara aplicacao documental concluida, QA da aplicacao pendente e implementacao nao iniciada. Nao foi observada reserva de ADR futura nem alteracao indevida de entradas anteriores no diff material.

## 9. Backlog

`docs/backlog.md` registra `ITEM-0002` com:

```yaml
status: planejado
adr: ADR-0031_ACEITA
aplicacao_documental: CONCLUIDA
qa_da_aplicacao: PENDENTE
implementacao: NAO_INICIADA
handoff: NAO_CRIADO
proxima_acao: QA_INDEPENDENTE_DA_APLICACAO
```

Nao foi marcado `pronto_para_handoff`, nao foi marcado implementado e nenhum numero de handoff foi reservado. Os itens `ITEM-0003` a `ITEM-0014` foram preservados como planejados ou bloqueado no caso de `ITEM-0014`. O backlog nao recebeu as regras internas D1-D15.

Observacao factual: o diff de backlog inclui a criacao material da secao `Itens planejados` com `ITEM-0002` a `ITEM-0014`; isto e compativel com a ressalva do pedido sobre alteracoes anteriores pertencentes a criacao dos itens de backlog.

## 10. Contrato do console

A nova secao `## 22. Navegacao, foco e selecao unica (ADR-0031)` propaga corretamente a maioria das decisoes aplicaveis: elegibilidade, lista de foco, Tab/Shift+Tab, entrada no item `0`, navegacao interna por item logico, matriz incompleta, redimensionamento, indicador e selecao unica.

Contudo, permanece texto normativo antigo em `docs/contratos/contrato_console.md:431` declarando que, quando ha multiplos elementos de corpo, `[⇆]` alterna o foco entre eles. Isso contradiz D14, que restringe `[⇆]` a pelo menos dois consoles focalizaveis, e enfraquece D2 ao permitir leitura por elementos de corpo em geral.

Resultado: `DEFEITO` para D2/D14 neste contrato.

## 11. Barra de menus e chips

As tabelas novas de `contrato_barra_de_menus.md` e `contrato_chip.md` registram corretamente parte de `QA31-001`: `[⇆]` por dois consoles focalizaveis e `[✥]` por console focado com mais de um item navegavel.

Persistem, porem, contradicoes normativas:

- `docs/contratos/contrato_barra_de_menus.md:280` ainda define `[⇆]` como foco entre elementos de corpo diferentes.
- `docs/contratos/contrato_barra_de_menus.md:357` a `:368` ainda define `[✥]` por existencia estatica de console navegavel e estado inativo, contrariando D14.
- `docs/contratos/contrato_chip.md:157` e `:206` ainda definem `[⇆]` como alternancia entre elementos de corpo.
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md:154` ainda distingue `[⇆]` e `[✥]` por corpos/corpo em foco.

`DOC-B009` continua pendente. Nenhum chip novo foi inventado e a ordem canonica foi preservada, mas a reconciliacao de `QA31-001` ficou incompleta.

Resultado: `DEFEITO` para D14.

## 12. Composicao do corpo

`docs/contratos/contrato_composicao_corpo.md` recebeu propagacao coerente de D14 na secao 6. Grupos permanecem estruturais e nao focalizaveis; a ordem espacial dos filhos foi usada apenas como base para foco nos documentos de console; coordenadas, distribuicao, ocupacao integral, cardinalidade, preenchimento e arvores assimetricas permanecem preservados.

Resultado: `PROPAGADA_CORRETAMENTE`.

## 13. Contratos JSON

`docs/contratos/contrato_json_console.md` preserva o mecanismo vigente de navegabilidade e nao cria campo estrutural novo. A atualizacao trata `console focalizavel` por mecanismos ja existentes: `politica_navegacao.navegavel` e `navegavel` no item.

`docs/contratos/contrato_tela_json.md` teve somente a inclusao de ADR-0031 em `adrs_aplicadas` (`numstat: 1 0`). Nao houve mudanca de schema. Foco, cursor, item corrente, pagina, filtro, modo e selecao continuam como estados de runtime, separados da configuracao estrutural.

Nao foram persistidos campos novos como:

```text
cursor_atual
console_focado
item_corrente
linha_atual
coluna_atual
lista_de_foco
```

Resultado: `PROPAGADA_CORRETAMENTE` / `PRESERVADA_POR_REFERENCIA`.

## 14. Nomenclatura do console

`docs/nomenclatura/32_CONSOLE.md` introduz definicoes coerentes para console focalizavel, console focado, item logico, item corrente, lista de foco, ordem de foco, travessia em profundidade, navegacao toroidal por eixo, linha fisica, coluna indicadora e selecao unica.

Ha, entretanto, resquicio contraditorio em `docs/nomenclatura/32_CONSOLE.md:89` a `:91`: "Celula vazia forma seu proprio toroide menor". A ADR-0031 D8/D9 determina que celulas vazias nao recebem cursor e nao participam do toroide. A propria secao 4.5 do modulo corrige isso, mas a permanencia da frase antiga cria contradicao terminologica material.

Resultado: `DEFEITO` para D8/D9.

## 15. Layout, redimensionamento e paginacao

`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` registra corretamente que redimensionamento preserva o item logico, que setas nao mudam de pagina e que paginacao interativa permanece no `ITEM-0003`. `<` e `>` nao foram declarados implementados e a topologia futura de paginas nao foi incorporada ao ciclo atual.

Resultado: `PROPAGADA_CORRETAMENTE` e `DEFERIMENTO_PRESERVADO`.

## 16. Apresentacoes e modos

`docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` registra corretamente que mudanca de modo preserva o item logico, que linhas de continuacao nao recebem indicador proprio e que navegacao multinivel, expansao e recolhimento permanecem fora da ADR-0031, com `ITEM-0007` como ciclo futuro.

Resultado: `PROPAGADA_CORRETAMENTE` e `DEFERIMENTO_PRESERVADO`.

## 17. Matriz D1-D15

| Decisao | ADR | Contrato | Nomenclatura | Indice/backlog | Resultado |
| ------- | --- | -------- | ------------ | -------------- | --------- |
| D1 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PRESERVADA_POR_REFERENCIA | PRESERVADA_POR_REFERENCIA | PROPAGADA_CORRETAMENTE |
| D2 | PROPAGADA_CORRETAMENTE | DEFEITO | PROPAGADA_CORRETAMENTE | PRESERVADA_POR_REFERENCIA | DEFEITO |
| D3 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D4 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D5 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D6 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D7 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D8 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | DEFEITO | NAO_APLICAVEL | DEFEITO |
| D9 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | DEFEITO | NAO_APLICAVEL | DEFEITO |
| D10 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D11 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D12 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D13 | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | PROPAGADA_CORRETAMENTE | NAO_APLICAVEL | PROPAGADA_CORRETAMENTE |
| D14 | PROPAGADA_CORRETAMENTE | DEFEITO | DEFEITO | PRESERVADA_POR_REFERENCIA | DEFEITO |
| D15 | PROPAGADA_CORRETAMENTE | DEFERIMENTO_PRESERVADO | DEFERIMENTO_PRESERVADO | PRESERVADA_POR_REFERENCIA | DEFERIMENTO_PRESERVADO |

## 18. Tratamento de `QA31-001`

```yaml
tratamento_esperado: PROPAGACAO_DOCUMENTAL
patch_da_adr: nao
decisao_nova: nao
resultado_observado: INSUFICIENTE
```

A aplicacao iniciou a propagacao correta das condicoes dos chips, mas nao reconciliou todas as secoes aplicaveis. Permanecem formulacoes antigas em `contrato_console.md`, `contrato_barra_de_menus.md`, `contrato_chip.md` e `31_BARRA_DE_MENUS_E_CHIPS.md`.

## 19. Tratamento de `QA31-002`

```yaml
tratamento_esperado: PRESERVACAO_CONTEXTUAL
defeito: nao
resultado_observado: ADEQUADO
```

As ocorrencias historicas internas de `ADR_CREATED_AWAITING_QA` permanecem contextualizadas. A ultima linha da ADR foi substituida por `ADR_APPLICATION_COMPLETED_AWAITING_QA`; nao ha multiplos encerramentos efetivos.

## 20. Fidelidade do relatorio de aplicacao

O relatorio de aplicacao e factual quanto a lista principal de arquivos alterados, quanto ao stage vazio, quanto a ausencia de implementacao e quanto a correcao factual de `contrato_tela_json.md` como `ALTERADO` com diff `1 0`.

Entretanto, sua afirmacao de referencias cruzadas aprovadas e de reconciliacao de `QA31-001` e incompleta diante dos diffs reais e do conteudo remanescente. O relatorio nao registra os textos conflitantes preservados em secoes ainda normativas.

```yaml
relatorio_aplicacao_factualmente_consistente: nao
contrato_tela_json_classificado_simultaneamente_como_alterado_e_preservado: nao
outros_arquivos_classificados_simultaneamente_como_alterado_e_preservado: nao_confirmado_no_relatorio_como_classe_explicita
```

## 21. Escopo material

Nao houve alteracao observada em:

```text
config/
tela/
demo/
orquestrador.py
pytest.ini
conftest.py
```

Nao foram criados codigo, teste, configuracao, demo, contrato novo, modulo de nomenclatura novo, handoff ou numero de handoff reservado por esta aplicacao.

## 22. Pontos `NAO_CONFIRMADOS`

```yaml
pontos_nao_confirmados: []
```

Nao foi necessario registrar afirmacao `NAO_CONFIRMADA` alem dos defeitos materiais descritos nos achados. As capacidades futuras permanecem tratadas como deferidas, nao como implementadas.

## 23. Achados

```yaml
achado:
  id: QAAPP31-001
  severidade: MAIOR
  arquivo: docs/contratos/contrato_barra_de_menus.md
  secao: "§11 [✥] — navegação restrita a console navegável"
  decisao_afetada: D14
  autoridade: "ADR-0031 D14; contrato_console.md §22.8"
  evidencia_material: "linhas 357-368: [✥] definido por console navegável estático e estado inativo"
  comportamento_encontrado: >
    A seção ainda declara que a existencia e ativacao de [✥] considera somente
    console navegavel, que o chip existe com ao menos um console navegavel e que
    nao aparece/desaparece por foco, dataset ou conteudo.
  comportamento_esperado: >
    [✥] deve aparecer somente quando houver console focado com mais de um item
    navegavel e deve estar ausente quando nao houver console focado, quando houver
    zero itens ou quando houver exatamente um item navegavel.
  correcao_necessaria: "Reconciliar §11 com ADR-0031 D14, sem estado inativo para [✥]."
```

```yaml
achado:
  id: QAAPP31-002
  severidade: MAIOR
  arquivo: docs/contratos/contrato_console.md
  secao: "§15 Relação com dashboard e lancador"
  decisao_afetada: D2/D14
  autoridade: "ADR-0031 D2 e D14"
  evidencia_material: "linhas 431-432: [⇆] alterna foco entre múltiplos elementos de corpo"
  comportamento_encontrado: >
    O contrato ainda permite leitura de [⇆] como alternancia entre multiplos
    elementos de corpo, nao entre consoles focalizaveis.
  comportamento_esperado: >
    [⇆] deve existir apenas com pelo menos dois consoles focalizaveis; dashboard,
    lancador, console nao navegavel e console navegavel sem itens nao contam.
  correcao_necessaria: "Substituir a regra remanescente por condicao baseada em consoles focalizaveis."
```

```yaml
achado:
  id: QAAPP31-003
  severidade: MAIOR
  arquivo: docs/contratos/contrato_chip.md
  secao: "§5 Tipos conceituais; §7 Chips canônicos"
  decisao_afetada: D14
  autoridade: "ADR-0031 D14; contrato_barra_de_menus.md §20"
  evidencia_material: "linhas 157 e 206: [⇆] como alternância/foco entre elementos de corpo"
  comportamento_encontrado: >
    O contrato de chip preserva descricoes canonicas antigas de [⇆] como foco
    ou alternancia entre elementos de corpo.
  comportamento_esperado: >
    A descricao canonica deve restringir [⇆] a foco entre consoles focalizaveis,
    preservando a ordem canonica sem ampliar a elegibilidade.
  correcao_necessaria: "Atualizar as descricoes canonicas remanescentes de [⇆]."
```

```yaml
achado:
  id: QAAPP31-004
  severidade: MENOR
  arquivo: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  secao: "§5 Distinções obrigatórias"
  decisao_afetada: D14
  autoridade: "ADR-0031 D14"
  evidencia_material: "linha 154: [⇆] muda foco entre corpos; [✥] move cursor dentro do corpo em foco"
  comportamento_encontrado: >
    A tabela terminologica preserva a formulacao antiga por corpos/corpo em foco,
    em contradicao com a propria secao 4.3 atualizada.
  comportamento_esperado: >
    A distincao deve usar consoles focalizaveis e console focado, sem generalizar
    para corpos.
  correcao_necessaria: "Reconciliar a tabela de distincoes obrigatorias com D14."
```

```yaml
achado:
  id: QAAPP31-005
  severidade: MAIOR
  arquivo: docs/nomenclatura/32_CONSOLE.md
  secao: "§4.3 Navegação por [✥]"
  decisao_afetada: D8/D9
  autoridade: "ADR-0031 D8 e D9"
  evidencia_material: "linhas 89-91: célula vazia forma seu próprio toróide menor"
  comportamento_encontrado: >
    O modulo ainda afirma que celula vazia forma seu proprio toroide menor,
    embora tambem diga que o cursor nunca entra em celula vazia.
  comportamento_esperado: >
    Celulas vazias nao recebem cursor e nao participam do toroide; nao ha
    compensacao entre eixos.
  correcao_necessaria: "Remover ou reformular a frase para preservar D8/D9 sem ambiguidade."
```

```yaml
achado:
  id: QAAPP31-006
  severidade: MAIOR
  arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
  secao: "§9.4 Referências cruzadas; §10 Decisões de interpretação"
  decisao_afetada: D14
  autoridade: "Diff real e documentos aplicados"
  evidencia_material: "o relatorio declara referencias cruzadas como PASSOU, mas ha conflitos remanescentes nos documentos citados"
  comportamento_encontrado: >
    O relatorio de aplicacao apresenta a reconciliacao de QA31-001 como concluida
    e as referencias cruzadas como aprovadas, sem registrar as secoes normativas
    remanescentes que ainda contradizem D14.
  comportamento_esperado: >
    O relatorio de aplicacao deve refletir os diffs e o conteudo real dos arquivos,
    registrando incompatibilidades materiais quando existirem.
  correcao_necessaria: "Corrigir o relatorio de aplicacao apos ajuste documental, ou registrar a rejeicao desta aplicacao."
```

Resumo quantitativo:

```yaml
achados_bloqueantes: 0
achados_maiores: 5
achados_menores: 1
notas: 0
```

## 24. Classificacao final

```yaml
classificacao: ADR_APPLICATION_QA_REJECTED
justificativa: >
  Ha achados maiores e menor. A aplicacao propagou parte substancial de D1-D15,
  mas deixou contradicoes normativas remanescentes em documentos aplicados,
  especialmente sobre D14 e sobre celulas vazias em D8/D9. Pela regra de
  classificacao, qualquer achado maior ou menor exige rejeicao.
```

## 25. Arquivos alterados

Arquivo criado nesta etapa:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
```

Arquivos preexistentes alterados por esta etapa:

```yaml
arquivos_preexistentes_alterados: []
```

## 26. Estado Git

Estado observado apos a criacao deste relatorio:

```yaml
stage: VAZIO
relatorio_criado_nao_rastreado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
git_diff_check: PASSOU
git_diff_cached_check: PASSOU
git_diff_no_index_check_relatorio: PASSOU_SEM_ERROS_DE_WHITESPACE
newline_final: CONFIRMADO
cercas_markdown_fechadas: CONFIRMADO
marcadores_de_conflito: AUSENTES
commit_executado: nao
```

## 27. Encerramento

```yaml
resultado: ADR_APPLICATION_QA_REJECTED
adr: ADR-0031
item_de_backlog: ITEM-0002
relatorio_criado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
achados_bloqueantes: 0
achados_maiores: 5
achados_menores: 1
notas: 0
pontos_nao_confirmados: 0
stage: VAZIO
commit_executado: nao
```

QA_APLICACAO_ADR_CONCLUIDO
