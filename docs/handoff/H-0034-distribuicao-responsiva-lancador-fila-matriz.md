---
handoff: H-0034
titulo: "Distribuição responsiva do lançador entre fila e matriz"
capacidade: "Aplicar no renderer a regra ativa de reorganização automática dos itens do lançador conforme a largura disponível"
status: aberto
data_criacao: 2026-07-15
reabre: nenhum
---

# H-0034 — Distribuição responsiva do lançador entre fila e matriz

## 1. Estado comprovado

O H-0030 está fechado e não deve ser reaberto.

Durante a validação manual do H-0030, foi registrado que os chips do `lancador`
não se reorganizavam em colunas quando faltava espaço horizontal. O levantamento
posterior (`docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md`, seção 8, ponto 3)
classificou o ponto como `REGRA_ATIVA_EXISTENTE` e recomendou `CRIAR_HANDOFF`.

Evidências comprovadas pelo levantamento:

- `docs/contratos/contrato_lancador.md`, seção 6: o renderer calcula
  automaticamente `fila` ou `matriz` a partir da largura real do terminal. Regra
  ativa, não opcional.
- `docs/NOMENCLATURA.md`, seções 8.1–8.3: confirma modos, algoritmo em duas
  etapas, ordem coluna-a-coluna e ausência de teto absoluto de colunas.
- `config/elementos/lancador.json`: parâmetros concretos de vãos, alinhamento e
  distribuição de colunas — autoridade transicional normativa (ADR-0008 e ADR-0021).
- `tela/renderizador.py::_linhas_lancador` (linhas 315–338): renderiza cada item
  como `"[{chip}] {texto}"` uma linha por item, sem cálculo de fila/matriz.
- `tela/teste_renderizador.py`: não foi localizada cobertura direta que prove a
  alternância responsiva fila/matriz para o `lancador`.

Não é necessária nova ADR para autorizar o comportamento descrito neste handoff.

A ADR-0023 (`docs/adr/ADR-0023-largura-minima-funcional-lancador.md`) está
aprovada e aplicada. Ela fecha a lacuna do comportamento abaixo do mínimo
de coluna válida e é autoridade ativa para a sequência de decisão do renderer.
Os contratos `contrato_lancador.md`, `contrato_tela_json.md`,
`contrato_composicao_corpo.md` e `docs/NOMENCLATURA.md` foram atualizados
para refletir a decisão da ADR-0023.

---

## 2. Objetivo

Especificar a implementação da regra normativa existente para que o `lancador`:

1. use uma única fila quando todos os itens couberem horizontalmente com vãos mínimos;
2. reorganize os itens em matriz de múltiplas colunas quando a fila não couber;
3. preencha a matriz coluna a coluna;
4. calcule as larguras das colunas pelo maior item da própria coluna;
5. mantenha a ordem declarativa dos itens;
6. não use paginação;
7. permaneça determinístico para a mesma largura e os mesmos itens;
8. não reutilize automaticamente a política da `barra_de_menus`;
9. preserve o limite de 15 caracteres e as demais regras já vigentes para textos,
   chips, ações e destinos;
10. acione o quadro mínimo canônico global quando nenhuma coluna válida couber
    na área alocada (ADR-0023).

---

## 3. Especificação técnica

Esta seção traduz para critérios executáveis exclusivamente o que está documentado
nas autoridades ativas. Nenhuma decisão nova foi criada.

### 3.1 Grandezas de largura e largura útil disponível

O handoff distingue cinco grandezas de largura, definidas pela ADR-0023 e
registradas em `docs/NOMENCLATURA.md` seção 6.3 e em
`docs/contratos/contrato_lancador.md` seção 6.7:

```
terminal_w
```

Largura total do terminal ou viewport.

```
area_lancador_w
```

Largura total efetivamente alocada ao elemento `lancador` pela composição —
inclui a caixa completa com bordas e padding externos.

```
lancador_caixa_min_w
```

Largura mínima total necessária para a caixa do `lancador`, incluindo as
unidades estruturais obrigatórias da representação atual (bordas e padding
externos da caixa). Relação conceitual:

```
lancador_caixa_min_w = coluna_minima_content_w + largura_estrutural_da_caixa
```

```
content_w
```

Largura interna disponível para o conteúdo após descontar a estrutura da caixa.

```
coluna_minima_content_w
```

Largura interna mínima necessária para representar integralmente uma coluna
válida completa, sem bordas nem padding externo da caixa. É a **largura mínima
funcional do `lancador`**: a menor `content_w` para a qual existe ao menos uma
distribuição válida do conjunto de itens declarados.

Comparações normativas válidas (grandezas no mesmo domínio):

```
content_w < coluna_minima_content_w    (domínio do conteúdo)
```

equivalente a:

```
area_lancador_w < lancador_caixa_min_w    (domínio da caixa completa)
```

Não é válido comparar `terminal_w` com `coluna_minima_content_w` nem
`area_lancador_w` com `coluna_minima_content_w` sem converter bordas e padding.

**Fato da implementação atual:** o `lancador` é renderizado como elemento do
corpo dentro de uma caixa bordeada por `_caixa`. Pela estrutura atual de
`_caixa` e `_caixa_de_elemento` (linhas 755–788 de `tela/renderizador.py`),
a relação é:

```
content_w = area_lancador_w - 3
```

— dois caracteres de borda vertical (`│`) mais um caractere de padding esquerdo
fixo. Esta relação reflete a implementação atual de `_caixa`/`_caixa_de_elemento`
e não é uma regra eterna independente da estrutura da caixa. Se a estrutura da
caixa mudar, a relação deve ser recalculada.

**Caminho recomendado de implementação:** o renderer do `lancador` deve receber
`content_w` para calcular o modo de distribuição. A função `_linhas_lancador`
(ou a função que a substituir) pode aceitar `content_w` como parâmetro
adicional; `_caixa_de_elemento` pode repassar o valor já disponível em seu
escopo. Esta é uma sugestão de estrutura compatível com a implementação atual —
não uma norma arquitetural permanente. A implementação pode adotar organização
diferente, desde que os comportamentos normativos sejam preservados.

### 3.2 Parâmetros de vão — origem normativa

Todos os vãos vêm de `config/elementos/lancador.json`, sem hardcoding.
O renderer deve ler o arquivo em tempo de execução. Parâmetros aplicáveis:

| Campo JSON | Semântica | Mínimo | Máximo |
|---|---|---|---|
| `layout.vaos.chip_texto.minimo/.maximo` | vão entre chip e texto do mesmo item | 1 | 3 |
| `layout.vaos.entre_itens_colunas_margem.minimo/.maximo` | vão entre itens/colunas na mesma linha e margem borda↔elemento | 2 | 5 |

Estes valores valem tanto para o modo fila quanto para o modo matriz.

### 3.3 Representação de cada item

Cada item é representado como duas sub-colunas independentes dentro de sua coluna:

- sub-coluna chip: `"[" + chip + "]"` — largura = `len(chip) + 2`
- sub-coluna texto: `texto` — largura = `len(texto)`

A largura mínima de um item (vão_chip_texto no mínimo) é:

```
item_w_min = chip_sub_w + vao_chip_texto_min + texto_sub_w
           = (len(chip) + 2) + 1 + len(texto)
```

Para itens com chip de um único caractere (caso universal dos itens de `demo.json`):
`chip_sub_w = 3`.

`texto` acima de 15 caracteres levanta `RenderizadorErro` antes de qualquer
cálculo de layout — comportamento preservado da implementação atual.

### 3.4 Algoritmo de seleção de modo

A sequência normativa de decisão do renderer, conforme ADR-0023 e
`contrato_lancador.md` seção 6.7, é:

```
obter area_lancador_w (largura total alocada ao lancador pela composição)
→ converter para content_w (descontar bordas e padding da caixa)
→ testar fila
→ testar matrizes válidas (n_rows crescente)
→ testar coluna mínima válida (n_col = 1, n_rows = n_itens)
→ se coluna mínima não couber: acionar o quadro mínimo canônico global
```

**Etapa 1 — tentativa de fila:**

```
fila_content_w_min = vao_margem_min
                   + sum(item_w_min para cada item)
                   + (n_itens - 1) × vao_entre_itens_min
                   + vao_margem_min
```

onde `vao_margem_min = 2` e `vao_entre_itens_min = 2` (de `lancador.json`).

Se `content_w >= fila_content_w_min`: **modo fila** — todos os itens em 1 linha,
1 coluna por item, nenhuma linha extra.

**Etapa 2 — distribuição em matriz:**

Se a fila não cabe, encontrar o maior `n_col` (menor `n_rows`) tal que a
distribuição caiba:

```
n_rows = 2, 3, ..., n_itens   (em ordem crescente)
n_col  = ceil(n_itens / n_rows)
```

Para cada candidato `(n_rows, n_col)`:

1. Atribuir itens às colunas coluna-a-coluna:
   - coluna `j` recebe itens nos índices `[j×n_rows, (j+1)×n_rows)` (até o último item existente)
2. Calcular a largura de cada coluna:
   ```
   chip_sub_w_col_j  = max(len(item["chip"]) + 2  para item em col_j)
   texto_sub_w_col_j = max(len(item["texto"])       para item em col_j)
   col_w_j = chip_sub_w_col_j + vao_chip_texto_min + texto_sub_w_col_j
   ```
3. Verificar se cabe:
   ```
   matriz_content_w_min = vao_margem_min
                        + sum(col_w_j  para j em [0, n_col))
                        + (n_col - 1) × vao_entre_colunas_min
                        + vao_margem_min
   ```
   Se `content_w >= matriz_content_w_min`: usar este `(n_rows, n_col)`.

