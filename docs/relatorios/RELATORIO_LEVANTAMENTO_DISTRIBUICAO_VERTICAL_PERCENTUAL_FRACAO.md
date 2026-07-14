# RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO

## 1. Identificacao e escopo

Levantamento tecnico e documental neutro sobre distribuicao de espaco no corpo quando `corpo.arranjo = "vertical"`, incluindo distribuicao de linhas entre filhos diretos e suporte aos modos `percentual` e `fracao`.

Este relatorio registra evidencias existentes no repositorio. Nao cria ADR, handoff, contrato, correcao, QA, commit ou implementacao.

## 2. Estado Git confirmado

Comandos executados no inicio:

```text
git status --short
```

Resultado: saida vazia.

```text
git log -1 --oneline
3332773 feat: implementa redimensionamento reativo da TUI
```

```text
git rev-parse HEAD
3332773a3f10e716115a164148af323fa86e608f
```

```text
git stash list
stash@{0}: On master: pre-H-0022
```

Conclusao: estado Git coincide com o informado pelo gerente: worktree limpo antes deste levantamento, stage vazio, HEAD esperado e stash preservado.

## 3. Metodo de busca

Foram consultados documentos ativos, ADRs, handoffs, relatorios historicos, configuracoes, codigo e testes com buscas por termos relacionados a `arranjo`, `vertical`, `horizontal`, `distribuicao`, `percentual`, `fracao`, `fração`, `peso`, `pesos`, `proporcao`, `proporção`, `altura`, `linhas`, `corpo`, `elementos`, `composicao`, `composição`, alocacao e divisao do espaco disponivel.

Ocorrencias foram classificadas por papel: autoridade normativa ativa, ADR ativa, contrato ativo, exemplo normativo, handoff historico, relatorio historico, implementacao, teste ou configuracao declarativa. Ocorrencias de `barra_de_menus.distribuicao` foram separadas de `corpo.distribuicao`, pois possuem semantica propria.

## 4. Inventario das autoridades

### Autoridades normativas ativas

- `docs/contratos/contrato_composicao_corpo.md`: contrato ativo v0.3, status ativo, aplica ADR-0011, ADR-0013, ADR-0015 e ADR-0017 nas linhas 1-24.
- `docs/contratos/contrato_tela_json.md`: contrato ativo v0.1, define schema macro de `tela.json` e registra `corpo`, `arranjo`, `grupo`, `distribuicao` e redimensionamento nas linhas 158-206 e 703-831.
- `docs/NOMENCLATURA.md`: glossario com status parcial, fonte de nomes validos para contratos nas linhas 15-25; registra `vertical`/`horizontal` como valores finais de arranjo nas linhas 129-174.

### ADRs ativas aplicaveis

- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`: fixa `vertical` e `horizontal` como nomes finais de `corpo.arranjo`, linhas 70-96; nao implementa codigo, linhas 123-128.
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`: distingue `corpo.arranjo = "vertical"` de ocupacao vertical do terminal, linhas 102-125 e 148-164; define preenchimento de altura entre cabecalho e barra, linhas 81-100.
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`: autoridade principal para arranjo e distribuicao por container. Define que `arranjo = vertical` reparte altura entre filhos diretos, linhas 107-118; que distribuicao aloca area, nao apenas conteudo, linhas 122-133; e os modos `igual`, `percentual` e `fracao`, linhas 136-163.
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`: define SIGWINCH, obtencao de dimensoes, par valido, redimensionamento, terminal pequeno demais e preservacao de composicao, linhas 81-185 e 198-228.

### Contratos aplicaveis

- `contrato_composicao_corpo.md` define `arranjo: "vertical"` como ordem/composicao vertical dos elementos do corpo e distingue isso de `preenchimento_altura_corpo`, linhas 234-258.
- `contrato_composicao_corpo.md` define arranjo por container e efeito de `vertical`, linhas 268-278.
- `contrato_composicao_corpo.md` define distribuicao por container e regra de quantidade de valores, linhas 279-298.
- `contrato_composicao_corpo.md` define modos de distribuicao, arredondamento e preenchimento de area alocada, linhas 509-576.
- `contrato_composicao_corpo.md` define regras R-17 a R-24, incluindo maiores restos e redimensionamento, linhas 752-793.
- `contrato_tela_json.md` define que `corpo` pode declarar `distribuicao`, que a ausencia equivale a `igual`, e remete as regras ao contrato de composicao, linhas 200-206 e 208-215.
- `contrato_json_tela_minima.md` traz exemplo normativo de `arranjo: "vertical"` e campo opcional `corpo.arranjo`, linhas 101-132 e 148-168.

