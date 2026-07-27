---
name: relatorio-qa-pos-patch-aplicacao-adr-0031
description: QA pos-patch da aplicacao documental da ADR-0031
metadata:
  type: relatorio_qa
  etapa: QA_POS_PATCH_APLICACAO_ADR
  adr: ADR-0031
  status: ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES
---

# Relatorio de QA Pos-Patch da Aplicacao Documental - ADR-0031

## 1. Identificacao

```yaml
etapa: QA_POS_PATCH_APLICACAO_ADR
adr: ADR-0031
objeto: patch_documental_da_aplicacao_da_ADR-0031
qa_inicial_rejeitado: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
relatorio_patch: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
relatorio_criado: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
data: 2026-07-25
```

## 2. Objeto e escopo

Este QA avaliou independentemente o patch documental da aplicacao da ADR-0031,
limitado aos achados `QAAPP31-001` a `QAAPP31-006` e a uma varredura residual
diretamente relacionada a D2, D8, D9 e D14.

Nao foram aplicadas correcoes, nao houve stage, nao houve commit, nao foi criado
handoff e nao foi avaliada implementacao.

## 3. Estado inicial

```yaml
adr: ADR-0031
status_da_adr: aceita
qa_semantico_da_adr: ADR_QA_APPROVED_WITH_NOTES
aplicacao_inicial:
  classificacao: ADR_APPLICATION_QA_REJECTED
patch_da_aplicacao:
  resultado: ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA
qa_pos_patch: PENDENTE
implementacao: NAO_INICIADA
handoff: NAO_CRIADO
stage: VAZIO
commit_executado: nao
```

A rejeicao inicial foi preservada como historico em
`docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md`.

## 4. Gate

| Check | Resultado | Evidencia |
|---|---|---|
| ADR-0031 existe | PASSOU | `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md` |
| `RELATORIO_QA_ADR-0031.md` existe | PASSOU | arquivo presente |
| `RELATORIO_APLICACAO_ADR-0031.md` existe | PASSOU | arquivo presente |
| QA inicial da aplicacao existe e termina rejeitado | PASSOU | ultima linha: `QA_APLICACAO_ADR_CONCLUIDO`; bloco final: `ADR_APPLICATION_QA_REJECTED` |
| `RELATORIO_PATCH_APLICACAO_ADR-0031.md` existe | PASSOU | arquivo presente |
| Relatorio de patch termina aguardando QA | PASSOU | ultima linha: `ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA` |
| Relatorio de aplicacao atualizado termina aguardando QA | PASSOU | ultima linha: `ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA` |
| Stage vazio | PASSOU | `git status --short` sem entradas staged |
| QA pos-patch ainda nao existia | PASSOU | `test -f` retornou ausente antes da criacao |

## 5. Arquivos consultados

Leitura integral obrigatoria realizada:

```text
docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
docs/relatorios/RELATORIO_QA_ADR-0031.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0031.md
docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
docs/nomenclatura/32_CONSOLE.md
```

Leitura seletiva por referencia cruzada:

```text
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
docs/adr/INDICE_ADR.md
docs/backlog.md
```

Nenhum conteudo de handoff foi usado como autoridade.

## 6. Metodo

1. Conferencia do gate e do stage.
2. Leitura das autoridades obrigatorias.
3. Execucao dos checks de estado material.
4. Exame do diff dos cinco documentos normativos corrigidos.
5. Comparacao direta de cada achado inicial com o conteudo material pos-patch.
6. Varredura residual por padroes antigos e por termos contextuais.
7. Conferencia das decisoes deferidas e do limite material.
8. Registro de achados sem aplicar correcao.

## 7. Estado material

Checks executados antes da criacao deste relatorio:

```yaml
git_diff_cached_check: PASSOU
git_diff_check: PASSOU
stage: VAZIO
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
```

O diff completo dos cinco documentos normativos corrigidos foi examinado. O
relatorio de patch tambem foi examinado por `git diff --no-index -- /dev/null`,
mas nao foi tratado como prova suficiente sem conferencia material.

## 8. Avaliacao de QAAPP31-001

Arquivo principal: `docs/contratos/contrato_barra_de_menus.md`.

Resultado: `CORRIGIDO`.

Evidencia material:

- Secao 8.3 define `[⇆]` por "pelo menos dois consoles focalizaveis" e `[✥]`
  por "console focado possui mais de um item navegavel".
- Linhas 280-284 distinguem `[⇆]` como foco entre consoles focalizaveis e
  `[✥]` como cursor entre itens do console focado.
- Secao 11 registra que `[✥]` aparece apenas com console focado e mais de um
  item navegavel.
- O bloco YAML da secao 11 registra:
  `estado_inativo_sem_movimento: nao_utilizado`.
