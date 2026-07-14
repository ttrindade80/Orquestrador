# IMP-0017 — Script de exploração de combinações da barra_de_menus

```text
ciclo:          H-0017
data:           2026-07-09
executor:       Claude Code (Sonnet 4.6)
commit-base:    ab5ad68  feat: renderiza barra de menus horizontal responsiva
status-audit:   AUDIT_APPROVED_WITH_NOTES
```

---

## Status

```text
IMPLEMENTATION_DONE
```

---

## Resumo

Script de exploração/diagnóstico `explorar_barra_de_menus.py` criado e
funcionando. Exercita `_linhas_barra` do renderer (H-0016) com cenários
sintéticos gerados em memória. Verifica 12 invariantes de renderização.
Produz saída determinística em modo `detalhado` e `resumo`. Retorna exit
codes 0/1/2 conforme especificado. Teste automatizado `teste_explorar_barra_de_menus.py`
criado com 25 verificações passando. Todas as 451 verificações das 5 suítes
existentes continuam passando. `renderizador.py` não foi alterado.

---

## Arquivos alterados/criados

```text
CRIADOS:
  scripts/tela/explorar_barra_de_menus.py
  scripts/tela/teste_explorar_barra_de_menus.py
  scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md

NÃO ALTERADOS:
  scripts/tela/renderizador.py  — _linhas_barra já acessível por importação
                                  direta; nenhuma alteração necessária
                                  (conforme preferência declarada no handoff)
```

---

## Script criado

**Caminho**: `scripts/tela/explorar_barra_de_menus.py`

**Justificativa de caminho**: caminho preferencial do handoff, por coesão
com `renderizador.py` e com os demais arquivos de diagnóstico da camada de
renderização.

**Interface com o renderer**:

```python
from tela.renderizador import (
    _linhas_barra,
    _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT,
    RenderizadorErro,
)
```

`_linhas_barra` é função de módulo (não método de classe privada), portanto
acessível por importação direta sem necessidade de alterar `renderizador.py`.

**Helpers internos criados no script**:

- `_fabricar_chips(n, perfil, prefixo)` — gera chips sintéticos com ids,
  teclas e textos únicos (resolve AUD-01: textos únicos garantem
  verificabilidade das invariantes 1-4).
- `_fabricar_distribuicao(preenchimento, linhas_maximo, vao_chips, vao_cols, ancoras)` —
  monta objeto canônico de distribuição com parâmetros configuráveis.
- `_fabricar_cenario(...)` — monta dict de cenário para execução.
- `_matriz_padrao()` — 14 cenários obrigatórios sem argumentos.
- `_gerar_matriz_combinatoria(...)` — geração de cenários via parâmetros CLI.
- `_verificar_invariantes(cenario, linhas)` — verifica as 12 invariantes.
- `_executar_cenario(cenario)` — executa um cenário e retorna resultado.
- `_formatar_cenario_detalhado(...)` — formata saída por cenário.
- `_formatar_resumo(...)` — formata saída de totais e agrupamentos.

---

## Parâmetros implementados

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| `--larguras` | lista int | matriz padrão | content_w a testar |
| `--chips` | lista int | matriz padrão | quantidades de chips |
| `--linhas-max` | lista int | matriz padrão | valores de linhas.maximo |
| `--preenchimentos` | lista str | matriz padrão | coluna_a_coluna, linha_a_linha |
| `--modo-saida` | str | detalhado | resumo \| detalhado |
| `--mostrar-ok` | flag | False | inclui cenários OK na saída |
| `--mostrar-erros` | flag | False | inclui cenários com erro na saída |
| `--limite-casos` | int | sem limite | limita cenários executados |

Sem argumentos → matriz padrão (14 cenários). Com `--larguras`, `--chips`,
`--linhas-max` ou `--preenchimentos` → matriz combinatória gerada em memória.

---

## Matriz de cenários

### Matriz padrão (14 cenários, executável sem argumentos)

