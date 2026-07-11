---
name: H-0024-distribuicao-vertical-percentual-fracao-corpo
description: Handoff de implementação — distribuição da altura útil do corpo entre seus elementos quando corpo.arranjo é vertical, aplicando os modos percentual e por fração de corpo.distribuicao e executando a divisão igual normativa (modo igual e ausência de distribuicao) conforme ADR-0015 (arranjo/distribuição por container, modos, arredondamento por maiores restos, preenchimento de área alocada), preservando o arranjo horizontal e o redimensionamento reativo H-0023
metadata:
  type: handoff
  status: proposto
  data: 2026-07-11
rastreabilidade:
  adr_base: docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
  adrs_preservadas:
    - docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
    - docs/adr/ADR-0017-redimensionamento-reativo-tui.md
  contratos_aplicaveis:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/NOMENCLATURA.md
  levantamento_base: docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
  escopo_permitido:
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
  relatorio_implementacao_esperado: docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
---

# H-0024 — Distribuição vertical da altura do corpo: modos percentual e por fração

## 1. Identificação e objetivo

Implementar a **distribuição da altura útil do corpo entre seus elementos**
quando `corpo.arranjo = "vertical"`, aplicando os modos de distribuição
`percentual` e `fracao` declarados em `corpo.distribuicao` e executando a
**divisão igual normativa** quando `modo = "igual"` ou quando `distribuicao`
está ausente (ausência ≡ `igual`), conforme a autoridade normativa ADR-0015 e os
contratos ativos.

**Capacidade coesa (indivisível):**

> Distribuir a altura útil do corpo entre seus elementos quando o arranjo for
> vertical, aplicando os modos percentual e por fração definidos pelas
> autoridades e executando corretamente a semântica normativa de divisão igual
> (modo `igual` e ausência de `distribuicao`), preservando a composição existente
> e o redimensionamento reativo já aprovado.

Este handoff **não** implementa código, **não** faz QA de si mesmo, **não**
decide arquitetura nova, **não** completa lacunas normativas e **não** prepara
commit. Ele é uma ordem de trabalho fechada para o executor de implementação.

## 2. Estado comprovado

### 2.1 Estado do repositório na criação deste handoff

```text
branch: master
HEAD:   3332773a3f10e716115a164148af323fa86e608f
mensagem: feat: implementa redimensionamento reativo da TUI
último ciclo fechado: H-0023 / ADR-0017 (relatório IMP-0024)
stage: vazio
stash: stash@{0}: On master: pre-H-0022 (preservado)

Arquivos não rastreados antes deste handoff:
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md

Último handoff numérico: H-0023 → próximo livre: H-0024
Último relatório de implementação numérico: IMP-0024 → próximo livre: IMP-0025
```

### 2.2 Estado esperado no início da implementação

O estado da seção 2.1 acrescido deste arquivo de handoff como arquivo novo não
rastreado:

```text
  ?? docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
```

O stage permanece vazio. O worktree contém o relatório de levantamento e este
handoff como não rastreados — não está limpo, e isso é esperado.

O relatório de levantamento
`docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`
**não deve ser alterado** por este ciclo.

### 2.3 Condição de bloqueio por estado

Se, no início da implementação, o HEAD, a branch, o stash ou o conjunto de
arquivos divergirem de forma relevante do estado descrito em 2.1/2.2, o executor
deve parar e registrar `BLOCKED_REPOSITORY_STATE` no relatório, sem implementar.

## 3. Autoridades

Em ordem decrescente de precedência (a ordem geral do processo prevalece — ver
seção 4):

1. **`docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`** —
   autoridade primária. Define: arranjo por container (Decisão 4), distribuição
   por container (Decisão 5), modos `igual`/`percentual`/`fracao` (Decisão 6),
   quantidade de valores (Decisão 7), arredondamento determinístico por maiores
   restos (Decisão 8), contato entre molduras no eixo vertical (Decisão 9),
   preenchimento de área alocada (Decisão 10), paginação dentro da área (Decisão
   12).
2. **`docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`** — fixa
   `vertical`/`horizontal` como valores finais de `corpo.arranjo`; `sobreposto`/
   `lado_a_lado` são aliases transicionais.
3. **`docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`** — define o
   corpo entre cabeçalho e barra e a distinção entre `corpo.arranjo = "vertical"`
   (composição) e ocupação vertical do terminal (preenchimento H-0015).
4. **`docs/adr/ADR-0017-redimensionamento-reativo-tui.md`** — política de
   obtenção/atualização de dimensões e de recálculo de áreas em nova dimensão
   válida, preservada integralmente.
5. **`docs/contratos/contrato_composicao_corpo.md`** — seções 4.8 (arranjo por
   container), 4.9 (distribuição por container e regra de quantidade), 5.7
   (modos), 5.8 (arredondamento), 5.9 (preenchimento de área alocada), 5.11
   (paginação dentro da área) e regras R-17, R-18, R-19, R-22, R-23, R-24.
6. **`docs/contratos/contrato_tela_json.md`** — seção 8 (`corpo` e
   `distribuicao` por container), seção 24 (redimensionamento reativo,
   referência documental).
7. **`docs/contratos/contrato_json_tela_minima.md`** — seções 5.1, 6.2 e 6.3
   (`corpo.arranjo` opcional; `distribuicao` opcional; ausência equivale a
   `igual`).
