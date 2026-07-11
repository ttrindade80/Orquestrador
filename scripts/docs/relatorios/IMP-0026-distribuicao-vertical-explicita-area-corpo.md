---
name: IMP-0026-distribuicao-vertical-explicita-area-corpo
description: "Resultado da implementacao do H-0025 — distribuicao vertical explicita da area do corpo entre filhos diretos (modos igual/percentual/fracao) conforme ADR-0018. Ausencia de distribuicao preservada; preenchimento interno das molduras; algoritmo generico de maiores restos."
metadata:
  type: relatorio_implementacao
  status: IMPLEMENTED
  handoff_origem: H-0025
  data: 2026-07-11
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_composicao_corpo.md"
  adr_relacionadas:
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
    - docs/adr/ADR-0017-redimensionamento-reativo-tui.md
  bugs_abertos: []
---

# IMP-0026 — Relatorio de Implementacao

## Handoff executado

`H-0025 — Distribuicao vertical explicita da area do corpo`

Autoridade operacional imediata:
`docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
(QA do handoff `H1_HANDOFF_APPROVED` em
`docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md`; unica proxima categoria
`IMPLEMENTAR`).

## Status final

`IMPLEMENTED`

Nao declara QA aprovado, nao declara ciclo fechado, nao declara pronto para
commit. A implementacao foi concluida; as suutes de teste locais passam.

## 1. Identificacao

Etapa executada: `IMPLEMENTAR`.

Relatorio criado:
`docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md`.

Data: 2026-07-11.

## 2. Handoff implementado

`H-0025 — Distribuicao vertical explicita da area do corpo`, secoes 5-12.

## 3. QA do handoff

`docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md`, status `H1_HANDOFF_APPROVED`,
matriz D1-D10 conforme. Unica proxima categoria: `IMPLEMENTAR`.

## 4. ADR-0018

`docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`,
autoridade primaria. Aplicacao documental aprovada com notas
(`ADR_APPLICATION_APPROVED_WITH_NOTES` em
`docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`).

Decisoes aplicadas nesta implementacao:

- D1: arranjo e distribuicao sao distintos; arranjo vertical sozinho nao
  reparte area.
- D2: ausencia de `distribuicao` preserva a construcao orientada pelo
  conteudo (altura natural por filho + preenchimento externo ADR-0013); nao
  materializa `igual`.
- D3: distribuicao explicita reparte a altura util integral entre filhos
  diretos.
- D4: preenchimento interno das molduras; a sobra fica dentro das molduras,
  nunca acumulada externamente abaixo do ultimo filho.
- D5: `igual` explicito divide igualmente; nao e fallback da ausencia.
- D6: `percentual` generico, soma 100, maiores restos, desempate por ordem.
- D7: `fracao` generico, qualquer vetor de pesos positivos.
- D8: conteudo maior que a cota permanece fora de escopo (terminal
  insuficiente).
- D9: a alteracao do JSON pertence ao handoff (§6.3 do H-0025).
- D10: cobertura de testes minima suficiente.

## 5. Relacao com H-0024 e IMP-0025

O H-0024 foi bloqueado em `ARCHITECTURE_REVIEW_REQUIRED` (IMP-0025) pela
colisao entre a semantica entao vigente (ausencia ≡ `igual`) e a regressao
historica `tela/teste_demo.py`. A ADR-0018 forneceu a decisao que eliminou a
contradicao (ausencia preserva conteudo; reparticao so com distribuicao
explicita). O H-0025 substitui operacionalmente o H-0024. Tanto o H-0024
quanto o IMP-0025 permanecem preservados como evidencia historica, sem
autoridade normativa superior, e nao foram alterados.

## 6. Estado Git inicial

Verificado antes de qualquer alteracao (conforme H-0025 §3):

```text
git branch --show-current      -> master
git rev-parse HEAD             -> 3332773a3f10e716115a164148af323fa86e608f
git log -1 --oneline           -> 3332773 feat: implementa redimensionamento reativo da TUI
git diff --check               -> sem saida
git diff --cached --stat       -> sem saida
git stash list                 -> stash@{0}: pre-H-0022 recuperado apos drop acidental
git rev-parse stash@{0}        -> 21f98d0f4a479d72e6df21b1dca1511c3ad38937
```

Estado conforme: branch, HEAD, stage vazio, ausencia de conflito/operacao
Git ativa, stash preservado. Os 6 documentos rastreados modificados e os
artefatos nao rastreados do ciclo ADR-0018/H-0024/H-0025 ja estavam presentes
(aplicacao documental acumulada) e nao foram confundidos com alteracoes desta
implementacao.

## 7. Seguranca entre sessoes

Antes de qualquer alteracao, foram feitas somente verificacoes de leitura.
Nao foi identificada outra sessao modificando o workspace: nao havia
operacao Git ativa, lock Git, stage preenchido, `MERGE_HEAD`, `REBASE_HEAD`,
`CHERRY_PICK_HEAD`, `REVERT_HEAD` nem `index.lock`. Nenhum comando
destrutivo de Git foi executado. O stash nao foi manipulado.

## 8. Arquivos lidos

Autoridades obrigatorias (leitura integral):

- `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
- `docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/NOMENCLATURA.md`

