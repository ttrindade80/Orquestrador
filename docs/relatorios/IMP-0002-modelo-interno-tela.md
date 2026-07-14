# Relatório de Implementação — H-0002 Modelo interno normalizado de tela

## Status

APROVADO

## Objetivo

Implementar uma camada de **modelo interno normalizado** da tela, que envolve
o dicionário produzido pelo loader H-0001 (`carregar_tela`) em uma estrutura
Python explícita baseada em `dataclass` da stdlib, acessível por nome e
auditável. O modelo:

- expõe `id`, `schema`, `cabecalho`, `corpo`, `barra_de_menus`;
- expõe cada elemento do corpo com `id` e `tipo` acessíveis por atributo;
- preserva os campos adicionais de cada elemento como dados inertes em
  `_campos_inertes`;
- preserva o JSON original completo em `_raw`;
- produz diagnóstico textual auditável via `ModeloTela.diagnostico()`;
- **não** valida novamente a estrutura macro (responsabilidade do H-0001);
- **não** executa bindings, chips, filtros, navegação, paginação, seleção,
  resolução de `tela_destino`/`origem_dados` nem qualquer comportamento de
  runtime.

A função pública é `construir_modelo(tela_raw: dict) -> ModeloTela`, que
recebe o dict já validado pelo loader e constrói a estrutura tipada.

## Arquivos criados ou alterados

| Arquivo | Alteração |
|---|---|
| `tela/modelo.py` | criado — módulo do modelo interno (`ModeloTelaErro`, `ElementoCorpo`, `Corpo`, `ModeloTela`, `construir_modelo`) |
| `tela/teste_modelo.py` | criado — diagnóstico verificável do modelo (30 verificações) |
| `docs/relatorios/IMP-0002-modelo-interno-tela.md` | criado — este relatório |

Arquivos **não alterados** deliberadamente (escopo minimizado conforme
ressalva 1 da auditoria):

- `tela/loader.py` — **não tocado**. A constante `TIPOS_CORPO_VALIDOS` é
  importada por `tela/modelo.py` via `from tela.loader import ...`, sem
  qualquer modificação no loader. Nenhuma linha existente foi editada;
  `carregar_tela` e todas as exceções do H-0001 permanecem byte-a-byte
  idênticas.
- `tela/__init__.py` — **não tocado** (permanece vazio). A reexportação
  opcional prevista no handoff não foi considerada necessária; os testes
  importam diretamente de `tela.modelo`.
- `tela/teste_loader.py` — **não tocado**. Os 37 critérios do H-0001
  continuam passando integralmente.

## Arquivos proibidos preservados

Confirmados intactos (não criados, não alterados, não removidos):

- `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md`, `docs/issues.md`
- `docs/contratos/*`
- `docs/adr/*`
- `docs/handoff/*` (incluindo `H-0002-modelo-interno-tela.md`)
- `docs/templates/*`
- `config/telas/orquestrador.json`
- `config/estilo.json`
- qualquer outro arquivo em `config/`

Nenhum novo JSON foi criado. Nenhum contrato, ADR, nomenclatura, backlog,
issue ou handoff foi alterado.

## Modelo interno implementado

Implementado em `tela/modelo.py` com `dataclass` da stdlib Python
(`dataclasses.dataclass`, `dataclasses.field`). Apenas biblioteca padrão.

### `ModeloTelaErro(Exception)`

Exceção base lançada por `construir_modelo` quando o dict de entrada não tem
o formato mínimo esperado (ausência de chave que o loader deveria ter
produzido, tipo incorreto, elemento sem `id`/`tipo`, tipo fora da taxonomia).

### `ElementoCorpo` (`@dataclass`)

```python
@dataclass
class ElementoCorpo:
    id: str
    tipo: str                                  # um de: console, lancador, dashboard
    _campos_inertes: dict = field(default_factory=dict, repr=False)
```

Contém todos os demais campos do elemento (titulo, origem_dados,
regra_geracao_itens, politica_*, colunas_ajustavel, itens, layout, campos,
marcadores, etc.) preservados sem interpretação, sem execução e sem
semântica nova.

### `Corpo` (`@dataclass`)

```python
@dataclass
class Corpo:
    arranjo: str | None
    elementos: list  # lista de ElementoCorpo
```

### `ModeloTela` (`@dataclass`)

```python
@dataclass
class ModeloTela:
    id: str
    schema: str
    cabecalho: dict
    corpo: Corpo
    barra_de_menus: dict
    _raw: dict = field(repr=False)
```

Métodos auxiliares somente leitura (não criam semântica nova, não ativam
bindings, não executam ações, não resolvem pendências):

