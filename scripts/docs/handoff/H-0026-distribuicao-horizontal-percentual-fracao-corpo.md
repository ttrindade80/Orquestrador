---
name: H-0026-distribuicao-horizontal-percentual-fracao-corpo
description: Handoff de implementacao — distribuicao horizontal explicita da largura util do corpo entre filhos diretos quando corpo.arranjo = horizontal, modos percentual e fracao, algoritmo de maiores restos; loader e modelo ja aceitam e preservam corpo.distribuicao; somente renderizador e testes precisam ser alterados
metadata:
  type: handoff
  status: proposto
  data: 2026-07-11
rastreabilidade:
  adrs_base:
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
  contratos_aplicaveis:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
  levantamento_base: docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
  handoff_precedente: docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
  relatorio_precedente: docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
  escopo_alteravel:
    - tela/renderizador.py
    - tela/teste_renderizador.py
    - docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
  escopo_somente_leitura:
    - tela/loader.py
    - tela/modelo.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
  relatorio_implementacao_esperado: docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
---

# H-0026 — Distribuição horizontal explícita do corpo (percentual e fração)

## 1. Identificação e status

| Campo | Valor |
|---|---|
| Identificador | H-0026 |
| Status | proposto |
| Data | 2026-07-11 |
| Ciclo anterior fechado | H-0025 / ADR-0018 |
| Relatório precedente | IMP-0026 |
| Relatório esperado | IMP-0027 |

Este handoff **não** implementa código, **não** faz QA de si mesmo, **não** decide
arquitetura nova, **não** completa lacunas normativas e **não** prepara commit. É uma
ordem de trabalho fechada para o executor de implementação.

---

## 2. Contexto do ciclo

O H-0025 entregou a distribuição vertical explícita da altura útil do corpo entre seus
filhos diretos nos modos `igual`, `percentual` e `fracao` (relatório IMP-0026). O ciclo
H-0025 excluiu explicitamente o arranjo horizontal.

O levantamento `RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md`
(status `L1_HORIZONTAL_DOCUMENTADO_HANDOFF_POSSIVEL`) comprovou que:

- a semântica normativa horizontal está fechada nas autoridades ativas;
- não é necessária nova ADR;
- o loader já aceita e valida `corpo.distribuicao` nos modos `percentual` e `fracao`
  quando `corpo.arranjo = "horizontal"`;
- o modelo já preserva `corpo.distribuicao` como `dict | None`;
- o renderizador ignora a distribuição declarada no arranjo horizontal e calcula
  larguras uniformes;
- faltam: cálculo de larguras por distribuição declarada no renderizador e testes
  positivos correspondentes.

---

## 3. Capacidade única deste ciclo

> Quando `corpo.distribuicao` estiver declarado com `modo: "percentual"` ou
> `modo: "fracao"` em container com `corpo.arranjo = "horizontal"`, calcular e alocar
> as larguras dos filhos diretos proporcionalmente aos valores declarados, aplicando o
> algoritmo de maiores restos, com soma exata da largura distribuível e preservação de
> todas as propriedades visuais horizontais já aprovadas.
>
> Quando `corpo.distribuicao` estiver ausente, o comportamento horizontal existente
> (particionamento uniforme, H-0019/H-0020/H-0021) é preservado sem alteração.

---

## 4. Estado comprovado do repositório

### 4.1 Referência Git

```text
branch:  master
commit:  1cc0dff feat: implementa distribuicao vertical explicita do corpo
stage:   vazio
alteracoes rastreadas: nenhuma
nao rastreados:
  - docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
  - docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
  - docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md
  - tela/__pycache__/
```

### 4.2 Verificação obrigatória no início da implementação

O executor deve executar antes de qualquer alteração:

```bash
git branch --show-current
git log -1 --oneline
git status --short
git diff --stat
git diff --cached --stat
```

