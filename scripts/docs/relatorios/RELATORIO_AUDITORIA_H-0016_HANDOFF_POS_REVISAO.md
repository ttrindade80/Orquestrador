# RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO

Auditoria pós-revisão do handoff `H-0016 — Migração canônica do JSON da
barra_de_menus e renderização horizontal responsiva`.

```text
auditor:        OpenCode / GLM (papel QA/auditoria de handoff)
data:           2026-07-09
alvo:           scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
commit-base:    b2eb458  feat: ocupa altura do terminal pelo corpo
ciclo:          H-0016
auditoria anterior: scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF.md (AUDIT_REJECTED)
```

---

## Status final

```text
AUDIT_APPROVED_WITH_NOTES
```

Todos os 4 achados bloqueantes/altos da auditoria anterior (B-001, B-002,
B-003, A-001) foram corrigidos. O handoff revisado está coerente, suficiente
e seguro para implementação. Persistem 4 achados de severidade média
(comportamentos não definidos para valores inválidos de
`ordem.politica`/`preenchimento_multilinha`/`linhas.*`/`overflow`) e 2 notas
não bloqueantes. Nenhum achado bloqueante ou de alta severidade.

---

## Arquivos analisados

```text
scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF.md

scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md

scripts/docs/contratos/contrato_processo_desenvolvimento.md
scripts/docs/contratos/contrato_tela_json.md
scripts/docs/contratos/contrato_barra_de_menus.md
scripts/docs/contratos/contrato_json_barra_de_menus.md
scripts/docs/contratos/contrato_chip.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_lancador.md
scripts/docs/contratos/contrato_json_lancador.md
scripts/docs/NOMENCLATURA.md

scripts/docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md
scripts/docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md
scripts/docs/relatorios/RELATORIO_QA_H-0015_OCUPACAO_VERTICAL_JANELA_TERMINAL_CORPO.md

scripts/tela/loader.py
scripts/tela/modelo.py
scripts/tela/renderizador.py
scripts/tela/demo.py
scripts/tela/diagnostico.py

scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py

scripts/config/telas/orquestrador.json
scripts/config/telas/grupo_minimo.json
scripts/config/telas/destino_minimo.json
scripts/config/telas/stub_b.json
```

---

## Comandos executados

```bash
git log --oneline -6
git status --short
git diff --stat
git diff --name-only
```

Saídas:

```text
git log --oneline -6:
  b2eb458 feat: ocupa altura do terminal pelo corpo
  4762583 docs: registra ocupacao vertical e barra responsiva
  8a6403a feat: migra arranjo vertical e barra declarativa
  ceaf0be docs: registra ADRs de arranjo e barra declarativa
  ab48702 feat: adiciona acesso demonstravel ao grupo minimo
  0bcb477 feat: implementa grupo estrutural minimo em tela isolada

git status --short:
  ?? scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
  ?? scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF.md

git diff --stat:      (vazio)
git diff --name-only: (vazio)
```

Estado do workspace **conforme esperado**: HEAD em `b2eb458`; apenas os dois
arquivos não rastreados esperados (o handoff H-0016 e a auditoria anterior).
**Nenhum achado de escopo** de arquivos modificados ou não rastreados fora do
esperado antes da criação deste relatório.

---

## Resumo executivo

A revisão do handoff H-0016 endereçou precisamente os 4 achados que motivaram
o `AUDIT_REJECTED` anterior:

- **B-001 (bloqueante) → CORRIGIDO**: nenhuma ocorrência de `scripts/testes/`
  permanece; todos os 5 arquivos de teste reais estão em `scripts/tela/` e
  constam da lista de arquivos permitidos; a referência a `teste_chip.py`
  inexistente foi removida.
- **B-002 (bloqueante / ARCHITECTURE_REVIEW_REQUIRED) → CORRIGIDO**:
  `ordem.politica` agora usa exclusivamente `"declaracao"` (valor normativo
  da ADR-0014 e do `contrato_barra_de_menus.md` seção 17), em toda estrutura
  canônica, semântica de campos, regras de ordem/âncoras, constante default e
  critério de aceite 7.
- **B-003 (bloqueante) → CORRIGIDO**: a seção "Atualização de testes e
  snapshots" reconhece que a mudança vertical → horizontal altera
  expectativas literais; o escopo positivo item 17 autoriza a atualização de
  snapshots; o handoff substitui explicitamente a contabilidade
  `L_barra = 2 + N_chips` por `L_barra = 2 + N_linhas_barra`.
