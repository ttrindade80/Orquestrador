---
name: H-0030-catalogo-telas-utilizaveis
description: Handoff de implementação — catálogo de cinco telas permanentes navegáveis pelo lançador do orquestrador; console único, dashboard único, matrizes 2×2, 3×2 e 2×4
metadata:
  type: handoff
  status: proposto
  data: 2026-07-13
rastreabilidade:
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
  handoff_precedente: docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
  relatorio_precedente: docs/relatorios/RELATORIO_FECHAMENTO_MANUAL_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
  escopo_alteravel:
    - config/telas/h0030_console_unico.json
    - config/telas/h0030_dashboard_unico.json
    - config/telas/h0030_matriz_2x2.json
    - config/telas/h0030_matriz_3x2.json
    - config/telas/h0030_matriz_2x4.json
    - config/telas/orquestrador.json
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
    - tela/teste_demo.py
    - docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
  escopo_somente_leitura:
    - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_json_lancador.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_json_dashboard.md
    - docs/NOMENCLATURA.md
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/demo.py
    - config/telas/destino_minimo.json
    - config/telas/grupo_minimo.json
    - config/telas/stub_b.json
    - config/telas/h0029_dashboard_igual.json
    - config/telas/h0029_dashboard_fracao.json
    - config/telas/h0029_dashboard_percentual.json
    - config/telas/h0029_grupo_pai_distribuido.json
    - config/telas/h0029_grupo_igual.json
    - config/telas/h0029_grupo_fracao.json
    - config/telas/h0029_grupo_percentual.json
    - tela/teste_diagnostico.py
    - tela/teste_explorar_barra_de_menus.py
  relatorio_implementacao_esperado: docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
---

# H-0030 — Catálogo de telas utilizáveis

## Status

proposto

---

## 1. Objetivo

Criar cinco telas permanentes como fixtures de integração do projeto e integrá-las ao lançador do orquestrador:

1. Uma tela com **console único** (`h0030_console_unico`).
2. Uma tela com **dashboard único** (`h0030_dashboard_unico`).
3. Uma tela com **grupo matricial 2×2** (`h0030_matriz_2x2`).
4. Uma tela com **grupo matricial 3×2** (`h0030_matriz_3x2`).
5. Uma tela com **grupo matricial 2×4** (`h0030_matriz_2x4`).

As cinco telas devem:

- ser carregáveis diretamente pela pipeline `loader → modelo → renderizador` sem erros;
- ser navegáveis a partir do lançador do orquestrador via tecla de chip;
- possuir conteúdo determinístico e mínimo suficiente para verificação visual;
- ampliar a suíte automatizada com testes de carregamento, construção de modelo e renderização.

Este handoff **não** implementa código, **não** faz QA de si mesmo, **não** decide arquitetura nova, **não** completa lacunas normativas e **não** prepara commit. É uma ordem de trabalho fechada para o executor de implementação.

---

## 2. Estado comprovado anterior

```yaml
H-0029:
  commit: 9ae4aa4
  titulo: Distribuição de containers com cardinalidade unitária
  estado: fechado
  qa_handoff: H1_HANDOFF_APPROVED
  suite_canonica: 1449/1449
  telas_permanentes_h0029: 7
  telas_h0029_no_lancador: nao
```

Os sete arquivos `h0029_*.json` foram criados e validados nesse ciclo. Não foram integrados ao lançador do orquestrador — essa exclusão foi explícita no escopo do H-0029.

### 2.1 Verificação obrigatória antes de qualquer alteração

O executor deve executar:

```bash
git log -1 --oneline
git status --short
git diff --stat
git diff --check
git diff --cached --stat
```

Se qualquer arquivo em `scripts/tela/*.py` apresentar alteração rastreada inesperada, parar imediatamente com:

```text
BLOCKED_REPOSITORY_STATE
```

Alterações documentais (`scripts/docs/`) e arquivos não rastreados não constituem divergência.

---

## 3. Identificadores das telas

| Tela | `id` | Arquivo |
|---|---|---|
| Console único | `h0030_console_unico` | `config/telas/h0030_console_unico.json` |
| Dashboard único | `h0030_dashboard_unico` | `config/telas/h0030_dashboard_unico.json` |
| Matriz 2×2 | `h0030_matriz_2x2` | `config/telas/h0030_matriz_2x2.json` |
| Matriz 3×2 | `h0030_matriz_3x2` | `config/telas/h0030_matriz_3x2.json` |
| Matriz 2×4 | `h0030_matriz_2x4` | `config/telas/h0030_matriz_2x4.json` |

---

## 4. Arquivos da implementação

### 4.1 Arquivos a criar

```text
config/telas/h0030_console_unico.json
config/telas/h0030_dashboard_unico.json
config/telas/h0030_matriz_2x2.json
config/telas/h0030_matriz_3x2.json
config/telas/h0030_matriz_2x4.json
docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
```

### 4.2 Arquivos a modificar

```text
config/telas/orquestrador.json    — acrescentar 5 itens ao array lancador_principal.itens
tela/teste_loader.py              — acrescentar classe de testes para as 5 telas
tela/teste_modelo.py              — acrescentar classe de testes para as 5 telas
tela/teste_renderizador.py        — acrescentar classe de testes para as 5 telas
tela/teste_demo.py                — atualizar proporcionalmente ao catálogo H-0030 (ver seção 4.4)
```

