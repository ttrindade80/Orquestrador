---
name: RELATORIO_QA_APLICACAO_ADR-0025
description: Auditoria documental independente da aplicacao da ADR-0025 nos documentos normativos ativos
metadata:
  type: relatorio_qa_aplicacao_adr
  ciclo: QA_APLICACAO_ADR
  adr_auditada: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  relatorio_aplicacao: docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  status_literal: BLOCKED_DOCUMENTATION
  status_normalizado: DOCUMENTACAO_BLOQUEADA
  causa: BLOCKED_USER_DECISION
  data: "2026-07-16"
---

# Relatorio QA da aplicacao da ADR-0025

## 1. Identificacao

Etapa executada:

```text
QA_APLICACAO_ADR
```

Etapa auditada:

```text
APLICAR_ADR - ADR-0025
```

Relatorio criado:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
```

## 2. Objetivo

Auditar documentalmente se a ADR-0025 foi aplicada aos documentos normativos
ativos de forma integral, fiel, sem decisao nova nao autorizada, sem
contradicao ativa, sem implementacao antecipada e sem arquivos fora do escopo.

Esta auditoria nao corrige documentos, nao altera contratos, nao altera a ADR,
nao cria handoff, nao implementa, nao cria JSONs, nao altera demos e nao prepara
commit.

## 3. ADR e QAs de entrada

ADR auditada:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
```

Relatorios de entrada lidos:

```text
docs/relatorios/RELATORIO_QA_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
```

Estado de entrada declarado pelo QA pos-patch:

```yaml
status_literal: ADR_APPROVED_WITH_NOTES
status_normalizado: ADR_APROVADA_COM_OBSERVACOES
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 3
decisoes_ausentes: 0
contradicoes_documentais: 0
proxima_categoria: APLICAR_ADR
```

## 4. Relatorio de aplicacao

Relatorio auditado:

```text
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
```

O relatorio de aplicacao declara:

```yaml
ciclo: APLICAR_ADR
adr: ADR-0025
status_saida: APLICACAO_CONCLUIDA
arquivos_modificados: 9
arquivos_criados: 1
decisoes_editoriais: 7
pendencias_mantidas: 5
proxima_categoria: null
```

## 5. Arquivos lidos

Arquivos obrigatorios lidos integralmente:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_QA_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_lancador.md
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
docs/adr/ADR-0023-largura-minima-funcional-lancador.md
docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
```

ADRs ativas adicionais localizadas pelo indice e materialmente consultadas por
meio dos contratos e remissoes lidas: ADR-0001, ADR-0002, ADR-0003, ADR-0015,
ADR-0017, ADR-0018, ADR-0019 e ADR-0020.

## 6. Estado Git inicial

`git status --short` antes da criacao deste relatorio:

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
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
```

Arquivos rastreados modificados: 8.

Arquivos nao rastreados no estado inicial: 4.

Arquivos no stage:

```text
nenhum
```

Arquivos inesperados fora de `docs/`:

```text
nenhum
```

Para todos os arquivos nao rastreados, quando nao houver evidencia de origem:

```yaml
origem: NAO_CONFIRMADA
produzido_pelo_executor: NAO_CONFIRMADO
produzido_pelo_usuario: NAO_CONFIRMADO
```

## 7. Diff e arquivos reais

`git diff --stat` retornou:

```text
docs/NOMENCLATURA.md                        |  87 +++++++++++++++++++
docs/adr/INDICE_ADR.md                      |   1 +
docs/contratos/contrato_composicao_corpo.md |  53 ++++++++++++
docs/contratos/contrato_json_console.md     |  96 +++++++++++++++++++++
docs/contratos/contrato_json_dashboard.md   | 116 +++++++++++++++++++++++++
docs/contratos/contrato_json_lancador.md    | 110 ++++++++++++++++++++++++
docs/contratos/contrato_lancador.md         |  67 +++++++++++++++
docs/contratos/contrato_tela_json.md        | 127 ++++++++++++++++++++++++++++
8 files changed, 657 insertions(+)
```

`git diff --name-only` retornou os mesmos 8 arquivos rastreados.

`git diff --check` retornou saida vazia para o diff rastreado.

`git diff --cached --name-only` retornou saida vazia.

Inspecao direta de nao rastreados por `git diff --no-index --stat`:

