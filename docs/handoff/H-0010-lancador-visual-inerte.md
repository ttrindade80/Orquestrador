---
name: H-0010-lancador-visual-inerte
description: Handoff de implementação — bloco visual inerte de lancador na demo, com itens hardcoded (chip, texto, tela_destino inativo), sem navegação real, sem registry e sem acionamento
metadata:
  type: handoff_implementacao
  status: SUPERSEDED_BLOQUEADO_NAO_IMPLEMENTAR
  id: H-0010
  data_criacao: 2026-07-08
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_lancador.md
  handoffs_anteriores:
    - docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md
  issues_relacionadas: []
---

# H-0010 — Lançador visual inerte

## Status

SUPERSEDED — BLOQUEADO — NÃO IMPLEMENTAR

## Aviso de superação

Este handoff foi bloqueado pela auditoria `RELATORIO_AUDITORIA_H-0010_HANDOFF.md` com status `ARCHITECTURE_REVIEW_REQUIRED`.

Não implementar este handoff.

Motivo: ele autorizava itens hardcoded no renderer e tratava `tela_destino` como campo inativo, em conflito com a resolução documental posterior.

Este ciclo será substituído por:

- H-0010A — Tela destino mínima / stub
- H-0010B — Lançador visual declarativo

## Contexto

O H-0009 foi implementado, aprovado (`QA_APPROVED_WITH_NOTES`) e commitado (`57f36d2`).

O pacote `tela/` está assim após H-0009:

```
tela/__init__.py             — marcador de pacote (vazio)
tela/loader.py               — loader/validador macro (H-0001)
tela/teste_loader.py         — 37 verificações, passando
tela/modelo.py               — modelo interno normalizado (H-0002)
tela/teste_modelo.py         — 30 verificações, passando
tela/renderizador.py         — renderer visual com largura dinâmica (H-0006/H-0007/H-0009)
tela/teste_renderizador.py   — 65 verificações, passando
tela/diagnostico.py          — ponto de entrada não interativo (H-0004)
tela/teste_diagnostico.py    — 26 verificações, passando
tela/demo.py                 — aplicação demonstrável com TTY sem echo (H-0008/H-0009)
tela/teste_demo.py           — 69 verificações, passando
```

`config/telas/orquestrador.json` contém um elemento de corpo do tipo `lancador` com
`id: "lancador_principal"`, `titulo: "Navegar"` e `itens: []` (vazio — pendência
documentada no JSON como `"pendencia_itens"`). Não há itens reais declarados.

O renderer atual (`renderizador.py`) gera três caixas hardcoded: `ORQUESTRADOR`
(derivada do modelo), `DASHBOARD` (placeholder) e `Menu` (placeholder de
barra_de_menus). Não há caixa visual de `lancador` no output.

## Objetivo

Estender `tela/renderizador.py` para incluir um bloco visual de `lancador` com itens
hardcoded simples (placeholder), sem qualquer forma de navegação, acionamento, registry
ou resolução de `tela_destino`.

A `tela/demo.py` passa a exibir o bloco de `lancador` automaticamente (via renderer),
preservando todos os comportamentos aprovados em H-0009: `b` alternando borda, Esc
saindo, `s` como atalho auxiliar, largura dinâmica e saída determinística via pipe.

## Leitura obrigatória realizada

Os seguintes artefatos foram lidos antes da redação deste handoff:

- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0009_HANDOFF.md`
- `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md`
- `docs/relatorios/RELATORIO_QA_H-0009_LAYOUT_TERMINAL_ENTRADA_SEM_ECHO.md`
- `tela/renderizador.py`
- `tela/demo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/diagnostico.py`
- `tela/teste_diagnostico.py`
- `config/telas/orquestrador.json`

## Escopo positivo

O H-0010 autoriza e especifica:

1. Adicionar a constante `_ITENS_LANCADOR` em `tela/renderizador.py` com itens hardcoded
   placeholder.
2. Adicionar a função `_caixa_lancador` em `tela/renderizador.py` que valida `texto`
   (≤ 15 chars, levanta `RenderizadorErro` se exceder) e monta o bloco visual.
3. Atualizar `renderizar_tela` em `tela/renderizador.py` para incluir a caixa do
   `lancador` na saída, posicionada entre a caixa do dashboard e a caixa do menu.
4. Atualizar `tela/teste_renderizador.py` com novos esperados e testes da caixa do
   lancador (presença de itens, rejeição de texto longo, inatividade de tela_destino).
5. Atualizar `tela/teste_demo.py` com novos esperados (constantes de string com o bloco
   do lancador) e verificações de presença na saída subprocess.
6. Atualizar `tela/teste_diagnostico.py` com novo esperado (constante de string com o
   bloco do lancador).
7. Criar `docs/relatorios/IMP-0010-lancador-visual-inerte.md`.

## Escopo negativo

O H-0010 **não implementa** nenhum dos itens abaixo:

- chamada real de tela;
- navegação por `tela_destino`;
- validação de existência de `tela_destino` como tela real;
- resolução ou abertura de `tela_destino`;
- registry de telas;
- registry de ações;
- bindings ativos;
- execução de ação;
- cursor de lançador;
- navegação por setas;
- navegação por `[✥]`;
- console real;
- dashboard real;
- dados reais;
- filtro;
- paginação;
- seleção;
- toggle;
- tela de processamento;
- leitura de `config/lancador.json`, `config/estilo.json` ou qualquer outro arquivo em
  `config/`;
- leitura de itens do `lancador_principal` em `config/telas/orquestrador.json` (os
  itens da demo são hardcoded como placeholder, independentemente do JSON);
- alteração de contratos;
- alteração de ADRs;
- alteração de NOMENCLATURA;
- alteração de documentação normativa;
- alteração de `config/telas/orquestrador.json` ou qualquer outro arquivo em `config/`.

## Decisão de inércia do lançador neste ciclo

O `contrato_lancador.md` define que o papel normal de um item de `lancador` é navegação
para `tela_destino`. Neste H-0010, o objetivo é **visual inerte**. A resolução é:

- `tela_destino` existe nos itens hardcoded apenas como dado declarativo preservado —
  chave presente no dict, valor nunca utilizado pelo renderer.
- Nenhum item chama, resolve, valida existência ou abre `tela_destino`.
- Acionamento de chip de item do `lancador` **não existe** neste ciclo: nenhum binding,
  nenhum handler de tecla, nenhuma ação, nenhum registry.
- `_caixa_lancador` recebe a lista de itens, usa apenas `chip` e `texto`, ignora
  `tela_destino` completamente.
- `tela_destino` não deve aparecer em nenhuma saída visual.
- Se a implementação exigir decidir semântica real de acionamento (handler de tecla,
  navegação, binding declarativo), o executor deve parar com
  `ARCHITECTURE_REVIEW_REQUIRED` antes de escrever qualquer linha de código.

## Arquivos permitidos para implementação futura

O executor pode criar ou alterar **somente** os arquivos abaixo:

```
tela/renderizador.py          — ALTERAR
tela/teste_renderizador.py    — ALTERAR
tela/teste_demo.py            — ALTERAR
tela/teste_diagnostico.py     — ALTERAR
tela/demo.py                  — PODE ALTERAR (somente se estritamente necessário;
                                código lógico provavelmente inalterado — o lancador
                                aparece automaticamente por ser incluído em
                                renderizar_tela; se demo.py exigir alteração de
                                lógica, o executor deve descrever o motivo antes de
                                alterar)
docs/relatorios/IMP-0010-lancador-visual-inerte.md  — CRIAR
```

A lista acima é exaustiva. Se a implementação exigir criar ou alterar qualquer outro
arquivo, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED` ou `BLOCKED`
(conforme a natureza do impedimento) e descrever objetivamente o que falta.

## Arquivos proibidos