Se o estado divergir, parar com `BLOCKED_REPOSITORY_STATE`.

Arquivos não rastreados esperados: `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md`,
`docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md`,
`docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md` e `tela/__pycache__/`. A presença desses
arquivos não rastreados corresponde ao estado esperado do ciclo e não é divergência.
Qualquer alteração rastreada não esperada é divergência relevante.

---

## 5. Decisão do usuário

O usuário decidiu tratar primeiro a distribuição fracionada/percentual no arranjo
horizontal do corpo raiz e fechar essa capacidade antes de trabalhar nos demais
arranjos e níveis de composição.

Este ciclo abrange exclusivamente `corpo.arranjo = "horizontal"` quando
`corpo.distribuicao.modo` for `"percentual"` ou `"fracao"`. Grupos horizontais,
distribuição vertical e outros arranjos estão fora de escopo.

---

## 6. Autoridades normativas obrigatórias

O executor deve ler as seções aplicáveis antes de implementar:

### 6.1 Autoridade primária para distribuição por container

**`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`**

- Decisão 4 (arranjo por container): `arranjo = horizontal` reparte largura entre
  filhos diretos — linhas 107–119.
- Decisão 5 (distribuição por container): container horizontal reparte colunas/largura
  — linhas 122–132.
- Decisão 6 (modos `percentual` e `fracao`) — linhas 142–163.
- Decisão 7 (quantidade de valores igual à de filhos diretos) — linhas 171–185.
- Decisão 8 (maiores restos) — linhas 189–209.
- Decisão 9 (contato horizontal, sem vão externo) — linhas 213–228.
- Decisão 10 (preenchimento de área alocada) — linhas 238–246.

### 6.2 Autoridade sobre ausência e semântica genérica dos modos

**`docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`**

- D1 (distinção arranjo × distribuição) — linha 107.
- D2 (ausência preserva construção orientada pelo conteúdo) — linhas 115–126.
- D5 (`igual` é modo explícito, não fallback) — linhas 154–158.
- D6 (`percentual` genérico) — linhas 162–169.
- D7 (`fracao` genérico, qualquer vetor válido) — linhas 173–193.
- Relação com ADR-0015 (preservação dos modos, pesos, maiores restos) — linhas 420–433.

### 6.3 Contratos ativos

**`docs/contratos/contrato_composicao_corpo.md`**

- Regra R-17: sem `distribuicao`, arranjo organiza filhos por conteúdo; com
  `distribuicao`, reparte largura no horizontal — linhas 836–844.
- Regra R-19: conversão a células inteiras por maiores restos — linhas 851–855.
- Distribuição por container horizontal reparte colunas/largura — linhas 290–299.
- Cardinalidade: `len(distribuicao.valores) == len(elementos)` — linhas 312–319.
- Modo `percentual` — linhas 558–566.
- Modo `fracao` — linhas 568–583.
- Arredondamento e maiores restos — linhas 618–638.
- Contato horizontal sem vão externo — linhas 514–527.
- Preenchimento horizontal por espaços — linhas 642–659.

**`docs/contratos/contrato_tela_json.md`**

- `corpo` e `grupo` podem declarar `distribuicao`; modos `igual`, `percentual`,
  `fracao` — linhas 200–206.

**`docs/contratos/contrato_json_tela_minima.md`**

- `distribuicao` opcional; modos explícitos — linhas 214–230.

### 6.4 Referências históricas e de formato (sem autoridade superior)

Somente para referência de formato e histórico, sem autoridade normativa:

- `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md`
- `docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md`

---

## 7. Dependências

### 7.1 Dependências satisfeitas

- ADR-0015: aceita, vigente.
- ADR-0018: registrada como aceita no índice; cadeia de QA aprovada conforme
  `docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0025.md:91–107`.
- H-0025: fechado e implementado (IMP-0026).
- Levantamento: status `L1_HORIZONTAL_DOCUMENTADO_HANDOFF_POSSIVEL`.

