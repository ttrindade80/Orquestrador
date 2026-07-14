---
name: QA-POS-PATCH-H0030-catalogo-telas-utilizaveis
description: Auditoria independente pos-patch do handoff H-0030 — Catalogo de telas utilizaveis
metadata:
  type: relatorio_qa_pos_patch
  data: 2026-07-13
  handoff_auditado: docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  relatorio_anterior: docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md
---

# QA pos-patch H-0030 — Catalogo de telas utilizaveis

## 1. Identificacao

Auditoria independente do handoff `docs/handoff/H-0030-catalogo-telas-utilizaveis.md` apos patch documental.

Esta etapa executou exclusivamente `QA_HANDOFF`. Nenhum JSON, codigo, teste, contrato, ADR, indice, relatorio anterior ou handoff foi corrigido. A unica saida criada nesta etapa e este relatorio.

## 2. Artefatos auditados

Artefatos lidos integralmente:

- `docs/handoff/H-0030-catalogo-telas-utilizaveis.md`
- `docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md`

Artefatos consultados para confirmacao proporcional:

- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_json_lancador.md`
- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- `config/telas/orquestrador.json`
- `config/telas/destino_minimo.json`
- `config/telas/grupo_minimo.json`
- `config/telas/h0029_*.json`
- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_diagnostico.py`
- `tela/teste_explorar_barra_de_menus.py`

## 3. Estado Git

Base de caminhos registrada: raiz Git `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`, com caminhos iniciados por `scripts/`.

```yaml
head: "9ae4aa4 fix: corrige distribuicao com cardinalidade unitaria"
status_antes_do_relatorio:
  - "?? scripts/docs/handoff/H-0030-catalogo-telas-utilizaveis.md"
  - "?? scripts/docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md"
diff_name_only: []
diff_cached_name_only: []
stage: vazio
arquivos_rastreados_modificados: []
arquivos_nao_rastreados_esperados_antes:
  - scripts/docs/handoff/H-0030-catalogo-telas-utilizaveis.md
  - scripts/docs/relatorios/RELATORIO_QA_H-0030_HANDOFF.md
arquivo_nao_rastreado_adicionado_por_esta_auditoria:
  - scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0030_HANDOFF.md
arquivos_inesperados: []
whitespace_handoff:
  comando: "git diff --no-index --check -- /dev/null scripts/docs/handoff/H-0030-catalogo-telas-utilizaveis.md"
  resultado: "sem mensagens de whitespace; codigo 1 esperado por comparacao no-index com arquivo novo"
```

O relatorio pos-patch nao existia antes desta auditoria.

## 4. Tabela dos seis achados anteriores

| Achado original | Resultado | Evidencia | Pendencia |
| --------------- | --------- | --------- | --------- |
| QA-H0030-BLOQ-001 | CORRIGIDO | `tela/teste_demo.py` aparece em `escopo_alteravel`, arquivos a modificar, escopo autorizado, criterios 14.6 e lista nominal acumulavel. | Nenhuma. |
| QA-H0030-ALTO-001 | CORRIGIDO | Secao 14.6 exige ciclo real por chips `1` a `5`, tela correta, Esc e retorno ao orquestrador; tambem preserva `d`, `g` e Esc na raiz. | Nenhuma. |
| QA-H0030-MEDIO-001 | CORRIGIDO | Secao 14.3-G adiciona verificacoes geometricas para 2x2, 3x2 e 2x4, cobertura, rotulos, divisorias, ausencia de lacuna/sobreposicao e largura 120. | Nenhuma. |
| QA-H0030-MEDIO-002 | CORRIGIDO | Condicao `BLOCKED_ID_CONFLICT` exclui o proprio handoff, relatorios do ciclo H-0030 e fixtures `h0030_*`. | Nenhuma. |
| QA-H0030-BAIXO-001 | CORRIGIDO | Marcadores `barra_de_menus` sao declarados esquematicos, nao copiaveis, e exigem materializacao integral da estrutura da secao 6.1. | Nenhuma. |
| QA-H0030-BAIXO-002 | CORRIGIDO | Secao 16 exige campos factuais separados para arquivos, ids, nomes, rotulos, chips, destinos, ordem, demonstracao, smoke tests, fixtures, testes, resultados, total, limitacoes, ressalvas, validacao manual pendente, Git, nao rastreados e preservacoes. | Nenhuma. |

