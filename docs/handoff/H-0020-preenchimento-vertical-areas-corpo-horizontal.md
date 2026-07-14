# H-0020 — Preenchimento vertical das áreas alocadas no corpo horizontal

## Status

```
HANDOFF_READY
```

---

## Metadados de rastreabilidade

| Item | Referência |
|------|-----------|
| ID | H-0020 |
| Commit base | `624e0a5  docs: registra levantamento pos H-0019` |
| Commit H-0019 | `29a8a79  feat: implementa layout horizontal plano do corpo` |
| Levantamento pós-H-0019 | `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0019_AJUSTES_LAYOUT_E_DIMENSAO.md` |
| Relatório de implementação a gerar | `docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md` |
| Relatório de auditoria obrigatório | `docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md` |
| Ciclos anteriores fechados | H-0015 a H-0019 (todos commitados, artefatos presentes) |
| Baseline no momento do handoff | 589/589 verificações em 6 suítes |
| Contratos aplicáveis | `contrato_composicao_corpo.md` (v0.3), `contrato_tela_json.md`, `contrato_json_tela_minima.md`, `contrato_barra_de_menus.md` |
| ADRs normativas | ADR-0013, ADR-0014, ADR-0015 |

---

## Contexto

O H-0019 implementou `corpo.arranjo = "horizontal"` com particionamento contíguo
da largura disponível entre filhos diretos de `corpo.elementos[]`. O ciclo foi
aprovado com QA `QA_APPROVED_WITH_NOTES` (589/589 verificações) e commitado em
`29a8a79`.

O levantamento pós-H-0019 (`624e0a5`) identificou uma lacuna de renderização:
`_montar_corpo_horizontal` normaliza a altura apenas até `altura_max` — a altura
do elemento mais alto entre as colunas — mas não até a altura disponível do corpo.
Quando o terminal é mais alto que o conteúdo, o preenchimento vertical herdado do
H-0015 insere linhas `" " * total_w` fora do bloco horizontal, sem preservar a
estrutura de colunas nem as bordas das áreas alocadas.

---

## Problema

### Comportamento atual

Em `_montar_corpo_horizontal` (`renderizador.py`, linhas 686–760):

```python
# Passo 4 — Normalizar altura com preenchimento inferior
altura_max = max(
    (len(linhas) for linhas in todas_as_linhas_por_area), default=0
)
for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_max:
        linhas.append(" " * larguras[i])
```

A função normaliza cada coluna até `altura_max` (máximo entre colunas), mas não
recebe `l_corpo_disponivel` (altura disponível do corpo para o fill vertical).

A assinatura atual:

```python
def _montar_corpo_horizontal(elementos, borda, total_w):
```

Em `renderizar_tela` (`renderizador.py`, linhas 907–938), o preenchimento H-0015
externo:

```python
l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
if l_corpo_fill > 0:
    partes.append(
        "\n".join(" " * total_w for _ in range(l_corpo_fill))
    )
```

insere linhas `" " * total_w` depois do bloco horizontal — strings planas de
`total_w` espaços, sem estrutura de coluna, sem bordas laterais das caixas.

### Consequência visual

Em terminal mais alto que o conteúdo das caixas horizontais:

1. O bloco horizontal fecha suas bordas inferiores (`╯╰`) na altura da caixa mais
   alta.
2. Caixas mais baixas fecham antes da altura máxima interna.
3. O fill H-0015 insere linhas de espaços abaixo do bloco sem estrutura de coluna.

Exemplo do que acontece (incorreto):

```text
╭────────╮╭────────╮
│ item A ││ item B │
╰────────╯╰────────╯
                    
                    
```

### Contradição normativa

Este comportamento contradiz a ADR-0015:

- **Decisão 5** (Distribuição por container):
  > distribuição aloca área, não apenas conteúdo;
  > elemento funcional deve preservar a área alocada;
  > sobra vertical vira linhas em branco.

- **Decisão 10** (Preenchimento de espaço vazio):
  > **Vertical:** preencher com linhas em branco; preservar altura da faixa.

E o `contrato_composicao_corpo.md` v0.3, seção 5.9:

> A distribuição define **área alocada**. O renderer deve preservar a área
> alocada. Se o conteúdo não preencher a área, o restante deve ser preenchido
> com branco.

---

## Objetivo

