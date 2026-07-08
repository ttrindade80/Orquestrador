---
name: H-0006-tela-minima-borda-fixa
description: Handoff de implementação da tela mínima demonstrável com borda fixa — evolui renderizar_tela para saída visual com três caixas bordeadas (cabeçalho derivado do modelo, dashboard placeholder hardcoded, menu inerte hardcoded)
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0006
  data_criacao: 2026-07-07
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
  handoffs_anteriores:
    - docs/handoff/H-0001-loader-validador-tela-json.md
    - docs/handoff/H-0002-modelo-interno-tela.md
    - docs/handoff/H-0003-renderizador-textual-estatico.md
    - docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
    - docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
  issues_relacionadas: []
---

# H-0006 — Tela mínima com borda fixa

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/handoff/H-0001-loader-validador-tela-json.md`
3. `docs/handoff/H-0002-modelo-interno-tela.md`
4. `docs/handoff/H-0003-renderizador-textual-estatico.md`
5. `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
6. `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
7. Este handoff

Se houver conflito entre este handoff e qualquer artefato acima, o executor
deve parar com `ARCHITECTURE_REVIEW_REQUIRED` e registrar a divergência.
Este handoff não pode criar regra nova que contradiga nenhum dos artefatos
acima.

---

## Instrução explícita ao executor (GLM/OpenCode)

**Leia este handoff integralmente antes de escrever qualquer linha de código.**

O executor deve:

- Seguir estritamente este handoff, sem reinterpretar arquitetura lendo
  contratos, ADRs ou NOMENCLATURA por conta própria.
- Não resolver ambiguidades por decisão local. Se algo não estiver coberto
  aqui, parar com `BLOCKED` e descrever a lacuna objetivamente.
- Não alterar contrato, ADR, NOMENCLATURA, configuração, backlog, issues,
  handoff anterior, relatório anterior, nem qualquer documento normativo.
- Não implementar nenhum item listado em "Fora de escopo".
- Não fazer commit do resultado — commit é responsabilidade do engenheiro.
- Não usar bibliotecas externas além da stdlib Python.
- Se faltar regra, arquivo permitido ou critério verificável: parar com
  `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED` descrevendo o que falta.

---

## Contexto herdado de H-0005

Os handoffs H-0001, H-0002, H-0003, H-0004 e H-0005 foram implementados e
aprovados. O relatório IMP-0005 registra status `APROVADO` e o QA
pós-escopo registra `QA_APPROVED_WITH_NOTES` (nota não bloqueante sobre
redação de escopo Git). O pacote `tela/` contém atualmente:

```
tela/__init__.py           — marcador de pacote (vazio)
tela/loader.py             — loader/validador macro (H-0001)
tela/teste_loader.py       — diagnóstico H-0001 (37 verificações, passando)
tela/modelo.py             — modelo interno normalizado (H-0002)
tela/teste_modelo.py       — diagnóstico H-0002 (30 verificações, passando)
tela/renderizador.py       — renderer estrutural (H-0005)
tela/teste_renderizador.py — diagnóstico H-0005 (39 verificações, passando)
tela/diagnostico.py        — ponto de entrada executável (H-0004)
tela/teste_diagnostico.py  — diagnóstico H-0004/H-0005 (27 verificações, passando)
```

### Pipeline estabelecido

```
config/telas/orquestrador.json
    → carregar_tela(None, "orquestrador")   [tela/loader.py      — H-0001]
    → dict (tela_raw)
    → construir_modelo(tela_raw)            [tela/modelo.py      — H-0002]
    → ModeloTela
    → renderizar_tela(modelo)               [tela/renderizador.py — H-0006]
    → str
```

### O que o H-0005 produzia

O renderer estrutural (H-0005) produzia a seguinte saída textual plana com
regiões nomeadas:

```
TELA: orquestrador
SCHEMA: tela.v1

REGIAO: cabecalho
  titulo: Orquestrador
  descricao: Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de survey

REGIAO: corpo
  arranjo: sobreposto
  componentes:
    [console] console_principal
    [dashboard] dashboard_info
    [lancador] lancador_principal

REGIAO: barra_de_menus
  chips:
    [chip_esc] Sair
    [chip_paginas] Páginas
    [...]
    [chip_ajuda] Ajuda
