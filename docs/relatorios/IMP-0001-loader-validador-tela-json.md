---
name: IMP-0001-loader-validador-tela-json
description: Resultado da implementacao H-0001 - loader e validador macro de tela.json para a tela raiz do Orquestrador
metadata:
  type: relatorio_implementacao
  status: IMPLEMENTED_POS_QA
  handoff_origem: H-0001
  data: 2026-07-07
  data_ajuste_pos_qa: 2026-07-07
rastreabilidade:
  contrato_alvo: "docs/contratos/contrato_tela_json.md"
  adr_relacionadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  bugs_abertos: []
---

# IMP-0001 — Relatorio de Implementacao

## Handoff executado

`H-0001 — Loader e validador minimo de tela JSON`

## Status final

`IMPLEMENTED_POS_QA`

### Historico de QA

| Ciclo | Status | Motivo |
|---|---|---|
| Implementacao inicial | `APROVADO_COM_RESSALVAS` (auto) | Implementacao funcionalmente correta |
| QA Codex (1o ciclo) | `QA_FAILED` | `python tela/teste_loader.py` deixava `tela/__pycache__/` (`loader.cpython-314.pyc`, `__init__.cpython-314.pyc`) no repositorio — viola escopo de arquivos permitidos e criterio de nao deixar bytecode |
| Ajuste local pos-QA | `IMPLEMENTED_POS_QA` | Correcao aplicada em `tela/teste_loader.py` (`sys.dont_write_bytecode = True`) + remocao de `tela/__pycache__/` + atualizacao deste relatorio |

## Arquivos alterados

| Arquivo | Alteracao |
|---|---|
| `tela/__init__.py` | criado (marcador de pacote, vazio) |
| `tela/loader.py` | criado (loader e validador macro) |
| `tela/teste_loader.py` | criado (diagnostico verificavel) |
| `docs/relatorios/IMP-0001-loader-validador-tela-json.md` | criado (este relatorio) |

Nenhum arquivo fora da lista permitida pelo handoff foi criado ou alterado.
Nenhum commit foi feito.

## Comportamento implementado

O modulo `tela/loader.py` implementa a funcao publica:

```python
carregar_tela(caminho_base, id_tela) -> dict
```

que localiza `config/telas/<id_tela>.json` sob `caminho_base`, le o
arquivo, analisa o JSON e executa as validacoes macro obrigatórias na
ordem definida no handoff:

1. arquivo existe — `TelaArquivoNaoEncontrado`;
2. JSON sintaticamente valido — `TelaJsonInvalido`;
3. campo `schema` presente — `TelaCampoObrigatorioAusente(campo="schema")`;
4. campo `id` presente e nao vazio — `TelaCampoObrigatorioAusente(campo="id")`;
5. `id` coincide com o nome base do arquivo (ADR-0009 secao 3) —
   `TelaIdNaoCoincideComArquivo`;
6. para a tela raiz (`id_tela == "orquestrador"`), `id == "orquestrador"` —
   `TelaIdIncorreto`;
7. `cabecalho` presente — `TelaCampoObrigatorioAusente(campo="cabecalho")`;
8. `corpo` presente e objeto — `TelaCampoObrigatorioAusente(campo="corpo")`
   / `TelaEstruturaInvalida`;
9. `barra_de_menus` presente — `TelaCampoObrigatorioAusente(campo="barra_de_menus")`;
10. `corpo.elementos` presente e lista —
    `TelaCampoObrigatorioAusente(campo="corpo.elementos")` /
    `TelaEstruturaInvalida`;
11. cada elemento de `corpo.elementos` possui `id` nao vazio —
    `TelaElementoSemId(indice=N)`;
12. cada elemento possui `tipo` nao vazio — `TelaElementoSemTipo(indice=N, id=X)`;
13. `tipo` pertence a taxonomia fechada `{console, lancador, dashboard}`
    (exposta em `TIPOS_CORPO_VALIDOS`) — `TelaTipoDesconhecido`.

A representacao interna retornada segue o formato minimo sugerido pelo
handoff:

