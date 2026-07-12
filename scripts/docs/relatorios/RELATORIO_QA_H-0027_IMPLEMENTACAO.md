# RELATORIO_QA_H-0027_IMPLEMENTACAO

Auditoria formal da implementação do handoff H-0027.

---

## 1. Identificação

- Artefato auditado: implementação produzida a partir de
  `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`
- Categoria processual executada: `QA_IMPLEMENTACAO`
- ADR base: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
  (status `aceita`)
- Auditor: agente formal de QA da implementação H-0027
- Data: 2026-07-12
- Branch: `master`
- Commit base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Relatório de implementação auditado:
  `docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md`

---

## 2. Estado Git no início do QA

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
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       |  27 +-
 .../adr/ADR-0007-tela-processamento-composicao.md  |  15 +-
 scripts/docs/adr/INDICE_ADR.md                     |   1 +
 .../docs/contratos/contrato_composicao_corpo.md    |  40 +-
 .../docs/contratos/contrato_json_tela_minima.md    |   7 +-
 scripts/docs/contratos/contrato_tela_json.md       |  15 +-
 scripts/tela/loader.py                             | 128 +-
 scripts/tela/modelo.py                             | 106 +-
 scripts/tela/renderizador.py                       | 291 +++++-
 scripts/tela/teste_loader.py                       | 445 ++++++-
 scripts/tela/teste_modelo.py                       | 185 +++
 scripts/tela/teste_renderizador.py                 | 422 ++++++
 12 files changed, 1428 insertions(+), 254 deletions(-)

git diff --check
(sem saída — sem conflitos de espaço em branco)

git diff --cached --stat
(sem saída — stage vazio)

