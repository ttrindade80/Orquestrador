# RELATORIO_AUDITORIA_H-0019_HANDOFF

```text
auditoria_por:   Claude Code (papel auditoria)
data:            2026-07-09
ciclo:           H-0019
titulo:          Layout horizontal plano do corpo
commit_base:     3b98856  docs: registra levantamento pos H-0018
handoff:         docs/handoff/H-0019-layout-horizontal-plano-corpo.md
```

---

## Status

```
HANDOFF_APPROVED_WITH_NOTES
```

---

## Resumo executivo

O handoff H-0019 está implementável. A numeração é correta, a rastreabilidade está
completa, o escopo está fechado, a barra_de_menus está protegida, os testes exigidos
cobrem os cenários obrigatórios e não há achados bloqueantes ou altos.

Há um achado de severidade MÉDIO (A-001): o handoff generaliza o algoritmo de
distribuição de espaço para N+1 vãos com N>=2, incluindo teste obrigatório para N=3,
enquanto o contrato e a NOMENCLATURA especificam explicitamente "3 vãos" para o caso
de "2 colunas/elementos". A generalização é matematicamente trivial e compatível com o
princípio de "vãos iguais", mas não está explicitamente autorizada pelo contrato para
N>2. O IMP-0019 deve documentar essa extensão como decisão local explícita neste ciclo.

Há dois achados de severidade BAIXO (A-002, A-003): omissão de dois arquivos na seção
"Preservações obrigatórias" (cobertos por outras seções) e ausência de teste para o
caso borda N=1 com arranjo="horizontal".

A implementação pode avançar diretamente após ciência das notas.

---

## Base verificada

| Item | Valor |
|------|-------|
| HEAD no momento da auditoria | `3b98856  docs: registra levantamento pos H-0018` |
| HEAD declarado no handoff | `3b98856` |
| Coincidência de base | SIM |
| Workspace | `?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md` (apenas o próprio handoff não rastreado) |

---

## Arquivos analisados

### Handoff e relatório auxiliar

```
docs/handoff/H-0019-layout-horizontal-plano-corpo.md          (lido na íntegra)
docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO.md  (lido na íntegra)
```

### Handoff e QA do ciclo anterior

```
docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md  (parcial — cabeçalho e contexto)
docs/relatorios/RELATORIO_QA_H-0018_POS_CORRECOES.md                    (parcial — status e arquivos)
```

### Contratos e NOMENCLATURA

```
docs/NOMENCLATURA.md                         (lido na íntegra)
docs/contratos/contrato_composicao_corpo.md  (lido na íntegra)
```

### Código inspecionado

```
tela/loader.py         (linhas 84, 140–162, 240–360 — arranjo, _validar_grupo, TelaEstruturaInvalida)
tela/modelo.py         (grep: arranjo, Corpo — linhas relevantes)
tela/renderizador.py   (linhas 775–844 — função renderizar_tela, laço de corpo)
config/telas/destino_minimo.json  (campo arranjo verificado)
config/telas/stub_b.json          (campo arranjo verificado)
```

---

## Comandos executados

```bash
# Estado do repositório
git log --oneline -8
# 3b98856 docs: registra levantamento pos H-0018
# 46e0cb9 feat: cobre distribuicao da barra de menus
# c8a20fa test: adiciona explorador da barra de menus
# ab5ad68 feat: renderiza barra de menus horizontal responsiva
# b2eb458 feat: ocupa altura do terminal pelo corpo
# 4762583 docs: registra ocupacao vertical e barra responsiva
# 8a6403a feat: migra arranjo vertical e barra declarativa
# ceaf0be docs: registra ADRs de arranjo e barra declarativa

git status --short
# ?? docs/handoff/H-0019-layout-horizontal-plano-corpo.md

git diff --stat
# (sem saída — workspace limpo exceto handoff untracked)

git diff --name-only
# (sem saída)
```

