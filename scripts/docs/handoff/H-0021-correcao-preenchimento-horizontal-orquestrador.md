# H-0021 — Correção pós-QA manual do preenchimento horizontal no orquestrador

## Status

```
HANDOFF_READY
```

---

## Metadados de rastreabilidade

| Item | Referência |
|------|-----------|
| ID | H-0021 |
| Commit base | `3132d4c  docs: registra investigacao pos H-0020` |
| Commit H-0020 | `79063ba  fix: preenche areas horizontais do corpo` |
| Relatório investigação pós-H-0020 | `docs/relatorios/RELATORIO_INVESTIGACAO_POS_H0020_HORIZONTAL_ORQUESTRADOR.md` |
| Relatório de implementação a gerar | `docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md` |
| Relatório de auditoria obrigatório | `docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md` |
| Ciclos anteriores fechados | H-0015 a H-0020 (todos commitados, artefatos presentes) |
| Baseline no momento do handoff | 621/621 verificações em 6 suítes |
| Contratos aplicáveis | `contrato_composicao_corpo.md` (v0.3), `contrato_tela_json.md`, `contrato_json_tela_minima.md`, `contrato_barra_de_menus.md` |
| ADRs normativas | ADR-0013, ADR-0014, ADR-0015 |

---

## Contexto

O H-0019 implementou particionamento horizontal contíguo da largura entre
filhos diretos de `corpo.elementos[]`. O H-0020 propagou `l_corpo_disponivel`
até `_montar_corpo_horizontal` e moveu o preenchimento vertical para dentro
de cada coluna, substituindo o fill externo H-0015 por fill interno
`" " * larguras[i]` por coluna.

A investigação pós-H-0020 (`RELATORIO_INVESTIGACAO_POS_H0020_HORIZONTAL_ORQUESTRADOR.md`)
revelou que o fill interno `" " * larguras[i]` é visualmente indistinguível
do fill externo H-0015: ao concatenar três colunas de larguras `27 + 27 + 26`,
o resultado é `" " * 80` — linha de espaços planos sem estrutura visual.

A causa raiz (H6 confirmada) é que `_caixa()` gera caixas completas
(topo + conteúdo + base). O fill adicionado em `_montar_corpo_horizontal`
vai **após** a base, não dentro da caixa estendida. Resultado: as caixas
fecham logo após o conteúdo e o fill abaixo não tem bordas laterais.

O H-0020 foi aprovado em QA automatizado (621/621) porque os testes
verificam apenas dimensões (número de linhas, largura) e **não** a presença
de bordas `│` nas linhas de preenchimento. Esta lacuna de cobertura (H4
confirmada) e a inconsistência entre a "Regra visual esperada" do H-0020
(caixas com bordas estendidas) e o algoritmo implementado (`" " * larguras[i]`)
são as causas secundárias.

O H-0021 corrige o preenchimento visual para que as caixas horizontais se
estendam visualmente até a altura alocada, com bordas laterais nas linhas de
fill e base na última linha da área horizontal.

---

## Problema

### Comportamento atual (com H-0020)

Em `_montar_corpo_horizontal` (`renderizador.py`, linha 754):

```python
for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_alvo:
        linhas.append(" " * larguras[i])
```

O fill `" " * larguras[i]` vai **abaixo da base** de cada caixa. Com três
colunas (`27 + 27 + 26 = 80`), a linha resultante é `" " * 80` —
visualmente idêntica ao fill externo H-0015 que o H-0020 pretendia substituir.

### Visual obtido (incorreto)

```
╭ ITENS ─────────────╮╭ INFO ──────────────╮╭ NAVEGAR ────────────╮
│ (console)           ││                    ││ [d] Destino         │
╰─────────────────────╯╰────────────────────╯│ [g] Grupo Min.      │
                                             ╰─────────────────────╯
         (linhas de espaços sem bordas — visualmente idêntico ao H-0015)
```

### Visual esperado (correto)

```
╭ ITENS ─────────────╮╭ INFO ──────────────╮╭ NAVEGAR ────────────╮
│ (console)           ││                    ││ [d] Destino         │
│                     ││                    ││ [g] Grupo Min.      │
│                     ││                    ││                     │
│                     ││                    ││                     │
╰─────────────────────╯╰────────────────────╯╰─────────────────────╯
```

### Contradição com ADR-0015

O comportamento atual contradiz:

- **D5** (Distribuição por container): elemento funcional deve preservar
  a área alocada; sobra vertical vira linhas em branco **dentro** do elemento.
- **D10** (Preenchimento de espaço vazio): preencher com linhas em branco
  que preservem a estrutura visual do container.

---

## Objetivo

