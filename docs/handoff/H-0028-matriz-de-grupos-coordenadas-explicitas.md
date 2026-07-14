---
name: H-0028-matriz-de-grupos-coordenadas-explicitas
description: Handoff de implementacao — estrutura matriz para o no grupo; grade bidimensional compartilhada com coordenadas explicitas; distribuicoes obrigatorias e independentes por eixo; validacao deterministica pelo loader; renderizacao por grade comum; compatibilidade retroativa integral com livre
metadata:
  type: handoff
  status: proposto
  data: 2026-07-12
rastreabilidade:
  adrs_base:
    - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  contratos_aplicaveis:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
  handoff_precedente: docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
  relatorio_precedente: docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
  escopo_alteravel:
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
    - docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md
  escopo_somente_leitura:
    - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
    - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
    - docs/adr/INDICE_ADR.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/NOMENCLATURA.md
    - config/telas/orquestrador.json
    - config/telas/grupo_minimo.json
    - config/telas/destino_minimo.json
    - config/telas/stub_b.json
  relatorio_implementacao_esperado: docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md
---

# H-0028 — Matriz declarativa de grupos com coordenadas explícitas

## Status

proposto

---

## 1. Identificação

| Campo | Valor |
|---|---|
| Identificador | H-0028 |
| Status | proposto |
| Data | 2026-07-12 |
| ADR base | ADR-0020 (aceita, 2026-07-12) |
| Ciclo anterior fechado | H-0027 / IMP-0028 |
| Relatório esperado | IMP-0029 |
| Commit-base | `f00b0bb` |

Este handoff **não** implementa código, **não** faz QA de si mesmo, **não** decide arquitetura nova fora do escopo das decisões D1–D16 da ADR-0020, **não** completa lacunas normativas e **não** prepara commit. É uma ordem de trabalho fechada para o executor de implementação.

---

## 2. Estado comprovado

```yaml
H-0026:
  commit: 40015b6
  estado: fechado

H-0027:
  commit: c003f3e
  estado: fechado
  qa_handoff: H1_HANDOFF_APPROVED
  qa_implementacao: I1_IMPLEMENTATION_APPROVED
  testes: 1004/1004

ADR-0020:
  titulo: Matriz declarativa de grupos com coordenadas explicitas
  status_no_arquivo: aceita
  status_no_indice: aceita
  qa_inicial: ADR_REJECTED
  achado_inicial: ACH-001
  patch: PATCH_ADR_CONCLUIDO
  qa_pos_patch: ADR_APPROVED_WITH_NOTES
  aplicacao: ADR_APPLICATION_COMPLETED
  qa_aplicacao: ADR_APPLICATION_APPROVED
  base_documental: aprovada
```

A rejeição inicial (`ADR_REJECTED`) é parte do histórico. O `ACH-001` (ambiguidade na semântica de ausência de distribuição nos eixos matriciais) foi resolvido pelo patch da D6 e propagado para todos os contratos afetados. As distribuições `matriz.linhas.distribuicao` e `matriz.colunas.distribuicao` são obrigatórias, explícitas e independentes.

A observação `OBS-001` do QA da aplicação (divergência de status da ADR-0018 entre arquivo e índice) é pendência histórica externa. Não representa risco para esta implementação.

### 2.1 Verificação obrigatória no início da implementação

O executor deve executar antes de qualquer alteração:

```bash
git log -1 --oneline
git status --short
git diff --stat
git diff --check
git diff --cached --stat
```

Se qualquer arquivo de `scripts/tela/*.py` apresentar alteração rastreada inesperada, parar com:

```text
BLOCKED_REPOSITORY_STATE
```

Alterações documentais (arquivos em `scripts/docs/`) e arquivos não rastreados não constituem divergência.

---

## 3. Autoridades

O executor deve ler integralmente antes de iniciar:

| Documento | Caminho relativo à raiz Git |
|---|---|
| ADR-0020 (autoridade primária) | `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` |
| ADR-0015 (composição, maiores restos) | `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` |
| ADR-0018 (ausência de distribuição) | `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` |
| ADR-0019 (profundidade, 3 níveis) | `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` |
| Contrato de composição de corpo | `scripts/docs/contratos/contrato_composicao_corpo.md` |
| Contrato tela JSON | `scripts/docs/contratos/contrato_tela_json.md` |
| Contrato JSON tela mínima | `scripts/docs/contratos/contrato_json_tela_minima.md` |
| Nomenclatura | `scripts/docs/NOMENCLATURA.md` |

Leitura complementar:

| Documento |
|---|
| `scripts/docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` |
| `scripts/docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md` |
| `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md` |

---

## 4. Objetivo

Implementar o comportamento `estrutura: "matriz"` para o nó `grupo`, conforme decidido pela ADR-0020 (D1–D16), extendendo os módulos `loader`, `modelo` e `renderizador` sem substituir nem degradar o comportamento `livre` existente.

O resultado deve permitir que um grupo declare uma grade bidimensional compartilhada:

```json
{
  "id": "g_2x4",
  "tipo": "grupo",
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": 2,
      "distribuicao": {"modo": "fracao", "valores": [1, 2]}
    },
    "colunas": {
      "quantidade": 4,
      "distribuicao": {"modo": "fracao", "valores": [1, 2, 1, 2]}
    },
    "celulas": [
      {"linha": 1, "coluna": 1, "elemento": "a"},
      {"linha": 1, "coluna": 2, "elemento": "b"},
      {"linha": 1, "coluna": 3, "elemento": "c"},
      {"linha": 1, "coluna": 4, "elemento": "d"},
      {"linha": 2, "coluna": 1, "elemento": "e"},
      {"linha": 2, "coluna": 2, "elemento": "f"},
      {"linha": 2, "coluna": 3, "elemento": "g"},
      {"linha": 2, "coluna": 4, "elemento": "h"}
    ]
  },
  "elementos": [
    {"id": "a", "tipo": "console"}, {"id": "b", "tipo": "dashboard"},
    {"id": "c", "tipo": "console"}, {"id": "d", "tipo": "lancador"},
    {"id": "e", "tipo": "console"}, {"id": "f", "tipo": "console"},
    {"id": "g", "tipo": "dashboard"}, {"id": "h", "tipo": "console"}
  ]
}
```

O renderer deve produzir duas faixas horizontais (com proporção 1:2) e quatro faixas verticais (com proporção 1:2:1:2). Todas as células da mesma coluna compartilham a mesma coordenada vertical; todas as células da mesma linha compartilham a mesma coordenada horizontal.

---

## 5. Problema funcional

O comportamento atual do nó `grupo` é inteiramente unidimensional:

- cada container declara `arranjo` local (`vertical` ou `horizontal`);
- cada container distribui área somente entre seus filhos diretos;
- grupos irmãos calculam divisões independentemente;
- o alinhamento de bordas entre grupos irmãos depende de coincidências (mesma distribuição, mesmas dimensões, mesma assinatura de restrições — ADR-0015 D14);
- não existe grade bidimensional compartilhada;
- não existe seletor declarativo de comportamento estrutural.

O novo caso de uso requer que todas as células de uma composição bidimensional compartilhem as mesmas coordenadas de linhas e colunas, garantindo alinhamento determinístico das bordas, independentemente de coincidências entre distribuições independentes.