- `elemento_por_id(id_elemento) -> ElementoCorpo | None`
- `elementos_por_tipo(tipo) -> list[ElementoCorpo]`
- `diagnostico() -> str` — retorna string contendo ao menos `id`, `schema`,
  `corpo.arranjo` e a lista de elementos com `id` e `tipo` de cada um.

### `construir_modelo(tela_raw: dict) -> ModeloTela`

- Não chama `carregar_tela` internamente.
- Não revalida a estrutura macro (responsabilidade do H-0001).
- Verifica apenas o formato mínimo do dict recebido (presença das chaves
  `id`, `schema`, `cabecalho`, `corpo`, `barra_de_menus`, `_raw`, e que
  `corpo.elementos` seja uma lista de dicts com `id`+`tipo`).
- Rejeita tipos fora de `TIPOS_CORPO_VALIDOS` com `ModeloTelaErro`
  (camada defensiva — o loader já rejeitaria antes).
- Constroi cada `ElementoCorpo` separando `id` e `tipo` dos demais campos,
  que vão para `_campos_inertes`.

### `TIPOS_CORPO_VALIDOS`

Importado de `tela.loader` (`from tela.loader import TIPOS_CORPO_VALIDOS`),
para evitar divergência da taxonomia fechada definida no H-0001.
Reexportado naturalmente como atributo de `tela.modelo`.

## Campos inertes preservados

Preservados sem execução, sem resolução, sem validação funcional e sem
rejeição por incompletude, exatamente como vieram do JSON:

- `bindings` (em `modelo._raw`) — dict inerte;
- `referencias_de_acoes` (em `modelo._raw`) — dict inerte com
  `status: "pendente_DOC-B009"`;
- `filtros` (em `modelo._raw`) — lista inerte;
- chips da `barra_de_menus` (em `modelo.barra_de_menus`) — lista completa
  preservada como-está, incluindo `chip_estilo.acao.tela_destino ==
  "pendente"`;
- `origem_dados` com `referencia == "pendente"` em `console_principal` e
  `dashboard_info` (em `_campos_inertes` de cada `ElementoCorpo`);
- `regra_geracao_itens` pendente em `console_principal` (em `_campos_inertes`);
- `itens == []` vazio de `lancador_principal` (em `_campos_inertes`);
- `campos` e `marcadores` com `fonte: "pendente"` em `dashboard_info`
  (em `_campos_inertes`);
- demais campos adicionais de cada elemento (titulo, politica_*, layout,
  colunas_ajustavel, filtro_de_grupo, formacao_de_selecao, posicao_dashboard,
  pendencia_itens, etc.) — todos em `_campos_inertes`;
- `metadados` top-level — preservado em `modelo._raw`;
- qualquer outro campo adicional do JSON não pertencente aos atributos
  estruturais mínimos — preservado em `_raw` ou em `_campos_inertes`,
  conforme o escopo.

## Invariantes do H-0001 preservados

O H-0002 **não enfraquece** nenhum invariante do H-0001. Evidência:
`python tela/teste_loader.py` retorna código de saída `0` com as **37
verificações** do H-0001 passando (saída completa na seção de comandos).
Nenhuma exceção do loader foi removida ou alterada em comportamento
(`TelaArquivoNaoEncontrado`, `TelaJsonInvalido`, `TelaCampoObrigatorioAusente`,
`TelaIdNaoCoincideComArquivo`, `TelaIdIncorreto`, `TelaEstruturaInvalida`,
`TelaElementoSemId`, `TelaElementoSemTipo`, `TelaTipoDesconhecido`). A função
`carregar_tela` permaneceu byte-a-byte idêntica — `tela/loader.py` não foi
modificado.

A validação macro continua sendo autoridade exclusiva do loader; o modelo
apenas constrói a estrutura tipada sobre o dict já validado.

## Fora de escopo não implementado

Confirmado **não implementado** (preservado estritamente como declaração
inerte), conforme handoff H-0002:

- renderer de qualquer região da tela;
- navegação real entre telas;
- execução de ações declaradas em chips;
- registry de ações (`referencias_de_acoes`);
- resolução ou ativação de `bindings`;
- filtros funcionais (`filtros[]`);
- paginação funcional;
- seleção funcional;
- alteração de estilo em runtime;
- dashboard dinâmico com dados reais;
- resolução funcional de `tela_destino`;
- resolução funcional de `origem_dados`;
- subclasses específicas por tipo de elemento do corpo
  (`ConsoleElemento`, `LancadorElemento`, `DashboardElemento`);
- registry de tipos de elemento;
- tipos internos completos de item do `console` (DOC-B008);
- execução de chips;
- alteração de JSON em runtime;
- qualquer estado de runtime (cursor, página, filtro ativo, seleção, foco)
  no modelo.

## Comandos executados

### `python -m json.tool config/telas/orquestrador.json`

