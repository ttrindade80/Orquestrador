# Relatório de QA — H-0013 Demo de acesso à tela grupo mínimo

## Status

`QA_APPROVED`

## Contexto

QA pós-implementação do H-0013 sobre o handoff
`docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md`.

O objetivo auditado foi confirmar que a implementação torna `grupo_minimo`
acessível pelo fluxo demonstrável a partir do lançador do Orquestrador, sem
avançar para segundo elemento no grupo, sem variar composição, sem implementar
composição horizontal e sem alterar runtime.

Nenhum código foi implementado nesta etapa de QA. Nenhum JSON de produção foi
alterado nesta etapa de QA. Nenhum teste foi alterado nesta etapa de QA.
Nenhum commit foi realizado. Este relatório é o único arquivo criado pelo QA.

## Arquivos lidos

- `docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0013_HANDOFF.md`
- `docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md`
- `docs/relatorios/RELATORIO_QA_H-0012_GRUPO_ESTRUTURAL_MINIMO_TELA_ISOLADA.md`
- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`
- `config/telas/destino_minimo.json`
- `tela/demo.py`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_diagnostico.py`
- `tela/teste_demo.py`

## Escopo verificado

Arquivos criados/alterados pela implementação, conforme `git status --short`
antes da criação deste relatório:

```text
 M config/telas/orquestrador.json
 M tela/teste_demo.py
 M tela/teste_diagnostico.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
?? docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0013_HANDOFF.md
```

Os arquivos modificados estão dentro da lista de alteração obrigatória ou
condicional permitida do H-0013. Os documentos não rastreados são os documentos
H-0013 esperados no ciclo.

Este relatório de QA foi criado nesta etapa:

- `docs/relatorios/RELATORIO_QA_H-0013_DEMO_ACESSO_TELA_GRUPO_MINIMO.md`

## Diff auditado

`git log --oneline -5`:

```text
0bcb477 feat: implementa grupo estrutural minimo em tela isolada
6c91279 docs: cancela H-0011 e remove H-0011A
a940fbc docs: fecha base documental de composicao hierarquica
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
```

`git diff --stat`:

```text
 scripts/config/telas/orquestrador.json |   6 ++
 scripts/tela/teste_demo.py             | 149 +++++++++++++++++++++++++++++++++
 scripts/tela/teste_diagnostico.py      |   1 +
 scripts/tela/teste_loader.py           |  39 ++++++++-
 scripts/tela/teste_modelo.py           |  33 ++++++--
 scripts/tela/teste_renderizador.py     |   2 +
 6 files changed, 222 insertions(+), 8 deletions(-)
```

`git diff --name-only`:

```text
scripts/config/telas/orquestrador.json
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
```

Diff específico de `config/telas/orquestrador.json`: a implementação adiciona
somente o item abaixo após `item_destino_minimo`:

```diff
+          },
+          {
+            "id": "item_grupo_minimo",
+            "chip": "g",
+            "texto": "Grupo Min.",
+            "tela_destino": "grupo_minimo"
```

Verificação de ausência de diff nos runtime proibidos:

```bash
git diff -- tela/demo.py tela/loader.py tela/modelo.py tela/renderizador.py tela/diagnostico.py
```

Resultado: sem saída. Não houve alteração em runtime proibido.

Verificação de ausência de diff em JSONs proibidos:

```bash
git diff -- config/telas/grupo_minimo.json config/telas/destino_minimo.json
```

Resultado: sem saída. `grupo_minimo.json` e `destino_minimo.json` permaneceram
inalterados.

Verificação de ausência de diff em contratos, ADRs, NOMENCLATURA e INDICE:

```bash
git diff -- docs/contratos docs/adr docs/NOMENCLATURA.md docs/INDICE.md
```

Resultado: sem saída. Não houve alteração nesses documentos.

## Verificações de JSON

- `python -m json.tool config/telas/orquestrador.json` — exit 0.

Confirmações por inspeção:

- `item_destino_minimo` foi preservado.
- `item_destino_minimo.chip == "d"`.
- `item_destino_minimo.tela_destino == "destino_minimo"`.
- `item_grupo_minimo` foi adicionado.
- `item_grupo_minimo.chip == "g"`.
- `item_grupo_minimo.texto == "Grupo Min."`.
- `len("Grupo Min.") == 10`, portanto dentro do limite `<= 15`.
- `item_grupo_minimo.tela_destino == "grupo_minimo"`.

## Testes executados

- `python tela/teste_loader.py`
  - exit code: 0
  - resumo: 66 verificações, 66 passaram, 0 falharam
  - `[FALHOU]`: ausente
  - traceback: ausente

