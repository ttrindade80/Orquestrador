---
name: QA-IMPLEMENTACAO-H0030-catalogo-telas-utilizaveis
description: Auditoria independente da implementacao do H-0030 — catalogo de telas utilizaveis
metadata:
  type: relatorio_qa_implementacao
  data: 2026-07-13
  handoff_auditado: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  relatorio_implementacao: docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
---

# QA implementacao H-0030 — Catalogo de telas utilizaveis

## 1. Identificacao

Auditoria independente da implementacao do H-0030, executando exclusivamente `QA_IMPLEMENTACAO`.

Este relatorio foi criado como unico artefato desta etapa:

```text
docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0030.md
```

Nao foram corrigidos arquivos, codigo, JSONs, testes, handoff, contratos, ADRs, indices ou relatorios anteriores. Nao houve stage, commit ou validacao manual humana.

## 2. Artefatos auditados

Lidos integralmente:

- `docs/handoff/H-0030-catalogo-telas-utilizaveis.md`
- `docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md`
- `docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md`

Lidos diretamente:

- `config/telas/h0030_console_unico.json`
- `config/telas/h0030_dashboard_unico.json`
- `config/telas/h0030_matriz_2x2.json`
- `config/telas/h0030_matriz_3x2.json`
- `config/telas/h0030_matriz_2x4.json`
- `config/telas/orquestrador.json`
- trechos alterados de `tela/teste_loader.py`
- trechos alterados de `tela/teste_modelo.py`
- trechos alterados de `tela/teste_renderizador.py`
- trechos alterados de `tela/teste_demo.py`
- diff e trecho final de `tela/teste_diagnostico.py`

## 3. Autoridades

Autoridades obrigatorias:

- `docs/handoff/H-0030-catalogo-telas-utilizaveis.md`
- `docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md`
- `docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md`

Autoridades consultadas proporcionalmente:

- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- artefatos H-0028/H-0029 necessarios para preservacoes.

## 4. Estado Git

Base de caminhos usada para Git: raiz Git `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`, com caminhos iniciados por `scripts/`.

```yaml
ultimo_commit: "9ae4aa4 fix: corrige distribuicao com cardinalidade unitaria"
stage: vazio
git_diff_check: sem_mensagens
arquivos_rastreados_modificados:
  - scripts/config/telas/orquestrador.json
  - scripts/tela/teste_demo.py
  - scripts/tela/teste_diagnostico.py
  - scripts/tela/teste_loader.py
  - scripts/tela/teste_modelo.py
  - scripts/tela/teste_renderizador.py
arquivos_nao_rastreados:
  - scripts/config/telas/h0030_console_unico.json
  - scripts/config/telas/h0030_dashboard_unico.json
  - scripts/config/telas/h0030_matriz_2x2.json
  - scripts/config/telas/h0030_matriz_2x4.json
  - scripts/config/telas/h0030_matriz_3x2.json
  - scripts/docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  - scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
  - scripts/docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md
  - scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0030.md
  - scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md
  - scripts/tela/__pycache__/
arquivos_em_stage: []
caches_e_temporarios:
  - scripts/tela/__pycache__/
arquivos_inesperados:
  - scripts/tela/__pycache__/
commit_h0030: inexistente
```

O arquivo deste relatorio nao existia antes da auditoria.

## 5. Lista real de arquivos do ciclo

Arquivos criados confirmados:

- `scripts/config/telas/h0030_console_unico.json`
- `scripts/config/telas/h0030_dashboard_unico.json`
- `scripts/config/telas/h0030_matriz_2x2.json`
- `scripts/config/telas/h0030_matriz_3x2.json`
- `scripts/config/telas/h0030_matriz_2x4.json`
- `scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md`

Arquivos modificados confirmados:

- `scripts/config/telas/orquestrador.json`
- `scripts/tela/teste_loader.py`
- `scripts/tela/teste_modelo.py`
- `scripts/tela/teste_renderizador.py`
- `scripts/tela/teste_demo.py`
- `scripts/tela/teste_diagnostico.py`

