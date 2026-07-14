# Relatório de QA — H-0014 pós-ajuste Orquestrador vertical

## Status

QA_APPROVED_WITH_NOTES

## Contexto

QA pós-ajuste executado antes de `git commit --amend` do H-0014. A revisão
humana apontou que `config/telas/orquestrador.json` ainda mantinha
`corpo.arranjo: "sobreposto"` após o commit do H-0014. O working tree atual
migra esse campo ativo para `"vertical"` e atualiza as expectativas dos testes
de loader/modelo.

## Arquivos lidos

- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md`
- Estado do Git via `git log`, `git status`, `git diff --stat`,
  `git diff --name-only` e diffs restritos de escopo.

## Verificações executadas

```text
git log --oneline -5
git status --short
git diff --stat
git diff --name-only
grep -R '"arranjo"[[:space:]]*:[[:space:]]*"sobreposto"' -n config/telas || true
grep -R '"arranjo"[[:space:]]*:[[:space:]]*"vertical"' -n config/telas/orquestrador.json config/telas/grupo_minimo.json || true
git diff --name-only -- docs/adr docs/contratos docs/NOMENCLATURA.md docs/handoff tela/modelo.py tela/renderizador.py tela/demo.py tela/diagnostico.py config/telas/destino_minimo.json config/telas/stub_b.json
find tela -name '__pycache__' -o -name '*.pyc'
```

Resultados relevantes:

```text
584ef3b feat: migra arranjo vertical e barra declarativa
ceaf0be docs: registra ADRs de arranjo e barra declarativa
ab48702 feat: adiciona acesso demonstravel ao grupo minimo
0bcb477 feat: implementa grupo estrutural minimo em tela isolada
6c91279 docs: cancela H-0011 e remove H-0011A
```

```text
 M config/telas/orquestrador.json
 M docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
 M tela/teste_loader.py
 M tela/teste_modelo.py
```

```text
scripts/config/telas/orquestrador.json             |   2 +-
...4-migracao-pos-adr-arranjo-barra-declarativa.md | 107 +++++++++++++++++++--
scripts/tela/teste_loader.py                       |   2 +-
scripts/tela/teste_modelo.py                       |   4 +-
4 files changed, 105 insertions(+), 10 deletions(-)
```

```text
scripts/config/telas/orquestrador.json
scripts/docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
```

`find tela -name '__pycache__' -o -name '*.pyc'` não retornou saída.

## Testes executados

```text
python tela/teste_loader.py        -> exit 0; 67/67; [FALHOU]=0; sem traceback
python tela/teste_modelo.py        -> exit 0; 53/53; [FALHOU]=0; sem traceback
python tela/teste_renderizador.py  -> exit 0; 112/112; [FALHOU]=0; sem traceback
python tela/teste_diagnostico.py   -> exit 0; 28/28; [FALHOU]=0; sem traceback
python tela/teste_demo.py          -> exit 0; 107/107; [FALHOU]=0; sem traceback
python -m json.tool config/telas/orquestrador.json -> exit 0; JSON válido
python -m json.tool config/telas/grupo_minimo.json -> exit 0; JSON válido
```

## Verificação do arranjo do Orquestrador

Confirmado:

```text
config/telas/orquestrador.json:24:    "arranjo": "vertical",
```

Os testes atualizados também confirmam a coerência:

```text
tela/teste_loader.py: tela.corpo.arranjo preservado - arranjo='vertical'
tela/teste_modelo.py: modelo.corpo.arranjo == 'vertical' - arranjo='vertical'
```

## Verificação de ocorrências remanescentes de sobreposto

Busca executada:

```text
config/telas/destino_minimo.json:9:    "arranjo": "sobreposto",
config/telas/stub_b.json:9:    "arranjo": "sobreposto",
```

Classificação:

| Arquivo | Ocorrência | Classificação | Justificativa |
|---|---|---|---|
| `config/telas/destino_minimo.json` | `corpo.arranjo: "sobreposto"` | ACEITÁVEL | Fora do ajuste pós-QA do Orquestrador e não alterado no working tree. Continua como ocorrência legada fora do fluxo migrado pelo H-0014. |
| `config/telas/stub_b.json` | `corpo.arranjo: "sobreposto"` | ACEITÁVEL | Artefato fora do fluxo migrado pelo H-0014 e não alterado no working tree. |

Nenhuma ocorrência remanescente foi classificada como BLOQUEANTE.

## Verificação de escopo

Escopo alterado antes deste relatório:

```text
config/telas/orquestrador.json
docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
tela/teste_loader.py
tela/teste_modelo.py
```

Validações:

- `orquestrador.json` agora usa `corpo.arranjo: "vertical"`.
- `grupo_minimo.json` continua usando `vertical` em `corpo.arranjo` e no
  grupo interno.
- `destino_minimo.json` e `stub_b.json` ainda têm `sobreposto`, mas não foram
  alterados e ficam fora do escopo desta correção.
- Loader e testes permanecem coerentes com ADR-0011 e H-0014: grupo rejeita
  `horizontal`/`lado_a_lado`; Orquestrador real é esperado como `vertical`.
- Não houve implementação de `horizontal`.
- Não houve adição de segundo elemento ao grupo.
- Não houve alteração em ADRs, contratos, `docs/NOMENCLATURA.md` ou
  `docs/handoff/`.
- `modelo.py`, `renderizador.py`, `demo.py` e `diagnostico.py` permanecem sem
  diff.

## Verificação para amend

O último commit é:

```text
584ef3b feat: migra arranjo vertical e barra declarativa
```

Esse commit corresponde ao H-0014. Portanto, do ponto de vista de QA, o amend
automático do último commit é permitido.

## Achados bloqueantes

0.

## Achados não bloqueantes

1. Permanecem ocorrências legadas de `corpo.arranjo: "sobreposto"` em
   `destino_minimo.json` e `stub_b.json`. Elas foram classificadas como
   aceitáveis por estarem fora do fluxo ajustado pelo H-0014 e fora desta
   correção pós-QA.
2. O relatório de implementação `IMP-0014...` contém uma ressalva futura sobre
   migrar `destino_minimo.json` para consistência total, mas isso não bloqueia
   o amend deste ajuste.

## Conclusão

QA aprovado com notas. A correção pós-ajuste do Orquestrador é válida, os
testes obrigatórios passaram, o JSON está válido, o escopo ficou restrito aos
arquivos esperados e o último commit é o H-0014.

Pode seguir para `git commit --amend`.
