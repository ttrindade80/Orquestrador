---
name: H-0008-aplicacao-demonstravel-borda-sair
description: Handoff de implementação da aplicação demonstrável mínima com alternância de borda e saída — cria tela/demo.py e tela/teste_demo.py, preservando diagnostico.py como não interativo, sem persistência, sem config, sem registry
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0008
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
    - docs/handoff/H-0007-alternancia-bordas-memoria.md
  issues_relacionadas: []
---

# H-0008 — Aplicação demonstrável mínima com borda/sair

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/handoff/H-0001-loader-validador-tela-json.md`
3. `docs/handoff/H-0002-modelo-interno-tela.md`
4. `docs/handoff/H-0003-renderizador-textual-estatico.md`
5. `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
6. `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
7. `docs/handoff/H-0006-tela-minima-borda-fixa.md`
8. `docs/handoff/H-0007-alternancia-bordas-memoria.md`
9. Este handoff

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
- Se entender que `[B] Borda` ou `[Esc] Sair` devem ser transformados em
  ações declarativas do JSON, parar imediatamente com
  `ARCHITECTURE_REVIEW_REQUIRED`. Os comandos `b` e `s` desta demo são
  internos de `tela/demo.py` — não são bindings declarativos, não são
  registry de ações, não são ações genéricas.

---

## Contexto herdado de H-0006/H-0007

O H-0007 foi implementado, aprovado (QA_APPROVED) e commitado (`b47f82d`).
O pacote `tela/` contém atualmente:

```
tela/__init__.py             — marcador de pacote (vazio)
tela/loader.py               — loader/validador macro (H-0001)
tela/teste_loader.py         — diagnóstico H-0001 (37 verificações, passando)
tela/modelo.py               — modelo interno normalizado (H-0002)
tela/teste_modelo.py         — diagnóstico H-0002 (30 verificações, passando)
tela/renderizador.py         — renderer visual com alternância de borda (H-0006/H-0007)
tela/teste_renderizador.py   — diagnóstico H-0006/H-0007 (58 verificações, passando)
tela/diagnostico.py          — ponto de entrada executável não interativo (H-0004)
tela/teste_diagnostico.py    — diagnóstico H-0004/H-0006 (26 verificações, passando)
```

### API entregue pelo H-0007

```python
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

Esta é a API que o H-0008 deve consumir. **Não alterar `tela/renderizador.py`.**

### Pipeline estabelecido (H-0006/H-0007)

```
config/telas/orquestrador.json
    → carregar_tela(None, "orquestrador")   [tela/loader.py       — H-0001]
    → dict (tela_raw)
    → construir_modelo(tela_raw)            [tela/modelo.py       — H-0002]
    → ModeloTela
    → renderizar_tela(modelo, tipo_borda)   [tela/renderizador.py — H-0006/H-0007]
    → str
```

### Saída com borda `"curva"` (default, H-0006/H-0007)

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

### Saída com borda `"reta"` (H-0007)

```
┌ ORQUESTRADOR ──────────────────────────┐
│ Tela raiz do sistema — ponto de entrada│
└────────────────────────────────────────┘

┌ DASHBOARD ─────────────────────────────┐
│ Dashboard de teste                     │
│ Sem dados carregados                   │
└────────────────────────────────────────┘

┌ Menu ──────────────────────────────────┐
│ [Esc] Sair    [B] Borda                │
└────────────────────────────────────────┘
```

### `tela/diagnostico.py` — invariante a preservar

`diagnostico.py` chama `renderizar_tela(modelo)` **sem `tipo_borda`** e é
não interativo. Ele deve permanecer exatamente assim após o H-0008. O H-0008
**não altera `diagnostico.py`**.

### Texto `[B] Borda` no menu — nota de contexto

O texto `[B] Borda` na caixa de menu é hardcoded inerte no renderer desde
o H-0006. Ele não está vinculado a nenhum binding ativo, registry de ações
ou evento de teclado real. O H-0008 cria comandos **internos** à demo que
**não são** a concretização desse texto como ação declarativa do JSON.

### Pendências que permanecem inertes