### 4.3 Arquivos proibidos

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
docs/adr/
docs/contratos/
config/telas/destino_minimo.json
config/telas/grupo_minimo.json
config/telas/stub_b.json
config/telas/h0029_*.json
```

A modificação de `orquestrador.json` é restrita ao array `lancador_principal.itens`. Nenhum outro campo desse arquivo pode ser alterado.

### 4.4 Escopo autorizado em `tela/teste_demo.py`

A autorização de modificar `tela/teste_demo.py` é restrita às mudanças diretamente necessárias ao catálogo H-0030:

- atualizar snapshots do lançador afetados pelos cinco novos itens;
- atualizar expectativas relacionadas aos chips disponíveis;
- atualizar fluxos de subprocesso dependentes do orquestrador;
- acrescentar smoke tests do ponto de entrada real para os cinco chips novos;
- preservar os chips `d` e `g` existentes;
- preservar o retorno por Esc nas telas de destino;
- preservar a saída por Esc na raiz do orquestrador.

Não é autorizada refatoração geral de `tela/teste_demo.py`. Toda alteração deve ser proporcional e limitada ao que o catálogo H-0030 exige.

### 4.5 Separação entre restrições de autoria e restrições de implementação

As restrições aplicadas ao autor deste handoff durante sua criação não constituem arquivos proibidos para o executor da implementação.

A futura implementação pode alterar todos os arquivos nominalmente permitidos neste handoff quando isso for necessário para implementar, testar e demonstrar a capacidade aprovada.

A lista de arquivos proibidos na seção 4.3 é parte do escopo da implementação, não uma extensão das restrições de autoria. Nenhuma proibição desta seção deve tornar incompatíveis: a implementação solicitada; a suíte canônica; os critérios de aceite; os smoke tests; a demonstração prática.

---

## 5. Rótulos do lançador

| Chip | Texto | `tela_destino` | Comprimento |
|---|---|---|---|
| `1` | `Console` | `h0030_console_unico` | 7 ✓ |
| `2` | `Dashboard` | `h0030_dashboard_unico` | 9 ✓ |
| `3` | `Matriz 2x2` | `h0030_matriz_2x2` | 10 ✓ |
| `4` | `Matriz 3x2` | `h0030_matriz_3x2` | 10 ✓ |
| `5` | `Matriz 2x4` | `h0030_matriz_2x4` | 10 ✓ |

Todos os textos estão dentro do limite de 15 caracteres (contrato_lancador.md).

Os chips `d` e `g` já estão ocupados pelos itens `item_destino_minimo` e `item_grupo_minimo`. Os chips `1`–`5` estão livres.

---

## 6. Tela com console único

### 6.1 Especificação normativa

Arquivo: `config/telas/h0030_console_unico.json`

```json
{
  "schema": "tela.v1",
  "id": "h0030_console_unico",
  "cabecalho": {
    "titulo": "H-0030 Console",
    "descricao": "Catálogo — corpo com console único"
  },
  "corpo": {
    "arranjo": "vertical",
    "distribuicao": {
      "modo": "igual"
    },
    "elementos": [
      {
        "id": "console_catalogo",
        "tipo": "console",
        "titulo": "Console",
        "origem_dados": null,
        "itens": [],
        "politica_composicao": {
          "alinhamento": "esquerda",
          "overflow_normal": "truncar_com_reticencias"
        },
        "politica_navegacao": {
          "navegavel": false
        },
        "politica_selecao": "nenhuma",
        "politica_paginacao": "sem",
        "politica_exibicao": {
          "modo_inicial": "normal",
          "verboso": false
        }
      }
    ]
  },
  "barra_de_menus": {
    "distribuicao": {
      "modo": "horizontal_responsiva",
      "ordem": {
        "politica": "declaracao",
        "ancoras": {
          "primeiro": ["chip_esc"],
          "ultimo": ["chip_ajuda"]
        }
      },
      "tentativa_inicial": "linha_unica",
      "quebra": "multilinha_quando_nao_couber",
      "preenchimento_multilinha": "coluna_a_coluna",
      "preenchimentos_multilinha_suportados": ["coluna_a_coluna", "linha_a_linha"],
      "linhas": {
        "minimo": 1,
        "maximo": 2,
        "preferir_menor_numero": true
      },
      "alinhamento_linhas": "esquerda",
      "espacamentos": {
        "margem_horizontal": {"minimo": 1, "maximo": null},
        "vao_chip_texto": {"minimo": 1, "maximo": 3},
        "vao_entre_chips": {"minimo": 2, "maximo": 6},
        "vao_entre_colunas": {"minimo": 2, "maximo": 8},
        "vao_vertical_entre_linhas": {"minimo": 0, "maximo": 0}
      },
      "colunas": {
        "largura": "por_maior_item_da_coluna",
        "subcolunas": {
          "chip": {"alinhamento": "esquerda"},
          "texto": {"alinhamento": "esquerda"}
        }
      },
      "overflow": {
        "quando_nao_couber": "erro_layout",
        "nao_omitir_chips": true,
        "nao_truncar_texto": true,
        "nao_reordenar": true
      }
    },
    "chips": [
      {
        "id": "chip_esc",
        "tipo": "acao",
        "tecla": "Esc",
        "texto": "Voltar",
        "acao": {
          "tipo": "acao_contextual_esc",
          "nota": "Voltar na tela interna sem selecao ativa (contrato_barra_de_menus secao 9)"
        },
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "rotulo_dinamico"
      },
      {
        "id": "chip_ajuda",
        "tipo": "acao",
        "tecla": "?",
        "texto": "Ajuda",
        "acao": {"tipo": "abrir_ajuda"},
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "visivel_ativo"
      }
    ]
  }
}
```

### 6.2 Notas de implementação

- `origem_dados: null` e `itens: []` correspondem ao envelope mínimo do `contrato_json_console.md`.
- O console não é navegável e não possui seleção, paginação ou binding de dados.
- `corpo.distribuicao: {modo: "igual"}` com um único filho atribui toda a área disponível ao console.
- A `barra_de_menus` segue o padrão canônico de `destino_minimo.json` com `chip_esc` (`Esc` / `Voltar`) e `chip_ajuda` (`?` / `Ajuda`).

---

## 7. Tela com dashboard único

### 7.1 Especificação normativa

Arquivo: `config/telas/h0030_dashboard_unico.json`

```json
{
  "schema": "tela.v1",
  "id": "h0030_dashboard_unico",
  "cabecalho": {
    "titulo": "H-0030 Dashboard",
    "descricao": "Catálogo — corpo com dashboard único"
  },
  "corpo": {
    "arranjo": "vertical",
    "distribuicao": {
      "modo": "igual"
    },
    "elementos": [
      {
        "id": "dashboard_catalogo",
        "tipo": "dashboard",
        "titulo": "Dashboard",
        "campos": [
          {
            "id": "tipo_corpo",
            "rotulo": "Tipo",
            "fonte": "literal",
            "valor": "dashboard único"
          },
          {
            "id": "ciclo",
            "rotulo": "Ciclo",
            "fonte": "literal",
            "valor": "H-0030"
          }
        ]
      }
    ]
  },
  "barra_de_menus": "<<ESQUEMÁTICO — materializar integralmente a estrutura normativa da seção 6.1>>"
}
```

> **Nota:** O bloco `barra_de_menus` acima é esquemático, não é JSON copiável. O executor deve inserir integralmente a estrutura normativa definida na seção 6.1 em substituição a esse marcador. A semântica da barra de menus não é alterada.

### 7.2 Notas de implementação

- Usa `campos` com `fonte: "literal"` — o mesmo padrão de `destino_minimo.json` e `h0029_dashboard_igual.json`.
- `corpo.distribuicao: {modo: "igual"}` com um único filho atribui toda a área ao dashboard.
- A `barra_de_menus` deve ser **idêntica** à especificada na seção 6.1.

---

## 8. Matrizes permanentes

### 8.1 Regras gerais

Cada tela de matriz contém um único elemento no corpo: um `grupo` com `estrutura: "matriz"`. O corpo declara `distribuicao: {modo: "igual"}` para atribuir toda a área disponível ao grupo.

O `grupo` com `estrutura: "matriz"`:

- **não** pode conter o campo `arranjo` (proibido pelo contrato_composicao_corpo.md R-25);
- **deve** declarar `matriz.linhas.distribuicao` e `matriz.colunas.distribuicao` explicitamente (ADR-0020 D6 — ausência não equivale a `igual`);
- **deve** cobrir todas as células do grid com entradas em `matriz.celulas[]`;
- os `id`s referenciados em `celulas[].elemento` devem corresponder a elementos no array `elementos[]` do mesmo grupo.

Os filhos de cada célula são dashboards com `campos` e `fonte: "literal"` exibindo a posição (linha, coluna). O conteúdo determinístico torna o grid visualmente verificável sem binding externo.

### 8.2 Tela `h0030_matriz_2x2`

Arquivo: `config/telas/h0030_matriz_2x2.json`

Grid: 2 linhas × 2 colunas = 4 células.
Distribuição: `igual` em ambos os eixos.

```json
{
  "schema": "tela.v1",
  "id": "h0030_matriz_2x2",
  "cabecalho": {
    "titulo": "H-0030 Matriz 2x2",
    "descricao": "Catálogo — grupo matricial 2 linhas × 2 colunas"
  },
  "corpo": {
    "arranjo": "vertical",
    "distribuicao": {
      "modo": "igual"
    },
    "elementos": [
      {
        "id": "g_2x2",
        "tipo": "grupo",
        "estrutura": "matriz",
        "matriz": {
          "linhas": {
            "quantidade": 2,
            "distribuicao": {"modo": "igual"}
          },
          "colunas": {
            "quantidade": 2,
            "distribuicao": {"modo": "igual"}
          },
          "celulas": [
            {"linha": 1, "coluna": 1, "elemento": "l1c1"},
            {"linha": 1, "coluna": 2, "elemento": "l1c2"},
            {"linha": 2, "coluna": 1, "elemento": "l2c1"},
            {"linha": 2, "coluna": 2, "elemento": "l2c2"}
          ]
        },
        "elementos": [
          {
            "id": "l1c1",
            "tipo": "dashboard",
            "titulo": "L1 C1",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 1"}]
          },
          {
            "id": "l1c2",
            "tipo": "dashboard",
            "titulo": "L1 C2",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 2"}]
          },
          {
            "id": "l2c1",
            "tipo": "dashboard",
            "titulo": "L2 C1",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 1"}]
          },
          {
            "id": "l2c2",
            "tipo": "dashboard",
            "titulo": "L2 C2",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 2"}]
          }
        ]
      }
    ]
  },
  "barra_de_menus": "<<ESQUEMÁTICO — materializar integralmente a estrutura normativa da seção 6.1>>"
}
```

> **Nota:** O bloco `barra_de_menus` acima é esquemático, não é JSON copiável. O executor deve inserir integralmente a estrutura normativa definida na seção 6.1 em substituição a esse marcador. A semântica da barra de menus não é alterada.

### 8.3 Tela `h0030_matriz_3x2`

Arquivo: `config/telas/h0030_matriz_3x2.json`

Grid: 3 linhas × 2 colunas = 6 células.
Distribuição: `igual` em ambos os eixos.

```json
{
  "schema": "tela.v1",
  "id": "h0030_matriz_3x2",
  "cabecalho": {
    "titulo": "H-0030 Matriz 3x2",
    "descricao": "Catálogo — grupo matricial 3 linhas × 2 colunas"
  },
  "corpo": {
    "arranjo": "vertical",
    "distribuicao": {
      "modo": "igual"
    },
    "elementos": [
      {
        "id": "g_3x2",
        "tipo": "grupo",
        "estrutura": "matriz",
        "matriz": {
          "linhas": {
            "quantidade": 3,
            "distribuicao": {"modo": "igual"}
          },
          "colunas": {
            "quantidade": 2,
            "distribuicao": {"modo": "igual"}
          },
          "celulas": [
            {"linha": 1, "coluna": 1, "elemento": "l1c1"},
            {"linha": 1, "coluna": 2, "elemento": "l1c2"},
            {"linha": 2, "coluna": 1, "elemento": "l2c1"},
            {"linha": 2, "coluna": 2, "elemento": "l2c2"},
            {"linha": 3, "coluna": 1, "elemento": "l3c1"},
            {"linha": 3, "coluna": 2, "elemento": "l3c2"}
          ]
        },
        "elementos": [
          {
            "id": "l1c1",
            "tipo": "dashboard",
            "titulo": "L1 C1",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 1"}]
          },
          {
            "id": "l1c2",
            "tipo": "dashboard",
            "titulo": "L1 C2",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 2"}]
          },
          {
            "id": "l2c1",
            "tipo": "dashboard",
            "titulo": "L2 C1",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 1"}]
          },
          {
            "id": "l2c2",
            "tipo": "dashboard",
            "titulo": "L2 C2",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 2"}]
          },
          {
            "id": "l3c1",
            "tipo": "dashboard",
            "titulo": "L3 C1",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 3, coluna 1"}]
          },
          {
            "id": "l3c2",
            "tipo": "dashboard",
            "titulo": "L3 C2",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 3, coluna 2"}]
          }
        ]
      }
    ]
  },
  "barra_de_menus": "<<ESQUEMÁTICO — materializar integralmente a estrutura normativa da seção 6.1>>"
}
```

> **Nota:** O bloco `barra_de_menus` acima é esquemático, não é JSON copiável. O executor deve inserir integralmente a estrutura normativa definida na seção 6.1 em substituição a esse marcador. A semântica da barra de menus não é alterada.

### 8.4 Tela `h0030_matriz_2x4`

Arquivo: `config/telas/h0030_matriz_2x4.json`

Grid: 2 linhas × 4 colunas = 8 células.
Distribuição: `igual` em ambos os eixos.

```json
{
  "schema": "tela.v1",
  "id": "h0030_matriz_2x4",
  "cabecalho": {
    "titulo": "H-0030 Matriz 2x4",
    "descricao": "Catálogo — grupo matricial 2 linhas × 4 colunas"
  },
  "corpo": {
    "arranjo": "vertical",
    "distribuicao": {
      "modo": "igual"
    },
    "elementos": [
      {
        "id": "g_2x4",
        "tipo": "grupo",
        "estrutura": "matriz",
        "matriz": {
          "linhas": {
            "quantidade": 2,
            "distribuicao": {"modo": "igual"}
          },
          "colunas": {
            "quantidade": 4,
            "distribuicao": {"modo": "igual"}
          },
          "celulas": [
            {"linha": 1, "coluna": 1, "elemento": "l1c1"},
            {"linha": 1, "coluna": 2, "elemento": "l1c2"},
            {"linha": 1, "coluna": 3, "elemento": "l1c3"},
            {"linha": 1, "coluna": 4, "elemento": "l1c4"},
            {"linha": 2, "coluna": 1, "elemento": "l2c1"},
            {"linha": 2, "coluna": 2, "elemento": "l2c2"},
            {"linha": 2, "coluna": 3, "elemento": "l2c3"},
            {"linha": 2, "coluna": 4, "elemento": "l2c4"}
          ]
        },
        "elementos": [
          {
            "id": "l1c1",
            "tipo": "dashboard",
            "titulo": "L1 C1",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 1"}]
          },
          {
            "id": "l1c2",
            "tipo": "dashboard",
            "titulo": "L1 C2",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 2"}]
          },
          {
            "id": "l1c3",
            "tipo": "dashboard",
            "titulo": "L1 C3",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 3"}]
          },
          {
            "id": "l1c4",
            "tipo": "dashboard",
            "titulo": "L1 C4",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 1, coluna 4"}]
          },
          {
            "id": "l2c1",
            "tipo": "dashboard",
            "titulo": "L2 C1",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 1"}]
          },
          {
            "id": "l2c2",
            "tipo": "dashboard",
            "titulo": "L2 C2",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 2"}]
          },
          {
            "id": "l2c3",
            "tipo": "dashboard",
            "titulo": "L2 C3",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 3"}]
          },
          {
            "id": "l2c4",
            "tipo": "dashboard",
            "titulo": "L2 C4",
            "campos": [{"id": "pos", "rotulo": "Posição", "fonte": "literal", "valor": "linha 2, coluna 4"}]
          }
        ]
      }
    ]
  },
  "barra_de_menus": "<<ESQUEMÁTICO — materializar integralmente a estrutura normativa da seção 6.1>>"
}
```

> **Nota:** O bloco `barra_de_menus` acima é esquemático, não é JSON copiável. O executor deve inserir integralmente a estrutura normativa definida na seção 6.1 em substituição a esse marcador. A semântica da barra de menus não é alterada.

---

## 9. Integração no lançador

O arquivo `config/telas/orquestrador.json` deve ter os seguintes 5 itens acrescentados ao array `lancador_principal.itens`, após os dois itens existentes:

```json
{
  "id": "item_console_unico",
  "chip": "1",
  "texto": "Console",
  "tela_destino": "h0030_console_unico"
},
{
  "id": "item_dashboard_unico",
  "chip": "2",
  "texto": "Dashboard",
  "tela_destino": "h0030_dashboard_unico"
},
{
  "id": "item_matriz_2x2",
  "chip": "3",
  "texto": "Matriz 2x2",
  "tela_destino": "h0030_matriz_2x2"
},
{
  "id": "item_matriz_3x2",
  "chip": "4",
  "texto": "Matriz 3x2",
  "tela_destino": "h0030_matriz_3x2"
},
{
  "id": "item_matriz_2x4",
  "chip": "5",
  "texto": "Matriz 2x4",
  "tela_destino": "h0030_matriz_2x4"
}
```

Após a implementação, `lancador_principal.itens` deve conter exatamente 7 itens na ordem:

1. `item_destino_minimo` (chip `d`) — pré-existente, não alterar
2. `item_grupo_minimo` (chip `g`) — pré-existente, não alterar
3. `item_console_unico` (chip `1`) — novo
4. `item_dashboard_unico` (chip `2`) — novo
5. `item_matriz_2x2` (chip `3`) — novo
6. `item_matriz_3x2` (chip `4`) — novo
7. `item_matriz_2x4` (chip `5`) — novo

Nenhum outro campo de `orquestrador.json` pode ser alterado.

---

## 10. Demonstração prática

`demo.py` não possui argumento de linha de comando para selecionar a tela inicial. As formas de demonstração são:

### 10.1 Navegação pelo lançador (recomendada após integração)

```bash
cd scripts
python3 tela/demo.py
# Na tela do orquestrador, pressionar a tecla de chip:
#   1 → h0030_console_unico
#   2 → h0030_dashboard_unico
#   3 → h0030_matriz_2x2
#   4 → h0030_matriz_3x2
#   5 → h0030_matriz_2x4
#   Esc → Sair
# Em qualquer tela de destino:
#   Esc → voltar ao orquestrador
```

### 10.2 Acesso direto por monkeypatch (TTY completo)

O mecanismo foi documentado e validado no H-0029 via achado QA-POS-H0029-001. A função `criar_estado_inicial` do módulo `tela.demo` deve ser sobrescrita **antes** de chamar `_d.main()`. O estado é construído diretamente no lambda; a função original não deve ser chamada.

```python
import sys
sys.path.insert(0, "scripts")
import tela.demo as _d

