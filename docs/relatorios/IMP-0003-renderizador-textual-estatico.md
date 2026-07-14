# IMP-0003 — Renderer textual estático mínimo da tela raiz

## 1. Objetivo do H-0003

Implementar o primeiro renderer textual estático mínimo da tela raiz do
Orquestrador, conforme `docs/handoff/H-0003-renderizador-textual-estatico.md`
(auditoria `APPROVED_WITH_NOTES`, 0 achados bloqueantes, 1 observação não
bloqueante).

O renderer consome o `ModeloTela` produzido pelo pipeline H-0001 + H-0002:

```
config/telas/orquestrador.json
    → carregar_tela(...)        [tela/loader.py   — H-0001]
    → construir_modelo(...)     [tela/modelo.py   — H-0002]
    → ModeloTela
    → renderizar_tela(modelo)  [tela/renderizador.py — H-0003]
    → str
```

A função `renderizar_tela(modelo: ModeloTela) -> str` gera uma string
textual determinística, auditável, sem dependência de terminal, sem
execução de ação, sem ativação de binding, sem consulta direta a JSON em
disco e sem alteração de estado. Campos pendentes (DOC-B008 / DOC-B009)
permanecem inertes.

## 2. Status inicial do Git

Capturado antes de qualquer alteração, com os artefatos do ciclo H-0003
já presentes como não rastreados:

```
$ git status --short
?? docs/handoff/H-0003-renderizador-textual-estatico.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0003_HANDOFF.md

$ git diff --stat
(vazio)
```

Os dois arquivos acima são pré-existentes ao início da implementação e
**não foram alterados**.

## 3. Arquivos criados ou alterados

Criados:

- `tela/renderizador.py` — módulo do renderer (`renderizar_tela`,
  `RenderizadorErro`).
- `tela/teste_renderizador.py` — diagnóstico verificável do H-0003.
- `docs/relatorios/IMP-0003-renderizador-textual-estatico.md` — este
  relatório.

`tela/__init__.py` **não foi alterado** (permanece vazio). A
reexportação conveniente não é necessária ao escopo do H-0003.

## 4. Arquivos lidos (sem alteração)

- `docs/handoff/H-0003-renderizador-textual-estatico.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0003_HANDOFF.md`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/__init__.py`
- `config/telas/orquestrador.json`
- `config/estilo.json`

## 5. Renderer textual criado

`tela/renderizador.py` implementa:

- `class RenderizadorErro(Exception)` — exceção local de renderização.
- `def renderizar_tela(modelo: ModeloTela) -> str` — renderização
  textual estática.

### Importação no módulo do renderer

```python
from tela.modelo import ModeloTela
```

Único import do módulo. **Não** importa `json`, `os`, `pathlib`,
`tela.loader`, nem usa `subprocess`/`exec`/`eval`/`open`.

### Contrato da função

| Aspecto | Regra |
|---|---|
| Entrada | `ModeloTela` (objeto de `construir_modelo`, H-0002) |
| Saída | `str` — representação textual estática, determinística |
| Efeitos colaterais | Nenhum |
| Determinismo | Mesmo `ModeloTela` → mesma string |
| Independência de terminal | A saída não muda com a largura do terminal |
| Argumento inválido | Lança `RenderizadorErro` (`None` ou tipo errado) |

A função valida `isinstance(modelo, ModeloTela)`; caso contrário lança
`RenderizadorErro`. Em operação normal com `ModeloTela` válido não lança
exceção.

## 6. API implementada

Assinatura exata:

```python
def renderizar_tela(modelo: ModeloTela) -> str:
```

Exceção:

```python
class RenderizadorErro(Exception):
    """Erro de renderizacao textual de tela."""
```

## 7. Formato da saída

Formato exato e obrigatório definido pelo handoff H-0003 (seção "Formato
textual determinístico"). Estrutura:

```
TELA: {modelo.id}
SCHEMA: {modelo.schema}

CABECALHO
  titulo: {modelo.cabecalho.get("titulo", "(ausente)")}
  descricao: {modelo.cabecalho.get("descricao", "(ausente)")}

CORPO
  arranjo: {modelo.corpo.arranjo ou "(não declarado)"}
  elementos:
    - id: {e.id} | tipo: {e.tipo}
    [...]

BARRA_DE_MENUS
  chips:
    - id: {chip["id"]} | texto: {chip.get("texto", "(ausente)")}
    [...]
