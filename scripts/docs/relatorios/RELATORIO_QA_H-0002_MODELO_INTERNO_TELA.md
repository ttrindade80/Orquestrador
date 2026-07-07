# Relatório de QA — H-0002 Modelo interno normalizado de tela

## Status

QA_APPROVED_WITH_NOTES

## Escopo auditado

- `docs/handoff/H-0002-modelo-interno-tela.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0002_HANDOFF.md`
- `docs/relatorios/IMP-0002-modelo-interno-tela.md`
- `tela/modelo.py`
- `tela/teste_modelo.py`
- `tela/loader.py`
- `tela/teste_loader.py`
- `config/telas/orquestrador.json`
- `config/estilo.json`
- `docs/handoff/H-0001-loader-validador-tela-json.md`
- `docs/relatorios/IMP-0001-loader-validador-tela-json.md`

## Resultado resumido

A implementacao do H-0002 cumpre o handoff: cria o modelo interno normalizado
com `dataclass`, preserva campos pendentes como dados inertes, mantem o H-0001
funcional, nao altera `loader.py`, `teste_loader.py`, `config/`, contratos,
ADRs, nomenclatura, backlog, issues ou handoffs rastreados, e nao implementa
renderer nem comportamento dinamico.

O status e `QA_APPROVED_WITH_NOTES` apenas porque `git status --short` contem
dois arquivos nao rastreados declarados como pre-existentes pelo ciclo
(`docs/handoff/H-0002-modelo-interno-tela.md` e
`docs/relatorios/RELATORIO_AUDITORIA_H-0002_HANDOFF.md`). Essa nota nao impede
commit dos arquivos de H-0002, desde que o engenheiro trate explicitamente os
nao rastreados no commit.

## Evidências de execução

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

```text
orquestrador.json OK
```

```bash
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"
```

```text
estilo.json OK
```

```bash
python tela/teste_loader.py
```

```text
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

Saida relevante confirmou tambem:

```text
[PASSOU] JSON sintaticamente invalido -> TelaJsonInvalido
[PASSOU] sem schema -> TelaCampoObrigatorioAusente(schema)
[PASSOU] sem id -> TelaCampoObrigatorioAusente(id)
[PASSOU] sem cabecalho -> TelaCampoObrigatorioAusente(cabecalho)
[PASSOU] sem corpo -> TelaCampoObrigatorioAusente(corpo)
[PASSOU] sem barra_de_menus -> TelaCampoObrigatorioAusente(barra_de_menus)
[PASSOU] sem corpo.elementos -> TelaCampoObrigatorioAusente(corpo.elementos)
[PASSOU] elemento sem id -> TelaElementoSemId
[PASSOU] elemento sem tipo -> TelaElementoSemTipo
[PASSOU] tipo desconhecido -> TelaTipoDesconhecido
[PASSOU] TIPOS_CORPO_VALIDOS == {console, lancador, dashboard}
```

```bash
python tela/teste_modelo.py
```

```text
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

Saida relevante confirmou tambem:

```text
[PASSOU] construir_modelo(carregar_tela(orquestrador))
[PASSOU] modelo.id == 'orquestrador'
[PASSOU] modelo.schema == 'tela.v1'
[PASSOU] modelo.corpo.elementos e lista com 3 itens
[PASSOU] tipos presentes = {console, dashboard, lancador}
[PASSOU] console_principal._campos_inertes preserva origem_dados.referencia == 'pendente' (inerte)
[PASSOU] lancador_principal._campos_inertes['itens'] == [] (inerte)
[PASSOU] chip_estilo.acao.tela_destino == 'pendente' preservado (inerte)
[PASSOU] modelo._raw['bindings'] preservado como dict inerte
[PASSOU] modelo._raw['referencias_de_acoes'] preservado como dict inerte
[PASSOU] modelo._raw['filtros'] preservado como lista inerte
[PASSOU] construir_modelo com tipo fora da taxonomia levanta ModeloTelaErro
```

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

```text
(vazio)
(vazio)
```

```bash
git status --short
```

```text
?? docs/handoff/H-0002-modelo-interno-tela.md
?? docs/relatorios/IMP-0002-modelo-interno-tela.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0002_HANDOFF.md
?? tela/modelo.py
?? tela/teste_modelo.py
```

```bash
git diff --stat
git diff --name-only
```

```text
(vazio)
(vazio)
```

Buscas de apoio:

```text
grep "render": vazio
grep "execut": apenas comentarios/testes de nao execucao
grep "binding": comentarios/testes de preservacao inerte
grep "filtro": comentarios/testes de preservacao inerte
grep "tela_destino": comentario/teste de preservacao inerte
```

## Conformidades

- `tela/modelo.py` foi criado.
- `tela/teste_modelo.py` foi criado.
- `docs/relatorios/IMP-0002-modelo-interno-tela.md` foi criado.
- `tela/modelo.py` define `ModeloTelaErro`, `ElementoCorpo`, `Corpo`,
  `ModeloTela` e `construir_modelo(tela_raw: dict) -> ModeloTela`.
- `ElementoCorpo`, `Corpo` e `ModeloTela` usam `dataclass` da biblioteca
  padrao.
- O modelo expoe `ModeloTela.id`, `ModeloTela.schema`, `ModeloTela.cabecalho`,
  `ModeloTela.corpo`, `ModeloTela.barra_de_menus`, `ModeloTela._raw`,
  `Corpo.elementos`, `ElementoCorpo.id` e `ElementoCorpo.tipo`.
- Campos adicionais dos elementos sao preservados em `_campos_inertes`.
- Campos top-level reais do JSON, incluindo `metadados`, `bindings`,
  `referencias_de_acoes` e `filtros`, permanecem preservados em `_raw`.
- Chips e `chip_estilo.acao.tela_destino == "pendente"` permanecem em
  `modelo.barra_de_menus` e `_raw`, sem execucao.
- `origem_dados`, `regra_geracao_itens`, campos pendentes do dashboard e
  `lancador_principal.itens == []` permanecem inertes em `_campos_inertes`.
- `diagnostico()` retorna string auditavel com id, schema, arranjo e elementos
  com id/tipo.
- Tipo desconhecido e rejeitado por `construir_modelo` com `ModeloTelaErro`,
  usando `TIPOS_CORPO_VALIDOS` importado de `tela.loader`.
- `python tela/teste_loader.py` preserva as 37 verificacoes do H-0001.
- Nenhum `__pycache__` nem `.pyc` permaneceu em `tela/`.

## Ressalvas

- `git status --short` lista `docs/handoff/H-0002-modelo-interno-tela.md` e
  `docs/relatorios/RELATORIO_AUDITORIA_H-0002_HANDOFF.md` como nao rastreados.
  O prompt e o relatorio de implementacao declaram esses dois arquivos como
  pre-existentes ao ciclo; por isso nao foram tratados como violacao.
- O relatorio de implementacao declarou `IMP-0002` como criado, mas ele tambem
  aparece nao rastreado. Isso e esperado para arquivo novo ainda nao commitado.

## Violações

Nenhuma violacao encontrada.

## Arquivos criados ou alterados no ciclo

- `tela/modelo.py` — criado no ciclo H-0002, permitido.
- `tela/teste_modelo.py` — criado no ciclo H-0002, permitido.
- `docs/relatorios/IMP-0002-modelo-interno-tela.md` — criado no ciclo H-0002,
  permitido.
- `docs/handoff/H-0002-modelo-interno-tela.md` — nao rastreado, declarado como
  pre-existente; nao tratado como alteracao do executor.
- `docs/relatorios/RELATORIO_AUDITORIA_H-0002_HANDOFF.md` — nao rastreado,
  declarado como pre-existente; nao tratado como alteracao do executor.

## Arquivos proibidos preservados

Confirmado por `git diff --stat`, `git diff --name-only` e leitura do status:
nao ha modificacao rastreada em `config/`, `docs/contratos/`, `docs/adr/`,
`docs/NOMENCLATURA.md`, `docs/INDICE.md`, `docs/backlog.md`, `docs/issues.md`,
`docs/handoff/`, `tela/loader.py`, `tela/__init__.py` ou `tela/teste_loader.py`.

## Fora de escopo

Nao foram encontrados indícios de renderer, navegacao real, execucao de acoes,
bindings ativos, filtros funcionais, paginacao, selecao, registry de acoes,
registry de tipos, subclasses por tipo de elemento, dashboard dinamico,
mudanca de estilo em runtime, resolucao funcional de `tela_destino`,
resolucao funcional de `origem_dados`, execucao de chips ou alteracao de JSON
em runtime.

## Decisão de QA

QA_APPROVED_WITH_NOTES

## Próxima ação recomendada

O ciclo pode seguir para consolidacao e commit. As notas nao impedem o commit;
recomenda-se apenas que o commit inclua explicitamente os arquivos novos do
H-0002 e trate conscientemente os dois artefatos nao rastreados declarados como
pre-existentes.