Corrigir `_montar_corpo_horizontal` em `renderizador.py` para que, em
`corpo.arranjo = "horizontal"`, cada área/coluna alocada seja preenchida
verticalmente até `l_corpo_disponivel` (altura disponível do corpo), não apenas
até `altura_max` (máximo entre colunas).

O preenchimento vertical deve ocorrer **dentro** de cada área/coluna alocada,
preservando a largura da faixa. O preenchimento H-0015 externo não deve inserir
linhas adicionais após o bloco horizontal quando este já consumiu toda a área.

### Regra visual esperada

Em terminal mais alto que o conteúdo:

```text
╭────────╮╭────────╮
│ item A ││ item B │
│        ││        │
│        ││        │
╰────────╯╰────────╯
```

Não deve acontecer:

```text
╭────────╮╭────────╮
│ item A ││ item B │
╰────────╯╰────────╯
                    
                    
```

---

## Leitura obrigatória

O executor deve ler na íntegra antes de tocar qualquer arquivo:

1. `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
2. `docs/NOMENCLATURA.md`
3. `docs/contratos/contrato_composicao_corpo.md` (v0.3)
4. `docs/contratos/contrato_tela_json.md`
5. `docs/contratos/contrato_json_tela_minima.md`
6. `docs/handoff/H-0019-layout-horizontal-plano-corpo.md`
7. `docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md`
8. `docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md`
9. `docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0019_AJUSTES_LAYOUT_E_DIMENSAO.md`
10. `tela/renderizador.py` (integralmente)
11. `tela/teste_renderizador.py` (integralmente)

Leia também apenas para proteção de regressão (não alterar):

```text
tela/loader.py
tela/modelo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
tela/explorar_barra_de_menus.py
```

---

## Escopo positivo

O H-0020 pode e deve implementar alterações apenas em:

```text
tela/renderizador.py
tela/teste_renderizador.py
docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
```

As alterações são:

1. Propagar `l_corpo_disponivel` até `_montar_corpo_horizontal`.
2. Estender a assinatura de `_montar_corpo_horizontal` com parâmetro
   `altura_disponivel: int | None = None`.
3. Quando `altura_disponivel` for fornecido, normalizar cada coluna até
   `altura_disponivel` em vez de `altura_max`.
4. Neutralizar o fill H-0015 externo quando o arranjo for horizontal e o bloco
   já consumiu toda a área disponível.
5. Adicionar testes em `tela/teste_renderizador.py` para os cenários listados na
   seção "Testes obrigatórios".

---

## Escopo negativo

O H-0020 **NÃO deve** implementar:

```
NÃO alterar loader.py.
NÃO alterar modelo.py.
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
NÃO implementar configuração declarativa de largura da tela.
NÃO adicionar campo largura/dimensao no JSON.
NÃO alterar orquestrador.json.
NÃO implementar distribuição percentual.
NÃO implementar distribuição por fração/pesos.
NÃO implementar grupos hierárquicos.
NÃO implementar arranjo dentro de grupo.
NÃO implementar profundidade de 3 níveis.
NÃO implementar sincronização de cortes.
NÃO implementar paginação real.
NÃO implementar reticências (...) para terminal pequeno.
NÃO implementar console real.
NÃO implementar navegação por [✥].
NÃO implementar foco entre elementos.
NÃO implementar seleção.
NÃO implementar filtros.
NÃO implementar ações.
NÃO criar registry novo.
NÃO fazer commit.
```

---

## Preservações obrigatórias

As seguintes funções e invariantes **não devem ser tocadas**:

- `_normalizar_distribuicao` (renderizador.py) — nome real com `r`
- `_validar_distribuicao` (renderizador.py)
- `_linhas_barra` (renderizador.py)
- `_validar_ancoras` (renderizador.py)
- `_montar_coluna_a_coluna` (renderizador.py)
- `_montar_linha_a_linha` (renderizador.py)
- `_texto_chip_barra` (renderizador.py)
- `_caixa_de_elemento` (renderizador.py)
- `_caixa` (renderizador.py)
- `_linha_topo` (renderizador.py)
- `_linha_base` (renderizador.py)
- `_linha_conteudo` (renderizador.py)
- Testes da classe `TestDistribuicaoH0018` (teste_renderizador.py)
- Testes da classe `TestArranjoH0019` — preservar ou atualizar conforme nota abaixo
- Snapshots de `teste_demo.py` e `teste_diagnostico.py` — não alterar sem justificativa

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

**Nota sobre `TestArranjoH0019`**: o teste
`test_arranjo_horizontal_padding_inferior` da classe `TestArranjoH0019` verifica
que a área mais curta é preenchida até `altura_max` com `altura` não fornecida.
Com H-0020, quando `altura` não é fornecida, o comportamento deve ser idêntico ao
H-0019 (preserva `altura_max`). O teste existente deve continuar passando sem
alteração. Apenas quando `altura` for fornecida é que a normalização vai até
`l_corpo_disponivel`. O executor deve verificar com cuidado que os testes
existentes de H-0019 continuam passando.

---

## Especificação funcional

### `tela/renderizador.py` — `_montar_corpo_horizontal`

**Extensão de assinatura:**

```python
def _montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None):
```

O parâmetro `altura_disponivel` é `int | None`. Quando `None`, o comportamento
é idêntico ao H-0019: normaliza até `altura_max` (sem alteração de comportamento
para chamadas sem `altura`). Quando fornecido como `int >= 1`, é a altura
alocada ao corpo inteiro (calculada pelo chamador como `l_corpo_disponivel`).

**Passo 4 revisado — Normalizar altura:**

```python
# Quando altura_disponivel é fornecida, usá-la como alvo do fill vertical.
# Quando não fornecida, usar altura_max (comportamento H-0019 preservado).
altura_alvo = altura_disponivel if altura_disponivel is not None else altura_max
if altura_alvo < altura_max:
    # Conteúdo já excede a área — preservar comportamento atual (sem truncar).
    # O chamador deve ter garantido que l_corpo_conteudo <= l_corpo_disponivel.
    altura_alvo = altura_max
