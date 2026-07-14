# RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO

## 1. Identificacao da etapa

Etapa executada: `LEVANTAMENTO`.

Capacidade investigada, exclusivamente: distribuicao percentual e por fracao no arranjo horizontal da composicao do corpo.

Este relatorio nao cria ADR, nao cria handoff, nao implementa, nao corrige documentos ou codigo, nao faz QA formal e nao prepara commit.

## 2. Data

2026-07-11.

## 3. Branch e commit verificados

Comandos iniciais exigidos:

| Comando | Resultado |
|---|---|
| `git branch --show-current` | `master` |
| `git log -1 --oneline` | `1cc0dff feat: implementa distribuicao vertical explicita do corpo` |
| `git status --short` | `?? tela/__pycache__/` |
| `git diff --stat` | sem saida |
| `git diff --cached --stat` | sem saida |

Divergencia em relacao ao estado de referencia: branch e commit conferem com a referencia informada (`master`, `1cc0dff`). A unica divergencia operacional observada e arquivo/diretorio nao rastreado de cache Python: `tela/__pycache__/`.

## 4. Estado Git

- Alteracoes rastreadas fora do stage: nenhuma (`git diff --stat` sem saida).
- Alteracoes no stage: nenhuma (`git diff --cached --stat` sem saida).
- Arquivos nao rastreados: `tela/__pycache__/`.
- Caches ou temporarios: `tela/__pycache__/` contem arquivos `.pyc` listados por `rg --files --hidden`, por exemplo `tela/__pycache__/modelo.cpython-314.pyc`.
- Branch/commit: sem divergencia frente ao estado de referencia.

Nenhum arquivo encontrado foi limpo, removido, adicionado ao stage ou corrigido.

## 5. Objetivo

Responder, com evidencias do repositorio real, se as autoridades documentais ativas ja definem de forma completa e sem contradicao a distribuicao percentual e por fracao no arranjo horizontal, de modo que a lacuna restante possa ser tratada por um handoff de implementacao, ou se e necessaria uma decisao documental/ADR antes do handoff.

## 6. Escopo positivo

- `corpo.arranjo = "horizontal"`.
- `grupo.arranjo = "horizontal"` apenas enquanto evidencia normativa/implementada atual de grupos horizontais.
- `corpo.distribuicao` nos modos `percentual` e `fracao`.
- Validacao de valores, quantidade, soma percentual, pesos positivos e preservacao no modelo.
- Calculo de dimensoes horizontais no renderizador.
- Testes e JSONs existentes relacionados.

## 7. Escopo negativo

Nao foram investigados ou propostos: nova arquitetura, composicao hierarquica em tres niveis como tema proprio, arranjos futuros, correcao documental, implementacao, novos testes, QA formal, commit ou handoff.

## 8. Metodologia e comandos usados

Comandos de estado Git:

```text
git branch --show-current
git log -1 --oneline
git status --short
git diff --stat
git diff --cached --stat
```

Comandos de localizacao e leitura:

```text
rg --files --hidden
rg -n --hidden 'arranjo|horizontal|distribuicao|percentual|fracao' scripts docs tela config
rg -n --hidden 'distribui|percent|fra[cç][aã]o|peso|pesos|horizontal|largura|coluna|soma|100|arredond|sobra|déficit|deficit|divis' scripts docs tela config
rg -n 'horizontal.*percentual|percentual.*horizontal|horizontal.*fracao|fracao.*horizontal|distribuicao.*horizontal|_montar_corpo_horizontal|corpo.*distribuicao|percentual|fracao|quantidade|soma igual|pesos|maiores restos|arredond' tela/teste_*.py
rg -n '"arranjo"|"distribuicao"|"modo"|"valores"' config/telas/*.json
```

Observacao metodologica: as duas buscas amplas com `scripts docs tela config` retornaram tambem `rg: scripts: No such file or directory`, pois o cwd ja e o diretorio `scripts`. A busca ainda leu `docs`, `tela` e `config`; leituras posteriores foram direcionadas nesses caminhos reais.