O primeiro `(n_rows, n_col)` que couber é o escolhido (o de menor `n_rows`, logo
o de maior `n_col`). Não existe teto absoluto de colunas — o único limite é
`content_w`.

**Etapa 3 — coluna mínima válida:**

Se nenhuma distribuição com `n_col > 1` couber (`n_rows < n_itens` esgotado),
verificar se uma coluna única completa cabe:

```
coluna_minima_content_w = vao_margem_min
                        + max_chip_sub_w + vao_chip_texto_min + max_texto_sub_w
                        + vao_margem_min
```

onde:
- `max_chip_sub_w = max(len(item["chip"]) + 2  para item em itens)`
- `max_texto_sub_w = max(len(item["texto"])     para item em itens)`

Se `content_w >= coluna_minima_content_w`: usar **n_col = 1**, **n_rows = n_itens**.
Uma coluna única pode ser usada somente quando for uma representação válida completa.

**Etapa 4 — quadro mínimo canônico global:**

Se `content_w < coluna_minima_content_w` (equivalentemente,
`area_lancador_w < lancador_caixa_min_w`), nenhuma representação válida
do `lancador` cabe. O renderer deve acionar o **quadro mínimo canônico global**
(`quadro mínimo de terminal pequeno`, ADR-0017, reutilizado por ADR-0023).

O quadro mínimo:
- substitui integralmente toda a tela ou sessão TUI normal;
- não é renderizado dentro da caixa ou área do `lancador`;
- não preserva cabeçalho, corpo, dashboards ou `barra_de_menus`;
- reutiliza o mecanismo canônico global já existente;
- não cria mensagem específica para o `lancador`;
- não cria estado local restrito ao `lancador` ou a qualquer outro componente;
- desaparece automaticamente quando o espaço suficiente retorna (ver seção 3.4.1).

**Caso especial — lista vazia:**
Nenhum item → 0 linhas de conteúdo, nenhum erro.

**Caso especial — 1 item:**
A coluna mínima cabe na menor largura funcional; resultado é 1 linha, 1 coluna.

### 3.4.1 Recuperação automática

O estado de quadro mínimo não é permanente. A cada redesenho:

- o renderer recalcula `area_lancador_w` e `content_w`;
- se `content_w >= coluna_minima_content_w` (equivalente a
  `area_lancador_w >= lancador_caixa_min_w`), o quadro mínimo desaparece;
- a tela normal é reconstruída integralmente;
- o `lancador` volta à representação normal (fila ou matriz, conforme couber),
  recalculada a partir da largura atual;
- não é necessária ação do usuário;
- não é necessário reiniciar a aplicação;
- não há persistência do estado de quadro mínimo entre redesenhos.

### 3.5 Distribuição de espaço excedente (após determinar o modo)

Após encontrar a distribuição que cabe com vãos mínimos:

1. Calcular excesso = `content_w − min_content_w_do_modo_escolhido`
2. Expandir vãos entre itens/colunas até o máximo (`vao_maximo = 5`), distribuindo
   uniformemente; fração inteira com maior-resto absorvido pelos primeiros vãos.
3. Se ainda sobrar excesso, expandir as margens até o máximo (`5` cada).
4. Se ainda sobrar, o excesso vai para a direita do bloco.

O comportamento do passo 4 (excesso à direita) equivale ao alinhamento
declarado como `"esquerda"` pela instância — que é a configuração de
`config/telas/demo/demo.json`. Este alinhamento é **propriedade declarada pela
instância**, não regra universal do `lancador`. O alinhamento horizontal
pertence à instância declarante; testes genéricos devem respeitar o alinhamento
declarado e não generalizar o valor da `demo` para qualquer `lancador`.

Para o modo fila: as margens são borda↔primeiro_item (esquerda) e
último_item↔borda (direita).

Para o modo matriz: a mesma lógica aplica-se horizontalmente a cada linha:
cada célula da linha recebe a largura da coluna correspondente; os vãos entre
colunas e as margens são distribuídos conforme acima.

### 3.6 Preenchimento vertical dentro do lançador

Por coluna que não atinge `n_rows` (última coluna com itens incompletos): célula
vazia — sem preenchimento visual especial. A linha correspondente contém apenas
as colunas que têm item naquela posição.

Margens verticais (de `lancador.json`):
- `layout.vertical.margem_borda_superior = 1`: pelo menos 1 linha em branco
  entre borda superior e primeiro item.
- `layout.vertical.margem_borda_inferior = 1`: pelo menos 1 linha em branco
  entre último item e borda inferior.

Estas linhas em branco devem ser incluídas nas `linhas_conteudo` retornadas ao
`_caixa`.

### 3.7 Ordem declarativa preservada

A ordem dos itens nas linhas de conteúdo segue estritamente a ordem de declaração
em `itens[]` do JSON. Nenhum item pode ser omitido, duplicado ou reordenado.

Mapeamento coluna-a-coluna: o item de índice global `k` ocupa a posição:
```
coluna = k // n_rows
linha_dentro_da_coluna = k % n_rows
```

### 3.8 Ausência de paginação e resolução de largura insuficiente

O `lancador` nunca pagina (seção 6.1 de `contrato_lancador.md`). Todos os itens
devem aparecer, independente do número de itens ou da largura.

Quando a largura for insuficiente para qualquer representação válida (fila,
matriz ou coluna única), o mecanismo de resolução é o quadro mínimo canônico
global (seção 3.4, etapa 4). Não existe truncamento, overflow, omissão ou perda
de itens. Não existe estado ou mensagem local restrito ao `lancador`.

---

## 4. Configuração demonstrativa identificada

```yaml
arquivo: config/telas/demo/demo.json
id_tela: demo
elemento_lancador: lancador_principal
n_itens: 7
alinhamento: "esquerda"
```

### 4.1 Itens do lancador_principal (demo.json)

| idx | chip | texto | chip_sub_w | texto_w | item_w_min |
|---|---|---|---|---|---|
| 0 | d | Destino | 3 | 7 | 11 |
| 1 | g | Grupo Min. | 3 | 10 | 14 |
| 2 | 1 | Console | 3 | 7 | 11 |
| 3 | 2 | Dashboard | 3 | 9 | 13 |
| 4 | 3 | Matriz 2x2 | 3 | 10 | 14 |
| 5 | 4 | Matriz 3x2 | 3 | 10 | 14 |
| 6 | 5 | Matriz 2x4 | 3 | 10 | 14 |

### 4.2 Limiares de largura calculados

**Fila (n_col=7):**

```
fila_content_w_min = 2 + (11+14+11+13+14+14+14) + 6×2 + 2
                   = 2 + 91 + 12 + 2
                   = 107
```

Requer `content_w ≥ 107`, ou seja `area_lancador_w ≥ 110`.

**Matrix 4 colunas × 2 linhas (n_col=4, n_rows=2):**

Atribuição coluna-a-coluna:

| coluna | itens (idx) | chip_sub_w | texto_sub_w | col_w |
|---|---|---|---|---|
| 0 | 0,1 (Destino, Grupo Min.) | 3 | max(7,10)=10 | 14 |
| 1 | 2,3 (Console, Dashboard) | 3 | max(7,9)=9 | 13 |
| 2 | 4,5 (Matriz 2x2, Matriz 3x2) | 3 | max(10,10)=10 | 14 |
| 3 | 6 (Matriz 2x4) | 3 | 10 | 14 |

```
matriz_4x2_content_w_min = 2 + (14+13+14+14) + 3×2 + 2
                         = 2 + 55 + 6 + 2
                         = 65
```

Requer `content_w ≥ 65`, ou seja `area_lancador_w ≥ 68`.

**Matrix 3 colunas × 3 linhas (n_col=3, n_rows=3):**

| coluna | itens (idx) | col_w |
|---|---|---|
| 0 | 0,1,2 | 3+1+max(7,10,7)=14 |
| 1 | 3,4,5 | 3+1+max(9,10,10)=14 |
| 2 | 6 | 3+1+10=14 |

```
matriz_3x3_content_w_min = 2 + (14+14+14) + 2×2 + 2 = 50
```

Requer `area_lancador_w ≥ 53`.

**Matrix 2 colunas × 4 linhas (n_col=2, n_rows=4):**

| coluna | itens (idx) | col_w |
|---|---|---|
| 0 | 0,1,2,3 | 3+1+max(7,10,7,9)=14 |
| 1 | 4,5,6 | 3+1+max(10,10,10)=14 |

```
matriz_2x4_content_w_min = 2 + (14+14) + 1×2 + 2 = 34
```

Requer `area_lancador_w ≥ 37`.

**Coluna mínima (n_col=1, n_rows=7):**

```
max_chip_sub_w  = 3   (todos os chips têm 1 caractere)
max_texto_sub_w = 10  (Grupo Min., Matriz 2x2, Matriz 3x2, Matriz 2x4)

coluna_minima_content_w = 2 + 3 + 1 + 10 + 2 = 18
lancador_caixa_min_w    = 18 + 3              = 21
```

Requer `content_w ≥ 18`, ou seja `area_lancador_w ≥ 21`.
Quando `area_lancador_w < 21` (equivalente: `content_w < 18`): quadro mínimo canônico global.

### 4.3 Dimensões para demonstração