for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_alvo:
        linhas.append(" " * larguras[i])
```

A variável de iteração muda de `altura_max` para `altura_alvo` na linha de
resultado. A lógica de concatenação (Passo 5) usa `altura_alvo` no lugar de
`altura_max`:

```python
for r in range(altura_alvo):
    linha = ""
    for linhas in todas_as_linhas_por_area:
        linha += linhas[r]
    linhas_resultado.append(linha)
```

---

### `tela/renderizador.py` — `renderizar_tela`

**Propagação de `l_corpo_disponivel` para o modo horizontal:**

No branch `if arranjo_corpo == "horizontal":`, quando `altura is not None`, o
chamador deve calcular `l_corpo_disponivel` antes da chamada a
`_montar_corpo_horizontal` e passá-lo como argumento:

```python
if arranjo_corpo == "horizontal":
    # Calcular l_corpo_disponivel antecipadamente quando altura for fornecida.
    if altura is not None:
        l_cab = _contar_linhas(partes[0])
        linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)
        l_barra = len(linhas_barra) + 2
        if l_cab + l_barra > altura:
            raise RenderizadorErro(
                "altura insuficiente: terminal com {0} linhas nao comporta "
                "cabecalho ({1}) + barra_de_menus ({2})".format(
                    altura, l_cab, l_barra
                )
            )
        _l_corpo_disponivel = altura - l_cab - l_barra
    else:
        linhas_barra = None  # será calculada depois
        _l_corpo_disponivel = None

    bloco_horizontal = _montar_corpo_horizontal(
        modelo.corpo.elementos, borda, total_w,
        altura_disponivel=_l_corpo_disponivel,
    )
    if bloco_horizontal:
        partes.append(bloco_horizontal)
```

**Neutralização do fill H-0015 externo no modo horizontal:**

Quando `arranjo_corpo == "horizontal"` e `altura is not None`, o bloco horizontal
já absorveu `l_corpo_disponivel` linhas. O fill H-0015 externo deve ser
neutralizado para esse caso, para evitar duplo preenchimento.

A forma mais segura é verificar o número de linhas do bloco e omitir o fill
externo:

```python
# No bloco H-0015 (linhas 907–938):
if altura is not None:
    # ... cálculo de l_cab, l_barra, l_corpo_conteudo, l_corpo_disponivel
    l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
    if l_corpo_fill > 0 and arranjo_corpo != "horizontal":
        # Modo horizontal já absorveu o fill dentro de _montar_corpo_horizontal.
        # Não inserir fill externo adicional.
        partes.append(
            "\n".join(" " * total_w for _ in range(l_corpo_fill))
        )