Nao foi executada suite de testes. Esta etapa priorizou inspecao documental, estatica e dos testes existentes.

## 9. Autoridades localizadas

Autoridades normativas ativas e aplicaveis:

- `docs/NOMENCLATURA.md`: define responsabilidade da nomenclatura como fonte de schema e semantica para contratos, linhas 32-36; registra `vertical`/`horizontal` como terminologia final de arranjo, linhas 131-143; distingue arranjo vertical de ocupacao vertical e afirma que tela horizontal tambem deve poder ocupar altura disponivel, linhas 165-173.
- `docs/adr/INDICE_ADR.md`: lista ADR-0011, ADR-0015 e ADR-0018 como aceitas, linhas 41, 45 e 48.
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`: fixa `vertical` e `horizontal` como nomes finais de `corpo.arranjo`, linhas 70-85; registra aliases transicionais, linhas 88-96; separa `corpo.arranjo` de `barra_de_menus.distribuicao`, linhas 130-143.
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`: define arranjo por container, linhas 107-119; distribuicao por container, linhas 122-132; modos `percentual` e `fracao`, linhas 142-158; quantidade de valores, linhas 171-185; maiores restos, linhas 189-209; contato horizontal, linhas 213-228; preenchimento de area, linhas 238-246.
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`: distingue arranjo e distribuicao, linhas 105-112; define ausencia de `distribuicao` no contexto vertical, linhas 113-126; preserva os modos, pesos, soma percentual, maiores restos e composicao hierarquica da ADR-0015 salvo conflito explicito, linhas 420-433. Observacao: o proprio arquivo registra `metadata.status: proposta` e `## Status proposta`, linhas 5-7 e 24-27, enquanto o indice registra ADR-0018 como aceita em `docs/adr/INDICE_ADR.md:48`.
- `docs/contratos/contrato_composicao_corpo.md`: contrato ativo, linhas 1-9; rastreia ADR-0011, ADR-0015, ADR-0017 e ADR-0018, linhas 20-24; define regra fundamental de renderer executor, linhas 53-70; define grupo como container que declara arranjo e distribuicao, linhas 114-130; define arranjo por container, linhas 269-288; define distribuicao por container, linhas 290-320; define particionamento horizontal contiguo, linhas 514-527; define ausencia e modos, linhas 531-588; define arredondamento, linhas 618-638; define preenchimento horizontal/vertical, linhas 642-659; regras R-17 a R-20, linhas 836-860.
- `docs/contratos/contrato_tela_json.md`: contrato ativo, linhas 1-12; define `grupo` como estrutural com `arranjo` e `distribuicao`, linhas 187-192; define que `corpo` e `grupo` podem declarar distribuicao e que os modos sao `igual`, `percentual`, `fracao`, linhas 200-206; registra semantica de ausencia/explicita para `corpo.distribuicao`, linhas 208-227.
- `docs/contratos/contrato_json_tela_minima.md`: define grupo com `arranjo: "horizontal"` no exemplo minimo, linhas 187-204; define `distribuicao` opcional e sem fallback `igual`, linhas 206-212; define `corpo` e `grupo` podendo declarar distribuicao e modos explicitos, linhas 214-230.

## 10. Documentos historicos consultados

Consultados somente como origem/transicao, sem autoridade normativa superior:

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`: handoff historico que ainda reproduzia ausencia como `igual`, linhas 153-156 e 233-259.
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`: registra bloqueio `ARCHITECTURE_REVIEW_REQUIRED`, linhas 27-38, por conflito entre ausencia como `igual` e regressao, linhas 144-220.
- `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`: substitui operacionalmente H-0024, linhas 61-99; escopo vertical explicito, linhas 40-53; decisoes de ausencia e modos, linhas 182-247.
- `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md`: registra implementacao H-0025, linhas 31-37; lista alteracoes, linhas 146-160; descreve validacao de modos, linhas 185-199; modelo, linhas 201-206; algoritmo de cotas, linhas 208-220.
- `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md`: registra fechamento pronto para commit, linhas 1-10; confirma cadeia ADR-0018/H-0025, linhas 87-159; registra que ADR-0018 aparece com status `proposta` no arquivo mas cadeia aprovada nos QAs, linhas 91-107.

