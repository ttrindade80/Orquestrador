---
name: H-0009-layout-terminal-entrada-sem-echo
description: Handoff de implementação — largura dinâmica pelo terminal, remoção de linha em branco entre regiões visuais, entrada por tecla direta sem echo, Esc real saindo da demo
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0009
  data_criacao: 2026-07-07
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/contratos/contrato_composicao_corpo.md
  handoffs_anteriores:
    - docs/handoff/H-0001-loader-validador-tela-json.md
    - docs/handoff/H-0002-modelo-interno-tela.md
    - docs/handoff/H-0003-renderizador-textual-estatico.md
    - docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
    - docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
    - docs/handoff/H-0006-tela-minima-borda-fixa.md
    - docs/handoff/H-0007-alternancia-bordas-memoria.md
    - docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
  issues_relacionadas: []
---

# H-0009 — Layout por dimensão do terminal e entrada sem echo

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/contratos/contrato_composicao_corpo.md`
3. `docs/handoff/H-0006-tela-minima-borda-fixa.md`
4. `docs/handoff/H-0007-alternancia-bordas-memoria.md`
5. `docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md`
6. Este handoff

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
- Não usar `curses`, `textual`, `rich` nem qualquer biblioteca de UI externa.
- Se a implementação exigir ativar chips reais, executar bindings declarativos
  do JSON, navegar entre telas ou criar registry de ações: parar com
  `ARCHITECTURE_REVIEW_REQUIRED`.
- Se faltar regra, arquivo permitido ou critério verificável: parar com
  `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED` descrevendo o que falta.

---

## Contexto herdado de H-0008

O H-0008 foi implementado, aprovado (QA_APPROVED) e commitado (`2c6efe6`).

O pacote `tela/` contém atualmente:

```
tela/__init__.py             — marcador de pacote (vazio)
tela/loader.py               — loader/validador macro (H-0001)
tela/teste_loader.py         — 37 verificações, passando
tela/modelo.py               — modelo interno normalizado (H-0002)
tela/teste_modelo.py         — 30 verificações, passando
tela/renderizador.py         — renderer visual com alternância de borda (H-0006/H-0007)
tela/teste_renderizador.py   — 58 verificações, passando
tela/diagnostico.py          — ponto de entrada não interativo (H-0004)
tela/teste_diagnostico.py    — 26 verificações, passando
tela/demo.py                 — aplicação demonstrável mínima (H-0008)
tela/teste_demo.py           — 49 verificações, passando
```

### API entregue pelo H-0007 (renderer atual)

```python
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

### API entregue pelo H-0008 (demo atual)

```python
criar_estado_inicial() -> dict                          # {"tipo_borda": "curva", "saindo": False}
processar_comando(estado: dict, comando: str) -> dict   # "b", "s" → novo estado
renderizar_estado(estado: dict, modelo: ModeloTela) -> str
main() -> int                                           # lê sys.stdin linha a linha
```

### Saída atual do renderer (largura fixa 42 chars, borda curva)

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

Note a linha em branco entre cada caixa (vinda de `"\n\n"` em `renderizar_tela`).

### Problemas a corrigir no H-0009

1. Largura fixa de 42 chars herdada dos ciclos visuais iniciais (dívida técnica
   provisória).
2. Linha em branco entre caixas/regiões visuais (separadores `"\n\n"` em
   `renderizar_tela`).
3. Entrada via `sys.stdin` linha a linha exige Enter e produz echo do caractere.
4. Menu exibe `[Esc] Sair` mas Esc real não sai; a saída é feita com `s` + Enter.

---

## Objetivo técnico do H-0009

Corrigir os quatro problemas acima de forma mínima e reversível, sem avançar
para dashboard real, lançador ou navegação.

Entregas obrigatórias:

1. `tela/renderizador.py` — aceita `largura` explícita opcional; sem `"\n\n"`
   entre caixas.
2. `tela/demo.py` — entrada por tecla direta (sem Enter, sem echo); Esc
   real saindo; largura lida do terminal.
3. `tela/teste_renderizador.py` — atualizado para nova API e novos esperados.
4. `tela/teste_demo.py` — atualizado para novos esperados e novos casos de
   teste (`"\x1b"`).
5. `tela/teste_diagnostico.py` — atualizado para novo esperado (sem `"\n\n"`).
6. `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md` — criado.

---

## Nota sobre R-10 do `contrato_composicao_corpo.md`

A seção 4.6 / R-10 do contrato diz: "O renderer sempre insere uma linha em
branco entre a borda e o conteúdo em qualquer elemento do corpo."

Esta regra refere-se ao espaçamento **interno** das caixas (entre a linha de
borda superior e a primeira linha de conteúdo), não às linhas em branco
**entre** caixas distintas. O renderer atual é um placeholder que não implementa
R-10 — não há linha em branco interna às caixas, e a correção de R-10 está fora
do escopo deste ciclo.

O H-0009 remove somente as linhas em branco **entre regiões visuais** (os
`"\n\n"` que separam caixas em `renderizar_tela`). Não adiciona nem remove
espaçamento interno às caixas. A conformidade com R-10 é tarefa futura, quando
o body composer real for implementado.

