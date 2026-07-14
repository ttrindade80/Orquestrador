---
name: H-0029-distribuicao-containers-cardinalidade-unitaria
description: Handoff de implementacao — investigar e corrigir distribuicao explicita em containers hierarquicos com exatamente um filho, criar sete telas JSON permanentes de demonstracao e validacao visual, preservando ausencia de distribuicao, independencia entre niveis, cardinalidade maior que 1 e JSONs fora de escopo
metadata:
  type: handoff
  status: READY_FOR_IMPLEMENTATION
  data: 2026-07-12
  patch: PATCH_HANDOFF_TELAS_PERMANENTES_2026-07-12
rastreabilidade:
  ciclo_anterior_fechado:
    ciclo: H-0028
    commit: 921a06f
    mensagem: "feat: implementa matriz declarativa de grupos"
    testes: "1133/1133"
    validacao_manual: MANUAL_VALIDATION_APPROVED
  evidencia_base:
    - docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
  adrs_base:
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
    - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
  contratos_aplicaveis:
    - docs/contratos/contrato_composicao_corpo.md
  handoffs_precedentes:
    - docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
    - docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
    - docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
    - docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md
  relatorio_implementacao_esperado: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
---

# H-0029 — Distribuicao de containers com cardinalidade unitaria

## 1. Identificacao

| Campo | Valor |
|---|---|
| Identificador | H-0029 |
| Status | READY_FOR_IMPLEMENTATION |
| Data | 2026-07-12 |
| Ciclo anterior fechado | H-0028 |
| Commit-base declarado pelo usuario | `921a06f` |
| Relatorio esperado | `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md` |

Este handoff **nao implementa codigo**, **nao faz QA de si mesmo**, **nao decide
arquitetura nova**, **nao prepara commit** e **nao
autoriza ciclos posteriores**. Ele e uma ordem de trabalho fechada para o executor
de implementacao do H-0029.

---

## 2. Estado comprovado

O ultimo ciclo fechado informado pelo usuario e:

```yaml
ciclo: H-0028
status: FECHADO
commit: 921a06f
mensagem: "feat: implementa matriz declarativa de grupos"
testes: "1133/1133"
validacao_manual: MANUAL_VALIDATION_APPROVED
```

Estado Git observado na criacao deste handoff, a partir do diretorio
`scripts/`:

```text
?? docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
```

O relatorio de levantamento nao rastreado deve ser preservado. Ele faz parte da
evidencia documental do ciclo H-0029 e nao pode ser alterado pelo executor.

O executor deve verificar antes de qualquer alteracao:

```bash
git log -1 --oneline
git status --short
git diff --stat
git diff --check
git diff --cached --stat
```

Se houver alteracao rastreada inesperada em `tela/*.py`, `config/telas/*.json`,
`docs/adr/`, `docs/contratos/` ou `docs/handoff/`, parar com:

```text
BLOCKED_REPOSITORY_STATE
```

A presenca do relatorio de levantamento nao rastreado e esperada e nao constitui
divergencia.

---

## 3. Evidencia inicial

O executor deve ler integralmente:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
```

Esse levantamento comprovou:

- ausencia de `corpo.distribuicao` preserva altura natural;
- distribuicao explicita permite que um container utilize a altura disponivel;
- `modo: "igual"` com um filho equivale matematicamente a peso unico;
- suporte geral de distribuicao ja existe no loader, modelo e renderer;
- `orquestrador.json` utiliza distribuicao explicita;
- `destino_minimo.json`, `stub_b.json` e `grupo_minimo.json` nao declaravam
  distribuicao no estado restaurado.

Observacao funcional apresentada pelo usuario, ainda a isolar por testes:

- tela com um unico `dashboard` ocupa corretamente a area quando recebe
  distribuicao explicita no corpo;
- grupo com mais de um elemento distribui corretamente;
- grupo com apenas um elemento nao distribuiu corretamente;
- distribuir o corpo raiz e deixar o grupo com cardinalidade unitaria produziu
  renderizacao incorreta;
- distribuir somente o grupo nao fez a tela raiz ocupar toda a area;
- `modo: "fracao"` com um filho e `valores: [1]` deve atribuir 100% da area ao
  filho.

Essas observacoes sao evidencias de reproducao, nao diagnostico causal. O executor
nao pode presumir antecipadamente qual funcao contem o defeito.

---

## 4. Autoridades

O executor deve ler integralmente antes de implementar:

| Documento | Uso no H-0029 |
|---|---|
| `docs/contratos/contrato_composicao_corpo.md` | autoridade ativa de composicao, grupo, distribuicao, modos, arredondamento, ausencia e matriz |
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | arvore do corpo, grupo, distribuicao por container, maiores restos, preenchimento de area |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | ausencia de distribuicao nao equivale a `igual`; distribuicao explicita aloca area |
| `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | profundidade por grupos e multiplicidade de filhos funcionais |
| `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` | preservacao de `estrutura: livre` e independencia de distribuicoes matriciais |
| `docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md` | precedente de distribuicao vertical explicita |
| `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md` | precedente de distribuicao horizontal explicita |
| `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` | precedente de grupos hierarquicos recursivos |
| `docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md` | precedente de matriz e preservacao do comportamento `livre` |