- As ocorrencias preservadas de `corpo em foco` estao restritas a `[Esc]`
  e selecao ativa, nao a `[⇆]` ou `[✥]`.

Nao permaneceu regra normativa de que basta existir console navegavel, de que
`[✥]` fica presente inativo sem movimento, de que foco/quantidade de itens nao
interferem, ou de que `[✥]` se aplica genericamente a qualquer corpo.

## 9. Avaliacao de QAAPP31-002

Arquivo principal: `docs/contratos/contrato_console.md`.

Resultado: `CORRIGIDO`.

Evidencia material:

- Secao 7 substitui a regra antiga por `[⇆]` entre consoles focalizaveis e
  `[✥]` no console em foco com mais de um item navegavel.
- Secao 14 registra `[⇆]` quando a tela possui pelo menos dois consoles
  focalizaveis.
- Secao 15 afirma que `dashboard`, `lancador`, grupos estruturais, consoles nao
  navegaveis e consoles navegaveis sem itens navegaveis nao entram na lista.
- Secao 22.1 define console focalizavel por navegacao declarada e ao menos um
  item com `navegavel: true`.

Nao restou regra normativa de `[⇆]` como alternancia entre elementos de corpo,
multiplos elementos ou foco entre corpos. A correcao nao redefiniu geometria ou
composicao do corpo.

## 10. Avaliacao de QAAPP31-003

Arquivo principal: `docs/contratos/contrato_chip.md`.

Resultado: `CORRIGIDO`.

Evidencia material:

- Secao 5 define o tipo `alternancia` como alternancia de foco entre consoles
  focalizaveis para `[⇆]`.
- Secao 7 descreve `[⇆]` como `Alternar (foco entre consoles focalizaveis)`.
- Secao 8 substitui as regras antigas por
  `tela_com_pelo_menos_dois_consoles_focalizaveis` e
  `console_focado_com_mais_de_um_item_navegavel`.
- Secao 9 explicita que `[✥]` nao possui estado inativo.
- Secao 14 restringe `[✥]` ao console focalizavel em foco com mais de um item
  navegavel.

Simbolo, identificador e ordem canonica foram preservados. Nenhum chip novo foi
criado. As regras genericas de estado inativo continuam validas para chips em
geral e a excecao especifica de `[✥]` esta documentada.

## 11. Avaliacao de QAAPP31-004

Arquivo principal: `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`.

Resultado: `CORRIGIDO`.

Evidencia material:

- Secao 4.3 define `[⇆]` com pelo menos dois consoles focalizaveis.
- Secao 4.3 define `[✥]` com console focado e mais de um item navegavel.
- Secao 4.4 registra a excecao de existencia dinamica de `[✥]`.
- Secao 5 registra a distincao equivalente a:
  `[⇆]` muda o foco entre consoles focalizaveis; `[✥]` move o cursor entre itens
  do console focado.

Nao foi encontrada coexistencia normativa antiga por `corpos`. Chip, tecla e
comportamento permanecem distintos.

## 12. Avaliacao de QAAPP31-005

Arquivo principal: `docs/nomenclatura/32_CONSOLE.md`.

Resultado: `CORRIGIDO`.

Evidencia material:

- Secao 4.3 afirma que celula vazia nao recebe cursor e nao participa do
  toroide.
- A mesma secao define que linha ou coluna sem outro item ocupado no eixo do
  movimento resulta em `SEM_MOVIMENTO`.
- A mesma secao nega compensacao para outra coluna, salto diagonal, busca pelo
  item geometricamente mais proximo e toroide composto por celulas vazias.
- Secao 4.5 define navegacao toroidal por eixo como exclusao de celula vazia do
  toroide, sem compensacao entre eixos.

No exemplo da ADR com:

```text
00 01 02 03
04 05
```

o comportamento material preservado e: `02` permanece em `02` com cima ou baixo,
`03` permanece em `03` com cima ou baixo, sem compensacao para outra coluna, sem
salto diagonal e sem busca por item proximo.

Os termos `ec`, `tg`, `tx`, item logico e linha fisica foram preservados.

## 13. Avaliacao de QAAPP31-006

Arquivo principal: `docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md`.

Resultado: `CORRIGIDO`.

Evidencia material:

- O relatorio preserva a aplicacao inicial como registro historico.
- Registra o QA inicial como `ADR_APPLICATION_QA_REJECTED`.
- Registra o patch documental como `CONCLUIDO`.
- Registra o QA pos-patch como `PENDENTE`.
- Nao afirma que o patch ja foi aprovado.
- Qualifica as afirmacoes antigas sobre referencias cruzadas e `QA31-001` como
  pertencentes ao registro da aplicacao inicial rejeitada.
