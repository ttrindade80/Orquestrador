---
name: relatorio-auditoria-h-0020-handoff
description: Relatório de auditoria do handoff H-0020 — Preenchimento vertical das áreas alocadas no corpo horizontal — verifica implementabilidade, restrição de escopo e coerência com ADR-0015, H-0019, QA do H-0019, levantamento pós-H-0019 e contratos vigentes
metadata:
  type: relatorio
  scope: scripts
  status: HANDOFF_APPROVED_WITH_NOTES
  data: "2026-07-10"
---

# RELATORIO_AUDITORIA_H-0020_HANDOFF

## Status

```
HANDOFF_APPROVED_WITH_NOTES
```

---

## Resumo executivo

O handoff H-0020 especifica a correção de `_montar_corpo_horizontal` em
`renderizador.py` para que cada área/coluna alocada seja preenchida verticalmente
até `l_corpo_disponivel` (altura disponível do corpo), não apenas até `altura_max`
(máximo entre colunas). A implementação também neutraliza o preenchimento externo
H-0015 no modo horizontal para evitar duplo preenchimento.

O handoff está implementável, restrito e coerente com ADR-0015, H-0019, QA do
H-0019, levantamento pós-H-0019 e contratos vigentes. O escopo positivo está
corretamente limitado a `tela/renderizador.py` e `tela/teste_renderizador.py`.
O escopo negativo enumera explicitamente todos os itens proibidos. O algoritmo
é suficientemente preciso e testável. A proteção da barra_de_menus está correta,
incluindo grafia `_normalizar_distribuicao` com `r` em todos os pontos normativos.
Os treze testes exigidos cobrem todos os critérios de aceite.

Há três achados de severidade NOTA, nenhum bloqueante.

---

## Base verificada

| Item | Valor |
|---|---|
| HEAD observado | `624e0a5  docs: registra levantamento pos H-0019` |
| Commit base declarado no handoff | `624e0a5  docs: registra levantamento pos H-0019` |
| Coincidência | SIM |
| Workspace antes da auditoria | `?? docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md` |
| Workspace esperado declarado | Coincide exatamente |

---

## Arquivos analisados

### Handoff auditado

```
docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
```

### Documentação normativa

```
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/NOMENCLATURA.md
docs/contratos/contrato_composicao_corpo.md (v0.3)
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
```

### Artefatos do H-0019

```
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md
docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0019_AJUSTES_LAYOUT_E_DIMENSAO.md
```

### Código — leitura integral

```
tela/renderizador.py  (linhas 240–300, 680–946 lidas na íntegra)
```

### Lidos para proteção de escopo (não alterar)

```
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

## Comandos executados

### Primeira trava obrigatória

```bash
git log --oneline -8
git status --short
git diff --stat
git diff --name-only
```

**Resultado:**

```
624e0a5 docs: registra levantamento pos H-0019
29a8a79 feat: implementa layout horizontal plano do corpo
9d4c74d docs: formaliza composicao hierarquica do corpo
3b98856 docs: registra levantamento pos H-0018
46e0cb9 feat: cobre distribuicao da barra de menus
c8a20fa test: adiciona explorador da barra de menus
ab5ad68 feat: renderiza barra de menus horizontal responsiva
b2eb458 feat: ocupa altura do terminal pelo corpo
---
?? docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
---   (sem saída)
---   (sem saída)
```

Workspace conforme — apenas o handoff não rastreado. Auditoria prosseguida.

### Grep obrigatório 1 — nomenclatura de funções protegidas

```bash
grep -n "_normaliza_distribuicao\|_normalizar_distribuicao\|_validar_distribuicao\|_linhas_barra" \
  docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md || true
```

**Resultado (seleção relevante):**

```
220:NÃO alterar _normalizar_distribuicao.
221:NÃO alterar _validar_distribuicao.
222:NÃO alterar _linhas_barra.
259:- `_normalizar_distribuicao` (renderizador.py) — nome real com `r`
260:- `_validar_distribuicao` (renderizador.py)
474:_normalizar_distribuicao     (função real em renderizador.py — com r)
484:**Atenção terminológica**: a função real chama-se `_normalizar_distribuicao`
486:que handoffs e relatórios anteriores citaram incorretamente `_normaliza_distribuicao`
488:`_normalizar_distribuicao`. Qualquer busca de auditoria deve usar o nome correto.
569:    Confirmar que nenhuma alteração ocorreu em _normalizar_distribuicao,
570:    _validar_distribuicao ou _linhas_barra.
752:**Mitigação**: usar sempre `_normalizar_distribuicao` (com `r`) em todos os
```

Grafia correta `_normalizar_distribuicao` (com `r`) em todos os pontos normativos.
A grafia histórica incorreta `_normaliza_distribuicao` aparece apenas como nota
sobre o QA-001 do H-0019. Conforme.

### Grep obrigatório 2 — itens de escopo negativo

```bash
grep -n "largura declarativa\|dimensao\|dimensão\|orquestrador.json\|H-0021\|grupo hierárquico\|reticências\|\.\.\." \
  docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md || true