```python
{
    "id": str,
    "schema": str,
    "cabecalho": dict,
    "corpo": {
        "arranjo": str | None,
        "elementos": [ { "id": str, "tipo": str, ...demais inertes } ],
    },
    "barra_de_menus": dict,
    "_raw": dict,   # JSON original completo, para diagnostico
}
```

O caminho base padrao (quando `caminho_base=None`) e computado como o pai
do diretorio `tela/` (raiz do repositorio de scripts), nunca hardcoded
como caminho absoluto do sistema de arquivos.

O script de diagnostico `tela/teste_loader.py` e executavel via
`python tela/teste_loader.py`. Ele:

- define `sys.dont_write_bytecode = True` antes de importar `tela.loader`,
  impedindo a geracao de `__pycache__`/`.pyc` no repositorio (correcao
  pos-QA do 1o ciclo);
- carrega o arquivo real `config/telas/orquestrador.json`;
- imprime `id`, `schema`, `corpo.arranjo` e o par `id`/`tipo` de cada
  elemento de corpo (conforme exigido no handoff);
- cria arquivos JSON temporarios em um diretorio tmp para testar todos
  os casos de erro previstos;
- remove o diretorio tmp ao final;
- retorna codigo de saida `0` se todos os criterios passaram, `1` caso
  contrario.

Apenas biblioteca padrao do Python (`json`, `os`, `pathlib`, `sys`,
`shutil`, `tempfile`).

## Comportamento deliberadamente nao implementado (fora de escopo)

Preservado estritamente como declaracao inerte, sem execucao, sem
resolucao e sem validacao funcional, conforme o handoff:

- renderizacao visual de qualquer regiao;
- navegação real entre telas;
- execucao de acoes declaradas em chips;
- registry de acoes / `referencias_de_acoes`;
- resolucao ou ativacao de `bindings`;
- filtros funcionais (`filtros[]`);
- paginacao funcional;
- selecao funcional;
- dashboard dinamico com dados reais;
- `tela_destino` pendente (incluido `chip_estilo`);
- `origem_dados`/`regra_geracao_itens` pendentes (DOC-B008);
- validacao interna de itens de `console` (DOC-B008);
- validacao de tipos/conteudo de chips (DOC-B009);
- `lancador_principal.itens` vazio;
- alteracoes em `config/telas/orquestrador.json` ou `config/estilo.json`;
- gravacao de qualquer estado de runtime no JSON.

## Evidencia por criterio de aceite

