---
name: H-0007-alternancia-bordas-memoria
description: Handoff de implementação da alternância de bordas em memória — estende renderizar_tela com parâmetro tipo_borda opcional, sem persistência, sem config, preservando saída default do H-0006
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0007
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
    - docs/handoff/H-0006-tela-minima-borda-fixa.md
  issues_relacionadas: []
---

# H-0007 — Alternância de bordas em memória

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/handoff/H-0001-loader-validador-tela-json.md`
3. `docs/handoff/H-0002-modelo-interno-tela.md`
4. `docs/handoff/H-0003-renderizador-textual-estatico.md`
5. `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
6. `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
7. `docs/handoff/H-0006-tela-minima-borda-fixa.md`
8. Este handoff

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

## Contexto herdado de H-0006

O H-0006 foi implementado, aprovado (QA_APPROVED_WITH_NOTES) e commitado
(`6a9315f`). O pacote `tela/` contém atualmente:

```
tela/__init__.py           — marcador de pacote (vazio)
tela/loader.py             — loader/validador macro (H-0001)
tela/teste_loader.py       — diagnóstico H-0001 (37 verificações, passando)
tela/modelo.py             — modelo interno normalizado (H-0002)
tela/teste_modelo.py       — diagnóstico H-0002 (30 verificações, passando)
tela/renderizador.py       — renderer visual com borda fixa (H-0006)
tela/teste_renderizador.py — diagnóstico H-0006 (36 verificações, passando)
tela/diagnostico.py        — ponto de entrada executável (H-0004)
tela/teste_diagnostico.py  — diagnóstico H-0004/H-0006 (26 verificações, passando)
```

### Pipeline estabelecido (H-0006)

```
config/telas/orquestrador.json
    → carregar_tela(None, "orquestrador")   [tela/loader.py       — H-0001]
    → dict (tela_raw)
    → construir_modelo(tela_raw)            [tela/modelo.py       — H-0002]
    → ModeloTela
    → renderizar_tela(modelo)               [tela/renderizador.py — H-0006]
    → str
```

### Saída default do H-0006 (borda curva)

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

Cada linha visual tem exatamente 42 caracteres Python. A saída termina com
`\n`. Esta saída **deve ser preservada como default do H-0007 sem alteração**.

### Largura fixa — nota de contexto (não normativa)

As constantes `TOTAL_WIDTH = 42`, `INNER_WIDTH = 40`, `CONTENT_WIDTH = 39`
foram introduzidas pelo H-0006 como exceção técnica provisória do estágio zero.

O H-0007 **preserva essas constantes provisoriamente**. Esta preservação:

- Não formaliza a largura fixa como regra de layout final.
- Não declara que essas constantes cumprem o contrato final de composição
  de corpo.
- Não autoriza calcular largura real de terminal.
- Não autoriza leitura de `config/layout_console.json` nem
  `config/lancador.json`.

Se surgir necessidade de resolver largura dinâmica, resize, layout por
terminal ou parâmetros de `config/layout_console.json` / `config/lancador.json`,
o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED` e registrar como
ciclo próprio posterior de layout — esses assuntos não pertencem ao H-0007.

### Pendências que permanecem inertes

- **DOC-B008**: tipos internos de item de `console` não definidos.
- **DOC-B009**: registry completo de ações e tipos de chip não fechado.
- **`lancador_principal.itens`**: lista vazia; `tela_destino` pendente.
- **`bindings`** e **`referencias_de_acoes`**: declarados como pendentes.

O renderer não deve tratar essas pendências como erro. São declaração inerte
no modelo — o renderer as ignora completamente.

---

## Objetivo técnico

Estender `tela/renderizador.py` para que `renderizar_tela` aceite um parâmetro
opcional `tipo_borda` que seleciona o conjunto de caracteres de borda **em
memória**, sem UI interativa, sem leitura de configuração externa, sem
persistência de qualquer natureza.

A chamada padrão sem `tipo_borda` deve continuar produzindo **exatamente** a
saída default do H-0006 — igualdade estrita, incluindo o `\n` final.

A alternância é exercitada apenas por chamada de função (em teste ou em código
que chama o renderer diretamente). Não há captura de teclado, não há loop de
aplicação, não há binding.

---

## API congelada

A assinatura do H-0007 é exatamente:

```python
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

**Esta é a única API autorizada. O implementador não pode escolher outra.**

Regras da assinatura:

| Aspecto | Regra |
|---|---|
| Parâmetro `modelo` | `ModeloTela` — obrigatório, mesma semântica do H-0006 |
| Parâmetro `tipo_borda` | `str`, opcional, default `"curva"` |
| Valores aceitos para `tipo_borda` | `"curva"` e `"reta"` — exatamente estes dois |
| Valor inválido para `tipo_borda` | Lançar `RenderizadorErro` |
| Retorno | `str` — representação visual determinística |
| Efeitos colaterais | Nenhum |

A chamada `renderizar_tela(modelo)` (sem `tipo_borda`) deve produzir saída
**idêntica** à produzida pela versão H-0006. A chamada
`renderizar_tela(modelo, tipo_borda="curva")` deve produzir saída **idêntica**
à chamada sem `tipo_borda`. Esta é uma invariante obrigatória, não opcional.

---

## Conjuntos de bordas

O H-0007 define exatamente dois conjuntos de bordas, identificados pelos
nomes `"curva"` e `"reta"`. Estes nomes são congelados — o implementador
não pode usar outros nomes nem adicionar outros conjuntos.

### Conjunto `"curva"` — default, saída H-0006

| Posição | Caractere | Unicode | Nome |
|---|---|---|---|
| Canto superior esquerdo | `╭` | U+256D | Canto arredondado |
| Canto superior direito | `╮` | U+256E | Canto arredondado |
| Canto inferior esquerdo | `╰` | U+2570 | Canto arredondado |
| Canto inferior direito | `╯` | U+256F | Canto arredondado |
| Borda vertical | `│` | U+2502 | Linha vertical |
| Borda horizontal | `─` | U+2500 | Linha horizontal |

### Conjunto `"reta"` — alternativa

| Posição | Caractere | Unicode | Nome |
|---|---|---|---|
| Canto superior esquerdo | `┌` | U+250C | Canto reto |
| Canto superior direito | `┐` | U+2510 | Canto reto |
| Canto inferior esquerdo | `└` | U+2514 | Canto reto |
| Canto inferior direito | `┘` | U+2518 | Canto reto |
| Borda vertical | `│` | U+2502 | Linha vertical (mesmo de `curva`) |
| Borda horizontal | `─` | U+2500 | Linha horizontal (mesmo de `curva`) |

**Observação**: os caracteres de borda vertical (`│`) e borda horizontal (`─`)
são idênticos nos dois conjuntos. Apenas os quatro cantos diferem entre
`"curva"` e `"reta"`.

---

## Escopo positivo

O H-0007 **autoriza e especifica**:

1. Alterar `tela/renderizador.py` para aceitar `tipo_borda` e implementar
   os dois conjuntos de bordas em memória.
2. Alterar `tela/teste_renderizador.py` para verificar a alternância de borda.
3. Alterar `tela/teste_diagnostico.py` somente se alguma verificação existente
   quebrar após a mudança de assinatura de `renderizar_tela`. Preferência:
   nenhuma alteração.
4. Criar `docs/relatorios/IMP-0007-alternancia-bordas-memoria.md`.

---

## Fora de escopo — proibições explícitas

O H-0007 **não implementa** nenhum dos itens abaixo:

- persistência de estilo ou de `tipo_borda`;
- leitura de `config/estilo.json` (nem parcial);
- leitura de `config/barra_de_menus.json`;
- leitura de `config/layout_console.json`;
- leitura de `config/lancador.json`;
- leitura de qualquer arquivo em `config/`;
- alteração de `config/telas/orquestrador.json`;
- preset completo de estilo ou tema;
- ciclo de estilo;
- layout responsivo ou ajuste dinâmico de tamanho de caixa ou janela;
- cálculo de largura real do terminal;
- largura dinâmica;
- resize;
- formalização da largura fixa como regra de layout;
- cores ou escape codes ANSI;
- captura real de teclado;
- binding da tecla `B` ou qualquer outra tecla;
- loop de aplicação;
- ações reais;
- registry de ações;
- registry de tipos;
- navegação entre telas;
- navegação por `tela_destino`;
- pop-up;
- dashboard real com dados;
- filtros funcionais;
- paginação funcional;
- seleção;
- `curses`, `textual`, `rich` ou qualquer biblioteca de UI;
- estado de borda persistido além da chamada de função;
- mais de dois conjuntos de borda (`"curva"` e `"reta"` são os únicos).

O texto `[B] Borda` continua aparecendo no menu inferior como texto inerte.
Neste ciclo, ele não executa ação real por teclado.

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os arquivos abaixo:

```
tela/renderizador.py                                    — ALTERAR
tela/teste_renderizador.py                              — ALTERAR
tela/teste_diagnostico.py                               — ALTERAR só se necessário
docs/relatorios/IMP-0007-alternancia-bordas-memoria.md  — CRIAR
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
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

