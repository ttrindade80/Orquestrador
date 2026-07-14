---
name: H-0014-migracao-pos-adr-arranjo-barra-declarativa
description: Handoff de implementação/migração — alinha grupo_minimo a arranjo vertical (ADR-0011) e reduz barra_de_menus do Orquestrador a chips aplicáveis (ADR-0012); sem nova capacidade de composição
metadata:
  type: handoff_implementacao
  status: HANDOFF_READY
  id: H-0014
  data_criacao: 2026-07-08
rastreabilidade:
  adrs_aplicadas:
    - docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
    - docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
  handoffs_anteriores:
    - docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
    - docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
  commit_base: ceaf0be
  handoffs_cancelados:
    - docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
---

# H-0014 — Migração pós-ADR: arranjo vertical e barra declarativa

## Status

`HANDOFF_READY`

---

## Metadados de rastreabilidade

| Campo | Valor |
|---|---|
| ID | H-0014 |
| Data de criação | 2026-07-08 |
| HEAD base | `ceaf0be` |
| Handoffs anteriores aprovados | H-0012 (QA_APPROVED_WITH_NOTES), H-0013 (aprovado) |
| ADRs aplicadas | ADR-0011, ADR-0012 |
| Commit base | `ceaf0be` — docs: registra ADRs de arranjo e barra declarativa |
| Sequência futura | H-0015 — Grupo estrutural com 2 elementos em arranjo vertical |

---

## Ordem de autoridade

Este handoff segue a hierarquia do `contrato_processo_desenvolvimento.md`:

1. Contrato de processo
2. ADRs aceitas (ADR-0011, ADR-0012)
3. Contratos de módulo
4. **Este handoff**
5. Relatório de implementação

Qualquer contradição entre este handoff e um contrato ou ADR deve ser reportada
como `ARCHITECTURE_REVIEW_REQUIRED`. O handoff não pode sobrescrever contrato.

---

## Contexto

Os handoffs H-0012 e H-0013 foram implementados e commitados. A base está limpa
em `ceaf0be`. O sistema entrega:

- `config/telas/grupo_minimo.json` — tela com grupo estrutural contendo 1 dashboard.
- `config/telas/orquestrador.json` — tela raiz com lançador apontando para `destino_minimo`
  e `grupo_minimo`.
- Suporte completo ao tipo `"grupo"` em `loader.py`, `modelo.py` e `renderizador.py`.
- Fluxo demonstrável: `g → grupo_minimo`, `d → destino_minimo`, `b` alterna borda,
  Esc volta/sai.

**Problema de terminologia**: `grupo_minimo.json` usa `"arranjo": "sobreposto"` em dois
campos (`corpo.arranjo` e `grupo_principal.arranjo`). A ADR-0011 (aceita em 2026-07-08)
define que `"vertical"` é o valor canônico final de arranjo e que `"sobreposto"` é alias
transicional. Novos handoffs (a partir de H-0014) devem usar `"vertical"`.

**Problema de chips**: `orquestrador.json` declara 11 chips em `barra_de_menus.chips[]`.
A ADR-0012 define que cada tela declara apenas chips aplicáveis. Dos 11 chips atuais,
9 referenciam capacidades não implementadas no ciclo atual (paginação, colunas, filtro de
grupo, alternância de foco, navegação por `[✥]`, seleção, enter, estilo, verboso). Apenas
`[Esc] Sair` e `[?] Ajuda` são aplicáveis.

**Decisão gerencial**: antes de implementar grupo com 2 elementos (H-0015), migrar a base
existente para que o código corrente não carregue terminologia e barra antigas. Este ciclo
é de migração pura — sem nova capacidade de composição.

---

## Objetivo

Alinhar a base existente às decisões ADR-0011 e ADR-0012, sem adicionar nova
capacidade de composição:

1. `grupo_minimo.json` passa a usar `arranjo: "vertical"` como valor canônico.
2. `loader.py` (`_validar_grupo`) reflete ADR-0011: rejeita `"horizontal"` (e seu alias
   `"lado_a_lado"`) como arranjo de grupo fora de escopo; remove referência histórica ao H-0012.
3. `orquestrador.json` reduz `barra_de_menus.chips[]` de 11 para 2 chips aplicáveis.
4. Testes são atualizados para refletir `"vertical"` e os 2 chips do Orquestrador —
   sem exigir conjunto global canônico.