Arquivos de configuracao que devem ser lidos:

```text
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/telas/stub_b.json
```

Arquivos de codigo e testes que devem ser lidos nos trechos relevantes:

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Nao ler relatorios historicos indiscriminadamente. Relatorios historicos sao
evidencia apenas quando este handoff os nomeia explicitamente.

---

## 5. Decisao fechada do ciclo

O H-0029 corrigira erros relacionados a distribuicao de containers hierarquicos
com cardinalidade unitaria.

Quando um container recebe area disponivel e declara distribuicao explicita:

- `modo: "igual"` com um filho atribui 100% da area distribuivel ao filho;
- `modo: "fracao"` com `valores: [1]` atribui 100% da area distribuivel ao filho;
- `modo: "percentual"` com `valores: [100]` atribui 100% da area distribuivel
  ao filho, pois o contrato ativo define um valor positivo por filho direto e
  soma exatamente 100;
- o resultado nao depende de existir mais de um filho;
- a distribuicao de um container atua somente sobre seus filhos diretos;
- nao ha propagacao implicita entre ancestrais e descendentes.

Alem da correcao do defeito, o H-0029 deve produzir sete telas JSON permanentes
que permitam demonstrar e validar visualmente todos os cenarios de cardinalidade
unitaria pelo pipeline real do demo.py.

---

## 6. Semantica obrigatoria a preservar

### 6.1 Ausencia de distribuicao

Se um container nao declara `distribuicao`:

- filhos permanecem em tamanho natural;
- nao surge distribuicao implicita;
- nao se materializa `modo: "igual"` como default;
- um descendente distribuido nao expande automaticamente o ancestral;
- a sobra pode permanecer como preenchimento externo conforme o comportamento
  ja existente.

### 6.2 Distribuicao explicita

Se um container declara `distribuicao` e recebe area:

- a soma das cotas atribuidas corresponde exatamente a area distribuivel;
- um unico filho recebe toda a area distribuivel;
- preenchimento, moldura e bordas permanecem dentro da cota atribuida;
- nao surgem lacunas externas indevidas;
- nao ha sobreposicao, perda de borda ou deslocamento da `barra_de_menus`.

### 6.3 Independencia entre niveis

Cada `distribuicao` atua somente sobre os filhos diretos do container em que foi
declarada.

```text
corpo.distribuicao
```

controla somente os filhos diretos do corpo.

```text
corpo.elementos[i].distribuicao
```

controla somente os filhos diretos daquele grupo.

E proibida qualquer propagacao implicita de distribuicao entre niveis.

---

## 7. Investigacao obrigatoria

Antes de aplicar qualquer correcao, o executor deve rastrear e registrar no
relatorio:

- geracao dos pesos para cardinalidade `1`;
- calculo das cotas por `_distribuir_alturas` e `_distribuir_larguras`;
- passagem de `altura_disponivel` no corpo raiz e nos grupos;
- passagem de `altura_alvo` ate `_caixa_de_elemento` e `_caixa`;
- passagem de largura/cotas no caminho horizontal;
- criacao da caixa do grupo estrutural via `_renderizar_container`;
- calculo da area interna apos bordas;
- preenchimento interno;
- composicao de grupos aninhados;
- condicoes especiais baseadas em `len(elementos)`;
- diferencas entre elemento funcional e grupo;
- diferencas entre container raiz e grupo aninhado;
- caminhos vertical e horizontal;
- interacao com `estrutura: matriz`, apenas para garantir preservacao e nao para
  ampliar o escopo.

O executor deve identificar o caminho causal no codigo antes de alterar a
implementacao.

---

## 8. Escopo positivo