- **A-001 (alta) → CORRIGIDO**: `scripts/tela/teste_demo.py` e
  `scripts/tela/teste_diagnostico.py` constam explicitamente da lista de
  arquivos permitidos (linhas 478–479), com justificativa (linha 484).

O handoff revisado está **alinhado à ADR-0014**, preserva integralmente o
H-0015, preserva o fluxo `g/d/b/Esc`, define a migração dos 4 JSONs como
entrega obrigatória, especifica o algoritmo de renderização horizontal
responsiva de forma implementável (linha única → multilinha `coluna_a_coluna`
→ `erro_layout`), define âncoras como validação (não reordenação), usa os IDs
reais (`chip_esc`, `chip_ajuda`) presentes nos 4 JSONs, e exige relatório
`IMP-0016`.

Persistem 4 achados de severidade **média** sobre comportamentos não definidos
para valores inválidos de `ordem.politica`, `preenchimento_multilinha`,
`linhas.*` e `overflow.quando_nao_couber` (audit points 15–18), herdadas da
auditoria anterior como M-001 a M-004. Essas lacunas não bloqueiam a
implementação porque: (a) a migração canônica usa apenas valores válidos;
(b) o handoff define `modo` desconhecido → `RenderizadorErro` (audit point
14), estabelecendo um padrão defensivo que o implementador pode estender; (c)
a seção "Critérios de bloqueio" oferece rota de fuga `ARCHITECTURE_REVIEW_REQUIRED`
para casos imprevistos.

Classificação final: **AUDIT_APPROVED_WITH_NOTES** — pronto para
implementação, com recomendação de que o implementador trate os valores
inválidos restantes como `RenderizadorErro` determinístico (decisão local,
sem nova norma).

---

## Verificação dos achados anteriores

### B-001 — Erro sistemático de path `scripts/testes/` (inexistente)

- **Status**: CORRIGIDO.
- **Evidência**:
  - `rg -n "scripts/testes" handoff` → nenhuma ocorrência.
  - `rg -n "teste_chip" handoff` → nenhuma ocorrência.
  - Seção "Arquivos permitidos" (linhas 463–482) lista corretamente:
    `scripts/tela/teste_loader.py`, `scripts/tela/teste_modelo.py`,
    `scripts/tela/teste_renderizador.py`, `scripts/tela/teste_demo.py`,
    `scripts/tela/teste_diagnostico.py`.
  - Seção "Arquivos proibidos" (linhas 490–500) não referencia paths
    inexistentes.
- **Conclusão**: cláusula de escopo de arquivos agora operacional.

### B-002 — Valor normativo `ordem.politica = "declaracao_validada"` fora da ADR-0014

- **Status**: CORRIGIDO.
- **Evidência**:
  - Estrutura canônica (linha 149): `"politica": "declaracao"`.
  - Semântica de campos (linha 197): `"declaracao"`: a ordem base é `chips[]`.
  - Regras de ordem (linha 218): `ordem.politica = "declaracao"` (valor
    normativo definido pela ADR-0014).
  - Constante default (linha 577): `"politica": "declaracao"`.
  - Critério de aceite 7 (linha 654): `ordem.politica` usa `"declaracao"`
    (não `"declaracao_validada"`).
  - ADR-0014 (linha 302): `ordem.politica: declaracao | grupos_declarados`.
  - `contrato_barra_de_menus.md` seção 17 (linhas 524–526): repassa
    `declaracao | grupos_declarados`.
  - A única ocorrência da substring `declaracao_validada` no handoff é na
    linha 654, onde afirma explicitamente que **não** se deve usar esse valor.
- **Conclusão**: divergência normativa removida; alinhamento total com
  ADR-0014 e contrato.

### B-003 — Contradição interna sobre preservação de testes existentes

- **Status**: CORRIGIDO.
- **Evidência**:
  - Seção "Atualização de testes e snapshots" (linhas 338–376) reconhece:
    "a migração (...) altera a forma física da barra (...) pode alterar
    snapshots e expectativas literais de renderização".
  - Nova contabilidade definida (linhas 344–354):
    `L_barra = 2 + N_linhas_barra` (antes: `L_barra = 2 + N_chips`).
  - Exemplo concreto (linhas 356–358): 2 chips em `largura=42` →
    `N_linhas_barra = 1` → `L_barra = 3` (antes era 4).
  - Lista de testes afetados (linhas 368–373): `_EXPECTED_ORQUESTRADOR`,
    `_EXPECTED_ORQUESTRADOR_RETA`, `teste_altura_explicita` com `l_barra = 4`
    e `n_minimo = 16` → `l_barra = 3` e `n_minimo = 15`.
  - Escopo positivo item 17 (linha 397): "Atualizar snapshots e expectativas
    literais de renderização afetados pela mudança de layout horizontal".
  - Regra técnica (linha 375): preservar a **intenção** dos testes, não o
    texto antigo das asserções.
  - A afirmação "Não remover nem alterar testes existentes" da versão
    rejeitada foi removida; substituída por autorização explícita de
    atualização.
  - Preservações obrigatórias item 12 (linha 455): "os testes existentes
    devem continuar passando **com as expectativas atualizadas** quando a
    mudança de layout for efeito esperado do H-0016".