O módulo `tela/renderizador.py` deve manter:

- `class RenderizadorErro(Exception)` — inalterada.
- `def renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str`
  — assinatura exatamente como definido acima.

### Constantes de layout (preservadas do H-0006, provisórias)

```python
TOTAL_WIDTH   = 42
INNER_WIDTH   = 40
CONTENT_WIDTH = 39
_LABEL_MAX    = 38
```

Estas constantes **não mudam**. São preservadas provisoriamente — sem
declaração normativa de layout.

### Conjuntos de bordas em memória

O módulo deve definir em nível de módulo (antes de qualquer função) um
dicionário ou estrutura equivalente que associe os nomes `"curva"` e
`"reta"` aos respectivos conjuntos de seis caracteres. Exemplo de estrutura
aceitável (o implementador pode usar outro nome de variável ou outra
organização interna equivalente):

```python
_BORDAS = {
    "curva": {
        "tl": "╭", "tr": "╮",
        "bl": "╰", "br": "╯",
        "v":  "│", "h":  "─",
    },
    "reta": {
        "tl": "┌", "tr": "┐",
        "bl": "└", "br": "┘",
        "v":  "│", "h":  "─",
    },
}
```

Restrições obrigatórias para essa estrutura:

- Definida como constante em tempo de importação do módulo.
- Sem leitura de arquivo externo (proibido abrir JSON, ler disco ou usar
  `import json`).
- Os caracteres de cada conjunto correspondem exatamente à tabela da seção
  "Conjuntos de bordas".
- As chaves aceitas são `"curva"` e `"reta"` — sem outras.

### Validação de `tipo_borda`

```python
if tipo_borda not in _BORDAS:
    raise RenderizadorErro(
        "tipo_borda invalido: {0!r}; valores aceitos: curva, reta".format(tipo_borda)
    )
```

O nome interno `_BORDAS` é sugestivo; o implementador pode usar outro nome
desde que a lógica seja equivalente. A validação é case-sensitive:
`"CURVA"` e `"Curva"` são inválidos.

### Validação de `modelo`

Mantida do H-0006: verificar `isinstance(modelo, ModeloTela)` antes de
qualquer processamento. Se `modelo` não for `ModeloTela`, lançar
`RenderizadorErro`. A ordem de validação (`modelo` antes ou depois de
`tipo_borda`) é livre, desde que ambas as validações ocorram antes de
qualquer renderização.

### Funções internas

As funções internas existentes (`_linha_topo`, `_linha_base`,
`_linha_conteudo`, `_caixa`) devem ser atualizadas para receber o conjunto
de caracteres de borda resolvido como parâmetro adicional. A assinatura
interna exata é livre, desde que o comportamento externo corresponda às
especificações deste handoff.

### Importações

Importação obrigatória no módulo do renderer:

```python
from tela.modelo import ModeloTela
```

Importações proibidas em `tela/renderizador.py` (mesmas do H-0006):

- `import json`
- `import os`
- `import pathlib` / `from pathlib import ...`
- `from tela.loader import carregar_tela`
- `subprocess`, `exec`, `eval` ou qualquer mecanismo de execução de processo

### Contrato da função