git diff --cached --name-only
(sem saída — stage vazio)
```

### 2.1 Classificação das alterações

| Arquivo rastreado modificado | Categoria |
|---|---|
| `docs/NOMENCLATURA.md` | Alteração documental preexistente (aplicação ADR-0019) |
| `docs/adr/ADR-0007-tela-processamento-composicao.md` | Alteração documental preexistente |
| `docs/adr/INDICE_ADR.md` | Alteração documental preexistente |
| `docs/contratos/contrato_composicao_corpo.md` | Alteração documental preexistente |
| `docs/contratos/contrato_json_tela_minima.md` | Alteração documental preexistente |
| `docs/contratos/contrato_tela_json.md` | Alteração documental preexistente |
| `tela/loader.py` | Alteração da implementação H-0027 |
| `tela/modelo.py` | Alteração da implementação H-0027 |
| `tela/renderizador.py` | Alteração da implementação H-0027 |
| `tela/teste_loader.py` | Alteração da implementação H-0027 |
| `tela/teste_modelo.py` | Alteração da implementação H-0027 |
| `tela/teste_renderizador.py` | Alteração da implementação H-0027 |

| Arquivo não rastreado | Categoria |
|---|---|
| `docs/adr/ADR-0019-...` | Ciclo ADR anterior (não tocado) |
| `docs/handoff/H-0027-...` | Handoff (não tocado) |
| `docs/relatorios/IMP-0028-...` | Relatório de implementação (criado) |
| `docs/relatorios/RELATORIO_QA_*` | Relatórios QA do ciclo (não tocados) |
| `tela/__pycache__/` | Cache Python (irrelevante) |

---

## 3. Verificação de escopo

### 3.1 Arquivos alterados pela implementação

Arquivos rastreados com diff de implementação:

| Arquivo | Permitido por H-0027 seção 8? |
|---|---|
| `tela/loader.py` | SIM |
| `tela/modelo.py` | SIM |
| `tela/renderizador.py` | SIM |
| `tela/teste_loader.py` | SIM |
| `tela/teste_modelo.py` | SIM |
| `tela/teste_renderizador.py` | SIM |

**`tela/teste_demo.py`**: listado como permitido por H-0027 seção 8, mas NÃO modificado.
Verificado por inspeção de `git status --short`: ausente do diff rastreado. Nenhuma alteração;
não é infração — a não-alteração de arquivo permitido é válida.

**`docs/relatorios/IMP-0028-...`**: novo arquivo não rastreado (`??`), criado conforme
exigido. Correto.

### 3.2 Arquivos proibidos

Nenhum arquivo proibido (ADRs, contratos, NOMENCLATURA, handoffs, JSONs ativos
existentes) foi alterado pela implementação. As seis alterações documentais
preexistentes são da aplicação ADR-0019, não do executor de H-0027. Confirmado
por `git diff --stat` e `git diff --name-only`.

### 3.3 Fixtures criadas

Nenhuma fixture criada em `config/telas/`. Os testes utilizam dicts em memória
e arquivos temporários. Conforme permitido — criação de fixtures era opcional.

### 3.4 Stage

Stage vazio confirmado (`git diff --cached --stat` sem saída).

---

## 4. Resultados das suítes de testes

### 4.1 Execução independente pelo auditor

| Suíte | Código de saída | Verificações | Passaram | Falharam |
|---|---|---|---|---|
| `python tela/teste_loader.py` | 0 | 127 | 127 | 0 |
| `python tela/teste_modelo.py` | 0 | 81 | 81 | 0 |
| `python tela/teste_renderizador.py` | 0 | 467 | 467 | 0 |
| `python tela/teste_demo.py` | 0 | 303 | 303 | 0 |
| `git diff --check` | 0 | — | — | — |

Total executável verificado pelo auditor: **978 verificações; 978 aprovadas; 0 falhas**.

### 4.2 Comparação com IMP-0028

O relatório IMP-0028 declara:

| Suíte | IMP-0028 | Auditor |
|---|---|---|
| `teste_loader.py` | 127/127 | 127/127 ✅ |
| `teste_modelo.py` | 81/81 | 81/81 ✅ |
| `teste_renderizador.py` | 467/467 | 467/467 ✅ |
| `teste_demo.py` | **não listado** | 303/303 |

O IMP-0028 omite `teste_demo.py` da tabela de resultados (ver ACH-002).

---

## 5. Verificação funcional — Loader

### 5.1 `_validar_grupo` recursiva

A função foi reescrita como recursiva com rastreamento de profundidade e
caminho (`nivel_grupo`, `caminho`). Confirmado por leitura de `tela/loader.py`
linhas 227–323.

- **Validação recursiva de grupos**: ✅ — recursão via `_validar_grupo(item, id_item, nivel_grupo + 1, caminho_grupo)` (linha 319).
- **Profundidade contada somente por nós `grupo`**: ✅ — o incremento `nivel_grupo + 1` só ocorre quando `tipo_item == "grupo"` (linha 310–319). Tipos funcionais passam sem incremento (linha 320–321).
- **Níveis 1, 2 e 3 aceitos**: ✅ — condição de rejeição é `nivel_grupo == 3` para filho do tipo `grupo` (linha 311). Grupos com `nivel_grupo=1,2,3` chegam à recursão.
- **Grupo no nível 4 rejeitado**: ✅ — quando `nivel_grupo == 3` e filho é `grupo`, lança `TelaGrupoInvalido` (linhas 311–317). Mensagem inclui `id_item`, `caminho_grupo` e "maximo e 3 niveis de grupos (ADR-0019 D4)".
- **Caminho estrutural suficiente**: ✅ — `caminho_grupo = "{caminho} → {id_grupo}"` (linha 283); mensagem de nível 4 usa `caminho_grupo` como contexto de diagnóstico.
- **Múltiplos filhos em grupos**: ✅ — laço em `sub` sem restrição de cardinalidade (linhas 285–323).
- **Múltiplos grupos irmãos**: ✅ — sem verificação de unicidade entre irmãos; múltiplos `tipo_item == "grupo"` no mesmo container são aceitos.
- **Grupos verticais e horizontais**: ✅ — `arranjo` validado contra `ARRANJOS_CORPO_VALIDOS` (inclui `None`, `"vertical"`, `"horizontal"`, `"sobreposto"`, `"lado_a_lado"`), linha 242–248.
- **Distribuição validada em cada grupo**: ✅ — bloco linhas 272–280 chama `_validar_distribuicao_corpo(distribuicao, len(sub))` quando `distribuicao is not None`.
- **Modos `igual`, `percentual`, `fracao`**: ✅ — reutiliza `_validar_distribuicao_corpo` que valida os três modos.
- **Quantidade de valores comparada somente aos filhos diretos**: ✅ — `n_elementos = len(sub)` conta apenas `sub = elemento.get("elementos")` (filhos diretos), linha 257+276.
- **Múltiplos dashboards aceitos**: ✅ — sem verificação de cardinalidade de `dashboard` em qualquer ponto do loader.
- **Preservação das validações não relacionadas**: ✅ — todas as 127 verificações do teste_loader.py aprovadas, incluindo casos históricos de arquivo ausente, JSON inválido, campos obrigatórios, etc.

### 5.2 Mensagem de distribuição de grupo

A função `_validar_distribuicao_corpo` usa o prefixo `"corpo.distribuicao"` em
suas mensagens (originalmente projetada para o corpo raiz). Ao ser reutilizada
para grupos (H-0027 seção 13.1 item 5), o texto interno preserva esse prefixo:

```text
"Grupo 'g1' em 'corpo': corpo.distribuicao.modo invalido: 'invalido'; ..."
```

O prefixo `"corpo.distribuicao"` é enganoso quando o erro ocorre em grupo —
refere-se à distribuição do grupo, não do corpo raiz. O contexto externo
(`"Grupo 'g1' em 'corpo':"`) identifica corretamente o container afetado,
mas a concatenação cria a leitura ambígua `"corpo': corpo.distribuicao..."`.

Não constitui bug funcional (a exceção correta é lançada, o grupo e o caminho
são identificados). Registrado como ACH-005 (observação).

### 5.3 Sítio de chamada em `carregar_tela`

`_validar_grupo(elemento, id_elemento)` chamada na linha 443 sem `nivel_grupo`
nem `caminho` explícitos: aplica defaults `nivel_grupo=1`, `caminho="corpo"`.
✅ Correto conforme H-0027 seção 13.2.

---

## 6. Verificação funcional — Modelo

### 6.1 Construção recursiva da árvore

Função `_construir_elementos_recursivo(elementos_raw, id_pai)` adicionada
(linhas 134–200). Confirmado:

- **Construção recursiva**: ✅ — para `tipo == "grupo"`, chama `_construir_elementos_recursivo(sub_raw, sub_id)` recursivamente (linha 167).
- **Preservação da ordem dos filhos**: ✅ — resultado construído por `for` em ordem de `elementos_raw` (linha 144); não há reordenação.
- **Preservação de grupos e funcionais**: ✅ — grupos produzem `ElementoCorpo(tipo="grupo", elementos=sub_elementos)` (linhas 173–179); funcionais produzem `ElementoCorpo` com `elementos=[]` (linhas 187–192).
- **`arranjo` e `distribuicao` preservados em `_campos_inertes`**: ✅ — `inertes = {chave: valor for ... if chave not in ("id", "tipo", "elementos")}` (linhas 168–171). `arranjo` e `distribuicao` ficam em `_campos_inertes`. Verificado por testes do modelo para 2 e 3 níveis.
- **Ausência de achatamento**: ✅ — `ElementoCorpo.elementos` mantém a sub-árvore recursiva; não aplana.
- **Limite coerente com o loader**: ✅ — o loader já rejeita nível 4 antes de chegar ao modelo; o modelo não revalida profundidade (responsabilidade do loader por H-0027 seção 14.1).

### 6.2 `elemento_por_id` e `elementos_por_tipo`

- **Escopo plano preservado**: ✅ — ambos percorrem somente `self.corpo.elementos` diretos (linhas 99–102 e 113). Não descem em grupos.
- **Docstrings explícitas**: ✅ — ambas as docstrings declaram `"Escopo plano: percorre somente self.corpo.elementos diretos, sem descer na arvore de grupos (H-0027 — limitacao documentada, nao bug)."` Confirmado pela leitura do arquivo.
- **Ausência de busca recursiva pública**: ✅ — não existe nenhum novo método público de busca recursiva.
- **Navegação direta da árvore permanece disponível**: ✅ — `elemento.elementos` expõe os filhos de cada nó; verificado em teste específico de `teste_modelo.py`.

---

## 7. Verificação funcional — Renderizador

### 7.1 Funções adicionadas

| Função | Linhas | Papel |
|---|---|---|
| `_renderizar_container_vertical` | 791–841 | Composição vertical com distribuição (cotas) ou orientada pelo conteúdo; despacha grupos recursivamente |
| `_renderizar_container_horizontal` | 844–928 | Composição horizontal com distribuição ou uniforme; despacha grupos recursivamente |
| `_renderizar_container` | 931–965 | Dispatcher principal: normaliza aliases e delega para vertical ou horizontal |

### 7.2 Composição recursiva

- **Grupos verticais**: ✅ — `_renderizar_container_vertical` linhas 809–833 despacha grupos via `_renderizar_container(arranjo_g, dist_g, elemento.elementos, borda, total_w, cota)`.
- **Grupos horizontais**: ✅ — `_renderizar_container_horizontal` linhas 881–893 despacha grupos via `_renderizar_container(arranjo_g, dist_g, elemento.elementos, borda, w, altura_disponivel)`.
- **Combinações vertical → horizontal**: ✅ — testado em `test_g2_vertical_horizontal` (corpo=v, g1=v, g2=h): "ESQQ" e "DIRR" na mesma linha confirmados.
- **Três níveis de grupos**: ✅ — testado em `test_g3_profundidade_maxima` (corpo=v, g1=v, g2=v, g3=v → funcional: "FOLHA" presente).
- **Distribuição independente em cada container**: ✅ — cada chamada recursiva a `_renderizar_container` usa o `distribuicao` do container que o chama, não herdado do pai.
- **Distribuição somente entre filhos diretos**: ✅ — `len(elementos)` passado como `n_elementos` nos cálculos de distribuição conta apenas filhos diretos do container.
- **Ausência de distribuição preservada**: ✅ — ramo `else` em `_renderizar_container_vertical` (linha 824) e cálculo uniforme em `_renderizar_container_horizontal` (linha 863–866) quando `distribuicao is None`.
- **Modos `igual`, `percentual`, `fracao`**: ✅ — reutiliza `_pesos_distribuicao` existente; testados em `test_distribuicao_igual_em_grupo`, `test_distribuicao_fracao_grupo_horizontal`, `test_distribuicao_percentual_grupo_vertical_com_altura`.
- **Maiores restos e desempate por ordem declarada**: ✅ — `_distribuir_alturas` e `_distribuir_larguras` preexistentes; não alteradas.
- **Propagação correta de largura e altura**: ✅ — em modo vertical, `total_w` é propagado integralmente ao grupo (largura total disponível); em modo horizontal, `w = larguras[i]` (largura alocada ao grupo).
- **Múltiplos grupos irmãos**: ✅ — testados em `test_multiplos_dashboards_em_grupos` e `test_mistura_grupo_e_funcional_no_corpo`.
- **Múltiplos funcionais**: ✅ — testados em `test_g1_vertical_produz_saida` (2 funcionais em g1).
- **Múltiplos dashboards**: ✅ — `test_multiplos_dashboards_em_grupos` confirma "PAINEL1" e "PAINEL2" presentes.
- **`grupo` sem moldura, título ou conteúdo próprio**: ✅ — grupo não chama `_caixa()` nem `_caixa_de_elemento()`; apenas retorna resultado de `_renderizar_container` recursivo. Verificado pela regressão `grupo_minimo` (grupo não adiciona caixa própria).

### 7.3 Integração em `renderizar_tela`

O ramo de corpo raiz foi substituído por:
```python
bloco_corpo = _renderizar_container(
    arranjo_corpo, distribuicao_corpo,
    modelo.corpo.elementos, borda, total_w, l_corpo_disponivel,
)
```
(linhas 1213–1216). ✅ — `_montar_corpo_horizontal` não é mais chamada pelo
caminho principal de `renderizar_tela`; preservada como função exportada.

### 7.4 Combinações não cobertas por testes explícitos

Os seguintes cenários do H-0027 seção 18 **não têm cobertura executável** em
`TestHierarquiaGruposH0027` ou em qualquer outra suíte do teste_renderizador.py:

| Cenário (H-0027 seção 18) | Ausente de |
|---|---|
| "Corpo horizontal com dois grupos filhos" | `TestHierarquiaGruposH0027` |
| "Grupo horizontal em corpo horizontal" | `TestHierarquiaGruposH0027` |
| "Grupo vertical em corpo horizontal" (`corpo(h) → grupo(v)`) | `TestHierarquiaGruposH0027` |
| "Três níveis com arranjos alternados (ex.: v → h → v)" | `TestHierarquiaGruposH0027` |

`test_g3_profundidade_maxima` usa exclusivamente `v → v → v`. `TestHierarquiaGruposH0027`
não contém nenhum teste com `_modelo_hierarquico("horizontal", ...)` como corpo raiz.

O código que implementa esses caminhos existe (`_renderizar_container_horizontal`
linhas 879–893 despacha grupos recursivamente) e é funcionalmente correto, mas
a ausência de testes executáveis viola o critério 6 de H-0027 seção 19:
"Todos os cenários da seção 18 têm cobertura executável (não apenas unitária)".

Registrado como ACH-001 (alto).

### 7.5 `_montar_corpo_horizontal` — comentário desatualizado

A função `_montar_corpo_horizontal` (linhas 968–1079) foi preservada sem
alteração. Seu comentário interno (linha 985) diz:
```
"Grupo não é expandido (ADR-0015 D2): conta como slot com área visualmente vazia."
```
Esse texto descreve o comportamento ANTERIOR (antes de H-0027). No estado atual,
grupos renderizados pelo caminho principal de `renderizar_tela` são expandidos
via `_renderizar_container`. O comentário em `_montar_corpo_horizontal` continua
descrevendo o comportamento dessa função específica (que não foi alterada e ainda
trata grupos como slots vazios), mas não o comportamento do sistema como um todo.

A função não é chamada por `renderizar_tela`; é preservada como função exportada
historicamente. O comentário é facticamente verdadeiro para a função, mas
semanticamente confuso quanto ao comportamento geral do sistema após H-0027.
Registrado como ACH-006 (baixo — observação).

---

## 8. Matriz de decisões D1–D7

| Decisão | Implementação | Testes | Resultado |
|---|---|---|---|
| D1 — contagem por grupos | `nivel_grupo` incrementa somente para `tipo == "grupo"` (loader L310–319); funcionais não incrementam | `[PASSOU] nivel 1 com 2 funcionais e valido` — funcionais não ativam contagem | ATENDIDA |
| D2 — três níveis | `nivel_grupo == 3` bloqueia filho `grupo` (L311–317); `nivel_grupo < 3` permite recursão | `2 niveis valido`, `3 niveis valido`, `nivel 4 → TelaGrupoInvalido`; modelo 2 e 3 níveis; renderizador test_g3 | ATENDIDA |
| D3 — funcionais no nível 3 | `elif tipo_item in TIPOS_CORPO_VALIDOS: pass` aceita funcionais em qualquer nível (L320–321) | `nivel 3 com 2 funcionais: valido, nao constitui nivel 4` | ATENDIDA |
| D4 — nível 4 inválido | `raise TelaGrupoInvalido("Grupo '{id}' em '{caminho}' criaria nivel 4...")` (L312–317) | Rejeição + verificação de id, caminho, texto "maximo e 3 niveis", determinismo | ATENDIDA |
| D5 — grupos irmãos | Sem verificação de unicidade entre irmãos; múltiplos filhos `tipo == "grupo"` aceitos | `multiplos grupos irmaos no nivel 1/2 sao validos`; renderizador test_multiplos_dashboards | ATENDIDA |
| D6 — múltiplos funcionais | Regra antiga removida; laço em `sub` sem restrição (L285–323) | `grupo com 2 filhos funcionais e valido`; modelo múltiplos filhos | ATENDIDA |
| D7 — múltiplos dashboards | Sem verificação de cardinalidade de `dashboard` em loader, modelo ou renderizador | `multiplos dashboards em grupos distintos sao validos`; renderizador test_multiplos_dashboards | ATENDIDA |

---

## 9. Verificação de preservações

| Capacidade | Evidência de preservação | Status |
|---|---|---|
| Telas planas (`orquestrador`, `destino_minimo`, `stub_b`) | `[PASSOU] lista plana 'orquestrador/destino_minimo/stub_b' carrega sem erro`; test_regressao_orquestrador; 303/303 demo | ✅ PRESERVADA |
| `grupo_minimo.json` (1 nível) | `[PASSOU] carregar_tela(grupo_minimo) sem excecao`; test_regressao_grupo_minimo; demo `g\n\x1b\n\x1b\n` | ✅ PRESERVADA |
| Distribuição vertical do corpo raiz | Cobertura em TestDistribuicaoVerticalCorpo; `test_json_real_orquestrador_distribui_212` | ✅ PRESERVADA |
| Distribuição horizontal percentual/fracionária | TestDistribuicaoHorizontalCorpo; 422 verificações adicionadas na suíte | ✅ PRESERVADA |
| Ausência de distribuição (orientado pelo conteúdo) | `ausencia de distribuicao: corpo.distribuicao is None (sem fallback igual)`; ramo `else` em `_renderizar_container_vertical` | ✅ PRESERVADA |
| Ordem declarada; maiores restos | `_distribuir_alturas`/`_distribuir_larguras` não alteradas; testes normativos passam | ✅ PRESERVADA |
| Tipos `console`, `lancador`, `dashboard` | Taxonomia fechada preservada; `TIPOS_CORPO_VALIDOS` inalterado | ✅ PRESERVADA |
| Navegação e `[✥]` | 303/303 verificações de demo, incluindo navegação TTY e subprocess | ✅ PRESERVADA |
| Bindings | `bindings preservado como declaracao inerte` — teste_loader.py | ✅ PRESERVADA |
| Diagnósticos não relacionados | 127/127 verificações do loader, incluindo casos de erro históricos | ✅ PRESERVADA |
| Redimensionamento reativo (ADR-0017) | 8.16 PTY: redução/ampliação com redraw — 303/303 verificações demo | ✅ PRESERVADA |

---

## 10. Auditoria do relatório IMP-0028

### 10.1 Verificação por item exigido (H-0027 seção 22)

| Item | Exigência | Status |
|---|---|---|
| 1 | Identificação: handoff, data, commit base, branch | ✅ PRESENTE (H-0027, 2026-07-12, 40015b6; branch não declarado mas inferível) |
| 2 | Estado Git inicial | ❌ AUSENTE — não há seção de estado Git inicial explícito com saída dos comandos executados |
| 3 | Arquivos alterados (lista exata com descrição) | ✅ PRESENTE (seção 2 do IMP-0028) |
| 4 | Comportamento implementado por camada | ✅ PRESENTE (seção 4 do IMP-0028) |
| 5 | Validação de profundidade | ✅ PRESENTE (seção 3 — D1; seção 4.1) |
| 6 | Recursão por camada | ✅ PRESENTE (seções 4.1, 4.2, 4.3) |
| 7 | Multiplicidade | ✅ PRESENTE (seção 3 — D3, D5, D6) |
| 8 | Múltiplos dashboards | ✅ PRESENTE (seção 3 — D7) |
| 9 | Testes adicionados: lista com nome e descrição | ✅ PRESENTE (seção 5) |
| 10 | Testes alterados: quatro históricos e substituições | ✅ PRESENTE (seção 5) |
| 11 | Testes executados: saída resumida de CADA suíte | ❌ PARCIAL — `teste_demo.py` ausente da tabela de resultados (seção 5) |
| 12 | Resultados: código de saída de cada suíte | ✅ PRESENTE para as 3 suítes listadas (seção 7 menciona "retorno 0") |
| 13 | Preservações confirmadas | ✅ PRESENTE (seção 6) |
| 14 | Limitações conhecidas (`elemento_por_id` plano) | ✅ PRESENTE (seção 6) |
| 15 | Estado Git final | ❌ AUSENTE — seção 7 menciona `git diff --check` passando, mas não registra saída completa dos comandos de estado Git final exigidos |
| 16 | Bloqueios encontrados | ❌ AUSENTE — nenhuma seção declara explicitamente "Bloqueios: nenhum" |

### 10.2 Autoapprovação

O IMP-0028 declara `Status: IMPLEMENTADO` no cabeçalho. Não usa nenhuma das
classificações reservadas ao processo de QA (`I1_IMPLEMENTATION_APPROVED`,
`I2_IMPLEMENTATION_PATCH_REQUIRED`, etc.). ✅ — não aprova formalmente a
própria implementação.

---

## 11. Achados

### ACH-001

```text
ID: ACH-001
Severidade: ALTA
Categoria: bug local de implementação (lacuna de cobertura de teste)
Descrição: Três cenários obrigatórios da matriz H-0027 seção 18 não têm
  cobertura executável em TestHierarquiaGruposH0027 nem em qualquer outra
  suíte de teste_renderizador.py:
  (a) "Corpo horizontal com dois grupos filhos" / "Grupo horizontal em corpo
      horizontal";
  (b) "Grupo vertical em corpo horizontal" — combinação horizontal → vertical;
  (c) "Três níveis com arranjos alternados (ex.: v → h → v)".
  test_g3_profundidade_maxima usa exclusivamente v→v→v. Nenhum teste usa
  _modelo_hierarquico("horizontal", ...) como corpo raiz com filhos grupo.