Todas as pendências declaradas no `config/telas/orquestrador.json`
(DOC-B008, DOC-B009, `bindings`, `lancador_principal.itens`, etc.)
continuam inertes e fora de escopo do H-0008.

---

## Objetivo técnico

Criar `tela/demo.py` — uma aplicação demonstrável local mínima que:

1. Carrega a tela raiz pelo pipeline já estabelecido (H-0001 + H-0002).
2. Renderiza inicialmente com `tipo_borda="curva"`.
3. Aceita o comando `b` para alternar o tipo de borda entre `"curva"` e `"reta"`.
4. Aceita o comando `s` para sair.
5. Mantém o estado de borda apenas em variável local em memória.
6. Não grava arquivo, não altera JSON, não persiste nenhuma preferência.
7. Não usa `curses`, `textual`, `rich` nem qualquer biblioteca de UI.
8. Lê comandos de `sys.stdin` linha a linha (suporta uso via pipe).
9. Não imprime prompt interativo (sem `input()`, sem mensagens como `"> "`).

Criar `tela/teste_demo.py` com cobertura automatizada do comportamento acima.

`tela/diagnostico.py` permanece não interativo e determinístico — não é
transformado em loop interativo.

---

## API interna congelada de `tela/demo.py`

O implementador deve definir exatamente as seguintes funções em
`tela/demo.py`. Os nomes são congelados — o implementador não pode usar
outros nomes.

### `criar_estado_inicial() -> dict`

Retorna o estado inicial da demonstração:

```python
{"tipo_borda": "curva", "saindo": False}
```

Regras:
- Retorna sempre um novo dict independente a cada chamada.
- Nunca usa estado global mutável.
- Não lê arquivo, não lê JSON, não acessa `sys.stdin`.

### `processar_comando(estado: dict, comando: str) -> dict`

Recebe o estado atual e um comando string. Retorna um novo dict de estado.

| Comando | Efeito |
|---|---|
| `"b"` | Alterna `tipo_borda`: `"curva"` → `"reta"` ou `"reta"` → `"curva"` |
| `"s"` | Define `saindo=True`; `tipo_borda` permanece inalterado |
| qualquer outro (incluindo string vazia) | Retorna cópia de `estado` sem alteração |

Regras obrigatórias:
- Não modifica o dict `estado` recebido como argumento.
- Retorna sempre um novo dict com as chaves `"tipo_borda"` e `"saindo"`.
- Não grava arquivo, não altera JSON, não lê disco.
- A validação de `comando` é case-sensitive: `"B"`, `"S"` não têm efeito.
- Não chama `renderizar_tela` nem acessa modelo.

### `renderizar_estado(estado: dict, modelo: ModeloTela) -> str`

Delega para a API do H-0007:

```python
return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"])
```

Regras:
- Não modifica `estado`, não modifica `modelo`.
- Nenhum efeito colateral além da chamada a `renderizar_tela`.

### `main() -> int`

Entrada principal da aplicação demonstrável. Deve:

1. Executar o bootstrap de `sys.path` (ver seção "Regras de implementação").
2. Chamar `carregar_tela(None, "orquestrador")` e `construir_modelo(tela_raw)`.
3. Chamar `criar_estado_inicial()` para obter o estado inicial.
4. Chamar `renderizar_estado(estado, modelo)` e imprimir o resultado com
   `print(saida, end="")`.
5. Iterar sobre `sys.stdin` linha a linha:
   - Para cada linha: `comando = linha.strip()`.
   - Chamar `novo_estado = processar_comando(estado, comando)`.
   - Atualizar `estado = novo_estado`.
   - Se `estado["saindo"]` é `True`: sair do loop imediatamente (sem
     re-renderizar).
   - Caso contrário: se `comando` foi `"b"`, imprimir nova renderização com
     `print(renderizar_estado(estado, modelo), end="")`. Para qualquer outro
     comando (incluindo vazio e desconhecido): **não** re-renderizar.
6. Retornar `0` (saída limpa).
7. Em `if __name__ == "__main__"`: chamar `sys.exit(main())`.

Regras:
- EOF em `sys.stdin` (fim do stream sem comando `s`) encerra o loop
  normalmente com retorno `0`.
