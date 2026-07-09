# Implementação — H-0014 Migração pós-ADR: arranjo vertical e barra declarativa

## Status

IMPLEMENTATION_COMPLETED (com correção pós-QA/revisão humana — ver seção
"Correção pós-QA/revisão humana" abaixo).

## Correção pós-QA/revisão humana

A revisão humana identificou que `config/telas/orquestrador.json` ainda
mantinha `corpo.arranjo: "sobreposto"`, o que não era resíduo inerte. A
correção migrou esse campo ativo para `vertical`, alinhando o
Orquestrador à ADR-0011 e ao objetivo do H-0014.

### Motivo

O handoff H-0014 (seção "Decisão sobre alias transicional `sobreposto`")
havia listado `orquestrador.json`, `destino_minimo.json` e `stub_b.json`
como mantendo `"sobreposto"` "fora do escopo de migração deste ciclo". A
revisão humana contestou essa classificação especificamente para o
**Orquestrador**: por ser a tela raiz (tela de entrada do sistema) e por
estar sendo ativamente editado neste próprio ciclo (redução de
`barra_de_menus.chips[]`), manter `corpo.arranjo: "sobreposto"` ao lado
da migração de `grupo_minimo.json` para `vertical` era inconsistente com
a ADR-0011 (itens 1, 2 e 6) e com o objetivo do H-0014. O campo é
`corpo.arranjo` ativo do Orquestrador — não resíduo inerte.

### Arquivos ajustados nesta correção

- `config/telas/orquestrador.json`: `corpo.arranjo` migrado de
  `"sobreposto"` para `"vertical"`.
- `tela/teste_loader.py`: asserção de `teste_caminho_feliz` (carrega o
  `orquestrador.json` real) atualizada de
  `corpo.arranjo == "sobreposto"` para `corpo.arranjo == "vertical"`.
- `tela/teste_modelo.py`: asserção de `teste_modelo_orquestrador`
  atualizada de `modelo.corpo.arranjo == "sobreposto"` para
  `modelo.corpo.arranjo == "vertical"`.

Nenhum outro arquivo foi alterado por esta correção. `modelo.py`,
`renderizador.py`, `demo.py` e `diagnostico.py` permanecem inalterados
(o renderer não lê `corpo.arranjo`; o modelo já preserva o valor
inertemente).

### Diff da correção

```diff
   "corpo": {
-    "arranjo": "sobreposto",
+    "arranjo": "vertical",
     "elementos": [
```

### Classificação das ocorrências remanescentes de `sobreposto`

Após a correção,
`grep -R '"arranjo"[[:space:]]*:[[:space:]]*"sobreposto"' -n config/telas`
retorna exatamente:

```text
config/telas/destino_minimo.json:9:    "arranjo": "sobreposto",
config/telas/stub_b.json:9:    "arranjo": "sobreposto",
```

Classificação (critério do H-0014: `sobreposto` só pode permanecer se
comprovadamente histórico/inativo/fora do fluxo migrado):

| Arquivo | Ocorrência | Classificação | Justificativa |
|---|---|---|---|
| `config/telas/orquestrador.json` | `corpo.arranjo` | ~~BLOQUEANTE~~ → CORRIGIDO | Tela raiz, ativamente editada neste ciclo (redução de chips). Migração para `vertical` era devida (ADR-0011, itens 1/2/6). Agora `vertical`. |
| `config/telas/destino_minimo.json` | `corpo.arranjo` | ACEITÁVEL | Fora do fluxo migrado pelo H-0014 (handoff linhas 161-165; commit `584ef3b` não o alterou). `corpo.arranjo` é runtime-inerte (renderizador não o consome). Tela é demonstrável via `d`, mas o valor não participa de nenhuma decisão visual. Recomenda-se migração em ciclo futuro para consistência total. |
| `config/telas/stub_b.json` | `corpo.arranjo` | ACEITÁVEL | Artefato de validação declarativa — H-0011 determina "NÃO ALTERAR" e "não conectar ao lançador"; não é navegável no demo. Histórico/inativo; runtime-inerte. |