Autoridade ou requisito: H-0027 seção 19 critério 6 ("Todos os cenários da seção 18
  têm cobertura executável"); H-0027 seção 20.4 (lista de novos testes obrigatórios
  em teste_renderizador.py: "Corpo horizontal com dois grupos filhos";
  "Combinação horizontal → vertical"; "Três níveis com arranjos alternados").
Arquivo e linha: tela/teste_renderizador.py — ausência de testes com corpo horizontal
  e grupo filho; ausência de test_g3 com arranjos alternados.
Impacto: O critério de aceite 6 de H-0027 seção 19 não está integralmente
  satisfeito. A implementação do código é funcionalmente correta
  (_renderizar_container_horizontal despacha grupos recursivamente em linhas 881–893),
  mas sem cobertura executável esses caminhos não são verificados.
Correção necessária: Adicionar ao TestHierarquiaGruposH0027 em teste_renderizador.py:
  (a) Teste com corpo.arranjo="horizontal" e dois grupos filhos;
  (b) Teste com corpo.arranjo="horizontal" e grupo com arranjo="vertical" internamente;
  (c) Teste com 3 níveis e arranjos alternados (ex.: corpo=v, g1=h, g2=v).
Nova decisão necessária: Não — os caminhos de código já existem; apenas cobertura de
  teste precisa ser adicionada.