- A ultima linha e `ADR_APPLICATION_PATCH_COMPLETED_AWAITING_QA`.

O relato do patch e compativel com os diffs reais dos cinco documentos
normativos examinados.

## 14. Varredura residual

Varredura literal dos padroes antigos:

```yaml
resultado: SEM_OCORRENCIAS
comando: grep -RIn com padroes de elementos de corpo, foco entre corpos, toroide menor e celula vazia forma
```

Ocorrencias contextuais avaliadas:

```yaml
- ocorrencia:
    arquivo: docs/contratos/contrato_console.md
    linha: 526
    contexto: tratamento de celula vazia como implementacao futura
    classificacao: COMPATIVEL
    justificativa: nao afirma que celula vazia participa do toroide; apenas cita o tema como parte da implementacao futura.
- ocorrencia:
    arquivo: docs/contratos/contrato_barra_de_menus.md
    linha: 283
    contexto: console navegavel sem itens navegaveis nao conta para "[⇆]"
    classificacao: COMPATIVEL
    justificativa: reforca D2/D14.
- ocorrencia:
    arquivo: docs/contratos/contrato_barra_de_menus.md
    linha: 295
    contexto: Esc limpa selecao ativa no corpo em foco
    classificacao: HISTORICA_CONTEXTUALIZADA
    justificativa: pertence apenas ao comportamento contextual de Esc.
- ocorrencia:
    arquivo: docs/contratos/contrato_barra_de_menus.md
    linha: 299
    contexto: Esc consulta selecao ativa no corpo em foco
    classificacao: HISTORICA_CONTEXTUALIZADA
    justificativa: pertence apenas ao comportamento contextual de Esc.
- ocorrencia:
    arquivo: docs/contratos/contrato_barra_de_menus.md
    linha: 382
    contexto: estado inativo sem movimento nao usado para "[✥]"
    classificacao: COMPATIVEL
    justificativa: nega o estado inativo antigo de "[✥]".
- ocorrencia:
    arquivo: docs/contratos/contrato_barra_de_menus.md
    linha: 664
    contexto: Esc limpa selecao ativa no corpo em foco
    classificacao: HISTORICA_CONTEXTUALIZADA
    justificativa: pertence apenas ao comportamento contextual de Esc.
- ocorrencia:
    arquivo: docs/contratos/contrato_chip.md
    linha: 242
    contexto: "[✥]" nao assume estado inativo
    classificacao: COMPATIVEL
    justificativa: documenta a excecao especifica de D14.
- ocorrencia:
    arquivo: docs/contratos/contrato_chip.md
    linha: 280
    contexto: "[✥]" nao possui estado inativo
    classificacao: COMPATIVEL
    justificativa: documenta ausencia em vez de inatividade.
- ocorrencia:
    arquivo: docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    linha: 42
    contexto: termo geral estado ativo / estado inativo
    classificacao: COMPATIVEL
    justificativa: regra geral terminologica, sem contradizer a excecao de "[✥]".
- ocorrencia:
    arquivo: docs/nomenclatura/32_CONSOLE.md
    linha: 135
    contexto: celula vazia e excluida do toroide
    classificacao: COMPATIVEL
    justificativa: afirma exatamente a regra esperada de D8/D9.
```

Contradicoes residuais normativas diretamente relacionadas a D2, D8, D9 ou D14:
`0`.

## 15. Decisoes deferidas

Permanecem fora do ciclo:

```text
ITEM-0003 — Paginacao interativa
ITEM-0004 — Acoes declarativas
ITEM-0005 — Abertura e retorno entre telas
ITEM-0006 — Selecao multipla
ITEM-0007 — Conteudo multinivel colapsavel
ITEM-0008 — Conteudo composto e heterogeneo
ITEM-0009 — Dashboard passivo
```

O patch nao criou paginacao, nao definiu Enter, nao definiu selecao multipla,
nao definiu expansao/recolhimento, nao tornou dashboard focalizavel e nao criou
handoff.

## 16. Limite material

O patch declarou e materialmente concentrou as correcoes em:

```text
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
docs/nomenclatura/32_CONSOLE.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0031.md
```

e criou:

```text
docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0031.md
```

O estado Git global contem alteracoes preexistentes fora desta etapa e fora do
limite nominal do patch, identificadas em `docs/adr/INDICE_ADR.md`,
`docs/backlog.md`, `docs/contratos/contrato_composicao_corpo.md`,
`docs/contratos/contrato_json_console.md`, `docs/contratos/contrato_tela_json.md`,
`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`,
`docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`, na ADR e
em relatorios nao rastreados anteriores. Essas alteracoes ja apareciam no estado
processual anterior e nao foram alteradas por este QA pos-patch.

