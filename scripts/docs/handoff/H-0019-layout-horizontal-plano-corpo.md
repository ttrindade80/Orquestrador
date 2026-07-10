# H-0019 — Layout horizontal plano do corpo

```text
status:         BLOCKED_BY_ADR_0015_PENDING_REVISION
ciclo:          H-0019
título:         Layout horizontal plano do corpo
depende-de:     H-0018 (implementado, IMP-0018, QA_POST_CORRECTIONS_APPROVED — commit 46e0cb9)
commit-base:    3b98856  docs: registra levantamento pos H-0018
data:           2026-07-09
autor-handoff:  Claude Code
executor:       OpenCode / GLM
```

---

## Bloqueio por ADR-0015

Este handoff não deve ser implementado no estado atual.

A ADR-0015 formalizou novas regras normativas para composição hierárquica do
corpo, distribuição de área horizontal/vertical, arredondamento determinístico,
preenchimento de área alocada, regras dinâmicas de mínimo/preferido/máximo e
sincronização de cortes entre grupos.

Como este handoff foi escrito antes da ADR-0015, ele deve ser revisado antes
de qualquer implementação. A retomada do H-0019 deve produzir uma versão
revisada compatível com a ADR-0015 e com os contratos atualizados.

Qualquer execução baseada nesta versão deve bloquear com
`ARCHITECTURE_REVIEW_REQUIRED`.

---

## Status

```
BLOCKED_BY_ADR_0015_PENDING_REVISION
```

---

## Revisão pós-auditoria

> **Revisão**: 2026-07-09 — por decisão do usuário sobre a semântica do layout horizontal
> do corpo.
>
> A versão original deste handoff (auditada em 2026-07-09, resultado
> `HANDOFF_APPROVED_WITH_NOTES`, relatório `RELATORIO_AUDITORIA_H-0019_HANDOFF.md`)
> especificava um algoritmo de N+1 vãos iguais como regra de distribuição de espaço.
> Essa interpretação foi rejeitada pelo usuário.
>
> A regra correta é: **particionamento contíguo da largura disponível entre os elementos
> diretos do corpo**. Não existem espaços vazios entre molduras. A primeira moldura
> inicia no primeiro caractere útil da linha. A última moldura termina no último
> caractere útil da linha. Molduras adjacentes ficam coladas, produzindo bordas lado a
> lado (`││`). Esta não é uma regra de vãos — é consequência natural do particionamento.
>
> Uma nova auditoria pós-revisão será realizada após esta correção.

---

## Metadados de rastreabilidade

| Item | Referência |
|------|-----------|
| ID | H-0019 |
| Base observada | `3b98856  docs: registra levantamento pos H-0018` |
| Relatório auxiliar pós-H-0018 | `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO.md` (commitado em 3b98856) |
| Ciclos preservados | H-0015, H-0016, H-0017, H-0018 (todos fechados, artefatos presentes) |
| Baseline no momento do levantamento | 544/544 verificações em 6 suítes |
| Contratos aplicáveis | `contrato_processo_desenvolvimento.md`, `contrato_tela_json.md`, `contrato_composicao_corpo.md`, `contrato_barra_de_menus.md`, `contrato_lancador.md`, `contrato_console.md`, `contrato_json_tela_minima.md`, `contrato_json_lancador.md`, `contrato_json_console.md`, `contrato_json_dashboard.md` |
| ADRs normativas | ADR-0008, ADR-0010, ADR-0011, ADR-0013, ADR-0014, ADR-0015 (bloqueante) |
| Relatório auditoria a gerar | `docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md` |
| Relatório de implementação a gerar | `docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md` |
| Relatório de QA a gerar | `docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md` |

**Nota sobre base observada**: O relatório auxiliar de levantamento pós-H-0018
(`RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO.md`) foi commitado pelo usuário
em `3b98856` ("docs: registra levantamento pos H-0018"). O HEAD verificado no
momento da criação deste handoff é `3b98856`, **não** `46e0cb9`. O commit `46e0cb9`
foi a base do levantamento, mas a base real do H-0019 é `3b98856`. Workspace limpo
(`git status --short`: sem saída). Nenhum arquivo modificado, staged ou não rastreado.

---

## Ordem de autoridade

```
contrato_processo_desenvolvimento.md
  > ADRs aceitas (ADR-0008, ADR-0010, ADR-0011, ADR-0013, ADR-0014, ADR-0015)
    > contratos de módulo (contrato_composicao_corpo.md, contrato_tela_json.md, ...)
      > este handoff (H-0019)  [BLOQUEADO — ver seção "Bloqueio por ADR-0015"]
        > decisões de implementação locais (IMP-0019)
```

O executor não decide arquitetura. Se qualquer item normativo estiver ausente ou conflitante,
bloquear com `ARCHITECTURE_REVIEW_REQUIRED` antes de implementar qualquer linha de código.

**Este handoff está bloqueado por ADR-0015. Qualquer execução baseada nesta versão
deve bloquear imediatamente com `ARCHITECTURE_REVIEW_REQUIRED`.**

---

## Contexto

Os ciclos H-0015 a H-0018 estabilizaram a ocupação vertical da janela (H-0015),
a migração e cobertura da `barra_de_menus` (H-0016, H-0017, H-0018). A `barra_de_menus`
está protegida e não deve ser alterada neste ciclo.