---

## 6. Escopo positivo

### 6.1 Módulo loader (`scripts/tela/loader.py`)

Estender `_validar_grupo` para reconhecer e validar `estrutura: "matriz"`.

### 6.2 Módulo modelo (`scripts/tela/modelo.py`)

Estender `_construir_elementos_recursivo` para transportar corretamente `estrutura` e `matriz` nas `_campos_inertes` do `ElementoCorpo` do tipo `grupo`. Nenhum campo novo em `ElementoCorpo` é necessário.

### 6.3 Módulo renderizador (`scripts/tela/renderizador.py`)

Adicionar `_renderizar_container_matriz` e estender `_renderizar_container` e seus chamadores internos para detectar e despachar o comportamento matricial.

### 6.4 Testes (`scripts/tela/teste_loader.py`, `teste_modelo.py`, `teste_renderizador.py`)

Criar novas classes de teste para cobrir o schema matricial, validações, modelo e renderização. Testes existentes não podem ser alterados, exceto se forem snapshot tests que precisem ser atualizados como consequência direta da feature aprovada — nesse caso, a atualização deve ser documentada no IMP-0029.

---

## 7. Escopo negativo

Não implementar neste handoff:

- células vazias, placeholders ou preenchimento automático;
- `rowspan`, `colspan` ou mesclagem;
- dimensões abaixo de 2 ou acima de 4;
- novo tipo funcional;
- mudança de navegação (chips, `[✥]`, `[⇆]`);
- mudança interna de `console`, `lancador` ou `dashboard`;
- paginação de matriz;
- rolagem de matriz;
- truncamento específico por célula;
- redução automática de dimensões quando área insuficiente;
- política numérica nova de tamanho mínimo por célula;
- correção da divergência de status da ADR-0018;
- alteração de contratos, ADRs, nomenclatura ou índice;
- alteração de JSON ativo (orquestrador, grupo_minimo, destino_minimo, stub_b);
- refatoração ampla sem vínculo direto com a matriz;
- sincronização explícita entre containers distintos (`matriz`–`livre` ou `matriz`–`matriz` irmãos).

---

## 8. Arquivos permitidos para implementação

| Arquivo (relativo à raiz Git) | Tipo de alteração permitida |
|---|---|
| `scripts/tela/loader.py` | Estender `_validar_grupo`; adicionar funções auxiliares de validação de matriz |
| `scripts/tela/modelo.py` | Estender `_construir_elementos_recursivo` para grupo matricial, se necessário |
| `scripts/tela/renderizador.py` | Adicionar `_renderizar_container_matriz`; estender `_renderizar_container`; atualizar chamadores internos de grupo |
| `scripts/tela/teste_loader.py` | Adicionar nova classe de teste de validação matricial |
| `scripts/tela/teste_modelo.py` | Adicionar nova classe de teste de modelo matricial |
| `scripts/tela/teste_renderizador.py` | Adicionar nova classe de teste de renderização matricial |
| `scripts/docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md` | Criar (relatório de implementação) |

**Total: 6 arquivos existentes alteráveis + 1 arquivo novo.**

Se um arquivo fora desta lista precisar ser alterado, parar com:

```text
ARCHITECTURE_REVIEW_REQUIRED
```

---

## 9. Arquivos proibidos

Nenhuma alteração é permitida nos arquivos abaixo:

- `scripts/tela/demo.py`
- `scripts/tela/diagnostico.py`
- `scripts/tela/teste_demo.py`
- `scripts/tela/teste_diagnostico.py`
- `scripts/tela/teste_explorar_barra_de_menus.py`
- `scripts/tela/explorar_barra_de_menus.py`
- `scripts/tela/__init__.py`
- `scripts/config/telas/orquestrador.json`
- `scripts/config/telas/grupo_minimo.json`
- `scripts/config/telas/destino_minimo.json`
- `scripts/config/telas/stub_b.json`
- `scripts/config/estilo.json`
- `scripts/config/lancador.json`
- `scripts/config/barra_de_menus.json`
- `scripts/config/cabecalho.json`
- `scripts/docs/adr/*.md` (todos)
- `scripts/docs/contratos/*.md` (todos)
- `scripts/docs/NOMENCLATURA.md`
- Qualquer relatório existente em `scripts/docs/relatorios/`

---

## 10. Leitura obrigatória para implementação

Antes de escrever qualquer linha de código, o executor deve ler:

1. `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` — decisões D1–D16 completas
2. `scripts/docs/contratos/contrato_composicao_corpo.md` — seções 3.3, 5.13–5.24, R-25–R-32
3. `scripts/tela/loader.py` — funções `_validar_grupo`, `_validar_distribuicao_corpo`, exceções
4. `scripts/tela/modelo.py` — dataclass `ElementoCorpo`, `_construir_elementos_recursivo`
5. `scripts/tela/renderizador.py` — funções `_renderizar_container`, `_renderizar_container_horizontal`, `_renderizar_container_vertical`, `_distribuir_alturas`, `_distribuir_larguras`, `_pesos_distribuicao`
6. `scripts/tela/teste_loader.py` — estrutura da classe de testes para loader
7. `scripts/tela/teste_renderizador.py` — estrutura das classes de testes de renderização
8. `scripts/docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md` — precedente imediato

---

## 11. Comportamento livre preservado

O comportamento `estrutura: "livre"` (ou ausência de `estrutura`) deve permanecer integralmente preservado:

- `arranjo` continua válido em `livre`;
- `distribuicao` continua opcional e local ao container;
- ausência de `distribuicao` continua seguindo a ADR-0018 (construção orientada pelo conteúdo, não equivalente a `igual`);
- modos `igual`, `percentual`, `fracao` permanecem;
- maiores restos preservados;
- composição recursiva por containers preservada;
- três níveis de grupos preservados;
- todos os JSONs existentes continuam válidos sem modificação.

Nenhuma linha de código do caminho `livre` pode ser alterada exceto para suportar minimamente o despacho matricial (passagem de `estrutura_g` e `matriz_g` nas chamadas internas).

---

## 12. Schema matricial

### 12.1 Seletor `estrutura`

O campo `estrutura` é um campo opcional do nó `grupo`. Valores aceitos: `"livre"`, `"matriz"`. Ausência equivale a `"livre"`.

### 12.2 Objeto `matriz` (obrigatório quando `estrutura: "matriz"`)

```json
{
  "estrutura": "matriz",
  "matriz": {
    "linhas": {
      "quantidade": <inteiro 2–4>,
      "distribuicao": <objeto de distribuição>
    },
    "colunas": {
      "quantidade": <inteiro 2–4>,
      "distribuicao": <objeto de distribuição>
    },
    "celulas": [
      {"linha": <1-based>, "coluna": <1-based>, "elemento": "<id>"},
      ...
    ]
  },
  "elementos": [
    {"id": "<id>", "tipo": "<tipo>"},
    ...
  ]
}
```

### 12.3 Proibições em `estrutura: "matriz"`

- `arranjo` é proibido (ADR-0020 D13);
- distribuição de qualquer eixo não pode ser omitida (ADR-0020 D6);
- distribuição implícita (default `igual`) não existe (INV-MAT-DIST-04);
- fallback para `livre` não existe (ADR-0020 D12).