```

Regras aplicadas: linha em branco separando blocos; indentação de 2
espaços para campos; rótulos de lista `  elementos:` / `  chips:`;
itens com 4 espaços + `- `; separador ` | ` entre pares
`chave: valor`; arranjo `None` → `(não declarado)`; campos ausentes de
cabeçalho/chip → `(ausente)`; terminador `\n`; string finaliza com
`\n` após a última linha de conteúdo.

### Saída real do pipeline para `orquestrador.json`

Reprodução literal do `str` retornado por
`renderizar_tela(construir_modelo(carregar_tela(None, "orquestrador")))`:

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

A string acima é idêntica ao "expected output literal" do handoff
(inclusive o `\n` final), confirmada por verificação de igualdade estrita
no diagnóstico (`saida == _EXPECTED_ORQUESTRADOR`).

Observação: a descrição preserva exatamente o texto do
`orquestrador.json`, incluindo `visao` sem acento, conforme alerta do
handoff ("Se o handoff registra que a descrição está sem acento em
`visao`, preserve exatamente"). Nenhuma correção ortográfica foi feita.

## 8. Testes criados

`tela/teste_renderizador.py` — diagnóstico sem framework externo, com
`sys.dont_write_bytecode = True` antes de qualquer import, saída
`[PASSOU]`/`[FALHOU]`, totais e código de saída 0/1.

Total: **39 verificações, todas passando**.

### 18 verificações obrigatórias do handoff (todas PASSOU)

1. `renderizar_tela` aceita `ModeloTela` válido sem exceção.
2. Saída é `str`.
3. Saída começa com `TELA: orquestrador`.
4. Saída contém `SCHEMA: tela.v1`.
5. Saída contém `CABECALHO`.
6. Saída contém `titulo: Orquestrador`.
7. Saída contém `descricao:`.
8. Saída contém `CORPO`.
9. Saída contém `arranjo: sobreposto`.
10. Saída contém `id: console_principal | tipo: console`.
11. Saída contém `id: dashboard_info | tipo: dashboard`.
12. Saída contém `id: lancador_principal | tipo: lancador`.
13. Saída contém `BARRA_DE_MENUS`.
14. Saída contém `id: chip_esc`.
15. Saída contém `id: chip_ajuda`.
16. Saída é determinística (duas chamadas idênticas).
17. Modelo fabricado com `id="teste_fabricado"` produz saída começando
    com `TELA: teste_fabricado` (renderer usa dados do modelo, não do
    JSON).
18. `renderizar_tela(None)` lança `RenderizadorErro`.

### Verificações adicionais (robustez / anti-regressão)

- Igualdade estrita da saída com o expected output literal do handoff.
- Modelo fabricado também verifica `SCHEMA: tela.v0`, `arranjo: linear`,
  `id: e1 | tipo: console`, `id: c1 | texto: Ok` e que a saída não
  menciona `orquestrador` (fortalecido conforme A-001 da auditoria).
- `renderizar_tela(<dict>)` lança `RenderizadorErro`.
- Renderer não importa `json`, `os`, `pathlib`, nem `tela.loader` (não
  chama `carregar_tela`).
- Renderer não abre nem lê arquivos (`open(`, `.read_text(`,
  `.read_bytes(`).
- Renderer não usa `subprocess`/`exec(`/`eval(`.
- Renderer não acessa `_campos_inertes` dos elementos.
- `renderizar_tela` não altera `modelo._raw`, `modelo.cabecalho`,
  `corpo.elementos` nem `barra_de_menus.chips`.
- `console._campos_inertes` preserva
  `origem_dados.referencia == "pendente"` (inerte).
- `lancador._campos_inertes["itens"] == []` preservado (inerte).
- Saída não vaza campos inertes (`origem_dados`, `bindings`, `filtros`,
  `tela_destino`, `regra_existencia`).

## 9. Invariantes preservados de H-0001 e H-0002

```
$ python tela/teste_loader.py
...
Total de verificacoes: 37
Passaram: 37
Falharam: 0
(EXIT 0)

$ python tela/teste_modelo.py
...
Total de verificacoes: 30
Passaram: 30
Falharam: 0
(EXIT 0)
```

Os invariantes herdados (rejeição de tipo fora de
`{console, lancador, dashboard}`, `ModeloTela` construído apenas a
partir do dict do loader, campos inertes preservados, não execução de
ações, não ativação de bindings, JSON não alterado) continuam válidos.

## 10. Comportamento deliberadamente não implementado (fora de escopo)

Conforme handoff H-0003 (seção "Fora de escopo"), o renderer **não**
implementa e mantém inertes:

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
- layout final responsivo completo;
- cálculo de bordas/colunas/truncamento dependente do terminal;
- renderização com escape codes ANSI ou cores;
- leitura direta de `config/telas/orquestrador.json` pelo renderer;
- alteração de JSON em runtime;
- qualquer estado de runtime (cursor, página, filtro ativo, seleção,
  foco).

Razão: cada item acima exige decisões arquiteturais, registry ou
contratos ainda não fechados (DOC-B008 / DOC-B009 / bindings). O H-0003
é estático mínimo e determinístico.

## 11. Campos inertes preservados

O renderer apenas lê `modelo.id`, `modelo.schema`, `modelo.cabecalho`
(`titulo`, `descricao`), `modelo.corpo.arranjo`,
`modelo.corpo.elementos[]` (`id`, `tipo`) e
`modelo.barra_de_menus["chips"][]` (`id`, `texto`). Os campos abaixo
permanecem inertes — sem execução, resolução ou interpretação:

- `bindings`
- `referencias_de_acoes`
- `filtros`
- `chips[*].acao`, `chips[*].regra_existencia`, `chips[*].regra_ativo`
- `tela_destino` (inclusive `"pendente"`)
- `origem_dados` (inclusive `{"referencia": "pendente"}`)
- `regra_geracao_itens`
- `itens` vazios de `lancador_principal`
- `_campos_inertes` de cada `ElementoCorpo`

Pendências documentais ativas permanecem: DOC-B008 (tipos internos de
item de console), DOC-B009 (registry de ações/tipos de chip),
`lancador_principal.itens` vazio, `bindings` e `referencias_de_acoes`
declarados pendentes.

## 12. Comandos executados e resultados

### Integridade dos JSONs de configuração

```
$ python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
orquestrador.json OK
$ python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"
estilo.json OK
```

### Invariante H-0001 (loader)

```
$ python tela/teste_loader.py
...
Total de verificacoes: 37
Passaram: 37
Falharam: 0
(EXIT 0)
```

### Invariante H-0002 (modelo)

```
$ python tela/teste_modelo.py
...
Total de verificacoes: 30
Passaram: 30
Falharam: 0
(EXIT 0)
```

### Testes H-0003 (renderer)

```
$ python tela/teste_renderizador.py
Diagnostico H-0003 - renderer textual estatico de tela
...
== Resumo ==
Total de verificacoes: 39
Passaram: 39
Falharam: 0
(EXIT 0)
```

### Verificação de bytecode

```
$ find tela -type d -name '__pycache__' -print
$ find tela -type f -name '*.pyc' -print
```

Nenhum diretório `__pycache__` nem arquivo `.pyc` encontrado em `tela/`.

### Estado do repositório

```
$ git status --short
?? docs/handoff/H-0003-renderizador-textual-estatico.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0003_HANDOFF.md
?? tela/renderizador.py
?? tela/teste_renderizador.py
?? docs/relatorios/IMP-0003-renderizador-textual-estatico.md

$ git diff --stat
(vazio)
```

Apenas arquivos criados pelo H-0003 aparecem como não rastreados. Os dois
primeiros são pré-existentes ao início da implementação. `git diff --stat`
é vazio: nenhum arquivo rastreado foi alterado (loader, modelo, testes
anteriores, configs e docs normativas intactos).

## 13. Achado não bloqueante da auditoria e tratamento

A auditoria (`RELATORIO_AUDITORIA_H-0003_HANDOFF.md`, A-001, severidade
"observação") registrou que o teste anti-regressão com modelo fabricado,
conforme descrito no handoff, prova isoladamente apenas o uso de
`id`/`schema`, sugerindo fortalecer para verificar também `arranjo`,
corpo e chips.

Tratamento: o teste fabricado em `tela/teste_renderizador.py` foi
**fortalecido dentro do escopo** (sem alterar contrato, nomenclatura ou
decisão arquitetural), passando a verificar adicionalmente:

- `arranjo: linear` (presente na saída);
- `id: e1 | tipo: console` (elemento do corpo fabricado);
- `id: c1 | texto: Ok` (chip fabricado);
- a saída fabricada não menciona `orquestrador`.

Isso demonstra que o renderer renderiza corpo e chips a partir dos dados
do `ModeloTela` recebido, e não do JSON em disco. Nenhuma ressalva
permanece.

## 14. Status final

```
APROVADO
```

Todos os critérios de aceite do H-0003 estão verificados: escopo e
arquivos respeitados, API e renderer conformes, formato da saída exato,
invariantes de H-0001/H-0002 preservados, sem `__pycache__`/`.pyc`, JSONs
válidos e inalterados, relatório criado, e o achado não bloqueante da
auditoria foi tratado dentro do escopo sem gerar nova ressalva.