## 11. Semantica normativa encontrada

### 11.1 `distribuicao` no horizontal

`distribuicao` e permitida e opcional para containers (`corpo` e `grupo`). O contrato de composicao diz que a distribuicao pertence ao mesmo container que declara o arranjo, e que container horizontal reparte colunas/largura: `docs/contratos/contrato_composicao_corpo.md:290-295`. O contrato de tela JSON afirma que tanto `corpo` quanto `grupo` podem declarar `distribuicao`: `docs/contratos/contrato_tela_json.md:200-206`; o contrato minimo repete essa regra: `docs/contratos/contrato_json_tela_minima.md:214-230`.

Classificacao: `NORMATIVA_COMPLETA`.

### 11.2 Modos admitidos

Os modos explicitos validos sao `igual`, `percentual` e `fracao`: `docs/contratos/contrato_composicao_corpo.md:551-574`, `docs/contratos/contrato_tela_json.md:200-206`, `docs/contratos/contrato_json_tela_minima.md:225-230`.

Classificacao: `NORMATIVA_COMPLETA`.

### 11.3 Modo `percentual`

Regra normativa: `distribuicao.valores[]` declara percentuais explicitos; a quantidade deve ser igual a filhos diretos; soma exatamente 100; valores positivos; soma diferente de 100 e invalida: `docs/contratos/contrato_composicao_corpo.md:558-566`; ADR-0015 registra o mesmo: `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:142-150`.

Classificacao: `NORMATIVA_COMPLETA`.

### 11.4 Modo `fracao`

Regra normativa: `distribuicao.valores[]` declara pesos relativos; um valor por filho direto; todos positivos; denominador implicito e a soma dos pesos; cota de cada filho e `valor_do_filho / soma_dos_valores`: `docs/contratos/contrato_composicao_corpo.md:568-583`; ADR-0015 registra o mesmo: `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:152-163`.

Classificacao: `NORMATIVA_COMPLETA`.

### 11.5 Valores invalidos

Zero e negativos sao rejeitados pela exigencia de valores positivos: `docs/contratos/contrato_composicao_corpo.md:560-564` e `docs/contratos/contrato_composicao_corpo.md:570-574`. Strings e booleanos nao sao nomeados literalmente nos contratos, mas a regra exige percentuais/pesos positivos; a implementacao os rejeita explicitamente por tipo numerico nao booleano em `tela/loader.py:143-145` e `tela/loader.py:205-210`, com testes em `tela/teste_loader.py:967-987`. Listas vazias sao rejeitadas quando ha filhos diretos porque `len(distribuicao.valores) == len(elementos)`: `docs/contratos/contrato_composicao_corpo.md:312-319`.

Classificacao: `NORMATIVA_COMPLETA` para zero, negativos e cardinalidade; `IMPLEMENTACAO_PARCIAL` para explicitacao tecnica de boolean/string, pois o codigo e os testes tornam a rejeicao observavel.

### 11.6 Associacao e ordem

Valores se associam aos filhos diretos do container por ordem declarada. A quantidade conta somente filhos diretos, nao netos ou descendentes internos: `docs/contratos/contrato_composicao_corpo.md:312-319`; ADR-0015, `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:171-185`; ADR-0018 preserva associacao posicional nos modos, `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:160-180`.

Classificacao: `NORMATIVA_COMPLETA`.

### 11.7 Grupos horizontais e elementos simples

Normativamente, `grupo` recebe area do container pai, redistribui entre filhos diretos e declara proprio `arranjo` e `distribuicao`: `docs/contratos/contrato_composicao_corpo.md:114-130`. O contrato minimo mostra `grupo` com `arranjo: "horizontal"` como exemplo minimo: `docs/contratos/contrato_json_tela_minima.md:187-204`. Logo a regra normativa e comum a containers, nao exclusiva de elementos simples.

