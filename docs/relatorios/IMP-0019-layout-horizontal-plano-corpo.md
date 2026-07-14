# IMP-0019 — Layout horizontal plano do corpo

## Status

```
IMPLEMENTATION_COMPLETE_WITH_NOTES
```

## Base verificada

| Item | Valor |
|---|---|
| HEAD no início | `9d4c74d  docs: formaliza composicao hierarquica do corpo` |
| Commit base esperado | `9d4c74d  docs: formaliza composicao hierarquica do corpo` |
| Coincidência | SIM |
| Workspace no início | ` M docs/handoff/H-0019-layout-horizontal-plano-corpo.md` + `?? RELATORIO_REVISAO_H-0019*` + `?? RELATORIO_AUDITORIA_H-0019_POS_REVISAO*` |
| Workspace esperado | Coincide exatamente |

## Arquivos alterados

| Arquivo | Ação |
|---|---|
| `tela/loader.py` | Modificado — constante `ARRANJOS_CORPO_VALIDOS` + validação de `corpo.arranjo` |
| `tela/renderizador.py` | Modificado — `_montar_corpo_horizontal` + branch em `renderizar_tela` |
| `tela/teste_loader.py` | Modificado — função `teste_arranjo_corpo_h0019` (10 verificações) |
| `tela/teste_renderizador.py` | Modificado — classe `TestArranjoH0019` (35 verificações) |
| `docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md` | Criado (este relatório) |

Arquivos NÃO alterados (conforme escopo proibido):

```
tela/modelo.py                           → NÃO alterado
tela/demo.py                             → NÃO alterado
tela/diagnostico.py                      → NÃO alterado
tela/teste_demo.py                       → NÃO alterado
tela/teste_diagnostico.py               → NÃO alterado
tela/explorar_barra_de_menus.py         → NÃO alterado
tela/teste_explorar_barra_de_menus.py   → NÃO alterado
config/telas/orquestrador.json          → NÃO alterado
config/telas/grupo_minimo.json          → NÃO alterado
config/telas/destino_minimo.json        → NÃO alterado
config/telas/stub_b.json                → NÃO alterado
docs/handoff/H-0019-*.md               → NÃO alterado
docs/relatorios/RELATORIO_AUDITORIA_*  → NÃO alterado
docs/relatorios/RELATORIO_REVISAO_*    → NÃO alterado
docs/NOMENCLATURA.md                    → NÃO alterado
docs/adr/ (todos)                       → NÃO alterado
docs/contratos/ (todos)                 → NÃO alterado
```

## Resumo da implementação

H-0019 adicionou suporte a `corpo.arranjo = "horizontal"` com particionamento
contíguo da largura disponível entre filhos diretos de `corpo.elementos[]`.
A implementação é o menor ciclo funcional verificável que abre o eixo de
layout horizontal do corpo:

1. `loader.py` passa a validar `corpo.arranjo` com conjunto de valores aceitos;
2. `renderizador.py` lê `modelo.corpo.arranjo`, normaliza aliases e aplica
   particionamento horizontal contíguo quando declarado;
3. Baseline 544/544 preservado; 45 novos casos adicionados (total 589/589).

## Decisões locais de implementação

**JSON novo vs fixture in-memory**: Opção B adotada. Todos os testes do renderer
usam `ModeloTela` construído sinteticamente (in-memory), sem criar novo arquivo
JSON em disco. Isso mantém a menor superfície de mudança e evita dependência de
fixture em disco para o novo comportamento.

**Migração de aliases** (`destino_minimo.json` e `stub_b.json` de `"sobreposto"`
para `"vertical"`): **NÃO realizada** neste ciclo. Ambos os arquivos continuam
com `"arranjo": "sobreposto"` e passam na validação do loader (alias aceito). A
migração fica como pendência declarada abaixo.

**Distribuição**: Opção A adotada — distribuição uniforme implícita (modo `igual`)
entre filhos diretos de `corpo.elementos[]`. Nenhum campo `distribuicao` é lido
ou exigido no JSON neste ciclo. Compatível com:

- `contrato_json_tela_minima.md` seção 6.3 (`distribuicao` ausente = modo `igual`);
- ADR-0015 Decisão 6 (modo `igual` é válido);
- JSONs existentes que não declaram `distribuicao` no `corpo`.

## Compatibilidade com ADR-0015