## 5. Evidencia da correcao de cada achado

### QA-H0030-BLOQ-001 — `tela/teste_demo.py`

Resultado: `CORRIGIDO`.

Evidencias:

- `tela/teste_demo.py` esta em `escopo_alteravel` nas linhas 22-33.
- O arquivo esta em `Arquivos a modificar`, com referencia explicita ao escopo da secao 4.4.
- A secao 4.4 autoriza snapshots, expectativas de chips, fluxos de subprocesso, smoke tests dos cinco chips novos, preservacao de `d` e `g`, retorno por Esc nas telas de destino e saida por Esc na raiz.
- A autorizacao e proporcional: a linha 196 proibe refatoracao geral.
- A lista de proibidos nao inclui `tela/teste_demo.py`; inclui `tela/demo.py`, `tela/teste_diagnostico.py` e `tela/teste_explorar_barra_de_menus.py`.
- A lista nominal acumulavel inclui `tela/teste_demo.py`.

Nao foi encontrada ocorrencia normativa que proiba alterar `tela/teste_demo.py`, limite a cobertura a loader/modelo/renderizador, impossibilite atualizar snapshots ou exija preservar expectativas literais incompatíveis com os cinco novos itens.

### QA-H0030-ALTO-001 — fluxo real do `demo.py`

Resultado: `CORRIGIDO`.

Evidencias:

- A secao 10.1 recomenda navegacao pelo lancador via `python3 tela/demo.py`.
- A secao 14.6 exige smoke tests em `tela/teste_demo.py` para os ciclos:
  - `1 -> h0030_console_unico`
  - `2 -> h0030_dashboard_unico`
  - `3 -> h0030_matriz_2x2`
  - `4 -> h0030_matriz_3x2`
  - `5 -> h0030_matriz_2x4`
- Cada ciclo deve comprovar `orquestrador -> chip -> tela correta -> Esc -> retorno ao orquestrador`.
- A mesma secao exige preservacao de `d -> destino_minimo`, `g -> grupo_minimo`, destino incorreto nao aberto, Esc na raiz e codigo esperado por ciclo.
- A linha 937 impede que monkeypatch substitua o caminho real pelo lancador.

O `demo.py` vigente percorre declarativamente `itens[]` do lancador para decidir `tela_destino`; portanto a demonstracao real e implementavel sem hardcode no codigo.

### QA-H0030-MEDIO-001 — testes geometricos

Resultado: `CORRIGIDO`.

Evidencias:

- A secao 14.3-G exige verificacoes para as tres matrizes.
- Os criterios cobrem dimensoes 2x2, 3x2 e 2x4; quantidade de linhas e colunas; cobertura integral; rotulos de posicao; divisorias verticais e horizontais; ausencia de lacunas e duplicidade; ausencia de sobreposicoes; largura alternativa deterministica `largura=120`.
- A secao 14.3-G declara que a cobertura automatizada nao substitui validacao visual humana.
- ADR-0020 D5 permite matrizes de 2 a 4 por eixo; D6 exige distribuicao por eixo; D7-D8 exigem grade comum e coordenadas explicitas; D13 proibe `arranjo` em `estrutura: "matriz"`. As especificacoes do handoff obedecem a essas regras.

Os criterios sao executaveis com as capacidades atuais de carregamento, modelo e renderizacao, acrescentando testes proporcionais em `tela/teste_renderizador.py`, sem exigir algoritmo novo de matriz.

### QA-H0030-MEDIO-002 — conflito de identificador

Resultado: `CORRIGIDO`.

