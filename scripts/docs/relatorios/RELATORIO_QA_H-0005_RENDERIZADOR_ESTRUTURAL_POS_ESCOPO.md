# RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL_POS_ESCOPO

Status final revisado: QA_APPROVED_WITH_NOTES
Data: 2026-07-07
QA: Codex
Ciclo: H-0005 — Renderer estrutural mínimo da tela raiz
Tipo: revisão complementar pontual de escopo Git

---

## 1. Identificação da revisão

Revisão complementar do QA do ciclo **H-0005 — Renderer estrutural mínimo da tela raiz**.

Escopo desta revisão: reavaliar apenas o bloqueio de escopo Git apontado no QA anterior, distinguindo artefatos pré-implementação do ciclo H-0005, artefatos da implementação, artefatos de QA e arquivos realmente fora do escopo aprovado.

Não houve reimplementação, correção de código, alteração de contratos, ADRs, NOMENCLATURA, configs, handoffs ou documentação normativa.

## 2. Referência ao QA anterior

Relatório anterior:

- `docs/relatorios/RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL.md`
- Status anterior: `QA_REJECTED`

Motivo do bloqueio anterior: o QA classificou como bloqueantes dois arquivos não rastreados:

- `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md`

## 3. Motivo da revisão

A revisão humana de escopo classificou esses dois arquivos como artefatos esperados do próprio ciclo H-0005, criados antes da implementação:

- o handoff foi criado na etapa de handoff;
- o relatório de auditoria foi criado na etapa de auditoria do handoff;
- ambos precedem a implementação do GLM/OpenCode;
- portanto, não são evidência de alteração fora do escopo pela implementação.

Eles continuam sendo arquivos a incluir no commit final do ciclo, mas não caracterizam violação do escopo do executor de implementação.

## 4. Arquivos lidos

Arquivos lidos nesta revisão:

- `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md`
- `docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md`
- `docs/relatorios/RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL.md`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `tela/teste_diagnostico.py`
- `tela/diagnostico.py`
- `tela/modelo.py`
- `config/telas/orquestrador.json`

`tela/teste_loader.py` e `tela/teste_modelo.py` foram executados para regressão mínima, mas não foram reabertos para leitura de conteúdo.

Não foram lidos contratos, ADRs, `NOMENCLATURA.md`, índices ou restante do projeto.

## 5. Comandos executados

Comandos obrigatórios de escopo:

```text
$ git status --short
 M tela/renderizador.py
 M tela/teste_diagnostico.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
?? docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL.md
```

```text
$ git diff --name-only
scripts/tela/renderizador.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_renderizador.py
```

```text
$ git diff --stat
 scripts/tela/renderizador.py       |  46 +++++++++-------
 scripts/tela/teste_diagnostico.py  |  91 ++++++++++++++++---------------
 scripts/tela/teste_renderizador.py | 108 ++++++++++++++++++-------------------
 3 files changed, 128 insertions(+), 117 deletions(-)
```

Regressão mínima:

```text
$ python tela/teste_loader.py
EXIT=0
Total de verificacoes: 37
Passaram: 37
Falharam: 0
```

```text
$ python tela/teste_modelo.py
EXIT=0
Total de verificacoes: 30
Passaram: 30
Falharam: 0
```

```text
$ python tela/teste_renderizador.py
EXIT=0
Total de verificacoes: 39
Passaram: 39
Falharam: 0
```

```text
$ python tela/teste_diagnostico.py
EXIT=0
Total de verificacoes: 27
Passaram: 27
Falharam: 0
```

```text
$ python tela/diagnostico.py
EXIT=0
Saida estrutural H-0005 impressa com REGIAO: cabecalho, REGIAO: corpo e REGIAO: barra_de_menus.
```

```text
$ python -m json.tool config/telas/orquestrador.json >/dev/null
EXIT=0
```

```text
$ git diff -- config/
EXIT=0
Saida vazia.
```

```text
$ find tela -type d -name '__pycache__' -print
EXIT=0
Saida vazia.
```

```text
$ find tela -type f -name '*.pyc' -print
EXIT=0
Saida vazia.
```

## 6. Classificação item a item do `git status --short`