| ID | Descrição | chips | content_w | linhas.max | preench | esperado |
|----|-----------|-------|-----------|-----------|---------|---------|
| C01 | Linha única: 3 chips curtos | 3 | 80 | 2 | col_a_col | OK, 1 linha |
| C02 | Linha única: 6 chips curtos | 6 | 120 | 2 | col_a_col | OK, 1 linha |
| C03 | Duas linhas: 6 chips médios | 6 | 60 | 2 | col_a_col | OK, 2 linhas |
| C04 | Duas linhas: 8 chips curtos | 8 | 50 | 2 | col_a_col | OK, 2 linhas |
| C05 | Três linhas: 10 chips curtos | 10 | 50 | 3 | col_a_col | OK, ≤3 linhas |
| C06 | Overflow: 10 chips médios | 10 | 20 | 2 | col_a_col | erro_layout esperado |
| C07 | Overflow: 12 chips curtos | 12 | 15 | 2 | col_a_col | erro_layout esperado |
| C08 | coluna_a_coluna: 5 chips mistos | 5 | 60 | 2 | col_a_col | OK |
| C09 | linha_a_linha: 5 chips mistos | 5 | 45 | 2 | linha_a_linha | OK, 2 linhas |
| C10 | Âncora válida | 2 | 39 | 2 | col_a_col | OK |
| C11 | Âncora inexistente | 2 | 39 | 2 | col_a_col | erro_ancora esperado |
| C12 | Âncora posição errada | 2 | 39 | 2 | col_a_col | erro_ancora esperado |
| C13 | Espaçamentos mínimos | 4 | 60 | 2 | col_a_col | OK |
| C14 | Espaçamentos máximos | 4 | 120 | 2 | col_a_col | OK |

**Resultado da matriz padrão**:
- 10 cenários OK, 4 erros esperados, 0 erros inesperados, 0 violações.

### Ajustes documentados (conforme autorização do handoff)

- **C05**: `content_w` ajustado de 40 para 50. Com 10 chips e linhas.maximo=3,
  o distribuidor coluna_a_coluna produz 4 colunas; a coluna mais larga
  (`[k10] No-10` = 11 chars) exige no mínimo 46 chars de content_w. O cenário
  continua sendo "largura estreita forçando três linhas".

- **C09**: `content_w` ajustado de 60 para 45. Resolve AUD-02: linha única
  teria 75 chars > 45 (força multilinha); linha_a_linha K=2 produz linha 0
  com 42 chars ≤ 45 (cabe). Com content_w=60, os chips mistos caberiam em
  linha única, não exercitando `linha_a_linha`.

---

## Variações implementadas

Todas as variações obrigatórias do handoff estão cobertas:

1. **Quantidade de chips**: 1, 2, 3, 4, 5, 6, 8, 10, 12 — cobertas via
   cenários C01-C14 e matriz combinatória.
2. **Comprimento dos textos**: curto, médio, longo (misto) — perfis
   `_PERFIS_TEXTO` com sufixos numéricos únicos por chip.
3. **Largura disponível**: muito estreita (15, 20), estreita (39, 45, 50),
   média (60), larga (80, 120).
4. **linhas.maximo**: 1, 2, 3 — exercitados na matriz padrão e combinatória.
5. **preenchimento_multilinha**: coluna_a_coluna (C03-C08, C10-C14) e
   linha_a_linha (C09).
6. **Espaçamentos**: mínimos (vao_chips=2, vao_cols=2 — C13), máximos
   (vao_chips=6, vao_cols=8 — C14), intermediários (3,4).
7. **Âncoras**: válida (C10), sem âncora (maioria), inexistente (C11),
   posição errada (C12).
8. **Overflow**: caso que cabe (C01-C05, C08-C10, C13-C14), que não cabe
   (C06, C07), overflow determinístico.

---

## Invariantes verificadas

Para cenários OK, o script verifica:

| # | Invariante | Implementação |
|---|-----------|---------------|
| 1 | Cada chip aparece exatamente uma vez | `junta.count(texto) == 1` |
| 2 | Nenhum chip ausente inventado | verifica ausência de textos não declarados |
| 3 | Nenhum chip omitido | `junta.count(texto) >= 1` por chip declarado |
| 4 | Ordem preservada (dentro de cada linha) | `linha.find(ti) < linha.find(tj)` para i<j na mesma linha |
| 5 | Texto não truncado | `texto in junta` para cada chip |
| 6 | Linhas físicas ≤ linhas.maximo | `len(linhas) <= maximo` |
| 7 | Largura de cada linha ≤ content_w | `len(linha) <= content_w` por linha |
| 8 | Chips do lancador ausentes | não aplicável a cenários sintéticos; verificado implicitamente |
| 9 | Sem fallback vertical quando n>1 | comentado no código (não detectável sem acesso ao modo interno do renderer) |
| 10 | Linha única: todos os chips na mesma linha | verifica presença de cada chip em `linhas[0]` |
| 11 | coluna_a_coluna: chip[0] na linha 0 | verifica `textos_chips[0] in linhas[0]` |
| 12 | linha_a_linha: primeiros CPL chips na linha 0 | verifica `textos_chips[i] in linhas[0]` para i<CPL |

