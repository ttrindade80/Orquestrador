---
name: LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR
description: Levantamento neutro para preparar decisao futura de integracao entre Orquestrador e Pipeline
metadata:
  type: relatorio_levantamento
  etapa: LEVANTAMENTO
  status: CONCLUIDO
  data: 2026-07-14
---

# LEVANTAMENTO - Preparacao de integracao Pipeline/Orquestrador

## 1. Objetivo e limites

Objetivo: inspecionar o estado real do repositorio do Orquestrador, localizar autoridades e dependencias, e registrar riscos/decisoes pendentes antes de qualquer ciclo substantivo de preparacao para integracao futura com o Pipeline.

Limites desta etapa:

- nao implementa migracao;
- nao move, renomeia ou remove arquivos;
- nao cria ADR;
- nao cria handoff;
- nao executa QA;
- nao faz commit;
- cria somente este arquivo de levantamento.

Classificacao desta etapa: `LEVANTAMENTO`.

## 2. Raiz e estado Git observados

Comandos executados a partir da raiz operacional:

```bash
$ git rev-parse --show-toplevel
/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador

$ pwd
/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador

$ git status --short
# saida vazia
```

Evidencias complementares:

```bash
$ git branch --show-current
master

$ git rev-parse --short HEAD
0143fd1

$ git log -1 --oneline
0143fd1 chore: migra orquestrador para repositorio independente

$ git diff --cached --name-only
# saida vazia

$ git remote -v
# saida vazia
```

Comparacao com estado esperado informado:

| Item esperado | Estado observado | Classificacao |
|---|---|---|
| branch `master` | `master` | CONVERGENTE |
| HEAD abreviado `0143fd1` | `0143fd1` | CONVERGENTE |
| workspace limpo | `git status --short` vazio antes deste relatorio | CONVERGENTE |
| stage vazio | `git diff --cached --name-only` vazio | CONVERGENTE |
| estrutura operacional `config/`, `docs/`, `tela/` | presentes | CONVERGENTE |
| suite canonica de seis scripts | registrada em H-0031 como seis scripts `tela/teste_*.py` | CONVERGENTE_COM_DOCUMENTACAO |
| resultado anterior `1796/1796` | registrado em `docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md` e `docs/relatorios/RELATORIO_QA_H-0031_IMPLEMENTACAO.md` | CONVERGENTE_COM_DOCUMENTACAO |

Divergencia material: nenhuma divergencia observada antes da criacao deste relatorio.

Observacao: a raiz contem tambem `.agents` e `.codex`, listados por `find . -maxdepth 1 -mindepth 1 -printf '%f\n' | sort`. Esses diretorios nao aparecem em `git status --short`; origem: `NAO_CONFIRMADA`.

## 3. Autoridades consultadas

Autoridades documentais lidas ou varridas por trecho relevante:

