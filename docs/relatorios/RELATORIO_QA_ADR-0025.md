---
name: RELATORIO_QA_ADR-0025
description: Auditoria documental independente da ADR-0025 sobre distribuicao matricial configuravel de nivel unico do conteudo dos elementos
metadata:
  type: relatorio_qa_adr
  adr_auditada: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  status_literal: ADR_REJECTED
  status_normalizado: ADR_REJEITADA
  data: "2026-07-16"
---

# Relatorio QA ADR-0025

## 1. Identificacao

Auditoria documental independente da ADR:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
```

Relatorio criado:

```text
docs/relatorios/RELATORIO_QA_ADR-0025.md
```

Estado normalizado de entrada:

```text
ADR_EM_QA
```

## 2. Objetivo da auditoria

Verificar se a ADR-0025 e fiel as decisoes explicitas do usuario, coerente com
as autoridades documentais ativas, limitada ao nivel unico, sem paginacao, sem
semantica multinivel, sem schema JSON final, sem valores universais e sem
antecipar implementacao, telas, demos ou aplicacao documental.

## 3. Arquivos lidos

Arquivos obrigatorios lidos:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_lancador.md
```

ADRs ativas materialmente relacionadas, localizadas por `docs/adr/INDICE_ADR.md`
e lidas:

```text
docs/adr/ADR-0001-menu-suporta-matriz.md
docs/adr/ADR-0002-menu-sobra-direita.md
docs/adr/ADR-0003-vaos-elasticos-menu.md
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0017-redimensionamento-reativo-tui.md
docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
docs/adr/ADR-0023-largura-minima-funcional-lancador.md
docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
```

Observacao: `ADR-0018` tem status local `proposta` no arquivo, mas aparece como
`aceita` no indice ativo; para esta auditoria, foi tratada como ativa por
autoridade do indice.

## 4. Estado Git observado

Antes da criacao deste relatorio, `git status --short` retornou:

```text
?? docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
```

Arquivos modificados rastreados: nenhum observado.