### 7.2 Dependências não satisfeitas neste ciclo

- Grupos horizontais: barragem no loader (`tela/loader.py:227–251`) não é removida
  neste ciclo.
- Composição em três níveis: fora de escopo.

---

## 8. Leitura obrigatória da futura implementação

O executor deve ler integralmente antes de qualquer alteração:

1. `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md`
   (levantamento base; status `L1_HORIZONTAL_DOCUMENTADO_HANDOFF_POSSIVEL`)
2. `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
3. `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
4. `docs/contratos/contrato_composicao_corpo.md` (seções relevantes §6.3)
5. `tela/renderizador.py` (integralmente, com atenção especial às seções §11)
6. `tela/teste_renderizador.py` (seção H-0025 e testes horizontais existentes)

---

## 9. Arquivos permitidos na implementação

### 9.1 Arquivos alteráveis (lista fechada)

```text
tela/renderizador.py
tela/teste_renderizador.py
docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
```

O executor **não** deve alterar nenhum arquivo fora desta lista.

Se durante a implementação for identificado que outro arquivo é indispensável,
registrar a evidência no relatório IMP-0027 e parar com `BLOCKED_EVIDENCE`,
acompanhado de:

- por que a implementação não pode ser feita com o código atual;
- qual requisito normativo exige a alteração;
- qual trecho exato será afetado;
- quais regressões devem ser testadas.

Não autorizar alteração preventiva.

### 9.2 Arquivos somente leitura

```text
tela/loader.py
tela/modelo.py
tela/teste_loader.py
tela/teste_modelo.py
```

O loader e o modelo são **suficientes como estão** (evidência no levantamento,
seções 12.1 e 12.2). O loader aceita e valida `corpo.distribuicao` independentemente
do eixo. O modelo preserva `distribuicao` como `dict | None`. Nenhuma alteração é
autorizada sem necessidade concreta demonstrada durante a implementação.

---

## 10. Arquivos proibidos nesta implementação

Todos os demais arquivos, incluindo sem limitação:

```text
docs/adr/
docs/contratos/
docs/NOMENCLATURA.md
docs/handoff/
config/telas/
tela/demo.py
tela/teste_demo.py
```

Não alterar contratos, ADRs, nomenclatura, JSONs declarativos de telas, nem
arquivos de demonstração neste ciclo.

---

## 11. Comportamento atual comprovado

### 11.1 Loader (`tela/loader.py`)

- Aceita `corpo.arranjo = "horizontal"` e aliases — linhas 33–37, 434–441.
- Valida `corpo.distribuicao` sempre que o campo existe em `corpo`,
  independentemente de `arranjo` — linhas 443–448.
- Modos aceitos: `igual`, `percentual`, `fracao` — linhas 39–42, 178–183.
- Valida quantidade igual aos filhos diretos — linhas 197–203.
- Valida valores numéricos não booleanos e estritamente positivos — linhas 143–145,
  205–210.
- Valida soma percentual igual a 100 — linhas 212–216.
- **Rejeita** grupo com `arranjo` horizontal como fora de escopo/não implementado —
  linhas 227–251.

### 11.2 Modelo (`tela/modelo.py`)

- Preserva `distribuicao` como `dict | None` — linhas 57–70.
- `construir_modelo` copia `corpo_raw.get("distribuicao")` sem conversão —
  linhas 271–275.
- Ausência de `corpo.distribuicao` resulta em `modelo.corpo.distribuicao is None`.

### 11.3 Renderizador — helpers existentes (`tela/renderizador.py`)

- `_pesos_distribuicao(distribuicao, n_filhos)` — linhas 203–216: devolve a lista de
  pesos a partir do dict de distribuição; suporta `igual`, `percentual` e `fracao`;
  genérico, sem hardcode de vetor.