| Aspecto | Regra |
|---|---|
| Entrada `modelo` | `ModeloTela` — mesmo contrato do H-0006 |
| Entrada `tipo_borda` | `str`, default `"curva"`; aceita `"curva"` e `"reta"` |
| Saída | `str` — determinística, visual, sem escape codes ANSI |
| Efeitos colaterais | Nenhum — não altera modelo, não grava arquivo, não lê config |
| Determinismo | Dado o mesmo `ModeloTela` e o mesmo `tipo_borda`, sempre retorna a mesma string |
| Independência de terminal | A saída não muda conforme a largura do terminal |
| Invariante de default | `renderizar_tela(m)` == `renderizar_tela(m, tipo_borda="curva")` para qualquer `ModeloTela` válido `m` |
| Invariante de conteúdo | Para qualquer `ModeloTela` válido `m`, o conteúdo textual é o mesmo em `"curva"` e `"reta"`; apenas os quatro cantos diferem |

### Campos que o renderer pode ou não acessar (mesmos do H-0006)

O renderer **usa** apenas:

- `modelo.cabecalho.get("titulo", "(ausente)")` — label da caixa de cabeçalho.
- `modelo.cabecalho.get("descricao", "(ausente)")[:39]` — conteúdo da caixa
  de cabeçalho.

O renderer **não acessa**:

- `modelo.corpo.elementos` (corpo não é consultado).
- `modelo.barra_de_menus` (não consultado).
- `modelo.id`, `modelo.schema` (não aparecem na saída).
- `modelo._raw`.
- `_campos_inertes` de qualquer `ElementoCorpo`.

---

## Saída esperada — borda `"curva"` (default, idêntica ao H-0006)