O contrato `contrato_composicao_corpo.md` seção 5.6 especifica o arranjo horizontal como
composição lado a lado dos elementos diretos de `corpo.elementos[]`. A regra de layout
adotada neste ciclo (por decisão do usuário, registrada pós-auditoria) é de
**particionamento contíguo** da largura disponível: sem espaços vazios entre molduras,
molduras adjacentes ficam coladas (`││`), a primeira caixa inicia no primeiro caractere
útil da linha e a última caixa termina no último caractere útil da linha.

O campo `corpo.arranjo` já é armazenado no modelo (`Corpo.arranjo: str | None`)
mas **não é lido pelo renderer** e **não é validado pelo loader no nível da tela**.
O renderer atual empilha todos os elementos verticalmente, ignorando o arranjo declarado.

Estado verificado no código (commit 3b98856):

- `loader.py` linha 347: `arranjo = corpo.get("arranjo")` — aceita qualquer valor,
  incluindo `"diagonal"`, sem erro.
- `modelo.py`: `Corpo(arranjo=..., elementos=[...])` — armazena sem validar. OK.
- `renderizador.py` linhas 779–795 (`renderizar_tela`): laço sequencial sobre
  `modelo.corpo.elementos`; o campo `modelo.corpo.arranjo` **não é lido em nenhum ponto**
  da função.
- `destino_minimo.json` e `stub_b.json`: declaram `"arranjo": "sobreposto"` (alias
  transicional de `"vertical"`, ADR-0011). Nenhum JSON ativo usa `"horizontal"`.

---

## Problema

1. **Renderer ignora `corpo.arranjo`**: telas com `arranjo = "horizontal"` são renderizadas
   verticalmente sem erro e sem aviso — comportamento silenciosamente incorreto.
2. **Loader não valida `arranjo` no nível da tela**: valor inválido como `"diagonal"` é
   aceito silenciosamente.
3. **Nenhum JSON ativo usa `horizontal`**: a funcionalidade não pode ser verificada
   em integração sem criar ou adaptar uma fixture.

---

## Objetivo

Implementar suporte mínimo e verificável a `corpo.arranjo = "horizontal"` com layout
horizontal **plano** dos elementos diretos de `corpo.elementos[]`, sem percentual/fração
e sem aninhamento.

O escopo é o menor ciclo funcional verificável que abre o eixo de layout do corpo:

- Loader valida `arranjo` no nível da tela.
- Renderer lê `modelo.corpo.arranjo` e aplica layout horizontal quando declarado.
- Aliases transicionais funcionam de forma determinística.
- Testes cobrem os novos comportamentos.
- Baseline 544/544 continua passando.

---

## Leitura obrigatória

O executor deve ler na íntegra antes de tocar qualquer arquivo:

1. `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO.md`
2. `docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md`
3. `docs/relatorios/RELATORIO_QA_H-0018_POS_CORRECOES.md`
4. `docs/NOMENCLATURA.md`
5. `docs/contratos/contrato_processo_desenvolvimento.md`
6. `docs/contratos/contrato_tela_json.md`
7. `docs/contratos/contrato_composicao_corpo.md`
8. `docs/contratos/contrato_barra_de_menus.md`
9. `docs/contratos/contrato_lancador.md`
10. `docs/contratos/contrato_console.md`
11. `docs/contratos/contrato_json_tela_minima.md`
12. `docs/contratos/contrato_json_lancador.md`
13. `docs/contratos/contrato_json_console.md`
14. `docs/contratos/contrato_json_dashboard.md`
15. `tela/loader.py` (integralmente)
16. `tela/modelo.py` (integralmente)
17. `tela/renderizador.py` (integralmente)
18. `tela/demo.py` (integralmente)
19. `tela/diagnostico.py` (integralmente)
20. `tela/teste_loader.py` (integralmente)
21. `tela/teste_modelo.py` (integralmente)
22. `tela/teste_renderizador.py` (integralmente)
23. `tela/teste_demo.py` (integralmente)
24. `tela/teste_diagnostico.py` (integralmente)
25. `config/telas/orquestrador.json`
26. `config/telas/grupo_minimo.json`
27. `config/telas/destino_minimo.json`
28. `config/telas/stub_b.json`
29. Este handoff até o final.

---

## Escopo positivo

O H-0019 pode e deve implementar:

```
1. loader.py: validar corpo.arranjo no nível da tela.
   Valores aceitos: None, "vertical", "horizontal",
   "sobreposto" (alias transitional → vertical),
   "lado_a_lado" (alias transitional → horizontal).
   Rejeitar qualquer outro valor com TelaEstruturaInvalida determinístico.

2. renderizador.py: ler modelo.corpo.arranjo na função renderizar_tela.
   Para None, "vertical", "sobreposto": preservar comportamento atual.
   Para "horizontal", "lado_a_lado": renderizar elementos diretos lado a lado.

3. Criar ou adaptar ao menos um JSON de teste com arranjo = "horizontal".
   (Decisão explícita exigida pelo executor — ver seção "JSONs de teste")

4. Adicionar testes em tela/teste_renderizador.py.

5. Adicionar testes em tela/teste_loader.py.

6. Migração de destino_minimo.json e stub_b.json de "sobreposto" para "vertical":
   OPCIONAL — somente se bundled como migração declarativa acoplada à validação
   de aliases. Ver seção "JSONs de teste" para regras.

7. Criar docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md.
```