| dimensão | content_w | modo resultante | linhas × colunas |
|---|---|---|---|
| area_lancador_w=80, altura=30 | 77 | matriz | 2 linhas × 4 colunas |
| area_lancador_w=110, altura=30 | 107 | fila | 1 linha × 7 colunas |

Limites exatos:
- `area_lancador_w=110` (content_w=107): fila cabe exatamente com vãos mínimos.
- `area_lancador_w=109` (content_w=106): fila não cabe (106 < 107) → matrix 4×2.
- `area_lancador_w=68` (content_w=65): matrix 4×2 cabe exatamente com vãos mínimos.
- `area_lancador_w=67` (content_w=64): matrix 4×2 não cabe (64 < 65) → matrix 3×3.
- `area_lancador_w=21` (content_w=18): coluna mínima cabe exatamente.
- `area_lancador_w=20` (content_w=17): coluna mínima não cabe → quadro mínimo canônico global.

**Esperados independentes para area_lancador_w=110 (content_w=107 — fila, sem excesso):**

```
excess = 107 - 107 = 0 → vãos e margens permanecem no mínimo
margin_left  = 2
margin_right = 2
vao_entre_itens = 2 (cada vão interno)
```

Posições de início de cada item dentro do `content_w` (0-indexado):

| item | início | conteúdo | largura |
|---|---|---|---|
| [d] Destino    |  2 | `[d] Destino`    | 11 |
| [g] Grupo Min. | 15 | `[g] Grupo Min.` | 14 |
| [1] Console    | 31 | `[1] Console`    | 11 |
| [2] Dashboard  | 44 | `[2] Dashboard`  | 13 |
| [3] Matriz 2x2 | 59 | `[3] Matriz 2x2` | 14 |
| [4] Matriz 3x2 | 75 | `[4] Matriz 3x2` | 14 |
| [5] Matriz 2x4 | 91 | `[5] Matriz 2x4` | 14 |

Verificação total: 2 + 11 + 2 + 14 + 2 + 11 + 2 + 13 + 2 + 14 + 2 + 14 + 2 + 14 + 2 = 107 ✓

Todos os 7 itens estão na mesma linha. Não há segunda linha. Não há quadro mínimo.
Seis vãos internos mínimos (2 cada). Margens mínimas (2 cada).
A sobra à direita é zero nessa largura.

**Esperados independentes para area_lancador_w=80 (content_w=77 — matriz 4×2):**

Larguras de coluna independentes:
- col 0: chip_sub=3, texto_sub=max(7,10)=10 → col_w=14
- col 1: chip_sub=3, texto_sub=max(7,9)=9   → col_w=13
- col 2: chip_sub=3, texto_sub=max(10,10)=10 → col_w=14
- col 3: chip_sub=3, texto_sub=10            → col_w=14

```
excess = 77 - 65 = 12
Vãos (3 × máx. expansão 3): expansão = 9, cada vão = 5
Margens (2 × restante 3): 3 ÷ 2 = q=1 r=1 → margin_left=4, margin_right=3
```

Layout por linha dentro do `content_w` (0-indexado):

| segmento | início | largura |
|---|---|---|
| margin_left       |  0 |  4 |
| col 0 (largura=14)|  4 | 14 |
| vão 1             | 18 |  5 |
| col 1 (largura=13)| 23 | 13 |
| vão 2             | 36 |  5 |
| col 2 (largura=14)| 41 | 14 |
| vão 3             | 55 |  5 |
| col 3 (largura=14)| 60 | 14 |
| margin_right      | 74 |  3 |
| total             |    | 77 | ✓

Atribuição de itens (preenchimento coluna-a-coluna):

| posição | col 0     | col 1     | col 2        | col 3        |
|---|---|---|---|---|
| linha 0 | Destino   | Console   | Matriz 2x2   | Matriz 2x4   |
| linha 1 | Grupo Min.| Dashboard | Matriz 3x2   | (vazio)      |

Dentro de cada célula, o chip ocupa 3 chars (sub-coluna chip) + vão_chip_texto=1 +
o texto alinhado à esquerda dentro de texto_sub_w (com padding à direita):
- col 0 linha 0: `[d] Destino   ` (texto "Destino" + 3 espaços de padding para texto_sub=10)
- col 0 linha 1: `[g] Grupo Min.` (texto "Grupo Min." sem padding, texto_sub=10 ✓)
- col 1 linha 0: `[1] Console  ` (texto "Console" + 2 espaços de padding para texto_sub=9)
- col 1 linha 1: `[2] Dashboard` (texto "Dashboard" sem padding, texto_sub=9 ✓)

A sobra à direita (margin_right=3) reflete o alinhamento `"esquerda"` declarado
pela instância `demo`. Uma implementação que distribua a sobra de forma diferente
em instâncias que declarem outro alinhamento não comete regressão.

---

## 5. Formas de evidência separadas

### 5.1 Teste automatizado determinístico (obrigatório)

Deve carregar semanticamente `config/telas/demo/demo.json` e confirmar
`modelo.id == "demo"`. Deve chamar o renderer com dimensões explícitas, sem
depender da largura física do terminal.

Dimensões obrigatórias declaradas neste handoff:
- `area_lancador_w=110` (content_w=107): provar fila
- `area_lancador_w=109` (content_w=106): provar fronteira imediatamente abaixo da fila
- `area_lancador_w=80` (content_w=77): provar a matriz esperada (4×2)
- `area_lancador_w=21` (content_w=18): provar coluna mínima válida (1 coluna completa)
- `area_lancador_w=20` (content_w=17): provar quadro mínimo canônico global
- `area_lancador_w=110` após `area_lancador_w=20`: provar recuperação automática
- Cenário isolado em memória com `terminal_w=80` constante e `area_lancador_w` variando
  entre 20 e 21: provar causalmente o gatilho `area_lancador_w < lancador_caixa_min_w`
  enquanto os requisitos globais da tela permanecem satisfeitos. Ver seção 9.5.

As provas com `largura=20` e `largura=21` passadas ao renderer com a configuração `demo`
em arranjo vertical verificam o comportamento em largura global extrema, mas **não
constituem, isoladamente, prova causal do novo gatilho interno**: nessa configuração,
`terminal_w` e `area_lancador_w` coincidem materialmente (o arranjo vertical repassa
`total_w` a todos os elementos), e o quadro mínimo pode ser acionado pelo mínimo global
preexistente da tela (ADR-0017), não pelo gatilho específico do `lancador` (ADR-0023).

A altura deve ser declarada explicitamente e suficiente: `30`, salvo valor
diferente justificado no relatório de implementação.

### 5.2 Smoke do ponto de entrada

```bash
python demo/demo.py
```

Objetivo: confirmar funcionamento do ponto de entrada demonstrativo real,
carregamento da identidade `demo`, presença dos sete itens e ausência de erro
de integração.

Este comando, isolado, **não prova** os limiares de largura 80, 109 ou 110.
Código de saída zero isolado não comprova a identidade da tela nem o modo de
distribuição ativo.

### 5.3 Pseudo-TTY (quando aplicável)

```bash
script -q /dev/null python demo/demo.py
```

Quando executado, pode confirmar: inicialização em ambiente TTY, entrada no modo
de tela e ausência de erro durante redimensionamento automatizado. Pseudo-TTY
não substitui observação humana de layout, redraw ou transição visual.

### 5.4 Validação humana em TTY real (obrigatória antes do fechamento)

A validação humana em TTY real é obrigatória para confirmar visualmente:

1. `fila` em largura suficiente (`area_lancador_w ≥ 110`);
2. transição para `matriz` ao reduzir abaixo de `area_lancador_w=110`;
3. redistribuição matriz coluna a coluna ao reduzir progressivamente;
4. quadro mínimo canônico global quando `area_lancador_w < 21`;
5. substituição integral da tela normal no quadro mínimo (ausência de
   cabeçalho, corpo e barra enquanto o quadro mínimo estiver ativo);
6. recuperação automática ao ampliar acima de `area_lancador_w=21`;
7. retorno do `lancador` para matriz e depois fila ao ampliar;
8. ausência de cintilação, resíduos ou tela parcialmente preservada.

Procedimento:

```bash
python demo/demo.py
# Redimensionar progressivamente a janela do terminal
# Largura esperada ao iniciar: área alocada ao lancador ≥ 110 → fila
# Reduzir para < 110: deve aparecer matriz 4×2
# Reduzir progressivamente: matriz 3×3, 2×4, 1×7 (coluna única)
# Reduzir para area_lancador_w < 21: deve aparecer quadro mínimo global
# Ampliar para area_lancador_w ≥ 21: deve restaurar tela normal automaticamente
```

Se o método não permitir reproduzir uma largura ou cenário, o resultado correto é:

```
VALIDACAO_MANUAL_INCONCLUSIVA
```

Não usar `MANUAL_VALIDATION_FAILED` sem cenário reproduzido e comportamento incorreto.

---

## 6. Escopo da futura implementação

### 6.1 Arquivos autorizados

A implementação pode alterar ou criar somente:

| arquivo | natureza | motivo |
|---|---|---|
| `tela/renderizador.py` | alteração | implementação da regra de fila/matriz e quadro mínimo |
| `tela/teste_renderizador.py` | alteração | testes focais e de integração |
| `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md` | criação | relatório factual da implementação |

A configuração `config/telas/demo/demo.json` será somente lida.
O `demo/demo.py` será somente executado.
Nenhum arquivo demonstrativo precisa ser alterado.
Os contratos e ADRs serão somente lidos.
O relatório de implementação poderá ser criado.

**Nenhuma nova configuração demonstrativa precisa ser criada.**