```
tela/loader.py               — proibido (H-0001)
tela/modelo.py               — proibido (H-0002)
tela/diagnostico.py          — proibido (H-0004; deve permanecer não interativo)
tela/teste_loader.py         — proibido (H-0001)
tela/teste_modelo.py         — proibido (H-0002)
tela/__init__.py             — proibido

docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/contratos/              (qualquer arquivo)
docs/adr/                    (qualquer arquivo)
docs/handoff/                (qualquer arquivo, incluindo este)
config/                      (qualquer arquivo)
```

---

## Especificação: `tela/renderizador.py`

### Constante `_ITENS_LANCADOR`

Adicionar ao módulo, antes de `renderizar_tela`, a constante de itens hardcoded
placeholder:

```python
_ITENS_LANCADOR = [
    {"chip": "C", "texto": "Console",   "tela_destino": "tela_console"},
    {"chip": "D", "texto": "Dashboard", "tela_destino": "tela_dashboard"},
    {"chip": "F", "texto": "Filtros",   "tela_destino": "tela_filtros"},
]
```

Regras sobre `_ITENS_LANCADOR`:

- Os itens são hardcoded placeholder — não são lidos de nenhum JSON nem de `config/`.
- `tela_destino` é dado declarativo inativo: presente no dict, nunca utilizado pelo
  renderer em nenhum caminho de código.
- Cada `texto` tem no máximo 15 caracteres: `"Console"` = 7, `"Dashboard"` = 9,
  `"Filtros"` = 7 — todos válidos segundo o contrato.
- Cada `chip` é um único caractere: `"C"`, `"D"`, `"F"`.

### Função `_caixa_lancador`

Adicionar ao módulo a função privada:

```python
def _caixa_lancador(titulo, itens, borda, inner_w, content_w, label_max):
    for item in itens:
        if len(item["texto"]) > 15:
            raise RenderizadorErro(
                "texto de item do lancador excede 15 caracteres: {0!r}".format(
                    item["texto"]
                )
            )
    linhas = ["[{0}] {1}".format(item["chip"], item["texto"]) for item in itens]
    return _caixa(titulo, linhas, borda, inner_w, content_w, label_max)
```

Regras sobre `_caixa_lancador`:

- `tela_destino` de cada item não é lido, validado, verificado nem passado adiante em
  nenhum caminho.
- A função não chama, resolve ou valida nenhum `tela_destino`.
- A função não acessa binding, handler, registry nem navegação.
- A função reutiliza a função privada `_caixa` existente.
- Formato de cada linha de item: `[{chip}] {texto}` — colchetes como caracteres
  literais, chip como caractere único declarado, espaço simples entre `]` e texto.
- Validação é feita **antes** de qualquer renderização: se qualquer item tiver
  `len(texto) > 15`, a exceção é levantada imediatamente, sem truncamento.

### Atualização de `renderizar_tela`

Incluir a caixa do lancador entre a caixa do dashboard e a caixa do menu:

```python
caixa_lancador = _caixa_lancador(
    "Navegar", _ITENS_LANCADOR, borda, inner_w, content_w, label_max
)

return (
    caixa_cabecalho + "\n"
    + caixa_dashboard + "\n"
    + caixa_lancador + "\n"
    + caixa_menu + "\n"
)
```

Regras:

- O título `"Navegar"` é hardcoded como placeholder — não é lido do `ModeloTela` nem
  do JSON. Corresponde ao `titulo` de `lancador_principal` em
  `config/telas/orquestrador.json` apenas por coincidência de referência; o renderer
  não lê esse campo.
- A posição (entre dashboard e menu) torna o lancador visualmente membro do corpo,
  separado da `barra_de_menus` representada pela caixa `"Menu"`.
- A invariante de largura de H-0009 é preservada: toda linha não-vazia tem exatamente
  `largura` chars (ou 42 no fallback).
- Sem linha em branco entre caixas (`"\n"` simples como separador).

### Saída esperada com `largura=None` (fallback 42) e `tipo_borda="curva"`