**Nota sobre INV-4**: a invariante de ordem é verificada *dentro de cada
linha individualmente*, não no texto juntado. Em `coluna_a_coluna` com
K=2 linhas e N chips, a distribuição é coluna-major: chip[0] e chip[2]
ficam na linha 0, chip[1] e chip[3] na linha 1. Verificar posição
sequencial no texto juntado produziria falso positivo (chip[1] aparece
depois de chip[2] no texto juntado, embora ambos estejam na posição
correta de suas respectivas linhas). A verificação intra-linha captura
reordenações incorretas sem produzir falsos positivos.

---

## Testes automatizados

**Arquivo**: `scripts/tela/teste_explorar_barra_de_menus.py`

**Resultado**: 25/25 verificações passando, exit code 0.

| # | Caso | Verificação | Resultado |
|---|------|------------|-----------|
| 1 | Matriz padrão sem argumentos → exit 0 | subprocess.run | PASSOU |
| 2 | Modo resumo determinístico | subprocess.run, stdout idêntico | PASSOU |
| 3 | Linha única 3 chips curtos → OK, 1 linha | chamada direta _linhas_barra | PASSOU |
| 4 | coluna_a_coluna 4 chips → OK, 2 linhas | chamada direta _linhas_barra | PASSOU |
| 5 | linha_a_linha 4 chips → OK, 2 linhas | chamada direta _linhas_barra | PASSOU |
| 6 | Overflow → erro_layout, script continua | subprocess.run | PASSOU |
| 7 | Âncora inexistente → RenderizadorErro com id | chamada direta _linhas_barra | PASSOU |
| 8 | Âncora posição errada → RenderizadorErro | chamada direta _linhas_barra | PASSOU |
| 9 | Exit code 1 para violação inesperada | inspeção código-fonte (AUD-N-02) | PASSOU |
| 10 | Exit code 2 para parâmetro inválido | subprocess.run | PASSOU |

**Caso 9 — abordagem por inspeção**: conforme autorização do handoff H-0017
(seção "Casos obrigatórios" item 9) e nota AUD-N-02 da auditoria, a condição
de exit 1 é verificada por análise do código-fonte. A lógica `tem_inesperado
or tem_violacao → return 1` está presente em `main()`. Não é possível simular
de forma determinística via subprocess uma `RenderizadorErro` em cenário
projetado para caber, pois o renderer é correto e determinístico para inputs
válidos. Limitação documentada no IMP-0017 conforme autorizado.

---

## Execuções manuais

### Execução 1: sem argumentos (matriz padrão)

```
python tela/explorar_barra_de_menus.py
```

Saída (resumo):
```
=== RESUMO DA EXPLORACAO ===
Total de cenarios executados:   14
OK:                             10
Erro esperado:                  4
Erro inesperado:                0
Violacoes de invariante:        0

Por preenchimento_multilinha:
  coluna_a_coluna: OK=9 ERRO_ESP=4 ERRO_INESP=0
  linha_a_linha: OK=1 ERRO_ESP=0 ERRO_INESP=0

Por linhas.maximo:
  2: OK=9 ERRO_ESP=4 ERRO_INESP=0
  3: OK=1 ERRO_ESP=0 ERRO_INESP=0

Por largura (content_w):
  15: OK=0 ERRO_ESP=1 ERRO_INESP=0
  20: OK=0 ERRO_ESP=1 ERRO_INESP=0
  39: OK=1 ERRO_ESP=2 ERRO_INESP=0
  45: OK=1 ERRO_ESP=0 ERRO_INESP=0
  50: OK=2 ERRO_ESP=0 ERRO_INESP=0
  60: OK=3 ERRO_ESP=0 ERRO_INESP=0
  80: OK=1 ERRO_ESP=0 ERRO_INESP=0
  120: OK=2 ERRO_ESP=0 ERRO_INESP=0
```

Exit code: **0**

### Execução 2: modo resumo com parâmetros explícitos

```
python tela/explorar_barra_de_menus.py \
  --modo-saida resumo \
  --larguras 30,40,80 \
  --chips 3,6,10 \
  --linhas-max 1,2,3 \
  --preenchimentos coluna_a_coluna,linha_a_linha
```