```

**Resultado (seleção relevante):**

```
233:NÃO adicionar campo largura/dimensao no JSON.
234:NÃO alterar orquestrador.json.
242:NÃO implementar reticências (...) para terminal pequeno.
461:...permanecem fora de escopo, conforme ADR-0015 D13.
764:  (largura declarativa da tela exige ciclo documental prévio antes de H-0021)
778:Terminal pequeno com reticências (...).
790:**Nota sobre largura declarativa**: o levantamento pós-H-0019 identificou...
```

Todas as ocorrências estão no contexto de exclusão de escopo ou nota explicativa.
Nenhuma ocorrência indica inclusão indevida desses temas no escopo do H-0020.

### Verificação final de estado

```bash
git diff --stat   → (sem saída)
git diff --name-only  → (sem saída)
git status --short → ?? docs/handoff/H-0020-preenchimento-vertical-areas-corpo-horizontal.md
```

Workspace inalterado durante toda a auditoria.

---

## Verificação de rastreabilidade

| Critério | Encontrado | Conforme |
|---|---|---|
| ID é H-0020 | `\| ID \| H-0020 \|` — linha 15 | ✓ |
| Título é "Preenchimento vertical das áreas alocadas no corpo horizontal" | Linha 1 do handoff | ✓ |
| Base observada coerente com histórico | `624e0a5 docs: registra levantamento pos H-0019` — coincide com HEAD | ✓ |
| H-0019 aparece como ciclo anterior | `\| Commit H-0019 \| \`29a8a79 feat: implementa layout horizontal plano do corpo\`` | ✓ |
| Levantamento pós-H-0019 citado | `\| Levantamento pós-H-0019 \| \`docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0019_AJUSTES_LAYOUT_E_DIMENSAO.md\`` | ✓ |
| Implementação bloqueada até auditoria aprovada | "Este handoff deve ser auditado antes de qualquer implementação." (seção "Exigência de auditoria") | ✓ |
| Não há tentativa de reabrir H-0019 | H-0019 tratado exclusivamente como ciclo encerrado e commitado | ✓ |

**Conclusão**: rastreabilidade plenamente verificada.

---

## Verificação de compatibilidade com ADR-0015

| Decisão ADR-0015 | Handoff H-0020 | Conforme |
|---|---|---|
| D5 — distribuição aloca área | Citada explicitamente como base normativa da contradição atual ("distribuição aloca área, não apenas conteúdo") | ✓ |
| D5 — sobra vertical vira linhas em branco dentro da área alocada | Objetivo central do handoff: fill vertical dentro das colunas, não fora | ✓ |
| D5 — elemento funcional preserva área alocada | Regra visual esperada (`╭────────╮╭────────╮` com fill interno) | ✓ |
| D9 — áreas adjacentes preservam particionamento contíguo | Exemplo visual correto mostra bordas coladas nas linhas de fill | ✓ |
| D9 — molduras sem vãos externos | "áreas adjacentes permanecem coladas em todas as linhas preenchidas" (teste 4) | ✓ |
| D10 — preenchimento vertical dentro da faixa | Algoritmo revisado: `linhas.append(" " * larguras[i])` até `altura_alvo` | ✓ |
| D13 — terminal pequeno com `...` fora de escopo | "Reticências (`...`) permanecem fora de escopo, conforme ADR-0015 D13." | ✓ |
| D14/D15 — sincronização de cortes fora de escopo | Listada explicitamente no escopo negativo (linha 240) | ✓ |
| D12 — paginação dentro da área alocada | `RenderizadorErro` determinístico preservado; nenhum truncamento silencioso | ✓ |

**Conclusão**: handoff plenamente compatível com ADR-0015.

