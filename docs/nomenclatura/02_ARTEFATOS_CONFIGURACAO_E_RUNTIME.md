---
name: nomenclatura-artefatos-configuracao-runtime
description: Nomenclatura dos artefatos de configuração e runtime — schema vs configuração concreta vs estado de runtime; separação motor/demo/produto; caminhos canônicos ativos ou reservados
metadata:
  type: nomenclatura
  scope: artefatos_configuracao_runtime
  fase_de_aplicacao: VIGENTE
---

# Artefatos, configuração e runtime

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário de:
- nomenclatura dos documentos de configuração do sistema;
- diferença entre schema, configuração concreta e estado de runtime;
- identificação e papel de cada artefato estrutural;
- separação entre motor compartilhado, demonstração e produto real;
- caminhos canônicos ativos ou reservados, devidamente classificados.

**Fronteira com o módulo `10`**: este módulo é proprietário do artefato
`config/estilo.json` como entidade e caminho (identidade, natureza de
configuração, relação com o runtime). O vocabulário interno de estilo —
campos, presets, indicadores e distinções semânticas — pertence ao
módulo `10_ESTILO.md`.

**Fronteira com o módulo `42`**: este módulo é proprietário do termo e
artefato `JSON estrutural da tela` — identidade do documento, natureza
de documento de configuração, caminho e relação com o schema da tela,
distinção geral entre configuração e runtime. O módulo
`42_DADOS_EXTERNOS_MULTINIVEL.md` referencia este termo exclusivamente
para delimitar a fronteira entre o JSON estrutural e o JSON externo de
conteúdo; essa referência é permitida e não constitui co-propriedade.
A repetição é classificada como
`REFERENCIA_PERMITIDA_COM_FRONTEIRA_EXPLICITA`.

Estados transitórios de migração não são apresentados como termos vigentes.

## 3. Termos proprietários

- `docs/NOMENCLATURA.md` (papel atual como fachada de compatibilidade e navegação)
- `config/estilo.json`
- `tela.json` (nome canônico da declaração por tela)
- `JSON estrutural da tela` (termo que designa o artefato `tela.json` como documento de configuração da interface)
- motor compartilhado (`tela/`)
- aplicação demonstrativa (`demo/`)
- produto real
- tela demonstrativa
- tela do produto real
- raiz declarativa da demonstração (`config/telas/demo/`)
- raiz declarativa do produto (`config/telas/`)
- ponto de entrada real (`orquestrador.py`)
- tela inicial real (`config/telas/orquestrador.json`)
- identidade real (`orquestrador`)
- `perfil` (campo raiz opcional do `tela.json`, ADR-0034)
- `controle_execucao` (objeto raiz opcional fechado do `tela.json`, ADR-0040)
- `modo_inicial` (único campo permitido em `controle_execucao`, ADR-0040)
- `controle_execucao.modo_inicial` (configuração concreta opcional do `tela.json`, ADR-0040)
- registro de ações
- ação registrada
- categoria da ação
- modos de execução aceitos
- autoridade implementacional da compatibilidade
- falha fechada de resolução
- ação legada não classificada

## 4. Definições

### 4.1 Responsabilidade de cada artefato (ADR-0008)

| Artefato | Responsabilidade |
|---|---|
| `docs/NOMENCLATURA.md` | No antigo monólito, substituído pela fachada na fase 2 da ADR-0029, este artefato era responsável por schema e semântica: quais campos existem, o que cada um significa, tipo, restrições e como o renderer deve interpretá-los. Atualmente `docs/NOMENCLATURA.md` atua somente como fachada de compatibilidade e navegação; a autoridade terminológica vigente está nos módulos proprietários. |
| `config/estilo.json` | Biblioteca global de aparência: presets de borda, chip, indicadores e demais parâmetros gerais de aparência. Não declara tela, conteúdo, composição, destino, ação, item de `lancador` nem instância de `dashboard`. |
| `tela.json` (JSON próprio de cada tela) | Declaração concreta da tela: composição do corpo, instâncias de `console`, `dashboard`, `lancador` e `barra_de_menus`, listas de itens, chips, destinos, ações registradas, regras de existência/ativo-inativo, parâmetros visuais locais, bindings, filtros e regras de exibição. Não é código executável. Não guarda estado de runtime nem declara categoria ou compatibilidade de ação. |