### 12.4 Presença indevida de `matriz` em `livre`

O contrato (`contrato_composicao_corpo.md` seção 3.3) exige que `arranjo` seja proibido em `estrutura: "matriz"`. O campo `matriz` em um grupo `livre` ou sem `estrutura` é campo inerte não validado nesta versão — não deve ser rejeitado. O loader não valida o conteúdo do objeto `matriz` em grupos que não declarem `estrutura: "matriz"`.

---

## 13. Validação do loader

A função `_validar_grupo` em `scripts/tela/loader.py` deve ser estendida. A ordem de validação abaixo é suficiente para impedir que uma matriz inválida chegue ao modelo ou ao renderer.

### 13.1 Ordem de validação para `estrutura: "matriz"`

1. **`estrutura`**: ler `estrutura = elemento.get("estrutura")`. Se não for `None`, `"livre"` ou `"matriz"`, rejeitar com `TelaGrupoInvalido` indicando o valor recebido e o caminho.

2. **`arranjo` em `"matriz"`**: se `estrutura == "matriz"` e `elemento.get("arranjo") is not None`, rejeitar com `TelaGrupoInvalido` indicando que `arranjo` é proibido em `estrutura: "matriz"`.

3. **`arranjo` em `"livre"` ou ausente**: validar `arranjo` contra `ARRANJOS_CORPO_VALIDOS` exatamente como hoje.

4. **Objeto `matriz`**: se `estrutura == "matriz"`, validar que `"matriz"` está presente e é um `dict`. Ausência ou tipo errado: rejeitar com `TelaGrupoInvalido` indicando o caminho.

5. **`linhas`**: ler `matriz["linhas"]`. Deve ser `dict`. Ler `quantidade`. Deve ser inteiro com `2 <= quantidade <= 4`. Caso contrário, rejeitar.

6. **`colunas`**: ler `matriz["colunas"]`. Mesma regra de dimensão.

7. **`linhas.distribuicao`**: ausência invalida a matriz (`INV-MAT-DIST-01`). Se ausente, rejeitar. Se presente, reutilizar `_validar_distribuicao_corpo(dist, n_linhas, prefixo_caminho + ".matriz.linhas")`.

8. **`colunas.distribuicao`**: ausência invalida a matriz (`INV-MAT-DIST-02`). Mesma regra.

9. **`celulas`**: ler `matriz["celulas"]`. Deve ser lista não vazia com exatamente `n_linhas * n_colunas` entradas.

10. **Cada entrada de `celulas`**: deve ser `dict` com `"linha"`, `"coluna"` e `"elemento"`. Cada um deve ter o tipo esperado (int ≥ 1, int ≥ 1, str não vazia).

11. **Limites de coordenada**: `1 <= linha <= n_linhas` e `1 <= coluna <= n_colunas`. Violação: rejeitar com coordenada afetada no diagnóstico.

12. **Coordenadas duplicadas**: o par `(linha, coluna)` não pode aparecer mais de uma vez. Rejeitar com par duplicado no diagnóstico.

13. **Elementos duplicados**: o valor de `elemento` não pode aparecer mais de uma vez em `celulas`. Rejeitar com id duplicado no diagnóstico.

14. **Referências a filhos diretos**: todo `elemento` referenciado em `celulas` deve existir em `elementos[]`. Rejeitar com id não encontrado no diagnóstico.

15. **Cobertura integral**: todo filho declarado em `elementos[]` deve aparecer exatamente uma vez em `celulas`. Rejeitar com id não associado no diagnóstico.

16. **Profundidade**: a validação recursiva existente (`nivel_grupo`) continua válida. Um `grupo` filho dentro de uma célula matricial conta normalmente como nível de grupo. Nenhuma exceção para `estrutura: "matriz"`.

17. **Validação de sub-elementos**: após validar o schema matricial, validar cada filho de `elementos[]` exatamente como hoje (id presente, tipo válido, recursão para tipo `grupo`).

### 13.2 Padrão de diagnóstico

Os diagnósticos devem seguir o padrão existente:
- identificar o caminho estrutural afetado: `"corpo → g1.matriz.linhas.distribuicao ausente"`;
- identificar o campo declarativo afetado;
- usar `TelaGrupoInvalido` para erros de estrutura de grupo;
- usar `TelaEstruturaInvalida` quando delegado de `_validar_distribuicao_corpo`.

Não inventar nova taxonomia de exceções se as existentes puderem ser reutilizadas.

### 13.3 Ausência de fallback

Nenhuma condição de invalidade da matriz pode resultar em:
- conversão silenciosa para `livre`;
- correção automática de dimensões;
- completar células ausentes;
- remover células excedentes;
- inferir coordenadas.

---

## 14. Representação no modelo

### 14.1 `ElementoCorpo` para grupo matricial

Nenhum campo novo é necessário em `ElementoCorpo`. A infraestrutura `_campos_inertes` já captura todos os campos do nó `grupo` que não são `id`, `tipo` e `elementos`.

Para um grupo com `estrutura: "matriz"`, após a construção pelo modelo:
- `elemento.tipo == "grupo"`;
- `elemento._campos_inertes["estrutura"] == "matriz"`;
- `elemento._campos_inertes["matriz"]` contém o dict com `linhas`, `colunas` e `celulas`;
- `elemento.elementos` contém a lista de `ElementoCorpo` dos filhos diretos, construída recursivamente na ordem de `elementos[]`.

### 14.2 Construção de `elementos` para grupo matricial

O método `_construir_elementos_recursivo` em `scripts/tela/modelo.py` constrói `elemento.elementos` a partir da lista `elementos[]` do JSON. Para grupos matriciais, essa lista é construída na ordem declarada do array `elementos[]` do JSON. O renderer usará o dict `celulas` (em `_campos_inertes["matriz"]["celulas"]`) para mapear cada filho ao seu retângulo de destino.

O modelo não deve:
- reordenar `elementos` por coordenada;
- preencher defaults;
- inferir coordenadas;
- duplicar filhos.

### 14.3 Verificação de necessidade de alteração no modelo

Se o comportamento atual de `_construir_elementos_recursivo` já preserva `estrutura` e `matriz` em `_campos_inertes` (conforme verificado pelo levantamento técnico — seção que inclui `"estrutura"` não em `("id", "tipo", "elementos")` e portanto capturado como inerte), não é necessária nenhuma alteração ao modelo.

O executor deve verificar isso antes de qualquer edição. Se não for necessária alteração, o IMP-0029 deve registrar explicitamente que `modelo.py` não foi alterado.

---

## 15. Cálculo da grade

A grade é calculada uma única vez para o container matricial.

### 15.1 Primitivas a reutilizar

- `_pesos_distribuicao(distribuicao, n)` — já existente em `scripts/tela/renderizador.py` (linha 203). Reutilizar sem modificação.
- `_distribuir_alturas(altura_disponivel, pesos)` — já existente (linha 219). Reutilizar sem modificação para calcular cotas das linhas.
- `_distribuir_larguras(largura_disponivel, pesos)` — já existente (linha 257). Reutilizar sem modificação para calcular cotas das colunas.

### 15.2 Sequência de cálculo em `_renderizar_container_matriz`