- Não imprime prompt (`"> "`, `"comando: "`, etc.).
- Não imprime mensagem de erro para comandos desconhecidos.
- Não imprime mensagem de despedida ao sair.

---

## Comportamento observável com `printf 'b\ns\n' | python tela/demo.py`

O comando exato de demonstração é:

```bash
printf 'b\ns\n' | python tela/demo.py
```

Saída esperada no stdout (exatamente dois renders, sem separador):

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
┌ ORQUESTRADOR ──────────────────────────┐
│ Tela raiz do sistema — ponto de entrada│
└────────────────────────────────────────┘

┌ DASHBOARD ─────────────────────────────┐
│ Dashboard de teste                     │
│ Sem dados carregados                   │
└────────────────────────────────────────┘

┌ Menu ──────────────────────────────────┐
│ [Esc] Sair    [B] Borda                │
└────────────────────────────────────────┘
```

Código de saída: `0`.

Explicação:
- `b` → estado muda para `"reta"`, reta é impressa.
- `s` → `saindo=True`, loop encerra sem nova renderização.

---

## Escopo positivo

O H-0008 autoriza e especifica:

1. Criar `tela/demo.py` conforme definido neste handoff.
2. Criar `tela/teste_demo.py` conforme definido neste handoff.
3. Criar `docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md`.
4. Alterar `tela/teste_diagnostico.py` **somente se** alguma verificação
   existente quebrar — preferência: nenhuma alteração.

---

## Fora de escopo — proibições explícitas

O H-0008 **não implementa** nenhum dos itens abaixo:

- lançador (H-0009 — ainda não autorizado);
- abertura de tela de teste;
- navegação entre telas ou por `tela_destino`;
- registry genérico de ações;
- bindings ativos declarativos do JSON;
- execução real de chips declarativos (`chip_esc`, `chip_borda`, etc.);
- transformação de `[B] Borda` em ação declarativa do JSON;
- transformação de `[Esc] Sair` em ação declarativa do JSON;
- dashboard real com dados;
- contrato novo de dashboard;
- pop-up;
- tela de processamento;
- filtros funcionais;
- paginação funcional;
- seleção funcional;
- resize ou largura dinâmica;
- layout responsivo;
- cálculo de largura real de terminal;
- leitura de `config/estilo.json`;
- leitura de `config/layout_console.json`;
- leitura de `config/lancador.json`;
- alteração de `config/telas/orquestrador.json`;
- alteração de qualquer arquivo em `config/`;
- alteração de contratos, ADRs, NOMENCLATURA ou documentos normativos;
- uso de `curses`, `textual`, `rich` ou qualquer biblioteca de UI;
- persistência de `tipo_borda` em arquivo ou variável global;
- impressão de prompt interativo (`input()`);
- transformação de `diagnostico.py` em loop interativo.

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os arquivos abaixo:

```
tela/demo.py                                                — CRIAR
tela/teste_demo.py                                          — CRIAR
tela/teste_diagnostico.py                                   — ALTERAR só se necessário
docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md  — CRIAR
```

A lista acima é exaustiva e sem exceção. Se a implementação exigir alterar
qualquer outro arquivo, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

---

## Arquivos proibidos de alterar

```
tela/loader.py               — proibido (H-0001)
tela/modelo.py               — proibido (H-0002)
tela/renderizador.py         — proibido (H-0006/H-0007; API já entregue)
tela/teste_loader.py         — proibido (H-0001)
tela/teste_modelo.py         — proibido (H-0002)
tela/teste_renderizador.py   — proibido (H-0006/H-0007)
tela/diagnostico.py          — proibido (H-0004; deve permanecer não interativo)
tela/__init__.py             — proibido

docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/contratos/              (qualquer arquivo)
docs/adr/                    (qualquer arquivo)
docs/handoff/                (qualquer arquivo, incluindo este)
docs/templates/              (qualquer arquivo)
config/                      (qualquer arquivo)
```

---

## Regras de implementação

### Bootstrap de `sys.path` em `tela/demo.py`

O mesmo padrão de `diagnostico.py` e dos outros módulos do pacote:

```python
import sys
sys.dont_write_bytecode = True