- **Verificação contra código real**:
  - `scripts/tela/teste_renderizador.py:60-77` (`_EXPECTED_ORQUESTRADOR`)
    codifica chips empilhados verticalmente — quebra esperada, autorizada.
  - `scripts/tela/teste_renderizador.py:969-970` (`teste_altura_explicita`)
    codifica `l_barra = 4` e `n_minimo = 16` — quebra esperada, autorizada.
  - `scripts/tela/teste_demo.py:123-126, 162-165, 176-179, 204-207` contêm
    snapshots com chips empilhados — quebra esperada, autorizada.
  - `scripts/tela/teste_diagnostico.py:60-63` contém snapshot com chips
    empilhados — quebra esperada, autorizada.
- **Conclusão**: contradição interna removida; caminho de implementação
  consistente.

### A-001 — `teste_demo.py` e `teste_diagnostico.py` fora das listas de escopo

- **Status**: CORRIGIDO.
- **Evidência**:
  - Linhas 478–479 da seção "Arquivos permitidos":
    `scripts/tela/teste_demo.py` e `scripts/tela/teste_diagnostico.py`.
  - Seção "Especificação funcional por módulo" (linhas 617–619):
    "Verificar se há asserções literais afetadas pela mudança de layout da
    barra. Se houver, atualizar as expectativas (...)".
  - Cobertura obrigatória por suíte (linhas 787–788): `teste_demo.py` e
    `teste_diagnostico.py` com snapshots atualizados quando necessário.
- **Conclusão**: ambos os arquivos agora classificados explicitamente.

---

## Verificação de aderência à ADR-0014

| Item da ADR-0014 | Cobertura no H-0016 revisado | Status |
|---|---|---|
| A.1 — barra declarativa por tela (ADR-0012) preservada | Sim (escopo negativo não reabre política declarativa) | OK |
| A.2 — campo controlador é `barra_de_menus.distribuicao` | Sim | OK |
| A.3 — `"horizontal"` não é linha única fixa | Sim (algoritmo responsivo) | OK |
| A.4 — `"horizontal"` = horizontal responsiva | Sim | OK |
| A.5 — `"horizontal"` é alias transitório | Sim (compatibilidade transitória mantida; seção dedicada) | OK |
| A.6 — formato canônico é objeto `modo = "horizontal_responsiva"` | Sim | OK |
| A.7 — renderer respeita declaração da instância | Sim | OK |
| A.8 — renderer não empilha um chip por linha quando horizontal | Sim (substitui `_linhas_barra` atual) | OK |
| A.9 — renderer não reordena chips por heurística | Sim (`ordem.politica = "declaracao"`; `nao_reordenar`) | OK |
| A.10 — renderer não inventa chips ausentes | Sim (`nao_omitir_chips`; escopo negativo) | OK |
| A.11 — renderer não completa com lista canônica global | Sim (escopo negativo) | OK |
| A.12 — erro de layout vira erro determinístico | Sim (`overflow.quando_nao_couber = "erro_layout"`) | OK |
| A.13 — barra não herda regra do `lancador` | Sim (escopo negativo) | OK |
| A.14 — chips de itens do `lancador` não são chips da barra | Sim (escopo negativo; critério 25) | OK |
| A.15 — distribuição da barra independente de `corpo.arranjo` | Sim (escopo negativo; critério 26) | OK |
| Parte B — alteração por termo específico completo | Sim (handoff nomeia `barra_de_menus.distribuicao` por extenso) | OK |
| Estrutura canônica futura (objeto declarativo) | Sim — handoff replica a estrutura, agora com `politica = "declaracao"` | OK |
| `ordem.politica`: `declaracao \| grupos_declarados` | Handoff usa `declaracao` (valor normativo); não implementa `grupos_declarados` neste ciclo | OK |
| `preenchimento_multilinha`: `coluna_a_coluna \| linha_a_linha` | Ambos suportados ou rejeitados deterministicamente | OK |
| Algoritmo normativo mínimo (passos 1–10) | Sim (linha única → multilinha → erro_layout) | OK |
| Overflow determinístico (`erro_layout`) | Sim | OK |

