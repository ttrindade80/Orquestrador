---
name: H-0003-renderizador-textual-estatico
description: Handoff de implementação do renderer textual estático mínimo — consome ModeloTela e produz string auditável determinística
metadata:
  type: handoff_implementacao
  status: READY_FOR_AUDIT
  id: H-0003
  data_criacao: 2026-07-07
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_estilo.md
  adr_relacionadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  handoffs_anteriores:
    - docs/handoff/H-0001-loader-validador-tela-json.md
    - docs/handoff/H-0002-modelo-interno-tela.md
  issues_relacionadas: []
---

# H-0003 — Renderer textual estático mínimo da tela raiz

## Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`
2. `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
3. `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
4. `docs/contratos/contrato_tela_json.md`
5. `docs/contratos/contrato_composicao_corpo.md`
6. `docs/contratos/contrato_lancador.md`
7. `docs/contratos/contrato_console.md`
8. `docs/contratos/contrato_chip.md`
9. `docs/contratos/contrato_barra_de_menus.md`
10. `docs/contratos/contrato_estilo.md`
11. `docs/handoff/H-0001-loader-validador-tela-json.md`
12. `docs/handoff/H-0002-modelo-interno-tela.md`
13. Este handoff

Se houver conflito entre este handoff e qualquer artefato acima, o executor
deve parar com `ARCHITECTURE_REVIEW_REQUIRED` e registrar a divergência. Este
handoff não pode criar regra nova que contradiga nenhum dos artefatos acima.

---

## Contexto

O H-0001 implementou o loader/validador macro de `tela.json` (`tela/loader.py`,
`tela/teste_loader.py`). O H-0002 implementou o modelo interno normalizado
(`tela/modelo.py`, `tela/teste_modelo.py`). Ambos estão aprovados por QA (ver
`docs/relatorios/IMP-0001-loader-validador-tela-json.md`,
`docs/relatorios/IMP-0002-modelo-interno-tela.md` e
`docs/relatorios/RELATORIO_QA_H-0002_MODELO_INTERNO_TELA.md`).

O pacote `tela/` contém atualmente:

```
tela/__init__.py         — marcador de pacote (vazio)
tela/loader.py           — loader/validador macro (H-0001)
tela/teste_loader.py     — diagnóstico H-0001 (37 verificações, todas passando)
tela/modelo.py           — modelo interno normalizado (H-0002)
tela/teste_modelo.py     — diagnóstico H-0002 (30 verificações, todas passando)
```

O H-0003 especifica o **primeiro renderer textual estático mínimo** da tela
raiz do Orquestrador. O renderer consome o `ModeloTela` produzido pelo H-0002 e
gera uma string textual auditável, determinística e testável. Não renderiza
interface visual completa, não calcula layout de terminal, não executa ações e
não ativa bindings.

### Pipeline completo após H-0003

```
config/telas/orquestrador.json
    → carregar_tela(base, "orquestrador")    [tela/loader.py   — H-0001]
    → construir_modelo(tela_raw)             [tela/modelo.py   — H-0002]
    → ModeloTela
    → renderizar_tela(modelo)               [tela/renderizador.py — H-0003]
    → str
```

O renderer **recebe `ModeloTela`**. Nunca acessa `config/telas/orquestrador.json`
diretamente, nunca chama `carregar_tela` e nunca importa `json`, `os` ou
`pathlib` para leitura de arquivo. O `_raw` de `ModeloTela` pode ser consultado
opcionalmente para diagnóstico interno, mas a renderização principal deve operar
sobre os campos estruturados (`modelo.id`, `modelo.schema`, `modelo.cabecalho`,
`modelo.corpo`, `modelo.barra_de_menus`).

### Pendências documentais que permanecem ativas e inertes no H-0003

- **DOC-B008**: tipos internos de item de `console` não definidos; `origem_dados`
  e `regra_geracao_itens` do `console_principal` marcados como `pendente`.
- **DOC-B009**: registry completo de ações e tipos de chip não fechado; ações
  dos chips são referências declarativas provisórias.
- **`lancador_principal.itens`**: lista vazia; `tela_destino` pendente.
- **`bindings`** e **`referencias_de_acoes`**: declarados como pendentes.

O renderer não deve tratar essas pendências como erro. São declaração inerte no
modelo — o renderer as preserva e as lista como dados estáticos sem executar
nada.

---

## Objetivo

Implementar uma função `renderizar_tela(modelo: ModeloTela) -> str` que:

1. Receba um `ModeloTela` produzido pelo pipeline H-0001 + H-0002.
2. Gere uma string textual que identifique a tela (`id` e `schema`).
3. Inclua uma seção `CABEÇALHO` com `titulo` e `descricao`.
4. Inclua uma seção `CORPO` com `arranjo` e lista de elementos, cada elemento
   com `id` e `tipo`.
5. Inclua uma seção `BARRA_DE_MENUS` com lista de chips, cada chip com `id`
   e `texto`.
6. Preserve campos inertes sem executá-los.
7. Produza saída determinística, testável e auditável.
8. Não dependa da largura real do terminal.
9. Não execute ação, não ative binding, não altere estado, não consulte JSON
   diretamente e não grave arquivo.

---

## Pré-condição obrigatória

Antes de criar qualquer arquivo, o executor deve confirmar que os invariantes de
H-0001 e H-0002 estão todos passando:

```bash
python tela/teste_loader.py    # todas as 37 verificações passando
python tela/teste_modelo.py    # todas as 30 verificações passando
```

Se qualquer verificação falhar, o executor deve parar imediatamente com
`BLOCKED` e registrar qual verificação falhou e em qual módulo.

---

## Arquivos permitidos

O executor pode criar ou alterar **somente** os arquivos abaixo, todos
relativos à raiz do repositório de scripts:

```
tela/renderizador.py                                            — módulo do renderer (CRIAR)
tela/teste_renderizador.py                                      — diagnóstico verificável (CRIAR)
docs/relatorios/IMP-0003-renderizador-textual-estatico.md      — relatório (CRIAR)
```

`tela/__init__.py` pode ser alterado somente se houver justificativa explícita e
mínima (ex.: reexportação conveniente de `renderizar_tela`). Se não for
estritamente necessário, preferir não alterar.

Os seguintes arquivos podem ser **lidos** mas **nunca alterados**:

```
tela/loader.py
tela/modelo.py
tela/teste_loader.py
tela/teste_modelo.py
config/telas/orquestrador.json
config/estilo.json
```

---

## Arquivos proibidos

O executor **não pode** criar, alterar, renomear, mover ou remover nenhum
arquivo fora dos listados em "Arquivos permitidos". São especificamente
proibidos:

```
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/contratos/          (qualquer arquivo)
docs/adr/                (qualquer arquivo)
docs/handoff/            (qualquer arquivo)
docs/templates/          (qualquer arquivo)
config/                  (qualquer arquivo)
tela/loader.py
tela/modelo.py
tela/teste_loader.py
tela/teste_modelo.py
```

Se a implementação exigir alterar qualquer contrato, ADR, nomenclatura, índice,
configuração, handoff anterior, relatório anterior ou qualquer decisão
documental, o executor deve parar com:

```
ARCHITECTURE_REVIEW_REQUIRED
```

e descrever objetivamente o que falta para desbloquear.

---

## Fora de escopo — proibições explícitas

O H-0003 **não implementa** nenhum dos itens abaixo. Implementar qualquer um
viola este handoff:

- navegação real entre telas;
- execução de ações declaradas em chips ou em itens de lancador;
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
- layout final responsivo completo;
- cálculo de bordas, colunas ou truncamento dependente da largura do terminal;
- renderização com escape codes ANSI ou cores de terminal;
- leitura direta de `config/telas/orquestrador.json` pelo renderer;
- alteração de JSON em runtime;
- qualquer estado de runtime (cursor, página, filtro ativo, seleção, foco).

---

## API de renderização

### Assinatura

```python
renderizar_tela(modelo: ModeloTela) -> str
```

### Módulo

`tela/renderizador.py`

### Importação obrigatória no módulo do renderer

```python
from tela.modelo import ModeloTela
```

Importações proibidas no módulo `tela/renderizador.py`:

- `import json`
- `import os`
- `import pathlib`
- `from tela.loader import carregar_tela`
- `subprocess`, `exec`, `eval` ou qualquer mecanismo de execução de processo

### Contrato da função

| Aspecto | Regra |
|---|---|
| Entrada | `ModeloTela` — objeto produzido por `construir_modelo` (H-0002) |
| Saída | `str` — representação textual estática, determinística, auditável |
| Efeitos colaterais | Nenhum — não altera o modelo, não grava arquivo, não consulta JSON, não executa ação, não ativa binding |
| Determinismo | Dado o mesmo `ModeloTela`, sempre retorna a mesma string |
| Independência de terminal | A saída não muda conforme a largura do terminal |