```
n_linhas = matriz_config["linhas"]["quantidade"]
n_colunas = matriz_config["colunas"]["quantidade"]
dist_linhas = matriz_config["linhas"]["distribuicao"]
dist_colunas = matriz_config["colunas"]["distribuicao"]

pesos_linhas = _pesos_distribuicao(dist_linhas, n_linhas)
pesos_colunas = _pesos_distribuicao(dist_colunas, n_colunas)

alturas = _distribuir_alturas(altura_disponivel, pesos_linhas)
larguras = _distribuir_larguras(total_w, pesos_colunas)
```

As listas `alturas` e `larguras` têm comprimento igual a `n_linhas` e `n_colunas` respectivamente. São calculadas **uma única vez** e compartilhadas por todas as células.

### 15.3 Regra invariante

```text
nenhuma célula pode recalcular isoladamente os limites das linhas ou colunas da matriz pai
```

O arredondamento de restos aplica-se **separadamente** em cada eixo (uma vez para linhas, uma vez para colunas). O arredondamento de linhas não afeta o cálculo de colunas e vice-versa.

---

## 16. Renderização das células

### 16.1 Função nova: `_renderizar_container_matriz`

Criar em `scripts/tela/renderizador.py` a função:

```
_renderizar_container_matriz(matriz_config, elementos, borda, total_w, altura_disponivel)
```

Passos internos:

1. Calcular `alturas` e `larguras` conforme seção 15.2.
2. Construir lookup: `elem_por_id = {e.id: e for e in elementos}`.
3. Construir lookup: `celula_para_id = {(c["linha"], c["coluna"]): c["elemento"] for c in matriz_config["celulas"]}`.
4. Para cada linha `r` em `range(1, n_linhas + 1)`:
   a. Construir lista de elementos na ordem das colunas: `[elem_por_id[celula_para_id[(r, c)]] for c in range(1, n_colunas + 1)]`.
   b. Construir lista de larguras correspondente: `[larguras[c-1] for c in range(1, n_colunas + 1)]`.
   c. Chamar `_renderizar_container_horizontal(distribuicao=None, elementos=..., borda=borda, total_w=total_w, altura_disponivel=alturas[r-1], larguras=...)` com as larguras pré-calculadas.
   d. Se o bloco resultante não for vazio, acumulá-lo.
5. Retornar `"\n".join(blocos)`.

A função `_renderizar_container_horizontal` já aceita o parâmetro `larguras` pré-calculadas (ver assinatura em linha 844 de `renderizador.py`). Reutilizá-la sem modificação.

### 16.2 Extensão de `_renderizar_container`

A função `_renderizar_container(arranjo, distribuicao, elementos, borda, total_w, altura_disponivel)` deve ser estendida para aceitar `estrutura=None` e `matriz_config=None` como parâmetros opcionais:

```
def _renderizar_container(arranjo, distribuicao, elementos, borda, total_w, altura_disponivel,
                           estrutura=None, matriz_config=None):
    if estrutura == "matriz":
        return _renderizar_container_matriz(
            matriz_config, elementos, borda, total_w, altura_disponivel
        )
    # código existente inalterado abaixo
```

O código existente (`arr` → `horizontal` / `vertical`) permanece integralmente.

### 16.3 Atualização dos chamadores internos

Dentro de `_renderizar_container_vertical` e `_renderizar_container_horizontal`, cada ocorrência do padrão:

```python
if elemento.tipo == "grupo":
    arranjo_g = elemento._campos_inertes.get("arranjo")
    dist_g = elemento._campos_inertes.get("distribuicao")
    bloco = _renderizar_container(
        arranjo_g, dist_g, elemento.elementos, borda, total_w, cota
    )
```

deve ser atualizada para incluir `estrutura_g` e `matriz_g`:

```python
if elemento.tipo == "grupo":
    estrutura_g = elemento._campos_inertes.get("estrutura")
    arranjo_g = elemento._campos_inertes.get("arranjo")
    dist_g = elemento._campos_inertes.get("distribuicao")
    matriz_g = elemento._campos_inertes.get("matriz")
    bloco = _renderizar_container(
        arranjo_g, dist_g, elemento.elementos, borda, total_w, cota,
        estrutura=estrutura_g, matriz_config=matriz_g
    )
```

Para grupos `livre` (ou sem `estrutura`), `estrutura_g` será `None` e `matriz_g` será `None`. O `_renderizar_container` continuará despachando para o caminho existente (`horizontal` ou `vertical`).

Todas as ocorrências desse padrão em `_renderizar_container_vertical` (com e sem distribuição — há dois blocos `if/else`) e em `_renderizar_container_horizontal` devem ser atualizadas. Verificar com `rg` antes de implementar.

---

## 17. Bordas e interseções

O renderer usa a estrutura de bordas (`borda["tl"]`, `borda["tr"]`, etc.) já definida. Para a renderização matricial:

- cada célula individual é renderizada como uma caixa completa com borda própria via `_caixa_de_elemento` (chamada por `_renderizar_container_horizontal` → `_caixa_de_elemento`);
- `_renderizar_container_horizontal` já produz bordas lado a lado, coladas sem vão externo (ADR-0015, contrato seção 5.6);
- as linhas horizontais de diferentes linhas da matriz são concatenadas verticalmente (`"\n".join(blocos)`);
- o caractere de borda lateral (`borda["v"]`) de células adjacentes na mesma linha já produz `││` quando colados;
- não existe lógica nova de interseção — o comportamento resultante é o mesmo do `horizontal` existente.

Se o terminal atual não produzir o caractere de interseção esperado (por exemplo, `┼` no lugar de `││`), isso é consequência da estrutura de bordas existente (que não usa `┼`). Não criar lógica nova de interseção.

---

## 18. Hierarquia e profundidade

- A contagem de profundidade continua exclusivamente por nós `grupo` (ADR-0019 D1).
- `estrutura: "matriz"` não acrescenta nível.
- Linhas, colunas e células não contam como nível.
- Um `grupo` filho dentro de uma célula matricial conta normalmente como nível de grupo.
- O limite máximo de 3 níveis de grupos permanece (ADR-0019 D2).
- A validação de profundidade (`nivel_grupo`) no loader continua intacta.
- Um `grupo` dentro de uma célula de um grupo no nível 3 estaria no nível 4 e deve ser rejeitado deterministicamente (ADR-0019 D4; EX-MAT-I8 do contrato).

---

## 19. Diagnósticos

Os diagnósticos de invalidade matricial devem seguir o padrão existente (caminho estrutural + campo + valor ou contexto).

Exemplos de caminhos a usar nas mensagens:

| Condição | Caminho a identificar |
|---|---|
| `estrutura` desconhecida | `<caminho_grupo>.estrutura` |
| `arranjo` proibido | `<caminho_grupo>.arranjo em estrutura: "matriz"` |
| Objeto `matriz` ausente | `<caminho_grupo>.matriz` |
| Dimensão inválida | `<caminho_grupo>.matriz.linhas.quantidade` ou `.colunas.quantidade` |
| Distribuição de linhas ausente | `<caminho_grupo>.matriz.linhas.distribuicao` |
| Distribuição de colunas ausente | `<caminho_grupo>.matriz.colunas.distribuicao` |
| Distribuição inválida | delegado de `_validar_distribuicao_corpo` com prefixo `<caminho_grupo>.matriz.linhas` ou `.colunas` |
| Lista `celulas` ausente ou não lista | `<caminho_grupo>.matriz.celulas` |
| Contagem de células errada | `<caminho_grupo>.matriz.celulas` (exibir esperado × encontrado) |
| Coordenada fora do limite | `<caminho_grupo>.matriz.celulas[i]` (exibir coordenada) |
| Coordenada duplicada | `<caminho_grupo>.matriz.celulas` (exibir par duplicado) |
| Elemento duplicado | `<caminho_grupo>.matriz.celulas` (exibir id duplicado) |
| Referência inexistente | `<caminho_grupo>.matriz.celulas[i].elemento` (exibir id) |
| Filho não associado | `<caminho_grupo>.elementos` (exibir id sem célula) |
| Profundidade | caminho existente (`nivel_grupo`) |

Não inventar nova taxonomia de exceções. Usar `TelaGrupoInvalido` e `TelaEstruturaInvalida` conforme o padrão existente.

---

## 20. Terminal pequeno e SIGWINCH

Preservar:

- detecção de `SIGWINCH` e redesenho — nenhuma alteração;
- quadro global de terminal pequeno — nenhuma alteração;
- `par de dimensões válido` / `últimas dimensões válidas` — nenhuma alteração;
- recálculo de dimensões no renderer a cada novo par válido — inclui matrizes.

A política específica de área insuficiente para matrizes (quando `alturas[r]` ou `larguras[c]` ficam muito pequenas após distribuição) **não está decidida** nas autoridades. A regra global existente da ADR-0017 é a única referência.

Se a implementação exigir decisão específica de tamanho mínimo por célula que não possa ser resolvida pelas regras globais existentes, parar com:

```text
ARCHITECTURE_REVIEW_REQUIRED
```

Não criar neste ciclo: paginação de matriz, rolagem, truncamento específico por célula, redução automática de linhas ou colunas, nova política numérica de tamanho mínimo.

---

## 21. Alterações declarativas

```text
alteracoes_declarativas_em_json_ativo: nenhuma
```

Todos os JSONs ativos (`orquestrador.json`, `grupo_minimo.json`, `destino_minimo.json`, `stub_b.json`) devem permanecer inalterados.

Fixtures e dados de teste para o schema matricial devem ser definidos como dicts inline dentro dos arquivos de teste, não como novos arquivos JSON em `config/telas/`.

---

## 22. Preservações

O futuro ciclo deve manter aprovados:

| Item | Status a preservar |
|---|---|
| Todos os JSONs existentes sem `estrutura` | válidos e sem alteração de comportamento |
| Grupos `livre` (ausência de `estrutura`) | comportamento inalterado |
| `estrutura: "livre"` explícito | comportamento inalterado |
| Ausência de `distribuicao` em `livre` | segue ADR-0018 (construção orientada pelo conteúdo) |
| Modos `igual`, `percentual`, `fracao` em `livre` | inalterados |
| Composição plana | inalterada |
| Composição hierárquica (1–3 níveis) | inalterada |
| `console`, `lancador`, `dashboard` | comportamento interno inalterado |
| Navegação e chips | inalterados |
| Redimensionamento reativo (`SIGWINCH`) | inalterado |
| Terminal pequeno (quadro global) | inalterado |
| Diagnósticos existentes | inalterados |
| Baseline de `1004/1004` (ajustado pelo novo total) | todos os testes anteriores passando |

---

## 23. Testes obrigatórios

### 23.1 Arquivos e comando

Arquivos de teste a criar/estender:

- `scripts/tela/teste_loader.py` — nova classe de teste (ex.: `TesteValidacaoMatriz`)
- `scripts/tela/teste_modelo.py` — nova classe de teste (ex.: `TesteModeloMatriz`)
- `scripts/tela/teste_renderizador.py` — nova classe de teste (ex.: `TesteRenderizadorMatriz`)

Comandos de execução (a partir da raiz Git):

```bash
python3 scripts/tela/teste_loader.py
python3 scripts/tela/teste_modelo.py
python3 scripts/tela/teste_renderizador.py
python3 scripts/tela/teste_demo.py
python3 scripts/tela/teste_diagnostico.py
python3 scripts/tela/teste_explorar_barra_de_menus.py
```

Cada comando deve terminar com código de saída zero. A suíte canônica é a execução direta dos seis arquivos. O comando de coleta `pytest` não é a suíte canônica de aceite deste projeto.

### 23.2 Testes de compatibilidade (não regredir)

- Grupo sem `estrutura`: comporta-se como `livre` (ausência → `livre`).
- `estrutura: "livre"` explícito: preserva arranjo e distribuição.
- Todos os testes anteriores passando (`1004/1004` ajustado pelo novo total).
- Ausência de `distribuicao` em `livre`: não equivale a `igual` (ADR-0018).
- Composição com um, dois e três níveis de grupos `livre`.
- JSONs de produção permanecem válidos (testar `carregar_tela` com cada JSON ativo ou mock equivalente).

### 23.3 Matrizes válidas

| Cenário |
|---|
| Matriz 2×2 com `igual` explícito nos dois eixos |
| Matriz 2×3 com `fracao` em linhas e `percentual` em colunas |
| Matriz 2×4 com `fracao` `[1,2]` em linhas e `[1,2,1,2]` em colunas |
| Matriz 3×2 com `percentual` nos dois eixos |
| Matriz 3×3 com `fracao` assimétrico em ambos os eixos |
| Matriz 3×4 com `igual` em linhas e `fracao` em colunas |
| Matriz 4×2 com `fracao` em linhas e `percentual` em colunas |
| Matriz 4×3 com `percentual` em linhas e `fracao` em colunas |
| Matriz 4×4 com `fracao` `[1,2,3,4]` em ambos os eixos |
| `igual` nos dois eixos com declaração explícita |
| `percentual` nos dois eixos (soma = 100 em cada eixo) |
| `fracao` nos dois eixos com pesos positivos |
| Modos diferentes entre linhas e colunas |
| Pesos assimétricos em linhas e colunas |
| Ordem embaralhada de `celulas[]` (posição por coordenada, não por ordem) |
| Filho do tipo `console` em célula |
| Filho do tipo `lancador` em célula |
| Filho do tipo `dashboard` em célula |
| Filho do tipo `grupo` (`livre`) em célula dentro do limite de profundidade |
| Grupo matricial no nível 1 de profundidade |
| Grupo matricial no nível 2 de profundidade |
| Grupo matricial no nível 3 de profundidade |

### 23.4 Matrizes inválidas (loader deve rejeitar)