| Criterio do handoff | Evidencia apresentada | Resultado |
|---|---|---|
| `config/telas/orquestrador.json` carregado sem erro | `teste_loader.py` carrega via `carregar_tela(base, "orquestrador")` — saida `[PASSOU] carregar_tela(orquestrador)` | OK |
| JSON invalido gera erro identificavel | caso `invalido.json` com texto corrompido -> `TelaJsonInvalido` (mensagem inclui path e detalhe do parser) | OK |
| `id` ausente gera erro identificando o campo | caso `sem_id` -> `TelaCampoObrigatorioAusente: Campo obrigatorio ausente: id` | OK |
| `id != "orquestrador"` na raiz gera erro | caso `id diverge do basename` -> `TelaIdNaoCoincideComArquivo`; `TelaIdIncorreto` exercitado via instanciacao direta (ver ressalva R-1) | OK |
| Nome base divergente do `id` interno gera erro comparando os valores | caso `arquivo_a.json` com `id="outro_id"` -> `TelaIdNaoCoincideComArquivo: id interno 'outro_id' nao coincide com nome do arquivo 'arquivo_a'` | OK |
| Ausencia de `cabecalho` gera erro | caso `sem_cabecalho` -> `TelaCampoObrigatorioAusente(cabecalho)` | OK |
| Ausencia de `corpo` gera erro | caso `sem_corpo` -> `TelaCampoObrigatorioAusente(corpo)` | OK |
| Ausencia de `barra_de_menus` gera erro | caso `sem_barra` -> `TelaCampoObrigatorioAusente(barra_de_menus)` | OK |
| Ausencia de `corpo.elementos` gera erro | caso `sem_elementos` -> `TelaCampoObrigatorioAusente(corpo.elementos)` | OK |
| Elemento sem `id` gera erro com indice | caso `elem_sem_id` -> `TelaElementoSemId: posicao 0` | OK |
| Elemento sem `tipo` gera erro identificando o elemento | caso `elem_sem_tipo` -> `TelaElementoSemTipo: Elemento 'x' (posicao 0)` | OK |
| Tipo desconhecido gera erro identificando o valor | caso `tipo_desconhecido` com `tipo="tabela"` -> `TelaTipoDesconhecido: 'tabela'` | OK |
| Tipos `console`, `dashboard`, `lancador` aceitos | casos `tipo_ok_console`, `tipo_ok_lancador`, `tipo_ok_dashboard` carregam sem erro | OK |
| `chips`, `bindings`, `referencias_de_acoes`, `filtros` carregados como declaracao inerte | verificacao de `isinstance(...)` em `_raw` no caminho feliz | OK |
| `lancador_principal.itens` vazio nao gera erro | carregamento real do orquestrador.json; `itens == []` preservado | OK |
| `tela_destino == "pendente"` nao gera erro | `chip_estilo.acao.tela_destino == "pendente"` preservado no caminho feliz | OK |
| `origem_dados` pendente nao gera erro | `console_principal.origem_dados.referencia == "pendente"` preservado | OK |
| `teste_loader.py` executavel e relata PASSOU/FALHA | 37 verificacoes, saida textual | OK |
| Saida mostra `id`, `schema`, tipos de elementos, status | bloco "Representacao interna carregada (resumo)" no final do diagnostico | OK |

## Aderencia ao contrato

| Regra contratual | Evidencia | Resultado |
|---|---|---|
| `contrato_tela_json.md` §3 — estrutura macro obrigatoria (`schema`, `id`, `cabecalho`, `corpo`, `barra_de_menus`) | validacoes 3-9 em `carregar_tela` | OK |
| `contrato_tela_json.md` §8 — `corpo.elementos[]`, cada elemento com `id` e `tipo`; taxonomia fechada | validacoes 10-13 em `carregar_tela` | OK |
| `contrato_tela_json.md` §23 — validacao obrigatoria antes de renderizar | `carregar_tela` levanta excecao antes de retornar representacao | OK |
| `contrato_composicao_corpo.md` §3 — taxonomia fechada `console`/`lancador`/`dashboard` | `TIPOS_CORPO_VALIDOS = {"console", "lancador", "dashboard"}` | OK |
| `ADR-0009` §2/§3 — caminho `config/telas/<id>.json` e coincidencia id<->basename | validacao 5; construcao do caminho em `carregar_tela` | OK |
| `ADR-0009` §4 — id canônico `orquestrador` para a raiz | validacao 6 (`TelaIdIncorreto`) | OK |
| `ADR-0008` §2 — estrutura macro fixa; JSON configura, nao redefine | loader apenas le e valida; nao introduz nova regiao | OK |
| `ADR-0008` §6 — `estilo.json` restrito a aparencia global | loader nao le `estilo.json` (fora de escopo deste handoff) | OK |

## Garantias de nao alteracao

| Garantia | Resultado |
|---|---|
| Nenhuma acao real e executada | OK — loader nao conhece o conceito de "acao" funcional |
| Nenhum binding e ativado | OK — `bindings` preservado em `_raw` sem interpretacao |
| Nenhum `tela_destino` pendente e resolvido | OK — preservado como string/dict inerte |
| Nenhum estado de runtime e gravado no JSON | OK — loader somente le |
| `config/telas/orquestrador.json` nao alterado | OK — `git status` nao o lista como modificado |
| `config/estilo.json` nao alterado | OK — `git status` nao o lista |
| Nenhum arquivo em `config/` alterado | OK — `git status` nao lista `config/` |
| Nenhum arquivo em `docs/contratos/`, `docs/adr/`, `docs/handoff/`, `NOMENCLATURA.md`, `INDICE.md`, `backlog.md`, `issues.md` alterado | OK — `git status` nao os lista |
| Nenhum arquivo fora dos 4 permitidos foi criado/alterado | OK — `git status --short` mostra apenas `tela/` e o handoff pre-existente (nao tocado) |