Arquivos nao rastreados antes do relatorio:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
```

O arquivo da ADR e o unico artefato material observado da etapa declarada
`CRIAR_ADR`. Nao foram observadas outras mudancas materiais inesperadas antes
da criacao deste relatorio.

## 5. Diff auditado

Comandos obrigatorios inspecionados:

```text
git status --short
git diff -- docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
git diff --check
```

Resultados:

- `git diff -- docs/adr/ADR-0025-...md` nao exibiu diff porque o arquivo esta
  nao rastreado.
- `git diff --check` nao reportou defeitos de whitespace em arquivos rastreados.
- Foi feita verificacao mecanica adicional com `git diff --no-index --check
  /dev/null docs/adr/ADR-0025-...md`; nao houve saida de erro de whitespace.

## 6. Decisoes explicitas usadas como autoridade

A ADR deveria preservar as decisoes explicitadas no pedido:

- capacidade generica adotavel por configuracao explicita por `dashboard`,
  `console`, `lancador` e elementos compativeis futuros;
- parametros concretos no JSON do elemento que organiza diretamente o conteudo;
- separacao entre ADR, aplicacao documental, implementacao, telas de teste e demo;
- nivel unico, sem recursao, cascata, heranca, achatamento ou propagacao;
- compatibilidade futura com multinivel sem defini-lo;
- paginacao fora do escopo;
- fallback canonico de terminal muito pequeno sem perda, duplicacao,
  truncamento, sobreposicao, reducao silenciosa de minimos ou renderizacao parcial;
- suporte a preferencia por linhas, preferencia por colunas e matriz fixa;
- independencia entre formacao, ordem, dimensionamento, distribuicao,
  alinhamento e fallback;
- minimos, maximos opcionais, distribuicao de sobra e restos inteiros
  deterministicos;
- familias futuras de telas de teste sem nomes finais ou valores universais;
- demo dedicado futuro, separado do demo principal, com nome e estrutura
  deixados para handoff futuro.

## 7. Analise de fidelidade

A ADR e majoritariamente fiel: declara capacidade generica, adocao explicita,
ausencia de migracao automatica, ausencia de schema final, ausencia de nomes de
campos definitivos e ausencia de valores universais.

Ha duas falhas documentais materiais:

- a ADR afirma que o indice confirma o identificador ADR-0025, mas o indice lido
  ainda termina em ADR-0024;
- a ADR transforma o futuro demo dedicado em obrigacao de usar o "ponto de
  entrada real do sistema", detalhe nao decidido no pedido e potencialmente
  concorrente com a separacao entre demonstracao e produto real.

## 8. Analise de nivel unico

A ADR define nivel unico de forma verificavel: uma area de distribuicao, um
conjunto ordenado de participantes imediatos e calculo local de formacao,
margens, vaos, dimensoes e alinhamento.

Ela proibe explicitamente achatamento, recursao, heranca, cascata, combinacao
de margens ou vaos entre niveis e propagacao de fallback entre niveis. Nao foi
identificada contradicao interna material nesse ponto.

## 9. Analise de compatibilidade futura com multinivel

A ADR preserva a possibilidade futura de um participante conter organizacao
interna propria, mantendo-o como uma unica unidade perante o nivel externo.
Tambem declara que semantica multinivel, ordem de calculo entre niveis,
heranca, cascata e propagacao de fallback exigirao decisao futura.

Nao ha definicao indevida de multinivel.

## 10. Analise da ausencia de paginacao

A ADR exclui paginacao de modo expresso e lista capacidade por pagina, divisao,
navegacao, controles, indicadores e metadados como fora do escopo. Nao foi
identificada definicao de paginacao para a nova capacidade.

## 11. Analise do fallback de terminal pequeno

A ADR preserva o fallback canonico quando nenhuma formacao valida comporta todos
os participantes e minimos. Ela proibe paginas, ocultacao, truncamento,
perda, duplicacao, sobreposicao, reducao de minimos, coordenadas negativas,
alteracao automatica da configuracao e renderizacao invalida.

O texto reconhece a necessidade de reconciliar o nome tecnico com `quadro minimo
de terminal pequeno` e com o fallback global do `lancador`. Isso e compativel
com ADR-0017, ADR-0023 e NOMENCLATURA.

## 12. Analise dos parametros no JSON do elemento

A ADR declara que os parametros de organizacao pertencem ao JSON do elemento que
organiza diretamente o conteudo daquele nivel. Tambem posterga nomes finais,
estrutura sintatica e validacoes para contratos posteriores.

Nao foram encontrados valores universais para `dashboard`, `console` ou
`lancador`.

## 13. Analise da separacao entre ADR e telas

A ADR separa decisao abstrata, aplicacao documental, loader/modelo/renderizador,
telas de teste e demo dedicado. Ela nao cria telas, JSONs, demo, contratos ou
handoff.

A ressalva e o achado QA-ADR0025-ALTO-001: a secao de demo avanca uma obrigacao
concreta de ponto de entrada que nao foi autorizada nesta decisao.

## 14. Analise do demo dedicado

A ADR registra corretamente a consequencia futura de um demo dedicado separado
do demo principal. Porem, ao exigir que esse demo "use o ponto de entrada real do
sistema", fixa uma direcao que o pedido reservou ao handoff futuro e que deve ser
reconciliada com ADR-0021/ADR-0022 antes de virar norma.

## 15. Analise das familias de testes

A ADR inclui as familias minimas solicitadas: preferencia por linhas, preferencia
por colunas, matriz fixa, centralizacao, margens horizontais e verticais,
distribuicao uniforme, cardinalidade unitaria e conjunto de tres ou quatro
participantes. A ADR nao transforma esses casos em nomes definitivos de arquivos.

## 16. Analise de coerencia interna

Os termos `elemento`, `participante`, `celula`, `linha`, `coluna`, `margem` e
`vao` sao usados de modo suficientemente consistente. Formacao e ordem de
preenchimento sao distinguidas; alinhamento global e alinhamento interno tambem.

Minimos e maximos possuem relacao coerente, sobra negativa torna formacao
invalida, cardinalidade unitaria e restos inteiros recebem exigencia
deterministica.

O principal problema de coerencia documental nao e semantico do algoritmo, mas
de rastreabilidade: a secao de documentos consultados atribui ao indice uma
confirmacao que ele nao fornece.

## 17. Analise de autoridade

A ADR complementa a composicao hierarquica do corpo (ADR-0015, ADR-0019) sem
substitui-la. Preserva a matriz declarativa de grupos (ADR-0020) como outra
camada: grupo estrutural na arvore de corpo, nao conteudo interno de elemento.

Preserva a ocupacao integral do corpo (ADR-0024) ao tratar margens como internas
ao elemento. Nao altera automaticamente politicas especificas de `lancador`,
`console` ou `dashboard`; reconhece a necessidade de reconciliacao documental.

O contrato ativo do `lancador` ainda contem algoritmo automatico de fila/matriz,
parametros transicionais em `config/elementos/lancador.json` e fallback global.
A ADR-0025 nao os substitui; por isso nao ha conflito arquitetural imediato, mas
ha necessidade real de reconciliacao em `APLICAR_ADR`.

## 18. Relacao com ADRs anteriores

Relacao verificada:

- ADR-0001, ADR-0002, ADR-0003: preservadas como politicas especificas do
  `lancador`; exigem mapeamento futuro para a capacidade generica.
- ADR-0010, ADR-0015, ADR-0019: preservadas; ADR-0025 opera dentro de elemento,
  nao na arvore de composicao do corpo.
- ADR-0017, ADR-0023: preservadas; fallback exige reconciliacao terminologica e
  de alcance.
- ADR-0020: complementada; matriz de grupos nao e a mesma coisa que distribuicao
  matricial de participantes internos de elemento.
- ADR-0021, ADR-0022: relevantes para o achado sobre demo e ponto de entrada.
- ADR-0024: preservada; margens internas nao reabrem preenchimento externo do corpo.

## 19. Documentos afetados

Documentos corretamente identificados como afetados para futura aplicacao:

```text
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_lancador.md
```

Nao foi exigida inclusao de arquivo adicional apenas por proximidade tematica.
ADR-0017, ADR-0021, ADR-0022, ADR-0023 e ADR-0024 foram autoridades consultadas,
nao necessariamente documentos a alterar pela aplicacao da ADR-0025.

## 20. Achados

```yaml
- id: QA-ADR0025-ALTO-001
  severidade: alto
  arquivo: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  secao: "36. Demo dedicado futuro"
  evidencia: "Linhas 947-955 exigem que o demo dedicado futuro use o ponto de entrada real do sistema."
  regra_ou_decisao_violada: "A decisao explicita autorizou registrar demo dedicado futuro separado do demo principal, mas reservou nome e estrutura concretos ao futuro handoff; ADR-0021 separa demonstracao e produto real; ADR-0022 define orquestrador.py como ponto de entrada do produto real, nao da demonstracao."
  impacto: "A ADR antecipa uma obrigacao concreta para o demo e pode criar concorrencia documental com a separacao entre aplicacao demonstrativa e produto real."
  correcao_necessaria: "Remover ou reescrever a obrigacao para limitar a ADR a registrar a necessidade futura de demo dedicado, deixando ponto de entrada, estrutura e nome para o handoff."
  exige_decisao_do_usuario: false