_d.criar_estado_inicial = lambda: {
    "tipo_borda": "curva",
    "saindo": False,
    "tela_atual": "h0030_console_unico",
    "pilha_telas": []
}
_d.main()
```

Substituir `"h0030_console_unico"` pelo `id` da tela desejada.

### 10.3 Renderização estática (pipeline direta, sem TUI)

```bash
cd scripts
python3 -c "
import sys, shutil
sys.path.insert(0, '.')
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
w = shutil.get_terminal_size().columns
m = construir_modelo(carregar_tela(None, 'h0030_console_unico'))
print(renderizar_tela(m, tipo_borda='curva', largura=w), end='')
"
```

Substituir `'h0030_console_unico'` pelo `id` da tela desejada.

---

## 11. Fixtures permanentes

As cinco telas são fixtures permanentes de integração do projeto. Após a implementação deste ciclo, não devem ser alteradas, renomeadas ou removidas:

| Arquivo | Propósito |
|---|---|
| `h0030_console_unico.json` | Fixture de console único — tipo funcional mínimo verificável |
| `h0030_dashboard_unico.json` | Fixture de dashboard único — tipo funcional mínimo verificável |
| `h0030_matriz_2x2.json` | Fixture de grade 2×2 — matriz de menor dimensão |
| `h0030_matriz_3x2.json` | Fixture de grade 3×2 — expansão vertical do grid |
| `h0030_matriz_2x4.json` | Fixture de grade 2×4 — expansão horizontal ao limite superior |

---

## 12. Preservações

Os seguintes arquivos são de leitura obrigatória e não devem ser modificados durante este ciclo:

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
config/telas/destino_minimo.json
config/telas/grupo_minimo.json
config/telas/stub_b.json
config/telas/h0029_dashboard_igual.json
config/telas/h0029_dashboard_fracao.json
config/telas/h0029_dashboard_percentual.json
config/telas/h0029_grupo_pai_distribuido.json
config/telas/h0029_grupo_igual.json
config/telas/h0029_grupo_fracao.json
config/telas/h0029_grupo_percentual.json
docs/adr/
docs/contratos/
```