8. **`docs/NOMENCLATURA.md`** — termos válidos de arranjo e a distinção
   obrigatória entre `corpo.arranjo = "vertical"` (composição) e ocupação
   vertical do terminal.

Nenhum relatório (incluindo o de levantamento) é fonte normativa. Relatórios e
código não criam regra.

## 4. Ordem de autoridade

1. `docs/contratos/contrato_processo_desenvolvimento.md`;
2. decisão explícita do usuário registrada neste handoff (distribuição vertical;
   modos percentual e por fração);
3. documentação normativa ativa e ADRs aplicadas (seção 3);
4. contratos ativos;
5. este handoff;
6. implementação;
7. relatórios.

Se houver conflito entre autoridades, ou se alguma semântica exigida por este
handoff não estiver definida pelas autoridades, o executor deve **parar** e
registrar `ARCHITECTURE_REVIEW_REQUIRED` no relatório, sem implementar e sem
criar ou corrigir ADR/contrato.

## 5. Decisão fechada e semântica normativa (reprodução das autoridades)

Toda a semântica abaixo é **reprodução** das autoridades citadas. Nada aqui é
regra nova.

### 5.1 Schema declarativo de `corpo.distribuicao`

`corpo.distribuicao` é **objeto opcional**. Sua ausência equivale ao modo `igual`
(contrato_json_tela_minima §6.3). Quando declarado, é um objeto com:

- `modo`: string. Valores normatizados: `igual` | `percentual` | `fracao`
  (ADR-0015 Decisão 6).
- `valores`: lista de números. Obrigatória para `percentual` e `fracao`. A
  contagem considera **somente filhos diretos** de `corpo.elementos[]`
  (ADR-0015 Decisão 7): cada item de `corpo.elementos[]` conta como **um** slot;
  `grupo` conta como um slot e **não** é expandido para efeito de contagem.

> O nome de campo `distribuicao.modo` é a forma canônica já usada pelo schema de
> `distribuicao` (forma canônica registrada em `barra_de_menus.distribuicao.modo`,
> NOMENCLATURA.md; e já nomeado como `distribuicao.modo = "percentual"` /
> `"fracao"` e `distribuicao.valores[]` na seção "O que fica fora de escopo" do
> H-0019). `distribuicao.valores[]` é a forma canônica registrada em ADR-0015
> Decisões 6 e 7 e no contrato §5.7. Este handoff não introduz nomes novos.

### 5.2 Modo `percentual` (ADR-0015 D6; contrato §5.7)

- `valores[]` declara percentuais explícitos;
- `len(valores) == len(corpo.elementos)` (filhos diretos);
- todos os valores positivos (`> 0`);
- soma dos valores **exatamente 100**; soma diferente de 100 é inválida.

Exemplo: `[40, 20, 40]` significa 40%, 20%, 40%.

### 5.3 Modo `fracao` (ADR-0015 D6; contrato §5.7)

- `valores[]` declara pesos relativos;
- `len(valores) == len(corpo.elementos)` (filhos diretos);
- todos os valores positivos (`> 0`);
- denominador implícito é a soma dos pesos;
- fração de cada filho é `valor_do_filho / soma_dos_valores`.

Exemplos: `[1, 1, 1]` → `1/3, 1/3, 1/3`; `[2, 1, 2]` → `2/5, 1/5, 2/5`
(equivalente a 40%, 20%, 40%).

### 5.4 Arredondamento por maiores restos (ADR-0015 D8; contrato §5.8; R-19)

Conversão de percentuais/frações para linhas inteiras pelo **método dos maiores
restos** sobre a altura útil do corpo (`l_corpo_disponivel`):

1. calcular a altura ideal real de cada filho
   (`altura_ideal_i = l_corpo_disponivel * peso_i / soma_pesos`);
2. tomar a parte inteira de cada uma;
3. somar as partes inteiras;
4. calcular o número de linhas restantes para fechar `l_corpo_disponivel`;
5. distribuir as unidades restantes aos maiores restos fracionários;
6. em empate de resto, priorizar a **ordem declarada** em `corpo.elementos[]`.

**Invariante obrigatório:** a soma das alturas alocadas é **exatamente igual** a
`l_corpo_disponivel`. Nenhuma linha perdida; nenhuma linha atribuída duas vezes.

Exemplos normativos (contrato §5.8; ADR-0015 D8):
- 68 linhas com `[1, 1, 1]` → `[23, 23, 22]`;
- 68 linhas com `[2, 1, 2]` → `[27, 14, 27]`.

### 5.5 Preenchimento de área alocada (ADR-0015 D10; contrato §5.9; R-18)

A distribuição define **área alocada**. Cada elemento preserva a altura alocada.
No eixo vertical, o preenchimento da área é feito com **linhas em branco**
(linhas internas bordeadas até a altura alocada), preservando a altura da faixa.
Conteúdo menor que a área recebe preenchimento; o elemento funcional não encolhe
abaixo da área alocada.

### 5.6 Contato entre molduras no eixo vertical (ADR-0015 D9)

- não existe linha vazia externa automática entre molduras verticais;
- a base de uma caixa pode ser seguida imediatamente pelo topo da próxima;
- linha em branco interna pertence ao elemento, não ao vão entre elementos.