| Cenário |
|---|
| `estrutura` com valor desconhecido (ex.: `"grade"`) |
| `estrutura: "matriz"` sem objeto `matriz` |
| Dimensão de linhas = 1 |
| Dimensão de linhas = 5 |
| Dimensão de colunas = 1 |
| Dimensão de colunas = 5 |
| `matrix.linhas.distribuicao` ausente |
| `matriz.colunas.distribuicao` ausente |
| Distribuições ausentes nos dois eixos |
| Somente um eixo com distribuição (linhas com, colunas sem) |
| `igual` implícito (ambos sem distribuição mas espera-se divisão igual) |
| Percentual de linhas que não soma 100 |
| Percentual de colunas que não soma 100 |
| Peso fracionário zero em linhas |
| Peso fracionário negativo em colunas |
| Quantidade de valores diferente da dimensão (linhas) |
| Quantidade de valores diferente da dimensão (colunas) |
| Coordenada `linha = 0` em `celulas` |
| Coordenada `coluna = 0` em `celulas` |
| Coordenada de linha fora do limite (acima de `n_linhas`) |
| Coordenada de coluna fora do limite (acima de `n_colunas`) |
| Coordenada `(linha, coluna)` duplicada em `celulas` |
| Mesmo `elemento` id em duas células diferentes |
| Referência em `celulas.elemento` a id inexistente em `elementos[]` |
| Filho de `elementos[]` não associado a nenhuma célula |
| Célula faltante (declaradas menos que `linhas × colunas`) |
| Célula excedente (declaradas mais que `linhas × colunas`) |
| `arranjo` presente em `estrutura: "matriz"` |
| Grupo filho (`estrutura: "livre"`) dentro de célula de grupo no nível 3 (criaria nível 4) |
| Tentativa de fallback para `livre` após invalidade (confirmar que erro é lançado, não fallback) |

### 23.5 Renderização e alinhamento (testes determinísticos)

Os testes de renderização devem verificar **coordenadas compartilhadas**, não apenas presença de conteúdo. Para verificar alinhamento:

1. Renderizar a matriz completa como string e dividir por `"\n"`.
2. Para cada coluna `c`, verificar que a posição horizontal da borda esquerda é **idêntica** em todas as linhas.
3. Para cada linha `r`, verificar que a altura (número de linhas do bloco) corresponde à cota calculada.

| Cenário |
|---|
| Alinhamento vertical de divisórias entre colunas em todas as linhas da matriz |
| Alinhamento horizontal de divisórias entre linhas em todas as colunas da matriz |
| Matriz 2×2 com pesos iguais: cotas iguais nos dois eixos |
| Matriz 2×4 com `[1,2]` em linhas e `[1,2,1,2]` em colunas: cotas distintas verificadas |
| Matriz 3×3 com dimensões ímpares do terminal: maiores restos aplicados separadamente por eixo |
| Distribuição com restos: soma de cotas = area total (verificar por eixo) |
| Matriz aninhada dentro de grupo `livre` no nível 2 |
| Grupo `livre` dentro de célula matricial |
| Grupo `livre` no nível 1 contendo grupo matricial no nível 2 |
| Redimensionamento: renderizar com `total_w` 1 = X, `total_w` 2 = X+20, verificar que grade é recalculada |
| Terminal pequeno: se o renderer levantar `RenderizadorErro` por largura insuficiente (< 10 chars por área), confirmar que o erro é propagado e não silenciado |

### 23.6 Suíte canônica de execução direta

O comando de coleta `pytest` **não é a suíte canônica de aceite deste projeto.** A suíte canônica é a execução direta dos seis arquivos a partir da raiz Git:

```bash
python3 scripts/tela/teste_loader.py
python3 scripts/tela/teste_modelo.py
python3 scripts/tela/teste_renderizador.py
python3 scripts/tela/teste_demo.py
python3 scripts/tela/teste_diagnostico.py
python3 scripts/tela/teste_explorar_barra_de_menus.py
```

#### Critérios de aprovação da suíte canônica

1. Código de saída zero em cada um dos seis executores diretos.
2. Nenhuma verificação direta reprovada.
3. Baseline histórico preservado (todos os testes anteriores aprovados).
4. Verificações novas do H-0028 aprovadas.
5. Total final maior ou igual ao baseline `1070` (total direto completo no commit-base `f00b0bb`).
6. Contagens individuais por arquivo registradas no IMP-0029.
7. Total agregado registrado no IMP-0029.
8. Nenhum erro ocultado.
9. Nenhuma alteração em arquivo de teste apenas para obter aprovação.
10. Nenhum arquivo fora do escopo alterado.

O critério não exige um número final fixo antecipado.

#### Baselines e relação entre 1004 e 1070

```yaml
baseline_1004:
  arquivos: [teste_loader.py, teste_modelo.py, teste_renderizador.py, teste_demo.py]
  finalidade: baseline_historico_do_h0027
  total: 1004/1004

baseline_1070:
  arquivos: [teste_loader.py, teste_modelo.py, teste_renderizador.py, teste_demo.py,
             teste_diagnostico.py, teste_explorar_barra_de_menus.py]
  finalidade: total_direto_completo_no_commit_base_f00b0bb
  total: 1070/1070
```

`1004/1004` e `1070/1070` não são contagens contraditórias. O primeiro é a contagem dos quatro arquivos principais do ciclo H-0027 (loader + modelo + renderizador + demo = 129 + 81 + 491 + 303). O segundo é a soma dos seis executores diretos no commit-base `f00b0bb`, incluindo também `teste_diagnostico.py` (28) e `teste_explorar_barra_de_menus.py` (38).

#### Evidência desta execução

```yaml
implementacao_h0028:
  status_executivo: IMPLEMENTATION_COMPLETED
  qa_implementacao: pendente
  direto_completo: 1133/1133
  novas_verificacoes: 63/63
  erros_pytest_introduzidos: 0
```

As contagens acima são evidência desta execução específica, não regra eterna para futuras reexecuções. A implementação não está declarada aprovada; o `qa_implementacao` permanece pendente.

#### Uso complementar do `pytest`

O comando `python3 -m pytest ...` pode ser executado como diagnóstico complementar não bloqueante. O comando de coleta `pytest` não é a suíte canônica de aceite deste projeto.

Quando executado, os resultados devem ser comparados com o baseline do mesmo commit:

```yaml
baseline_pytest_f00b0bb:
  passed: 207
  errors: 10
  failures: 0
  codigo_saida: 1

erros_preexistentes:
  quantidade: 10
  causa: funcoes_nomeadas_teste_com_argumentos_posicionais_coletadas_indevidamente_pelo_pytest
  node_ids:
    - "tela/teste_loader.py::teste_erros (fixture tmp_base ausente)"
    - "tela/teste_loader.py::teste_tipos_validos (fixture tmp_base ausente)"
    - "tela/teste_loader.py::teste_grupo_estrutural (fixture tmp_base ausente)"
    - "tela/teste_loader.py::teste_arranjo_corpo_h0019 (fixture tmp_base ausente)"
    - "tela/teste_loader.py::teste_distribuicao_corpo_h0025 (fixture tmp_base ausente)"
    - "tela/teste_loader.py::teste_hierarquia_grupos_adr0019 (fixture tmp_base ausente)"
    - "tela/teste_demo.py::teste_navegacao_minima (fixture modelo ausente)"
    - "tela/teste_demo.py::teste_renderizar_estado (fixture modelo ausente)"
    - "tela/teste_demo.py::teste_renderizar_estado_altura (fixture modelo ausente)"
    - "tela/teste_diagnostico.py::teste_modo_executavel (fixture resultado_esperado ausente)"
  introduzidos_por_h0028: false
  arquivos_proibidos: [teste_demo.py, teste_diagnostico.py]
```