```

### ACH-002

```text
ID: ACH-002
Severidade: MÉDIA
Categoria: falta documental (relatório de implementação)
Descrição: IMP-0028 seção 5 lista resultados de apenas três suítes
  (loader, modelo, renderizador). A suíte teste_demo.py não aparece na tabela
  de resultados. H-0027 seção 22 item 11 requer "saída resumida de cada suíte
  (com contagem de aprovados)" e H-0027 seção 21 exige a execução de
  teste_demo.py. Executada pelo auditor: 303/303 aprovadas, código 0.
Autoridade ou requisito: H-0027 seção 22 item 11; H-0027 seção 21.
Arquivo e linha: docs/relatorios/IMP-0028-... seção 5.
Impacto: Documental — o relatório não registra formalmente o resultado de
  teste_demo.py. A funcionalidade está correta.
Correção necessária: Adicionar ao IMP-0028 seção 5 a linha de teste_demo.py
  (303 verificações, código 0).
Nova decisão necessária: Não.
```

### ACH-003

```text
ID: ACH-003
Severidade: MÉDIA
Categoria: falta documental (relatório de implementação)
Descrição: IMP-0028 não registra o estado Git inicial (H-0027 seção 22 item 2)
  com saída dos comandos `git log -1 --oneline`, `git status --short`,
  `git diff --stat`, `git diff --check`, `git diff --cached --stat`, como
  exigido pela seção 2.2 do handoff. Tampouco registra o estado Git final
  (H-0027 seção 22 item 15) com os mesmos comandos.
