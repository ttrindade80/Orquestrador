---
name: relatorio-qa-adr-0031
description: QA semantico da ADR-0031 sobre navegacao simples e selecao unica em console de nivel unico
metadata:
  type: relatorio_qa
  etapa: QA_SEMANTICO_ADR
  adr: ADR-0031
  status: ADR_QA_APPROVED_WITH_NOTES
---

# Relatorio de QA semantico - ADR-0031

## 1. Identificacao

```yaml
etapa: QA_SEMANTICO_ADR
adr: ADR-0031
item_de_backlog: ITEM-0002
objeto: docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
relatorio_criado: docs/relatorios/RELATORIO_QA_ADR-0031.md
data: 2026-07-25
```

## 2. Objeto e escopo

O QA avaliou semanticamente a ADR-0031 quanto a fidelidade das decisoes do usuario, separacao entre decisao arquitetural e implementacao, escopo positivo/negativo, compatibilidade com contratos e ADRs vigentes, genealogia, resolucao de pontos anteriormente `NAO_CONFIRMADOS`, marcador de encerramento, coerencia interna, validacoes futuras e propagacao documental.

O QA nao aplicou patch na ADR, nao alterou contratos, nomenclatura, backlog, indice, codigo, testes ou configuracoes.

## 3. Arquivos consultados

Leitura integral:

```text
docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
docs/backlog.md
docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

Leitura seletiva por referencia material:

```text
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_chip.md
docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
docs/nomenclatura/32_CONSOLE.md
docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md
```

Nao foram lidos handoffs ou minutas de implementacao antecipadamente.

## 4. Estado inicial

```yaml
adr: ADR-0031
item_de_backlog: ITEM-0002
status_de_entrada: ADR_CREATED_AWAITING_QA
stage: VAZIO
commit_executado: nao
workspace_observado:
  - "M  docs/backlog.md"
  - "?? docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md"
  - "?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md"
  - "?? docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md"
```

Os arquivos preexistentes informados foram preservados.

## 5. Metodo

1. Conferencia do estado Git inicial.
2. Leitura integral da ADR-0031.
3. Leitura integral dos dois levantamentos, do backlog e da ADR-0030.
4. Conferencia seletiva dos contratos, nomenclaturas e ADRs historicas citadas.
5. Comparacao das decisoes D1-D15 com os criterios de fidelidade do usuario.
6. Analise de separacao entre decisao e implementacao.
7. Mapeamento dos pontos previamente `NAO_CONFIRMADOS`.
8. Verificacao do marcador `ADR_CREATED_AWAITING_QA`.
9. Registro de achados e classificacao final.

## 6. Fidelidade D1-D15

| Decisao | Avaliacao |
|---|---|
| D1 | Conforme. Limita o ciclo a foco entre consoles, navegacao de nivel unico, cursor, selecao unica, indicador, chips e compatibilidade com redimensionamento/modos. |
| D2 | Conforme. Apenas consoles com navegacao declarada e ao menos um item `navegavel: true` entram na lista; dashboard, lancador, consoles sem declaracao e consoles sem itens navegaveis ficam fora. |
| D3 | Conforme. Define lista linear por travessia hierarquica em profundidade e trata grupos estruturais como nao focalizaveis. O modelo e conceitual. |
| D4 | Conforme. Ordena irmaos espacialmente da esquerda para a direita e de cima para baixo, inclusive em matriz por linhas. |
| D5 | Conforme. Tab e Shift+Tab percorrem a mesma lista circular em sentidos opostos. |
| D6 | Conforme. Toda entrada em console reinicia no item logico `0`, sem restaurar cursor anterior ao retornar por Tab/Shift+Tab. |
| D7 | Conforme. Ordena itens por linha, coluna e matriz em row-major; linhas fisicas de continuacao nao viram itens. |
| D8 | Conforme. Setas formam toroides independentes por eixo na pagina atual, sem troca de linha por esquerda/direita e sem troca de coluna por cima/baixo. |
| D9 | Conforme. Cobre um item, uma linha, uma coluna, matriz incompleta, celulas vazias fora do cursor e ausencia de compensacao. |
| D10 | Conforme. Preserva item logico em redimensionamento e mudanca de modo, distinguindo entrada no console de redistribuicao do console ja focado. |
| D11 | Conforme. Apenas o console focado exibe o indicador do item corrente; nao cria indicador extra no titulo. |
| D12 | Conforme. Reserva espaco estavel para indicador, mostra simbolo apenas na primeira linha fisica do item corrente, usa espaco nas continuacoes e deriva o simbolo do estilo global. |
| D13 | Conforme. Selecao unica e somente o item sob cursor, sem conjunto persistente, sem toggle por espaco e sem indicador de inclusao. |
| D14 | Conforme. Refina `[⇆]` para pelo menos dois consoles focalizaveis e `[✥]` para console focado com mais de um item; nao inventa chip novo. |
| D15 | Conforme. Setas nao atravessam paginas; paginacao interativa, acoes, transicao entre telas, selecao multipla e navegacao multinivel ficam deferidas. |

## 7. Escopo positivo e negativo

Escopo positivo confirmado:

```text
foco entre consoles navegaveis
navegacao de nivel unico
cursor e selecao unica
indicador visual
chips associados
redimensionamento e modos
```

Escopo negativo confirmado:

```text
paginacao interativa
acoes
abertura e retorno entre telas
selecao multipla
navegacao multinivel
expansao e recolhimento
dashboard
```

As mencoes a paginacao futura, Enter, selecao multipla, expansao/recolhimento e dashboard aparecem como fronteira ou decisao deferida, nao como aplicacao no ciclo atual.

## 8. Genealogia

```yaml
decisoes_do_usuario:
  estado: CONFIRMADO
  conteudo: D1-D15
