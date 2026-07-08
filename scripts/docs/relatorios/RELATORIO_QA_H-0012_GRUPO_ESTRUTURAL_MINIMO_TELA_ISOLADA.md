# Relatório de QA — H-0012 Grupo estrutural mínimo em tela isolada

## Status

`QA_APPROVED_WITH_NOTES`

## Contexto

QA pós-implementação do H-0012 sobre o handoff
`docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`.

O objetivo auditado foi confirmar que a implementação introduz somente o
grupo estrutural mínimo em tela isolada (`config/telas/grupo_minimo.json`),
mantendo lista plana compatível e preservando Orquestrador, demo,
diagnóstico, contratos, ADRs, NOMENCLATURA e INDICE.

Nenhum código foi implementado nesta etapa de QA. Nenhum commit foi realizado.
Este relatório é o único arquivo criado pelo QA.

## Arquivos lidos

- `docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md`
- `docs/relatorios/LEVANTAMENTO_H-0012_POS_AUDITORIA.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF_POS_AJUSTES.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `config/telas/grupo_minimo.json`
- `config/telas/orquestrador.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/diagnostico.py`
- `tela/demo.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_diagnostico.py`
- `tela/teste_demo.py`

## Escopo verificado

Arquivos criados/alterados pela implementação, conforme `git status --short`:

```text
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? config/telas/grupo_minimo.json
?? docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
?? docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
?? docs/relatorios/LEVANTAMENTO_H-0012_POS_AUDITORIA.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF_POS_AJUSTES.md
```

Os seis arquivos modificados e `config/telas/grupo_minimo.json` estão dentro do
escopo permitido do H-0012. Os demais `??` são documentos de handoff,
auditoria, levantamento e implementação esperados na etapa documental.

## Diff auditado

Comandos obrigatórios:

```bash
git log --oneline -5
```

```text
6c91279 docs: cancela H-0011 e remove H-0011A
a940fbc docs: fecha base documental de composicao hierarquica
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
ec0a59e docs: fecha contratos incrementais de tela json
```

```bash
git diff --stat
```

```text
 scripts/tela/loader.py             |  95 +++++++++++++++++++++-
 scripts/tela/modelo.py             | 107 ++++++++++++++++++++++---
 scripts/tela/renderizador.py       |  64 ++++++++++-----
 scripts/tela/teste_loader.py       | 158 +++++++++++++++++++++++++++++++++++++
 scripts/tela/teste_modelo.py       |  98 +++++++++++++++++++++++
 scripts/tela/teste_renderizador.py | 101 ++++++++++++++++++++++++
 6 files changed, 591 insertions(+), 32 deletions(-)