| Caminho | Trecho/simbolo consultado | Evidencia | Classificacao |
|---|---|---|---|
| `docs/adr/INDICE_ADR.md` | tabela de ADRs aceitas | ADR-0001 a ADR-0020 aceitas | AUTORIDADE_ATIVA |
| `docs/NOMENCLATURA.md` | politica ADR-0008; secoes Estilo, Tela, Corpo, `orquestrador.py` legado | define responsabilidades de `config/estilo.json`, `tela.json`, termos `console`, `dashboard`, `barra_de_menus` | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` | modelo de configuracao por tela | base para JSON declarativo por tela | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0009-caminho-formato-jsons-tela.md` | caminho `config/telas/<id>.json`; `orquestrador.json`; `config/estilo.json` fora de `config/telas/` | caminho canonico atual | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` | `dashboard` como elemento funcional; `posicao_dashboard` descontinuado | dashboard segue composicao do corpo | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md` | barra declarativa por tela | renderer nao deve inventar chips ausentes | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` | `barra_de_menus.distribuicao.modo = horizontal_responsiva`; termo especifico completo | chips declarados, sem omissao/truncamento/reordenacao | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | composicao e distribuicao de corpo | base para grupos/distribuicao | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | ausencia de distribuicao nao equivale a `igual` | preserva construcao por conteudo | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | multiplicidade de dashboards e grupos | remove cardinalidade global de dashboard | AUTORIDADE_ATIVA |
| `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` | `grupo.estrutura = matriz` | base das telas H-0030 de matriz | AUTORIDADE_ATIVA |
| `docs/contratos/contrato_json_tela_minima.md` | caminho, campos obrigatorios, `config/telas/<id>.json` | contrato de envelope minimo | CONTRATO_ATIVO |
| `docs/contratos/contrato_tela_json.md` | relacao `estilo.json` global x `tela.json` | tela concreta declarativa | CONTRATO_ATIVO |
| `docs/contratos/contrato_composicao_corpo.md` | R-1, R-3, R-5, pendencias | fonte do corpo e `dashboard` | CONTRATO_ATIVO |
| `docs/contratos/contrato_barra_de_menus.md` | chips, estado dinamico, relacao com estilo | barra fixa e declarativa | CONTRATO_ATIVO |
| `docs/contratos/contrato_chip.md` | relacao do chip com `config/estilo.json` | aparencia do chip | CONTRATO_ATIVO |
| `docs/contratos/contrato_estilo.md` | estilo universal | borda, chip, indicadores, tiling | CONTRATO_ATIVO |
| `docs/contratos/contrato_console.md` | console como container navegavel | sem tipos internos fechados | CONTRATO_ATIVO |
| `docs/contratos/contrato_lancador.md` | lancador como corpo de navegacao | destino por `tela_destino` | CONTRATO_ATIVO |
| `docs/handoff/H-0031-migracao-repositorio-orquestrador-raiz-independente.md` | migracao para raiz independente | confirma escopo do ultimo ciclo | HISTORICO_RECENTE |
| `docs/relatorios/IMP-0031-migracao-repositorio-orquestrador-raiz-independente.md` | testes e arquivos alterados | seis scripts, `1796/1796` | HISTORICO_RECENTE |
| `docs/relatorios/RELATORIO_QA_H-0031_IMPLEMENTACAO.md` | QA implementacao H-0031 | confirma suite `1796 / 1796` | HISTORICO_RECENTE |
| `docs/handoff/H-0030-catalogo-telas-utilizaveis.md` | catalogo H-0030 | origem das cinco telas H-0030 | HISTORICO_RECENTE |
| `docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md` | catalogo implementado | classifica H-0030 como fixtures/catalogo | HISTORICO_RECENTE |

Leituras de codigo/configuracao:

- todos os arquivos diretamente sob `config/`;
- todos os arquivos diretamente sob `config/telas/`;
- toda a arvore `tela/`;
- arquivos de entrada executaveis na raiz: nenhum arquivo diretamente na raiz foi encontrado por `find . -maxdepth 1 -type f -print | sort`;
- referencias em testes e documentacao recente via `rg`.

## 4. Arvore real relevante

Raiz operacional observada:

```text
.agents
.codex
.git
config
docs
tela
```

Diretorios de ambiente:

| Caminho | Estado | Origem |
|---|---|---|
| `.agents/` | existe fisicamente, nao rastreado em `git status --short` | NAO_CONFIRMADA |
| `.codex/` | existe fisicamente, nao rastreado em `git status --short` | NAO_CONFIRMADA |

Arquivos diretamente em `config/`:

```text
config/barra_de_menus.json
config/cabecalho.json
config/estilo.json
config/lancador.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json
```

Arquivos diretamente em `config/telas/`:

```text
config/telas/destino_minimo.json
config/telas/grupo_minimo.json
config/telas/h0029_dashboard_fracao.json
config/telas/h0029_dashboard_igual.json
config/telas/h0029_dashboard_percentual.json
config/telas/h0029_grupo_fracao.json
config/telas/h0029_grupo_igual.json
config/telas/h0029_grupo_pai_distribuido.json
config/telas/h0029_grupo_percentual.json
config/telas/h0030_console_unico.json
config/telas/h0030_dashboard_unico.json
config/telas/h0030_matriz_2x2.json
config/telas/h0030_matriz_2x4.json
config/telas/h0030_matriz_3x2.json
config/telas/orquestrador.json
config/telas/stub_b.json
```

Arquivos em `tela/`:

```text
tela/__init__.py
tela/demo.py
tela/diagnostico.py
tela/explorar_barra_de_menus.py
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Pontos de entrada presentes:

| Caminho | Funcao observada | Evidencia |
|---|---|---|
| `tela/demo.py` | aplicacao demonstravel minima; possui `main()` e `if __name__ == "__main__"` | docstring e linhas de import/fluxo; `tela/teste_demo.py` invoca via subprocess |
| `tela/diagnostico.py` | diagnostico executavel da tela raiz | docstring; `gerar_diagnostico_tela`; `tela/teste_diagnostico.py` invoca via subprocess |
| `tela/explorar_barra_de_menus.py` | script exploratorio de combinacoes da barra | docstring; `if __name__ == "__main__"` |
| `orquestrador.py` | PREVISTO_NAO_CRIADO | nao encontrado por `rg --files`; mencionado apenas como intencao/legado em documentos |
| `demo/` | PREVISTO_NAO_CRIADO | nao encontrado na raiz |
| `config/telas/demo/` | PREVISTO_NAO_CRIADO | nao encontrado sob `config/telas/` |

Testes e demonstracoes:

| Caminho | Tipo | Evidencia |
|---|---|---|
| `tela/teste_loader.py` | teste executavel direto | docstring `python tela/teste_loader.py`; resumo H-0031 `244/244` |
| `tela/teste_modelo.py` | teste executavel direto | docstring; resumo H-0031 `148/148` |
| `tela/teste_renderizador.py` | teste executavel direto | docstring; resumo H-0031 `980/980` |
| `tela/teste_demo.py` | teste executavel direto e subprocess de demo | docstring; chama `python tela/demo.py`; resumo H-0031 `358/358` |
| `tela/teste_diagnostico.py` | teste executavel direto e subprocess de diagnostico | docstring; chama `python tela/diagnostico.py`; resumo H-0031 `28/28` |
| `tela/teste_explorar_barra_de_menus.py` | teste executavel direto e subprocess de exploracao | docstring; resumo H-0031 `38/38` |

Arquivos nao rastreados antes da criacao deste relatorio: nenhum, conforme `git status --short` vazio.

## 5. Inventario classificado

### 5.1 Codigo em `tela/`