regras_contratuais_preexistentes:
  estado: CONFIRMADO
  exemplos:
    - politica_navegacao
    - navegavel_em_item
    - cursor_por_item
    - selecao_unica_sem_toggle
    - ec_tg_tx
    - indicador_derivado_do_estilo_global
evidencias_dos_levantamentos:
  estado: CONFIRMADO
  uso: inventario_de_lacunas_e_invariantes
decisoes_tecnicas_de_handoff: []
```

A ADR nao atribui aos levantamentos autoridade superior as decisoes do usuario. Regras preexistentes foram separadas de decisoes novas. ADR-0030 foi descrita como encerramento do Bloco 1 de estilo, com Blocos 2 e 3 futuros. Nenhuma decisao tecnica de implementacao foi inventada como handoff.

## 9. Compatibilidade e nao regressao

Compatibilidade confirmada:

- Matriz de grupos e coordenadas explicitas permanecem preservadas; a navegacao atua sobre consoles/itens, nao sobre celulas da matriz estrutural de grupos.
- Ocupacao integral do corpo e cardinalidade unitaria permanecem preservadas; a coluna indicadora e interna ao console.
- Distribuicoes horizontal, vertical e matricial continuam vigentes.
- Linhas incompletas sao tratadas apenas no dominio dos itens do console e nao reabrem distribuicao estrutural.
- Redimensionamento e responsividade recalculam visualizacao sem alterar declaracao estrutural.
- Conteudo externo multinivel e separacao entre JSON estrutural e documento externo permanecem preservados.
- Modos verboso e nao verboso sao preservados, inclusive a divergencia terminologica registrada entre `modo normal` e `modo nao verboso`.
- Estilo global materializado permanece autoridade para o indicador.
- Paginacao existente permanece como apresentacao/estado de runtime; setas nao viram mecanismo de troca de pagina.
- Separacao entre configuracao estrutural e estado de runtime foi mantida.
- Dashboard e lancador continuam fora da navegacao interna do console.
- `ec`, `tg` e `tx` foram preservados como terminologia ativa, sem alegacao de materializacao fisica global nao comprovada.

Nao foi identificado conflito real com ADR historica, contrato ou nomenclatura que exija correcao da ADR-0031.

## 10. Pontos `NAO_CONFIRMADOS`

| Ponto original | Decisao que resolve | Autoridade | Resultado |
|---|---|---|---|
| `arquivo_proprio_DOC_B009` | D15 / decisoes deferidas | Fronteira de escopo do usuario | Resolvido como fora do ciclo; nao inventa arquivo nem registry. |
| `DOC_B009_como_item_de_backlog_material` | D15 / ITEM-0004 | Fronteira de escopo do usuario e backlog | Resolvido como ciclo futuro; nao reclassifica DOC-B009. |
| `regra_inicial_do_cursor` | D6 | Usuario | Resolvido: entrada em console sempre posiciona item `0`. |
| `regra_inicial_do_foco` | D3-D6 e modelo conceitual | Usuario | Resolvido no limite do ciclo: lista linear e entrada no console; zero consoles sem foco. |
| `equivalencia_formal_entre_foco_e_selecao_unica` | D11-D13 | Usuario + contrato_console | Resolvido sem equivalencia indevida: foco do console, cursor do item e selecao unica ficam separados. |
| `diferenca_formal_completa_entre_foco_e_selecao_unica_como_estados_distintos` | D11-D13 | Usuario + regras preexistentes | Resolvido para o ciclo: console focado, item corrente e item sob cursor sao distinguidos. |
| `preservacao_do_estado_da_tela_de_origem` | D15 | Usuario | Permanece fora do ciclo, corretamente deferido para abertura/retorno entre telas. |
| `aplicacao_automatica_do_mecanismo_do_lancador_ao_Enter_do_console` | D13-D15 | Usuario + contratos | Resolvido como nao aplicavel neste ciclo; Enter nao e implementado pela ADR. |
| `regra_de_linha_incompleta_para_navegacao` | D8-D9 | Usuario | Resolvido: celulas vazias nao participam do toroide e nao ha compensacao. |
| algoritmo detalhado de movimento 2D | D8-D9 | Usuario | Resolvido no nivel arquitetural: toroide por eixo e por pagina atual. |
| tratamento detalhado de celulas vazias | D8-D9 | Usuario | Resolvido: sem cursor, sem participacao no toroide. |
| preservacao integral de cursor/foco ao redimensionar | D10 | Usuario | Resolvido para item logico do console focado; outros estados de tela permanecem fora. |
| restauracao de cursor/foco ao trocar cenario ou retornar por pilha | D6 e D15 | Usuario | Resolvido para retorno por Tab no mesmo ciclo; retorno por pilha/tela fica fora. |
| registry completo de acoes declarativas | D15 | Usuario | Permanece fora do ciclo, corretamente deferido para ITEM-0004. |

Quantidade de pontos ainda indevidamente nao confirmados dentro do escopo da ADR: `0`.

## 11. Coerencia interna

Nao foram identificadas contradicoes materiais entre D1-D15.

Conferencias especificas:

- D6 e D10 sao compativeis: entrada em console reinicia no item `0`; redistribuicao do console ja focado preserva o item logico corrente.
- A ADR distingue item logico de linha fisica.
- A ADR distingue foco do console, cursor do item e selecao unica.
- "Selecionado", "corrente", "focado" e "incluido" sao usados de forma consistente com os contratos e a nomenclatura.
- Paginacao nao foi incorporada ao escopo das setas.
- Enter e acoes permanecem fora do ciclo.
- Selecao multipla nao foi incorporada a selecao unica.
- A regra visual do indicador nao redefine a geometria estrutural do corpo.
- Os exemplos normativos de D4 e D9 sao compativeis com as decisoes.

## 12. Marcador de encerramento

Ocorrencias verificadas de `ADR_CREATED_AWAITING_QA` na ADR:

| Linha aproximada | Contexto | Avaliacao |
|---|---|---|
| 7 | metadata.status | Referencia de estado; aceitavel. |
| 37 | tabela de identificacao | Referencia de estado; aceitavel. |
| 48 | secao Status | Citacao literal do estado; aceitavel. |
| 1009 | bloco YAML de encerramento, `status_literal` | Requisito documental; aceitavel. |
| 1033 | ultima linha | Encerramento efetivo; aceitavel. |

As ocorrencias internas nao simulam multiplos encerramentos, nao geram ambiguidade de status e nao contradizem o status da ADR.

## 13. Validacoes futuras

A ADR preve validacoes futuras para os casos requeridos:

```yaml
zero_consoles_focalizaveis: previsto
um_console_com_um_item: previsto
uma_linha: previsto
uma_coluna: previsto
matriz_completa: previsto
matriz_incompleta: previsto
multiplos_consoles: previsto
grupos_hierarquicos_assimetricos: previsto
Tab_circular: previsto
Shift_Tab_circular: previsto
retorno_ao_console_no_item_0: previsto
console_vazio_fora_da_lista: previsto
console_nao_navegavel_fora_da_lista: previsto
indicador_apenas_no_console_focado: previsto
linhas_de_continuacao_sem_indicador_repetido: previsto
coluna_indicadora_estavel: previsto
redimensionamento: previsto
modo_verboso_e_nao_verboso: previsto
recalculo_de_vizinhancas: previsto
chips_condicionais: previsto
setas_restritas_a_pagina: previsto
ausencia_de_selecao_multipla: previsto
ausencia_de_execucao_de_acoes: previsto
```

Nao ha ausencia material de caso obrigatorio.

## 14. Propagacao documental

A ADR identifica adequadamente documentos para atualizacao, inspecao ou preservacao futura:

```text
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
docs/adr/INDICE_ADR.md
docs/backlog.md
```

A ADR nao exige alteracao imediata desses arquivos, nao declara aplicacao concluida e preserva o fluxo documental futuro.

## 15. Achados

```yaml
achado:
  id: QA31-001
  severidade: NOTA
  secao_da_adr: "D14; secao 15; secao 19"
  decisao_afetada: D14
  autoridade: "decisao do usuario; contrato_barra_de_menus.md; contrato_chip.md"
  comportamento_encontrado: >
    A ADR refina as condicoes de aparicao de `[⇆]` e `[✥]` com base em consoles
    focalizaveis e no console focado com mais de um item, enquanto os contratos
    vigentes ainda possuem formulacoes anteriores baseadas em console navegavel
    ou multiplos elementos de corpo.
  comportamento_esperado: >
    A diferenca deve permanecer registrada como propagacao documental futura,
    sem exigir alteracao imediata dos contratos nesta etapa.
  correcao_necessaria: nenhuma