```

**Atenção ao fluxo de `linhas_barra`:** o cálculo de `linhas_barra` ocorre após
o bloco de corpo. No modo horizontal com `altura` fornecida, `linhas_barra` é
calculada antecipadamente para derivar `l_barra`. Garantir que `linhas_barra` não
seja calculada duas vezes (o resultado deve ser armazenado e reutilizado). O
executor deve verificar o fluxo completo antes de implementar e garantir que a
chamada a `_linhas_barra` ocorra exatamente uma vez.

---

## Algoritmo esperado — resumo

### Fluxo com `altura` fornecida e `arranjo_corpo == "horizontal"`

```
1. Calcular l_cab (linhas do cabeçalho).
2. Calcular linhas_barra = _linhas_barra(...).
3. Calcular l_barra = len(linhas_barra) + 2.
4. Verificar l_cab + l_barra <= altura (RenderizadorErro se exceder).
5. l_corpo_disponivel = altura - l_cab - l_barra.
6. bloco_horizontal = _montar_corpo_horizontal(
       elementos, borda, total_w,
       altura_disponivel=l_corpo_disponivel
   )
   → _montar_corpo_horizontal normaliza cada coluna até l_corpo_disponivel.
   → O bloco retornado tem exatamente l_corpo_disponivel linhas.
7. partes.append(bloco_horizontal).
8. NÃO inserir fill H-0015 externo (o fill já está dentro do bloco).
9. partes.append(caixa de barra_de_menus, usando linhas_barra calculada no passo 2).
10. Resultado = "\n".join(partes) + "\n".
    → Total de linhas = l_cab + l_corpo_disponivel + l_barra = altura. ✓
```

### Fluxo com `altura is None` e `arranjo_corpo == "horizontal"` (preservação H-0019)

```
1. _montar_corpo_horizontal(elementos, borda, total_w)
   → altura_disponivel=None → normaliza até altura_max (comportamento H-0019).
2. Sem fill H-0015 (altura is None → bloco H-0015 não é executado).
3. Resultado sem preenchimento vertical (comportamento H-0019 preservado).
```

### Fluxo com arranjo vertical/None/sobreposto (preservação H-0015)

```
O branch `else` e o bloco H-0015 são preservados integralmente.
Nenhuma alteração no comportamento não-horizontal.
```

---

## Política de terminal pequeno

H-0020 **não implementa** política nova para terminal pequeno. Se o conteúdo
exceder a área disponível (`l_corpo_conteudo > l_corpo_disponivel`), o
comportamento atual continua vigente: `RenderizadorErro` determinístico (já
implementado no H-0015). Reticências (`...`) permanecem fora de escopo, conforme
ADR-0015 D13.

Não introduzir política de truncamento, compactação ou fallback silencioso.

---

## Proteção da barra_de_menus

O handoff protege explicitamente os seguintes artefatos — não devem ser alterados:

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
(com `r`, linha 249 do `renderizador.py`). O QA-001 do ciclo H-0019 registrou
que handoffs e relatórios anteriores citaram incorretamente `_normaliza_distribuicao`
(sem `r`). Esta é nota histórica documental apenas — a função real é
`_normalizar_distribuicao`. Qualquer busca de auditoria deve usar o nome correto.

---

## Testes obrigatórios

Os seguintes testes devem ser adicionados em `tela/teste_renderizador.py`.

### Testes novos (classe `TestPreenchimentoVerticalH0020` ou equivalente)

```text
1. test_horizontal_alto_mantém_bordas_ate_altura_disponivel:
   Modelo com corpo.arranjo = "horizontal", 2 elementos, altura suficiente
   (ex.: altura = 30).
   Confirmar que cada linha do bloco horizontal tem exatamente total_w chars.
   Confirmar que o bloco tem exatamente l_corpo_disponivel linhas.
   Confirmar que as bordas laterais aparecem em todas as linhas (não apenas
   nas linhas de conteúdo da caixa mais alta).
   Confirmar que não há linhas de preenchimento externas (" " * total_w)
   depois do bloco horizontal e antes da barra_de_menus.