Evidencia: a secao 13 define `BLOCKED_ID_CONFLICT` somente para "outro handoff ou outro artefato ativo" com identificador concorrente, excluindo expressamente o proprio handoff, os relatorios do ciclo H-0030 e as fixtures `h0030_*`.

Busca local proporcional encontrou apenas o handoff auditado em `docs/handoff/*0030*`, alem de relatorios do ciclo e referencias historicas `DOC-0030` fora do escopo do identificador `H-0030`.

### QA-H0030-BAIXO-001 — placeholders

Resultado: `CORRIGIDO`.

Evidencias:

- Os marcadores de `barra_de_menus` nas secoes 7.1, 8.2, 8.3 e 8.4 dizem `ESQUEMATICO`.
- A nota apos cada bloco declara que o marcador nao e JSON copiavel.
- O executor deve materializar integralmente a estrutura normativa da secao 6.1.
- A secao 7.2 exige que a barra seja identica a especificada na secao 6.1; as notas das matrizes repetem que a semantica nao e alterada.

Nao ha placeholder restante que seja apresentado como JSON final valido. O uso de bloco `json` com marcador esquematico nao e defeito residual, porque a nota normativa imediatamente adjacente impede copia como configuracao final.

### QA-H0030-BAIXO-002 — relatorio de implementacao

Resultado: `CORRIGIDO`.

Evidencias:

- A secao 16 exige relatorio factual e veda autoaprovacao formal.
- Os campos separados cobrem arquivos criados, arquivos modificados, identificadores, nomes de arquivos, rotulos, chips, destinos, ordem final do lancador, demonstracao, smoke tests, fixtures, testes, resultados por script, total de verificacoes, limitacoes, ressalvas, validacao manual pendente, estado Git, arquivos nao rastreados, preservacao de `d` e `g`, preservacao das sete telas `h0029_*` e demais preservacoes do ciclo.

## 6. Busca de residuos

| Ocorrencia buscada | Classificacao | Evidencia |
|---|---|---|
| `teste_demo.py` | normativa correta | Permitido em 4.2/4.4/14.6/17.1; tambem listado como fixture/teste ativo em 17.2. |
| `demo.py` | normativa correta | Mantido somente leitura/proibido para alteracao; usado como ponto de entrada real e alvo de smoke tests. |
| `arquivos proibidos` | normativa correta | Secao 4.3 e preservacoes da secao 12 nao contradizem `tela/teste_demo.py`. |
| `não alterar` | normativa correta | Aplica-se a itens preexistentes `d`/`g` e arquivos preservados, nao aos arquivos permitidos. |
| `proibido` | normativa correta | Proibe campos/arquivos fora de escopo e `arranjo` em matriz conforme contrato/ADR. |
| `somente` | normativa correta | Usado para leitura obrigatoria, escopo restrito e demonstracoes, sem restringir indevidamente a implementacao. |
| `monkeypatch` | normativa correta | Permitido como complementar; explicitamente nao substitui caminho real. |
| `snapshots` | normativa correta | Atualizacao autorizada em `tela/teste_demo.py` de forma proporcional. |
| `chips` | normativa correta | Chips novos e preservados especificados; sem conflito com `d`/`g`. |
| `Esc` | normativa correta | Exige retorno das telas internas e saida vigente na raiz. |
| `BLOCKED_ID_CONFLICT` | normativa correta | Exclui proprio handoff, relatorios do ciclo e fixtures. |
| `barra_de_menus` | normativa correta | Secao 6.1 e marcadores esquematicos exigem materializacao integral. |
| `relatorio de implementacao` | normativa correta | Secao 16 ampliada e factual. |
| `lista nominal` | normativa correta | Secao 17 lista arquivos do ciclo e ativos preservados. |

Declaracao do patch confirmada: as ocorrencias sao esperadas ou normativas corretas. Nenhum residuo contraditorio foi identificado.

## 7. Auditoria completa do handoff

### Capacidade

Conforme:

- cinco telas permanentes especificadas por `id` e arquivo;
- console unico especificado com envelope minimo de console;
- dashboard unico especificado com campos literais, compativel com exemplos permanentes atuais;
- matrizes 2x2, 3x2 e 2x4 dentro do intervalo permitido por ADR-0020;
- integracao dos cinco destinos no lancador;
- demonstracao real pelo lancador e demonstracoes complementares por monkeypatch/renderizacao estatica;
- fixtures permanentes declaradas;
- validacao manual futura enumerada.

### Escopo negativo

Conforme. Permanecem fora:

- navegacao interna do console;
- selecao;
- acoes simuladas;
- conteudo por JSON de testes;
- auditoria H-0025/H-0026;
- compatibilizacao com `pytest`;
- nova ADR;
- algoritmo novo de matriz;
- refatoracao geral.

### Arquivos permitidos

Conforme. A lista nominal inclui:

- `config/telas/h0030_console_unico.json`
- `config/telas/h0030_dashboard_unico.json`
- `config/telas/h0030_matriz_2x2.json`
- `config/telas/h0030_matriz_3x2.json`
- `config/telas/h0030_matriz_2x4.json`
- `config/telas/orquestrador.json`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md`

`tela/demo.py` nao esta autorizado para alteracao; deve ser executado e preservado. Isso e coerente com o contrato do lancador, pois o `demo.py` atual navega por itens declarados.

### Lancador

Conforme:

- estado atual de `config/telas/orquestrador.json`: dois itens, `d -> destino_minimo` e `g -> grupo_minimo`;
- handoff exige preservar `d` e `g`;
- chips `1` a `5` apontam para as cinco novas telas;
- total final esperado: sete itens;
- rotulos respeitam limite contratual de 15 caracteres;
- destinos devem existir apos implementacao;
- ausencia de hardcode mantida, pois a alteracao e declarativa no JSON;
- ordem final explicita.

### Suite canonica

Conforme. O handoff exige execucao direta dos seis scripts, codigo de saida 0 em todos e relatorio por script. Os seis scripts canônicos permanecem identificaveis no escopo do ciclo:

- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`
- `tela/teste_explorar_barra_de_menus.py`

Nao foi aceita apenas meta numerica: tambem foram confirmados escopo, preservacoes e exigencia de resultado por script.

### Validacao manual

Conforme. A secao 15 declara validacao futura, humana, apos aprovacao automatizada, e enumera console, dashboard, matrizes e lancador. O handoff nao declara homologacao visual concluida.

## 8. Novos achados

Nenhum novo achado corretivo foi identificado.

```yaml
novos_achados_bloqueantes: 0
novos_achados_altos: 0
novos_achados_medios: 0
novos_achados_baixos: 0
observacoes_novas: 0
```

## 9. Itens conformes

- Handoff e relatorio anterior puderam ser lidos integralmente.
- O patch corrige os seis achados formais anteriores.
- Nao ha residuo normativo que proiba `tela/teste_demo.py`.
- `tela/demo.py` permanece preservado e ainda exercitavel como ponto de entrada real.
- O estado atual do lancador possui somente `d` e `g`; chips `1` a `5` estao livres.
- Nao existem fixtures `config/telas/h0030_*.json` antes da implementacao.
- As sete fixtures `h0029_*` existem e permanecem fora de alteracao.
- Os criterios automatizados e manuais sao suficientes para a implementacao avancar sem nova decisao documental.

## 10. Conclusao

O handoff pos-patch esta completo, coerente e implementavel. Os seis achados anteriores foram corrigidos, nao ha resíduo contraditorio, nao ha novo defeito corretivo e nao falta decisao documental para a proxima etapa substantiva.

## 11. Status literal e normalizado

```yaml
status_literal: H1_HANDOFF_APPROVED
status_normalizado: APPROVED
```

## 12. Proxima categoria

```yaml
proxima_categoria: IMPLEMENTAR_HANDOFF
```