**Conclusão ADR-0014**: aderência total. Nenhuma divergência normativa
identificada. O campo extra `preenchimentos_multilinha_suportados` (herdado
como N-001 da auditoria anterior) é uma extensão que não contradiz semântica
da ADR — ver achado PR-N-01.

---

## Verificação da migração JSON

Inventário pré-migração confirmado pela leitura direta dos 4 JSONs ativos:

| Arquivo | `distribuicao` atual | chips[] (ordem) |
|---|---|---|
| `orquestrador.json` | `"horizontal"` (string) | `chip_esc` (Esc/Sair), `chip_ajuda` (?/Ajuda) |
| `grupo_minimo.json` | `"horizontal"` (string) | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |
| `destino_minimo.json` | `"horizontal"` (string) | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |
| `stub_b.json` | `"horizontal"` (string) | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |

Verificação dos pontos de auditoria de migração:

- **(1) Inclui migração dos 4 JSONs como escopo positivo**: Sim (escopo
  positivo itens 1–4; critérios 1–4). OK.
- **(2) Não adia migração para ciclo futuro**: Sim — migração é entrega
  obrigatória deste ciclo. OK.
- **(3) Define estrutura canônica suficiente para `distribuicao`**: Sim
  (linhas 145–186). B-002 corrigido. OK.
- **(4) Usa `ordem.politica = "declaracao"`**: Sim. OK.
- **(5) Preserva exatamente a lista de chips em cada JSON**: Sim (escopo
  negativo linhas 516–520). OK.
- **(6) Proíbe adicionar chips canônicos ausentes**: Sim (escopo negativo
  linha 425). OK.
- **(7) Proíbe remover chips existentes**: Sim (linha 518). OK.
- **(8) Proíbe reordenar chips existentes**: Sim (linha 519). OK.
- **(9) Proíbe alterar `id/tecla/texto/acao/regra_existencia/regra_ativo/forma_exibicao`**:
  Sim (linha 520). OK.
- **(10) Renderer usa a declaração do JSON, não defaults inventados**: Sim
  (regras técnicas 1–5; escopo negativo). OK.
- **(11) Compatibilidade transitória com `"horizontal"` sem substituir o
  caminho canônico**: Sim (seção "Compatibilidade transitória" linhas
  322–334; critérios 19–20). OK.

Os IDs de âncora propostos (`chip_esc`, `chip_ajuda`) correspondem
exatamente aos IDs reais nos 4 JSONs. O handoff ainda instrui explicitamente
(linha 188): "O implementador deve usar os IDs reais dos chips encontrados
nos JSONs — não renomear IDs apenas para combinar com o exemplo." OK.

---

## Verificação de loader/modelo

- `scripts/tela/loader.py:357`: retorna `barra_de_menus` como dict bruto
  (`dados.get("barra_de_menus")`), sem validar nem transformar `distribuicao`.
- `scripts/tela/modelo.py:79`: declara `barra_de_menus: dict`;
  `construir_modelo` (linhas 190–191) valida apenas que a chave existe, sem
  inspecionar `distribuicao`.

O handoff está **alinhado** a esse comportamento: o escopo negativo (linha
432) proíbe alterar `loader.py`/`modelo.py` para validar `distribuicao` e
atribui a validação ao renderer. **(12) Define o papel de loader.py e
modelo.py de forma suficiente**: Sim. OK.

Observação (ver PR-N-02): `loader.py` e `modelo.py` aparecem na lista de
"Arquivos permitidos" (linhas 469–470) apesar de o escopo negativo proibir
alterá-los para `distribuicao`. Em prática, nenhuma alteração de fonte é
necessária (o dict bruto já preserva o objeto canônico); os testes
`teste_loader.py`/`teste_modelo.py` é que ganham asserções de que a
distribuição é exposta como objeto. Não bloqueante.

---

## Verificação de renderização horizontal responsiva