Nenhuma ocorrência remanescente é `corpo.arranjo` ativo de tela migrada
pelo H-0014. `destino_minimo.json` e `stub_b.json` não foram alterados
por esta correção (fora do escopo permitido e fora do fluxo migrado).

### Verificação pós-correção

```bash
python -c "import json; print(json.load(open('config/telas/orquestrador.json'))['corpo']['arranjo'])"
```

Resultado: `vertical`.

```bash
python tela/teste_loader.py        # 67/67, exit 0
python tela/teste_modelo.py        # 53/53, exit 0
python tela/teste_renderizador.py  # 112/112, exit 0
python tela/teste_diagnostico.py   # 28/28, exit 0
python tela/teste_demo.py          # 107/107, exit 0
```

Todos com `[FALHOU]=0`, sem traceback. `python -m json.tool` em
`orquestrador.json` e `grupo_minimo.json`: ambos `OK` (exit 0). Nenhum
`__pycache__`/`*.pyc` em `tela/`. Nenhum commit realizado.

## Objetivo

Alinhar a base existente às decisões ADR-0011 (terminologia de arranjo
`vertical`/`horizontal`) e ADR-0012 (`barra_de_menus` declarativa por
tela) **antes** de qualquer nova capacidade de composição. Este ciclo é
de migração pura: nenhuma nova capacidade de composição é introduzida.

Base antes da implementação: `ceaf0be` — docs: registra ADRs de arranjo e
barra declarativa (HEAD informada pelo handoff H-0014).

## Resumo da migração

A migração foi majoritariamente declarativa em JSON, com uma única
alteração pontual de validação no loader:

1. `config/telas/grupo_minimo.json`: `corpo.arranjo` e
   `grupo_principal.arranjo` migrados de `"sobreposto"` para `"vertical"`
   (terminologia canônica final — ADR-0011).
2. `config/telas/orquestrador.json`: `barra_de_menus.chips[]` reduzido
   de 11 para 2 chips aplicáveis ao ciclo atual (ADR-0012).
3. `tela/loader.py` (`_validar_grupo`): passou a rejeitar `"horizontal"`
   (termo final) **e** `"lado_a_lado"` (alias transicional) como arranjo
   de grupo fora de escopo, com mensagem citando ADR-0011 e H-0014.
4. Testes atualizados para refletir `"vertical"` em contexto de grupo e
   os 2 chips do Orquestrador, sem exigir conjunto global canônico.
5. Criado este relatório.

Nenhum código de runtime (`modelo.py`, `renderizador.py`, `demo.py`,
`diagnostico.py`) precisou ser alterado — o renderer já lia
`barra_de_menus.chips[]` declarativamente e o modelo já preserva
`arranjo` inertemente.

## Arquivos criados

- `docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md`

## Arquivos alterados

- `config/telas/grupo_minimo.json`
- `config/telas/orquestrador.json`
- `tela/loader.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`

`modelo.py` e `renderizador.py` **não** foram alterados (verificação
confirmou que já preservam/renderizam declarativamente — conforme
expectativa do handoff, seções F-4 e F-5).

## Decisão sobre alias transicional `sobreposto`

**Não foi mantido `sobreposto` como alias ativo no grupo.** O handoff
H-0014 (seção "Decisão sobre alias transicional `sobreposto` em grupo")
deixou explícito que não é necessário preservar `sobreposto` como alias
no grupo, pois o único JSON de grupo (`grupo_minimo.json`) está sendo
migrado diretamente para `"vertical"` e não há grupo ativo com
`sobreposto` após a migração. Portanto **não foi implementada
normalização de alias no loader**.

- `grupo_minimo.json` agora usa `arranjo: "vertical"` em `corpo.arranjo`
  e em `grupo_principal.arranjo`. Nenhuma ocorrência de `"sobreposto"`
  permanece neste arquivo.