| Item | Classificação | Justificativa |
|---|---|---|
| `M tela/renderizador.py` | `ARTEFATO_IMPLEMENTACAO_H0005` | Arquivo autorizado pelo handoff para alterar o renderer para o formato estrutural H-0005. |
| `M tela/teste_diagnostico.py` | `ARTEFATO_IMPLEMENTACAO_H0005` | Arquivo autorizado pelo handoff para atualizar verificações de formato dependentes do H-0003. |
| `M tela/teste_renderizador.py` | `ARTEFATO_IMPLEMENTACAO_H0005` | Arquivo autorizado pelo handoff para validar o novo formato H-0005. |
| `?? docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md` | `ARTEFATO_PRE_IMPLEMENTACAO_H0005` | Artefato de handoff do próprio ciclo, criado antes da implementação. |
| `?? docs/relatorios/IMP-0005-renderizador-estrutural-tela-raiz.md` | `ARTEFATO_IMPLEMENTACAO_H0005` | Relatório IMP autorizado como artefato da implementação H-0005. |
| `?? docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md` | `ARTEFATO_PRE_IMPLEMENTACAO_H0005` | Relatório de auditoria do handoff, criado antes da implementação. |
| `?? docs/relatorios/RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL.md` | `ARTEFATO_QA_H0005` | Relatório produzido pelo QA anterior. |

Após a criação deste relatório complementar, o caminho abaixo também deve ser classificado como `ARTEFATO_QA_H0005`:

- `docs/relatorios/RELATORIO_QA_H-0005_RENDERIZADOR_ESTRUTURAL_POS_ESCOPO.md`

## 7. Arquivo realmente fora de escopo

Não foi encontrado arquivo realmente fora do escopo aprovado após distinguir:

1. artefatos pré-implementação do ciclo H-0005;
2. artefatos produzidos pela implementação;
3. artefatos produzidos pelo QA.

`git diff --name-only` e `git diff --stat` mostram somente os três arquivos rastreados de implementação autorizados:

- `scripts/tela/renderizador.py`
- `scripts/tela/teste_diagnostico.py`
- `scripts/tela/teste_renderizador.py`

Não há alteração em `config/`.

## 8. Reavaliação do bloqueio anterior

O bloqueio anterior foi **reclassificado**.

Os dois arquivos que motivaram o `QA_REJECTED` anterior:

- `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md`

não devem ser tratados como arquivos alterados pela implementação nem como violação do escopo do GLM/OpenCode, pois são artefatos pré-implementação esperados do próprio ciclo H-0005.

Portanto, o bloqueio de escopo Git do QA anterior não se sustenta após a distinção temporal indicada pela revisão humana.

## 9. Reavaliação do IMP-0005

O IMP-0005 declara aderência de escopo e contém formulações como:

- somente arquivos permitidos foram alterados;
- nenhum arquivo fora do escopo foi alterado;
- os arquivos de handoff/auditoria já estavam presentes antes da implementação.

Interpretação desta revisão: essas declarações devem ser lidas como declarações sobre a implementação do GLM/OpenCode, não sobre todos os artefatos não rastreados do ciclo H-0005.

Após separar os artefatos pré-implementação, a declaração não é objetivamente falsa quanto à implementação. Porém, a redação é ambígua porque pode ser lida como declaração sobre o estado Git completo, incluindo artefatos não rastreados pré-implementação.

Classificação: `NAO_BLOQUEANTE`.

Recomendação: ajuste documental opcional no IMP-0005 antes do commit para explicitar que a afirmação de escopo se refere à implementação e que o handoff e a auditoria são artefatos pré-implementação do ciclo.

## 10. Achados

### BLOQUEANTE

Nenhum achado bloqueante.

### NAO_BLOQUEANTE

1. O IMP-0005 tem redação ambígua sobre escopo Git quando lido contra o estado completo de arquivos não rastreados. Após a distinção temporal, a declaração é aceitável como referência à implementação, mas merece ajuste documental opcional antes do commit.

### OBSERVACAO

1. A implementação funcional já aprovada no QA anterior continua válida: testes de loader, modelo, renderizador, diagnóstico e executável passaram.
2. `git diff -- config/` não produziu saída; não houve alteração em configuração.
3. Não há `__pycache__` nem `.pyc` residual em `tela/`.
4. O relatório complementar atual é artefato de QA do próprio ciclo e deve ser incluído no conjunto final de artefatos se a revisão humana assim decidir.

## 11. Decisão final revisada

`QA_APPROVED_WITH_NOTES`

Justificativa:

- os únicos arquivos fora da implementação são artefatos esperados do próprio ciclo H-0005 ou artefatos de QA;
- os testes obrigatórios passam;
- não há alteração em `config/`;
- não há cache/bytecode residual;
- a implementação funcional já aprovada no QA anterior continua válida;
- resta apenas nota não bloqueante sobre ambiguidade documental do IMP-0005.

## 12. Recomendação objetiva de próxima ação

O ciclo H-0005 pode seguir para revisão humana/commit.

Antes do commit, recomenda-se opcionalmente ajustar o IMP-0005 para deixar explícito que a afirmação de ausência de arquivo fora de escopo se refere à implementação do GLM/OpenCode, enquanto `docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md` e `docs/relatorios/RELATORIO_AUDITORIA_H-0005_HANDOFF.md` são artefatos pré-implementação do próprio ciclo.
