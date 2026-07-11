# RELATORIO_QA_H-0024_HANDOFF

## 1. Identificacao

Relatorio formal de QA do handoff `H-0024`.

Artefato auditado:

```text
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
```

Status final:

```text
H2_HANDOFF_PATCH_REQUIRED
```

Unica proxima categoria:

```text
PATCH_HANDOFF
```

## 2. Escopo do QA

Este QA avaliou exclusivamente o handoff H-0024 contra a decisao explicita do usuario, as autoridades normativas ativas, o relatorio de levantamento e o estado real do repositorio.

Nao foram corrigidos problemas do handoff. Nao foi implementado codigo. Nao foi criado ADR, contrato, prompt de proxima etapa, commit, stage ou alteracao de historico Git.

## 3. Estado Git inicial

Comandos executados:

```text
git status --short
?? docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
```

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

```text
git branch --show-current
master
```

Verificacao do caminho do relatorio de QA antes da escrita:

```text
docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md
nao existia
```

Stage: vazio. Arquivos rastreados modificados: nenhum no inicio do QA. Arquivos nao rastreados esperados: levantamento e handoff H-0024. Stash preservado.

O handoff novo foi inspecionado com `git diff --no-index /dev/null docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`; o retorno `1` foi tratado como esperado para arquivo novo com diferencas.

## 4. Artefatos auditados

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`
- estado real do repositorio, codigo e testes relacionados ao escopo permitido/proibido

## 5. Autoridades

Autoridades lidas nas versoes atuais do repositorio:

- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/NOMENCLATURA.md`

A ordem de autoridade usada neste QA foi: decisao explicita do usuario; documentacao normativa ativa; ADR aprovada e aplicada; contrato ativo; handoff; implementacao; relatorios e conversas.

## 6. Metodo

O QA comparou textualmente as afirmacoes do handoff com as autoridades, com o levantamento e com o codigo atual. Foram verificados: fidelidade normativa, lacunas preservadas, coerencia interna, capacidade coesa, arquivos permitidos/proibidos, escopo positivo/negativo, especificacao por modulo, criterios de aceite, testes, relatorio de implementacao, validacao manual, condicoes de bloqueio e ausencia de implementacao antecipada.

## 7. Matriz de conformidade

| Item | Resultado | Evidencia |
|---|---|---|
| Decisao explicita: vertical + percentual/fracao | Conforme | Handoff linhas 34-37 e 250-271 |
| Autoridades obrigatorias localizadas | Conforme | Todos os caminhos existem |
| Semantica de `vertical` | Conforme | Handoff linhas 103-108, 223-228; ADR-0011 linhas 70-96; ADR-0013 linhas 102-164 |
| Percentual | Conforme | Handoff linhas 169-176; ADR-0015 linhas 142-150; contrato linhas 515-523 |
| Fracao | Conforme | Handoff linhas 178-187; ADR-0015 linhas 152-163; contrato linhas 525-535 |
| Arredondamento e residuos | Conforme | Handoff linhas 189-207; ADR-0015 linhas 189-209; contrato linhas 544-564 |
| Preenchimento de area alocada | Conforme | Handoff linhas 209-215; ADR-0015 linhas 238-247; contrato linhas 568-575 |
| `modo = igual` | Nao conforme | Achado H2-001 |
| Arquivos permitidos tecnicos | Conforme com ressalva | Loader/modelo/renderizador/testes sao suficientes |
| Arquivos proibidos versus tarefas | Nao conforme | Achado H2-002 |
| Testes exigidos | Conforme | Handoff linhas 540-641 |
| Validacao manual | Conforme | Handoff linhas 643-659 |
| Ausencia de implementacao antecipada | Conforme | Git inicial sem codigo/teste/config alterado |

## 8. Achados

### H2-001

Severidade: media

Arquivo e linha:

```text
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md:238
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md:243
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md:405
```

Evidencia: o handoff determina que, quando `corpo.distribuicao` esta ausente ou `modo = igual`, o corpo vertical preserve o comportamento atual de empilhamento sequencial com preenchimento externo, e ainda exige que o loader aceite `modo = "igual"` sem valores.

Autoridade violada: ADR-0015 Decisao 6, linhas 138-140; `contrato_composicao_corpo.md` secao 5.7, linhas 511-513; `contrato_json_tela_minima.md` linhas 205-215. Essas autoridades definem que `igual` divide a area disponivel igualmente entre filhos diretos e que ausencia de `distribuicao` equivale a `igual`.

Impacto: o handoff cria uma semantica operacional local para `modo = igual`/ausencia distinta da autoridade normativa, ao mesmo tempo em que valida `igual` como schema aceito. Isso viola a verificacao obrigatoria de nao introduzir nova semantica para `modo = igual` e pode levar o implementador a aprovar uma configuracao explicita que nao executa a semantica normatizada.

Categoria de correcao: `HANDOFF_LOCAL`

### H2-002

Severidade: media

Arquivo e linha:

```text
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md:339
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md:358
docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md:669
```

Evidencia: o handoff exige usar `docs/templates/TEMPLATE_RELATORIO_IMPL.md` para o relatorio de implementacao, mas esse arquivo nao aparece na lista de arquivos permitidos nem na lista de arquivos somente para leitura. A secao de arquivos proibidos declara que qualquer arquivo nao listado nas secoes 8 e 9 esta proibido.

Autoridade violada: coerencia interna do handoff e regra processual solicitada pelo QA sobre compatibilidade entre arquivos proibidos e tarefas exigidas.

Impacto: o executor recebe simultaneamente uma tarefa obrigatoria que depende de um caminho especifico e uma lista fechada que proibe caminhos nao listados. A correcao e local ao handoff; nao ha necessidade de ADR ou nova regra normativa.