| Caminho atual | Categoria | Funcao observada | Referencias recebidas | Referencias emitidas | Destino pretendido declarado | Risco se movido/renomeado |
|---|---|---|---|---|---|---|
| `tela/__init__.py` | codigo | pacote Python `tela` | imports `from tela...` dependem do pacote | nenhuma material observada | intencao do usuario: migrar codigo de `tela/` para `demo/` | ALTO: quebra imports absolutos `tela.*` |
| `tela/loader.py` | codigo generico | carrega `config/telas/<id>.json`, valida schema macro | testes, `demo.py`, `diagnostico.py`, `modelo.py` | `Path(__file__).resolve().parent.parent`; `os.path.join("config","telas",...)` | destino ainda nao decidido; codigo pode ser generico | ALTO: caminho depende de estar um nivel abaixo da raiz; imports `tela.loader` |
| `tela/modelo.py` | codigo generico | constroi modelo inerte a partir do loader | testes, `demo.py`, `diagnostico.py`, `renderizador.py` | `from tela.loader import ...` | destino ainda nao decidido; codigo pode ser generico | ALTO: import absoluto e pacote `tela` |
| `tela/renderizador.py` | codigo generico/demonstracao | renderiza `ModeloTela`; nao acessa JSON diretamente | testes, `demo.py`, `diagnostico.py`, explorador | `from tela.modelo import ModeloTela` | destino ainda nao decidido | ALTO: import absoluto; testes verificam proibicoes de import |
| `tela/demo.py` | demonstracao/entrada atual | demo TUI; navega por `lancador.itens[].tela_destino`; carrega por id | `tela/teste_demo.py`; H-0030 chama ponto de entrada real | `from tela.loader/modelo/renderizador`; `_carregar_modelo_por_id`; `__file__` bootstrap | intencao do usuario: migrar para `demo/`; futuro produto usara `orquestrador.py` | ALTO: subprocesses chamam `tela/demo.py`; snapshots dependem do caminho |
| `tela/diagnostico.py` | entrada diagnostica | encadeia carregar/modelar/renderizar `orquestrador` | `tela/teste_diagnostico.py`, `tela/teste_demo.py` | `from tela.loader/modelo/renderizador`; `__file__` bootstrap | nao declarado | ALTO: subprocesses chamam `tela/diagnostico.py` |
| `tela/explorar_barra_de_menus.py` | demonstracao/exploracao | exercita combinacoes de barra | `tela/teste_explorar_barra_de_menus.py` | `Path(__file__).resolve().parent.parent`; `from tela.renderizador` | nao declarado | MEDIO/ALTO: teste invoca script e importa modulo |

### 5.2 Testes em `tela/`

| Caminho atual | Categoria | Funcao observada | Referencias emitidas | Destino pretendido declarado | Risco se movido/renomeado |
|---|---|---|---|---|---|
| `tela/teste_loader.py` | teste | valida loader, JSONs reais, catalogo H-0030 e preservacoes H-0029 | `Path(__file__).parent.parent`, `from tela`, `config/telas/orquestrador.json`, ids H-0029/H-0030 | destino ainda nao decidido | ALTO: depende de pacote e caminhos atuais |
| `tela/teste_modelo.py` | teste | valida modelo e catalogo H-0030 | `from tela.loader/modelo`, ids `orquestrador`, `grupo_minimo`, H-0030 | destino ainda nao decidido | ALTO |
| `tela/teste_renderizador.py` | teste | valida renderer, geometria, JSONs H-0029/H-0030 | `from tela.*`, varios `carregar_tela(_BASE_PADRAO, id)` | destino ainda nao decidido | ALTO |
| `tela/teste_demo.py` | teste | valida demo, subprocess, snapshots, navegacao | subprocess `[sys.executable, "tela/demo.py"]`, `config/telas/orquestrador.json` | destino ainda nao decidido | MUITO_ALTO: path literal em subprocess |
| `tela/teste_diagnostico.py` | teste | valida diagnostico e invariantes anteriores | subprocess `[sys.executable, "tela/diagnostico.py"]` | destino ainda nao decidido | ALTO |
| `tela/teste_explorar_barra_de_menus.py` | teste | valida explorador | subprocess do script; `from tela.renderizador` | destino ainda nao decidido | ALTO |

### 5.3 Configuracao direta em `config/`

| Caminho atual | Categoria | Funcao observada | Consumidores observados | Vinculo documental | Destino pretendido declarado | Risco se movido/renomeado |
|---|---|---|---|---|---|---|
| `config/estilo.json` | configuracao de estilo | biblioteca global de aparencia: borda, chip, indicadores | documentacao e testes historicos; renderer atual hardcoda bordas e nao le este arquivo | ADR-0009; `docs/NOMENCLATURA.md`; `contrato_estilo.md` | deve permanecer fora de `config/telas/` pela ADR-0009; reorganizacao interna ainda pendente | MEDIO: autoridade documental forte, mas consumidor runtime atual limitado |
| `config/cabecalho.json` | configuracao de parametros de elemento | parametros de apresentacao de cabecalho | NAO_CONFIRMADO em runtime atual | `docs/NOMENCLATURA.md`; `contrato_cabecalho.md` | possivel grupo futuro de parametros de elementos | MEDIO |
| `config/barra_de_menus.json` | configuracao de parametros de elemento/barra | ordem canonica, rotulos e regras de chips | NAO_CONFIRMADO em runtime atual; docs/testes consultam conceitos | `contrato_barra_de_menus.md`; ADR-0012/0014 | possivel grupo futuro de parametros de elementos | MEDIO |
| `config/lancador.json` | configuracao de layout e parametros de elemento | layout/verificacao/navegacao do lancador | NAO_CONFIRMADO em runtime atual | ADR-0001/0002/0003; `contrato_lancador.md` | possivel grupo futuro de parametros de elementos/layout | MEDIO |
| `config/layout_console.json` | configuracao de layout | parametros de layout do console | NAO_CONFIRMADO em runtime atual; contrato exige leitura futura | `contrato_composicao_corpo.md` criterio cita este arquivo | possivel grupo de layout ou parametros de console | MEDIO |
| `config/layout_dado.json` | outra categoria comprovada: obsoleto/transicional | rastreabilidade da migracao `dado` -> `console` | NAO_CONFIRMADO em runtime atual | `docs/NOMENCLATURA.md` marca obsoleto/transicional | destino ainda nao decidido; nao usar como fonte canonica | BAIXO/MEDIO |
| `config/layout_menu.json` | outra categoria comprovada: obsoleto/transicional | rastreabilidade da migracao `menu` -> `lancador` | NAO_CONFIRMADO em runtime atual | `docs/NOMENCLATURA.md` marca obsoleto/transicional | destino ainda nao decidido; nao usar como fonte canonica | BAIXO/MEDIO |