5. Fluxo demonstrável do H-0013 é preservado intacto.

---

## Leitura obrigatória realizada

O preparador deste handoff leu e analisou:

```
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
docs/adr/INDICE_ADR.md

docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_processo_desenvolvimento.md

docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md

docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
docs/relatorios/RELATORIO_QA_H-0012_GRUPO_ESTRUTURAL_MINIMO_TELA_ISOLADA.md
docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md
docs/relatorios/RELATORIO_QA_H-0013_DEMO_ACESSO_TELA_GRUPO_MINIMO.md
docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md

config/telas/orquestrador.json
config/telas/grupo_minimo.json
config/telas/destino_minimo.json

tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

---

## Decisões técnicas explicitadas

### Arranjo

```
- "vertical" é o valor canônico de arranjo para grupo_minimo (corpo e grupo).
- grupo_minimo.json deve usar arranjo: "vertical" nos campos:
    corpo.arranjo                → "vertical"
    grupo_principal.arranjo      → "vertical"
- "sobreposto" não deve aparecer em grupo_minimo.json após a migração.
- orquestrador.json, destino_minimo.json e stub_b.json mantêm "sobreposto"
  como valor legado (fora do escopo de migração deste ciclo);
  esses JSONs não são alterados neste handoff.
- O loader não valida vocabulário de corpo.arranjo no nível macro —
  "sobreposto" nos outros JSONs continua preservado inertamente.
  Esta não-validação é intencional e não deve ser alterada neste ciclo.
- "horizontal" não é implementado neste ciclo.
```

**Decisão sobre alias transicional `sobreposto` em grupo**:
Não é necessário preservar `sobreposto` como alias no grupo. O único JSON de
grupo (`grupo_minimo.json`) está sendo migrado diretamente para `"vertical"`.
Não há grupo ativo com `sobreposto` após a migração. Portanto, **não é
necessário implementar normalização de alias no loader**.

**Decisão sobre `_validar_grupo` no loader**:
O invariante atual rejeita `arranjo == "lado_a_lado"`. Após ADR-0011, o termo
canônico do conceito rejeitado é `"horizontal"`. O loader deve passar a rejeitar
`"horizontal"` (termo final) **e** `"lado_a_lado"` (alias transicional). Ambos
são fora de escopo para grupo no H-0014. A referência histórica ao H-0012 na
mensagem de erro deve ser atualizada para H-0014 com linguagem da ADR-0011.

### barra_de_menus

```
- barra_de_menus do Orquestrador declara apenas chips aplicáveis ao ciclo atual.
- Chips aplicáveis ao Orquestrador no ciclo atual:
    chip_esc   [Esc] Sair   — implementado (Esc sai da tela raiz)
    chip_ajuda [?]   Ajuda  — declarado "sempre"; presente em todas as
                              telas mínimas (destino_minimo, grupo_minimo)