### 5.7 Área útil vertical (ADR-0013; renderer atual)

A altura útil do corpo é `l_corpo_disponivel = altura − l_cabecalho − l_barra`,
exatamente como já calculado em `renderizar_tela` (linhas do cabeçalho e da
barra_de_menus **não** pertencem à área distribuível). Este handoff **reutiliza**
esse cálculo existente; não redefine a área útil.

### 5.8 Modos ativos neste ciclo e semântica de `igual`/ausência

A decisão explícita do usuário e o escopo positivo (seção 6) centram o ciclo na
**distribuição vertical** pelos modos `percentual` e `fracao`. A norma, porém, já
define a semântica de `igual` e da ausência de `distribuicao`, e esta capacidade
deve **executá-la corretamente** — não preservar o comportamento antigo. A
semântica normativa reproduzida é literalmente:

```text
ausência de corpo.distribuicao
≡ modo = "igual"
≡ divisão igual da área disponível entre os filhos diretos
```

Autoridades: ADR-0015 Decisão 6 (`igual` divide a área disponível igualmente
entre filhos diretos); `contrato_composicao_corpo.md` §5.7 (idem);
`contrato_json_tela_minima.md` §6.2/§6.3 (ausência de `distribuicao` equivale a
`igual`). Portanto:

- o **algoritmo de distribuição vertical** deste ciclo é ativado quando
  `corpo.arranjo` é vertical e `altura` é fornecida, para os modos `igual`
  (incluindo ausência de `distribuicao`), `percentual` e `fracao`;
- em `corpo.arranjo = "vertical"` com `altura` fornecida, ausência de
  `distribuicao` e `modo = "igual"` produzem o **mesmo resultado**:
  `l_corpo_disponivel` é repartido **igualmente** entre os filhos diretos (pesos
  unitários), pelo método dos maiores restos (seção 5.4), com soma exatamente
  igual a `l_corpo_disponivel`;
- `igual` **não** é modo novo, arquitetura nova nem ciclo independente: é a
  semântica normativa **já existente**, agora executada. Não há terceira política
  de compatibilidade para ausência/`igual`, e `igual` não é tratado como lacuna
  normativa;
- o comportamento anterior de **empilhamento sequencial com preenchimento
  vertical externo (H-0015)** **não** é mais o resultado de ausência/`igual` em
  corpo vertical com altura definida: ele é substituído pela divisão igual da
  área. Não deve haver retorno ao empilhamento sequencial antigo enquanto a
  `altura` estiver definida;
- **`altura is None`** (nenhuma dimensão a distribuir) é a única condição em que
  não há área útil a repartir — e vale igualmente para `igual`, `percentual` e
  `fracao`; nesse caso a distribuição não é aplicada (seção 11.5), por ausência de
  área e **não** por semântica específica de `igual`.

## 6. Escopo positivo

O executor deve, **exclusivamente** dentro dos arquivos permitidos (seção 8):

1. **Loader** — validar `corpo.distribuicao` conforme seção 11.1 e preservar o
   objeto validado no dicionário normalizado retornado por `carregar_tela`.
2. **Modelo** — preservar `corpo.distribuicao` no objeto `Corpo` conforme seção
   11.2, sem interpretação arquitetural.
3. **Distribuição** — implementar o cálculo das alturas por elemento (maiores
   restos) para os modos `igual` (incluindo ausência de `distribuicao`, com pesos
   unitários), `percentual` e `fracao` conforme seção 11.3.
4. **Renderização** — aplicar as alturas calculadas ao empilhamento vertical,
   preenchendo cada área alocada, conforme seção 11.4, sem inserir preenchimento
   vertical externo adicional quando a área é distribuída (qualquer modo,
   incluindo `igual`/ausência, com `altura` definida).
5. **Integração com redimensionamento** — garantir que o recálculo ocorra
   naturalmente a partir da altura corrente recebida por `renderizar_tela`,
   conforme seção 11.5, sem alterar a máquina de redimensionamento do H-0023.
6. **Testes** — implementar os casos obrigatórios da seção 14 em
   `tela/teste_loader.py`, `tela/teste_modelo.py` e `tela/teste_renderizador.py`.
7. **Regressão** — verificar que todas as suítes existentes continuam passando
   (seção 15), incluindo as do H-0019/H-0020/H-0021/H-0023.