---

## Escopo negativo

O H-0019 **NÃO deve** implementar:

```
NÃO alterar barra_de_menus.distribuicao.
NÃO alterar _normaliza_distribuicao.
NÃO alterar _validar_distribuicao.
NÃO alterar _linhas_barra.
NÃO refatorar explorar_barra_de_menus.py.
NÃO alterar teste_explorar_barra_de_menus.py.
NÃO alterar contrato_barra_de_menus.md.
NÃO alterar contrato_chip.md.
NÃO implementar distribuição percentual/fração de largura.
NÃO implementar aninhamento de grupos com arranjo próprio.
NÃO implementar arranjo horizontal dentro de grupo aninhado.
NÃO implementar combinação especial horizontal + dashboard + indicador de paginação.
NÃO migrar posicao_dashboard.
NÃO implementar console real (conteúdo de dados real).
NÃO implementar navegação por [✥].
NÃO implementar foco entre elementos.
NÃO implementar seleção.
NÃO implementar paginação.
NÃO implementar filtros.
NÃO alterar ações ou registry.
NÃO criar registry novo.
NÃO alterar ADR, contrato ou NOMENCLATURA.md.
NÃO reabrir H-0011.
NÃO recriar H-0011A.
NÃO usar H-0011 ou H-0011A como base implementável.
NÃO fazer commit.
```

---

## Preservações obrigatórias

As seguintes funções e invariantes do H-0018 **não devem ser tocadas**:

- `_normaliza_distribuicao` (renderizador.py)
- `_validar_distribuicao` (renderizador.py)
- `_linhas_barra` (renderizador.py)
- `_validar_ancoras` (renderizador.py)
- Testes da classe `TestDistribuicaoH0018` (teste_renderizador.py)
- Snapshots de `teste_demo.py` e `teste_diagnostico.py` — alterar **somente** se houver
  mudança visual inevitável e justificada; registrar no IMP-0019 qualquer alteração.

A `barra_de_menus` está estabilizada. Qualquer alteração em `_linhas_barra`,
`_normaliza_distribuicao` ou `_validar_distribuicao` sem necessidade explícita pode
reverter coberturas de H-0018 e é proibida neste ciclo.

---

## Especificação funcional por módulo

### `tela/loader.py`

**Onde alterar**: após a linha `arranjo = corpo.get("arranjo")` (linha 347 do commit base).

**O que adicionar**: validação de que o valor lido é um dos aceitos.

```python
ARRANJOS_CORPO_VALIDOS = {None, "vertical", "horizontal", "sobreposto", "lado_a_lado"}

arranjo = corpo.get("arranjo")
if arranjo not in ARRANJOS_CORPO_VALIDOS:
    raise TelaEstruturaInvalida(
        "corpo.arranjo invalido: {0!r}; valores aceitos: "
        "vertical, horizontal, sobreposto (alias), lado_a_lado (alias)".format(arranjo)
    )
```

A constante `ARRANJOS_CORPO_VALIDOS` pode ser definida ao nível do módulo para permitir
importação em testes. A exceção usada deve ser `TelaEstruturaInvalida` (já existente).

**O que preservar**: todo o restante do loader, especialmente `_validar_grupo`, que
já rejeita `"horizontal"` e `"lado_a_lado"` em grupos — essa validação é sobre GRUPOS,
não sobre o nível da tela, e deve ser preservada intacta.

**Não alterar**: `TIPOS_CORPO_VALIDOS`, `TIPOS_ESTRUTURAIS_VALIDOS`, `_validar_grupo`,
nenhuma outra lógica de validação.

---

### `tela/modelo.py`

**Não alterar.** `Corpo.arranjo: str | None` já armazena qualquer valor. A validação
é responsabilidade do loader. O modelo não precisa de modificações para suportar H-0019.

Se o executor identificar necessidade de alterar o modelo, deve bloquear com
`ARCHITECTURE_REVIEW_REQUIRED` e descrever a necessidade precisamente.

---

### `tela/renderizador.py`

**Onde alterar**: apenas na função `renderizar_tela` (a partir da linha 779 do commit base),
especificamente no trecho que percorre `modelo.corpo.elementos` para montar `partes`.

**O que NÃO alterar**: `_normaliza_distribuicao`, `_validar_distribuicao`, `_linhas_barra`,
`_validar_ancoras`, `_montar_coluna_a_coluna`, `_montar_linha_a_linha`, `_texto_chip_barra`,
`_caixa_de_elemento`, `_caixa`, `_linha_topo`, `_linha_base`, `_linha_conteudo`.

**O que adicionar**:

Antes do laço sobre `modelo.corpo.elementos`, ler e normalizar o arranjo:

```python
arranjo_corpo = modelo.corpo.arranjo
# Aliases transicionais (ADR-0011)
if arranjo_corpo == "sobreposto":
    arranjo_corpo = "vertical"
if arranjo_corpo == "lado_a_lado":
    arranjo_corpo = "horizontal"
# None e "vertical" seguem o comportamento atual
```

No laço sobre `modelo.corpo.elementos`, introduzir branch por `arranjo_corpo`:

```python
if arranjo_corpo == "horizontal":
    # Ver seção "Algoritmo de layout horizontal plano"
    bloco_horizontal = _montar_corpo_horizontal(
        modelo.corpo.elementos, borda, total_w, inner_w, content_w, label_max
    )
    partes.append(bloco_horizontal)
else:
    # Comportamento atual (vertical / None / sobreposto normalizado)
    for elemento in modelo.corpo.elementos:
        ...  # código existente preservado integralmente
```

A função auxiliar `_montar_corpo_horizontal` recebe a lista de elementos e os parâmetros
de dimensionamento. Ver algoritmo na seção seguinte. A função é interna ao módulo.

**Preenchimento vertical (H-0015)**: a lógica de `altura` deve continuar funcionando
após a introdução do horizontal. O bloco horizontal é tratado como um único bloco de
string (como qualquer outra parte de corpo), e `l_corpo_conteudo` deve contar suas
linhas normalmente. Não alterar a lógica de preenchimento H-0015.

---

## Algoritmo de layout horizontal plano

O algoritmo se aplica quando `arranjo_corpo == "horizontal"` (após normalização de aliases).

**Regra fundamental**: não existe espaço vazio entre molduras no layout horizontal do
corpo. A primeira moldura começa no primeiro caractere útil da linha. A última moldura
termina no último caractere útil da linha. Molduras adjacentes ficam coladas, produzindo
bordas lado a lado: `││` em linhas internas, `╮╭` no topo e `╯╰` na base (conforme
estilo ativo). Esta é consequência natural do particionamento contíguo da largura entre
todos os elementos diretos do corpo — não é uma regra de vãos.

### Suporte a N

Este ciclo implementa `N >= 2` por particionamento contíguo da largura. Registrar no
IMP-0019 que isso não é regra de vãos — é consequência natural de particionar a largura
entre todos os elementos diretos do corpo.

### Entradas

- `elementos`: lista de `ElementoCorpo` de `modelo.corpo.elementos` (todos os tipos,
  incluindo `grupo`)
- `borda`, `total_w`, `inner_w`, `content_w`, `label_max`: parâmetros de dimensionamento
  da tela

### Passo 1 — Coletar elementos funcionais diretos

Percorrer `elementos` e coletar os elementos que geram caixas visuais:

```python
funcionais = []
for elemento in elementos:
    if elemento.tipo == "grupo":
        for interno in elemento.elementos:
            funcionais.append(interno)
    else:
        funcionais.append(elemento)
# Filtrar Nones (elementos de tipo desconhecido que _caixa_de_elemento ignora)
```

`N = len(funcionais)`. Se `N == 0`, retornar string vazia (nenhum elemento).
Se `N == 1`, renderizar como vertical (apenas um elemento não justifica layout horizontal).

### Passo 2 — Calcular largura de cada faixa por particionamento contíguo

```python
N = len(funcionais)
base_w = total_w // N
resto = total_w % N
# Distribuição determinística da esquerda para a direita:
# as primeiras `resto` faixas recebem base_w + 1; as demais recebem base_w.
# Invariante: sum(larguras) == total_w
larguras = [base_w + (1 if i < resto else 0) for i in range(N)]
```

Verificar cabimento mínimo (molduras + conteúdo mínimo):

```python
for i, w in enumerate(larguras):
    if w < 10:
        raise RenderizadorErro(
            "arranjo horizontal: largura {0} insuficiente para {1} elementos "
            "lado a lado (minimo 10 chars por faixa; faixa {2} calculada com {3})".format(
                total_w, N, i, w
            )
        )
```

Parâmetros derivados para cada faixa `i` (onde `w = larguras[i]`):

```python
inner_w_i   = w - 2
content_w_i = w - 3
label_max_i = w - 4
```

### Passo 3 — Renderizar cada elemento em sua faixa

Para cada elemento em `funcionais`, renderizar com a largura de sua faixa:

```python
caixa_str = _caixa_de_elemento(
    elemento, borda, inner_w_i, content_w_i, label_max_i
)
if caixa_str is None:
    caixa_str = ""  # elemento de tipo desconhecido: vazio
```

Converter `caixa_str` em lista de linhas: `linhas_faixa = caixa_str.split("\n")`.
Registrar `largura_faixa = larguras[i]` (largura declarada) e `altura_faixa = len(linhas_faixa)`.

### Passo 4 — Normalizar altura com padding inferior

```python
altura_max = max(len(linhas) for linhas in todas_as_linhas_por_faixa)
for i, linhas in enumerate(todas_as_linhas_por_faixa):
    while len(linhas) < altura_max:
        linhas.append(" " * larguras[i])  # padding da largura da própria faixa
```

### Passo 5 — Concatenar faixas linha a linha (sem separador)

```python
linhas_resultado = []
for r in range(altura_max):
    linha = ""
    for i, linhas in enumerate(todas_as_linhas_por_faixa):
        linha += linhas[r]
    # A concatenação direta produz bordas coladas:
    # - "││" em linhas internas (borda direita da faixa i + borda esquerda da faixa i+1)
    # - "╮╭" no topo das faixas adjacentes
    # - "╯╰" na base das faixas adjacentes
    # Invariante: len(linha) == total_w (garantido pelo particionamento contíguo)
    linhas_resultado.append(linha)
resultado_str = "\n".join(linhas_resultado)
```

### Passo 6 — Preservações obrigatórias