Este handoff autoriza exclusivamente:

- reproducao automatizada do defeito;
- correcao do tratamento de cardinalidade unitaria em containers com
  distribuicao explicita;
- preservacao de cardinalidade maior que `1`;
- preservacao da ausencia de distribuicao;
- preservacao da independencia entre niveis;
- cobertura de containers verticais;
- cobertura de containers horizontais caso o mesmo caminho de codigo seja
  afetado;
- cobertura de composicoes em dois ou mais niveis com cardinalidade unitaria;
- cobertura de terminais com mais de uma dimensao util;
- comportamento deterministico em area insuficiente, sem criar nova politica
  normativa;
- criacao dos sete arquivos JSON de tela permanentes `h0029_*` definidos
  nominalmente na secao 11A;
- testes de integracao nominais que carregam cada um dos sete JSONs `h0029_*`
  pelo loader real, constroem o modelo e verificam a geometria relevante;
- inspecao da interface real de `tela/demo.py` e documentacao dos comandos
  exatos para abertura de cada tela no relatorio;
- relatorio factual de implementacao com sequencia de comandos de validacao
  visual para o usuario.

Cenarios obrigatorios:

1. container raiz do corpo com um unico elemento funcional;
2. corpo raiz com um unico grupo;
3. grupo com um unico elemento funcional;
4. composicao em dois ou mais niveis com cardinalidade unitaria;
5. `modo: "igual"` com um filho;
6. `modo: "fracao"` com `valores: [1]`;
7. `modo: "percentual"` com `valores: [100]`;
8. containers verticais;
9. containers horizontais, se o caminho de codigo afetado for comum;
10. preservacao do comportamento correto com dois ou mais filhos;
11. preservacao da semantica de ausencia de distribuicao;
12. terminais com mais de uma dimensao util;
13. area insuficiente com resultado deterministico ou erro deterministico ja
    autorizado pelas regras existentes;
14. tela `h0029_dashboard_igual` — corpo com `modo: "igual"`, um dashboard;
15. tela `h0029_dashboard_fracao` — corpo com `modo: "fracao"`, `valores: [1]`,
    um dashboard;
16. tela `h0029_dashboard_percentual` — corpo com `modo: "percentual"`,
    `valores: [100]`, um dashboard;
17. tela `h0029_grupo_pai_distribuido` — corpo com `fracao [1]`, um grupo sem
    distribuicao propria com um dashboard;
18. tela `h0029_grupo_igual` — corpo com `igual`, grupo com `igual`, um
    dashboard;
19. tela `h0029_grupo_fracao` — corpo com `fracao [1]`, grupo com `fracao [1]`,
    um dashboard;
20. tela `h0029_grupo_percentual` — corpo com `percentual [100]`, grupo com
    `percentual [100]`, um dashboard.

---

## 9. Escopo negativo

Ficam explicitamente fora do H-0029:

- tela 2x2;
- tela 3x2;
- tela 2x4;
- nova tela de console unico;
- nova tela de dashboard unico integrada ao lancador;
- inclusao das telas `h0029_*` no lancador do orquestrador;
- navegacao do console;
- selecao no console;
- execucao de acoes;
- carregamento de conteudo de JSON de testes;
- nova politica de altura minima, overflow, truncamento, paginacao, scroll ou
  degradacao;
- propagacao implicita de distribuicao entre niveis;
- alteracao de `orquestrador.json`;
- alteracao de contratos, ADRs, nomenclatura ou indices documentais;
- refatoracao ampla sem vinculo direto com a causa encontrada;
- catalogo geral de telas permanentes;
- console unico permanente fora das fixtures H-0029;
- commit ou alteracao de historico Git.

E proibido criar telas permanentes alem das sete `h0029_*` autorizadas
nominalmente na secao 11A. Permanecem proibidos: alteracao de funcionalidades
do console, navegacao, selecao ou execucao de acoes.

Se a correcao exigir qualquer mudanca normativa, parar com:

```text
ARCHITECTURE_REVIEW_REQUIRED
```

---

## 10. Arquivos autorizados

Lista fechada de arquivos que o executor pode alterar ou criar, se a investigacao
confirmar necessidade:

```text
tela/renderizador.py
tela/teste_renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
config/telas/h0029_dashboard_igual.json
config/telas/h0029_dashboard_fracao.json
config/telas/h0029_dashboard_percentual.json
config/telas/h0029_grupo_pai_distribuido.json
config/telas/h0029_grupo_igual.json
config/telas/h0029_grupo_fracao.json
config/telas/h0029_grupo_percentual.json
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
```