`demo/demo.py` e `demo/teste_demo.py` não precisam ser alterados para esta
entrega. Se a análise do implementador identificar que uma alteração focal é
estritamente necessária em um destes arquivos, deve parar e pedir autorização
ao usuário (seção 13).

### 6.2 Arquivos preservados — proibida qualquer alteração

- `docs/contratos/` (todos os arquivos)
- `docs/adr/` (todos os arquivos)
- `docs/NOMENCLATURA.md`
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- `config/telas/demo/destino_minimo.json`
- `config/telas/demo/grupo_minimo.json`
- Todos os arquivos relacionados à `barra_de_menus` (exceto leitura)
- Arquivos relacionados ao cabeçalho
- Arquivos do ponto de entrada real do Orquestrador
- Handoffs e relatórios históricos do H-0030
- Qualquer arquivo não listado nominalmente em 6.1

---

## 7. Escopo negativo — o que este handoff não inclui

- Alteração da política do cabeçalho
- Quebra ou reticências da descrição do cabeçalho
- Alteração dos espaçamentos de `destino_minimo` ou `grupo_minimo`
- Nova ADR
- Alteração de contratos ou nomenclatura
- Mudança na distribuição da `barra_de_menus`
- Paginação do `lancador`
- Navegação, seleção ou execução de ações novas
- Alteração da semântica dos chips
- Persistência de estado
- Mudança no limite de caracteres do `texto`
- Alteração do ponto de entrada real `orquestrador.py`
- Criação do H-0033
- Refatoração ampla do renderer
- Commit

---

## 8. Alterações declarativas obrigatórias

```yaml
alteracoes_declarativas: nenhuma
```

`config/telas/demo/demo.json` já possui `lancador_principal` com 7 itens e
`regras_exibicao`/`layout` de alinhamento `"esquerda"` suficientes para
demonstrar fila e matriz de forma reproduzível. O implementador não deve criar
novos itens, alterar textos existentes nem adicionar campos ao JSON da tela.

---

## 9. Demonstração operacional

### 9.1 Pré-condições

**Suíte focal (pytest):**

```bash
python -m pytest tela/teste_renderizador.py -q --tb=no
```

Linha de base focal anterior informada: `217 passed`.

Esta contagem é evidência focal anterior e deverá ser atualizada factualmente
após a implementação. Esta suíte focal **não substitui** a suíte canônica completa.

**Suíte canônica completa:**

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python demo/teste_demo.py
python demo/teste_diagnostico.py
python demo/teste_explorar_barra_de_menus.py
```

Linha de base canônica anterior comprovada: `1803/1803`, `6/6` códigos de saída zero.

### 9.2 Prova automatizada de fila (area_lancador_w=110)

```bash
python -c "
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
raw = carregar_tela(None, 'demo', 'config/telas/demo')
modelo = construir_modelo(raw)
assert modelo.id == 'demo', f'id esperado demo, obtido {modelo.id}'
saida = renderizar_tela(modelo, largura=110, altura=30)
linhas = saida.splitlines()
# Prova: 7 itens presentes
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip in saida, f'chip {chip} ausente em largura=110'
# Prova: modo fila — [d] e [g] na mesma linha
lancador_linhas = [l for l in linhas if '[d]' in l or '[g]' in l]
assert any('[d]' in l and '[g]' in l for l in lancador_linhas), '[d] e [g] devem estar na mesma linha (fila)'
print('FILA OK: identity=demo, [d] e [g] na mesma linha em largura=110')
"
```

### 9.3 Prova automatizada de matriz 4×2 (area_lancador_w=80)

```bash
python -c "
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
raw = carregar_tela(None, 'demo', 'config/telas/demo')
modelo = construir_modelo(raw)
assert modelo.id == 'demo'
saida = renderizar_tela(modelo, largura=80, altura=30)
linhas = saida.splitlines()
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip in saida, f'chip {chip} ausente em largura=80'
linhas_d = [i for i, l in enumerate(linhas) if '[d]' in l]
linhas_g = [i for i, l in enumerate(linhas) if '[g]' in l]
linhas_1 = [i for i, l in enumerate(linhas) if '[1]' in l]
linhas_2 = [i for i, l in enumerate(linhas) if '[2]' in l]
assert linhas_d[0] != linhas_g[0], 'matriz: [d] e [g] devem estar em linhas diferentes'
assert linhas_d[0] == linhas_1[0], 'matriz: [d] e [1] devem estar na mesma linha (row 0)'
assert linhas_g[0] == linhas_2[0], 'matriz: [g] e [2] devem estar na mesma linha (row 1)'
assert linhas_d[0] < linhas_g[0], 'ordem: [d] antes de [g] (col 0)'
print('MATRIZ 4x2 OK: identity=demo, ordem coluna-a-coluna verificada em largura=80')
"
```

### 9.4 Prova automatizada de fronteira (area_lancador_w=110 vs 109)

```bash
python -c "
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
raw = carregar_tela(None, 'demo', 'config/telas/demo')
modelo = construir_modelo(raw)
# Fila em 110
s110 = renderizar_tela(modelo, largura=110, altura=30)
assert any('[d]' in l and '[g]' in l for l in s110.splitlines()), 'largura=110: fila esperada'
# Matriz em 109
s109 = renderizar_tela(modelo, largura=109, altura=30)
linhas_109 = s109.splitlines()
linhas_d = [i for i, l in enumerate(linhas_109) if '[d]' in l]
linhas_g = [i for i, l in enumerate(linhas_109) if '[g]' in l]
assert linhas_d[0] != linhas_g[0], 'largura=109: [d] e [g] em linhas diferentes (matriz)'
print('FRONTEIRA OK: fila em 110, matriz em 109')
"
```

### 9.5 Prova automatizada do quadro mínimo

#### 9.5.1 Verificação de fronteira global (suplementar — não isola o gatilho interno)

A verificação abaixo usa `config/telas/demo/demo.json` com `corpo.arranjo = "vertical"`.
Nessa configuração, o renderer repassa `total_w` a todos os elementos verticais; a
largura passada via `largura=N` determina simultaneamente `terminal_w` e
`area_lancador_w`. Portanto, estas verificações demonstram o comportamento em largura
global extrema, mas **não isolam o novo gatilho interno** `area_lancador_w < lancador_caixa_min_w`:
o quadro mínimo em `largura=20` pode ser acionado pelo mínimo global preexistente da
tela (ADR-0017), não necessariamente pelo gatilho específico do `lancador` (ADR-0023).

```yaml
largura_total_20:
  prova: comportamento global em largura extrema
  isola_gatilho_interno_do_lancador: false

largura_total_21:
  prova: primeira largura total em que a coluna calculada pode ser válida no cenário direto
  isola_gatilho_interno_do_lancador: false
```

```bash
python -c "
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
raw = carregar_tela(None, 'demo', 'config/telas/demo')
modelo = construir_modelo(raw)
# Coluna mínima válida em largura=21 (verificação de fronteira suplementar)
s21 = renderizar_tela(modelo, largura=21, altura=30)
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip in s21, f'chip {chip} ausente em largura=21 (coluna mínima deve caber)'
# Quadro mínimo em largura=20 (verificação de fronteira suplementar)
s20 = renderizar_tela(modelo, largura=20, altura=30)
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip not in s20, f'chip {chip} presente em largura=20 (quadro mínimo esperado)'
print('FRONTEIRA GLOBAL OK: coluna minima em largura=21, quadro minimo em largura=20')
print('Nota: prova suplementar de fronteira — nao isola o gatilho interno do lancador')
"
```

#### 9.5.2 Especificação do modelo em memória para prova isolada

O cenário isolado usa capacidades já existentes de composição. Nenhuma configuração
nova é criada; `config/telas/demo/demo.json` e `demo/demo.py` não são alterados.

| Parâmetro | Valor |
|---|---|
| `terminal_w` | 80 (constante nos dois casos, passado como `largura=80`) |
| `altura` | 30 (constante nos dois casos) |
| `corpo.arranjo` | `"horizontal"` (modo existente — nenhuma política nova) |
| `corpo.distribuicao.modo` | `"fracao"` (modo existente — nenhum campo novo) |
| Elementos do corpo | lancador + console (tipos existentes) |
| Conteúdo do lancador | 7 itens da demo (idênticos nos dois casos) |
| Elemento na área restante | `console` (renderiza `(console)` sem erro) |
| `coluna_minima_content_w` | 18 |
| `lancador_caixa_min_w` | 21 |

**Caso insuficiente:**

```yaml
corpo.distribuicao.valores: [20, 60]
area_lancador_w: 20     # _distribuir_larguras(80, [20, 60]) → [20, 60]
area_console_w: 60      # suficiente; não aciona o mínimo de 10 do container horizontal
resultado_esperado: quadro mínimo canônico global
causa: content_w_lancador = 20 − 3 = 17 < coluna_minima_content_w = 18
```

**Caso limite válido (controle):**

```yaml
corpo.distribuicao.valores: [21, 59]
area_lancador_w: 21     # _distribuir_larguras(80, [21, 59]) → [21, 59]
area_console_w: 59      # suficiente
resultado_esperado: tela normal com uma coluna válida completa
causa: content_w_lancador = 21 − 3 = 18 = coluna_minima_content_w = 18
```

A única diferença material entre os dois casos é `area_lancador_w = 20` versus
`area_lancador_w = 21`. O `terminal_w`, a `altura`, os itens do `lancador` e o
`console` restante são idênticos.

Código de construção do modelo em memória (implementável em `tela/teste_renderizador.py`):

```python
from tela.modelo import ModeloTela, Corpo, ElementoCorpo
from tela.renderizador import renderizar_tela