---

## Verificação de escopo positivo

### Arquivos autorizados para alteração

| Arquivo | Declarado no handoff | Conforme |
|---|---|---|
| `tela/renderizador.py` | Listado explicitamente (seção "Escopo positivo") | ✓ |
| `tela/teste_renderizador.py` | Listado explicitamente | ✓ |
| `docs/relatorios/IMP-0020-preenchimento-vertical-areas-corpo-horizontal.md` | Listado explicitamente | ✓ |

### Alterações previstas verificadas

| Alteração | Encontrada no handoff | Conforme |
|---|---|---|
| Propagar `l_corpo_disponivel` até `_montar_corpo_horizontal` | Item 1 do escopo positivo; detalhada na especificação funcional | ✓ |
| Estender assinatura com `altura_disponivel: int \| None = None` | Item 2; especificação funcional linha 312 | ✓ |
| Normalizar colunas até `l_corpo_disponivel` quando fornecido | Item 3; pseudocódigo `altura_alvo` | ✓ |
| Neutralizar fill H-0015 externo no modo horizontal | Item 4; seção `renderizar_tela` — fill H-0015 | ✓ |
| Preservar comportamento H-0019 quando `altura_disponivel = None` | Seção "Preservações obrigatórias", nota `TestArranjoH0019` | ✓ |
| Preservar vertical/default integralmente | Seção "Fluxo com arranjo vertical/None/sobreposto (preservação H-0015)" | ✓ |
| Preservar alias `sobreposto` → `vertical` | Critério de aceite 7; teste `test_sobreposto_preserva_comportamento_atual` | ✓ |
| Preservar alias `lado_a_lado` → comportamento horizontal | Critério de aceite 8; teste `test_lado_a_lado_preserva_comportamento_horizontal` | ✓ |

**Conclusão**: escopo positivo correto, completo e verificável.

---

## Verificação de escopo negativo

Verificação linha a linha dos 33 itens do escopo negativo declarados (linhas 214–251 do handoff):

| Categoria | Itens verificados | Conforme |
|---|---|---|
| loader.py, modelo.py | Ambos listados como "NÃO alterar" (linhas 217–218) | ✓ |
| Funções protegidas da barra_de_menus | `barra_de_menus.distribuicao`, `_normalizar_distribuicao`, `_validar_distribuicao`, `_linhas_barra`, `_validar_ancoras` — todos listados (linhas 219–223) | ✓ |
| Artefatos da barra_de_menus | `explorar_barra_de_menus.py`, `teste_explorar_barra_de_menus.py`, `contrato_barra_de_menus.md`, `contrato_chip.md` — todos listados (linhas 224–227) | ✓ |
| Documentação normativa | contratos, ADRs, NOMENCLATURA.md — listados (linhas 228–230) | ✓ |
| JSONs de configuração | "JSONs de configuração (config/)", `orquestrador.json` — listados (linhas 231, 234) | ✓ |
| Campo no JSON | "configuração declarativa de largura", "campo largura/dimensao no JSON" — listados (linhas 232–233) | ✓ |
| Distribuição | "percentual", "por fração/pesos" — listados (linhas 235–236) | ✓ |
| Grupos hierárquicos e aninhamento | "grupos hierárquicos", "arranjo dentro de grupo", "profundidade de 3 níveis" — listados (linhas 237–239) | ✓ |
| Sincronização, paginação, terminal pequeno | "sincronização de cortes", "paginação real", "reticências (...)" — listados (linhas 240–242) | ✓ |
| Elementos de runtime | "console real", "navegação por [✥]", "foco", "seleção", "filtros", "ações", "registry novo" — listados (linhas 243–249) | ✓ |
| Controle processual | "NÃO fazer commit" — listado (linha 250) | ✓ |

Nenhum item proibido aparece fora das listas de exclusão.

**Conclusão**: escopo negativo completo e sem violações.

---

## Verificação do algoritmo esperado