Classificacao: `NORMATIVA_COMPLETA`.

### 11.8 Ausencia de `distribuicao` no horizontal

A regra ativa e geral: sem `distribuicao`, preserva-se a construcao orientada pelo conteudo; nao equivale ao modo `igual`; nao ha reparticao proporcional automatica; a sobra no eixo do arranjo pode permanecer como preenchimento externo: `docs/contratos/contrato_composicao_corpo.md:531-549`; R-17 afirma que sem `distribuicao` o arranjo apenas organiza os filhos conforme dimensoes orientadas pelo conteudo, e com `distribuicao` reparte largura no horizontal ou altura no vertical: `docs/contratos/contrato_composicao_corpo.md:836-844`.

Classificacao: `NORMATIVA_COMPLETA`.

### 11.9 Arredondamento, sobra e deficit

Percentuais/frações devem ser convertidos por maiores restos; soma final igual a area disponivel; empates por ordem declarada: `docs/contratos/contrato_composicao_corpo.md:618-638`; R-19 reforca qualquer conversao para celulas inteiras: `docs/contratos/contrato_composicao_corpo.md:851-855`. Com distribuicao explicita, a soma das cotas ocupa toda a area distribuivel e a sobra excedente ao conteudo vira preenchimento interno, nunca acumulada fora do ultimo filho: `docs/contratos/contrato_composicao_corpo.md:301-310` e `docs/contratos/contrato_composicao_corpo.md:642-659`. Conteudo maior que cota fica fora de escopo nesta versao: `docs/contratos/contrato_composicao_corpo.md:590-609`.

Classificacao: `NORMATIVA_COMPLETA` para arredondamento e sobra distribuivel; `FORA_DE_ESCOPO` para politica de conteudo maior que a cota.

### 11.10 Formulacoes concorrentes

Nao foi localizada contradicao semantica ativa que exija nova ADR para horizontal. A ADR-0015 define a regra horizontal geral; a ADR-0018 substitui apenas a equivalencia ausencia = `igual` e preserva distribuicao por container, modos, pesos, soma percentual, maiores restos e composicao hierarquica: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:414-433`.

Inconsistencia documental nao semantica registrada: `docs/adr/INDICE_ADR.md:48` marca ADR-0018 como aceita, mas `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:5-7` e `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:24-27` ainda dizem `proposta`. A cadeia de fechamento H-0025 tambem registra essa situacao e confirma os QAs aprovados: `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md:87-107`.

Classificacao: `EVIDENCIA_INSUFICIENTE` apenas para status textual interno da ADR-0018; nao altera a conclusao semantica horizontal porque os contratos ativos ja incorporam as regras e o pedido informa H-0025/ADR-0018 como ciclo formalmente encerrado.

## 12. Implementacao por modulo

### 12.1 Loader

O loader aceita `corpo.arranjo = "horizontal"` e aliases: `tela/loader.py:33-37`, `tela/loader.py:434-441`.

O loader aceita `corpo.distribuicao` sem restringir ao arranjo vertical: ele valida sempre que o campo existe em `corpo`, independentemente de `arranjo`: `tela/loader.py:443-448`.

Modos aceitos: `igual`, `percentual`, `fracao`: `tela/loader.py:39-42`, `tela/loader.py:178-183`.

Validacoes implementadas:

- objeto obrigatorio quando declarado: `tela/loader.py:171-176`;
- `valores` lista para `percentual`/`fracao`: `tela/loader.py:190-195`;
- quantidade igual aos filhos diretos: `tela/loader.py:197-203`;
- valores numericos nao booleanos e estritamente positivos: `tela/loader.py:143-145`, `tela/loader.py:205-210`;
- soma percentual igual a 100: `tela/loader.py:212-216`.

Restricao relevante: grupo com `arranjo` horizontal ou `lado_a_lado` e rejeitado como fora de escopo/nao implementado: `tela/loader.py:227-251`. Portanto a capacidade horizontal em grupos, embora normatizada, nao esta implementada no loader.

Classificacao: `IMPLEMENTACAO_PARCIAL`.

### 12.2 Modelo

O modelo preserva `distribuicao` como `dict | None`, diferenciando ausencia de declaracao explicita: `tela/modelo.py:57-70`. `construir_modelo` copia `corpo_raw.get("distribuicao")` sem conversao: `tela/modelo.py:271-275`.

Nao ha normalizacao especifica para horizontal; o modelo transporta o valor validado.

Classificacao: `IMPLEMENTACAO_PARCIAL` no conjunto da capacidade, pois preserva dados, mas nao calcula dimensoes.

### 12.3 Renderizador

O renderizador possui helpers genericos de pesos e maiores restos para altura: `_pesos_distribuicao` retorna pesos de `igual`, `percentual` e `fracao`: `tela/renderizador.py:203-216`; `_distribuir_alturas` aplica maiores restos no eixo vertical/altura: `tela/renderizador.py:219-254`.

O ramo horizontal chama `_montar_corpo_horizontal` antes do ramo de distribuicao vertical: `tela/renderizador.py:969-994`. Esse caminho nao passa `modelo.corpo.distribuicao` para `_montar_corpo_horizontal`.

`_montar_corpo_horizontal` calcula larguras uniformes por `total_w // N` e resto distribuido para os primeiros slots: `tela/renderizador.py:756-782`. O docstring ainda chama isso de "Distribuicao uniforme implicita": `tela/renderizador.py:756-761`.

