# H-0019 — Layout horizontal plano do corpo

```text
status:          HANDOFF_REVISED_READY
ciclo:           H-0019
título:          Layout horizontal plano do corpo
depende-de:      H-0018 (implementado, IMP-0018, QA_POST_CORRECTIONS_APPROVED — commit 46e0cb9)
commit-base:     9d4c74d  docs: formaliza composicao hierarquica do corpo
data-criacao:    2026-07-09
data-revisao:    2026-07-10
status-anterior: BLOCKED_BY_ADR_0015_PENDING_REVISION
autor-handoff:   Claude Code
executor:        OpenCode / GLM
```

---

## Status

```
HANDOFF_REVISED_READY
```

Este handoff foi revisado após a formalização e commit da ADR-0015. A versão
anterior estava bloqueada com `BLOCKED_BY_ADR_0015_PENDING_REVISION` e não
devia ser implementada.

A versão atual está compatível com a ADR-0015 e com os contratos atualizados
(v0.3 de `contrato_composicao_corpo.md`, conforme commit `9d4c74d`).

Implementação só pode ocorrer com base nesta versão revisada, após nova
auditoria.

---

## Revisão pós-ADR-0015

### Histórico do bloqueio

O handoff H-0019 foi criado em 2026-07-09 com base no levantamento
pós-H-0018 (commit `3b98856`). Foi auditado (resultado
`HANDOFF_APPROVED_WITH_NOTES`, relatório
`RELATORIO_AUDITORIA_H-0019_HANDOFF.md`) e então bloqueado pelo commit da
ADR-0015 antes de qualquer implementação.

Status anterior: `BLOCKED_BY_ADR_0015_PENDING_REVISION`

Nenhuma linha de código foi escrita com base na versão anterior do H-0019.

### Autoridade da revisão

A ADR-0015 (`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`,
commit `9d4c74d`) é autoridade superior ao H-0019 e a todos os contratos
de módulo anteriores. Onde a versão anterior do H-0019 contradiz a ADR-0015,
a ADR-0015 prevalece.

### Mudanças conceituais aplicadas nesta revisão

**1. `grupo` NÃO é expandido no layout horizontal plano**

A versão anterior do H-0019 (Passo 1 do algoritmo) "expandia" grupos
coletando seus filhos internos como funcionais no mesmo nível:

```python
# INTERPRETAÇÃO REJEITADA — versão anterior
if elemento.tipo == "grupo":
    for interno in elemento.elementos:
        funcionais.append(interno)  # ERRADO segundo ADR-0015
```

A ADR-0015 (Decisão 2) estabelece que `grupo` é nó estrutural que recebe
área do container pai e redistribui internamente — não é transparente.
No H-0019 "plano", cada filho direto de `corpo.elementos[]` — incluindo
`grupo` — conta como um slot que recebe área alocada. Como `grupo` não tem
representação visual própria (sem borda, sem moldura, sem conteúdo),
a área alocada a um `grupo` fica visualmente vazia no H-0019. Isso é
correto: a redistribuição interna do grupo é responsabilidade do H-0020.

Consequência: o teste `test_arranjo_horizontal_grupo_estrutural` da
versão anterior foi movido para "Fora de escopo futuro" (H-0020).

**2. "lado a lado" removido como termo normativo**

A expressão "lado a lado" não deve aparecer como termo normativo em texto
livre neste handoff. Usos substituídos por:

- `arranjo horizontal`
- `particionamento contíguo da largura`
- `filhos diretos`
- `área alocada`
- `bordas adjacentes coladas`

O alias transitional `lado_a_lado` (entre backticks, literal) permanece
como nome de campo aceito pelo loader — não é termo normativo em prosa.

**3. N+1 vãos e 3 vãos: interpretações rejeitadas**

A regra de "N+1 vãos iguais" (borda↔coluna_1, coluna_1↔coluna_2,
coluna_2↔borda) foi adotada na primeira versão deste handoff e rejeitada
pelo usuário na revisão pós-auditoria de 2026-07-09. Permanece registrada
apenas como interpretação histórica rejeitada nos riscos (R-4).

A regra vigente é **particionamento contíguo** da largura disponível
entre filhos diretos — consequência natural de dividir a área entre os
filhos sem vão externo. Formalizadapela ADR-0015 Decisão 9.

**4. Distribuição: Opção A adotada**

Veja seção "Política para distribuição neste ciclo".

**5. Commit base atualizado**

O commit base desta versão revisada é `9d4c74d` (ADR-0015 commitada),
não `3b98856` (levantamento pós-H-0018). A implementação deve ocorrer
a partir deste estado do repositório.

### Proteção de implementações anteriores

Qualquer implementação baseada na versão anterior do H-0019 (status
`BLOCKED_BY_ADR_0015_PENDING_REVISION`) deve parar imediatamente com:

```
ARCHITECTURE_REVIEW_REQUIRED
```

---

## Metadados de rastreabilidade