- `_distribuir_alturas(altura_disponivel, pesos)` — linhas 219–254: aplica maiores
  restos no eixo vertical; contém o algoritmo normativo completo (soma exata,
  desempate por ordem declarada). **Este helper é reutilizável para colunas**, pois
  o algoritmo de maiores restos é idêntico para qualquer eixo.

### 11.4 Renderizador — ramo horizontal atual (`tela/renderizador.py`)

- `_montar_corpo_horizontal(elementos, borda, total_w, altura_disponivel=None)` —
  linhas 756–853: particionamento horizontal contíguo; calcula **uniformemente**
  `base_w = total_w // N` e `resto = total_w % N`, ignorando qualquer `distribuicao`
  declarada — linhas 778–782. O docstring descreve isso como "Distribuição uniforme
  implícita".

- Ramo de despacho principal — linhas 969–994: detecta `arranjo_corpo == "horizontal"`,
  calcula `_l_corpo_disponivel` e chama `_montar_corpo_horizontal`; **não passa
  `distribuicao_corpo`** para a função.

- A variável `distribuicao_corpo = modelo.corpo.distribuicao` existe no escopo
  (linha 966), mas é usada apenas no ramo vertical (linhas 995–1040).

### 11.5 Teste existente de horizontal com distribuição declarada

`tela/teste_renderizador.py`, função
`test_arranjo_horizontal_nao_regride_com_distribuicao` — linhas 3763–3795.

Este teste declara `distribuicao={"modo": "fracao", "valores": [1, 1]}` em arranjo
horizontal, mas **verifica apenas que não há erro e que o particionamento contíguo
permanece**. O comentário da função registra explicitamente que H-0025 não
implementou distribuição horizontal. Este teste precisará ser atualizado neste ciclo.

---

## 12. Comportamento esperado após implementação

### 12.1 Com `corpo.distribuicao` declarado em horizontal

Quando `corpo.arranjo = "horizontal"` **e** `corpo.distribuicao` estiver declarado
com `modo: "percentual"` ou `modo: "fracao"`:

- calcular os pesos a partir de `distribuicao` usando o helper `_pesos_distribuicao`
  existente;
- converter pesos para larguras inteiras pelo algoritmo de maiores restos;
- usar essas larguras para alocar cada filho direto do corpo;
- garantir que a soma das larguras seja exatamente `total_w` (largura interna
  distribuível);
- preservar o particionamento contíguo (bordas coladas, sem vão externo);
- preservar bordas, margens e largura total da moldura;
- preservar o preenchimento horizontal por espaços nas áreas alocadas.

### 12.2 Sem `corpo.distribuicao` (ausência)

Quando `corpo.distribuicao` estiver ausente (`None`):

- preservar integralmente o comportamento atual de particionamento uniforme
  (`base_w = total_w // N`, `resto = total_w % N`) — linhas 778–782;
- não criar distribuição implícita;
- não converter ausência em modo `igual`.

O caminho sem distribuição **não é redefinido como nova norma arquitetural** neste
ciclo; é preservado como comportamento operacional existente.

---

## 13. Especificação por módulo

### 13.1 Loader

**Classificação: somente leitura.**

O loader já aceita e valida `corpo.distribuicao` nos modos aplicáveis para
`corpo.arranjo = "horizontal"` (levantamento §12.1). A validação não é condicionada
ao eixo. Nenhuma alteração é necessária ou autorizada neste ciclo.

Validações já existentes que permanecem válidas:

- objeto obrigatório quando declarado — `tela/loader.py:171–176`;
- `valores` como lista para `percentual`/`fracao` — `tela/loader.py:190–195`;
- quantidade igual aos filhos diretos — `tela/loader.py:197–203`;
- valores numéricos positivos não booleanos — `tela/loader.py:205–210`;
- soma percentual igual a 100 — `tela/loader.py:212–216`.

### 13.2 Modelo

**Classificação: somente leitura.**