## 5. Respostas obrigatorias: autoridade normativa

- Documento ativo que define `arranjo: "vertical"`: `contrato_composicao_corpo.md` linhas 170-180, 234-258 e 268-278; `contrato_tela_json.md` linhas 238-253; `contrato_json_tela_minima.md` linhas 101-132 e 148-155.
- Semantica normativa para distribuicao da altura entre filhos: sim. ADR-0015 linhas 107-118 e 122-133; contrato de composicao linhas 268-288.
- Modo percentual: sim. ADR-0015 linhas 142-150; contrato de composicao linhas 515-523.
- Modo por fracao: sim, como pesos relativos. ADR-0015 linhas 152-163; contrato de composicao linhas 525-535.
- Percentuais devem totalizar: exatamente 100. ADR-0015 linhas 144-148; contrato linhas 517-521.
- Fracoes: tratadas como pesos relativos, com denominador implicito pela soma dos pesos. ADR-0015 linhas 154-158; contrato linhas 527-531.
- Valores invalidos, zero, negativos, ausencia e somas incompativeis: percentuais e fracoes exigem quantidade igual a filhos diretos e valores positivos; soma percentual diferente de 100 e invalida. ADR-0015 linhas 144-148, 154-158 e 171-180; contrato linhas 517-531 e 290-298. Ausencia de `distribuicao` equivale ao modo `igual`: `contrato_json_tela_minima.md` linhas 205-211.
- Arredondamento e linhas residuais: metodo dos maiores restos; soma final igual a area disponivel; empates pela ordem declarada. ADR-0015 linhas 189-209; contrato linhas 544-564 e 762-765.
- Bordas, separadores, margens, cabecalho, barra de menus e area util do corpo: ADR-0013 define corpo entre cabecalho e barra, linhas 81-85; contrato de composicao distingue cabecalho/barra/corpo e linhas nao pertencentes ao corpo, linhas 234-258 e 260-266; contrato_tela_json define execucao TTY e redimensionamento, linhas 653-699 e 703-831.
- Elementos com altura minima ou conteudo que nao cabe: pagina dentro da area alocada para `console` esta definida na ADR-0015 linhas 271-278 e contrato linhas 611-617; terminal pequeno demais esta definido em ADR-0017 linhas 198-228 e contrato_tela_json linhas 802-818. Conceitos de `minimo`, `preferido`, `maximo`, `restante` e `conteudo` existem como conceitos futuros na ADR-0015 linhas 250-267 e contrato linhas 579-607, mas a politica final por elemento funcional ainda nao esta implementada.
- Redimensionamento do terminal: sim. ADR-0017 linhas 81-185 e 198-228; contrato_tela_json linhas 703-831; contrato_composicao_corpo linhas 783-793.

## 6. Coerencia documental

Formulacoes equivalentes:

- ADR-0015 e `contrato_composicao_corpo.md` concordam que `arranjo = vertical` reparte linhas/altura entre filhos diretos, que distribuicao aloca area e que sobra vertical vira linhas em branco.
- ADR-0011, ADR-0013 e contratos concordam que `corpo.arranjo = "vertical"` e ocupacao vertical do terminal sao conceitos distintos.
- ADR-0017, `contrato_tela_json.md` e `contrato_composicao_corpo.md` concordam que redimensionamento recalcula areas, mas nao altera composicao declarativa.

Contradicoes documentais ativas localizadas: nenhuma contradição ativa bloqueante foi localizada para o escopo deste levantamento.

Semanticas ausentes ou incompletas:

- A semantica de `minimo`/`preferido`/`maximo` por elemento esta registrada como conceito futuro, nao como schema fechado de validacao e implementacao.
- `sincronizacao` explicita futura tem exemplo conceitual, mas schema final nao fechado: ADR-0015 linhas 314-333; contrato linhas 635-648.