| Critério | Avaliação | Conforme |
|---|---|---|
| `renderizar_tela` calcula `l_corpo_disponivel` | Especificação funcional mostra `_l_corpo_disponivel = altura - l_cab - l_barra` no branch horizontal com `altura` | ✓ |
| No modo horizontal, `l_corpo_disponivel` é repassado para `_montar_corpo_horizontal` | `_montar_corpo_horizontal(..., altura_disponivel=_l_corpo_disponivel)` | ✓ |
| `_montar_corpo_horizontal` decide altura alvo | `altura_alvo = altura_disponivel if altura_disponivel is not None else altura_max` | ✓ |
| Com `altura_disponivel`, alvo é a altura disponível do corpo | `if altura_alvo < altura_max: altura_alvo = altura_max` (sem truncamento) | ✓ |
| Cada coluna preenchida até altura alvo | `while len(linhas) < altura_alvo: linhas.append(...)` | ✓ |
| Linhas preenchidas preservam largura da faixa | `linhas.append(" " * larguras[i])` — mesma lógica do H-0019 | ✓ |
| Concatenação mantém bordas adjacentes coladas | `for r in range(altura_alvo): linha += linhas[r]` — mesma lógica, bordas surgem naturalmente | ✓ |
| Não há linhas finais `" " * total_w` após bloco horizontal | Fill H-0015 neutralizado via `and arranjo_corpo != "horizontal"` | ✓ |
| `altura_disponivel = None` preserva comportamento H-0019 | `altura_alvo = altura_max` quando `altura_disponivel is None` — test_horizontal_sem_altura_preserva_h0019 | ✓ |
| Em vertical/default, fill H-0015 permanece preservado | Seção "Fluxo com arranjo vertical/None/sobreposto" — `else` branch intacto | ✓ |

**Nota sobre o fluxo de `linhas_barra`**: o handoff identifica corretamente o risco R-4
(dupla chamada a `_linhas_barra`). A especificação mostra `linhas_barra = None # será
calculada depois` no branch horizontal com `altura is None`, implicando que o executor
precisará adicionar uma guarda na linha 897 atual do renderer (`if linhas_barra is None:`).
O risco está documentado, a mitigação está descrita, e o algoritmo é implementável.
Classificado como NOTA (ver Achado A-003).

**Conclusão**: algoritmo suficientemente preciso e testável.

---

## Verificação de proteção da barra_de_menus

| Artefato | Status no handoff | Grafia | Conforme |
|---|---|---|---|
| `barra_de_menus.distribuicao` | "NÃO alterar" (escopo negativo, linha 219) | — | ✓ |
| `_normalizar_distribuicao` | "NÃO alterar" (linha 220); "nome real com `r`" (linha 259); "função real em renderizador.py — com r" (linha 474) | `r` presente — CORRETO | ✓ |
| `_validar_distribuicao` | "NÃO alterar" (linha 221); listada em preservações e proteção | — | ✓ |
| `_linhas_barra` | "NÃO alterar" (linha 222); listada em preservações e algoritmo (como uso, não alteração) | — | ✓ |
| `_validar_ancoras` | "NÃO alterar" (linha 223); listada em preservações | — | ✓ |
| `tela/explorar_barra_de_menus.py` | "NÃO alterar" (escopo negativo, linha 224); artefatos proibidos | — | ✓ |
| `tela/teste_explorar_barra_de_menus.py` | "NÃO alterar" (escopo negativo, linha 225); artefatos proibidos | — | ✓ |
| `docs/contratos/contrato_barra_de_menus.md` | "NÃO alterar" (linha 226); artefatos proibidos | — | ✓ |
| `docs/contratos/contrato_chip.md` | "NÃO alterar" (linha 227); artefatos proibidos | — | ✓ |

**Nota terminológica**: a seção "Proteção da barra_de_menus" (linha 484–488) cita
explicitamente o QA-001 do H-0019 — a grafia incorreta `_normaliza_distribuicao`
(sem `r`) é referenciada apenas como nota histórica documental. Todos os pontos
normativos do H-0020 usam corretamente `_normalizar_distribuicao` (com `r`). O handoff
instrui auditoria a usar o nome correto. Conforme.

**Conclusão**: proteção da barra_de_menus correta e explícita.

---

## Verificação de testes exigidos

