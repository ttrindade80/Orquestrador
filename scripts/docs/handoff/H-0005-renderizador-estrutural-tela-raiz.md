---
name: H-0005-renderizador-estrutural-tela-raiz
description: Handoff de implementação do renderer estrutural mínimo da tela raiz — evolui renderizar_tela para saída com regiões nomeadas e componentes tipados, mantendo determinismo e auditabilidade
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0005
  data_criacao: 2026-07-07
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
  adr_relacionadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  handoffs_anteriores:
    - docs/handoff/H-0001-loader-validador-tela-json.md
    - docs/handoff/H-0002-modelo-interno-tela.md
    - docs/handoff/H-0003-renderizador-textual-estatico.md
    - docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md
  issues_relacionadas: []
---

# H-0005 — Renderer estrutural mínimo da tela raiz

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
3. `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
4. `docs/handoff/H-0001-loader-validador-tela-json.md`
5. `docs/handoff/H-0002-modelo-interno-tela.md`
6. `docs/handoff/H-0003-renderizador-textual-estatico.md`
7. `docs/handoff/H-0004-diagnostico-executavel-tela-raiz.md`
8. Este handoff

Se houver conflito entre este handoff e qualquer artefato acima, o executor
deve parar com `ARCHITECTURE_REVIEW_REQUIRED` e registrar a divergência. Este
handoff não pode criar regra nova que contradiga nenhum dos artefatos acima.

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

## Contexto herdado de H-0003 e H-0004

Os handoffs H-0001, H-0002, H-0003 e H-0004 foram implementados. O relatório
IMP-0004 registra status `APROVADO_COM_RESSALVAS` (ressalvas objetivas não
bloqueantes). O pacote `tela/` contém atualmente:

```
tela/__init__.py           — marcador de pacote (vazio)
tela/loader.py             — loader/validador macro (H-0001)
tela/teste_loader.py       — diagnóstico H-0001 (37 verificações, todas passando)
tela/modelo.py             — modelo interno normalizado (H-0002)
tela/teste_modelo.py       — diagnóstico H-0002 (30 verificações, todas passando)
tela/renderizador.py       — renderer textual estático (H-0003)
tela/teste_renderizador.py — diagnóstico H-0003 (39 verificações, todas passando)
tela/diagnostico.py        — ponto de entrada executável (H-0004)
tela/teste_diagnostico.py  — diagnóstico H-0004 (27 verificações, todas passando)
```

### Pipeline já estabelecido

```
config/telas/orquestrador.json
    → carregar_tela(None, "orquestrador")   [tela/loader.py      — H-0001]
    → dict (tela_raw)
    → construir_modelo(tela_raw)            [tela/modelo.py      — H-0002]
    → ModeloTela
    → renderizar_tela(modelo)               [tela/renderizador.py — H-0003 / H-0005]
    → str
```

### O que o H-0003 produzia

O renderer textual estático (H-0003) produzia a seguinte saída para
`orquestrador.json`:

```
TELA: orquestrador
SCHEMA: tela.v1

CABECALHO
  titulo: Orquestrador
  descricao: Tela raiz do sistema — ponto de entrada e visao consolidada do pipeline de survey

CORPO
  arranjo: sobreposto
  elementos:
    - id: console_principal | tipo: console
    - id: dashboard_info | tipo: dashboard
    - id: lancador_principal | tipo: lancador

BARRA_DE_MENUS
  chips:
    - id: chip_esc | texto: Sair
    - id: chip_paginas | texto: Páginas
    [...]
    - id: chip_ajuda | texto: Ajuda