```yaml
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md: 1203 insertions
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md: 359 insertions
docs/relatorios/RELATORIO_QA_ADR-0025.md: 363 insertions
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md: 465 insertions
```

`git diff --no-index --check /dev/null` retornou saida vazia para ADR-0025 e
para os dois relatorios QA de entrada. Para o relatorio de aplicacao, retornou
trailing whitespace nas linhas 14 a 29.

## 8. Resolucao da divergencia 8 versus 9

Pelo estado Git real antes deste relatorio:

```yaml
quantidade_real_de_documentos_modificados_rastreados: 8
quantidade_real_de_documentos_nao_rastreados: 4
lista_real_modificados_rastreados:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_json_dashboard.md
  - docs/contratos/contrato_json_lancador.md
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_tela_json.md
lista_real_nao_rastreados:
  - docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_ADR-0025.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
```

Comparacao:

```yaml
retorno_yaml_do_prompt:
  modificados: 8
  criados: 1
retorno_tabela_do_prompt:
  documentos_modificados_listados: 9
  documentos_criados_listados: 1
relatorio_aplicacao_atual:
  arquivos_modificados: 9
  arquivos_criados: 1
diff_git_rastreado:
  modificados: 8
  criados: 0
status_git_incluindo_nao_rastreados:
  modificados_rastreados: 8
  nao_rastreados: 4
```

Classificacao:

```yaml
resultado: divergencia_entre_relatorio_e_diff
impacto: |
  O diff rastreado confirma 8 documentos modificados. A tabela do relatorio de
  aplicacao lista 9 documentos alterados porque inclui a ADR-0025, mas a ADR
  esta nao rastreada no Git e nao aparece como modificacao rastreada. O erro
  8 versus 9 citado no prompt nao existe literalmente no resumo atual do
  relatorio de aplicacao, que declara 9, mas a contagem continua nao
  reconciliada com o estado Git material.
```

## 9. Analise das sete decisoes editoriais

O relatorio de aplicacao declara `decisoes_editoriais: 7`, mas a lista nominal
tem oito decisoes, numeradas de 4.1 a 4.8.

Classificacao independente:

| Item | Documento | Classificacao | Autoridade | Conforme |
|---|---|---|---|---|
| Nome do campo `distribuicao_matricial` | relatorio de aplicacao, secao 4.1 | SEMANTICA | ADR-0025 autorizou escolher nomes em APLICAR_ADR | sim, mas nao editorial |
| Valores de `formacao.politica` | secao 4.2 | SEMANTICA | ADR-0025, secoes 15 e 41 | sim, mas nao editorial |
| Valores de distribuicao horizontal/vertical | secao 4.3 | SEMANTICA | ADR-0025, secoes 22, 23 e 41 | sim, mas nao editorial |
| Valores de `ordem_expansao` | secao 4.4 | SEMANTICA | ADR-0025, secao 25 | sim, mas nao editorial |
| Valores de `politica_resto` | secao 4.5 | SEMANTICA | ADR-0025, secao 26 | sim, mas nao editorial |
| Valores de dimensionamento | secao 4.6 | SEMANTICA | ADR-0025, secao 20 | parcialmente; `minimo_fixo` ficou incompleto |
| Valores de alinhamento interno | secao 4.7 | SEMANTICA | ADR-0025, secao 27 | sim, mas nao editorial |
| Reconciliacao terminologica do fallback | secao 4.8 | SEMANTICA | ADR-0025, secao 29, ADR-0017 e ADR-0023 | sim, mas nao editorial |

Conclusao: nenhuma das decisoes listadas e puramente editorial pelos criterios
desta auditoria. Elas alteram ou fecham vocabulario, estrutura declarativa ou
semantica. A maioria estava autorizada pela ADR-0025, mas a classificacao
`editorial` e a contagem 7 sao materialmente imprecisas.

## 10. Fidelidade a ADR-0025

Preservado:

```yaml
distribuicao_matricial_configuravel_nivel_unico: sim
configuracao_no_json_do_elemento_organizador: sim
participantes_imediatos: sim
preferencia_por_linhas: sim
preferencia_por_colunas: sim
matriz_fixa: sim
ordem_por_linha: sim
ordem_por_coluna: sim
separacao_formacao_ordem_dimensionamento_distribuicao_alinhamento: sim
eixos_independentes: sim
minimos_inviolaveis: sim
maximos_opcionais: sim
distribuicao_deterministica: parcialmente
tratamento_deterministico_dos_restos: sim
cardinalidade_unitaria: sim
terminal_pequeno: sim
recuperacao_deterministica: sim
ausencia_de_paginacao_na_capacidade: sim
ausencia_de_semantica_multinivel: sim
ausencia_de_migracao_automatica: sim
demo_e_jsons_de_teste_como_obrigacoes_futuras: sim
```

Nao preservado integralmente:

```yaml
tratamento_de_participante_maior_que_dimensao_fixa: nao_definido
reconciliacao_lancador_quando_distribuicao_matricial_presente: nao_definida
reconciliacao_console_quando_distribuicao_matricial_presente: nao_definida
```

## 11. Estrutura JSON

Campo formalizado:

```text
distribuicao_matricial
```

Local:

```text
corpo.elementos[] > elemento funcional > distribuicao_matricial
```

Comparacao dos contratos especificos:

```yaml
dashboard:
  define_tabela_normativa: sim
  quantidade_real_de_linhas_de_campo: 26
console:
  remete_ao_dashboard_secao_9_2: sim
  divergencia_de_nome: nao
lancador:
  remete_ao_dashboard_secao_9_2: sim
  divergencia_de_nome: nao
```

O relatorio de aplicacao declara "tabela de 24 campos", mas a tabela real em
`contrato_json_dashboard.md` possui 26 linhas de campo, de
`formacao.politica` ate `alinhamento_interno.vertical`.

## 12. Vocabulario

O vocabulario usa `snake_case` e e consistente entre os tres contratos
especificos por remissao ao contrato do dashboard.

Nao foram encontrados sinonimos concorrentes para o campo principal. A
NOMENCLATURA distingue:

- `distribuicao_matricial` de `distribuicao`;
- `matriz de grupos` de distribuicao matricial de elemento funcional;
- margem interna de espaco externo proibido;
- nivel unico de multinivel.

## 13. Validacoes

Validacoes cobertas:

```yaml
campos_desconhecidos: rejeicao_controlada
campos_sempre_obrigatorios_quando_estrutura_presente: definido
valores_fechados: definido
minimo_e_maximo: parcialmente_definido
linhas_e_colunas: parcialmente_definido
cardinalidade_unitaria: coberta_por_politica_resto_e_fallback
restos_inteiros: coberto_por_politica_resto
combinacoes_contraditorias: parcialmente_definidas
```

Lacuna bloqueante: o contrato admite `dimensionamento.*.politica =
"minimo_fixo"` e exige `dimensionamento.*.minimo`, mas nao define o que ocorre
quando o participante exige dimensao maior que a dimensao fixa. A ADR-0025
exigia que o contrato JSON declarasse esse tratamento e proibiu comportamento
implicito.

## 14. Nivel unico

Conforme. A aplicacao declara que `distribuicao_matricial` organiza somente
participantes imediatos do elemento declarante, sem recursao, heranca, cascata
ou propagacao entre niveis.

## 15. Ausencia de paginacao

Conforme para a capacidade da ADR-0025. Ocorrencias de paginacao permanecem em
politicas ativas do `console` e da composicao de corpo, mas a nova capacidade
declara explicitamente que nao define paginacao do conjunto de participantes.

## 16. Ausencia de multinivel

Conforme. A ADR, a NOMENCLATURA e `contrato_tela_json.md` mantem multinivel,
recursao, heranca e cascata fora do escopo.

## 17. Fallback

Conforme quanto a terminologia. A aplicacao reconciliou:

```yaml
terminal_muito_pequeno: condicao_geometrica
quadro_minimo_de_terminal_pequeno: estado_canonico_exibido
fallback_concorrente: nao
recuperacao_deterministica: preservada
```

## 18. Compatibilidade

```yaml
jsons_antigos_mudam_sem_declaracao: false
migracao_automatica: false
reescrita_automatica: false
aplicacao_recursiva: false
defaults_estruturais_novos: false
campos_desconhecidos: definido_conforme_politica_ativa
configuracoes_invalidas: rejeicao_controlada
```