O modelo já preserva `corpo.distribuicao` como `dict | None` sem conversão
(`tela/modelo.py:271–275`). Nenhuma alteração é necessária ou autorizada.

### 13.3 Renderizador

**Classificação: arquivo principal de alteração.**

#### 13.3.1 Ponto de intervenção obrigatório

O executor deve intervir no ramo de despacho principal do arranjo horizontal,
localizado em `tela/renderizador.py:969–994`.

Atualmente o ramo chama `_montar_corpo_horizontal` **sem considerar**
`distribuicao_corpo`. A implementação deve:

1. verificar se `distribuicao_corpo` (já disponível na variável da linha 966) está
   presente (`is not None`) antes de chamar `_montar_corpo_horizontal`;
2. quando presente, calcular os pesos via `_pesos_distribuicao(distribuicao_corpo,
   len(modelo.corpo.elementos))` (helper existente, linha 203);
3. calcular larguras inteiras pelo algoritmo de maiores restos aplicado à largura
   distribuível `total_w`;
4. usar essas larguras em vez do particionamento uniforme atual;
5. quando ausente, manter o comportamento uniforme integralmente.

#### 13.3.2 Reutilização do algoritmo existente

O algoritmo de maiores restos implementado em `_distribuir_alturas`
(`tela/renderizador.py:219–254`) é **idêntico** ao necessário para larguras: recebe
a dimensão disponível e uma lista de pesos, devolve cotas inteiras com soma exata e
desempate por ordem declarada.

O executor pode:

- criar um novo helper `_distribuir_larguras` análogo a `_distribuir_alturas`,
  reutilizando a mesma lógica; ou
- extrair o algoritmo comum para um helper genérico de cotas se isso for local ao
  cálculo de cotas e não introduzir arquitetura nova; ou
- modificar `_montar_corpo_horizontal` para aceitar `larguras` explícitas como
  parâmetro opcional, calculadas externamente.

Qualquer extração ou generalização deve:

- permanecer local ao cálculo de cotas no módulo `renderizador.py`;
- reutilizar a mesma regra normativa de maiores restos;
- não alterar o comportamento vertical aprovado;
- não introduzir arquitetura nova;
- ser coberta por testes.

O executor não deve impor refatoração ampla. A intervenção mínima é suficiente.

#### 13.3.3 Comportamentos que devem permanecer inalterados

- Particionamento uniforme quando `distribuicao_corpo is None` — linhas 778–782.
- Concatenação horizontal sem separador externo — linhas 843–853.
- Preenchimento vertical das colunas com `altura_disponivel` — linhas 824–841.
- Verificação de largura mínima por área — linhas 785–793.
- Toda lógica de altura disponível horizontal (`_l_corpo_disponivel`) — linhas
  974–991.
- Ramo vertical com distribuição explícita — linhas 995–1040.

---

## 14. Algoritmo normativo de cotas

### 14.1 Modo `percentual`

- Um valor por filho direto do `corpo.elementos[]`.
- Todos os valores positivos; soma exatamente 100.
- Largura ideal real de cada filho: `total_w * valor_i / 100`.
- Conversão por maiores restos para colunas inteiras.
- Soma final das cotas inteiras exatamente igual a `total_w`.
- Empates de resto resolvidos por ordem declarada (menor índice prevalece).

### 14.2 Modo `fracao`

- Um peso positivo por filho direto do `corpo.elementos[]`.
- Denominador implícito: `soma_dos_pesos = sum(valores)`.
- Largura ideal real de cada filho: `total_w * peso_i / soma_dos_pesos`.
- Conversão por maiores restos para colunas inteiras.
- Soma final das cotas inteiras exatamente igual a `total_w`.
- Empates de resto resolvidos por ordem declarada.

### 14.3 Algoritmo de maiores restos (normativo)