| Decisão ADR-0015 | Tratamento no H-0019 |
|---|---|
| D1 — Corpo como árvore | `_montar_corpo_horizontal` itera sobre `corpo.elementos[]` sem expansão de nós |
| D2 — Grupo como nó estrutural | `_caixa_de_elemento` retorna `None` para grupo; área fica vazia (linhas=[]) |
| D3 — Nível | H-0019 opera somente no nível 1 (filhos diretos de `corpo`) |
| D4 — Arranjo por container | `corpo.arranjo = "horizontal"` declarado no container raiz |
| D5 — Distribuição por container | Opção A: modo `igual` implícito; `distribuicao` não lido |
| D6 — Modos de distribuição | Modo `igual` adotado |
| D8 — Arredondamento determinístico | `base_w + (1 if i < resto else 0)` nas primeiras `resto` áreas |
| D9 — Contato entre molduras | Concatenação direta; bordas adjacentes `││`, `╮╭`, `╯╰` natural |
| D10 — Preenchimento de área alocada | `linhas.append(" " * larguras[i])` para altura menor |
| D13 — Terminal muito pequeno | `RenderizadorErro` determinístico; `...` fora de escopo |

## Política de distribuição aplicada

```
Opção A — Sem distribuicao explícita neste ciclo. Foi aplicada distribuição
uniforme implícita entre filhos diretos de corpo.elementos[] no container
raiz corpo. Distribuição percentual/fração fica fora do escopo.
```

## Detalhes por módulo

### `tela/loader.py`

**Constante adicionada** (nível de módulo, antes de `_ID_TELA_RAIZ`):

```python
ARRANJOS_CORPO_VALIDOS = {None, "vertical", "horizontal", "sobreposto", "lado_a_lado"}
```

**Validação adicionada** (após `arranjo = corpo.get("arranjo")`):

```python
if arranjo not in ARRANJOS_CORPO_VALIDOS:
    raise TelaEstruturaInvalida(
        "corpo.arranjo invalido: {0!r}; valores aceitos: "
        "vertical, horizontal, sobreposto (alias), lado_a_lado (alias)".format(arranjo)
    )
```

**Preservado integralmente**: `_validar_grupo` (que rejeita `"horizontal"` e
`"lado_a_lado"` em grupos — validação de GRUPOS, não de nível de tela).

### `tela/renderizador.py`

**Função auxiliar adicionada** (antes de `renderizar_tela`):
`_montar_corpo_horizontal(elementos, borda, total_w)`.

Algoritmo:
1. N=0 → retorna `""`
2. N=1 → `_caixa_de_elemento` na largura total (sem particionamento)
3. N≥2 → `larguras = [total_w//N + (1 if i < resto else 0) for i in range(N)]`
4. Verifica cabimento mínimo (`w >= 10` por área)
5. Renderiza cada filho com `_caixa_de_elemento(..., w-2, w-3, w-4)`
6. Grupo retorna `None` → `linhas_area = []` (área vazia)
7. Normaliza altura: preenche com `" " * larguras[i]` até `altura_max`
8. Concatena linha a linha sem separador externo

**Branch adicionado em `renderizar_tela`** (substitui o laço de corpo):

```python
arranjo_corpo = modelo.corpo.arranjo
if arranjo_corpo == "sobreposto":
    arranjo_corpo = "vertical"
if arranjo_corpo == "lado_a_lado":
    arranjo_corpo = "horizontal"

if arranjo_corpo == "horizontal":
    bloco_horizontal = _montar_corpo_horizontal(
        modelo.corpo.elementos, borda, total_w
    )
    if bloco_horizontal:
        partes.append(bloco_horizontal)
else:
    # Comportamento atual preservado integralmente (vertical/None/sobreposto)
    for elemento in modelo.corpo.elementos:
        ...
```

**Interação com H-0015** (`altura` explícita): o bloco horizontal é uma string
multi-linha appended a `partes` — exatamente como qualquer outra caixa de corpo.
`_contar_linhas(bloco_horizontal)` retorna `altura_max` corretamente.
`l_corpo_conteudo = sum(_contar_linhas(p) for p in partes[1:])` funciona sem alteração.

**Grupo não é expandido**: no branch horizontal, `_caixa_de_elemento` retorna
`None` para `grupo`; a área fica vazia (ADR-0015 D2). Redistribuição interna
vai para H-0020.

## Tratamento dos achados da auditoria pós-revisão

### A-001 — NOTA

A-001 tratado como nota: expansão de grupo no modo vertical é comportamento
pré-existente (linhas 784–793 do `renderizador.py` no commit `9d4c74d`) e fica
fora do escopo do H-0019. O modo horizontal implementado neste ciclo atua
apenas sobre filhos diretos do corpo raiz, compatível com ADR-0015. O H-0019
não piora a situação — o branch `else` preserva o código existente integralmente,
sem qualquer alteração no comportamento vertical/None/sobreposto.

