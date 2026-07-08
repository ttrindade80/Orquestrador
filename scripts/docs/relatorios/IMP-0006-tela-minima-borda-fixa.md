# Relatório de Implementação — H-0006 Tela mínima com borda fixa

## Status

IMPLEMENTATION_COMPLETED

## Arquivos alterados

- `tela/renderizador.py` — ALTERADO (formato visual com borda fixa H-0006)
- `tela/teste_renderizador.py` — ALTERADO (verificações H-0006, 5 seções)
- `tela/teste_diagnostico.py` — ALTERADO (verificações de formato atualizadas)
- `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md` — CRIAR (este relatório)

Nenhum outro arquivo foi criado ou alterado. `git diff --stat` confirma
apenas os 3 arquivos de código; `docs/handoff/` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0006_HANDOFF.md` aparecem como
não rastreados pré-existentes (fora do escopo desta implementação).

## Resumo da implementação

O handoff H-0006 especifica a evolução de `renderizar_tela(modelo: ModeloTela) -> str`
de um renderer estrutural textual (H-0005, formato `TELA:`/`SCHEMA:`/`REGIAO:`)
para um renderer visual com borda fixa composto por três caixas bordeadas,
cada linha com exatamente 42 caracteres Python.

### O que foi implementado

1. **Assinatura e classe preservadas**:
   - `class RenderizadorErro(Exception)` — mantida.
   - `def renderizar_tela(modelo: ModeloTela) -> str` — assinatura inalterada.

2. **Importações**: única importação de aplicação é
   `from tela.modelo import ModeloTela`. Nenhuma importação de `json`,
   `os`, `pathlib`, `tela.loader`, `subprocess`, nem mecanismos de execução.

3. **Constantes de layout** (H-0006):
   - `TOTAL_WIDTH = 42`, `INNER_WIDTH = 40`, `CONTENT_WIDTH = 39`,
     `_LABEL_MAX = 38`.

4. **Caixas produzidas**:
   - **Caixa de cabeçalho** — label derivado de
     `modelo.cabecalho.get("titulo", "(ausente)").upper()` (truncado a 38);
     conteúdo de `modelo.cabecalho.get("descricao", "(ausente)")[:39]`.
   - **Caixa de dashboard** — hardcoded: label `DASHBOARD`, linhas
     `Dashboard de teste` e `Sem dados carregados`.
   - **Caixa de menu** — hardcoded: label `Menu`, linha
     `[Esc] Sair    [B] Borda`.

5. **Caracteres de borda**: `╭ ╮ ╰ ╯ │ ─` (Unicode U+256D/U+256E/U+2570/
   U+256F/U+2502/U+2500), conforme tabela do handoff.

6. **Ressalva da auditoria respeitada**: o handoff menciona textualmente
   `modelo.cabecalho.titulo`/`descricao`, mas a API real do modelo usa
   `cabecalho: dict`. A implementação usa exclusivamente
   `modelo.cabecalho.get(...)`, sem criar atributos `.titulo`/`.descricao`,
   sem alterar `tela/modelo.py` e sem adaptar o modelo interno.

### Saída real do pipeline (`orquestrador.json`)

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

Saída em igualdade estrita (incluindo o `\n` final) com a constante
`_EXPECTED_ORQUESTRADOR` definida no handoff. Cada uma das 12 linhas
não-vazias possui exatamente 42 caracteres Python.

## Decisões não tomadas

Este ciclo NÃO implementa (permanecem inertes como texto/declaração):

- alternância de borda;
- estado de borda ativo;
- estilo configurável (nenhuma leitura de `config/estilo.json`);
- leitura de `config/barra_de_menus.json`;
- persistência de estilo;
- ações reais (nenhuma ação executada);
- navegação real entre telas (nenhuma resolução de `tela_destino`);
- bindings ativos;
- filtros funcionais;
- paginação funcional;
- seleção;
- registry de ações;
- registry de tipos;
- execução real de chips;
- dashboard real com dados;
- loop de aplicação;
- pop-up, tela de processamento, interface interativa;
- `curses`, `textual`, `rich` ou qualquer biblioteca de UI.

`[Esc] Sair` e `[B] Borda` são apenas texto inerte na caixa de menu —
nenhum binding é registrado e nenhuma ação é executada.

## Verificações executadas

Comandos obrigatórios executados a partir da raiz do repositório de
scripts:

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/diagnostico.py
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --stat
```

### 1. Integridade do JSON

