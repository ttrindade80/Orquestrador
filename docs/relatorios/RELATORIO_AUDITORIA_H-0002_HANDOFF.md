# Relatorio de Auditoria - H-0002 Handoff

## Status

APROVADO_COM_RESSALVAS

## Escopo auditado

- `docs/handoff/H-0002-modelo-interno-tela.md`
- `docs/INDICE.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_estilo.md`
- `config/telas/orquestrador.json`
- `config/estilo.json`
- `docs/handoff/H-0001-loader-validador-tela-json.md`
- `docs/relatorios/IMP-0001-loader-validador-tela-json.md`
- `tela/loader.py`
- `tela/teste_loader.py`
- `docs/backlog.md`
- `docs/issues.md`

## Resultado resumido

O handoff H-0002 esta coerente com o contrato de processo, ADR-0008,
ADR-0009, contratos ativos, H-0001 e estado real do repositorio. Ele define
uma camada de modelo interno com `dataclass`, limita o escopo a construcao
inerte sobre o dict validado pelo loader, preserva os invariantes de H-0001,
proibe renderer e comportamento de runtime, e contem criterios de aceite
observaveis.

A classificacao e `APROVADO_COM_RESSALVAS` por duas ressalvas menores:

- a regra de `tela/loader.py` mistura "adicionar codigo ao final" com
  "salvo adicao de importacao no topo"; isso e implementavel, mas deve ser
  tratado com cuidado para nao alterar nenhuma linha existente nem o
  comportamento de `carregar_tela`;
- `git status --short` ja mostra `docs/handoff/H-0002-modelo-interno-tela.md`
  como arquivo nao rastreado antes da implementacao; o executor/QA deve
  distinguir esse estado preexistente de alteracoes feitas no ciclo H-0002.

Nenhuma ressalva impede a implementacao.

## Evidencias

### Existencia dos arquivos obrigatorios

Todos os arquivos obrigatorios listados no prompt de auditoria existem. Nao
houve condicao de `BLOCKED` por arquivo ausente.

Comandos executados:

```bash
test -f docs/handoff/H-0002-modelo-interno-tela.md && echo "handoff H-0002 existe"
test -f config/telas/orquestrador.json && echo "orquestrador.json existe"
test -f tela/loader.py && echo "loader.py existe"
test -f tela/teste_loader.py && echo "teste_loader.py existe"
```

Saida:

```text
handoff H-0002 existe
orquestrador.json existe
loader.py existe
teste_loader.py existe
```

### JSONs de configuracao