Se o executor entender que remover `"\n\n"` interfere com R-10 ou exige decisão
contratual, deve parar com `BLOCKED` e descrever o conflito.

---

## Especificação: `tela/renderizador.py`

### Nova assinatura de `renderizar_tela`

```python
def renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva", largura: int | None = None) -> str:
```

Regras:

- Quando `largura=None`, usar `TOTAL_WIDTH = 42` como fallback (preserva
  comportamento exato do H-0006/H-0007/H-0008 para `diagnostico.py`).
- Quando `largura` for fornecido, usar o valor fornecido como `total_w`.
- A partir de `total_w`, derivar:
  - `inner_w = total_w - 2`
  - `content_w = total_w - 3`
  - `label_max = total_w - 4`
- As funções auxiliares `_linha_topo`, `_linha_base`, `_linha_conteudo`,
  `_caixa` devem ser atualizadas para aceitar e usar as dimensões derivadas.
  O implementador pode refatorar os parâmetros dessas funções privadas
  livremente, desde que o comportamento externo de `renderizar_tela` seja
  o especificado aqui.
- `largura` menor que 10 tem comportamento indefinido neste ciclo; não é
  necessário validar nem tratar.

### Remoção das linhas em branco entre caixas

A linha de retorno de `renderizar_tela` deve mudar de:

```python
return (
    caixa_cabecalho + "\n\n"
    + caixa_dashboard + "\n\n"
    + caixa_menu + "\n"
)
```

Para:

```python
return (
    caixa_cabecalho + "\n"
    + caixa_dashboard + "\n"
    + caixa_menu + "\n"
)
```

Nenhuma outra mudança de estrutura visual está autorizada.

### Constantes de módulo

Manter `TOTAL_WIDTH = 42` como constante pública de fallback. As outras
constantes (`INNER_WIDTH`, `CONTENT_WIDTH`, `_LABEL_MAX`) podem permanecer
como constantes de módulo (usadas como fallback quando `largura=None`) ou
ser internalizadas nas funções auxiliares — decisão do implementador.

### Saída esperada com `largura=None` (fallback 42) e `tipo_borda="curva"`

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

Sem linha em branco entre caixas. Cada linha não-vazia tem exatamente 42
chars Python. A string termina com `"\n"`.

### Saída esperada com `largura=None` (fallback 42) e `tipo_borda="reta"`

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

### Invariante de largura com `largura=W` explícito

Quando `largura=W` for fornecido, toda linha não-vazia da saída deve ter
exatamente `W` chars Python.

---

## Especificação: `tela/demo.py`

### Mudanças no dict de estado

O dict de estado permanece com exatamente duas chaves:

| Chave | Tipo | Valor inicial |
|---|---|---|
| `"tipo_borda"` | `str` | `"curva"` |
| `"saindo"` | `bool` | `False` |

Nenhuma chave nova deve ser adicionada.

### Nova assinatura de `processar_comando`

```python
processar_comando(estado: dict, comando: str) -> dict
```

| Comando | Efeito |
|---|---|
| `"b"` | Alterna `tipo_borda`: `"curva"` → `"reta"` ou `"reta"` → `"curva"` |
| `"s"` | Define `saindo=True`; `tipo_borda` permanece inalterado |
| `"\x1b"` | Define `saindo=True`; `tipo_borda` permanece inalterado |
| qualquer outro (incluindo string vazia) | Retorna cópia de `estado` sem alteração |

Regras obrigatórias (herdadas de H-0008, agora incluindo `"\x1b"`):

- Não modifica o dict `estado` recebido como argumento.
- Retorna sempre um novo dict com as chaves `"tipo_borda"` e `"saindo"`.
- A validação de `comando` é case-sensitive.
- Não chama `renderizar_tela` nem acessa modelo.

Sobre o comando `"s"` (atalho auxiliar):

`"s"` é mantido como atalho auxiliar de saída. Justificativa: permite testes
automatizados via pipe sem TTY real (os testes de subprocess existentes usam
`printf 'b\ns\n' | python tela/demo.py`). `"s"` não substitui nem elimina
`"\x1b"` — ambos coexistem. `"s"` é comando interno da demo; não é binding
declarativo do JSON.

### Nova assinatura de `renderizar_estado`

```python
renderizar_estado(estado: dict, modelo: ModeloTela, largura: int | None = None) -> str
```

Implementação:

```python
def renderizar_estado(estado, modelo, largura=None):
    return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"], largura=largura)
```

Regras:

- Não modifica `estado` nem `modelo`.
- Nenhum efeito colateral além da chamada a `renderizar_tela`.
- `largura=None` produz saída determinística com fallback 42 chars.

### Função privada de captura de tecla única

O implementador deve definir uma função privada (nome livre, sugestão:
`_ler_tecla_unica`) que:

- Use `termios` e `tty` da biblioteca padrão do Python.
- Entre em modo raw (`tty.setraw(fd)`) para o file descriptor de stdin.
- Leia exatamente 1 char com `sys.stdin.read(1)`.
- Restaure o estado original do terminal com `termios.tcsetattr` em bloco
  `finally`, garantindo restauração mesmo em caso de exceção.