- id: QA-ADR0025-MEDIO-001
  severidade: medio
  arquivo: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  secao: "34. Contratos e documentos afetados"
  evidencia: "A linha 859 declara `docs/adr/INDICE_ADR.md` como confirmacao do identificador ADR-0025, mas o indice lido lista ADR-0001 a ADR-0024 e ainda nao registra ADR-0025."
  regra_ou_decisao_violada: "Rastreabilidade documental e verificacao obrigatoria por autoridade ativa; o retorno da criacao nao substitui a inspecao do arquivo e das autoridades."
  impacto: "O texto atribui ao indice uma evidencia que nao existe, criando registro documental falso ainda que corrigivel."
  correcao_necessaria: "Alterar a descricao do papel do indice para refletir o estado real: indice consultado e pendente de atualizacao em APLICAR_ADR, sem afirmar confirmacao do identificador."
  exige_decisao_do_usuario: false
```

## 21. Observacoes

```yaml
- id: OBS-ADR0025-001
  severidade: observacao
  arquivo: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  secao: "33. Aplicacao a dashboard, console e lancador"
  evidencia: "A ADR reconhece possiveis contradicoes com regras especificas de lancador e console e remete a reconciliacao a APLICAR_ADR."
  regra_ou_decisao_violada: null
  impacto: "Nao bloqueia a ADR, mas deve ser tratado como item real de aplicacao documental, especialmente diante do contrato_lancador.md secoes 6.1 a 6.5."
  correcao_necessaria: "Nenhuma nesta ADR, salvo se a correcao dos achados alterar a secao."
  exige_decisao_do_usuario: false

- id: OBS-ADR0025-002
  severidade: observacao
  arquivo: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  secao: "29. Terminal muito pequeno"
  evidencia: "A ADR usa `terminal muito pequeno` e registra reconciliacao futura com `quadro minimo de terminal pequeno`."
  regra_ou_decisao_violada: null
  impacto: "A reconciliacao terminologica e necessaria em APLICAR_ADR, mas o texto nao cria variante local proibida."
  correcao_necessaria: "Nenhuma obrigatoria nesta ADR."
  exige_decisao_do_usuario: false
```

## 22. Conclusao

A ADR-0025 esta substantivamente alinhada ao escopo de nivel unico e preserva as
principais restricoes: sem schema final, sem valores universais, sem paginacao,
sem multinivel, sem migracao automatica e sem redefinicao silenciosa do
`lancador`.

Ainda assim, a auditoria rejeita a ADR na forma atual porque ha correcao
documental obrigatoria: uma obrigacao futura de demo sem autoridade suficiente
e uma afirmacao factual incorreta sobre o indice ADR. Os defeitos sao
corrigiveis na propria ADR e nao exigem nova decisao arquitetural.

## 23. Status literal

```text
ADR_REJECTED
```

## 24. Status normalizado

```text
ADR_REJEITADA
```

## 25. Proxima categoria permitida

```text
CORRIGIR_ADR
```