### 4.2 Separação motor / demonstração / produto real (ADR-0021)

| Termo | Definição |
|---|---|
| motor compartilhado | `tela/`; contém conceitualmente loader, modelo, renderizador e contratos genéricos de tela. É reutilizado pela demonstração e pelo produto real. |
| aplicação demonstrativa | `demo/`; diretório destinado a pontos de entrada, utilitários e testes exclusivos da demonstração. |
| produto real | Orquestrador operacional futuro, com telas declarativas diretamente em `config/telas/<id>.json` e ponto de entrada principal futuro `orquestrador.py`. |
| tela demonstrativa | Tela declarativa usada pela demonstração, sob a raiz `config/telas/demo/<id>.json`. |
| tela do produto real | Tela declarativa do Orquestrador real, sob `config/telas/<id>.json`. |
| raiz declarativa da demonstração | `config/telas/demo/`, raiz das telas demonstrativas. |
| raiz declarativa do produto | `config/telas/`, raiz reservada às telas do produto real. |

### 4.3 Tela inicial real reservada (ADR-0022)

| Termo | Definição |
|---|---|
| ponto de entrada real | `orquestrador.py`; arquivo futuro diretamente na raiz, reservado ao produto real e reutilizador do motor compartilhado `tela/`. |
| tela inicial real | `config/telas/orquestrador.json`; arquivo futuro/reservado ao produto real, com identificador interno `orquestrador`. |
| identidade real | `orquestrador`; identidade exclusiva do produto real, distinta de `demo`. |

### 4.4 Regras de localização

- Todos os JSON de configuração ficam em `config/`, na raiz do Orquestrador,
  irmã de `docs/`.
- Nunca criar JSON de configuração dentro de `docs/`.
- Para `lancador`: arquivo canônico é `config/elementos/lancador.json`;
  não criar `config/layout_lancador.json`.
- Nomenclatura de arquivo: nunca usar abreviação que misture dois termos já
  distinguidos no glossário.

### 4.5 Estado de runtime (não pertence ao JSON da tela)

Cursor atual, página atual, filtro ativo, modo verboso, seleção atual e item
focado são estado de execução, não configuração. O JSON pode declarar defaults
iniciais; o estado vivo pertence à execução.

No controle universal da ADR-0040, a configuração concreta é declarada pelo
objeto raiz opcional e fechado `controle_execucao` do `tela.json`, que contém
exatamente o campo obrigatório `modo_inicial`, limitado a `executar` ou
`dry_run`. A ausência do objeto significa não adoção da capacidade e não há
default implícito; propriedade interna adicional é inválida. O modo corrente
após a abertura é inicializado por `modo_inicial`, é estado de runtime e existe
uma única vez por instância da tela. A suspensão e o retorno à mesma instância
preservam esse estado; nova abertura ou recarga o reinicializam pelo valor
configurado. O estado vivo não é persistido de volta no JSON.
`dry_run_ativo` continua restrito ao estado de runtime da especialização focal
da ADR-0037 e não é configuração concreta universal.

O **registro de ações** é o contrato semântico da autoridade mantida junto à
implementação. Uma **ação registrada** declara a **categoria da ação** como
`processo`, `navegacao` ou `visualizacao`; uma ação de processo declara também
os **modos de execução aceitos**, somente entre `executar` e `dry_run`. Essa
autoridade implementacional da compatibilidade não pode ser inferida ou
contradita pelo JSON. Resolução ausente ou insuficiente é **falha fechada de
resolução**. Ação legada não classificada é inelegível para tela adotante.

A seleção múltipla do console (`ITEM-0006`, ADR-0034) é caso concreto de
estado de runtime: o conjunto de IDs estáveis selecionado nunca é persistido
no `tela.json` — apenas a política (`politica_selecao: multipla`) é
configuração concreta. Autoridade terminológica de seleção múltipla:
`docs/nomenclatura/32_CONSOLE.md`.