Derivação das dimensões da caixa `"Navegar"` para width=42:
- `label_max = 38`, `label = "Navegar"` (7 chars), dashes = 38 − 7 = 31
- `content_w = 39`
- `inner_w = 40`

```
╭ ORQUESTRADOR ──────────────────────────╮
│ Tela raiz do sistema — ponto de entrada│
╰────────────────────────────────────────╯
╭ DASHBOARD ─────────────────────────────╮
│ Dashboard de teste                     │
│ Sem dados carregados                   │
╰────────────────────────────────────────╯
╭ Navegar ───────────────────────────────╮
│ [C] Console                            │
│ [D] Dashboard                          │
│ [F] Filtros                            │
╰────────────────────────────────────────╯
╭ Menu ──────────────────────────────────╮
│ [Esc] Sair    [B] Borda                │
╰────────────────────────────────────────╯
```

Sem linha em branco entre caixas. Cada linha não-vazia tem exatamente 42 chars Python.
A string termina com `"\n"`.

### Saída esperada com `largura=None` (fallback 42) e `tipo_borda="reta"`

```
┌ ORQUESTRADOR ──────────────────────────┐
│ Tela raiz do sistema — ponto de entrada│
└────────────────────────────────────────┘
┌ DASHBOARD ─────────────────────────────┐
│ Dashboard de teste                     │
│ Sem dados carregados                   │
└────────────────────────────────────────┘
┌ Navegar ───────────────────────────────┐
│ [C] Console                            │
│ [D] Dashboard                          │
│ [F] Filtros                            │
└────────────────────────────────────────┘
┌ Menu ──────────────────────────────────┐
│ [Esc] Sair    [B] Borda                │
└────────────────────────────────────────┘
```

### Invariante de largura

A invariante de H-0009 permanece inalterada: quando `largura=W` for fornecido, toda
linha não-vazia da saída — incluindo as linhas do lancador — deve ter exatamente `W`
chars Python.

---

## Especificação: `tela/teste_renderizador.py`

### Constantes de saída esperada

Atualizar `_EXPECTED_ORQUESTRADOR` e `_EXPECTED_ORQUESTRADOR_RETA` para incluir o bloco
do lancador:

```python
_EXPECTED_ORQUESTRADOR = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Navegar ───────────────────────────────╮\n"
    "│ [C] Console                            │\n"
    "│ [D] Dashboard                          │\n"
    "│ [F] Filtros                            │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menu ──────────────────────────────────╮\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "╰────────────────────────────────────────╯\n"
)

_EXPECTED_ORQUESTRADOR_RETA = (
    "┌ ORQUESTRADOR ──────────────────────────┐\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "└────────────────────────────────────────┘\n"
    "┌ DASHBOARD ─────────────────────────────┐\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "└────────────────────────────────────────┘\n"
    "┌ Navegar ───────────────────────────────┐\n"
    "│ [C] Console                            │\n"
    "│ [D] Dashboard                          │\n"
    "│ [F] Filtros                            │\n"
    "└────────────────────────────────────────┘\n"
    "┌ Menu ──────────────────────────────────┐\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "└────────────────────────────────────────┘\n"
)
```

**Nota sobre comprimento das linhas**: cada linha não-vazia das constantes acima deve
ter exatamente 42 chars Python. O implementador deve verificar com
`all(len(ln)==42 for ln in _EXPECTED_ORQUESTRADOR.split("\n") if ln)` antes de
finalizar.

Referência de derivação da linha de título do lancador:
```python
# "╭ Navegar " + "─" * 31 + "╮" — total 42 chars
# label_max=38, len("Navegar")=7, dashes=38-7=31
```

Referência de derivação das linhas de conteúdo (content_w=39):
```python
# "[C] Console"  — 11 chars, pad=28 → "│ [C] Console" + " "*28 + "│" = 42
# "[D] Dashboard" — 13 chars, pad=26 → "│ [D] Dashboard" + " "*26 + "│" = 42
# "[F] Filtros"  — 11 chars, pad=28 → "│ [F] Filtros" + " "*28 + "│" = 42
```

