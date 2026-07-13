---
name: IMP-0030-catalogo-telas-utilizaveis
description: "Resultado da implementacao do catalogo de cinco telas utilizaveis (console, dashboard, matrizes 2x2/3x2/2x4) integradas ao lancador do orquestrador"
metadata:
  type: relatorio_implementacao
  status: IMPLEMENTED
  handoff_origem: H-0030
  data: 2026-07-13
rastreabilidade:
  handoff_origem: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  adrs_base:
    - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  contratos_aplicaveis:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_json_lancador.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_json_dashboard.md
  commit_base: 9ae4aa4
  bugs_abertos: []
---

# IMP-0030 — Catalogo de telas utilizaveis

## 1. Identificacao e estado inicial

- Ciclo: `H-0030 — Catalogo de telas utilizaveis`.
- Commit-base verificado: `9ae4aa4 fix: corrige distribuicao com cardinalidade unitaria`.
- Estado Git antes da implementacao: HEAD `9ae4aa4`; somente os tres documentos
  nao rastreados esperados do ciclo documental (`H-0030-catalogo-telas-utilizaveis.md`,
  `RELATORIO_QA_H-0030_HANDOFF.md`, `RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md`);
  `git diff` rastreado vazio; `git diff --cached` vazio; `git diff --check`
  sem mensagens.
- Baseline da suite canonica antes da implementacao: 1449/1449 verificacoes,
  todos os seis scripts com codigo de saida 0.

## 2. Arquivos e telas

### 2.1 Arquivos criados

| Arquivo | Conteudo |
|---|---|
| `scripts/config/telas/h0030_console_unico.json` | Fixture de console unico |
| `scripts/config/telas/h0030_dashboard_unico.json` | Fixture de dashboard unico |
| `scripts/config/telas/h0030_matriz_2x2.json` | Fixture de matriz 2x2 |
| `scripts/config/telas/h0030_matriz_3x2.json` | Fixture de matriz 3x2 |
| `scripts/config/telas/h0030_matriz_2x4.json` | Fixture de matriz 2x4 |
| `scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md` | Este relatorio |

### 2.2 Arquivos modificados

| Arquivo | Alteracao |
|---|---|
| `scripts/config/telas/orquestrador.json` | Acrescentados 5 itens ao array `lancador_principal.itens` (nicos 1..5); nenhum outro campo alterado |
| `scripts/tela/teste_loader.py` | Atualizada assercao de 2 para 7 itens do lancador; adicionada funcao `teste_h0030_catalogo` com cobertura de carregamento, integracao no lancador e preservacoes |
| `scripts/tela/teste_modelo.py` | Atualizada assercao de 2 para 7 itens do lancador; adicionada classe `TestModeloCatalogoH0030` com interpretacao de modelo das 5 telas |
| `scripts/tela/teste_renderizador.py` | Atualizados snapshots `_EXPECTED_ORQUESTRADOR`/`_EXPECTED_ORQUESTRADOR_RETA` e dimensoes do teste de altura explicita (NAVEGAR de 4 para 9 linhas); adicionada classe `TestCatalogoH0030` com verificacoes geometricas das matrizes |
| `scripts/tela/teste_demo.py` | Atualizados snapshots `_EXPECTED_CURVA`/`_EXPECTED_RETA`/`_EXPECTED_DIAGNOSTICO_CURVA_42`; `_ALTURA_SUBPROCESS` de 24 para 30; env do subprocess passa a fixar `COLUMNS=80/LINES=30`; adicionada funcao `teste_navegacao_h0030` com smoke tests dos chips 1..5 |
| `scripts/tela/teste_diagnostico.py` | Atualizado SOMENTE o snapshot `_EXPECTED_ORQUESTRADOR` (justificativa na secao 12). Apos o patch QA-IMP-H0030-BAIXO-001, o diff fica restrito ao snapshot (ver secao 14) |

### 2.3 Identificacao de cada tela

| Tela | `id` | Arquivo | Rotulo no lancador | Chip | `tela_destino` |
|---|---|---|---|---|---|
| Console unico | `h0030_console_unico` | `config/telas/h0030_console_unico.json` | `Console` | `1` | `h0030_console_unico` |
| Dashboard unico | `h0030_dashboard_unico` | `config/telas/h0030_dashboard_unico.json` | `Dashboard` | `2` | `h0030_dashboard_unico` |
| Matriz 2x2 | `h0030_matriz_2x2` | `config/telas/h0030_matriz_2x2.json` | `Matriz 2x2` | `3` | `h0030_matriz_2x2` |
| Matriz 3x2 | `h0030_matriz_3x2` | `config/telas/h0030_matriz_3x2.json` | `Matriz 3x2` | `4` | `h0030_matriz_3x2` |
| Matriz 2x4 | `h0030_matriz_2x4` | `config/telas/h0030_matriz_2x4.json` | `Matriz 2x4` | `5` | `h0030_matriz_2x4` |

### 2.4 Ordem final dos itens do lancador (`lancador_principal.itens`)