### 5.4 Telas declarativas em `config/telas/`

Todos os arquivos abaixo sao `tela declarativa` porque possuem `schema: tela.v1`, `id`, `cabecalho`, `corpo`, `barra_de_menus` e seguem o caminho canonico da ADR-0009.

| Caminho atual | Categoria adicional comprovada | Funcao observada | Referencias recebidas | Destino pretendido declarado | Risco se movido/renomeado |
|---|---|---|---|---|---|
| `config/telas/orquestrador.json` | entrada real/draft atual | tela raiz atual; `id=orquestrador`; corpo com `console`, `dashboard`, `lancador`; destinos d/g/1..5 | loader default, demo, diagnostico, todos os testes principais | usuario declarou renomear para `config/telas/demo/demo.json` ou equivalente aprovado | MUITO_ALTO |
| `config/telas/destino_minimo.json` | demonstracao/teste | tela destino minima H-0010A | `tela/teste_demo.py`, `teste_loader.py`, `teste_renderizador.py` | usuario declarou migrar telas existentes para `config/telas/demo/` | ALTO |
| `config/telas/grupo_minimo.json` | demonstracao/teste | grupo estrutural minimo | testes e demo via chip `g` | migracao pretendida para subpasta demo | ALTO |
| `config/telas/stub_b.json` | demonstracao/teste | stub declarativo legado | preservacoes em `teste_loader.py`/`teste_renderizador.py` | migracao pretendida para subpasta demo | MEDIO/ALTO |
| `config/telas/h0029_*.json` | teste/fixture permanente H-0029 | sete telas de distribuicao/cardinalidade | `tela/teste_loader.py` preserva; `tela/teste_renderizador.py` geometria H-0029 | migracao pretendida para subpasta demo ainda precisa decidir se fixtures seguem junto | ALTO |
| `config/telas/h0030_console_unico.json` | fixture/catalogo H-0030 | catalogo: console unico | loader/modelo/renderizador/demo H-0030 | migracao pretendida para subpasta demo | ALTO |
| `config/telas/h0030_dashboard_unico.json` | fixture/catalogo H-0030 | catalogo: dashboard unico | loader/modelo/renderizador/demo H-0030 | migracao pretendida para subpasta demo | ALTO |
| `config/telas/h0030_matriz_2x2.json` | fixture/catalogo H-0030 | catalogo: matriz 2x2 | loader/modelo/renderizador/demo H-0030 | migracao pretendida para subpasta demo | ALTO |
| `config/telas/h0030_matriz_2x4.json` | fixture/catalogo H-0030 | catalogo: matriz 2x4 | loader/modelo/renderizador/demo H-0030 | migracao pretendida para subpasta demo | ALTO |
| `config/telas/h0030_matriz_3x2.json` | fixture/catalogo H-0030 | catalogo: matriz 3x2 | loader/modelo/renderizador/demo H-0030 | migracao pretendida para subpasta demo | ALTO |

Destino ainda nao decidido: todos os arquivos que seriam movidos para `config/telas/demo/` dependem da politica de compatibilidade de `carregar_tela`, da regra de coincidencia `id`/nome do arquivo, do destino dos testes, e da decisao se fixtures H-0029/H-0030 sao demonstracao, regressao permanente ou outro grupo.

## 6. Referencias e dependencias

### 6.1 Referencias ativas em codigo e testes

