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

## 4. Definições

### 4.1 Responsabilidade de cada artefato (ADR-0008)

| Artefato | Responsabilidade |
|---|---|
| `docs/NOMENCLATURA.md` | No antigo monólito, substituído pela fachada na fase 2 da ADR-0029, este artefato era responsável por schema e semântica: quais campos existem, o que cada um significa, tipo, restrições e como o renderer deve interpretá-los. Atualmente `docs/NOMENCLATURA.md` atua somente como fachada de compatibilidade e navegação; a autoridade terminológica vigente está nos módulos proprietários. |
| `config/estilo.json` | Biblioteca global de aparência: presets de borda, chip, indicadores e demais parâmetros gerais de aparência. Não declara tela, conteúdo, composição, destino, ação, item de `lancador` nem instância de `dashboard`. |
| `tela.json` (JSON próprio de cada tela) | Declaração concreta da tela: composição do corpo, instâncias de `console`, `dashboard`, `lancador` e `barra_de_menus`, listas de itens, chips, destinos, ações registradas, regras de existência/ativo-inativo, parâmetros visuais locais, bindings, filtros e regras de exibição. Não é código executável. Não guarda estado de runtime. |

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

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `schema` × `configuração concreta` | Schema define estrutura e semântica (nos módulos proprietários; `docs/NOMENCLATURA.md` atua somente como fachada de compatibilidade e navegação); configuração concreta guarda os valores lidos pelo renderer (em `config/`) |
| `configuração concreta` × `estado de runtime` | Configuração é declarada antes da execução; estado é produzido e mantido durante a execução |
| motor compartilhado (`tela/`) × aplicação demonstrativa (`demo/`) | `tela/` é motor reutilizável; `demo/` é aplicação demonstrativa — não é segunda implementação de loader, modelo ou renderizador |
| tela demonstrativa × tela do produto real | Tela demonstrativa fica em `config/telas/demo/<id>.json`; tela do produto real fica em `config/telas/<id>.json` |
| `orquestrador.py` × `demo/demo.py` | Ponto de entrada futuro do produto real × ponto de entrada da demonstração atual |

## 6. Relação com contratos

- `contrato_tela_json.md`: autoridade do schema completo de `tela.json`.
- `contrato_estilo.md`: autoridade das regras de uso de `config/estilo.json`.

## 7. Relação com ADRs

- ADR-0008: modelo de configuração por tela; responsabilidade de cada artefato.
- ADR-0009: caminho, nomenclatura e formato dos JSONs de tela.
- ADR-0021: separação demo/produto real/motor; política de caminhos.
- ADR-0022: ponto de entrada real; tela inicial real; identidade `orquestrador`.

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