| Item | Referência |
|------|-----------|
| ID | H-0019 |
| Commit base (revisão) | `9d4c74d  docs: formaliza composicao hierarquica do corpo` |
| Commit base (criação original) | `3b98856  docs: registra levantamento pos H-0018` |
| Relatório levantamento pós-H-0018 | `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO.md` |
| Relatório auditoria H-0019 | `docs/relatorios/RELATORIO_AUDITORIA_H-0019_HANDOFF.md` |
| Relatório revisão pós-ADR-0015 | `docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md` |
| Relatório de implementação a gerar | `docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md` |
| Relatório de QA a gerar | `docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md` |
| Ciclos preservados | H-0015, H-0016, H-0017, H-0018 (todos fechados, artefatos presentes) |
| Baseline no momento da revisão | 544/544 verificações em 6 suítes |
| Contratos aplicáveis | `contrato_processo_desenvolvimento.md`, `contrato_tela_json.md`, `contrato_composicao_corpo.md` (v0.3), `contrato_barra_de_menus.md`, `contrato_lancador.md`, `contrato_console.md`, `contrato_json_tela_minima.md`, `contrato_json_lancador.md`, `contrato_json_console.md`, `contrato_json_dashboard.md` |
| ADRs normativas | ADR-0008, ADR-0010, ADR-0011, ADR-0013, ADR-0014, ADR-0015 (autoridade superior) |

---

## Ordem de autoridade

```
contrato_processo_desenvolvimento.md
  > ADR-0015 (autoridade superior — formaliza composição hierárquica e distribuição)
    > ADR-0008, ADR-0010, ADR-0011, ADR-0013, ADR-0014
      > contratos de módulo (contrato_composicao_corpo.md v0.3, contrato_tela_json.md, ...)
        > este handoff revisado (H-0019, HANDOFF_REVISED_READY)
          > decisões de implementação locais (IMP-0019)
```

O executor não decide arquitetura. Se qualquer item normativo estiver ausente
ou conflitante, bloquear com `ARCHITECTURE_REVIEW_REQUIRED` antes de
implementar qualquer linha de código.

---

## Contexto

Os ciclos H-0015 a H-0018 estabilizaram a ocupação vertical da janela
(H-0015), a migração e cobertura da `barra_de_menus` (H-0016, H-0017,
H-0018). A `barra_de_menus` está protegida e não deve ser alterada neste
ciclo.

A ADR-0015 (commit `9d4c74d`) formalizou o corpo como árvore de composição,
`grupo` como nó estrutural, arranjo e distribuição por container, arredondamento
determinístico, preenchimento de área alocada, regras dinâmicas de dimensão
(conceituais) e sincronização de cortes (conceitual).

O `contrato_composicao_corpo.md` (v0.3) foi atualizado pela ADR-0015. A seção
5.6 registra como regra vigente o **particionamento contíguo** da largura
disponível entre filhos diretos. A regra anterior de "3 vãos iguais" está
explicitamente supersedida.

O campo `corpo.arranjo` já é armazenado no modelo (`Corpo.arranjo: str | None`)
mas **não é lido pelo renderer** e **não é validado pelo loader no nível da
tela**. O renderer atual empilha todos os elementos verticalmente, ignorando
o arranjo declarado.

Estado verificado no código (commit `9d4c74d`):

- `loader.py` linha 347: `arranjo = corpo.get("arranjo")` — aceita qualquer
  valor, incluindo `"diagonal"`, sem erro.
- `modelo.py`: `Corpo(arranjo=..., elementos=[...])` — armazena sem validar.
- `renderizador.py` (`renderizar_tela`): laço sequencial sobre
  `modelo.corpo.elementos`; o campo `modelo.corpo.arranjo` **não é lido**.
- JSONs ativos: `destino_minimo.json` e `stub_b.json` declaram
  `"arranjo": "sobreposto"` (alias transitional de `"vertical"`, ADR-0011).
  Nenhum JSON ativo usa `"horizontal"`.

---

## Problema

1. **Renderer ignora `corpo.arranjo`**: telas com `arranjo = "horizontal"` são
   renderizadas verticalmente sem erro e sem aviso — comportamento
   silenciosamente incorreto.
2. **Loader não valida `arranjo` no nível da tela**: valor inválido como
   `"diagonal"` é aceito silenciosamente.
3. **Nenhum JSON ativo usa `horizontal`**: a funcionalidade não pode ser
   verificada em integração sem criar ou adaptar uma fixture.

---

## Objetivo

Implementar suporte mínimo e verificável a `corpo.arranjo = "horizontal"` com
**particionamento contíguo** da largura disponível entre filhos diretos de
`corpo.elementos[]`, sem `distribuicao` explícita (modo uniforme implícito),
sem grupos hierárquicos aninhados com redistribuição interna, sem percentual/
fração e sem aninhamento.

O escopo é o menor ciclo funcional verificável que abre o eixo de layout
horizontal do corpo:

- Loader valida `arranjo` no nível da tela.
- Renderer lê `modelo.corpo.arranjo` e aplica particionamento horizontal
  quando declarado.
- Aliases transicionais funcionam de forma determinística.
- Testes cobrem os novos comportamentos.
- Baseline 544/544 continua passando.

---

## Leitura obrigatória

O executor deve ler na íntegra antes de tocar qualquer arquivo:

1. `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
2. `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0015_COMPOSICAO_HIERARQUICA_DISTRIBUICAO_CORPO.md`
3. `docs/relatorios/RELATORIO_VERIFICACAO_DOCUMENTAL_ADR-0015_POS_CORRECAO.md`
4. `docs/relatorios/RELATORIO_REVISAO_H-0019_HANDOFF_POS_ADR-0015.md`
5. `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO.md`
6. `docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md`
7. `docs/relatorios/RELATORIO_QA_H-0018_POS_CORRECOES.md`
8. `docs/NOMENCLATURA.md`
9. `docs/contratos/contrato_processo_desenvolvimento.md`
10. `docs/contratos/contrato_tela_json.md`
11. `docs/contratos/contrato_composicao_corpo.md` (v0.3)
12. `docs/contratos/contrato_barra_de_menus.md`
13. `docs/contratos/contrato_lancador.md`
14. `docs/contratos/contrato_console.md`
15. `docs/contratos/contrato_json_tela_minima.md`
16. `docs/contratos/contrato_json_lancador.md`
17. `docs/contratos/contrato_json_console.md`
18. `docs/contratos/contrato_json_dashboard.md`
19. `tela/loader.py` (integralmente)
20. `tela/modelo.py` (integralmente)
21. `tela/renderizador.py` (integralmente)
22. `tela/demo.py` (integralmente)
23. `tela/diagnostico.py` (integralmente)
24. `tela/teste_loader.py` (integralmente)
25. `tela/teste_modelo.py` (integralmente)
26. `tela/teste_renderizador.py` (integralmente)
27. `tela/teste_demo.py` (integralmente)
28. `tela/teste_diagnostico.py` (integralmente)
29. `config/telas/orquestrador.json`
30. `config/telas/grupo_minimo.json`
31. `config/telas/destino_minimo.json`
32. `config/telas/stub_b.json`
33. Este handoff até o final.

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
   Para "horizontal", "lado_a_lado": aplicar particionamento contíguo
   da largura disponível entre filhos diretos de corpo.elementos[].

3. Criar ou adaptar ao menos um JSON de teste com arranjo = "horizontal".
   (Decisão explícita exigida pelo executor — ver seção "Especificação
   funcional por módulo / JSONs de teste")

4. Adicionar testes em tela/teste_renderizador.py.

5. Adicionar testes em tela/teste_loader.py.

6. Migração de destino_minimo.json e stub_b.json de "sobreposto" para
   "vertical": OPCIONAL — somente se bundled como migração declarativa
   acoplada à validação de aliases. Ver seção de JSONs de teste.

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
NÃO implementar distribuição percentual de largura.
NÃO implementar distribuição por fração/pesos.
NÃO implementar distribuicao explícita como campo JSON neste ciclo.
NÃO implementar redistribuição interna de grupo (H-0020).
NÃO implementar arranjo horizontal dentro de grupo aninhado.
NÃO implementar combinação horizontal + dashboard + indicador de paginação.
NÃO migrar posicao_dashboard.
NÃO implementar console real (conteúdo de dados real).
NÃO implementar navegação por [✥].
NÃO implementar foco entre elementos.
NÃO implementar seleção.
NÃO implementar paginação real.
NÃO implementar terminal pequeno com reticências (...).
NÃO implementar filtros.
NÃO alterar ações ou registry.
NÃO criar registry novo.
NÃO alterar ADR, contrato ou NOMENCLATURA.md.
NÃO reabrir H-0011.
NÃO recriar H-0011A.
NÃO usar H-0011 ou H-0011A como base implementável.
NÃO expandir grupo em filhos funcionais no layout horizontal.
NÃO implementar sincronização de cortes entre grupos.
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
- Snapshots de `teste_demo.py` e `teste_diagnostico.py` — alterar **somente**
  se houver mudança visual inevitável e justificada; registrar no IMP-0019
  qualquer alteração.

Os seguintes artefatos não devem ser alterados neste ciclo:

- `tela/explorar_barra_de_menus.py`
- `tela/teste_explorar_barra_de_menus.py`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_chip.md`
- `docs/adr/` (qualquer arquivo)
- `docs/contratos/` (exceto JSONs de teste em `config/telas/`)
- `docs/NOMENCLATURA.md`

Qualquer necessidade de alterar `_linhas_barra`, `_normaliza_distribuicao`,
`_validar_distribuicao` ou qualquer arquivo da `barra_de_menus` deve parar
com `ARCHITECTURE_REVIEW_REQUIRED`.

---

## Especificação funcional por módulo

### `tela/loader.py`

**Onde alterar**: após a linha `arranjo = corpo.get("arranjo")` (linha 347
do commit base `9d4c74d`).

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

A constante `ARRANJOS_CORPO_VALIDOS` pode ser definida ao nível do módulo
para permitir importação em testes. A exceção usada deve ser
`TelaEstruturaInvalida` (já existente).

**O que preservar**: todo o restante do loader, especialmente `_validar_grupo`,
que já rejeita `"horizontal"` e `"lado_a_lado"` em grupos — essa validação
é sobre GRUPOS, não sobre o nível da tela, e deve ser preservada intacta.

**Não alterar**: `TIPOS_CORPO_VALIDOS`, `TIPOS_ESTRUTURAIS_VALIDOS`,
`_validar_grupo`, nenhuma outra lógica de validação.

---

### `tela/modelo.py`

**Não alterar.** `Corpo.arranjo: str | None` já armazena qualquer valor.
A validação é responsabilidade do loader. O modelo não precisa de
modificações para suportar H-0019.

Se o executor identificar necessidade de alterar o modelo, deve bloquear
com `ARCHITECTURE_REVIEW_REQUIRED` e descrever a necessidade precisamente.

---

### `tela/renderizador.py`