1. `item_destino_minimo` (chip `d`) — destino_minimo (pre-existente, preservado)
2. `item_grupo_minimo` (chip `g`) — grupo_minimo (pre-existente, preservado)
3. `item_console_unico` (chip `1`) — h0030_console_unico (novo)
4. `item_dashboard_unico` (chip `2`) — h0030_dashboard_unico (novo)
5. `item_matriz_2x2` (chip `3`) — h0030_matriz_2x2 (novo)
6. `item_matriz_3x2` (chip `4`) — h0030_matriz_3x2 (novo)
7. `item_matriz_2x4` (chip `5`) — h0030_matriz_2x4 (novo)

Total final: 7 itens. Chips sem duplicidade: `d, g, 1, 2, 3, 4, 5`. Todos os
`texto` tem comprimento <= 15 caracteres (`Destino`=7, `Grupo Min.`=10,
`Console`=7, `Dashboard`=9, `Matriz 2x2`=10, `Matriz 3x2`=10, `Matriz 2x4`=10).

## 3. Demonstracao e testes

### 3.1 Mecanismo real de demonstracao

A demonstracao primaria e o caminho real pelo lancador, executado por
subprocess do ponto de entrada vigente `tela/demo.py` (secao 14.6 do handoff).
Para cada chip `1`..`5`, o ciclo comprovado e:

```text
orquestrador -> chip -> tela_destino correta -> Esc -> retorno ao orquestrador -> Esc -> saida
```

O `demo.py` percorre declarativamente `lancador_principal.itens[]` para decidir
`tela_destino` (sem hardcode no codigo). A tela aberta e identificada pelo
marcador de cabecalho (`H-0030 CONSOLE`, `H-0030 DASHBOARD`, `H-0030 MATRIZ 2X2`,
`H-0030 MATRIZ 3X2`, `H-0030 MATRIZ 2X4`).

Monkeypatch nao e usado como substituto do caminho real; o handoff documenta
monkeypatch (`criar_estado_inicial`) apenas como tecnica complementar/focal
(secao 10.2), nao empregada como prova unica aqui.

### 3.2 Smoke tests do `demo.py` (secao 14.6)

| Chip | Tela aberta | Ciclo rc=0 | Marcador presente | Orquestrador apos Esc | Destino incorreto ausente | 3 renders (orq,dest,orq) |
|---|---|---|---|---|---|---|
| `1` | h0030_console_unico | OK | OK | OK | OK | OK |
| `2` | h0030_dashboard_unico | OK | OK | OK | OK | OK |
| `3` | h0030_matriz_2x2 | OK | OK | OK | OK | OK |
| `4` | h0030_matriz_3x2 | OK | OK | OK | OK | OK |
| `5` | h0030_matriz_2x4 | OK | OK | OK | OK | OK |

Cada ciclo gera exatamente `3 * 30 = 90` newlines (3 renders x altura 30) e
stderr vazio. A saida bate por igualdade estrita com `renderizar_tela(orq) +
renderizar_tela(dest) + renderizar_tela(orq)` em largura 80 / altura 30.

Preservacoes comprovadas em `teste_demo.py`:

| Fluxo | Resultado |
|---|---|
| Chip `d` continua abrindo `destino_minimo` | OK |
| Chip `g` continua abrindo `grupo_minimo` | OK |
| Chip nao declarado `z` nao altera `tela_atual` | OK |
| Esc na raiz encerra o subprocess com codigo 0 | OK |

### 3.3 Fixtures permanentes criadas

| Arquivo | Proposito |
|---|---|
| `h0030_console_unico.json` | Fixture de console unico — tipo funcional minimo verificavel |
| `h0030_dashboard_unico.json` | Fixture de dashboard unico — tipo funcional minimo verificavel |
| `h0030_matriz_2x2.json` | Fixture de grade 2x2 — matriz de menor dimensao |
| `h0030_matriz_3x2.json` | Fixture de grade 3x2 — expansao vertical do grid |
| `h0030_matriz_2x4.json` | Fixture de grade 2x4 — expansao horizontal ao limite superior |

### 3.4 Testes executados e resultados por script

| Script | Verificacoes | Passaram | Falharam | Codigo de saida |
|---|---|---|---|---|
| `tela/teste_loader.py` | 244 | 244 | 0 | 0 |
| `tela/teste_modelo.py` | 148 | 148 | 0 | 0 |
| `tela/teste_renderizador.py` | 894 | 894 | 0 | 0 |
| `tela/teste_demo.py` | 358 | 358 | 0 | 0 |
| `tela/teste_diagnostico.py` | 28 | 28 | 0 | 0 |
| `tela/teste_explorar_barra_de_menus.py` | 38 | 38 | 0 | 0 |

### 3.5 Total agregado de verificacoes

**1710/1710** verificacoes aprovadas (baseline 1449, +261 de cobertura H-0030),
todos os seis scripts canonicos com codigo de saida `0`.

Incrementos por script: loader +72, modelo +60, renderizador +74, demo +55
(diagnostico +0 em contagem — apenas snapshot atualizado).

## 4. Evidencia por criterio de aceite

### 4.1 Carregamento (14.1) — `teste_loader.py`

