# RELATORIO_QA_H-0026_HANDOFF

## 1. Identificacao

Etapa executada: `QA_HANDOFF`.

Data: 2026-07-11.

Papel: auditor formal do handoff H-0026, sem implementacao, sem correcao do
handoff, sem alteracao normativa, sem commit e sem stage.

## 2. Artefato auditado

Artefato principal:

```text
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
```

Evidencia de arquivo novo:

```text
wc -l docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
737 docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
```

`git diff --no-index /dev/null docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md`
retornou codigo 1, esperado para arquivo novo com conteudo.

## 3. Branch, commit e estado Git

Comandos obrigatorios executados no inicio do QA:

| Comando | Resultado |
|---|---|
| `git branch --show-current` | `master` |
| `git log -1 --oneline` | `1cc0dff feat: implementa distribuicao vertical explicita do corpo` |
| `git status --short` | tres arquivos/diretorios nao rastreados, listados na secao 4 |
| `git diff --stat` | sem saida |
| `git diff --cached --stat` | sem saida |

Estado confirmado: branch e commit batem com o informado; nao ha alteracao
rastreada fora do stage; stage vazio.

## 4. Arquivos nao rastreados

Estado real no inicio do QA:

```text
?? docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
?? tela/__pycache__/
```

Nenhum arquivo nao rastreado foi limpo, removido, movido ou adicionado ao stage.

## 5. Autoridades consultadas

Autoridades obrigatorias consultadas:

- `docs/NOMENCLATURA.md`: responsabilidade de schema/semantica, linhas 32-36; terminologia final `vertical`/`horizontal`, linhas 131-143.
- `docs/adr/INDICE_ADR.md`: ADR-0011, ADR-0015 e ADR-0018 aceitas, linhas 41, 45 e 48.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`: nomes finais e aliases, linhas 70-103; separacao frente a `barra_de_menus.distribuicao`, linhas 130-143.
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`: arranjo horizontal reparte largura, linhas 107-119; distribuicao por container, linhas 122-132; modos, cardinalidade, maiores restos, contato e preenchimento, linhas 136-246.
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`: ausencia nao equivale a `igual`, linhas 113-126; `percentual` e `fracao` genericos, linhas 160-193; preservacao da ADR-0015 salvo conflito, linhas 414-433.
- `docs/contratos/contrato_composicao_corpo.md`: contrato ativo e ADRs aplicadas, linhas 1-24; arranjo/distribuicao por container, linhas 269-310; ausencia e modos, linhas 531-588; maiores restos, linhas 618-638; preenchimento, linhas 642-659; R-17 a R-20, linhas 836-860.
- `docs/contratos/contrato_tela_json.md`: `corpo` e `grupo` podem declarar `distribuicao`, linhas 200-206; semantica de `corpo.distribuicao`, linhas 208-227.
- `docs/contratos/contrato_json_tela_minima.md`: `grupo` estrutural e exemplo horizontal, linhas 187-204; `distribuicao` opcional e modos explicitos, linhas 206-230.

Referencias historicas consultadas sem autoridade superior:

- `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`, linhas 40-57.
- `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md`, linhas 31-37 e 146-160.

Relatorio de levantamento consultado integralmente:

- `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md`, status final `L1_HORIZONTAL_DOCUMENTADO_HANDOFF_POSSIVEL`, linhas 319-321.

## 6. Metodologia

Foram executadas verificacoes de estado Git, leitura integral do handoff e do
levantamento, leitura das secoes aplicaveis das autoridades obrigatorias e
inspecao estatica dos arquivos de codigo/teste autorizados para conferencia de
implementabilidade.

Nao foi executada a suite completa, conforme limite da etapa. Nao houve alteracao
em codigo, testes, contratos, ADRs, nomenclatura, stage, stash, branch ou historico
Git.

## 7. Resumo do handoff

O handoff define uma unica capacidade: distribuicao explicita percentual e
fracionaria no corpo raiz horizontal. O escopo positivo aparece em
`docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md:71-80` e
`docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md:117-125`.

O handoff autoriza somente:

```text
tela/renderizador.py
tela/teste_renderizador.py
docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
```

conforme linhas 223-244, e classifica loader/modelo/testes respectivos como
somente leitura nas linhas 246-258.

## 8. Matriz de verificacao

| Verificacao | Resultado |
|---|---|
| Autoridade horizontal fechada | Conforme |
| Levantamento usado como evidencia, nao autoridade normativa | Conforme |
| Capacidade unica | Conforme |
| Regras de `percentual` e `fracao` | Conforme |
| Maiores restos, soma exata e desempate | Conforme |
| Preservacao do contato horizontal | Conforme |
| Preservacao operacional da ausencia | Conforme, com delimitacao correta |
| Arquivos permitidos minimos | Conforme |
| Liberdade tecnica local | Conforme |
| Criterios de aceite | Parcialmente conforme; achado H0026-QA-M01 |
| Estado Git documentado no handoff | Nao conforme; achado H0026-QA-A01 |
| Ausencia de implementacao antecipada | Conforme |

## 9. Analise de autoridade

O handoff cita autoridades atuais e aplicaveis: ADR-0015, ADR-0018 e contratos
ativos nas linhas 129-180. A regra horizontal nao foi importada indevidamente do
vertical: ADR-0015 define expressamente que container horizontal reparte
colunas/largura (`ADR-0015:122-132`) e o contrato ativo repete a regra
(`contrato_composicao_corpo.md:290-310`, R-17 em `836-844`).

O levantamento e citado como base de evidencia nas linhas 56-67 e 213-214, mas o
handoff preserva a ordem de autoridade ao listar ADRs e contratos como autoridades
normativas nas linhas 129-180.

A inconsistencia textual da ADR-0018 foi tratada como nao bloqueante: o indice a
marca como aceita (`INDICE_ADR.md:48`), o arquivo interno ainda diz `proposta`
(`ADR-0018:5-7`, `24-27`), e o levantamento registra que isso nao altera a
conclusao semantica horizontal (`RELATORIO_LEVANTAMENTO...:161-167`).

## 10. Analise de escopo positivo

O handoff exige calculo de larguras percentuais e fracionarias, associacao por
ordem declarada, maiores restos, soma exata e preservacao de contato horizontal
nas linhas 343-356 e 456-495.

Os modos estao fechados:

- `percentual`: linhas 458-465.
- `fracao`: linhas 467-474.
- algoritmo normativo: linhas 476-486.
- restricoes posicionais: linhas 488-495.

## 11. Analise de escopo negativo

O handoff exclui grupos horizontais, outros arranjos e distribuicao vertical nas
linhas 123-125, proibe alteracao de ADRs/contratos/nomenclatura/JSONs nas linhas
262-277 e deixa politica de conteudo maior que a cota fora do ciclo nas linhas
497-502 e 634-642.

## 12. Analise de arquivos permitidos e proibidos

A lista fechada de arquivos alteraveis e suficiente para a implementacao:

- `tela/renderizador.py`: contem o ramo horizontal e helpers existentes.
- `tela/teste_renderizador.py`: contem cobertura horizontal e vertical de regressao.
- `docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md`: relatorio esperado.

Loader e modelo estao corretamente classificados como somente leitura, pois:

- `tela/loader.py:443-448` valida `corpo.distribuicao` sempre que declarado,
  sem condicionar ao eixo.
- `tela/modelo.py:271-275` preserva `corpo.distribuicao`.

## 13. Analise por modulo

### Loader

Conforme. O loader aceita `corpo.arranjo = "horizontal"` e aliases
(`tela/loader.py:33-37`, `434-441`), valida modos `igual`, `percentual` e
`fracao` (`39-42`, `178-183`), cardinalidade (`197-203`), positividade
(`205-210`) e soma percentual 100 (`212-216`). Grupos horizontais continuam
rejeitados (`227-251`), como exige o escopo negativo.

### Modelo

Conforme. `Corpo.distribuicao` e `dict | None` (`tela/modelo.py:57-70`) e
`construir_modelo` copia `corpo_raw.get("distribuicao")` sem conversao
(`271-275`).

### Renderizador

Conforme. `_pesos_distribuicao` ja e generico (`tela/renderizador.py:203-216`).
`_distribuir_alturas` implementa maiores restos e desempate por ordem
(`219-254`). O caminho horizontal atual calcula `base_w` e `resto` uniformes e
ignora a distribuicao (`756-782`), e o despacho horizontal nao passa
`distribuicao_corpo` (`969-994`). A variavel existe em `966` e e usada apenas no
ramo vertical (`995-1040`).

### Testes

Conforme em estrutura geral. Ha testes horizontais sem distribuicao
(`tela/teste_renderizador.py:2370-2482`), suite vertical H-0025
(`3370-3821`) e teste horizontal com distribuicao declarada que documenta a
ausencia de suporte atual (`3763-3795`). O handoff exige atualizar esse teste nas
linhas 600-611.

## 14. Analise dos criterios de aceite

Os 23 criterios das linhas 506-534 sao objetivos em sua maioria e cobrem modos,
maiores restos, soma exata, contato, largura total, ausencia, regressao vertical,
loader/modelo, escopo documental, relatorio e ausencia de commit.

Defeito encontrado: o criterio/teste de empate de restos fica incompleto quando
detalhado em T07, pois nao fixa fixture nem resultado numerico esperado. Ver
H0026-QA-M01.

## 15. Analise dos testes

O handoff cobre:

- percentual `[50, 50]`: linhas 546-550.
- percentual assimetrico `[60, 40]`: linhas 551-555.
- fracao `[1, 1]`: linhas 556-560.
- fracao `[2, 1]`: linhas 561-565.
- equivalencia `[2, 1]` e `[4, 2]`: linhas 566-570.
- largura nao divisivel, maiores restos e soma exata: linhas 572-588.
- bordas em contato e largura total: linhas 590-598.
- ausencia sem regressao: linhas 613-622.
- regressao vertical H-0025: linhas 624-627.
- rejeicoes do loader: linhas 629-632.
- atualizacao do teste existente: linhas 600-611.

Pendencia: T07 (`docs/handoff/...:578-582`) nao define valores/largura/resultado
inequivocos para o empate de restos.

## 16. Analise das condicoes de bloqueio

As condicoes de bloqueio nas linhas 674-708 sao adequadas: mandam parar diante de
regra ausente, politica nova, alteracao da ausencia, grupos horizontais, ampliacao
hierarquica, contradicao normativa, arquivo obrigatorio ausente, IMP-0027 ocupado,
estado Git divergente ou necessidade de arquivo fora da lista.

O proprio handoff, porem, contem estado Git incompleto nas linhas 88-96 e
112-113; isso pode acionar bloqueio indevido. Ver H0026-QA-A01.

## 17. Analise da ausencia de implementacao antecipada

Conforme. O handoff nao altera codigo, testes, contratos ou ADRs; o arquivo novo
tem conteudo de ordem de trabalho e criterios, nao implementacao disfarçada. As
linhas 44-46 e 720-737 delimitam que ele nao implementa, nao faz QA de si mesmo,
nao altera loader/modelo sem necessidade e nao prepara commit.

## 18. Achados numerados

### H0026-QA-A01

- Severidade: alto.
- Arquivo e linha: `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md:88-96` e `112-113`.
- Regra ou autoridade aplicavel: estado informado ao gerente e verificacao obrigatoria de estado Git deste QA; o handoff tambem manda parar se o estado divergir (`docs/handoff/...:110`, `692-696`, `700-706`).
- Descricao objetiva: o handoff registra como nao rastreados esperados apenas o levantamento e `tela/__pycache__/`, omitindo o proprio arquivo de handoff `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md`, que esta realmente nao rastreado no inicio do QA.
- Impacto: o futuro executor pode identificar divergencia de estado e parar com bloqueio de repositorio/evidencia, embora o estado real seja o estado esperado do ciclo.
- Categoria de correcao: patch de handoff.
- Exige: patch de handoff; nao exige ADR nem nova evidencia externa.

### H0026-QA-M01

- Severidade: medio.
- Arquivo e linha: `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md:578-582`.
- Regra ou autoridade aplicavel: requisito deste QA de que os testes definam larguras esperadas de forma inequivoca; criterio de maiores restos e desempate por ordem em `docs/contratos/contrato_composicao_corpo.md:618-638` e R-19 em `851-855`.
- Descricao objetiva: T07 exige um fixture de empate de restos, mas deixa para o executor escolher valores e largura que produzam o empate; nao registra resultado concreto esperado.
- Impacto: parte da cobertura obrigatoria fica menos auditavel e permite variacao operacional desnecessaria na implementacao/teste.
- Categoria de correcao: patch de handoff.
- Exige: patch de handoff; nao exige ADR.

### H0026-QA-O01

- Severidade: observacao.
- Arquivo e linha: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:5-7`, `24-27`; `docs/adr/INDICE_ADR.md:48`.
- Regra ou autoridade aplicavel: indice de ADRs aceitas e contratos ativos.
- Descricao objetiva: ha inconsistencia textual ja conhecida: ADR-0018 aparece como `proposta` no arquivo e como aceita no indice.
- Impacto: nao bloqueia este handoff, pois os contratos ativos ja incorporam a semantica e o levantamento registrou a inconsistencia como nao semantica.
- Categoria de correcao: nenhuma neste ciclo.
- Exige: nenhuma alteracao neste QA.

## 19. Conclusao

O handoff e arquiteturalmente implementavel e a semantica horizontal de
`percentual` e `fracao` esta fechada nas autoridades ativas. Loader e modelo nao
precisam de alteracao; renderizador e testes autorizados sao suficientes.

Entretanto, ha dois defeitos reais no texto do handoff: um alto, sobre o estado
Git esperado, e um medio, sobre fixture de teste nao inequivoca. Ambos sao
corrigiveis por patch do handoff, sem nova ADR.

## 20. Status final unico

`H2_HANDOFF_PATCH_REQUIRED`

## 21. Lista do unico arquivo criado ou alterado

Arquivo criado nesta etapa:

```text
docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md
```