_ITENS_LANCADOR_DEMO = [
    {"id": "i0", "chip": "d", "texto": "Destino"},
    {"id": "i1", "chip": "g", "texto": "Grupo Min."},
    {"id": "i2", "chip": "1", "texto": "Console"},
    {"id": "i3", "chip": "2", "texto": "Dashboard"},
    {"id": "i4", "chip": "3", "texto": "Matriz 2x2"},
    {"id": "i5", "chip": "4", "texto": "Matriz 3x2"},
    {"id": "i6", "chip": "5", "texto": "Matriz 2x4"},
]
# max_chip_sub_w=3, max_texto_sub_w=10
# coluna_minima_content_w = 2+3+1+10+2 = 18; lancador_caixa_min_w = 21

_BARRA_MINIMA = {"chips": [{"id": "esc", "tecla": "Esc", "texto": "Sair"}]}

def _modelo_isolado(area_lancador_w, terminal_w=80):
    """Modelo sintético com arranjo horizontal e area_lancador_w controlada independentemente."""
    area_restante = terminal_w - area_lancador_w
    return ModeloTela(
        id="teste_isolamento_lancador",
        schema="tela.v1",
        cabecalho={"titulo": "TESTE", "descricao": "Isolamento do gatilho lancador"},
        corpo=Corpo(
            arranjo="horizontal",
            distribuicao={"modo": "fracao", "valores": [area_lancador_w, area_restante]},
            elementos=[
                ElementoCorpo(
                    id="lancador_teste",
                    tipo="lancador",
                    _campos_inertes={"titulo": "Navegar", "itens": _ITENS_LANCADOR_DEMO},
                ),
                ElementoCorpo(
                    id="console_resto",
                    tipo="console",
                    _campos_inertes={"titulo": "Console"},
                ),
            ],
        ),
        barra_de_menus=_BARRA_MINIMA,
        _raw={},
    )
```

#### 9.5.3 Prova isolada do gatilho interno (obrigatória)

```bash
python -c "
from tela.modelo import ModeloTela, Corpo, ElementoCorpo
from tela.renderizador import renderizar_tela

_ITENS = [
    {'id': 'i0', 'chip': 'd', 'texto': 'Destino'},
    {'id': 'i1', 'chip': 'g', 'texto': 'Grupo Min.'},
    {'id': 'i2', 'chip': '1', 'texto': 'Console'},
    {'id': 'i3', 'chip': '2', 'texto': 'Dashboard'},
    {'id': 'i4', 'chip': '3', 'texto': 'Matriz 2x2'},
    {'id': 'i5', 'chip': '4', 'texto': 'Matriz 3x2'},
    {'id': 'i6', 'chip': '5', 'texto': 'Matriz 2x4'},
]
# lancador_caixa_min_w=21; coluna_minima_content_w=18

barra = {'chips': [{'id': 'esc', 'tecla': 'Esc', 'texto': 'Sair'}]}

def _modelo(area_w):
    return ModeloTela(
        id='teste_isolamento_lancador', schema='tela.v1',
        cabecalho={'titulo': 'TESTE', 'descricao': 'Isolamento'},
        corpo=Corpo(
            arranjo='horizontal',
            distribuicao={'modo': 'fracao', 'valores': [area_w, 80 - area_w]},
            elementos=[
                ElementoCorpo(id='lancador_teste', tipo='lancador',
                              _campos_inertes={'titulo': 'Navegar', 'itens': _ITENS}),
                ElementoCorpo(id='console_resto', tipo='console',
                              _campos_inertes={'titulo': 'Console'}),
            ],
        ),
        barra_de_menus=barra, _raw={},
    )

# 1. Controle: terminal_w=80, area_lancador_w=21 → tela normal
s21 = renderizar_tela(_modelo(21), largura=80, altura=30)
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip in s21, f'FALHA controle: chip {chip} ausente (area_lancador_w=21, terminal_w=80)'
# terminal_w=80 é suficiente para a tela normal → requisitos globais satisfeitos

# 2. Caso insuficiente: terminal_w=80 (mesmo), area_lancador_w=20 → quadro mínimo
s20 = renderizar_tela(_modelo(20), largura=80, altura=30)
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip not in s20, f'FALHA: chip {chip} presente (area_lancador_w=20, quadro minimo esperado)'
# Nenhum elemento da tela normal deve permanecer visível no quadro mínimo

# Prova causal:
# - terminal_w=80 constante nos dois casos → mínimo global preexistente não foi violado
# - area_console_w=60 (ou 59) → console renderizável; demais componentes válidos
# - única condição inválida: area_lancador_w=20 < lancador_caixa_min_w=21
# - portanto o quadro mínimo foi causado exclusivamente pelo gatilho do lancador (ADR-0023)
print('ISOLAMENTO OK: terminal_w=80 constante')
print('area_lancador_w=21 → tela normal (controle); area_lancador_w=20 → quadro minimo global')
print('Causa: area_lancador_w < lancador_caixa_min_w; requisitos globais satisfeitos em ambos os casos')
"
```

### 9.6 Prova automatizada de recuperação

#### 9.6.1 Recuperação no cenário global (suplementar)

A prova abaixo usa a configuração `demo` com arranjo vertical. Confirma que após
`largura=20` (fronteira global), o retorno para `largura=110` restaura a tela normal.
Não isola o gatilho interno do `lancador` (ver classificação na seção 9.5.1).

```bash
python -c "
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
raw = carregar_tela(None, 'demo', 'config/telas/demo')
modelo = construir_modelo(raw)
# Quadro mínimo em largura=20 (suplementar)
s20 = renderizar_tela(modelo, largura=20, altura=30)
for chip in ['[d]', '[g]']:
    assert chip not in s20, f'chip {chip} nao deveria aparecer em largura=20'
# Recuperação: voltar para largura=110 deve restaurar a fila
s110 = renderizar_tela(modelo, largura=110, altura=30)
assert any('[d]' in l and '[g]' in l for l in s110.splitlines()), 'recuperacao: fila esperada em 110'
print('RECUPERACAO GLOBAL OK: tela normal restaurada ao voltar para largura=110')
print('Nota: prova suplementar de fronteira global — nao isola o gatilho interno do lancador')
"
```

#### 9.6.2 Recuperação isolada (obrigatória)

A sequência obrigatória é `area_lancador_w = 21 → 20 → 21`, com `terminal_w = 80`
constante. O renderer não mantém estado entre chamadas puras: a prova de recuperação
é equivalente a demonstrar que `renderizar_tela(_modelo(21), largura=80, altura=30)`
produz tela normal independentemente de ter sido chamado antes ou depois de
`renderizar_tela(_modelo(20), largura=80, altura=30)`. Não é alegada validação de
estado interno entre chamadas; o que se prova é o determinismo: mesma entrada → mesma saída.

```bash
python -c "
from tela.modelo import ModeloTela, Corpo, ElementoCorpo
from tela.renderizador import renderizar_tela

_ITENS = [
    {'id': 'i0', 'chip': 'd', 'texto': 'Destino'},
    {'id': 'i1', 'chip': 'g', 'texto': 'Grupo Min.'},
    {'id': 'i2', 'chip': '1', 'texto': 'Console'},
    {'id': 'i3', 'chip': '2', 'texto': 'Dashboard'},
    {'id': 'i4', 'chip': '3', 'texto': 'Matriz 2x2'},
    {'id': 'i5', 'chip': '4', 'texto': 'Matriz 3x2'},
    {'id': 'i6', 'chip': '5', 'texto': 'Matriz 2x4'},
]
barra = {'chips': [{'id': 'esc', 'tecla': 'Esc', 'texto': 'Sair'}]}

def _modelo(area_w):
    return ModeloTela(
        id='teste_isolamento_lancador', schema='tela.v1',
        cabecalho={'titulo': 'TESTE', 'descricao': 'Isolamento'},
        corpo=Corpo(
            arranjo='horizontal',
            distribuicao={'modo': 'fracao', 'valores': [area_w, 80 - area_w]},
            elementos=[
                ElementoCorpo(id='lancador_teste', tipo='lancador',
                              _campos_inertes={'titulo': 'Navegar', 'itens': _ITENS}),
                ElementoCorpo(id='console_resto', tipo='console',
                              _campos_inertes={'titulo': 'Console'}),
            ],
        ),
        barra_de_menus=barra, _raw={},
    )

# Sequência: area_lancador_w = 21 → 20 → 21
# Passo 1: area_lancador_w=21 → tela normal
s_antes = renderizar_tela(_modelo(21), largura=80, altura=30)
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip in s_antes, f'FALHA passo 1: chip {chip} ausente (area_lancador_w=21)'

# Passo 2: area_lancador_w=20 → quadro mínimo
s_minimo = renderizar_tela(_modelo(20), largura=80, altura=30)
for chip in ['[d]', '[g]']:
    assert chip not in s_minimo, f'FALHA passo 2: chip {chip} presente (area_lancador_w=20)'

# Passo 3: area_lancador_w=21 novamente → tela normal reconstruída
s_depois = renderizar_tela(_modelo(21), largura=80, altura=30)
for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
    assert chip in s_depois, f'FALHA passo 3: chip {chip} ausente apos recuperacao'
