# Relatório de QA — H-0014 Migração pós-ADR: arranjo e barra declarativa

## Status

QA_APPROVED_WITH_NOTES

## Contexto

Auditoria pós-implementação do H-0014 no projeto `orquestrador_novo`, a partir do handoff `docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md`, da auditoria aprovada do handoff e do relatório `IMP-0014`.

Objetivo verificado: migrar `grupo_minimo` para arranjo canônico `vertical`, reduzir a `barra_de_menus` do Orquestrador aos chips aplicáveis, preservar ausência de grupo com 2 elementos/horizontal/aninhamento e não migrar o Orquestrador inteiro para grupo.

## Arquivos lidos

- `docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0014_HANDOFF.md`
- `docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `config/telas/grupo_minimo.json`
- `config/telas/orquestrador.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/demo.py`
- `tela/diagnostico.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`

## Verificações executadas

```bash
git status --short
```

Resultado antes da criação deste relatório:

```text
 M config/telas/grupo_minimo.json
 M config/telas/orquestrador.json
 M tela/loader.py
 M tela/teste_demo.py
 M tela/teste_diagnostico.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md
?? docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0014_HANDOFF.md
```

```bash
git diff --stat
```

Resultado:

```text
 scripts/config/telas/grupo_minimo.json |  4 +-
 scripts/config/telas/orquestrador.json | 99 ----------------------------------
 scripts/tela/loader.py                 | 12 +++--
 scripts/tela/teste_demo.py             | 27 ----------
 scripts/tela/teste_diagnostico.py      |  9 ----
 scripts/tela/teste_loader.py           | 21 +++++---
 scripts/tela/teste_modelo.py           |  8 +--
 scripts/tela/teste_renderizador.py     | 22 +-------
 8 files changed, 31 insertions(+), 171 deletions(-)
```

```bash
git diff --name-only
```

Resultado:

```text
scripts/config/telas/grupo_minimo.json
scripts/config/telas/orquestrador.json
scripts/tela/loader.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
```

## Testes executados

| Comando | Resultado |
|---|---|
| `python tela/teste_loader.py` | exit 0; 67/67; sem `[FALHOU]`; sem traceback |
| `python tela/teste_modelo.py` | exit 0; 53/53; sem `[FALHOU]`; sem traceback |
| `python tela/teste_renderizador.py` | exit 0; 112/112; sem `[FALHOU]`; sem traceback |
| `python tela/teste_diagnostico.py` | exit 0; 28/28; sem `[FALHOU]`; sem traceback |
| `python tela/teste_demo.py` | exit 0; 107/107; sem `[FALHOU]`; sem traceback |
| `python -m json.tool config/telas/orquestrador.json` | exit 0; JSON válido |
| `python -m json.tool config/telas/grupo_minimo.json` | exit 0; JSON válido |

## Verificação de escopo

Escopo aprovado.

Os arquivos modificados por `git diff --name-only` ficam restritos ao conjunto permitido: `grupo_minimo.json`, `orquestrador.json`, `loader.py` e testes. Não há diff em `docs/adr/`, `docs/contratos/`, `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `config/telas/destino_minimo.json`, `tela/modelo.py`, `tela/renderizador.py`, `tela/demo.py` nem `tela/diagnostico.py`.

O diff confirma que:

- `grupo_minimo.json` alterou somente `corpo.arranjo` e `grupo_principal.arranjo` de `"sobreposto"` para `"vertical"`;
- `orquestrador.json` reduziu `barra_de_menus.chips[]` de 11 para 2 chips;
- `loader.py` alterou somente a validação/documentação local de grupo para rejeitar `"horizontal"` e `"lado_a_lado"`;
- testes foram atualizados para o novo arranjo/chips declarados.

Não houve segundo elemento no grupo, grupo com 2 elementos, arranjo horizontal implementado, lado a lado, aninhamento de grupos, novo tipo funcional, novo registry, novo mecanismo de chip, console real, foco, seleção, navegação por `[✥]` ou migração do Orquestrador inteiro para grupo.

## Verificação de arranjo vertical

Aprovado.

`config/telas/grupo_minimo.json` declara:

- `corpo.arranjo == "vertical"`;
- `corpo.elementos[0].id == "grupo_principal"`;
- `corpo.elementos[0].arranjo == "vertical"`;
- exatamente 1 elemento interno, `dashboard_conteudo`;
- nenhuma ocorrência de `"sobreposto"`.