- `destino_minimo.json` e `stub_b.json` **mantêm** `"sobreposto"` como
  valor legado em `corpo.arranjo` (fora do escopo de migração deste
  ciclo, conforme handoff; `corpo.arranjo` é runtime-inerte — o
  renderizador não o consome). O loader continua preservando
  inertemente qualquer string em `corpo.arranjo` no nível macro — esta
  não-validação é intencional e não foi alterada.
- `orquestrador.json` constava nesta etapa com `"sobreposto"` em
  `corpo.arranjo`, mas isso foi corrigido na revisão humana pós-QA
  (migrado para `"vertical"` — ver seção "Correção pós-QA/revisão
  humana").

### Como o loader trata `horizontal` e `lado_a_lado` após a atualização

Em `_validar_grupo` (única alteração de `loader.py`):

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

- `"vertical"` é aceito (caminho canônico).
- `"sobreposto"` continua aceito inertemente (alias transicional de
  vertical; não há grupo ativo com esse valor após a migração).
- Ausência de `arranjo` no grupo continua válida (CA-16 preservada).
- `"horizontal"` e `"lado_a_lado"` são rejeitados com `TelaGrupoInvalido`.

O bullet do docstring de `_validar_grupo` foi atualizado para refletir
`"horizontal"`/`"lado_a_lado"` (é parte da própria função; CA-17
preservada — nenhuma outra linha de `loader.py` mudou).

### Por que `modelo.py` e `renderizador.py` não foram alterados

- `modelo.py` copia `arranjo` (de corpo e de grupo) inertemente em
  `Corpo.arranjo` e em `_campos_inertes`. A troca de valor
  `"sobreposto"` → `"vertical"` não exige alteração de código.
- `renderizador.py` não lê `corpo.arranjo` nem `grupo.arranjo` para
  decisões visuais; lê `barra_de_menus.get("chips", [])` e percorre o
  que receber. A redução de chips não exige alteração de código do
  renderer — ele já era declarativo (confirmado por ADR-0012 e pelo
  levantamento que originou a ADR).

## Chips removidos ou preservados no Orquestrador

### Preservados (2 chips aplicáveis ao ciclo atual)

| id | tecla | texto | justificativa |
|---|---|---|---|
| `chip_esc` | `Esc` | `Sair` | Implementado — Esc sai da tela raiz (pilha vazia). Copiado da declaração atual sem alteração de campos internos. |
| `chip_ajuda` | `?` | `Ajuda` | Declarado `"sempre"`; presente em todas as telas mínimas (`destino_minimo`, `grupo_minimo`). Copiado sem alteração. |

### Removidos (9 chips de capacidades não implementadas/não aplicáveis)

| id | tecla | texto | justificativa da remoção |
|---|---|---|---|
| `chip_paginas` | `<>` | `Páginas` | Paginação não implementada. |
| `chip_colunas` | `-+` | `Colunas` | Ajuste de colunas não implementado. |
| `chip_grupos` | `#` | `Grupos` | Filtro de grupo não implementado. |
| `chip_alternar` | `⇆` | `Alternar` | Alternância de foco não implementada. |
| `chip_navegar` | `✥` | `Navegar` | Navegação por `[✥]` não implementada. |
| `chip_selecionar` | `␣` | `Selecionar` | Seleção não implementada. |
| `chip_enter` | `⏎` | `Todos` | Ação enter não implementada. |
| `chip_estilo` | `\|` | `Estilo` | Tela de estilo não definida/implementada (`tela_destino == "pendente"`). |
| `chip_verboso` | `V` | `Verboso` | Modo verboso não implementado. |

Conforme ADR-0012 (itens 3, 7 e 8): cada tela declara apenas chips
aplicáveis ao seu estado/capacidade atual; a natureza canônica de um
chip não basta para justificar sua declaração quando a capacidade não
existe.

### Preservados (não-chips)

Os campos `filtros`, `bindings`, `referencias_de_acoes`,
`lancador_principal.itens[]` (itens `d → destino_minimo` e
`g → grupo_minimo`) e `metadados` do `orquestrador.json` **não** foram
alterados — apenas `barra_de_menus.chips[]` foi reduzido.

## Diff da declaração

### `config/telas/grupo_minimo.json`

```diff
   "corpo": {
-    "arranjo": "sobreposto",
+    "arranjo": "vertical",
     "elementos": [
       {
         "id": "grupo_principal",
         "tipo": "grupo",
-        "arranjo": "sobreposto",
+        "arranjo": "vertical",
```

### `config/telas/orquestrador.json`

`barra_de_menus.chips[]` reduzido de 11 para 2 entradas (`chip_esc` e
`chip_ajuda`), sem alterar nenhum outro campo top-level.

## Constantes `_EXPECTED_*` atualizadas

O bloco `Menus` das constantes que cristalizavam a saída do Orquestrador
foi reduzido de 11 linhas de chip para 2 (`[Esc] Sair` e `[?] Ajuda`).
As strings exatas foram **derivadas** executando `renderizar_tela` sobre
o modelo atualizado (não calculadas manualmente), conforme orientação do
handoff.

| Arquivo | Constante | Largura |
|---|---|---|
| `tela/teste_renderizador.py` | `_EXPECTED_ORQUESTRADOR` | 42 (curva) |
| `tela/teste_renderizador.py` | `_EXPECTED_ORQUESTRADOR_RETA` | 42 (reta) |
| `tela/teste_demo.py` | `_EXPECTED_CURVA` | 80 (curva) |
| `tela/teste_demo.py` | `_EXPECTED_RETA` | 80 (reta) |
| `tela/teste_demo.py` | `_EXPECTED_DIAGNOSTICO_CURVA_42` | 42 (curva) |
| `tela/teste_diagnostico.py` | `_EXPECTED_ORQUESTRADOR` | 42 (curva) |

As constantes `_EXPECTED_DESTINO_MINIMO_*` e `_EXPECTED_GRUPO_MINIMO_*`
(em `teste_demo.py`) já continham apenas 2 chips cada (`[Esc] Voltar` e
`[?] Ajuda`) e **não** foram alteradas.

## Asserções de presença de chips atualizadas

- `tela/teste_renderizador.py`: a asserção
  `"saida contem '[<>] Páginas' (chip do JSON)"` foi substituída por
  `"saida NAO contem '[<>] Paginas' (chip removido do Orquestrador)"`.
  Demais asserções de ausência (ex.: `'[B] Borda' nao aparece`) foram
  mantidas.
- `tela/teste_loader.py` e `tela/teste_modelo.py`: as asserções que
  exigiam a presença de `chip_estilo` (um dos 9 chips removidos) foram
  atualizadas para registrar a **remoção** (`chip_estilo is None`),
  conforme ADR-0012 (item 8) e a regra do handoff de remover asserções
  de presença dos 9 chips removidos. Nenhum teste passa a exigir
  conjunto global canônico de chips (CA-24).

## Testes de loader adicionados

- `teste_loader.py`: adicionado caso
  `"grupo com arranjo 'horizontal' -> TelaGrupoInvalido (ADR-0011)"`
  como caso primário da ADR-0011. O caso existente de `"lado_a_lado"`
  foi mantido como teste secundário de alias transicional
  (`"alias de horizontal"`).
- Grupo fabricado `_grupo_minimo_dict` migrado para `arranjo: "vertical"`
  (em `base_g` e no `corpo` que o envolve), atendendo CA-18/CA-19.

## Testes executados

### Validade dos JSONs alterados

```bash
python -m json.tool config/telas/grupo_minimo.json >/dev/null && echo "grupo_minimo.json OK"
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

Resultado: ambos `OK` (exit 0).

### Integridade de JSONs não alterados

```bash
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
```

Resultado: `destino_minimo.json OK` (exit 0).

### Testes automatizados

| Comando | Exit code | [FALHOU] | Traceback | Total / Passaram |
|---|---|---|---|---|
| `python tela/teste_loader.py` | 0 | 0 | 0 | 67 / 67 |
| `python tela/teste_modelo.py` | 0 | 0 | 0 | 53 / 53 |
| `python tela/teste_renderizador.py` | 0 | 0 | 0 | 112 / 112 |
| `python tela/teste_diagnostico.py` | 0 | 0 | 0 | 28 / 28 |
| `python tela/teste_demo.py` | 0 | 0 | 0 | 107 / 107 |

### Verificação de migração de arranjo

```bash
python -c "from tela.loader import carregar_tela; r=carregar_tela(None,'grupo_minimo'); print('corpo:', r['corpo']['arranjo']); print('grupo:', r['corpo']['elementos'][0].get('arranjo'))"
```

Resultado: `corpo: vertical` / `grupo: vertical` — ambos canônicos.

### Verificação dos chips do Orquestrador

```bash
python -c "import json; raw=json.load(open('config/telas/orquestrador.json')); print([c['tecla'] for c in raw['barra_de_menus']['chips']])"
```

Resultado: `['Esc', '?']` — exatamente 2 chips aplicáveis. Confirmada
preservação de `filtros`, `bindings`, `referencias_de_acoes` e dos itens
`d`/`g` do lançador.

### Verificação de rejeição de `horizontal` no grupo

Grupo fabricado com `arranjo: "horizontal"` → `TelaGrupoInvalido`:

```text
Grupo 'g1' com arranjo 'horizontal' e fora de escopo no H-0014
(arranjo horizontal nao implementado para grupo;
 'lado_a_lado' e alias transicional de 'horizontal' — ADR-0011)
```

### Verificação de preservação do fluxo demonstrável (subprocess)

```bash
python tela/demo.py  # input: g\n\x1b\n\x1b\n
```

Resultado: `exit 0`; `GRUPO MINIMO` presente; `[Esc] Voltar` presente
(em `grupo_minimo`); `[Esc] Sair` presente (no Orquestrador); stderr
vazio. Fluxo do H-0013 preservado intacto.

## Verificações de escopo

- `tela/demo.py` não foi alterado (nenhum diff).
- `tela/diagnostico.py` não foi alterado (nenhum diff).
- `tela/modelo.py` não foi alterado (nenhum diff).
- `tela/renderizador.py` não foi alterado (nenhum diff).
- `config/telas/destino_minimo.json` não foi alterado.
- `config/telas/stub_b.json` não foi alterado.
- `config/telas/grupo_minimo.json` continua com exatamente 1 elemento
  funcional interno (nenhum segundo elemento adicionado).
- Nenhum contrato em `docs/contratos/` foi alterado.
- Nenhuma ADR em `docs/adr/` foi alterada.
- `docs/NOMENCLATURA.md` e `docs/INDICE.md` não foram alterados.
- `docs/handoff/` não foi alterado pelo executor.
- Nenhum commit foi realizado.
- Nenhum arquivo fora da lista de permitidos foi criado ou alterado.

## Fora de escopo preservado

Nenhuma nova capacidade de composição foi introduzida. Em particular,
**não** foram implementados: segundo elemento no grupo; grupo com 2+
elementos; arranjo horizontal; lado a lado como novo caminho;
aninhamento de grupos; distribuição percentual/fração; migração do
Orquestrador inteiro para grupo; novo tipo funcional; console real;
foco; seleção; navegação por `[✥]`; novo registry; novo mecanismo de
chip.

O fluxo demonstrável do H-0013 permanece funcional:

- `g` abre `grupo_minimo`;
- `d` abre `destino_minimo`;
- `b` alterna borda (curva ↔ reta);
- `Esc` em `grupo_minimo` volta ao Orquestrador;
- `Esc` em `destino_minimo` volta ao Orquestrador;
- `Esc` na raiz (pilha vazia) sai.

## Cobertura dos critérios de aceite

- **CA-01..CA-06** (`grupo_minimo.json`): atendidos — JSON válido;
  `corpo.arranjo == "vertical"`; `grupo_principal.arranjo == "vertical"`;
  nenhuma ocorrência de `"sobreposto"`; demais campos inalterados;
  `carregar_tela(None, "grupo_minimo")` sem erro.
- **CA-07..CA-12** (`orquestrador.json`): atendidos — JSON válido;
  `barra_de_menus.chips[]` com exatamente 2 chips (`chip_esc`,
  `chip_ajuda`); os 9 chips removidos ausentes; `filtros`,
  `bindings`, `referencias_de_acoes` preservados; `lancador` com os 2
  itens (`d`, `g`); `carregar_tela(None, "orquestrador")` sem erro.
- **CA-13..CA-17** (`loader.py`): atendidos — rejeita `horizontal` e
  `lado_a_lado`; aceita `vertical` e ausência de `arranjo`; apenas
  `_validar_grupo` alterada.
- **CA-18..CA-24** (testes): atendidos — grupo fabricado usa `vertical`;
  asserção de arranjo do grupo em `teste_modelo.py` reflete `vertical`;
  constantes `_EXPECTED_*` do Orquestrador refletem 2 chips; nenhuma
  asserção exige presença dos 9 chips removidos; nenhum teste exige
  conjunto global canônico.
- **CA-25** (fluxo demonstrável): atendido — subprocess confirma
  navegação `g`/`d`, `b`, Esc.
- **CA-26..CA-32** (testes automatizados / JSON): atendidos — todos
  exit 0.
- **CA-33..CA-43** (escopo/rastreabilidade): atendidos — arquivos
  proibidos intactos; nenhum arquivo fora da lista permitida alterado;
  IMP-0014 criado; nenhum commit; nenhuma nova capacidade.

## Estado Git final

```bash
git status --short
```

```text
 M scripts/config/telas/grupo_minimo.json
 M scripts/config/telas/orquestrador.json
 M scripts/tela/loader.py
 M scripts/tela/teste_demo.py
 M scripts/tela/teste_diagnostico.py
 M scripts/tela/teste_loader.py
 M scripts/tela/teste_modelo.py
 M scripts/tela/teste_renderizador.py
?? scripts/docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md
?? scripts/docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
?? scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0014_HANDOFF.md
```

Os 8 arquivos `M` (modificados) estão todos dentro da lista de
permitidos do H-0014. Os `??` são: o handoff H-0014 e o relatório de
auditoria (documentos não rastreados esperados, anteriores à
implementação, não tocados pelo executor) e este relatório IMP-0014
(criado pelo executor).

```bash
git diff --stat
```

```text
 scripts/config/telas/grupo_minimo.json |  4 +-
 scripts/config/telas/orquestrador.json | 99 ----------------------------------
 scripts/tela/loader.py                 | 12 +++--
 scripts/tela/teste_demo.py             | 27 ----------
 scripts/tela/teste_diagnostico.py      |  9 ----
 scripts/tela/teste_loader.py           | 21 +++++---
 scripts/tela/teste_modelo.py           |  8 +--
 scripts/tela/teste_renderizador.py     | 22 +-------
 8 files changed, 31 insertions(+), 171 deletions(-)
```

## Confirmação de ausência de cache/bytecode

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Resultado: nenhuma saída — nenhum `__pycache__` nem `.pyc` permanece
no workspace.

## Resultado final

PASSOU.

Todos os comandos obrigatórios encerram com código de saída 0, sem
linhas `[FALHOU]` e sem traceback. Somente arquivos permitidos foram
criados/alterados. A migração pós-ADR (arranjo `vertical` em
`grupo_minimo`; `barra_de_menus` do Orquestrador reduzida a chips
aplicáveis) foi concluída sem introduzir nova capacidade de composição,
e o fluxo demonstrável do H-0013 permanece intacto.
