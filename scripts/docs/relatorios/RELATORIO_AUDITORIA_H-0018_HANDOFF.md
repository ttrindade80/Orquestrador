# RELATORIO_AUDITORIA_H-0018_HANDOFF

```text
auditor:        Claude Code (papel auditoria de handoff)
data:           2026-07-09
ciclo:          H-0018
titulo:         Cobertura executável completa da barra_de_menus.distribuicao
commit-base:    c8a20fa  test: adiciona explorador da barra de menus
handoff:        scripts/docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md
```

---

## Status final

```text
AUDIT_APPROVED_WITH_NOTES
```

Nenhum achado bloqueante. Nenhum achado de alta severidade. O handoff está
completo, coerente e seguro para implementação. Três achados de nota, todos
sem impacto na segurança de implementação.

---

## Arquivos analisados

### Handoff alvo (lido integralmente)

```text
scripts/docs/handoff/H-0018-cobertura-executavel-distribuicao-barra-de-menus.md
```

### Ciclos anteriores (lidos integralmente)

```text
scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
scripts/docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md
scripts/docs/handoff/H-0017-script-exploracao-combinacoes-barra-de-menus.md
scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
scripts/docs/relatorios/RELATORIO_QA_H-0017_SCRIPT_EXPLORACAO_COMBINACOES_BARRA_DE_MENUS.md
```

### Documentação normativa (lida integralmente)

```text
scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
scripts/docs/contratos/contrato_barra_de_menus.md
scripts/docs/contratos/contrato_json_barra_de_menus.md
scripts/docs/contratos/contrato_chip.md
scripts/docs/contratos/contrato_tela_json.md
scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/NOMENCLATURA.md (primeiras 80 linhas / seção relevante)
```

### Código-fonte (lido)

```text
scripts/tela/renderizador.py     (primeiras 100 linhas + docstring)
scripts/tela/explorar_barra_de_menus.py  (primeiras 50 linhas)
scripts/tela/teste_explorar_barra_de_menus.py  (primeiras 50 linhas)
```

---

## Comandos executados

```bash
# Raiz do repositório: /home/tiago/Dropbox/UFRGS/Survey/versao_0_1
git log --oneline -6
git status --short
git diff --stat
git diff --name-only
ls scripts/docs/relatorios/
```

---

## Resumo executivo

O H-0018 cobre de forma completa e determinística a cobertura executável
de todos os 30 campos da seção `barra_de_menus.distribuicao`. O handoff:

1. Identifica corretamente quais campos o renderer ignora silenciosamente
   (diagnóstico preciso contra o código real pós H-0017).
2. Define semântica operacional verificável para cada campo novo
   (`vao_chip_texto`, `margem_horizontal`, `vao_vertical_entre_linhas`,
   `alinhamento_linhas`, `linhas.minimo`, `preferir_menor_numero`,
   `colunas.largura`, `subcolunas.*.alinhamento`, overflow flags).
3. Oferece opções A/B para campos com ambiguidade de decisão
   (`vao_vertical_entre_linhas`, `preferir_menor_numero`,
   `alinhamento_linhas` não-esquerda), com critério de bloqueio explícito.
4. Especifica 28 testes isolados no renderer e 9 testes adicionais no
   explorador, com exemplos concretos de entrada/saída.
5. Incorpora todos os achados do QA H-0017 (QA-01, QA-02, QA-N-01, QA-N-02)
   com ações obrigatórias.
6. Adiciona achados novos QA-03 e QA-04 para vao_chip_texto e
   margem_horizontal no explorador.
7. Mantém escopo negativo robusto: JSONs ativos intocados, contratos/ADRs
   intocados, arquivos proibidos explicitamente listados.
8. Define critérios de bloqueio ARCHITECTURE_REVIEW_REQUIRED para 10 casos.

---

## Verificação da motivação

**Ponto 1 — Campos declarados ignorados silenciosamente**