Ressalva: configuracoes novas que usem `minimo_fixo`, ou que declarem
`distribuicao_matricial` em `lancador` ou `console` com sobreposicoes
especificas, ainda exigem decisao normativa para interpretacao completa.

## 19. Analise por documento

### ADR-0025

Status atualizado para `aceita e aplicada`. Nao foi localizada autoafirmacao
de QA da aplicacao. A mudanca de status e coerente com a aplicacao, mas o
arquivo esta nao rastreado no Git, portanto o diff rastreado nao comprova uma
modificacao sobre base versionada.

### INDICE_ADR.md

Entrada ADR-0025 presente, titulo fiel e status `aceita e aplicada`. Nao foram
localizadas alteracoes indevidas de entradas historicas no diff apresentado.

### NOMENCLATURA.md

Termos canonicos adicionados. A reconciliacao entre "terminal muito pequeno" e
`quadro minimo de terminal pequeno` esta clara. Multinivel permanece futuro.

### contrato_tela_json.md

Define local declarativo, elementos autorizados, nivel unico, compatibilidade,
ausencia de paginacao e fallback. Conforme, com remissao aos contratos
especificos.

### contrato_composicao_corpo.md

Preserva a arvore hierarquica, a composicao por `grupo`, a ocupacao integral e
a distincao entre margem interna e espaco externo proibido. Conforme.

### contrato_lancador.md

Preserva politicas especificas quando `distribuicao_matricial` esta ausente.
Nao fecha a reconciliacao quando o campo esta presente. Isso deixa decisao
normativa pendente para configuracao nova explicitamente admitida.

### contrato_json_dashboard.md

Formaliza a estrutura principal. Mantem pendencia de alinhamento horizontal do
dashboard e nao resolve `minimo_fixo` excedido.

### contrato_json_console.md

Remete ao vocabulario do dashboard. Declara coexistencia entre politicas do
console e `distribuicao_matricial`, mas deixa a reconciliacao para contratos de
conteudo e handoff futuro.

### contrato_json_lancador.md

Remete ao vocabulario do dashboard. Mapeia sobreposicoes com ADR-0001, ADR-0002
e ADR-0003, mas declara a reconciliacao como pendencia futura.

## 20. Reconciliacao de dashboard

Estado:

```yaml
alinhamento_horizontal_dashboard: FUTURA_NAO_BLOQUEANTE
impacto_na_aplicacao: medio
correcao_necessaria_antes_da_aprovacao: nao_isoladamente
```

A pendencia preexistente foi delimitada e nao substitui silenciosamente a
politica antiga. Entretanto, qualquer uso concreto de `distribuicao_matricial`
em dashboard com alinhamento interno devera evitar dupla autoridade com a
politica antiga de alinhamento.

## 21. Reconciliacao de console

Estado:

```yaml
reconciliacao_console_politicas_especificas: DECISAO_AUSENTE
documentos_afetados:
  - docs/contratos/contrato_json_console.md
impacto_na_aplicacao: alto
correcao_necessaria_antes_da_aprovacao: sim
```

O contrato declara que as politicas especificas do `console` coexistem com
`distribuicao_matricial` e nao sao substituidas. Tambem declara que a
reconciliacao de vaos, alinhamento de colunas e numero de colunas ajustavel
pertence a contratos de conteudo e handoff futuro. Para uma configuracao nova
que declare a estrutura, falta precedencia normativa suficiente.

## 22. Reconciliacao de lancador

Estado:

```yaml
reconciliacao_lancador_adr_0001_0002_0003: DECISAO_AUSENTE
documentos_afetados:
  - docs/contratos/contrato_lancador.md
  - docs/contratos/contrato_json_lancador.md
impacto_na_aplicacao: alto
correcao_necessaria_antes_da_aprovacao: sim
```

O contrato preserva ADR-0001, ADR-0002 e ADR-0003 quando o campo esta ausente,
mas, quando `distribuicao_matricial` esta presente, ainda e necessario mapear
ou substituir algoritmo automatico, sobra a direita e vaos elasticos. A nova
estrutura admite uma configuracao que os contratos ainda nao conseguem
interpretar integralmente.

## 23. Divergencia H-0034

Estado:

```yaml
divergencia_h_0034: FUTURA_NAO_BLOQUEANTE
impacto_na_aplicacao: baixo
correcao_necessaria_antes_da_aprovacao: nao
```