- **Cabeçalho**: o cabeçalho é montado em `partes[0]` antes do laço de corpo.
  O bloco horizontal substitui o laço, mas `partes[0]` (cabeçalho) é preservado.
- **`barra_de_menus`**: montada e adicionada a `partes` APÓS o bloco do corpo,
  exatamente como no fluxo atual.
- **Preenchimento vertical (H-0015)**: o bloco horizontal resultante é uma string
  com múltiplas linhas. `_contar_linhas(bloco_horizontal)` deve retornar
  `len(linhas_resultado)`. O cálculo de `l_corpo_conteudo` deve somar
  `_contar_linhas(bloco_horizontal)` (string única) em vez de somar as caixas individuais.
  **Se `altura` for fornecido e o corpo horizontal já tiver `>= l_corpo_disponivel` linhas,
  lançar `RenderizadorErro` (como no fluxo atual).**
- **`altura` explícita**: quando fornecido, o total final da saída deve continuar
  tendo exatamente `altura` linhas.

### Regra de cabimento mínimo

```
Se base_w < 10 (equivalente a total_w // N < 10) → RenderizadorErro determinístico.
Mensagem deve incluir: total_w, N, largura calculada da faixa.
Nunca truncar silenciosamente, nunca omitir elemento, nunca reordenar elemento e
nunca fazer fallback silencioso para vertical.
```

---

## Política para aliases transicionais

| Valor declarado no JSON | Comportamento no renderer | Comportamento no loader |
|-------------------------|--------------------------|------------------------|
| `"vertical"` | Renderização vertical (atual) | Aceito |
| `"horizontal"` | Renderização horizontal plana | Aceito |
| `"sobreposto"` | Renderização vertical (alias) | Aceito |
| `"lado_a_lado"` | Renderização horizontal plana (alias) | Aceito |
| `None` / ausente | Renderização vertical (default atual) | Aceito (None) |
| Qualquer outro valor | — | `TelaEstruturaInvalida` |

A normalização dos aliases ocorre no **renderer**, não no loader. O loader apenas aceita
o conjunto de valores válidos; o renderer mapeia aliases para comportamento concreto.
O modelo armazena o valor como declarado no JSON (sem normalização no modelo).

`destino_minimo.json` e `stub_b.json` declaram `"sobreposto"`. Com a validação do
loader, `"sobreposto"` deve ser aceito (está no conjunto válido). Portanto esses JSONs
continuam funcionando sem alteração.

---

## Política para JSONs de teste/configuração

O executor deve decidir **uma** das opções abaixo e registrar a decisão no IMP-0019:

**Opção A — Criar JSON mínimo novo** (`config/telas/horizontal_teste.json`):

- Tela de teste com `arranjo = "horizontal"` e dois ou mais elementos diretos.
- Não precisa ter `barra_de_menus` sofisticada (pode ter os mesmos chips que `destino_minimo`).
- Não perturba JSONs de produção.
- Referenciada apenas nos testes do renderer (fixture sintética ou via `carregar_tela`).

**Opção B — Adaptar fixture existente no teste** (in-memory):

- Construir `ModeloTela` sinteticamente no teste sem carregar JSON de disco.
- Não cria novo arquivo JSON.
- Mais isolado; menor superfície de mudança.

**Regras independentes da opção escolhida**:

- Não alterar `orquestrador.json` nem `grupo_minimo.json`.
- Não alterar `destino_minimo.json` nem `stub_b.json` (a menos que a migração opcional
  abaixo seja incluída).

**Migração opcional de aliases** (`"sobreposto"` → `"vertical"` em `destino_minimo.json`
e `stub_b.json`): pode ser incluída neste ciclo somente se:

- O handoff declarar explicitamente como migração declarativa acoplada à validação.
- A migração for pequena (2 arquivos, 1 campo cada).
- Os snapshots de `teste_demo.py` e `teste_diagnostico.py` não precisarem de alteração
  (o comportamento visual é idêntico: `"sobreposto"` e `"vertical"` produzem o mesmo resultado).
- A mudança for registrada no IMP-0019 como migração declarativa.

**Se a migração NÃO for incluída**: registrar como pendência posterior no IMP-0019.
A presença de `"sobreposto"` continua válida pois o loader aceita o alias.

---

## Testes obrigatórios

### Suítes existentes (devem continuar passando — baseline)

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_explorar_barra_de_menus.py
```

Todos os 544 casos atuais devem continuar passando antes de rodar os novos.

### Novos testes obrigatórios em `tela/teste_loader.py`

```text
test_loader_arranjo_vertical_aceito:
    carregar_tela com JSON que declara arranjo = "vertical".
    Confirmar sem erro.

test_loader_arranjo_horizontal_aceito:
    carregar_tela com JSON (ou dict sintético) que declara arranjo = "horizontal".
    Confirmar sem erro.

test_loader_arranjo_sobreposto_aceito:
    arranjo = "sobreposto".
    Confirmar sem erro (alias transicional aceito).

test_loader_arranjo_lado_a_lado_aceito:
    arranjo = "lado_a_lado".
    Confirmar sem erro (alias transicional aceito).

test_loader_arranjo_none_aceito:
    arranjo ausente do JSON (None).
    Confirmar sem erro.