- Retorne o char lido como `str`.

Exemplo de estrutura aceitável (não é código normativo):

```python
def _ler_tecla_unica():
    import termios
    import tty
    fd = sys.stdin.fileno()
    config_original = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, config_original)
    return ch
```

O implementador pode usar variante com um único bloco `try/finally` cobrindo
o loop inteiro em vez de por-leitura — desde que o terminal seja restaurado
em qualquer saída (normal, exceção, Ctrl+C).

### Importações novas permitidas em `tela/demo.py`

- `import shutil` — para `shutil.get_terminal_size`
- `import termios` — para modo raw
- `import tty` — para modo raw

Estas importações devem ser feitas dentro da função que as utiliza (lazy
import), ou no nível de módulo — decisão do implementador. Se importadas no
nível de módulo, devem ser condicionadas a `try/except ImportError` somente se
necessário para compatibilidade; em Linux/macOS padrão, `termios` e `tty`
estão disponíveis sem guarda.

Importações ainda proibidas em `tela/demo.py`:

- `import json`, `import os`, `import pathlib`
- `import curses`, `import textual`, `import rich`
- `import subprocess`, `exec`, `eval`
- Qualquer biblioteca de terceiros não pertencente à stdlib Python.

### Nova assinatura e comportamento de `main()`

```python
def main() -> int:
```

Passos obrigatórios:

1. Executar o bootstrap de `sys.path` (padrão herdado de H-0008).
2. Chamar `carregar_tela(None, "orquestrador")` e `construir_modelo(tela_raw)`.
3. Chamar `criar_estado_inicial()` para obter o estado inicial.
4. Ler a largura real do terminal:
   ```python
   largura = shutil.get_terminal_size(fallback=(80, 24)).columns
   ```
5. Imprimir o render inicial: `print(renderizar_estado(estado, modelo, largura), end="")`.
6. Detectar se stdin é TTY: `sys.stdin.isatty()`.
7. **Modo TTY** (quando `sys.stdin.isatty()` é `True`):
   - Usar `_ler_tecla_unica()` (ou equivalente) em loop.
   - Cada char lido é passado diretamente para `processar_comando(estado, ch)`.
   - Se `estado["saindo"]` é `True`: encerrar o loop imediatamente.
   - Se `ch == "b"` e estado não está saindo: imprimir novo render com
     `print(renderizar_estado(estado, modelo, largura), end="")`.
   - O char NÃO deve aparecer na tela (sem echo).
   - O terminal deve ser restaurado ao sair do loop (via `finally`).
8. **Modo não-TTY** (quando `sys.stdin.isatty()` é `False`):
   - Iterar sobre `sys.stdin` linha a linha.
   - Para cada linha: `comando = linha.strip()`.
   - Chamar `novo_estado = processar_comando(estado, comando)`.
   - Atualizar `estado = novo_estado`.
   - Se `estado["saindo"]` é `True`: sair do loop imediatamente.
   - Se `comando == "b"`: imprimir novo render.
   - Para qualquer outro comando (incluindo vazio e desconhecido): não re-renderizar.
9. Retornar `0` (saída limpa).
10. Em `if __name__ == "__main__"`: chamar `sys.exit(main())`.

Regras adicionais de `main()`:

- EOF em `sys.stdin` (modo não-TTY) encerra o loop normalmente com retorno `0`.
- Não imprime prompt (`"> "`, `"comando: "`, etc.) em nenhum modo.
- Não imprime mensagem de erro para comandos desconhecidos.
- Não imprime mensagem de despedida ao sair.
- Em modo TTY, `b` e `"\x1b"` não aparecem na tela (modo raw desativa echo).

### Estrutura obrigatória do arquivo `tela/demo.py`

O arquivo deve conter, nesta ordem:

1. Docstring descritiva do módulo.
2. `import sys` e `sys.dont_write_bytecode = True`.
3. Bloco `if __name__ == "__main__"` com bootstrap de `sys.path`.
4. Importações de `tela.*` e de módulos stdlib necessários.
5. Definição de `criar_estado_inicial()`.
6. Definição de `processar_comando(estado, comando)`.
7. Definição de `renderizar_estado(estado, modelo, largura=None)`.
8. Definição da função privada de captura de tecla (se separada).
9. Definição de `main()`.
10. Bloco `if __name__ == "__main__": sys.exit(main())`.

---

## Especificação: `tela/teste_demo.py`

### Constantes de saída esperada (H-0009)

As constantes `_EXPECTED_CURVA` e `_EXPECTED_RETA` devem ser atualizadas para
refletir a remoção das linhas em branco entre caixas. Novo valor obrigatório:

```python
_EXPECTED_CURVA = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
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
    "┌ Menu ──────────────────────────────────┐\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "└────────────────────────────────────────┘\n"
)
```

Estas constantes são geradas com `largura=None` (fallback 42). Todos os testes
que comparam saída exata do renderer devem usar `largura=42` explicitamente ou
deixar `largura=None` e comparar com estas constantes.