### Seção nova — lançador visual inerte

Adicionar verificações para a caixa do lancador. As verificações são listadas abaixo
com critério:

| Verificação | Critério |
|---|---|
| saída curva bate com `_EXPECTED_ORQUESTRADOR` | `renderizar_tela(modelo) == _EXPECTED_ORQUESTRADOR` (igualdade estrita) |
| saída reta bate com `_EXPECTED_ORQUESTRADOR_RETA` | `renderizar_tela(modelo, tipo_borda="reta") == _EXPECTED_ORQUESTRADOR_RETA` (igualdade estrita) |
| saída curva contém `"╭ Navegar"` | `"╭ Navegar" in saida` |
| saída reta contém `"┌ Navegar"` | `"┌ Navegar" in saida_reta` |
| saída contém `"[C] Console"` | `"[C] Console" in saida` |
| saída contém `"[D] Dashboard"` | `"[D] Dashboard" in saida` |
| saída contém `"[F] Filtros"` | `"[F] Filtros" in saida` |
| lancador aparece antes de `"╭ Menu"` | `saida.index("╭ Navegar") < saida.index("╭ Menu")` |
| `"tela_console"` não aparece na saída | `"tela_console" not in saida` |
| `"tela_dashboard"` não aparece na saída | `"tela_dashboard" not in saida` |
| `"tela_filtros"` não aparece na saída | `"tela_filtros" not in saida` |
| saída não contém `"\n\n"` | `"\n\n" not in saida` |
| cada linha não-vazia tem 42 chars | `all(len(ln)==42 for ln in saida.split("\n") if ln)` |
| saída com `largura=60` contém `"╭ Navegar"` | `"╭ Navegar" in renderizar_tela(modelo, largura=60)` |
| cada linha não-vazia com `largura=60` tem 60 chars | `all(len(ln)==60 for ln in renderizar_tela(modelo, largura=60).split("\n") if ln)` |

### Verificações de validação de texto

Importar `_caixa_lancador` e `_BORDAS` diretamente do módulo para os testes de
validação:

```python
from tela.renderizador import _caixa_lancador, _BORDAS, RenderizadorErro
borda = _BORDAS["curva"]
```

| Verificação | Critério |
|---|---|
| texto de exatamente 15 chars é aceito | `_caixa_lancador("T", [{"chip":"X","texto":"a"*15,"tela_destino":"t"}], borda, 40, 39, 38)` não levanta exceção e retorna `str` |
| texto de 16 chars levanta `RenderizadorErro` | `_caixa_lancador("T", [{"chip":"X","texto":"a"*16,"tela_destino":"t"}], borda, 40, 39, 38)` levanta `RenderizadorErro` |
| texto de 0 chars é aceito | texto vazio `""` não levanta exceção |
| mensagem de erro menciona o texto rejeitado | excepção com `"a"*16` — `str(exc)` contém `"aaaaaaaaaaaaaaaa"` |
| `_caixa_lancador` existe no módulo | `callable(getattr(renderizador_module, "_caixa_lancador", None))` |

**Total mínimo de verificações em `teste_renderizador.py` após H-0010**: mínimo de 65
verificações existentes + verificações novas acima. O relatório IMP-0010 deve registrar
o total exato.

---

## Especificação: `tela/teste_demo.py`

### Constantes de saída esperada

Atualizar `_EXPECTED_CURVA` e `_EXPECTED_RETA` para incluir o bloco do lancador:

```python
_EXPECTED_CURVA = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Navegar ───────────────────────────────╮\n"
    "│ [C] Console                            │\n"
    "│ [D] Dashboard                          │\n"
    "│ [F] Filtros                            │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menu ──────────────────────────────────╮\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "╰────────────────────────────────────────╯\n"
)

_EXPECTED_RETA = (
    "┌ ORQUESTRADOR ──────────────────────────┐\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "└────────────────────────────────────────┘\n"
    "┌ DASHBOARD ─────────────────────────────┐\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "└────────────────────────────────────────┘\n"
    "┌ Navegar ───────────────────────────────┐\n"
    "│ [C] Console                            │\n"
    "│ [D] Dashboard                          │\n"
    "│ [F] Filtros                            │\n"
    "└────────────────────────────────────────┘\n"
    "┌ Menu ──────────────────────────────────┐\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "└────────────────────────────────────────┘\n"
)
```

### Verificações de subprocess

O `_EXPECTED_SUBPROCESS_CURVA` e `_EXPECTED_SUBPROCESS_RETA` são construídos
dinamicamente chamando `renderizar_tela(modelo, tipo_borda=..., largura=80)` — portanto
atualizam automaticamente com o novo renderer, sem alteração de lógica.

Adicionar verificações de presença do lancador no stdout do subprocess:

| Verificação | Critério |
|---|---|
| stdout de `b\ns\n` contém `"╭ Navegar"` | `"╭ Navegar" in proc.stdout` |
| stdout de `b\ns\n` contém `"┌ Navegar"` após `b` | `"┌ Navegar" in proc.stdout` |
| `"tela_console"` ausente no stdout | `"tela_console" not in proc.stdout` |
| `"tela_dashboard"` ausente no stdout (lancador) | `"tela_dashboard" not in proc.stdout` |
| `"tela_filtros"` ausente no stdout | `"tela_filtros" not in proc.stdout` |

**Nota**: `"tela_dashboard"` aqui refere-se ao valor de `tela_destino` do item do
lancador — não à string `"DASHBOARD"` do bloco de dashboard, que pode continuar
presente na saída.

Todas as 69 verificações existentes devem continuar passando. **Total mínimo em
`teste_demo.py` após H-0010**: mínimo de 69 existentes + verificações novas acima.

---

## Especificação: `tela/teste_diagnostico.py`

Atualizar a constante `_EXPECTED_ORQUESTRADOR` para incluir o bloco do lancador:

```python
_EXPECTED_ORQUESTRADOR = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Navegar ───────────────────────────────╮\n"
    "│ [C] Console                            │\n"
    "│ [D] Dashboard                          │\n"
    "│ [F] Filtros                            │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menu ──────────────────────────────────╮\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "╰────────────────────────────────────────╯\n"
)
```

Nenhuma outra alteração em `tela/teste_diagnostico.py` é necessária. O número de
verificações permanece 26 — apenas a constante de esperado muda.

---

## Critérios de aceite

- [ ] A demo renderiza um bloco visual de `lancador` com título `"Navegar"`.
- [ ] O bloco do `lancador` aparece entre o bloco do dashboard e o bloco do menu
      (elemento do corpo, não `barra_de_menus`).
- [ ] Os itens exibem `chip` e `texto` no formato `[chip] texto`.
- [ ] `"Console"` (7 chars, ≤ 15): aceito e exibido.
- [ ] `"Dashboard"` (9 chars, ≤ 15): aceito e exibido.
- [ ] `"Filtros"` (7 chars, ≤ 15): aceito e exibido.
- [ ] `_caixa_lancador` rejeita `texto` de 16 chars com `RenderizadorErro` — nunca
      trunca.
- [ ] `_caixa_lancador` aceita `texto` de exatamente 15 chars sem erro.
- [ ] A exceção de rejeição é levantada antes de qualquer renderização.
- [ ] Nenhum dos valores de `tela_destino` (`"tela_console"`, `"tela_dashboard"`,
      `"tela_filtros"`) aparece em nenhuma saída visual.