| Referencia | Arquivo e trecho | Natureza | Impacto de movimentacao | Atualizacao necessaria | Compatibilidade transitoria |
|---|---|---|---|---|---|
| `config/telas/<id_tela>.json` | `tela/loader.py:567`, docstring; `tela/loader.py:594`, `os.path.join("config", "telas", id_tela + ".json")` | ativa | mover telas quebra carregamento | alterar politica de resolucao de caminho ou criar compatibilidade | ausente |
| `Path(__file__).resolve().parent.parent` | `tela/loader.py:141`; testes e explorador possuem `_BASE_PADRAO`/`_BASE` | ativa/dinamica | mover `tela/` para `demo/` preserva nivel relativo se `demo/` ficar na raiz; mover para subnivel quebra | revisar base path em todos os arquivos | ausente |
| `from tela.loader/modelo/renderizador` | `tela/demo.py:117-119`, `tela/diagnostico.py:48-50`, `tela/modelo.py:23`, `tela/renderizador.py:67`, testes | ativa | renomear pacote `tela` para `demo` quebra imports | atualizar imports ou criar alias pacote | ausente |
| `python tela/demo.py` | `tela/teste_demo.py:821`, `876`, `918`, `976`, `1027`, `1084`, `1660`, `1696`, `2732`, `2860`, `3093`, `3179` | ativa/subprocess | mover demo quebra suite | atualizar subprocesses e snapshots | ausente |
| `python tela/diagnostico.py` | `tela/teste_diagnostico.py:235-238`; `tela/teste_demo.py:1173-1180` | ativa/subprocess | mover diagnostico quebra suite | atualizar subprocesses | ausente |
| `orquestrador` id default | `tela/demo.py:136`; `tela/diagnostico.py:53`; `tela/loader.py:38` `_ID_TELA_RAIZ` | ativa | renomear `orquestrador.json` para `demo.json` quebra id/nome e default | decidir se `id` muda, se tela raiz demo continua `orquestrador`, ou se loader aceita aliases | ausente |
| `config/telas/orquestrador.json` literal | `tela/teste_demo.py:797`, `942`; docstrings em testes | ativa/teste | renomear arquivo quebra verificacoes de integridade e snapshots | atualizar testes autorizadamente | ausente |
| `orquestrador.json` em comentarios/testes | `tela/teste_loader.py:138`; `tela/teste_renderizador.py:152`, `4650` | ativa/teste/regressao | altera expectativa sem nova autoridade | atualizar escopo e criterios | ausente |
| `chip_estilo is None` | `tela/teste_loader.py:242-250`; `tela/teste_modelo.py:280-288` | ativa/regressao | adicionar acesso a estilos na barra conflita com teste atual | ADR/contrato e atualizacao de testes necessarios | ausente |

### 6.2 Referencias documentais relevantes

| Referencia | Arquivo e trecho | Natureza | Impacto |
|---|---|---|---|
| `config/telas/<id>.json` | `docs/adr/ADR-0009-caminho-formato-jsons-tela.md:49-56`; `docs/contratos/contrato_json_tela_minima.md:322-340` | normativa ativa | subdiretorio `config/telas/demo/` nao esta coberto explicitamente; requer decisao/ADR ou atualizacao contratual |
| `config/telas/orquestrador.json` | ADR-0009 registra caminho para tela raiz | normativa ativa | renomear para `demo.json` conflita com identificador canonico atual `orquestrador` sem nova decisao |
| `config/estilo.json` fora de `config/telas/` | `docs/adr/ADR-0009...:83-86`; `docs/NOMENCLATURA.md:35` | normativa ativa | organizacao futura de JSONs deve preservar papel de biblioteca global ou alterar autoridade |
| `dashboard` segue composicao do corpo | ADR-0010 decisao 1/4; `contrato_composicao_corpo.md` R-5 | normativa ativa | remover dados especificos do dashboard e mudar tela minima requer ADR/handoff, nao apenas edicao |
| `barra_de_menus` declarativa por tela | ADR-0012/ADR-0014; contratos | normativa ativa | adicionar acesso a estilos exige chip declarado e possivelmente registry/tela destino |
| `orquestrador.py` | `docs/NOMENCLATURA.md:1042,1052` menciona legado/futuro primeiro caso concreto | historica/pendente | nao ha contrato ativo de comportamento do futuro ponto de entrada |

### 6.3 Dependencias de ordem observadas

- `carregar_tela` exige coincidencia entre `id` interno e basename (`tela/loader.py`, classe `TelaIdNaoCoincideComArquivo` e validacao por `caminho_arquivo.stem`). Portanto, renomear `orquestrador.json` para `demo.json` sem alterar `id` para `demo` quebra a validacao.
- `tela/demo.py` inicia em `tela_atual = "orquestrador"` e chama `carregar_tela(None, tela_atual)`. Portanto, uma demo renomeada precisa decidir novo id inicial, alias, ou compatibilidade.
- A suite usa subprocess com caminhos literais `tela/demo.py` e `tela/diagnostico.py`; mover codigo exige atualizar testes no mesmo ciclo ou fornecer wrapper transitorio.
- A nova barra com acesso a estilos conflita com testes que comprovam ausencia de `chip_estilo`; essa mudanca requer autoridade explicita e atualizacao de testes.

## 7. Impacto sobre testes e demonstracao

Suite canonica atual documentada em H-0031:

| Script | Verificacoes H-0031 | Dependencias materiais |
|---|---:|---|
| `python3 tela/teste_loader.py` | 244/244 | pacote `tela`, `config/telas/orquestrador.json`, ids H-0029/H-0030 |
| `python3 tela/teste_modelo.py` | 148/148 | pacote `tela`, modelos de `orquestrador`, `grupo_minimo`, H-0030 |
| `python3 tela/teste_renderizador.py` | 980/980 | pacote `tela`, snapshots/saida de JSONs reais, H-0029/H-0030 |
| `python3 tela/teste_demo.py` | 358/358 | subprocess `tela/demo.py`, `config/telas/orquestrador.json`, navegacao d/g/1..5 |
| `python3 tela/teste_diagnostico.py` | 28/28 | subprocess `tela/diagnostico.py`, `gerar_diagnostico_tela("orquestrador")` |
| `python3 tela/teste_explorar_barra_de_menus.py` | 38/38 | subprocess/import do explorador e renderer |

