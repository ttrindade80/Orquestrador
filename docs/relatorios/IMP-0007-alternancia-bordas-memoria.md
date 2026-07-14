# Relatório de Implementação — H-0007 Alternância de bordas em memória

## Status

IMPLEMENTATION_COMPLETED

---

## Arquivos alterados

Arquivos criados ou alterados estritamente dentro do escopo autorizado
("Arquivos permitidos" do handoff H-0007):

| Arquivo | Ação |
|---|---|
| `tela/renderizador.py` | ALTERADO |
| `tela/teste_renderizador.py` | ALTERADO |
| `docs/relatorios/IMP-0007-alternancia-bordas-memoria.md` | CRIADO (este arquivo) |

Arquivos **não** alterados (preservados conforme handoff / preferência):

- `tela/teste_diagnostico.py` — nenhuma verificação existente quebrou
  após a alteração de assinatura; o diagnóstico chama
  `renderizar_tela(modelo)` sem `tipo_borda` (default `"curva"` =
  saída H-0006), portanto permanece compatível sem alteração.
- `tela/loader.py`, `tela/modelo.py`, `tela/teste_loader.py`,
  `tela/teste_modelo.py`, `tela/diagnostico.py`, `tela/__init__.py` —
  intocados.
- `config/telas/orquestrador.json` e demais arquivos em `config/` —
  intocados.
- `docs/contratos/`, `docs/adr/`, `docs/NOMENCLATURA.md`,
  `docs/INDICE.md`, `docs/backlog.md`, `docs/issues.md`,
  `docs/handoff/`, `docs/templates/` — intocados.

`git diff --name-only` confirma que apenas `scripts/tela/renderizador.py`
e `scripts/tela/teste_renderizador.py` foram modificados.

---

## Resumo da implementação

### Objetivo do H-0007

Estender `tela/renderizador.py` para que `renderizar_tela` aceite um
parâmetro opcional `tipo_borda` que seleciona o conjunto de caracteres
de borda **em memória**, sem UI interativa, sem leitura de configuração
externa, sem persistência de qualquer natureza. A chamada padrão sem
`tipo_borda` continua produzindo exatamente a saída default do H-0006
(borda curva), em igualdade estrita incluindo o `\n` final.

### O que foi implementado

1. Adicionado o parâmetro `tipo_borda: str = "curva"` à função
   `renderizar_tela`, com a assinatura congelada do handoff.
2. Definida a constante de módulo `_BORDAS` associando os nomes
   `"curva"` e `"reta"` aos respectivos conjuntos de seis caracteres
   (quatro cantos + vertical + horizontal), em tempo de importação,
   sem leitura de arquivo.
3. Adicionada validação de `tipo_borda`: valores fora de
   `{"curva", "reta"}` lançam `RenderizadorErro`, com validação
   case-sensitive (`"CURVA"` e `"Curva"` são inválidos).
4. As funções internas `_linha_topo`, `_linha_base`, `_linha_conteudo`
   e `_caixa` foram atualizadas para receber o conjunto de bordas
   resolvido como parâmetro adicional, produzindo os cantos
   apropriados.
5. Validada a invariante de default:
   `renderizar_tela(m) == renderizar_tela(m, tipo_borda="curva")`.
6. Atualizado `tela/teste_renderizador.py` com a Seção 6 (nova),
   preservando integralmente as Seções 1–5 do H-0006.

### Assinatura da função e estrutura de bordas

Assinatura congelada implementada:

```python
def renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

Excerto da constante `_BORDAS` definida em nível de módulo em
`tela/renderizador.py`:

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

Validação de `tipo_borda` (case-sensitive):

```python
if tipo_borda not in _BORDAS:
    raise RenderizadorErro(
        "tipo_borda invalido: {0!r}; valores aceitos: curva, reta".format(
            tipo_borda
        )
    )
