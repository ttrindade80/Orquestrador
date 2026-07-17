---
name: RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025
description: Auditoria documental independente pos-patch da aplicacao da ADR-0025
metadata:
  type: relatorio_qa_aplicacao_adr
  ciclo: QA_APLICACAO_ADR
  rodada: POS_PATCH
  adr_auditada: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  qa_anterior: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
  status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
  status_normalizado: APLICACAO_ADR_APROVADA_COM_OBSERVACOES
  data: "2026-07-16"
---

# Relatorio QA pos-patch da aplicacao da ADR-0025

## 1. Identificacao

Etapa executada:

```text
QA_APLICACAO_ADR
```

Rodada:

```text
POS_PATCH
```

Relatorio criado:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
```

## 2. Objetivo

Auditar documentalmente a rodada pos-patch da aplicacao da ADR-0025, verificando
se o `PATCH_APLICACAO_ADR` corrigiu os seis achados do QA anterior, aplicou as
tres decisoes complementares explicitas do usuario, preservou as autoridades
normativas ativas e nao introduziu regressao documental.

Esta auditoria nao corrige contratos, nao altera a ADR, nao altera relatorios
anteriores, nao cria handoff, nao implementa, nao cria JSONs e nao prepara
commit.

## 3. Etapa auditada

```text
PATCH_APLICACAO_ADR - ADR-0025
```

## 4. ADR e relatorios de entrada

ADR auditada:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
```

Relatorio de aplicacao auditado:

```text
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
```

QA anterior da aplicacao:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
```

QAs anteriores da ADR:

```text
docs/relatorios/RELATORIO_QA_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
```

## 5. Arquivos lidos

Arquivos lidos integralmente ou por inspecao material completa das secoes
normativas afetadas:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
docs/relatorios/RELATORIO_QA_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_json_console.md
docs/adr/ADR-0001-menu-suporta-matriz.md
docs/adr/ADR-0002-menu-sobra-direita.md
docs/adr/ADR-0003-vaos-elasticos-menu.md
docs/adr/ADR-0023-largura-minima-funcional-lancador.md
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
```

## 6. Estado Git inicial

Comandos executados antes da criacao deste relatorio:

```text
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff --cached --name-only
```

`git status --short` retornou:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_json_dashboard.md
 M docs/contratos/contrato_json_lancador.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
?? docs/relatorios/RELATORIO_QA_ADR-0025.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
```

Registro separado:

```yaml
arquivos_rastreados_modificados: 8
arquivos_nao_rastreados: 5
stage: vazio
arquivos_fora_de_docs: nenhum
git_diff_check: saida_vazia
git_diff_cached_name_only: saida_vazia
```

Arquivos inesperados em relacao ao conjunto declarado como alterado pelo patch:

```yaml
- arquivo: docs/NOMENCLATURA.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: modificado no estado Git, mas declarado como preservado pelo patch
- arquivo: docs/adr/INDICE_ADR.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: modificado no estado Git, mas nao listado entre arquivos alterados pelo patch
- arquivo: docs/contratos/contrato_composicao_corpo.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: modificado no estado Git, mas declarado como preservado pelo patch
- arquivo: docs/contratos/contrato_tela_json.md
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
  observacao: modificado no estado Git, mas declarado como preservado pelo patch
```

Esses arquivos sao coerentes com a aplicacao original da ADR-0025, mas o estado
Git atual nao prova, sozinho, a autoria ou o momento exato dessas modificacoes.

## 7. Diff real

`git diff --stat` retornou:

```text
docs/NOMENCLATURA.md                        |  87 ++++++++++++++++
docs/adr/INDICE_ADR.md                      |   1 +
docs/contratos/contrato_composicao_corpo.md |  53 ++++++++++
docs/contratos/contrato_json_console.md     | 127 +++++++++++++++++++++++
docs/contratos/contrato_json_dashboard.md   | 152 ++++++++++++++++++++++++++++
docs/contratos/contrato_json_lancador.md    | 122 ++++++++++++++++++++++
docs/contratos/contrato_lancador.md         |  86 ++++++++++++++++
docs/contratos/contrato_tela_json.md        | 127 +++++++++++++++++++++++
8 files changed, 755 insertions(+)
```

`git diff --name-only` retornou:

```text
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
```

Arquivos realmente alterados pelo patch conforme declaracao e evidencias
internas do relatorio de aplicacao:

```text
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_json_console.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
```

Arquivos preexistentes preservados pelo patch conforme declaracao, mas
presentes no estado Git por historico anterior ou origem nao confirmada:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_QA_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
```