### Exceção para argumento inválido

O renderer deve lançar `RenderizadorErro` (definida em `tela/renderizador.py`)
quando receber argumento inválido (ex.: `None` ou objeto que não seja
`ModeloTela`). Em operação normal com `ModeloTela` válido, não deve lançar
exceção.

```python
class RenderizadorErro(Exception):
    """Erro de renderização textual de tela."""
```

---

## Formato textual determinístico

O formato abaixo é **exato e obrigatório**. O implementador não pode escolher
outro formato sem aprovação explícita. Cada linha, cada espaço de indentação e
cada separador são parte da especificação.

### Regras de formato

| Elemento | Regra |
|---|---|
| Linha 1 | `TELA: {modelo.id}` |
| Linha 2 | `SCHEMA: {modelo.schema}` |
| Separação entre blocos | Linha em branco entre identificação e seções, e entre seções |
| Cabeçalho de seção | Nome em maiúsculas, sem indentação (`CABEÇALHO`, `CORPO`, `BARRA_DE_MENUS`) |
| Campos dentro de seção | Indentação de 2 espaços |
| Rótulo de lista | `  chips:` ou `  elementos:` (2 espaços) |
| Item de lista | 4 espaços + `- ` |
| Separador dentro de item | ` \| ` (espaço, barra vertical, espaço) |
| `arranjo` ausente (`None`) | `  arranjo: (não declarado)` |
| `cabecalho.titulo` ausente | `  titulo: (ausente)` |
| `cabecalho.descricao` ausente | `  descricao: (ausente)` |
| `chip.texto` ausente | `texto: (ausente)` |
| Ordem dos elementos | Segue `modelo.corpo.elementos` na ordem declarada |
| Ordem dos chips | Segue `modelo.barra_de_menus.get("chips", [])` na ordem declarada |
| Codificação | UTF-8; nenhum escape code de terminal |
| Terminador de linha | `\n` |
| Linha final | A string termina com `\n` após a última linha de conteúdo |

### Template

```
TELA: {modelo.id}
SCHEMA: {modelo.schema}

CABEÇALHO
  titulo: {modelo.cabecalho.get("titulo", "(ausente)")}
  descricao: {modelo.cabecalho.get("descricao", "(ausente)")}

CORPO
  arranjo: {modelo.corpo.arranjo ou "(não declarado)"}
  elementos:
    - id: {e.id} | tipo: {e.tipo}
    [um item por linha para cada e em modelo.corpo.elementos]

BARRA_DE_MENUS
  chips:
    - id: {chip["id"]} | texto: {chip.get("texto", "(ausente)")}
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

CABEÇALHO
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
    - id: chip_colunas | texto: Colunas
    - id: chip_grupos | texto: Grupos
    - id: chip_alternar | texto: Alternar
    - id: chip_navegar | texto: Navegar
    - id: chip_selecionar | texto: Selecionar
    - id: chip_enter | texto: Todos
    - id: chip_estilo | texto: Estilo
    - id: chip_verboso | texto: Verboso
    - id: chip_ajuda | texto: Ajuda
```

A string acima termina com `\n` após a linha `    - id: chip_ajuda | texto: Ajuda`.

---

## Campos pendentes e inertes

Os seguintes campos, presentes em `modelo._raw` ou em `_campos_inertes` dos
elementos, permanecem **inertes** — o renderer não pode executar, resolver,
ativar nem atribuir semântica nova a eles:

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

## Invariantes herdados de H-0001 e H-0002

O H-0003 não pode enfraquecer nenhum invariante do H-0001 nem do H-0002. Devem
continuar válidos após a implementação:

- `python tela/teste_loader.py` retorna código de saída 0 com todas as 37
  verificações passando;
- `python tela/teste_modelo.py` retorna código de saída 0 com todas as 30
  verificações passando;
- JSON inválido continua gerando `TelaJsonInvalido` no loader;
- tipo fora de `{console, lancador, dashboard}` continua rejeitado com
  `TelaTipoDesconhecido` no loader;
- `ModeloTela` continua construído exclusivamente a partir do dict do loader;
- campos inertes continuam preservados sem execução;
- nenhuma ação real é executada;
- nenhum binding é ativado;
- nenhum estado de runtime é gravado no JSON;
- `config/telas/orquestrador.json` não é alterado;
- `config/estilo.json` não é alterado;
- nenhum `__pycache__` nem `.pyc` deve permanecer em `tela/` após os testes.

