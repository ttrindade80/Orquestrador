# RELATORIO_AUDITORIA_H-0016_HANDOFF

Auditoria do handoff `H-0016 — Migração de JSON e renderização horizontal
responsiva da barra de menus`.

```text
auditor:        OpenCode / GLM (papel QA/auditoria de handoff)
data:           2026-07-09
alvo:           scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
commit-base:    b2eb458  feat: ocupa altura do terminal pelo corpo
ciclo:          H-0016
```

---

## Status final

```text
AUDIT_REJECTED
```

Motivo: o handoff é **ambíguo, internamente contraditório e insuficiente para
implementação segura**. Foram identificados **3 achados bloqueantes**:

1. **B-001 (bloqueante)** — Erro sistemático de path: o handoff referencia
   `scripts/testes/` que **não existe** no workspace. Todos os testes estão em
   `scripts/tela/`. As listas de "Arquivos permitidos" e "Arquivos proibidos"
   estão incorretas para todos os arquivos de teste, tornando o escopo de
   arquivos não operacional.
2. **B-002 (bloqueante / `ARCHITECTURE_REVIEW_REQUIRED`)** — O handoff introduz
   `ordem.politica = "declaracao_validada"`, valor **não definido** na ADR-0014
   (que fixa apenas `declaracao | grupos_declarados`) nem em
   `contrato_barra_de_menus.md`. Contradição normativa com ADR/contrato.
3. **B-003 (bloqueante)** — Contradição interna: o handoff exige simultaneamente
   "Não remover nem alterar testes existentes" e "Todos os 398+ testes
   existentes continuem passando", mas a própria alteração de renderização
   (chips verticais → horizontais) **quebra asserções literais hardcoded** em
   testes existentes (`_EXPECTED_ORQUESTRADOR`, `l_barra = 4`).

O item B-002, isoladamente, também classificaria como
`ARCHITECTURE_REVIEW_REQUIRED`. O status final `AUDIT_REJECTED` reflete o
conjunto de bloqueios de implementação segura.

---

## Arquivos analisados

```text
scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md
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

Verificação estrutural adicional (auditoria):

```text
find scripts -type d -name "testes"   →  (nenhum resultado)
find scripts -name "teste_*.py"       →  todos em scripts/tela/
find scripts -name "teste_chip*"      →  (nenhum resultado)
```

---

## Comandos executados

```bash
git log --oneline -6
git status --short
git diff --stat
git diff --name-only
find scripts -type d -name "testes"
find scripts -name "teste_*.py"
find scripts -name "teste_chip*"
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