Autoridade ou requisito: H-0027 seção 22 itens 2 e 15.
Arquivo e linha: docs/relatorios/IMP-0028-... seção ausente.
Impacto: Documental. O estado Git verificado pelo auditor é coerente com o
  esperado pelo handoff.
Correção necessária: Adicionar ao IMP-0028 seções de estado Git inicial e final
  com a saída dos comandos.
Nova decisão necessária: Não.
```

### ACH-004

```text
ID: ACH-004
Severidade: BAIXA
Categoria: falta documental (relatório de implementação)
Descrição: IMP-0028 não declara explicitamente "Bloqueios encontrados: nenhum"
  como exigido por H-0027 seção 22 item 16. A seção poderia ao menos declarar
  que nenhum bloqueio foi encontrado (BLOCKED_REPOSITORY_STATE,
  ARCHITECTURE_REVIEW_REQUIRED, BLOCKED_SCOPE).
Autoridade ou requisito: H-0027 seção 22 item 16.
Arquivo e linha: docs/relatorios/IMP-0028-... (seção ausente).
Impacto: Mínimo — é razoável inferir que não houve bloqueio pela existência do
  relatório completo, mas a declaração explícita é exigida.
Correção necessária: Adicionar seção "Bloqueios: nenhum encontrado."
Nova decisão necessária: Não.
```

### ACH-005

```text
ID: ACH-005
Severidade: BAIXA
Categoria: observação sem correção obrigatória
Descrição: A reutilização de _validar_distribuicao_corpo para grupos produz
  mensagens com o texto interno "corpo.distribuicao" quando o erro ocorre em
  distribuição de grupo. Exemplo: "Grupo 'g1' em 'corpo': corpo.distribuicao.modo
  invalido: 'invalido'; valores aceitos: igual, percentual, fracao". O prefixo
  interno "corpo.distribuicao" é enganoso — refere-se à distribuição do grupo,
  não do corpo raiz. O contexto externo "Grupo 'g1' em 'corpo':" identifica
  corretamente o container afetado.