| Criterio | Resultado |
|---|---|
| `carregar_tela` nao lanca para cada uma das 5 telas | OK |
| `id` confere com basename; `schema` == `tela.v1` | OK |
| cabecalho/corpo/barra_de_menus presentes | OK |
| console unico corpo[0].tipo == `console` | OK |
| dashboard unico corpo[0].tipo == `dashboard` | OK |
| matrizes corpo[0].tipo == `grupo`, estrutura == `matriz`, sem `arranjo` | OK |

### 4.2 Construcao de modelo (14.2) — `teste_modelo.py`

| Criterio | Resultado |
|---|---|
| `construir_modelo` nao lanca para as 5 telas | OK |
| Interpretacao do console unico (origem_dados null, itens []) | OK |
| Interpretacao do dashboard unico (2 campos literais Tipo/Ciclo) | OK |
| Dimensoes das matrizes (2x2, 3x2, 2x4) | OK |
| Coordenadas explicitas + grade integral | OK |
| Identificadores consistentes (celulas referenciam filhos) | OK |

### 4.3 Renderizacao (14.3) — `teste_renderizador.py`

| Criterio | Resultado |
|---|---|
| `renderizar_tela` sem excecao para as 5 telas (largura 80) | OK |
| Saida nao None e nao vazia | OK |
| Console unico exibe `CONSOLE`/`(console)`/`[Esc] Voltar` | OK |
| Dashboard unico exibe `dashboard único`/`H-0030`/`DASHBOARD` | OK |

### 4.3-G Verificacoes geometricas (14.3-G) — `teste_renderizador.py`

| Criterio | 2x2 | 3x2 | 2x4 |
|---|---|---|---|
| Quantidade de linhas de celulas (faixas) | 2 OK | 3 OK | 2 OK |
| Colunas por faixa | 2 OK | 2 OK | 4 OK |
| Cobertura integral (todos os rotulos de posicao) | OK | OK | OK |
| Cada rotulo aparece exatamente uma vez | OK | OK | OK |
| Divisoria vertical entre colunas | OK | OK | OK |
| Divisoria horizontal entre faixas | OK | OK | OK |
| Sem sobreposicao na mesma linha | OK | OK | OK |
| Largura alternativa 120 mantem regioes e 120 chars/linha | OK | OK | OK |

### 4.4 Integracao no lancador (14.4) — `teste_loader.py`

| Criterio | Resultado |
|---|---|
| Exatamente 7 itens em `lancador_principal.itens` | OK |
| Ordem final confere (id, chip, tela_destino) | OK |
| Chips `1`..`5` nao conflitam com `d`/`g` | OK |
| Todos os `texto` <= 15 caracteres | OK |
| Os 5 `tela_destino` novos resolvem para arquivos existentes | OK |

### 4.6 Smoke tests do demo (14.6) — `teste_demo.py`

Cobertos integralmente conforme secao 3.2 acima.

## 5. Aderencia ao contrato

| Regra contratual | Evidencia | Resultado |
|---|---|---|
| contrato_tela_json — schema/id/cabecalho/corpo/barra_de_menus | `teste_loader.teste_h0030_catalogo` | OK |
| contrato_composicao_corpo R-25 — `arranjo` proibido em matriz | loader valida; matrizes sem `arranjo` | OK |
| ADR-0020 D6 — distribuicao por eixo obrigatória em matriz | `linhas.distribuicao`/`colunas.distribuicao` declarados | OK |
| ADR-0020 D7/D8 — grade integral, coordenadas explicitas | cobertura completa em todas as matrizes | OK |
| contrato_lancador — `texto` <= 15 chars | todos os 7 itens dentro do limite | OK |
| contrato_json_console — envelope minimo (origem_dados/itens) | `h0030_console_unico` aderente | OK |
| contrato_json_dashboard — campos com `fonte: literal` | `h0030_dashboard_unico` aderente | OK |

## 6. Preservacoes

- Chips `d` (`destino_minimo`) e `g` (`grupo_minimo`) preservados, na mesma
  posicao e ordem, sem alteracao de id/rotulo/destino.
- As sete telas `h0029_*` nao foram alteradas (`git diff --stat` vazio para
  `config/telas/h0029_*.json`).
- `config/telas/grupo_minimo.json`, `config/telas/destino_minimo.json` e
  `config/telas/stub_b.json` nao foram alterados.
- `tela/demo.py`, `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`,
  `tela/diagnostico.py` nao foram alterados (`git diff --stat` vazio para
  esses modulos).
- `tela/teste_explorar_barra_de_menus.py` nao foi alterado.
- Nenhum commit foi realizado; nenhum stage foi realizado (`git diff --cached`
  vazio ao final).

## 7. Limitacoes

- A renderizacao das matrizes exige `altura` explicita no `renderizar_tela`
  (comportamento pre-existente do renderer H-0028: matriz requer
  `altura_disponivel` para distribuir linhas). Os testes geometricos usam
  `altura=24` (largura 80) e `altura=24` (largura 120), dimensoes deterministicas.
- O orquestrador com 7 itens no lancador requer altura >= 28 em largura 80
  (caixa NAVEGAR com 7 itens = 9 linhas). Por isso o subprocess da demo agora
  fixa `COLUMNS=80/LINES=30` (em vez de remover as variaveis e forçar o
  fallback 80x24), para que o orquestrador renderize em dimensao suficiente.