```bash
# Verificação de referências indevidas
grep -RIn "H-0020\|RELATORIO_LEVANTAMENTO_H-0019" \
  docs/handoff/H-0019-layout-horizontal-plano-corpo.md \
  docs/relatorios/RELATORIO_LEVANTAMENTO_POS_H0018_PROXIMO_CORPO.md
# (sem saída — nenhuma referência indevida)
```

```bash
# Verificação de toque indevido na barra
grep -n "_normaliza_distribuicao\|_validar_distribuicao\|_linhas_barra\|barra_de_menus.distribuicao" \
  docs/handoff/H-0019-layout-horizontal-plano-corpo.md
# Todas as ocorrências são na forma de PROIBIÇÃO (escopo negativo,
# preservações obrigatórias, riscos). Nenhuma prescreve alteração.
```

```bash
# Verificação de termos de layout do corpo
grep -n "corpo.arranjo\|horizontal\|vertical\|sobreposto\|lado_a_lado\|N+1\|percentual\|fracao\|aninhamento" \
  docs/handoff/H-0019-layout-horizontal-plano-corpo.md
# Resultados confirmam uso correto e consistente de todos os termos.
```

```bash
# Estado do código — confirmação das afirmações do handoff
# loader.py linha 347: arranjo = corpo.get("arranjo")  → SEM validação
# renderizador.py linha 779: for elemento in modelo.corpo.elementos  → laço sequencial
# modelo.py: Corpo.arranjo: str | None  → armazena sem validar
# destino_minimo.json: arranjo = "sobreposto"
# stub_b.json: arranjo = "sobreposto"
```

---

## Verificação de numeração e rastreabilidade

| Item | Esperado | Encontrado | Status |
|------|----------|------------|--------|
| ID do handoff | H-0019 | H-0019 | OK |
| Relatório auxiliar pós-H-0018 sem número H | Confirmar | Confirmado: não consome número H (nota explícita no relatório) | OK |
| Referência a `RELATORIO_LEVANTAMENTO_H-0019` | Ausente | Ausente (grep vazio) | OK |
| Referência a H-0020 | Ausente | Ausente (grep vazio) | OK |
| Base observada declarada | `3b98856` | `3b98856` | OK |
| Base observada coincide com HEAD | Sim | Sim | OK |
| Relatório IMP-0019 exigido | `IMP-0019-layout-horizontal-plano-corpo.md` | Exigido explicitamente na seção de metadados e relatório de implementação | OK |

A nota sobre base observada (por que é `3b98856` e não `46e0cb9`) é clara e correta.

---

## Verificação de aderência aos contratos

### contrato_composicao_corpo.md — seção 5.6

O contrato especifica:
> "o espaço horizontal disponível é distribuído em **3 vãos iguais**: borda↔coluna_1, coluna_1↔coluna_2, coluna_2↔borda."

O handoff cita corretamente esta seção e apresenta N+1 como generalização de 3 vãos
para o caso canônico de N=2. O critério de aceite 6 especifica:
> "Para N=2: 3 vãos iguais (borda↔col_1, col_1↔col_2, col_2↔borda)."

Para N=2 (caso contratual): CONFORME.
Para N>2 (generalização): ver achado A-001.

### NOMENCLATURA.md — seção 10

A NOMENCLATURA especifica:
> "Em modo lado a lado (2 colunas), o espaço horizontal se distribui em 3 vãos, igualmente."

A expressão "(2 colunas)" é descritiva do caso especificado. O handoff extende para
N colunas. Ver achado A-001.

### ADR-0011 — terminologia arranjo

O handoff usa corretamente os termos finais (`vertical`, `horizontal`) e os aliases
transicionais (`sobreposto` → vertical, `lado_a_lado` → horizontal). CONFORME.

### ADR-0014 — filtro por substring proibido

O handoff adverte explicitamente (riscos R-1 e R-2) contra uso de substring
`"horizontal"` como critério de busca/alteração. CONFORME.

---

## Verificação de escopo positivo