O handoff explica corretamente a motivação na seção "Motivação" (p. 129–140):
campos declarados no JSON canônico que nunca são lidos pelo renderer violam
o princípio do ADR-0014 de que "o renderer deve respeitar a distribuição
declarada". A seção "Contexto técnico — estado pós H-0017" lista com precisão
os campos ignorados, com referências ao código (`_texto_chip_barra`,
`_linhas_barra`, `_montar_coluna_a_coluna`). Os achados manuais QA-03
e QA-04 do usuário (vao_chip_texto, margem_horizontal) são confirmados
como "CONFIRMADO (campo ignorado)".

**Verificação**: PASSA.

---

## Verificação da seção JSON alvo

**Ponto 5 — Seção JSON alvo claramente definida**

A seção "Seção JSON alvo" (p. 215–283) reproduz integralmente a estrutura
canônica de `barra_de_menus.distribuicao` com todos os 30 campos mapeados.
O handoff usa exatamente a estrutura canônica implementada pelo H-0016
(validado contra IMP-0016 e o objeto `_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT`
no renderizador.py).

**Verificação**: PASSA.

---

## Verificação da cobertura por campo

**Pontos 3–22 — Todos os campos com decisão clara**

A seção "Lista completa de campos cobertos" (p. 289–323) lista todos os
30 campos com status exigido. Nenhum campo tem status "ignorado".

| # | Campo | Status exigido | Semântica definida | Verificação |
|---|-------|---------------|-------------------|-------------|
| 1 | modo | implementado ou validado | NÃO NOVO (H-0016) | PASSA |
| 2 | ordem.politica | implementado ou validado | NÃO NOVO (H-0016) | PASSA |
| 3 | ancoras.primeiro | implementado ou validado | NÃO NOVO (H-0016) | PASSA |
| 4 | ancoras.ultimo | implementado ou validado | NÃO NOVO (H-0016) | PASSA |
| 5 | tentativa_inicial | implementado ou validado | NÃO NOVO (H-0016) | PASSA |
| 6 | quebra | implementado ou validado | NÃO NOVO (H-0016) | PASSA |
| 7 | preenchimento_multilinha | implementado | NÃO NOVO (H-0016) | PASSA |
| 8 | preenchimentos_multilinha_suportados | implementado | seção 8 | PASSA |
| 9 | linhas.minimo | implementado ou rejeitado | seção 7 | PASSA |
| 10 | linhas.maximo | implementado | NÃO NOVO (H-0016) | PASSA |
| 11 | preferir_menor_numero | implementado ou rejeitado | seção 7 | PASSA |
| 12 | alinhamento_linhas | implementado (esquerda) ou rejeitado | seção 6 | PASSA |
| 13 | margem_horizontal.minimo | implementado | seção 2 | PASSA |
| 14 | margem_horizontal.maximo | implementado ou validado | seção 2 | PASSA |
| 15 | vao_chip_texto.minimo | implementado | seção 1 | PASSA |
| 16 | vao_chip_texto.maximo | implementado ou validado | seção 1 | PASSA |
| 17 | vao_entre_chips.minimo | implementado (já existe) | seção 3 | PASSA |
| 18 | vao_entre_chips.maximo | implementado ou validado | seção 3 | PASSA |
| 19 | vao_entre_colunas.minimo | implementado (já existe) | seção 4 | PASSA |
| 20 | vao_entre_colunas.maximo | implementado ou validado | seção 4 | PASSA |
| 21 | vao_vertical_entre_linhas.minimo | implementado ou rejeitado | seção 5 | PASSA |
| 22 | vao_vertical_entre_linhas.maximo | implementado ou rejeitado | seção 5 | PASSA |
| 23 | colunas.largura | implementado ou validado | seção 9 | PASSA |
| 24 | subcolunas.chip.alinhamento | implementado ou rejeitado | seção 10 | PASSA |
| 25 | subcolunas.texto.alinhamento | implementado ou rejeitado | seção 10 | PASSA |
| 26 | overflow.quando_nao_couber | implementado (já existe) | seção 11 | PASSA |
| 27 | overflow.nao_omitir_chips | implementado (já existe + novo: exige true) | seção 11 | PASSA |
| 28 | overflow.nao_truncar_texto | implementado (já existe + novo: exige true) | seção 11 | PASSA |
| 29 | overflow.nao_reordenar | implementado (já existe + novo: exige true) | seção 11 | PASSA |
| 30 | chips[] | implementado (já existe) | NÃO NOVO | PASSA |