---

## 13. Condições de bloqueio

| Condição | Código de parada |
|---|---|
| Qualquer arquivo `tela/*.py` apresentar diff rastreado antes da implementação | `BLOCKED_REPOSITORY_STATE` |
| Qualquer arquivo `h0030_*.json` já existir em `config/telas/` | `BLOCKED_FILE_EXISTS` |
| Existir outro handoff ou outro artefato ativo com o identificador `H-0030` concorrente, excluindo `docs/handoff/H-0030-catalogo-telas-utilizaveis.md`, os relatórios do ciclo H-0030 e as fixtures `h0030_*` | `BLOCKED_ID_CONFLICT` |
| A suíte canônica apresentar falha antes de qualquer alteração | `BLOCKED_SUITE_FAILING` |

---

## 14. Critérios de aceite automatizados

### 14.1 Carregamento

| Verificação | Script |
|---|---|
| `carregar_tela(None, "h0030_console_unico")` não lança exceção | `teste_loader.py` |
| `carregar_tela(None, "h0030_dashboard_unico")` não lança exceção | `teste_loader.py` |
| `carregar_tela(None, "h0030_matriz_2x2")` não lança exceção | `teste_loader.py` |
| `carregar_tela(None, "h0030_matriz_3x2")` não lança exceção | `teste_loader.py` |
| `carregar_tela(None, "h0030_matriz_2x4")` não lança exceção | `teste_loader.py` |