# Determinismo: s_antes == s_depois (sem estado persistente entre chamadas)
assert s_antes == s_depois, 'FALHA: recuperacao nao deterministica (resultado difere do passo 1)'
# Confirmação: os itens permaneceram integrais e na ordem; demais componentes retornaram
print('RECUPERACAO ISOLADA OK: sequencia 21->20->21; terminal_w=80 constante')
print('Sem reinicio; sem comando do usuario; sem estado persistente; reconstrucao deterministica')
"
```

### 9.7 Prova de ausência de paginação

```bash
python -c "
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
raw = carregar_tela(None, 'demo', 'config/telas/demo')
modelo = construir_modelo(raw)
for largura in [21, 37, 53, 68, 80, 109, 110]:
    saida = renderizar_tela(modelo, largura=largura, altura=30)
    for chip in ['[d]', '[g]', '[1]', '[2]', '[3]', '[4]', '[5]']:
        assert chip in saida, f'chip {chip} ausente em largura={largura} (paginacao?)'
print('SEM PAGINACAO OK: todos os 7 chips presentes em todas as larguras válidas')
"
```

### 9.8 Smoke do ponto de entrada

```bash
python demo/demo.py
```

Confirma: funcionamento do ponto de entrada, carregamento da identidade `demo`,
ausência de erro de integração. Este comando não prova os limiares de largura.

---

## 10. Testes obrigatórios

### 10.1 Suíte focal e suíte canônica completa

**Suíte focal:**

```bash
python -m pytest tela/teste_renderizador.py -q --tb=short
```

Linha de base focal anterior informada: `217 passed`. Após a implementação, a
contagem deve ser atualizada com o total real (217 existentes + novos).

Esta suíte focal **não é** a suíte canônica completa.

**Suíte canônica completa:**

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python demo/teste_demo.py
python demo/teste_diagnostico.py
python demo/teste_explorar_barra_de_menus.py
```

Linha de base canônica anterior comprovada: `1803/1803`, `6/6` códigos de saída zero.

O relatório de implementação deve registrar:
- resultado individual de cada script;
- total consolidado;
- código de saída de cada comando;
- distinção entre contagem focal por `pytest` e contagem canônica dos scripts;
- registro de qualquer alteração de contagem decorrente dos novos testes.

Não é permitido que a suíte focal substitua a suíte canônica completa.

### 10.2 Testes focais do cálculo de fila

**T-01 — Fila cabe exatamente (zero excesso)**

```python
# Items: chip "A" texto "Uno" (item_w=3+1+3=7), chip "B" texto "Dos" (item_w=3+1+3=7)
# fila_content_w_min = 2 + 7+7 + 1×2 + 2 = 20
# content_w = 20 → fila cabe com vãos mínimos
# Verificação: a saída contém exatamente 1 linha de conteúdo do lancador
# e essa linha contém "[A]" e "[B]"
```

**T-02 — Fila 1 item (cardinalidade 1)**

```python
# Item: chip "X" texto "Unico" (5 chars), item_w=3+1+5=9
# fila_content_w_min = 2+9+2 = 13
# A qualquer content_w ≥ 13: 1 linha de conteúdo com "[X] Unico"
# Verificação: exatamente 1 linha de conteúdo (sem fragmentação em matrix)
```

**T-03 — Cardinalidade zero**

```python
# Items = []
# content_w = qualquer valor positivo
# Verificação: 0 linhas de conteúdo retornadas, sem RenderizadorErro
```

**T-04 — Limite exato de largura (content_w = fila_content_w_min)**

```python
# Mesmo conjunto de 2 itens do T-01
# content_w = 20: 1 linha (fila)
# content_w = 19: 2+ linhas (matriz)
# Verificação do limite: fila em 20, matriz em 19
```

**T-05 — 1 unidade abaixo do limite (content_w = fila_content_w_min - 1)**

```python
# Mesmo conjunto do T-01, content_w = 19
# Resultado esperado: 2 linhas de conteúdo (matrix, 1 col, 2 rows)
# Linha 0: "[A] Uno" (com padding)
# Linha 1: "[B] Dos" (com padding)
# Verificação: "[A]" e "[B]" em linhas diferentes
```

### 10.3 Testes focais do cálculo de matriz

**T-06 — Ordem coluna-a-coluna (3 itens, 2 colunas)**

```python
# Items: chip "A" texto "AAA" (7), chip "B" texto "BBB" (7), chip "C" texto "CCC" (7)
# Fila min: 2+7+7+7+2×2+2 = 30; content_w = 20 < 30 → matrix
# n_rows=2, n_col=2
# col 0: items A, B → col_w = 7
# col 1: items C   → col_w = 7
# matrix_content_w_min = 2+7+7+1×2+2 = 20 → cabe em content_w=20
# Atribuição:
#   row 0: col0=[A], col1=[C]
#   row 1: col0=[B], col1=vazio
# Verificações:
#   - "[A]" e "[C]" na mesma linha (row 0)
#   - "[B]" em linha separada (row 1)
#   - "[A]" aparece antes (linha de índice menor) que "[B]"
#   - Todos os 3 chips presentes
```

**T-07 — Largura de coluna por coluna, não global (2 colunas com larguras distintas)**

```python
# Items:
#   chip "A" texto "Curto"         (5 chars) → item_w=3+1+5=9
#   chip "B" texto "MuitoMaisLong" (13 chars) → item_w=3+1+13=17
#   chip "C" texto "Ok"            (2 chars) → item_w=3+1+2=6
# n_itens=3; content_w=30
#
# Fila min = 2 + 9+17+6 + 2×2 + 2 = 38 > 30 → não cabe
#
# Tentativa matrix n_rows=2, n_col=2:
#   col 0: items A(Curto), B(MuitoMaisLong)
#     chip_sub = max(3,3) = 3
#     texto_sub = max(5,13) = 13
#     col_w_0 = 3+1+13 = 17
#   col 1: item C(Ok)
#     chip_sub = 3
#     texto_sub = 2
#     col_w_1 = 3+1+2 = 6
#   matrix_content_w_min = 2 + 17+6 + 1×2 + 2 = 29 ≤ 30 → cabe
#
# Verificações com content_w=30:
#   - col_w_0 = 17 (independente de col_w_1)
#   - col_w_1 = 6  (independente de col_w_0)
#   - col_w_1 ≠ col_w_0 (colunas com larguras distintas)
#   - Linha 0: "[A] Curto" alinhado em col_w_0=17, depois gap, depois "[C] Ok" em col_w_1=6
#   - Linha 1: "[B] MuitoMaisLong" em col_w_0=17, depois gap, depois (vazio) em col_w_1=6
#   - "[A]" e "[C]" na mesma linha; "[B]" em linha diferente
#   - Posição de início de col 1 = margin_left + col_w_0 + gap
#   - A largura maior de col 0 (17) NÃO é aplicada a col 1 (6)
#
# O teste deve falhar se a implementação usar largura global única para todas as colunas.
# Os valores esperados são derivados das autoridades deste handoff, não da função implementada.
```

**T-08 — Ausência de paginação (muitos itens, largura restrita)**

```python
# Items: 10 itens com chip de 1 char, texto de 4 chars (item_w = 3+1+4 = 8)
# coluna_minima_content_w = 2 + 3 + 1 + 4 + 2 = 12
# Em content_w = 12: coluna única válida com 10 linhas
# Verificação: todos os 10 chips presentes, nenhum omitido
```

**T-09 — Redução e ampliação (determinismo)**

```python
# Mesmo conjunto de itens renderizado a content_w=20, depois a content_w=30,
# e de volta a content_w=20: o resultado deve ser idêntico nas duas chamadas
# com content_w=20 (mesmo itens, mesma largura → mesma saída)
```

**T-14 — Fronteira do quadro mínimo (coluna mínima e um abaixo)**

```python
# Items: chip "A" texto "ABCDE" (5 chars), chip "B" texto "XY" (2 chars)
# max_chip_sub = 3, max_texto_sub = max(5,2) = 5
# coluna_minima_content_w = 2 + 3 + 1 + 5 + 2 = 13
#
# content_w = 13: coluna mínima válida → todos os chips presentes
# content_w = 12: abaixo do mínimo → quadro mínimo canônico global
#   Nenhum chip do lancador deve aparecer na saída
#   Cabeçalho, corpo e barra_de_menus não aparecem enquanto quadro mínimo ativo
#
# Verificações:
#   - Em content_w=13: "[A]" e "[B]" presentes na saída
#   - Em content_w=12: "[A]" e "[B]" ausentes na saída
#   - Em content_w=12: nenhum elemento da tela normal visível
```

**T-15 — Recuperação automática após quadro mínimo**

```python
# Mesmo conjunto de T-14
# Renderizar com content_w=12 (quadro mínimo)
# Renderizar novamente com content_w=13 (coluna mínima)
# Verificação: chips presentes na segunda renderização (recuperação automática)
# A primeira renderização não deve afetar a segunda — sem estado persistente
```

Os testes T-14 e T-15 usam itens sintéticos com `coluna_minima_content_w = 13` e não
dependem da configuração `demo`. Eles provam o comportamento de fronteira de forma geral,
mas **não constituem, isoladamente, prova causal do gatilho `area_lancador_w < lancador_caixa_min_w`**
com viewport global suficiente. Os testes de isolamento abaixo são obrigatórios para
essa prova.

**T-ISOL-01 — Isolamento do gatilho: modelo em memória, viewport global constante**