- [ ] Nenhum `tela_destino` é chamado, aberto, resolvido ou validado como tela real.
- [ ] Não há registry de telas ou ações.
- [ ] Não há navegação nova: sem setas, sem `[✥]`, sem cursor, sem handler de tecla.
- [ ] `b` continua alternando borda (curva ↔ reta).
- [ ] Esc continua saindo (`"\x1b"` define `saindo=True`).
- [ ] `s` continua como atalho auxiliar de pipe/teste.
- [ ] Saída por pipe permanece determinística (largura 80 via `shutil.get_terminal_size`
      em subprocess).
- [ ] Diagnóstico continua não interativo e determinístico (fallback 42).
- [ ] `"╭ Navegar"` presente na saída do `python tela/diagnostico.py`.
- [ ] Não há linhas em branco entre caixas/regiões visuais (`"\n\n"` ausente).
- [ ] Invariante de largura preservada: toda linha não-vazia tem exatamente `W` chars
      para `largura=W`.
- [ ] `python tela/teste_loader.py` retorna 0 (37 verificações — inalterado).
- [ ] `python tela/teste_modelo.py` retorna 0 (30 verificações — inalterado).
- [ ] `python tela/teste_renderizador.py` retorna 0 (mínimo 65 existentes + novas).
- [ ] `python tela/teste_diagnostico.py` retorna 0 (26 verificações — constante
      atualizada).
- [ ] `python tela/teste_demo.py` retorna 0 (mínimo 69 existentes + novas).
- [ ] Nenhum documento normativo foi alterado.
- [ ] Nenhum arquivo em `config/` foi alterado.
- [ ] `config/telas/orquestrador.json` inalterado após execução da demo.

## Testes mínimos esperados

Numeração orientativa para o relatório IMP-0010:

### Em `tela/teste_renderizador.py`

1. `renderizar_tela(modelo) == _EXPECTED_ORQUESTRADOR` (igualdade estrita — constante atualizada)
2. `renderizar_tela(modelo, tipo_borda="reta") == _EXPECTED_ORQUESTRADOR_RETA` (igualdade estrita)
3. `"╭ Navegar" in renderizar_tela(modelo)` — caixa lancador presente na saída curva
4. `"┌ Navegar" in renderizar_tela(modelo, tipo_borda="reta")` — presente na saída reta
5. `"[C] Console" in renderizar_tela(modelo)` — item 1 presente
6. `"[D] Dashboard" in renderizar_tela(modelo)` — item 2 presente
7. `"[F] Filtros" in renderizar_tela(modelo)` — item 3 presente
8. `saida.index("╭ Navegar") < saida.index("╭ Menu")` — lancador antes do menu
9. `"tela_console" not in renderizar_tela(modelo)` — tela_destino inativo
10. `"tela_dashboard" not in renderizar_tela(modelo)` — tela_destino inativo
11. `"tela_filtros" not in renderizar_tela(modelo)` — tela_destino inativo
12. `"\n\n" not in renderizar_tela(modelo)` — sem linhas em branco entre caixas
13. `all(len(ln)==42 for ln in renderizar_tela(modelo).split("\n") if ln)` — largura
14. `all(len(ln)==60 for ln in renderizar_tela(modelo, largura=60).split("\n") if ln)` — invariante
15. `"╭ Navegar" in renderizar_tela(modelo, largura=60)` — lancador com largura explícita
16. `_caixa_lancador("T", [{"chip":"X","texto":"a"*15,"tela_destino":"t"}], borda, 40, 39, 38)` — aceita 15 chars
17. `_caixa_lancador("T", [{"chip":"X","texto":"a"*16,"tela_destino":"t"}], borda, 40, 39, 38)` levanta `RenderizadorErro`
18. texto vazio `""` não levanta exceção em `_caixa_lancador`
19. mensagem da exceção de rejeição contém o texto rejeitado
20. `_caixa_lancador` existe e é callable no módulo

### Em `tela/teste_demo.py`

21. `_EXPECTED_CURVA` atualizada contém `"╭ Navegar ───────────────────────────────╮\n"`
22. `_EXPECTED_RETA` atualizada contém `"┌ Navegar ───────────────────────────────┐\n"`
23. Subprocess com `b\ns\n`: `"╭ Navegar" in proc.stdout`
24. Subprocess com `b\ns\n`: `"┌ Navegar" in proc.stdout`
25. `"tela_console" not in proc.stdout`
26. `"tela_filtros" not in proc.stdout`