### Seção 1 — Estado inicial (sem mudança de comportamento)

Manter as 4 verificações existentes. Nenhuma verificação nova necessária.

### Seção 2 — `processar_comando` (adições obrigatórias)

Adicionar às verificações existentes:

| Verificação | Critério |
|---|---|
| `"\x1b"` define `saindo == True` | `processar_comando({"tipo_borda":"curva","saindo":False},"\x1b")["saindo"] == True` |
| `"\x1b"` não altera `tipo_borda` (curva) | `processar_comando({"tipo_borda":"curva","saindo":False},"\x1b")["tipo_borda"] == "curva"` |
| `"\x1b"` não altera `tipo_borda` (reta) | `processar_comando({"tipo_borda":"reta","saindo":False},"\x1b")["tipo_borda"] == "reta"` |
| `processar_comando` não modifica dict original com `"\x1b"` | `estado_original["saindo"]` permanece `False` após chamada com `"\x1b"` |
| `"s"` mantido como atalho auxiliar: `"s"` define `saindo == True` | verificação existente mantida |

Manter todas as verificações existentes de `processar_comando` (14 verificações).
Total da seção: mínimo 18 verificações (14 existentes + 4 novas de `"\x1b"`).

### Seção 3 — `renderizar_estado` (atualizações obrigatórias)

Atualizar comparações de saída para usar as novas constantes sem `"\n\n"`.

Adicionar verificações para `largura` explícita:

| Verificação | Critério |
|---|---|
| `renderizar_estado(estado_curva, modelo, largura=42)` == `_EXPECTED_CURVA` | igualdade estrita |
| `renderizar_estado(estado_reta, modelo, largura=42)` == `_EXPECTED_RETA` | igualdade estrita |
| `renderizar_estado(estado_curva, modelo, largura=60)` — cada linha tem 60 chars | `all(len(ln)==60 for ln in saida.split("\n") if ln)` |
| `renderizar_estado(estado_curva, modelo)` == `renderizar_estado(estado_curva, modelo, largura=None)` | igualdade — fallback equivalente |

### Seção 4 — Integração via subprocess (atualizações obrigatórias)

O subprocess test mantém `input="b\ns\n"` (modo não-TTY, `s` disponível).

**Verificações de saída sem igualdade estrita de string completa:**

A largura usada pelo subprocess depende de `shutil.get_terminal_size`. Em
contexto de pipe (stdout capturado, sem TTY), o Python usa o fallback
`(80, 24)`, retornando `largura=80`. O teste deve construir o esperado
chamando `renderizar_tela` diretamente com `largura=80`:

```python
_LARGURA_SUBPROCESS = 80  # fallback de shutil.get_terminal_size em pipe
_EXPECTED_SUBPROCESS_CURVA = renderizar_tela(modelo, tipo_borda="curva", largura=_LARGURA_SUBPROCESS)
_EXPECTED_SUBPROCESS_RETA  = renderizar_tela(modelo, tipo_borda="reta",  largura=_LARGURA_SUBPROCESS)
saida_esperada = _EXPECTED_SUBPROCESS_CURVA + _EXPECTED_SUBPROCESS_RETA
```

O teste usa a variável de ambiente `COLUMNS` como guarda: se `COLUMNS` estiver
definida no ambiente do processo de teste, pode interferir. O subprocess deve
ser invocado sem `COLUMNS` no env para garantir determinismo:

```python
import os
env_sem_columns = {k: v for k, v in os.environ.items() if k != "COLUMNS"}
proc = subprocess.run(
    [sys.executable, "tela/demo.py"],
    cwd=str(_BASE_PADRAO),
    input="b\ns\n",
    capture_output=True,
    text=True,
    env=env_sem_columns,
)
```

Verificações obrigatórias do subprocess:

| Verificação | Critério |
|---|---|
| Encerra com código 0 | `proc.returncode == 0` |
| stdout contém render curva inicial | `"╭ ORQUESTRADOR" in proc.stdout` |
| stdout contém render reta após `b` | `"┌ ORQUESTRADOR" in proc.stdout` |
| stdout não contém linha em branco entre caixas | `"\n\n" not in proc.stdout` |
| stdout bate com esperado construído via `renderizar_tela(..., largura=80)` | `proc.stdout == saida_esperada` |
| stderr está vazio | `proc.stderr == ""` |
| `config/telas/orquestrador.json` inalterado após demo | conteúdo antes == conteúdo depois |

Adicionar também verificação via `"\x1b"` no subprocess (modo linha com Esc):

```python
proc_esc = subprocess.run(
    [sys.executable, "tela/demo.py"],
    cwd=str(_BASE_PADRAO),
    input="b\n\x1b\n",   # b + Esc como linha
    capture_output=True,
    text=True,
    env=env_sem_columns,
)
```

| Verificação | Critério |
|---|---|
| Demo encerra com `b\n\x1b\n` e código 0 | `proc_esc.returncode == 0` |
| stdout contém render curva e render reta após `b` | ambos presentes |
| stdout idêntico à execução com `b\ns\n` | `proc_esc.stdout == proc.stdout` |