Termos antigos ainda presentes:

- `sobreposto` e `lado_a_lado` permanecem como aliases transicionais em ADR-0011 linhas 88-96, contrato linhas 172-180 e loader linhas 33-37. Isso e transicional documentado, nao contradicao ativa.
- JSONs reais ainda usam `sobreposto` em `destino_minimo.json` e `stub_b.json`, ambos como configuracao transicional aceita.

Regra existente apenas em handoff/relatorio:

- Handoffs H-0019, H-0020 e H-0021 proibiram implementar percentual/fracao em seus escopos. Isso e historico de escopo, nao autoridade superior contra a regra ativa da ADR-0015.

## 7. Inventario da implementacao

### Modelo e loader

- `tela/loader.py` define tipos funcionais, tipo estrutural `grupo` e arranjos aceitos para o corpo raiz, linhas 25-37.
- `_validar_grupo` rejeita grupo com `arranjo` horizontal ou `lado_a_lado`, exige exatamente 1 elemento interno e proibe aninhamento neste ciclo, linhas 146-229. Isso diverge da norma futura de profundidade ate 3 como implementacao parcial/historica, nao como contrato novo.
- `carregar_tela` valida `corpo.elementos[]` e `corpo.arranjo`, mas nao valida `corpo.distribuicao`, `distribuicao.modo` nem `distribuicao.valores`, linhas 318-369.
- `tela/modelo.py` cria `Corpo(arranjo, elementos)` sem campo proprio de `distribuicao`, linhas 57-63 e 263. Campos adicionais dos elementos sao preservados como `_campos_inertes`, linhas 250-260.

### Renderer

- `_caixa` aceita `altura_alvo` e preenche com linhas internas bordeadas ate a altura alvo, linhas 172-188, mas esse parametro nao e usado no caminho vertical atual de `renderizar_tela`.
- `_normalizar_distribuicao`, `_validar_distribuicao` e `_linhas_barra` tratam exclusivamente `barra_de_menus.distribuicao`, nao `corpo.distribuicao`, linhas 259-285, 292-489 e 582-664.
- `_montar_corpo_horizontal` implementa particionamento horizontal uniforme implicito entre filhos diretos, com maiores restos sobre largura (`total_w % N`), linhas 696-723. Nao le `corpo.distribuicao`.
- `_montar_corpo_horizontal` calcula `altura_max`, `altura_alvo` e preenche cada coluna ate `altura_disponivel` quando fornecida, linhas 749-793.
- `renderizar_tela` normaliza aliases `sobreposto -> vertical` e `lado_a_lado -> horizontal`, linhas 889-895.
- Caminho horizontal: calcula `l_corpo_disponivel = altura - l_cab - l_barra`, chama `_montar_corpo_horizontal(..., altura_disponivel=...)`, linhas 901-927.
- Caminho vertical: empilha caixas na ordem declarada; grupos sao expandidos apenas para seu unico elemento interno; nao distribui `l_corpo_disponivel` entre filhos, linhas 927-946.
- Preenchimento vertical geral H-0015: calcula `l_corpo_conteudo`, `l_corpo_disponivel` e insere linhas fisicas de espacos apos o ultimo elemento do corpo e antes da barra quando `arranjo_corpo != "horizontal"`, linhas 956-998.
- Resultado atual para `arranjo = "vertical"`: elementos recebem caixas por sua altura renderizada; sobra de altura vai para fill externo apos todos os elementos, nao para areas individuais distribuidas entre eles.

### Demo e redimensionamento

- `tela/demo.py` valida pares de dimensoes em `_par_dimensoes_valido`, linhas 343-350.
- Obtem dimensoes por `ioctl(TIOCGWINSZ)`, ambiente e fallback inicial, linhas 353-409.
- Instala handler `SIGWINCH` com wakeup pipe, linhas 412-426.
- Gera quadro minimo para terminal pequeno demais, linhas 437-457.
- `_resolver_conteudo` chama `renderizar_estado(..., largura, altura)` ou quadro minimo se pequeno/erro, linhas 460-471.
- `main` em TTY inicializa dimensoes, usa pipe e `select`, recalcula ao receber resize e reapresenta o quadro com as novas dimensoes, linhas 518-592.