**Onde alterar**: apenas na função `renderizar_tela`, especificamente no
trecho que percorre `modelo.corpo.elementos` para montar `partes`.

**O que NÃO alterar**: `_normaliza_distribuicao`, `_validar_distribuicao`,
`_linhas_barra`, `_validar_ancoras`, `_montar_coluna_a_coluna`,
`_montar_linha_a_linha`, `_texto_chip_barra`, `_caixa_de_elemento`,
`_caixa`, `_linha_topo`, `_linha_base`, `_linha_conteudo`.

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
    # Ver seção "Algoritmo de particionamento horizontal do corpo"
    bloco_horizontal = _montar_corpo_horizontal(
        modelo.corpo.elementos, borda, total_w, inner_w, content_w, label_max
    )
    partes.append(bloco_horizontal)
else:
    # Comportamento atual (vertical / None / sobreposto normalizado)
    for elemento in modelo.corpo.elementos:
        ...  # código existente preservado integralmente
```

A função auxiliar `_montar_corpo_horizontal` recebe a lista de elementos
e os parâmetros de dimensionamento. Ver algoritmo na seção seguinte.
A função é interna ao módulo.

**Preenchimento vertical (H-0015)**: a lógica de `altura` deve continuar
funcionando após a introdução do horizontal. O bloco horizontal é tratado
como um único bloco de string (como qualquer outra parte de corpo), e
`l_corpo_conteudo` deve contar suas linhas normalmente. Não alterar a
lógica de preenchimento H-0015.

---

### JSONs de teste/configuração

O executor deve decidir **uma** das opções abaixo e registrar a decisão
no IMP-0019:

**Opção A — Criar JSON mínimo novo** (`config/telas/horizontal_teste.json`):

- Tela de teste com `arranjo = "horizontal"` e dois ou mais elementos
  funcionais diretos.
- Não perturba JSONs de produção.
- Referenciada apenas nos testes do renderer.

**Opção B — Adaptar fixture existente no teste** (in-memory):

- Construir `ModeloTela` sinteticamente no teste sem carregar JSON de disco.
- Não cria novo arquivo JSON.
- Mais isolado; menor superfície de mudança.

**Regras independentes da opção escolhida**:

- Não alterar `orquestrador.json` nem `grupo_minimo.json`.
- Não alterar `destino_minimo.json` nem `stub_b.json` (a menos que a
  migração opcional abaixo seja incluída).

**Migração opcional de aliases** (`"sobreposto"` → `"vertical"` em
`destino_minimo.json` e `stub_b.json`): pode ser incluída neste ciclo
somente se declarada explicitamente no IMP-0019, a migração for pequena
(2 arquivos, 1 campo cada), e os snapshots de `teste_demo.py` e
`teste_diagnostico.py` não precisarem de alteração (comportamento visual
idêntico). Se a migração NÃO for incluída, registrar como pendência
posterior no IMP-0019.

---

## Algoritmo de particionamento horizontal do corpo

O algoritmo se aplica quando `arranjo_corpo == "horizontal"` (após
normalização de aliases).

**Regra fundamental (ADR-0015, Decisão 9)**: o espaço horizontal é
particionado de forma **contígua** entre filhos diretos de
`corpo.elementos[]`. Não existem vãos externos entre áreas adjacentes.
A primeira área começa no primeiro caractere útil da linha. A última área
termina no último caractere útil da linha. Áreas adjacentes ficam coladas,
produzindo bordas adjacentes: `││` em linhas internas, `╮╭` no topo e
`╯╰` na base (conforme estilo ativo). Esta é consequência natural do
particionamento — não é regra de vãos.

### Sobre `grupo` neste algoritmo

`grupo` em `corpo.elementos[]` **não é expandido** neste algoritmo
(conforme ADR-0015, Decisão 2). Cada filho direto de `corpo.elementos[]`
— funcional ou estrutural — conta como um slot que recebe área alocada.
`grupo` não tem representação visual própria; sua área alocada fica
visualmente vazia no H-0019. Suporte à redistribuição interna de `grupo`
vai para H-0020.

### Entradas

- `elementos`: lista de `ElementoCorpo` de `modelo.corpo.elementos`
  (todos os filhos diretos do container raiz `corpo`)
- `borda`, `total_w`, `inner_w`, `content_w`, `label_max`: parâmetros
  de dimensionamento da tela

### Passo 1 — Identificar filhos diretos

```python
# Trabalha com todos os filhos diretos de corpo.elementos[]
# Grupo: slot com área alocada, sem renderização interna no H-0019
N = len(elementos)
if N == 0:
    return ""
if N == 1:
    # Um único filho direto: renderizar na largura total (sem particionamento)
    caixa = _caixa_de_elemento(elementos[0], borda, inner_w, content_w, label_max)
    return caixa if caixa else ""
```

### Passo 2 — Calcular largura de cada área por particionamento contíguo

```python
# Distribuição uniforme (modo igual — Opção A, H-0019 sem distribuicao explícita)
base_w = total_w // N
resto = total_w % N
# Arredondamento por maiores restos (ADR-0015, Decisão 8):
# as primeiras `resto` áreas recebem base_w + 1; as demais recebem base_w.
# Invariante: sum(larguras) == total_w
larguras = [base_w + (1 if i < resto else 0) for i in range(N)]
```

Verificar cabimento mínimo (molduras + conteúdo mínimo):

```python
for i, w in enumerate(larguras):
    if w < 10:
        raise RenderizadorErro(
            "arranjo horizontal: largura {0} insuficiente para {1} elementos "
            "no particionamento horizontal (minimo 10 chars por area; "
            "area {2} calculada com {3})".format(total_w, N, i, w)
        )