Os dez erros existem em `f00b0bb` por razão estrutural pré-existente ao H-0028: funções nomeadas com `teste_` recebem argumentos posicionais fornecidos pelo `main()` interno de cada arquivo, não por fixtures `pytest`. Esses erros não foram introduzidos pelo H-0028 e não devem ser usados isoladamente para rejeitar a implementação. Não corrigí-los exigiria alterar arquivos proibidos neste ciclo (`teste_demo.py`, `teste_diagnostico.py`) ou adicionar configuração `pytest` fora da lista permitida.

Qualquer erro adicional ou causa diferente dos dez acima deve ser investigado como possível regressão. A comparação deve considerar: quantidade, node IDs, arquivos, linhas, fixtures e causas. A existência de dez erros preexistentes não autoriza ignorar regressões futuras.

---

## 24. Validação manual futura

**Esta seção descreve validação a ser executada pelo QA pós-implementação. Não executar nesta etapa.**

### 24.1 Objetivo

Como o objetivo envolve alinhamento visual em TTY, os testes automáticos não são suficientes para verificar o resultado visual. Uma sessão TTY real é necessária para confirmar que as divisórias verticais e horizontais da matriz estão alinhadas.

```yaml
validacao_visual_tty:
  executor: usuario
  automatizavel_pelo_sistema: false
  status_antes_da_execucao_humana: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

O implementador e o auditor automatizado podem fornecer o roteiro, os comandos, as dimensões e os critérios de aprovação e reprovação, e podem registrar que a validação permanece pendente. Não podem executar a homologação visual em nome do usuário, simular inspeção humana, declarar bordas visualmente aprovadas, substituir a validação manual por teste automatizado nem apresentar capturas ou strings como homologação humana conclusiva.

A pendência manual não é classificada como falha funcional automática. É um gate separado antes do fechamento final do ciclo.

### 24.2 Risco: dependência de JSON ativo

A arquitetura atual não possui mecanismo de carregamento de fixture JSON isolada sem alterar um JSON de produção. Para a validação manual, há duas opções:

**Opção A** (sem alterar JSON ativo): criar temporariamente um script de demonstração ad-hoc que monte um `ModeloTela` diretamente a partir de um dict (sem `carregar_tela`), passando pelo `construir_modelo` e chamando `renderizar_tela`. Isso não requer arquivo de configuração em `config/telas/`.

**Opção B** (alterar JSON ativo): modificar temporariamente um JSON de produção para incluir `estrutura: "matriz"`. Isso requer alteração de arquivo proibido.

O executor deve usar a **Opção A** se possível. Se a arquitetura não permitir `construir_modelo(dict)` diretamente a partir de dados inline sem `carregar_tela`, registrar isso como risco no IMP-0029 sem decidir solução nova.

### 24.3 Cenários a verificar manualmente

1. **Matriz 2×2 com `igual` nos dois eixos** (terminal de pelo menos 40 colunas × 20 linhas):
   - Verificar que os quatro filhos ocupam áreas iguais.
   - Verificar que a divisória vertical central está alinhada nas duas linhas.
   - Verificar que a divisória horizontal central está alinhada nas duas colunas.

2. **Matriz 2×4 com `[1,2]` em linhas e `[1,2,1,2]` em colunas** (terminal de pelo menos 80 colunas × 30 linhas):
   - Verificar que as cotas de colunas variam proporcionalmente (colunas 2 e 4 têm o dobro da largura das colunas 1 e 3).
   - Verificar que as colunas são alinhadas nas duas linhas.
   - Verificar que a linha inferior (proporção 2) tem o dobro da altura da linha superior (proporção 1).

3. **Pesos assimétricos com restos** (matriz 3×3 em terminal de dimensão ímpar):
   - Verificar que a soma das cotas fechou a dimensão exata (sem lacuna nem sobreposição).
   - Verificar que divisórias não se deslocam entre linhas.

4. **Redimensionamento**: com a matriz ativa, redimensionar o terminal (arrastar janela ou `stty cols X rows Y` em sessão TTY):
   - Verificar que a grade é recalculada automaticamente.
   - Verificar que as divisórias permanecem alinhadas após cada redimensionamento.

### 24.4 Critérios de aprovação manual

- Todas as divisórias verticais de uma mesma coluna estão na mesma posição horizontal em todas as linhas.
- Todas as divisórias horizontais de uma mesma linha estão na mesma posição vertical em todas as colunas.
- Não aparecem lacunas, duplicações nem deslocamentos entre células adjacentes.
- Redimensionamento produz nova grade coerente.

### 24.5 Critérios de reprovação manual

- Qualquer divisória deslocada entre linhas ou colunas da mesma grade.
- Qualquer lacuna visual (linha em branco não prevista) entre células.
- Grade visualmente inconsistente após redimensionamento.

---

## 25. Relatório de implementação esperado

O relatório esperado é:

```text
scripts/docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md
```

O executor não pode autoaprovar a implementação.

### 25.1 Conteúdo obrigatório do IMP-0029

O relatório de implementação deve registrar:

- handoff executado: H-0028;
- commit-base confirmado;
- estado Git no início (saída de `git status --short` e `git diff --stat`);
- arquivos alterados e quais modificações foram feitas em cada um;
- schema implementado: confirmar que `estrutura: "matriz"` é validado e rejeitado deterministicamente quando inválido;
- validações do loader: listar cada validação da seção 13 e confirmar presença no código;
- modelo: confirmar que `_campos_inertes` transporta `estrutura` e `matriz` sem alteração ou confirmar quais alterações foram necessárias;
- renderer: confirmar adição de `_renderizar_container_matriz` e extensão de `_renderizar_container`;
- alinhamento: confirmar que `alturas` e `larguras` são calculados uma vez por container matricial;
- diagnósticos: confirmar que caminhos estruturais afetados aparecem nas mensagens de erro;
- testes executados: resultados dos seis executores diretos (seção 23.6), com contagens individuais por arquivo e total agregado;
- testes diretos:
  - comandos executados (um por arquivo);
  - contagem individual por arquivo;
  - total agregado;
  - código de saída de cada executor;
  - resultado (`aprovado` / `reprovado`);
- pytest complementar (se executado):
  - resultado com comparação ao baseline `f00b0bb` (207 passed, 10 errors);
  - erros novos identificados ou confirmação de ausência;
  - erros preexistentes listados separadamente, sem misturá-los com falhas funcionais do H-0028;
- resultados: total de testes passando, total de testes novos, baseline histórico `1004/1004` (H-0027) e baseline direto completo `1070/1070` (f00b0bb) preservados;
- validações não executadas: listar quaisquer cenários de teste que não foram cobertos;
- necessidade de TTY real: declarar se a validação manual da seção 24 foi ou não executada;
- resíduos: confirmar `git diff --check` limpo e stage vazio;
- estado Git ao final: saída de `git status --short`;
- bloqueios: registrar qualquer `ARCHITECTURE_REVIEW_REQUIRED` encontrado;
- ausência de commit: confirmar que nenhum commit foi criado.

---

## 26. Critérios de aceite

1. **Ausência de regressão em `livre`**: todos os `1004` testes anteriores passam sem modificação de comportamento.

2. **Validação completa do schema matricial**: cada cenário inválido da seção 23.4 produz erro determinístico com caminho estrutural identificado.

3. **Modelo sem inferências**: `_campos_inertes["estrutura"]` e `_campos_inertes["matriz"]` transportam o declarado; nenhum default é preenchido.

4. **Grade única por matriz**: as funções `_distribuir_alturas` e `_distribuir_larguras` são chamadas **uma vez** por container matricial, não por célula.

5. **Alinhamento global de bordas**: testes determinísticos da seção 23.5 confirmam que a posição horizontal da divisória entre colunas é idêntica em todas as linhas da mesma matriz.

6. **Maiores restos separados por eixo**: a soma das `alturas` é igual a `altura_disponivel`; a soma das `larguras` é igual a `total_w`. Verificado por testes específicos.

7. **Cobertura completa de células**: `len(celulas) == n_linhas * n_colunas` validado pelo loader antes do modelo e do renderer.

8. **Profundidade máxima preservada**: grupo no nível 4 (inclusive dentro de célula matricial) é rejeitado deterministicamente.

9. **Erros determinísticos**: nenhuma condição de invalidade matricial produz fallback silencioso para `livre` ou comportamento indefinido.

10. **Terminal pequeno preservado**: o renderer não cria nova política; o `RenderizadorErro` existente (largura < 10 por área) é o único tratamento definido.

11. **`SIGWINCH` preservado**: o recálculo da grade matricial é acionado pelo mesmo mecanismo de redesenho existente, sem handler novo.

12. **Suíte canônica aprovada**: código de saída zero nos seis executores diretos (seção 23.6); nenhuma verificação direta reprovada; baseline histórico `1004/1004` (H-0027) preservado; baseline direto completo `1070/1070` (f00b0bb) preservado; verificações novas do H-0028 aprovadas; total final ≥ `1070`.

13. **Validação manual futura definida**: seção 24 presente e concreta; risco de dependência de JSON ativo documentado se aplicável.

14. **Relatório de implementação criado**: `IMP-0029` presente em `scripts/docs/relatorios/` com todos os campos da seção 25.1.

15. **Nenhum arquivo fora do escopo**: somente os arquivos listados na seção 8 foram alterados.

16. **Stage vazio**: `git diff --cached --check` limpo ao final da implementação.

17. **Nenhum commit**: nenhum commit foi criado durante a implementação.

---

## 27. Condições de bloqueio

Parar com `ARCHITECTURE_REVIEW_REQUIRED` quando:

- faltar regra normativa para decidir comportamento não coberto pela ADR-0020 D1–D16;
- contratos apresentarem contradição entre si ou com a ADR-0020;
- a área insuficiente para células matriciais exigir política nova não resolvível pelas regras globais da ADR-0017;
- o renderer atual não permitir grade comum sem decisão arquitetural nova;
- a profundidade não puder ser verificada sem alterar ADR-0019 ou os contratos;
- for necessário alterar documento normativo (ADR, contrato, nomenclatura, índice);
- for necessário escolher default, inferência ou fallback não documentado;
- a lista nominal de arquivos da seção 8 for insuficiente para completar a implementação.

Parar com `BLOCKED_EVIDENCE` quando:

- arquivo indispensável da seção 10 não for localizado;
- teste obrigatório da seção 23 não puder ser identificado como verificável;
- não for possível comprovar o baseline `1004/1004`;
- estado Git impedir separar o escopo deste ciclo do estado atual do repositório.

---

## 28. Estado Git esperado ao final da implementação

```text
git status --short
 M scripts/tela/loader.py
 M scripts/tela/modelo.py       (se alteração for necessária; ver seção 14.3)
 M scripts/tela/renderizador.py
 M scripts/tela/teste_loader.py
 M scripts/tela/teste_modelo.py
 M scripts/tela/teste_renderizador.py
