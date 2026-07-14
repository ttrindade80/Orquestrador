# RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO

Reauditoria da implementação H-0027 após o patch de correção emitido pelo
`RELATORIO_QA_H-0027_IMPLEMENTACAO.md` (`I2_IMPLEMENTATION_PATCH_REQUIRED`).
Verificação concentrada na resolução de `ACH-001` a `ACH-006`, na ausência de
regressões, no escopo do patch, nos testes e no estado Git. Não repete
integralmente o QA anterior; cita-o quando o estado é idêntico.

---

## 1. Identificação

- Artefato auditado: implementação produzida a partir de
  `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`
- Categoria processual executada: `QA_POS_PATCH` (reauditoria da implementação)
- ADR base: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
  (status `aceita`)
- Auditor: agente formal de QA da implementação H-0027 (pós-patch)
- Data: 2026-07-12
- Branch: `master`
- Commit base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Relatório de QA anterior: `docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md`
- Classificação anterior: `I2_IMPLEMENTATION_PATCH_REQUIRED`
- Relatório de implementação auditado:
  `docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md`

Limites estritos desta etapa:

- reauditar a implementação H-0027 quanto à resolução de `ACH-001` a `ACH-006`;
- verificar ausência de regressão nas áreas preservadas (D1–D7 e capacidades anteriores);
- confirmar o escopo do patch e o estado Git;
- produzir somente este relatório;
- não corrigir a implementação, os testes ou o `IMP-0028`;
- não alterar handoff, ADRs, contratos, nomenclatura ou índice;
- não preparar commit, não fazer commit ou push;
- não executar etapa posterior.

---

## 2. Estado Git inicial

Comandos executados a partir de `scripts/` (raiz efetiva dos caminhos declarados
na documentação; toplevel Git em `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`).

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       |  27 +-
 scripts/docs/adr/ADR-0007-tela-processamento-composicao.md  |  15 +-
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md    |  40 +-
 scripts/docs/contratos/contrato_json_tela_minima.md    |   7 +-
 scripts/docs/contratos/contrato_tela_json.md       |  15 +-
 scripts/tela/loader.py                             | 165 +++---
 scripts/tela/modelo.py                             | 106 ++--
 scripts/tela/renderizador.py                       | 297 ++++++----
 scripts/tela/teste_loader.py                       | 460 +++++++++++++--
 scripts/tela/teste_modelo.py                       | 185 ++++++
 scripts/tela/teste_renderizador.py                 | 621 +++++++++++++++++++++
 12 files changed, 1669 insertions(+), 270 deletions(-)

git diff --check
(sem saída — sem conflitos de espaço em branco)

git diff --cached --stat
(sem saída)