Corrigir `_montar_corpo_horizontal` em `renderizador.py` para que, em
`corpo.arranjo = "horizontal"` ou `"lado_a_lado"`, cada caixa seja
visualmente estendida até a altura alocada:

1. Topo na linha 0.
2. Linhas de conteúdo nas linhas 1..k.
3. Linhas internas bordeadas (`│ ... │`) nas linhas k+1..h-2.
4. Base (`╰───╯`) na linha h-1 (última linha da altura alocada).

A concatenação de colunas bordadas gera bordas adjacentes coladas:

```
│        ││        │   ← linhas internas
╰────────╯╰────────╯   ← base na última linha
```

---

## Leitura obrigatória

O executor deve ler na íntegra antes de tocar qualquer arquivo:

1. `docs/relatorios/RELATORIO_INVESTIGACAO_POS_H0020_HORIZONTAL_ORQUESTRADOR.md`
2. `docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md`
3. `docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md`
4. `docs/relatorios/RELATORIO_QA_H-0020_PREENCHIMENTO_VERTICAL_AREAS_CORPO_HORIZONTAL.md`
5. `docs/handoff/H-0019-layout-horizontal-plano-corpo.md`
6. `docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md`
7. `docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md`
8. `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
9. `docs/NOMENCLATURA.md`
10. `docs/contratos/contrato_composicao_corpo.md` (v0.3)
11. `docs/contratos/contrato_tela_json.md`
12. `docs/contratos/contrato_json_tela_minima.md`
13. `tela/renderizador.py` (integralmente)
14. `tela/teste_renderizador.py` (integralmente)
15. `tela/demo.py` (integralmente)
16. `tela/loader.py` (integralmente)
17. `tela/modelo.py` (integralmente)
18. `config/telas/orquestrador.json`

Leia também apenas para proteção de regressão (não alterar):

```text
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
tela/explorar_barra_de_menus.py
```

---

## Escopo positivo

O H-0021 pode e deve implementar alterações apenas em:

```text
tela/renderizador.py
tela/teste_renderizador.py
docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md
```

As alterações são:

1. Extrair helper interno `_montar_caixa_com_altura` (ou adaptar `_caixa()`) em
   `renderizador.py` para gerar caixa bordeada com altura alvo — ver "Política
   para decomposição de caixa".
2. Modificar `_montar_corpo_horizontal` para usar o helper ao gerar cada coluna,
   produzindo linhas de fill bordeadas e base na última linha.
3. Adicionar testes em `tela/teste_renderizador.py` para os cenários listados
   na seção "Testes obrigatórios".
4. Criar `docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md`.

---

## Escopo negativo

O H-0021 **NÃO deve** implementar:

```
NÃO alterar loader.py.
NÃO alterar modelo.py.
NÃO alterar demo.py.
NÃO alterar barra_de_menus.distribuicao.
NÃO alterar _normalizar_distribuicao.
NÃO alterar _validar_distribuicao.
NÃO alterar _linhas_barra.
NÃO alterar _validar_ancoras.
NÃO alterar explorar_barra_de_menus.py.
NÃO alterar teste_explorar_barra_de_menus.py.
NÃO alterar contrato_barra_de_menus.md.
NÃO alterar contrato_chip.md.
NÃO alterar contratos.
NÃO alterar ADRs.
NÃO alterar NOMENCLATURA.md.
NÃO alterar JSONs de configuração (config/).
NÃO alterar orquestrador.json.
NÃO implementar distribuição vertical do corpo.
NÃO implementar corpo.distribuicao percentual/fracao.
NÃO implementar distribuição horizontal percentual/fracao.
NÃO implementar grupos hierárquicos.
NÃO implementar arranjo dentro de grupo.
NÃO implementar distribuicao dentro de grupo.
NÃO implementar profundidade de 3 níveis.
NÃO implementar sincronização de cortes.
NÃO implementar paginação real.
NÃO implementar terminal pequeno com reticências (...).
NÃO implementar configuração declarativa de largura da tela.
NÃO adicionar campo largura/dimensao no JSON.
NÃO implementar console real.
NÃO implementar navegação por [✥].
NÃO implementar foco entre elementos.
NÃO implementar seleção.
NÃO implementar filtros.
NÃO implementar ações.
NÃO criar registry novo.
NÃO fazer commit.
```

A distribuição vertical do corpo fica deslocada para:

```
H-0022 — Distribuição vertical do corpo e preenchimento das áreas alocadas
```

---

## Preservações obrigatórias

As seguintes funções e invariantes **não devem ser tocadas** (exceto conforme
permitido pela "Política para decomposição de caixa"):

- `_normalizar_distribuicao` (renderizador.py) — nome real com `r`
- `_validar_distribuicao` (renderizador.py)
- `_linhas_barra` (renderizador.py)
- `_validar_ancoras` (renderizador.py)
- `_montar_coluna_a_coluna` (renderizador.py)
- `_montar_linha_a_linha` (renderizador.py)
- `_texto_chip_barra` (renderizador.py)
- `_linha_topo` (renderizador.py)
- `_linha_base` (renderizador.py)
- `_linha_conteudo` (renderizador.py)
- `_contar_linhas` (renderizador.py)
- `_linhas_console` (renderizador.py)
- `_linhas_dashboard` (renderizador.py)
- `_linhas_lancador` (renderizador.py)
- Testes das classes `TestDistribuicaoH0018`, `TestArranjoH0019`,
  `TestPreenchimentoVerticalH0020` (atualizar se necessário, não remover)
- Snapshots de `teste_demo.py` e `teste_diagnostico.py` — não alterar

Os seguintes artefatos não devem ser alterados:

```
tela/loader.py
tela/modelo.py
tela/demo.py
tela/diagnostico.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/explorar_barra_de_menus.py
tela/teste_explorar_barra_de_menus.py
docs/contratos/ (todos)
docs/adr/ (todos)
docs/NOMENCLATURA.md
config/ (todos os JSONs)
```

**Nota sobre `TestPreenchimentoVerticalH0020`**: os testes existentes da
classe `TestPreenchimentoVerticalH0020` verificam dimensões (número de linhas,
largura total) mas **não** verificam presença de bordas laterais nas linhas
de fill. Com H-0021, esses testes continuam passando (as dimensões são
preservadas). Não remover nem regredir esses testes. Adicionar novos testes
de H-0021 em classe própria.

---

## Especificação funcional

### Algoritmo de fill bordeado por coluna

Para cada elemento em `_montar_corpo_horizontal`, com `altura_disponivel`
fornecida, o preenchimento deve gerar uma caixa visualmente completa com
altura `altura_alvo`:

```
linha 0:         topo (já gerado por _caixa_de_elemento ou helper)
linha 1..k:      conteúdo (já gerado)
linha k+1..h-2:  borda["v"] + " " * inner_w_i + borda["v"]
linha h-1:       _linha_base(borda, inner_w_i)
```

onde `h = altura_alvo` e `inner_w_i = larguras[i] - 2`.

### Linha de fill bordeado

Para coluna de largura `w`:

```python
borda["v"] + " " * (w - 2) + borda["v"]
```

Comprimento: `1 + (w - 2) + 1 = w = larguras[i]` ✓ (invariante preservado).

### Base na última linha

A linha de base de cada coluna usa `_linha_base(borda, inner_w_i)`:

```python
_linha_base(borda, w - 2)
# = borda["bl"] + borda["h"] * (w - 2) + borda["br"]
# comprimento = 1 + (w - 2) + 1 = w ✓
```

A base deve ocupar **exatamente** a linha `altura_alvo - 1` de cada coluna.

### Quando `altura_disponivel` é `None`

Comportamento H-0019/H-0020 preservado integralmente: normalização até
`altura_max` com `" " * larguras[i]` (sem bordas). O H-0021 não altera
esse caminho.

### Invariantes mantidos

1. `len(linha_concatenada) == total_w` para toda linha do bloco horizontal.
2. O bloco tem exatamente `altura_alvo` linhas quando `altura_disponivel` é
   fornecida.
3. Áreas adjacentes ficam coladas: `│` final de coluna `i` e `│` inicial
   de coluna `i+1` são contíguos (`││`) nas linhas internas.
4. Bases adjacentes: `╯╰` (ou `┘└`) ao concatenar as bases de colunas
   adjacentes.

---

## Algoritmo esperado

### Substituição do fill no caminho com `altura_disponivel`

O trecho atual em `_montar_corpo_horizontal` (linhas 754–756):

```python
# ATUAL (H-0020) — preenche com espaços sem bordas:
for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_alvo:
        linhas.append(" " * larguras[i])