## 8. Comportamento atualmente suportado

- `corpo.arranjo = "vertical"` e ausencia de arranjo sao aceitos e renderizados como empilhamento sequencial.
- `sobreposto` e `lado_a_lado` sao aceitos como aliases transicionais.
- `corpo.arranjo = "horizontal"` distribui largura de forma uniforme implicita entre filhos diretos do corpo raiz.
- O modo horizontal com `altura` fornecida preenche cada area/coluna ate `l_corpo_disponivel`.
- O modo vertical com `altura` fornecida preenche a sobra total com linhas de espacos apos o bloco de corpo, antes da barra.
- Redimensionamento TTY recalcula largura/altura e redesenha; nao altera arranjo.

## 9. Comportamento documentado, mas ainda nao implementado

- `corpo.distribuicao` e `grupo.distribuicao` como campos semanticamente executados.
- Modo `percentual` para corpo/grupo.
- Modo `fracao` para corpo/grupo.
- Validacao de `distribuicao.valores[]` no loader/modelo.
- Distribuicao vertical de `l_corpo_disponivel` entre cada filho direto quando `arranjo = "vertical"`.
- Preenchimento de area alocada individual no caminho vertical.
- Profundidade de grupos ate 3 niveis e redistribuicao por grupos conforme ADR-0015.
- Regras dimensionais finais de `minimo`/`preferido`/`maximo` por elemento funcional.

## 10. Inventario das configuracoes

Configuracoes reais com `arranjo`:

- `config/telas/orquestrador.json`: `corpo.arranjo = "vertical"` nas linhas 23-25; tres filhos diretos (`console_principal`, `dashboard_info`, `lancador_principal`) nas linhas 26-123. Nao declara `corpo.distribuicao`.
- `config/telas/grupo_minimo.json`: `corpo.arranjo = "vertical"` nas linhas 8-10; `grupo_principal.arranjo = "vertical"` nas linhas 11-15; um dashboard interno nas linhas 16-29. Nao declara `corpo.distribuicao` nem `grupo.distribuicao`.
- `config/telas/destino_minimo.json`: `corpo.arranjo = "sobreposto"` nas linhas 8-10; alias transicional de vertical; um dashboard. Nao declara `corpo.distribuicao`.
- `config/telas/stub_b.json`: `corpo.arranjo = "sobreposto"` nas linhas 8-10; alias transicional de vertical; um dashboard. Nao declara `corpo.distribuicao`.

Configuracoes com `distribuicao`:

- `rg` em `config/telas/*.json` localizou `distribuicao` apenas em `barra_de_menus`: `orquestrador.json` linha 126, `grupo_minimo.json` linha 34, `destino_minimo.json` linha 27 e `stub_b.json` linha 27.
- Nao foram localizadas configuracoes reais com `corpo.distribuicao.modo = "percentual"` ou `"fracao"`.

Exemplo normativo:

- `docs/contratos/contrato_json_tela_minima.md` mostra exemplo com `"arranjo": "vertical"` nas linhas 101-118; declara que `arranjo` fixa layout e ignora `tiling`, linhas 120-127.
- O mesmo contrato registra que `grupo` declara `arranjo`, `distribuicao` e `elementos[]`, linhas 186-206, e que `distribuicao` ausente equivale a `igual`, linhas 205-211.

## 11. Inventario dos testes

### Testes de loader/modelo

- `tela/teste_loader.py` valida preservacao de `corpo.arranjo = "vertical"` do Orquestrador, linhas 196-198.
- `tela/teste_loader.py` cobre `grupo_minimo`, grupo estrutural, rejeicoes de grupo invalido e grupo horizontal/lado_a_lado, linhas 532-675.
- `tela/teste_loader.py` cobre validacao de `corpo.arranjo` aceito/rejeitado para `vertical`, `horizontal`, aliases, ausencia e invalidos, linhas 724-809.
- `tela/teste_modelo.py` verifica `modelo.corpo.arranjo == "vertical"` e elementos, linhas 113-127.
- `tela/teste_modelo.py` preserva `grupo._campos_inertes["arranjo"] == "vertical"`, linhas 370-372.