```

```yaml
achado:
  id: QA31-002
  severidade: NOTA
  secao_da_adr: "secao 20 e ultima linha"
  decisao_afetada: nenhuma
  autoridade: "criterio de encerramento do QA"
  comportamento_encontrado: >
    A string `ADR_CREATED_AWAITING_QA` aparece em metadata, tabela de status,
    secao de status, bloco de encerramento e ultima linha.
  comportamento_esperado: >
    Ocorrencias internas podem existir quando sao referencia de estado,
    exemplo, citacao literal ou requisito documental; somente a ultima linha
    deve funcionar como encerramento efetivo.
  correcao_necessaria: nenhuma
```

Resumo quantitativo:

```yaml
achados_bloqueantes: 0
achados_maiores: 0
achados_menores: 0
notas: 2
```

## 16. Classificacao final

```yaml
classificacao: ADR_QA_APPROVED_WITH_NOTES
justificativa: >
  Nao ha achados bloqueantes, maiores ou menores. As notas registram apenas
  fronteiras historicas/documentais que nao exigem correcao da ADR.
```

## 17. Arquivos alterados

```yaml
arquivos_preexistentes_alterados: []
arquivo_criado:
  - docs/relatorios/RELATORIO_QA_ADR-0031.md
outros_arquivos_criados: []
```

## 18. Estado Git

Estado esperado apos a criacao deste relatorio:

```yaml
stage: VAZIO
commit_executado: nao
arquivos_preservados:
  - docs/backlog.md
  - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_COMPATIBILIDADE_NAVEGACAO_DISTRIBUICAO_CONSOLE.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_NAVEGACAO_SELECAO_UNICA_ACOES.md
arquivo_nao_rastreado_criado:
  - docs/relatorios/RELATORIO_QA_ADR-0031.md
```

## 19. Encerramento

```yaml
resultado: ADR_QA_APPROVED_WITH_NOTES
adr: ADR-0031
relatorio_criado: docs/relatorios/RELATORIO_QA_ADR-0031.md
achados_bloqueantes: 0
achados_maiores: 0
achados_menores: 0
notas: 2
pontos_nao_confirmados_no_escopo: 0
stage: VAZIO
commit_executado: nao
```

QA_SEMANTICO_ADR_CONCLUIDO