Evidencia historica (somente leitura, sem autoridade superior):

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`

Codigo/testes/JSON lidos antes de editar:

- `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`
- `tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`
- `tela/teste_demo.py`, `tela/demo.py`
- `config/telas/orquestrador.json`
- `docs/templates/TEMPLATE_RELATORIO_IMPL.md`

## 9. Arquivos alterados

Somente arquivos da lista fechada do H-0025 §7.1:

| Arquivo | Alteracao |
|---|---|
| `tela/loader.py` | validacao opcional de `corpo.distribuicao` (igual/percentual/fracao); preservacao da ausencia |
| `tela/modelo.py` | campo `distribuicao` em `Corpo`; preservacao sem conversao |
| `tela/renderizador.py` | algoritmo generico de cotas (maiores restos, desempate); preenchimento interno; helpers `_pesos_distribuicao`/`_distribuir_alturas`; `altura_alvo` em `_caixa_de_elemento` |
| `tela/teste_loader.py` | validacao de distribuicao (ausencia, igual, percentual, fracao, erros) |
| `tela/teste_modelo.py` | preservacao de distribuicao no modelo (presente e ausente) |
| `tela/teste_renderizador.py` | `TestDistribuicaoVerticalH0025`; adaptacao de testes H-0015 para modelo sem distribuicao |
| `tela/teste_demo.py` | adaptacao minima do sub-cenario altura=15 (H-0025 §11.5 item 1) |
| `config/telas/orquestrador.json` | declaracao `distribuicao: {modo: fracao, valores: [2,1,2]}` |
| `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md` | criado (este relatorio) |

Nenhum arquivo fora da lista fechada foi alterado por esta implementacao. Os
6 documentos rastreados modificados (`docs/NOMENCLATURA.md`,
`docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_*.md`) sao alteracoes
acumuladas da aplicacao documental da ADR-0018, pre-existentes ao inicio
desta etapa, e nao foram tocados.

## 10. Comportamento sem distribuicao

Quando `corpo.distribuicao` esta ausente (ADR-0018 D2):

- o loader nao materializa `modo: igual` nem cria objeto `distribuicao`
  (`corpo.distribuicao` permanece `None`);
- o modelo preserva `corpo.distribuicao is None`;
- o renderer percorre o caminho orientado pelo conteudo: cada filho usa sua
  altura natural; com altura explicita, o preenchimento externo H-0013/H-0015
  (linhas de espacos abaixo do ultimo filho) e preservado integralmente;
- telas existentes sem distribuicao (`destino_minimo`, `grupo_minimo`,
  `stub_b`) nao sofrem alteracao comportamental.

Verificacao: `teste_ausencia_preserva_altura_natural_sem_cota`,
`teste_ausencia_nao_materializa_igual_no_modelo`,
`test_telas_sem_distribuicao_nao_mudam`.

## 11. Validacao dos modos

Implementada em `_validar_distribuicao_corpo` (`tela/loader.py`):

- `igual`: declarado explicitamente; nao exige `valores`; nao e fallback da
  ausencia; pesos equivalentes derivados no renderer.
- `percentual`: um valor por filho direto; todos positivos; soma
  exatamente 100; associacao posicional; erro deterministico (`TelaEstruturaInvalida`).
- `fracao`: um peso por filho direto; todos estritamente positivos;
  denominador igual a soma dos pesos; qualquer vetor valido aceito;
  associacao posicional; erro deterministico.
- `len(valores) == len(elementos)` (filhos diretos do container).
- `bool` nao e aceito como numero (validado separadamente).

Cobertura: `teste_distribuicao_corpo_h0025` (loader, 16 verificacoes).

## 12. Representacao no modelo

`Corpo` (`tela/modelo.py`) recebeu o campo `distribuicao: dict | None = None`.
`construir_modelo` passa `corpo_raw.get("distribuicao")` sem conversao, sem
revalidacao e sem substituir valores declarados. Ausencia vira `None`
(distinta de `igual`).

## 13. Algoritmo de cotas

`_distribuir_alturas(altura_disponivel, pesos)` (`tela/renderizador.py`):

1. cota ideal real = `altura * peso / soma_dos_pesos`;
2. parte inteira (floor);
3. `faltam = altura - sum(partes_inteiras)`;
4. ordena indices por resto fracionario decrescente, desempatando por indice
   crescente (ordem declarada);
5. atribui uma unidade aos `faltam` maiores restos.

Invariantes: `sum(cotas) == altura_disponivel`; cotas inteiras nao negativas;
empates resolvidos pela ordem declarada.

Exemplos normativos conferidos (contrato secao 5.8):
`68,[1,1,1] -> [23,23,22]`; `68,[2,1,2] -> [27,14,27]`.

## 14. Maiores restos

Verificado em `test_algoritmo_maiores_restos_distribui_residuo`:
`10,[1,1,1] -> [4,3,3]` (floor `[3,3,3]`, falta 1, maior resto recebe).

## 15. Desempate

Verificado em `test_algoritmo_desempate_por_ordem_declarada`:
`14,[1,1,1] -> [5,5,4]` (3-way tie, dois primeiros por ordem declarada);
`5,[2,2] -> [3,2]` (empate, primeiro declarado recebe).

## 16. Preenchimento interno

Quando a cota atribuida e maior que a altura natural do filho (ADR-0018 D4):
a moldura ocupa toda a cota via `_caixa(altura_alvo=cota)` (linhas em branco
bordeadas `│ ... │` inseridas entre o conteudo e a base, dentro da moldura).
A sobra nao fica acumulada externamente abaixo do ultimo filho.

Verificado em `test_preenchimento_interno_moldura_ocupa_cota` e
`test_sem_sobra_externa_abaixo_do_ultimo_filho`.

## 17. Alteracao do JSON real

`config/telas/orquestrador.json`, objeto `corpo`:

```json
"distribuicao": {
  "modo": "fracao",
  "valores": [2, 1, 2]
}
```

Validado por `python -m json.tool` e pelo loader. Demais campos preservados.

## 18. Ordem dos filhos

Confirmada apos a alteracao, sem reordenacao:

```text
1. console_principal   (console)
2. dashboard_info      (dashboard)
3. lancador_principal  (lancador)
```

## 19. Associacao `[2,1,2]`

Associacao posicional pela ordem declarada (H-0025 §6.3):

| Posicao | Filho | Peso |
|---|---|---|
| 1 | `console_principal` | 2 |
| 2 | `dashboard_info` | 1 |
| 3 | `lancador_principal` | 2 |

`[2,1,2]` e configuracao concreta do Orquestrador, nao hardcode do renderer.
O algoritmo trata `[1,1,1]`, `[2,1,2]`, `[1,3,1]` e `[5,2,7]` pelo mesmo
codigo generico, sem condicao especial.

## 20. Tratamento do cenario historico de altura 15

Conforme H-0025 §11.5 (item 1): o sub-cenario `altura=15` em
`tela/teste_demo.py::teste_renderizar_estado_altura` foi substituido por um
modelo do orquestrador SEM `distribuicao` (fixture isolada construida por
copia do `tela_raw` sem o campo `distribuicao`). Isso preserva a cobertura
"altura minima sem fill = saida natural" para uma tela sem distribuicao.

Justificativa: o orquestrador real agora declara distribuicao; em `altura=15`
a cota de algum filho fica menor que sua altura natural (terminal
insuficiente), caso explicitamente fora de escopo pela D8 da ADR-0018. O
vetor `[2,1,2]` permanece matematicamente valido; `altura=15` nao e tratada
como altura suportada normativa do produto. Nenhuma politica de altura
minima, overflow, truncamento nem redistribuicao por altura natural foi
introduzida. A cobertura de redimensionamento do H-0023
(`teste_redimensionamento_reativo_h0023`) nao foi removida.

Os testes H-0015 de preenchimento externo em `tela/teste_renderizador.py`
(`teste_altura_explicita`, `test_altura_minima_com_barra_horizontal`,
`test_renderizar_tela_preserva_altura_h0015`,
`test_vertical_nao_regride_apos_h0021`) foram adaptados para usar o helper
`_modelo_orquestrador_sem_distribuicao()`, preservando integralmente a
cobertura do comportamento H-0013/H-0015 para telas sem distribuicao.

## 21. Preservacao do arranjo horizontal

A distribuicao horizontal nao foi implementada neste ciclo (fora de escopo,
H-0025 §9). O arranjo horizontal existente (H-0019/H-0020/H-0021) permanece
sem regressao. Verificado em
`test_arranjo_horizontal_nao_regride_com_distribuicao`: um modelo com
`arranjo=horizontal` + `distribuicao` declarada continua renderizando pelo
particionamento contiguo (bordas `╮╭` presentes, largura total preservada).

## 22. Testes criados ou ajustados

Novos:

- `teste_distribuicao_corpo_h0025` (`tela/teste_loader.py`): 16 verificacoes
  de validacao (ausencia, igual, percentual valido/invalido, fracao
  valido/invalido, quantidade, modo, tipo, bool, constante).
- `TestDistribuicaoVerticalH0025` (`tela/teste_renderizador.py`): 54
  verificacoes cobrindo algoritmo (exemplos normativos, soma exata, vetores
  genericos, maiores restos, desempate, pesos), ausencia, `igual`,
  `percentual`, `fracao [1,1,1]`/`[2,1,2]`/`[1,3,1]`/`[5,2,7]`, soma das
  cotas, ausencia de sobra externa, preenchimento interno, JSON real,
  redimensionamento, telas sem distribuicao, arranjo horizontal.
- Modelo: 2 verificacoes (preservacao de distribuicao presente e ausente).

Ajustados (minimamente, para preservar cobertura H-0013/H-0015 em telas sem
distribuicao):

- `teste_altura_explicita` (usa `_modelo_orquestrador_sem_distribuicao`).
- `test_altura_minima_com_barra_horizontal`.
- `test_renderizar_tela_preserva_altura_h0015`.
- `test_vertical_nao_regride_apos_h0021`.
- `teste_renderizar_estado_altura` (sub-cenario altura=15, H-0025 §11.5).

Helper adicionado: `_modelo_orquestrador_sem_distribuicao()`.

## 23. Comandos executados

| Comando | Codigo de saida |
|---|---|
| `python -m json.tool config/telas/orquestrador.json` | 0 |
| `python tela/teste_loader.py` | 0 |
| `python tela/teste_modelo.py` | 0 |
| `python tela/teste_renderizador.py` | 0 |
| `python tela/teste_demo.py` | 0 |
| `git diff --check` | 0 (sem saida) |
| `git diff --stat` | 0 |
| `git diff --name-only` | 0 |
| `git status --short` | 0 |
| `git diff --cached --stat` | 0 (sem saida) |
| `git diff --cached --name-only` | 0 (sem saida) |
| `git diff --no-index /dev/null docs/relatorios/IMP-0026-...md` | 1 (esperado p/ arquivo novo) |

## 24. Resultados completos

| Suite | Total | Passaram | Falharam | Codigo de saida |
|---|---|---|---|---|
| `tela/teste_loader.py` | 105 | 105 | 0 | 0 |
| `tela/teste_modelo.py` | 58 | 58 | 0 | 0 |
| `tela/teste_renderizador.py` | 385 | 385 | 0 | 0 |
| `tela/teste_demo.py` | 303 | 303 | 0 | 0 |

Nenhuma falha ocultada. Os controles cresceram em relacao ao baseline
(loader 89->105; modelo 56->58; renderizador 331->385; demo 303->303).

## 25. Limitacoes

- Conteudo maior que a cota (terminal insuficiente) permanece fora de escopo
  (ADR-0018 D8). Em alturas muito pequenas com distribuicao declarada, o
  renderer pode levantar `RenderizadorErro` (sem truncamento). Nenhuma
  politica de altura minima, overflow, truncamento, paginacao de `lancador`,
  rejeicao, degradacao, redistribuicao por altura natural nem prioridade por
  tipo foi introduzida.
- A distribuicao horizontal nao foi implementada (fora de escopo).
- Grupos aninhados com distribuicao propria nao foram implementados (fora de
  escopo). A distribuicao aplica-se ao container `corpo`.

## 26. Itens diferidos

- Cobertura ampla de combinacoes (matriz exaustiva de vetores, alturas e
  quantidades de filhos): diferida para handoff de testes posterior (D10).
- Validacao manual visual em TTY real: nao realizada (ver §27).
- Distribuicao horizontal e grupos com distribuicao propria.

## 27. Validacao manual realizada ou nao realizada

Validacao manual visual em TTY real: **nao realizada**. Nenhuma evidencia de
usuario foi fornecida. A verificacao automatica confirma: (a) a distribuicao
ocorre apenas com `distribuicao` explicita + `altura` fornecida; (b) a soma
das cotas ocupa toda a area distribuivel; (c) a sobra e absorvida
internamente nas molduras; (d) o redimensionamento recalcula as cotas. A
verificacao visual em terminal real permanece pendente para ciclo posterior.

## 28. Estado Git final

```text
git branch --show-current      -> master
git rev-parse HEAD             -> 3332773a3f10e716115a164148af323fa86e608f
git diff --check               -> sem saida
git diff --cached --stat       -> sem saida
git diff --cached --name-only  -> sem saida
```

Rastreados modificados por esta implementacao (8 arquivos permitidos):
`config/telas/orquestrador.json`, `tela/loader.py`, `tela/modelo.py`,
`tela/renderizador.py`, `tela/teste_demo.py`, `tela/teste_loader.py`,
`tela/teste_modelo.py`, `tela/teste_renderizador.py`.

Rastreados modificados pre-existentes (aplicacao ADR-0018, nao tocados aqui):
`docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`,
`docs/contratos/contrato_composicao_corpo.md`,
`docs/contratos/contrato_json_tela_minima.md`,
`docs/contratos/contrato_processo_desenvolvimento.md`,
`docs/contratos/contrato_tela_json.md`.

## 29. Estado do stash

```text
git stash list          -> stash@{0}: pre-H-0022 recuperado apos drop acidental
git rev-parse stash@{0} -> 21f98d0f4a479d72e6df21b1dca1511c3ad38937
```

Stash preservado. Nenhum comando de manipulacao de stash foi executado.

## 30. Arquivos nao rastreados

Pre-existentes do ciclo ADR-0018/H-0024/H-0025 (nao criados por esta etapa,
exceto o IMP-0026):

- `docs/adr/ADR-0018-...md`
- `docs/handoff/H-0024-...md`, `docs/handoff/H-0025-...md`
- `docs/relatorios/IMP-0025-...md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_...md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_...md`
- `docs/relatorios/RELATORIO_QA_ADR-0018.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md`
- `docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_H-0025_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md`

Criado por esta etapa:

- `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md`

## 31. Bloqueios

Nenhum. A implementacao foi concluida dentro do escopo autorizado sem
necessidade de decisao arquitetural adicional. Nao houve
`ARCHITECTURE_REVIEW_REQUIRED`, `BLOCKED_EVIDENCE` nem
`BLOCKED_REPOSITORY_STATE`.

## 32. Conclusao da implementacao sem autoaprovacao

A implementacao do H-0025 foi concluida. As suutes de teste locais passam
(loader 105/105, modelo 58/58, renderizador 385/385, demo 303/303). O JSON
real do Orquestrador declara `distribuicao: {modo: fracao, valores: [2,1,2]}`
e a ordem/associacao dos filhos foi preservada. A ausencia de distribuicao
preserva o comportamento orientado pelo conteudo. O algoritmo e generico
(maiores restos, desempate por ordem declarada, preenchimento interno).

Este relatorio **nao** declara QA aprovado, **nao** declara ciclo fechado e
**nao** declara pronto para commit. A autoaprovacao nao e realizada.

## Arquivos alterados

| Arquivo | Alteracao |
|---|---|
| `scripts/tela/loader.py` | modificado |
| `scripts/tela/modelo.py` | modificado |
| `scripts/tela/renderizador.py` | modificado |
| `scripts/tela/teste_loader.py` | modificado |
| `scripts/tela/teste_modelo.py` | modificado |
| `scripts/tela/teste_renderizador.py` | modificado |
| `scripts/tela/teste_demo.py` | modificado |
| `scripts/config/telas/orquestrador.json` | modificado |
| `scripts/docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md` | criado |

## Evidencia por criterio de aceite

| Criterio do handoff | Evidencia | Resultado |
|---|---|---|
| 1 JSON sem distribuicao valido/carregado | `destino_minimo`, `grupo_minimo`, `stub_b` carregam; `teste_telas_sem_distribuicao_nao_mudam` | OK |
| 2 Ausencia nao gera igual/objeto | `teste_ausencia_nao_materializa_igual_no_modelo`; loader retorna `None` | OK |
| 3 igual explicito divide igualmente | `test_igual_explicito_divide_igualmente` ([6,6,6]) | OK |
| 4 percentual exige soma 100 | loader rejeita soma!=100; `test_percentual_explicito` | OK |
| 5 fracao aceita vetor positivo | `test_fracao_111/212/vetor_generico_adicional` | OK |
| 6 cardinalidade por filho direto | loader rejeita qtd incompativel | OK |
| 7 associacao posicional | `_pesos_distribuicao` + `_corpo_alturas` por ordem | OK |
| 8 soma cotas == area | `test_soma_das_cotas_igual_area_distribuivel` | OK |
| 9 maiores restos | `test_algoritmo_maiores_restos_*` | OK |
| 10 empates por ordem declarada | `test_algoritmo_desempate_por_ordem_declarada` | OK |
| 11 moldura ocupa cota | `test_preenchimento_interno_moldura_ocupa_cota` | OK |
| 12 linhas sobrantes dentro da moldura | bordas `│ ... │` nas linhas internas | OK |
| 13 sem sobra abaixo do ultimo filho | `test_sem_sobra_externa_abaixo_do_ultimo_filho` | OK |
| 14 sem distribuicao preserva conteudo | `test_ausencia_preserva_altura_natural_sem_cota` | OK |
| 15 `[1,1,1]` | `test_fracao_111` | OK |
| 16 `[2,1,2]` | `test_fracao_212` | OK |
| 17 outros vetores genericos | `test_fracao_vetor_generico_adicional` ([1,3,1],[5,2,7]) | OK |
| 18 JSON declara `[2,1,2]` | `test_json_real_orquestrador_distribui_212` | OK |
| 19 JSON sintaticamente valido | `python -m json.tool` | OK |
| 20 loader preserva declaracao | `teste_caminho_feliz` (H-0025) | OK |
| 21 modelo preserva sem conversao | `teste_modelo_orquestrador` (H-0025) | OK |
| 22 cenario real distribui area | `test_json_real_orquestrador_distribui_212` ([7,4,7]) | OK |
| 23 telas sem distribuicao inalteradas | `test_telas_sem_distribuicao_nao_mudam` | OK |
| 24 arranjo horizontal sem regressao | `test_arranjo_horizontal_nao_regride_com_distribuicao` | OK |
| 25 sem politica de altura minima/overflow | nenhuma introduzida; D8 fora de escopo | OK |
| 26 altura=15 nao invalida vetor valido | adaptado conforme §11.5 | OK |
| 27 testes minimos passam | ver §24 | OK |
| 28 nenhum arquivo fora da lista | ver §9 e §33 | OK |

## Aderencia ao contrato

| Regra contratual | Evidencia | Resultado |
|---|---|---|
| contrato_composicao_corpo.md §4.8/4.9/5.7/5.8/5.9 | distribuicao opcional; ausencia != igual; maiores restos; preenchimento interno | OK |
| contrato_tela_json.md secao 8 (corpo.distribuicao) | ausencia preserva conteudo; explicita reparte area | OK |
| contrato_json_tela_minima.md §6.3 | ausencia nao equivale a igual | OK |
| NOMENCLATURA.md | distincao arranjo x distribuicao preservada | OK |

## Bloqueios

Nenhum.

## Observacoes para QA

- A adaptacao dos testes H-0013/H-0015 para usar
  `_modelo_orquestrador_sem_distribuicao()` preserva a cobertura original de
  preenchimento externo para telas sem distribuicao. Recomenda-se conferir
  que o helper produz alturas naturais identicas ao orquestrador original
  (3+2+4=9 no corpo), o que e verificado pelos asserts de cotas.
- O cenario de altura=15 em `teste_demo.py` agora usa modelo sem distribuicao
  (H-0025 §11.5 item 1). O orquestrador real com distribuicao em altura=15
  levanta `RenderizadorErro` (terminal insuficiente, D8) — comportamento
  esperado e fora de escopo.
- A validacao visual em TTY real nao foi realizada.