Para arquivos nao rastreados relevantes, `git diff --no-index --check
/dev/null <arquivo>` retornou saida vazia. O codigo de saida diferente de zero
foi tratado apenas como diferenca contra `/dev/null`, nao como defeito.

## 8. Resumo do patch

O patch declarou corrigidos:

```text
QA-APP-ADR0025-BLOQ-001
QA-APP-ADR0025-ALTO-001
QA-APP-ADR0025-ALTO-002
QA-APP-ADR0025-MEDIO-001
QA-APP-ADR0025-BAIXO-001
QA-APP-ADR0025-BAIXO-002
```

Tambem declarou aplicar tres decisoes complementares explicitas do usuario:

```text
DEC-APP-0025-01
DEC-APP-0025-02
DEC-APP-0025-03
```

## 9. Reavaliacao dos seis achados

```yaml
QA-APP-ADR0025-BLOQ-001:
  resultado: CORRIGIDO
  evidencia: >
    contrato_json_dashboard.md secao 9.2.1 define o tratamento quando
    dimensionamento.colunas.politica ou dimensionamento.linhas.politica e
    minimo_fixo e o participante exige dimensao superior. A regra vale para
    linhas e colunas, nao cresce a dimensao externa automaticamente, nao
    invalida a formacao externa apenas por essa exigencia, atribui o tratamento
    interno ao participante e proibe truncamento, quebra, rolagem, paginacao,
    propagacao de fallback, reducao de minimos e crescimento externo automatico.
QA-APP-ADR0025-ALTO-001:
  resultado: CORRIGIDO
  evidencia: >
    contrato_lancador.md secao 11.3 e contrato_json_lancador.md secao 9.4
    declaram tabela normativa de precedencia. Quando distribuicao_matricial
    esta presente, formacao, distribuicao horizontal, vaos e margens
    sobrepostas deixam de concorrer com ADR-0001, ADR-0002 e ADR-0003.
    Quando ausente, o comportamento historico permanece. H-0034 fica separado.
QA-APP-ADR0025-ALTO-002:
  resultado: CORRIGIDO
  evidencia: >
    contrato_json_console.md secao 10.3 declara que as politicas geometricas
    antigas sao integralmente substituidas quando distribuicao_matricial esta
    presente, sem coexistencia, complemento, cascata ou heranca parcial. As
    politicas funcionais nao geometricas permanecem preservadas.
QA-APP-ADR0025-MEDIO-001:
  resultado: CORRIGIDO
  evidencia: >
    RELATORIO_APLICACAO_ADR-0025.md distingue oito decisoes semanticas da
    aplicacao original, zero decisoes editoriais confirmadas, tres decisoes
    semanticas pos-QA e total de onze decisoes semanticas documentadas.
QA-APP-ADR0025-BAIXO-001:
  resultado: CORRIGIDO
  evidencia: >
    RELATORIO_APLICACAO_ADR-0025.md registra 26 caminhos de campo na tabela
    normativa de contrato_json_dashboard.md secao 9.2, com criterio explicito:
    cada linha normativa de caminho, de formacao.politica ate
    alinhamento_interno.vertical.
QA-APP-ADR0025-BAIXO-002:
  resultado: CORRIGIDO
  evidencia: >
    git diff --no-index --check /dev/null
    docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md retornou saida vazia.
```

## 10. Analise de DEC-APP-0025-01

```yaml
decisao: DEC-APP-0025-01
fidelidade: integral
documentos_afetados:
  - docs/contratos/contrato_json_dashboard.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_lancador.md
regra_normativa_resultante: >
  Quando minimo_fixo e usado em linhas ou colunas e o participante exige
  dimensao superior, a distribuicao externa entrega a area calculada e o
  participante trata internamente seu conteudo.
ambiguidade_remanescente: nenhuma bloqueante
contradicao_remanescente: nenhuma
resultado: APLICADA_INTEGRALMENTE
```

A regra preserva a coerencia semantica de `minimo_fixo`: o minimo externo e
fixo e inviolavel no nivel externo; a exigencia interna do participante nao
reduz minimos, nao aumenta a matriz automaticamente e nao cria formacao externa
invalida por si so.

## 11. Autoridade do tratamento interno

A decisao explicita do usuario em DEC-APP-0025-01 constitui autoridade
normativa suficiente para selecionar `TRATAMENTO_INTERNO_DO_PARTICIPANTE`.

As autoridades ativas sustentam a fronteira, sem precisar definir uma regra
multinivel completa:

```yaml
ADR-0025_secoes_7_e_8:
  sustenta:
    - participante imediato tratado como unidade no nivel externo
    - descendentes nao participam diretamente da matriz do nivel externo
    - distribuicao interna futura pertence ao participante
  limite:
    - por si so, nao escolhia antes o tratamento para minimo_fixo excedido
contrato_composicao_corpo_secao_11_1:
  sustenta:
    - separacao entre composicao hierarquica, distribuicao de area e
      distribuicao interna de participantes
contrato_especifico_do_participante:
  sustenta:
    - responsabilidade do participante por seu conteudo interno
decisao_do_usuario:
  sustenta:
    - ausencia de crescimento externo
    - ausencia de invalidacao externa apenas pela exigencia interna
    - ausencia de reorganizacao de descendentes
```

A afirmacao generica de que o participante e unidade unica nao seria, sozinha,
suficiente para provar todas as consequencias. Nesta rodada, a decisao do
usuario fecha a escolha normativa; os documentos ativos fornecem a fronteira
entre nivel externo e tratamento interno.

## 12. Analise de DEC-APP-0025-02

```yaml
decisao: DEC-APP-0025-02
fidelidade: integral
documentos_afetados:
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_json_lancador.md
regra_normativa_resultante: >
  Quando distribuicao_matricial esta presente no lancador, a nova configuracao
  tem precedencia sobre ADR-0001, ADR-0002 e ADR-0003 nas responsabilidades
  geometricas sobrepostas. Quando ausente, as politicas antigas permanecem.
ambiguidade_remanescente: nenhuma bloqueante
contradicao_remanescente: nenhuma
resultado: APLICADA_INTEGRALMENTE
```

## 13. Precedencia do lancador

Verificacao:

```yaml
tabela_normativa_de_precedencia: presente
algoritmo_automatico_fila_matriz_substituido_quando_campo_presente: sim
sobra_obrigatoria_a_direita_substituida_quando_campo_presente: sim
vaos_elasticos_e_margens_antigas_substituidos_quando_campo_presente: sim
alinhamento_e_dimensionamento_sobrepostos_tratados: sim
regras_funcionais_nao_geometricas_preservadas: sim
ADR_0023_largura_minima_e_fallback_preservada: sim
ausencia_do_campo_preserva_comportamento_antigo: sim
jsons_antigos_compativeis: sim
H_0034_corrigido_silenciosamente: nao
duas_politicas_concorrentes: nao
```

Observacao documental: a abertura da secao 11 de `contrato_lancador.md` ainda
usa a formula "o que requer reconciliacao futura". A subsecoes 11.3, 11.4 e
11.5, porem, fecham a precedencia aplicavel para `distribuicao_matricial` e
separam H-0034. Essa ocorrencia e classificada como texto introdutorio
historico/desatualizado, sem contradicao normativa ativa.

## 14. Analise de DEC-APP-0025-03

```yaml
decisao: DEC-APP-0025-03
fidelidade: integral
documentos_afetados:
  - docs/contratos/contrato_json_console.md
regra_normativa_resultante: >
  Quando distribuicao_matricial esta presente no console, as politicas
  geometricas antigas relacionadas a organizacao do conjunto sao substituidas
  integralmente. Quando ausente, todo comportamento anterior permanece.
ambiguidade_remanescente: nenhuma bloqueante
contradicao_remanescente: nenhuma
resultado: APLICADA_INTEGRALMENTE
```

## 15. Substituicao das politicas do console

Verificacao:

```yaml
politicas_antigas_de_vaos_substituidas: sim
politicas_antigas_de_alinhamento_substituidas: sim
alinhamento_de_colunas_substituido: sim
quantidade_ou_ajuste_de_colunas_substituido: sim
formacao_e_distribuicao_geometrica_antigas_substituidas: sim
combinacao_soma_cascata_ou_complemento: nao
politicas_funcionais_nao_geometricas_preservadas: sim
paginacao_do_console_preservada_fora_da_capacidade_ADR_0025: sim
ausencia_do_campo_preserva_comportamento_antigo: sim
jsons_antigos_compativeis: sim
remissao_a_handoff_futuro_para_precedencia: nao
lista_de_politicas_preservadas_contem_regra_geometrica_concorrente: nao
```

A paginacao do console permanece como politica funcional do console, mas a
capacidade ADR-0025 nao passa a definir paginacao do conjunto de participantes.

## 16. Regressoes

Verificacao de regressao:

```yaml
semantica_multinivel_nova: false
recursao: false
heranca: false
cascata: false
paginacao_na_capacidade_ADR_0025: false
default_estrutural: false
migracao_automatica: false
alteracao_de_JSON_existente: false
regra_universal_nao_decidida: false
crescimento_externo_implicito: false
invalidacao_externa_implicita: false
truncamento_interno_implicito: false
substituicao_excessiva_de_regras_funcionais_console: false
substituicao_excessiva_de_regras_funcionais_lancador: false
correcao_silenciosa_H_0034: false
conflito_com_ocupacao_integral_do_corpo: false
conflito_entre_minimo_fixo_e_minimos_inviolaveis: false
duas_autoridades_geometricas_simultaneas: false
```

## 17. Estrutura JSON

```yaml
campo_principal: distribuicao_matricial
quantidade_de_caminhos_de_campo: 26
estrutura_consistente_entre_dashboard_console_lancador: true
nivel_unico: true
paginacao_da_capacidade: false
multinivel: false
aplicacao_recursiva: false
migracao_automatica: false
jsons_antigos_preservados: true
campos_adicionais_nao_documentados_exigidos_pelo_patch: false
```

## 18. Compatibilidade

```yaml
jsons_antigos:
  preservados: true
  evidencia: ausencia de distribuicao_matricial preserva comportamento anterior
migracao_automatica: false
reescrita_automatica_de_JSON: false
default_estrutural_novo: false
campos_desconhecidos: rejeicao_controlada
```

## 19. Paginacao

A ADR-0025 e os contratos aplicados mantem paginacao fora da capacidade de
distribuicao matricial. Ocorrencias de paginacao no console continuam
pertencendo ao comportamento funcional do console e nao se tornam regra da nova
capacidade. O `lancador` continua sem paginacao.

## 20. Multinivel

A aplicacao preserva nivel unico. `distribuicao_matricial` organiza apenas os
participantes imediatos do elemento declarante, sem recursao, heranca, cascata
ou propagacao a descendentes.

## 21. Fallback

O fallback aplicavel e o `quadro minimo de terminal pequeno`, ja estabelecido
pelas autoridades ativas. A aplicacao nao cria variante concorrente, nao cria
fallback local e nao autoriza truncamento, ocultacao, paginacao ou renderizacao
parcial para forcar encaixe.

## 22. Pendencias resolvidas

```yaml
comportamento_minimo_fixo_excedido:
  estado: RESOLVIDA
  evidencia: contrato_json_dashboard.md secao 9.2.1 e remissoes de console/lancador
reconciliacao_lancador_adr_0001_0002_0003:
  estado: RESOLVIDA
  evidencia: contrato_lancador.md secao 11.3 e contrato_json_lancador.md secao 9.4
reconciliacao_console_politicas_especificas:
  estado: RESOLVIDA
  evidencia: contrato_json_console.md secao 10.3
```

## 23. Pendencias mantidas

```yaml
divergencia_h_0034:
  classificacao: futura_nao_bloqueante
  evidencia: >
    contrato_lancador.md secao 11.4 e contrato_json_lancador.md secao 9.5
    declaram que a divergencia permanece separada e nao foi corrigida por esta
    aplicacao.
alinhamento_horizontal_dashboard:
  classificacao: futura_nao_bloqueante
  evidencia: >
    contrato_json_dashboard.md secao 9.5 mantem a pendencia da NOMENCLATURA
    delimitada e sem criar duas autoridades simultaneas para
    distribuicao_matricial.
```

## 24. Busca de residuos

Busca executada nos documentos afetados por:

```text
reconciliacao futura
reconciliação futura
pendente de handoff
coexistem
coexistência
nao substitui
não substitui
minimo_fixo
mínimo fixo
participante maior
dimensao maior
dimensão maior
algoritmo automatico
algoritmo automático
sobra a direita
sobra à direita
vaos elasticos
vãos elásticos
numero de colunas
número de colunas
alinhamento de colunas
decisoes_editoriais
decisões editoriais
24 campos
arquivos_modificados: 9
```

Classificacao das ocorrencias materiais:

```yaml
ocorrencia_historica:
  - ADR-0002 no indice
  - referencias historicas de sobra a direita e vaos elasticos no lancador
regra_aplicavel_quando_campo_ausente:
  - algoritmo automatico, sobra a direita e vaos elasticos preservados no lancador
politica_substituida_quando_campo_presente:
  - contrato_lancador.md secao 11.3
  - contrato_json_lancador.md secao 9.4
  - contrato_json_console.md secao 10.3
texto_legitimo:
  - ocorrencias de minimo_fixo na decisao DEC-APP-0025-01
  - ocorrencias de coexistencia em contextos nao relacionados a ADR-0025
  - alinhamento horizontal do dashboard como pendencia futura delimitada
residuo_contraditorio:
  - nenhum
```