Restricoes:

- `tela/renderizador.py` e autorizado para a correcao ja identificada do defeito
  de cardinalidade unitaria. Se a validacao das telas `h0029_*` revelar
  necessidade de correcao adicional, o executor a implementa dentro do mesmo
  escopo sem nova aprovacao. Se a causa exigir mudanca normativa, parar com
  `ARCHITECTURE_REVIEW_REQUIRED`.

- Alteracoes em `tela/loader.py` ou `tela/modelo.py` **nao estao pre-autorizadas**.
  Esses arquivos ja aceitam e preservam distribuicao declarada; se a causa tecnica
  exigir alteracao neles, o executor deve registrar a evidencia e parar com:

  ```text
  ARCHITECTURE_REVIEW_REQUIRED
  ```

- `config/telas/grupo_minimo.json` **nao pode ser alterado**. Ele deve permanecer
  com seu conteudo original durante todo o H-0029. Pode ser lido como referencia
  estrutural, usado como entrada de testes de preservacao, comparado com os novos
  arquivos e utilizado como evidencia do comportamento historico. Nao pode receber
  distribuicao experimental nem ser usado como fixture modificavel.

- Os sete JSONs `h0029_*` devem ser construidos a partir dos JSONs ativos
  `destino_minimo.json` (para dashboards diretos) e `grupo_minimo.json` (para
  grupos com dashboard) como modelos de referencia. Nao inventar campos. Nao criar
  semantica nova. Nao alterar os arquivos usados como referencia.

---

## 11. Arquivos proibidos

E proibido alterar:

```text
docs/adr/
docs/contratos/
docs/NOMENCLATURA.md
docs/INDICE.md
docs/adr/INDICE_ADR.md
docs/handoff/
docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md
config/telas/orquestrador.json
config/telas/destino_minimo.json
config/telas/stub_b.json
config/telas/grupo_minimo.json
tela/demo.py
tela/diagnostico.py
tela/explorar_barra_de_menus.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_explorar_barra_de_menus.py
```

Excecoes:

- `config/telas/h0029_*.json`: os sete arquivos autorizados nominalmente na
  secao 11A estao fora desta proibicao; eles sao criados, nao alterados.

Os arquivos `config/telas/grupo_minimo.json`, `config/telas/destino_minimo.json`,
`config/telas/stub_b.json` e `config/telas/orquestrador.json` sao de referencia
preservada. Podem ser usados somente como referencia estrutural, entrada de testes
de preservacao, comparacao com os novos arquivos ou evidencia do comportamento
historico. Nao podem ser alterados, nao podem receber distribuicao experimental e
nao podem ser usados como fixtures modificaveis durante o H-0029.

Tambem e proibido criar telas permanentes alem das sete `h0029_*` autorizadas
na secao 11A, incluir telas no lancador, alterar o lanzador, adicionar navegacao,
selecao ou execucao de acoes.

---

## 11A. Telas permanentes autorizadas

Esta secao define nominalmente os sete arquivos JSON permanentes autorizados.
O executor deve construi-los a partir dos JSONs de referencia existentes
(`destino_minimo.json` e `grupo_minimo.json`), sem inventar campos nem criar
semantica nova. Os arquivos de referencia sao de leitura exclusiva e nao podem
ser alterados durante o H-0029.

Cada tela deve conter:

- `schema`: `"tela.v1"`;
- `id`: correspondente ao nome do arquivo sem a extensao `.json`;
- `cabecalho` com `titulo` e `descricao` que identifiquem claramente o cenario;
- `corpo` com exatamente a estrutura descrita;
- `barra_de_menus` valida, copiada de `destino_minimo.json` ou `grupo_minimo.json`.

### 11A.1 `h0029_dashboard_igual.json`

**Identificador:** `h0029_dashboard_igual`

**Estrutura do corpo:**

```text
corpo (arranjo: vertical, distribuicao: {modo: "igual"})
└── dashboard
```

**Distribuicao do corpo:**

```json
{
  "modo": "igual"
}
```

**Resultado esperado:** o dashboard unico ocupa toda a area disponivel entre o
cabecalho e a `barra_de_menus`. A altura total da tela e igual a `altura`
fornecida. Nao ha lacuna externa nem sobreposicao.

---

### 11A.2 `h0029_dashboard_fracao.json`

**Identificador:** `h0029_dashboard_fracao`