```

Parâmetros derivados para cada área `i` (onde `w = larguras[i]`):

```python
inner_w_i   = w - 2
content_w_i = w - 3
label_max_i = w - 4
```

### Passo 3 — Renderizar cada filho em sua área alocada

Para cada filho em `elementos`, renderizar com a largura de sua área:

```python
caixa_str = _caixa_de_elemento(
    elemento, borda, inner_w_i, content_w_i, label_max_i
)
if caixa_str is None:
    # Elemento estrutural (grupo) ou tipo desconhecido: área vazia
    caixa_str = ""
```

Converter `caixa_str` em lista de linhas: `linhas_area = caixa_str.split("\n")`.

### Passo 4 — Normalizar altura com preenchimento inferior

```python
altura_max = max(len(linhas) for linhas in todas_as_linhas_por_area)
for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_max:
        # Preenchimento dentro da área alocada (ADR-0015, Decisão 10)
        linhas.append(" " * larguras[i])
```

### Passo 5 — Concatenar áreas linha a linha (sem separador externo)

```python
linhas_resultado = []
for r in range(altura_max):
    linha = ""
    for i, linhas in enumerate(todas_as_linhas_por_area):
        linha += linhas[r]
    # Concatenação direta produz bordas adjacentes coladas:
    # - "││" em linhas internas
    # - "╮╭" no topo das áreas adjacentes
    # - "╯╰" na base das áreas adjacentes
    # Invariante: len(linha) == total_w (garantido pelo particionamento contíguo)
    linhas_resultado.append(linha)
resultado_str = "\n".join(linhas_resultado)
```

### Passo 6 — Preservações obrigatórias

- **Cabeçalho**: montado em `partes[0]` antes do laço de corpo.
  O bloco horizontal substitui o laço, mas `partes[0]` (cabeçalho)
  é preservado.
- **`barra_de_menus`**: montada e adicionada a `partes` APÓS o bloco
  do corpo, exatamente como no fluxo atual.
- **Preenchimento vertical (H-0015)**: o bloco horizontal resultante
  é uma string com múltiplas linhas. `_contar_linhas(bloco_horizontal)`
  deve retornar `len(linhas_resultado)`. O cálculo de `l_corpo_conteudo`
  deve somar `_contar_linhas(bloco_horizontal)`.
- **`altura` explícita**: quando fornecido, o total final da saída deve
  continuar tendo exatamente `altura` linhas.

---

## Política para aliases transicionais

| Valor declarado no JSON | Comportamento no renderer | Comportamento no loader |
|-------------------------|--------------------------|------------------------|
| `"vertical"` | Particionamento vertical (atual) | Aceito |
| `"horizontal"` | Particionamento horizontal plano | Aceito |
| `"sobreposto"` | Particionamento vertical (alias) | Aceito |
| `"lado_a_lado"` | Particionamento horizontal plano (alias) | Aceito |
| `None` / ausente | Particionamento vertical (default atual) | Aceito (None) |
| Qualquer outro valor | — | `TelaEstruturaInvalida` |

A normalização dos aliases ocorre no **renderer**, não no loader. O loader
apenas aceita o conjunto de valores válidos; o renderer mapeia aliases para
comportamento concreto. O modelo armazena o valor como declarado no JSON
(sem normalização no modelo).

`destino_minimo.json` e `stub_b.json` declaram `"sobreposto"`. Com a
validação do loader, `"sobreposto"` deve ser aceito (está no conjunto
válido). Portanto esses JSONs continuam funcionando sem alteração.

`"sobreposto"` e `"lado_a_lado"` são aliases transicionais literais —
não são terminologia final e não devem ser usados como termos normativos
em novos textos ou código. Novos JSONs e contratos devem usar `"vertical"`
ou `"horizontal"`.

---

## Política para distribuição neste ciclo

**Decisão: Opção A — Sem `distribuicao` explícita neste ciclo**

H-0019 implementa `corpo.arranjo = "horizontal"` com distribuição uniforme
implícita (`modo = igual`) entre filhos diretos de `corpo.elementos[]`.
Nenhum campo `distribuicao` é lido ou exigido no JSON neste ciclo.

**Justificativa**:

- `contrato_json_tela_minima.md` (v0.1, ADR-0015 aplicada) define
  `distribuicao` como **opcional** no container.
- ADR-0015 Decisão 6 define `modo = igual` como modo válido: divide a
  área disponível igualmente entre filhos diretos.
- Nenhuma regra nos contratos vigentes proíbe distribuição uniforme
  implícita quando `distribuicao` não é declarada.
- Os JSONs existentes (`orquestrador.json`, `destino_minimo.json`, etc.)
  não declaram `distribuicao` no `corpo`.

**O que fica fora de escopo**:

- `distribuicao.modo = "percentual"` (H-0020 ou posterior)
- `distribuicao.modo = "fracao"` (H-0020 ou posterior)
- `distribuicao.valores[]` como campo JSON (H-0020 ou posterior)
- Regras dinâmicas de mínimo/preferido/máximo (ciclo futuro)

**Registro obrigatório no IMP-0019**: o executor deve registrar
explicitamente a adoção da Opção A e confirmar que os contratos vigentes
permitem distribuição uniforme implícita.

---

## Política para largura insuficiente

Se `base_w < 10` (equivalente a `total_w // N < 10`):