- `python tela/teste_modelo.py`
  - exit code: 0
  - resumo: 53 verificações, 53 passaram, 0 falharam
  - `[FALHOU]`: ausente
  - traceback: ausente

- `python tela/teste_renderizador.py`
  - exit code: 0
  - resumo: 112 verificações, 112 passaram, 0 falharam
  - `[FALHOU]`: ausente
  - traceback: ausente

- `python tela/teste_diagnostico.py`
  - exit code: 0
  - resumo: 28 verificações, 28 passaram, 0 falharam
  - `[FALHOU]`: ausente
  - traceback: ausente

- `python tela/teste_demo.py`
  - exit code: 0
  - resumo: 107 verificações, 107 passaram, 0 falharam
  - `[FALHOU]`: ausente
  - traceback: ausente

## Verificações funcionais

### Lançador do Orquestrador

Atendido.

`lancador_principal.itens[]` agora contém dois itens:

- `item_destino_minimo`, com `chip = "d"` e `tela_destino = "destino_minimo"`;
- `item_grupo_minimo`, com `chip = "g"` e `tela_destino = "grupo_minimo"`.

O item novo foi anexado depois do item existente. O item existente não foi
removido, renomeado nem reordenado.

### Rota `grupo_minimo`

Atendido.

A sondagem direta confirmou que o comando `g` no Orquestrador muda
`tela_atual` para `grupo_minimo`, empilha `orquestrador` em `pilha_telas` e
mantém `saindo = False`. Também confirmou que Esc em `grupo_minimo` retorna
para `orquestrador`, esvazia a pilha e não marca saída.

O teste de subprocess em `tela/teste_demo.py` cobre
`g\n\x1b\n\x1b\n` e confirmou três renders: Orquestrador, `grupo_minimo`,
Orquestrador. A saída contém `GRUPO MINIMO` e `[Esc] Voltar`, com stderr vazio.

### Preservação de `destino_minimo`

Atendido.

A sondagem direta confirmou que `d` continua navegando para `destino_minimo`
e empilhando `orquestrador`. Os testes existentes de navegação via subprocess
para `d\n\x1b\n\x1b\n` continuam passando e confirmam retorno ao
Orquestrador por Esc.

### Preservação dos controles globais da demo

Atendido.

Esc na raiz continua definindo `saindo = True` com pilha vazia. O comando `b`
continua alternando `tipo_borda`; a sondagem direta confirmou alternância para
`reta` enquanto `tela_atual = "grupo_minimo"` e `pilha_telas = ["orquestrador"]`.

### Preservação de `grupo_minimo`

Atendido.

`grupo_minimo.json` não teve diff. A tela continua com `corpo.elementos[]`
contendo exatamente um `grupo`, e esse grupo contém exatamente um elemento
interno do tipo `dashboard`. Nenhum segundo elemento foi adicionado ao grupo.
Nenhuma composição horizontal foi implementada.

### Preservação de runtime

Atendido.

Não houve diff em:

- `tela/demo.py`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/diagnostico.py`

O chip `g` foi usado apenas como valor declarativo em item existente do
`lancador_principal.itens[]`, aproveitando o binding já existente em
`processar_comando`.

### Preservação documental e arquitetural

Atendido.

Não houve alteração em:

- `docs/contratos/`
- `docs/adr/`
- `docs/NOMENCLATURA.md`
- `docs/INDICE.md`
- H-0011
- H-0011A

O H-0013 não reabre H-0011, não recria H-0011A e não cria micro-handoff
derivado.

## Verificação de cache

Durante a execução dos testes foi gerado `tela/__pycache__/`. O artefato foi
removido ao final da auditoria para limpar o workspace.

Verificação final:

```bash
find tela -type d -name __pycache__ -print
find tela -type f -name '*.pyc' -print
```

Resultado: sem saída. Nenhum cache/bytecode permaneceu no workspace.

## Achados bloqueantes

0.

## Achados não bloqueantes

0.

## Pontos positivos

- Mudança de produção restrita a `config/telas/orquestrador.json`.
- Runtime permaneceu intacto.
- Rota nova para `grupo_minimo` coberta por testes unitários e subprocess.
- Rota antiga para `destino_minimo` preservada por testes.
- `grupo_minimo` não foi expandido.
- O chip `g` foi usado apenas como valor declarativo de item já suportado.
- Nenhum cache/bytecode permaneceu no workspace após limpeza.

## Decisão final

`QA_APPROVED`

A implementação do H-0013 está coerente com o handoff, não altera runtime
proibido, preserva `destino_minimo`, expõe `grupo_minimo` pelo fluxo
demonstrável e mantém o grupo estrutural mínimo com exatamente um elemento
interno. Não foram encontrados achados bloqueantes nem não bloqueantes.