```

Deve ser substituído por lógica que, quando `altura_disponivel` foi fornecido,
produz fill bordeado e base posicionada na última linha:

```python
for i, linhas in enumerate(todas_as_linhas_por_area):
    w = larguras[i]
    if altura_disponivel is not None:
        # Fill bordeado: borda lateral + espaços internos + borda lateral
        linha_fill = borda["v"] + " " * (w - 2) + borda["v"]
        # Preencher com linhas bordeadas até antes da última posição
        while len(linhas) < altura_alvo - 1:
            linhas.append(linha_fill)
        # Base na última linha (se houver espaço)
        if len(linhas) < altura_alvo:
            linhas.append(_linha_base(borda, w - 2))
    else:
        # Comportamento H-0019/H-0020: fill de espaços sem bordas
        while len(linhas) < altura_alvo:
            linhas.append(" " * w)
```

**Atenção**: a base atual gerada por `_caixa_de_elemento` (via `_caixa()`)
já está incluída nas linhas de cada área antes do fill. O fill bordeado deve
**substituir** a base existente ou **ser inserido antes** dela. O executor
deve verificar a ordem das linhas em `todas_as_linhas_por_area` ao
implementar. Ver "Considerações sobre a base existente".

### Considerações sobre a base existente

`_caixa_de_elemento` chama `_caixa()`, que inclui `_linha_base` como última
linha. Portanto, ao entrar no loop de fill, cada `linhas_area` já termina
com a base da caixa:

```
linhas_area = [topo, conteúdo_1, ..., conteúdo_k, base]
              ← k+2 linhas ← índice 0 a k+1