O ramo de distribuicao explicita so executa quando nao e horizontal e quando `distribuicao_corpo is not None and altura is not None`: `tela/renderizador.py:995-1040`. Portanto `percentual` e `fracao` em `corpo.arranjo = "horizontal"` sao ignorados pelo renderizador atual; a largura permanece uniforme.

Preservacao de bordas e contato horizontal esta implementada no caminho uniforme: concatenacao sem separador externo em `tela/renderizador.py:843-853`, com testes de bordas coladas em `tela/teste_renderizador.py:2402-2429`.

Classificacao: `IMPLEMENTACAO_AUSENTE` para calculo horizontal percentual/fracao; `IMPLEMENTACAO_PARCIAL` para particionamento horizontal uniforme e preservacao visual basica.

## 13. Cobertura de testes

### 13.1 Loader

Ha testes de ausencia, `igual`, `percentual` valido, soma percentual invalida, `fracao` valida, zero, negativo, quantidade divergente, modo desconhecido, distribuicao nao-dict, string e bool: `tela/teste_loader.py:826-987`.

Esses testes usam `corpo.arranjo = "vertical"` no helper: `tela/teste_loader.py:828-837`. Nao ha teste positivo especifico de loader para `corpo.arranjo = "horizontal"` com `percentual` ou `fracao`.

Classificacao: `TESTE_AUSENTE` para horizontal especifico no loader; cobertura geral de validacao existe.

### 13.2 Modelo

Ha teste de preservacao de `fracao [2,1,2]` no modelo real do Orquestrador: `tela/teste_modelo.py:123-130`. Ha teste de ausencia preservada como `None`: `tela/teste_modelo.py:353-358`.

Nao ha teste especifico de modelo para `arranjo = "horizontal"` com `percentual` ou `fracao`.

Classificacao: `TESTE_AUSENTE` para horizontal especifico no modelo.

### 13.3 Renderizador

Ha testes de arranjo horizontal sem distribuicao explicita cobrindo lado a lado, bordas coladas, largura total e resto uniforme: `tela/teste_renderizador.py:2370-2478`.

Ha cobertura vertical H-0025 para algoritmo, `percentual`, `fracao`, maiores restos, soma exata e ausencia: `tela/teste_renderizador.py:3370-3668`.