Nao foram encontradas ocorrencias materiais de `24 campos` nem
`arquivos_modificados: 9` no relatorio de aplicacao pos-patch.

## 25. Fidelidade do relatorio de aplicacao

O relatorio de aplicacao foi corrigido nos pontos auditados:

```yaml
decisoes_semanticas_da_aplicacao_original: 8
decisoes_editoriais_confirmadas: 0
decisoes_semanticas_pos_qa: 3
total_de_decisoes_semanticas_documentadas: 11
quantidade_de_caminhos_de_campo: 26
trailing_whitespace: removido
arquivos_rastreados_modificados: 8
adr_nao_rastreada_preexistente_alterada_pela_aplicacao: 1
relatorio_criado_pela_aplicacao: 1
relatorios_qa_preexistentes_preservados: 2
```

A ADR nao e chamada de arquivo rastreado modificado. O relatorio de QA da
aplicacao nao e atribuido a aplicacao original. As decisoes pos-QA aparecem
identificadas como posteriores e distintas das oito decisoes originais.

## 26. Estado Git final

Comandos executados apos a criacao deste relatorio:

```text
git status --short
git diff --stat
git diff --name-only
git diff --check
git diff --cached --name-only
git diff --no-index --check /dev/null docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
```

`git status --short` retornou:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_json_dashboard.md
 M docs/contratos/contrato_json_lancador.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
?? docs/relatorios/RELATORIO_QA_ADR-0025.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
```

Confirmacao:

```yaml
novo_arquivo_criado_nesta_etapa:
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
documentos_auditados_alterados_por_esta_etapa: nenhum
stage: vazio
arquivos_fora_de_docs: nenhum
git_diff_stat_rastreado: 8 files changed, 755 insertions(+)
git_diff_name_only_rastreado:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_dashboard.md
  - docs/contratos/contrato_json_lancador.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
git_diff_check: saida_vazia
git_diff_cached_name_only: saida_vazia
novo_relatorio_no_index_check: saida_vazia
```

## 27. Achados

Achados bloqueantes: 0.

Achados altos: 0.

Achados medios: 0.

Achados baixos: 0.

Achados novos:

```yaml
[]
```

## 28. Observacoes

```yaml
- id: OBS-QA-POS-APP-ADR0025-001
  severidade: observacao
  arquivo: docs/contratos/contrato_lancador.md
  secao: "11. Capacidade de distribuicao matricial"
  evidencia: >
    A abertura da secao ainda menciona "o que requer reconciliacao futura",
    mas a secao 11.3 fecha a precedencia aplicavel quando
    distribuicao_matricial esta presente.
  impacto: >
    Texto introdutorio historico/desatualizado, sem contradicao normativa ativa.
  correcao_necessaria: nenhuma antes do handoff.

- id: OBS-QA-POS-APP-ADR0025-002
  severidade: observacao
  arquivo: docs/contratos/contrato_lancador.md
  secao: "11.4"
  evidencia: >
    A divergencia H-0034 permanece separada e nao foi corrigida
    silenciosamente.
  impacto: futura nao bloqueante.
  correcao_necessaria: ciclo documental proprio, quando autorizado.

- id: OBS-QA-POS-APP-ADR0025-003
  severidade: observacao
  arquivo: docs/contratos/contrato_json_dashboard.md
  secao: "9.5"
  evidencia: >
    O alinhamento horizontal do dashboard permanece pendencia futura
    delimitada.
  impacto: futura nao bloqueante.
  correcao_necessaria: nenhuma para aprovar esta aplicacao.
```

## 29. Conclusao

O `PATCH_APLICACAO_ADR` corrigiu integralmente os seis achados do QA anterior.
As tres decisoes complementares do usuario foram aplicadas de forma fiel:
`minimo_fixo` excedido recebeu tratamento interno do participante; o `lancador`
recebeu precedencia normativa da nova configuracao quando presente; e o
`console` recebeu substituicao integral das politicas geometricas antigas
quando `distribuicao_matricial` e declarada.

Nao foram identificadas decisoes ausentes, contradicoes documentais ativas ou
regressoes que exijam novo patch antes do proximo fluxo. Restam apenas
observacoes futuras nao bloqueantes.

## 30. Status literal

```text
ADR_APPLICATION_APPROVED_WITH_NOTES
```

## 31. Status normalizado e proxima categoria

```yaml
status_normalizado: APLICACAO_ADR_APROVADA_COM_OBSERVACOES
proxima_categoria: CRIAR_HANDOFF
```