**Estrutura do corpo:**

```text
corpo (arranjo: vertical, distribuicao: {modo: "fracao", valores: [1]})
└── dashboard
```

**Distribuicao do corpo:**

```json
{
  "modo": "fracao",
  "valores": [1]
}
```

**Resultado esperado:** geometricamente equivalente a `h0029_dashboard_igual`.

---

### 11A.3 `h0029_dashboard_percentual.json`

**Identificador:** `h0029_dashboard_percentual`

**Estrutura do corpo:**

```text
corpo (arranjo: vertical, distribuicao: {modo: "percentual", valores: [100]})
└── dashboard
```

**Distribuicao do corpo:**

```json
{
  "modo": "percentual",
  "valores": [100]
}
```

**Resultado esperado:** geometricamente equivalente a `h0029_dashboard_igual`
e `h0029_dashboard_fracao`.

---

### 11A.4 `h0029_grupo_pai_distribuido.json`

**Identificador:** `h0029_grupo_pai_distribuido`

**Estrutura do corpo:**

```text
corpo (arranjo: vertical, distribuicao: {modo: "fracao", valores: [1]})
└── grupo (arranjo: vertical, sem distribuicao propria)
    └── dashboard
```

**Distribuicao do corpo:**

```json
{
  "modo": "fracao",
  "valores": [1]
}
```

**O grupo nao deve declarar distribuicao interna.**

**Resultado esperado:**

- o grupo recebe toda a cota do corpo (`fracao [1]`);
- o dashboard permanece em altura natural dentro do grupo;
- a sobra pertence a area estrutural do grupo;
- a tela mantem a altura total correta;
- a `barra_de_menus` permanece na posicao correta;
- nao ha sobreposicao nem desaparecimento de linhas.

Este e o cenario que reproduz diretamente o caminho corrigido no renderer.

---

### 11A.5 `h0029_grupo_igual.json`

**Identificador:** `h0029_grupo_igual`

**Estrutura do corpo:**

```text
corpo (arranjo: vertical, distribuicao: {modo: "igual"})
└── grupo (arranjo: vertical, distribuicao: {modo: "igual"})
    └── dashboard
```

**Resultado esperado:**

- o grupo ocupa toda a area do corpo;
- o dashboard ocupa toda a area interna distribuivel do grupo;
- a borda inferior do dashboard fica imediatamente antes da `barra_de_menus`;
- altura total da tela igual a `altura` fornecida.

---

### 11A.6 `h0029_grupo_fracao.json`

**Identificador:** `h0029_grupo_fracao`

**Estrutura do corpo:**

```text
corpo (arranjo: vertical, distribuicao: {modo: "fracao", valores: [1]})
└── grupo (arranjo: vertical, distribuicao: {modo: "fracao", valores: [1]})
    └── dashboard
```

**Resultado esperado:** geometricamente equivalente a `h0029_grupo_igual`.

---

### 11A.7 `h0029_grupo_percentual.json`

**Identificador:** `h0029_grupo_percentual`

**Estrutura do corpo:**

```text
corpo (arranjo: vertical, distribuicao: {modo: "percentual", valores: [100]})
└── grupo (arranjo: vertical, distribuicao: {modo: "percentual", valores: [100]})
    └── dashboard
```

**Resultado esperado:** geometricamente equivalente a `h0029_grupo_igual` e
`h0029_grupo_fracao`.

---

## 12. Matriz minima de testes automatizados

### 12.1 Cenarios de distribuicao (testes sinteticos e de integracao existentes)

O executor deve adicionar testes focais equivalentes aos cenarios abaixo, sem
depender apenas de inspecao visual:

| Distribuicao do corpo | Filho do corpo | Distribuicao do grupo | Filhos do grupo | Resultado esperado |
|---|---|---|---:|---|
| ausente | elemento funcional | n/a | - | altura natural preservada |
| `igual` | elemento funcional | n/a | - | filho recebe toda a area do corpo |
| `fracao [1]` | elemento funcional | n/a | - | equivalente geometricamente a `igual` |
| `percentual [100]` | elemento funcional | n/a | - | equivalente geometricamente a `igual` |
| `igual` | grupo | ausente | 1 | grupo recebe toda a cota do corpo; filho interno permanece natural |
| `fracao [1]` | grupo | ausente | 1 | mesmo comportamento geometrico do caso anterior |
| ausente | grupo | `igual` | 1 | grupo raiz permanece natural; distribuicao atua apenas internamente |
| ausente | grupo | `fracao [1]` | 1 | equivalente ao caso interno `igual` |
| ausente | grupo | `percentual [100]` | 1 | equivalente ao caso interno `igual` |
| `igual` | grupo | `igual` | 1 | grupo ocupa o corpo e o unico filho ocupa toda a area interna distribuivel |
| `fracao [1]` | grupo | `fracao [1]` | 1 | distribuicao integral nos dois niveis |
| `percentual [100]` | grupo | `percentual [100]` | 1 | distribuicao integral nos dois niveis |
| `igual` | grupo | `igual` ou `fracao` | 2 ou mais | comportamento existente preservado |