```
→ RenderizadorErro determinístico.

Mensagem deve incluir: total_w, N, largura calculada da área.
Nunca truncar silenciosamente.
Nunca omitir elemento.
Nunca reordenar elemento.
Nunca fazer fallback silencioso para arranjo vertical.
```

Política de terminal muito pequeno com reticências (`...`) está
**explicitamente fora de escopo do H-0019** (ADR-0015 Decisão 13 registra
como conceito futuro). O H-0019 usa apenas `RenderizadorErro` determinístico.

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
    Confirmar sem erro (alias transitional aceito).

test_loader_arranjo_lado_a_lado_aceito:
    arranjo = "lado_a_lado".
    Confirmar sem erro (alias transitional aceito).

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
    Confirmar que a saída tem os 2 elementos empilhados (particionamento vertical).
    Confirmar que barra_de_menus aparece ao final.

test_arranjo_vertical_preserva_comportamento:
    Modelo com corpo.arranjo = "vertical", 2 elementos.
    Confirmar saída idêntica ao caso None.
    Confirmar sem erro.

test_arranjo_sobreposto_preserva_vertical:
    Modelo com corpo.arranjo = "sobreposto".
    Confirmar saída idêntica ao caso "vertical".
    Confirmar sem erro.

test_arranjo_horizontal_dois_elementos:
    Modelo com corpo.arranjo = "horizontal", 2 elementos funcionais diretos
    (ex.: lancador + dashboard).
    Confirmar que as 2 áreas aparecem na mesma faixa de linhas na saída.
    Confirmar que a barra_de_menus aparece ABAIXO do bloco horizontal.
    Confirmar que o número total de linhas é menor que com arranjo vertical.

test_arranjo_lado_a_lado_alias_horizontal:
    Modelo com corpo.arranjo = "lado_a_lado".
    Confirmar saída idêntica ao caso "horizontal".
    Confirmar sem erro.

test_arranjo_horizontal_areas_contiguas:
    Modelo com corpo.arranjo = "horizontal", 2 elementos, largura=42.
    Extrair as linhas do bloco horizontal e confirmar que:
    - aparece "││" (duas laterais adjacentes) nas linhas internas;
    - aparece "╮╭" (ou equivalente conforme estilo ativo) na linha de topo;
    - aparece "╯╰" (ou equivalente conforme estilo ativo) na linha de base;
    - o primeiro caractere de cada linha é a lateral esquerda da primeira área
      (primeira área começa no primeiro caractere útil);
    - o último caractere de cada linha é a lateral direita da última área
      (última área termina no último caractere útil);
    - cada linha tem exatamente 42 caracteres (largura total preservada).

test_arranjo_horizontal_resto_deterministico:
    Modelo com corpo.arranjo = "horizontal", 3 elementos, largura não
    divisível por 3 (ex.: 100).
    Confirmar que as larguras somam exatamente 100.
    Confirmar que as áreas com resto extra são as primeiras (índices 0, 1, ...).
    Exemplo: 100 // 3 = 33, resto = 1 → larguras [34, 33, 33].

test_arranjo_horizontal_padding_inferior:
    Modelo com corpo.arranjo = "horizontal", 2 elementos com alturas
    diferentes após renderização.
    Confirmar que o bloco horizontal tem altura uniforme (a menor área
    é preenchida com linhas de espaços dentro da sua largura alocada).

test_arranjo_horizontal_largura_insuficiente:
    Modelo com corpo.arranjo = "horizontal", 2 elementos, largura pequena
    (ex.: 18).
    Confirmar RenderizadorErro com mensagem determinística mencionando
    "arranjo horizontal".
    Confirmar que NÃO há fallback silencioso para arranjo vertical.

test_arranjo_horizontal_tres_elementos:
    Modelo com corpo.arranjo = "horizontal", 3 elementos funcionais diretos.
    Confirmar que os 3 aparecem na mesma faixa de linhas na saída.

test_arranjo_horizontal_com_altura_preserva_h0015:
    Modelo com corpo.arranjo = "horizontal", altura=40 (ou qualquer valor
    suficiente).
    Confirmar que a saída tem exatamente 40 linhas (preenchimento vertical
    de H-0015 funciona com arranjo horizontal).

test_arranjo_horizontal_barra_preservada:
    Modelo com corpo.arranjo = "horizontal".
    Confirmar que _linhas_barra é chamada normalmente e a barra aparece
    ao rodapé.
    Confirmar que nenhuma alteração ocorreu em barra_de_menus, chips ou
    distribuicao da barra.
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
(JSON novo vs fixture in-memory; migração de aliases bundled vs adiada;
 confirmação de Opção A para distribuição)

## Implementação em loader.py
(Constante ARRANJOS_CORPO_VALIDOS; onde inserida; trecho de código)

## Implementação em renderizador.py
(Função _montar_corpo_horizontal; onde inserida no fluxo; interação com H-0015;
 confirmação de que grupo não é expandido)

## Testes do loader adicionados

## Testes do renderer adicionados

## Alterações em snapshots (se houver)
(Justificativa obrigatória para qualquer snapshot alterado)