```

O fill H-0020 acrescenta `" " * w` após a base existente:

```
[topo, c_1, ..., c_k, base, " "*w, " "*w, ...]
```

Para o H-0021 com bordas, a abordagem mais segura é **remover a base
existente antes de aplicar o fill** e reposicioná-la ao final:

```python
# Para cada coluna, quando altura_disponivel é fornecida:
# 1. Remover a base existente (última linha de linhas_area)
# 2. Preencher com fill bordeado até altura_alvo - 1
# 3. Reposicionar a base como linha altura_alvo - 1
```

Alternativamente, verificar se a última linha é a base e tratá-la
adequadamente. **O executor deve escolher a abordagem mais cirúrgica e
registrá-la no IMP-0021.**

Uma implementação segura para o caso com `altura_disponivel`:

```python
for i, linhas in enumerate(todas_as_linhas_por_area):
    w = larguras[i]
    if altura_disponivel is not None:
        # Extrair base existente (última linha, gerada por _caixa())
        if linhas:
            base_linha = linhas.pop()   # remove a base temporariamente
        else:
            base_linha = _linha_base(borda, w - 2)
        # Preencher com fill bordeado até antes da última posição
        linha_fill = borda["v"] + " " * (w - 2) + borda["v"]
        while len(linhas) < altura_alvo - 1:
            linhas.append(linha_fill)
        # Reposicionar a base na última linha
        linhas.append(base_linha)
    else:
        # Comportamento H-0019/H-0020 preservado
        while len(linhas) < altura_alvo:
            linhas.append(" " * w)
```

Esse padrão garante que `len(linhas) == altura_alvo` ao final e que a base
esteja sempre na posição `altura_alvo - 1`. O executor pode adotar variante
equivalente, desde que o resultado seja idêntico.

### Caso especial: caixa com conteúdo que já alcança `altura_alvo`

Se `len(linhas_area) >= altura_alvo` antes do fill (conteúdo excede ou
iguala a altura alvo), nenhum fill é necessário. O comportamento atual
(manter `altura_alvo = altura_max` sem truncar) é preservado. A base
permanece como a última linha da caixa original — não reposicionar.

### Fluxo com `altura_disponivel` e caixa vazia (grupo ou tipo desconhecido)

Quando `_caixa_de_elemento` retorna `None` ou `""` para um elemento
(tipo `grupo` sem visual), `linhas_area` começa como `[]`. Nesse caso:

- Não há base a extrair.
- O fill bordeado deve produzir `altura_alvo - 1` linhas de
  `borda["v"] + " " * (w - 2) + borda["v"]` seguidas de uma linha de base.

Este caso garante que áreas de grupo também exibam bordas laterais e base
posicionada na última linha.

---

## Política para decomposição de caixa

### Opção preferencial — Helper interno `_montar_caixa_com_altura`

Extrair helper interno no `renderizador.py` que encapsule a lógica de
montagem de caixa com altura alvo, sem alterar contratos públicos:

```python
def _montar_caixa_com_altura(label, linhas_conteudo, borda, inner_w, content_w, label_max, altura_alvo):
    """Monta caixa bordeada com altura_alvo linhas.

    Estrutura:
      linha 0:       topo
      linhas 1..k:   conteudo
      linhas k+1..h-2: borda["v"] + " " * inner_w + borda["v"]
      linha h-1:     base

    Quando altura_alvo <= k+2 (conteúdo preenche ou excede a altura),
    gera a caixa normal (topo + conteúdo + base) sem fill.
    """
    linhas = [_linha_topo(label, borda, label_max)]
    for texto in linhas_conteudo:
        linhas.append(_linha_conteudo(texto, borda, content_w))
    linha_fill = borda["v"] + " " * inner_w + borda["v"]
    while len(linhas) < altura_alvo - 1:
        linhas.append(linha_fill)
    linhas.append(_linha_base(borda, inner_w))
    return "\n".join(linhas)