### Testes de renderizador

- `teste_altura_explicita`: cobre altura explicita, preenchimento vertical externo, linhas de fill, altura insuficiente para corpo/cabecalho+barra e determinismo, `tela/teste_renderizador.py` linhas 958-1151.
- `TestArranjoH0019`: cobre `None`/`vertical`/`sobreposto` preservados, horizontal, alias, bordas contiguas, resto deterministico de largura, padding inferior e largura insuficiente, linhas 2276-2606.
- `TestPreenchimentoVerticalH0020`: cobre preenchimento vertical das areas alocadas no corpo horizontal, ausencia de fill externo no horizontal, preservacao de vertical/sobreposto/None e `l_corpo_disponivel`, linhas 2609-2917.
- `TestPreenchimentoBordeadoH0021`: cobre fill bordeado horizontal, base na ultima linha, bordas adjacentes, nao regressao de vertical/sobreposto/None, linhas 2921-3296.
- Testes de `barra_de_menus.distribuicao` existem em `TestLinhasBarra` e `TestDistribuicaoH0018`, mas sao da barra, nao do corpo, linhas 1197-2241.

### Cobertura ausente para o escopo futuro

- Nao foi localizada cobertura executavel de `corpo.distribuicao.modo = "percentual"`.
- Nao foi localizada cobertura executavel de `corpo.distribuicao.modo = "fracao"`.
- Nao foi localizada cobertura de distribuicao de `l_corpo_disponivel` entre filhos no caminho vertical.
- Nao foi localizada cobertura de `distribuicao.valores[]` invalido/zero/negativo/soma percentual != 100 no corpo.
- Nao foi localizada cobertura de arredondamento por maiores restos aplicado a linhas no arranjo vertical.
- Cobertura de redimensionamento existe para TUI em `tela/teste_demo.py` conforme relatorio IMP-0024, mas nao foi reexecutada neste levantamento.

## 12. Matriz regra/documentacao/codigo/teste

| Regra | Documentacao | Codigo | Teste | Estado |
|---|---|---|---|---|
| `arranjo = vertical` e valor final | ADR-0011; contratos | loader aceita; renderer empilha | loader/modelo/renderizador | Implementado como empilhamento |
| Vertical reparte altura entre filhos diretos | ADR-0015; contrato | Nao implementado no caminho vertical | Nao localizado | Normatizado nao implementado |
| Distribuicao aloca area, nao apenas conteudo | ADR-0015; contrato | Horizontal implementa; vertical nao distribui por filho | Horizontal coberto | Parcial |
| Distribuicao ausente = `igual` | contrato_json_tela_minima | Horizontal usa igual implicito; vertical usa empilhamento + fill externo | Horizontal coberto | Parcial |
| `percentual` | ADR-0015; contrato | Nao reconhecido para corpo | Nao localizado | Normatizado nao implementado |
| `fracao` | ADR-0015; contrato | Nao reconhecido para corpo | Nao localizado | Normatizado nao implementado |
| Validar `len(valores) == len(elementos)` | ADR-0015; contrato | Nao implementado para corpo | Nao localizado | Normatizado nao implementado |
| Valores positivos e soma percentual 100 | ADR-0015; contrato | Nao implementado para corpo | Nao localizado | Normatizado nao implementado |
| Maiores restos | ADR-0015; contrato | Implementado apenas para larguras iguais no horizontal | Horizontal coberto | Parcial |
| Sobra vertical vira linhas em branco na area | ADR-0015; contrato | Horizontal sim; vertical sobra externa ao bloco | Horizontal e fill externo cobertos | Parcial |
| Redimensionamento recalcula areas sem mudar arranjo | ADR-0017; contrato | demo recalcula largura/altura e renderer recebe altura | teste_demo/relatorios | Implementado para TUI geral |
| Terminal pequeno demais | ADR-0017; contrato | demo quadro minimo | teste_demo/relatorios | Implementado |

## 13. Contradicoes

Nao ha contradicao documental ativa bloqueante entre ADR-0015, contratos e ADR-0017 para criar um handoff de implementacao.

Ha desalinhamentos entre autoridade e implementacao:

- Contratos autorizam `corpo.distribuicao`/`grupo.distribuicao`, mas o loader retorna apenas `corpo.arranjo` e `elementos`, sem `distribuicao`.
- ADR-0015 autoriza profundidade ate 3, mas o loader atual rejeita grupo aninhado e grupo com mais de 1 elemento por escopo historico de H-0012.
- Handoffs H-0019/H-0020/H-0021 proibiram percentual/fracao em seus ciclos, enquanto a autoridade superior atual ja os normatiza. Isso nao e contradicao ativa; e registro historico de escopo.

## 14. Lacunas

- Campo `Corpo.distribuicao` ausente no modelo.
- `carregar_tela` nao preserva `corpo.distribuicao` no dict normalizado.
- Ausencia de validador de `corpo.distribuicao`.
- Ausencia de algoritmo comum para distribuir area por `igual`, `percentual` e `fracao`.
- Caminho vertical nao repassa cotas de altura para `_caixa_de_elemento`.
- `_caixa_de_elemento` nao aceita `altura_alvo`.
- Grupos nao redistribuem areas entre multiplos filhos; implementacao atual so trata grupo estrutural com um interno.
- Testes inexistentes para percentual/fracao no corpo e para arredondamento de linhas residuais.

## 15. Decisoes ja fechadas

- `vertical` e `horizontal` sao valores finais de `corpo.arranjo`; aliases sao transicionais.
- `arranjo = vertical` reparte altura entre filhos diretos do container.
- Distribuicao pertence ao mesmo container que declara o arranjo.
- Distribuicao aloca area, nao apenas conteudo.
- Modos `igual`, `percentual` e `fracao` estao normatizados.
- Percentuais somam exatamente 100.
- Fracao usa pesos relativos.
- Arredondamento usa maiores restos e empates seguem ordem declarada.
- Sobra vertical vira linhas em branco.
- Redimensionamento reativo nao altera composicao declarativa.

## 16. Decisoes ainda ausentes

Ausentes ou apenas conceituais para ciclos futuros:

- Schema final de restricoes dimensionais (`minimo`, `preferido`, `maximo`, `restante`, `conteudo`) por elemento/container.
- Schema final de sincronizacao explicita de cortes.
- Politica completa de grupos aninhados na implementacao corrente, embora a autoridade conceitual de ate 3 niveis ja exista.

Nao foi localizada decisao ausente que bloqueie a criacao de handoff para implementar distribuicao vertical basica + `igual`/`percentual`/`fracao` conforme regras ja documentadas.

## 17. Riscos para criacao do handoff

- Risco de confundir `barra_de_menus.distribuicao` com `corpo.distribuicao`; os nomes compartilham palavra, mas os contratos separam os dominios.
- Risco de alterar o comportamento horizontal ja coberto por H-0019/H-0021 ao criar helper comum.
- Risco de tratar fill externo H-0015 como distribuicao vertical por filho; hoje ele apenas preenche a sobra global.
- Risco de implementar grupos aninhados ou restricoes dimensionais dinamicas alem do necessario para percentual/fracao.
- Risco de usar `vertical` como substring ambigua e afetar ocupacao vertical do terminal, violando ADR-0013/ADR-0017.

## 18. Classificacao do futuro ciclo

| Item | Categoria | Evidencia |
|---|---|---|
| distribuicao vertical basica | NORMATIZADO_NAO_IMPLEMENTADO | ADR-0015 linhas 107-118; renderer vertical linhas 927-998 nao distribui por filho |
| preenchimento da area vertical disponivel | PARCIALMENTE_IMPLEMENTADO | fill externo vertical linhas 956-998; area por filho apenas no horizontal linhas 749-793 |
| modo percentual | NORMATIZADO_NAO_IMPLEMENTADO | ADR-0015 linhas 142-150; sem codigo para corpo |
| modo por fracao | NORMATIZADO_NAO_IMPLEMENTADO | ADR-0015 linhas 152-163; sem codigo para corpo |
| validacao declarativa | PARCIALMENTE_IMPLEMENTADO | loader valida arranjo linhas 353-360; nao valida distribuicao |
| arredondamento e linhas residuais | PARCIALMENTE_IMPLEMENTADO | horizontal usa resto de largura linhas 718-723; linhas verticais nao cobertas |
| tratamento de altura insuficiente | PARCIALMENTE_IMPLEMENTADO | renderizador levanta erro por altura insuficiente linhas 969-985; TUI mostra quadro minimo linhas 460-471; minimos por elemento sao futuros |
| integracao com redimensionamento | PARCIALMENTE_IMPLEMENTADO | demo recalcula dimensoes linhas 518-592; novo algoritmo vertical ainda inexistente |
| testes automatizados | PARCIALMENTE_IMPLEMENTADO | altura/horizontal cobertos; percentual/fracao/vertical por area ausentes |
| validacao manual em TTY | JA_NORMATIZADO_E_IMPLEMENTADO | H-0023/IMP-0024 registram validacao; nao aplicavel especificamente ao algoritmo ainda inexistente |

