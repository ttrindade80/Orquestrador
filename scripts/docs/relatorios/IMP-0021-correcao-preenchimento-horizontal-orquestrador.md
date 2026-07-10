# IMP-0021 — Correção pós-QA manual do preenchimento horizontal no orquestrador

## Status

```
IMPLEMENTATION_COMPLETE
```

---

## Base verificada

| Item | Valor |
|------|-------|
| HEAD observado | `3132d4c  docs: registra investigacao pos H-0020` |
| Workspace antes da implementação | `?? docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md` / `?? docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md` |
| Arquivos staged/modificados | nenhum |
| Workspace conforme esperado | sim |

---

## Arquivos alterados

```
 M tela/renderizador.py
 M tela/teste_renderizador.py
```

Criado:

```
docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md
```

Não alterados (confirmado):

```
tela/loader.py
tela/modelo.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
tela/explorar_barra_de_menus.py
config/telas/orquestrador.json
docs/handoff/H-0021-correcao-preenchimento-horizontal-orquestrador.md
docs/relatorios/RELATORIO_AUDITORIA_H-0021_HANDOFF.md
docs/adr/ (todos)
docs/contratos/ (todos)
docs/NOMENCLATURA.md
```

---

## Resumo da implementação

Dois pontos de alteração cirúrgica em `tela/renderizador.py`:

1. `_caixa()` recebeu parâmetro opcional `altura_alvo=None` (Opção B). Quando fornecido, linhas de fill bordeadas são inseridas entre o conteúdo e a base até que a caixa atinja `altura_alvo` linhas.

2. O loop de fill em `_montar_corpo_horizontal` foi substituído: quando `altura_disponivel is not None`, extrai a base existente de cada coluna, preenche com linhas bordeadas (`borda["v"] + " " * (w - 2) + borda["v"]`) até a posição `altura_alvo - 1`, e reposiciona a base na última linha. Quando `altura_disponivel is None`, preserva o comportamento H-0019/H-0020 integralmente (`" " * w`).

14 novos testes foram adicionados na classe `TestPreenchimentoBordeadoH0021` em `tela/teste_renderizador.py`.

---

## Decisão de implementação

Foi adotada a opção B recomendada pela auditoria: parâmetro opcional `altura_alvo` em `_caixa()`, preservando comportamento atual quando não fornecido.

A lógica real de fill bordeado em `_montar_corpo_horizontal` usa o padrão pop+fill+append descrito na seção "Considerações sobre a base existente" do handoff: a base existente é removida temporariamente, o fill bordeado é inserido, e a base é reposicionada na última posição. Isso é equivalente ao uso de `_caixa()` com `altura_alvo` e mais seguro por reutilizar o resultado de `_caixa_de_elemento()` sem duplicar lógica de despacho.

---

## Adaptação de _caixa

`_caixa()` recebeu o parâmetro nomeado `altura_alvo=None` ao final da assinatura:

```python
def _caixa(label, linhas_conteudo, borda, inner_w, content_w, label_max, altura_alvo=None):
```

Quando `altura_alvo is not None`:

```python
if altura_alvo is not None:
    linha_fill = borda["v"] + " " * inner_w + borda["v"]
    while len(partes) < altura_alvo - 1:
        partes.append(linha_fill)
partes.append(_linha_base(borda, inner_w))
```

Todos os usos existentes de `_caixa()` continuam sem `altura_alvo` → `None` por default → comportamento inalterado.

---

## Preenchimento bordeado no horizontal

O trecho substituído em `_montar_corpo_horizontal` (antigo H-0020):

```python
# ANTES (H-0020):
for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_alvo:
        linhas.append(" " * larguras[i])
```

Substituído por (H-0021):

```python
for i, linhas in enumerate(todas_as_linhas_por_area):
    w = larguras[i]
    if altura_disponivel is not None:
        if linhas:
            base_linha = linhas.pop()
        else:
            base_linha = _linha_base(borda, w - 2)
        linha_fill = borda["v"] + " " * (w - 2) + borda["v"]
        while len(linhas) < altura_alvo - 1:
            linhas.append(linha_fill)
        linhas.append(base_linha)
    else:
        while len(linhas) < altura_alvo:
            linhas.append(" " * w)
```