Autoridade ou requisito: H-0027 seção 13.1 item 5 ("mensagem de erro incluindo
  o caminho do grupo"). O caminho é incluído; o texto interno é ambíguo.
Arquivo e linha: tela/loader.py linha 276–280; tela/loader.py linha 148–216
  (_validar_distribuicao_corpo, mensagens com "corpo.distribuicao").
Impacto: Mínimo — diagnóstico funciona; localização do erro é possível. Nenhuma
  incorreção lógica.
Correção necessária: Não (observação). Melhoria opcional: parametrizar o prefixo
  de "corpo.distribuicao" em _validar_distribuicao_corpo para aceitar o caminho
  do container. Fora do escopo do H-0027.
Nova decisão necessária: Não.
```

### ACH-006

```text
ID: ACH-006
Severidade: BAIXA
Categoria: observação sem correção obrigatória
Descrição: O comentário interno de _montar_corpo_horizontal (linha 985 de
  renderizador.py) diz: "Grupo não é expandido (ADR-0015 D2): conta como slot
  com área visualmente vazia." Esse comentário é facticamente correto para a
  função em si (que não foi alterada), mas pode confundir leitores quanto ao
  comportamento do sistema após H-0027, onde grupos são expandidos recursivamente
  pelo caminho principal (_renderizar_container → _renderizar_container_horizontal).
Autoridade ou requisito: Sem conflito normativo. Observação de clareza.
Arquivo e linha: tela/renderizador.py linha 985.
Impacto: Mínimo — comentário interno de função não mais chamada pelo caminho
  principal. Não afeta comportamento.
Correção necessária: Não (observação). Melhoria opcional: acrescentar ao
  comentário que a função é preservada historicamente e não é chamada pelo
  caminho principal a partir de H-0027.
Nova decisão necessária: Não.
```

---

## 12. Validação manual

### Determinismo dos resultados

A recursão de layout é determinística: dada a mesma estrutura de modelo e
as mesmas dimensões, a saída é idêntica entre chamadas. Os testes verificam
isso explicitamente (`"saida e deterministica (duas chamadas identicas)"`).
Não é necessária validação humana para verificar correção da recursão de layout.

### Comportamento visual em TTY real

Os testes de renderizador executam verificações de conteúdo de texto; a
apresentação visual real em terminal depende do renderer de caracteres do
terminal. Os testes de teste_demo.py executam via PTY (seção 8.16) e
verificam comportamento de redimensionamento.

**Não há comportamento visual ou interativo que exija validação humana
obrigatória para as capacidades do H-0027.** Os resultados de renderização
hierárquica são determinísticos e verificados pelos testes existentes.

---

## 13. Estado Git final do QA

Idêntico ao inicial — o QA não alterou arquivos rastreados.

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git diff --check
(sem saída)

git diff --cached --stat
(sem saída)
```

O único arquivo novo criado pelo QA é este relatório
(`docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md`, não rastreado).

---

## 14. Arquivos fora do escopo

Nenhum arquivo proibido foi alterado pela implementação. As seis alterações
documentais rastreadas são preexistentes (aplicação ADR-0019). A implementação
alterou somente os seis arquivos autorizados em `tela/`.

---

## 15. Fixtures criadas

Nenhuma.

---

## 16. Classificação final

```text
I2_IMPLEMENTATION_PATCH_REQUIRED
```

**Justificativa**: A implementação das três camadas (loader, modelo, renderizador)
está funcionalmente correta e todas as 978 verificações executáveis aprovam.
As decisões D1–D7 da ADR-0019 estão integralmente atendidas. As quatro substituições
de testes históricos foram realizadas corretamente. As preservações das capacidades
anteriores foram verificadas.

O bloqueio é o **ACH-001**: três cenários obrigatórios da matriz H-0027 seção 18
não têm cobertura executável em nenhuma suíte:
(a) corpo horizontal com grupos filhos,
(b) combinação horizontal → vertical,
(c) três níveis com arranjos alternados.

Isso viola o critério 6 de H-0027 seção 19 ("Todos os cenários da seção 18 têm
cobertura executável") e os requisitos explícitos de H-0027 seção 20.4.

O patch necessário restringe-se à adição de testes em `tela/teste_renderizador.py`
(arquivo autorizado). Não requer alteração de handoff, ADR, contrato ou arquitetura.

---

## 17. Resumo final

```text
status:                        I2_IMPLEMENTATION_PATCH_REQUIRED
relatorio:                     docs/relatorios/RELATORIO_QA_H-0027_IMPLEMENTACAO.md
handoff_auditado:              docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
implementacao_auditada:        tela/loader.py, tela/modelo.py, tela/renderizador.py,
                               tela/teste_loader.py, tela/teste_modelo.py,
                               tela/teste_renderizador.py
decisoes_D1_D7:                D1 ATENDIDA; D2 ATENDIDA; D3 ATENDIDA; D4 ATENDIDA;
                               D5 ATENDIDA; D6 ATENDIDA; D7 ATENDIDA
achados_bloqueantes:           NENHUM
achados_altos:                 ACH-001 (cobertura faltante para cenários de corpo
                               horizontal e três níveis alternados)
achados_medios:                ACH-002 (teste_demo.py ausente do IMP-0028);
                               ACH-003 (estado Git ausente do IMP-0028)
achados_baixos:                ACH-004 (bloqueios não declarados no IMP-0028);
                               ACH-005 (mensagem enganosa "corpo.distribuicao" em grupo);
                               ACH-006 (comentário desatualizado em _montar_corpo_horizontal)
observacoes:                   Implementação funcionalmente correta; código dos três
                               caminhos não cobertos é correto; falta apenas cobertura.
arquivos_fora_do_escopo:       NENHUM
fixtures_criadas:              NENHUMA
testes:                        978 aprovadas / 978 total / 0 falhas (127+81+467+303)
git:                           commit-base 40015b6 confirmado; stage vazio; diff --check
                               limpo; 6 docs preexistentes + 6 arquivos tela/ modificados;
                               somente IMP-0028 novo não rastreado
validacao_manual:              I5 NÃO NECESSÁRIO — resultados determinísticos e cobertos
correcao_necessaria:           SIM — adicionar 3+ testes em tela/teste_renderizador.py
                               (a) corpo horizontal com 2 grupos filhos;
                               (b) corpo horizontal → grupo vertical;
                               (c) 3 níveis com arranjos alternados
nova_decisao_do_usuario_necessaria: NÃO
proxima_categoria:             patch de teste + novo QA_IMPLEMENTACAO
```