---

## Testes esperados

### Execução

```bash
python tela/teste_renderizador.py
```

### Estrutura obrigatória do script

- Definir `sys.dont_write_bytecode = True` **antes** de qualquer import.
- Importar apenas da biblioteca padrão, de `tela.loader`, `tela.modelo` e
  `tela.renderizador`.
- Imprimir `[PASSOU] <nome>` ou `[FALHOU] <nome>` para cada verificação.
- Imprimir ao final: `Total de verificacoes`, `Passaram`, `Falharam`.
- Retornar código de saída 0 se todos passaram, 1 se algum falhou.
- Não usar `unittest`, `pytest` nem nenhum framework externo.

### Verificações obrigatórias

| Verificação | Critério |
|---|---|
| `renderizar_tela` aceita `ModeloTela` válido sem exceção | Nenhuma exceção lançada para o modelo do orquestrador |
| Saída é `str` | `isinstance(saida, str) is True` |
| Saída começa com `"TELA: orquestrador"` | `saida.startswith("TELA: orquestrador")` |
| Saída contém `"SCHEMA: tela.v1"` | String presente na saída |
| Saída contém `"CABEÇALHO"` | String presente na saída |
| Saída contém `"titulo: Orquestrador"` | String presente na saída |
| Saída contém `"descricao:"` | String presente na saída |
| Saída contém `"CORPO"` | String presente na saída |
| Saída contém `"arranjo: sobreposto"` | String presente na saída |
| Saída contém `"id: console_principal \| tipo: console"` | String presente na saída |
| Saída contém `"id: dashboard_info \| tipo: dashboard"` | String presente na saída |
| Saída contém `"id: lancador_principal \| tipo: lancador"` | String presente na saída |
| Saída contém `"BARRA_DE_MENUS"` | String presente na saída |
| Saída contém `"id: chip_esc"` | String presente na saída |
| Saída contém `"id: chip_ajuda"` | String presente na saída |
| Saída é determinística | Duas chamadas com o mesmo modelo produzem saída idêntica |
| Saída usando modelo fabricado usa dados do modelo, não do JSON | Criar `ModeloTela` com `id="teste_fabricado"`, verificar que a saída começa com `"TELA: teste_fabricado"` |
| `renderizar_tela(None)` lança `RenderizadorErro` | Exceção do tipo correto |

### Verificação com modelo fabricado (anti-regressão de acesso direto ao JSON)

O teste deve construir um `ModeloTela` fabricado manualmente (usando as
dataclasses importadas de `tela.modelo`) com `id="teste_fabricado"` e verificar
que a saída começa com `TELA: teste_fabricado` — provando que o renderer usa os
dados do modelo, não do JSON em disco.

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
```

---

## Verificações obrigatórias da implementação

Executar a partir do diretório raiz do repositório de scripts, nesta ordem:

```bash
# 1. Integridade dos JSONs de configuração
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"

# 2. Invariantes de H-0001 preservados
python tela/teste_loader.py

# 3. Invariantes de H-0002 preservados
python tela/teste_modelo.py

# 4. Testes do H-0003
python tela/teste_renderizador.py

# 5. Verificação de bytecode
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print

# 6. Estado do repositório
git status --short
git diff --stat
```

Todos os comandos devem produzir saída limpa. O relatório deve incluir a saída
real de cada um.

---

## Relatório de implementação obrigatório

O executor deve criar:

```
docs/relatorios/IMP-0003-renderizador-textual-estatico.md
```

O relatório deve conter:

1. **Objetivo do H-0003**: o que foi especificado e o que foi implementado.
2. **Arquivos criados ou alterados**: lista completa com caminho relativo à
   raiz do repositório.
3. **Assinatura da função e módulos importados**: assinatura exata de
   `renderizar_tela`, quais módulos são importados em `tela/renderizador.py`.
4. **Saída real do pipeline** para `orquestrador.json`: reprodução literal do
   `str` retornado por `renderizar_tela(construir_modelo(carregar_tela(...)))`.
5. **Invariantes de H-0001 e H-0002**: evidência de que as 37 verificações do
   loader e as 30 do modelo continuam passando (saída dos comandos).
6. **Comportamento fora de escopo preservado como inerte**: lista dos itens não
   implementados e por quê cada um foi mantido inerte.
7. **Pendências preservadas**: confirmação de que DOC-B008, DOC-B009 e campos
   `pendente` continuam sem execução.
8. **Saída real de todos os comandos de verificação**: cópia integral.
9. **Resultado final**: `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Critérios de aceite do H-0003