Documentacao do ciclo presente como nao rastreada:

- `scripts/docs/handoff/H-0030-catalogo-telas-utilizaveis.md`
- `scripts/docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md`
- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md`

Arquivo criado por esta auditoria:

- `scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0030.md`

## 6. Analise dos cinco JSONs

Os cinco JSONs sao sintaticamente validos (`python -m json.tool` com codigo 0), possuem `schema: tela.v1`, `id` correspondente ao arquivo, `cabecalho`, `corpo`, `barra_de_menus` integralmente materializada, conteudo deterministico, ausencia de placeholders documentais e uso de capacidades ja existentes.

### Console unico

```yaml
arquivo: config/telas/h0030_console_unico.json
id: h0030_console_unico
elementos_corpo: 1
tipo: console
origem_dados: null
itens: []
politica_navegacao.navegavel: false
politica_selecao: nenhuma
politica_paginacao: sem
resultado: conforme
```

Nao ha navegacao interna, selecao, acoes simuladas ou fonte externa de dados ainda nao implementada.

### Dashboard unico

```yaml
arquivo: config/telas/h0030_dashboard_unico.json
id: h0030_dashboard_unico
elementos_corpo: 1
tipo: dashboard
campos_literais:
  - tipo_corpo: "dashboard único"
  - ciclo: "H-0030"
resultado: conforme
```

Nao foi introduzida regra nova de composicao ou dimensionamento.

### Matrizes

```yaml
h0030_matriz_2x2:
  dimensoes: "2x2"
  celulas: 4
  coordenadas: completas
  filhos: [l1c1, l1c2, l2c1, l2c2]
  arranjo_no_grupo_matriz: ausente
  distribuicao_linhas: {modo: igual}
  distribuicao_colunas: {modo: igual}
h0030_matriz_3x2:
  dimensoes: "3x2"
  celulas: 6
  coordenadas: completas
  filhos: [l1c1, l1c2, l2c1, l2c2, l3c1, l3c2]
  arranjo_no_grupo_matriz: ausente
  distribuicao_linhas: {modo: igual}
  distribuicao_colunas: {modo: igual}
h0030_matriz_2x4:
  dimensoes: "2x4"
  celulas: 8
  coordenadas: completas
  filhos: [l1c1, l1c2, l1c3, l1c4, l2c1, l2c2, l2c3, l2c4]
  arranjo_no_grupo_matriz: ausente
  distribuicao_linhas: {modo: igual}
  distribuicao_colunas: {modo: igual}
resultado: conforme
```

As matrizes aderem a ADR-0020 quanto a dimensoes permitidas, distribuicao obrigatoria por eixo, coordenadas explicitas, grade integral e proibicao de `arranjo` dentro do grupo com `estrutura: "matriz"`.

## 7. Analise do lancador

O diff de `scripts/config/telas/orquestrador.json` altera somente `lancador_principal.itens`, acrescentando cinco objetos apos os dois itens pre-existentes. Nao foi identificado hardcode novo em codigo Python para resolver os destinos.

Ordem final completa:

```yaml
- chip: d
  id: item_destino_minimo
  rotulo: Destino
  tela_destino: destino_minimo
- chip: g
  id: item_grupo_minimo
  rotulo: Grupo Min.
  tela_destino: grupo_minimo
- chip: "1"
  id: item_console_unico
  rotulo: Console
  tela_destino: h0030_console_unico
- chip: "2"
  id: item_dashboard_unico
  rotulo: Dashboard
  tela_destino: h0030_dashboard_unico
- chip: "3"
  id: item_matriz_2x2
  rotulo: Matriz 2x2
  tela_destino: h0030_matriz_2x2
- chip: "4"
  id: item_matriz_3x2
  rotulo: Matriz 3x2
  tela_destino: h0030_matriz_3x2
- chip: "5"
  id: item_matriz_2x4
  rotulo: Matriz 2x4
  tela_destino: h0030_matriz_2x4
