# IMP-0028 — Implementação: Composição hierárquica do corpo com três níveis de grupos

**Handoff executado:** H-0027
**ADR aplicado:** ADR-0019
**Data:** 2026-07-12
**Status:** IMPLEMENTADO (patch aplicado — aguarda QA_POS_PATCH)

---

## 1. Escopo executado

Implementação integral das decisões D1–D7 do ADR-0019 nos três módulos (`loader`, `modelo`, `renderizador`) e atualização completa das suítes de teste, conforme especificado no H-0027.

Patch posterior aplicado em resposta ao `I2_IMPLEMENTATION_PATCH_REQUIRED` emitido pelo `RELATORIO_QA_H-0027_IMPLEMENTACAO.md`, corrigindo os achados ACH-001, ACH-005 e ACH-006, e completando os registros documentais ACH-002, ACH-003 e ACH-004.

---

## 2. Estado Git inicial da implementação H-0027

Estado capturado no início da implementação (commit-base confirmado pelo QA formal):

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       |  27 +-
 scripts/docs/adr/ADR-0007-tela-processamento-composicao.md |  15 +-
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md |  40 +-
 scripts/docs/contratos/contrato_json_tela_minima.md |   7 +-
 scripts/docs/contratos/contrato_tela_json.md       |  15 +-
 scripts/tela/loader.py                             | 128 +-
 scripts/tela/modelo.py                             | 106 +-
 scripts/tela/renderizador.py                       | 291 +++++-
 scripts/tela/teste_loader.py                       | 445 ++++++-
 scripts/tela/teste_modelo.py                       | 185 +++
 scripts/tela/teste_renderizador.py                 | 422 ++++++
 12 files changed, 1428 insertions(+), 254 deletions(-)

git diff --check
(sem saída — sem conflitos de espaço em branco)

git diff --cached --stat
(sem saída — stage vazio)