```
1. calcular largura_ideal[i] = total_w * peso[i] / soma_pesos  (real)
2. cota[i] = floor(largura_ideal[i])  (inteiro)
3. faltam = total_w - sum(cota[i])
4. ordenar índices por resto decrescente (largura_ideal[i] - cota[i]),
   desempatando por índice crescente (ordem declarada)
5. atribuir +1 aos `faltam` primeiros índices na ordem acima
6. invariante: sum(cota[i]) == total_w
```

### 14.4 Restrições normativas

- A associação dos valores aos filhos segue a **ordem declarada** em
  `corpo.elementos[]`. Valor na posição `i` corresponde ao filho na posição `i`.
- Nenhuma cota pode ser deslocada para filho diferente do que corresponde
  posicionalmente.
- Nenhuma sobra pode ser perdida fora de `total_w`.
- Nenhuma coluna pode receber colunas fora de sua cota.

### 14.5 O que este ciclo não define

- Política para conteúdo maior que a cota horizontal (fora de escopo normativo
  explícito — `docs/contratos/contrato_composicao_corpo.md:590–609`).
- Largura mínima por tipo de elemento (fora de escopo deste ciclo).
- Distribuição automática quando `corpo.distribuicao` está ausente.

---

## 15. Critérios de aceite

O QA futuro deve verificar objetivamente todos os itens abaixo:

| # | Critério |
|---|---|
| 1 | `percentual [50, 50]` em `total_w=42` gera dois filhos com larguras iguais (21 cada) |
| 2 | `percentual [60, 40]` em `total_w=42` gera larguras proporcionais (25, 17 — maiores restos) |
| 3 | `fracao [1, 1]` em `total_w=42` gera dois filhos com larguras iguais (21 cada) |
| 4 | `fracao [2, 1]` em `total_w=42` gera larguras na proporção 2:1 (28, 14) |
| 5 | `fracao [2, 1]` e `fracao [4, 2]` geram larguras idênticas (equivalência por escala) |
| 6 | Largura não divisível exatamente distribui sobra pelos maiores restos |
| 7 | Empate de restos resolvido por ordem declarada (menor índice recebe a unidade extra) |
| 8 | Soma das larguras é exatamente igual a `total_w` |
| 9 | Bordas horizontais permanecem em contato (`╮╭` visível) |
| 10 | Largura total da moldura preservada (cada linha com exatamente `total_w` chars) |
| 11 | Conteúdo menor que a cota preenchido com espaços conforme contrato |
| 12 | `corpo.distribuicao` ausente: comportamento uniforme preservado sem alteração |
| 13 | Distribuição vertical existente (H-0025) não regride |
| 14 | Teste `test_arranjo_horizontal_nao_regride_com_distribuicao` atualizado para verificar larguras reais |
| 15 | Loader e modelo não foram alterados |
| 16 | Nenhum contrato ou ADR foi alterado |
| 17 | Somente os arquivos autorizados (§9.1) foram modificados |
| 18 | Relatório IMP-0027 foi produzido |
| 19 | Não há commit |
| 20 | Grupos horizontais continuam fora de escopo (loader ainda os rejeita) |
| 21 | Nenhuma política de conteúdo maior que a cota foi introduzida |
| 22 | Soma percentual diferente de 100 continua sendo rejeitada pelo loader |
| 23 | Peso não positivo continua sendo rejeitado pelo loader |

---

## 16. Testes obrigatórios

### 16.1 Testes positivos de distribuição horizontal

Os testes a seguir devem ser adicionados em `tela/teste_renderizador.py`, na classe
ou seção correspondente ao H-0026. Cada teste deve verificar as larguras efetivas
das colunas renderizadas.

**T01 — `percentual [50, 50]` simétrico**

Fixture: 2 filhos, `modo: "percentual"`, `valores: [50, 50]`, `total_w=42`.
Verificação: cada filho ocupa exatamente 21 colunas; soma = 42; `╮╭` presente.

**T02 — `percentual` assimétrico**