### Seção 5 — Preservação do diagnóstico (atualizações obrigatórias)

A função `gerar_diagnostico_tela()` continua chamando `renderizar_tela(modelo)`
sem `largura` → usa fallback 42 chars → saída determinística. O conteúdo muda
(sem `"\n\n"` entre caixas) mas o determinismo e a não-interatividade são
preservados.

A constante de comparação nesta seção deve ser `_EXPECTED_CURVA` (definida
acima, sem linhas em branco entre caixas). A verificação `gerar_diagnostico_tela()
bate com _EXPECTED_CURVA` usa a nova constante.

### Seção 6 (nova) — Inspeção de código para modo sem echo

Adicionar verificações por inspeção de texto de `tela/demo.py`:

| Verificação | Critério |
|---|---|
| `demo.py` contém `termios` | `"termios" in texto_mod` |
| `demo.py` contém `tty` | `"tty" in texto_mod` |
| `demo.py` contém `shutil.get_terminal_size` | `"shutil.get_terminal_size" in texto_mod` |
| `demo.py` contém `isatty` | `"isatty" in texto_mod` |
| `demo.py` não contém `input(` | `"input(" not in texto_mod` |
| `demo.py` não contém `curses` | ausência de import |
| `demo.py` não contém `textual` | ausência de import |
| `demo.py` não contém `rich` | ausência de import |

---

## Especificação: `tela/teste_renderizador.py`

### Constantes de saída esperada

Atualizar `_EXPECTED_ORQUESTRADOR` e `_EXPECTED_ORQUESTRADOR_RETA` para remover
as linhas em branco entre caixas. Novo valor obrigatório:

```python
_EXPECTED_ORQUESTRADOR = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
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
    "┌ Menu ──────────────────────────────────┐\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "└────────────────────────────────────────┘\n"
)
```

### Verificações a atualizar

- Verificação `"cada linha da saida tem exatamente 42 chars Python"`: continua
  válida para `renderizar_tela(modelo)` com `largura=None` (fallback 42). Manter.
- Verificação `"saida bate com expected output literal do handoff H-0006"`:
  atualizar comentário para referenciar H-0009 (saída mudou — sem `"\n\n"`).
- Todas as outras verificações continuam funcionando sem mudança.

### Seção nova — `largura` explícita

Adicionar verificações para o parâmetro `largura`:

| Verificação | Critério |
|---|---|
| `renderizar_tela(modelo, largura=42)` == `_EXPECTED_ORQUESTRADOR` | igualdade estrita com fallback |
| `renderizar_tela(modelo, largura=42, tipo_borda="reta")` == `_EXPECTED_ORQUESTRADOR_RETA` | igualdade estrita |
| `renderizar_tela(modelo, largura=60)` retorna str | `isinstance(resultado, str)` |
| cada linha não-vazia de `renderizar_tela(modelo, largura=60)` tem 60 chars | `all(len(ln)==60 for ln in saida.split("\n") if ln)` |
| saída com `largura=60` começa com `"╭ ORQUESTRADOR"` | `saida.startswith("╭ ORQUESTRADOR")` |
| saída com `largura=60` não contém `"\n\n"` | `"\n\n" not in saida` |
| `renderizar_tela(modelo)` == `renderizar_tela(modelo, largura=None)` | `largura=None` é equivalente a omitir |

---

## Especificação: `tela/teste_diagnostico.py`

Atualizar a constante `_EXPECTED_ORQUESTRADOR` para remover as linhas em branco
entre caixas. Novo valor obrigatório:

```python
_EXPECTED_ORQUESTRADOR = (
    "╭ ORQUESTRADOR ──────────────────────────╮\n"
    "│ Tela raiz do sistema — ponto de entrada│\n"
    "╰────────────────────────────────────────╯\n"
    "╭ DASHBOARD ─────────────────────────────╮\n"
    "│ Dashboard de teste                     │\n"
    "│ Sem dados carregados                   │\n"
    "╰────────────────────────────────────────╯\n"
    "╭ Menu ──────────────────────────────────╮\n"
    "│ [Esc] Sair    [B] Borda                │\n"
    "╰────────────────────────────────────────╯\n"
)
```

Nenhuma outra alteração em `tela/teste_diagnostico.py` é necessária. O número
de verificações permanece 26 (apenas os valores esperados mudam).

---

## Escopo positivo autorizado

O H-0009 autoriza e especifica:

1. Alterar `tela/renderizador.py` — adicionar `largura`, remover `"\n\n"`.
2. Alterar `tela/demo.py` — entrada sem echo, Esc real, `processar_comando`
   com `"\x1b"`, `renderizar_estado` com `largura`, `main()` com TTY detection.
3. Alterar `tela/teste_renderizador.py` — novos esperados, novos testes de `largura`.
4. Alterar `tela/teste_demo.py` — novos esperados, novos testes de `"\x1b"`.
5. Alterar `tela/teste_diagnostico.py` — atualizar constante de esperado.
6. Criar `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md`.

---