git diff --cached --name-only
(sem saída — stage vazio)
```

### 2.1 Classificação das alterações no início

| Arquivo rastreado modificado | Categoria |
|---|---|
| `docs/NOMENCLATURA.md` | Alteração documental preexistente (aplicação ADR-0019) |
| `docs/adr/ADR-0007-tela-processamento-composicao.md` | Alteração documental preexistente |
| `docs/adr/INDICE_ADR.md` | Alteração documental preexistente |
| `docs/contratos/contrato_composicao_corpo.md` | Alteração documental preexistente |
| `docs/contratos/contrato_json_tela_minima.md` | Alteração documental preexistente |
| `docs/contratos/contrato_tela_json.md` | Alteração documental preexistente |
| `tela/loader.py` | Alteração da implementação H-0027 |
| `tela/modelo.py` | Alteração da implementação H-0027 |
| `tela/renderizador.py` | Alteração da implementação H-0027 |
| `tela/teste_loader.py` | Alteração da implementação H-0027 |
| `tela/teste_modelo.py` | Alteração da implementação H-0027 |
| `tela/teste_renderizador.py` | Alteração da implementação H-0027 |

| Arquivo não rastreado | Categoria |
|---|---|
| `docs/adr/ADR-0019-...` | Ciclo ADR anterior (não tocado) |
| `docs/handoff/H-0027-...` | Handoff (não tocado) |
| `docs/relatorios/IMP-0028-...` | Este relatório (criado) |
| `docs/relatorios/RELATORIO_QA_*` | Relatórios QA do ciclo (não tocados) |
| `tela/__pycache__/` | Cache Python (irrelevante) |

---

## 3. Arquivos modificados

| Arquivo | Natureza da alteração |
|---|---|
| `tela/loader.py` | `_validar_grupo` reescrita com recursão e rastreamento de profundidade; `_validar_distribuicao_corpo` parametrizada com `prefixo_caminho` (patch ACH-005) |
| `tela/modelo.py` | `_construir_elementos_recursivo` adicionada; `construir_modelo` atualizado; docstrings de escopo plano adicionadas |
| `tela/renderizador.py` | `_renderizar_container`, `_renderizar_container_vertical`, `_renderizar_container_horizontal` adicionadas; `renderizar_tela` atualizada; comentário de `_montar_corpo_horizontal` atualizado (patch ACH-006) |
| `tela/teste_loader.py` | 4 testes históricos substituídos; `teste_hierarquia_grupos_adr0019` adicionada (22 verificações); 2 verificações de contexto de caminho adicionadas (patch ACH-005) |
| `tela/teste_modelo.py` | `teste_hierarquia_grupos_adr0019_modelo` adicionada (25 verificações) |
| `tela/teste_renderizador.py` | `TestHierarquiaGruposH0027` adicionada com 16 métodos originais + 3 novos métodos (patch ACH-001) |

---

## 4. Decisões D1–D7 — implementação por módulo

### D1 — Profundidade contada somente por nós `grupo`
**Loader:** `_validar_grupo` recebe `nivel_grupo` (inteiro, raiz=1). O parâmetro incrementa apenas quando o filho é do tipo `"grupo"`. Tipos funcionais (`console`, `lancador`, `dashboard`) não incrementam o nível.

### D2 — Máximo de 3 níveis de grupos; nível 4 é inválido
**Loader:** quando `nivel_grupo == 3` e um filho é `"grupo"`, lança `TelaGrupoInvalido` antes de descer. Mensagem inclui o `id` do grupo ofensor, o caminho completo (`caminho_grupo`) e explicita o máximo de 3 níveis.

### D3 — Múltiplos filhos por container sem restrição de cardinalidade
**Loader:** `_validar_grupo` itera sobre todos os filhos sem contar. **Modelo:** `_construir_elementos_recursivo` constrói todos os filhos da lista raw. **Renderizador:** `_renderizar_container_vertical` e `_renderizar_container_horizontal` iteram sobre todos os `elementos`.

### D4 — Mensagem de erro determinística para nível 4
**Loader:** mensagem fixa no formato `"Grupo '{id}' em '{caminho}' criaria nivel 4 de grupo, que e invalido; maximo e 3 niveis de grupos (ADR-0019 D4)"`. Testado por dupla execução com mesma entrada — saídas iguais confirmadas.

### D5 — Múltiplos grupos irmãos permitidos em qualquer nível
**Loader:** ausência de verificação de unicidade de tipo `"grupo"` entre irmãos. **Modelo:** `_construir_elementos_recursivo` processa todos independentemente de tipo.

### D6 — Múltiplos elementos funcionais dentro de um grupo são válidos
**Loader:** regra antiga `TelaGrupoInvalido` para grupo com mais de 1 elemento removida. Agora qualquer quantidade ≥ 1 é válida (mínimo 1 já era obrigatório pela verificação de lista não-vazia).

### D7 — Sem limite global de dashboards por tela
**Loader:** verificação de cardinalidade de `dashboard` removida. **Renderizador:** renderiza cada instância independentemente.

---

## 5. Alterações por módulo

### 5.1 `tela/loader.py`

**`_validar_distribuicao_corpo`** — parametrizada com `prefixo_caminho="corpo"` (patch ACH-005):
- Todas as mensagens de erro substituem `"corpo.distribuicao"` por `"{prefixo_caminho}.distribuicao"`
- Default `"corpo"` preserva comportamento anterior para chamadas do corpo raiz
- Chamada de `_validar_grupo` passa `caminho_grupo` como prefixo, produzindo mensagens como `"corpo → g1.distribuicao.modo invalido"` em vez de `"corpo.distribuicao.modo invalido"` (diagnóstico correto do container afetado)

**`_validar_grupo`** — refatorada de função plana para recursiva:

```python
def _validar_grupo(elemento, id_grupo, nivel_grupo=1, caminho="corpo"):
```

- Valida `arranjo` (aceita `None` e todos os arranjos do corpo)
- `caminho_grupo` calculado antes de validar `distribuicao` para uso como prefixo de caminho
- Valida `distribuicao` quando presente (reutiliza `_validar_distribuicao_corpo` com `caminho_grupo`)
- Itera sobre filhos:
  - Se `tipo == "grupo"` e `nivel_grupo == 3`: lança `TelaGrupoInvalido` (D4)
  - Se `tipo == "grupo"` e `nivel_grupo < 3`: chama `_validar_grupo(item, id_item, nivel_grupo + 1, caminho_grupo)`
  - Se tipo funcional válido: passa sem ação
  - Tipo desconhecido: lança `TelaTipoDesconhecido`

O sítio de chamada em `carregar_tela` permanece inalterado: `_validar_grupo(elemento, id_elemento)` — defaults aplicam.

### 5.2 `tela/modelo.py`

**`_construir_elementos_recursivo(elementos_raw, id_pai)`** — nova função de módulo:
- Para `tipo == "grupo"`: constrói `ElementoCorpo` com `elementos=_construir_elementos_recursivo(sub_raw, sub_id)` e `_campos_inertes` contendo todos os campos exceto `id`, `tipo`, `elementos` (preserva `arranjo` e `distribuicao` para o renderizador)
- Para tipos funcionais: constrói `ElementoCorpo` com `_campos_inertes` contendo todos os campos exceto `id` e `tipo`

**`construir_modelo`** — bloco `if tipo == "grupo"` atualizado para chamar `_construir_elementos_recursivo` em vez do código inline anterior.

**`elemento_por_id` e `elementos_por_tipo`** — docstrings atualizadas para declarar explicitamente o escopo plano como limitação documentada (H-0027).

### 5.3 `tela/renderizador.py`

**`_renderizar_container(arranjo, distribuicao, elementos, borda, total_w, altura_disponivel)`** — dispatcher principal recursivo:
- `"sobreposto"` e `None` → alias de `"vertical"`
- `"lado_a_lado"` → alias de `"horizontal"`
- Delega para `_renderizar_container_vertical` ou `_renderizar_container_horizontal`

**`_renderizar_container_vertical(distribuicao, elementos, borda, total_w, inner_w, content_w, label_max, altura_disponivel)`**:
- Com `distribuicao` e `altura_disponivel`: distribui alturas por `_distribuir_alturas`; cada filho de tipo `"grupo"` é despachado recursivamente via `_renderizar_container`; cada funcional recebe `altura_alvo=cota`
- Sem distribuição ou sem altura: construção orientada pelo conteúdo (content-driven, ADR-0018)

**`_renderizar_container_horizontal(distribuicao, elementos, borda, total_w, altura_disponivel, larguras=None)`**:
- Calcula larguras por distribuição, uniforme ou argumento externo
- Cada filho de tipo `"grupo"` é despachado recursivamente
- Normaliza altura entre colunas; aplica fill horizontal interno

**Comentário de `_montar_corpo_horizontal`** atualizado (patch ACH-006): o comentário que afirmava `"Grupo não é expandido (ADR-0015 D2): conta como slot com área visualmente vazia."` foi substituído por texto que deixa claro que a função é preservada como exportada histórica e que o caminho principal usa `_renderizar_container` desde H-0027, que expande grupos recursivamente.

**`renderizar_tela`** — seção de corpo substituída:
```python
bloco_corpo = _renderizar_container(
    arranjo_corpo, distribuicao_corpo,
    modelo.corpo.elementos, borda, total_w, l_corpo_disponivel,
)
```
Flag `_corpo_vertical_distribuido` preservada para controlar fill externo.

---

## 6. Testes

### Testes históricos substituídos (`teste_loader.py`)

Os 4 testes em `teste_grupo_estrutural` que esperavam `TelaGrupoInvalido` para comportamentos agora válidos foram substituídos por testes positivos:

| Antes | Depois |
|---|---|
| "grupo com 2 elementos → TelaGrupoInvalido" | "grupo com 2 funcionais é válido (D6)" |
| "grupo dentro de grupo → TelaGrupoInvalido" | "nivel 1→2 é válido (D2)" |
| "grupo com arranjo 'horizontal' → TelaGrupoInvalido" | "arranjo horizontal é válido (D5)" |
| "grupo com arranjo 'lado_a_lado' → TelaGrupoInvalido" | "arranjo lado_a_lado é válido (D5)" |

### Novos testes adicionados (implementação original H-0027)

**`teste_hierarquia_grupos_adr0019` (loader — seção 20.2):** 22 verificações cobrindo nível 1 com 1/2 funcionais, 2 níveis, 3 níveis, 3 níveis com múltiplos funcionais, rejeição de nível 4 + mensagem determinística (4 sub-verificações), múltiplos irmãos nos níveis 1 e 2, mistura grupo+funcional, arranjo vertical/ausente, distribuição `igual`/`percentual`/`fracao`, vetor errado → `TelaEstruturaInvalida`, modo inválido → `TelaEstruturaInvalida`, múltiplos dashboards, arranjo inválido `"diagonal"` → `TelaGrupoInvalido`.

**`teste_hierarquia_grupos_adr0019_modelo` (modelo — seção 20.3):** 25 verificações cobrindo árvore de 2 e 3 níveis (incluindo verificação de `_campos_inertes` com `arranjo` e `distribuicao` em cada nível), múltiplos filhos de grupo, escopo plano de `elemento_por_id` e `elementos_por_tipo` (4 verificações + navegação direta).

**`TestHierarquiaGruposH0027` (renderizador — seção 20.4):** 16 métodos originais (~35 verificações) cobrindo grupo nível 1 vertical, grupo nível 1 horizontal (lado a lado), arranjo `None` equivalente a vertical, 2 níveis verticais, 2 níveis vertical+horizontal, 3 níveis (profundidade máxima v→v→v), distribuição `igual` com e sem altura, distribuição `fracao` em grupo horizontal, mistura grupo+funcional no corpo, múltiplos dashboards (D7), regressão `orquestrador.json`, regressão `grupo_minimo.json`, distribuição `percentual` 70/30 com altura, alias `sobreposto`, alias `lado_a_lado`, grupo vazio sem exceção.

### Novos testes adicionados pelo patch ACH-001

**`test_corpo_horizontal_com_grupos_filhos` (renderizador):** 7 verificações.
- Cenário: corpo horizontal com dois grupos filhos (`g1` vertical e `g2` vertical)
- Valida: saída não vazia, `ALFA` presente, `BETA` presente, `ALFA` e `BETA` na mesma linha, grupos não são slots vazios, largura total 42 preservada, saída determinística

**`test_horizontal_grupo_vertical` (renderizador):** 7 verificações.
- Cenário: corpo horizontal com grupo vertical interno (`g1` vertical com `CIMA` e `BAIXO`)
- Valida: saída não vazia, `CIMA` presente, `BAIXO` presente, ordem vertical preservada (`CIMA` antes de `BAIXO`), ausência de achatamento (linhas distintas), ausência de slot vazio, largura total 42 preservada

**`test_tres_niveis_arranjos_alternados` (renderizador):** 10 verificações.
- Cenário: corpo vertical → g1 horizontal → g2 vertical → g3 horizontal → `FA` e `FB`; com `TOPO` como funcional direto de g1
- Usa `largura=80` para garantir área suficiente nos três níveis de particionamento horizontal sem truncamento de título
- Valida: saída não vazia, `FA` e `FB` presentes (funcionais nível 3), `TOPO` presente (funcional nível 1), `FA` e `FB` na mesma linha (g3 horizontal), ausência de achatamento, largura 80 preservada, determinismo, ordem declarada (`FA` à esquerda de `FB`), existência dos três níveis

### Novas verificações adicionadas pelo patch ACH-005

**2 verificações em `teste_loader.py`** (após o teste `"grupo com distribuicao.modo invalido"`):
- `ACH-005: mensagem de dist em grupo contem caminho do grupo ('corpo → g1')` — verifica que o caminho do grupo aparece na mensagem
- `ACH-005: mensagem de dist em grupo NAO usa 'corpo.distribuicao' isolado` — verifica que a mensagem não se refere ao corpo raiz

### Resultados finais pós-patch

| Suite | Código de saída | Verificações | Passaram | Falharam |
|---|---|---|---|---|
| `python tela/teste_loader.py` | 0 | 129 | 129 | 0 |
| `python tela/teste_modelo.py` | 0 | 81 | 81 | 0 |
| `python tela/teste_renderizador.py` | 0 | 491 | 491 | 0 |
| `python tela/teste_demo.py` | 0 | 303 | 303 | 0 |
| `git diff --check` | 0 | — | — | — |

**Total: 1004 verificações; 1004 aprovadas; 0 falhas.**

---

## 7. Compatibilidade retroativa preservada

- `_montar_corpo_horizontal`: mantida sem alteração funcional (ainda exportada e testada diretamente); apenas o comentário interno foi atualizado
- `renderizar_tela` com `orquestrador.json` e `grupo_minimo.json`: saídas preservadas (verificadas por testes de regressão)
- Flag `_corpo_vertical_distribuido`: lógica de fill externo preservada
- `elemento_por_id` e `elementos_por_tipo`: comportamento de escopo plano inalterado (limitação documentada, não bug)
- `_validar_distribuicao_corpo` com default `prefixo_caminho="corpo"`: chamadas do corpo raiz produzem mensagens idênticas às anteriores

---

## 8. Estado Git final após o patch

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       |  27 +-
 scripts/docs/adr/ADR-0007-tela-processamento-composicao.md |  15 +-
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md |  40 +-
 scripts/docs/contratos/contrato_json_tela_minima.md |   7 +-
 scripts/docs/contratos/contrato_tela_json.md       |  15 +-
 scripts/tela/loader.py                             | 165 +++---
 scripts/tela/modelo.py                             | 106 ++--
 scripts/tela/renderizador.py                       | 297 ++++++----
 scripts/tela/teste_loader.py                       | 460 +++++++++++++--
 scripts/tela/teste_modelo.py                       | 185 ++++++
 scripts/tela/teste_renderizador.py                 | 621 +++++++++++++++++++++
 12 files changed, 1669 insertions(+), 270 deletions(-)

git diff --check
(sem saída — sem conflitos de espaço em branco)

git diff --cached --stat
(sem saída — stage vazio)

git diff --cached --name-only
(sem saída — stage vazio)
```