```

O H-0006 substitui esse formato por um formato visual com caixas bordeadas,
conforme descrito neste handoff.

### Pendências documentais que permanecem inertes

- **DOC-B008**: tipos internos de item de `console` não definidos.
- **DOC-B009**: registry completo de ações e tipos de chip não fechado.
- **`lancador_principal.itens`**: lista vazia; `tela_destino` pendente.
- **`bindings`** e **`referencias_de_acoes`**: declarados como pendentes.

O renderer não deve tratar essas pendências como erro. São declaração inerte
no modelo — o renderer as ignora completamente.

---

## Objetivo técnico

Evoluir `tela/renderizador.py` para que `renderizar_tela(modelo: ModeloTela)`
produza uma **saída visual com borda fixa** composta por três caixas:

1. **Caixa de cabeçalho** — label derivado de `modelo.cabecalho.titulo`;
   conteúdo derivado de `modelo.cabecalho.descricao` (truncado).
2. **Caixa de dashboard** — label e conteúdo **hardcoded** como placeholder.
   Não usa nenhum dado de `modelo.corpo`.
3. **Caixa de menu** — label e conteúdo **hardcoded** com `[Esc] Sair` e
   `[B] Borda` como texto inerte. Não usa nenhum dado de
   `modelo.barra_de_menus`.

A função principal continua sendo:

```python
renderizar_tela(modelo: ModeloTela) -> str
```

O renderer continua consumindo `ModeloTela`. Não pode ler JSON bruto
diretamente. Não pode executar ações, bindings, chips ou navegação. A
borda é fixa — sem cálculo de largura de terminal, sem alternância de
estilo, sem carregamento de configuração de estilo.

---

## Escopo positivo

O H-0006 **autoriza e especifica**:

1. Alterar `tela/renderizador.py` para o novo formato visual com borda fixa.
2. Alterar `tela/teste_renderizador.py` para verificar o novo formato.
3. Alterar `tela/teste_diagnostico.py` para atualizar as verificações de
   formato que dependiam do formato H-0005 (justificativa abaixo).
4. Criar `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md`.

### Justificativa objetiva para alterar `tela/teste_diagnostico.py`

O `tela/teste_diagnostico.py` contém verificações de formato do H-0005
(`"REGIAO: cabecalho" in resultado`, `"TELA: orquestrador"` como prefixo,
`"[console] console_principal" in resultado`, etc.). O H-0006 muda o formato
do renderer — esses tokens deixam de aparecer na saída. Sem atualização do
arquivo, `python tela/teste_diagnostico.py` retornaria código de saída 1,
violando o invariante que exige código de saída 0. A atualização é
objetivamente necessária. O `tela/diagnostico.py` em si **não pode ser
alterado** — ele apenas encadeia o pipeline independente do formato da saída.

---

## Fora de escopo — proibições explícitas

O H-0006 **não implementa** nenhum dos itens abaixo:

- alternância de bordas;
- estado de borda ativo;
- leitura de `config/estilo.json` (nem parcial);
- persistência de estilo;
- loop de aplicação;
- navegação real entre telas;
- ações reais;
- bindings ativos;
- filtros funcionais;
- paginação funcional;
- seleção;
- registry de ações;
- registry de tipos;
- execução real de chips;
- navegação por `tela_destino`;
- dashboard real com dados;
- pop-up;
- tela de processamento;
- interface interativa;
- cálculo de largura de terminal;
- cores ou escape codes ANSI;
- `curses`, `textual`, `rich` ou qualquer biblioteca de UI;
- renderer visual final;
- contrato de dashboard;
- schema de dashboard;
- registry de dashboard.

`[Esc] Sair` e `[B] Borda` devem aparecer **apenas como texto inerte** na
caixa de menu. Nenhum binding é registrado, nenhuma ação é executada.

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os arquivos abaixo:

```
tela/renderizador.py                            — ALTERAR (novo formato visual)
tela/teste_renderizador.py                      — ALTERAR (verificações do novo formato)
tela/teste_diagnostico.py                       — ALTERAR (atualizar verificações de formato)
docs/relatorios/IMP-0006-tela-minima-borda-fixa.md — CRIAR
```

A lista acima é exaustiva e sem exceção. Se a implementação exigir alterar
qualquer outro arquivo, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

---

## Arquivos proibidos de alterar

```
tela/loader.py             — proibido (H-0001)
tela/modelo.py             — proibido (H-0002)
tela/teste_loader.py       — proibido (H-0001)
tela/teste_modelo.py       — proibido (H-0002)
tela/diagnostico.py        — proibido (H-0004; cadeia não muda)
tela/__init__.py           — proibido

docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/contratos/            (qualquer arquivo)
docs/adr/                  (qualquer arquivo)
docs/handoff/              (qualquer arquivo, incluindo este)
docs/templates/            (qualquer arquivo)
config/                    (qualquer arquivo)
```

---

## Regras de implementação

### Assinatura

```python
renderizar_tela(modelo: ModeloTela) -> str
```

A assinatura **não muda**. O módulo `tela/renderizador.py` deve manter:

- `class RenderizadorErro(Exception)` — definida no módulo.
- `def renderizar_tela(modelo: ModeloTela) -> str` — função pública.

### Importações

Importação obrigatória no módulo do renderer:

```python
from tela.modelo import ModeloTela
```

Importações proibidas em `tela/renderizador.py`:

- `import json`
- `import os`
- `import pathlib`
- `from tela.loader import carregar_tela`
- `subprocess`, `exec`, `eval` ou qualquer mecanismo de execução de processo

### Contrato da função

| Aspecto | Regra |
|---|---|
| Entrada | `ModeloTela` — objeto produzido por `construir_modelo` (H-0002) |
| Saída | `str` — representação visual com borda fixa, determinística, auditável |
| Efeitos colaterais | Nenhum — não altera o modelo, não grava arquivo, não consulta JSON, não executa ação, não ativa binding |
| Determinismo | Dado o mesmo `ModeloTela`, sempre retorna a mesma string |
| Independência de terminal | A saída não muda conforme a largura do terminal |

### Campos derivados do modelo (caixa de cabeçalho)

O renderer usa **somente** estes campos de `ModeloTela` para construir a
caixa de cabeçalho:

| Campo do modelo | Uso |
|---|---|
| `modelo.cabecalho.get("titulo", "(ausente)")` | Label da caixa (uppercase, máx. 38 chars) |
| `modelo.cabecalho.get("descricao", "(ausente)")[:39]` | Linha de conteúdo da caixa |

O modelo **não é consultado** para a caixa de dashboard nem para a caixa de
menu — ambas são totalmente hardcoded (ver seção "Campos fixos").

### Campos fixos (hardcoded) — caixa de dashboard e caixa de menu

| Elemento | Valor fixo |
|---|---|
| Label da caixa de dashboard | `DASHBOARD` |
| Linha de conteúdo 1 do dashboard | `Dashboard de teste` |
| Linha de conteúdo 2 do dashboard | `Sem dados carregados` |
| Label da caixa de menu | `Menu` |
| Linha de conteúdo do menu | `[Esc] Sair    [B] Borda` |

Esses valores são constantes no código. O renderer não lê `modelo.corpo`,
`modelo.barra_de_menus`, `modelo.id`, `modelo.schema` nem `modelo._raw`
para construir essas caixas.

### Exceção para argumento inválido

`RenderizadorErro` deve ser lançada quando o argumento recebido não for
`ModeloTela` (ex.: `None`, `dict`, ou qualquer outro tipo). Em operação
normal com `ModeloTela` válido, não deve lançar exceção.

### Campos inertes — o renderer não pode acessar

O renderer **não pode** acessar, iterar ou usar:

- `elemento._campos_inertes` de qualquer `ElementoCorpo`
- `modelo.corpo.elementos` (corpo não é consultado)
- `modelo.barra_de_menus.get("chips", [])` (barra de menus não é consultada)
- `modelo.id`, `modelo.schema` (não aparecem na saída)
- `modelo._raw`

---

## Formato visual com borda fixa — especificação exata

O formato abaixo é **exato e obrigatório**. O implementador não pode
escolher outro formato sem aprovação explícita.

### Constantes de layout

```python
TOTAL_WIDTH   = 42   # largura total de cada linha, incluindo bordas
INNER_WIDTH   = 40   # largura interna (entre os dois caracteres de borda)
CONTENT_WIDTH = 39   # largura máxima do texto de conteúdo (após 1 espaço de margem)
```

### Caracteres de borda

| Caractere | Unicode | Nome |
|---|---|---|
| `╭` | U+256D | Canto superior esquerdo arredondado |
| `╮` | U+256E | Canto superior direito arredondado |
| `╰` | U+2570 | Canto inferior esquerdo arredondado |
| `╯` | U+256F | Canto inferior direito arredondado |
| `│` | U+2502 | Linha vertical |
| `─` | U+2500 | Linha horizontal |

### Regras de formato

| Elemento | Regra |
|---|---|
| Borda superior com label | `╭ {LABEL} {─×(38-len(LABEL))}╮` |
| Borda inferior | `╰{'─'×40}╯` |
| Linha de conteúdo | `│ {text:<39}│` (text padded à direita com espaços até 39 chars) |
| Label da caixa de cabeçalho | `modelo.cabecalho.get("titulo", "(ausente)").upper()` truncado a 38 chars |
| Conteúdo da caixa de cabeçalho | `modelo.cabecalho.get("descricao", "(ausente)")[:39]` |
| Label da caixa de dashboard | `DASHBOARD` (fixo) |
| Conteúdo do dashboard linha 1 | `Dashboard de teste` (fixo) |
| Conteúdo do dashboard linha 2 | `Sem dados carregados` (fixo) |
| Label da caixa de menu | `Menu` (fixo) |
| Conteúdo do menu | `[Esc] Sair    [B] Borda` (fixo, 4 espaços entre Sair e [B]) |
| Separação entre caixas | Uma linha em branco (`\n`) |
| Sem linha em branco inicial | A string começa diretamente com `╭` |
| Terminador de linha | `\n` para cada linha, incluindo a última |
| Linha final | A string termina com `\n` após `╰{'─'×40}╯` da última caixa |
| Codificação | UTF-8; sem escape codes ANSI |

### Verificação dos contadores de dashes

| Label | len(LABEL) | Dashes no topo (38 - len) | Dashes na base |
|---|---|---|---|
| ORQUESTRADOR | 12 | 26 | 40 (fixo) |
| DASHBOARD | 9 | 29 | 40 (fixo) |
| Menu | 4 | 34 | 40 (fixo) |

### Saída esperada para o estado atual de `config/telas/orquestrador.json`

A string abaixo é a saída **exata** esperada quando o pipeline completo é
executado sobre o `orquestrador.json` atual. O teste de regressão deve
comparar a saída real com este valor (igualdade estrita, incluindo o `\n`
final).

```
╭ ORQUESTRADOR ──────────────────────────╮
│ Tela raiz do sistema — ponto de entrada│
╰────────────────────────────────────────╯