### A-002 — BAIXO

A-002 tratado: teste formal adicionado. O caso N=1 com `arranjo="horizontal"`
é coberto pelo método `test_arranjo_horizontal_n1` na classe `TestArranjoH0019`
em `tela/teste_renderizador.py`. O teste verifica:
- renderização sem erro;
- cada linha tem exatamente `total_w` chars (largura total, sem particionamento);
- o elemento aparece na saída;
- sem `╮╭` (área única, sem partição interna).

## Testes executados

| Suíte | Antes | Depois | Exit |
|---|---|---|---|
| `tela/teste_loader.py` | 79/79 | 89/89 | 0 |
| `tela/teste_modelo.py` | 56/56 | 56/56 | 0 |
| `tela/teste_renderizador.py` | 226/226 | 261/261 | 0 |
| `tela/teste_demo.py` | 117/117 | 117/117 | 0 |
| `tela/teste_diagnostico.py` | 28/28 | 28/28 | 0 |
| `tela/teste_explorar_barra_de_menus.py` | 38/38 | 38/38 | 0 |
| **Total** | **544/544** | **589/589** | **0** |

Novos casos: +10 em `teste_loader.py`, +35 em `teste_renderizador.py` = **+45**.

## Resultado dos testes

```
PASS — 589/589 — zero regressões
```

## Verificação de proteção da barra_de_menus

```bash
git diff -- tela/renderizador.py | grep -n "_normaliza_distribuicao\|_validar_distribuicao\|_linhas_barra" || true
```

Saída: (nenhuma linha) — funções protegidas não foram alteradas.

Funções intocadas:
- `_normaliza_distribuicao` ✓
- `_validar_distribuicao` ✓
- `_linhas_barra` ✓
- `_validar_ancoras` ✓
- `_montar_coluna_a_coluna` ✓
- `_montar_linha_a_linha` ✓

## Verificação de arquivos proibidos

```bash
git diff --name-only
```

Saída:
```
scripts/docs/handoff/H-0019-layout-horizontal-plano-corpo.md  (pré-existente, não alterado neste ciclo)
scripts/tela/loader.py
scripts/tela/renderizador.py
scripts/tela/teste_loader.py
scripts/tela/teste_renderizador.py
```

Nenhum arquivo proibido foi alterado.

## Verificação de caches

```bash
find . -name '__pycache__' -type d -print
find . -name '*.pyc' -print
```

Saída: (nenhuma linha) — nenhum cache criado (`PYTHONDONTWRITEBYTECODE=1` aplicado).

## Verificação final de estado

```
git diff --stat:
  5 files, 1186 insertions(+), 414 deletions(-)

git status --short:
   M docs/handoff/H-0019-layout-horizontal-plano-corpo.md
   M tela/loader.py
   M tela/renderizador.py
   M tela/teste_loader.py
   M tela/teste_renderizador.py
  ?? docs/relatorios/RELATORIO_AUDITORIA_H-0019_POS_REVISAO_ADR-0015.md
  ?? docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md
  ?? docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
```

## Pendências ou notas

1. **Migração de aliases adiada**: `destino_minimo.json` e `stub_b.json` continuam
   com `"arranjo": "sobreposto"`. Como `"sobreposto"` é alias aceito pelo loader
   e pelo renderer, isso não causa nenhuma regressão. Migração para `"vertical"`
   fica para ciclo futuro.

2. **Redistribuição interna de grupo (H-0020)**: no modo horizontal, `grupo` em
   `corpo.elementos[]` conta como slot com área visualmente vazia. A implementação
   de redistribuição interna vai para H-0020.

3. **Distribuição percentual/fração**: completamente fora de escopo. Campo
   `distribuicao` no `corpo` não é lido em nenhuma circunstância neste ciclo.

4. **Terminal muito pequeno**: `RenderizadorErro` determinístico é o único
   tratamento para largura insuficiente. Reticências (`...`) ficam para ciclo
   futuro conforme ADR-0015 D13.

## Conclusão

H-0019 implementado com sucesso. Baseline preservado: 544/544 → 589/589 (zero
regressões). Funções protegidas da `barra_de_menus` não alteradas. Escopo
negativo respeitado integralmente. Achados A-001 e A-002 tratados. Decisão
de distribuição (Opção A) registrada. `corpo.arranjo = "horizontal"` funciona
com particionamento contíguo, bordas adjacentes coladas (`││`, `╮╭`, `╯╰`),
resto determinístico (maiores restos), preenchimento inferior de áreas menores
e `RenderizadorErro` para largura insuficiente.