2. test_horizontal_preenchimento_dentro_das_colunas:
   Modelo com corpo.arranjo = "horizontal", 2 elementos com conteúdo diferente,
   altura suficiente.
   Confirmar que o preenchimento vertical (linhas " " * largura_area) ocorre
   dentro de cada área/coluna, não fora do bloco.
   Confirmar que nenhuma linha após o bloco horizontal é composta por
   " " * total_w (fill externo) antes da barra_de_menus.

3. test_horizontal_sem_linhas_total_w_apos_bloco:
   Modelo com corpo.arranjo = "horizontal", 2 elementos, altura = 40.
   Extrair as linhas da saída entre o fim do cabeçalho e o início da
   barra_de_menus.
   Confirmar que nenhuma dessas linhas é " " * total_w (string de espaços
   sem estrutura de coluna).

4. test_horizontal_bordas_adjacentes_em_linhas_preenchidas:
   Modelo com corpo.arranjo = "horizontal", 2 elementos, altura = 25.
   Extrair as linhas do bloco horizontal após o conteúdo da caixa mais alta.
   Confirmar que as áreas adjacentes permanecem coladas em todas as linhas
   preenchidas (bordas laterais de cada caixa quando aplicável).

5. test_horizontal_largura_total_em_todas_linhas_preenchidas:
   Modelo com corpo.arranjo = "horizontal", 2 elementos, altura = 20.
   Confirmar que todas as linhas do bloco horizontal têm exatamente total_w
   caracteres, inclusive nas linhas de preenchimento abaixo do conteúdo.

6. test_horizontal_colunas_diferentes_preenchidas_mesma_altura:
   Modelo com corpo.arranjo = "horizontal", 2 elementos com alturas
   renderizadas diferentes, altura fornecida.
   Confirmar que ambas as colunas são preenchidas até l_corpo_disponivel
   (não apenas até a altura da coluna mais alta).

7. test_vertical_preserva_comportamento_atual:
   Modelo com corpo.arranjo = "vertical", altura fornecida.
   Confirmar que o comportamento é idêntico ao pré-H-0020 (fill externo
   H-0015 continua funcionando normalmente).

8. test_sobreposto_preserva_comportamento_atual:
   Modelo com corpo.arranjo = "sobreposto", altura fornecida.
   Confirmar comportamento idêntico ao caso "vertical".

9. test_none_preserva_comportamento_atual:
   Modelo com corpo.arranjo = None, altura fornecida.
   Confirmar comportamento idêntico ao caso "vertical".

10. test_lado_a_lado_preserva_comportamento_horizontal:
    Modelo com corpo.arranjo = "lado_a_lado", altura fornecida.
    Confirmar que o bloco horizontal é preenchido até l_corpo_disponivel
    (igual ao caso "horizontal").

11. test_horizontal_sem_altura_preserva_h0019:
    Modelo com corpo.arranjo = "horizontal", 2 elementos, SEM altura fornecida.
    Confirmar que o comportamento é idêntico ao H-0019: normalização até
    altura_max apenas, sem preenchimento adicional.
    Os testes existentes da classe TestArranjoH0019 devem continuar passando
    sem alteração.

12. test_barra_de_menus_preservada_apos_h0020:
    Modelo com corpo.arranjo = "horizontal", altura fornecida.
    Confirmar que a barra_de_menus aparece ao final com seus chips inalterados.
    Confirmar que nenhuma alteração ocorreu em _normalizar_distribuicao,
    _validar_distribuicao ou _linhas_barra.
    Confirmar que teste_explorar_barra_de_menus.py continua 38/38.

13. test_baseline_completo_continua_passando:
    (Verificação de regressão, não teste novo em si)
    Executar todas as 6 suítes; confirmar que os 589 casos anteriores
    continuam passando.
```

---

## Relatório de implementação exigido

O executor deve criar:

```text
docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md
```

Com a seguinte estrutura:

```markdown
# IMP-0020 — Preenchimento vertical das áreas alocadas no corpo horizontal

## Status

## Base verificada

## Arquivos alterados

## Resumo da implementação

## Como l_corpo_disponivel foi propagado
(Descrever o fluxo exato: onde é calculado, como é passado para
_montar_corpo_horizontal, como o bloco resultante tem l_corpo_disponivel linhas)

## Como o preenchimento H-0015 externo foi neutralizado no modo horizontal
(Descrever a condição exata e onde no código ela foi inserida)