if __name__ == "__main__":
    _raiz_scripts = "/".join(__file__.replace("\\", "/").split("/")[:-2])
    if _raiz_scripts and _raiz_scripts not in sys.path:
        sys.path.insert(0, _raiz_scripts)
```

### Importações obrigatórias em `tela/demo.py`

```python
from tela.loader import carregar_tela
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import renderizar_tela
```

### Importações proibidas em `tela/demo.py`

- `import json`
- `import os`
- `import curses`, `import textual`, `import rich`
- `import subprocess`, `exec`, `eval`
- `import pathlib` / `from pathlib import ...`
- Qualquer biblioteca de terceiros não pertencente à stdlib Python.

### Estrutura obrigatória de `tela/demo.py`

O arquivo deve conter, nesta ordem:

1. Docstring descritiva do módulo.
2. `import sys` e `sys.dont_write_bytecode = True`.
3. Bloco `if __name__ == "__main__"` com bootstrap de `sys.path`.
4. Importações de `tela.*`.
5. Definição de `criar_estado_inicial()`.
6. Definição de `processar_comando(estado, comando)`.
7. Definição de `renderizar_estado(estado, modelo)`.
8. Definição de `main()`.
9. Bloco `if __name__ == "__main__": sys.exit(main())`.

### Estado interno — estrutura exata do dict

O dict de estado tem exatamente duas chaves:

| Chave | Tipo | Valor inicial |
|---|---|---|
| `"tipo_borda"` | `str` | `"curva"` |
| `"saindo"` | `bool` | `False` |

Nenhuma outra chave deve ser adicionada ao dict de estado.

### `processar_comando` — imutabilidade obrigatória

O implementador deve criar um novo dict dentro de `processar_comando` em vez
de modificar o argumento `estado`. Exemplo de estrutura aceitável:

```python
def processar_comando(estado, comando):
    novo = {"tipo_borda": estado["tipo_borda"], "saindo": estado["saindo"]}
    if comando == "b":
        novo["tipo_borda"] = "reta" if estado["tipo_borda"] == "curva" else "curva"
    elif comando == "s":
        novo["saindo"] = True
    return novo
```

O implementador pode usar outra organização interna equivalente, desde que:
- `estado` não seja modificado in-place.
- O dict retornado tenha exatamente as chaves `"tipo_borda"` e `"saindo"`.

### Loop de `main()` — estrutura obrigatória

```python
def main():
    # bootstrap já executado antes das importações; não repetir aqui
    tela_raw = carregar_tela(None, "orquestrador")
    modelo = construir_modelo(tela_raw)
    estado = criar_estado_inicial()
    print(renderizar_estado(estado, modelo), end="")
    for linha in sys.stdin:
        comando = linha.strip()
        novo_estado = processar_comando(estado, comando)
        estado = novo_estado
        if estado["saindo"]:
            break
        if comando == "b":
            print(renderizar_estado(estado, modelo), end="")
    return 0