| Item | Exigido | No handoff | Status |
|------|---------|------------|--------|
| Validar `corpo.arranjo` no loader | Sim | Sim — seção "loader.py", constante `ARRANJOS_CORPO_VALIDOS`, exceção `TelaEstruturaInvalida` | OK |
| Renderer lê `modelo.corpo.arranjo` | Sim | Sim — seção "renderizador.py", branch `if arranjo_corpo == "horizontal"` | OK |
| Aliases transicionais funcionam deterministicamente | Sim | Sim — normalização explícita no renderer | OK |
| Testes novos em teste_loader.py | Sim | Sim — 8 testes listados | OK |
| Testes novos em teste_renderizador.py | Sim | Sim — 12 testes listados | OK |
| Criar IMP-0019 | Sim | Sim — estrutura completa exigida | OK |
| Criar/adaptar JSON de teste | Sim | Sim — Opção A (JSON novo) ou Opção B (in-memory) | OK |

---

## Verificação de escopo negativo

| Item proibido | No handoff | Status |
|--------------|------------|--------|
| Distribuição percentual/fração | NÃO implementar — listado explicitamente | OK |
| Aninhamento de grupos com arranjo próprio | NÃO implementar | OK |
| Console real | NÃO implementar | OK |
| Foco entre elementos | NÃO implementar | OK |
| Navegação por [✥] | NÃO implementar | OK |
| Seleção | NÃO implementar | OK |
| Paginação | NÃO implementar | OK |
| Filtros | NÃO implementar | OK |
| Registry novo | NÃO implementar | OK |
| Migração de posicao_dashboard | NÃO implementar | OK |
| Alterar ADR / contrato / NOMENCLATURA | NÃO alterar | OK |
| Reabrir H-0011 | NÃO reabrir | OK |
| Recriar H-0011A | NÃO recriar | OK |
| Usar H-0011/H-0011A como base | NÃO usar | OK |
| Fazer commit | NÃO fazer | OK |

---

## Verificação da regra de 3 vãos iguais

### Caso N=2 (contratual)

O handoff preserva exatamente a regra contratual de 3 vãos iguais para N=2:
- Critério de aceite 6: "Para N=2: 3 vãos iguais (borda↔col_1, col_1↔col_2, col_2↔borda)."
- Teste `test_arranjo_horizontal_vaos_iguais`: verifica empiricamente a igualdade de vãos.
- O algoritmo produz matematicamente 3 vãos iguais para N=2 (demonstrável pelo código do Passo 2–6).

CONFORME para N=2.

### Caso N>2 (generalização)

O handoff generaliza para "N+1 vãos iguais" com N elementos, incluindo:
- Teste obrigatório `test_arranjo_horizontal_tres_elementos` (N=3, 4 vãos).
- Algoritmo genérico com `(N+1) * VAO_MIN` e `w_col = espaco_colunas // N`.

O contrato especifica "3 vãos" (para 2 elementos). A NOMENCLATURA especifica
"(2 colunas)". A generalização para N>2 com N+1 vãos não está explicitamente
autorizada pelos documentos normativos.

O handoff apresenta N+1 como generalização natural e matematicamente consistente,
não como decisão arquitetural nova. O contrato não PROÍBE N>2.

**Achado A-001** — ver seção de Achados.

O handoff NÃO substitui a regra contratual por algoritmo genérico SEM citar a
regra contratual: cita "3 vãos" explicitamente e deriva N+1 como generalização.
O algoritmo é explicitamente descrito e não é implícito.

Classificação: o handoff menciona N+1 e o apresenta como generalização segura e
compatível para o caso canônico N=2. A extensão para N>2 não está bloqueada com
`ARCHITECTURE_REVIEW_REQUIRED` pelo handoff — deixa como decisão local de implementação.
Dado que o contrato não proíbe N>2 e a generalização é matematicamente trivial,
a auditoria classifica como achado MÉDIO (não ARCHITECTURE_REVIEW_REQUIRED), com
exigência de documentação no IMP-0019.

---

## Verificação de aliases transicionais