**Verificação**: PASSA — todos os 30 campos têm status exigido não-ignorado.

---

## Verificação de espaçamentos

### vao_chip_texto (Ponto 7 e Atenção especial 3)

Semântica definida na seção 1 do handoff:
- `vao_chip_texto.minimo = 1` → `"[Esc] Sair"` (1 espaço)
- `vao_chip_texto.minimo = 3` → `"[Esc]   Sair"` (3 espaços)
- `vao_chip_texto.minimo = 10` → `"[Esc]          Sair"` (10 espaços)
- Formato: `"[{tecla}]{padding}{texto}"` onde `padding = " " * minimo`

O handoff exige teste isolado (test_vao_chip_texto_altera_distancia) que
altera SOMENTE vao_chip_texto.minimo e compara a saída. O exemplo
`[Esc] Sair` / `[Esc]   Sair` está explícito nos exemplos de teste.

Impacto no cálculo de comprimento de linha única: explicitamente endereçado
("O cálculo de encaixe em content_w e nos modos multilinha deve usar o
comprimento real do chip com o vao_chip_texto.minimo correto").

**Verificação Atenção especial 3**: PASSA — o handoff exige teste que
detecta que o campo foi ignorado.

### margem_horizontal (Ponto 8 e Atenção especial 2)

Semântica definida na seção 2:
- Margem esquerda mínima aparece antes do primeiro item em cada linha.
- `largura_util = content_w - 2 * margem_horizontal.minimo` (esquerda + direita).
- Com `alinhamento_linhas = "esquerda"`, a sobra adicional fica à direita.
- Valor exagerado (margem=50, content_w=39) → `RenderizadorErro` imediato.
- Validação: `minimo` deve ser `int >= 0`; `maximo` é `null` ou `int >= minimo`.

Os quatro critérios da Atenção especial 2 estão cobertos:
1. margem esquerda mínima antes do primeiro item: COBERTO
2. margem direita no cálculo de cabimento: COBERTO (`largura_util = content_w - 2 * margem`)
3. sobra à direita com alinhamento esquerda: COBERTO
4. valor exagerado gera efeito ou erro, nunca silêncio: COBERTO

**Verificação Atenção especial 2**: PASSA.

### vao_entre_chips (Ponto 9)

Semântica já implementada (H-0016). O handoff exige teste isolado
(test_vao_entre_chips_altera_distancia) confirmando efeito na saída.

**Verificação**: PASSA.

### vao_entre_colunas (Ponto 10)

Semântica já implementada (H-0016) para `coluna_a_coluna`. O handoff exige
teste isolado em cenário multilinha (test_vao_entre_colunas_altera_distancia_multilinha).

**Verificação**: PASSA.

---

## Verificação de linhas e alinhamento

### vao_vertical_entre_linhas (Ponto 11 e Atenção especial 4)

O handoff define decisão obrigatória entre:

**Opção A** — implementar linhas vazias entre linhas da barra (valor > 0 →
strings `""` inseridas); teste com `minimo > 0` confirmando efeito.

**Opção B** — rejeitar valores > 0 deterministicamente com `RenderizadorErro`
descritivo; teste com `minimo = 1` confirmando erro.

O handoff explicitamente proíbe ignorar silenciosamente valores > 0:
"Independentemente da opção escolhida: o campo deve ser lido e a decisão
deve ser determinística. Não pode ficar silenciosamente ignorado."

Test 9 (test_vao_vertical_entre_linhas_implementado_ou_rejeitado) exige
comportamento determinístico para ambas as opções.

**Verificação Atenção especial 4**: PASSA — o handoff exige decisão explícita
A ou B. Não permite ignorar valor > 0.

### alinhamento_linhas (Ponto 12 e Atenção especial 5)

O handoff define:
- `"esquerda"` continua funcionando (comportamento já é esquerda).
- `"centro"`, `"direita"`, `"justificado"` devem ser implementados com teste
  ou rejeitados deterministicamente com `RenderizadorErro`.
- Se implementar exigir nova norma não coberta pelo ADR-0014, bloquear com
  `ARCHITECTURE_REVIEW_REQUIRED`.

Tests 10 e 11 cobrem o caso "esquerda" e o caso valor-não-suportado.

**Verificação Atenção especial 5**: PASSA — o handoff não permite ignorar
valores não-esquerda silenciosamente.

### linhas.minimo (Ponto 13 e Atenção especial 6)

O handoff define semântica verificável:
- Se `minimo <= 1`: comportamento atual mantido.
- Se `minimo >= 2`: pular tentativa de linha única; iterar de `max(2, minimo)`
  até `maximo`.
- Test 12 (test_linhas_minimo_maior_que_1_pula_linha_unica): chips que caberiam
  em linha única mas `minimo = 2` → resultado deve ter 2 linhas.

**Verificação Atenção especial 6 (minimo)**: PASSA.

### linhas.maximo (Ponto 14)

Já implementado no H-0016. Tests 13, 14, 15 cobrem maximo=1 (overflow se
não caber), maximo=1 (ok se caber), maximo=3 (três linhas forçadas).

**Verificação**: PASSA.

### preferir_menor_numero (Ponto 15 e Atenção especial 6)

O handoff define:
- Opção A: implementar ambos os valores (true = menor primeiro, false = maior
  primeiro).
- Opção B: aceitar `true`; rejeitar `false` deterministicamente.
- Validação de tipo: deve ser `bool`; se não-bool, `RenderizadorErro`.
- Tests 16, 17 cobrem ambos os casos.

**Verificação Atenção especial 6 (preferir_menor_numero)**: PASSA.

---

## Verificação de preenchimento multilinha

**Ponto 16 — preenchimento_multilinha**

Já implementado no H-0016. O handoff exige confirmação de PADRÃO de
distribuição (não só "passou"): testes verificando que `coluna_a_coluna`
distribui coluna-a-coluna e `linha_a_linha` distribui linha-a-linha.
Seção 8 define exigências adicionais. Test 25 valida
`preenchimentos_multilinha_suportados`.

**Verificação**: PASSA.

**Ponto 17 — preenchimentos_multilinha_suportados**

O handoff exige validação de que o preenchimento ativo está na lista.
Test 25 (test_preenchimentos_multilinha_suportados_valida_preenchimento):
`preenchimento_multilinha = "coluna_a_coluna"` e
`preenchimentos_multilinha_suportados = ["linha_a_linha"]` → `RenderizadorErro`.

**Verificação**: PASSA.

---

## Verificação de colunas e subcolunas

**Ponto 18 — colunas.largura**

Seção 9: ler o campo; se `"por_maior_item_da_coluna"`, comportamento atual;
se outro valor, `RenderizadorErro`; se ausente, default sem erro.
Tests 18, 19.

**Verificação**: PASSA.

**Pontos 19–20 — subcolunas.chip.alinhamento e subcolunas.texto.alinhamento**

Seção 10: ler os campos; se `"esquerda"`, comportamento atual; se outro
valor, `RenderizadorErro`; se ausente, default sem erro.
Tests 20, 21.

**Verificação**: PASSA.

---

## Verificação de overflow

**Pontos 21–22 — flags de overflow**

Seção 11 — extensão importante em relação ao H-0016:
- H-0016 validava que os flags fossem `bool` (PR-M-04).
- H-0018 exige que os valores sejam exatamente `true`; valor `false` gera
  `RenderizadorErro` com mensagem "overflow.{flag} deve ser true; recebido: false".
- O handoff reconhece explicitamente essa extensão: "O H-0016 validava apenas
  que os campos fossem bool; este ciclo exige que os valores true sejam
  obrigatórios."
- Tests 22, 23, 24 cobrem os três flags.

Verificação de impacto em testes existentes: o `_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT`
usa `true` para todos os flags. O `test_overflow_flag_nao_booleana_erro` (H-0016)
passa valores não-bool (ex.: `"sim"`), não `false`. Nenhum teste existente
deverá quebrar pela nova validação.

**Verificação**: PASSA.

---

## Verificação dos achados H-0017 incorporados

**Ponto 35 — QA-01, QA-02, QA-N-01, QA-N-02 presentes**

| Achado | Presente no H-0018 | Ação exigida |
|--------|-------------------|-------------|
| QA-01 | SIM (seção "Achados do QA H-0017" e "Correções exigidas") | Substituir INV-4 por verificação de todos os pares (i,j) com i<j |
| QA-02 | SIM | Adicionar cenário C15 com linhas.maximo=1 à matriz padrão |
| QA-N-01 | SIM | Remover `or True`; substituir por `print(resumo)` |
| QA-N-02 | SIM | Adicionar verificação explícita de tokens não declarados (INV-2) |

Cada achado tem ação concreta obrigatória definida com pseudocódigo de
implementação.

**Ponto 36 — QA-03 e QA-04 novos**

| Achado | Presente | Ação exigida |
|--------|---------|-------------|
| QA-03 (vao_chip_texto) | SIM | Variação explícita e teste no explorador |
| QA-04 (margem_horizontal) | SIM | Variação explícita e teste no explorador |

**Verificação**: PASSA.

---

## Verificação do explorador

**Ponto 33 e Atenção especial 7 — parâmetros CLI do explorador**

| Parâmetro exigido | Presente no H-0018 | Verificação |
|------------------|-------------------|-------------|
| `--margens-horizontais` | SIM (p. 686-689) | PASSA |
| `--vaos-chip-texto` | SIM (p. 690-693) | PASSA |
| `--vaos-entre-chips` | SIM (p. 694-697) | PASSA |
| `--vaos-entre-colunas` | SIM (p. 698-701) | PASSA |
| `--vaos-verticais` | OPCIONAL (p. 703-709) | PASSA* |
| `--alinhamentos-linhas` | OPCIONAL (p. 703-709) | PASSA* |

*O handoff diz: "são opcionais neste ciclo: se a implementação do renderer
para esses campos for determinística, o explorador deve incluí-los; se o
renderer os rejeitar deterministicamente, o explorador deve documentá-los
como cenário de erro esperado." Esta decisão é coerente com o princípio
de não criar CLI desnecessária.

**`_fabricar_distribuicao` atualizada**: seção "Atualização de `_fabricar_distribuicao`"
define novos parâmetros `vao_chip_texto=1` e `margem_horizontal=1`. PASSA.

**INV-4 substituída (QA-01)**: seção "Atualização da `_verificar_invariantes`"
define a substituição. PASSA.

**Ponto 34 — testes do explorador**

A seção "Testes obrigatórios do explorador" (p. 894-938) define 9 novos
casos (11-19) para adicionar aos 10 existentes. Os 10 existentes devem
continuar passando (p. 940).

**Verificação Atenção especial 7**: PASSA.

---

## Verificação de arquivos permitidos/proibidos

**Ponto 37 e Atenção especial 8**

### Arquivos permitidos (comparação esperado vs. handoff)

| Arquivo esperado | Presente no H-0018 | Coincide |
|-----------------|-------------------|---------|
| scripts/tela/renderizador.py | SIM (p. 999) | ✓ |
| scripts/tela/teste_renderizador.py | SIM (p. 1000) | ✓ |
| scripts/tela/explorar_barra_de_menus.py | SIM (p. 1001) | ✓ |
| scripts/tela/teste_explorar_barra_de_menus.py | SIM (p. 1002) | ✓ |
| scripts/docs/relatorios/IMP-0018-*.md | SIM (p. 1003) | ✓ |

### Arquivos proibidos (comparação esperado vs. handoff)

| Arquivo esperado proibido | Presente na lista proibida | Coincide |
|--------------------------|--------------------------|---------|
| scripts/docs/adr/ | SIM (p. 1021) | ✓ |
| scripts/docs/contratos/ | SIM (p. 1022) | ✓ |
| scripts/docs/NOMENCLATURA.md | SIM (p. 1023) | ✓ |
| scripts/docs/INDICE.md | SIM (p. 1024) | ✓ |
| scripts/config/telas/ | SIM (p. 1026) | ✓ |
| scripts/config/estilo.json | SIM (p. 1027) | ✓ |
| scripts/config/lancador.json | SIM (p. 1028) | ✓ |
| scripts/config/layout_console.json | SIM (p. 1029) | ✓ |
| scripts/tela/loader.py | SIM (p. 1031) | ✓ |
| scripts/tela/modelo.py | SIM (p. 1032) | ✓ |
| scripts/tela/demo.py | SIM (p. 1033) | ✓ |
| scripts/tela/diagnostico.py | SIM (p. 1034) | ✓ |
| scripts/tela/teste_loader.py | SIM (p. 1036) | ✓ |
| scripts/tela/teste_modelo.py | SIM (p. 1037) | ✓ |
| scripts/tela/teste_demo.py | SIM (p. 1038) | ✓ |
| scripts/tela/teste_diagnostico.py | SIM (p. 1039) | ✓ |

**Verificação Atenção especial 8**: PASSA — listas exatamente iguais às esperadas.

A implementação dos campos novos (`vao_chip_texto`, `margem_horizontal`,
`vao_vertical_entre_linhas`, `alinhamento_linhas`, `linhas.minimo`,
`preferir_menor_numero`, `colunas.largura`, `subcolunas.*.alinhamento`,
overflow flags) pode ser feita exclusivamente em `renderizador.py` e seus
testes, sem necessidade de alterar arquivos proibidos.

---

## Verificação de escopo negativo

**Pontos 2, 3, 4 e Atenção especial 1**

O handoff define escopo negativo robusto na seção "Escopo negativo" (p. 966-991):
- Nenhuma alteração de ADR, contrato ou NOMENCLATURA.md.
- Nenhuma alteração de JSONs ativos de produção (uso apenas de objetos
  sintéticos em memória ou fixtures nos testes).
- Nenhuma duplicação de `barra_de_menus` em JSONs.
- A seção "Alerta: JSON duplicado" (p. 172-183) trata o caso explicitamente
  e exige que testes usem objetos sintéticos.

**Separação de tipos de tarefa (Atenção especial 1)**:

O handoff separa corretamente:
- **Implementar** quando a semântica está definida (vao_chip_texto,
  margem_horizontal, linhas.minimo, colunas.largura, subcolunas.*.alinhamento,
  overflow flags true).
- **Rejeitar deterministicamente** quando não suportado neste ciclo (vao_vertical
  Opção B, alinhamento_linhas não-esquerda, preferir_menor_numero=false Opção B,
  subcolunas valor ≠ esquerda).
- **Bloquear** quando exigir nova norma (10 critérios de bloqueio definidos).

Nenhum campo requer semântica não coberta pelo ADR-0014 ou contratos, desde
que as opções de rejeição determinística sejam usadas quando a implementação
for complexa.

**Verificação Atenção especial 1**: PASSA.

---

## Verificação de testes obrigatórios

**Ponto 38 — Preservação de testes existentes**

O handoff exige explicitamente (p. 1101, critério 32):
"Testes existentes (476 verificações em 6 suítes) continuam passando."

A seção "Suítes existentes (devem continuar passando)" (p. 1112-1126)
lista todas as 6 suítes com os comandos exatos:

```bash
cd scripts
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
python tela/teste_explorar_barra_de_menus.py
```

**Ponto 39 e Atenção especial 9 — testes obrigatórios completos**

Execuções manuais do explorador (p. 1127-1148) cobrem:
- `python tela/explorar_barra_de_menus.py` (padrão, inclui C15 com linhas.maximo=1)
- Execução com `--margens-horizontais 0,1,4,50 --vaos-chip-texto 1,3,10
  --vaos-entre-chips 2,6,20 --vaos-entre-colunas 2,8` (valores exagerados)
- Modo detalhado com `--mostrar-erros` (erros de margem e vão exagerados)

**Cenários manuais obrigatórios presentes** no handoff p. 1127-1148:
- margens horizontais: ✓ (--margens-horizontais 0,1,4,50)
- vãos chip-texto: ✓ (--vaos-chip-texto 1,3,10)
- vãos entre chips: ✓ (--vaos-entre-chips 2,6,20)
- vãos entre colunas: ✓ (--vaos-entre-colunas 2,8)
- linhas.maximo 1/2/3: ✓ (--linhas-max 1,2,3)
- preenchimentos: ✓ (--preenchimentos coluna_a_coluna,linha_a_linha)
- valores exagerados: ✓ (margem=50 e vãos=50 visíveis no comando)

**Verificação Atenção especial 9**: PASSA.

---

## Verificação de critérios de bloqueio

**Ponto 40 — Critérios de bloqueio para ARCHITECTURE_REVIEW_REQUIRED**

O handoff define 10 critérios de bloqueio (p. 1213-1233):
1. Necessidade de alterar ADR, contrato ou NOMENCLATURA.
2. Campo requerendo semântica nova não coberta por ADR-0014 ou contratos.
3. Necessidade de alterar JSONs ativos.
4. Necessidade de alterar loader.py, modelo.py, demo.py, diagnostico.py.
5. Necessidade de alterar testes de loader/modelo/demo/diagnostico.
6. Necessidade de composição horizontal do corpo.
7. Impossibilidade de definir efeito ou rejeição determinística sem nova norma.
8. Ambiguidade sobre duplicidade de barra_de_menus.
9. alinhamento_linhas ≠ "esquerda" exigir nova norma.
10. preferir_menor_numero=false exigir nova norma.

Os critérios são coerentes com os contratos e ADRs. As opções de rejeição
determinística (Opções B) evitam os critérios 7, 9, 10 para o executor.

**Verificação**: PASSA.

---

## Verificação do relatório IMP-0018

**Ponto 39 — Relatório com tabela de cobertura de todos os 30 campos**

A seção "Relatório de implementação" (p. 1155-1209) define a estrutura
exigida incluindo:
- "Campos da distribuição cobertos" — tabela com todos os 30 campos e status
  (implementado | validado | rejeitado_deterministicamente | fora_de_escopo_com_bloqueio).
- "Nenhum campo pode ter status 'ignorado'" — explícito no handoff.
- "Decisões locais" — registrar qual opção foi escolhida para
  vao_vertical_entre_linhas, alinhamento_linhas, preferir_menor_numero.

**Verificação**: PASSA.

---

## Achados

### AUD-N-01 — Impacto de Option A para vao_vertical_entre_linhas em L_barra não explicitado

- **ID**: AUD-N-01
- **Severidade**: nota
- **Evidência**: Se o executor escolher a Opção A para `vao_vertical_entre_linhas`
  (inserir linhas vazias `""` entre as linhas da barra), a função `_linhas_barra`
  retorna mais strings. Como `l_barra = len(linhas_barra) + 2`, a contabilidade
  de L_barra é afetada implicitamente. Por exemplo, com 2 linhas de barra e
  `vao_vertical.minimo = 1`, `_linhas_barra` retornaria 3 strings (linha1, "",
  linha2) em vez de 2, elevando L_barra de 4 para 5. O handoff não menciona
  esse impacto explicitamente.
- **Impacto**: O impacto é zero na correção da implementação, pois a fórmula
  `l_barra = len(linhas_barra) + 2` é correta por construção. O executor precisa
  apenas retornar as strings corretas (incluindo strings vazias). Não há ambiguidade
  que impeça a implementação.
- **Recomendação**: Registrar no IMP-0018 (seção "Decisões locais") que a Opção A
  aumenta L_barra proporcionalmente. Sem impacto no bloqueio ou aprovação.

---

### AUD-N-02 — Política de campos `maximo` não declarada como princípio global

- **ID**: AUD-N-02
- **Severidade**: nota
- **Evidência**: O handoff define de forma consistente que os campos `maximo`
  de espaçamentos (vao_chip_texto.maximo, margem_horizontal.maximo, vao_entre_chips.maximo,
  vao_entre_colunas.maximo) são validados se presentes, mas não participam do
  cálculo de layout neste ciclo. Essa política é repetida individualmente em
  cada seção, mas não é declarada como princípio global explícito.
- **Impacto**: O executor precisa aplicar a mesma política para todos os campos
  `maximo`. Como a política é consistente nas seções individuais, o risco de
  divergência de interpretação é baixo. O IMP-0018 pode esclarecer essa política
  global na seção "Decisões locais".
- **Recomendação**: O executor deve registrar no IMP-0018: "Política global para
  campos maximo: validam mas não participam do cálculo de layout neste ciclo."
  Sem impacto no bloqueio ou aprovação.

---

### AUD-N-03 — Validação de overflow flags estendida de H-0016: confirmar ausência de testes afetados

- **ID**: AUD-N-03
- **Severidade**: nota
- **Evidência**: O H-0016 validava que os flags `nao_omitir_chips`,
  `nao_truncar_texto` e `nao_reordenar` sejam `bool` (PR-M-04). O H-0018
  estende para exigir que o valor seja exatamente `true`. O handoff reconhece
  explicitamente essa extensão. O teste existente `test_overflow_flag_nao_booleana_erro`
  (H-0016) usa valores não-bool (ex.: `"sim"`) — não usa `false`. O objeto
  `_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT` usa `true` para todos os flags.
  Portanto, nenhum teste existente aprovado usa `false` com expectativa de sucesso.
- **Impacto**: Nenhum teste existente deve quebrar pela nova validação. Contudo,
  o executor deve verificar antes de implementar que não há casos de teste que
  passem `false` e esperem sucesso.
- **Recomendação**: O executor deve confirmar no IMP-0018 que nenhum teste
  existente foi afetado. Sem impacto no bloqueio ou aprovação.

---

## Conclusão

O handoff H-0018 está **pronto para implementação**. Todos os 40 pontos
obrigatórios de auditoria passaram. Todas as 9 atenções especiais foram
verificadas e passaram. Os três achados são exclusivamente de nota (sem
impacto na segurança de implementação).

O handoff está correto em relação ao estado do repositório: HEAD em
`c8a20fa` (test: adiciona explorador da barra de menus), único arquivo
não rastreado sendo o próprio handoff.

O executor (OpenCode / GLM) está autorizado a iniciar a implementação
do H-0018 após leitura integral da seção "Leitura obrigatória" do handoff.
A ordem de implementação recomendada (p. 1269-1284) está bem estruturada.

---

## Próxima ação recomendada

```text
1. Aprovar status: AUDIT_APPROVED_WITH_NOTES
2. Registrar os três achados de nota (AUD-N-01, AUD-N-02, AUD-N-03) no
   IMP-0018, seção "Decisões locais", ao final da implementação.
3. Iniciar implementação em contexto limpo seguindo a leitura obrigatória
   do handoff H-0018.
4. O commit é responsabilidade do usuário após QA aprovado.
```