O algoritmo descrito (seção "Algoritmo de renderização horizontal
responsiva", linhas 234–318) cobre os pontos da atenção especial 3:

| Requisito (Atenção especial 3) | Cobertura | Status |
|---|---|---|
| 1. linha única quando couber | `tentativa_inicial = "linha_unica"`; fluxo passo 5; pseudocódigo | OK |
| 2. multilinha quando linha única não couber | `quebra = "multilinha_quando_nao_couber"`; fluxo passo 6 | OK |
| 3. preenchimento coluna_a_coluna | Seção dedicada com `ceil(N/K)` e exemplo [A,B,C,D,E] K=2 | OK |
| 4. linha_a_linha implementado ou rejeitado deterministicamente | Implementado como modo alternativo; rejeição determinística se não implementado | OK |
| 5. `erro_layout` quando não couber em `linhas.maximo` | Fluxo passo 7; pseudocódigo linha 556; critérios 11–12 | OK |
| 6. cada chip aparece exatamente uma vez | `nao_omitir_chips`; regras 3–4; critério 21 | OK |
| 7. nenhum chip truncado/omitido/inventado/reordenado | `nao_truncar_texto`, `nao_omitir_chips`, `nao_reordenar`; A.10/A.11 | OK |
| 8. nova contabilidade `L_barra = 2 + N_linhas_barra` | Seção "Nova contabilidade de L_barra" linhas 342–364 | OK |

Assinatura `_linhas_barra(barra_de_menus: dict, content_w: int) -> list[str]`
e atualização da chamada em `renderizar_tela` (passando `content_w = total_w -
3`) estão especificadas e coerentes com o código atual
(`scripts/tela/renderizador.py:197`, `:327`, `:361`, `:373`). O invariante
`l_barra = len(linhas_barra) + 2` permanece válido porque `_linhas_barra`
continua retornando lista de strings (1 ou 2 elementos conforme o encaixe).

Verificação do cálculo de encaixe para largura 42 (`content_w = 39`):
- `[Esc] Sair` (10 chars) + 2 espaços (`vao_entre_chips.minimo`) + `[?] Ajuda` (9 chars) = 21 ≤ 39 → cabe em linha única.
- `N_linhas_barra = 1` → `L_barra = 3` (antes era 4 com empilhamento vertical).
- `n_minimo = L_cab (3) + L_corpo_conteudo (9) + L_barra (3) = 15` (antes era 16).

Os exemplos de `coluna_a_coluna` (linhas 292–297) e `linha_a_linha` (linhas
306–308) com `[A,B,C,D,E]` e `K=2` são matematicamente corretos e
implementáveis.

**Lacunas de comportamento para entradas inválidas** (audit points 14–18):
ver achados PR-M-01 a PR-M-04. O audit point 14 (modo desconhecido) está
coberto (linha 252: "outros valores → `RenderizadorErro`"). Os pontos 15–18
permanecem não definidos.

---

## Verificação de ordem e âncoras

- **`ordem.politica = "declaracao"`**: valor normativo correto (ADR-0014
  linha 302; contrato seção 17 linhas 524–526). OK.
- **Ordem base é `barra_de_menus.chips[]`**: Sim (linha 197; linha 219:
  "A ordem dos chips na saída visual é exatamente a ordem de declaração em
  `chips[]`"). OK.
- **Âncoras validam a declaração**: Sim (linhas 226–230: "restrições de
  validação"; "O renderer NÃO move automaticamente um chip"). OK.
- **Âncoras não reordenam chips automaticamente**: Sim (linhas 221–224,
  229). OK.
- **Âncora inexistente → erro determinístico**: Sim (critério 17 linha 670:
  "Com âncora para id inexistente em `chips[]`, levanta `RenderizadorErro`").
  OK.
- **Âncora em posição errada → erro determinístico**: Sim (critérios 15–16
  linhas 668–669). OK.
- **IDs reais**: Sim — handoff usa `chip_esc`/`chip_ajuda` (IDs reais dos 4
  JSONs) e instrui explicitamente (linha 188) a usar os IDs reais. OK.

Atende integralmente à atenção especial 2.

---

## Verificação de atualização de testes/snapshots

O handoff reconhece que a renderização horizontal da barra altera
expectativas literais:

- **Permite atualizar `teste_renderizador.py`**: Sim (linhas 611–615; escopo
  positivo item 17; arquivo na lista de permitidos).
- **Permite atualizar `teste_demo.py`**: Sim (linhas 617–619; arquivo na
  lista de permitidos).
- **Permite atualizar `teste_diagnostico.py`**: Sim (linhas 617–619; arquivo
  na lista de permitidos).
- **Permite atualizar `teste_loader.py`**: Sim (arquivo na lista de
  permitidos; cobertura obrigatória linha 784).
- **Permite atualizar `teste_modelo.py`**: Sim (arquivo na lista de
  permitidos; cobertura obrigatória linha 785).

Substituição da contabilidade:

- **Antes**: `L_barra = 2 + N_chips` (linhas 345–348).
- **Depois**: `L_barra = 2 + N_linhas_barra` (linhas 350–354).

O handoff **não** assume `l_barra = 4` nem snapshot antigo como imutável. OK.

Atende integralmente à atenção especial 4.

---

## Verificação de escopo positivo

Pontos 1–17 do escopo positivo (linhas 381–397): migrar 4 JSONs, substituir
`_linhas_barra`, normalizar `distribuicao`, validar âncoras, linha única,
multilinha `coluna_a_coluna`, `linha_a_linha` alternativo, `erro_layout`,
atualizar chamada em `renderizar_tela`, preservar `l_barra`, adicionar testes
para caminho canônico, âncoras violadas, `erro_layout` e atualizar
snapshots/expectativas literais. Todos presentes e detalhados. OK.

O escopo positivo **não puxa correções do H-0015** (preenchimento vertical
solto, distribuição de altura entre elementos do corpo,
placeholder/marcador de console). Atende à atenção especial 5. OK.

---

## Verificação de escopo negativo

Pontos de auditoria 21–27:

- **(21) Não hardcoda lista canônica global de chips**: Sim (linha 425). OK.
- **(22) Não herda regras do `lancador`**: Sim (linha 430). OK.
- **(23) Não mistura chips do `lancador` com `barra_de_menus`**: Sim (linha
  431). OK.
- **(24) Não mistura `barra_de_menus.distribuicao` com `corpo.arranjo`**:
  Sim (reforça A.15; linha 403). OK.
- **(25) Não implementa composição horizontal do corpo**: Sim (linha 403).
  OK.
- **(26) Não corrige distribuição vertical do H-0015**: Sim (linha 406).
  OK.
- **(27) Não implementa grupo com 2 elementos, aninhamento,
  percentual/fração, console real, paginação, filtros, seleção ou registry
  novo**: Sim — escopo negativo explícito (linhas 407–417). OK.

---

## Verificação de arquivos permitidos/proibidos

**Arquivos permitidos** (linhas 463–482):

```text
scripts/config/telas/orquestrador.json
scripts/config/telas/grupo_minimo.json
scripts/config/telas/destino_minimo.json
scripts/config/telas/stub_b.json
scripts/tela/loader.py
scripts/tela/modelo.py
scripts/tela/renderizador.py
scripts/tela/demo.py
scripts/tela/diagnostico.py
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
```

Todos os paths existem no workspace. A lista é **suficiente e mínima** para
o escopo declarado. Os 5 arquivos de teste reais estão corretamente
classificados.

**Arquivos proibidos** (linhas 490–500):

```text
scripts/docs/contratos/            ← todos os arquivos de contrato
scripts/docs/adr/                  ← todos os ADRs
scripts/docs/NOMENCLATURA.md
scripts/docs/INDICE.md
scripts/config/estilo.json
scripts/config/lancador.json
scripts/config/layout_console.json
```

A cláusula de bloqueio `ARCHITECTURE_REVIEW_REQUIRED` (linhas 502, 832–849)
para qualquer arquivo proibido que precise ser alterado está definida.

Atende ao `contrato_processo_desenvolvimento.md` seção 2 ("limites claros de
arquivos permitidos e proibidos") e seção 8 ("escopo permitido e
insuficiente"). OK.

---

## Verificação de critérios de aceite

Os 33 critérios de aceite (linhas 646–696) são **observáveis e testáveis**:

- **JSON (1–7)**: 4 JSONs com `modo = "horizontal_responsiva"`; chips
  preservados; JSONs válidos; `ordem.politica = "declaracao"`.
- **Renderer canônico (8–14)**: assinatura; linha única; multilinha;
  `erro_layout`; `coluna_a_coluna`; `linha_a_linha` implementado ou
  rejeitado.
- **Âncoras (15–18)**: `primeiro`/`ultimo` válidas/violadas; id inexistente.
- **Compatibilidade transitória (19–20)**: alias string; `distribuicao`
  ausente/`None`.
- **Preservações e proibições (21–26)**: cada chip uma vez; nenhum
  inventado/truncado/omitido; chips de `lancador` ausentes; `corpo.arranjo`
  independente.
- **Testes e snapshots (27–33)**: snapshots atualizados; H-0015 preservado;
  `g/d/b/Esc` preservados; diagnóstico determinístico; todos os testes
  passam; nenhum arquivo fora do escopo; nenhum `__pycache__`/`.pyc`.

**H-0015 (atenção especial 5)**:

- Critério 28 (linha 690): "H-0015 continua funcionando com altura explícita,
  considerando o novo `l_barra`". OK.
- Preservações obrigatórias itens 1–2 (linhas 444–445): assinatura de
  `renderizar_tela` e parâmetro `altura` preservados integralmente. OK.
- Escopo negativo (linha 406): "Não corrigir o preenchimento vertical do
  H-0015". OK.

**Fluxo `g/d/b/Esc` (ponto 29)**:

- Critério 29 (linha 691): "`g/d/b/Esc` continuam funcionando". OK.
- Escopo negativo (linha 419): "Não alterar semântica de Esc, g, d, b ou
  Enter". OK.

Atende à atenção especial 5.

---

## Verificação de testes exigidos

A classe `TestLinhasBarra` proposta (linhas 716–780) cobre: linha única,
multilinha, `erro_layout`, alias string, distribuição ausente, chips vazia,
âncoras primeiro/último válidas/violadas/id inexistente, ordem preservada,
chips do `lancador` ausentes, `coluna_a_coluna`, `linha_a_linha` implementado
ou rejeitado, `renderizar_tela` com canônico, preservação de altura H-0015,
altura mínima com barra horizontal, fluxo `g/d/b/Esc`.

Cobertura obrigatória por suíte (linhas 782–788):

- **`teste_loader.py`**: JSONs migrados carregam corretamente; distribuição
  exposta como objeto. OK.
- **`teste_modelo.py`**: modelo expõe distribuição como objeto ao renderer.
  OK.
- **`teste_renderizador.py`**: todos os casos acima + snapshots atualizados.
  OK.
- **`teste_demo.py`**: snapshots atualizados quando necessário. OK.
- **`teste_diagnostico.py`**: diagnóstico determinístico; snapshots
  atualizados se necessário. OK.

Atende aos pontos 32–34 da auditoria.

---

## Achados

### PR-M-01 — Comportamento para `ordem.politica` desconhecida/não suportada não definido

- **Severidade**: média
- **Evidência**: O handoff suporta apenas `"declaracao"`. Não define
  comportamento para:
  - `"grupos_declarados"` (valor presente na ADR-0014 linha 302 e no
    contrato seção 17, mas não implementado neste ciclo);
  - valores desconhecidos/inválidos.
  Audit point 15. Persiste do M-002 da auditoria anterior.
- **Impacto**: JSON hipotético com `politica` não suportada teria
  comportamento indefinido no renderer. Para a migração canônica (todos os
  4 JSONs usam `"declaracao"`), não há impacto.
- **Recomendação**: Recomenda-se que o implementador trate qualquer
  `politica` diferente de `"declaracao"` como `RenderizadorErro`
  determinístico (decisão local, sem nova norma, seguindo o padrão já
  estabelecido para `modo` desconhecido na linha 252).

### PR-M-02 — Comportamento para `preenchimento_multilinha` desconhecido não definido

- **Severidade**: média
- **Evidência**: O handoff lista `preenchimentos_multilinha_suportados =
  ["coluna_a_coluna", "linha_a_linha"]` e diz que `linha_a_linha` pode ser
  rejeitado com `RenderizadorErro` se não implementado (linha 310), mas não
  define explicitamente o comportamento para valores fora dessa lista.
  Audit point 16. Persiste do M-003 da auditoria anterior.
- **Impacto**: JSON com `preenchimento_multilinha` inválido teria
  comportamento indefinido. Para a migração canônica
  (`coluna_a_coluna`), não há impacto.
- **Recomendação**: Recomenda-se que o implementador trate valores fora de
  `preenchimentos_multilinha_suportados` como `RenderizadorErro`
  determinístico.

### PR-M-03 — Comportamento para limites inválidos em `linhas.minimo`/`linhas.maximo` não definido

- **Severidade**: média
- **Evidência**: O handoff fixa valores canônicos (`minimo=1`, `maximo=2`)
  mas não define comportamento para entradas inválidas (ex.: `minimo >
  maximo`, valores não inteiros, `maximo < 1`). Audit point 17. Persiste do
  M-001 da auditoria anterior.
- **Impacto**: Renderer recebendo JSON malformado sem regra determinística
  de rejeição. Para a migração canônica (valores válidos), não há impacto.
- **Recomendação**: Recomenda-se que o implementador trate
  `minimo > maximo`, `maximo < 1` e tipos inválidos como `RenderizadorErro`
  antes do cálculo de layout.

### PR-M-04 — Comportamento para `overflow.quando_nao_couber` desconhecido não definido

- **Severidade**: média
- **Evidência**: O handoff assume `overflow.quando_nao_couber = "erro_layout"`
  como único valor, mas não define comportamento para outros valores.
  Audit point 18. Persiste do M-004 da auditoria anterior.
- **Impacto**: Valor alternativo de overflow teria comportamento
  indefinido. Para a migração canônica (`erro_layout`), não há impacto.
- **Recomendação**: Recomenda-se que o implementador trate apenas
  `"erro_layout"` como aceito; demais valores levantam `RenderizadorErro`.

### PR-N-01 — Campo `preenchimentos_multilinha_suportados` ausente da estrutura canônica de referência da ADR-0014

- **Severidade**: nota
- **Evidência**: A estrutura canônica de referência na ADR-0014 (linhas
  217–289) não inclui o campo `preenchimentos_multilinha_suportados`; o
  handoff o introduz como campo canônico nos 4 JSONs (linha 158). A ADR-0014
  (linhas 314–317) permite ao handoff "confirmar ou refinar" valores no
  contrato/JSON, mas o campo em si é uma extensão estrutural, não um
  refinamento de valor. Persiste do N-001 da auditoria anterior.
- **Impacto**: Baixo; não contradiz semântica da ADR, apenas a estende com
  metadados sobre modos suportados pela implementação H-0016.
- **Recomendação**: Registrar o campo em revisão futura da ADR/contrato, ou
  tratá-lo como constante interna do renderer. Não bloqueia este ciclo.

### PR-N-02 — `loader.py` e `modelo.py` na lista de permitidos apesar de escopo negativo proibir alteração

- **Severidade**: nota
- **Evidência**: `scripts/tela/loader.py` e `scripts/tela/modelo.py` constam
  da lista de "Arquivos permitidos" (linhas 469–470), mas o escopo negativo
  (linha 432) diz "Não alterar `loader.py` nem `modelo.py` para validar ou
  transformar `distribuicao`". A justificativa para inclusão (linha 484)
  menciona "validação/carga, modelo exposto", mas em prática nenhuma
  alteração de fonte é necessária (o dict bruto já preserva o objeto
  canônico).
- **Impacto**: Baixo; inclusão super permissiva mas sem dano — o implementador
  que ler o escopo negativo entenderá a proibição. Apenas `teste_loader.py`
  e `teste_modelo.py` ganham novas asserções.
- **Recomendação**: Em revisão futura, considerar remover `loader.py` e
  `modelo.py` (fonte) da lista de permitidos para reduzir ambiguidade, ou
  adicionar nota explicativa de que estão listados apenas como precaução.

---

## Conclusão

O handoff H-0016 revisado **endereçou integralmente os 4 achados
bloqueantes/altos** da auditoria anterior (B-001, B-002, B-003, A-001) e
está **alinhado à ADR-0014**, ao `contrato_barra_de_menus.md`, ao
`contrato_tela_json.md`, ao `contrato_processo_desenvolvimento.md` e ao
`contrato_json_barra_de_menus.md`. Não introduz normas novas sem lastro
documental (após a correção de B-002) e não contradiz nenhum contrato ou
ADR.

O handoff permite implementar, sem decisão arquitetural adicional:

1. Migração dos 4 JSONs ativos para `barra_de_menus.distribuicao` como
   objeto canônico.
2. Preservação/exposição da distribuição pelo loader/modelo (dict bruto).
3. Renderização horizontal responsiva da `barra_de_menus` a partir do JSON.
4. Validação de âncoras como restrição (não reordenação).
5. Compatibilidade transitória com alias string `"horizontal"`.
6. Atualização de testes/snapshots afetados pela mudança física da barra.
7. Preservação do H-0015 e dos fluxos `g/d/b/Esc`.

Persistem 4 achados de severidade média (PR-M-01 a PR-M-04) sobre
comportamentos não definidos para valores inválidos de
`ordem.politica`/`preenchimento_multilinha`/`linhas.*`/`overflow`, e 2 notas
(PR-N-01, PR-N-02). Nenhum é bloqueante: a migração canônica usa apenas
valores válidos, o handoff define o padrão defensivo para `modo`
desconhecido (linha 252), e a seção "Critérios de bloqueio" oferece rota de
fuga `ARCHITECTURE_REVIEW_REQUIRED` para casos imprevistos.

---

## Próxima ação recomendada

```text
1. Liberar o handoff H-0016 revisado para implementação com status
   AUDIT_APPROVED_WITH_NOTES.
2. Recomendar ao implementador (OpenCode / GLM) que trate os valores
   inválidos identificados em PR-M-01 a PR-M-04 como RenderizadorErro
   determinístico, seguindo o padrão já estabelecido para modo desconhecido
   (linha 252 do handoff). Isso é decisão local de implementação e não exige
   nova norma.
3. Implementar H-0016 seguindo a ordem recomendada no handoff (linhas
   874–881): migrar JSONs → implementar _linhas_barra → atualizar chamada
   → rodar testes → atualizar snapshots → adicionar novos testes → criar
   IMP-0016.
4. Registrar PR-N-01 (preenchimentos_multilinha_suportados) e PR-N-02
   (loader/modelo na lista de permitidos) para revisão futura de
   ADR/contrato/handoff, sem bloquear o ciclo atual.
```