Arquivos que precisariam ser autorizados em futuro handoff para manter a suite:

- `tela/loader.py` para nova politica de localizacao ou compatibilidade de `config/telas/demo/`;
- `tela/demo.py` se o ponto de entrada demo mudar ou se houver wrapper;
- `tela/diagnostico.py` se diagnostico acompanhar a migracao;
- `tela/modelo.py` se imports/pacote forem renomeados;
- `tela/renderizador.py` se a tela minima ou estilos exigirem comportamento nao implementado;
- todos os `tela/teste_*.py` para paths/imports/snapshots;
- todos os JSONs em `config/telas/` que forem movidos/renomeados;
- possiveis wrappers em `tela/` ou `demo/`, caso se decida compatibilidade transitoria.

Sem autorizacao desses arquivos, ha conflito provavel entre criterios de aceite e arquivos afetados.

## 8. Separacao entre demonstracao e produto real

Componentes inequivocamente demonstrativos pelo estado observado:

- `tela/demo.py`: docstring declara "Aplicacao demonstravel local minima".
- `tela/explorar_barra_de_menus.py`: script de exploracao, nao ponto de entrada real.
- `config/telas/h0030_*.json`: H-0030 e IMP-0030 tratam como catalogo/fixtures de telas utilizaveis.
- `config/telas/destino_minimo.json`, `grupo_minimo.json`, `stub_b.json`: telas de teste/destino demonstrativo conforme titulos/docstrings e cobertura dos testes.

Componentes genericos que podem ser compartilhados, mas nao podem ser classificados como demonstracao sem decisao arquitetural:

- `tela/loader.py`;
- `tela/modelo.py`;
- `tela/renderizador.py`;
- contratos e ADRs de tela, corpo, barra, estilo, console, lancador, dashboard;
- `config/estilo.json` e possivelmente parametros transicionais de `config/`.

Componentes acoplados ao nome/caminho `tela/`:

- todos os imports `from tela...`;
- bootstraps por `__file__` em `demo.py` e `diagnostico.py`;
- bases por `Path(__file__).resolve().parent.parent` em loader/testes/explorador;
- subprocesses em testes;
- documentacao de execucao dos seis scripts.

`orquestrador.py`:

- nao existe fisicamente;
- nao ha contrato ativo especifico para seu comportamento;
- ha mencoes em `docs/NOMENCLATURA.md` relacionadas a legado/futuro primeiro caso concreto, mas nao uma autoridade operacional suficiente para criar o arquivo;
- criacao exige decisao sobre responsabilidades: ponto de entrada real, relacao com demo, uso de loader/modelo/renderizador, politica de configuracao, interface com Pipeline e comportamento minimo.

Decisoes necessarias antes de mover toda a arvore para `demo/`:

- se codigo generico fica em `demo/`, em pacote compartilhado novo, ou permanece em `tela/`;
- se `demo/` e apenas aplicacao demonstrativa ou pacote de infraestrutura;
- se havera compatibilidade de imports `tela.*`;
- se os seis scripts canonicos mudam de caminho;
- se `config/telas/demo/` aceita subdiretorios e como `carregar_tela` resolve ids;
- se `orquestrador.py` nasce no mesmo ciclo ou depois da migracao demo.

## 9. Agrupamento dos JSON de configuracao

Grupos por funcao comprovada:

| Grupo funcional | Arquivos | Finalidade comprovada | Consumidores observados | Vinculos contratuais | Sobreposicao/dependencia |
|---|---|---|---|---|---|
| Aparencia global | `config/estilo.json` | presets de borda, chip, indicadores | documentos; renderer atual ainda hardcoda parte de bordas | `contrato_estilo.md`, `contrato_chip.md`, ADR-0004/0009 | nao deve entrar em `config/telas/` pela ADR-0009 |
| Parametros de apresentacao por regiao/tipo | `config/cabecalho.json`, `config/barra_de_menus.json`, `config/lancador.json`, `config/layout_console.json` | parametros de cabecalho, barra, lancador, console | runtime atual NAO_CONFIRMADO; contratos referenciam | contratos de cabecalho/barra/lancador/console/composicao | mistura "layout" e "propriedades de elemento" |
| Layout transicional obsoleto | `config/layout_dado.json`, `config/layout_menu.json` | rastreabilidade de `dado` -> `console` e `menu` -> `lancador` | runtime atual NAO_CONFIRMADO | `docs/NOMENCLATURA.md` marca obsoleto/transicional | nao usar como fonte canonica nova |
| Telas declarativas | `config/telas/*.json` | declaracao concreta de telas | loader/demo/diagnostico/testes | ADR-0009, contrato_json_tela_minima, contrato_tela_json | futuro `config/telas/demo/` requer decisao |

Possiveis criterios objetivos para nomear diretorios:

- separar por papel (`aparencia`, `layout`, `elementos`, `telas`);
- separar por consumidor (`renderer`, `loader`, `demo`, `produto`);
- separar por estabilidade (`ativo`, `transicional`, `demo`);
- separar por granularidade (`global`, `por_tipo`, `por_tela`).

NOME_FINAL_PENDENTE_DE_DECISAO_DO_USUARIO

## 10. Opcoes nao normativas de nomes

As opcoes abaixo nao sao decisao.