git diff --cached --name-only
(sem saída)
```

Observações:

- commit-base `40015b6` confirmado;
- stage vazio confirmado;
- `git diff --check` limpo (código de saída 0);
- 6 alterações documentais rastreadas preexistentes (aplicação ADR-0019);
- 6 arquivos `tela/*.py` rastreados modificados (implementação H-0027 + patch);
- arquivos não rastreados: ADR-0019, handoff H-0027, IMP-0028 e relatórios QA
  do ciclo; `tela/__pycache__/` (cache Python, irrelevante).

---

## 3. Artefatos consultados

Lidos integralmente:

- `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md`
- `docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md`

Inspecionados por diff e conteúdo:

- `tela/loader.py` (diff completo; funções `_validar_distribuicao_corpo`,
  `_validar_grupo`)
- `tela/modelo.py` (diff; construção recursiva; docstrings de escopo plano)
- `tela/renderizador.py` (diff completo; `_renderizar_container*`;
  comentário de `_montar_corpo_horizontal`)
- `tela/teste_loader.py` (substituições dos 4 testes históricos;
  `teste_hierarquia_grupos_adr0019`; 2 verificações ACH-005)
- `tela/teste_modelo.py` (`teste_hierarquia_grupos_adr0019_modelo`)
- `tela/teste_renderizador.py` (`TestHierarquiaGruposH0027`, incluindo os 3
  métodos novos ACH-001 e a chamada em `run_all`)
- `tela/teste_demo.py` (executado; sem alteração declarada pelo patch)

Consultados quando necessário para confirmar a preservação de D1–D7:

- ADR-0019 e contratos ativos (somente leitura; não alterados).

---

## 4. Matriz de resolução — `ACH-001` a `ACH-006`

| Achado  | Evidência pós-patch                                           | Resultado |
| ------- | ------------------------------------------------------------ | --------- |
| ACH-001 | `tela/teste_renderizador.py:4701-4895` (3 métodos novos) + `run_all` linhas 4916-4918; saída `491/491` com 24 verificações `ACH-001a/b/c` `[PASSOU]` | RESOLVIDO |
| ACH-002 | `docs/relatorios/IMP-0028-...md` seção 6, tabela "Resultados finais pós-patch" (linhas 250-258): registra `teste_demo.py` 303/303, código 0; total 1004/1004 | RESOLVIDO |
| ACH-003 | `docs/relatorios/IMP-0028-...md` seção 2 (estado Git inicial, linhas 18-99) e seção 8 (estado Git final, linhas 272-331): saída dos comandos exigidos | RESOLVIDO |
| ACH-004 | `docs/relatorios/IMP-0028-...md` seção 9 (linhas 343-345): "Nenhum bloqueio encontrado durante a implementação..." | RESOLVIDO |
| ACH-005 | `tela/loader.py`: `_validar_distribuicao_corpo` parametrizada com `prefixo_caminho="corpo"` (default preserva raiz); `_validar_grupo` passa `caminho_grupo`; 2 verificações em `tela/teste_loader.py:1336-1350` | RESOLVIDO |
| ACH-006 | `tela/renderizador.py:984-988`: comentário de `_montar_corpo_horizontal` reescrito declarando preservação histórica e uso de `_renderizar_container` no caminho principal | RESOLVIDO |

---

## 5. Análise dos testes adicionados (ACH-001)

Os três métodos novos confirmados em `TestHierarquiaGruposH0027`
(`tela/teste_renderizador.py:4701-4895`), todos registrados em `run_all`
(linhas 4916-4918) e portanto executáveis.

### 5.1 `test_corpo_horizontal_com_grupos_filhos` (ACH-001a)

- Estrutura: `corpo horizontal → [g1 vertical (ALFA), g2 vertical (BETA)]`.
- Linhas 4702-4750; 7 verificações.
- Exercita o caminho real do renderizador recursivo
  (`renderizar_tela → _renderizar_container(horizontal) →
  _renderizar_container_horizontal` despachando grupos via
  `_renderizar_container` recursivo em `_renderizar_container_horizontal`).
- Valida: saída não vazia; `ALFA` e `BETA` presentes; `ALFA` e `BETA` na mesma
  linha (grupos lado a lado); grupos não viram slots vazios; largura total 42
  preservada em todas as linhas não vazias; determinismo (duas chamadas
  idênticas).
- Comprova renderização dos descendentes; detecta achatamento, sobreposição ou
  perda de área; não se limita a ausência de exceção.

### 5.2 `test_horizontal_grupo_vertical` (ACH-001b)

- Estrutura: `corpo horizontal → g1 vertical → [CIMA, BAIXO]`.
- Linhas 4753-4807; 7 verificações.
- Exercita a combinação `horizontal → vertical` no renderizador recursivo.
- Valida: saída não vazia; `CIMA` e `BAIXO` presentes; ordem vertical
  preservada (`CIMA` antes de `BAIXO`); ausência de achatamento (linhas
  distintas); ausência de slot vazio; largura total 42 preservada.

### 5.3 `test_tres_niveis_arranjos_alternados` (ACH-001c)

- Estrutura: `corpo vertical → g1 horizontal → [g2 vertical → g3 horizontal →
  [FA, FB], TOPO (dashboard)]`.
- Linhas 4810-4895; 10 verificações; usa `largura=80` para garantir área
  suficiente em três níveis de particionamento.
- Exercita três níveis de grupos com arranjos alternados (`v → h → v → h`).
- Valida: saída não vazia; `FA` e `FB` presentes (funcionais nível 3);
  `TOPO` presente (funcional nível 1); `FA` e `FB` na mesma linha (g3
  horizontal); ausência de achatamento; largura 80 preservada; determinismo;
  ordem declarada (`FA` à esquerda de `FB`); existência dos três níveis.

### 5.4 Métodos informados pelo executor

Confirmados com os nomes exatos declarados:

```text
test_corpo_horizontal_com_grupos_filhos   (tela/teste_renderizador.py:4702)
test_horizontal_grupo_vertical            (tela/teste_renderizador.py:4753)
test_tres_niveis_arranjos_alternados      (tela/teste_renderizador.py:4810)
```

Todos os três produzem `[PASSOU]` em todas as suas verificações (24 verificações
totais confirmadas na reexecução independente do auditor).

### 5.5 Classificação de ACH-001

```text
ACH-001: RESOLVIDO
```

Os três cenários obrigatórios ausentes (corpo horizontal com grupos filhos;
combinação `horizontal → vertical`; três níveis com arranjos alternados) agora
têm cobertura executável não trivial. Os testes exercitam caminhos reais do
renderizador recursivo, validam saída e dimensões observáveis, comprovam que os
grupos não viram slots vazios, comprovam renderização dos descendentes e
detectam achatamento/sobreposição/perda de área.

---

## 6. Análise das mensagens (ACH-005)

### 6.1 Implementação

`_validar_distribuicao_corpo(distribuicao, n_elementos, prefixo_caminho="corpo")`
(`tela/loader.py`):

- default `prefixo_caminho="corpo"` preserva o comportamento anterior para
  chamadas do corpo raiz;
- todas as mensagens substituem o prefixo fixo `"corpo.distribuicao"` por
  `"{prefixo_caminho}.distribuicao"`.

`_validar_grupo(elemento, id_grupo, nivel_grupo=1, caminho="corpo")`:

- calcula `caminho_grupo = "{caminho} → {id_grupo}"`;
- chama `_validar_distribuicao_corpo(distribuicao, len(sub), caminho_grupo)` e
  envolve a exceção em `"Grupo '{id_grupo}' em '{caminho}': {exc}"`.

### 6.2 Comportamento confirmado independentemente

Execução direta de `_validar_distribuicao_corpo`:

```text
ROOT_PATH_MSG:  TelaEstruturaInvalida -> corpo.distribuicao.modo invalido: 'invalido'; valores aceitos: igual, percentual, fracao
GROUP_PATH_MSG: TelaEstruturaInvalida -> corpo → g1.distribuicao.modo invalido: 'invalido'; valores aceitos: igual, percentual, fracao
```

Execução pelo loader (mensagem efetiva do teste `teste_loader.py:1342-1350`):

```text
Grupo 'g1' em 'corpo': corpo → g1.distribuicao.modo invalido: 'invalido'; valores aceitos: igual, percentual, fracao
```

### 6.3 Verificação dos requisitos do roteiro

| Requisito | Confirmado | Evidência |
| --- | --- | --- |
| Erros de distribuição na raiz usam `corpo.distribuicao` | SIM | `ROOT_PATH_MSG` acima; mensagens raiz inalteradas |
| Erros dentro de grupos usam o caminho estrutural real do grupo | SIM | `GROUP_PATH_MSG`; `caminho_grupo` em `_validar_grupo` |
| A validação continua determinística | SIM | mesma entrada → mesma mensagem (mensagens formatadas por `str.format`, sem estado) |
| Semântica de `igual`, `percentual` e `fracao` não foi alterada | SIM | blocos de validação de modo/valores/soma intocados; apenas o prefixo foi parametrizado |
| Quantidade de valores continua comparada aos filhos diretos | SIM | `n_elementos = len(sub)` em `_validar_grupo`; `_validar_distribuicao_corpo` compara `len(valores) != n_elementos` |

### 6.4 Cobertura mínima de testes do loader (ACH-005)

- Caminho de erro na raiz: SIM — `teste_distribuicao_corpo_h0025` mantém
  verificações com `corpo.distribuicao.modo invalido`, `corpo.distribuicao
  percentual exige soma igual a 100`, etc. (suíte 127→129 aprova).
- Caminho de erro em grupo: SIM —
  `teste_hierarquia_grupos_adr0019` verifica `grupo com distribuicao.modo
  invalido → TelaEstruturaInvalida` e `grupo com distribuicao vetor tamanho
  errado → TelaEstruturaInvalida`.
- Ausência da expressão enganosa `corpo.distribuicao` para erro interno: SIM —
  verificação
  `"ACH-005: mensagem de dist em grupo NAO usa 'corpo.distribuicao' isolado"`
  (`tela/teste_loader.py:1346-1350`), aprovada.

### 6.5 Avaliação do formato efetivo `corpo → g1.distribuicao`

O formato produzido segue o mesmo padrão de caminho adotado pelo loader para
erros estruturais: o separador `" → "` é exatamente o usado na mensagem de nível
4 (`Grupo 'g4' em 'corpo → g1 → g2 → g3' criaria nivel 4...`). O sufixo
`.distribuicao.modo invalido` é o campo do container, agora qualificado pelo
prefixo do caminho estrutural. O formato é **consistente e não ambíguo**:
identifica o container (`corpo → g1`) e o campo (`.distribuicao.modo`). Não há
divergência do padrão de caminho do loader, nem sobreposição com a referência ao
corpo raiz. A envoltória adicional `"Grupo 'g1' em 'corpo': "` aumenta ainda
mais a localização. Sem achado.

### 6.6 Classificação de ACH-005

```text
ACH-005: RESOLVIDO
```

A observação anterior (mensagem enganosa `corpo.distribuicao` em grupo) foi
corrigida por parametrização do prefixo. A reutilização é determinística, a
semântica dos modos foi preservada, a contagem continua por filhos diretos e a
mensagem interna agora reflete o caminho estrutural real.

---

## 7. Análise do `IMP-0028`

### 7.1 ACH-002 — `teste_demo.py` no IMP-0028

A seção 6 do `IMP-0028` (tabela "Resultados finais pós-patch", linhas 250-258)
registra explicitamente:

```text
| Suite                       | Código de saída | Verificações | Passaram | Falharam |
| python tela/teste_demo.py   | 0               | 303          | 303      | 0        |
```

Inclui comando, código de saída, verificações aprovadas, falhas e resultado
final. Total declarado: 1004/1004. Confere com a reexecução independente do
auditor (303/303, código 0). **RESOLVIDO.**

### 7.2 ACH-003 — estado Git no IMP-0028

- Estado Git inicial: seção 2 (linhas 18-99), com saída de `git log -1
  --oneline`, `git status --short`, `git diff --stat`, `git diff --check`,
  `git diff --cached --stat`, `git diff --cached --name-only`, e classificação
  das alterações (rastreadas documentais preexistentes vs. rastreadas da
  implementação vs. não rastreadas).
- Estado Git final: seção 8 (linhas 272-331), com os mesmos comandos, e
  classificação final (seção 8.1, linhas 329-340).

Distingue alterações documentais anteriores à implementação, arquivos alterados
pela implementação e `tela/__pycache__/`. Stage documentado como vazio em ambos
os estados. **RESOLVIDO.**

### 7.3 ACH-004 — bloqueios no IMP-0028

Seção 9 (linhas 343-345) declara explicitamente:

```text
Nenhum bloqueio encontrado durante a implementação (BLOCKED_REPOSITORY_STATE,
ARCHITECTURE_REVIEW_REQUIRED e BLOCKED_SCOPE não ocorreram).
```

O `IMP-0028` não declara aprovação formal da própria implementação (cabeçalho
declara `Status: IMPLEMENTADO (patch aplicado — aguarda QA_POS_PATCH)`; não usa
classificações reservadas ao QA como `I1_*`). **RESOLVIDO.**

### 7.4 Comparação dos resultados declarados pelo executor vs. auditor

| Suíte | IMP-0028 (declarado) | Auditor (independente) | Divergência |
| --- | --- | --- | --- |
| `teste_loader.py` | 129/129, código 0 | 129/129, código 0 | NENHUMA |
| `teste_modelo.py` | 81/81, código 0 | 81/81, código 0 | NENHUMA |
| `teste_renderizador.py` | 491/491, código 0 | 491/491, código 0 | NENHUMA |
| `teste_demo.py` | 303/303, código 0 | 303/303, código 0 | NENHUMA |
| `git diff --check` | código 0 | código 0 | NENHUMA |

Total: 1004/1004 — coincide com o declarado. Nenhuma divergência.

---

## 8. Regressões

### 8.1 Matriz D1–D7

| Decisão | Estado pós-patch | Evidência | Regressão? |
| --- | --- | --- | --- |
| D1 — contagem por níveis de grupos | Intacta | `_validar_grupo` incrementa `nivel_grupo` somente para `tipo == "grupo"` (loader); funcionais não incrementam; `teste_loader.py` aprova | NÃO |
| D2 — três níveis de grupos | Intacta | `nivel_grupo == 3` rejeita filho `grupo`; níveis 1-3 aceitos; modelo 2/3 níveis; renderer `test_g3` + `test_tres_niveis_arranjos_alternados` | NÃO |
| D3 — funcionais no nível 3 | Intacta | `elif tipo_item in TIPOS_CORPO_VALIDOS: pass` aceita funcionais em qualquer nível; teste `nivel 3 com 2 funcionais` | NÃO |
| D4 — nível 4 inválido | Intacta | `TelaGrupoInvalido` com id, caminho completo e "maximo e 3 niveis"; determinismo verificado | NÃO |
| D5 — múltiplos grupos irmãos | Intacta | ausência de verificação de unicidade; `multiplos grupos irmaos no nivel 1/2` | NÃO |
| D6 — múltiplos funcionais | Intacta | regra antiga removida; `grupo com 2 filhos funcionais e valido` | NÃO |
| D7 — múltiplos dashboards | Intacta | sem cardinalidade global; `multiplos dashboards em grupos distintos`; renderer `test_multiplos_dashboards_em_grupos` | NÃO |

### 8.2 Capacidades preservadas

| Capacidade | Evidência | Regressão? |
| --- | --- | --- |
| Loader recursivo | `_validar_grupo` recursiva com profundidade e caminho; 129/129 | NÃO |
| Modelo recursivo | `_construir_elementos_recursivo` preserva árvore; 81/81 | NÃO |
| Renderizador recursivo | `_renderizar_container*`; 491/491 | NÃO |
| Métodos públicos planos do modelo | `elemento_por_id`/`elementos_por_tipo` planos com docstrings explícitas | NÃO |
| Distribuição vertical do corpo raiz | `TestDistribuicaoVerticalH0025` aprova; `test_json_real_orquestrador_distribui_212` | NÃO |
| Distribuição horizontal do corpo raiz | `TestDistribuicaoHorizontalH0026` aprova | NÃO |
| Distribuição em grupos | `test_distribuicao_igual_em_grupo`, `_fracao_grupo_horizontal`, `_percentual_grupo_vertical_com_altura` | NÃO |
| Ausência de distribuição | ramo `else` content-driven; `test_ausencia_*` | NÃO |
| Modos `igual`, `percentual`, `fracao` | `_pesos_distribuicao` reutilizado; testes normativos | NÃO |
| Maiores restos e ordem declarada | `_distribuir_alturas`/`_distribuir_larguras` não alterados; `TestDistribuicaoHorizontalH0026` algoritmo | NÃO |
| JSONs ativos (`orquestrador`, `grupo_minimo`, `destino_minimo`, `stub_b`) | regressões loader + renderer + demo 303/303 | NÃO |
| Navegação, `[✥]` e bindings | demo 303/303 (navegação TTY/subprocess); `bindings preservado como declaracao inerte` | NÃO |
| Comportamento da demo | demo 303/303, código 0; seção 8.16 PTY redimensionamento | NÃO |

Não houve regressão.

---

## 9. Testes executados (independentes)

| Comando | Código de saída | Verificações | Passaram | Falharam | Resultado |
| --- | --- | --- | --- | --- | --- |
| `python tela/teste_loader.py` | 0 | 129 | 129 | 0 | APROVADO |
| `python tela/teste_modelo.py` | 0 | 81 | 81 | 0 | APROVADO |
| `python tela/teste_renderizador.py` | 0 | 491 | 491 | 0 | APROVADO |
| `python tela/teste_demo.py` | 0 | 303 | 303 | 0 | APROVADO |
| `git diff --check` | 0 | — | — | — | APROVADO |

Total executável verificado pelo auditor: **1004 verificações; 1004 aprovadas;
0 falhas.** Coincide com o total declarado pelo executor (1004/1004). Nenhuma
divergência em relação ao `IMP-0028`.

As 24 verificações `ACH-001a/b/c` e as 2 verificações `ACH-005` foram
confirmadas `[PASSOU]` na reexecução.

---

## 10. Escopo e Git

### 10.1 Arquivos alterados pela implementação H-0027 (antes do patch)

Conforme o QA anterior e o `IMP-0028` seção 2, a implementação original alterou
os 6 arquivos `tela/*.py` rastreados:

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

e criou `docs/relatorios/IMP-0028-...md` (não rastreado). `tela/teste_demo.py`
foi listado como permitido (H-0027 seção 8) mas **não** modificado — válido.

### 10.2 Arquivos alterados pelo patch

O executor declarou ter alterado no patch:

```text
tela/loader.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_renderizador.py
docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
```

Confirmação independente:

- `tela/loader.py`: diff contém a parametrização de `_validar_distribuicao_corpo`
  (prefixo) e o uso de `caminho_grupo` em `_validar_grupo` — alterações do patch
  ACH-005. ✅
- `tela/renderizador.py`: diff contém as 3 funções `_renderizar_container*`
  (implementação original) **e** o comentário reescrito de
  `_montar_corpo_horizontal` (patch ACH-006). ✅
- `tela/teste_loader.py`: diff contém as substituições dos 4 testes históricos
  e a suíte `teste_hierarquia_grupos_adr0019` (implementação original) **e** as
  2 verificações ACH-005 (patch). ✅
- `tela/teste_renderizador.py`: diff contém a classe `TestHierarquiaGruposH0027`
  (implementação original) **e** os 3 métodos novos ACH-001 (patch). ✅
- `docs/relatorios/IMP-0028-...md`: completado pelo patch (ACH-002, ACH-003,
  ACH-004). ✅

Observação: `tela/modelo.py` (106) e `tela/teste_modelo.py` (185) têm diff stat
idêntico ao da implementação original relatado no QA anterior
(`RELATORIO_QA_H-0027_IMPLEMENTACAO.md` seção 2: `modelo.py 106`, `teste_modelo.py
185`), indicando que **não foram tocados pelo patch** — coerente com a declaração
do executor. O patch restringiu-se aos 4 arquivos de código declarados + IMP-0028.

### 10.3 Arquivos não classificados como fora do escopo

Os 6 documentos rastreados modificados (`docs/NOMENCLATURA.md`,
`docs/adr/ADR-0007-...md`, `docs/adr/INDICE_ADR.md`,
`docs/contratos/contrato_composicao_corpo.md`,
`docs/contratos/contrato_json_tela_minima.md`,
`docs/contratos/contrato_tela_json.md`) são a **aplicação documental preexistente
da ADR-0019**, explicitamente excluída da classificação de fora-de-escopo pelo
roteiro e pelo `IMP-0028` seção 2.1. Não constituem alteração do patch nem da
implementação H-0027.

### 10.4 Arquivos que não devem ter sido alterados

Verificação por `git status --short` e `git diff --name-only`:

```text
docs/adr/*                    — ADR-0007 e INDICE_ADR: apenas alteração documental preexistente (ADR-0019); ADR-0019 nova não rastreada. Nenhuma alteração pelo patch.
docs/contratos/*              — apenas alteração documental preexistente. Nenhuma alteração pelo patch.
docs/NOMENCLATURA.md          — apenas alteração documental preexistente. Nenhuma alteração pelo patch.
docs/handoff/*                — H-0027 não rastreado, não alterado pelo patch.
docs/relatorios/* exceto IMP-0028 e este relatório — não alterados pelo patch.
config/telas/*.json           — nenhum alterado (diff vazio sobre config/).
```

### 10.5 Stage

Stage vazio confirmado (`git diff --cached --stat` sem saída;
`git diff --cached --name-only` sem saída).

### 10.6 Arquivos fora do escopo

```text
NENHUM
```

---

## 11. Validação manual

A recursão de layout é determinística: dada a mesma estrutura de modelo e as
mesmas dimensões, a saída é idêntica entre chamadas. Os testes novos
`ACH-001a/c` verificam isso explicitamente (`saida == saida2`).

Os resultados de renderização hierárquica são determinísticos em conteúdo e
dimensões (largura total preservada em todas as linhas não vazias; ordem
declarada; ausência de achatamento), e esses invariantes são cobertos
executavelmente. A apresentação visual final em terminal depende do renderer de
caracteres do terminal, mas não há comportamento visual ou interativo obrigatório
do H-0027 que não esteja comprovado pelos testes automatizados (a demonstração
interativa via PTY é coberta por `teste_demo.py` seção 8.16, 303/303).

Não há validação humana em TTY real obrigatória pendente.

---

## 12. Achados novos

Nenhum achado novo bloqueante, alto, médio ou baixo foi identificado nesta
reauditoria.

### 12.1 Observações

- O `IMP-0028` seção 5.3 relata que o patch atualizou o comentário de
  `_montar_corpo_horizontal` (ACH-006); confirmado em `tela/renderizador.py:984-988`.
  O comentário agora (a) descreve corretamente que a função histórica não
  expande grupos; (b) esclarece que o caminho principal atual usa
  `_renderizar_container`; (c) não afirma que o sistema atual não suporta grupos
  horizontais; (d) não mascara comportamento funcional incorreto. Achado
  documental no código, sem alteração funcional — atendido.
- As 3 fixtures de teste são modelos sintéticos em memória (`_modelo_hierarquico`,
  `_grupo`, `_funcional`), sem criação de arquivos em `config/telas/` — permitido
  pelo H-0027 seção 8.
- O formato de mensagem `corpo → g1.distribuicao.modo invalido` (ACH-005) é
  consistente com o padrão de caminho do loader (separador `" → "`) e não é
  ambíguo; não constitui novo achado.

---

## 13. Conclusão

O patch aplicado em resposta ao `I2_IMPLEMENTATION_PATCH_REQUIRED` resolveu
integralmente os seis achados do QA anterior:

- **ACH-001 (ALTA)**: os três cenários obrigatórios ausentes (corpo horizontal
  com grupos filhos; combinação `horizontal → vertical`; três níveis com
  arranjos alternados) ganharam cobertura executável não trivial em
  `TestHierarquiaGruposH0027`, com 24 verificações que exercitam os caminhos
  reais do renderizador recursivo e validam saída, dimensões, ordem, determinismo
  e ausência de achatamento/sobreposição/perda de área.
- **ACH-002 (MÉDIA)**: o `IMP-0028` agora registra `teste_demo.py` (303/303,
  código 0) e o total 1004/1004.
- **ACH-003 (MÉDIA)**: o `IMP-0028` agora contém estado Git inicial (seção 2) e
  final (seção 8) com a saída dos comandos exigidos.
- **ACH-004 (BAIXA)**: o `IMP-0028` agora contém seção explícita de bloqueios
  (seção 9).
- **ACH-005 (BAIXA)**: a mensagem de erro de distribuição em grupo agora usa o
  caminho estrutural real (`corpo → g1.distribuicao...`) em vez do
  `corpo.distribuicao` enganoso, sem alterar a semântica dos modos nem a
  contagem por filhos diretos.
- **ACH-006 (BAIXA)**: o comentário de `_montar_corpo_horizontal` foi atualizado
  para declarar a preservação histórica e o caminho principal via
  `_renderizar_container`.

Todas as quatro suítes passam independentemente (1004/1004, código 0).
`git diff --check` limpo. Stage vazio. Nenhuma regressão em D1–D7 ou nas
capacidades anteriores. O escopo do patch restringiu-se aos 4 arquivos de código
declarados + `IMP-0028`; nenhum arquivo proibido foi alterado; os 6 documentos
rastreados modificados são a aplicação documental preexistente da ADR-0019.
Nenhum arquivo fora do escopo. Nenhum achado novo. Nenhuma validação manual
obrigatória pendente. Nenhuma nova decisão do usuário necessária.

---

## 14. Status final

```text
I1_IMPLEMENTATION_APPROVED
```

Justificativa: `ACH-001` a `ACH-006` estão **RESOLVIDOS**; todas as suítes
passam (1004/1004, código 0); não há regressão; o `IMP-0028` está completo; não
há arquivo fora do escopo; nenhuma validação manual obrigatória pendente;
nenhuma correção adicional necessária.

---

## 15. Próxima categoria (sem executá-la)

A implementação H-0027 está aprovada. A próxima etapa processual é a preparação
e criação do commit (etapa separada, executada após `I1_IMPLEMENTATION_APPROVED`,
sob autorização explícita do usuário). Esta auditoria **não** prepara, **não**
cria e **não** faz push de commit, conforme os limites de encerramento.

---

## 16. Estado Git final

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       |  27 +-
 scripts/docs/adr/ADR-0007-tela-processamento-composicao.md  |  15 +-
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 scripts/docs/contratos/contrato_composicao_corpo.md    |  40 +-
 scripts/docs/contratos/contrato_json_tela_minima.md    |   7 +-
 scripts/docs/contratos/contrato_tela_json.md       |  15 +-
 scripts/tela/loader.py                             | 165 +++---
 scripts/tela/modelo.py                             | 106 ++--
 scripts/tela/renderizador.py                       | 297 ++++++----
 scripts/tela/teste_loader.py                       | 460 +++++++++++++--
 scripts/tela/teste_modelo.py                       | 185 ++++++
 scripts/tela/teste_renderizador.py                 | 621 +++++++++++++++++++++
 12 files changed, 1669 insertions(+), 270 deletions(-)

git diff --check
(sem saída — código de saída 0)

git diff --cached --stat
(sem saída — stage vazio)

git diff --cached --name-only
(sem saída — stage vazio)
```

O único novo arquivo criado nesta auditoria é
`docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md` (este relatório,
não rastreado). Nenhum arquivo rastreado foi alterado pelo QA. A ADR-0019, o
handoff H-0027, o `IMP-0028`, os demais relatórios do ciclo e
`tela/__pycache__/` permanecem não rastreados, sem alteração, remoção,
movimentação ou stage. Stage permanece vazio ao final.