| # | Teste exigido | Cenário | Criterio de aceite coberto | Conforme |
|---|---|---|---|---|
| 1 | `test_horizontal_alto_mantém_bordas_ate_altura_disponivel` | altura=30; bordas em todas as linhas; nenhum fill externo | CA-1, CA-3, CA-4 | ✓ |
| 2 | `test_horizontal_preenchimento_dentro_das_colunas` | fill dentro das áreas, não fora | CA-2 | ✓ |
| 3 | `test_horizontal_sem_linhas_total_w_apos_bloco` | altura=40; nenhuma linha `" " * total_w` após bloco | CA-2 | ✓ |
| 4 | `test_horizontal_bordas_adjacentes_em_linhas_preenchidas` | altura=25; bordas coladas nas linhas fill | CA-4 | ✓ |
| 5 | `test_horizontal_largura_total_em_todas_linhas_preenchidas` | altura=20; `len(ln) == total_w` | CA-3 | ✓ |
| 6 | `test_horizontal_colunas_diferentes_preenchidas_mesma_altura` | colunas com alturas diferentes; ambas até `l_corpo_disponivel` | CA-5 | ✓ |
| 7 | `test_vertical_preserva_comportamento_atual` | `arranjo="vertical"`; fill H-0015 intacto | CA-7 | ✓ |
| 8 | `test_sobreposto_preserva_comportamento_atual` | `arranjo="sobreposto"` | CA-7 | ✓ |
| 9 | `test_none_preserva_comportamento_atual` | `arranjo=None` | CA-7 | ✓ |
| 10 | `test_lado_a_lado_preserva_comportamento_horizontal` | `arranjo="lado_a_lado"` → horizontal com fill | CA-8 | ✓ |
| 11 | `test_horizontal_sem_altura_preserva_h0019` | sem `altura`; normaliza até `altura_max` apenas | CA-6 | ✓ |
| 12 | `test_barra_de_menus_preservada_apos_h0020` | chips inalterados; 38/38 `teste_explorar_barra_de_menus.py` | CA-9, CA-10 | ✓ |
| 13 | `test_baseline_completo_continua_passando` | 589 casos anteriores passando | CA-11 | ✓ |

Todos os treze critérios de aceite do handoff têm pelo menos um teste correspondente.
A nota sobre `TestArranjoH0019` está corretamente incluída: o teste existente
`test_arranjo_horizontal_padding_inferior` deve continuar passando sem alteração.

**Conclusão**: cobertura de testes suficiente.

---

## Verificação da relação com H-0020 citado na ADR-0015

A ADR-0015 Decisão 17 diz: "H-0020 será responsável por criar/expandir grupos
conforme planejamento futuro."

| Critério | Avaliação | Conforme |
|---|---|---|
| Handoff registra a mudança de escopo | Seção "Fora de escopo futuro" (linhas 767–773): "H-0020 estava planejado para isso pela ADR-0015 D17, mas o levantamento pós-H-0019 definiu H-0020 como preenchimento vertical." | ✓ |
| Não tenta implementar grupos hierárquicos | Escopo negativo: "NÃO implementar grupos hierárquicos" (linha 237) | ✓ |
| Deixa grupos para ciclo futuro | "A redistribuição interna de grupo fica para ciclo posterior." | ✓ |
| Não cria conflito prático com ADR-0015 | ADR-0015 D17 não é vinculante sobre numeração — registra intenção; levantamento pós-H-0019 redefiniu o escopo processualmente | ✓ |

**Nota sobre tensão normativa residual**: `contrato_composicao_corpo.md` seção 9
(pendências) ainda lista "H-0020 será responsável por criar/expandir grupos" —
referência que precede a redefinição do levantamento pós-H-0019. Não é conflito
insolúvel: a redefinição é documentada e rastreável no levantamento pós-H-0019
e no próprio H-0020. O contrato pode ser atualizado em ciclo documental futuro.
Classificado como NOTA (ver Achado A-001).

**Classificação**: NOTA — não exige `ARCHITECTURE_REVIEW_REQUIRED`. A redefinição
é processualmente documentada, tecnicamente consistente com ADR-0015 e não afeta
escopo técnico do H-0020.

---

## Achados