```

Se este helper for adotado, `_montar_corpo_horizontal` deve chamar
`_montar_caixa_com_altura` diretamente (obtendo `label` e `linhas_conteudo`
via funções auxiliares existentes: `_linhas_console`, `_linhas_dashboard`,
`_linhas_lancador`) ao invés de `_caixa_de_elemento`, mas **somente** quando
`altura_disponivel` é fornecida.

### Opção alternativa — Parâmetro opcional em `_caixa()`

Adaptar `_caixa()` com parâmetro opcional `altura_alvo=None`:

```python
def _caixa(label, linhas_conteudo, borda, inner_w, content_w, label_max, altura_alvo=None):
    partes = [_linha_topo(label, borda, label_max)]
    for texto in linhas_conteudo:
        partes.append(_linha_conteudo(texto, borda, content_w))
    if altura_alvo is not None:
        linha_fill = borda["v"] + " " * inner_w + borda["v"]
        while len(partes) < altura_alvo - 1:
            partes.append(linha_fill)
    partes.append(_linha_base(borda, inner_w))
    return "\n".join(partes)
```

Com esta opção, `_caixa_de_elemento` pode receber `altura_alvo` opcional e
passá-la para `_caixa()`. Todos os usos existentes de `_caixa()` sem
`altura_alvo` preservam comportamento atual.

### Critério de escolha

O executor deve escolher a abordagem mais cirúrgica e com menor superfície
de alteração. A opção alternativa (parâmetro em `_caixa()`) tem menor
impacto: altera apenas a assinatura interna de `_caixa()`, sem criar novos
fluxos de despacho. A opção preferencial cria um helper explícito, mais
legível mas com maior alteração estrutural. **Qualquer das duas é aceita**,
desde que:

1. Todos os usos existentes de `_caixa()` ou `_caixa_de_elemento()` sem
   `altura_alvo` preservem comportamento atual sem alteração visível.
2. O caminho `altura_disponivel is None` em `_montar_corpo_horizontal`
   continue com fill `" " * larguras[i]` (comportamento H-0019/H-0020).
3. A abordagem escolhida seja registrada no IMP-0021.

### Bloqueio arquitetural

Se qualquer abordagem exigir alteração de modelo, loader, contratos, ADRs,
JSONs, arquitetura de grupos ou mudança estrutural ampla que vá além de
`renderizador.py` e `teste_renderizador.py`, a implementação deve parar com:

```
ARCHITECTURE_REVIEW_REQUIRED
```

---

## Caso de integração com orquestrador.json

O executor deve adicionar teste de integração em memória com
`orquestrador.json`, sem alterar o arquivo persistente:

```python
tela_raw = carregar_tela(None, "orquestrador")
tela_raw["corpo"]["arranjo"] = "horizontal"   # ajuste em memória
modelo = construir_modelo(tela_raw)
saida = renderizar_tela(modelo, tipo_borda="curva", largura=80, altura=30)
```

O teste deve verificar:

- Filhos diretos: `console_principal`, `dashboard_info`, `lancador_principal`.
- `altura_disponivel` do corpo: `24` (= 30 − 3 linhas de cabeçalho − 3 linhas de barra).
- Bloco horizontal tem exatamente `24` linhas.
- Linhas internas de fill contêm `│` (borda vertical) por coluna.
- Não há sequência final de linhas `" " * 80` após o fechamento das caixas.
- Base das caixas aparece na linha `23` (última linha da área horizontal,
  índice 0-based).
- `len(linha) == 80` para toda linha do bloco.
- `dashboard_info` sem conteúdo literal ocupa área visual bordeada.

Realizar o mesmo teste para o alias `lado_a_lado`:

```python
tela_raw["corpo"]["arranjo"] = "lado_a_lado"
saida_lado = renderizar_tela(modelo_lado, tipo_borda="curva", largura=80, altura=30)
```

Verificar que `saida_lado` produz o mesmo comportamento visual
(bordas laterais, base na última linha).

---

## Proteção da barra_de_menus

O H-0021 protege explicitamente os seguintes artefatos — não devem ser
alterados:

```
barra_de_menus.distribuicao  (campo do modelo — não alterar)
_normalizar_distribuicao     (função real em renderizador.py — com r)
_validar_distribuicao        (renderizador.py)
_linhas_barra                (renderizador.py)
_validar_ancoras             (renderizador.py)
tela/explorar_barra_de_menus.py
tela/teste_explorar_barra_de_menus.py
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_chip.md
```

**Atenção terminológica**: a função real chama-se `_normalizar_distribuicao`
(com `r`, linha 249 do `renderizador.py`). Não usar `_normaliza_distribuicao`
como nome real da função — essa grafia sem `r` é inconsistência documental
histórica registrada no QA-001 do H-0019 e no IMP-0020 (A-002). Qualquer
busca de auditoria deve usar o nome correto `_normalizar_distribuicao`.

---

## Testes obrigatórios

Os seguintes testes devem ser adicionados em `tela/teste_renderizador.py`
(classe `TestPreenchimentoBordeadoH0021` ou equivalente).

```text
 1. test_horizontal_fill_bordeado_orquestrador_json:
    orquestrador.json em memória com arranjo="horizontal", largura=80, altura=30.
    Confirmar que linhas internas do bloco horizontal contêm "│" por coluna.
    Confirmar que não há linha " " * 80 no interior do bloco após o conteúdo.
    Confirmar que o bloco tem 24 linhas.

 2. test_horizontal_fill_bordeado_lado_a_lado_alias:
    orquestrador.json em memória com arranjo="lado_a_lado", largura=80, altura=30.
    Confirmar comportamento idêntico ao teste 1.

 3. test_horizontal_fill_linhas_internas_com_bordas_laterais:
    Modelo sintético com corpo.arranjo="horizontal", 2 elementos, altura suficiente.
    Extrair linhas do bloco abaixo do conteúdo.
    Confirmar que cada linha começa com borda["v"] e termina com borda["v"].
    Confirmar len(linha) == total_w para cada linha do bloco.

 4. test_horizontal_base_na_ultima_linha_da_area:
    Modelo sintético com corpo.arranjo="horizontal", 2 elementos, altura fornecida.
    Confirmar que a última linha do bloco horizontal é composta por
    bases adjacentes coladas (ex.: "╰...╯╰...╯").
    Confirmar que a base aparece exatamente na última linha, não antes.

 5. test_horizontal_bordas_adjacentes_em_fill_e_base:
    Modelo com corpo.arranjo="horizontal", 2 elementos, altura fornecida.
    Nas linhas de fill: confirmar que borda direita da coluna 0 e borda
    esquerda da coluna 1 são contíguos ("││").
    Na linha de base: confirmar que "╯╰" aparece na junção das duas colunas.

 6. test_horizontal_largura_total_em_todas_linhas_apos_h0021:
    Modelo com corpo.arranjo="horizontal", 2 elementos, altura fornecida.
    Confirmar que TODAS as linhas do bloco horizontal (topo, conteúdo, fill,
    base) têm exatamente total_w caracteres.

 7. test_horizontal_dashboard_sem_literal_tem_bordas:
    orquestrador.json em memória com arranjo="horizontal".
    dashboard_info não tem campos com fonte="literal".
    Confirmar que a área do dashboard exibe bordas laterais nas linhas
    de fill (não apenas espaços).
    Confirmar que a base do dashboard aparece na última linha da área.

 8. test_horizontal_filhos_preservados_em_ordem:
    orquestrador.json em memória com arranjo="horizontal", largura=80, altura=30.
    Confirmar que os 3 filhos (console, dashboard, lancador) aparecem na
    saída na ordem declarada (da esquerda para a direita).
    Confirmar que nenhum filho é omitido.

 9. test_horizontal_sem_altura_preserva_h0019_h0020:
    Modelo com corpo.arranjo="horizontal", 2 elementos, SEM altura fornecida.
    Confirmar que o comportamento é idêntico ao H-0019/H-0020: fill sem bordas
    ("" * largura_area), normalização até altura_max apenas.