## Resultados de testes
(Tabela: suite / verificações / exit code)

## Execuções do explorador (confirmar que não foram afetadas)

## Confirmação de escopo negativo
(Confirmar que barra_de_menus, _normaliza_distribuicao, _validar_distribuicao,
 _linhas_barra não foram alteradas; confirmar que grupo não foi expandido;
 confirmar Opção A adotada)

## Limitações conhecidas

## Pendências para ciclo futuro
```

---

## Critérios de aceite

```
 1. corpo.arranjo = "vertical" preserva particionamento vertical atual
    (empilhamento sequencial). Saída idêntica ao comportamento pré-H-0019.

 2. corpo.arranjo = "sobreposto" preserva particionamento vertical atual
    como alias transitional. Saída idêntica ao caso "vertical".

 3. corpo.arranjo = None preserva comportamento atual (vertical por default).

 4. corpo.arranjo = "horizontal" renderiza dois ou mais filhos diretos com
    particionamento contíguo da largura disponível. As áreas de cada filho
    aparecem na mesma faixa horizontal de linhas.

 5. corpo.arranjo = "lado_a_lado" renderiza como alias transitional de
    horizontal. Saída idêntica ao caso "horizontal".

 6. O particionamento horizontal usa distribuição uniforme implícita (Opção A)
    entre N filhos diretos de corpo.elementos[]. Não existem vãos externos
    entre áreas. Áreas adjacentes ficam coladas, produzindo bordas adjacentes:
    "││" nas linhas internas, "╮╭" no topo e "╯╰" na base (conforme estilo
    ativo). A primeira área inicia no primeiro caractere útil da linha.
    A última área termina no último caractere útil. A soma das larguras das
    áreas é exatamente total_w (invariante do particionamento contíguo).
    O resto da divisão inteira (total_w % N) é distribuído deterministicamente
    — uma unidade extra nas primeiras `resto` áreas (maiores restos, ADR-0015
    Decisão 8).

 7. Filhos com alturas diferentes recebem preenchimento inferior de linhas
    de espaços dentro da sua área alocada, de forma que todas as colunas
    tenham a mesma altura (ADR-0015 Decisão 10).

 8. Largura insuficiente para comportar N filhos com w_area >= 10 gera
    RenderizadorErro determinístico, sem truncamento e sem fallback silencioso
    para arranjo vertical.

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

15. `grupo` em corpo.elementos[] não é expandido; conta como slot alocado
    com área vazia no H-0019.
```

---

## Riscos e mitigação

### R-1 — Confundir `corpo.arranjo = "horizontal"` com `barra_de_menus.distribuicao.modo = "horizontal_responsiva"`

**Descrição**: os dois contextos usam a substring `"horizontal"` com semânticas
completamente distintas. `corpo.arranjo = "horizontal"` é composição dos
elementos do corpo (ADR-0011). `barra_de_menus.distribuicao.modo =
"horizontal_responsiva"` é distribuição visual dos chips (ADR-0014). São
módulos, regiões e contratos distintos.

**Sintoma de confusão**: alterar `_linhas_barra`, `_normaliza_distribuicao`
ou `_validar_distribuicao` ao trabalhar no arranjo do corpo.

**Mitigação**: buscas devem usar padrões específicos: `modelo.corpo.arranjo`
ou `"arranjo":` para o corpo; `barra_de_menus.distribuicao` para a barra.
Filtros por substring `"horizontal"` são proibidos como critério de alteração
automática (ADR-0014). O H-0019 toca apenas a função `renderizar_tela` e o
trecho de validação do loader — não toca nenhuma função de barra.

---

### R-2 — Substituição por substring `"horizontal"` ou `"vertical"`

**Descrição**: usar grep/replace global por `"horizontal"` ou `"vertical"` em
qualquer arquivo pode acidentalmente alterar `_normaliza_distribuicao` (que
testa a string `"horizontal"` para alias de `barra_de_menus.distribuicao`)
ou comentários e snapshots não relacionados.

**Mitigação**: toda alteração deve ser feita por localização precisa de
linha/função. Nunca usar substituição global por substring ambígua (ADR-0014,
Parte B). O executor deve identificar exatamente as linhas a alterar antes
de escrever qualquer código.

---

### R-3 — Reabrir H-0011 ou H-0011A

**Descrição**: ao implementar o particionamento horizontal, pode surgir
tentação de referenciar ou reabrir H-0011 (renderização com barra mínima —
CANCELADO antes de qualquer implementação) ou H-0011A (REMOVIDO por
granularidade excessiva) como "base histórica".

**Mitigação**: H-0011 e H-0011A permanecem como referências históricas
arquivadas. Nenhum código, decisão ou estrutura deste ciclo pode ser baseada
nesses artefatos. O H-0019 é independente e se baseia nos contratos ADR-0011,
ADR-0015 e `contrato_composicao_corpo.md` v0.3.

---

### R-4 — Introduzir vão externo ou espaçamento entre áreas

**Descrição**: implementar qualquer forma de espaço vazio entre as áreas do
particionamento horizontal — seja "N+1 vãos iguais" (INTERPRETAÇÃO
REJEITADA), "3 vãos" (INTERPRETAÇÃO REJEITADA), vão lateral, padding entre
colunas ou qualquer separador entre áreas adjacentes.

**Por que é risco**: a regra correta (ADR-0015 Decisão 9) é particionamento
contíguo: não existe vão externo entre áreas. Introduzir separadores viola
a regra e produz saída visual incorreta.

**Interpretação rejeitada historicamente**: a especificação original de
N+1 vãos iguais (borda↔coluna_1, coluna_1↔coluna_2, coluna_2↔borda) foi
adotada na versão inicial do handoff e rejeitada pelo usuário por decisão
explícita pós-auditoria (2026-07-09). Não retomar essa interpretação.

**Mitigação**: a largura de cada área é calculada por
`larguras[i] = total_w // N + (1 if i < resto else 0)`,
com `sum(larguras) == total_w`. A concatenação das áreas é direta,
sem separador.