| Opcao | Significado | Abrangeria | Vantagens | Ambiguidades/conflitos |
|---|---|---|---|---|
| `config/aparencia/` | biblioteca global visual | `estilo.json` | nome claro para borda/chip/indicadores | ADR-0009 hoje fixa `config/estilo.json`; mover requer ADR/contrato |
| `config/layout/` | parametros de layout | `layout_console.json`, talvez `lancador.json`, `cabecalho.json`, `barra_de_menus.json` | separa dimensoes/vaos/alinhamento | `barra_de_menus.json` tambem contem ordem/acao; `lancador.json` contem navegacao |
| `config/elementos/` | propriedades por tipo/regiao | `cabecalho.json`, `barra_de_menus.json`, `lancador.json`, `layout_console.json` | aproxima "parametros de cada parte da tela" | pode misturar layout com comportamento |
| `config/parametros_elementos/` | parametros/propriedades por componente | mesmos acima | explicito e autoexplicativo | nome longo; conflita com status transicional de alguns arquivos |
| `config/transicional/` | artefatos nao canonicos | `layout_dado.json`, `layout_menu.json` | reduz risco de uso indevido | mover arquivos obsoletos tambem requer autorizacao e atualizacao documental |
| `config/telas/demo/` | telas demonstrativas | JSONs existentes se aprovados como demo | libera `config/telas/` para produto real | conflita com ADR-0009 e loader atual que espera arquivo direto |

NOME_FINAL_PENDENTE_DE_DECISAO_DO_USUARIO

## 11. Escopo documental e necessidade de ADR

| Tema | Estado documental observado | Classificacao |
|---|---|---|
| Separacao entre demonstracao e produto real | intencao declarada pelo usuario; nao encontrada ADR especifica | requer ADR |
| Movimentacao `tela/` -> `demo/` | intencao declarada; H-0031 migrou `scripts/tela` -> `tela`, nao `tela` -> `demo` | requer ADR ou handoff com decisao previa |
| Politica `config/telas/` x `config/telas/demo/` | ADR-0009 fixa `config/telas/<id>.json`; subdiretorio nao coberto | requer ADR e atualizacao contratual |
| Renomear `config/telas/orquestrador.json` para `demo.json` | conflita com regra id/basename e caminho atual | requer ADR/contrato/handoff |
| Definir tela minima real do Orquestrador | contratos permitem `console`, `dashboard`, `barra_de_menus`, mas conteudo especifico nao decidido | requer ADR |
| Remover dados atuais especificos do dashboard | `orquestrador.json` tem campos pendentes de dashboard; contrato ainda cita draft numerico do Orquestrador | requer ADR/atualizacao contratual |
| Incorporar acesso a estilos na `barra_de_menus` | historico registra `chip_estilo` removido; testes atuais exigem ausencia | requer ADR/contrato/testes |
| Criar `orquestrador.py` | arquivo inexistente; sem contrato ativo | requer ADR ou contrato antes de handoff |
| Organizar JSONs de `config/` em diretorios | ADR-0009 preserva transicionais; nomes ainda nao decididos | requer decisao do usuario e provavelmente ADR/contrato |
| Manter `config/estilo.json` fora de `config/telas/` | ja documentado | ja documentado |
| Executar mudancas puramente declarativas em JSON | contrato de processo permite em certas condicoes | simples aplicacao somente se nao alterar arquitetura/caminho/schema |

Conclusao: ha varias decisoes independentes. Uma ADR unica pode ser coesa apenas se seu escopo for "separacao estrutural demo/produto e politica de caminhos". A tela minima real, `orquestrador.py`, acesso a estilos e organizacao de JSONs podem exigir ADRs separadas ou secoes claramente independentes.

## 12. Dependencias obrigatorias de sequencia

DEPENDENCIA_OBRIGATORIA

1. Decidir o escopo documental antes de criar ADR: uma ADR unica ou ADRs separadas.
2. Decidir se `config/telas/demo/` e permitido antes de mover qualquer JSON.
3. Decidir regra de resolucao de ids/caminhos antes de renomear `orquestrador.json`.
4. Decidir destino de codigo generico antes de mover toda a arvore `tela/`.
5. Decidir compatibilidade transitoria antes de atualizar testes/subprocesses.
6. Definir comportamento de `orquestrador.py` antes de cria-lo.
7. Decidir se o acesso a estilos e declarativo inerte ou navegacao real antes de recolocar `chip_estilo` ou equivalente.

ORDEM_RECOMENDADA

1. ADR de separacao demo/produto e politica de caminhos.
2. Atualizacao de contratos afetados (`contrato_json_tela_minima.md`, `contrato_tela_json.md`, possivelmente processo).
3. Handoff de migracao estrutural com escopo nominal dos JSONs, codigo e testes.
4. Implementacao da migracao com compatibilidade definida.
5. ADR da tela minima do Orquestrador real.
6. Handoff para `orquestrador.py` e tela real minima.

PODE_OCORRER_EM_PARALELO_DOCUMENTAL

- levantamento de nomes de diretorios de `config/`;
- levantamento do contrato de estilos/tela de estilos;
- levantamento de responsabilidades entre demo e produto real.

CICLO_POSTERIOR

- implementacao da tela de estilos capaz de alterar borda/chips;
- criacao de navegacao real para tela de estilos;
- integracao concreta com Pipeline;
- remocao definitiva de wrappers/aliases transitorios, se forem criados.

## 13. Alternativas de divisao de ciclos