```

Os caracteres de borda vertical (`│`) e horizontal (`─`) são idênticos
nos dois conjuntos; apenas os quatro cantos diferem entre `"curva"` e
`"reta"`.

---

## Decisões não tomadas

Este ciclo **não toma** nenhuma decisão arquitetural e **não
implementa** nenhum dos itens abaixo (todos permanecem inertes ou fora
de escopo, conforme handoff H-0007):

- Layout dinâmico, resize, cálculo de largura real do terminal,
  layout responsivo ou ajuste dinâmico de caixa/janela.
- Persistência de estilo ou de `tipo_borda` entre chamadas.
- Estilo configurável, tema, cores ou escape codes ANSI.
- Leitura de `config/estilo.json`, `config/barra_de_menus.json`,
  `config/layout_console.json`, `config/lancador.json` ou qualquer
  arquivo em `config/`.
- Formalização da largura fixa (`TOTAL_WIDTH=42`, `INNER_WIDTH=40`,
  `CONTENT_WIDTH=39`) como regra normativa de layout final — estas
  constantes foram apenas preservadas como herança técnica provisória
  do H-0006.
- Ações reais, registry de ações ou registry de tipos.
- Navegação entre telas, navegação por `tela_destino` ou pop-up.
- Dashboard real com dados; filtros, paginação ou seleção funcionais.
- Loop de aplicação, captura real de teclado, bindings ativos ou
  binding da tecla `B`. O texto `[B] Borda` permanece apenas texto
  inerte no menu inferior.
- Mais de dois conjuntos de borda (`"curva"` e `"reta"` são os únicos).
- `curses`, `textual`, `rich` ou qualquer biblioteca de UI externa.

---

## Verificações executadas

Comandos obrigatórios executados a partir da raiz do repositório de
scripts (`scripts/`). Todas as saídas abaixo são integrais e reais.

### 1. Integridade do JSON de configuração

Comando:

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

Saída:

```text
orquestrador.json OK
```

### 2. Invariantes H-0001 (`tela/teste_loader.py`)

Comando:

```bash
python tela/teste_loader.py
```

Saída (resumo):

```text
== Resumo ==
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

### 3. Invariantes H-0002 (`tela/teste_modelo.py`)

Comando:

```bash
python tela/teste_modelo.py
```

Saída (resumo):

```text
== Resumo ==
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

### 4. Verificação de bytecode

Comandos:

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Saída:

```text
(vazia)
```

Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes (todos os
módulos usam `sys.dont_write_bytecode = True`).

### 5. Estado do repositório

Comando:

```bash
git status --short
```

Saída:

```text
 M tela/renderizador.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0007-alternancia-bordas-memoria.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0007_HANDOFF.md
?? docs/relatorios/IMP-0007-alternancia-bordas-memoria.md
```

Os arquivos `docs/handoff/H-0007-...md` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0007_HANDOFF.md` já existiam
como não-rastreados antes da implementação (não foram criados nem
alterados por este ciclo). O único artefato criado por este ciclo é
`docs/relatorios/IMP-0007-alternancia-bordas-memoria.md`.

Comando:

```bash
git diff --stat
```

Saída:

```text
 scripts/tela/renderizador.py       | 108 +++++++++++++++------
 scripts/tela/teste_renderizador.py | 189 ++++++++++++++++++++++++++++++++++++-
 2 files changed, 267 insertions(+), 30 deletions(-)
```

Comando:

```bash
git diff --name-only
```

Saída:

```text
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
```

Apenas os dois arquivos autorizados foram modificados.

---

## Resultado dos testes

### Testes do H-0007 (`tela/teste_renderizador.py`)

Comando:

```bash
python tela/teste_renderizador.py
```

Saída:

```text
Diagnostico H-0006/H-0007 - renderer visual com borda (curva/reta)
Base padrao: /home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
Python: 3.14.6

== Renderer sobre modelo de config/telas/orquestrador.json ==
[PASSOU] renderizar_tela aceita ModeloTela valido sem excecao
[PASSOU] saida e str - tipo=str
[PASSOU] saida comeca com '╭ ORQUESTRADOR'
[PASSOU] saida contem '│ Tela raiz do sistema'
[PASSOU] saida contem '╭ DASHBOARD'
[PASSOU] saida contem 'Dashboard de teste'
[PASSOU] saida contem 'Sem dados carregados'
[PASSOU] saida contem '╭ Menu'
[PASSOU] saida contem '[Esc] Sair'
[PASSOU] saida contem '[B] Borda'
[PASSOU] saida contem '╰' (borda inferior)
[PASSOU] saida e deterministica (duas chamadas identicas)
[PASSOU] cada linha da saida tem exatamente 42 chars Python
[PASSOU] saida bate com expected output literal do handoff H-0006

== Modelo fabricado: renderer usa dados do modelo, nao do JSON ==
[PASSOU] saida fabricada comeca com '╭ FAB' - prefixo='╭ FAB ──────────────────────────────────'
[PASSOU] saida fabricada contem 'desc fab'
[PASSOU] saida fabricada contem '╭ DASHBOARD' (hardcoded)
[PASSOU] saida fabricada contem '[Esc] Sair' (hardcoded)
[PASSOU] saida fabricada contem '[B] Borda' (hardcoded)
[PASSOU] saida fabricada nao menciona 'orquestrador'
[PASSOU] saida fabricada nao menciona 'ORQUESTRADOR'

== Casos de erro do renderer ==
[PASSOU] renderizar_tela(None) lanca RenderizadorErro - RenderizadorErro: renderizar_tela exige ModeloTela; recebido: NoneType
[PASSOU] renderizar_tela(<dict>) lanca RenderizadorErro - RenderizadorErro: renderizar_tela exige ModeloTela; recebido: dict

== Proibicoes de import/leitura no modulo do renderer ==
[PASSOU] renderer nao importa 'json'
[PASSOU] renderer nao importa 'os'
[PASSOU] renderer nao importa 'pathlib'
[PASSOU] renderer nao importa tela.loader (nao chama carregar_tela)
[PASSOU] renderer nao abre nem le arquivos (open/read_text/read_bytes)
[PASSOU] renderer nao usa subprocess/exec/eval
[PASSOU] renderer nao acessa _campos_inertes dos elementos

== Inercia: renderer nao executa/resolve/ativa ==
[PASSOU] renderizar_tela nao altera modelo._raw
[PASSOU] renderizar_tela nao altera modelo.cabecalho
[PASSOU] renderizar_tela nao altera corpo.elementos
[PASSOU] renderizar_tela nao altera barra_de_menus.chips
[PASSOU] saida nao vaza campos inertes (origem_dados/bindings/filtros/tela_destino/regra_existencia)
[PASSOU] saida nao expoe id interno de chip ('[chip_esc]')

== Alternancia de borda em memoria (H-0007) ==
[PASSOU] renderizar_tela(modelo, tipo_borda='curva') sem excecao
[PASSOU] renderizar_tela(modelo, tipo_borda='curva') == renderizar_tela(modelo)
[PASSOU] renderizar_tela(modelo, tipo_borda='reta') sem excecao
[PASSOU] saida reta e str - tipo=str
[PASSOU] saida reta contem '┌' (canto superior esquerdo reto)
[PASSOU] saida reta contem '┐' (canto superior direito reto)
[PASSOU] saida reta contem '└' (canto inferior esquerdo reto)
[PASSOU] saida reta contem '┘' (canto inferior direito reto)
[PASSOU] saida reta nao contem '╭' (canto curvo ausente)
[PASSOU] saida reta nao contem '╮' (canto curvo ausente)
[PASSOU] saida reta nao contem '╰' (canto curvo ausente)
[PASSOU] saida reta nao contem '╯' (canto curvo ausente)
[PASSOU] saida reta contem '│ Tela raiz do sistema' (conteudo preservado)
[PASSOU] saida reta contem 'Dashboard de teste' (conteudo preservado)
[PASSOU] saida reta contem '[B] Borda' (menu inerte preservado)
[PASSOU] cada linha da saida reta tem exatamente 42 chars Python
[PASSOU] saida reta bate com _EXPECTED_ORQUESTRADOR_RETA (igualdade estrita)
[PASSOU] trocar borda altera somente os quatro cantos
[PASSOU] linhas de conteudo (│ ...) sao identicas entre curva e reta
[PASSOU] renderizar_tela(modelo, tipo_borda='invalida') lanca RenderizadorErro - RenderizadorErro: tipo_borda invalido: 'invalida'; valores aceitos: curva, reta
[PASSOU] renderizar_tela(modelo, tipo_borda='CURVA') lanca RenderizadorErro (case sensitive) - RenderizadorErro: tipo_borda invalido: 'CURVA'; valores aceitos: curva, reta
[PASSOU] saida reta e deterministica (duas chamadas identicas)

== Resumo ==
Total de verificacoes: 58
Passaram: 58
Falharam: 0
```