### 4.6 `perfil` como configuração concreta (ADR-0034)

`perfil` é um campo raiz opcional do `tela.json`, aditivo e compatível com
`tela.v1`. Declara a classe funcional da tela quando ela não é uma tela de
composição livre — por exemplo, `perfil: resultado_execucao` identifica a
tela padrão e reutilizável de resultado do `ITEM-0006`. `perfil` é
configuração concreta declarada antes da execução; não confundir com o
estado de visualização ou de seleção vivos durante a sessão (§4.5). Autoridade
comportamental completa: `contrato_tela_json.md` seção 34.

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `schema` × `configuração concreta` | Schema define estrutura e semântica (nos módulos proprietários; `docs/NOMENCLATURA.md` atua somente como fachada de compatibilidade e navegação); configuração concreta guarda os valores lidos pelo renderer (em `config/`) |
| `configuração concreta` × `estado de runtime` | Configuração é declarada antes da execução; estado é produzido e mantido durante a execução |
| motor compartilhado (`tela/`) × aplicação demonstrativa (`demo/`) | `tela/` é motor reutilizável; `demo/` é aplicação demonstrativa — não é segunda implementação de loader, modelo ou renderizador |
| tela demonstrativa × tela do produto real | Tela demonstrativa fica em `config/telas/demo/<id>.json`; tela do produto real fica em `config/telas/<id>.json` |
| `orquestrador.py` × `demo/demo.py` | Ponto de entrada futuro do produto real × ponto de entrada da demonstração atual |
| `controle_execucao` × modo corrente | Objeto raiz fechado de configuração concreta, com exatamente `modo_inicial` × estado de runtime único por instância, não persistido |
| contrato semântico do registro × arquitetura física | Regras de categoria, compatibilidade, resolução e falha fechada × localização e estrutura internas reversíveis, não decididas aqui |

## 6. Relação com contratos

- `contrato_tela_json.md`: autoridade do schema completo de `tela.json`.
- `contrato_estilo.md`: autoridade das regras de uso de `config/estilo.json`.

## 7. Relação com ADRs

- ADR-0008: modelo de configuração por tela; responsabilidade de cada artefato.
- ADR-0009: caminho, nomenclatura e formato dos JSONs de tela.
- ADR-0021: separação demo/produto real/motor; política de caminhos.
- ADR-0022: ponto de entrada real; tela inicial real; identidade `orquestrador`.
- ADR-0034: campo raiz `perfil`; seleção múltipla como estado de runtime.
- ADR-0040: distinção entre estado inicial declarado e modo corrente de runtime.
- ADR-0040: objeto fechado `controle_execucao` e autoridade implementacional
  do registro de ações.

## 8. Aliases ou termos descontinuados relacionados

Estados transitórios dos artefatos JSON estão classificados como conteúdo
histórico no `RELATORIO_HISTORICO_NOMENCLATURA_MONOLITICA.md`. Não são termos
ativos neste módulo.

## 9. Conteúdo que não pertence a este módulo

- Status transitórios de migração de artefatos JSON → relatório histórico.
- Caminhos de artefatos obsoletos (`layout_dado.json`, `layout_menu.json`) →
  relatório histórico.
- Regras de comportamento do renderer → contratos correspondentes.
- Definição de elementos funcionais → módulo `20` e módulos `30`-`34`.
- Vocabulário interno de estilo (campos, presets, indicadores, `tiling`,
  distinções semânticas de cor) → módulo `10_ESTILO.md`.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§0 (linhas 27-87)"
  intervalo_ou_bloco: "NOM-LEV-003, NOM-LEV-004"
origem_normativa: ADR-0008, ADR-0021, ADR-0022
contratos_relacionados:
  - contrato_tela_json.md
  - contrato_estilo.md
adrs_relacionadas:
  - ADR-0008
  - ADR-0009
  - ADR-0021
  - ADR-0022
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS: []
```