test_loader_arranjo_invalido_diagonal:
    arranjo = "diagonal".
    Confirmar TelaEstruturaInvalida determinístico.
    Confirmar mensagem menciona "corpo.arranjo".

test_loader_arranjo_invalido_string_vazia:
    arranjo = "".
    Confirmar TelaEstruturaInvalida.

test_loader_arranjo_invalido_tipo_inteiro:
    arranjo = 1 (inteiro).
    Confirmar TelaEstruturaInvalida.
```

### Novos testes obrigatórios em `tela/teste_renderizador.py`

```text
test_arranjo_none_preserva_vertical:
    Modelo com corpo.arranjo = None, 2 elementos.
    Confirmar que a saída tem os 2 elementos empilhados verticalmente (caixas sequenciais).
    Confirmar que barra_de_menus aparece ao final.

test_arranjo_vertical_preserva_comportamento:
    Modelo com corpo.arranjo = "vertical", 2 elementos.
    Confirmar saída idêntica ao caso None.
    Confirmar sem erro.

test_arranjo_sobreposto_preserva_vertical:
    Modelo com corpo.arranjo = "sobreposto".
    Confirmar saída idêntica ao caso "vertical".
    Confirmar sem erro.

test_arranjo_horizontal_dois_elementos_lado_a_lado:
    Modelo com corpo.arranjo = "horizontal", 2 elementos (ex.: lancador + dashboard).
    Confirmar que as 2 caixas aparecem LADO A LADO na saída (na mesma faixa de linhas).
    Confirmar que a barra_de_menus aparece ABAIXO (não junto das colunas).
    Confirmar que o número total de linhas é menor que com arranjo vertical
    (2 elementos lado a lado ocupam menos linhas do que 2 elementos empilhados).

test_arranjo_lado_a_lado_alias_horizontal:
    Modelo com corpo.arranjo = "lado_a_lado".
    Confirmar saída idêntica ao caso "horizontal".
    Confirmar sem erro.

test_arranjo_horizontal_caixas_coladas:
    Modelo com corpo.arranjo = "horizontal", 2 elementos, largura=42.
    Extrair as linhas da faixa horizontal e confirmar que:
    - aparece "││" (duas barras verticais adjacentes) no ponto de junção das caixas
      nas linhas internas;
    - aparece "╮╭" (ou equivalente conforme estilo ativo) na linha de topo das caixas;
    - aparece "╯╰" (ou equivalente conforme estilo ativo) na linha de base das caixas;
    - o primeiro caractere de cada linha é a borda esquerda da caixa da esquerda
      (primeira caixa inicia no primeiro caractere útil);
    - o último caractere de cada linha é a borda direita da caixa da direita
      (última caixa termina no último caractere útil);
    - cada linha tem exatamente 42 caracteres (largura total disponível).

test_arranjo_horizontal_padding_inferior:
    Modelo com corpo.arranjo = "horizontal", 2 elementos de alturas diferentes
    (ex.: dashboard com 5 campos vs lancador com 2 itens).
    Confirmar que a faixa horizontal tem linhas de altura uniforme (a menor é completada).

test_arranjo_horizontal_largura_insuficiente:
    Modelo com corpo.arranjo = "horizontal", 2 elementos, largura muito pequena (ex.: 20).
    Confirmar RenderizadorErro com mensagem determinística mencionando "arranjo horizontal".
    Confirmar que NÃO há fallback silencioso para vertical.

test_arranjo_horizontal_tres_elementos:
    Modelo com corpo.arranjo = "horizontal", 3 elementos diretos.
    Confirmar que os 3 aparecem lado a lado na saída.

test_arranjo_horizontal_com_altura_preserva_h0015:
    Modelo com corpo.arranjo = "horizontal", altura=40 (ou qualquer valor suficiente).
    Confirmar que a saída tem exatamente 40 linhas (preenchimento vertical funciona).

test_arranjo_horizontal_barra_preservada:
    Modelo com corpo.arranjo = "horizontal".
    Confirmar que _linhas_barra é chamada normalmente e a barra aparece ao rodapé.
    (Nenhuma alteração em barra_de_menus, chips, distribuição.)

test_arranjo_horizontal_grupo_estrutural:
    Modelo com corpo.arranjo = "horizontal", corpo.elementos contendo um grupo estrutural.
    Confirmar que o elemento interno do grupo é tratado como elemento funcional direto
    para fins do layout horizontal plano.
```

### Verificação de caches

```bash
find . -name '__pycache__' -type d -print
find . -name '*.pyc' -print
```

Nenhum cache deve existir após a execução com `PYTHONDONTWRITEBYTECODE=1`.

---

## Relatório de implementação exigido

O executor deve criar:

```text
docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
```

Com a seguinte estrutura:

```markdown
# IMP-0019 — Layout horizontal plano do corpo

## Status

## Resumo

## Arquivos alterados/criados

## Decisões locais
(JSON novo vs fixture in-memory; migração de aliases bundled vs adiada)

## Implementação em loader.py
(Constante ARRANJOS_CORPO_VALIDOS; onde inserida; trecho de código)

## Implementação em renderizador.py
(Função _montar_corpo_horizontal; onde inserida no fluxo; interação com H-0015)

## Testes do loader adicionados

## Testes do renderer adicionados

## Alterações em snapshots (se houver)
(Justificativa obrigatória para qualquer snapshot alterado)