## Interação com o caso altura is None (preservação H-0019)
(Confirmar que altura_disponivel=None preserva comportamento H-0019)

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
 1. corpo.arranjo = "horizontal" com altura fornecida preenche cada coluna
    até l_corpo_disponivel (não apenas até altura_max).

 2. Nenhuma linha de preenchimento " " * total_w é inserida depois do bloco
    horizontal e antes da barra_de_menus quando altura é fornecida.

 3. Todas as linhas do bloco horizontal (inclusive as de preenchimento) têm
    exatamente total_w caracteres.

 4. Áreas adjacentes permanecem coladas em todas as linhas preenchidas,
    preservando a estrutura horizontal.

 5. Colunas de alturas renderizadas diferentes são ambas preenchidas até
    l_corpo_disponivel quando altura é fornecida.

 6. corpo.arranjo = "horizontal" sem altura fornecida preserva comportamento
    H-0019: normalização até altura_max, sem preenchimento adicional.
    Todos os testes de TestArranjoH0019 continuam passando sem alteração.

 7. corpo.arranjo = "vertical" / "sobreposto" / None preserva comportamento
    H-0015 (fill externo intacto).

 8. corpo.arranjo = "lado_a_lado" (alias transitional) preserva comportamento
    horizontal — preenchimento até l_corpo_disponivel.

 9. A barra_de_menus permanece inalterada: _normalizar_distribuicao,
    _validar_distribuicao e _linhas_barra não foram tocadas.

10. teste_explorar_barra_de_menus.py: 38/38 (sem regressão).

11. Baseline completo: 589 + novos casos passando. Zero regressões.

12. Nenhum arquivo proibido alterado (loader, modelo, contratos, ADRs,
    NOMENCLATURA, JSONs de configuração).

13. Nenhum cache __pycache__ nem .pyc no workspace após execução.
```

---

## Riscos e mitigação

### R-1 — Duplo preenchimento vertical

**Descrição**: se o fill H-0015 externo não for neutralizado corretamente no
modo horizontal, linhas `" " * total_w` serão inseridas depois do bloco, que já
preencheu `l_corpo_disponivel` linhas — resultando em saída maior que `altura`.

**Mitigação**: a condição de neutralização deve ser verificada estritamente por
`arranjo_corpo == "horizontal"` (após normalização de aliases). O executor deve
checar que a soma final de linhas é exatamente `altura` com um teste explícito
(critério de aceite 3 via soma de linhas do cabeçalho + bloco + barra).

---

### R-2 — Regressão em testes de H-0019

**Descrição**: `test_arranjo_horizontal_padding_inferior` verifica preenchimento
até `altura_max` sem `altura` fornecida. Se a implementação modificar o
comportamento quando `altura is None`, este teste falhará.

**Mitigação**: `altura_disponivel=None` em `_montar_corpo_horizontal` deve
preservar exatamente o comportamento H-0019 (`altura_alvo = altura_max`). O
executor deve executar toda a classe `TestArranjoH0019` antes de declarar a
implementação completa.

---

### R-3 — Confundir `altura_max` de bloco com `l_corpo_disponivel`

**Descrição**: `altura_max` normaliza colunas com alturas diferentes dentro do
bloco (invariante do H-0019, a preservar como passo intermediário). O
`l_corpo_disponivel` é a altura total disponível do corpo. As duas variáveis
têm papéis distintos.

**Mitigação**: o algoritmo revisado deve manter `altura_max` como passo
intermediário (para garantir que colunas mais curtas sejam primeiro preenchidas
até o nível da mais alta) e depois estender até `altura_alvo = l_corpo_disponivel`.
Na prática, se `altura_disponivel >= altura_max`, o `while len(linhas) < altura_alvo`
preencherá todas as colunas até `altura_alvo`, cobrindo os dois passos em um único
laço. O executor pode simplificar para um único laço direto com `altura_alvo`.

---

### R-4 — `_linhas_barra` calculada duas vezes

**Descrição**: no modo horizontal com `altura` fornecida, `_linhas_barra` é
chamada antecipadamente para calcular `l_barra`. Se o fluxo chamar
`_linhas_barra` novamente depois, haverá chamada duplicada (sem consequência
funcional, mas ineficiente e inconsistente).

**Mitigação**: o executor deve garantir que `linhas_barra` seja calculada uma
única vez e reutilizada tanto para `l_barra` quanto para a caixa final da barra.
Armazenar em variável local antes do branch de arranjo ou estruturar o fluxo de
forma que o valor seja calculado uma única vez.

---

### R-5 — Alterar funções protegidas da barra_de_menus

**Descrição**: ao modificar `renderizar_tela`, introduzir inadvertidamente
chamada a `_linhas_barra` com parâmetros errados ou alterar o fluxo de montagem
da caixa da barra.

**Sintoma**: testes de `TestDistribuicaoH0018` ou `teste_explorar_barra_de_menus.py`
falham após as alterações.

**Mitigação**: executar `PYTHONDONTWRITEBYTECODE=1 python
tela/teste_explorar_barra_de_menus.py` após cada alteração incremental no
renderer. Verificar que `_normalizar_distribuicao`, `_validar_distribuicao` e
`_linhas_barra` não aparecem no diff de alterações.

---

### R-6 — Usar grafia incorreta `_normaliza_distribuicao`

**Descrição**: o QA-001 do H-0019 documentou inconsistência documental entre a
grafia `_normaliza_distribuicao` (sem `r`, citada em handoffs/IMP) e o nome real
`_normalizar_distribuicao` (com `r`). Repetir a grafia incorreta no IMP-0020 ou
nos testes pode criar nova inconsistência documental.

**Mitigação**: usar sempre `_normalizar_distribuicao` (com `r`) em todos os
documentos e verificações do H-0020. A grafia `_normaliza_distribuicao` pode
aparecer apenas como nota histórica do QA-001 do H-0019.

---

## Fora de escopo futuro

Os itens abaixo foram identificados e **explicitamente adiados**:

```
Configuração declarativa de largura da tela — requer ciclo documental prévio.
  (largura declarativa da tela exige ciclo documental prévio antes de H-0021)
  Ver Tema B do levantamento pós-H-0019.