- A demonstracao visual em TTY real permanece exclusiva do usuario (secao 9).

## 8. Ressalvas

- A cobertura automatizada das matrizes (geometria, divisorias, cobertura,
  ausencia de sobreposicao) nao substitui a validacao visual humana; a secao
  14.3-G do handoff e explicita quanto a isso.
- Os testes de matriz verificam rotulos de posicao (`linha N, coluna M`),
  titulos de celula (`L<n> C<m>`), contagem de faixas/colunas, padroes de
  juncao entre caixas (`╮╭`) e largura alternativa 120. Defeitos visuais
  sutis (alinhamento de pixel, proporcao estetica) nao sao detectaveis
  automaticamente.
- A alteracao do snapshot em `tela/teste_diagnostico.py` (secao 12) e a unico
  ponto de divergencia em relacao a instrucao "nao altere os outros dois
  scripts canonicos"; justificada pela secao 4.5 do handoff.

## 9. Validacao manual humana pendente

Itens da secao 15 do handoff nao executados automaticamente (exclusivos do
usuario em TTY real):

### 9.1 Console unico

- [ ] `h0030_console_unico` carrega no demo via chip `1`.
- [ ] Console vazio renderiza com bordas visiveis; ocupa toda a altura acima
      da barra; barra na ultima linha.
- [ ] `Esc` retorna ao orquestrador sem erros.

### 9.2 Dashboard unico

- [ ] `h0030_dashboard_unico` carrega no demo via chip `2`.
- [ ] Campos `Tipo` (`dashboard único`) e `Ciclo` (`H-0030`) visiveis.
- [ ] `Esc` retorna ao orquestrador sem erros.

### 9.3 Matrizes

- [ ] `h0030_matriz_2x2` carrega via chip `3`; grid 2x2 com bordas em todas as
      intersecoes; cada celula exibe seu rotulo de posicao; sem lacunas/sobreposicoes.
- [ ] `h0030_matriz_3x2` carrega via chip `4`; grid 3x2.
- [ ] `h0030_matriz_2x4` carrega via chip `5`; grid 2x4.
- [ ] `Esc` retorna ao orquestrador em todas as matrizes.

### 9.4 Lancador do orquestrador

- [ ] Lancador exibe os 7 itens.
- [ ] Chips `1`..`5` respondem e abrem a tela correta.
- [ ] Chips `d`/`g` continuam funcionando sem regressao.
- [ ] `Esc` no orquestrador continua saindo do sistema.

## 10. Estado Git ao final

Saida de `git status --short`:

```text
 M scripts/config/telas/orquestrador.json
 M scripts/tela/teste_demo.py
 M scripts/tela/teste_diagnostico.py
 M scripts/tela/teste_loader.py
 M scripts/tela/teste_modelo.py
 M scripts/tela/teste_renderizador.py
?? scripts/config/telas/h0030_console_unico.json
?? scripts/config/telas/h0030_dashboard_unico.json
?? scripts/config/telas/h0030_matriz_2x2.json
?? scripts/config/telas/h0030_matriz_2x4.json
?? scripts/config/telas/h0030_matriz_3x2.json
?? scripts/docs/handoff/H-0030-catalogo-telas-utilizaveis.md
?? scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
?? scripts/docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md
?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md
?? scripts/tela/__pycache__/
```

Saida de `git diff --name-only` (modificacoes rastreadas):

```text
scripts/config/telas/orquestrador.json
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
```

Saida de `git diff --check`: sem mensagens de erro de whitespace.

Stage (`git diff --cached`): vazio (nenhum `git add` realizado).

### 10.1 Arquivos rastreados modificados

- `scripts/config/telas/orquestrador.json` (somente `lancador_principal.itens`)
- `scripts/tela/teste_loader.py`
- `scripts/tela/teste_modelo.py`
- `scripts/tela/teste_renderizador.py`
- `scripts/tela/teste_demo.py`
- `scripts/tela/teste_diagnostico.py` (somente snapshot `_EXPECTED_ORQUESTRADOR`)

### 10.2 Arquivos nao rastreados

- `scripts/config/telas/h0030_console_unico.json` (novo)
- `scripts/config/telas/h0030_dashboard_unico.json` (novo)
- `scripts/config/telas/h0030_matriz_2x2.json` (novo)
- `scripts/config/telas/h0030_matriz_3x2.json` (novo)
- `scripts/config/telas/h0030_matriz_2x4.json` (novo)
- `scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md` (novo)
- Os tres documentos do ciclo documental ja presentes antes da implementacao.
- `scripts/tela/__pycache__/`: cache de bytecode pre-existente (gerado pelo
  Python em tempo de importacao; nao criado deliberadamente por este ciclo).

## 11. Confirmacoes obrigatorias

- `tela/demo.py` nao foi alterado (`git diff --stat` vazio).
- `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`, `tela/diagnostico.py`
  nao foram alterados.