```text
orquestrador.json OK
```

### `python -m json.tool config/estilo.json`

```text
estilo.json OK
```

### `python tela/teste_loader.py` (H-0001 — invariantes preservados)

```text
Diagnostico H-0001 - loader/validador de tela.json
Base padrao: /home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
Python: 3.14.6

== Carregamento do arquivo real config/telas/orquestrador.json ==
[PASSOU] carregar_tela(orquestrador)
[PASSOU] tela.id == 'orquestrador' - id='orquestrador'
[PASSOU] tela.schema presente - schema='tela.v1'
[PASSOU] tela.cabecalho presente
[PASSOU] tela.barra_de_menus presente
[PASSOU] tela.corpo presente
[PASSOU] tela.corpo.arranjo preservado - arranjo='sobreposto'
[PASSOU] tela.corpo.elementos e lista com 3 itens - n=3
[PASSOU] tipos presentes = {console, dashboard, lancador} - tipos=['console', 'dashboard', 'lancador']
[PASSOU] ids dos elementos presentes - ids=['console_principal', 'dashboard_info', 'lancador_principal']
[PASSOU] _raw preserva o JSON original completo

-- Declaracao inerte preservada (DOC-B008 / DOC-B009) --
[PASSOU] chip_estilo.tela_destino == 'pendente' carregado sem erro
[PASSOU] console_principal.origem_dados.referencia == 'pendente' inerte
[PASSOU] lancador_principal.itens == [] carregado sem erro
[PASSOU] bindings preservado como declaracao inerte
[PASSOU] referencias_de_acoes preservado como declaracao inerte
[PASSOU] filtros preservado como declaracao inerte

== Casos de erro (arquivos temporarios em /tmp/tela_loader_h0001_...) ==
[PASSOU] arquivo ausente -> TelaArquivoNaoEncontrado
[PASSOU] JSON sintaticamente invalido -> TelaJsonInvalido
[PASSOU] sem schema -> TelaCampoObrigatorioAusente(schema)
[PASSOU] sem id -> TelaCampoObrigatorioAusente(id)
[PASSOU] id vazio -> TelaCampoObrigatorioAusente(id)
[PASSOU] id diverge do basename -> TelaIdNaoCoincideComArquivo
[PASSOU] sem cabecalho -> TelaCampoObrigatorioAusente(cabecalho)
[PASSOU] sem corpo -> TelaCampoObrigatorioAusente(corpo)
[PASSOU] sem barra_de_menus -> TelaCampoObrigatorioAusente(barra_de_menus)
[PASSOU] sem corpo.elementos -> TelaCampoObrigatorioAusente(corpo.elementos)
[PASSOU] corpo.elementos nao e lista -> TelaEstruturaInvalida
[PASSOU] elemento sem id -> TelaElementoSemId
[PASSOU] elemento sem tipo -> TelaElementoSemTipo
[PASSOU] tipo desconhecido -> TelaTipoDesconhecido
[PASSOU] tipo nao string -> TelaElementoSemTipo (reuso da categoria)

== Aceitacao dos tipos validos (taxonomia fechada) ==
[PASSOU] tipo 'console' aceito
[PASSOU] tipo 'lancador' aceito
[PASSOU] tipo 'dashboard' aceito
[PASSOU] TIPOS_CORPO_VALIDOS == {console, lancador, dashboard}

== Excecao TelaIdIncorreto (verificacao de classe) ==
[PASSOU] TelaIdIncorreto instanciavel e mensagem e auditavel

== Resumo ==
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

Código de saída: `0`.

### `python tela/teste_modelo.py` (H-0002 — novo)

```text
Diagnostico H-0002 - modelo interno normalizado de tela
Base padrao: /home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
Python: 3.14.6

== Construcao do modelo para config/telas/orquestrador.json ==
[PASSOU] construir_modelo(carregar_tela(orquestrador))
[PASSOU] modelo.id == 'orquestrador' - id='orquestrador'
[PASSOU] modelo.schema == 'tela.v1' - schema='tela.v1'
[PASSOU] modelo.cabecalho e dict com 'titulo' e 'descricao'
[PASSOU] modelo.corpo e Corpo com arranjo e elementos
[PASSOU] modelo.corpo.arranjo == 'sobreposto' - arranjo='sobreposto'
[PASSOU] modelo.corpo.elementos e lista com 3 itens - n=3
[PASSOU] cada elemento e ElementoCorpo com id e tipo acessiveis
[PASSOU] tipos presentes = {console, dashboard, lancador} - tipos=['console', 'dashboard', 'lancador']
[PASSOU] elemento_por_id('console_principal') retorna elemento tipo console
[PASSOU] elemento_por_id('dashboard_info') retorna elemento tipo dashboard
[PASSOU] elemento_por_id('lancador_principal') retorna elemento tipo lancador
[PASSOU] elemento_por_id('inexistente') retorna None
[PASSOU] elementos_por_tipo('console') retorna lista com 1 item - n=1