| Valor JSON | Comportamento loader | Comportamento renderer | Handoff | Status |
|-----------|---------------------|----------------------|---------|--------|
| `"vertical"` | Aceito | Vertical (atual) | Explícito | OK |
| `"horizontal"` | Aceito | Horizontal plano | Explícito | OK |
| `"sobreposto"` | Aceito | Vertical (alias) | Explícito | OK |
| `"lado_a_lado"` | Aceito | Horizontal (alias) | Explícito | OK |
| `None` / ausente | Aceito | Vertical (default) | Explícito | OK |
| `"diagonal"` | `TelaEstruturaInvalida` | — | Explícito (teste obrigatório) | OK |
| `""` | `TelaEstruturaInvalida` | — | Explícito (teste obrigatório) | OK |
| `1` (inteiro) | `TelaEstruturaInvalida` | — | Explícito (teste obrigatório) | OK |

A normalização dos aliases ocorre no renderer, não no loader — conforme especificado.
O modelo armazena o valor como declarado (sem normalização). CONFORME.

`destino_minimo.json` e `stub_b.json` declaram `"sobreposto"` — confirmado por
inspeção direta. Com a validação do loader, `"sobreposto"` continuará funcionando
sem alteração (está no conjunto `ARRANJOS_CORPO_VALIDOS`). CONFORME.

---

## Verificação de proteção da barra_de_menus

| Elemento protegido | Escopo negativo | Preservações obrigatórias | Critério de aceite | Status |
|-------------------|-----------------|--------------------------|-------------------|--------|
| `_normaliza_distribuicao` | NÃO alterar ✓ | Listada ✓ | — | OK |
| `_validar_distribuicao` | NÃO alterar ✓ | Listada ✓ | — | OK |
| `_linhas_barra` | NÃO alterar ✓ | Listada ✓ | — | OK |
| `tela/explorar_barra_de_menus.py` | NÃO refatorar ✓ | **Não listada** | Critério 11 ✓ | BAIXO (A-002) |
| `tela/teste_explorar_barra_de_menus.py` | NÃO alterar ✓ | **Não listada** | Critério 11 ✓ | BAIXO (A-002) |
| `contrato_barra_de_menus.md` | NÃO alterar ✓ | — | — | OK |
| `contrato_chip.md` | NÃO alterar ✓ | — | — | OK |

As referências às funções de barra no corpo do handoff são todas na forma de
PROIBIÇÕES (escopo negativo, riscos R-1, R-2, R-6, seção de preservações).
Nenhuma prescreve alteração. CONFORME.

Risco R-1 (confundir `corpo.arranjo = "horizontal"` com `barra_de_menus.distribuicao`)
está explicitamente documentado com sintoma e mitigação. CONFORME.

---

## Verificação de testes exigidos

| Teste obrigatório | Presente no handoff | Localização |
|-------------------|---------------------|-------------|
| loader aceita valores válidos (vertical, horizontal, sobreposto, lado_a_lado, None) | Sim | 5 testes em teste_loader.py |
| loader rejeita valor inválido (diagonal, "", inteiro) | Sim | 3 testes em teste_loader.py |
| None preserva comportamento | Sim | `test_arranjo_none_preserva_vertical` |
| vertical preserva comportamento | Sim | `test_arranjo_vertical_preserva_comportamento` |
| sobreposto preserva comportamento | Sim | `test_arranjo_sobreposto_preserva_vertical` |
| horizontal renderiza lado a lado | Sim | `test_arranjo_horizontal_dois_elementos_lado_a_lado` |
| lado_a_lado renderiza como horizontal | Sim | `test_arranjo_lado_a_lado_alias_horizontal` |
| largura insuficiente gera RenderizadorErro | Sim | `test_arranjo_horizontal_largura_insuficiente` |
| padding inferior para alturas diferentes | Sim | `test_arranjo_horizontal_padding_inferior` |
| barra_de_menus continua passando | Sim | `test_arranjo_horizontal_barra_preservada` + critério 11 |
| baseline completo continua passando | Sim | Critério 12 (544 + novos = zero regressões) |

Todos os testes obrigatórios estão presentes. CONFORME.

**Nota sobre N=1**: o algoritmo (Passo 1) especifica fallback para N=1 →
renderizar como vertical, mas não há teste correspondente. Ver achado A-003.