- Chips a remover (referenciam capacidades não implementadas):
    chip_paginas    [<>] Páginas    — paginação não implementada
    chip_colunas    [-+] Colunas    — ajuste de colunas não implementado
    chip_grupos     [#]  Grupos     — filtro de grupo não implementado
    chip_alternar   [⇆] Alternar   — alternância de foco não implementada
    chip_navegar    [✥] Navegar    — navegação por [✥] não implementada
    chip_selecionar [␣] Selecionar — seleção não implementada
    chip_enter      [⏎] Todos      — ação enter não implementada
    chip_estilo     [|]  Estilo    — tela de estilo não definida/implementada
    chip_verboso    [V]  Verboso    — modo verboso não implementado
- O renderer não gera chips próprios — lê barra_de_menus.chips[] declarado.
  Essa propriedade já existe e não exige alteração de código.
- Testes devem esperar exatamente os chips declarados no JSON —
  sem exigir conjunto global canônico obrigatório.
- "g" e "d" são itens do lançador (corpo), não chips de barra_de_menus.
  Não devem ser adicionados como chips de barra.
- "b" é controle interno de demo.py — não é chip de barra_de_menus.
```

**Sobre `filtros`, `bindings` e `referencias_de_acoes`**:
Esses campos de `orquestrador.json` não fazem parte do escopo deste handoff.
**Não remover** `filtros`, `bindings` nem `referencias_de_acoes` do JSON do
Orquestrador. Apenas `barra_de_menus.chips[]` deve ser reduzido.

### Demo

O fluxo demonstrável do H-0013 deve ser preservado intacto:

```
- python tela/demo.py é o ponto de entrada.
- "g" abre grupo_minimo.
- "d" abre destino_minimo.
- "b" alterna borda (curva ↔ reta).
- Esc em destino_minimo volta ao Orquestrador.
- Esc em grupo_minimo volta ao Orquestrador.
- Esc no Orquestrador (pilha vazia) sai.
```

`demo.py` é **proibido** neste ciclo. O fluxo acima já funciona; nenhuma
alteração de código de módulo é necessária para preservá-lo.

---

## Escopo positivo

O H-0014 deve implementar **apenas** o seguinte:

### 1. Alterar `config/telas/grupo_minimo.json`

Migrar dois campos de `"sobreposto"` para `"vertical"`:

```json
"corpo": {
  "arranjo": "vertical",   ← era "sobreposto"
  "elementos": [
    {
      "id": "grupo_principal",
      "tipo": "grupo",
      "arranjo": "vertical",  ← era "sobreposto"
      ...
    }
  ]
}
```

Nenhum outro campo do JSON deve ser alterado.

### 2. Alterar `config/telas/orquestrador.json`

Reduzir `barra_de_menus.chips[]` de 11 chips para exatamente 2:

```json
"barra_de_menus": {
  "distribuicao": "horizontal",
  "chips": [
    {
      "id": "chip_esc",
      "tipo": "acao",
      "tecla": "Esc",
      "texto": "Sair",
      "acao": { ... },
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
```

Os 9 chips removidos são: `chip_paginas`, `chip_colunas`, `chip_grupos`,
`chip_alternar`, `chip_navegar`, `chip_selecionar`, `chip_enter`, `chip_estilo`,
`chip_verboso`. Os campos `chip_esc` e `chip_ajuda` devem ser copiados da
declaração atual sem alteração de seus campos internos.

Não remover `filtros`, `bindings`, `referencias_de_acoes` nem nenhum outro campo
top-level do JSON — apenas `barra_de_menus.chips[]` é reduzido.

### 3. Alterar `tela/loader.py`

Atualizar `_validar_grupo` para refletir ADR-0011:

**Antes:**
```python
if arranjo == "lado_a_lado":
    raise TelaGrupoInvalido(
        "Grupo '{0}' com arranjo 'lado_a_lado' e fora de escopo no "
        "H-0012".format(id_grupo)
    )
```

**Depois:**
```python
if arranjo in ("horizontal", "lado_a_lado"):
    raise TelaGrupoInvalido(
        "Grupo '{0}' com arranjo '{1}' e fora de escopo no H-0014 "
        "(arranjo horizontal nao implementado para grupo; "
        "'lado_a_lado' e alias transicional de 'horizontal' — ADR-0011)".format(
            id_grupo, arranjo
        )
    )
```

Apenas esta alteração em `_validar_grupo`. Nenhuma outra mudança em `loader.py`.

### 4. Alterar `tela/teste_loader.py`

Atualizar casos que referenciam `grupo_minimo` com `"sobreposto"`:

- Qualquer JSON fabricado de grupo com `arranjo: "sobreposto"` em casos de caminho
  válido deve mudar para `arranjo: "vertical"`.
- O caso de rejeição de grupo com `arranjo: "lado_a_lado"` deve ser atualizado
  (ou complementado) para testar rejeição de `arranjo: "horizontal"` como o
  caso primário da ADR-0011. O caso de `"lado_a_lado"` pode ser mantido como
  teste secundário de alias transicional ou substituído pelo de `"horizontal"`.
- Verificar se há asserção explícita sobre o valor `corpo.arranjo == "sobreposto"`
  para a tela `grupo_minimo`; se houver, mudar para `"vertical"`.
- Manter todos os casos existentes de Orquestrador, destino_minimo e stub_b
  sem alteração (esses JSONs ainda usam `sobreposto` — nenhuma quebra esperada).

### 5. Alterar `tela/teste_modelo.py`

- Verificar se há asserção explícita sobre `modelo.corpo.arranjo == "sobreposto"`
  para a tela `grupo_minimo`; se houver, mudar para `"vertical"`.
- Verificar se há JSON fabricado de grupo com `arranjo: "sobreposto"` em casos
  positivos; se houver, mudar para `"vertical"`.
- Manter todos os casos existentes de Orquestrador e demais telas sem alteração.

### 6. Alterar `tela/teste_renderizador.py`

**Atualização obrigatória — `_EXPECTED_ORQUESTRADOR` e `_EXPECTED_ORQUESTRADOR_RETA`**:

As constantes que contêm os 11 chips da barra do Orquestrador devem ser reduzidas
a 2 chips. O bloco `Menus` passa de 11 linhas de chip para 2 linhas:

```python
# Seção Menus nas constantes — após migração (largura 42):
"╭ Menus ─────────────────────────────────╮\n"
"│ [Esc] Sair                             │\n"
"│ [?] Ajuda                              │\n"
"╰────────────────────────────────────────╯\n"
```

O executor deve derivar as strings exatas executando `renderizar_tela` sobre o
modelo do Orquestrador após a atualização do JSON, usando a largura correspondente.
Não calcular padding manualmente.

**Atualização condicional — testes explícitos de chips**:

Se o arquivo contiver verificações explícitas como:
- `"saida contem '[<>] Páginas'"` — remover ou marcar como não mais esperado
- `"saida contem '[✥] Navegar'"` — idem
- Qualquer asserção de presença dos 9 chips removidos — remover essas asserções

Testes de **ausência** como `"'[B] Borda' nao aparece"` devem ser mantidos.

**Atualização condicional — modelos fabricados**:

Se houver modelos fabricados com `arranjo: "sobreposto"` em contexto de grupo
(não de corpo plano), atualizar para `"vertical"`. Modelos fabricados para
testar o corpo plano do Orquestrador não precisam mudar (o Orquestrador ainda
usa `sobreposto` neste ciclo).

### 7. Alterar `tela/teste_demo.py`

Atualizar todas as constantes de expected output que incluem os chips do Orquestrador:

- `_EXPECTED_CURVA` (largura 80) — bloco Menus de 11 chips → 2 chips
- `_EXPECTED_RETA` (largura 80) — idem
- `_EXPECTED_DIAGNOSTICO_CURVA_42` (largura 42) — idem
- `_EXPECTED_GRUPO_MINIMO_CURVA_80` e correlatas — verificar se incluem saída do
  Orquestrador; se não, não alterar

O executor deve derivar as strings exatas executando `renderizar_tela` sobre o
modelo atualizado. Não calcular padding manualmente.

Manter todos os casos de navegação (`g → grupo_minimo`, `d → destino_minimo`,
Esc, `b`) funcionando. A alteração de chips não afeta o fluxo de navegação.

### 8. Alterar `tela/teste_diagnostico.py`

Atualizar `_EXPECTED_ORQUESTRADOR` para refletir os 2 chips do Orquestrador
(antes tinha 11). A estrutura é a mesma; apenas o bloco Menus fica menor.

O executor deve derivar a string exata via `renderizar_tela` ou via `diagnostico.py`.

### 9. Criar `docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md`

Relatório de implementação conforme o padrão do projeto. Ver seção de relatório.

---

## Escopo negativo

O executor **não deve** implementar nada além do escopo positivo acima.

```
NÃO adicionar segundo elemento ao grupo.
NÃO implementar grupo com 2 ou mais elementos funcionais.
NÃO implementar arranjo horizontal.
NÃO implementar lado_a_lado como novo caminho.
NÃO implementar aninhamento de grupos.
NÃO implementar distribuição percentual ou fração.
NÃO migrar orquestrador.json para estrutura de grupo hierárquico.
NÃO migrar destino_minimo.json nem stub_b.json de "sobreposto" para "vertical".
NÃO remover "sobreposto" de orquestrador.json, destino_minimo.json ou stub_b.json.
NÃO adicionar validação de vocabulário para corpo.arranjo no nível macro do loader.
NÃO remover filtros, bindings ou referencias_de_acoes de orquestrador.json.
NÃO criar novo tipo funcional.
NÃO criar novo mecanismo de chip.
NÃO criar registry de qualquer tipo.
NÃO implementar console real.
NÃO implementar foco.
NÃO implementar seleção.
NÃO implementar navegação por [✥].
NÃO alterar tela/demo.py.
NÃO alterar tela/modelo.py (se não houver alteração necessária após análise).
NÃO alterar tela/renderizador.py (se não houver alteração necessária após análise).
NÃO alterar tela/diagnostico.py.
NÃO alterar docs/adr/.
NÃO alterar docs/contratos/.
NÃO alterar docs/NOMENCLATURA.md.
NÃO alterar docs/INDICE.md.
NÃO alterar docs/handoff/ (exceto o próprio H-0014 já criado e o relatório IMP-0014).
NÃO usar letras na numeração de handoffs.
NÃO reabrir H-0011.
NÃO recriar H-0011A.
NÃO fazer commit.
```

---

## Especificação funcional por módulo

### F-1. `config/telas/grupo_minimo.json` — ALTERAR

Dois campos mudam:

| Campo | Antes | Depois |
|---|---|---|
| `corpo.arranjo` | `"sobreposto"` | `"vertical"` |
| `corpo.elementos[0].arranjo` (grupo_principal) | `"sobreposto"` | `"vertical"` |

Todos os demais campos permanecem idênticos. O JSON deve continuar válido e
carregável pelo loader sem qualquer outra alteração.

### F-2. `config/telas/orquestrador.json` — ALTERAR

Campo `barra_de_menus.chips[]` muda de 11 entradas para 2:

| Ação | id | tecla | texto |
|---|---|---|---|
| MANTER | `chip_esc` | `Esc` | `Sair` |
| MANTER | `chip_ajuda` | `?` | `Ajuda` |
| REMOVER | `chip_paginas` | `<>` | `Páginas` |
| REMOVER | `chip_colunas` | `-+` | `Colunas` |
| REMOVER | `chip_grupos` | `#` | `Grupos` |
| REMOVER | `chip_alternar` | `⇆` | `Alternar` |
| REMOVER | `chip_navegar` | `✥` | `Navegar` |
| REMOVER | `chip_selecionar` | `␣` | `Selecionar` |
| REMOVER | `chip_enter` | `⏎` | `Todos` |
| REMOVER | `chip_estilo` | `|` | `Estilo` |
| REMOVER | `chip_verboso` | `V` | `Verboso` |

Copiar os dois objetos de chip preservados da declaração atual sem
alterar nenhum de seus campos internos (incluindo campos `acao` e `nota`).

### F-3. `tela/loader.py` — ALTERAR (somente `_validar_grupo`)

A única mudança é na validação de `arranjo` dentro do grupo. O código deve:
- Rejeitar `"horizontal"` (novo termo canônico — ADR-0011).
- Rejeitar `"lado_a_lado"` (alias transicional de `"horizontal"` — ADR-0011).
- Atualizar a mensagem de erro para citar ADR-0011 e H-0014.
- Nenhuma outra linha de `loader.py` deve ser alterada.

O executor **não deve** adicionar validação de vocabulário para `corpo.arranjo`
no nível macro (fora do contexto de grupo). O loader deve continuar preservando
inertamente qualquer string em `corpo.arranjo` das telas raiz.

### F-4. `tela/modelo.py` — CONDICIONAL

`modelo.py` preserva o valor de `corpo.arranjo` e `grupo.arranjo` inertamente.
A migração de `grupo_minimo.json` de `"sobreposto"` para `"vertical"` não exige
nenhuma alteração em `modelo.py`.

O executor deve verificar se há algum caso que exija alteração antes de modificar.
Se não houver, **não alterar `modelo.py`**.

### F-5. `tela/renderizador.py` — CONDICIONAL

O renderer não lê `corpo.arranjo` nem `grupo.arranjo` para decisões visuais. A
migração de valor não altera o comportamento visual. A redução de chips em
`orquestrador.json` não exige alteração de código do renderer — ele já lê
`barra_de_menus.get("chips", [])` e percorre o que receber.

O executor deve verificar se há algum caso que exija alteração antes de modificar.
Se não houver, **não alterar `renderizador.py`**.

### F-6. `tela/demo.py` — PROIBIDO

`demo.py` é proibido neste ciclo. O fluxo demonstrável já funciona com o
código existente. A migração de chips e arranjo é puramente declarativa no JSON.
Se a análise sugerir alteração de `demo.py`, parar com `ARCHITECTURE_REVIEW_REQUIRED`.

---

## Arquivos permitidos

Lista explícita e exaustiva. O executor **só pode** criar ou alterar arquivos
desta lista.

### Alterar obrigatório

```
config/telas/grupo_minimo.json
config/telas/orquestrador.json
tela/loader.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

### Alterar condicional (verificar antes de alterar)

```
tela/modelo.py
  Somente se a verificação revelar caso que exija alteração.
  Expectativa: não precisará ser alterado.

tela/renderizador.py
  Somente se a verificação revelar caso que exija alteração.
  Expectativa: não precisará ser alterado.
```

### Criar

```
docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
```

---

## Arquivos proibidos

O executor **não pode** criar nem alterar:

```
docs/adr/
docs/contratos/
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/handoff/
  (exceto o próprio handoff H-0014 já criado antes da implementação
   e o relatório IMP-0014 que o executor deve criar)
config/telas/destino_minimo.json
config/telas/stub_b.json
config/estilo.json
config/lancador.json
config/barra_de_menus.json
config/cabecalho.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json
tela/demo.py
tela/diagnostico.py
tela/__init__.py
qualquer arquivo não listado como permitido acima
```

---

## Critérios de aceite

O executor deve verificar **todos** os itens abaixo. Nenhum item pode ser ignorado.

### Sobre `grupo_minimo.json`

```
CA-01. grupo_minimo.json é JSON sintaticamente válido.
CA-02. grupo_minimo.corpo.arranjo == "vertical".
CA-03. grupo_minimo.corpo.elementos[0].arranjo == "vertical" (grupo_principal).
CA-04. Nenhum campo de grupo_minimo.json usa "sobreposto".
CA-05. Todos os demais campos de grupo_minimo.json permanecem inalterados.
CA-06. carregar_tela(None, "grupo_minimo") carrega sem erro.
```

### Sobre `orquestrador.json`

```
CA-07. orquestrador.json é JSON sintaticamente válido.
CA-08. barra_de_menus.chips[] contém exatamente 2 chips:
       chip_esc ([Esc] Sair) e chip_ajuda ([?] Ajuda).
CA-09. Os 9 chips removidos não aparecem em barra_de_menus.chips[].
CA-10. filtros, bindings e referencias_de_acoes de orquestrador.json
       permanecem inalterados.
CA-11. lancador_principal.itens[] preserva os 2 itens (d → destino_minimo,
       g → grupo_minimo) sem alteração.
CA-12. carregar_tela(None, "orquestrador") carrega sem erro.
```

### Sobre `loader.py`

```
CA-13. O loader rejeita grupo com arranjo: "horizontal" com TelaGrupoInvalido.
CA-14. O loader rejeita grupo com arranjo: "lado_a_lado" com TelaGrupoInvalido.
CA-15. O loader aceita grupo com arranjo: "vertical" sem erro.
CA-16. O loader aceita grupo sem campo arranjo (ausência de arranjo é válida).
CA-17. Nenhuma outra linha de loader.py foi alterada além de _validar_grupo.
```

### Sobre os testes

```
CA-18. Nenhum teste fabricado usa "sobreposto" em contexto de grupo vertical.
CA-19. Testes de grupo refletem arranjo "vertical" onde aplicável.
CA-20. _EXPECTED_ORQUESTRADOR e _EXPECTED_ORQUESTRADOR_RETA em teste_renderizador.py
       refletem apenas 2 chips na seção Menus.
CA-21. Nenhuma asserção em teste_renderizador.py exige presença dos 9 chips removidos.
CA-22. Constantes de expected output do Orquestrador em teste_demo.py refletem 2 chips.
CA-23. _EXPECTED_ORQUESTRADOR em teste_diagnostico.py reflete 2 chips.
CA-24. Nenhum teste exige conjunto global canônico de chips obrigatórios.
```

### Sobre o fluxo demonstrável

```
CA-25. Fluxo do H-0013 preservado:
       - chip "g" continua navegando para grupo_minimo.
       - chip "d" continua navegando para destino_minimo.
       - "b" continua alternando borda.
       - Esc em grupo_minimo volta ao Orquestrador.
       - Esc em destino_minimo volta ao Orquestrador.
       - Esc no Orquestrador (pilha vazia) sai.
```

### Sobre testes automatizados

```
CA-26. python tela/teste_loader.py     → exit 0, sem [FALHOU], sem traceback.
CA-27. python tela/teste_modelo.py     → exit 0, sem [FALHOU], sem traceback.
CA-28. python tela/teste_renderizador.py → exit 0, sem [FALHOU], sem traceback.
CA-29. python tela/teste_demo.py       → exit 0, sem [FALHOU], sem traceback.
CA-30. python tela/teste_diagnostico.py  → exit 0, sem [FALHOU], sem traceback.
CA-31. python -m json.tool config/telas/orquestrador.json → JSON válido.
CA-32. python -m json.tool config/telas/grupo_minimo.json → JSON válido.
```

### Sobre escopo e rastreabilidade

```
CA-33. tela/demo.py não foi alterado (nenhum diff).
CA-34. tela/diagnostico.py não foi alterado (nenhum diff).
CA-35. config/telas/destino_minimo.json não foi alterado.
CA-36. config/telas/stub_b.json não foi alterado.
CA-37. Nenhum contrato em docs/contratos/ foi alterado.
CA-38. Nenhuma ADR em docs/adr/ foi alterada.
CA-39. docs/NOMENCLATURA.md não foi alterado.
CA-40. Nenhum arquivo fora da lista de permitidos foi criado ou alterado.
CA-41. docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
       foi criado pelo executor.
CA-42. Nenhum commit foi realizado pelo executor.
CA-43. Nenhuma nova capacidade de composição foi introduzida.
```

---

## Comandos obrigatórios de verificação

O executor deve executar **todos** os comandos abaixo.

### Validade dos JSONs alterados

```bash
python -m json.tool config/telas/grupo_minimo.json >/dev/null && echo "grupo_minimo.json OK"
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

### JSONs não alterados (integridade)

```bash
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
```

### Testes automatizados

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
```

Todos devem encerrar com código de saída 0, sem linhas `[FALHOU]` e sem traceback.

### Verificação de migração de arranjo

```bash
python -c "
import sys, json
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from tela.loader import carregar_tela
raw = carregar_tela(None, 'grupo_minimo')
arranjo_corpo = raw['corpo']['arranjo']
arranjo_grupo = raw['corpo']['elementos'][0].get('arranjo')
print('corpo.arranjo:', arranjo_corpo)
print('grupo.arranjo:', arranjo_grupo)
assert arranjo_corpo == 'vertical', 'FALHOU: corpo.arranjo nao e vertical'
assert arranjo_grupo == 'vertical', 'FALHOU: grupo.arranjo nao e vertical'
print('OK — arranjo vertical confirmado')
"
```

### Verificação de chips do Orquestrador

```bash
python -c "
import sys, json
sys.dont_write_bytecode = True
from pathlib import Path
raw = json.loads(Path('config/telas/orquestrador.json').read_text(encoding='utf-8'))
chips = raw['barra_de_menus']['chips']
teclas = [c['tecla'] for c in chips]
print('chips:', teclas)
assert len(chips) == 2, 'FALHOU: esperado 2 chips, encontrado {}'.format(len(chips))
assert teclas == ['Esc', '?'], 'FALHOU: chips incorretos: {}'.format(teclas)
print('OK — 2 chips aplicáveis confirmados')
"
```

### Verificação de rejeição de horizontal no grupo

```bash
python -c "
import sys
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from tela.loader import TelaGrupoInvalido, carregar_tela
import json, tempfile
from pathlib import Path as P

base = P(tempfile.mkdtemp())
(base / 'config' / 'telas').mkdir(parents=True)
tela_h = {
  'schema': 'tela.v1', 'id': 'grupo_h',
  'cabecalho': {'titulo': 'Teste'},
  'corpo': {
    'arranjo': 'vertical',
    'elementos': [{
      'id': 'g1', 'tipo': 'grupo', 'arranjo': 'horizontal',
      'elementos': [{'id': 'e1', 'tipo': 'dashboard'}]
    }]
  },
  'barra_de_menus': {'distribuicao': 'horizontal', 'chips': []}
}
(base / 'config' / 'telas' / 'grupo_h.json').write_text(json.dumps(tela_h), encoding='utf-8')
try:
    carregar_tela(base, 'grupo_h')
    print('FALHOU: nao levantou TelaGrupoInvalido para horizontal')
except TelaGrupoInvalido as e:
    print('OK — horizontal rejeitado:', e)
"
```

### Verificação de preservação da demo (subprocess)

```bash
python -c "
import subprocess, sys, os
env = {k: v for k, v in os.environ.items() if k != 'COLUMNS'}
p = subprocess.run(
    [sys.executable, 'tela/demo.py'],
    cwd='.',
    input='g\n\x1b\n\x1b\n',
    capture_output=True, text=True, env=env
)
print('exit:', p.returncode)
print('GRUPO MINIMO no stdout:', 'GRUPO MINIMO' in p.stdout)
print('Esc Voltar no stdout:', '[Esc] Voltar' in p.stdout)
print('Esc Sair no stdout (orquestrador):', '[Esc] Sair' in p.stdout)
print('stderr vazio:', p.stderr == '')
assert p.returncode == 0, 'FALHOU: exit != 0'
assert 'GRUPO MINIMO' in p.stdout, 'FALHOU: GRUPO MINIMO nao encontrado'
assert p.stderr == '', 'FALHOU: stderr nao vazio'
print('OK — fluxo demonstravel preservado')
"
```

### Cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --name-only
```

---

## Relatório de implementação obrigatório

O executor deve criar:

```
docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
```

O relatório deve conter no mínimo:

1. **Resumo da migração**: o que foi feito, em qual base (commit/HEAD).
2. **Arquivos criados e alterados**: lista exaustiva.
3. **Decisões de compatibilidade/alias**:
   - O que aconteceu com `sobreposto` em `grupo_minimo.json`.
   - Como o loader trata `"horizontal"` e `"lado_a_lado"` após a atualização.
   - Por que `modelo.py` e `renderizador.py` foram ou não foram alterados.
4. **Chips removidos do Orquestrador**: lista dos 9 chips removidos com justificativa
   (capacidade não implementada) e confirmação dos 2 chips preservados.
5. **Testes executados**: saída completa de cada comando de verificação.
6. **Fora de escopo preservado**: confirmação de que nenhuma capacidade nova foi
   introduzida e que o fluxo demonstrável do H-0013 continua funcional.
7. **Status final**: PASSOU / FALHOU (com detalhe de cada falha).

O relatório não cria regra nova. Apenas evidencia o que foi feito.

---

## Instrução de bloqueio ao executor

Leia este handoff integralmente antes de alterar qualquer arquivo.

**Regras obrigatórias:**

1. Não decidir arquitetura nova. Toda decisão não coberta por este handoff ou
   pelos contratos citados deve ser reportada como `ARCHITECTURE_REVIEW_REQUIRED`.

2. Não alterar contrato, ADR, NOMENCLATURA nem INDICE.

3. Não resolver lacuna por inferência. Se faltar regra, arquivo permitido ou
   critério verificável, parar com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`.

4. Não fazer commit.

5. Não implementar nada fora do escopo positivo.

6. Criar o relatório `IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md`
   antes de encerrar.

### Parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

```
- A migração de arranjo exigir alteração de contrato ou NOMENCLATURA.
- A migração exigir que o loader valide vocabulário de corpo.arranjo no nível macro.
- Não for claro quais chips do Orquestrador são aplicáveis além de Esc e Ajuda.
- A alteração exigir migrar orquestrador.json inteiro para grupo hierárquico.
- A alteração exigir implementar horizontal.
- A alteração exigir adicionar segundo elemento ao grupo.
- Alterar demo.py se tornar necessário para preservar o fluxo demonstrável.
- Houver contradição entre este handoff e um contrato ou ADR vigente.
- Houver lacuna de especificação que impeça decidir sem assumir arquitetura.
- Os testes existentes exigirem comportamento contrário às ADRs-0011/0012.
```

### Parar com `BLOCKED` se:

```
- config/telas/grupo_minimo.json ou config/telas/orquestrador.json não puderem ser alterados.
- tela/loader.py, tela/teste_loader.py, tela/teste_renderizador.py, tela/teste_demo.py
  ou tela/teste_diagnostico.py estiverem ausentes.
- Algum critério de aceite não puder ser verificado pelos meios disponíveis.
- Algum arquivo obrigatório não estiver na lista de permitidos.
- Os testes passando em HEAD base quebrarem por motivo não relacionado às alterações
  deste handoff (indicaria estado inconsistente pré-existente).
```

---

## Próximo ciclo previsto

**H-0015** — Grupo estrutural com 2 elementos em arranjo vertical.

O H-0015 relaxará o invariante do H-0012 de "exatamente 1 elemento funcional dentro
do grupo". Ele só pode ser implementado após H-0014 estar concluído e validado,
pois H-0015 deve usar `"vertical"` como terminologia canônica desde sua criação.

O H-0014 não decide arquitetura de grupos com 2+ elementos. Essa decisão pertence
ao H-0015 e ao seu respectivo handoff.