### 8.1 Classificação das alterações no estado final

Os mesmos 12 arquivos rastreados modificados do estado inicial continuam modificados. O patch acrescentou mais linhas nos arquivos de código da implementação (`loader.py`, `renderizador.py`, `teste_loader.py`, `teste_renderizador.py`). Nenhum novo arquivo rastreado foi criado pelo patch. O conjunto de arquivos não rastreados é o mesmo do início, acrescido de `RELATORIO_QA_H-0027_IMPLEMENTACAO.md` (criado durante o QA, não tocado pelo patch).

| Comparação | Estado |
|---|---|
| Commit-base | `40015b6` (inalterado — patch não commitado) |
| Stage | Vazio |
| `git diff --check` | Limpo |
| Novos arquivos criados pelo patch | Nenhum |
| Arquivos proibidos alterados | Nenhum |

---

## 9. Bloqueios encontrados

Nenhum bloqueio encontrado durante a implementação (`BLOCKED_REPOSITORY_STATE`, `ARCHITECTURE_REVIEW_REQUIRED` e `BLOCKED_SCOPE` não ocorreram).

---

## 10. Limitações conhecidas

- `elemento_por_id` e `elementos_por_tipo` têm escopo plano: percorrem somente `corpo.elementos` diretos, sem descer na árvore de grupos. Esta é uma limitação documentada (H-0027), não um bug. A navegação direta via `elemento.elementos` permanece disponível.
- `tela/teste_demo.py` não foi modificado pelo patch (não era necessário — a suíte passou em 303/303 sem alteração).