```

Essa saída listava os elementos do corpo como itens planos de uma lista.
O H-0005 evolui esse formato para uma **representação estrutural** com regiões
nomeadas e componentes tipados, conforme descrito neste handoff.

### Pendências documentais que permanecem inertes

- **DOC-B008**: tipos internos de item de `console` não definidos.
- **DOC-B009**: registry completo de ações e tipos de chip não fechado.
- **`lancador_principal.itens`**: lista vazia; `tela_destino` pendente.
- **`bindings`** e **`referencias_de_acoes`**: declarados como pendentes.

O renderer não deve tratar essas pendências como erro. São declaração inerte
no modelo — o renderer as atravessa sem executar nada.

---

## Objetivo técnico

Evoluir `tela/renderizador.py` para que `renderizar_tela(modelo: ModeloTela)`
produza uma saída **estrutural mínima** da tela raiz, com:

1. Regiões nomeadas (`REGIAO: cabecalho`, `REGIAO: corpo`,
   `REGIAO: barra_de_menus`) em vez de rótulos planos.
2. Componentes do corpo listados com seu tipo em destaque, na forma
   `[{tipo}] {id}` (ex.: `[console] console_principal`), em vez da forma
   plana `- id: {id} | tipo: {tipo}`.
3. Chips da barra de menus listados na forma `[{id}] {texto}` em vez de
   `- id: {id} | texto: {texto}`.
4. Saída ainda determinística, auditável, sem dependência de terminal, sem
   execução de ação, sem ativação de binding, sem consulta direta a JSON.

A função principal continua sendo:

```python
renderizar_tela(modelo: ModeloTela) -> str
```

O renderer continua consumindo `ModeloTela`. Não pode ler JSON bruto
diretamente. Não pode executar ações, bindings, chips ou navegação.

---

## Escopo positivo

O H-0005 **autoriza e especifica**:

1. Alterar `tela/renderizador.py` para o novo formato estrutural.
2. Alterar `tela/teste_renderizador.py` para verificar o novo formato.
3. Alterar `tela/teste_diagnostico.py` para atualizar as verificações de
   formato que dependiam do formato H-0003 (justificativa abaixo).
4. Criar `docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md`.

### Justificativa objetiva para alterar `tela/teste_diagnostico.py`

O `tela/teste_diagnostico.py` contém verificações de formato do H-0003
(`"CABECALHO" in resultado`, `"CORPO" in resultado`, `"BARRA_DE_MENUS" in
resultado`, `"id: console_principal | tipo: console" in resultado`, etc.). O
H-0005 muda o formato do renderer — esses tokens deixam de aparecer na saída.
Sem atualização do arquivo, `python tela/teste_diagnostico.py` retornaria
código de saída 1 (verificações de formato falhando), violando o invariante
que exige código de saída 0. A atualização é objetivamente necessária para
manter o invariante. O `tela/diagnostico.py` em si **não precisa ser alterado**
— ele apenas encadeia o pipeline independente do formato da saída.

---

## Fora de escopo — proibições explícitas

O H-0005 **não implementa** nenhum dos itens abaixo. Implementar qualquer um
viola este handoff:

- loop de aplicação;
- navegação real entre telas;
- execução de ações declaradas em chips ou itens de lancador;
- registry de ações (`referencias_de_acoes`);
- resolução de `bindings`;
- ativação de filtros funcionais (`filtros[]`);
- paginação funcional;
- seleção funcional;
- registry de tipos de elemento;
- execução de chips;
- navegação por `tela_destino`;
- dashboard dinâmico com dados reais;
- mudança de estilo em runtime;
- carregamento ou aplicação de `config/estilo.json`;
- bordas, molduras ou qualquer primitiva de borda;
- cores ou escape codes ANSI;
- chips visuais finais com aparência definitiva;
- cálculo de largura de terminal ou layout responsivo;
- interface interativa;
- `curses`, `textual`, `rich` ou qualquer biblioteca de UI;
- renderer visual final;
- pop-up;
- tela de processamento;
- seleção de item por cursor;
- qualquer estado de runtime (cursor, página, filtro ativo, seleção, foco);
- leitura direta de `config/telas/orquestrador.json` pelo renderer;
- alteração de JSON em runtime.

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os arquivos abaixo, todos
relativos à raiz do repositório de scripts:

```
tela/renderizador.py                                          — ALTERAR (novo formato)
tela/teste_renderizador.py                                    — ALTERAR (verificações do novo formato)
tela/teste_diagnostico.py                                     — ALTERAR (atualizar verificações de formato)
docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md — CRIAR
```

A lista acima é exaustiva e sem exceção.

---

## Arquivos proibidos de alterar

O executor **não pode** criar, alterar, renomear, mover ou remover nenhum
arquivo fora dos listados em "Arquivos permitidos". São especificamente
proibidos:

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

Se a implementação exigir alterar qualquer arquivo fora do escopo aprovado,
o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

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
| Saída | `str` — representação estrutural estática, determinística, auditável |
| Efeitos colaterais | Nenhum — não altera o modelo, não grava arquivo, não consulta JSON, não executa ação, não ativa binding |
| Determinismo | Dado o mesmo `ModeloTela`, sempre retorna a mesma string |
| Independência de terminal | A saída não muda conforme a largura do terminal |

### Exceção para argumento inválido

`RenderizadorErro` deve continuar sendo lançada quando o argumento recebido
não for `ModeloTela` (ex.: `None`, `dict`, ou qualquer outro tipo). Em
operação normal com `ModeloTela` válido, não deve lançar exceção.

### Campos inertes — o renderer não pode acessar

O renderer **não pode** acessar, iterar ou usar nenhum campo de
`elemento._campos_inertes` de nenhum `ElementoCorpo`. A renderização dos
componentes do corpo usa exclusivamente `elemento.id` e `elemento.tipo`.

---

## Formato textual estrutural — especificação exata

O formato abaixo é **exato e obrigatório**. O implementador não pode escolher
outro formato sem aprovação explícita. Cada linha, cada espaço de indentação
e cada marcador fazem parte da especificação.

### Regras de formato

| Elemento | Regra |
|---|---|
| Linha 1 | `TELA: {modelo.id}` |
| Linha 2 | `SCHEMA: {modelo.schema}` |
| Separação entre blocos | Linha em branco entre identificação e regiões, e entre regiões |
| Cabeçalho de região | `REGIAO: {nome}` sem indentação; nome em minúsculas sem acentos (`cabecalho`, `corpo`, `barra_de_menus`) |
| Campos dentro de região | Indentação de 2 espaços |
| Rótulo de lista de componentes | `  componentes:` (2 espaços) |
| Rótulo de lista de chips | `  chips:` (2 espaços) |
| Item de componente | 4 espaços + `[{tipo}] {id}` |
| Item de chip | 4 espaços + `[{id}] {texto}` |
| `arranjo` ausente (`None`) | `  arranjo: (não declarado)` |
| `cabecalho.titulo` ausente | `  titulo: (ausente)` |
| `cabecalho.descricao` ausente | `  descricao: (ausente)` |
| `chip.texto` ausente | `    [{id}] (ausente)` |
| Ordem dos componentes | Segue `modelo.corpo.elementos` na ordem declarada |
| Ordem dos chips | Segue `modelo.barra_de_menus.get("chips", [])` na ordem declarada |
| Codificação | UTF-8; nenhum escape code de terminal |
| Terminador de linha | `\n` |
| Linha final | A string termina com `\n` após a última linha de conteúdo |

### Template

```
TELA: {modelo.id}
SCHEMA: {modelo.schema}