╭ DASHBOARD ─────────────────────────────╮
│ Dashboard de teste                     │
│ Sem dados carregados                   │
╰────────────────────────────────────────╯

╭ Menu ──────────────────────────────────╮
│ [Esc] Sair    [B] Borda                │
╰────────────────────────────────────────╯
```

**Observação de truncamento**: a descrição completa em `orquestrador.json` é
`"Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de survey"`
(81 chars em Python). Os primeiros 39 chars Python são
`"Tela raiz do sistema — ponto de entrada"`, que preenche exatamente o
campo de conteúdo sem padding. O caractere `—` (U+2014, em-dash) conta
como 1 char Python.

**Verificação de largura linha a linha** (total = 42 chars cada):

| Linha | Composição | Total |
|---|---|---|
| `╭ ORQUESTRADOR ──────────────────────────╮` | 1+1+12+1+26+1 | 42 |
| `│ Tela raiz do sistema — ponto de entrada│` | 1+1+39+1 | 42 |
| `╰────────────────────────────────────────╯` | 1+40+1 | 42 |
| `╭ DASHBOARD ─────────────────────────────╮` | 1+1+9+1+29+1 | 42 |
| `│ Dashboard de teste                     │` | 1+1+18+21+1 | 42 |
| `│ Sem dados carregados                   │` | 1+1+20+19+1 | 42 |
| `╭ Menu ──────────────────────────────────╮` | 1+1+4+1+34+1 | 42 |
| `│ [Esc] Sair    [B] Borda                │` | 1+1+23+16+1 | 42 |

### Constante Python para o teste

```python
_EXPECTED_ORQUESTRADOR = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "╰────────────────────────────────────────╯\n"
    "\n"
    "╭ Menu ──────────────────────────────────╮\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "╰────────────────────────────────────────╯\n"
)
```

**Contagem de dashes nas strings literais acima** (deve ser verificada
caractere a caractere antes de qualquer commit):

- Linha 1: `──────────────────────────` = 26 dashes (entre `ORQUESTRADOR ` e `╮`)
- Linha 3: `────────────────────────────────────────` = 40 dashes
- Linha 5: `─────────────────────────────` = 29 dashes (entre `DASHBOARD ` e `╮`)
- Linha 8: `────────────────────────────────────────` = 40 dashes
- Linha 10: `──────────────────────────────────────` = 34 dashes (entre `Menu ` e `╮`)  
  **Atenção**: linha 10 = `╭ Menu ──────────────────────────────────╮`; dashes = 38-4 = 34.
- Linha 12: `────────────────────────────────────────` = 40 dashes

Se qualquer linha divergir de 42 chars, o executor deve reportar `BLOCKED`
com a linha exata que diverge.

---

## Campos inertes — preservação obrigatória

Os seguintes campos permanecem **inertes** — o renderer não pode executar,
resolver, ativar nem atribuir semântica nova a eles:

- `bindings`
- `referencias_de_acoes`
- `filtros`
- `chips[*].acao`
- `chips[*].regra_existencia`
- `chips[*].regra_ativo`
- `tela_destino` (qualquer valor)
- `origem_dados` (qualquer valor)
- `regra_geracao_itens`
- `itens` vazios de `lancador_principal`
- quaisquer campos em `_campos_inertes` de cada `ElementoCorpo`
- `modelo.corpo.elementos` (não consultado pelo renderer H-0006)
- `modelo.barra_de_menus` (não consultado pelo renderer H-0006)
- `modelo.id`, `modelo.schema` (não aparecem na saída)

---

## Pré-condição obrigatória

Antes de alterar qualquer arquivo, o executor deve confirmar que os
invariantes de todos os handoffs anteriores estão passando:

```bash
python tela/teste_loader.py    # todas as 37 verificações passando
python tela/teste_modelo.py    # todas as 30 verificações passando
python tela/teste_renderizador.py  # todas as 39 verificações passando (formato H-0005)
python tela/teste_diagnostico.py   # todas as 27 verificações passando
python tela/diagnostico.py         # imprime saída H-0005 e encerra com código 0
```

Se qualquer verificação falhar, o executor deve parar imediatamente com
`BLOCKED` e registrar qual verificação falhou e em qual módulo.

---

## Testes obrigatórios

### `tela/teste_renderizador.py` — atualizado para formato H-0006

#### Estrutura obrigatória do script

- Definir `sys.dont_write_bytecode = True` **antes** de qualquer import.
- Importar apenas da biblioteca padrão, de `tela.loader`, `tela.modelo` e
  `tela.renderizador`.
- Imprimir `[PASSOU] <nome>` ou `[FALHOU] <nome>` para cada verificação.
- Imprimir ao final: `Total de verificacoes`, `Passaram`, `Falharam`.
- Retornar código de saída 0 se todos passaram, 1 se algum falhou.
- Não usar `unittest`, `pytest` nem nenhum framework externo.

#### Verificações obrigatórias

**Seção 1 — Renderer sobre `orquestrador.json`**:

| Verificação | Critério |
|---|---|
| `renderizar_tela` aceita `ModeloTela` válido sem exceção | Nenhuma exceção lançada |
| Saída é `str` | `isinstance(saida, str) is True` |
| Saída começa com `"╭ ORQUESTRADOR"` | `saida.startswith("╭ ORQUESTRADOR")` |
| Saída contém `"│ Tela raiz do sistema"` | String presente na saída |
| Saída contém `"╭ DASHBOARD"` | String presente na saída |
| Saída contém `"Dashboard de teste"` | String presente na saída |
| Saída contém `"Sem dados carregados"` | String presente na saída |
| Saída contém `"╭ Menu"` | String presente na saída |
| Saída contém `"[Esc] Sair"` | String presente na saída |
| Saída contém `"[B] Borda"` | String presente na saída |
| Saída contém `"╰"` (borda inferior) | String presente na saída |
| Saída é determinística | Duas chamadas com o mesmo modelo produzem saída idêntica |
| Saída bate com expected output literal do H-0006 | Igualdade estrita com `_EXPECTED_ORQUESTRADOR` |

**Seção 2 — Modelo fabricado** (renderer usa dados do modelo, não do JSON):

Construir um `ModeloTela` fabricado com `id="teste_fabricado"`, `titulo="Fab"`,
`descricao="desc fab"` e verificar:

| Verificação | Critério |
|---|---|
| Saída fabricada começa com `"╭ FAB"` | `saida_fab.startswith("╭ FAB")` |
| Saída fabricada contém `"desc fab"` | String presente na saída fabricada |
| Saída fabricada contém `"╭ DASHBOARD"` (hardcoded) | String presente |
| Saída fabricada contém `"[Esc] Sair"` (hardcoded) | String presente |
| Saída fabricada contém `"[B] Borda"` (hardcoded) | String presente |
| Saída fabricada não menciona `"orquestrador"` | `"orquestrador" not in saida_fab` |
| Saída fabricada não menciona `"ORQUESTRADOR"` | `"ORQUESTRADOR" not in saida_fab` |

Código de construção do modelo fabricado:

```python
from tela.modelo import ElementoCorpo, Corpo, ModeloTela