## Comandos de verificação executados

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/estilo.json >/dev/null && echo "estilo.json OK"
python tela/teste_loader.py
echo "teste_loader_exit=$?"
find . -name "__pycache__" -not -path "./.git/*" -print
find . -type f -name "*.pyc" -not -path "./.git/*" -print
git status --short --untracked-files=all
git diff --stat
```

### Resultado `python -m json.tool config/telas/orquestrador.json`

```
orquestrador.json OK
```

### Resultado `python -m json.tool config/estilo.json`

```
estilo.json OK
```

### Resultado `python tela/teste_loader.py` (pos-ajuste QA)

```
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
[PASSOU] arquivo ausente -> TelaArquivoNaoEncontrado - TelaArquivoNaoEncontrado: Arquivo nao encontrado: config/telas/nao_existe.json
[PASSOU] JSON sintaticamente invalido -> TelaJsonInvalido - TelaJsonInvalido: JSON invalido em: config/telas/invalido.json - Expecting property name enclosed in double quotes: line 1 column 3 (char 2)
[PASSOU] sem schema -> TelaCampoObrigatorioAusente(schema) - TelaCampoObrigatorioAusente: Campo obrigatorio ausente: schema
[PASSOU] sem id -> TelaCampoObrigatorioAusente(id) - TelaCampoObrigatorioAusente: Campo obrigatorio ausente: id
[PASSOU] id vazio -> TelaCampoObrigatorioAusente(id) - TelaCampoObrigatorioAusente: Campo obrigatorio ausente: id
[PASSOU] id diverge do basename -> TelaIdNaoCoincideComArquivo - TelaIdNaoCoincideComArquivo: id interno 'outro_id' nao coincide com nome do arquivo 'arquivo_a'
[PASSOU] sem cabecalho -> TelaCampoObrigatorioAusente(cabecalho)
[PASSOU] sem corpo -> TelaCampoObrigatorioAusente(corpo)
[PASSOU] sem barra_de_menus -> TelaCampoObrigatorioAusente(barra_de_menus)
[PASSOU] sem corpo.elementos -> TelaCampoObrigatorioAusente(corpo.elementos)
[PASSOU] corpo.elementos nao e lista -> TelaEstruturaInvalida - TelaEstruturaInvalida: 'corpo.elementos' ausente ou nao e uma lista
[PASSOU] elemento sem id -> TelaElementoSemId - TelaElementoSemId: Elemento na posicao 0 nao possui campo 'id'
[PASSOU] elemento sem tipo -> TelaElementoSemTipo - TelaElementoSemTipo: Elemento 'x' (posicao 0) nao possui campo 'tipo'
[PASSOU] tipo desconhecido -> TelaTipoDesconhecido - TelaTipoDesconhecido: Tipo desconhecido 'tabela' em elemento 'x'; tipos validos: console, lancador, dashboard
[PASSOU] tipo nao string -> TelaElementoSemTipo (reuso da categoria)

== Aceitacao dos tipos validos (taxonomia fechada) ==
[PASSOU] tipo 'console' aceito
[PASSOU] tipo 'lancador' aceito
[PASSOU] tipo 'dashboard' aceito
[PASSOU] TIPOS_CORPO_VALIDOS == {console, lancador, dashboard}

== Excecao TelaIdIncorreto (verificacao de classe) ==
[PASSOU] TelaIdIncorreto instanciavel e mensagem e auditavel - id esperado para tela raiz: 'orquestrador'; encontrado: 'outro'

== Resumo ==
Total de verificacoes: 37
Passaram: 37
Falharam: 0

== Representacao interna carregada (resumo) ==
id: orquestrador
schema: tela.v1
corpo.arranjo: sobreposto
  elemento: id='console_principal' tipo='console'
  elemento: id='dashboard_info' tipo='dashboard'
  elemento: id='lancador_principal' tipo='lancador'