REGIAO: cabecalho
  titulo: {modelo.cabecalho.get("titulo", "(ausente)")}
  descricao: {modelo.cabecalho.get("descricao", "(ausente)")}

REGIAO: corpo
  arranjo: {modelo.corpo.arranjo ou "(não declarado)"}
  componentes:
    [{e.tipo}] {e.id}
    [um item por linha para cada e em modelo.corpo.elementos]

REGIAO: barra_de_menus
  chips:
    [{chip["id"]}] {chip.get("texto", "(ausente)")}
    [um item por linha para cada chip em modelo.barra_de_menus.get("chips", [])]
```

### Saída esperada para o estado atual de `config/telas/orquestrador.json`

A string abaixo é a saída **exata** esperada quando o pipeline completo é
executado sobre o `orquestrador.json` atual. O teste de regressão deve
comparar a saída real com este valor (igualdade estrita, incluindo o `\n`
final):

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
    [chip_colunas] Colunas
    [chip_grupos] Grupos
    [chip_alternar] Alternar
    [chip_navegar] Navegar
    [chip_selecionar] Selecionar
    [chip_enter] Todos
    [chip_estilo] Estilo
    [chip_verboso] Verboso
    [chip_ajuda] Ajuda
```

A string acima termina com `\n` após a linha `    [chip_ajuda] Ajuda`.

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
- `tela_destino` (qualquer valor, incluindo `"pendente"`)
- `origem_dados` (qualquer valor, incluindo `{"referencia": "pendente"}`)
- `regra_geracao_itens`
- `itens` vazios de `lancador_principal`
- quaisquer campos em `_campos_inertes` de cada `ElementoCorpo`

---

## Pré-condição obrigatória

Antes de alterar qualquer arquivo, o executor deve confirmar que os
invariantes dos quatro handoffs anteriores estão todos passando:

```bash
python tela/teste_loader.py    # todas as 37 verificações passando
python tela/teste_modelo.py    # todas as 30 verificações passando
python tela/teste_renderizador.py  # todas as 39 verificações passando (formato H-0003)
python tela/teste_diagnostico.py   # todas as 27 verificações passando
python tela/diagnostico.py         # imprime a tela e encerra com código 0
```