Os testes da secao 12.1 devem verificar objetivamente:

- quantidade total de linhas produzidas;
- largura das linhas;
- altura util calculada para o corpo;
- altura recebida pelo unico filho;
- equivalencia geometrica entre `igual`, `fracao [1]` e `percentual [100]`;
- soma exata das cotas;
- posicao da borda inferior;
- posicao da `barra_de_menus`;
- ausencia de linhas externas indevidas;
- ausencia de lacunas;
- ausencia de sobreposicao;
- preservacao de bordas;
- comportamento em pelo menos duas alturas de terminal;
- preservacao dos casos com dois ou mais filhos;
- preservacao da ausencia de distribuicao;
- rejeicao deterministica apenas quando a area for realmente insuficiente.

### 12.2 Testes nominais dos sete JSONs permanentes

Para cada um dos sete JSONs `h0029_*`, os testes devem verificar, carregando
o arquivo real pelo loader:

- JSON sintaticamente valido;
- carregamento pelo loader sem excecao;
- construcao do modelo sem excecao;
- quantidade correta de filhos diretos do corpo (deve ser 1);
- modo e valores da distribuicao do corpo conforme declarado;
- quando aplicavel, modo e valores da distribuicao do grupo;
- renderizacao com largura e altura fixas sem excecao;
- altura total da tela igual a `altura` fornecida;
- largura uniforme de todas as linhas nao vazias;
- posicao da `barra_de_menus` imediatamente apos a area do corpo;
- posicao da borda inferior do dashboard nos cenarios em que ele deve preencher
  a area distribuida (telas 11A.1-11A.3 e 11A.5-11A.7);
- preservacao da altura natural do dashboard nos cenarios de grupo sem
  distribuicao propria (tela 11A.4);
- ausencia de sobreposicao;
- ausencia de lacunas externas indevidas;
- equivalencia geometrica entre `h0029_dashboard_igual`,
  `h0029_dashboard_fracao` e `h0029_dashboard_percentual`;
- equivalencia geometrica entre `h0029_grupo_igual`, `h0029_grupo_fracao` e
  `h0029_grupo_percentual`.

Os testes devem falhar caso a geometria visivel esperada nao seja produzida.
Nao basta verificar somente a quantidade total de linhas.

---

## 13. Estrategia de testes

O executor deve separar:

1. testes unitarios com estruturas sinteticas, isolando calculo e renderer;
2. testes de integracao loader -> modelo -> renderer usando ao menos um JSON real
   existente e usando nominalmente cada um dos sete JSONs `h0029_*` como descrito
   na secao 12.2;
3. regressao da suite canonica do projeto;
4. leitura focal de `grupo_minimo.json` como referencia para identificar o
   defeito, sem alterar o arquivo;
5. pseudo-TTY, se necessario para reproduzir dimensoes;
6. validacao humana em TTY real, obrigatoria conforme a secao 16B.

O executor de implementacao nao pode declarar aprovacao visual. O relatorio deve
registrar:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

---

## 14. Verificacoes obrigatorias

Antes de emitir o relatorio, o executor deve executar a suite canonica do projeto.
A referencia do ciclo anterior e `1133/1133`; qualquer diferenca deve ser
explicada factualmente.

Tambem deve executar testes focais suficientes para demonstrar:

- reproducao automatizada do defeito antes da correcao;
- identificacao do caminho causal;
- correcao sem criar distribuicao implicita;
- cardinalidade `1` funcionando nos modos explicitos permitidos;
- equivalencia entre `igual`, `fracao [1]` e `percentual [100]`;
- preservacao de cardinalidade maior que `1`;
- preservacao da independencia entre niveis;
- preservacao dos JSONs e comportamentos fora do escopo;
- ausencia de alteracao em `orquestrador.json`, `destino_minimo.json` e
  `stub_b.json`;