?? scripts/docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md

(e os arquivos não rastreados já existentes do ciclo ADR-0020)
```

- Stage: vazio.
- Nenhum commit criado.
- `git diff --check` limpo.
- `git diff --cached --check` limpo.

---

## 29. Fora de escopo

Declarados explicitamente fora de escopo deste ciclo:

- células vazias em qualquer forma (placeholders, nulos, reservados);
- `rowspan`, `colspan` ou mesclagem de células;
- dimensão menor que 2 ou maior que 4 (essas combinações são inválidas e rejeitadas, não implementadas de forma alternativa);
- novo tipo funcional;
- mudança de navegação (chips, `[✥]`, `[⇆]`, `[⏎]`, `[Esc]`);
- mudança interna de comportamento de `console`, `lancador` ou `dashboard`;
- paginação de matriz;
- rolagem de matriz;
- truncamento específico por célula;
- redução automática de linhas ou colunas;
- nova política numérica de tamanho mínimo por célula;
- correção da divergência de status da ADR-0018;
- alteração de contratos, ADRs, nomenclatura ou índice de ADRs;
- alteração de JSON ativo;
- refatoração ampla de módulos além do escopo direto da matriz;
- sincronização entre containers distintos (`matriz`–`livre` irmãos ou `matriz`–`matriz` irmãos);
- aplicação documental de qualquer nova ADR;
- alinhamento entre containers de composição distintos.

---

## 30. Documentos consultados

| Documento | Tipo | Papel |
|---|---|---|
| `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` | ADR | Autoridade primária (D1–D16) |
| `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | ADR | Maiores restos, composição, preenchimento |
| `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | ADR | Ausência de distribuição em `livre` |
| `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | ADR | Profundidade, 3 níveis de grupos |
| `scripts/docs/NOMENCLATURA.md` | Nomenclatura | Termos de matriz de grupos (§15) |
| `scripts/docs/contratos/contrato_composicao_corpo.md` | Contrato | Seções 3.3, 5.13–5.24, R-25–R-32 |
| `scripts/docs/contratos/contrato_tela_json.md` | Contrato | Schema da tela, validações futuras |
| `scripts/docs/contratos/contrato_json_tela_minima.md` | Contrato | Envelope mínimo, seção 6.4 |
| `scripts/docs/adr/INDICE_ADR.md` | Índice | Confirmação sequencial |
| `scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md` | Relatório | Histórico de rejeição e ACH-001 |
| `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0020.md` | Relatório | Confirmação de resolução do ACH-001 |
| `scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md` | Relatório | Aplicação documental |
| `scripts/docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0020.md` | Relatório | Aprovação da aplicação |
| `scripts/docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` | Handoff | Precedente direto |
| `scripts/docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md` | Relatório | Implementação anterior, baseline |
| `scripts/docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md` | Relatório | Fechamento do H-0027, confirmação de 1004/1004 |
| `scripts/tela/loader.py` | Código | Levantamento técnico: `_validar_grupo`, `_validar_distribuicao_corpo`, exceções |
| `scripts/tela/modelo.py` | Código | Levantamento técnico: `ElementoCorpo`, `_construir_elementos_recursivo` |
| `scripts/tela/renderizador.py` | Código | Levantamento técnico: `_renderizar_container`, `_distribuir_alturas`, `_distribuir_larguras`, `_pesos_distribuicao`, `_renderizar_container_horizontal` |