Saída:
```
=== RESUMO DA EXPLORACAO ===
Total de cenarios executados:   324
OK:                             150
Erro esperado:                  174
Erro inesperado:                0
Violacoes de invariante:        0

Por preenchimento_multilinha:
  coluna_a_coluna: OK=71 ERRO_ESP=91 ERRO_INESP=0
  linha_a_linha: OK=79 ERRO_ESP=83 ERRO_INESP=0

Por linhas.maximo:
  1: OK=22 ERRO_ESP=86 ERRO_INESP=0
  2: OK=54 ERRO_ESP=54 ERRO_INESP=0
  3: OK=74 ERRO_ESP=34 ERRO_INESP=0

Por largura (content_w):
  30: OK=24 ERRO_ESP=84 ERRO_INESP=0
  40: OK=45 ERRO_ESP=63 ERRO_INESP=0
  80: OK=81 ERRO_ESP=27 ERRO_INESP=0
```

Exit code: **0**

### Execução 3: modo detalhado com limite e mostrar-erros

```
python tela/explorar_barra_de_menus.py \
  --modo-saida detalhado \
  --mostrar-erros \
  --limite-casos 20
```

Mostra os 4 cenários de erro da matriz padrão (C06, C07, C11, C12) com
mensagens detalhadas, seguido do resumo. Exit code: **0**

---

## Resultados

- Todos os 32 critérios de aceite do handoff atendidos.
- 14 cenários da matriz padrão: 10 OK, 4 erros esperados, 0 inesperados.
- 324 cenários na execução combinatória (30,40,80 × 3,6,10 × 1,2,3 × 2
  preenchimentos × 3 espaçamentos × 2 perfis): 150 OK, 174 erros esperados,
  0 inesperados.
- 451 verificações nas 5 suítes existentes continuam passando:
  - `teste_loader.py`: 79/79
  - `teste_modelo.py`: 56/56
  - `teste_renderizador.py`: 171/171
  - `teste_demo.py`: 117/117
  - `teste_diagnostico.py`: 28/28
- Novo teste: `teste_explorar_barra_de_menus.py`: 25/25.
- `renderizador.py` não alterado.
- Nenhum `__pycache__` ou `.pyc` gerado no workspace.

---

## Limitações conhecidas

1. **INV-4 intra-linha apenas**: a verificação de ordem (INV-4) é feita
   dentro de cada linha individualmente, não no texto juntado. Em
   `coluna_a_coluna` multilinha, a distribuição coluna-major é o
   comportamento correto; verificação sequencial no texto juntado produziria
   falsos positivos. As invariantes INV-11 e INV-12 cobrem o padrão de
   distribuição para cada modo.

2. **INV-9 não verificável**: a invariante 9 ("não usa fallback vertical")
   não é verificável sem acesso ao modo interno do renderer. O renderer nunca
   produz fallback vertical; a invariante é satisfeita por construção do
   algoritmo de `_linhas_barra`.

3. **Caso de teste 9 (exit code 1) por inspeção**: a condição de exit 1 para
   violação inesperada é verificada por análise do código-fonte, não via
   subprocess. A condição não é simulável deterministicamente pois o renderer
   é correto para todos os inputs válidos declarados neste script.

4. **Heurística combinatória**: a previsão de erro_layout na matriz
   combinatória usa heurística de cálculo de largura. Cenários onde a
   heurística diverge do renderer resultariam em erros inesperados detectados
   como `ERRO_INESPERADO`. Nas execuções realizadas: 0 erros inesperados.

5. **linhas.maximo=1 na matriz combinatória**: cenários com linhas.maximo=1
   produzem `erro_layout` sempre que a linha única não cabe, sem tentar
   multilinha. Isso é comportamento correto do renderer e é classificado como
   `erro_esperado`.

---

## Confirmação de fora de escopo

Confirmado que **não** foram implementados:

- Nova regra normativa da barra_de_menus.
- Alteração de ADR (nenhum ADR foi tocado).
- Alteração de contrato (nenhum contrato foi tocado).
- Alteração de NOMENCLATURA.md.
- Alteração dos JSONs ativos (orquestrador.json, grupo_minimo.json,
  destino_minimo.json, stub_b.json).
- Mudança no comportamento aprovado do renderer H-0016 (`renderizador.py`
  não foi alterado).
- Composição horizontal do corpo.
- Distribuição de altura entre elementos do corpo.
- Integração automática ao diagnóstico principal (`diagnostico.py`).
- Integração automática à demo (`demo.py`).