A linha de fill tem comprimento `1 + (w - 2) + 1 = w = larguras[i]` — invariante de largura preservado (mitiga R-4).

A base é reposicionada exatamente em `altura_alvo - 1` (última linha da coluna).

Caso de área vazia (`linhas == []`): guarda `if linhas:` evita `IndexError`; a base é gerada via `_linha_base(borda, w - 2)` (mitiga R-1).

---

## Integração com orquestrador.json em memória

Snippet de integração usado nos testes:

```python
tela_raw = carregar_tela(_BASE_PADRAO, "orquestrador")
tela_raw["corpo"]["arranjo"] = "horizontal"
modelo = construir_modelo(tela_raw)
saida = renderizar_tela(modelo, tipo_borda="curva", largura=80, altura=30)
```

Verificações executadas nos testes 1, 7 e 8:

| Verificação | Resultado |
|-------------|-----------|
| Filhos: `console_principal`, `dashboard_info`, `lancador_principal` | ✓ presentes na ordem declarada |
| `l_corpo_disponivel = 24` (= 30 − 3 − 3) | ✓ bloco tem 24 linhas |
| Linhas internas contêm `│` por coluna | ✓ todas as linhas intermediárias têm `│` |
| Sem linhas `" " * 80` após caixas | ✓ nenhuma linha de espaços planos no bloco |
| Base na linha 23 (última, 0-based) | ✓ `╰` em `linhas_bloco[-1]`; ausente nas linhas anteriores |
| `len(linha) == 80` para toda linha | ✓ invariante preservado |
| `dashboard_info` sem literal: bordas | ✓ char[27] das linhas intermediárias é `│`; char[27] da última linha é `╰` |

O arquivo persistente `config/telas/orquestrador.json` não foi alterado.

---

## Tratamento do alias lado_a_lado

O alias `lado_a_lado` é normalizado para `"horizontal"` em `renderizar_tela` (linha 869–870 do renderizador, inalterada). O teste 2 confirma que `lado_a_lado` produz saída idêntica ao `horizontal` com fill bordeado.

---

## Preservação de comportamento sem altura_alvo

Quando `altura_disponivel is None` (caminho else), o comportamento H-0019/H-0020 é preservado integralmente:

```python
else:
    while len(linhas) < altura_alvo:
        linhas.append(" " * w)
```

O teste 9 verifica que: o bloco tem `altura_max` linhas (não estendido); o fill da segunda coluna em `row[2][21:]` é `" " * 21` (espaços, sem bordas).

---

## Compatibilidade com H-0019 e H-0020

- `TestArranjoH0019`: 13 testes — todos passando (293/293 incluindo outras classes).
- `TestPreenchimentoVerticalH0020`: 12 testes — todos passando. Verificações dimensionais (número de linhas, largura) continuam corretas; as linhas de fill agora têm bordas em vez de espaços, mas os testes da H-0020 não verificavam o conteúdo das linhas de fill (somente dimensões e presença de `││`/`╯╰` nas linhas estruturais).

---

## Compatibilidade com ADR-0015

| Decisão ADR-0015 | Status |
|-----------------|--------|
| D5 — elemento funcional preserva área alocada; sobra vertical vira linhas em branco **dentro** do elemento | ✓ fill bordeado dentro de cada caixa |
| D9 — particionamento contíguo sem separador; bordas adjacentes naturais | ✓ `││` no fill e `╯╰` na base |
| D10 — preenchimento de espaço vazio preserva estrutura visual | ✓ linhas bordeadas `│ ... │` preservam a estrutura visual da caixa |

---

## Tratamento das notas da auditoria

### NOTA-1