Ha um teste de `arranjo = "horizontal"` com `distribuicao={"modo": "fracao", "valores": [1,1]}`, mas o proprio comentario declara que H-0025 nao implementa distribuicao horizontal e o teste apenas preserva particionamento contiguo/sem erro: `tela/teste_renderizador.py:3763-3795`.

Nao foram localizados testes positivos de horizontal com `percentual` calculando larguras, horizontal com `fracao` calculando larguras, invalidos horizontais especificos, arredondamento horizontal por pesos declarados ou sobra horizontal com distribuicao declarada.

Classificacao: `TESTE_AUSENTE`.

### 13.4 JSONs

`config/telas/orquestrador.json` declara `corpo.arranjo = "vertical"` com `distribuicao` `fracao [2,1,2]`: `config/telas/orquestrador.json:23-28`.

Busca em `config/telas/*.json` localizou `arranjo` horizontal apenas em `barra_de_menus.distribuicao` como `horizontal_responsiva`, nao como `corpo.arranjo = "horizontal"` com `percentual`/`fracao`: `config/telas/stub_b.json:27-28`, `config/telas/destino_minimo.json:27-28`, `config/telas/grupo_minimo.json:34-35`, `config/telas/orquestrador.json:130-131`.

Nao ha JSON demonstrativo atual com `corpo.arranjo = "horizontal"` e `corpo.distribuicao` `percentual` ou `fracao`.

Classificacao: `TESTE_AUSENTE`/`IMPLEMENTACAO_AUSENTE` como demonstracao.

## 14. Matriz de evidencias

| Aspecto | Autoridade normativa | Implementacao | Testes | Situacao |
|---|---|---|---|---|
| Horizontal sem `distribuicao` | Ausencia preserva conteudo e nao reparte automaticamente: `docs/contratos/contrato_composicao_corpo.md:531-549`, R-17 `docs/contratos/contrato_composicao_corpo.md:836-844` | Renderizador horizontal reparte uniformemente sempre: `tela/renderizador.py:756-782`, chamado em `tela/renderizador.py:969-994` | Testes H-0019 cobrem horizontal uniforme: `tela/teste_renderizador.py:2370-2478` | `IMPLEMENTACAO_PARCIAL` |
| Horizontal `percentual` | Modo definido e soma 100: `docs/contratos/contrato_composicao_corpo.md:558-566` | Loader aceita/valida: `tela/loader.py:178-216`; renderizador nao usa no horizontal: `tela/renderizador.py:969-994` | So vertical: `tela/teste_renderizador.py:3575-3585`; sem teste horizontal positivo | `IMPLEMENTACAO_AUSENTE`, `TESTE_AUSENTE` |
| Horizontal `fracao` | Pesos positivos, denominador soma: `docs/contratos/contrato_composicao_corpo.md:568-583` | Loader aceita/valida: `tela/loader.py:178-216`; renderizador nao usa no horizontal: `tela/renderizador.py:969-994` | Teste horizontal declara fracao mas espera apenas nao regressao: `tela/teste_renderizador.py:3763-3795` | `IMPLEMENTACAO_AUSENTE`, `TESTE_AUSENTE` |
| Validacao da quantidade | `len(distribuicao.valores) == len(elementos)`: `docs/contratos/contrato_composicao_corpo.md:312-319` | `tela/loader.py:197-203` | `tela/teste_loader.py:921-936` | `NORMATIVA_COMPLETA` |
| Soma percentual | Soma exatamente 100: `docs/contratos/contrato_composicao_corpo.md:560-564` | `tela/loader.py:212-216` | `tela/teste_loader.py:860-887` | `NORMATIVA_COMPLETA` |
| Pesos positivos | Positivos e denominador soma: `docs/contratos/contrato_composicao_corpo.md:570-574` | `tela/loader.py:205-210`; `_distribuir_alturas` rejeita soma nao positiva: `tela/renderizador.py:237-244` | `tela/teste_loader.py:888-919` | `NORMATIVA_COMPLETA` |
| Normalizacao fracionaria | Fracao de cada filho = valor/soma: `docs/contratos/contrato_composicao_corpo.md:570-574` | Algoritmo vertical usa `altura * peso / soma`: `tela/renderizador.py:229-245`; nao ha largura horizontal equivalente | Vertical: `tela/teste_renderizador.py:3597-3626`; horizontal ausente | `IMPLEMENTACAO_AUSENTE` no horizontal |
| Arredondamento e sobra | Maiores restos e soma exata: `docs/contratos/contrato_composicao_corpo.md:618-638`; R-19 `docs/contratos/contrato_composicao_corpo.md:851-855` | Horizontal uniforme usa resto por ordem, sem pesos declarados: `tela/renderizador.py:775-782` | Uniforme: `tela/teste_renderizador.py:2449-2478`; pesos horizontais ausentes | `IMPLEMENTACAO_PARCIAL` |
| Grupos horizontais | Grupo declara arranjo/distribuicao: `docs/contratos/contrato_composicao_corpo.md:114-130`; exemplo horizontal `docs/contratos/contrato_json_tela_minima.md:187-204` | Loader rejeita grupo horizontal: `tela/loader.py:227-251` | Sem teste positivo de grupo horizontal; restricao atual inferida do codigo | `IMPLEMENTACAO_AUSENTE` |
| Preservacao de margens e espacamentos | Contato horizontal sem vao externo: `docs/contratos/contrato_composicao_corpo.md:514-527`; preenchimento horizontal por espacos: `docs/contratos/contrato_composicao_corpo.md:642-659` | Concatenacao sem separador e linhas com largura total: `tela/renderizador.py:843-853` | Bordas coladas e largura preservada: `tela/teste_renderizador.py:2402-2447` | `IMPLEMENTACAO_PARCIAL` |