8. **Relatório** — produzir `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
   conforme seção 17.

## 7. Escopo negativo

O executor **não deve**:

- alterar o comportamento do **arranjo horizontal** (`_montar_corpo_horizontal`,
  H-0019/H-0020/H-0021) — se um helper comum for extraído, o resultado do
  caminho horizontal deve permanecer idêntico;
- criar novos valores para `corpo.arranjo` (`vertical`/`horizontal` e aliases são
  finais);
- criar novos modos de distribuição além de `igual`, `percentual` e `fracao`
  (os três já normatizados em ADR-0015 Decisão 6);
- definir restrições dimensionais finais ainda não normatizadas (`minimo`,
  `preferido`, `maximo`, `restante`, `conteudo`) nem **altura mínima por
  elemento** — esses conceitos são futuros (ADR-0015 Decisão 11);
- definir sincronização entre elementos ou grupos (ADR-0015 Decisões 14/15,
  schema não fechado);
- implementar `grupo.distribuicao` ou redistribuição vertical entre múltiplos
  filhos de um `grupo`, nem alterar a restrição atual de grupo estrutural com um
  único elemento interno;
- introduzir prioridade, expansão ou encolhimento por tipo de elemento;
- alterar a taxonomia de `console`, `dashboard` ou `lancador`;
- reformular o modelo geral de composição;
- alterar contratos, ADRs, `NOMENCLATURA.md`, índices ou schemas normativos;
- alterar arquivos de configuração em `config/` (JSONs de produção) — as fixtures
  de teste devem ser construídas **em memória** (dicionário/JSON inline ou
  construção direta de `ModeloTela`);
- alterar `tela/demo.py`, `tela/teste_demo.py`, `tela/diagnostico.py` ou qualquer
  máquina de TTY, entrada, alternate screen, `SIGWINCH` ou redraw além de
  consumir a altura já fornecida a `renderizar_tela`;
- corrigir problemas não relacionados encontrados durante a implementação;
- fazer stage, commit, push ou alteração de histórico Git;
- refatorar código além do necessário para a capacidade.

## 8. Arquivos permitidos na implementação (lista fechada)

Esta lista é **exaustiva**. Nenhum outro arquivo pode ser criado ou alterado.

```text
tela/loader.py                 — ALTERAR (validação declarativa de corpo.distribuicao)
tela/modelo.py                 — ALTERAR (preservar distribuicao em Corpo)
tela/renderizador.py           — ALTERAR (cálculo + renderização da distribuição vertical)
tela/teste_loader.py           — ALTERAR (testes de carregamento/validação)
tela/teste_modelo.py           — ALTERAR (testes de preservação no modelo)
tela/teste_renderizador.py     — ALTERAR (testes de distribuição/arredondamento/renderização/resize)
docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md — CRIAR (relatório)
```

O relatório de implementação é artefato processual obrigatório; sua criação não
amplia o escopo técnico.

### 8.1 Arquivos condicionais — avaliados e **excluídos**

- `tela/demo.py` e `tela/teste_demo.py`: **excluídos**. A distribuição vertical é
  função pura de `renderizar_tela`, que já recebe `largura`/`altura` recalculadas
  pelo laço reativo do H-0023 (levantamento §7, `_resolver_conteudo` →
  `renderizar_estado` → `renderizar_tela`). A recomputação após redimensionamento
  é obtida sem tocar em `demo.py`; ela é verificada no nível de
  `tela/teste_renderizador.py` chamando `renderizar_tela` com alturas sucessivas.
  `tela/teste_demo.py` é executado apenas como **regressão** (seção 15), sem
  alteração.
- `config/telas/*.json`: **excluídos**. Nenhuma tela real declara
  `corpo.distribuicao` (levantamento §10); as fixtures ficam em memória nos
  testes.

## 9. Arquivos somente para leitura

```text
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
docs/adr/ADR-0017-redimensionamento-reativo-tui.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
docs/NOMENCLATURA.md
docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
docs/templates/TEMPLATE_RELATORIO_IMPL.md
tela/demo.py
config/telas/orquestrador.json
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/telas/stub_b.json
```

`docs/templates/TEMPLATE_RELATORIO_IMPL.md` é **somente leitura**: o executor
pode lê-lo e usá-lo como estrutura para criar o relatório de implementação
`IMP-0025` (seções 17 e 8). O executor **não** pode editar, substituir ou criar
variante do template, nem alterar qualquer outro arquivo de `docs/templates/`.

## 10. Arquivos proibidos

Qualquer arquivo não listado nas seções 8 e 9 está proibido para **alteração**.
Os arquivos da seção 9 podem ser **lidos**, mas não alterados. Em particular:

```text
docs/adr/                 — nenhuma ADR pode ser criada ou alterada
docs/contratos/           — nenhum contrato pode ser alterado
docs/NOMENCLATURA.md      — proibido
docs/INDICE.md            — proibido (não registra handoffs individualmente)
docs/templates/           — somente leitura: TEMPLATE_RELATORIO_IMPL.md pode ser lido
                            para estruturar o relatório (seção 9); nenhum arquivo de
                            docs/templates/ pode ser criado, editado, substituído ou variado
docs/handoff/             — nenhum outro handoff; este arquivo não é reescrito pelo executor
docs/relatorios/          — apenas IMP-0025 pode ser criado; o relatório de levantamento é imutável
config/                   — nenhum JSON de configuração de produção
tela/demo.py              — proibido alterar
tela/teste_demo.py        — proibido alterar (apenas executar como regressão)
tela/diagnostico.py       — proibido
Git hooks, ambiente, dependências externas — proibidos
```

Não há lista aberta de "outros arquivos necessários". Se um arquivo
indispensável não previsto aqui for identificado, o executor deve **parar** e
registrar `BLOCKED_EVIDENCE` no relatório, em vez de ampliar o escopo.

## 11. Especificação por camada

### 11.1 Loader (`tela/loader.py`)

**Campos reconhecidos:** `corpo.distribuicao` (objeto), com `distribuicao.modo`
(string) e `distribuicao.valores` (lista de números).

**Compatibilidade:** `corpo.distribuicao` é **opcional**. Sua ausência é válida e
deve preservar o comportamento atual (nenhum erro; nenhuma distribuição). Todas as
configurações existentes (que não declaram `corpo.distribuicao`) continuam
carregando exatamente como hoje.

**Validações obrigatórias quando `corpo.distribuicao` está presente:**

1. `corpo.distribuicao` deve ser objeto (`dict`); caso contrário, erro de
   estrutura.
2. `distribuicao.modo` obrigatório e ∈ `{"igual", "percentual", "fracao"}`; valor
   desconhecido ou ausente é erro.
3. Para `modo ∈ {"percentual", "fracao"}`:
   - `distribuicao.valores` obrigatório e deve ser lista;
   - `len(valores) == len(corpo.elementos)` (filhos diretos; `grupo` conta como um
     slot);
   - todos os `valores` numéricos e estritamente positivos (`> 0`);
   - para `percentual`: `sum(valores) == 100` exatamente; soma diferente de 100 é
     erro.
4. Para `modo == "igual"`: `valores` não é exigido; a ausência de `valores` é
   válida (os pesos são unitários no cálculo — seções 5.8 e 11.3).

**Erros esperados:** rejeição determinística, **sem fallback silencioso** (R-22).
As exceções devem seguir o padrão existente do loader — reutilizar
`TelaEstruturaInvalida` (usada hoje para `corpo.arranjo` inválido) com mensagem
descritiva que identifique o campo e o motivo (ex.: modo inválido; quantidade de
valores diferente do número de filhos diretos; valor não positivo; soma de
percentuais diferente de 100). Não criar taxonomia de exceção que contrarie o
padrão atual.

**Retorno normalizado:** o dicionário `corpo` retornado por `carregar_tela` deve
incluir `distribuicao` (o objeto validado) quando presente, e não incluí-lo (ou
incluí-lo como `None`) quando ausente. Nenhum outro campo do retorno muda.

### 11.2 Modelo (`tela/modelo.py`)

**Dados preservados:** o `dataclass` `Corpo` deve passar a preservar
`distribuicao` (objeto validado do loader ou `None`).

**Tipo e invariante:** `distribuicao` é `None` ou um `dict` com `modo` (e
`valores` quando `modo ∈ {percentual, fracao}`). O modelo **não** calcula alturas,
**não** interpreta a distribuição e **não** valida de novo — apenas transporta o
dado já validado pelo loader.

**Compatibilidade:** a construção de `Corpo` deve manter todos os objetos e
comportamentos existentes; o novo campo tem default que preserva telas sem
`distribuicao` (por exemplo, `distribuicao=None`).

### 11.3 Distribuição de espaço (`tela/renderizador.py`)

Implementar o cálculo das alturas por elemento para `modo ∈ {igual, percentual,
fracao}` (a ausência de `corpo.distribuicao` é tratada como `igual`):

- **Entrada:** `l_corpo_disponivel` (altura útil já calculada em `renderizar_tela`),
  a lista de filhos diretos `corpo.elementos[]` e `corpo.distribuicao`.
- **Elementos participantes:** cada item de `corpo.elementos[]` é um slot na ordem
  declarada; `grupo` conta como um slot (não é expandido para a contagem).
- **Pesos:** `igual` (e ausência de `distribuicao`) → pesos **unitários** (`1`
  para cada filho direto), equivalente a `fracao` com `[1, 1, …, 1]`; `percentual`
  → `valores`; `fracao` → `valores` (como pesos). O denominador é `sum(pesos)`
  (para `igual`, o número de filhos; para `percentual`, 100; para `fracao`, a soma
  dos pesos).
- **Cálculo:** método dos maiores restos (seção 5.4), produzindo uma lista de
  alturas inteiras cuja soma é **exatamente** `l_corpo_disponivel`, com empates
  resolvidos pela ordem declarada.
- **Invariantes matemáticos exigidos:** `sum(alturas) == l_corpo_disponivel`;
  cada altura resultante `>= 0`; nenhuma linha perdida ou duplicada; determinismo
  total (mesma entrada → mesma saída).

Este cálculo deve viver em função dedicada e testável isoladamente (por exemplo,
uma função interna que receba `l_corpo_disponivel`, `modo`, `valores` e retorne a
lista de alturas). A extração de qualquer lógica comum com o caminho horizontal é
permitida **somente** se o comportamento do caminho horizontal permanecer
byte-a-byte idêntico (verificado pelas suítes de regressão H-0019/H-0020/H-0021).

### 11.4 Renderização (`tela/renderizador.py`)

- **Consumo das alturas:** cada elemento é renderizado dentro da sua altura
  alocada. `_caixa` **já** aceita `altura_alvo`; o executor deve propagar
  `altura_alvo` por `_caixa_de_elemento` (adicionar parâmetro opcional
  `altura_alvo=None`, repassado a `_caixa`), preservando todas as chamadas atuais
  (default `None` mantém o comportamento vigente).
- **Preenchimento da área:** cada caixa preenche sua altura alocada com linhas
  internas bordeadas até `altura_alvo`, como já faz `_caixa` (mesmo mecanismo
  usado no caminho horizontal H-0021). Preserva bordas e o espaçamento interno
  universal (R-10).
- **Empilhamento:** as caixas são concatenadas na ordem declarada, sem linha
  vazia externa automática entre molduras (ADR-0015 D9).
- **`grupo`:** um `grupo` conta como um slot e recebe uma altura alocada; essa
  altura é aplicada ao seu único elemento funcional interno (comportamento atual
  de expansão de grupo estrutural com um filho). Grupos com múltiplos filhos ou
  aninhados permanecem fora de escopo.
- **Ausência de preenchimento externo duplicado:** com a distribuição vertical
  ativa — qualquer modo (`igual`/ausência, `percentual` ou `fracao`) desde que a
  `altura` esteja definida —, a soma das alturas alocadas já ocupa todo o
  `l_corpo_disponivel`; o preenchimento vertical externo H-0015 (linhas físicas
  após o último elemento) **não** deve ser inserido. Deve haver guarda explícita
  análoga à guarda A-003 já presente no modo horizontal. O fill externo H-0015 no
  caminho vertical permanece aplicável **apenas** quando não há área a distribuir
  (`altura is None`, seção 11.5); com `altura` definida, a área é integralmente
  repartida entre os filhos e o empilhamento sequencial antigo **não** retorna.
- **Preservação de áreas não pertencentes ao corpo:** cabeçalho, barra_de_menus e
  moldura permanecem inalterados; a distribuição não invade nem altera essas
  regiões (a área distribuível é exatamente `l_corpo_disponivel`).
- **Conteúdo que excede a área alocada:** este handoff **não** define altura
  mínima por elemento nem nova política de overflow. Se o conteúdo natural de um
  elemento exceder sua altura alocada, o comportamento é o já existente: `_caixa`
  não trunca, e a verificação já presente em `renderizar_tela`
  (`l_corpo_conteudo > l_corpo_disponivel → RenderizadorErro` determinístico)
  permanece a política aplicável. Nenhuma paginação nova é introduzida (paginação
  dentro da área é conceito futuro — ADR-0015 D12).

### 11.5 Integração com o redimensionamento (H-0023)

- **Recálculo a partir da altura atual:** a distribuição é função pura da
  `altura` recebida por `renderizar_tela`. O laço reativo do H-0023 já re-invoca
  `renderizar_tela` com o novo par válido de dimensões (R-24); portanto o
  recálculo das alturas ocorre automaticamente a cada nova altura, sem cache.
- **Ausência de cache dimensional obsoleto:** nenhuma altura calculada pode ser
  memoizada entre chamadas; cada render recomputa a partir da `altura` corrente.
- **Preservação do redraw e da máquina de sessão:** nenhuma alteração em
  `demo.py`, no wakeup pipe, no handler de `SIGWINCH`, no alternate screen ou no
  redraw. A composição declarativa não é alterada pelo redimensionamento (R-23).
- **`altura is None`:** quando `renderizar_tela` é chamada sem `altura` (ex.: uso
  sem dimensão explícita), não há área útil a distribuir; isso vale igualmente
  para todos os modos (`igual`/ausência, `percentual`, `fracao`). Nessa condição
  o empilhamento sequencial é preservado **apenas por ausência de área definida**
  (não por semântica específica de `igual`) e a distribuição não é aplicada. Isso
  deve ser registrado explicitamente e coberto por teste.

## 12. Itens verificáveis exigidos

O executor deve deixar demonstrável, por teste ou diff:

1. como a área útil vertical é identificada (`l_corpo_disponivel`);
2. quais linhas não pertencem à área distribuível (cabeçalho e barra);
3. como os elementos participantes são identificados (filhos diretos; grupo = 1
   slot);
4. como o modo é carregado (loader) e representado (modelo `Corpo.distribuicao`);
5. como os valores são validados (seção 11.1);
6. como a altura de cada elemento é calculada (maiores restos);
7. como arredondamento e linhas residuais são tratados (invariante de soma);
8. como cada elemento é renderizado dentro da área atribuída (`altura_alvo`);
9. como a redistribuição ocorre após mudança de altura (função pura recomputada);
10. quais comportamentos atuais são preservados (seção 13).

## 13. Preservações obrigatórias

- compatibilidade de **carregamento** com todas as configurações válidas atuais
  (sem `corpo.distribuicao`): continuam carregando sem erro. Em corpo vertical com
  `altura` definida, passam a ser renderizadas por **divisão igual** (`igual` ≡
  ausência), conforme a norma — não há garantia de resultado visual byte-a-byte
  idêntico ao empilhamento antigo, que era não normativo;
- comportamento do arranjo **horizontal** (H-0019/H-0020/H-0021) byte-a-byte;
- comportamento do arranjo **vertical sem área a distribuir** (`altura is None`):
  empilhamento sequencial + preenchimento vertical externo H-0015 preservados
  **apenas** nessa condição;
- taxonomia ativa (`console`, `dashboard`, `lancador`, `grupo` estrutural);
- bordas, cabeçalho, barra_de_menus e moldura;
- composição declarada de `console`, `dashboard` e `lancador`;
- redimensionamento reativo aprovado no H-0023 (SIGWINCH, redraw, restauração de
  terminal, entrada TTY);
- todos os testes anteriormente aprovados não relacionados à nova capacidade;
- stash preservado `stash@{0}: On master: pre-H-0022`.

## 14. Casos obrigatórios de teste

Testes construídos com fixtures **em memória** (dicionário/JSON inline ou
construção direta de `ModeloTela`), sem alterar `config/`.

### 14.1 Carregamento e modelo (`teste_loader.py`, `teste_modelo.py`)

- corpo vertical válido com `distribuicao.modo = "percentual"` e `valores`
  válidos carrega e preserva `distribuicao`;
- corpo vertical válido com `distribuicao.modo = "fracao"` e `valores` válidos
  carrega e preserva `distribuicao`;
- `distribuicao` ausente permanece válida e não altera o carregamento
  (compatibilidade);
- `modo` desconhecido é rejeitado;
- `valores` com `len != len(elementos)` é rejeitado (percentual e fração);
- valor zero e valor negativo são rejeitados (percentual e fração);
- soma de percentuais diferente de 100 é rejeitada;
- `modo = "igual"` sem `valores` é aceito como schema válido;
- o objeto `Corpo` preserva `distribuicao` (percentual, fração e `None`);
- as mensagens/tipos de erro são compatíveis com o padrão existente do loader.

### 14.2 Distribuição vertical (`teste_renderizador.py`)

- dois elementos; três ou mais elementos;
- altura útil divisível exatamente entre os pesos;
- altura útil com linhas residuais (arredondamento);
- área útil menor (terminal menor) e maior (terminal maior);
- soma das alturas alocadas igual a `l_corpo_disponivel` (invariante);
- ausência de linha perdida ou atribuída duas vezes;
- caso-limite de área mínima em que a distribuição ainda cabe; abaixo dele, o
  `RenderizadorErro` determinístico existente por altura insuficiente é levantado
  (sem definir altura mínima por elemento).

### 14.3 Modo `igual` e ausência de `distribuicao` (`teste_renderizador.py`)

- `distribuicao` **ausente** em corpo vertical produz **divisão igual** de
  `l_corpo_disponivel` entre os filhos diretos (pesos unitários), **não** o
  empilhamento sequencial antigo;
- `modo = "igual"` **explícito** produz a mesma divisão igual;
- **equivalência:** para a mesma altura e os mesmos filhos, ausência de
  `distribuicao` e `modo = "igual"` produzem alturas **idênticas**;
- dois filhos diretos; três ou mais filhos diretos;
- divisão exata (altura múltipla do número de filhos, ex.: 66 linhas com 3 filhos
  → `[22, 22, 22]`);
- divisão com linhas residuais pela regra dos maiores restos (ex.: 68 linhas com
  3 filhos → `[23, 23, 22]`, empate resolvido pela ordem declarada);
- soma das alturas alocadas **exatamente igual** à área distribuível
  `l_corpo_disponivel`;
- **ausência de retorno ao empilhamento sequencial antigo** quando a `altura`
  está definida (o `l_corpo_disponivel` inteiro é repartido entre as áreas);
- regressão: `percentual` e `fracao` continuam produzindo suas distribuições
  normativas inalteradas.

### 14.4 Percentual (`teste_renderizador.py`)

- divisão uniforme (ex.: `[50, 50]`); divisão não uniforme (ex.: `[40, 20, 40]`);
- arredondamento e linha residual (ex.: 68 linhas com `[40, 20, 40]` → `[27, 14,
  27]`);
- rejeições normativas (soma ≠ 100, valor não positivo, contagem incorreta) —
  cobertas no loader (14.1).

### 14.5 Fração (`teste_renderizador.py`)

- pesos iguais (`[1, 1, 1]` → `[23, 23, 22]` em 68 linhas);
- pesos diferentes (`[2, 1, 2]` → `[27, 14, 27]` em 68 linhas);
- mais de dois elementos; arredondamento e linha residual;
- empate de resto resolvido pela ordem declarada;
- rejeições normativas cobertas no loader (14.1).

### 14.6 Renderização (`teste_renderizador.py`)

- cada elemento limitado/preenchido à altura atribuída;
- área alocada preenchida com linhas internas bordeadas;
- bordas preservadas; molduras verticais em contato sem linha vazia externa;
- ausência de sobra vertical externa quando a distribuição está ativa (o
  `l_corpo_disponivel` inteiro é ocupado pelas áreas);
- ausência de invasão do cabeçalho, da barra_de_menus e da moldura;
- caminho vertical **sem área a distribuir** (`altura is None`) continua
  produzindo o preenchimento externo H-0015 (não regressão).

### 14.7 Redimensionamento (`teste_renderizador.py`)

- ampliação: `renderizar_tela` com altura maior recomputa as alturas alocadas;
- redução: altura menor recomputa;
- múltiplas mudanças sucessivas: sequência de alturas produz, a cada altura, a
  distribuição correta e determinística;
- recomputação de percentuais, de frações e da divisão igual (`igual`/ausência)
  verificada para pelo menos duas alturas distintas;
- `altura is None`: distribuição não é aplicada; empilhamento preservado apenas
  por ausência de área definida.

### 14.8 Regressão

- os testes do H-0019/H-0020/H-0021 (arranjo/preenchimento horizontal) passam sem
  alteração;
- os testes de altura explícita e preenchimento vertical externo H-0015 passam;
- os testes de `barra_de_menus.distribuicao` (independentes de
  `corpo.distribuicao`) passam.

## 15. Suítes e verificações locais

Comandos reais das suítes afetadas (executar todas):

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
```

Justificativa de inclusão:
- `teste_loader.py`, `teste_modelo.py`, `teste_renderizador.py`: suítes
  diretamente afetadas pela nova capacidade;
- `teste_demo.py`: executada como **regressão** para comprovar que a máquina de
  redimensionamento/sessão (H-0023) permanece intacta, mesmo sem alteração em
  `demo.py`.

Verificações Git locais do executor (não constituem QA formal):

```bash
git diff --check
git status --short
```

## 16. Validação manual

Distinção obrigatória a registrar no relatório:

1. **Testes automatizados** — cobrem o cálculo, a validação, o arredondamento, a
   renderização e a recomputação por altura (seções 14–15).
2. **Pseudo-TTY** — não aplicável a este ciclo: a capacidade é função pura de
   `renderizar_tela` e não altera a máquina de sessão; a integração reativa já é
   coberta pelas suítes de `demo` do H-0023 (executadas como regressão).
3. **Validação humana em TTY real** — a capacidade introduz comportamento visual
   novo (áreas verticais distribuídas por percentual/fração ocupando toda a altura
   do corpo). O executor deve **registrar como pendente para o QA** a verificação
   visual em terminal real de: (a) distribuição percentual e por fração em corpo
   vertical com 2+ elementos ocupando integralmente a altura útil; (b) ausência de
   sobra/rasgo entre molduras; (c) recomputação correta ao redimensionar o
   terminal. O implementador **não** pode declarar validação humana concluída sem
   evidência do usuário.

## 17. Relatório de implementação esperado

Caminho exato e não conflitante (próximo identificador livre confirmado):

```text
docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
```

Usar `docs/templates/TEMPLATE_RELATORIO_IMPL.md` (arquivo **somente leitura** da
seção 9) como estrutura; não editá-lo nem criar variante. O relatório deve
registrar, no mínimo:

- identificação do handoff (H-0024);
- autoridades usadas;
- arquivos alterados;
- comportamento implementado;
- validações declarativas do loader;
- algoritmo de distribuição aplicado conforme a norma (maiores restos);
- tratamento de arredondamento e resíduos (invariante de soma);
- integração com o redimensionamento;
- testes executados e resultado de cada suíte;
- verificações Git (`git diff --check`, `git status --short`);
- validações manuais ainda pendentes (TTY real);
- limitações e itens fora de escopo (ex.: `grupo.distribuicao`; mínimos por
  elemento; modos dimensionais futuros `restante`/`conteudo`);
- bloqueios, se houver;
- divergências entre handoff e repositório, se encontradas.

## 18. Critérios de aceite

| Critério | Evidência esperada |
|---|---|
| `corpo.distribuicao` percentual válido é carregado e preservado | Teste de loader/modelo |
| `corpo.distribuicao` fração válido é carregado e preservado | Teste de loader/modelo |
| `distribuicao` ausente preserva o carregamento atual | Teste de loader |
| `distribuicao` ausente e `modo = igual` produzem divisão igual da área | Testes de renderizador |
| Ausência e `igual` produzem alturas idênticas (equivalência) | Teste de renderizador |
| Modo/valores inválidos são rejeitados sem fallback silencioso | Testes de loader |
| Alturas por elemento calculadas por maiores restos, soma = `l_corpo_disponivel` | Testes de renderizador |
| Exemplos normativos `[1,1,1]`/`[2,1,2]` em 68 linhas conferem | Testes de renderizador |
| Cada elemento preenche sua área alocada; bordas preservadas | Testes de renderizador |
| Distribuição ativa (qualquer modo, altura definida) suprime o fill externo H-0015 no vertical | Teste de renderizador |
| Corpo vertical não retorna ao empilhamento sequencial antigo com altura definida | Teste de renderizador |
| Caminho vertical sem área a distribuir (`altura is None`) preserva o fill externo H-0015 | Teste de não regressão |
| Arranjo horizontal permanece idêntico | Suítes H-0019/H-0020/H-0021 |
| Recomputação correta para alturas sucessivas | Testes de renderizador |
| Máquina de redimensionamento/sessão H-0023 intacta | `teste_demo.py` (regressão) |
| `altura is None` não aplica distribuição | Teste de renderizador |

## 19. Condições de bloqueio

O executor deve **parar**, não implementar, e registrar a condição adequada
quando:

- o estado Git divergir do estado comprovado (2.1/2.2) → `BLOCKED_REPOSITORY_STATE`;
- alguma semântica exigida não estiver definida pelas autoridades, ou ADR e
  contrato divergirem → `ARCHITECTURE_REVIEW_REQUIRED`;
- a capacidade exigir definir restrição dimensional pendente (mínimo/preferido/
  máximo/altura mínima por elemento) ou sincronização futura →
  `ARCHITECTURE_REVIEW_REQUIRED`;
- o tratamento de arredondamento ou resíduos não puder ser aplicado conforme a
  norma → `ARCHITECTURE_REVIEW_REQUIRED`;
- um arquivo indispensável não previsto nas seções 8/9 for necessário →
  `BLOCKED_EVIDENCE`;
- a capacidade exigir alteração documental (ADR/contrato/nomenclatura/schema)
  antes da implementação → `ARCHITECTURE_REVIEW_REQUIRED`.

O executor **não** cria ADR e **não** corrige documentação normativa.