Os rótulos "preferencial" e "alternativa" do handoff foram tratados operacionalmente seguindo a recomendação da auditoria: opção B por menor impacto. O parâmetro `altura_alvo=None` foi adicionado ao final da assinatura de `_caixa()`, sem impactar usos existentes. A lógica de fill em `_montar_corpo_horizontal` usa o padrão pop+fill+append, que é equivalente à opção B e descrito explicitamente na seção "Considerações sobre a base existente" do handoff.

### NOTA-2

A opção B foi adotada porque evita o problema de dois passes necessário na opção A para calcular `altura_alvo` correta. Com a opção B (pop+fill+append sobre a saída de `_caixa_de_elemento()`), o `altura_alvo` já está disponível em `_montar_corpo_horizontal` antes de processar qualquer coluna, sem necessidade de calcular `linhas_conteudo` separadamente de cada elemento.

---

## Testes executados

| Suíte | Verificações antes | Verificações depois | Exit code |
|-------|--------------------|---------------------|-----------|
| `teste_loader.py` | 89/89 | 89/89 | 0 |
| `teste_modelo.py` | 56/56 | 56/56 | 0 |
| `teste_renderizador.py` | 293/293 | 331/331 | 0 |
| `teste_demo.py` | 117/117 | 117/117 | 0 |
| `teste_diagnostico.py` | 28/28 | 28/28 | 0 |
| `teste_explorar_barra_de_menus.py` | 38/38 | 38/38 | 0 |
| **Total** | **621/621** | **659/659** | **0** |

---

## Resultado dos testes

Todos os 659 testes passam. Nenhuma regressão.

Os 38 novos testes (`TestPreenchimentoBordeadoH0021`) cobrem:
- Fill bordeado com `orquestrador.json` em memória (tests 1, 7, 8)
- Alias `lado_a_lado` (test 2)
- Bordas laterais em linhas intermediárias (test 3)
- Base na última linha (test 4)
- Bordas adjacentes `││` e `╯╰` (test 5)
- Largura total em todas as linhas (test 6)
- Preservação do comportamento sem altura (test 9)
- Não-regressão de `vertical`, `sobreposto`, `None` (tests 10, 11, 12)
- Preservação da barra de menus (test 13)
- Registro do baseline completo (test 14)

---

## Verificação de proteção da barra_de_menus

```bash
git diff -- tela/renderizador.py | grep -n "_normalizar_distribuicao\|_validar_distribuicao\|_linhas_barra" || true
```

Saída: (sem saída — nenhuma dessas funções foi alterada no diff)

As funções `_normalizar_distribuicao` (com `r`), `_validar_distribuicao` e `_linhas_barra` permaneceram intactas. `teste_explorar_barra_de_menus.py`: 38/38.

---

## Verificação de arquivos proibidos

```bash
git diff --name-only
```

Saída:
```
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
```

Apenas os dois arquivos permitidos foram modificados. Nenhum arquivo proibido foi alterado.

```bash
grep -RIn "H-0020A\|H-0019A\|H-0011B" docs/relatorios/IMP-0021-correcao-preenchimento-horizontal-orquestrador.md tela/renderizador.py tela/teste_renderizador.py || true
```

Saída: (sem saída — nenhuma referência a handoff com letra)

---

## Caches

```bash
find . -name '__pycache__' -type d -print
find . -name '*.pyc' -print
```

Ambos sem saída — nenhum cache criado (executado com `PYTHONDONTWRITEBYTECODE=1`).

---

## Pendências

Nenhuma. A distribuição vertical do corpo fica para H-0022 (fora de escopo deste ciclo).

---

## Conclusão

O H-0021 corrigiu o preenchimento visual do modo horizontal: as caixas agora se estendem visualmente até a altura alocada, com bordas laterais (`│ ... │`) nas linhas de fill e base (`╰ ... ╯`) posicionada na última linha da área. A correção é cirúrgica, limitada a `_caixa()` e ao loop de fill de `_montar_corpo_horizontal`, sem impacto em qualquer outro componente.

O comportamento `altura_disponivel=None` (H-0019/H-0020) foi preservado integralmente. Zero regressões em 621 verificações anteriores. 38 novos testes foram adicionados, totalizando 659/659.