```

```bash
git diff --name-only
```

```text
scripts/tela/loader.py
scripts/tela/modelo.py
scripts/tela/renderizador.py
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
```

```bash
git diff --name-only -- tela/loader.py tela/modelo.py tela/renderizador.py tela/teste_loader.py tela/teste_modelo.py tela/teste_renderizador.py
```

```text
scripts/tela/loader.py
scripts/tela/modelo.py
scripts/tela/renderizador.py
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
```

```bash
git diff --name-only -- config/telas/orquestrador.json config/telas/destino_minimo.json config/telas/stub_b.json tela/demo.py tela/diagnostico.py tela/teste_demo.py tela/teste_diagnostico.py docs/contratos docs/adr docs/NOMENCLATURA.md docs/INDICE.md
```

Resultado: sem saída. Nenhum arquivo proibido possui diff.

## Verificações de JSON

- `python -m json.tool config/telas/grupo_minimo.json` — exit 0.
- `python -m json.tool config/telas/orquestrador.json` — exit 0.
- `python -m json.tool config/telas/destino_minimo.json` — exit 0.
- `python -m json.tool config/telas/stub_b.json` — exit 0.

`grupo_minimo.json` contém `schema = "tela.v1"`, `id = "grupo_minimo"`, nome
base coerente, exatamente 1 grupo em `corpo.elementos[]`, grupo com
`tipo = "grupo"`, `arranjo = "sobreposto"`, exatamente 1 dashboard interno,
`dashboard.campos[]` operacional e campo literal com valor
`Dashboard dentro de grupo estrutural`.

## Testes executados

- `python tela/teste_loader.py`
  - exit code: 0
  - `[FALHOU]`: ausente
  - traceback: ausente
  - resumo: 61 verificações, 61 passaram, 0 falharam

- `python tela/teste_modelo.py`
  - exit code: 0
  - `[FALHOU]`: ausente
  - traceback: ausente
  - resumo: 49 verificações, 49 passaram, 0 falharam

- `python tela/teste_renderizador.py`
  - exit code: 0
  - `[FALHOU]`: ausente
  - traceback: ausente
  - resumo: 112 verificações, 112 passaram, 0 falharam

- `python tela/teste_diagnostico.py`
  - exit code: 0
  - `[FALHOU]`: ausente
  - traceback: ausente
  - resumo: 28 verificações, 28 passaram, 0 falharam

- `python tela/teste_demo.py`
  - exit code: 0
  - `[FALHOU]`: ausente
  - traceback: ausente
  - resumo: 95 verificações, 95 passaram, 0 falharam

- `python tela/diagnostico.py`
  - exit code: 0
  - `[FALHOU]`: ausente
  - traceback: ausente
  - resumo: renderização padrão do Orquestrador preservada, com saída esperada
    pelos testes estritos de diagnóstico/demo.

Verificação de cache:

```bash
find tela -name '__pycache__' -o -name '*.pyc'
```

Resultado: sem saída. Nenhum cache/bytecode encontrado.

## Verificações funcionais

### Loader

Atendido.

O loader mantém `TIPOS_CORPO_VALIDOS = {"console", "lancador", "dashboard"}` e
introduz `TIPOS_ESTRUTURAIS_VALIDOS = {"grupo"}` separado da taxonomia
funcional. `grupo` não é tratado como quarto tipo funcional.

Coberturas verificadas em código e testes:

- lista plana existente continua válida (`orquestrador`, `destino_minimo`,
  `stub_b`);
- `grupo_minimo` carrega sem erro;
- grupo mínimo é aceito;
- grupo sem `elementos` é rejeitado;
- grupo com `elementos` vazio é rejeitado;
- grupo com 2 elementos é rejeitado;
- grupo aninhado é rejeitado;
- grupo com `arranjo = "lado_a_lado"` é rejeitado;
- tipo interno desconhecido é rejeitado com `TelaTipoDesconhecido`.

### Modelo

Atendido.

`ElementoCorpo` ganhou campo `elementos` com `default_factory=list`. Para
`tipo = "grupo"`, o modelo preserva `id`, `tipo`, `arranjo` em campos inertes
e expõe o dashboard interno como `ElementoCorpo`. Para elementos funcionais
diretos, a lista plana segue com comportamento anterior e `elementos == []`.

Os helpers `elemento_por_id("grupo_principal")` e
`elementos_por_tipo("grupo")` funcionam para o grupo mínimo. A taxonomia
funcional permanece separada: `grupo.tipo` não pertence a
`TIPOS_CORPO_VALIDOS`, enquanto o interno `dashboard` pertence.

### Renderer

Atendido.

O renderer extraiu o despacho funcional para `_caixa_de_elemento`. Para
`tipo = "grupo"`, percorre `elemento.elementos` e renderiza o dashboard interno
com o mesmo mecanismo da lista plana. O grupo não gera caixa própria, título
visual próprio, borda extra nem linha extra.

O teste confirma:

- caixa do dashboard interno aparece;
- valor literal aparece;
- `grupo_principal` não vaza na saída;
- há exatamente 3 caixas em `grupo_minimo` (cabeçalho, dashboard interno,
  menus);
- saída do grupo é igual à saída de uma lista plana equivalente;
- Orquestrador permanece com saída esperada.

Não foi implementado `lado_a_lado`, múltiplos elementos, percentual/fração,
grupo dentro de grupo, `posicao_dashboard` como nova regra ativa, foco,
seleção, navegação por `[✥]`, nova ação ou registry.

### Preservação do Orquestrador

Atendido.

`config/telas/orquestrador.json`, `tela/diagnostico.py`, `tela/demo.py`,
`tela/teste_diagnostico.py` e `tela/teste_demo.py` não possuem diff.

`python tela/diagnostico.py` encerrou com exit 0 e imprime a saída padrão
esperada do Orquestrador. `tela/teste_diagnostico.py` também valida igualdade
estrita com o output literal esperado do H-0010A.

### Preservação de arquivos proibidos

Atendido.

O comando de escopo proibido retornou vazio para:

- `config/telas/orquestrador.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`
- `tela/demo.py`
- `tela/diagnostico.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`
- `docs/contratos/`
- `docs/adr/`
- `docs/NOMENCLATURA.md`
- `docs/INDICE.md`

## Achados bloqueantes

0.

## Achados não bloqueantes

1. Divergência documental já conhecida: o H-0012 usa corretamente o formato
   operacional atual `dashboard.campos[]`, enquanto
   `contrato_json_dashboard.md` ainda descreve envelope mínimo com `conteudo`
   e `regras_exibicao`. O próprio handoff pós-ajustes registra essa
   harmonização como fora de escopo, portanto não bloqueia.

2. O workspace mantém documentos não rastreados da etapa documental
   (`H-0012`, auditorias e levantamento), além do relatório de implementação.
   Isso está previsto no estado esperado e não é violação da implementação.

## Pontos positivos

- Separação clara entre tipo estrutural (`grupo`) e tipos funcionais
  (`console`, `lancador`, `dashboard`).
- Validações negativas do loader cobrem os principais limites do H-0012.
- Modelo expõe o elemento interno sem obrigar o renderer a manipular dict cru.
- Renderer reaproveita o mesmo despacho funcional da lista plana.
- Testes preservam explicitamente Orquestrador, diagnóstico e demo.
- Nenhum arquivo proibido foi alterado.
- Nenhum cache/bytecode foi deixado após a execução dos testes.

## Conclusão

A implementação cumpre o H-0012 sem expandir escopo. Não há achados
bloqueantes. Pode seguir para revisão humana e commit com status
`QA_APPROVED_WITH_NOTES`.