Fixture: 2 filhos, `modo: "percentual"`, `valores: [60, 40]`, `total_w=42`.
Verificação: larguras são 25 e 17 (maiores restos); soma = 42.

**T03 — `fracao [1, 1]` simétrico**

Fixture: 2 filhos, `modo: "fracao"`, `valores: [1, 1]`, `total_w=42`.
Verificação: cada filho ocupa exatamente 21 colunas; soma = 42.

**T04 — `fracao [2, 1]` assimétrico**

Fixture: 2 filhos, `modo: "fracao"`, `valores: [2, 1]`, `total_w=42`.
Verificação: larguras são 28 e 14; soma = 42.

**T05 — Equivalência por escala de frações**

Fixture par 1: `valores: [2, 1]`, `total_w=42`.
Fixture par 2: `valores: [4, 2]`, `total_w=42`.
Verificação: as larguras calculadas nos dois casos são idênticas.

**T06 — Maiores restos com largura não divisível**

Fixture: 3 filhos, `modo: "fracao"`, `valores: [1, 1, 1]`, `total_w` não divisível
por 3 (ex.: `total_w=100`). Verificação: soma das larguras = 100; o primeiro filho
recebe a unidade extra (ordem declarada); resultado concreto esperado: `[34, 33, 33]`.

**T07 — Empate de restos resolvido por ordem declarada**

Fixture: 3 filhos, `modo: "fracao"`, `valores: [1, 1, 1]`, `total_w=101`.
Cotas ideais iguais (`101/3`); partes inteiras `[33, 33, 33]`; faltam 2 colunas;
restos empatados; desempate por ordem declarada; posições 0 e 1 recebem a unidade
extra; soma final = 101. Verificação: larguras `[34, 34, 33]`.

**T08 — Soma das larguras igual à largura distribuível**

Para cada fixture de distribuição declarada acima, verificar explicitamente que
`sum(larguras) == total_w`. Esta verificação pode estar embutida nos testes acima ou
ser um teste dedicado ao invariante.

**T09 — Bordas em contato com distribuição explícita**

Fixture: 2 ou 3 filhos com distribuição explícita. Verificação: `╮╭` presente na
linha de topo; `╯╰` presente na linha de base; `││` presente nas linhas internas.

**T10 — Largura total preservada com distribuição explícita**

Fixture: 2 filhos com distribuição percentual ou fracionária em `total_w=42`.
Verificação: todas as linhas da saída têm exatamente 42 caracteres.

### 16.2 Atualização do teste existente de horizontal com distribuição

**Teste a atualizar:** `test_arranjo_horizontal_nao_regride_com_distribuicao`
(`tela/teste_renderizador.py:3763–3795`).

Atualmente verifica apenas ausência de erro e particionamento contíguo, pois
H-0025 não implementou distribuição horizontal. Após este ciclo, o teste deve
verificar que a distribuição declarada **altera as larguras** conforme os valores:
com `fracao [1, 1]` em `total_w=42`, cada área deve ter exatamente 21 colunas.

O comportamento de particionamento contíguo (bordas coladas) **deve ser mantido**
na verificação.

### 16.3 Verificações de não regressão obrigatórias

**T-NR01 — Ausência de `corpo.distribuicao` preserva comportamento uniforme**

Fixture existente sem `distribuicao` declarada (ex.:
`test_arranjo_horizontal_dois_elementos`, `test_arranjo_horizontal_areas_contiguas`,
`test_arranjo_horizontal_resto_deterministico` — linhas 2370–2482).

Verificação: todos continuam passando sem alteração; o particionamento uniforme não
é afetado pela introdução dos modos explícitos.

**T-NR02 — Distribuição vertical H-0025 não regride**

A suite de testes da classe de distribuição vertical H-0025
(`tela/teste_renderizador.py:3797–3814`) deve continuar passando integralmente.

**T-NR03 — Rejeições do loader permanecem válidas**