### 14.2 Construção de modelo

| Verificação | Script |
|---|---|
| `construir_modelo(tela)` não lança exceção para cada uma das 5 telas | `teste_modelo.py` |

### 14.3 Renderização

| Verificação | Script |
|---|---|
| `renderizar_tela(modelo, tipo_borda="curva", largura=80)` não lança exceção para cada tela | `teste_renderizador.py` |
| O resultado não é `None` e não é string vazia | `teste_renderizador.py` |
| Para `h0030_matriz_2x2`: a saída contém 4 regiões de dashboard (L1C1, L1C2, L2C1, L2C2) | `teste_renderizador.py` |
| Para `h0030_matriz_3x2`: a saída contém 6 regiões de dashboard | `teste_renderizador.py` |
| Para `h0030_matriz_2x4`: a saída contém 8 regiões de dashboard | `teste_renderizador.py` |

### 14.3-G Verificações geométricas das matrizes

Os testes a seguir verificam propriedades estruturais ou geométricas observáveis na saída renderizada com dimensões de terminal determinísticas (`largura=80`, altura correspondente ao grid). Não substituem validação visual humana, mas tornam defeitos geométricos detectáveis automaticamente. Não devem introduzir algoritmo novo de matriz.

**`h0030_matriz_2x2` (2 linhas × 2 colunas)**