_modelo_fab = ModeloTela(
    id="teste_fabricado",
    schema="tela.v0",
    cabecalho={"titulo": "Fab", "descricao": "desc fab"},
    corpo=Corpo(
        arranjo="linear",
        elementos=[ElementoCorpo(id="e1", tipo="console")],
    ),
    barra_de_menus={"chips": [{"id": "c1", "texto": "Ok"}]},
    _raw={},
)
saida_fab = renderizar_tela(_modelo_fab)
```

**Seção 3 — Casos de erro do renderer**:

| Verificação | Critério |
|---|---|
| `renderizar_tela(None)` lança `RenderizadorErro` | Exceção do tipo correto |
| `renderizar_tela(<dict>)` lança `RenderizadorErro` | Exceção do tipo correto |

**Seção 4 — Proibições de import/leitura no módulo do renderer**:

| Verificação | Critério |
|---|---|
| renderer não importa `'json'` | `"import json" not in texto_mod` |
| renderer não importa `'os'` | `"import os" not in texto_mod` |
| renderer não importa `'pathlib'` | `"import pathlib" not in texto_mod and "from pathlib" not in texto_mod` |
| renderer não importa `tela.loader` | `"from tela.loader" not in texto_mod and "import tela.loader" not in texto_mod` |
| renderer não abre nem lê arquivos | `"open(" not in texto_mod and ".read_text(" not in texto_mod and ".read_bytes(" not in texto_mod` |
| renderer não usa subprocess/exec/eval | `"subprocess" not in texto_mod and "exec(" not in texto_mod and "eval(" not in texto_mod` |
| renderer não acessa `_campos_inertes` | `"_campos_inertes" not in texto_mod` |

**Seção 5 — Inércia**:

| Verificação | Critério |
|---|---|
| `renderizar_tela` não altera `modelo._raw` | `modelo._raw == raw_antes` |
| `renderizar_tela` não altera `modelo.cabecalho` | `modelo.cabecalho == cabecalho_antes` |
| `renderizar_tela` não altera `corpo.elementos` | Lista de (id, tipo) inalterada |
| `renderizar_tela` não altera `barra_de_menus.chips` | Lista de chips inalterada |
| Saída não vaza campos inertes | `"origem_dados" not in saida and "bindings" not in saida and "filtros" not in saida and "tela_destino" not in saida and "regra_existencia" not in saida` |
| Saída não expõe id interno de chip (`[chip_esc]`) | `"[chip_esc]" not in saida` |

### `tela/teste_diagnostico.py` — verificações de formato atualizadas

O `tela/teste_diagnostico.py` deve ser atualizado para substituir as
verificações de formato do H-0005 pelos equivalentes do H-0006. A estrutura
do script (pré-condição via subprocess, resumo, código de saída) deve ser
preservada.

#### Substituição obrigatória da constante

A constante `_EXPECTED_ORQUESTRADOR` deve ser substituída pela constante
do H-0006 definida na seção "Constante Python para o teste" acima.

#### Verificações de formato que devem ser substituídas (H-0005 → H-0006)

| Verificação antiga (H-0005) | Nova verificação (H-0006) |
|---|---|
| `resultado.startswith("TELA: orquestrador")` | `resultado.startswith("╭ ORQUESTRADOR")` |
| `"SCHEMA: tela.v1" in resultado` | REMOVER (schema não aparece no novo formato) |
| `"REGIAO: cabecalho" in resultado` | `"╭ ORQUESTRADOR" in resultado` |
| `"titulo: Orquestrador" in resultado` | `"│ Tela raiz do sistema" in resultado` |
| `"REGIAO: corpo" in resultado` | `"╭ DASHBOARD" in resultado` |
| `"arranjo: sobreposto" in resultado` | `"Dashboard de teste" in resultado` |
| `"[console] console_principal" in resultado` | `"Sem dados carregados" in resultado` |
| `"[dashboard] dashboard_info" in resultado` | `"╭ Menu" in resultado` |
| `"[lancador] lancador_principal" in resultado` | `"[Esc] Sair" in resultado` |
| `"REGIAO: barra_de_menus" in resultado` | `"[B] Borda" in resultado` |
| `"[chip_esc]" in resultado` | `"╰" in resultado` (borda inferior presente) |
| `"[chip_ajuda]" in resultado` | `"│" in resultado` (borda lateral presente) |

#### Verificações que permanecem (não afetadas pela mudança de formato)

- `gerar_diagnostico_tela()` não lança exceção.
- Retorno é `str`.
- Resultado é determinístico (duas chamadas idênticas).
- Resultado bate com `_EXPECTED_ORQUESTRADOR` atualizado (igualdade estrita).
- Campos inertes não vazam na saída.
- `gerar_diagnostico_tela("orquestrador") == gerar_diagnostico_tela()`.
- Modo executável encerra com código 0.
- `python tela/diagnostico.py` stdout == `gerar_diagnostico_tela()`.
- Proibições de importação em `tela/diagnostico.py`.

#### Atualização obrigatória da pré-condição de subprocess

O loop de subprocess deve referenciar H-0006 (não mais H-0005):

```python
for rotulo, script in (
    ("H-0001", "tela/teste_loader.py"),
    ("H-0002", "tela/teste_modelo.py"),
    ("H-0006", "tela/teste_renderizador.py"),   # era H-0005; formato atualizado
):
```

---

## Critérios de aceite verificáveis

### Escopo e arquivos

- [ ] Somente os arquivos listados em "Arquivos permitidos" foram criados ou
      alterados.
- [ ] Nenhum arquivo fora do escopo autorizado foi criado ou alterado.
- [ ] Nenhum contrato, ADR, nomenclatura, índice, handoff anterior,
      relatório anterior, `config/*.json`, `docs/INDICE.md`,
      `docs/backlog.md` ou `docs/issues.md` foi alterado.

### API e renderer

- [ ] `tela/renderizador.py` mantém `renderizar_tela(modelo: ModeloTela) -> str`.
- [ ] `tela/renderizador.py` mantém `RenderizadorErro(Exception)`.
- [ ] `renderizar_tela` não importa `json`, `os`, `pathlib`, nem chama
      `carregar_tela`.
- [ ] `renderizar_tela` não executa ação, não ativa binding, não altera
      estado, não grava arquivo, não chama subprocess nem eval.
- [ ] `renderizar_tela` não acessa `_campos_inertes` de nenhum `ElementoCorpo`.
- [ ] `renderizar_tela` não acessa `modelo.corpo.elementos`.
- [ ] `renderizar_tela` não acessa `modelo.barra_de_menus`.
- [ ] `renderizar_tela` não acessa `modelo.id` nem `modelo.schema`.
- [ ] `renderizar_tela(None)` lança `RenderizadorErro`.

### Formato da saída

- [ ] A saída começa com `╭ ORQUESTRADOR`.
- [ ] A saída contém `│ Tela raiz do sistema` (conteúdo da caixa de cabeçalho).
- [ ] A saída contém `╭ DASHBOARD` (label hardcoded da caixa de corpo).
- [ ] A saída contém `Dashboard de teste` (conteúdo placeholder hardcoded).
- [ ] A saída contém `Sem dados carregados` (conteúdo placeholder hardcoded).
- [ ] A saída contém `╭ Menu` (label hardcoded da caixa de menu).
- [ ] A saída contém `[Esc] Sair` (texto inerte hardcoded).
- [ ] A saída contém `[B] Borda` (texto inerte hardcoded).
- [ ] A saída contém `╰` (borda inferior).
- [ ] `[Esc]` e `[B]` aparecem apenas como texto inerte — `"[chip_esc]" not in saida`.
- [ ] Chamadas repetidas com o mesmo modelo produzem saída idêntica.
- [ ] Saída com modelo fabricado `titulo="Fab"` começa com `╭ FAB` (renderer
      usa `modelo.cabecalho.titulo`).
- [ ] Saída com modelo fabricado contém `desc fab` (renderer usa
      `modelo.cabecalho.descricao`).
- [ ] Saída com modelo fabricado contém `╭ DASHBOARD` (hardcoded, independe
      do modelo fabricado).
- [ ] Saída bate com o expected output literal definido neste handoff
      (igualdade estrita, incluindo `\n` final).
- [ ] Cada linha da saída tem exatamente 42 chars (contagem Python, sem o `\n`).

### Invariantes preservados

- [ ] `python tela/teste_loader.py` retorna código de saída 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna código de saída 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna código de saída 0 (verificações
      atualizadas para formato H-0006).
- [ ] `python tela/teste_diagnostico.py` retorna código de saída 0 (verificações
      de formato atualizadas).
- [ ] `python tela/diagnostico.py` imprime a saída no formato H-0006 e encerra
      com código de saída 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` é JSON válido e não foi alterado.
- [ ] Nenhum JSON alterado em runtime.
- [ ] Nenhuma ação executada.
- [ ] Nenhum binding ativado.
- [ ] Nenhum chip executado.
- [ ] Nenhum estado gravado.
- [ ] Saída determinística (independente de largura de terminal).
- [ ] Sem dependência de biblioteca de UI (`curses`, `textual`, `rich`, etc.).
- [ ] Sem leitura de `config/estilo.json`.

### Campos inertes na saída

- [ ] A saída não contém `origem_dados`.
- [ ] A saída não contém `bindings`.
- [ ] A saída não contém `filtros`.
- [ ] A saída não contém `tela_destino`.
- [ ] A saída não contém `regra_existencia`.
- [ ] A saída não contém `_campos_inertes`.
- [ ] A saída não contém `[chip_esc]` (id interno do chip não exposto).
- [ ] A saída não contém `[chip_ajuda]` (id interno do chip não exposto).
- [ ] A saída não contém `REGIAO:` (formato antigo H-0005 não deve aparecer).
- [ ] A saída não contém `TELA:` (formato antigo H-0005 não deve aparecer).
- [ ] A saída não contém `SCHEMA:` (formato antigo H-0005 não deve aparecer).

### Relatório

- [ ] `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md` criado com
      resultado `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Comandos de verificação obrigatórios

Executar a partir do diretório raiz do repositório de scripts. O relatório
IMP-0006 deve incluir a saída real de cada comando.

```bash
# 1. Integridade do JSON de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"

# 2. Invariantes de H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes de H-0002 preservados
python tela/teste_modelo.py

# 4. Testes do H-0006 (renderer com borda fixa)
python tela/teste_renderizador.py

# 5. Teste integrado do diagnóstico (verificações atualizadas)
python tela/teste_diagnostico.py

# 6. Ponto de entrada executável
python tela/diagnostico.py

# 7. Verificação de bytecode
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print

# 8. Estado do repositório
git status --short
git diff --stat
```

Todos os comandos devem produzir saída limpa (códigos de saída 0, sem
falhas). `find` deve produzir saída vazia.

---

## Condições de bloqueio

O executor deve parar imediatamente com `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se:

1. Qualquer verificação de H-0001 (`python tela/teste_loader.py`) falhar.
2. Qualquer verificação de H-0002 (`python tela/teste_modelo.py`) falhar.
3. Qualquer verificação de H-0005 (pré-condição) falhar antes da alteração.
4. Qualquer verificação de H-0004 (`python tela/teste_diagnostico.py` com
   formato ainda H-0005) falhar.
5. A implementação exigir criar arquivo fora dos listados em "Arquivos
   permitidos".
6. A implementação exigir alterar contrato, ADR, nomenclatura, índice,
   configuração, backlog, issues, handoff anterior ou relatório anterior.
7. A implementação exigir dependência externa além da stdlib Python.
8. A implementação exigir calcular largura real do terminal.
9. A implementação exigir executar ação, resolver `tela_destino`, ativar
   binding, aplicar filtro, navegar, paginar ou selecionar.
10. A implementação exigir carregar ou aplicar `config/estilo.json`.
11. A implementação exigir alternância de borda ou estado de borda ativo.
12. A implementação exigir cores ou escape codes ANSI.
13. A implementação exigir acessar `_campos_inertes` de qualquer
    `ElementoCorpo`.
14. A implementação exigir acessar `modelo.corpo.elementos`,
    `modelo.barra_de_menus` ou `modelo.schema`.
15. A saída do renderer divergir do expected output literal definido neste
    handoff por razão não prevista aqui.
16. Qualquer linha da saída tiver comprimento Python diferente de 42 chars
    (sem contar `\n`).
17. A implementação exigir tomar decisão arquitetural não coberta por este
    handoff.

---

## Formato esperado do relatório `IMP-0006`

O executor deve criar:

```
docs/relatorios/IMP-0006-tela-minima-borda-fixa.md
```

O relatório deve conter obrigatoriamente:

1. **Objetivo do H-0006**: o que foi especificado e o que foi implementado.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo.
3. **Assinatura da função e módulos importados**: assinatura exata de
   `renderizar_tela` e quais módulos são importados em `tela/renderizador.py`.
4. **Saída real do pipeline** para `orquestrador.json`: reprodução literal da
   string retornada por `renderizar_tela(construir_modelo(carregar_tela(...)))`.
5. **Invariantes de H-0001 e H-0002**: evidência de que as 37 e 30
   verificações respectivas continuam passando (saída dos comandos).
6. **Resultado dos testes do H-0006**: saída completa de
   `python tela/teste_renderizador.py`.
7. **Resultado dos testes do diagnóstico atualizados**: saída completa de
   `python tela/teste_diagnostico.py`.
8. **Resultado do modo executável**: saída de `python tela/diagnostico.py`.
9. **Comportamento fora de escopo preservado como inerte**: lista dos itens
   não implementados e confirmação de que permanecem inertes.
10. **Pendências preservadas**: confirmação de que DOC-B008, DOC-B009 e
    campos `pendente` continuam sem execução.
11. **Saída real de todos os comandos de verificação**: cópia integral.
12. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Checklist final para QA

- [ ] H-0006 lido integralmente antes de qualquer alteração.
- [ ] Pré-condições verificadas (todos os testes anteriores passando).
- [ ] Somente os arquivos autorizados foram criados ou alterados.
- [ ] `git diff --stat` não mostra alterações em arquivos fora do escopo.
- [ ] Nenhum contrato, ADR ou documento normativo alterado.
- [ ] Formato da saída bate com o expected output literal (igualdade estrita).
- [ ] Saída com modelo fabricado `titulo="Fab"` começa com `╭ FAB`.
- [ ] Saída com modelo fabricado contém `desc fab` (dado do modelo).
- [ ] Saída com modelo fabricado contém `╭ DASHBOARD` (hardcoded).
- [ ] `renderizar_tela(None)` lança `RenderizadorErro`.
- [ ] `renderizar_tela` não acessa `_campos_inertes`, `modelo.corpo.elementos`,
      `modelo.barra_de_menus`, `modelo.id` nem `modelo.schema`.
- [ ] `renderizar_tela` não importa `json`, `os`, `pathlib`, nem `carregar_tela`.
- [ ] `python tela/teste_loader.py` retorna 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna 0 (formato H-0006).
- [ ] `python tela/teste_diagnostico.py` retorna 0 (verificações atualizadas).
- [ ] `python tela/diagnostico.py` imprime saída H-0006 e encerra com 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` válido e inalterado.
- [ ] Saída não contém `origem_dados`, `bindings`, `filtros`, `tela_destino`,
      `regra_existencia`, `_campos_inertes`, `TELA:`, `SCHEMA:`, `REGIAO:`.
- [ ] Saída não contém `[chip_esc]` nem `[chip_ajuda]` (ids internos).
- [ ] `[Esc] Sair` e `[B] Borda` são texto inerte — nenhum binding registrado.
- [ ] Cada linha da saída tem exatamente 42 chars Python (sem `\n`).
- [ ] `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md` criado com
      resultado final documentado.
- [ ] Commit não realizado (responsabilidade do engenheiro).