```

O implementador pode usar outra organização equivalente, desde que:
- O comportamento observável seja idêntico ao definido neste handoff.
- Não imprima re-render para comandos que não sejam `"b"`.
- Não imprima nada extra ao sair via `"s"` ou EOF.

---

## Estrutura obrigatória de `tela/teste_demo.py`

### Cabeçalho

```python
import sys
sys.dont_write_bytecode = True
from pathlib import Path
_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))
import subprocess
from tela.loader import carregar_tela
from tela.modelo import construir_modelo, ModeloTela
from tela.renderizador import renderizar_tela
from tela.demo import criar_estado_inicial, processar_comando, renderizar_estado
```

### Estrutura geral do script de teste

- `sys.dont_write_bytecode = True` antes de qualquer import.
- Imprimir `[PASSOU] <nome>` ou `[FALHOU] <nome>` para cada verificação.
- Imprimir ao final: `Total de verificacoes`, `Passaram`, `Falharam`.
- Retornar código de saída 0 se todos passaram, 1 se algum falhou.
- Não usar `unittest`, `pytest` nem nenhum framework externo.

### Seção 1 — Estado inicial

| Verificação | Critério |
|---|---|
| `criar_estado_inicial()` retorna dict | `isinstance(criar_estado_inicial(), dict)` |
| estado inicial tem `tipo_borda == "curva"` | `criar_estado_inicial()["tipo_borda"] == "curva"` |
| estado inicial tem `saindo == False` | `criar_estado_inicial()["saindo"] == False` |
| duas chamadas retornam dicts independentes | `criar_estado_inicial() is not criar_estado_inicial()` |

### Seção 2 — `processar_comando`

| Verificação | Critério |
|---|---|
| `"b"` sobre estado curva → `tipo_borda == "reta"` | `processar_comando({"tipo_borda":"curva","saindo":False},"b")["tipo_borda"] == "reta"` |
| `"b"` sobre estado reta → `tipo_borda == "curva"` | `processar_comando({"tipo_borda":"reta","saindo":False},"b")["tipo_borda"] == "curva"` |
| `"b"` não altera `saindo` | `processar_comando({"tipo_borda":"curva","saindo":False},"b")["saindo"] == False` |
| `"s"` define `saindo == True` | `processar_comando({"tipo_borda":"curva","saindo":False},"s")["saindo"] == True` |
| `"s"` não altera `tipo_borda` | `processar_comando({"tipo_borda":"curva","saindo":False},"s")["tipo_borda"] == "curva"` |
| `"s"` sobre estado reta preserva `tipo_borda == "reta"` | `processar_comando({"tipo_borda":"reta","saindo":False},"s")["tipo_borda"] == "reta"` |
| comando desconhecido `"x"` não altera `tipo_borda` | retorno `tipo_borda` == original |
| comando desconhecido `"x"` não altera `saindo` | retorno `saindo` == `False` |
| string vazia não altera estado | retorno idêntico ao original em conteúdo |
| `"B"` (maiúsculo) não tem efeito | `processar_comando({"tipo_borda":"curva","saindo":False},"B")["tipo_borda"] == "curva"` |
| `"S"` (maiúsculo) não altera `saindo` | `processar_comando({"tipo_borda":"curva","saindo":False},"S")["saindo"] == False` |
| `processar_comando` não modifica o dict original — `"b"` | `estado_original["tipo_borda"]` permanece `"curva"` após chamada com `"b"` |
| `processar_comando` não modifica o dict original — `"s"` | `estado_original["saindo"]` permanece `False` após chamada com `"s"` |
| alternância completa: curva → reta → curva | dois `"b"` consecutivos retornam ao `tipo_borda` inicial |

### Seção 3 — `renderizar_estado`

Pré-condição: carregar modelo real via `carregar_tela`/`construir_modelo`.

| Verificação | Critério |
|---|---|
| `renderizar_estado` com `tipo_borda="curva"` retorna str | `isinstance(resultado, str)` |
| saída curva começa com `╭ ORQUESTRADOR` | `resultado.startswith("╭ ORQUESTRADOR")` |
| saída curva bate com expected H-0006/H-0007 | igualdade estrita com `_EXPECTED_CURVA` |
| `renderizar_estado` com `tipo_borda="reta"` retorna str | `isinstance(resultado, str)` |
| saída reta começa com `┌ ORQUESTRADOR` | `resultado.startswith("┌ ORQUESTRADOR")` |
| saída reta bate com expected H-0007 | igualdade estrita com `_EXPECTED_RETA` |
| `renderizar_estado` não altera `estado` | dict de entrada inalterado após chamada |
| `renderizar_estado` não altera `modelo` | `modelo.cabecalho` inalterado após chamada |

Constantes obrigatórias em `tela/teste_demo.py`:

```python
_EXPECTED_CURVA = (
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

_EXPECTED_RETA = (
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

### Seção 4 — Integração via subprocess (demo completo)

Usar `subprocess.run` com `input="b\ns\n"`.

| Verificação | Critério |
|---|---|
| `python tela/demo.py` encerra com código 0 | `proc.returncode == 0` |
| stdout contém render curva inicial (`╭ ORQUESTRADOR`) | `"╭ ORQUESTRADOR" in proc.stdout` |
| stdout contém render reta após `b` (`┌ ORQUESTRADOR`) | `"┌ ORQUESTRADOR" in proc.stdout` |
| stdout bate com `_EXPECTED_CURVA + _EXPECTED_RETA` | `proc.stdout == _EXPECTED_CURVA + _EXPECTED_RETA` |
| stderr está vazio | `proc.stderr == ""` |
| `config/telas/orquestrador.json` inalterado após demo | conteúdo do arquivo idêntico ao lido antes do subprocess |

Para a verificação do JSON, ler o conteúdo do arquivo **antes** de executar
o subprocess e comparar com o conteúdo **após**:

```python
caminho_json = _BASE_PADRAO / "config" / "telas" / "orquestrador.json"
json_antes = caminho_json.read_text(encoding="utf-8")
# ... subprocess ...
json_depois = caminho_json.read_text(encoding="utf-8")
# verificar: json_antes == json_depois
```

### Seção 5 — Preservação do diagnóstico

| Verificação | Critério |
|---|---|
| `gerar_diagnostico_tela()` não lança exceção | nenhuma exceção levantada |
| retorno de `gerar_diagnostico_tela()` é str | `isinstance(resultado, str)` |
| retorno bate com `_EXPECTED_CURVA` (default curva H-0006/H-0007) | igualdade estrita |
| `python tela/diagnostico.py` encerra com código 0 | `proc.returncode == 0` (subprocess) |
| stdout de `diagnostico.py` bate com `_EXPECTED_CURVA` | igualdade estrita |
| `diagnostico.py` não contém `sys.stdin` | `"sys.stdin" not in texto_mod` |
| `diagnostico.py` não contém `input(` | `"input(" not in texto_mod` |

Importação obrigatória em `tela/teste_demo.py` para a seção 5:

```python
from tela.diagnostico import gerar_diagnostico_tela
```

---

## Critérios de aceite verificáveis

### Escopo e arquivos

- [ ] Somente os arquivos listados em "Arquivos permitidos" foram criados
      ou alterados.
- [ ] Nenhum arquivo fora do escopo autorizado foi criado ou alterado.
- [ ] Nenhum contrato, ADR, nomenclatura, índice, handoff anterior,
      relatório anterior, `config/*.json`, `docs/INDICE.md`,
      `docs/backlog.md` ou `docs/issues.md` foi alterado.

### API interna de `tela/demo.py`

- [ ] `criar_estado_inicial()` retorna `{"tipo_borda": "curva", "saindo": False}`.
- [ ] Duas chamadas a `criar_estado_inicial()` retornam dicts independentes.
- [ ] `processar_comando(estado, "b")` alterna `tipo_borda` sem modificar `estado`.
- [ ] `processar_comando(estado, "b")` com `tipo_borda="curva"` → `"reta"`.
- [ ] `processar_comando(estado, "b")` com `tipo_borda="reta"` → `"curva"`.
- [ ] `processar_comando(estado, "s")` define `saindo=True` sem alterar `tipo_borda`.
- [ ] `processar_comando(estado, "x")` retorna cópia inalterada.
- [ ] `processar_comando(estado, "B")` não altera `tipo_borda` (case-sensitive).
- [ ] `processar_comando(estado, "S")` não altera `saindo` (case-sensitive).
- [ ] `renderizar_estado(estado_curva, modelo)` == `renderizar_tela(modelo, "curva")`.
- [ ] `renderizar_estado(estado_reta, modelo)` == `renderizar_tela(modelo, "reta")`.

### Comportamento da demo (subprocess)

- [ ] `printf 'b\ns\n' | python tela/demo.py` encerra com código 0.
- [ ] stdout contém render curva (`╭ ORQUESTRADOR`) antes de `b`.
- [ ] stdout contém render reta (`┌ ORQUESTRADOR`) após `b`.
- [ ] stdout bate exatamente com `_EXPECTED_CURVA + _EXPECTED_RETA`.
- [ ] stderr está vazio em execução normal.
- [ ] EOF sem `s` encerra com código 0 (teste via `printf '' | python tela/demo.py`).

### Ausência de persistência

- [ ] `config/telas/orquestrador.json` inalterado após execução da demo.
- [ ] Nenhum arquivo novo criado em `config/` ou `tela/` durante execução.
- [ ] Segunda execução da demo inicia com `tipo_borda="curva"` (estado reiniciado).
- [ ] `processar_comando` não usa variável global mutável.

### Ausência de registry, bindings, navegação

- [ ] `tela/demo.py` não importa `json`, `os`, `pathlib`.
- [ ] `tela/demo.py` não usa `curses`, `textual`, `rich`.
- [ ] `tela/demo.py` não abre arquivos em disco além do que `carregar_tela` faz.
- [ ] `tela/demo.py` não acessa `config/estilo.json`, `config/layout_console.json`,
      `config/lancador.json`.
- [ ] Comandos `b` e `s` são internos à demo — não são ações declarativas do JSON.
- [ ] `config/telas/orquestrador.json` não foi alterado.

### Preservação do diagnóstico

- [ ] `tela/diagnostico.py` não foi alterado.
- [ ] `gerar_diagnostico_tela()` sem argumentos retorna saída idêntica ao H-0006 (curva).
- [ ] `python tela/diagnostico.py` imprime saída curva e encerra com código 0.
- [ ] `diagnostico.py` não contém `sys.stdin` nem `input(`.
- [ ] `tela/teste_diagnostico.py` continua passando 26 verificações sem alteração
      (ou com alteração mínima justificada se inevitável).

### Invariantes preservados

- [ ] `python tela/teste_loader.py` retorna código 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna código 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna código 0 (58 verificações).
- [ ] `python tela/teste_diagnostico.py` retorna código 0 (26 verificações).
- [ ] `python tela/diagnostico.py` imprime saída H-0006/H-0007 (curva) e encerra 0.
- [ ] `python tela/teste_demo.py` retorna código 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` é JSON válido e não foi alterado.

---

## Pré-condição obrigatória

Antes de criar qualquer arquivo, confirmar que todos os invariantes
anteriores estão passando:

```bash
python tela/teste_loader.py     # 37 verificações passando
python tela/teste_modelo.py     # 30 verificações passando
python tela/teste_renderizador.py   # 58 verificações passando
python tela/teste_diagnostico.py    # 26 verificações passando
python tela/diagnostico.py          # saída curva H-0006, código 0
```

Se qualquer verificação falhar, parar imediatamente com `BLOCKED` e
registrar qual verificação falhou e em qual módulo.

---

## Comandos de verificação obrigatórios

Executar a partir do diretório raiz do repositório de scripts. O relatório
IMP-0008 deve incluir a saída real de cada comando.

```bash
# 1. Integridade do JSON de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"

# 2. Invariantes H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes H-0002 preservados
python tela/teste_modelo.py

# 4. Invariantes H-0006/H-0007 preservados
python tela/teste_renderizador.py

# 5. Invariantes H-0004/H-0006 preservados
python tela/teste_diagnostico.py

# 6. Testes da demo (H-0008)
python tela/teste_demo.py

# 7. Diagnóstico executável (saída curva H-0006/H-0007, não interativo)
python tela/diagnostico.py

# 8. Demo demonstrável (dois renders: curva e reta)
printf 'b\ns\n' | python tela/demo.py

# 9. Demo com EOF sem 's' (deve encerrar com código 0)
printf '' | python tela/demo.py; echo "exit_code=$?"

# 10. Verificação de bytecode
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print

# 11. Estado do repositório
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

1. Qualquer pré-condição de H-0001 a H-0007 falhar antes de iniciar.
2. A implementação exigir alterar qualquer arquivo fora de "Arquivos permitidos".
3. A implementação exigir alterar `tela/renderizador.py` (a API do H-0007 é
   suficiente — se não for, registrar como lacuna, não modificar).
4. A implementação exigir alterar `tela/diagnostico.py`.
5. A implementação exigir transformar os comandos `b` ou `s` em ações
   declarativas do JSON ou em bindings ativos: **ARCHITECTURE_REVIEW_REQUIRED**.
6. A implementação exigir registry genérico de ações.
7. A implementação exigir leitura de `config/estilo.json`,
   `config/layout_console.json`, `config/lancador.json` ou qualquer outro
   arquivo em `config/`.
8. A implementação exigir `curses`, `textual`, `rich` ou biblioteca de UI.
9. A implementação exigir persistência de `tipo_borda` em arquivo ou
   variável global.
10. A implementação exigir navegação entre telas ou `tela_destino`.
11. A implementação exigir cálculo de largura real de terminal.
12. A implementação exigir dependência externa além da stdlib Python.
13. `python tela/teste_diagnostico.py` falhar após as alterações e não
    houver alteração mínima disponível dentro do escopo autorizado.
14. A saída de `printf 'b\ns\n' | python tela/demo.py` divergir do
    comportamento definido neste handoff.
15. Qualquer linha visual tiver comprimento Python diferente de 42 chars.

---

## Formato esperado do relatório `IMP-0008`

O executor deve criar:

```
docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md
```

O relatório deve conter obrigatoriamente:

1. **Status**: `IMPLEMENTATION_COMPLETED`, `APROVADO`, `APROVADO_COM_RESSALVAS`
   ou `BLOQUEADO`.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo.
3. **Arquivos não alterados**: confirmação explícita dos arquivos proibidos.
4. **API interna implementada**: excertos de `criar_estado_inicial`,
   `processar_comando`, `renderizar_estado` e `main`.
5. **Saída real de `printf 'b\ns\n' | python tela/demo.py`**: reprodução
   literal do stdout.
6. **Resultado dos testes da demo**: saída completa de
   `python tela/teste_demo.py` com total de verificações.
7. **Invariantes H-0001 a H-0007 preservados**: saída dos cinco scripts
   de teste anteriores (resumo com total de verificações).
8. **Resultado do diagnóstico**: saída de `python tela/diagnostico.py`.
9. **Ausência de persistência**: confirmação de que `config/telas/orquestrador.json`
   não foi alterado.
10. **Comportamento fora de escopo preservado como inerte**: lista dos itens
    não implementados.
11. **Saída real de todos os comandos de verificação**: cópia integral.
12. **Nota sobre largura fixa**: confirmação de que `TOTAL_WIDTH=42`,
    `INNER_WIDTH=40`, `CONTENT_WIDTH=39` foram preservadas provisoriamente
    sem declaração normativa.
13. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Checklist final para QA

- [ ] H-0008 lido integralmente antes de qualquer criação de arquivo.
- [ ] Pré-condições verificadas (todos os testes anteriores passando).
- [ ] Somente os arquivos autorizados foram criados ou alterados.
- [ ] `git diff --stat` não mostra alterações em arquivos fora do escopo.
- [ ] Nenhum contrato, ADR ou documento normativo alterado.
- [ ] `tela/demo.py` criado com as quatro funções nomeadas exatamente:
      `criar_estado_inicial`, `processar_comando`, `renderizar_estado`, `main`.
- [ ] `criar_estado_inicial()` retorna `{"tipo_borda": "curva", "saindo": False}`.
- [ ] `processar_comando(estado, "b")` alterna borda sem modificar `estado`.
- [ ] `processar_comando(estado, "s")` define `saindo=True`.
- [ ] `processar_comando(estado, "X")` não altera estado (case-sensitive).
- [ ] `printf 'b\ns\n' | python tela/demo.py` encerra com código 0.
- [ ] stdout bate exatamente com `_EXPECTED_CURVA + _EXPECTED_RETA`.
- [ ] EOF sem `s` encerra com código 0.
- [ ] `config/telas/orquestrador.json` inalterado após execução da demo.
- [ ] `tela/diagnostico.py` não alterado.
- [ ] `gerar_diagnostico_tela()` continua retornando saída curva H-0006/H-0007.
- [ ] `diagnostico.py` não contém `sys.stdin` nem `input(`.
- [ ] `tela/demo.py` não importa `json`, `os`, `pathlib`, `curses`,
      `textual`, `rich`.
- [ ] Comandos `b` e `s` são internos à demo — não são ações declarativas.
- [ ] `python tela/teste_loader.py` retorna 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna 0 (58 verificações).
- [ ] `python tela/teste_diagnostico.py` retorna 0 (26 verificações).
- [ ] `python tela/diagnostico.py` imprime saída curva H-0006 e encerra 0.
- [ ] `python tela/teste_demo.py` retorna 0 (todas as verificações passando).
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` válido e inalterado.
- [ ] `docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md` criado
      com resultado final documentado.
- [ ] Commit não realizado (responsabilidade do engenheiro).