Se qualquer verificação falhar, o executor deve parar imediatamente com
`BLOCKED` e registrar qual verificação falhou e em qual módulo.

---

## Testes obrigatórios

### `tela/teste_renderizador.py` — atualizado para formato H-0005

#### Estrutura obrigatória do script

- Definir `sys.dont_write_bytecode = True` **antes** de qualquer import.
- Importar apenas da biblioteca padrão, de `tela.loader`, `tela.modelo` e
  `tela.renderizador`.
- Imprimir `[PASSOU] <nome>` ou `[FALHOU] <nome>` para cada verificação.
- Imprimir ao final: `Total de verificacoes`, `Passaram`, `Falharam`.
- Retornar código de saída 0 se todos passaram, 1 se algum falhou.
- Não usar `unittest`, `pytest` nem nenhum framework externo.

#### Verificações obrigatórias

| Verificação | Critério |
|---|---|
| `renderizar_tela` aceita `ModeloTela` válido sem exceção | Nenhuma exceção lançada para o modelo do orquestrador |
| Saída é `str` | `isinstance(saida, str) is True` |
| Saída começa com `"TELA: orquestrador"` | `saida.startswith("TELA: orquestrador")` |
| Saída contém `"SCHEMA: tela.v1"` | String presente na saída |
| Saída contém `"REGIAO: cabecalho"` | String presente na saída |
| Saída contém `"titulo: Orquestrador"` | String presente na saída |
| Saída contém `"descricao:"` | String presente na saída |
| Saída contém `"REGIAO: corpo"` | String presente na saída |
| Saída contém `"arranjo: sobreposto"` | String presente na saída |
| Saída contém `"[console] console_principal"` | String presente na saída |
| Saída contém `"[dashboard] dashboard_info"` | String presente na saída |
| Saída contém `"[lancador] lancador_principal"` | String presente na saída |
| Saída contém `"REGIAO: barra_de_menus"` | String presente na saída |
| Saída contém `"[chip_esc]"` | String presente na saída |
| Saída contém `"[chip_ajuda]"` | String presente na saída |
| Saída é determinística | Duas chamadas com o mesmo modelo produzem saída idêntica |
| Saída com modelo fabricado usa dados do modelo, não do JSON | `ModeloTela(id="teste_fabricado", ...)` → saída começa com `"TELA: teste_fabricado"` |
| `renderizar_tela(None)` lança `RenderizadorErro` | Exceção do tipo correto |

#### Verificação com modelo fabricado