Total: 58 verificações (36 do H-0006 preservadas + 22 novas do H-0007),
todas passando.

### Testes do diagnóstico (`tela/teste_diagnostico.py`)

Comando:

```bash
python tela/teste_diagnostico.py
```

Saída (resumo):

```text
== Resumo ==
Total de verificacoes: 26
Passaram: 26
Falharam: 0
```

Inclui verificação por subprocess de que `tela/teste_loader.py`,
`tela/teste_modelo.py` e `tela/teste_renderizador.py` retornam 0, e de
que `python tela/diagnostico.py` produz stdout idêntico a
`gerar_diagnostico_tela()` (saída curva/H-0006).

### Modo executável (`tela/diagnostico.py`)

Comando:

```bash
python tela/diagnostico.py
```

Saída (saída curva/H-0006, preservada):

```text
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

Código de saída: `0`.

### Saída real do pipeline — borda `"curva"` (default, idêntica ao H-0006)

```text
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

Reprodução literal da constante `_EXPECTED_ORQUESTRADOR` do
`tela/teste_renderizador.py`. Invariante confirmada por igualdade
estrita:

```text
renderizar_tela(modelo) == renderizar_tela(modelo, tipo_borda="curva")
```

### Saída real do pipeline — borda `"reta"`

```text
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

Reprodução literal da constante `_EXPECTED_ORQUESTRADOR_RETA`,
verificada por igualdade estrita. Cada linha visual tem exatamente 42
caracteres Python.

### Invariantes H-0001 e H-0002 preservados

- `tela/teste_loader.py`: 37/37 verificações passando.
- `tela/teste_modelo.py`: 30/30 verificações passando.

---

## Observações

### Comportamento fora de escopo preservado como inerte

Confirmado que os itens abaixo permanecem inertes / não implementados,
conforme handoff H-0007:

- `[B] Borda` é apenas texto inerte no menu — nenhum binding da tecla
  `B`, nenhuma captura de teclado, nenhum loop de aplicação.
- Nenhuma ação real, registry de ações ou registry de tipos criado.
- Nenhuma leitura de `config/estilo.json`,
  `config/barra_de_menus.json`, `config/layout_console.json` nem
  `config/lancador.json`.
- Nenhuma persistência de `tipo_borda` entre chamadas; a seleção de
  borda é estritamente local a cada invocação de `renderizar_tela`.
- Nenhum cálculo de largura de terminal, nenhum resize, nenhuma
  largura dinâmica.
- Nenhuma cor nem escape code ANSI.
- `renderizar_tela` não altera `modelo._raw`, `modelo.cabecalho`,
  `corpo.elementos` nem `barra_de_menus.chips`; não acessa
  `_campos_inertes`, `modelo.corpo.elementos`, `modelo.id` nem
  `modelo.schema` para composição da saída.
- Saída não vaza `origem_dados`, `bindings`, `filtros`, `tela_destino`,
  `regra_existencia`, `_campos_inertes` nem ids internos de chip
  (`[chip_esc]`, `[chip_ajuda]`).

### Nota sobre largura fixa (provisória)

As constantes `TOTAL_WIDTH = 42`, `INNER_WIDTH = 40` e
`CONTENT_WIDTH = 39` foram preservadas inalteradas a partir do H-0006,
como herança técnica provisória do estágio zero. Esta preservação **não
formaliza** a largura fixa como regra final de layout, **não declara**
que essas constantes cumprem o contrato final de composição de corpo,
**não autoriza** cálculo de largura real de terminal e **não autoriza**
leitura de `config/layout_console.json` nem `config/lancador.json`.
Questões de layout dinâmico, resize e layout por terminal pertencem a
ciclo próprio posterior (fora do H-0007).

### Commit

Commit não realizado — responsabilidade do engenheiro, conforme handoff.

---

## Resultado final

APROVADO