Redistribuição interna de grupo (H-0020 estava planejado para isso pela ADR-0015
  D17, mas o levantamento pós-H-0019 definiu H-0020 como preenchimento vertical.
  A redistribuição interna de grupo fica para ciclo posterior.)

Profundidade de 3 níveis.
Arranjo dentro de grupo aninhado.
Distribuição percentual de largura.
Distribuição por fração/pesos.
Regras dinâmicas de mínimo/preferido/máximo.
Sincronização de cortes entre grupos.
Paginação real.
Terminal pequeno com reticências (...).
Console real com conteúdo de dados.
Navegação por [✥].
Foco entre elementos.
Seleção.
Filtros.
Ações.
Registry novo.
Alterações em barra_de_menus.
Combinação corpo.arranjo = "horizontal" + dashboard presente (pendência de contrato).
```

**Nota sobre largura declarativa**: o levantamento pós-H-0019 identificou
ausência de configuração declarativa de largura da tela no JSON. Este tema
**não pertence ao H-0020**. A implementação de largura declarativa exige ciclo
documental prévio que feche semântica, atualize contratos e NOMENCLATURA.md
(seção 6 afirma largura sempre dinâmica — contradição direta com campo
declarativo) e possivelmente estenda a ADR-0015 D11. Apenas após esse ciclo
documental o tema receberá número de handoff próprio (candidato a H-0021).

---

## Exigência de auditoria

Este handoff deve ser auditado antes de qualquer implementação. A implementação
só poderá ocorrer após auditoria aprovada e autorização explícita do usuário.

O relatório de auditoria deve ser criado em:

```text
docs/relatorios/RELATORIO_AUDITORIA_H-0020_HANDOFF.md
```

A auditoria deve confirmar:

1. Que a extensão de assinatura de `_montar_corpo_horizontal` está correta e
   compatível com os contratos vigentes.
2. Que a neutralização do fill H-0015 externo no modo horizontal está correta
   e não introduz fallback silencioso.
3. Que o comportamento sem `altura` (H-0019 preservado) está correto.
4. Que os testes cobrem todos os critérios de aceite.
5. Que a proteção da barra_de_menus está explícita e verificável.
6. Que o Tema B (largura declarativa) não foi incluído no escopo.
7. Que `_normalizar_distribuicao` (com `r`) é o nome correto citado em todos
   os pontos de verificação.

---

## Saída esperada do implementador

```
IMPLEMENTATION_COMPLETED

arquivos-alterados:
  tela/renderizador.py
  tela/teste_renderizador.py
  docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md

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