A divergencia do H-0034 nao foi corrigida silenciosamente. A aplicacao preserva
o ciclo corretivo separado.

## 24. Pendencias mantidas

```yaml
reconciliacao_lancador_adr_0001_0002_0003:
  estado: DECISAO_AUSENTE
  correcao_necessaria_antes_da_aprovacao: sim
divergencia_h_0034:
  estado: FUTURA_NAO_BLOQUEANTE
  correcao_necessaria_antes_da_aprovacao: nao
alinhamento_horizontal_dashboard:
  estado: FUTURA_NAO_BLOQUEANTE
  correcao_necessaria_antes_da_aprovacao: nao_isoladamente
comportamento_minimo_fixo_excedido:
  estado: DECISAO_AUSENTE
  correcao_necessaria_antes_da_aprovacao: sim
reconciliacao_console_politicas_especificas:
  estado: DECISAO_AUSENTE
  correcao_necessaria_antes_da_aprovacao: sim
```

## 25. Demo e produto

Conforme.

```yaml
demo_dedicado_futuro_preservado: true
demo_criado: false
nome_definitivo_definido: false
comando_definitivo_definido: false
uso_do_ponto_de_entrada_do_produto_obrigado: false
ponto_de_entrada_real_interpretacao: metodo_real_do_artefato_demonstrado
adr_0021_preservada: true
adr_0022_preservada: true
```

## 26. Busca de residuos

Busca executada nos documentos alterados por:

```text
paginacao
paginação
multinivel
multinível
recursao
recursão
heranca
herança
cascata
terminal muito pequeno
quadro minimo
quadro mínimo
matriz de grupos
distribuicao_matricial
distribuição matricial
ponto de entrada real
ponto de entrada do sistema
default
padrao
padrão
automatico
automático
```

Resultado: as ocorrencias de paginacao, defaults, matriz de grupos e ponto de
entrada real em secoes anteriores sao historicas ou pertencem a politicas
ativas de outros dominios. As ocorrencias novas da ADR-0025 preservam a
exclusao de paginacao e multinivel. A ocorrencia de "ponto de entrada real" em
NOMENCLATURA pertence a ADR-0022 e nao vincula o demo da ADR-0025 ao produto
real.

## 27. Fidelidade do relatorio

Divergencias materiais identificadas:

```yaml
contagem_8_versus_9:
  classificacao: divergencia_entre_relatorio_e_diff
decisoes_editoriais:
  declarado: 7
  lista_real: 8
  editoriais_confirmadas: 0
  semanticas_identificadas: 8
estrutura_json:
  quantidade_de_campos_declarada: 24
  quantidade_real_na_tabela: 26
git_diff_check:
  rastreado: limpo
  relatorio_aplicacao_nao_rastreado: trailing_whitespace
```

## 28. Achados