```python
# Modelo sintético em memória (ver seção 9.5.2)
# terminal_w = 80 (constante) — passado como largura=80 ao renderer
# area_lancador_w = 20 (via distribuicao={'modo':'fracao','valores':[20,60]})
# Demais requisitos globais: satisfeitos (area_console_w=60; barra_de_menus cabe em content_w=77)
#
# coluna_minima_content_w = 18; lancador_caixa_min_w = 21
# Condição inválida: content_w_lancador = 17 < coluna_minima_content_w = 18
#
# Resultado esperado: quadro mínimo canônico global
# Verificações:
#   - Nenhum dos 7 chips do lancador presente na saída
#   - Nenhum elemento da tela normal visível (nenhum chip de cabeçalho, corpo ou barra)
# Causa específica comprovada: a única diferença entre T-ISOL-01 e T-ISOL-02 é
#   area_lancador_w = 20 versus area_lancador_w = 21, com terminal_w=80 constante
#
# Os valores esperados derivam da seção 4.2 deste handoff, não da implementação.
```

**T-ISOL-02 — Controle no limite: mesmo modelo, mesmo viewport, area_lancador_w=21**

```python
# Mesmo modelo sintético de T-ISOL-01, com distribuicao={'modo':'fracao','valores':[21,59]}
# terminal_w = 80 (idêntico ao T-ISOL-01)
# area_lancador_w = 21 (via _distribuir_larguras(80, [21,59]) → [21,59])
#
# Condição válida: content_w_lancador = 18 = coluna_minima_content_w = 18
#
# Resultado esperado: tela normal com uma coluna válida completa
# Verificações:
#   - Todos os 7 chips presentes: [d], [g], [1], [2], [3], [4], [5]
#   - Nenhum quadro mínimo
#   - Uma coluna válida completa (7 itens, 7 linhas de conteúdo)
#   - Nenhum truncamento, paginação, omissão ou overflow
#
# Diferença material em relação a T-ISOL-01: somente area_lancador_w = 21 vs 20
```

**T-ISOL-03 — Recuperação isolada: sequência 21 → 20 → 21**

```python
# Sequência de renderizações com o mesmo modelo e terminal_w=80 constante:
#   Passo 1: _modelo_isolado(21) → tela normal   (todos os 7 chips presentes)
#   Passo 2: _modelo_isolado(20) → quadro mínimo (nenhum chip presente)
#   Passo 3: _modelo_isolado(21) → tela normal   (todos os 7 chips presentes)
#
# O renderer não mantém estado entre chamadas puras; portanto:
#   s_passo1 == s_passo3 (determinismo: mesma entrada → mesma saída)
#
# Confirmações:
#   - Não houve reinício
#   - Não houve comando do usuário entre os passos
#   - Resultado do passo 3 é idêntico ao passo 1 (assert s_passo1 == s_passo3)
#   - Os itens permaneceram integrais e na ordem; demais componentes retornaram
#
# Os valores esperados não são calculados chamando a mesma função a ser implementada.
```

### 10.4 Teste de integração com a configuração demonstrativa

**T-10 — ID da tela e modo fila (area_lancador_w=110)**

```python
# carregar_tela("demo", "config/telas/demo") → construir_modelo → renderizar_tela(largura=110, altura=30)
# content_w = 107; excess = 0; fila exata; todos os vãos e margens mínimos
#
# Verificações obrigatórias:
#   - modelo.id == "demo"
#   - len(itens) == 7
#   - Todos os 7 chips presentes ([d][g][1][2][3][4][5])
#   - [d] e [g] na mesma linha (fila — content_w=107 ≥ fila_content_w_min=107)
#   - Exatamente 1 linha de conteúdo do lancador (não há segunda linha)
#   - Nenhum chip em linha diferente da linha principal
#   - Ausência de quadro mínimo (todos os chips do lancador visíveis)
#
# Verificações de posicionamento (derivadas da tabela da seção 4.3):
#   - [d] aparece na posição de conteúdo 2 (após margem esquerda=2)
#   - [g] aparece na posição 15 (após [d](11) + gap(2) = 13 + 2 = 15)
#   - Seis vãos internos iguais ao mínimo (2 chars cada, pois excess=0)
#   - Margem direita = 2 (mínimo, pois excess=0)
#
# Os valores esperados derivam da seção 4.3 deste handoff, não da implementação.
```

**T-11 — Modo matriz 4×2 (area_lancador_w=80)**

```python
# renderizar_tela(modelo, largura=80, altura=30)
# content_w = 77; excess = 12; matriz 4×2
#
# Verificações de estrutura:
#   - [d] e [g] em linhas de índice diferentes (matrix, não fila)
#   - [d] e [1] na mesma linha (row 0, cols 0 e 1)
#   - [g] e [2] na mesma linha (row 1, cols 0 e 1)
#   - [3] e [d] na mesma linha (row 0, cols 2 e 0)
#   - [4] e [g] na mesma linha (row 1, cols 2 e 0)
#   - [5] na mesma linha que [d] (row 0, col 3)
#   - Todos os 7 chips presentes
#   - Ausência de paginação
#   - Ausência de quadro mínimo
#
# Verificações de larguras independentes (derivadas da seção 4.3):
#   - col 0 (Destino/Grupo Min.) = chip_sub=3, texto_sub=10, col_w=14
#   - col 1 (Console/Dashboard) = chip_sub=3, texto_sub=9,  col_w=13
#   - col 2 (Matriz 2x2/Matriz 3x2) = chip_sub=3, texto_sub=10, col_w=14
#   - col 3 (Matriz 2x4) = chip_sub=3, texto_sub=10, col_w=14
#   - col 1 (largura=13) é distinta de col 0 (largura=14)
#
# Verificações de layout com excess=12 (derivadas da seção 4.3):
#   - Três vãos internos = 5 cada (máximo, após distribuição do excess)
#   - margin_left = 4, margin_right = 3 (excesso residual distribuído)
#   - Col 0 começa na posição 4 dentro do content_w
#   - Col 1 começa na posição 23 (4 + 14 + 5)
#   - Col 2 começa na posição 41 (23 + 13 + 5)
#   - Col 3 começa na posição 60 (41 + 14 + 5)
#   - Sobra à direita = 3 chars (margin_right=3, reflete alinhamento "esquerda" da instância demo)
#
# Os valores esperados derivam da seção 4.3 deste handoff, não da implementação.
```

**T-12 — Limite exato de fila (area_lancador_w=110) vs abaixo (area_lancador_w=109)**

```python
# renderizar_tela(modelo, largura=110, altura=30): [d] e [g] na mesma linha
# renderizar_tela(modelo, largura=109, altura=30): [d] e [g] em linhas diferentes
```

**T-13 — Componentes não relacionados preservados**

```python
# Na saída de renderizar_tela(modelo, largura=80, altura=30):
# - Cabeçalho ainda presente: "╭ ORQUESTRADOR"
# - Barra ainda presente: "[Esc]" e "[?]"
# - Caixa do lancador com título: "╭ NAVEGAR"
```

### 10.5 Princípio de independência dos valores esperados

Nenhum teste pode calcular o valor esperado chamando a mesma função ou
reproduzindo integralmente o mesmo algoritmo da implementação. Os valores
esperados nos testes acima derivam das especificações desta seção 3 e da tabela
da seção 4.3, calculados manualmente.

---

## 11. Critérios de aceite

1. Todos os itens cabem em uma única fila quando `content_w ≥ fila_content_w_min`.
2. A redução abaixo do limite da fila ativa a matriz.
3. A matriz possui múltiplas colunas quando a largura permite.
4. A ordem de preenchimento é coluna-a-coluna.
5. Nenhum item é perdido, duplicado ou reordenado.
6. A largura de cada coluna é calculada pelo maior item da própria coluna,
   com chip e texto como sub-colunas independentes — o maior item de uma coluna
   não altera indevidamente as demais colunas.
7. O alinhamento horizontal é conforme o declarado pela instância.
8. Não existe paginação — todos os itens aparecem em qualquer largura válida.
9. O comportamento é determinístico para a mesma largura e os mesmos itens.
10. Cardinalidade zero não provoca erro — retorna 0 linhas de conteúdo.
11. Cardinalidade um permanece válida — retorna exatamente 1 linha.
12. Uma coluna única pode ser usada somente quando for uma representação válida completa
    (`content_w ≥ coluna_minima_content_w`).
13. Quando `content_w < coluna_minima_content_w`, o quadro mínimo canônico global
    é acionado — exatamente um caractere abaixo da largura mínima funcional.
14. O quadro mínimo substitui integralmente toda a tela normal: cabeçalho, corpo,
    `lancador`, dashboards e `barra_de_menus` não são exibidos enquanto ativo.
15. A recuperação automática ocorre quando `content_w` volta a `≥ coluna_minima_content_w`;
    a tela normal é reconstruída integralmente sem ação do usuário.
16. Após recuperação, o `lancador` retorna ao modo normal (fila ou matriz, conforme couber).
17. A prova semântica da tela `demo` confirma `modelo.id == "demo"`.
18. A prova automatizada usa dimensões explícitas independentes da largura do terminal.
19. O smoke real do ponto de entrada (`python demo/demo.py`) termina com código de saída zero.
20. A validação humana em TTY real confirma as transições visuais antes do fechamento.
21. A suíte focal aprovada após implementação registra contagem atualizada.
22. A suíte canônica completa (6 scripts, 1803+ testes) está aprovada.
23. O limite exato entre fila e matriz possui teste de fronteira (T-04, T-12).
24. A prova isolada do gatilho (T-ISOL-01/T-ISOL-02) demonstra que `area_lancador_w < lancador_caixa_min_w`
    aciona o quadro mínimo global enquanto `terminal_w` permanece suficiente para a tela
    normal em outras condições; o cenário de controle (T-ISOL-02) confirma que a tela
    normal é produzida com os mesmos itens e o mesmo `terminal_w`.