- Nao houve commit nem stage.
- Nenhum arquivo `h0029_*` foi alterado.
- `grupo_minimo.json`, `destino_minimo.json`, `stub_b.json` inalterados.
- Os 5 JSONs novos sao sintaticamente validos.
- Todos os `tela_destino` existem em disco.
- `orquestrador.json` contem exatamente os 2 itens preservados e os 5 novos.
- Ausencia de chips duplicados confirmada.
- Limites de rotulos (<= 15) confirmados.

## 12. Alteracao de `tela/teste_diagnostico.py` — justificativa

A instrucao operacional "nao altere os outros dois scripts canonicos" conflita
com a obrigacao de manter a suite canonica verde apos a expansao obrigatoria
do lancador (secao 9 do handoff). O `tela/teste_diagnostico.py` possui um
snapshot de igualdade estrita (`_EXPECTED_ORQUESTRADOR`, linhas 47-63) da
renderizacao do orquestrador em largura 42, contendo apenas os chips `d`/`g`.
A adicao dos 5 itens (obrigatoria) muda essa renderizacao e quebra a igualdade
estrita, fazendo o script sair com codigo 1 (27/28 antes da correcao).

A secao 4.5 do handoff H-0030 e explicita: "Nenhuma proibicao desta secao deve
tornar incompativeis: a implementacao solicitada; a suite canonica; os
criterios de aceite; os smoke tests; a demonstracao pratica." A decisao de
atualizar SOMENTE o snapshot `_EXPECTED_ORQUESTRADOR` (acrescentando as 5 linhas
`[1]..[5]` na caixa NAVEGAR) foi tomada para preservar a compatibilidade da
suite canonica exigida pelo handoff, sem alterar nenhuma logica de teste. O
usuario autorizou esta alteracao minima durante a implementacao.

Nenhuma outra linha de `tela/teste_diagnostico.py` foi modificada; a alteracao
foi estritamente proporcional (snapshot de render) e esta limitada ao escopo do
H-0030.

### 12.1 Restauracao do escopo literal apos patch (QA-IMP-H0030-BAIXO-001)