| Alternativa | Descricao | Coesao | Risco | Testabilidade | Reversibilidade | Dependencias |
|---|---|---|---|---|---|---|
| A | ciclo documental unico para demo/produto/caminhos, depois implementacao estrutural | alta para estrutura | medio | boa: suite antes/depois | boa se handoff granular | exige ADR bem delimitada |
| B | ADRs separadas: estrutura demo/produto; tela minima; `orquestrador.py`; config JSONs | alta por decisao | menor por ciclo | boa por tema | alta | mais ciclos e mais trabalho documental |
| C | migrar demonstracao primeiro, adiar `orquestrador.py` e tela minima | coesa para limpeza | medio/alto se loader/testes mudarem muito | boa se wrappers claros | media | precisa resolver `config/telas/demo/` e imports antes |

Comparacao neutra:

- A reduz fragmentacao, mas pode ficar ampla demais se incluir estilo e `orquestrador.py`.
- B e a mais clara para auditoria, mas exige mais artefatos.
- C entrega separacao fisica cedo, mas nao resolve produto real e pode gerar compatibilidade temporaria longa.

Nenhuma alternativa foi iniciada.

## 14. DECISOES_NECESSARIAS_DO_USUARIO

1. A ADR deve cobrir uma decisao unica ampla de separacao demo/produto ou ser dividida em ADRs menores?
2. O diretorio final para telas demonstrativas sera `config/telas/demo/` ou outro caminho?
3. `config/telas/orquestrador.json` deve virar `config/telas/demo/demo.json` com `id = "demo"`, ou deve haver alias/compatibilidade mantendo `id = "orquestrador"`?
4. Os testes atuais devem migrar para `demo/`, permanecer em `tela/`, ou ir para outro pacote/diretorio?
5. Codigo generico hoje em `tela/loader.py`, `tela/modelo.py` e `tela/renderizador.py` pertence a demo, ao Orquestrador real, ou a um nucleo compartilhado?
6. Haverá compatibilidade temporaria para imports `tela.*` e subprocesses `tela/demo.py`?
7. Qual e o nome final dos diretorios de configuracao de layout e parametros de elementos?
8. `orquestrador.py` sera criado ja no proximo ciclo ou apenas documentado?
9. Qual a responsabilidade minima de `orquestrador.py`: chamar demo, carregar tela real, integrar Pipeline, ou apenas stub?
10. A tela minima real do Orquestrador sera implementada no mesmo ciclo da migracao estrutural ou em ciclo posterior?
11. O acesso a estilos na `barra_de_menus` sera apenas um chip declarativo inerte ou devera navegar para uma tela funcional?
12. A tela de estilos pertence ao mesmo ciclo da preparacao ou obrigatoriamente ao ciclo seguinte?
13. Os JSONs H-0029/H-0030 sao demo, fixtures permanentes de regressao, ou ambos?
14. Deve haver wrapper transitorio para manter a suite canonica enquanto os caminhos mudam?

## 15. Fatos nao confirmados

| Fato | Status | Observacao |
|---|---|---|
| Origem de `.agents/` e `.codex/` | NAO_CONFIRMADO | existem na raiz fisica, nao rastreados |
| Consumidor runtime atual de `config/cabecalho.json` | NAO_CONFIRMADO | contratos referenciam; codigo atual observado nao le diretamente |
| Consumidor runtime atual de `config/barra_de_menus.json` | NAO_CONFIRMADO | renderer usa declaracao da tela e defaults internos |
| Consumidor runtime atual de `config/lancador.json` | NAO_CONFIRMADO | contratos referenciam; renderer atual usa logica propria |
| Consumidor runtime atual de `config/layout_console.json` | NAO_CONFIRMADO | contrato exige futuro/criterio; leitura direta nao confirmada |
| Escopo exato da futura integracao com Pipeline | NAO_CONFIRMADO | nao ha contrato lido para interface Pipeline |
| Nome definitivo de diretorios novos de `config/` | NAO_CONFIRMADO | usuario declarou que nao decidiu |
| Comportamento do futuro `orquestrador.py` | NAO_CONFIRMADO | arquivo inexistente e sem contrato especifico |

## 16. Arquivos alterados nesta etapa

Arquivo criado:

```text
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
```

Arquivos alterados:

```text
docs/relatorios/LEVANTAMENTO_PREPARACAO_INTEGRACAO_PIPELINE_ORQUESTRADOR.md
```

Nenhum outro arquivo foi criado, movido, renomeado, removido ou alterado nesta etapa.

## 17. Conclusao

O estado atual observado confirma a raiz independente do Orquestrador em `master`, HEAD `0143fd1`, workspace e stage limpos antes da criacao deste relatorio, com estrutura operacional `config/`, `docs/` e `tela/`.

A direcao declarada pelo usuario ainda nao possui autoridade documental suficiente para implementacao direta. As decisoes sobre separacao demo/produto, politica de subdiretorios em `config/telas/`, renomeacao de `orquestrador.json`, destino de codigo generico, compatibilidade transitoria, organizacao de `config/`, tela minima real, `orquestrador.py` e acesso a estilos precisam ser fechadas antes de ADR/handoff de implementacao.

Dependencias obrigatorias principais:

- definir politica de caminhos/ids antes de mover JSONs;
- definir destino do pacote/imports antes de mover `tela/`;
- definir compatibilidade transitoria antes de preservar a suite canonica;
- definir escopo documental antes de criar ADR;
- definir responsabilidade de `orquestrador.py` antes de cria-lo.