## Fora de escopo — proibições explícitas

O H-0009 **não implementa** nenhum dos itens abaixo:

- dashboard real ou dados de dashboard;
- contrato novo de dashboard;
- lançador;
- abertura de tela de teste;
- navegação entre telas ou por `tela_destino`;
- registry de ações;
- bindings ativos declarativos do JSON;
- execução real de chips declarativos;
- pop-up;
- tela de processamento;
- filtros funcionais;
- paginação funcional;
- seleção funcional;
- resize reativo completo via SIGWINCH;
- sistema completo de layout;
- constraints avançadas de layout;
- layout responsivo complexo;
- leitura de `config/estilo.json`;
- leitura de `config/layout_console.json`;
- leitura de `config/lancador.json`;
- declaração de tamanho no `config/telas/orquestrador.json`;
- alteração de `config/telas/orquestrador.json`;
- alteração de qualquer arquivo em `config/`;
- alteração de contratos, ADRs, NOMENCLATURA ou documentos normativos;
- uso de `curses`, `textual`, `rich` ou qualquer biblioteca de UI externa;
- persistência de `tipo_borda` em arquivo ou variável global;
- linha em branco interna às caixas (conformidade com R-10 do contrato);
- transformação de `diagnostico.py` em loop interativo;
- transformação de `b` ou `"\x1b"` em ações declarativas do JSON.

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os arquivos abaixo:

```
tela/renderizador.py          — ALTERAR
tela/teste_renderizador.py    — ALTERAR
tela/demo.py                  — ALTERAR
tela/teste_demo.py            — ALTERAR
tela/teste_diagnostico.py     — ALTERAR
docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md  — CRIAR
```

A lista acima é exaustiva e sem exceção. Se a implementação exigir alterar
qualquer outro arquivo, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

---