10. test_vertical_nao_regride_apos_h0021:
    Modelo com corpo.arranjo="vertical", altura fornecida.
    Confirmar comportamento idêntico ao pré-H-0021 (fill externo H-0015).

11. test_sobreposto_nao_regride_apos_h0021:
    Modelo com corpo.arranjo="sobreposto", altura fornecida.
    Confirmar comportamento idêntico ao caso "vertical".

12. test_none_nao_regride_apos_h0021:
    Modelo com corpo.arranjo=None, altura fornecida.
    Confirmar comportamento idêntico ao caso "vertical".

13. test_barra_de_menus_preservada_apos_h0021:
    Modelo com corpo.arranjo="horizontal", altura fornecida.
    Confirmar que a barra_de_menus aparece ao final com seus chips inalterados.
    Confirmar que _normalizar_distribuicao, _validar_distribuicao e _linhas_barra
    permanecem intocadas.
    Confirmar que teste_explorar_barra_de_menus.py continua 38/38.

14. test_baseline_completo_continua_passando:
    (Verificação de regressão, não teste novo em si)
    Executar todas as 6 suítes; confirmar que os 621 casos anteriores
    continuam passando sem regressão.
```

---

## Relatório de implementação exigido

O executor deve criar:

```text
docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md
```

O IMP-0021 deve registrar:

```markdown
# IMP-0021 — Correção pós-QA manual do preenchimento horizontal no orquestrador