## Resultados de testes
(Tabela: suite / verificações / exit code)

## Execuções do explorador (confirmar que não foram afetadas)

## Confirmação de escopo negativo
(Confirmar que barra_de_menus, _normaliza_distribuicao, _validar_distribuicao,
 _linhas_barra não foram alteradas)

## Limitações conhecidas

## Pendências para ciclo futuro
```

---

## Critérios de aceite

```
 1. corpo.arranjo = "vertical" preserva renderização vertical atual (empilhamento
    sequencial). Saída idêntica ao comportamento pré-H-0019.

 2. corpo.arranjo = "sobreposto" preserva renderização vertical atual como alias
    transicional. Saída idêntica ao caso "vertical".

 3. corpo.arranjo = None preserva comportamento atual (vertical por default).

 4. corpo.arranjo = "horizontal" renderiza dois ou mais elementos diretos lado a lado.
    As caixas de cada elemento aparecem na mesma faixa horizontal de linhas.

 5. corpo.arranjo = "lado_a_lado" renderiza como alias transicional de horizontal.
    Saída idêntica ao caso "horizontal".

 6. O layout horizontal usa particionamento contíguo da largura disponível entre os
    N elementos diretos do corpo. Não existem espaços vazios entre molduras.
    Caixas adjacentes ficam coladas, produzindo bordas lado a lado: "││" nas linhas
    internas, "╮╭" no topo e "╯╰" na base (conforme estilo ativo).
    A primeira caixa inicia no primeiro caractere útil da linha (coluna 0).
    A última caixa termina no último caractere útil da linha (coluna total_w-1).
    A soma das larguras das faixas é exatamente total_w (invariante do particionamento).
    O resto da divisão inteira (total_w % N) é distribuído deterministicamente
    da esquerda para a direita (uma unidade extra nas primeiras `resto` faixas).

 7. Elementos com alturas diferentes recebem padding inferior de linhas de espaços
    para que todas as colunas tenham a mesma altura, permitindo concatenação
    linha a linha sem mistura de conteúdo de linhas distintas.

 8. Largura insuficiente para comportar N elementos com w_col >= 10 gera
    RenderizadorErro determinístico, sem truncamento e sem fallback silencioso
    para vertical.

 9. Loader rejeita corpo.arranjo inválido (ex.: "diagonal", "") com
    TelaEstruturaInvalida, sem silêncio.

10. Loader aceita explicitamente None, "vertical", "horizontal",
    "sobreposto", "lado_a_lado".

11. Testes da barra_de_menus (classe TestDistribuicaoH0018 e
    teste_explorar_barra_de_menus.py) continuam passando sem alteração.

12. Baseline completo: 544 + novos casos passando. Zero regressões.
    (O número exato de novos casos deve ser registrado no IMP-0019.)

13. Nenhum arquivo de ADR, contrato, NOMENCLATURA.md alterado.

14. Nenhum cache __pycache__ nem .pyc no workspace após execução.
```

---

## Riscos e mitigação

### R-1 — Confundir `corpo.arranjo = "horizontal"` com `barra_de_menus.distribuicao.modo = "horizontal_responsiva"`

**Descrição**: os dois contextos usam a substring `"horizontal"` com semânticas completamente
distintas. `corpo.arranjo = "horizontal"` é composição dos elementos do corpo (ADR-0011).
`barra_de_menus.distribuicao.modo = "horizontal_responsiva"` é distribuição visual dos
chips (ADR-0014). São módulos, regiões e contratos distintos.

**Sintoma de confusão**: alterar `_linhas_barra`, `_normaliza_distribuicao` ou `_validar_distribuicao`
ao trabalhar no arranjo do corpo.

**Mitigação**: buscas devem usar padrões específicos: `modelo.corpo.arranjo` ou `"arranjo":`
para o corpo; `barra_de_menus.distribuicao` para a barra. Filtros por substring `"horizontal"`
são proibidos como critério de alteração automática (ADR-0014). O H-0019 toca apenas a função
`renderizar_tela` e o trecho de validação do loader — não toca nenhuma função de barra.

---

### R-2 — Substituição por substring `"horizontal"` ou `"vertical"`

**Descrição**: usar grep/replace global por `"horizontal"` ou `"vertical"` em qualquer arquivo
pode acidentalmente alterar `_normaliza_distribuicao` (que testa a string `"horizontal"` para
alias de `barra_de_menus.distribuicao`) ou comentários e snapshots não relacionados.

**Mitigação**: toda alteração deve ser feita por localização precisa de linha/função. Nunca
usar substituição global por substring ambígua (ADR-0014, Parte B). O executor deve identificar
exatamente as linhas a alterar antes de escrever qualquer código.

---

### R-3 — Reabrir H-0011 ou H-0011A

**Descrição**: ao implementar layout horizontal, pode surgir tentação de referenciar ou
reabrir H-0011 (renderização lado a lado com barra mínima — CANCELADO antes de qualquer
implementação) ou H-0011A (REMOVIDO por granularidade excessiva) como "base histórica".

**Mitigação**: H-0011 e H-0011A permanecem como referências históricas arquivadas.
Nenhum código, decisão ou estrutura deste ciclo pode ser baseada nesses artefatos.
O H-0019 é independente e se baseia nos contratos ADR-0011 e contrato_composicao_corpo.md.

---

### R-4 — Introduzir regra de vãos ou espaçamento entre molduras

**Descrição**: implementar qualquer forma de espaço vazio entre as caixas do layout
horizontal — seja "N+1 vãos iguais", "3 vãos", vão lateral, padding entre colunas
ou qualquer separador horizontal entre molduras adjacentes.

**Por que é risco**: a regra correta (pós-auditoria) é de particionamento contíguo:
não existe espaço entre molduras. Introduzir vãos ou separadores viola a regra e produz
saída visual incorreta (caixas não coladas), além de contradizer o critério de aceite 6.

**Interpretação rejeitada neste ciclo**: a especificação original de N+1 vãos iguais
(borda↔coluna_1, coluna_1↔coluna_2, coluna_2↔borda) foi adotada na versão inicial do
handoff e rejeitada pelo usuário por decisão explícita pós-auditoria. Não retomar essa
interpretação.

**Mitigação**: a largura de cada faixa é calculada por `larguras[i] = total_w // N + (1 if i < resto else 0)`,
com `sum(larguras) == total_w`. A concatenação das faixas é direta, sem separador.
Nenhuma lógica de vão, espaçamento ou padding lateral é introduzida.