```yaml
- id: QA-APP-ADR0025-BLOQ-001
  severidade: bloqueante
  arquivo: docs/contratos/contrato_json_dashboard.md
  secao: "9.2 Vocabulário de campos"
  evidencia: "A tabela admite dimensionamento.*.politica = minimo_fixo, mas nao define o comportamento quando participante exige dimensao maior que o minimo/fixo."
  regra_ou_decisao_violada: "ADR-0025 secao 20: o contrato JSON devera declarar como tratar participante que exige dimensao maior que dimensao fixa; nao deve existir comportamento implicito."
  impacto: "Configuracao valida pela tabela nao pode ser interpretada de forma deterministica sem nova decisao."
  correcao_necessaria: "Decisao normativa sobre crescimento, tratamento interno ou invalidacao da formacao."
  exige_decisao_do_usuario: true
  causa: BLOCKED_USER_DECISION

- id: QA-APP-ADR0025-ALTO-001
  severidade: alto
  arquivo: docs/contratos/contrato_lancador.md
  secao: "11.3 Reconciliação futura necessária"
  evidencia: "Quando o lancador adotar distribuicao_matricial explicitamente, ainda sera necessario mapear ou substituir algoritmo automatico, sobra a direita e vaos elasticos."
  regra_ou_decisao_violada: "A aplicacao deveria reconciliar contratos especificos de lancador."
  impacto: "Configuracao nova com distribuicao_matricial no lancador fica sem precedencia normativa suficiente."
  correcao_necessaria: "Fechar a precedencia ou bloquear formalmente o uso no lancador ate ciclo proprio."
  exige_decisao_do_usuario: true

- id: QA-APP-ADR0025-ALTO-002
  severidade: alto
  arquivo: docs/contratos/contrato_json_console.md
  secao: "10.3 Relação com políticas existentes do console"
  evidencia: "O contrato declara coexistencia sem substituicao e remete reconciliacao de vaos, alinhamento e colunas a contratos de conteudo e handoff futuro."
  regra_ou_decisao_violada: "A aplicacao deveria evitar duas politicas simultaneas sem precedencia."
  impacto: "Configuracao nova com distribuicao_matricial no console pode ficar ambigua."
  correcao_necessaria: "Definir precedencia, fronteira ou bloqueio de uso ate contrato de conteudo."
  exige_decisao_do_usuario: true

- id: QA-APP-ADR0025-MEDIO-001
  severidade: medio
  arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  secao: "4 e 8"
  evidencia: "O resumo declara decisoes_editoriais: 7, mas a lista possui 8 decisoes, todas semanticas pelos criterios desta auditoria."
  regra_ou_decisao_violada: "Fidelidade do relatorio de aplicacao."
  impacto: "O relatorio subestima e classifica incorretamente decisoes de vocabulario e estrutura."
  correcao_necessaria: "Corrigir contagem e classificacao em ciclo autorizado."
  exige_decisao_do_usuario: false

- id: QA-APP-ADR0025-BAIXO-001
  severidade: baixo
  arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  secao: "3.7"
  evidencia: "O relatorio declara tabela de 24 campos; a tabela real possui 26 linhas de campo."
  regra_ou_decisao_violada: "Fidelidade do relatorio de aplicacao."
  impacto: "Contagem de estrutura JSON imprecisa."
  correcao_necessaria: "Corrigir contagem ou criterio de contagem."
  exige_decisao_do_usuario: false

- id: QA-APP-ADR0025-BAIXO-002
  severidade: baixo
  arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
  secao: "linhas 14-29"
  evidencia: "git diff --no-index --check apontou trailing whitespace no relatorio de aplicacao."
  regra_ou_decisao_violada: "Higiene documental e fidelidade do estado Git."
  impacto: "Defeito mecanico corrigivel no artefato criado."
  correcao_necessaria: "Remover whitespace em ciclo autorizado."
  exige_decisao_do_usuario: false
```

## 29. Observacoes

```yaml
- id: OBS-QA-APP-ADR0025-001
  descricao: "A reconciliacao terminologica do fallback esta coerente."
- id: OBS-QA-APP-ADR0025-002
  descricao: "Paginacao e multinivel permanecem fora do escopo da nova capacidade."
- id: OBS-QA-APP-ADR0025-003
  descricao: "Demo dedicado e JSONs de teste permanecem futuros e nao foram criados."
- id: OBS-QA-APP-ADR0025-004
  descricao: "Nao houve alteracao em config/, demo/ ou tela/ no estado Git inicial."
- id: OBS-QA-APP-ADR0025-005
  descricao: "A divergencia H-0034 foi preservada como ciclo separado."
```

## 30. Conclusao

A aplicacao propagou a estrutura principal da ADR-0025 aos documentos
normativos autorizados e preservou compatibilidade de JSONs antigos,
nivel unico, ausencia de paginacao, ausencia de multinivel e fallback
canonico.

Entretanto, a aplicacao nao pode ser aprovada porque a estrutura aceita
configuracoes novas que ainda dependem de decisao normativa para serem
interpretadas: `minimo_fixo` excedido, reconciliacao do `lancador` com
ADR-0001/0002/0003 e reconciliacao do `console` com politicas especificas.

O caso de `minimo_fixo` e bloqueante porque a ADR-0025 exigiu que os contratos
declarassem o tratamento de participante maior que dimensao fixa e proibiu
comportamento implicito.

## 31. Status literal

```text
BLOCKED_DOCUMENTATION
```

## 32. Status normalizado e proxima categoria

```yaml
status_normalizado: DOCUMENTACAO_BLOQUEADA
causa: BLOCKED_USER_DECISION
proxima_categoria: DECISAO_DOCUMENTAL
```