```

Confirmacoes:

- `d` e `g` preservados.
- chips `1` a `5` incluidos.
- exatamente sete itens.
- sem chips duplicados.
- todos os rotulos respeitam limite de 15 caracteres.
- todos os `tela_destino` existem.
- ordem corresponde ao handoff.

## 8. Analise dos testes

### Loader

`tela/teste_loader.py` cobre carregamento das cinco telas, identificadores, `schema`, estruturas obrigatorias, destinos via lancador, preservacao de telas existentes e alguns erros ja existentes. Resultado: conforme.

### Modelo

`tela/teste_modelo.py` cobre console unico, dashboard unico, dimensoes 2x2/3x2/2x4, coordenadas, grade integral, identificadores e validacoes existentes. Resultado: conforme.

### Renderizador

`tela/teste_renderizador.py` cobre renderizacao das cinco telas, conteudo deterministico de console/dashboard, rotulos das matrizes, titulos das celulas, quantidade de faixas, largura 80 e largura 120.

Ha defeito de cobertura: parte das assercoes declaradas como geometricas e de ausencia de lacuna/sobreposicao e apenas indireta ou tautologica. O teste de divisoria horizontal aceita `len(inicioss) >= 2` como prova de divisoria, e o teste de sobreposicao verifica duplicidade textual do mesmo rotulo na mesma linha, nao coordenadas de regioes. Ver achado `QA-IMP-H0030-MEDIO-001`.

### Demonstracao

`tela/teste_demo.py` cobre fluxos reais por subprocess:

```text
1 -> h0030_console_unico
2 -> h0030_dashboard_unico
3 -> h0030_matriz_2x2
4 -> h0030_matriz_3x2
5 -> h0030_matriz_2x4
```

Para cada fluxo, o teste executa:

```text
orquestrador -> chip -> tela correta -> Esc -> orquestrador -> Esc -> saida
```

Tambem cobre `d -> destino_minimo`, `g -> grupo_minimo`, Esc na raiz, chip invalido, identidade da tela aberta, codigo de saida e ausencia de dependencia exclusiva de monkeypatch. Resultado funcional: conforme.

Observacao: ha uma mensagem residual em `tela/teste_demo.py` que ainda diz `altura=24`/`72 newlines`, embora a execucao real esteja em altura 30/90. Ver observacao `QA-IMP-H0030-OBS-001`.

### Diagnostico

O snapshot `_EXPECTED_ORQUESTRADOR` foi atualizado com os cinco novos itens e corresponde ao orquestrador real com sete itens.

A autorizacao operacional do usuario para `tela/teste_diagnostico.py` fica registrada como fato comprovado:

```yaml
arquivo: tela/teste_diagnostico.py
autorizacao: CONFIRMADA_PELO_USUARIO
tipo: EXCECAO_OPERACIONAL_AUTORIZADA
escopo:
  - atualizar exclusivamente o snapshot _EXPECTED_ORQUESTRADOR
motivo:
  - refletir a expansao obrigatoria do lancador de dois para sete itens
nova_arquitetura: nao
nova_semantica: nao
patch_retroativo_do_handoff: nao_exigido
```

Contudo, o diff tambem adicionou um comentario nas linhas 47-50 fora do valor atribuido a `_EXPECTED_ORQUESTRADOR`. Isso excede o escopo literal "atualizar exclusivamente o snapshot", sem alterar logica, funcoes, casos de teste ou outro snapshot. Ver achado `QA-IMP-H0030-BAIXO-001`.

## 9. Resultados independentes da suite

Execucao a partir de `scripts/`, sem usar `pytest`:

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
  aprovadas: 894
  total: 894
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
resultado_total: "1710/1710"
scripts_com_exit_zero: "6/6"
```

Os resultados declarados pela implementacao foram reproduzidos independentemente.

## 10. Analise da excecao autorizada em `tela/teste_diagnostico.py`

Conforme quanto ao conteudo do snapshot:

- a diferenca textual do snapshot corresponde aos cinco novos itens `[1]` a `[5]`;
- ordem, rotulos e chips correspondem ao JSON real;
- nenhuma funcao, caso de teste ou outro snapshot foi alterado;
- o teste nao foi enfraquecido e continua com igualdade estrita;
- a atualizacao nao mascara regressao funcional do diagnostico.

Nao conforme em escopo estrito:

- linhas 47-50 adicionam comentario fora do snapshot;
- o relatorio IMP afirma que nenhuma outra linha de `tela/teste_diagnostico.py` foi modificada, o que contradiz o diff real.

Classificacao: excesso real baixo, limitado a comentario e fidelidade documental; nao e desvio de arquitetura nem bloqueio documental.

## 11. Preservacoes

Confirmado por `git diff --name-only` especifico e por conteudo/testes quando necessario:

- sete telas `h0029_*` inalteradas;
- `grupo_minimo.json` inalterado;
- `destino_minimo.json` inalterado;
- `stub_b.json` inalterado;
- `tela/demo.py` inalterado;
- `tela/loader.py` inalterado;
- `tela/modelo.py` inalterado;
- `tela/renderizador.py` inalterado;
- `tela/diagnostico.py` inalterado;
- `tela/teste_explorar_barra_de_menus.py` inalterado;
- contratos, ADRs e indices inalterados;
- ausencia de stage;
- ausencia de commit.

## 12. Fidelidade do relatorio IMP

O IMP registra corretamente:

- arquivos criados;
- arquivos modificados;
- identificadores, nomes, rotulos, chips e destinos;
- ordem do lancador;
- demonstracao e smoke tests;
- fixtures;
- testes e resultados;
- total agregado e codigos de saida;
- limitacoes e ressalvas;
- validacao manual pendente;
- estado Git, arquivos nao rastreados e ausencia de commit;
- preservacoes;
- excecao autorizada de `tela/teste_diagnostico.py` como decisao explicita do usuario.

Inconsistencia encontrada:

- o IMP declara que `tela/teste_diagnostico.py` teve somente o snapshot alterado e que nenhuma outra linha foi modificada, mas o diff inclui comentario novo fora do snapshot. Ver `QA-IMP-H0030-BAIXO-002`.

## 13. Achados