25. As provas de fronteira global (`largura=20` e `largura=21` com a configuração `demo`
    em arranjo vertical) são classificadas explicitamente como suplementares e não
    constituem, isoladamente, prova causal do novo gatilho interno.

---

## 12. Relatório de implementação obrigatório

Criar: `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md`

O relatório deve registrar:

- Autoridades usadas: ADR-0023 e sua aplicação aprovada, contratos ativos,
  nomenclatura ativa, demais ADRs aplicáveis
- Arquivos alterados (lista nominal)
- Regra normativa aplicada (referência às seções deste handoff e às autoridades)
- Algoritmo implementado (pseudocódigo ou descrição do código)
- Função(ões) alterada(s) em `tela/renderizador.py` e estrutura resultante
  (como caminho recomendado de implementação, não como norma permanente)
- As cinco grandezas de largura usadas (`terminal_w`, `area_lancador_w`,
  `lancador_caixa_min_w`, `content_w`, `coluna_minima_content_w`)
- Algoritmo de seleção de fila e matriz com as etapas 1 a 4
- Valor calculado de `coluna_minima_content_w` para a configuração usada
- Limite de coluna válida e acionamento do quadro mínimo global
- Configuração demonstrativa usada (`config/telas/demo/demo.json`)
- Dimensões testadas (ao mínimo: largura=20, 21, 80, 109, 110)
- Dimensões explícitas declaradas como numéricas (não dependentes do terminal)
- Prova de fila: evidência de que [d] e [g] aparecem na mesma linha em largura=110
- Prova de matriz: evidência de que [d] e [g] aparecem em linhas diferentes em largura=80
- Prova da ordem coluna-a-coluna: qual item aparece em qual linha em largura=80
- Prova do quadro mínimo: evidência em largura=20 (classificada como fronteira suplementar)
- Prova de recuperação: evidência ao voltar para largura suficiente (suplementar)
- Prova de fronteira global e prova isolada do gatilho, registradas separadamente:

```yaml
prova_global_largura_20_21:
  finalidade: fronteira suplementar
  isolamento_do_gatilho: false

prova_isolada_area_lancador:
  terminal_w: 80
  area_insuficiente: 20
  area_valida: 21
  minimo_caixa: 21
  modelo_em_memoria: teste_isolamento_lancador (arranjo=horizontal, fracao [20,60] / [21,59])
  demais_requisitos_globais: satisfeitos (controle com area_lancador_w=21 produziu tela normal)
  evidencias: saida com area=20 sem chips do lancador; saida com area=21 com todos os 7 chips
  resultado: quadro_minimo em area=20 causado exclusivamente por area_lancador_w < lancador_caixa_min_w
```

- Explicação de por que o quadro mínimo no cenário isolado não foi causado pelo mínimo
  global preexistente da tela: o controle T-ISOL-02 (área=21, mesmo terminal_w=80) produziu
  tela normal, provando que os requisitos globais estavam satisfeitos; a única diferença
  no caso insuficiente foi `area_lancador_w = 20 < lancador_caixa_min_w = 21`.
- Esperados independentes usados (referência às seções 4.3 e 10.4)
- Testes criados e resultados
- Resultado da suíte focal: `python -m pytest tela/teste_renderizador.py -q`
  com contagem atualizada (distinguida da suíte canônica)
- Resultado da suíte canônica completa (6 scripts, contagem individual e total)
- Resultado do smoke do ponto de entrada (`python demo/demo.py`, código de saída)
- Resultado do pseudo-TTY, quando executado
- Resultado da validação humana em TTY real (ou `VALIDACAO_MANUAL_INCONCLUSIVA`
  com motivo; não usar `MANUAL_VALIDATION_FAILED` sem cenário reproduzido e
  comportamento incorreto observado)
- Estado Git ao final (`git status --short`)
- Arquivos não rastreados
- Temporários ou caches observados e não removidos
- Exceções operacionais autorizadas, se existirem
- Limitações identificadas
- Itens não validados
- Bloqueios encontrados
- Fatos `NAO_CONFIRMADO`

O relatório **não pode autoaprovar formalmente a implementação**.

---

## 13. Exceção operacional

Se durante a implementação um arquivo fora da lista nominal (seção 6.1) for
estritamente necessário para cumprir o handoff, preservar a suíte obrigatória
ou evitar o aborto desproporcional da entrega, o executor deve **parar antes
de alterá-lo** e pedir autorização explícita ao usuário.

O pedido deve informar:
- arquivo;
- motivo exato;
- escopo exato da alteração;
- mudança esperada.

A autorização não permite criar semântica, arquitetura ou política nova.

---

## 14. Verificação de coerência e exequibilidade

Confirmações antes da conclusão deste handoff:

1. ✅ Arquivo de demonstração identificado nominalmente: `config/telas/demo/demo.json`
2. ✅ A implementação pode alterar o renderer (`tela/renderizador.py`)
3. ✅ Testes focais e de integração podem ser criados em `tela/teste_renderizador.py`
4. ✅ A suíte focal pode ser executada: `python -m pytest tela/teste_renderizador.py -q`
5. ✅ A suíte canônica completa exige os seis scripts diretos — linha de base: `1803/1803`
6. ✅ A demonstração diferencia semanticamente fila (largura=110) e matriz (largura=80)
7. ✅ A demonstração inclui prova de fronteira global (`largura=20` e `largura=21` com
   configuração `demo` em arranjo vertical, classificadas como suplementares) e prova
   isolada do gatilho (`area_lancador_w=20` vs `area_lancador_w=21` com `terminal_w=80`
   constante, usando modelo em memória com arranjo horizontal)
8. ✅ O relatório de implementação pode ser criado em `docs/relatorios/`
9. ✅ Nenhum arquivo necessário está simultaneamente proibido
10. ✅ Nenhuma permissão genérica ou contraditória foi concedida
11. ✅ Nenhuma regra exclusiva da `barra_de_menus` foi transferida ao `lancador`
12. ✅ Nenhuma decisão nova foi inventada — todas as regras derivam das autoridades ativas
13. ✅ O H-0030 permanece fechado
14. ✅ O H-0033 permanece fora do escopo
15. ✅ A ADR-0023 está aprovada e aplicada; suas grandezas e regra de fallback são autoridades ativas
16. ✅ As provas automatizadas usam dimensões numéricas explícitas, sem dependência do terminal
17. ✅ As provas para smoke, pseudo-TTY e validação humana estão separadas e com papéis distintos
18. ✅ O alinhamento horizontal é preservado como propriedade da instância; demo usa "esquerda"
19. ✅ O teste isolado (T-ISOL-01/T-ISOL-02/T-ISOL-03) usa somente `ModeloTela`, `Corpo`,
    `ElementoCorpo` e `renderizar_tela` — todos em `tela/teste_renderizador.py`, sem
    arquivo de configuração novo
20. ✅ O viewport global (`terminal_w=80`) permanece suficiente para a tela normal: o
    controle T-ISOL-02 com `area_lancador_w=21` e `terminal_w=80` produz tela normal
21. ✅ A área interna do `lancador` é controlada independentemente da largura global,
    via `corpo.arranjo="horizontal"` e `corpo.distribuicao={"modo":"fracao","valores":[N, 80-N]}`
22. ✅ Os valores 20 e 21 são comparados no mesmo domínio: `area_lancador_w` (caixa completa)
    versus `lancador_caixa_min_w=21`; nenhuma comparação mistura domínios
23. ✅ Nenhuma política de composição nova foi introduzida: `"horizontal"` e `"fracao"` já
    existem e estão documentados; o modelo sintético usa somente semânticas suportadas
24. ✅ Não restaram afirmações de que `renderizar_tela(modelo_demo, largura=20, altura=30)`
    isola o gatilho interno do `lancador`: a seção 9.5.1 e o YAML de classificação
    declaram explicitamente `isola_gatilho_interno_do_lancador: false`

---

## 15. Condições de bloqueio (não atingidas)

As autoridades ativas definem com precisão suficiente:
- a fronteira entre fila e matriz (seção 3.4);
- a ordem e a largura das colunas (seções 3.4 e 3.5);
- os parâmetros de vão (seção 3.2, via `config/elementos/lancador.json`);
- a configuração demonstrativa (seção 4);
- o comportamento abaixo do mínimo de coluna (ADR-0023, seção 3.4 deste handoff).

Nenhuma condição de `ARCHITECTURE_REVIEW_REQUIRED` ou `BLOCKED_EVIDENCE`
foi atingida.

---

## Saída final

```text
etapa: PATCH_HANDOFF
status: concluido
handoff: H-0034
arquivo_corrigido: docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
arquivos_alterados: somente o handoff listado acima
configuracao_demonstrativa: config/telas/demo/demo.json (lancador_principal, 7 itens)
ponto_de_entrada: demo/demo.py
escopo_futura_implementacao:
  - tela/renderizador.py
  - tela/teste_renderizador.py
  - docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
suite_focal: "python -m pytest tela/teste_renderizador.py -q — linha de base focal anterior: 217 passed"
suite_canonica: "6 scripts diretos — linha de base: 1803/1803, 6/6 códigos de saída zero"
verificacao_coerencia: todos os 24 pontos confirmados
bloqueios: nenhum
git: handoff corrigido (nao rastreado); nenhum outro arquivo alterado
```