## 19. Recomendacao da unica proxima categoria

`CRIAR_HANDOFF`

Justificativa: as regras necessarias para distribuir altura em `arranjo = "vertical"` e para modos `igual`, `percentual` e `fracao` ja estao documentadas em ADR ativa e contratos ativos, sem contradicao documental bloqueante localizada. O problema principal e lacuna de implementacao/testes, nao falta de ADR.

## 20. Evidencias por arquivo e linha

- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`: valores finais e aliases, linhas 70-96; nao implementa migracao, linhas 123-128.
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`: altura disponivel e preenchimento pelo renderer, linhas 81-100; distincao de `corpo.arranjo = "vertical"`, linhas 102-125 e 148-164.
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`: arranjo vertical reparte altura, linhas 107-118; distribuicao por container, linhas 122-133; modos, linhas 136-163; quantidade de valores, linhas 171-180; maiores restos, linhas 189-209; preenchimento, linhas 238-247.
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`: SIGWINCH e dimensoes, linhas 81-185; terminal pequeno demais, linhas 198-228.
- `docs/contratos/contrato_composicao_corpo.md`: objetivo e ADRs aplicadas, linhas 29-39; `grupo`, linhas 113-129; `arranjo`, linhas 170-180; altura disponivel, linhas 234-266; arranjo/distribuicao, linhas 268-298; modos e arredondamento, linhas 509-576; regras R-17 a R-24, linhas 752-793.
- `docs/contratos/contrato_tela_json.md`: corpo e distribuicao, linhas 158-206; arranjo, linhas 238-253; execucao TTY, linhas 653-699; redimensionamento, linhas 703-831.
- `docs/contratos/contrato_json_tela_minima.md`: exemplo `arranjo = "vertical"`, linhas 101-132; campo opcional `corpo.arranjo`, linhas 148-168; grupo/distribuicao, linhas 186-215.
- `config/telas/orquestrador.json`: corpo vertical com tres elementos, linhas 23-123.
- `config/telas/grupo_minimo.json`: corpo e grupo verticais, linhas 8-15.
- `tela/loader.py`: arranjos aceitos, linhas 33-37; validacao de grupo, linhas 146-229; validacao de corpo/arranjo e retorno sem distribuicao, linhas 318-369.
- `tela/modelo.py`: `Corpo` sem distribuicao, linhas 57-63; construcao do corpo, linha 263.
- `tela/renderizador.py`: `_caixa`, linhas 172-188; distribuicao da barra, linhas 259-285, 292-489 e 582-664; corpo horizontal, linhas 696-793; renderizacao vertical/fill, linhas 889-998.
- `tela/demo.py`: dimensoes e SIGWINCH, linhas 343-426; quadro minimo, linhas 437-471; loop TTY reativo, linhas 518-592.
- `tela/teste_renderizador.py`: altura explicita, linhas 958-1151; arranjo horizontal/vertical preservado, linhas 2276-2606; preenchimento horizontal, linhas 2609-2917; nao regressao H-0021, linhas 2921-3296.
- `tela/teste_loader.py`: validacao de arranjo, linhas 724-809; grupo estrutural, linhas 532-675.
- `tela/teste_modelo.py`: corpo vertical e grupo preservado, linhas 113-127 e 370-372.

## 21. Arquivos criados ou alterados

Criado por este levantamento:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
```

Nenhum outro arquivo foi alterado por este levantamento.