## Status

## Base verificada

## Arquivos alterados

## Resumo da implementação

## Como _caixa foi decomposta ou adaptada
(Descrever a abordagem escolhida: helper _montar_caixa_com_altura
ou parâmetro opcional em _caixa(); justificar a escolha)

## Como o preenchimento bordeado foi gerado
(Descrever a lógica de fill: borda["v"] + " " * inner_w + borda["v"];
como a base foi reposicionada na última linha; tratamento de caixa vazia)

## Como orquestrador.json foi testado em memória
(Descrever o snippet de integração; quais verificações foram feitas)

## Tratamento do alias lado_a_lado

## Testes executados
(Tabela: suíte / verificações antes / verificações depois / exit code)

## Resultado dos testes

## Verificação de proteção da barra_de_menus
(Confirmar _normalizar_distribuicao, _validar_distribuicao, _linhas_barra
intocadas — usar nome correto com r)

## Pendências

## Conclusão
```

---

## Critérios de aceite

```
 1. corpo.arranjo = "horizontal" com altura fornecida produz linhas internas
    de fill com bordas laterais: borda["v"] + " " * (w - 2) + borda["v"].

 2. A base das caixas aparece na última linha da altura alocada — não antes.

 3. Linhas de fill bordeado são adjacentes entre colunas: "││" nas linhas
    internas, "╯╰" na linha de base.

 4. len(linha) == total_w para toda linha do bloco horizontal, inclusive nas
    linhas de fill bordeado e na linha de base.

 5. Não há sequência de linhas " " * total_w (fill externo plano) no interior
    do bloco horizontal após o conteúdo das caixas.

 6. dashboard sem conteúdo literal ocupa área visual bordeada (bordas laterais
    e base posicionada na última linha da área).

 7. Filhos diretos (console, dashboard, lancador) aparecem na ordem declarada,
    sem omissão e sem reordenação.

 8. corpo.arranjo = "horizontal" sem altura fornecida preserva comportamento
    H-0019/H-0020: fill " " * largura_area, sem bordas adicionadas.

 9. corpo.arranjo = "lado_a_lado" produz comportamento idêntico ao
    "horizontal" — bordas, base posicionada, fill bordeado.

10. corpo.arranjo = "vertical" / "sobreposto" / None preserva comportamento
    H-0015 (fill externo de espaços intacto, sem alteração).

11. _normalizar_distribuicao, _validar_distribuicao e _linhas_barra não foram
    alteradas. teste_explorar_barra_de_menus.py: 38/38.

12. Baseline completo: 621 + novos casos passando. Zero regressões.

13. Nenhum arquivo proibido alterado (loader, modelo, contratos, ADRs,
    NOMENCLATURA, JSONs de configuração).