Os testes de rejeição do loader para `percentual` e `fracao` inválidos
(`tela/teste_loader.py:826–987`) devem continuar passando. O loader não é alterado.

### 16.4 Escopo negativo de testes

Não exigir neste ciclo:

- testes de grupo horizontal;
- testes de política para conteúdo maior que a cota;
- matriz exaustiva de larguras possíveis;
- validação manual em TTY real, salvo se o executor demonstrar objetivamente sua
  necessidade para verificar o comportamento implementado.

---

## 17. Relatório de implementação esperado

O executor deve criar ao final:

```text
docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
```

Este é o próximo identificador documental disponível comprovado no repositório
(IMP-0026 é o último existente; nenhum IMP-0027 existe).

O relatório deve registrar obrigatoriamente:

- handoff executado (H-0026);
- arquivos alterados (lista com diff summary);
- comportamento implementado (modos, larguras, algoritmo);
- decisões normativas utilizadas (ADR-0015 D5–D8, ADR-0018 D6/D7);
- testes executados e resultados;
- saída dos comandos de teste;
- regressões verificadas (T-NR01, T-NR02, T-NR03);
- limitações mantidas (grupos horizontais, política de conteúdo maior que a cota);
- bloqueios encontrados, se houver;
- estado Git ao final (branch, commit, stage);
- arquivos não rastreados presentes;
- ausência de commit.

---

## 18. Condições de bloqueio

### 18.1 `ARCHITECTURE_REVIEW_REQUIRED`

Parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

- alguma regra necessária não estiver definida nas autoridades listadas em §6;
- for necessário decidir política nova não presente nos contratos;
- o comportamento de arredondamento horizontal não puder ser derivado das autoridades;
- a implementação exigir alterar a semântica de ausência de `corpo.distribuicao`;
- a implementação exigir incluir grupos horizontais como pré-requisito;
- o suporte exigir ampliar a composição hierárquica;
- houver contradição normativa não registrada pelo levantamento.

### 18.2 `BLOCKED_EVIDENCE`

Parar com `BLOCKED_EVIDENCE` se:

- algum arquivo obrigatório listado em §9.1 não for localizado no repositório;
- o próximo ID de relatório (IMP-0027) estiver ocupado;
- o estado Git divergir do descrito em §4;
- for necessário alterar arquivo fora da lista fechada de §9.1 sem justificativa
  normativa concreta;
- o algoritmo de maiores restos exigir alterar `_distribuir_alturas` de forma
  que afete o comportamento vertical.

### 18.3 `BLOCKED_REPOSITORY_STATE`

Parar com `BLOCKED_REPOSITORY_STATE` se:

- houver alteração rastreada não esperada no início da implementação;
- houver operação Git ativa (MERGE_HEAD, REBASE_HEAD, CHERRY_PICK_HEAD etc.);
- outra sessão estiver modificando o workspace.

Não resolver bloqueios dentro da implementação. Registrar a evidência e parar.

---

## 19. Proibição de commit

O executor **não** deve preparar, executar nem sugerir commit ao final da
implementação. A implementação termina com o relatório IMP-0027 criado e os testes
passando.

---

## 20. Limite de encerramento

Criado somente este arquivo de handoff. Nenhuma outra alteração foi realizada
nesta etapa.

O executor de implementação deve:

1. verificar o estado do repositório (§4.2);
2. ler as autoridades obrigatórias (§6 e §8);
3. implementar o escopo positivo em `tela/renderizador.py` (§13.3);
4. atualizar e criar testes em `tela/teste_renderizador.py` (§16);
5. executar as suites de teste e verificar regressões;
6. criar o relatório IMP-0027 (§17);
7. parar em qualquer condição de bloqueio (§18).

Não fazer QA do handoff, não alterar loader nem modelo sem necessidade comprovada,
não alterar contratos ou ADRs, não alterar JSONs declarativos de telas, não
manipular stash, não preparar commit.