---

### R-5 — Expandir `grupo` em filhos funcionais

**Descrição**: ao implementar o particionamento horizontal, reproduzir a
lógica da versão anterior do H-0019 (Passo 1 antigo) que expandia `grupo`
em seus filhos internos como se fossem filhos funcionais diretos.

**Por que é risco**: ADR-0015 Decisão 2 define `grupo` como nó estrutural
que recebe área do container pai e redistribui internamente. `grupo` não
é transparente. Expandir grupo no H-0019 antecipa comportamento que pertence
ao H-0020 e pode gerar inconsistências com o modelo de árvore do corpo.

**Mitigação**: Passo 1 do algoritmo revisado itera diretamente sobre
`elementos` sem expansão. `_caixa_de_elemento` retorna `None` para grupo
(sem visual); a área alocada fica visualmente vazia no H-0019.

---

### R-6 — Regressão na barra_de_menus estabilizada no H-0018

**Descrição**: ao modificar `renderizar_tela` para suportar arranjo
horizontal, introduzir inadvertidamente chamada a `_linhas_barra` com
parâmetros errados ou alterar o fluxo de montagem da caixa da barra.

**Sintoma**: testes de `TestDistribuicaoH0018` ou
`teste_explorar_barra_de_menus.py` falham após as alterações.

**Mitigação**: executar `PYTHONDONTWRITEBYTECODE=1 python
tela/teste_renderizador.py` e `PYTHONDONTWRITEBYTECODE=1 python
tela/teste_explorar_barra_de_menus.py` após cada alteração incremental
no renderer. A barra_de_menus deve ser a ÚLTIMA parte adicionada a `partes`,
exatamente como no fluxo atual.

---

### R-7 — Fallback silencioso de horizontal para vertical

**Descrição**: implementar horizontal de forma que, se a largura for
insuficiente ou houver erro, a saída caia silenciosamente para o arranjo
vertical sem erro.

**Por que é risco**: viola o princípio de que o renderer nunca faz fallback
silencioso (ADR-0014/ADR-0015). O executor não pode saber que o arranjo
declarado não foi respeitado.

**Mitigação**: qualquer condição que impeça o particionamento horizontal
deve lançar `RenderizadorErro` determinístico com mensagem descritiva.
Nunca alterar silenciosamente o comportamento. O critério de aceite 8
verifica explicitamente a ausência de fallback silencioso.

---

## Fora de escopo futuro

Os itens abaixo foram identificados e **explicitamente adiados**:

```
Implementação completa de grupos hierárquicos com redistribuição interna (H-0020)
Profundidade de 3 níveis
Arranjo dentro de grupo aninhado
Distribuição percentual de largura
Distribuição por fração/pesos
Distribuicao como campo JSON explícito no corpo
Regras dinâmicas de mínimo/preferido/máximo
Sincronização de cortes entre grupos
Paginação real
Terminal pequeno com reticências (...)
Console real com conteúdo de dados
Navegação por [✥]
Foco entre elementos
Seleção
Filtros
Ações
Registry novo
Alterações em barra_de_menus
Alterações em contratos
Alterações em ADRs
Alterações em NOMENCLATURA
Combinação corpo.arranjo = "horizontal" + dashboard presente (pendência de contrato)
Migração formal de destino_minimo.json e stub_b.json (se não bundled neste ciclo)
test_arranjo_horizontal_grupo_estrutural (redistribuição interna de grupo — H-0020)
```

---

## Exigência de nova auditoria

Esta versão revisada do H-0019 deve ser auditada antes de qualquer
implementação. A nova auditoria deve:

1. Confirmar que nenhuma regra ativa contradiz a ADR-0015.
2. Confirmar que "lado a lado" não aparece como termo normativo.
3. Confirmar que grupo não é expandido no algoritmo.
4. Confirmar que Opção A (distribuição uniforme implícita) está compatível
   com os contratos vigentes.
5. Confirmar que todos os testes obrigatórios cobrem os cenários listados.
6. Confirmar que a proteção da barra_de_menus está explícita.

Relatório de auditoria deve ser criado em:

```text
docs/relatorios/RELATORIO_AUDITORIA_H-0019_POS_REVISAO_ADR-0015.md
```

O executor não deve iniciar implementação antes de receber status de auditoria
`HANDOFF_APPROVED` ou equivalente do novo relatório.

---

## Saída esperada do implementador

```
IMPLEMENTATION_COMPLETED

arquivos-alterados:
  tela/loader.py
  tela/teste_loader.py
  tela/renderizador.py
  tela/teste_renderizador.py
  [config/telas/horizontal_teste.json  ← se Opção A de JSON for escolhida]
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