Nao foi observado patch em codigo, testes, configuracoes, demos ou handoffs.

## 17. Pontos NAO_CONFIRMADOS

```yaml
pontos_nao_confirmados: []
```

Nenhuma conclusao material exigida ficou sem demonstracao por conteudo ou diff.

## 18. Matriz dos seis achados

| Achado inicial | Arquivo principal       | Resultado pos-patch | Evidencia |
| -------------- | ----------------------- | ------------------- | --------- |
| QAAPP31-001    | contrato_barra_de_menus | CORRIGIDO | Secoes 8.3, 11 e 20 usam console focado com >1 item navegavel e ausencia de "[✥]" sem movimento |
| QAAPP31-002    | contrato_console        | CORRIGIDO | Secoes 7, 14, 15 e 22 restringem "[⇆]" a consoles focalizaveis |
| QAAPP31-003    | contrato_chip           | CORRIGIDO | Secoes 5, 7, 8, 9 e 14 usam foco entre consoles focalizaveis e excecao de "[✥]" |
| QAAPP31-004    | nomenclatura 31         | CORRIGIDO | Secoes 4.3, 4.4 e 5 distinguem consoles focalizaveis e console focado |
| QAAPP31-005    | nomenclatura 32         | CORRIGIDO | Secoes 4.3 e 4.5 excluem celulas vazias do cursor e do toroide |
| QAAPP31-006    | relatorio de aplicacao  | CORRIGIDO | Secao "Patch posterior ao QA rejeitado" preserva rejeicao inicial e termina aguardando QA |

## 19. Novos achados

```yaml
achado:
  id: QAPOST31-001
  origem:
    - VARREDURA_RESIDUAL
  severidade: NOTA
  arquivo: estado_git_global
  secao: estado_material_e_limite_material
  decisao_afetada: nenhuma
  autoridade: instrucoes_da_etapa
  evidencia_material: git_status_short_com_alteracoes_preexistentes_fora_desta_etapa
  comportamento_encontrado: >
    O worktree global contem alteracoes e arquivos nao rastreados de etapas
    anteriores alem do relatorio criado neste QA pos-patch.
  comportamento_esperado: >
    O QA pos-patch deve preservar essas alteracoes, identifica-las nominalmente,
    manter o stage vazio e criar somente o novo relatorio.
  correcao_necessaria: nenhuma
```

Resumo:

```yaml
achados_bloqueantes: 0
achados_maiores: 0
achados_menores: 0
notas: 1
```

## 20. Classificacao final

```yaml
classificacao: ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES
justificativa: >
  Os seis achados iniciais foram corrigidos e nao ha contradicoes residuais
  normativas diretamente relacionadas a D2, D8, D9 ou D14. A nota registrada
  documenta apenas o estado global preexistente do worktree, sem exigir patch.
```

## 21. Arquivos alterados

```yaml
arquivos_preexistentes_alterados_por_esta_etapa: []
arquivo_criado_por_esta_etapa:
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
outros_arquivos_criados_por_esta_etapa: []
```

## 22. Estado Git

Estado observado apos a criacao deste relatorio:

```yaml
stage: VAZIO
commit_executado: nao
relatorio_criado_nao_rastreado: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0031.md
arquivos_preexistentes_alterados_por_esta_etapa: []
outros_arquivos_criados_por_esta_etapa: []
checks_mecanicos:
  test_relatorio_existe: PASSOU
  grep_secoes: PASSOU
  grep_QAAPP31_001_a_006: PASSOU
  grep_classificacao_final: PASSOU
  git_diff_check: PASSOU
  git_diff_cached_check: PASSOU
  git_diff_no_index_check_relatorio: PASSOU_SEM_ERROS_DE_WHITESPACE
  git_diff_no_index_exit_code: 1_ESPERADO_POR_ARQUIVO_NOVO_COM_DIFERENCAS
  newline_final: CONFIRMADO
  cercas_markdown: FECHADAS
  marcadores_de_conflito: AUSENTES
```

## 23. Encerramento

```yaml
resultado: ADR_APPLICATION_POST_PATCH_QA_APPROVED_WITH_NOTES
adr: ADR-0031
achados_iniciais:
  QAAPP31-001: CORRIGIDO
  QAAPP31-002: CORRIGIDO
  QAAPP31-003: CORRIGIDO
  QAAPP31-004: CORRIGIDO
  QAAPP31-005: CORRIGIDO
  QAAPP31-006: CORRIGIDO
novos_achados: 1
achados_bloqueantes: 0
achados_maiores: 0
achados_menores: 0
notas: 1
contradicoes_residuais: 0
pontos_nao_confirmados: 0
stage: VAZIO
commit_executado: nao
```

QA_POS_PATCH_APLICACAO_ADR_CONCLUIDO