```
orquestrador.json OK
```

### 2. Invariantes H-0001 — `tela/teste_loader.py`

```
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

### 3. Invariantes H-0002 — `tela/teste_modelo.py`

```
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

### 4. Testes H-0006 — `tela/teste_renderizador.py`

```
Total de verificacoes: 36
Passaram: 36
Falharam: 0
```

Verificações: renderizar aceita `ModeloTela` válido; saída é `str`;
saída começa com `╭ ORQUESTRADOR`; contém `│ Tela raiz do sistema`,
`╭ DASHBOARD`, `Dashboard de teste`, `Sem dados carregados`,
`╭ Menu`, `[Esc] Sair`, `[B] Borda`, `╰`; determinística; cada linha
tem 42 chars; igualdade estrita com o expected output; modelo fabricado
`titulo="Fab"` produz `╭ FAB` e `desc fab`, com caixas hardcoded
presentes e sem mencionar `orquestrador`/`ORQUESTRADOR`;
`renderizar_tela(None)` e `renderizar_tela(<dict>)` lançam
`RenderizadorErro`; proibições de import/leitura; inércia (não altera
`_raw`/`cabecalho`/`corpo.elementos`/`barra_de_menus.chips`; não vaza
campos inertes nem id interno de chip).

### 5. Diagnóstico integrado — `tela/teste_diagnostico.py`

```
Total de verificacoes: 26
Passaram: 26
Falharam: 0
```

Pré-condição subprocess agora referencia H-0006 para o renderer
(atualizado de H-0005). Verificações de formato substituídas conforme
tabela do handoff (ex.: `resultado.startswith("╭ ORQUESTRADOR")`,
`"╭ DASHBOARD" in resultado`, `"╰" in resultado`, `"│" in resultado`).

### 6. Ponto de entrada executável — `tela/diagnostico.py`

Encerra com código de saída 0 e imprime a saída H-0006 (3 caixas, 42
chars por linha). `stdout == gerar_diagnostico_tela()`.

### 7. Verificação de bytecode

```
find tela -type d -name '__pycache__' -print   (saída vazia)
find tela -type f -name '*.pyc' -print          (saída vazia)
```

Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.

## Resultado dos testes

| Comando | Resultado |
|---|---|
| `python -m json.tool config/telas/orquestrador.json` | OK |
| `python tela/teste_loader.py` | 37/37 passaram, exit 0 |
| `python tela/teste_modelo.py` | 30/30 passaram, exit 0 |
| `python tela/teste_renderizador.py` | 36/36 passaram, exit 0 |
| `python tela/teste_diagnostico.py` | 26/26 passaram, exit 0 |
| `python tela/diagnostico.py` | saída H-0006, exit 0 |
| `find tela ... __pycache__` | vazio |
| `find tela ... *.pyc` | vazio |

### Estado do repositório

`git status --short`:

```
 M tela/renderizador.py
 M tela/teste_diagnostico.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0006-tela-minima-borda-fixa.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0006_HANDOFF.md
```

`git diff --stat`:

```
 scripts/tela/renderizador.py       | 122 ++++++++++++++-----------
 scripts/tela/teste_diagnostico.py  | 112 +++++++++++++-------------
 scripts/tela/teste_renderizador.py | 183 +++++++++++++++----------------------
 3 files changed, 194 insertions(+), 223 deletions(-)
```

Os arquivos não rastreados em `docs/handoff/` e `docs/relatorios/` são
pré-existentes (o handoff e seu relatório de auditoria), não criados nem
modificados por esta implementação.

## Observações

- A ressalva de auditoria (`cabecalho: dict` em vez de atributos
  `.titulo`/`.descricao`) foi integralmente respeitada: o renderer usa
  `modelo.cabecalho.get("titulo", "(ausente)")` e
  `modelo.cabecalho.get("descricao", "(ausente)")`, sem conflito com o
  handoff (a própria tabela "Campos derivados do modelo" do H-0006 já
  especifica a forma `.get(...)`).
- Pendências documentais preservadas como inertes: DOC-B008, DOC-B009,
  `lancador_principal.itens == []`, `bindings`, `referencias_de_acoes`,
  `filtros`, `tela_destino` pendente — nenhuma resolvida ou ativada.
- A caixa de dashboard e a caixa de menu não consultam `modelo.corpo`,
  `modelo.barra_de_menus`, `modelo.id` nem `modelo.schema`.
- Commit não realizado — responsabilidade do engenheiro.