| ID | Severidade | Descrição | Evidência | Impacto | Correção recomendada |
|---|---|---|---|---|---|
| A-001 | NOTA | `contrato_composicao_corpo.md` seção 9 (pendências) menciona "H-0020 será responsável por criar/expandir grupos" — referência que precede a redefinição do escopo de H-0020 feita pelo levantamento pós-H-0019. | `contrato_composicao_corpo.md` linhas 852–856 vs. `RELATORIO_LEVANTAMENTO_POS_H0019_AJUSTES_LAYOUT_E_DIMENSAO.md` seção "Separação recomendada" e H-0020 seção "Fora de escopo futuro" linhas 767–773. | Tensão normativa documental entre contrato (pré-redefinição) e handoff (pós-redefinição). Não afeta implementabilidade do H-0020 nem cria conflito técnico. | Atualizar `contrato_composicao_corpo.md` seção 9 em ciclo documental futuro para refletir que grupos ficaram para ciclo posterior. |
| A-002 | NOTA | `IMP-0019` lista `_normaliza_distribuicao` (sem `r`) em "Funções intocadas" — inconsistência documental pré-existente. O H-0020 usa corretamente `_normalizar_distribuicao` em todos os pontos normativos e instrui auditoria a usar o nome correto. | `IMP-0019-layout-horizontal-plano-corpo.md` linha 224: `- \`_normaliza_distribuicao\` ✓`. Já registrado como QA-001 no `RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md`. | Apenas inconsistência documental no IMP-0019 — pré-existente e já documentada. O H-0020 não herda nem reproduz o erro. | Nenhuma ação necessária no H-0020. A inconsistência do IMP-0019 pode ser corrigida em ciclo documental futuro. |
| A-003 | NOTA | O risco R-4 (dupla chamada a `_linhas_barra`) é corretamente identificado no handoff mas a especificação funcional não explicita o padrão de código para a linha 897 do renderer atual. O executor precisará adicionar uma guarda (`if linhas_barra is None:`) antes de `linhas_barra = _linhas_barra(...)` na linha 897. | Handoff linhas 406–411 (R-4) e `renderizador.py` linha 897: `linhas_barra = _linhas_barra(modelo.barra_de_menus, content_w)` executada incondicionalmente; especificação funcional não mostra padrão explícito para esta linha. | Sem a guarda, `_linhas_barra` seria chamada duas vezes no modo horizontal com `altura` fornecida — sem consequência funcional, mas ineficiente e inconsistente com a mitigação declarada. | O executor deve implementar a guarda. Guia suficiente está no handoff (R-4 e mitigação). Não exige correção do handoff. |

**Resumo por severidade:**

| Severidade | Quantidade | Bloqueia aprovação |
|---|---|---|
| BLOQUEANTE | 0 | — |
| ALTO | 0 | — |
| MÉDIO | 0 | — |
| BAIXO | 0 | — |
| NOTA | 3 | Não |

---

## Decisão

```
APROVADO_COM_NOTAS
```

**Justificativa:**

- Nenhum achado BLOQUEANTE, ALTO ou MÉDIO.
- Escopo positivo estritamente limitado a `renderizador.py` e `teste_renderizador.py`.
- Escopo negativo completo e explícito — 33 itens verificados.
- Nenhuma alteração proposta em loader/modelo/contratos/ADRs/JSONs.
- Algoritmo implementável sem decisão arquitetural aberta.
- Proteção da barra_de_menus correta — `_normalizar_distribuicao` (com `r`) em todos
  os pontos normativos.
- Treze testes exigidos cobrem todos os onze critérios de aceite.
- Tema B (largura declarativa) explicitamente fora de escopo.
- Grupos hierárquicos explicitamente fora de escopo.
- Redefinição de H-0020 (vs ADR-0015 D17) corretamente documentada.
- Três achados NOTA não comprometem implementabilidade.

**Critérios de aprovação verificados:**

- [x] Nenhum achado bloqueante, alto ou médio
- [x] Escopo restrito a `renderizador.py` e `teste_renderizador.py`
- [x] Nenhuma alteração proposta em loader/modelo/contratos/ADR/JSON
- [x] Algoritmo implementável sem decisão arquitetural aberta
- [x] Proteção da `barra_de_menus` explícita e verificável
- [x] Testes suficientes para todos os critérios de aceite
- [x] Largura declarativa fora de escopo
- [x] Grupos hierárquicos fora de escopo

---

## Conclusão

O handoff H-0020 está aprovado com notas. A especificação é suficientemente precisa
para permitir implementação direta sem ambiguidade arquitetural. O algoritmo de
preenchimento vertical dentro das colunas alocadas (em vez de fill externo `" " * total_w`)
está corretamente fundamentado na ADR-0015 D5 e D10. A neutralização do fill H-0015
externo está corretamente especificada. O comportamento de regressão para H-0019 e H-0015
está coberto por testes explícitos.

Os três achados NOTA são todos pré-existentes ou de detalhe de implementação — nenhum
exige correção do handoff antes de prosseguir.

A implementação **só pode iniciar após autorização explícita do usuário**, conforme
exigência declarada no handoff.