```yaml
- id: QA-IMP-H0030-MEDIO-001
  severidade: médio
  arquivo: scripts/tela/teste_renderizador.py
  trecho_ou_diff: "linhas 6585-6633"
  autoridade: "H-0030 secao 14.3-G; prompt QA_IMPLEMENTACAO: verificar linhas, colunas, cobertura integral, divisorias verticais/horizontais, intersecoes, ausencia de lacunas e sobreposicoes; testes nao tautologicos"
  problema: >
    A cobertura geometrica das matrizes e parcialmente indireta/tautologica.
    A divisoria horizontal e considerada provada por `len(inicioss) >= 2`,
    isto e, pela existencia de mais de uma faixa, sem inspecionar linha de
    borda, coordenadas de corte ou intersecoes. A ausencia de sobreposicao
    verifica apenas duplicidade textual do mesmo rotulo na mesma linha, nao
    regioes, cortes, largura ocupada ou colisoes entre celulas distintas.
    Intersecoes da grade nao sao verificadas de modo especifico.
  impacto: >
    Uma regressao de renderizacao com divisorias horizontais/intersecoes
    incorretas, lacunas visuais ou sobreposicao entre regioes pode passar
    pelos testes H-0030 desde que os titulos e rotulos continuem aparecendo.
  correcao_necessaria: >
    Fortalecer `tela/teste_renderizador.py` com assercoes sobre coordenadas
    reais das bordas, linhas horizontais, cortes verticais por faixa, pontos
    de encontro entre linhas e colunas, contiguidade sem espacos externos e
    nao sobreposicao de caixas/regioes.

- id: QA-IMP-H0030-BAIXO-001
  severidade: baixo
  arquivo: scripts/tela/teste_diagnostico.py
  trecho_ou_diff: "linhas 47-50; diff adiciona comentario antes de _EXPECTED_ORQUESTRADOR"
  autoridade: "excecao operacional autorizada pelo usuario: atualizar exclusivamente o snapshot _EXPECTED_ORQUESTRADOR"
  problema: >
    A alteracao autorizada em `tela/teste_diagnostico.py` deveria ficar
    exclusivamente no snapshot `_EXPECTED_ORQUESTRADOR`, mas o diff tambem
    adiciona comentario fora do snapshot. O comentario nao altera execucao,
    logica, caso de teste nem outro snapshot.
  impacto: >
    Excesso pequeno de escopo em arquivo cuja excecao era deliberadamente
    restrita; nao causa regressao funcional, mas quebra a literalidade da
    autorizacao.
  correcao_necessaria: >
    Remover o comentario ou registrar a justificativa somente no relatorio
    de implementacao, mantendo `tela/teste_diagnostico.py` limitado ao snapshot.

- id: QA-IMP-H0030-BAIXO-002
  severidade: baixo
  arquivo: scripts/docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
  trecho_ou_diff: "secao 12; declaracao 'Nenhuma outra linha de tela/teste_diagnostico.py foi modificada'"
  autoridade: "prompt QA_IMPLEMENTACAO: comparar IMP com arquivos, diff e testes reais"
  problema: >
    O IMP afirma que somente o snapshot foi alterado e que nenhuma outra linha
    de `tela/teste_diagnostico.py` foi modificada, mas o diff real inclui
    comentario novo nas linhas 47-50.
  impacto: >
    O relatorio de implementacao fica impreciso justamente no ponto da excecao
    operacional autorizada.
  correcao_necessaria: >
    Atualizar o IMP para refletir o diff real ou ajustar o arquivo para que a
    declaracao volte a ser verdadeira.

- id: QA-IMP-H0030-OBS-001
  severidade: observação
  arquivo: scripts/tela/teste_demo.py
  trecho_ou_diff: "linha 1134"
  autoridade: "prompt QA_IMPLEMENTACAO: registrar evidencia fiel dos testes"
  problema: >
    Uma mensagem de teste ainda diz `propaga altura=24: stdout tem 72 newlines`,
    embora `_ALTURA_SUBPROCESS` seja 30 e a execucao independente tenha contado
    90 newlines. A condicao usa `3 * _ALTURA_SUBPROCESS`, portanto o teste
    passa corretamente; apenas o texto diagnostico esta obsoleto.
  impacto: >
    Pode confundir leitura humana do log, mas nao altera a verificacao executada.
  correcao_necessaria: >
    Ajustar a mensagem para `altura=30` e `90 newlines` em ciclo de patch local.
```

## 14. Validacao manual

A validacao humana permanece pendente.

O handoff possui criterios enumerados para TTY real na secao 15, cobrindo console unico, dashboard unico, matrizes e lancador do orquestrador.

Esta auditoria nao executou nem simulou aprovacao visual humana.

Como ha achados tecnicos/documentais locais, nao resta exclusivamente validacao humana; portanto o status final nao e `I5_MANUAL_VALIDATION_REQUIRED`.

## 15. Conclusao

A implementacao criou as cinco telas, integrou os sete itens do lancador, preservou os destinos existentes, manteve os artefatos proibidos principais inalterados e reproduziu a suite canonica declarada com `1710/1710` verificacoes e `6/6` scripts com codigo 0.

Entretanto, ha patch local necessario: a cobertura geometrica do renderizador nao prova integralmente todos os criterios exigidos para matrizes; a excecao de `tela/teste_diagnostico.py` excedeu estritamente o snapshot por comentario; e o IMP ficou impreciso nesse ponto.

## 16. Status literal

```text
I2_IMPLEMENTATION_PATCH_REQUIRED
```

## 17. Status normalizado

```text
PATCH_REQUIRED
```

## 18. Proxima categoria

```text
CORRIGIR_IMPLEMENTACAO
```