O QA da implementacao (achado `QA-IMP-H0030-BAIXO-001`) detectou que o diff
inicial de `tela/teste_diagnostico.py` incluia, alem do snapshot, um comentario
explicativo de 4 linhas antes de `_EXPECTED_ORQUESTRADOR`. Embora inerte
(sem efeito sobre logica, funcoes, casos de teste ou outros snapshots), esse
comentario excedia o escopo literal da autorizacao ("atualizar exclusivamente
o snapshot `_EXPECTED_ORQUESTRADOR`") e tornava imprecisa a afirmacao desta
secao ("Nenhuma outra linha foi modificada").

Apos o patch, o comentario foi removido. O diff final de
`tela/teste_diagnostico.py` fica agora restrito exclusivamente as 5 linhas do
snapshot `_EXPECTED_ORQUESTRADOR` (itens `[1]..[5]` na caixa NAVEGAR),
restaurando a literalidade da autorizacao e a fidelidade desta secao. A
justificativa da excecao autorizada permanece registrada aqui, em vez de
vazar para dentro do arquivo de teste.

## 13. Observacoes para QA

- Revisar a alteracao de `tela/teste_diagnostico.py` (secao 12) quanto a
  aderencia a secao 4.5 do handoff.
- Revisar a mudanca de `_ALTURA_SUBPROCESS` (24 -> 30) e do env do subprocess
  (agora fixa `COLUMNS=80/LINES=30`) em `teste_demo.py`, proporcionais ao
  lancador ampliado.
- Revisar a atualizacao de dimensoes em `teste_renderizador.py`
  (`teste_altura_explicita`, `test_json_real_orquestrador_distribui_212`,
  `TestLinhasBarra.test_altura_minima_com_barra_horizontal`) — todas
  decorrentes da NAVEGAR passar de 4 para 9 linhas.
- A validacao visual humana (secao 9) permanece pendente e deve ser executada
  pelo usuario em TTY real.

## 14. Patch de implementacao (pos-QA `I2_IMPLEMENTATION_PATCH_REQUIRED`)

Esta secao registra o patch de correcao executado apos o QA da implementacao
(`RELATORIO_QA_IMPLEMENTACAO_H-0030.md`, status
`I2_IMPLEMENTATION_PATCH_REQUIRED`). O patch corrige exclusivamente os achados
autorizados e a observacao textual listados abaixo; nao realiza QA pos-patch,
nao aprova a implementacao, nao executa validacao manual humana, nao faz stage
nem commit.

```yaml
qa_origem: RELATORIO_QA_IMPLEMENTACAO_H-0030.md
status_origem: I2_IMPLEMENTATION_PATCH_REQUIRED
achados_corrigidos:
  - QA-IMP-H0030-MEDIO-001
  - QA-IMP-H0030-BAIXO-001
  - QA-IMP-H0030-BAIXO-002
observacao_corrigida:
  - QA-IMP-H0030-OBS-001
arquivos_alterados_no_patch:
  - scripts/tela/teste_renderizador.py
  - scripts/tela/teste_diagnostico.py
  - scripts/tela/teste_demo.py
  - scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
testes_focais:
  - python tela/teste_renderizador.py
  - python tela/teste_demo.py
  - python tela/teste_diagnostico.py
suite_canonica:
  - python tela/teste_loader.py
  - python tela/teste_modelo.py
  - python tela/teste_renderizador.py
  - python tela/teste_demo.py
  - python tela/teste_diagnostico.py
  - python tela/teste_explorar_barra_de_menus.py
resultado_total_pos_patch: "1772/1772"
codigos_saida: "6/6 com codigo 0"
validacao_manual: PENDENTE
qa_pos_patch: NAO_EXECUTADO
stage: vazio
commit: inexistente
```

### 14.1 QA-IMP-H0030-MEDIO-001 — fortalecimento dos testes geometricos

Achado: a cobertura geometrica das matrizes em `tela/teste_renderizador.py`
era parcialmente indireta/tautologica — a divisoria horizontal era "provada"
apenas por `len(faixas) >= 2` e a ausencia de sobreposicao apenas por
duplicidade textual do mesmo rotulo na mesma linha; intersecoes da grade nao
eram verificadas de modo especifico.

Correcao: adicionado o metodo
`TestCatalogoH0030.test_matrizes_geometria_coordenadas`, que deriva as
propriedades estruturais diretamente das posicoes dos caracteres de borda na
saida renderizada (via helpers existentes `_linhas_corpo_renderizado` e
`_posicoes_bordas_linha`). Para cada matriz (2x2, 3x2, 2x4) e para largura 80
e altura 24 (dimensoes deterministicas do handoff), o metodo verifica por
coordenadas reais:

1. quantidade correta de faixas de linhas (topos "╭"/"┌" na coluna 0);
2. quantidade correta de colunas em cada faixa (bases "╰"/"└" + contagem de
   divisores verticais derivada dos cortes internos);
3. coordenadas das bordas externas (colunas 0 e largura-1; topo e base do
   corpo);
4. coordenadas dos cortes verticais por faixa (divisores agrupados em pares
   de colunas adjacentes);
5. coordenadas das divisorias horizontais (base da faixa superior seguida
   imediatamente pelo topo da faixa inferior);
6. alinhamento dos cortes verticais entre as faixas (conjunto de cortes
   internos identico em todas as faixas);
7. pontos de encontro entre bordas horizontais e verticais (cruzamento dos
   divisores com a linha de base da faixa superior);
8. contiguidade entre caixas adjacentes (paredes direita/esquerda
   consecutivas, sem coluna de espaco);
9. ausencia de coluna vazia inesperada entre caixas (reafirmacao da
   contiguidade, registrada em separado para rastreabilidade da cobertura);
10. ausencia de linha vazia inesperada entre faixas (base+1 == topo seguinte);
11. ausencia de sobreposicao entre retangulos de celulas distintas (areas
    internas comuns == 0; paredes compartilhadas nao contam como sobreposicao);
12. cobertura integral da regiao ocupada pela matriz (numero de retangulos
    == n_linhas*n_colunas; faixas contiguas verticalmente);
13. preservacao dos rotulos e titulos esperados (todos os rotulos de posicao
    presentes; cada um aparece exatamente uma vez);
14. largura padrao prevista (todas as linhas nao-vazias com largura 80);
15. largura alternativa `120` (ja coberto por `test_matrizes_largura_alternativa_120`:
    sem excecao, mantem regioes, todas as linhas com 120 chars).

O metodo nao aceita `len(faixas) >= 2` como prova de divisoria nem
duplicidade/unicidade de rotulo como prova de ausencia de sobreposicao. Um
teste de sensibilidade (remocao simulada de uma divisoria) confirma que as
assercoes detectam a regressao (as faixas colapsam e a contagem de
bases/topos falha). A cobertura existente foi preservada; nenhum teste foi
reduzido ou removido.

Resultado: `teste_renderizador.py` passou de 894 para 956 verificacoes
(+62), todas aprovadas, codigo de saida 0.

### 14.2 QA-IMP-H0030-BAIXO-001 — remocao de comentario excedente

Achado: o diff inicial de `tela/teste_diagnostico.py` incluia um comentario
explicativo de 4 linhas antes do snapshot `_EXPECTED_ORQUESTRADOR`, excedendo
o escopo literal da autorizacao ("atualizar exclusivamente o snapshot").

Correcao: o comentario foi removido. A justificativa da excecao autorizada foi
transferida para a secao 12.1 deste relatorio, fora do arquivo de teste. O
diff final de `tela/teste_diagnostico.py` fica restrito exclusivamente as 5
linhas do snapshot (itens `[1]..[5]` na caixa NAVEGAR). Nenhuma logica,
funcao, caso de teste, mensagem, outro snapshot ou estrutura do arquivo foi
modificada.

### 14.3 QA-IMP-H0030-BAIXO-002 — restauracao da afirmacao factual

Achado: a secao 12 afirmava que "Nenhuma outra linha de
`tela/teste_diagnostico.py` foi modificada", mas o diff real incluia o
comentario extra (BAIXO-001), tornando a afirmacao imprecisa.

Correcao: apos a remocao do comentario (14.2), a afirmacao voltou a ser
literalmente verdadeira — "Somente o snapshot `_EXPECTED_ORQUESTRADOR` foi
alterado." A secao 2.2 (linha do diagnostico) e a secao 12.1 foram
atualizadas para registrar o patch e confirmar o escopo restaurado. Este
relatorio nao foi reescrito; foram acrescentados o resultado do patch
(secao 14) e a correcao da unica afirmacao factual afetada.

### 14.4 QA-IMP-H0030-OBS-001 — mensagem textual residual

Achado: uma mensagem de teste em `tela/teste_demo.py` ainda dizia
`propaga altura=24: stdout tem 72 newlines (3 renders x 24)`, embora
`_ALTURA_SUBPROCESS` seja `30` e a execucao real produza `90` newlines. A
condicao executavel (`3 * _ALTURA_SUBPROCESS`) ja estava correta; apenas o
texto diagnostico estava obsoleto.

Correcao: a mensagem foi ajustada para `propaga altura=30: stdout tem 90
newlines (3 renders x 30)`. O comentario imediatamente acima tambem foi
atualizado para refletir `COLUMNS=80/LINES=30` fixados no env e `30` linhas
por render. A expressao executavel continua baseada em
`3 * _ALTURA_SUBPROCESS`; nenhuma logica, condicao ou fluxo do teste foi
alterado.

### 14.5 Testes executados apos o patch (suite canonica)

```yaml
- script: tela/teste_loader.py
  aprovadas: 244
  total: 244
  falhas: 0
  codigo_saida: 0
- script: tela/teste_modelo.py
  aprovadas: 148
  total: 148
  falhas: 0
  codigo_saida: 0
- script: tela/teste_renderizador.py
  aprovadas: 956
  total: 956
  falhas: 0
  codigo_saida: 0
- script: tela/teste_demo.py
  aprovadas: 358
  total: 358
  falhas: 0
  codigo_saida: 0
- script: tela/teste_diagnostico.py
  aprovadas: 28
  total: 28
  falhas: 0
  codigo_saida: 0
- script: tela/teste_explorar_barra_de_menus.py
  aprovadas: 38
  total: 38
  falhas: 0
  codigo_saida: 0
resultado_total: "1772/1772"
scripts_com_exit_zero: "6/6"
```

O total aumentou de 1710 para 1772 (+62) em funcao exclusiva do
fortalecimento da cobertura geometrica do renderizador (14.1). Nenhum teste
existente foi reduzido ou removido.

### 14.6 Estado pos-patch

- Validacao manual humana: **PENDENTE** (itens da secao 9, exclusivos do
  usuario em TTY real).
- QA pos-patch: **NAO EXECUTADO** nesta etapa.
- Stage: **vazio** (nenhum `git add` realizado).
- Commit: **inexistente** (HEAD continua `9ae4aa4`).

## 15. Segundo patch de implementacao (pos-QA pos-patch `I2_IMPLEMENTATION_PATCH_REQUIRED`)

Esta secao registra o segundo patch de correcao, executado apos o QA pos-patch
da implementacao (`RELATORIO_QA_POS_PATCH_H-0030_IMPLEMENTACAO.md`, status
`I2_IMPLEMENTATION_PATCH_REQUIRED`). O QA pos-patch classificou tres achados
como `CORRIGIDO` (`QA-IMP-H0030-BAIXO-001`, `QA-IMP-H0030-BAIXO-002`,
`QA-IMP-H0030-OBS-001`) e um como `PARCIALMENTE_CORRIGIDO`
(`QA-IMP-H0030-MEDIO-001`). Este segundo patch corrige exclusivamente a
pendencia residual do achado medio; nao reabre nem altera os itens ja
corrigidos, nao realiza QA pos-patch, nao aprova a implementacao, nao executa
validacao manual humana, nao faz stage nem commit.

```yaml
qa_origem: RELATORIO_QA_POS_PATCH_H-0030_IMPLEMENTACAO.md
status_origem: I2_IMPLEMENTATION_PATCH_REQUIRED
achado_residual:
  - QA-IMP-H0030-MEDIO-001
resultado_anterior: PARCIALMENTE_CORRIGIDO
pendencia_residual_identificada: >
  A cobertura nova (test_matrizes_geometria_coordenadas) deriva os cortes
  verticais da propria saida renderizada e verifica apenas quantidade e
  alinhamento entre faixas, sem compara-los contra coordenadas esperadas para
  a distribuicao igual. Um corte vertical deslocado de forma consistente pode
  passar. Adicionalmente, a verificacao de encontros HxV contra a linha de
  base e pouco discriminante, pois _posicoes_bordas_linha tambem considera o
  caractere horizontal `─`, de modo que uma base horizontal completa tende a
  conter qualquer coluna de corte deslocado.
correcao_aplicada: >
  Adicionado o metodo TestCatalogoH0030.test_matrizes_cortes_distribuicao_igual
  em tela/teste_renderizador.py, incluido em run_all. O metodo deriva as
  coordenadas esperadas dos cortes internos exclusivamente da largura (80) e
  do numero de colunas (passo = largura // n_colunas; corte k cai no par
  (k*passo-1, k*passo)), independente do algoritmo produtivo e da propria
  saida, e prova propriedades geométricas independentes:
    (1) os cortes internos de cada faixa caem exatamente nos pares de colunas
        esperados para distribuicao igual ((39,40) para 2 colunas;
        (19,20),(39,40),(59,60) para 4 colunas) — um corte deslocado falha;
    (2) o encontro HxV entre cada divisoria horizontal e cada corte interno
        ocorre em pares de quinas adjacentes (╮╭ no topo da faixa inferior,
        ╯╰ na base da faixa superior), nunca em traco horizontal `─` —
        tornando a prova de interseccao especifica;
    (3) regressao explicita de lacuna/coluna vazia no corte: as colunas
        imediatamente anterior e posterior a cada corte esperado devem ambas
        conter parede vertical `|` numa linha de conteudo.
assercoes_adicionadas_ou_ajustadas: >
  Novo metodo test_matrizes_cortes_distribuicao_igual com 3 propriedades
  geométricas independentes por matriz (corte deslocado, quina HxV base+topo,
  coluna vazia no corte), cobrindo 2x2, 3x2 e 2x4. Nenhuma assercao anterior
  foi alterada, dividida artificialmente nem removida. Cada nova verificacao
  corresponde a uma propriedade geométrica independente e identificavel.
propriedades_geometricas_comprovadas: >
  (a) igualdade dos cortes verticais contra coordenadas esperadas da
  distribuicao igual (sensibilidade a corte deslocado de forma consistente —
  pendencia (i) do QA pos-patch);
  (b) interseccao HxV por quinas (╮╭/╯╰) e nao por traco `─` (sensibilidade
  a base horizontal completa tornando o encontro pouco especifico — pendencia
  (ii) do QA pos-patch);
  (c) contiguidade sem coluna vazia nas duas colunas do corte (regrassao de
  lacuna entre caixas vizinhas).
arquivos_alterados:
  - scripts/tela/teste_renderizador.py
  - scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
teste_focal:
  - python tela/teste_renderizador.py
suite_canonica:
  - python tela/teste_loader.py
  - python tela/teste_modelo.py
  - python tela/teste_renderizador.py
  - python tela/teste_demo.py
  - python tela/teste_diagnostico.py
  - python tela/teste_explorar_barra_de_menus.py
resultado_total: "1796/1796"
codigos_saida: "6/6 com codigo 0"
validacao_manual: PENDENTE
qa_pos_patch: NAO_EXECUTADO
stage: vazio
commit: inexistente
```

### 15.1 Sensibilidade confirmada

A pendencia residual (i) — corte vertical deslocado de forma consistente — foi
confirmada como detectavel: simulando-se um deslocamento do corte interno de
`(39,40)` para `(38,39)` na matriz 2x2, a nova assercao de igualdade falha
(paredes `[38,40]` nao formam o par esperado `(39,40)`). A pendencia residual
(ii) — encontro HxV pouco discriminante — foi tornada especifica pela exigencia
de pares de quinas `╮╭`/`╯╰` (e nao `─`) nas colunas de corte da divisoria
horizontal, de modo que um corte deslocado para uma coluna de base preenchida
por traco horizontal nao satisfaz a assercao.

### 15.2 Resultados por script (segundo patch)

```yaml
- script: tela/teste_loader.py
  aprovadas: 244
  total: 244
  falhas: 0
  codigo_saida: 0
- script: tela/teste_modelo.py
  aprovadas: 148
  total: 148
  falhas: 0
  codigo_saida: 0
- script: tela/teste_renderizador.py
  aprovadas: 980
  total: 980
  falhas: 0
  codigo_saida: 0
- script: tela/teste_demo.py
  aprovadas: 358
  total: 358
  falhas: 0
  codigo_saida: 0
- script: tela/teste_diagnostico.py
  aprovadas: 28
  total: 28
  falhas: 0
  codigo_saida: 0
- script: tela/teste_explorar_barra_de_menus.py
  aprovadas: 38
  total: 38
  falhas: 0
  codigo_saida: 0
resultado_total: "1796/1796"
scripts_com_exit_zero: "6/6"
```

O total subiu de 1772 para 1796 (+24) em funcao exclusiva do novo metodo
`test_matrizes_cortes_distribuicao_igual` (3 propriedades x 3 matrizes, com
subverificacoes por faixa e por corte). Nenhum teste existente foi reduzido,
dividido artificialmente nem removido.

### 15.3 Preservacoes do segundo patch

- Nenhum arquivo produtivo foi alterado (`tela/renderizador.py` sem diff).
- Os arquivos ja corrigidos no patch anterior nao receberam novas alteracoes:
  `tela/teste_diagnostico.py`, `tela/teste_demo.py`,
  `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0030.md`,
  `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_IMPLEMENTACAO.md` sem diff
  novo.
- Os JSONs `config/telas/*.json` sem diff novo.
- Nenhum stage, nenhum commit (HEAD continua `9ae4aa4`).

### 15.4 Estado pos-segundo-patch

- Validacao manual humana: **PENDENTE** (itens da secao 9, exclusivos do
  usuario em TTY real).
- QA pos-patch: **NAO EXECUTADO** nesta etapa.
- Stage: **vazio** (nenhum `git add` realizado).
- Commit: **inexistente** (HEAD continua `9ae4aa4`).