-- Declaracao inerte preservada (DOC-B008 / DOC-B009) --
[PASSOU] console_principal._campos_inertes preserva origem_dados.referencia == 'pendente' (inerte)
[PASSOU] lancador_principal._campos_inertes['itens'] == [] (inerte)
[PASSOU] modelo.barra_de_menus e dict nao vazio
[PASSOU] chip_estilo.acao.tela_destino == 'pendente' preservado (inerte)
[PASSOU] modelo._raw preserva JSON original completo
[PASSOU] modelo._raw['bindings'] preservado como dict inerte
[PASSOU] modelo._raw['referencias_de_acoes'] preservado como dict inerte
[PASSOU] modelo._raw['filtros'] preservado como lista inerte
[PASSOU] modelo.diagnostico() retorna string nao vazia contendo id
[PASSOU] diagnostico contem schema, arranjo e tipo de cada elemento
[PASSOU] TIPOS_CORPO_VALIDOS reexportado por tela.modelo == {console, lancador, dashboard}

== Casos de erro do construtor de modelo ==
[PASSOU] construir_modelo({}) levanta ModeloTelaErro
[PASSOU] construir_modelo(None) levanta ModeloTelaErro
[PASSOU] construir_modelo sem 'corpo' levanta ModeloTelaErro
[PASSOU] construir_modelo sem 'corpo.elementos' levanta ModeloTelaErro
[PASSOU] construir_modelo com tipo fora da taxonomia levanta ModeloTelaErro

== Resumo ==
Total de verificacoes: 30
Passaram: 30
Falharam: 0

== Diagnostico do modelo ==
id: orquestrador
schema: tela.v1
corpo.arranjo: sobreposto
  elemento: id='console_principal' tipo='console'
  elemento: id='dashboard_info' tipo='dashboard'
  elemento: id='lancador_principal' tipo='lancador'
```

Código de saída: `0`.

### Verificação de bytecode

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Saída:

```text
(vazio)
(vazio)
```

Nenhum `__pycache__` nem `.pyc` gerado (ambos scripts de teste definem
`sys.dont_write_bytecode = True` antes de qualquer import).

## Git status final

```bash
git status --short --untracked-files=all
```

Saída:

```text
?? docs/handoff/H-0002-modelo-interno-tela.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0002_HANDOFF.md
?? tela/modelo.py
?? tela/teste_modelo.py
```

```bash
git diff --stat
git diff --name-only
```

Saída (ambos):

```text
(vazio)
```

Nenhum arquivo **rastreado** foi modificado por esta implementação. Nenhum
arquivo fora do escopo permitido foi criado.

## Ressalvas

- **R-1 (auditoria ressalva 1 — `tela/loader.py`).** Conforme orientação da
  auditoria (preferir não alterar `tela/loader.py`; se reexportação for
  necessária, preferir `tela/__init__.py`), **nenhuma alteração** foi feita
  em `tela/loader.py`. A constante `TIPOS_CORPO_VALIDOS` é importada por
  `tela/modelo.py` via `from tela.loader import TIPOS_CORPO_VALIDOS`, sem
  editar nenhuma linha do loader. `tela/__init__.py` também não precisou ser
  alterado (permanece vazio): os testes importam diretamente de
  `tela.modelo`. `carregar_tela` e todas as exceções do H-0001 permanecem
  byte-a-byte idênticas — `git diff --stat` retorna vazio.
- **R-2 (auditoria ressalva 2 — arquivos pré-existentes não rastreados).**
  Os arquivos listados abaixo aparecem em `git status --short` como `??` mas
  são **pré-existentes ao início da implementação** (não criados e não
  alterados por este ciclo):
  - `docs/handoff/H-0002-modelo-interno-tela.md`
  - `docs/relatorios/RELATORIO_AUDITORIA_H-0002_HANDOFF.md`
- **R-3 (escopo minimizado).** A reexportação opcional via `tela/__init__.py`
  prevista no handoff não foi considerada necessária; `tela/__init__.py`
  permanece vazio para minimizar o conjunto de arquivos alterados e evitar
  qualquer efeito colateral de importação em `tela/teste_loader.py`.
- **R-4 (sem commit).** Conforme o handoff e o prompt operacional, nenhum
  commit foi feito.
- **R-5 (sem decisão arquitetural local).** Nenhuma lacuna do handoff foi
  preenchida com decisão local; a estrutura segue fielmente a seção "Escolha
  arquitetural" do H-0002.

## Resultado final

APROVADO