| Verificação | Script |
|---|---|
| A saída renderizada possui exatamente 2 linhas de conteúdo de célula | `teste_renderizador.py` |
| A saída possui exatamente 2 colunas (2 dashboards por linha) | `teste_renderizador.py` |
| A grade cobre todas as 4 células sem lacuna e sem célula duplicada | `teste_renderizador.py` |
| Cada célula exibe o rótulo de posição declarado no JSON | `teste_renderizador.py` |
| A divisória vertical central aparece na saída (caractere de borda presente) | `teste_renderizador.py` |
| A divisória horizontal central aparece na saída | `teste_renderizador.py` |
| Não há sobreposição entre regiões de célula vizinhas | `teste_renderizador.py` |
| Com `largura=120`, a renderização também não lança exceção e mantém 4 regiões | `teste_renderizador.py` |

**`h0030_matriz_3x2` (3 linhas × 2 colunas)**

| Verificação | Script |
|---|---|
| A saída possui exatamente 3 linhas de conteúdo de célula | `teste_renderizador.py` |
| A saída possui exatamente 2 colunas por linha | `teste_renderizador.py` |
| A grade cobre todas as 6 células sem lacuna e sem célula duplicada | `teste_renderizador.py` |
| Cada célula exibe o rótulo de posição declarado no JSON | `teste_renderizador.py` |
| Divisórias verticais e horizontais presentes na saída | `teste_renderizador.py` |
| Não há sobreposição entre regiões vizinhas | `teste_renderizador.py` |
| Com `largura=120`, a renderização não lança exceção e mantém 6 regiões | `teste_renderizador.py` |