O teste deve construir um `ModeloTela` fabricado com `id="teste_fabricado"` e
verificar que a saída usa os dados do modelo, não do JSON em disco:

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
# verificar: saida_fab.startswith("TELA: teste_fabricado")
# verificar: "SCHEMA: tela.v0" in saida_fab
# verificar: "arranjo: linear" in saida_fab
# verificar: "[console] e1" in saida_fab
# verificar: "[c1] Ok" in saida_fab
# verificar: "orquestrador" not in saida_fab
```

### `tela/teste_diagnostico.py` — verificações de formato atualizadas

O `tela/teste_diagnostico.py` deve ser atualizado para substituir as
verificações de formato do H-0003 pelos equivalentes do H-0005. A estrutura
do script (pré-condição via subprocess, resumo, código de saída) deve ser
preservada.

Verificações de formato que devem ser **substituídas** (H-0003 → H-0005):

| Verificação antiga (H-0003) | Nova verificação (H-0005) |
|---|---|
| `"CABECALHO" in resultado` | `"REGIAO: cabecalho" in resultado` |
| `"CORPO" in resultado` | `"REGIAO: corpo" in resultado` |
| `"BARRA_DE_MENUS" in resultado` | `"REGIAO: barra_de_menus" in resultado` |
| `"id: console_principal \| tipo: console" in resultado` | `"[console] console_principal" in resultado` |
| `"id: dashboard_info \| tipo: dashboard" in resultado` | `"[dashboard] dashboard_info" in resultado` |
| `"id: lancador_principal \| tipo: lancador" in resultado` | `"[lancador] lancador_principal" in resultado` |
| `"id: chip_esc" in resultado` | `"[chip_esc]" in resultado` |
| `"id: chip_ajuda" in resultado` | `"[chip_ajuda]" in resultado` |

A constante `_EXPECTED_ORQUESTRADOR` deve ser atualizada para o novo formato
H-0005 (saída exata definida neste handoff, seção "Saída esperada").

Verificações que **permanecem** (não são afetadas pela mudança de formato):

- `gerar_diagnostico_tela()` não lança exceção.
- Retorno é `str`.
- Resultado começa com `"TELA: orquestrador"`.
- Resultado contém `"SCHEMA: tela.v1"`.
- Resultado contém `"titulo: Orquestrador"`.
- Resultado contém `"arranjo: sobreposto"`.
- Resultado é determinístico (duas chamadas idênticas).
- Resultado bate com saída esperada (igualdade estrita com `_EXPECTED_ORQUESTRADOR` atualizado).
- Campos inertes não vazam na saída.
- `gerar_diagnostico_tela("orquestrador") == gerar_diagnostico_tela()`.
- Modo executável encerra com código 0.
- `python tela/diagnostico.py` stdout == `gerar_diagnostico_tela()`.
- Proibições de importação em `tela/diagnostico.py`.
- Invariantes H-0001, H-0002, H-0003 e H-0005 preservados via subprocess.

O executor deve atualizar a linha de pré-condição do H-0003 para também
verificar que `tela/teste_renderizador.py` passa com o novo formato:

```python
for rotulo, script in (
    ("H-0001", "tela/teste_loader.py"),
    ("H-0002", "tela/teste_modelo.py"),
    ("H-0005", "tela/teste_renderizador.py"),   # era H-0003; formato atualizado
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
- [ ] `renderizar_tela` não importa `json`, `os`, `pathlib` para abertura de
      arquivo, nem chama `carregar_tela`.
- [ ] `renderizar_tela` não executa ação, não ativa binding, não altera estado,
      não grava arquivo, não chama subprocess nem eval.
- [ ] `renderizar_tela` não acessa `_campos_inertes` de nenhum `ElementoCorpo`.
- [ ] `renderizar_tela(None)` lança `RenderizadorErro`.

### Formato da saída

- [ ] A saída começa com `TELA: orquestrador`.
- [ ] A segunda linha é `SCHEMA: tela.v1`.
- [ ] A saída contém `REGIAO: cabecalho` com `titulo` e `descricao`.
- [ ] A saída contém `REGIAO: corpo` com `arranjo` e lista `componentes:`.
- [ ] Cada componente aparece como `    [{tipo}] {id}`.
- [ ] A saída contém `REGIAO: barra_de_menus` com lista `chips:`.
- [ ] Cada chip aparece como `    [{id}] {texto}`.
- [ ] Chamadas repetidas com o mesmo modelo produzem saída idêntica.
- [ ] Saída com modelo fabricado `id="teste_fabricado"` começa com
      `TELA: teste_fabricado` (renderer usa dados do modelo, não do JSON).
- [ ] Saída bate com o expected output literal definido neste handoff
      (igualdade estrita, incluindo `\n` final).

### Invariantes preservados

- [ ] `python tela/teste_loader.py` retorna código de saída 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna código de saída 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna código de saída 0 (com as
      verificações atualizadas para formato H-0005).
- [ ] `python tela/teste_diagnostico.py` retorna código de saída 0 (com as
      verificações de formato atualizadas).
- [ ] `python tela/diagnostico.py` imprime a saída no formato H-0005 e
      encerra com código 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` é JSON válido e não foi alterado.
- [ ] `config/estilo.json` é JSON válido e não foi alterado.
- [ ] Nenhum JSON alterado em runtime.
- [ ] Nenhuma ação executada.
- [ ] Nenhum binding ativado.
- [ ] Nenhum chip executado.
- [ ] Nenhum estado gravado.
- [ ] Saída determinística (independente de largura de terminal).
- [ ] Sem dependência de biblioteca de UI (`curses`, `textual`, `rich`, etc.).

### Campos inertes na saída

- [ ] A saída não contém `origem_dados`.
- [ ] A saída não contém `bindings`.
- [ ] A saída não contém `filtros`.
- [ ] A saída não contém `tela_destino`.
- [ ] A saída não contém `regra_existencia`.
- [ ] A saída não contém `_campos_inertes`.

### Relatório

- [ ] `docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md` criado
      com resultado `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Testes — comandos de verificação obrigatórios

Executar a partir do diretório raiz do repositório de scripts:

```bash
# 1. Integridade dos JSONs de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"

# 2. Invariantes de H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes de H-0002 preservados
python tela/teste_modelo.py

# 4. Testes do H-0005 (renderer estrutural)
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

Todos os comandos devem produzir saída limpa. O relatório deve incluir a
saída real de cada um.

---

## Condições de bloqueio

O executor deve parar imediatamente com `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se:

1. Qualquer verificação de H-0001 (`python tela/teste_loader.py`) falhar.
2. Qualquer verificação de H-0002 (`python tela/teste_modelo.py`) falhar.
3. Qualquer verificação de H-0003 (antes da alteração de
   `tela/teste_renderizador.py`) falhar.
4. Qualquer verificação de H-0004 (`python tela/teste_diagnostico.py` com
   formato ainda H-0003) falhar.
5. A implementação exigir criar arquivo fora dos listados em "Arquivos
   permitidos".
6. A implementação exigir alterar contrato, ADR, nomenclatura, índice,
   configuração, backlog, issues, handoff anterior ou relatório anterior.
7. A implementação exigir dependência externa além da stdlib Python.
8. A implementação exigir calcular largura real do terminal.
9. A implementação exigir executar ação, resolver `tela_destino`, ativar
   binding, aplicar filtro, navegar, paginar ou selecionar.
10. A implementação exigir carregar ou aplicar `config/estilo.json`.
11. A implementação exigir bordas, cores ou escape codes ANSI.
12. A implementação exigir acessar `_campos_inertes` de qualquer
    `ElementoCorpo`.
13. A implementação exigir tomar decisão arquitetural não coberta por este
    handoff.
14. A saída do renderer divergir do expected output literal definido neste
    handoff por razão não prevista aqui.

---

## Formato esperado do relatório `IMP-0005`

O executor deve criar:

```
docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md
```

O relatório deve conter obrigatoriamente:

1. **Objetivo do H-0005**: o que foi especificado e o que foi implementado.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo à
   raiz do repositório.
3. **Assinatura da função e módulos importados**: assinatura exata de
   `renderizar_tela` e quais módulos são importados em `tela/renderizador.py`.
4. **Saída real do pipeline** para `orquestrador.json`: reprodução literal do
   `str` retornado por `renderizar_tela(construir_modelo(carregar_tela(...)))`.
5. **Invariantes de H-0001 e H-0002**: evidência de que as 37 e 30
   verificações respectivas continuam passando (saída dos comandos).
6. **Resultado dos testes do H-0005**: saída completa de
   `python tela/teste_renderizador.py`.
7. **Resultado dos testes do diagnóstico atualizados**: saída completa de
   `python tela/teste_diagnostico.py`.
8. **Resultado do modo executável**: saída de `python tela/diagnostico.py`.
9. **Comportamento fora de escopo preservado como inerte**: lista dos itens
   não implementados e por quê cada um foi mantido inerte.
10. **Pendências preservadas**: confirmação de que DOC-B008, DOC-B009 e
    campos `pendente` continuam sem execução.
11. **Saída real de todos os comandos de verificação**: cópia integral.
12. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Checklist final para QA

- [ ] H-0005 lido integralmente antes de qualquer alteração.
- [ ] Pré-condições verificadas (todos os testes anteriores passando).
- [ ] Somente os arquivos autorizados foram criados ou alterados.
- [ ] `git diff --stat` não mostra alterações em arquivos fora do escopo.
- [ ] Nenhum contrato, ADR ou documento normativo alterado.
- [ ] Formato da saída bate com o expected output literal (igualdade estrita).
- [ ] Saída com modelo fabricado usa dados do modelo, não do JSON em disco.
- [ ] `renderizar_tela(None)` lança `RenderizadorErro`.
- [ ] `renderizar_tela` não acessa `_campos_inertes`.
- [ ] `renderizar_tela` não importa `json`, `os`, `pathlib`, nem `carregar_tela`.
- [ ] `python tela/teste_loader.py` retorna 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna 0 (formato H-0005).
- [ ] `python tela/teste_diagnostico.py` retorna 0 (verificações atualizadas).
- [ ] `python tela/diagnostico.py` imprime saída H-0005 e encerra com 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` válido e inalterado.
- [ ] `config/estilo.json` válido e inalterado.
- [ ] Saída não contém campos inertes (`origem_dados`, `bindings`, `filtros`,
      `tela_destino`, `regra_existencia`, `_campos_inertes`).
- [ ] `docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md` criado
      com resultado final documentado.
- [ ] Commit não realizado (responsabilidade do engenheiro).