Categoria de correcao: `HANDOFF_LOCAL`

## 9. Analise dos arquivos permitidos e proibidos

A lista tecnica permitida e suficiente para a implementacao da capacidade principal:

- `tela/loader.py`: responsavel por carregar e validar `corpo` e `corpo.arranjo`; ainda nao valida `corpo.distribuicao`.
- `tela/modelo.py`: define `Corpo(arranjo, elementos)` e constroi o modelo; falta preservar `distribuicao`.
- `tela/renderizador.py`: contem `_caixa` com `altura_alvo`, `_caixa_de_elemento`, `_montar_corpo_horizontal` e `renderizar_tela`; e o local natural para calcular alturas, aplicar cotas e recomputar por altura recebida.
- `tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`: cobrem as responsabilidades afetadas.
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`: caminho nao conflitante no estado auditado.

A exclusao de `tela/demo.py`, `tela/teste_demo.py` e `config/telas/*.json` e tecnicamente justificavel: o redimensionamento ja chama `renderizar_tela` com altura atual, `teste_demo.py` pode ser apenas regressao, e fixtures podem ser em memoria.

Defeito localizado: o template `docs/templates/TEMPLATE_RELATORIO_IMPL.md` e exigido, mas nao listado como permitido ou somente leitura.

## 10. Analise do escopo positivo e negativo

O escopo positivo cobre carregamento, validacao declarativa, modelo, calculo de altura util, identificacao de filhos diretos, distribuicao percentual, distribuicao por fracao, arredondamento, residuos, aplicacao no renderizador, preenchimento, recomputacao por renderizacao e preservacao de cabecalho/barra/moldura.

O escopo negativo exclui horizontal, novos modos, restricoes dimensionais pendentes, sincronizacao, politicas por tipo, taxonomia, documentacao normativa, alteracoes de TTY, commit e etapas posteriores.

Nao foram localizadas capacidades independentes indevidamente agregadas, como reformulacao geral da composicao, nova arquitetura de redimensionamento ou suporte a modos `restante`/`conteudo`.

Defeito localizado: a delimitacao do `modo = igual` transforma uma semantica ja normatizada em comportamento preservado/local, o que exige patch do handoff.

## 11. Analise por modulo

Loader: o handoff define campos, forma dos dados, rejeicoes, ausencia de fallback silencioso e compatibilidade. A responsabilidade e compatível com `tela/loader.py`.

Modelo: o handoff limita o modelo a preservar `distribuicao` sem interpretar alturas, compativel com a estrutura atual de `Corpo`.

Renderizador: o handoff define entrada, area util, algoritmo, soma das alturas, arredondamento, residuos, preenchimento, bordas e separadores. A area tecnica e compativel com o codigo atual.

Redimensionamento: o handoff preserva a arquitetura de eventos e usa a altura atual de `renderizar_tela`, sem exigir alteracao em `demo.py`.

Ressalva: a aceitacao de `modo = igual` sem a semantica normativa de divisao igual precisa ser resolvida no handoff antes da implementacao.

## 12. Analise dos testes

O handoff exige casos concretos para:

- configuracoes verticais validas;
- percentual valido e invalido;
- fracao valida e invalida;
- dois elementos;
- tres ou mais elementos;
- pesos iguais e diferentes;
- altura divisivel e com resto;
- ampliacao, reducao e multiplos redimensionamentos;
- soma exata da area distribuivel;
- preservacao de bordas;
- ausencia de invasao de cabecalho/barra;
- regressao de arranjo horizontal e regressao geral.

Comandos exigidos conferidos:

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
git diff --check
git status --short
```

Nao foram executados testes automatizados neste QA de handoff, pois a etapa nao e QA de implementacao.

## 13. Analise do relatorio de implementacao previsto

O handoff exige:

```text
docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
```

O padrao numerico esta coerente com o ultimo relatorio `IMP-0024`. O caminho nao existia no estado auditado. O conteudo minimo exigido e suficiente: identificacao, autoridades, arquivos alterados, comportamento, validacoes, algoritmo, residuos, redimensionamento, testes, Git, validacao manual pendente, limitacoes, bloqueios e divergencias.

Defeito localizado: a instrucao de usar `docs/templates/TEMPLATE_RELATORIO_IMPL.md` entra em conflito com a lista fechada por omissao desse arquivo.

## 14. Validacao manual

O handoff separa adequadamente testes automatizados, pseudo-TTY e TTY real. Ele nao declara validacao humana antecipadamente concluida e obriga o implementador a registrar a validacao visual em TTY real como pendente para QA quando nao houver evidencia do usuario.

## 15. Ausencia de implementacao antecipada

O estado Git inicial continha apenas:

```text
?? docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
```

Nao havia arquivos rastreados modificados, stage preenchido, alteracoes de codigo, testes, configuracoes, documentacao normativa, relatorio de levantamento, relatorio de implementacao ou commit preparado.

## 16. Riscos residuais

- A implementacao futura deve cuidar para nao misturar `barra_de_menus.distribuicao` com `corpo.distribuicao`.
- A preservacao byte-a-byte do arranjo horizontal deve ser verificada por regressao.
- O comportamento de conteudo maior que a area alocada ainda depende da politica existente de erro/overflow, sem nova altura minima por elemento.
- A validacao manual em TTY real permanece pendente para QA posterior.

## 17. Classificacao final

Status:

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: foram localizados achados medios corrigiveis no proprio handoff, com regra ja documentada. As autoridades existem e sao suficientes para a capacidade principal. Nao ha bloqueio documental que exija ADR nova.

## 18. Unica proxima categoria

```text
PATCH_HANDOFF
```

## 19. Arquivos criados ou alterados pelo QA

Criado por esta etapa de QA:

```text
docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md
```

Nenhum outro arquivo foi alterado pelo QA.