**`h0030_matriz_2x4` (2 linhas × 4 colunas)**

| Verificação | Script |
|---|---|
| A saída possui exatamente 2 linhas de conteúdo de célula | `teste_renderizador.py` |
| A saída possui exatamente 4 colunas por linha | `teste_renderizador.py` |
| A grade cobre todas as 8 células sem lacuna e sem célula duplicada | `teste_renderizador.py` |
| Cada célula exibe o rótulo de posição declarado no JSON | `teste_renderizador.py` |
| Três divisórias verticais e uma horizontal presentes na saída | `teste_renderizador.py` |
| Não há sobreposição entre regiões vizinhas | `teste_renderizador.py` |
| Com `largura=120`, a renderização não lança exceção e mantém 8 regiões | `teste_renderizador.py` |

### 14.4 Integração no lançador

| Verificação | Script |
|---|---|
| `orquestrador.json` possui exatamente 7 itens em `lancador_principal.itens` | `teste_loader.py` |
| Os 5 valores `tela_destino` novos resolvem para arquivos existentes em `config/telas/` | `teste_loader.py` |
| Os chips `1`–`5` não conflitam com os chips preexistentes `d` e `g` | `teste_loader.py` |
| Todos os `texto` dos 7 itens possuem comprimento ≤ 15 | `teste_loader.py` |

### 14.5 Baseline da suíte

| Verificação | Evidência |
|---|---|
| Suíte canônica ≥ 1449 verificações após a implementação | execução direta dos 6 scripts |
| Código de saída 0 em todos os 6 scripts | execução direta dos 6 scripts |

### 14.6 Smoke tests do ponto de entrada real (`tela/demo.py`)

Os critérios abaixo devem ser verificados em `tela/teste_demo.py`. O caminho real pelo lançador não pode depender exclusivamente de monkeypatch; o monkeypatch pode ser usado como técnica complementar ou de execução focal, mas não como substituto da demonstração real.

**Ciclo completo por chip (para cada um dos cinco chips novos)**

| Verificação | Script |
|---|---|
| Chip `1` abre `h0030_console_unico`: ciclo orquestrador → chip `1` → tela correta → Esc → retorno ao orquestrador | `teste_demo.py` |
| Chip `2` abre `h0030_dashboard_unico`: ciclo completo orquestrador → chip `2` → tela correta → Esc → retorno | `teste_demo.py` |
| Chip `3` abre `h0030_matriz_2x2`: ciclo completo orquestrador → chip `3` → tela correta → Esc → retorno | `teste_demo.py` |
| Chip `4` abre `h0030_matriz_3x2`: ciclo completo orquestrador → chip `4` → tela correta → Esc → retorno | `teste_demo.py` |
| Chip `5` abre `h0030_matriz_2x4`: ciclo completo orquestrador → chip `5` → tela correta → Esc → retorno | `teste_demo.py` |

**Preservação dos fluxos existentes**

| Verificação | Script |
|---|---|
| Chip `d` continua abrindo `destino_minimo` | `teste_demo.py` |
| Chip `g` continua abrindo `grupo_minimo` | `teste_demo.py` |
| Destino incorreto não é aberto para nenhum chip | `teste_demo.py` |
| Esc no orquestrador encerra o sistema com o código de saída esperado | `teste_demo.py` |
| Cada execução de ciclo termina com código de saída esperado | `teste_demo.py` |

---

## 15. Critérios de validação manual futura

A validação manual deve ser executada pelo usuário após aprovação automatizada.

### 15.1 Console único

| Verificação | Esperado |
|---|---|
| `h0030_console_unico` carrega no demo via chip `1` | sim |
| Console vazio renderiza com bordas visíveis | sim |
| Console ocupa toda a altura disponível acima da barra de menus | sim |
| `barra_de_menus` está na última linha da tela | sim |
| `Esc` retorna ao orquestrador sem erros | sim |

### 15.2 Dashboard único

| Verificação | Esperado |
|---|---|
| `h0030_dashboard_unico` carrega no demo via chip `2` | sim |
| Dashboard ocupa toda a altura disponível acima da barra de menus | sim |
| Campos `Tipo` (`dashboard único`) e `Ciclo` (`H-0030`) estão visíveis | sim |
| `Esc` retorna ao orquestrador sem erros | sim |

### 15.3 Matrizes

| Verificação | Esperado |
|---|---|
| `h0030_matriz_2x2` carrega no demo via chip `3` | sim |
| Grid 2×2 visível com bordas em todas as interseções | sim |
| Cada célula exibe seu rótulo de posição (ex.: "linha 1, coluna 1") | sim |
| Não há lacunas nem sobreposições entre células | sim |
| `h0030_matriz_3x2` carrega no demo via chip `4` | sim |
| Grid 3×2 visível com 3 linhas e 2 colunas | sim |
| `h0030_matriz_2x4` carrega no demo via chip `5` | sim |
| Grid 2×4 visível com 2 linhas e 4 colunas | sim |
| `Esc` retorna ao orquestrador em todas as matrizes | sim |