```python
_EXPECTED_ORQUESTRADOR_CURVA = (
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

Esta constante é idêntica a `_EXPECTED_ORQUESTRADOR` já existente em
`tela/teste_renderizador.py`. O teste de igualdade estrita com o expected
output do H-0006 deve ser mantido sem alteração.

---

## Saída esperada — borda `"reta"`

```python
_EXPECTED_ORQUESTRADOR_RETA = (
    "┌ ORQUESTRADOR ──────────────────────────┐\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "└────────────────────────────────────────┘\n"
    "\n"
    "┌ DASHBOARD ─────────────────────────────┐\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "└────────────────────────────────────────┘\n"
    "\n"
    "┌ Menu ──────────────────────────────────┐\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "└────────────────────────────────────────┘\n"
)
```

### Verificação linha a linha — borda `"reta"` (total = 42 chars Python cada)

| Linha | Composição | Total |
|---|---|---|
| `┌ ORQUESTRADOR ──────────────────────────┐` | 1+1+12+1+26+1 | 42 |
| `│ Tela raiz do sistema — ponto de entrada│` | 1+1+39+1 | 42 |
| `└────────────────────────────────────────┘` | 1+40+1 | 42 |
| `┌ DASHBOARD ─────────────────────────────┐` | 1+1+9+1+29+1 | 42 |
| `│ Dashboard de teste                     │` | 1+1+18+21+1 | 42 |
| `│ Sem dados carregados                   │` | 1+1+20+19+1 | 42 |
| `┌ Menu ──────────────────────────────────┐` | 1+1+4+1+34+1 | 42 |
| `│ [Esc] Sair    [B] Borda                │` | 1+1+23+16+1 | 42 |

### Invariante de conteúdo entre bordas

Trocando `tipo_borda` de `"curva"` para `"reta"`:

- Apenas os quatro caracteres de canto mudam: `╭→┌`, `╮→┐`, `╰→└`, `╯→┘`.
- Os caracteres `│` e `─` permanecem iguais.
- Todo o conteúdo textual (títulos, textos das caixas) permanece idêntico.
- A largura de cada linha permanece 42 chars Python.

---

## Pré-condição obrigatória

Antes de alterar qualquer arquivo, o executor deve confirmar que os
invariantes de todos os handoffs anteriores estão passando:

```bash
python tela/teste_loader.py    # 37 verificações passando
python tela/teste_modelo.py    # 30 verificações passando
python tela/teste_renderizador.py  # 36 verificações passando (formato H-0006)
python tela/teste_diagnostico.py   # 26 verificações passando
python tela/diagnostico.py         # imprime saída H-0006 e encerra com código 0
```

Se qualquer verificação falhar, o executor deve parar imediatamente com
`BLOCKED` e registrar qual verificação falhou e em qual módulo.

---

## Testes obrigatórios

### `tela/teste_renderizador.py` — atualizado para H-0007

#### Estrutura obrigatória do script

Preservar a estrutura do H-0006:

- `sys.dont_write_bytecode = True` antes de qualquer import.
- Importar apenas da biblioteca padrão, de `tela.loader`, `tela.modelo` e
  `tela.renderizador`.
- Imprimir `[PASSOU] <nome>` ou `[FALHOU] <nome>` para cada verificação.
- Imprimir ao final: `Total de verificacoes`, `Passaram`, `Falharam`.
- Retornar código de saída 0 se todos passaram, 1 se algum falhou.
- Não usar `unittest`, `pytest` nem nenhum framework externo.

#### Seções existentes (H-0006) — devem continuar passando sem alteração

As seções 1 a 5 do H-0006 devem continuar presentes e passar sem
modificação:

- Seção 1 — Renderer sobre `orquestrador.json`
- Seção 2 — Modelo fabricado
- Seção 3 — Casos de erro do renderer
- Seção 4 — Proibições de import/leitura no módulo do renderer
- Seção 5 — Inércia

As verificações `renderizar_tela(None) lanca RenderizadorErro` e
`renderizar_tela(<dict>) lanca RenderizadorErro` devem continuar passando.

#### Seção 6 — Alternância de borda (NOVA)

Adicionar uma nova seção de testes cobrindo exclusivamente a alternância
em memória. A constante `_EXPECTED_ORQUESTRADOR_RETA` definida neste
handoff deve ser declarada no script de teste.

| Verificação | Critério |
|---|---|
| `renderizar_tela(modelo, tipo_borda="curva")` sem exceção | Nenhuma exceção lançada |
| `renderizar_tela(modelo, tipo_borda="curva")` == `renderizar_tela(modelo)` | Igualdade estrita |
| `renderizar_tela(modelo, tipo_borda="reta")` sem exceção | Nenhuma exceção lançada |
| Saída `reta` é `str` | `isinstance(saida_reta, str) is True` |
| Saída `reta` contém `┌` (canto superior esquerdo reto) | `"┌" in saida_reta` |
| Saída `reta` contém `┐` (canto superior direito reto) | `"┐" in saida_reta` |
| Saída `reta` contém `└` (canto inferior esquerdo reto) | `"└" in saida_reta` |
| Saída `reta` contém `┘` (canto inferior direito reto) | `"┘" in saida_reta` |
| Saída `reta` não contém `╭` (canto curvo ausente) | `"╭" not in saida_reta` |
| Saída `reta` não contém `╮` (canto curvo ausente) | `"╮" not in saida_reta` |
| Saída `reta` não contém `╰` (canto curvo ausente) | `"╰" not in saida_reta` |
| Saída `reta` não contém `╯` (canto curvo ausente) | `"╯" not in saida_reta` |
| Saída `reta` contém `"│ Tela raiz do sistema"` (conteúdo preservado) | `"│ Tela raiz do sistema" in saida_reta` |
| Saída `reta` contém `"Dashboard de teste"` (conteúdo preservado) | `"Dashboard de teste" in saida_reta` |
| Saída `reta` contém `"[B] Borda"` (menu inerte preservado) | `"[B] Borda" in saida_reta` |
| Cada linha da saída `reta` tem exatamente 42 chars Python | `all(len(ln) == 42 for ln in saida_reta.split("\n") if ln != "")` |
| Saída `reta` bate com `_EXPECTED_ORQUESTRADOR_RETA` (igualdade estrita) | `saida_reta == _EXPECTED_ORQUESTRADOR_RETA` |
| `renderizar_tela(modelo, tipo_borda="invalida")` lança `RenderizadorErro` | Exceção do tipo correto |
| `renderizar_tela(modelo, tipo_borda="CURVA")` lança `RenderizadorErro` (case sensitive) | Exceção do tipo correto |
| Saída `reta` é determinística (duas chamadas idênticas) | `renderizar_tela(m, "reta") == renderizar_tela(m, "reta")` |

### `tela/teste_diagnostico.py` — condicionalmente atualizado

Preferência: **nenhuma alteração**.

O `tela/diagnostico.py` chama `renderizar_tela(modelo)` sem `tipo_borda`,
que produz a saída `"curva"` (default). As verificações existentes em
`tela/teste_diagnostico.py` comparam com `_EXPECTED_ORQUESTRADOR` (curva),
que continuará válido após o H-0007.

Só alterar `tela/teste_diagnostico.py` se alguma verificação existente
falhar após a alteração de `tela/renderizador.py`. Nesse caso, o executor
deve descrever qual verificação falhou, por que falhou, e qual a alteração
mínima necessária para restaurar o invariante sem sair do escopo autorizado.
Se não houver alteração mínima disponível dentro do escopo, parar com
`BLOCKED`.

---

## Critérios de aceite verificáveis

### Escopo e arquivos

- [ ] Somente os arquivos listados em "Arquivos permitidos" foram criados
      ou alterados.
- [ ] Nenhum arquivo fora do escopo autorizado foi criado ou alterado.
- [ ] Nenhum contrato, ADR, nomenclatura, índice, handoff anterior,
      relatório anterior, `config/*.json`, `docs/INDICE.md`,
      `docs/backlog.md` ou `docs/issues.md` foi alterado.

### API e assinatura

- [ ] `tela/renderizador.py` mantém `renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str`.
- [ ] `tela/renderizador.py` mantém `RenderizadorErro(Exception)`.
- [ ] `renderizar_tela(None)` continua lançando `RenderizadorErro`.
- [ ] `renderizar_tela(<dict>)` continua lançando `RenderizadorErro`.
- [ ] `renderizar_tela(modelo, tipo_borda="invalida")` lança `RenderizadorErro`.
- [ ] `renderizar_tela(modelo, tipo_borda="CURVA")` lança `RenderizadorErro`
      (case sensitive).
- [ ] `renderizar_tela` não importa `json`, `os`, `pathlib`, nem chama
      `carregar_tela`.
- [ ] `renderizar_tela` não abre arquivos em disco para obter bordas.
- [ ] Os conjuntos de bordas são definidos em memória como constantes no
      módulo, sem acesso a disco.

### Saída default preservada (H-0006)

- [ ] `renderizar_tela(modelo)` produz saída idêntica ao H-0006 (igualdade
      estrita, incluindo `\n` final).
- [ ] `renderizar_tela(modelo, tipo_borda="curva")` produz saída idêntica
      ao H-0006.
- [ ] `renderizar_tela(modelo)` == `renderizar_tela(modelo, tipo_borda="curva")`.
- [ ] A saída default começa com `╭ ORQUESTRADOR`.
- [ ] A saída default contém `╰` (canto curvo inferior).
- [ ] Cada linha da saída default tem exatamente 42 chars Python.

### Borda alternativa (`"reta"`)

- [ ] `renderizar_tela(modelo, tipo_borda="reta")` não lança exceção.
- [ ] Saída `reta` contém `┌`, `┐`, `└`, `┘`.
- [ ] Saída `reta` não contém `╭`, `╮`, `╰`, `╯`.
- [ ] Saída `reta` contém `│ Tela raiz do sistema` (conteúdo preservado).
- [ ] Saída `reta` contém `Dashboard de teste` (conteúdo preservado).
- [ ] Saída `reta` contém `[B] Borda` (menu inerte preservado).
- [ ] Cada linha da saída `reta` tem exatamente 42 chars Python.
- [ ] Saída `reta` bate com `_EXPECTED_ORQUESTRADOR_RETA` (igualdade estrita).
- [ ] Saída `reta` é determinística (duas chamadas com mesmo modelo produzem
      saída idêntica).

### Invariante de conteúdo entre bordas

- [ ] Trocando `tipo_borda` de `"curva"` para `"reta"`, apenas os quatro
      cantos mudam.
- [ ] `│` e `─` são iguais em curva e reta.
- [ ] Conteúdo textual (títulos, textos de caixa) é igual entre curva e reta.
- [ ] Largura de cada linha permanece 42 chars em ambas as bordas.

### Preservação de largura (provisória)

- [ ] As constantes `TOTAL_WIDTH = 42`, `INNER_WIDTH = 40`,
      `CONTENT_WIDTH = 39` estão presentes e inalteradas no módulo.
- [ ] Nenhuma leitura de `config/layout_console.json` nem
      `config/lancador.json`.
- [ ] Nenhum cálculo de largura de terminal.
- [ ] Nenhuma declaração normativa de layout nos arquivos alterados.

### Invariantes preservados

- [ ] `python tela/teste_loader.py` retorna código de saída 0 (37
      verificações).
- [ ] `python tela/teste_modelo.py` retorna código de saída 0 (30
      verificações).
- [ ] `python tela/teste_renderizador.py` retorna código de saída 0
      (seções 1–5 do H-0006 inalteradas + seção 6 nova).
- [ ] `python tela/teste_diagnostico.py` retorna código de saída 0.
- [ ] `python tela/diagnostico.py` imprime a saída H-0006 (curva) e encerra
      com código de saída 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` é JSON válido e não foi alterado.

### Inércia e proibições

- [ ] `renderizar_tela` não altera `modelo._raw`.
- [ ] `renderizar_tela` não altera `modelo.cabecalho`.
- [ ] `renderizar_tela` não acessa `_campos_inertes`.
- [ ] `renderizar_tela` não acessa `modelo.corpo.elementos`.
- [ ] `renderizar_tela` não acessa `modelo.barra_de_menus`.
- [ ] `renderizar_tela` não acessa `modelo.id` nem `modelo.schema`.
- [ ] Saída não contém `origem_dados`, `bindings`, `filtros`,
      `tela_destino`, `regra_existencia`, `_campos_inertes`.
- [ ] Saída não contém `[chip_esc]` nem `[chip_ajuda]` (ids internos).
- [ ] `[B] Borda` continua texto inerte — nenhum binding registrado.
- [ ] Nenhuma ação real criada.
- [ ] Nenhum loop ou interação criado.
- [ ] Sem leitura de `config/estilo.json`.
- [ ] Sem leitura de `config/barra_de_menus.json`.

### Relatório

- [ ] `docs/relatorios/IMP-0007-alternancia-bordas-memoria.md` criado com
      resultado `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Comandos de verificação obrigatórios

Executar a partir do diretório raiz do repositório de scripts. O relatório
IMP-0007 deve incluir a saída real de cada comando.

```bash
# 1. Integridade do JSON de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"

# 2. Invariantes de H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes de H-0002 preservados
python tela/teste_modelo.py

# 4. Testes do H-0007 (renderer com alternância de borda)
python tela/teste_renderizador.py

# 5. Teste integrado do diagnóstico
python tela/teste_diagnostico.py

# 6. Ponto de entrada executável (deve produzir saída curva/H-0006)
python tela/diagnostico.py

# 7. Verificação de bytecode
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print

# 8. Estado do repositório
git status --short
git diff --stat
git diff --name-only
```

Todos os comandos devem produzir saída limpa (códigos de saída 0, sem
falhas). `find` deve produzir saída vazia.

---

## Condições de bloqueio

O executor deve parar imediatamente com `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se:

1. Qualquer verificação de H-0001 (`python tela/teste_loader.py`) falhar.
2. Qualquer verificação de H-0002 (`python tela/teste_modelo.py`) falhar.
3. Qualquer verificação pré-condição de H-0006 (`python
   tela/teste_renderizador.py` antes da alteração) falhar.
4. Qualquer verificação de `python tela/teste_diagnostico.py` falhar e não
   houver alteração mínima disponível dentro do escopo autorizado.
5. A implementação exigir criar arquivo fora dos listados em "Arquivos
   permitidos".
6. A implementação exigir alterar contrato, ADR, nomenclatura, índice,
   configuração, backlog, issues, handoff anterior ou relatório anterior.
7. A implementação exigir dependência externa além da stdlib Python.
8. A implementação exigir calcular largura real do terminal.
9. A implementação exigir leitura de `config/layout_console.json`,
   `config/lancador.json`, `config/estilo.json` ou qualquer arquivo em
   `config/`.
10. A implementação exigir captura de teclado para alternar borda.
11. A implementação exigir persistência de `tipo_borda` entre chamadas.
12. A implementação exigir mais de dois conjuntos de borda.
13. A implementação exigir cores ou escape codes ANSI.
14. A saída com `tipo_borda="curva"` divergir do expected output H-0006 por
    qualquer razão.
15. Qualquer linha de saída tiver comprimento Python diferente de 42 chars
    (sem contar `\n`).
16. A implementação exigir tomar decisão arquitetural não coberta por este
    handoff.
17. Surgir necessidade de largura dinâmica, resize ou layout por terminal:
    parar com `ARCHITECTURE_REVIEW_REQUIRED` — registrar como ciclo próprio
    posterior de layout, sem implementar nada disso no H-0007.

---

## Formato esperado do relatório `IMP-0007`

O executor deve criar:

```
docs/relatorios/IMP-0007-alternancia-bordas-memoria.md
```

O relatório deve conter obrigatoriamente:

1. **Objetivo do H-0007**: o que foi especificado e o que foi implementado.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo.
3. **Assinatura da função e estrutura de bordas**: assinatura exata de
   `renderizar_tela` e como os conjuntos de borda estão definidos em memória
   (excerto da constante `_BORDAS` ou equivalente).
4. **Saída real do pipeline** para `orquestrador.json` com
   `tipo_borda="curva"`: reprodução literal da string — deve ser idêntica
   ao H-0006.
5. **Saída real do pipeline** para `orquestrador.json` com
   `tipo_borda="reta"`: reprodução literal da string.
6. **Invariantes de H-0001 e H-0002**: evidência de que as 37 e 30
   verificações respectivas continuam passando.
7. **Resultado dos testes do H-0007**: saída completa de
   `python tela/teste_renderizador.py`.
8. **Resultado dos testes do diagnóstico**: saída completa de
   `python tela/teste_diagnostico.py`.
9. **Resultado do modo executável**: saída de `python tela/diagnostico.py`
   (deve ser saída curva/H-0006).
10. **Comportamento fora de escopo preservado como inerte**: lista dos itens
    não implementados e confirmação de que permanecem inertes.
11. **Saída real de todos os comandos de verificação**: cópia integral.
12. **Nota sobre largura fixa**: confirmação explícita de que
    `TOTAL_WIDTH=42`, `INNER_WIDTH=40`, `CONTENT_WIDTH=39` foram
    preservadas provisoriamente sem declaração normativa de layout.
13. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Checklist final para QA

- [ ] H-0007 lido integralmente antes de qualquer alteração.
- [ ] Pré-condições verificadas (todos os testes anteriores passando).
- [ ] Somente os arquivos autorizados foram criados ou alterados.
- [ ] `git diff --stat` não mostra alterações em arquivos fora do escopo.
- [ ] Nenhum contrato, ADR ou documento normativo alterado.
- [ ] Assinatura `renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str` implementada.
- [ ] `renderizar_tela(modelo)` == `renderizar_tela(modelo, tipo_borda="curva")` (igualdade estrita).
- [ ] `renderizar_tela(modelo)` com saída idêntica ao H-0006 (igualdade
      estrita com `_EXPECTED_ORQUESTRADOR`).
- [ ] `renderizar_tela(modelo, tipo_borda="reta")` sem exceção.
- [ ] Saída `reta` contém `┌`, `┐`, `└`, `┘` e não contém `╭`, `╮`, `╰`, `╯`.
- [ ] Saída `reta` com conteúdo textual idêntico à saída `curva`.
- [ ] Saída `reta` bate com `_EXPECTED_ORQUESTRADOR_RETA` (igualdade estrita).
- [ ] Cada linha de qualquer saída tem exatamente 42 chars Python.
- [ ] `renderizar_tela(modelo, tipo_borda="invalida")` lança `RenderizadorErro`.
- [ ] `renderizar_tela(modelo, tipo_borda="CURVA")` lança `RenderizadorErro`.
- [ ] `renderizar_tela(None)` lança `RenderizadorErro`.
- [ ] Conjuntos de borda definidos em memória (sem leitura de arquivo).
- [ ] `python tela/teste_loader.py` retorna 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna 0.
- [ ] `python tela/teste_diagnostico.py` retorna 0.
- [ ] `python tela/diagnostico.py` imprime saída H-0006 (curva) e encerra
      com 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` válido e inalterado.
- [ ] Saída não contém `origem_dados`, `bindings`, `filtros`,
      `tela_destino`, `regra_existencia`, `_campos_inertes`.
- [ ] `[B] Borda` é texto inerte — nenhum binding registrado.
- [ ] Sem leitura de `config/estilo.json`, `config/barra_de_menus.json`,
      `config/layout_console.json`, `config/lancador.json`.
- [ ] Largura fixa provisória preservada sem declaração normativa.
- [ ] `docs/relatorios/IMP-0007-alternancia-bordas-memoria.md` criado com
      resultado final documentado.
- [ ] Commit não realizado (responsabilidade do engenheiro).