```

Codigo de saida: `teste_loader_exit=0`.

### Resultado `find . -name "__pycache__" -not -path "./.git/*" -print`

```
(vazio)
```

Nenhum diretorio `__pycache__` gerado pela execucao do diagnostico.

### Resultado `find . -type f -name "*.pyc" -not -path "./.git/*" -print`

```
(vazio)
```

Nenhum arquivo `.pyc` gerado pela execucao do diagnostico.

### Resultado `git status --short --untracked-files=all`

```
?? docs/handoff/H-0001-loader-validador-tela-json.md
?? docs/relatorios/IMP-0001-loader-validador-tela-json.md
?? tela/__init__.py
?? tela/loader.py
?? tela/teste_loader.py
```

(o handoff ja existia como artefato nao rastreado antes da implementacao;
`tela/__init__.py`, `tela/loader.py`, `tela/teste_loader.py` sao os arquivos
do pacote criado; o relatorio e este proprio arquivo. Nenhum
`__pycache__`/`.pyc` aparece como nao rastreado.)

### Resultado `git diff --stat`

```
(vazio)
```

Nenhum arquivo rastreado foi modificado.

## Bloqueios

Nenhum bloqueio. Nenhuma decisao sobre DOC-B008 ou DOC-B009 foi exigida pela
implementacao; todos os campos pendentes foram tratados estritamente como
declaracao inerte, conforme o handoff.

## Observacoes para QA

- **R-0 (correcao pos-QA, 1o ciclo).** A QA Codex do 1o ciclo falhou
  porque `python tela/teste_loader.py` deixava
  `tela/__pycache__/{loader.cpython-314.pyc, __init__.cpython-314.pyc}`
  no repositorio, violando o escopo de arquivos permitidos pelo handoff.
  Correcao aplicada: inserida a linha `sys.dont_write_bytecode = True`
  em `tela/teste_loader.py`, antes de qualquer import de `tela.loader`;
  o diretorio `tela/__pycache__/` previamente gerado foi removido do
  filesystem. Verificacao pos-ajuste: `find . -name "__pycache__"` e
  `find . -type f -name "*.pyc"` retornam ambos vazio. A falha era
  local ao diagnostico; o loader (`tela/loader.py`) nao precisou ser
  alterado.
- **R-1 (ressalva menore, sem impacto funcional).** A excecao
  `TelaIdIncorreto` (validacao 6 do handoff) e, com a ordem de validacao
  adotada, inalcancavel na pratica: ela so poderia disparar quando
  `id_tela == "orquestrador"` e `id_interno != "orquestrador"`, mas a
  validacao 5 (`TelaIdNaoCoincideComArquivo`) ja dispara antes nesse
  cenario, porque o basename do arquivo sempre sera `"orquestrador"`. A
  classe e a validacao foram mantidas por fidelidade ao handoff e como
  camada defenciva; o diagnostico exercita a classe por instanciacao
  direta para confirmar que ela existe e produz mensagem auditavel. QA
  pode avaliar se a redundancia deve ser removida em handoff posterior.
- **R-2 (convencao de nomes).** O handoff permite que o implementador
  use dataclasses, TypedDict ou dict. Foi usado `dict` simples, conforme
  a "sugestao minima" do handoff. Nenhuma regra arquitetural nova foi
  introduzida.
- **R-3 (paths).** O caminho base padrao e computado a partir de
  `Path(__file__).resolve().parent.parent` (raiz do repositorio de
  scripts). Nenhum caminho absoluto de sistema de arquivos esta
  hardcoded no codigo.
- **R-4 (sem commit).** Conforme o handoff e o prompt operacional,
  nenhum commit foi feito.
- **R-5 (sem .gitignore).** A correcao foi feita via
  `sys.dont_write_bytecode = True` no diagnostico, conforme orientacao
  do prompt de ajuste. Nenhum `.gitignore` foi criado (seria fora do
  escopo de arquivos permitidos).