---

### R-5 — Misturar horizontal plano com aninhamento de grupos

**Descrição**: ao implementar o layout horizontal, incluir suporte a grupos aninhados com
arranjos próprios ou a elementos dentro de grupo com arranjo horizontal.

**Por que é risco**: o H-0019 é layout horizontal PLANO — apenas elementos diretos de
`corpo.elementos[]`. Grupos são containers estruturais; seus elementos internos participam
do layout horizontal como elementos funcionais diretos (não formam sub-layout separado).

**Mitigação**: o algoritmo (`_montar_corpo_horizontal`) percorre `elementos` e para cada
`grupo` coleta os elementos funcionais internos. Sem recursão, sem sub-layout, sem arranjo
dentro de grupo.

---

### R-6 — Regressão na barra_de_menus estabilizada no H-0018

**Descrição**: ao modificar `renderizar_tela` para suportar arranjo horizontal, introduzir
inadvertidamente chamada a `_linhas_barra` com parâmetros errados ou alterar o fluxo de
montagem da caixa da barra.

**Sintoma**: testes de `TestDistribuicaoH0018` ou `teste_explorar_barra_de_menus.py` falham
após as alterações.

**Mitigação**: executar `PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py` e
`PYTHONDONTWRITEBYTECODE=1 python tela/teste_explorar_barra_de_menus.py` após cada alteração
incremental no renderer. A barra_de_menus deve ser a ÚLTIMA parte adicionada a `partes`,
exatamente como no fluxo atual.

---

### R-7 — Fallback silencioso de horizontal para vertical

**Descrição**: implementar horizontal de forma que, se a largura for insuficiente ou houver
erro, a saída caia silenciosamente para o layout vertical sem erro.

**Por que é risco**: viola o princípio de que o renderer nunca faz fallback silencioso
(ADR-0014 generalizado). O executor não pode saber que o layout declarado não foi respeitado.

**Mitigação**: qualquer condição que impeça o layout horizontal deve lançar `RenderizadorErro`
determinístico com mensagem descritiva. Nunca alterar silenciosamente o comportamento.
O critério de aceite 8 verifica explicitamente a ausência de fallback silencioso.

---

## Fora de escopo futuro

Os itens abaixo foram identificados e **explicitamente adiados** — não são lacunas:

- Combinação `arranjo = "horizontal"` + `dashboard` presente com indicador de paginação
  (especificado em `contrato_composicao_corpo.md` seção 9 como "pendente").
- Migração do campo `posicao_dashboard` (ADR-0010).
- Schema de grupos hierárquicos com arranjo horizontal dentro de grupo.
- Distribuição percentual/fração de espaço entre elementos.
- Aninhamento de grupos com arranjos próprios.
- Implementação de console real com conteúdo de dados.
- Navegação por `[✥]`, foco, seleção, paginação, filtros.
- Migração formal de `destino_minimo.json` e `stub_b.json` (se não bundled neste ciclo).

---

## Saída esperada do implementador

```
IMPLEMENTATION_COMPLETED

arquivos-alterados:
  tela/loader.py
  tela/teste_loader.py
  tela/renderizador.py
  tela/teste_renderizador.py
  [config/telas/horizontal_teste.json  ← se Opção A for escolhida]
  [config/telas/destino_minimo.json    ← se migração bundled]
  [config/telas/stub_b.json            ← se migração bundled]
  [tela/teste_demo.py                  ← somente se snapshot inevitável]
  [tela/teste_diagnostico.py           ← somente se snapshot inevitável]
  docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md

testes:
  teste_loader.py:                     <N>/<N>
  teste_modelo.py:                     56/56
  teste_renderizador.py:               <N>/<N>
  teste_demo.py:                       117/117 (ou <N>/<N> se snapshot ajustado)
  teste_diagnostico.py:                28/28   (ou <N>/<N> se snapshot ajustado)
  teste_explorar_barra_de_menus.py:    38/38

verificacoes:
  git status --short
  git diff --stat
  git diff --name-only
  find . -name '__pycache__' -type d -print  → (sem saída)
  find . -name '*.pyc' -print               → (sem saída)
```