## Arquivos proibidos de alterar

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
docs/templates/              (qualquer arquivo)
config/                      (qualquer arquivo)
```

---

## Pré-condição obrigatória

Antes de criar ou alterar qualquer arquivo, confirmar que todos os invariantes
anteriores estão passando:

```bash
python tela/teste_loader.py         # 37 verificações passando
python tela/teste_modelo.py         # 30 verificações passando
python tela/teste_renderizador.py   # 58 verificações passando
python tela/teste_diagnostico.py    # 26 verificações passando
python tela/teste_demo.py           # 49 verificações passando
python tela/diagnostico.py          # saída curva H-0008, código 0
printf 'b\ns\n' | python tela/demo.py   # dois renders: curva + reta, código 0
```

Se qualquer verificação falhar, parar imediatamente com `BLOCKED` e registrar
qual verificação falhou e em qual módulo.

---

## Critérios de aceite verificáveis

### Largura dinâmica

- [ ] `renderizar_tela(modelo)` usa `largura=None` → fallback 42 chars; saída
      sem `"\n\n"` entre caixas; cada linha não-vazia tem 42 chars.
- [ ] `renderizar_tela(modelo, largura=60)` → cada linha não-vazia tem 60 chars.
- [ ] `renderizar_tela(modelo, largura=42)` == `renderizar_tela(modelo)`.
- [ ] `renderizar_tela(modelo, largura=None)` == `renderizar_tela(modelo)`.
- [ ] `diagnostico.py` continua sem `largura` explícito → usa fallback 42.

### Ausência de linha em branco entre regiões visuais

- [ ] Saída de `renderizar_tela(modelo)` não contém `"\n\n"`.
- [ ] Saída de `renderizar_tela(modelo, largura=60)` não contém `"\n\n"`.
- [ ] Saída de `python tela/diagnostico.py` não contém linha em branco entre caixas.
- [ ] Saída de `python tela/demo.py` (interativo ou pipe) não contém `"\n\n"`.

### Entrada sem Enter e sem echo

- [ ] Em modo TTY real: `b` alterna borda sem precisar Enter.
- [ ] Em modo TTY real: `b` não aparece na tela (confirmação manual de QA).
- [ ] Em modo TTY real: Esc sai sem precisar Enter.
- [ ] Em modo TTY real: Esc não aparece na tela (confirmação manual de QA).
- [ ] `demo.py` contém `termios` (inspeção de código).
- [ ] `demo.py` contém `tty` (inspeção de código).
- [ ] `demo.py` contém `shutil.get_terminal_size` (inspeção de código).
- [ ] `demo.py` contém `isatty` (inspeção de código).
- [ ] `demo.py` não contém `input(` (inspeção de código).

### Esc real funcionando

- [ ] `processar_comando(estado, "\x1b")["saindo"] == True`.
- [ ] `processar_comando({"tipo_borda":"curva","saindo":False}, "\x1b")["tipo_borda"] == "curva"`.
- [ ] `processar_comando({"tipo_borda":"reta","saindo":False}, "\x1b")["tipo_borda"] == "reta"`.
- [ ] `processar_comando` não modifica dict original com `"\x1b"`.
- [ ] Subprocess com `input="b\n\x1b\n"` encerra com código 0 e saída idêntica
      à subprocess com `input="b\ns\n"`.
- [ ] `[Esc] Sair` exibido no menu corresponde a comportamento real (Esc sai).

### `s` como atalho auxiliar

- [ ] `processar_comando(estado, "s")["saindo"] == True` (auxiliar mantido).
- [ ] `s` é comando interno; não é binding declarativo do JSON.
- [ ] Subprocess com `input="b\ns\n"` continua funcionando e encerrando com 0.

### Estado em memória

- [ ] Estado de borda continua somente em memória local.
- [ ] `config/telas/orquestrador.json` inalterado após execução da demo.
- [ ] `processar_comando` não usa variável global mutável.
- [ ] Segunda execução da demo inicia com `tipo_borda="curva"`.

### Diagnóstico não interativo

- [ ] `tela/diagnostico.py` não foi alterado.
- [ ] `gerar_diagnostico_tela()` retorna saída determinística sem `"\n\n"`.
- [ ] `python tela/diagnostico.py` encerra com código 0 sem solicitar entrada.
- [ ] `diagnostico.py` não contém `sys.stdin` nem `input(`.

### Testes automatizados

- [ ] `python tela/teste_loader.py` retorna código 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna código 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna código 0 (mínimo 65
      verificações: 58 existentes + 7 novas de `largura`).
- [ ] `python tela/teste_diagnostico.py` retorna código 0 (26 verificações).
- [ ] `python tela/teste_demo.py` retorna código 0 (mínimo 58 verificações:
      49 existentes + novas de `"\x1b"`, `largura`, inspeção de código).

### Escopo e ausências

- [ ] Somente os arquivos listados em "Arquivos permitidos" foram criados ou alterados.
- [ ] Nenhum arquivo fora do escopo autorizado foi criado ou alterado.
- [ ] Nenhum contrato, ADR, nomenclatura, índice, handoff anterior,
      relatório anterior ou `config/` foi alterado.
- [ ] Não há dashboard real.
- [ ] Não há lançador.
- [ ] Não há navegação entre telas.
- [ ] Não há registry de ações.
- [ ] Não há bindings ativos do JSON.
- [ ] Não há uso de `curses`, `textual`, `rich` ou biblioteca de UI externa.

---

## Condições de bloqueio

O executor deve parar imediatamente com `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se:

1. Qualquer pré-condição (H-0001 a H-0008) falhar antes de iniciar.
2. A implementação exigir alterar qualquer arquivo fora de "Arquivos permitidos".
3. A implementação exigir alterar `tela/diagnostico.py`.
4. A implementação exigir alterar `tela/loader.py` ou `tela/modelo.py`.
5. A implementação exigir ativar chips reais, executar bindings declarativos
   do JSON ou criar registry de ações: **ARCHITECTURE_REVIEW_REQUIRED**.
6. A implementação exigir `curses`, `textual`, `rich` ou biblioteca de UI.
7. A implementação exigir persistência de estado em arquivo ou variável global.
8. A implementação exigir navegação entre telas ou `tela_destino`.
9. A implementação exigir SIGWINCH ou resize reativo completo:
   **ARCHITECTURE_REVIEW_REQUIRED**.
10. A implementação exigir leitura de `config/estilo.json`,
    `config/layout_console.json`, `config/lancador.json` ou qualquer outro
    arquivo em `config/`.
11. A implementação exigir dependência externa além da stdlib Python.
12. `python tela/teste_diagnostico.py` falhar após as alterações e não houver
    alteração mínima dentro do escopo autorizado.
13. A saída do renderer com `largura=None` contiver `"\n\n"`.
14. Qualquer linha não-vazia de `renderizar_tela(modelo, largura=W)` tiver
    comprimento Python diferente de `W` chars.
15. A demo em modo TTY exibir o char `b` ou Esc na tela após a tecla ser
    pressionada.
16. `diagnostico.py` solicitar entrada do usuário após as alterações.

---

## Comandos de verificação obrigatórios

Executar a partir do diretório raiz do repositório de scripts. O relatório
IMP-0009 deve incluir a saída real de cada comando.

```bash
# 1. Integridade do JSON de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"

# 2. Invariantes H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes H-0002 preservados
python tela/teste_modelo.py

# 4. Invariantes H-0006/H-0007 preservados (novo total ≥ 65)
python tela/teste_renderizador.py

# 5. Invariantes H-0004/H-0006 preservados (26 verificações; esperado atualizado)
python tela/teste_diagnostico.py

# 6. Testes da demo (H-0009; novo total ≥ 58)
python tela/teste_demo.py

# 7. Diagnóstico executável (não interativo; sem linha em branco entre caixas)
python tela/diagnostico.py

# 8. Demo via pipe com s (modo não-TTY; sem linha em branco entre caixas)
printf 'b\ns\n' | python tela/demo.py

# 9. Demo via pipe com Esc (modo não-TTY; saída deve ser idêntica ao comando 8)
printf 'b\n\x1b\n' | python tela/demo.py

# 10. Demo com EOF sem comando de saída (deve encerrar com código 0)
printf '' | python tela/demo.py; echo "exit_code=$?"

# 11. Verificação de bytecode
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print

# 12. Estado do repositório
git status --short
git diff --stat
git diff --name-only
```

Todos os comandos devem produzir saída limpa (códigos de saída 0, sem
falhas). `find` deve produzir saída vazia.

### Demonstração manual obrigatória (QA)

```bash
python tela/demo.py
```

Confirmação manual dos itens a seguir (não automatizável por depender de TTY):

- pressionar `b` alterna a borda sem Enter;
- o caractere `b` não aparece na tela;
- pressionar Esc sai sem Enter;
- Esc não aparece na tela;
- as caixas ocupam a largura calculada do terminal;
- não há linha em branco entre caixas.

---

## Formato esperado do relatório `IMP-0009`

O executor deve criar:

```
docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md
```

O relatório deve conter obrigatoriamente:

1. **Status**: `IMPLEMENTATION_COMPLETED`, `APROVADO`, `APROVADO_COM_RESSALVAS`
   ou `BLOQUEADO`.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo.
3. **Arquivos não alterados**: confirmação explícita dos arquivos proibidos.
4. **API implementada**: excertos das mudanças em `renderizar_tela`,
   `processar_comando`, `renderizar_estado` e `main`.
5. **Saída real de `python tela/diagnostico.py`**: reprodução literal do stdout
   (sem linhas em branco entre caixas, sem interação).
6. **Saída real de `printf 'b\ns\n' | python tela/demo.py`**: reprodução literal.
7. **Saída real de `printf 'b\n\x1b\n' | python tela/demo.py`**: reprodução literal.
8. **Resultado dos testes**: saída completa dos scripts de teste com total de
   verificações.
9. **Invariantes H-0001 a H-0008 preservados**: confirmação com totais.
10. **Ausência de persistência**: confirmação de que `config/telas/orquestrador.json`
    não foi alterado.
11. **Saída real de todos os comandos de verificação**: cópia integral.
12. **Confirmação de ausência de `"\n\n"` entre caixas**: evidência literal.
13. **Confirmação de largura dinâmica**: evidência de que `renderizar_tela` com
    `largura` explícito produz linhas do comprimento correto.
14. **Nota sobre R-10**: confirmar que espaçamento interno às caixas (R-10)
    não foi alterado e está fora do escopo deste ciclo.
15. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Checklist final para QA

- [ ] H-0009 lido integralmente antes de qualquer criação ou alteração de arquivo.
- [ ] Pré-condições verificadas (todos os testes H-0001 a H-0008 passando).
- [ ] Somente os arquivos autorizados foram criados ou alterados.
- [ ] `git diff --stat` não mostra alterações em arquivos fora do escopo.
- [ ] Nenhum contrato, ADR ou documento normativo alterado.
- [ ] `renderizar_tela` aceita `largura` opcional com fallback 42.
- [ ] Saída de `renderizar_tela(modelo)` não contém `"\n\n"`.
- [ ] Saída de `renderizar_tela(modelo, largura=60)` tem linhas de 60 chars.
- [ ] `processar_comando(estado, "\x1b")` define `saindo=True`.
- [ ] `processar_comando(estado, "\x1b")` não altera `tipo_borda`.
- [ ] `processar_comando` não modifica dict original com `"\x1b"`.
- [ ] `renderizar_estado` aceita `largura` opcional.
- [ ] `main()` lê largura com `shutil.get_terminal_size(fallback=(80, 24))`.
- [ ] `main()` detecta TTY com `sys.stdin.isatty()`.
- [ ] Em modo TTY: entrada sem Enter, sem echo, Esc sai (verificação manual).
- [ ] Em modo não-TTY: linha a linha, `s` e `"\x1b"` funcionam.
- [ ] Terminal restaurado ao sair (try/finally em torno de modo raw).
- [ ] `demo.py` contém `termios`, `tty`, `shutil.get_terminal_size`, `isatty`.
- [ ] `demo.py` não importa `json`, `os`, `pathlib`, `curses`, `textual`, `rich`.
- [ ] `tela/diagnostico.py` não alterado.
- [ ] `diagnostico.py` não contém `sys.stdin` nem `input(`.
- [ ] `gerar_diagnostico_tela()` retorna saída sem `"\n\n"` e determinística.
- [ ] `python tela/teste_loader.py` retorna 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna 0 (mínimo 65 verificações).
- [ ] `python tela/teste_diagnostico.py` retorna 0 (26 verificações).
- [ ] `python tela/diagnostico.py` imprime saída sem `"\n\n"` e encerra 0.
- [ ] `python tela/teste_demo.py` retorna 0 (mínimo 58 verificações).
- [ ] `printf 'b\ns\n' | python tela/demo.py` encerra com 0.
- [ ] `printf 'b\n\x1b\n' | python tela/demo.py` encerra com 0.
- [ ] Saídas de `b\ns\n` e `b\n\x1b\n` são idênticas.
- [ ] Stdout das demos via pipe não contém `"\n\n"`.
- [ ] `config/telas/orquestrador.json` válido e inalterado.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md` criado.
- [ ] Commit não realizado (responsabilidade do engenheiro).