14. Nenhum cache __pycache__ nem .pyc no workspace após execução.
```

---

## Riscos e mitigação

### R-1 — Remover base antes de reposicioná-la, com caixa vazia

**Descrição**: quando `_caixa_de_elemento` retorna `None` ou `""` para
um elemento `grupo`, `linhas_area = []`. Tentar `linhas.pop()` em lista
vazia causa `IndexError`.

**Mitigação**: verificar `if linhas:` antes de extrair a base. Se a lista
estiver vazia, usar `_linha_base(borda, larguras[i] - 2)` diretamente como
base. O executor deve testar explicitamente o caso de área vazia.

---

### R-2 — Regressão em testes H-0019 e H-0020

**Descrição**: modificar o caminho `altura_disponivel is None` em
`_montar_corpo_horizontal` pode quebrar testes existentes de `TestArranjoH0019`
e `TestPreenchimentoVerticalH0020` que verificam fill `" " * larguras[i]`.

**Mitigação**: o caminho `altura_disponivel is None` deve permanecer
inalterado (fill de espaços sem bordas). O executor deve executar toda a
classe `TestArranjoH0019` e `TestPreenchimentoVerticalH0020` antes de
declarar a implementação completa.

---

### R-3 — Base duplicada ou fora de posição

**Descrição**: se a base existente (gerada por `_caixa()`) não for removida
antes do fill bordeado, a base aparecerá no meio da coluna e outra base
será adicionada ao final — resultando em `base_original + fill + nova_base`.

**Mitigação**: o algoritmo deve sempre extrair (ou descartar) a base existente
antes de aplicar o fill bordeado. Verificar com teste que `_linha_base` aparece
exatamente uma vez e na posição `altura_alvo - 1`.

---

### R-4 — Largura incorreta na linha de fill bordeado

**Descrição**: usar `larguras[i]` em vez de `larguras[i] - 2` no fill
`borda["v"] + " " * ??? + borda["v"]` resulta em linha com `larguras[i] + 2`
caracteres — violando o invariante `len(linha) == total_w`.

**Mitigação**: a linha de fill interna tem `inner_w_i = larguras[i] - 2`
espaços internos. O comprimento total é `1 + (larguras[i] - 2) + 1 = larguras[i]`.
O executor deve verificar `len(linha_fill) == larguras[i]` em teste explícito.

---

### R-5 — Alterar `_caixa()` e introduzir regressão em usos externos

**Descrição**: se a opção alternativa (parâmetro em `_caixa()`) for adotada,
qualquer uso existente de `_caixa()` com argumentos posicionais pode
inadvertidamente receber `altura_alvo` se a ordem de parâmetros for alterada.

**Mitigação**: `altura_alvo=None` deve ser parâmetro **nomeado** com default
`None`, acrescentado ao final da assinatura. Os usos existentes de `_caixa()`
não mudam. O executor deve verificar que nenhum uso existente quebra após
a alteração via grep do diff.

---

### R-6 — Usar grafia incorreta `_normaliza_distribuicao`

**Descrição**: reproduzir a inconsistência documental histórica
`_normaliza_distribuicao` (sem `r`) no IMP-0021 ou nos testes.

**Mitigação**: usar sempre `_normalizar_distribuicao` (com `r`) em todos
os documentos e verificações do H-0021. A grafia incorreta pode aparecer
apenas como nota histórica referenciando QA-001 do H-0019 / A-002 do IMP-0020.

---

### R-7 — Introduzir fallback silencioso para comportamento H-0020

**Descrição**: em vez de corrigir o fill bordeado, deixar silenciosamente
o comportamento H-0020 (`" " * larguras[i]`) como fallback quando a
decomposição de `_caixa()` falhar.

**Mitigação**: não implementar fallback silencioso. Se a decomposição não
for implementável sem revisão arquitetural, parar com
`ARCHITECTURE_REVIEW_REQUIRED`.

---

## Fora de escopo futuro

Os itens abaixo foram identificados e **explicitamente adiados**:

```
Distribuição vertical do corpo (H-0022).
corpo.distribuicao percentual/fracao.
Distribuição horizontal percentual/fracao.
Grupos hierárquicos com redistribuição interna.
Arranjo dentro de grupo.
Distribuicao dentro de grupo.
Profundidade de 3 níveis.
Sincronização de cortes.
Paginação real.
Terminal pequeno com reticências (...).
Configuração declarativa de largura da tela.
Campo largura/dimensao no JSON.
Console real com conteúdo de dados.
Navegação por [✥].
Foco entre elementos.
Seleção.
Filtros.
Ações.
Registry novo.
Alterações em barra_de_menus.
Alterações em contratos.
Alterações em ADRs.
Alterações em NOMENCLATURA.
Mudanças em orquestrador.json.
```

---

## Exigência de auditoria

Este handoff deve ser auditado antes de qualquer implementação. A implementação
só poderá ocorrer após auditoria aprovada e autorização explícita do usuário.

O relatório de auditoria deve ser criado em:

```text
docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md
```

A auditoria deve confirmar:

1. Que a abordagem escolhida para decomposição de `_caixa()` está correta e
   não altera comportamento de usos existentes.
2. Que o fill bordeado `borda["v"] + " " * (w - 2) + borda["v"]` tem
   comprimento `w` (invariante de largura preservado).
3. Que a base é posicionada exatamente em `altura_alvo - 1` (última linha).
4. Que o caminho `altura_disponivel is None` preserva comportamento H-0019/H-0020.
5. Que os testes cobrem bordas laterais, base posicionada e integração com
   `orquestrador.json` em memória.
6. Que a proteção da barra_de_menus está explícita e verificável.
7. Que `_normalizar_distribuicao` (com `r`) é o nome correto citado em todos
   os pontos de verificação.
8. Que o escopo positivo se limita a `renderizador.py` e `teste_renderizador.py`.

---

## Saída esperada do implementador

```
IMPLEMENTATION_COMPLETED

arquivos-alterados:
  tela/renderizador.py
  tela/teste_renderizador.py
  docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md

testes:
  teste_loader.py:                     89/89
  teste_modelo.py:                     56/56
  teste_renderizador.py:               <N>/<N>
  teste_demo.py:                       117/117
  teste_diagnostico.py:                28/28
  teste_explorar_barra_de_menus.py:    38/38

verificacoes:
  git status --short
  git diff --stat
  git diff --name-only
  find . -name '__pycache__' -type d -print  → (sem saída)
  find . -name '*.pyc' -print               → (sem saída)
```