- carregamento bem-sucedido de cada um dos sete JSONs `h0029_*` pelo loader;
- construcao de modelo sem excecao para cada JSON `h0029_*`;
- geometria esperada para cada um dos sete JSONs `h0029_*`;
- equivalencia geometrica entre os tres modos de dashboard e entre os tres
  modos de grupo.

---

## 15. Criterios de aceite

O H-0029 so pode ser reportado como implementado se todos os criterios abaixo
forem verdadeiros:

1. ha teste automatizado que reproduz o defeito de cardinalidade unitaria;
2. o relatorio identifica o caminho causal no codigo;
3. a correcao nao cria distribuicao implicita;
4. `igual` com um filho ocupa 100% da area distribuivel;
5. `fracao [1]` com um filho ocupa 100% da area distribuivel;
6. `percentual [100]` com um filho ocupa 100% da area distribuivel;
7. `igual`, `fracao [1]` e `percentual [100]` sao geometricamente equivalentes
   em cardinalidade unitaria;
8. cardinalidade maior que `1` permanece correta;
9. distribuicao do corpo nao altera implicitamente distribuicao de grupo;
10. distribuicao de grupo nao expande implicitamente o corpo ancestral;
11. containers verticais passam nos cenarios obrigatorios;
12. containers horizontais passam ou o relatorio justifica por que o caminho
    horizontal nao foi afetado;
13. a posicao da `barra_de_menus` permanece correta;
14. nao ha lacunas externas indevidas nem sobreposicao;
15. a suite canonica passa integralmente;
16. o relatorio de implementacao e factual e lista arquivos alterados;
17. validacao manual e marcada como pendente quando depender de TTY real;
18. os sete JSONs permanentes `h0029_*` existem no repositorio, com os
    identificadores corretos;
19. todos os sete JSONs sao sintaticamente validos e carregaveis pelo loader;
20. todos os sete JSONs possuem testes de integracao nominais na suite;
21. os testes nominais verificam a geometria relevante de cada tela, nao apenas
    a quantidade de linhas;
22. a suite canonica esta aprovada apos a criacao dos JSONs e dos testes;
23. o QA da implementacao esta aprovado;
24. o usuario executou as sete telas e a validacao manual da secao 16B esta
    aprovada;
25. nenhum JSON precisou ser editado manualmente para repetir os cenarios;
26. as telas `h0029_*` nao estao integradas ao lancador do orquestrador.

---

## 16. Relatorio de implementacao

Criar ou atualizar:

```text
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
```

O relatorio deve registrar:

- causa tecnica encontrada;
- arquivos alterados e criados;
- comportamento anterior;
- comportamento corrigido;
- testes adicionados;
- resultados dos testes focais;
- regressao canonica executada;
- estado Git antes e depois;
- limitacoes;
- necessidade ou dispensa justificada de pseudo-TTY;
- interface real de `tela/demo.py` inspecionada: o que suporta, como carrega
  telas por ID, o que nao esta disponivel via CLI;
- comando exato para abrir cada uma das sete telas `h0029_*` usando o pipeline
  real do demo.py (loader -> modelo -> renderer), sem editar JSONs;
- sequencia completa de comandos para o usuario executar a validacao visual de
  todas as sete telas;
- `VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO`, enquanto a validacao da secao 16B
  nao for concluida pelo usuario.

O implementador nao pode autoaprovar formalmente a implementacao.

---

## 16A. Uso pelo demo.py

O executor deve:

1. ler integralmente `tela/demo.py`, inspecionando a interface real da funcao
   `main()`, do estado inicial e das funcoes de carregamento expostas;
2. determinar o mecanismo real pelo qual o pipeline carrega telas por ID
   (via `carregar_tela`, `construir_modelo` e `renderizar_tela`);
3. verificar se `demo.py` aceita argumentos de linha de comando para definir
   a tela inicial; se nao aceitar, documentar isso explicitamente;
4. registrar o comando exato — usando o pipeline real do `demo.py`, sem
   modificar `demo.py` e sem editar JSONs — para abrir cada uma das sete
   telas `h0029_*`;
5. confirmar que todas as sete telas carregam pelo loader real sem excecao;
6. registrar os comandos no relatorio de implementacao da secao 16.

O relatorio deve fornecer ao usuario uma sequencia direta e autocontida de
comandos para executar a validacao visual de todas as sete telas.

Restricoes:

- nao modificar `tela/demo.py`;
- nao adicionar as telas `h0029_*` ao lancador do `orquestrador.json`;
- nao depender de edicao manual de JSONs para repetir os cenarios.

---

## 16B. Validacao manual obrigatoria (TTY real)

Esta etapa so pode ser executada pelo usuario, apos o QA da implementacao.

O usuario deve abrir cada uma das sete telas `h0029_*` usando os comandos
documentados no relatorio da secao 16, em terminal TTY real, e registrar:

```yaml
tela: h0029_dashboard_igual
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado: APROVADO | REPROVADO | NAO_EXECUTADO
```

```yaml
tela: h0029_dashboard_fracao
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado: APROVADO | REPROVADO | NAO_EXECUTADO
```

```yaml
tela: h0029_dashboard_percentual
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado: APROVADO | REPROVADO | NAO_EXECUTADO
```

```yaml
tela: h0029_grupo_pai_distribuido
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado: APROVADO | REPROVADO | NAO_EXECUTADO
```

```yaml
tela: h0029_grupo_igual
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado: APROVADO | REPROVADO | NAO_EXECUTADO
```

```yaml
tela: h0029_grupo_fracao
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado: APROVADO | REPROVADO | NAO_EXECUTADO
```

```yaml
tela: h0029_grupo_percentual
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado: APROVADO | REPROVADO | NAO_EXECUTADO
```

Criterios visuais para aprovacao:

- tela abre sem erro;
- cabecalho permanece correto;
- corpo ocupa a area esperada;
- bordas aparecem nas posicoes esperadas;
- `barra_de_menus` permanece no fim da tela;
- nao ha desaparecimento de linhas;
- nao ha sobreposicao;
- nao ha espaco externo onde o elemento deveria ocupar a cota.

Somente o usuario pode concluir esta validacao.

O implementador e o auditor devem registrar:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

ate que o usuario apresente os resultados de todas as sete telas.

---

## 16C. Lista acumulada de arquivos do ciclo

Arquivos esperados ao final do H-0029:

```text
tela/renderizador.py                          (modificado)
tela/teste_renderizador.py                    (modificado)
config/telas/h0029_dashboard_igual.json       (criado)
config/telas/h0029_dashboard_fracao.json      (criado)
config/telas/h0029_dashboard_percentual.json  (criado)
config/telas/h0029_grupo_pai_distribuido.json (criado)
config/telas/h0029_grupo_igual.json           (criado)
config/telas/h0029_grupo_fracao.json          (criado)
config/telas/h0029_grupo_percentual.json      (criado)
docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
                                              (nao rastreado; nao alterar)
docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
                                              (nao rastreado; nao alterar)
docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
                                              (nao rastreado; nao alterar)
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
                                              (criado ou atualizado)
docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
                                              (nao rastreado; nao alterar)
```

Os arquivos de relatorio e handoff nao rastreados pertencem ao fluxo documental
do ciclo e nao devem ser alterados pelo implementador.

---

## 17. Condicoes de bloqueio

Parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

- o comportamento esperado contradizer contrato ativo;
- cardinalidade unitaria exigir nova politica nao documentada;
- `percentual [100]` deixar de ser valido por autoridade mais forte;
- a correcao exigir propagacao implicita entre niveis;
- a causa nao puder ser distinguida de configuracao declarativa incorreta;
- autoridades ativas estiverem contraditorias;
- for indispensavel alterar `loader.py`, `modelo.py`, contratos, ADRs,
  nomenclatura ou indices;
- a geometria dos JSONs `h0029_*` revelar necessidade de mudanca normativa.

Parar com `H3_BLOCKED_DOCUMENTATION` se a documentacao ativa for insuficiente
para decidir a semantica sem nova ADR.

Parar com `BLOCKED_USER_DECISION` se houver mais de uma correcao normativa
possivel e nenhuma autoridade escolher entre elas.

---

## 18. Encerramento do executor

Ao encerrar, o executor deve apresentar status factual, sem commit:

```text
status_literal:
status_normalizado:
relatorio:
arquivos_criados:
arquivos_alterados:
testes_executados:
validacao_manual:
bloqueios:
```

Status normalizados permitidos para a implementacao:

- `IMPLEMENTED_PENDING_QA`
- `BLOCKED_DOCUMENTATION`
- `BLOCKED_USER_DECISION`
- `ARCHITECTURE_REVIEW_REQUIRED`
- `BLOCKED_REPOSITORY_STATE`