### Em `tela/teste_diagnostico.py`

27. `gerar_diagnostico_tela()` == `_EXPECTED_ORQUESTRADOR` (constante atualizada com lancador)

## Condições de bloqueio

O executor deve parar imediatamente com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`
nas condições abaixo:

- `BLOCKED` — se a implementação exigir criar ou alterar qualquer arquivo fora de
  "Arquivos permitidos".
- `BLOCKED` — se qualquer critério de aceite não puder ser verificado com os arquivos
  permitidos.
- `BLOCKED` — se qualquer pré-condição falhar antes de iniciar (testes de H-0001 a
  H-0009 não passando com os totais esperados).
- `BLOCKED` — se a implementação exigir leitura de `config/lancador.json`,
  `config/estilo.json` ou qualquer arquivo em `config/`.
- `BLOCKED` — se a implementação exigir alterar `tela/diagnostico.py`.
- `BLOCKED` — se a implementação exigir alterar `tela/loader.py` ou `tela/modelo.py`.
- `BLOCKED` — se a implementação exigir dependência externa além da stdlib Python.
- `ARCHITECTURE_REVIEW_REQUIRED` — se for necessário definir navegação real, registry,
  ação, binding, cursor ou semântica de acionamento do lançador.
- `ARCHITECTURE_REVIEW_REQUIRED` — se a implementação exigir resolver, validar
  existência ou abrir qualquer `tela_destino`.
- `ARCHITECTURE_REVIEW_REQUIRED` — se a implementação exigir alterar
  `config/telas/orquestrador.json` para adicionar itens ao `lancador_principal` (os
  itens são hardcoded placeholder; o JSON não deve ser alterado).
- `ARCHITECTURE_REVIEW_REQUIRED` — se a lógica de `tela/demo.py` precisar de alteração
  além de constantes de teste (o lancador deve aparecer via `renderizar_tela` sem
  mudança de lógica na demo).

## Relatório de implementação esperado

O executor deve criar:

```
docs/relatorios/IMP-0010-lancador-visual-inerte.md
```

O relatório deve conter obrigatoriamente:

1. **Status**: `IMPLEMENTATION_COMPLETED`, `APROVADO`, `APROVADO_COM_RESSALVAS` ou
   `BLOQUEADO`.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo.
3. **Arquivos não alterados**: confirmação explícita de cada arquivo proibido.
4. **API implementada**: excertos de `_ITENS_LANCADOR`, `_caixa_lancador` e da
   atualização do retorno de `renderizar_tela`.
5. **Saída real de `python tela/diagnostico.py`**: reprodução literal do stdout — deve
   conter `"╭ Navegar"` e os três itens.
6. **Saída real de `printf 'b\ns\n' | python tela/demo.py`**: reprodução literal —
   deve conter o bloco lancador nos renders curvo e reto.
7. **Resultado dos testes**: saída completa dos scripts de teste com total de
   verificações por suíte.
8. **Invariantes H-0001 a H-0009 preservados**: confirmação com totais por suíte.
9. **Ausência de tela_destino na saída**: confirmação de que `"tela_console"`,
   `"tela_dashboard"` e `"tela_filtros"` não aparecem em nenhuma saída visual.
10. **Confirmação de validação de texto**: evidência de que texto de 16 chars levanta
    `RenderizadorErro` (excerto do teste ou execução).
11. **Ausência de `"\n\n"` entre caixas**: evidência literal.
12. **Invariante de largura**: evidência de que linhas não-vazias com `largura=W` têm
    `W` chars para pelo menos dois valores de `W`.
13. **Ausência de persistência**: confirmação de que `config/telas/orquestrador.json`
    não foi alterado (conteúdo antes == conteúdo depois da execução da demo).
14. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.