Comandos executados:

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"
```

Saida:

```text
orquestrador.json OK
estilo.json OK
```

### Git e bytecode

Comandos executados:

```bash
git status --short
find tela -type d -name '__pycache__' -o -type f -name '*.pyc'
```

Saida:

```text
?? docs/handoff/H-0002-modelo-interno-tela.md
```

O comando de bytecode/cache retornou vazio.

### Trechos auditados do H-0002

- Ordem de autoridade e bloqueio por conflito: `docs/handoff/H-0002-modelo-interno-tela.md`, linhas 21-37.
- Pendencias mantidas como inertes: linhas 81-97.
- Objetivo do modelo interno: linhas 101-121.
- Escolha por `dataclass` e classes `ElementoCorpo`, `Corpo`, `ModeloTela`: linhas 125-165.
- Proibicao de runtime, resolucao e subclasses por tipo: linhas 167-179.
- Funcao publica `construir_modelo(tela_raw: dict) -> ModeloTela`: linhas 181-210.
- Arquivos permitidos e regra especifica de `loader.py`: linhas 214-239.
- Arquivos proibidos e retorno `ARCHITECTURE_REVIEW_REQUIRED`: linhas 243-268.
- Fora de escopo obrigatorio: linhas 272-295.
- Tarefas e testes esperados: linhas 299-378.
- Invariantes herdados do H-0001: linhas 382-405.
- Campos pendentes e inertes: linhas 409-433.
- Criterios de aceite: linhas 437-515.
- Comandos de verificacao esperados: linhas 519-545.
- Relatorio obrigatorio: linhas 549-582.
- Condicoes de bloqueio e instrucao explicita: linhas 586-624.

### Conteudo real de `orquestrador.json`

O JSON real contem os campos pendentes que o H-0002 cobre:

- `origem_dados` e `regra_geracao_itens` em `console_principal`: `config/telas/orquestrador.json`, linhas 30-37.
- politicas declarativas de navegacao, selecao, paginacao, colunas, filtro e modo verboso: linhas 38-61.
- `origem_dados` pendente em `dashboard_info`: linhas 68-71.
- campos e marcadores com `fonte: "pendente"`: linhas 72-98.
- `lancador_principal.itens == []`: linhas 100-109.
- `barra_de_menus.chips`: linhas 113-238.
- `chip_estilo.acao.tela_destino == "pendente"`: linhas 203-216.
- `filtros`: linhas 240-249.
- `bindings`: linhas 250-252.
- `referencias_de_acoes`: linhas 253-256.

## Conformidades encontradas

- Respeita o contrato de processo: ha contrato aplicavel, handoff fechado,
  criterios de aceite verificaveis e limites claros de arquivos permitidos e
  proibidos.
- Nao contradiz ADR-0008: o modelo atua sobre declaracao por tela, nao move
  composicao para codigo, nao altera `estilo.json`, e preserva configuracao
  concreta como dados.
- Nao contradiz ADR-0009: assume `config/telas/<id>.json`, `id`
  `"orquestrador"` e pipeline carregado por `carregar_tela`.
- Nao contradiz contratos ativos: evita renderer, registry de acoes, registry
  de tipos, resolucao de bindings, filtros funcionais, paginacao, selecao e
  navegacao.
- Preserva H-0001: mantem o loader como autoridade da validacao macro e exige
  que `python tela/teste_loader.py` continue passando com 37 verificacoes.
- Define suficientemente o modelo interno: `ElementoCorpo`, `Corpo`,
  `ModeloTela`, `ModeloTelaErro`, `construir_modelo`, campos minimos,
  diagnostico e regras de erro.
- Define preservacao inerte dos campos pendentes reais do JSON:
  `bindings`, `referencias_de_acoes`, `filtros`, `chips`, `tela_destino`,
  `origem_dados`, `regra_geracao_itens`, `itens` vazios e valores
  `"pendente"`.
- Proibe explicitamente renderer, navegacao, acoes, bindings ativos, filtros
  funcionais, paginacao, selecao, registries, dashboard dinamico, mudanca de
  estilo em runtime, execucao de chips e alteracao de JSON em runtime.
- Exige relatorio de implementacao em
  `docs/relatorios/IMP-0002-modelo-interno-tela.md`.
- Deixa claro quando retornar `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`.

## Ressalvas

1. **Regra de `loader.py` requer cuidado operacional.**
   O handoff diz que o executor pode adicionar codigo ao final do arquivo,
   mas tambem permite "salvo adicao de importacao no topo". A combinacao nao
   cria contradicao material, mas a implementacao deve evitar qualquer edicao
   de linha existente. Preferencia operacional: se houver reexportacao, faze-la
   no final; se uma importacao no topo for usada, documentar no relatorio que
   nenhuma linha existente nem comportamento observavel foi alterado.

2. **`git status --short` ja lista o proprio H-0002 como nao rastreado.**
   A saida atual e:

   ```text
   ?? docs/handoff/H-0002-modelo-interno-tela.md
   ```

   Como `docs/handoff/` e proibido para a implementacao, o executor nao deve
   tocar esse arquivo. O relatorio de implementacao e a QA devem registrar que
   esse item era preexistente ao ciclo e avaliar somente arquivos criados ou
   alterados pelo executor.

3. **Frase de preservacao em `_campos_inertes` e `_raw` pode ser lida de forma
   ampla demais.**
   A secao "Campos pendentes e inertes" lista campos de escopos diferentes
   depois de dizer que serao preservados em `_campos_inertes` de
   `ElementoCorpo` e em `_raw` de `ModeloTela`. Os criterios de aceite
   esclarecem a expectativa correta: campos de elemento em `_campos_inertes`,
   chips em `modelo.barra_de_menus`/`_raw`, e top-level `bindings`,
   `referencias_de_acoes` e `filtros` em `_raw`. Nao bloqueia, mas convem ao
   implementador seguir os criterios de aceite.

## Bloqueios

Nenhum bloqueio encontrado.

## Violacoes ou contradicoes

Nenhuma violacao contratual ou contradicao arquitetural material encontrada.

## Recomendacao

O handoff pode seguir para implementacao pelo GLM/OpenCode com as ressalvas
acima documentadas. As ressalvas nao impedem implementacao; devem ser tratadas
como cuidados de execucao e QA.