`python tela/teste_loader.py` carrega `grupo_minimo` sem erro, e `python tela/teste_modelo.py` confirma preservação do `arranjo` do grupo como `"vertical"`.

## Verificação de sobreposto residual

ACEITÁVEL — sobreposto residual inerte/fora do escopo.

Evidência:

- `grupo_minimo.json` não contém `"sobreposto"`;
- `orquestrador.json`, `destino_minimo.json` e `stub_b.json` ainda contêm `"sobreposto"` em `corpo.arranjo`;
- o handoff H-0014 explicitamente orienta não migrar/remover `"sobreposto"` desses JSONs e não adicionar validação de vocabulário para `corpo.arranjo` no nível macro;
- `loader.py` continua preservando `corpo.arranjo` macro inertemente;
- os testes confirmam que `orquestrador`, `destino_minimo` e `stub_b` continuam carregando sem erro.

O loader não normaliza nem rejeita `"sobreposto"` em grupo. Como não há JSON ativo de grupo com `"sobreposto"` após a migração, isso permanece compatível com o H-0014. A decisão de remover aliases transicionais de modo mais amplo pertence a ciclo futuro.

## Verificação de horizontal

Aprovado.

`horizontal` não foi implementado como renderização nova. A única mudança relacionada é a rejeição explícita em `_validar_grupo`:

```python
if arranjo in ("horizontal", "lado_a_lado"):
    raise TelaGrupoInvalido(...)
```

`python tela/teste_loader.py` cobre:

- grupo com `arranjo: "horizontal"` rejeitado com `TelaGrupoInvalido`;
- grupo com `arranjo: "lado_a_lado"` rejeitado com `TelaGrupoInvalido`;
- grupo com `arranjo: "vertical"` aceito;
- grupo sem `arranjo` aceito.

## Verificação da barra_de_menus do Orquestrador

Aprovado.

`config/telas/orquestrador.json` contém exatamente 2 chips em `barra_de_menus.chips[]`:

- `chip_esc`, tecla `Esc`, texto `Sair`;
- `chip_ajuda`, tecla `?`, texto `Ajuda`.

Os 9 chips removidos não aparecem mais na barra do Orquestrador: `[<>]`, `[-+]`, `[#]`, `[⇆]`, `[✥]`, `[␣]`, `[⏎]`, `[|]`, `[V]`.

`g` e `d` permanecem como chips de itens do `lancador_principal.itens[]`, não como chips da `barra_de_menus`:

- `d -> destino_minimo`;
- `g -> grupo_minimo`.

`modelo.py`, `renderizador.py`, `loader.py` e `demo.py` não inventam chips. `renderizador.py` percorre `barra_de_menus.get("chips", [])`; os testes atualizados não exigem conjunto global obrigatório de chips.

## Verificação do fluxo demonstrável

Aprovado por testes automatizados em `python tela/teste_demo.py`.

Confirmado:

- `g` abre `grupo_minimo`;
- `d` abre `destino_minimo`;
- `b` alterna borda;
- `Esc` em `grupo_minimo` volta para Orquestrador;
- `Esc` em `destino_minimo` volta para Orquestrador;
- `Esc` na raiz sai.

## Verificação de cache/bytecode

```bash
find tela -name '__pycache__' -o -name '*.pyc'
```

Resultado: sem saída. Critério atendido.

## Achados bloqueantes

0.

## Achados não bloqueantes

1. `sobreposto` residual permanece em `orquestrador.json`, `destino_minimo.json` e `stub_b.json`, mas é aceitável porque o H-0014 manda preservar esses usos inertemente fora do escopo.
2. O pedido de QA apontou possível inconsistência no resumo do implementador. A verificação com `git diff --name-only` mostra que `modelo.py`, `renderizador.py`, `demo.py` e `diagnostico.py` não foram alterados; apenas seus arquivos de teste correspondentes aparecem no diff. Classificação: erro/ambiguidade textual não bloqueante no IMP-0014, sem extrapolação técnica.

## Pontos positivos

- Migração de `grupo_minimo` ficou mínima e declarativa.
- Redução da barra do Orquestrador está alinhada à ADR-0012.
- Testes cobrem rejeição de `horizontal` e preservam o fluxo demonstrável.
- Arquivos proibidos não foram alterados.
- Não há cache/bytecode residual.

## Conclusão

QA aprovado com notas não bloqueantes. A implementação cumpre H-0014, não extrapola escopo e pode seguir para revisão humana e commit.