---

## Achados

| ID | Severidade | Descrição | Evidência | Impacto | Correção recomendada |
|----|-----------|-----------|-----------|---------|---------------------|
| A-001 | MÉDIO | Generalização para N+1 vãos com N>2 não contratualizada explicitamente | Contrato seção 5.6: "3 vãos (coluna_1, coluna_2)"; NOMENCLATURA seção 10: "(2 colunas)". Handoff usa N+1 com teste obrigatório para N=3 | Caso N=2 está contratualizado; N>2 é extensão local não autorizada pelo contrato. A implementação de `test_arranjo_horizontal_tres_elementos` depende da decisão de suportar N>2 | IMP-0019 deve documentar explicitamente: "suporte a N>=2 é extensão local do princípio de vãos iguais (contrato seção 5.6, caso canônico N=2). Esta extensão foi decidida neste ciclo e deve ser incluída em atualização contratual futura." Não é necessário corrigir o handoff — documentar no IMP. |
| A-002 | BAIXO | `explorar_barra_de_menus.py` e `teste_explorar_barra_de_menus.py` ausentes da seção "Preservações obrigatórias" | Seção "Preservações obrigatórias" lista apenas funções de renderizador.py e classes de testes. Os arquivos do explorador estão no escopo negativo (linhas 194–195) e no critério 11, mas não na seção de preservações | Ambiguidade formal na seção "Preservações obrigatórias". Sem impacto real (os arquivos estão protegidos por outras seções) | Nenhuma correção necessária antes da implementação. O executor deve tratar os arquivos do explorador como protegidos conforme escopo negativo. |
| A-003 | BAIXO | Caso N=1 com `arranjo = "horizontal"` sem teste correspondente | Passo 1 do algoritmo: "Se N == 1, renderizar como vertical". Nenhum teste verifica esse comportamento. A regra geral proíbe fallback silencioso | Potencial contradição com a regra "nunca fallback silencioso". O comportamento N=1 → vertical não é verificável automaticamente | O executor pode opcionalmente adicionar `test_arranjo_horizontal_um_elemento` ao IMP-0019. Se não adicionado, documentar que N=1 é caso borda sem teste formal neste ciclo. |

---

## Decisão

```
APROVADO_COM_NOTAS
```

Justificativa:

- Nenhum achado BLOQUEANTE ou ALTO.
- Achado MÉDIO A-001 não exige correção do handoff — exige documentação no IMP-0019.
  A generalização N+1 é matematicamente correta, explícita no handoff, e não cria
  decisão arquitetural implícita (o handoff a descreve abertamente).
- Achados BAIXOS A-002 e A-003 não comprometem a implementação.
- Todos os critérios de aprovação estão satisfeitos para o caso contratual N=2.

Pontos obrigatórios satisfeitos:
- [x] Numeração correta (H-0019, não H-0020)
- [x] Sem referência remanescente a H-0020 como próximo ciclo
- [x] Implementável sem decisão arquitetural implícita (decisões são explícitas)
- [x] Regra dos 3 vãos clara e compatível com contrato para N=2
- [x] Escopo fechado
- [x] Barra_de_menus protegida
- [x] Testes exigidos suficientes
- [x] Sem achados bloqueantes, altos ou médios que exijam correção do handoff

---

## Conclusão

O handoff H-0019 está apto para implementação imediata. O executor deve:

1. Implementar conforme especificado, com foco no caso contratual N=2 (3 vãos).
2. Ao implementar `test_arranjo_horizontal_tres_elementos`, documentar no IMP-0019
   que suporte a N>=2 é extensão local do princípio de vãos iguais do contrato.
3. Tratar `explorar_barra_de_menus.py` e `teste_explorar_barra_de_menus.py` como
   arquivos protegidos, conforme escopo negativo do handoff.
4. Opcionalmente: adicionar teste para N=1 com arranjo="horizontal".

O baseline de 544 verificações deve ser mantido. O IMP-0019 deve registrar a decisão
local sobre suporte a N>2.