### 15.4 Lançador do orquestrador

| Verificação | Esperado |
|---|---|
| O lançador do orquestrador exibe os 7 itens após a implementação | sim |
| Os chips `1`–`5` respondem à tecla pressionada e abrem a tela correta | sim |
| Os chips `d` e `g` continuam funcionando sem regressão | sim |
| `Esc` no orquestrador continua saindo do sistema | sim |

---

## 16. Relatório de implementação esperado

O executor deve produzir `docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md` usando `docs/templates/TEMPLATE_RELATORIO_IMPL.md`.

O relatório deve ser factual e não pode autoaprovar formalmente a implementação.

O relatório deve incluir os seguintes campos separados:

### 16.1 Identificação e estado inicial

1. Identificação do ciclo e hash do commit-base verificado.
2. Lista de verificação do estado anterior (repositório limpo antes de qualquer alteração).

### 16.2 Arquivos e telas

3. **Arquivos criados** — lista nominal de cada arquivo criado com seu caminho completo.
4. **Arquivos modificados** — lista nominal de cada arquivo modificado com seu caminho completo.
5. Para cada tela criada, campo separado com: identificador (`id`), nome do arquivo, rótulo exibido no lançador, chip associado e `tela_destino`.
6. Ordem final dos itens do lançador em `lancador_principal.itens` após a implementação (7 itens numerados).

### 16.3 Demonstração e testes

7. Mecanismo de demonstração utilizado (navegação pelo lançador ou monkeypatch) e resultado observado para cada chip `1`–`5`.
8. Smoke tests do `demo.py`: resultado de cada verificação da seção 14.6, por script.
9. Fixtures permanentes criadas neste ciclo: lista e propósito de cada uma.
10. Testes executados: nome de cada script e quantidade de verificações.
11. Resultados por script da suíte canônica: código de saída e contagem de verificações.
12. Quantidade total de verificações após a implementação.

### 16.4 Preservações, limitações e estado final

13. Confirmação de preservação dos chips `d` (`destino_minimo`) e `g` (`grupo_minimo`).
14. Confirmação de preservação das sete telas `h0029_*` sem alteração.
15. Demais preservações exigidas pelo handoff (loader, modelo, renderizador, demo.py, testes existentes não cobertos por este ciclo).
16. Limitações conhecidas da implementação.
17. Ressalvas sobre cobertura automatizada ou comportamentos não verificados.
18. Validação manual pendente (itens da seção 15 não executados automaticamente).
19. Estado Git ao final: saída de `git status --short` e `git diff --stat`.
20. Arquivos não rastreados presentes ao final.

---

## 17. Lista nominal acumulável

### 17.1 Arquivos deste ciclo

```text
config/telas/h0030_console_unico.json
config/telas/h0030_dashboard_unico.json
config/telas/h0030_matriz_2x2.json
config/telas/h0030_matriz_3x2.json
config/telas/h0030_matriz_2x4.json
config/telas/orquestrador.json
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
docs/relatorios/IMP-0030-catalogo-telas-utilizaveis.md
docs/handoff/H-0030-catalogo-telas-utilizaveis.md
```

### 17.2 Fixtures permanentes ativos de ciclos anteriores

```text
config/telas/destino_minimo.json
config/telas/grupo_minimo.json
config/telas/stub_b.json
config/telas/h0029_dashboard_igual.json
config/telas/h0029_dashboard_fracao.json
config/telas/h0029_dashboard_percentual.json
config/telas/h0029_grupo_pai_distribuido.json
config/telas/h0029_grupo_igual.json
config/telas/h0029_grupo_fracao.json
config/telas/h0029_grupo_percentual.json
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
```

---

## 18. Rastreamento de achados QA

Achados formais do relatório `RELATORIO_QA_H-0030_HANDOFF.md` tratados neste patch:

| ID | Severidade | Tratamento |
|---|---|---|
| QA-H0030-BLOQ-001 | bloqueante | `tela/teste_demo.py` autorizado e exigido; escopo limitado ao catálogo H-0030 (seções 4.2, 4.4, 14.6) |
| QA-H0030-ALTO-001 | alto | Smoke tests do ponto de entrada real adicionados na seção 14.6 |
| QA-H0030-MEDIO-001 | médio | Verificações geométricas das matrizes adicionadas na seção 14.3-G |
| QA-H0030-MEDIO-002 | médio | Condição BLOCKED_ID_CONFLICT corrigida na seção 13 para excluir o próprio handoff e ciclo H-0030 |
| QA-H0030-BAIXO-001 | baixo | Placeholders JSON nas seções 7.1, 8.2, 8.3 e 8.4 substituídos por marcadores esquemáticos explícitos com nota de materialização |
| QA-H0030-BAIXO-002 | baixo | Seção 16 expandida com campos factuais separados (seções 16.1–16.4) |
| QA-H0030-OBS-001 | observação | Não exige alteração de conteúdo no handoff; registrado apenas |