## 15. Achados numerados

1. `NORMATIVA_COMPLETA` — A autoridade ativa define que distribuicao por container se aplica ao horizontal repartindo largura/colunas: `docs/contratos/contrato_composicao_corpo.md:290-299`; ADR-0015, `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:122-132`.
2. `NORMATIVA_COMPLETA` — `percentual` e `fracao` estao definidos com quantidade, positividade, soma 100 no percentual e denominador soma dos pesos na fracao: `docs/contratos/contrato_composicao_corpo.md:558-583`.
3. `NORMATIVA_COMPLETA` — Valores se associam por filhos diretos e ordem declarada; netos/descendentes nao contam: `docs/contratos/contrato_composicao_corpo.md:312-319`.
4. `NORMATIVA_COMPLETA` — Arredondamento por maiores restos, soma exata e desempate por ordem declarada estao definidos para conversao a celulas inteiras: `docs/contratos/contrato_composicao_corpo.md:618-638`.
5. `IMPLEMENTACAO_PARCIAL` — Loader aceita e valida `corpo.distribuicao` para `corpo.arranjo = "horizontal"` porque a validacao nao e condicionada ao eixo: `tela/loader.py:434-448`.
6. `IMPLEMENTACAO_AUSENTE` — Renderizador horizontal ignora `modelo.corpo.distribuicao` e calcula larguras uniformes por quantidade de filhos: `tela/renderizador.py:756-782`, `tela/renderizador.py:969-994`.
7. `IMPLEMENTACAO_AUSENTE` — Grupos horizontais sao normativos, mas o loader os rejeita como fora de escopo/nao implementados: `docs/contratos/contrato_json_tela_minima.md:187-204`; `tela/loader.py:227-251`.
8. `TESTE_AUSENTE` — Nao ha teste positivo que verifique largura horizontal por `percentual`; a cobertura `percentual` existente e vertical: `tela/teste_renderizador.py:3575-3585`.
9. `TESTE_AUSENTE` — Nao ha teste positivo que verifique largura horizontal por `fracao`; o teste horizontal com `fracao` declara que distribuicao horizontal nao foi implementada e apenas protege nao regressao: `tela/teste_renderizador.py:3763-3795`.
10. `OCORRENCIA_HISTORICA` — H-0025 foi vertical por escopo explicito, nao horizontal: `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md:40-53`; o relatorio de implementacao confirma alteracoes focadas em distribuicao vertical: `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md:146-160`.
11. `EVIDENCIA_INSUFICIENTE` — Ha inconsistencia de status textual da ADR-0018 (`proposta` no arquivo, aceita/aprovada na cadeia). Evidencia: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:5-7`, `docs/adr/INDICE_ADR.md:48`, `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md:91-107`. Nao foi localizada contradicao semantica horizontal decorrente disso.

## 16. Contradicoes ou lacunas

### 16.1 Contradicoes normativas

Nao foi localizada contradicao normativa ativa sobre a semantica horizontal de `percentual` e `fracao`. A ADR-0015 define a regra geral horizontal; a ADR-0018 preserva modos, pesos, soma percentual, maiores restos e composicao hierarquica salvo o ponto ausencia = `igual`: `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:414-433`.

### 16.2 Lacunas de implementacao

- Renderizador nao calcula larguras horizontais por `percentual` ou `fracao`: `tela/renderizador.py:756-782`, `tela/renderizador.py:969-994`.
- Renderizador horizontal atual aplica particionamento uniforme mesmo quando ha `distribuicao` declarada: teste preserva esse comportamento em `tela/teste_renderizador.py:3763-3795`.
- Grupos horizontais sao barrados no loader: `tela/loader.py:227-251`.

### 16.3 Lacunas de teste

- Sem teste positivo de horizontal `percentual`.
- Sem teste positivo de horizontal `fracao` verificando proporcao real.
- Sem teste negativo horizontal especifico de quantidade/soma/peso; existem testes gerais de loader em `tela/teste_loader.py:826-987`.
- Sem JSON demonstrativo de `corpo.arranjo = "horizontal"` com `corpo.distribuicao` `percentual` ou `fracao`: busca em `config/telas/*.json` localizou apenas Orquestrador vertical com `fracao`, `config/telas/orquestrador.json:23-28`.

## 17. Perguntas que exigem decisao do usuario

Nenhuma pergunta arquitetural e necessaria para permitir handoff de implementacao da distribuicao percentual e por fracao no arranjo horizontal.

Perguntas operacionais que um futuro handoff pode precisar delimitar, sem exigir ADR:

1. O handoff horizontal deve incluir tambem a correcao do comportamento de ausencia de `distribuicao` no horizontal, hoje uniforme, para alinhar a ADR-0018/contrato geral?
2. O handoff horizontal deve incluir grupos horizontais agora, ou restringir explicitamente o primeiro ciclo ao `corpo` raiz e deixar grupo horizontal para ciclo proprio?
3. Deve ser criado JSON demonstrativo horizontal neste ciclo de implementacao ou a cobertura deve ficar apenas em modelos sinteticos de teste?

## 18. Conclusao

As autoridades documentais ativas ja fornecem semantica suficiente para um handoff de implementacao da distribuicao `percentual` e `fracao` no arranjo horizontal.

A regra nao precisa ser importada indevidamente do vertical: a ADR-0015 e o contrato ativo definem distribuicao por container, dizem expressamente que container horizontal reparte largura/colunas, definem modos, quantidade, associacao por filhos diretos, positividade, soma percentual, denominador fracionario, maiores restos, soma exata, contato entre molduras e preenchimento horizontal por espacos.

A lacuna encontrada e de implementacao e cobertura: o loader/modelo ja aceitam/preservam `corpo.distribuicao`, mas o renderizador horizontal nao usa essa declaracao e continua calculando larguras uniformes. Grupos horizontais tambem permanecem nao implementados apesar de normatizados. Nao foi identificada necessidade de nova ADR antes de um handoff de implementacao.

## 19. Status final unico

`L1_HORIZONTAL_DOCUMENTADO_HANDOFF_POSSIVEL`

## 20. Lista do unico arquivo criado ou alterado

Arquivo criado:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
```