O H-0003 é considerado concluído somente quando todos os critérios abaixo
forem verificáveis:

### Escopo e arquivos

- [ ] Somente `tela/renderizador.py`, `tela/teste_renderizador.py` e
      `docs/relatorios/IMP-0003-renderizador-textual-estatico.md` foram
      criados (mais `tela/__init__.py` opcionalmente).
- [ ] Nenhum arquivo fora do escopo autorizado foi criado ou alterado.
- [ ] Nenhum contrato, ADR, nomenclatura, índice, handoff anterior, relatório
      anterior, `config/*.json`, `docs/INDICE.md`, `docs/backlog.md` ou
      `docs/issues.md` foi alterado.

### API e renderer

- [ ] `tela/renderizador.py` define `renderizar_tela(modelo: ModeloTela) -> str`.
- [ ] `tela/renderizador.py` define `RenderizadorErro(Exception)`.
- [ ] `renderizar_tela` não importa `json`, `os`, `pathlib` para abertura de
      arquivo, nem chama `carregar_tela`.
- [ ] `renderizar_tela` não executa ação, não ativa binding, não altera estado,
      não grava arquivo, não chama subprocess nem eval.
- [ ] `renderizar_tela(None)` lança `RenderizadorErro`.

### Formato da saída

- [ ] A saída começa com `TELA: orquestrador`.
- [ ] A segunda linha é `SCHEMA: tela.v1`.
- [ ] A saída contém `CABEÇALHO` com `titulo` e `descricao`.
- [ ] A saída contém `CORPO` com `arranjo` e lista de elementos.
- [ ] Cada elemento aparece como `    - id: {id} | tipo: {tipo}`.
- [ ] A saída contém `BARRA_DE_MENUS` com lista de chips.
- [ ] Cada chip aparece como `    - id: {id} | texto: {texto}`.
- [ ] Chamadas repetidas com o mesmo modelo produzem saída idêntica.
- [ ] Modelo fabricado com `id="teste_fabricado"` produz saída começando com
      `TELA: teste_fabricado` (renderer usa dados do modelo, não do JSON).

### Invariantes preservados

- [ ] `python tela/teste_loader.py` retorna código de saída 0 (37 verificações).
- [ ] `python tela/teste_modelo.py` retorna código de saída 0 (30 verificações).
- [ ] `python tela/teste_renderizador.py` retorna código de saída 0.
- [ ] Nenhum `__pycache__` nem `.pyc` em `tela/` após os testes.
- [ ] `config/telas/orquestrador.json` é JSON válido e não foi alterado.
- [ ] `config/estilo.json` é JSON válido e não foi alterado.

### Relatório

- [ ] `docs/relatorios/IMP-0003-renderizador-textual-estatico.md` criado com
      resultado `APROVADO`, `APROVADO_COM_RESSALVAS` ou `BLOQUEADO`.

---

## Condições de bloqueio

O executor deve parar imediatamente com `BLOCKED` ou
`ARCHITECTURE_REVIEW_REQUIRED` se:

1. Qualquer verificação de H-0001 (`python tela/teste_loader.py`) falhar.
2. Qualquer verificação de H-0002 (`python tela/teste_modelo.py`) falhar.
3. A implementação exigir criar arquivo fora dos listados em "Arquivos
   permitidos".
4. A implementação exigir alterar contrato, ADR, nomenclatura, índice,
   configuração, backlog, issues, handoff anterior ou relatório anterior.
5. A implementação exigir dependência externa além da stdlib Python.
6. A implementação exigir calcular largura real do terminal.
7. A implementação exigir executar ação, resolver `tela_destino`, ativar
   binding, aplicar filtro, navegar, paginar ou selecionar.
8. A implementação exigir tomar decisão arquitetural não coberta por este
   handoff.
9. O formato textual exigir informação não disponível em `ModeloTela` sem
   acessar JSON diretamente.

---

## Instrução explícita ao executor

**Parar imediatamente com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`** se
qualquer condição de bloqueio for atingida.

**Não preencher lacunas** de especificação com decisão local.

**Não fazer commit** do resultado — o commit é responsabilidade do engenheiro.

**Não alterar** nenhum arquivo fora do escopo aprovado.

**Não implementar** nenhum item listado em "Fora de escopo".