git diff --stat:    (vazio)
git diff --name-only: (vazio)
```

Estado do workspace **conforme esperado**: HEAD em `b2eb458`; único arquivo novo
não rastreado é o próprio handoff H-0016. Sem outros arquivos modificados ou
não rastreados. **Nenhum achado de escopo** de arquivos fora do esperado.

---

## Resumo executivo

O handoff H-0016 é **bem estruturado, detalhado e, em larga medida, alinhado à
ADR-0014**. Cobre corretamente: migração dos 4 JSONs ativos, preservação dos
chips (não adicionar/remover/reordenar/alterar), validação de âncoras como
restrição (não reordenação), compatibilidade transitória com o alias
`"horizontal"`, algoritmo normativo mínimo (linha única → multilinha →
`erro_layout`), preservação do H-0015 (altura explícita, `l_barra =
len(linhas_barra) + 2`, erro determinístico de altura insuficiente) e
preservação do fluxo `g/d/b/Esc`. Os IDs de âncora (`chip_esc`, `chip_ajuda`)
correspondem aos IDs reais dos 4 JSONs ativos.

Contudo, **não está pronto para implementação segura** devido a 3 achados
bloqueantes:

- **B-001**: paths `scripts/testes/*` inexistentes — todo o bloqueio de escopo
  de arquivos de teste está comprometido;
- **B-002**: valor normativo `declaracao_validada` ausente da ADR-0014 e do
  contrato;
- **B-003**: contradição entre "preservar testes existentes" e a mudança
  observável de layout que invalida asserções literais existentes.

Há ainda 4 achados de severidade média (comportamentos não especificados para
valores inválidos de `linhas.*`, `ordem.politica`, `preenchimento_multilinha` e
`overflow.quando_nao_couber`) e 2 notas (campo novo
`preenchimentos_multilinha_suportados` fora da estrutura canônica da ADR;
convenção de path `scripts/` divergente do H-0015).

Recomendação: **rejeitar o handoff para revisão**. Os bloqueios B-001 e B-003
são corrigíveis no próprio handoff; B-002 exige decisão
arquitetural/documental (ou alterar a ADR-0014/contrato para registrar
`declaracao_validada`, ou usar o valor `declaracao` já normatizado).

---

## Verificação de aderência à ADR-0014

| Item da ADR-0014 | Cobertura no H-0016 | Status |
|---|---|---|
| A.1 — barra declarativa por tela (ADR-0012) preservada | Sim (escopo negativo não reabre política declarativa) | OK |
| A.2 — campo controlador é `barra_de_menus.distribuicao` (termo específico) | Sim | OK |
| A.3 — `"horizontal"` não é linha única fixa | Sim (algoritmo responsivo) | OK |
| A.4 — `"horizontal"` = horizontal responsiva | Sim | OK |
| A.5 — `"horizontal"` é alias transitório | Sim (compatibilidade transitória mantida) | OK |
| A.6 — formato canônico é objeto declarativo `modo = "horizontal_responsiva"` | Sim | OK |
| A.7 — renderer respeita declaração da instância | Sim | OK |
| A.8 — renderer não empilha um chip por linha quando horizontal | Sim (substitui `_linhas_barra` atual) | OK |
| A.9 — renderer não reordena chips por heurística | Sim (ordem por declaração; âncoras como validação) | OK |
| A.10 — renderer não inventa chips ausentes | Sim | OK |
| A.11 — renderer não completa com lista canônica global | Sim (escopo negativo) | OK |
| A.12 — erro de layout vira erro determinístico, não omissão silenciosa | Sim (`overflow.quando_nao_couber = "erro_layout"`) | OK |
| A.13 — barra não herda regra do `lancador` | Sim (escopo negativo) | OK |
| A.14 — chips de itens do `lancador` não são chips da barra | Sim (escopo negativo) | OK |
| A.15 — distribuição da barra independente de `corpo.arranjo` | Sim (escopo negativo) | OK |
| Parte B — alteração por termo específico completo | Sim (handoff nomeia o termo completo) | OK |
| Estrutura canônica futura (objeto declarativo) | **Parcial** — handoff replica a estrutura, mas usa `ordem.politica = "declaracao_validada"` (valor **fora** da ADR) e adiciona campo `preenchimentos_multilinha_suportados` (ausente da ADR) | **B-002 / N-001** |
| Algoritmo normativo mínimo (passos 1–10) | Sim (linha única → multilinha → erro_layout) | OK |
| Overflow determinístico (`erro_layout`) | Sim | OK |

**Conclusão ADR-0014**: aderência ampla, com **uma divergência normativa
bloqueante** (B-002: `declaracao_validada`) e uma extensão não documentada
(N-001: `preenchimentos_multilinha_suportados`).

---

## Verificação da migração JSON

Inventário pré-migração confirmado pela leitura direta dos 4 JSONs ativos:

| Arquivo | `distribuicao` atual | chips[] (ordem) |
|---|---|---|
| `scripts/config/telas/orquestrador.json` | `"horizontal"` (string) | `chip_esc` (Esc/Sair), `chip_ajuda` (?/Ajuda) |
| `scripts/config/telas/grupo_minimo.json` | `"horizontal"` (string) | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |
| `scripts/config/telas/destino_minimo.json` | `"horizontal"` (string) | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |
| `scripts/config/telas/stub_b.json` | `"horizontal"` (string) | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |

Verificação dos pontos de auditoria de migração:

- **(1) Inclui migração dos 4 JSONs como escopo positivo**: Sim (escopo positivo
  itens 1–4; critérios 1–4). OK.
- **(2) Não adia migração para ciclo futuro**: Sim — a migração é entrega
  obrigatória deste ciclo. OK.
- **(3) Define estrutura canônica suficiente para `distribuicao`**: Sim, com
  ressalva B-002 (usa valor `declaracao_validada` fora da ADR). Parcial.
- **(4) Preserva exatamente a lista de chips em cada JSON**: Sim (escopo
  negativo: "Os demais campos de `barra_de_menus` (especialmente `chips[]`) não
  devem ser alterados"; critério 5). OK.
- **(5) Proíbe adicionar chips canônicos ausentes**: Sim (reforça A.11;
  escopo negativo). OK.
- **(6) Proíbe remover chips existentes**: Sim. OK.
- **(7) Proíbe reordenar chips existentes**: Sim (`nao_reordenar`;
  `ordem.politica` por declaração). OK.
- **(8) Proíbe alterar `id/tecla/texto/acao/regra_existencia/regra_ativo/forma_exibicao`**:
  Sim (escopo negativo: "Os demais campos de `barra_de_menus` (especialmente
  `chips[]`) não devem ser alterados"). OK.
- **(9) Renderer usa a declaração do JSON, não defaults inventados fora do JSON**:
  Sim (regras técnicas 1–5). OK.
- **(10) Compatibilidade transitória com `"distribuicao": "horizontal"` sem
  substituir o caminho canônico**: Sim (seção "Compatibilidade transitória";
  critérios 15–16). OK.

Os IDs de âncora propostos (`chip_esc`, `chip_ajuda`) batem com os IDs reais
presentes nos 4 JSONs. OK.

---

## Verificação de loader/modelo

- `scripts/tela/loader.py:349-358` retorna `barra_de_menus` como dict bruto
  preservado (`dados.get("barra_de_menus")`), sem validar nem transformar
  `distribuicao`.
- `scripts/tela/modelo.py:79` declara `barra_de_menus: dict` e `construir_modelo`
  repassa o dict sem inspeção de `distribuicao`.

O handoff está **alinhado** a esse comportamento: o escopo negativo proíbe
alterar `loader.py`/`modelo.py` para validar `distribuicao` e atribui a
validação ao renderer. **(11) Define o papel de loader.py e modelo.py de forma
suficiente**: Sim. OK.

Não há, portanto, exigência de mudança em loader/modelo — o que é coerente com
o fato de `distribuicao` ser preservado como declaração inerte até o renderer.

---

## Verificação de renderização horizontal responsiva

O algoritmo descrito (seção "Algoritmo de renderização horizontal responsiva")
cobrem os pontos de atenção especial 3:

| Requisito (Atenção especial 3) | Cobertura | Status |
|---|---|---|
| 1. linha única quando couber | `tentativa_inicial = "linha_unica"`; fluxo passo 5 | OK |
| 2. multilinha quando linha única não couber | `quebra = "multilinha_quando_nao_couber"`; fluxo passo 6 | OK |
| 3. preenchimento coluna_a_coluna | Seção dedicada com fórmula `ceil(N/K)` e exemplo | OK |
| 4. linha_a_linha implementado ou rejeitado deterministicamente | Implementado como modo alternativo suportado | OK |
| 5. `erro_layout` quando não couber em `linhas.maximo` | Fluxo passo 7; critério 10–11 | OK |
| 6. cada chip aparece exatamente uma vez | `nao_omitir_chips`; regras 3–4; critério 20 | OK |
| 7. nenhum chip truncado/omitido/inventado/reordenado | `nao_truncar_texto`, `nao_omitir_chips`, `nao_reordenar`; A.10/A.11 | OK |

Assinatura `_linhas_barra(barra_de_menus: dict, content_w: int) -> list[str]`
e atualização da chamada em `renderizar_tela` (passando `content_w = total_w -
3`) estão especificadas e coerentes com o código atual
(`scripts/tela/renderizador.py:361` e `:327`). O invariante `l_barra =
len(linhas_barra) + 2` permanece válido porque `_linhas_barra` continua
retornando lista de strings (1 ou 2 elementos conforme o encaixe).

** Lacunas de comportamento para entradas inválidas** (audit points 13–17) —
ver seção "Achados" M-001 a M-004: o handoff não define explicitamente o
comportamento para `modo` desconhecido (parcialmente coberto), `ordem.politica`
desconhecida, `preenchimento_multilinha` desconhecido,
`overflow.quando_nao_couber` desconhecido e limites inválidos em
`linhas.minimo`/`linhas.maximo`.

Nota sobre `content_w`: a regra técnica 8 afirma que `content_w = total_w - 3`,
coerente com `scripts/tela/renderizador.py:327`. OK.

---

## Verificação de ordem e âncoras

- **`ordem.politica`**: o handoff usa **`"declaracao_validada"`**, valor **não
  presente** na ADR-0014 (que fixa `declaracao | grupos_declarados` — ver
  `ADR-0014` seção "Campos e semânticas" e "Ordem e âncoras") nem em
  `contrato_barra_de_menus.md` seção 17 (que repete `declaracao |
  grupos_declarados`). → **B-002**.
- **Âncoras como validação, não reordenação**: Sim — handoff deixa claro que o
  renderer NÃO move chips para satisfazer âncoras; violação é erro
  (`RenderizadorErro`). Atende ao ponto 18 e à atenção especial 2. OK.
- **Âncora inexistente**: o handoff define que `ancoras.primeiro`/`ultimo`
  validam `chips[0].id`/`chips[-1].id`; se o id declarado na âncora não existir
  em `chips[]`, a comparação falha e levanta erro determinístico. Atende à
  atenção especial 2. OK.
- **Âncora em posição errada**: Sim — erro determinístico (critérios 12–13). OK.
- **IDs reais**: o handoff usa `chip_esc`/`chip_ajuda`, que são exatamente os
  IDs reais nos 4 JSONs ativos, e explicita essa correspondência (linha 187).
  Atende ao ponto 19 e à atenção especial 2. OK.

---

## Verificação de escopo positivo

Pontos 1–17 do escopo positivo (migrar 4 JSONs, substituir `_linhas_barra`,
normalizar `distribuicao`, validar âncoras, linha única, multilinha
`coluna_a_coluna`, `linha_a_linha`, `erro_layout`, atualizar chamada em
`renderizar_tela`, preservar `l_barra`, adicionar testes): todos presentes e
detalhados. OK.

O escopo positivo **não puxa correções do H-0015** (preenchimento vertical
solto, distribuição de altura entre elementos do corpo,
placeholder/marcador de console) — atende à atenção especial 4. OK.

---

## Verificação de escopo negativo

Pontos de auditoria 21–26:

- **(21) Não herda regras do `lancador`**: Sim (reforça A.13; escopo negativo).
  OK.
- **(22) Não mistura chips do `lancador` com `barra_de_menus`**: Sim (reforça
  A.14). OK.
- **(23) Não mistura `barra_de_menus.distribuicao` com `corpo.arranjo`**: Sim
  (reforça A.15). OK.
- **(24) Não implementa composição horizontal do corpo**: Sim. OK.
- **(25) Não corrige distribuição vertical do H-0015**: Sim — o handoff
  preserva o bloco `altura` integralmente. OK.
- **(26) Não implementa grupo com 2 elementos, aninhamento,
  percentual/fração, console real, paginação, filtros, seleção ou registry
  novo**: Sim — escopo negativo explícito. OK.

---

## Verificação de arquivos permitidos/proibidos

**Achado bloqueante B-001** — Erro sistemático de path em arquivos de teste.

O handoff declara (seção "Arquivos permitidos"):

```text
scripts/config/telas/orquestrador.json
scripts/config/telas/grupo_minimo.json
scripts/config/telas/destino_minimo.json
scripts/config/telas/stub_b.json
scripts/tela/renderizador.py
scripts/testes/teste_renderizador.py        ← PATH INEXISTENTE
scripts/docs/relatorios/IMP-0016-...md
```

E na seção "Arquivos proibidos":

```text
scripts/testes/teste_loader.py              ← PATH INEXISTENTE
scripts/testes/teste_modelo.py              ← PATH INEXISTENTE
scripts/testes/teste_demo.py                ← PATH INEXISTENTE
scripts/testes/teste_chip.py                ← PATH INEXISTENTE (arquivo não existe em lugar algum)
```

Verificação estrutural do workspace:

```text
find scripts -type d -name "testes"   →  (não existe)
find scripts -name "teste_*.py"       →  todos em scripts/tela/
find scripts -name "teste_chip*"      →  (não existe)
```

Os arquivos reais são:

```text
scripts/tela/teste_renderizador.py
scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
```

**Impactos concretos**:

1. O arquivo que o implementador deve editar (`scripts/tela/teste_renderizador.py`)
   **não está na lista de permitidos** — está apenas o path inexistente
   `scripts/testes/teste_renderizador.py`.
2. Seguindo o handoff literalmente, o implementador criaria
   `scripts/testes/teste_renderizador.py`, que **nunca seria executado** pela
   infraestrutura de testes atual (que roda `python tela/teste_renderizador.py`
   a partir de `scripts/`).
3. Os arquivos reais `scripts/tela/teste_demo.py` e
   `scripts/tela/teste_diagnostico.py` **não aparecem em nenhuma das duas
   listas** (permitidos/proibidos) — o implementador fica sem orientação sobre
   se pode atualizá-los caso suas asserções quebrem com a mudança de layout.
4. A lista de proibidos referencia `scripts/testes/teste_chip.py`, arquivo que
   **não existe** no workspace — indicando erro de inventário.

Esta seção **não é operacional** e compromete a cláusula de escopo mínimo do
`contrato_processo_desenvolvimento.md` (seção 2: "limites claros de arquivos
permitidos e proibidos").

---

## Verificação de critérios de aceite

Os 24 critérios de aceite (JSON 1–6, renderer canônico 7–11, âncoras 12–14,
compatibilidade 15–16, preservações H-0015 17–19, proibições 20–22, testes
23–24) são **observáveis e testáveis**, em sua maioria.

**Contradição B-003** entre critérios:

- **Critério 17**: "renderizar_tela com altura=None produz comportamento
  idêntico ao pré-H-0016 (**exceto pela distribuição horizontal dos chips**)".
- **Critério 23**: "Todos os 398+ testes existentes continuam passando".

O critério 17 admite explicitamente que a saída **muda** (chips antes em 2
linhas verticais passam a 1 linha horizontal quando couber). Em largura 42
(`content_w = 39`), `[Esc] Sair` (10) + 2 espaços + `[?] Ajuda` (9) = 21 ≤ 39,
logo **cabe em linha única** — a barra passa de 4 linhas físicas (topo + 2
chips + base) para 3 (topo + 1 linha horizontal + base).

Testes existentes que **quebram** com essa mudança:

- `scripts/tela/teste_renderizador.py:60-77` (`_EXPECTED_ORQUESTRADOR`)
  codifica a barra com chips empilhados verticalmente; a asserção literal
  `saida == _EXPECTED_ORQUESTRADOR` (linha 252) **falha** após H-0016.
- `scripts/tela/teste_renderizador.py:80-97` (`_EXPECTED_ORQUESTRADOR_RETA`)
  — mesma quebra para borda reta.
- `scripts/tela/teste_renderizador.py:968-970` (`teste_altura_explicita`)
  codifica `l_barra = 4` e `n_minimo = 16`; após H-0016 `l_barra` passa a 3 e
  `n_minimo` a 15, quebrando as asserções que comparam `altura=N_minimo` com
  `altura=None` (linhas 988-991) e a contagem de fills na altura 24.

Contudo, a seção de testes obrigatórios diz: "Não remover nem alterar testes
existentes" (linha 537). Essas duas exigências são **incompatíveis**: não é
possível manter todos os 394/398 testes existentes passando **e** não alterar
testes existentes **e** mudar o layout da barra para horizontal. O
implementador ficaria sem caminho válido.

---

## Verificação de testes exigidos

A classe `TestLinhasBarra` proposta cobre: linha única, multilinha, `erro_layout`,
alias string, distribuição ausente, chips vazia, âncoras
primeiro/último válidas/violadas, ordem preservada, `coluna_a_coluna`,
`renderizar_tela` com canônico e preservação de altura H-0015. Cobertura
**adequada** para renderer.

**Pontos de auditoria 31 (testes para JSON, loader/modelo, renderer, demo e
diagnóstico)**:

- JSON: coberto pelos critérios 1–6 (validade `json.loads` + preservação de
  chips). OK.
- loader/modelo: não há novos testes exigidos — coerente, pois loader/modelo
  não mudam. OK (implícito).
- renderer: coberto pela classe `TestLinhasBarra`. OK.
- **demo e diagnóstico**: o handoff **não exige explicitamente** novos testes
  para `demo.py`/`diagnostico.py`, mas o critério 23 exige que os testes
  existentes desses módulos continuem passando. Como a mudança de layout pode
  invalidar asserções em `teste_demo.py`/`teste_diagnostico.py` (que não estão
  sequer nas listas de arquivos), há lacuna. → A-001 (ligado a B-001/B-003).

---

## Achados

### B-001 — Erro sistemático de path `scripts/testes/` (inexistente)

- **Severidade**: bloqueante
- **Evidência**:
  - Handoff linhas 404, 424–427 referenciam `scripts/testes/teste_*.py`.
  - `find scripts -type d -name "testes"` → nenhum resultado.
  - Testes reais estão em `scripts/tela/teste_*.py` (5 arquivos).
  - `scripts/testes/teste_chip.py` (proibido) não existe em lugar algum.
- **Impacto**: A cláusula de escopo de arquivos é não operacional. O
  implementador não sabe qual arquivo editar (o real
  `scripts/tela/teste_renderizador.py` não está em "permitidos"), e criar
  `scripts/testes/teste_renderizador.py` produziria um arquivo órfão nunca
  executado. Os reais `scripts/tela/teste_demo.py` e
  `scripts/tela/teste_diagnostico.py` ficam sem classificação.
- **Recomendação**: Substituir todas as ocorrências de `scripts/testes/` por
  `scripts/tela/`; adicionar `scripts/tela/teste_diagnostico.py` e
  `scripts/tela/teste_demo.py` à lista de proibidos (ou permitidos
  condicionalmente, caso suas asserções exijam atualização); remover a
  referência a `teste_chip.py` inexistente.

### B-002 — Valor normativo `ordem.politica = "declaracao_validada"` fora da ADR-0014 e do contrato

- **Severidade**: bloqueante (classificável também como
  `ARCHITECTURE_REVIEW_REQUIRED`)
- **Evidência**:
  - Handoff linhas 148, 196, 217, 223–224, 500 usam
    `ordem.politica = "declaracao_validada"`.
  - `ADR-0014` seção "Campos e semânticas" fixa:
    `ordem.politica: declaracao | grupos_declarados`.
  - `contrato_barra_de_menus.md` seção 17 repete: `ordem.politica = "declaracao"`
    ou `"grupos_declarados"`.
  - O próprio handoff (linha 52) determina: "Se qualquer item normativo estiver
    ausente ou conflitante, bloquear com `ARCHITECTURE_REVIEW_REQUIRED`".
- **Impacto**: O JSON migrado carregará um valor de `politica` não reconhecido
  pela ADR/contrato; futura validação contratual poderia rejeitar
  `declaracao_validada` como valor inválido. O handoff introduz norma nova sem
  lastro documental, violando a hierarquia de autoridade
  (`contrato_processo_desenvolvimento.md` seção 3).
- **Recomendação**: Decidir arquiteturalmente entre (a) usar o valor
  `declaracao` já normatizado pela ADR-0014 (e tratar a validação de âncoras
  como comportamento inerente ao renderer, sem renomear a política) ou (b)
  atualizar a ADR-0014 e o `contrato_barra_de_menus.md` para registrar
  `declaracao_validada` antes da implementação. Até lá, manter
  `ARCHITECTURE_REVIEW_REQUIRED`.

### B-003 — Contradição interna sobre preservação de testes existentes

- **Severidade**: bloqueante
- **Evidência**:
  - Handoff linha 537: "Não remover nem alterar testes existentes".
  - Handoff critério 23: "Todos os 398+ testes existentes continuem passando".
  - Handoff critério 17: a saída **muda** (chips verticais → horizontais).
  - `scripts/tela/teste_renderizador.py:60-97` define
    `_EXPECTED_ORQUESTRADOR`/`_EXPECTED_ORQUESTRADOR_RETA` com chips
    empilhados; asserção literal `saida == _EXPECTED_ORQUESTRADOR` (linha 252).
  - `scripts/tela/teste_renderizador.py:968-991` codifica `l_barra = 4` e
    compara `altura=N_minimo` com `altura=None`.
- **Impacto**: Em `largura=42`, os 2 chips (`[Esc] Sair`, `[?] Ajuda`) cabem
  em linha única (≈21 ≤ 39), então a barra passa de 4 para 3 linhas físicas.
  As asserções literais existentes **falham inevitavelmente**, e o implementador
  não pode satisfazer simultaneamente "não alterar testes" + "todos passando".
  Impasse operacional.
- **Recomendação**: Redigir a cláusula de testes para autorizar
  explicitamente a **atualização** das asserções literais afetadas pela
  mudança de layout (e recalculo de `l_barra`/`n_minimo`), mantendo o espírito
  dos testes. Especificar quais testes existentes terão asserções
  atualizadas vs. quais permanecem intocados.

### A-001 — `teste_demo.py` e `teste_diagnostico.py` fora das listas de escopo

- **Severidade**: alta
- **Evidência**: Os arquivos reais `scripts/tela/teste_demo.py` e
  `scripts/tela/teste_diagnostico.py` não aparecem em "permitidos" nem em
  "proibidos" (a lista de proibidos referencia os paths inexistentes
  `scripts/testes/teste_demo.py` etc.).
- **Impacto**: Se as asserções desses módulos dependem do layout da barra
  (provável, dado que `demo.py` renderiza a tela e `diagnostico.py` também),
  a mudança vertical→horizontal pode quebrá-los sem que o implementador tenha
  autorização clara para atualizá-los.
- **Recomendação**: Classificar explicitamente esses dois arquivos (proibidos,
  ou permitidos condicionalmente) e exigir verificação de que continuam
  passando.

### M-001 — Comportamento para limites inválidos em `linhas.minimo`/`linhas.maximo` não definido

- **Severidade**: média
- **Evidência**: O handoff fixa os valores canônicos (`minimo=1`, `maximo=2`)
  mas não define o comportamento para entradas inválidas (ex.: `minimo >
  maximo`, valores não inteiros, `maximo < 1`). Audit point 16.
- **Impacto**: Renderer recebe um JSON malformado sem regra determinística de
  rejeição.
- **Recomendação**: Definir que `minimo > maximo`, `maximo < 1` ou tipos
  inválidos levantam `RenderizadorErro` antes do cálculo de layout.

### M-002 — Comportamento para `ordem.politica` desconhecida não definido

- **Severidade**: média
- **Evidência**: O handoff suporta apenas `declaracao_validada`; não define o
  que fazer com `grupos_declarados` (presente na ADR-0014) nem com valores
  desconhecidos. Audit point 14.
- **Impacto**: Ambiguidade sobre rejeitar ou ignorar políticas não suportadas.
- **Recomendação**: Declarar explicitamente que qualquer `politica` diferente
  do valor suportado levanta `RenderizadorErro` (ou definir fallback
  determinístico).

### M-003 — Comportamento para `preenchimento_multilinha` desconhecido não definido

- **Severidade**: média
- **Evidência**: O handoff lista `preenchimentos_multilinha_suportados =
  ["coluna_a_coluna", "linha_a_linha"]` mas não diz que valor fora dessa lista
  é erro. Audit point 15.
- **Impacto**: JSON com `preenchimento_multilinha` inválido teria comportamento
  indefinido.
- **Recomendação**: Explicitar que valor fora de
  `preenchimentos_multilinha_suportados` levanta `RenderizadorErro`.

### M-004 — Comportamento para `overflow.quando_nao_couber` desconhecido não definido

- **Severidade**: média
- **Evidência**: O handoff assume `overflow.quando_nao_couber = "erro_layout"`
  mas não define comportamento para outros valores. Audit point 17.
- **Impacto**: Valor alternativo de overflow teria comportamento indefinido.
- **Recomendação**: Definir que apenas `"erro_layout"` é aceito; demais valores
  levantam `RenderizadorErro`.

### N-001 — Campo `preenchimentos_multilinha_suportados` ausente da estrutura canônica da ADR-0014

- **Severidade**: nota
- **Evidência**: A estrutura canônica de referência na ADR-0014 não inclui o
  campo `preenchimentos_multilinha_suportados`; o handoff o introduz como campo
  canônico nos 4 JSONs. A ADR-0014 permite ao handoff "confirmar ou refinar"
  valores no contrato/JSON, mas o campo em si é uma extensão.
- **Impacto**: Baixo; não contradiz semântica da ADR, apenas a estende.
- **Recomendação**: Registrar o campo em revisão futura da ADR/contrato, ou
  removê-lo da declaração canônica e tratá-lo como constante interna do
  renderer.

### N-002 — Convenção de path `scripts/` divergente do H-0015

- **Severidade**: nota
- **Evidência**: O H-0016 usa prefixo `scripts/` em todos os caminhos (ex.:
  `scripts/tela/renderizador.py`, `scripts/config/telas/...`). O H-0015 usa
  paths relativos a `scripts/` (ex.: `tela/renderizador.py`,
  `config/telas/...`). Atenção especial 5.
- **Impacto**: Baixo; o projeto pode ser executado da raiz do repo ou de dentro
  de `scripts/`. A divergência pode gerar ambiguidade operacional sobre se os
  comandos devem ser executados da raiz ou de `scripts/`, especialmente porque
  a infraestrutura de testes atual roda `python tela/teste_renderizador.py` a
  partir de `scripts/`.
- **Recomendação**: Padronizar a convenção (recomenda-se executar comandos a
  partir da raiz do repositório e manter o prefixo `scripts/`, ou documentar
  explicitamente o `cd scripts` antes dos comandos de teste).

---

## Conclusão

O handoff H-0016 é **conceitualmente sólido e bem alinhado à ADR-0014** no que
tange à semântica de distribuição horizontal responsiva, âncoras como
validação, overflow determinístico, preservação do H-0015 e preservação do
fluxo `g/d/b/Esc`. O inventário de JSONs e chips está correto, e os IDs de
âncora correspondem aos IDs reais.

Porém, **não está pronto para implementação segura** devido a três bloqueios:

1. **B-001**: erro sistemático de path que torna as listas de arquivos
   permitidos/proibidos não operacionais;
2. **B-002**: valor normativo `declaracao_validada` sem lastro na ADR-0014 ou
   no contrato (exige decisão arquitetural);
3. **B-003**: contradição interna entre "não alterar testes existentes",
   "398+ passando" e a mudança observável de layout da barra.

Somam-se 1 achado alto, 4 médios e 2 notas que devem ser endereçados na
revisão do handoff.

---

## Próxima ação recomendada

```text
1. Devolver o handoff H-0016 ao autor (Claude Code) para revisão, com status
   AUDIT_REJECTED.
2. Corrigir B-001: trocar scripts/testes/ → scripts/tela/ em toda parte;
   classificar teste_demo.py e teste_diagnostico.py; remover teste_chip.py.
3. Decidir B-002 em via arquitetural:
   (a) usar ordem.politica = "declaracao" (valor da ADR-0014); ou
   (b) atualizar ADR-0014 + contrato_barra_de_menus.md para registrar
       "declaracao_validada" antes da implementação.
4. Resolver B-003: autorizar explicitamente a atualização das asserções
   literais afetadas pela mudança de layout (incluindo recalculo de
   l_barra/n_minimo em teste_altura_explicita), listando os testes a alterar.
5. Especificar comportamentos determinísticos para M-001 a M-004 (valores
   inválidos de linhas.*/politica/preenchimento_multilinha/overflow).
6. Reauditar após revisão.
```
