---
name: H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao
description: "Handoff 1/4 do ciclo ADR-0042 (ITEM-0007) — fundação de resolução de politica_navegacao.tipo (fallback de compatibilidade para nivel_unico), preservação integral do comportamento vigente de nivel_unico, passividade de tabela com falha focal em declaração incompatível, e infraestrutura mínima para os três handoffs seguintes sem antecipar seu comportamento"
metadata:
  type: handoff
  status: CONCLUIDO
rastreabilidade:
  handoff: H-0052
  adr: ADR-0042
  item: ITEM-0007
  ordem_no_ciclo: "1/4"
  capacidade: fundacao_e_compatibilidade_das_politicas_de_navegacao
  handoffs_seguintes:
    - id: H-0053
      capacidade: arvore_colapsavel
    - id: H-0054
      capacidade: selecao_multinivel
    - id: H-0055
      capacidade: dois_niveis_por_foco
---

# Handoff H-0052 — Fundação e compatibilidade das políticas de navegação

## 1. Identificação

```yaml
handoff: H-0052
adr: ADR-0042
item: ITEM-0007
ordem_no_ciclo: 1/4
capacidade: fundacao_e_compatibilidade_das_politicas_de_navegacao
```

A quantidade de quatro handoffs deste ciclo é decisão operacional, não
obrigação normativa da ADR-0042.

---

## 2. Estado transportado

```yaml
ADR-0042:
  status: aceita
  qa_adr: ADR_APPROVED
  aplicacao: ADR_APPLIED
  qa_aplicacao: ADR_APPLICATION_APPROVED
implementacao:
  status: IMPLEMENTED
  relatorio: docs/relatorios/IMP-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
  qa: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0052_P08.md
validacao_manual:
  status: MANUAL_VALIDATION_APPROVED
  relatorio: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0052.md
handoffs_aprovados_pelo_usuario:
  quantidade: 4
  decomposicao:
    1: fundacao_e_compatibilidade   # este handoff
    2: arvore_colapsavel            # H-0053
    3: selecao_multinivel           # H-0054
    4: dois_niveis_por_foco         # H-0055
```

---

## 3. Capacidade coesa de H-0052

A implementação futura de H-0052 deve entregar, exclusivamente:

1. Resolução do discriminador `politica_navegacao.tipo`, com fallback de
   compatibilidade `tipo` ausente → `nivel_unico`, restrito ao caso em que
   `politica_navegacao` é objeto válido (D-MULTI-13), e validação
   obrigatória, no carregamento, do valor de `tipo` quando presente contra o
   conjunto fechado de cinco literais — rejeitando valor desconhecido sem
   coerção para `nivel_unico` (D-MULTI-12).
2. Preservação integral do comportamento vigente de `nivel_unico` (D-MULTI-03)
   — nenhum redesenho, quatro setas, topologia toroidal por eixo, exclusão de
   células vazias, foco/cursor/seleção como mecanismos distintos.
3. Comportamento passivo de `tabela` como política de navegação (D-MULTI-04):
   fora do ciclo de foco, sem cursor, sem `[✥]`, sem fallback para
   `nivel_unico`; declaração incompatível (`tabela` com `navegavel: true`)
   produz falha focal usando o mecanismo canônico já existente
   (`TelaEstruturaInvalida`).
4. Infraestrutura mínima compartilhada — uma única função pura de resolução
   do tipo efetivo — que H-0053, H-0054 e H-0055 possam consumir sem duplicar
   a resolução da política.
5. Garantia de que os valores literais `arvore_colapsavel`,
   `selecao_multinivel` e `dois_niveis_por_foco`, quando declarados, são
   transportados fielmente pela função de resolução e **não tornam o console
   focalizável nem navegável por este handoff** — evita que caiam
   silenciosamente no comportamento de `nivel_unico` antes de suas próprias
   políticas serem implementadas. Isso não é comportamento provisório a ser
   desfeito: H-0053/H-0054/H-0055 **adicionam** dispatch específico sobre a
   mesma função de resolução; nada criado aqui precisa ser removido depois.

Não antecipe o comportamento de `arvore_colapsavel`, `selecao_multinivel` ou
`dois_niveis_por_foco` além do item 5 acima.

---

## 4. Autoridade declarativa (transportada da ADR-0042 / contratos)

```json
"politica_navegacao": {
  "navegavel": true,
  "tipo": "nivel_unico"
}
```

- `politica_navegacao` permanece objeto (`contrato_json_console.md` §7.1).
- Discriminador literal: `tipo`.
- Valores fechados: `nivel_unico`, `tabela`, `arvore_colapsavel`,
  `selecao_multinivel`, `dois_niveis_por_foco`.
- `tipo` ausente → efetivo `nivel_unico`; ausência não invalida a
  configuração (D-MULTI-13).
- `navegavel` preserva semântica vigente; não se cria matriz geral
  `navegavel × tipo` além da incompatibilidade fechada para `tabela`
  (D-MULTI-04).
- Proibido: alias, segundo discriminador, segunda forma declarativa,
  inferência por estrutura/apresentação/fixture/nome de arquivo.

---

## 5. Leitura autorizada realizada e proprietários localizados

Leitura integral das seis autoridades do manifesto (ADR-0042,
`contrato_console.md`, `contrato_json_console.md`,
`docs/nomenclatura/32_CONSOLE.md`,
`docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`,
ADR-0041) foi executada nesta etapa de autoria do handoff.

A descoberta focal (`rg` sobre `tela`, `demo`, `config`) localizou os
proprietários atuais, todos lidos:

| Proprietário | Papel atual | Ponto de intervenção |
|---|---|---|
| `tela/navegacao.py` | `console_e_focalizavel()` (linhas 58–74) lê hoje apenas `politica_navegacao.get("navegavel")`; ignora `tipo` por completo. `lista_foco`, `avancar_foco`, `recuar_foco`, `exibir_chip_navegar`, `console_focado` consomem `console_e_focalizavel`/`itens_navegaveis` sem conhecer `tipo`. Já `mover_direita`/`mover_esquerda`/`mover_cima`/`mover_baixo` (via `_mover_horizontal`/`_mover_vertical`) operam diretamente sobre o console recebido e não consultam `console_e_focalizavel`. | Adicionar função pura de resolução de `tipo` efetivo; consumi-la em `console_e_focalizavel`. Ajustar adicionalmente as funções públicas de movimento (ou o ponto comum imediatamente consumido por elas) para que uma chamada direta sobre console `tabela` também não altere o cursor (§7.2). |
| `tela/carregamento/envelope_pre_adr_0028.py` | `_validar_valores_envelope_pre_adr_0028()` (linhas 130–135) hoje só valida que `politica_navegacao` é `dict`; não valida `tipo`. É chamada (linha 315) exclusivamente para consoles do envelope clássico (`itens` + as cinco políticas) — exatamente o escopo de `politica_navegacao.tipo` desta ADR. | Adicionar validação obrigatória de que `tipo`, quando presente, pertence ao conjunto fechado de cinco valores, e validação da combinação incompatível `tipo: "tabela"` + `navegavel: true`, ambas levantando `TelaEstruturaInvalida` (mecanismo canônico já usado exaustivamente neste arquivo — ver `tela/carregamento/erros.py`). |
| `tela/teste_navegacao.py` | Testes unitários puros de `tela/navegacao.py` (dicts locais via `_console()`/`_item()`, sem loader/JSON). | Acrescentar testes focais de H-0052; extensão opcional e retrocompatível do helper `_console()` com parâmetro `tipo_navegacao=None`. |
| `tela/teste_loader.py` | Testes do loader, incluindo validações estruturais que levantam `TelaEstruturaInvalida` via `envelope_pre_adr_0028.py`. | Acrescentar teste focal da falha focal de `tabela` navegável. |
| `demo/demo_navegacao.py` | Ponto de entrada real de demonstração TTY do H-0040/ADR-0031 (`python -m demo.demo_navegacao --tela <json>`), reutiliza `demo/demo.py` integralmente. | Nenhuma alteração de código; apenas consumido para demonstração com novas fixtures. |

---

## 6. Escopo futuro nominal (arquivos alteráveis)

A implementação futura de H-0052 pode alterar **somente**:

```text
tela/navegacao.py
tela/carregamento/envelope_pre_adr_0028.py
tela/teste_navegacao.py
tela/teste_loader.py
```

E pode **criar** (arquivos novos, caminho nominal fechado):

```text
config/telas/demo/h0052_nivel_unico_explicito.json
config/telas/demo/h0052_tabela_passiva.json
docs/relatorios/IMP-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
```

Nenhum outro arquivo de código, teste ou configuração pode ser alterado sem
passar pela cláusula de exceção (§13).

### 6.1 Arquivos preservados (não alterar)

```text
docs/adr/ADR-0042-navegacao-multinivel-do-console.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/nomenclatura/32_CONSOLE.md
docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
docs/adr/ADR-0041-paginacao-universal-por-pageup-e-pagedown.md
docs/backlog.md
tela/distribuicao_matricial.py
tela/paginacao.py
tela/selecao.py
tela/modelo.py
tela/loader.py
tela/renderizacao/**
demo/demo.py
demo/demo_navegacao.py
config/telas/demo/h0030_console_unico.json
config/telas/demo/h0045_validacao_nova_pagina.json
```

`tela/loader.py` só importa `_console_em_escopo_d23` de
`envelope_pre_adr_0028.py`; a alteração desta etapa fica interna ao módulo
`envelope_pre_adr_0028.py` e não exige tocar `tela/loader.py`. Se a
implementação futura constatar que isso é insuficiente, aplica-se a cláusula
de exceção (§13) — não uma alteração automática.

---

## 7. Especificação de comportamento a implementar

### 7.1 Função de resolução (infraestrutura compartilhada)

Criar em `tela/navegacao.py` uma função pura, por exemplo
`tipo_navegacao_efetivo(elemento)`:

- lê `elemento._campos_inertes.get("politica_navegacao")`;
- se for `dict` e não houver chave `tipo`, retorna o literal `"nivel_unico"`
  (fallback de compatibilidade, D-MULTI-13);
- se **não** for `dict`, a função **não** normaliza para `"nivel_unico"`: essa
  forma é estruturalmente inválida e já é rejeitada pelo carregamento vigente
  (§7.3) antes de alcançar um console em uso; a função de resolução não
  mascara esse erro estrutural nem inventa comportamento de compatibilidade
  para ele — `politica_navegacao` continua obrigatoriamente objeto
  (`contrato_json_console.md` §7.1);
- se houver `tipo`, retorna o valor literal exatamente como declarado —
  **sem** coagir `arvore_colapsavel`, `selecao_multinivel` ou
  `dois_niveis_por_foco` para `"nivel_unico"`;
- não infere `tipo` de estrutura, apresentação, fixture ou nome de arquivo;
- não valida aqui o conjunto fechado de valores (validação obrigatória
  pertence ao carregamento, §7.3) — a função de navegação apenas resolve e
  transporta uma entrada já estruturalmente válida.

### 7.2 `console_e_focalizavel` (nivel_unico e tabela)

Ajustar `console_e_focalizavel(elemento)` para:

- quando `tipo_navegacao_efetivo(elemento) == "tabela"`: retornar sempre
  `False` (não focalizável), independentemente de `navegavel` — a
  passividade de `tabela` não depende de `navegavel` ser `true` (o caso
  `true` é erro de carregamento, tratado em §7.3, e nunca deveria alcançar
  esta função num JSON validado; a checagem aqui é defensiva e não substitui
  a validação de carga);
- quando `tipo_navegacao_efetivo(elemento)` for `"arvore_colapsavel"`,
  `"selecao_multinivel"` ou `"dois_niveis_por_foco"`: retornar sempre
  `False` nesta etapa — nenhum dispatch de comportamento é criado por
  H-0052; a política é reconhecida e transportada, mas fica inerte até seu
  próprio handoff;
- quando `tipo_navegacao_efetivo(elemento) == "nivel_unico"` (explícito ou
  por ausência): preservar exatamente a lógica vigente (`navegavel` +
  presença de item navegável) — nenhuma outra condição é adicionada.

As funções `itens_navegaveis`, `grade_de_itens`, `avancar_foco`,
`recuar_foco`, `exibir_chip_navegar` e `console_focado` não precisam mudar:
todas dependem de `console_e_focalizavel`/`lista_foco`, que já filtram
corretamente uma vez ajustadas conforme acima.

`mover_direita`, `mover_esquerda`, `mover_cima` e `mover_baixo` exigem
atenção separada. Requisito comportamental, válido inclusive fora do fluxo
usual mediado por `console_e_focalizavel`/`lista_foco`:

```text
console com tipo_navegacao_efetivo = tabela
+
chamada direta de mover_direita / mover_esquerda / mover_cima / mover_baixo
→ nenhuma alteração de cursor
```

A implementação futura fica autorizada a alterar, dentro de
`tela/navegacao.py`, as funções públicas de movimento ou o ponto comum
imediatamente consumido por elas (por exemplo `_mover_horizontal`/
`_mover_vertical`), para que rejeitem ou façam no-op quando o console
resolvido for `tabela`. Não se prescreve arquitetura além do necessário; cabe
ao implementador escolher a menor solução dentro desse arquivo, desde que:

- `nivel_unico` permaneça com comportamento integralmente inalterado;
- `tabela` seja realmente passiva mesmo em chamada direta às quatro funções;
- as três políticas futuras continuem sem comportamento antecipado;
- nenhuma função de seleção ou paginação seja alterada.

### 7.3 Falha focal de `tabela` navegável (carregamento)

Em `_validar_valores_envelope_pre_adr_0028` (`envelope_pre_adr_0028.py`,
após a validação existente de que `politica_navegacao` é `dict`, linhas
130–135): quando `politica_navegacao.get("tipo") == "tabela"` **e**
`politica_navegacao.get("navegavel")` for verdadeiro, levantar
`TelaEstruturaInvalida` com mensagem explicando a incompatibilidade.

Não inventar novo momento, camada ou mecanismo de falha — este é o
mecanismo canônico já usado por todo o restante do arquivo para exatamente
este tipo de rejeição estrutural. Não criar segunda política de erro.

É obrigatório validar, no mesmo ponto de intervenção, o conjunto fechado de
`tipo` quando presente. A validação deve:

- aceitar somente os cinco literais fechados: `nivel_unico`, `tabela`,
  `arvore_colapsavel`, `selecao_multinivel`, `dois_niveis_por_foco`;
- rejeitar valor textual desconhecido, levantando `TelaEstruturaInvalida`
  (mesmo mecanismo canônico, sem segunda camada de erro);
- rejeitar forma não textual de `tipo` quando incompatível com o contrato
  vigente;
- não criar alias nem fazer coerção de valor inválido;
- não converter valor inválido para `nivel_unico`;
- não criar matriz geral `navegavel × tipo` além da incompatibilidade fechada
  de `tabela` + `navegavel: true` já especificada acima — nenhuma outra
  combinação normativa entre `navegavel` e `tipo` é criada por H-0052.

A validação do literal, para os três valores futuros
(`arvore_colapsavel`, `selecao_multinivel`, `dois_niveis_por_foco`), confirma
apenas que o discriminador é reconhecido; não implica focalizabilidade nem
qualquer comportamento antecipado desses valores (§7.2, §3 item 5).

---

## 8. Entradas mínimas de teste

### Caso LEGADO

```json
"politica_navegacao": { "navegavel": true }
```

Resultado: `tipo_navegacao_efetivo` = `"nivel_unico"`; console focalizável
nas mesmas condições vigentes.

### Caso EXPLICITO_NIVEL_UNICO

```json
"politica_navegacao": { "navegavel": true, "tipo": "nivel_unico" }
```

Resultado: idêntico ao caso LEGADO — mesmo comportamento efetivo.

### Caso TABELA (válido, passivo)

```json
"politica_navegacao": { "navegavel": false, "tipo": "tabela" }
```

Resultado: console nunca focalizável; sem cursor; sem `[✥]`.

### Caso TABELA_INCOMPATIVEL (falha focal)

```json
"politica_navegacao": { "navegavel": true, "tipo": "tabela" }
```

Resultado: `TelaEstruturaInvalida` no carregamento.

### Caso NAO_OBJETO (rejeição estrutural, sem fallback)

```json
"politica_navegacao": "navegavel"
```

(ou qualquer valor não-`dict`, por exemplo lista ou número.)

Resultado: rejeitado pelo carregamento vigente (`TelaEstruturaInvalida`);
`tipo_navegacao_efetivo` não é chamada para normalizar essa entrada em
`nivel_unico` — não há fallback para forma estruturalmente inválida.

### Caso TIPO_DESCONHECIDO (rejeição de enumeração)

```json
"politica_navegacao": { "navegavel": true, "tipo": "grade_livre" }
```

Resultado: `TelaEstruturaInvalida` no carregamento — valor textual fora do
conjunto fechado de cinco literais, sem coerção para `nivel_unico`.

### Caso TIPO_NAO_TEXTUAL (rejeição de forma), quando aplicável ao validador

```json
"politica_navegacao": { "navegavel": true, "tipo": 1 }
```

Resultado: `TelaEstruturaInvalida` no carregamento, se essa fronteira for
diretamente aplicável ao validador vigente.

### Casos de transporte literal (handoffs futuros)

```json
"politica_navegacao": { "navegavel": true, "tipo": "arvore_colapsavel" }
"politica_navegacao": { "navegavel": true, "tipo": "selecao_multinivel" }
"politica_navegacao": { "navegavel": true, "tipo": "dois_niveis_por_foco" }
```

Resultado: `tipo_navegacao_efetivo` retorna o literal declarado;
`console_e_focalizavel` retorna `False` para os três (§7.2).

Se a representação real exigir campos adicionais além dos mostrados, usar a
forma mínima já existente em `tela/teste_navegacao.py::_console()` (dicts
locais) ou nas fixtures de `config/telas/demo/`. Não inventar schema
paralelo de teste.

---

## 9. Fixtures

### 9.1 Testes unitários (`tela/teste_navegacao.py`, `tela/teste_loader.py`)

Reutilizar o padrão local de construção de `ElementoCorpo` já existente em
`tela/teste_navegacao.py::_console()`/`_item()` — sem tocar em JSON. Extensão
opcional retrocompatível do helper `_console()` com parâmetro
`tipo_navegacao=None` (quando `None`, comportamento idêntico ao atual, sem
chave `tipo` no dict de `politica_navegacao`).

### 9.2 Demonstração (`demo/demo_navegacao.py`)

- Caso LEGADO: reutilizar `config/telas/demo/h0045_validacao_nova_pagina.json`
  (já `navegavel: true`, sem `tipo`, múltiplos itens navegáveis) — fixture
  existente, não recriar.
- Caso EXPLICITO_NIVEL_UNICO: criar
  `config/telas/demo/h0052_nivel_unico_explicito.json`, mesma estrutura
  mínima de `config/telas/demo/h0030_console_unico.json` (envelope completo:
  `id`, `cabecalho`, `corpo.elementos[0]` tipo `console` com as cinco
  políticas, `barra_de_menus` com `chip_esc`/`chip_ajuda`), com `itens`
  populado por ao menos dois itens navegáveis e
  `"politica_navegacao": {"navegavel": true, "tipo": "nivel_unico"}`.
  `id` do JSON deve ser `"h0052_nivel_unico_explicito"` (coincide com o nome
  do arquivo, conforme exigido pelo loader/`demo_navegacao.py`).
- Caso TABELA: criar `config/telas/demo/h0052_tabela_passiva.json`, mesmo
  envelope mínimo, com
  `"politica_navegacao": {"navegavel": false, "tipo": "tabela"}` e `itens`
  vazio ou com itens não navegáveis. `id` = `"h0052_tabela_passiva"`.

Não criar fixture de árvore, seleção multinível ou dois níveis por foco.

---

## 10. Temporários e saídas

```yaml
entrada_real: nenhuma
fixtures:
  - config/telas/demo/h0045_validacao_nova_pagina.json   # reutilizada, não alterada
  - config/telas/demo/h0052_nivel_unico_explicito.json   # nova
  - config/telas/demo/h0052_tabela_passiva.json           # nova
temporarios:
  - construcao local de ElementoCorpo em tela/teste_navegacao.py (nao persistida)
  - JSON minimo em memoria ou arquivo temporario de teste em tela/teste_loader.py
    para exercitar a falha focal (nao e fixture permanente do projeto)
saida_persistente: nenhuma
saida_de_teste: relatorios padrao do pytest (stdout/collector); sem artefato
  gravado em disco pelo runtime da capacidade
sobrescrita: nenhuma (nenhum arquivo existente e sobrescrito; apenas os dois
  arquivos novos listados em fixtures sao criados)
limpeza: nenhuma pendente — nao ha estado de runtime persistido em JSON
  (politica de navegacao resolvida e recalculada a cada leitura, D-MULTI-13,
  contrato_console.md R-6)
```

---

## 11. Testes obrigatórios

Mínimo exigido, todos como testes automatizados:

1. `politica_navegacao` objeto sem `tipo` resolve para `nivel_unico`
   (`tipo_navegacao_efetivo`).
2. `politica_navegacao` não-objeto **não** recebe fallback: a função de
   resolução não a normaliza para `nivel_unico`; a entrada permanece
   estruturalmente inválida e é rejeitada pelo carregamento vigente — teste
   explícito dessa fronteira, distinto da regressão do item 5.
3. `tipo: "nivel_unico"` explícito preserva o comportamento vigente (mesma
   assertiva de focalizabilidade/movimento que os testes AT-0001–AT-0040 já
   cobrem para o caso legado).
4. Caso LEGADO e caso EXPLICITO_NIVEL_UNICO são semanticamente equivalentes
   — mesmo cenário de movimento executado com e sem `tipo`, resultado
   idêntico.
5. `politica_navegacao` continua objeto — validação de carga rejeita valor
   não-`dict` (regressão do comportamento já existente em
   `envelope_pre_adr_0028.py`).
6. `navegavel` continua consumido com sua semântica vigente (regressão dos
   testes existentes de `console_e_focalizavel`).
7. Cada um dos cinco valores fechados de `tipo` (`nivel_unico`, `tabela`,
   `arvore_colapsavel`, `selecao_multinivel`, `dois_niveis_por_foco`) é
   aceito quanto ao discriminador, tanto pela validação de carregamento
   quanto por `tipo_navegacao_efetivo` — sem exigir que H-0052 implemente
   comportamento das três políticas futuras.
8. Valor textual de `tipo` fora da enumeração fechada é rejeitado no
   carregamento via `TelaEstruturaInvalida`, sem coerção para `nivel_unico`.
9. Valor de `tipo` estruturalmente incompatível/não textual é rejeitado no
   carregamento, quando essa fronteira for aplicável diretamente ao
   validador vigente.
10. `tipo: "tabela"` (válido, `navegavel: false`) nunca entra em
    `lista_foco`/no ciclo de foco.
11. Console `tabela` nunca recebe cursor (`cursores` nunca populado para seu
    `id` em nenhum ponto do fluxo de foco).
12. Console `tabela` nunca faz `exibir_chip_navegar` retornar `True` quando é
    o único console da tela.
13. Chamada direta de cada um dos quatro `mover_*`
    (`mover_direita`/`mover_esquerda`/`mover_cima`/`mover_baixo`) sobre um
    console `tabela` não altera seu estado de cursor — teste que chama as
    funções públicas de movimento diretamente sobre o console `tabela`
    (fora do fluxo mediado por `console_e_focalizavel`/`lista_foco`),
    conforme requisito comportamental de §7.2.
14. `tabela` navegável (`navegavel: true` + `tipo: "tabela"`) não cai
    silenciosamente em `nivel_unico` — levanta `TelaEstruturaInvalida` no
    carregamento.
15. Valores dos handoffs futuros (`arvore_colapsavel`, `selecao_multinivel`,
    `dois_niveis_por_foco`) não são convertidos silenciosamente para
    `nivel_unico`: (a) `tipo_navegacao_efetivo` retorna o literal declarado;
    (b) `console_e_focalizavel` retorna `False` para os três; (c) nenhum
    comportamento próprio é exigido nesta etapa.
16. Paginação existente não sofre regressão: suíte completa de
    `tela/teste_paginacao.py` e `demo/teste_demo_paginacao.py` permanece
    verde, sem alteração de arquivo.
17. Testes preexistentes de `nivel_unico` (`tela/teste_navegacao.py`,
    AT-0001 a AT-0040) continuam passando sem alteração de asserção.

### Comando da suíte canônica

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

### Comando focal reproduzível de H-0052

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py tela/teste_loader.py tela/teste_paginacao.py -v
```

(`testpaths = tela demo` e `python_files = teste_*.py`, conforme
`pytest.ini` da raiz do projeto — caminhos e convenção de nome verificados
nesta leitura.)

---

## 12. Demonstração reproduzível

Usar o ponto de entrada real já existente, `demo/demo_navegacao.py`
(nenhum segundo framework de demonstração é criado):

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao \
  --tela config/telas/demo/h0045_validacao_nova_pagina.json

PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao \
  --tela config/telas/demo/h0052_nivel_unico_explicito.json

PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao \
  --tela config/telas/demo/h0052_tabela_passiva.json
```

Resultados esperados:

- Os dois primeiros comandos preservam integralmente o comportamento de
  nível único: console focalizado, cursor visível, quatro setas efetivas,
  `[✥]` presente quando há mais de um item navegável — comportamento
  visualmente indistinguível entre os dois.
- O terceiro comando exibe o console `tabela` sem foco, sem cursor e sem
  `[✥]` (dado não haver outro console focalizável na fixture mínima, o chip
  `[⇆]`/`[✥]` refletem ausência de console focalizável).

Esta constatação depende de sessão TTY real (SIGWINCH, cbreak mode,
alternate screen) e **é validação manual do usuário** — o agente de
implementação não pode declarar aprovação humana simulada. Os três comandos
acima são reproduzíveis e devem ser fornecidos prontos no relatório de
implementação para execução pelo usuário.

---

## 13. Exceção operacional focal

O agente de implementação não pode ampliar unilateralmente o escopo nominal
(§6). Se um arquivo fora da lista for estritamente necessário, deve parar
antes da alteração e retornar:

```yaml
status: ESCOPO_ADICIONAL_NECESSARIO
caminho:
motivo:
mudanca_esperada:
impacto_se_nao_autorizado:
```

Essa exceção não autoriza mudança automática.

---

## 14. Bloqueios

```yaml
bloqueio_documental: nenhum
decisao_de_usuario_pendente: nenhuma
arquivo_adicional_necessario: nenhum_identificado_nesta_leitura
impossibilidade_tecnica: nenhuma
```

Preferência de implementação (por exemplo, nome exato da função de
resolução em `tela/navegacao.py`) não constitui bloqueio — fica a critério
do implementador dentro dos limites de §7.

---

## 15. Critérios de aceite

H-0052 só pode ser concluído se, cumulativamente:

- [ ] Compatibilidade das telas existentes é preservada (nenhuma fixture ou
      tela pré-existente muda de comportamento).
- [ ] Fallback de `nivel_unico` ocorre somente quando `politica_navegacao` é
      objeto válido e `tipo` está ausente; entrada não-objeto não é
      mascarada como `nivel_unico` (§7.1, §11 item 2).
- [ ] `tipo: "nivel_unico"` produz comportamento equivalente ao caso legado.
- [ ] `tipo`, quando presente, é validado contra o conjunto fechado de cinco
      valores; valor desconhecido ou de forma incompatível é rejeitado via
      `TelaEstruturaInvalida`, sem coerção para `nivel_unico` (§7.3, §11
      itens 7–9).
- [ ] `tabela` é realmente passiva (sem foco, sem cursor, sem `[✥]`).
- [ ] Chamada direta de cada um dos quatro `mover_*` sobre `tabela` não
      altera o cursor, inclusive fora do fluxo mediado por foco (§7.2, §11
      item 13).
- [ ] `tabela` navegável incompatível produz falha focal via
      `TelaEstruturaInvalida`, sem novo mecanismo de erro.
- [ ] Nenhuma das três políticas futuras (`arvore_colapsavel`,
      `selecao_multinivel`, `dois_niveis_por_foco`) ganha comportamento
      antecipado.
- [ ] Nenhuma política futura cai silenciosamente em `nivel_unico` — nem na
      resolução do literal, nem na focalizabilidade.
- [ ] Paginação permanece intacta (§11 item 16).
- [ ] Nenhum novo schema ou arquitetura normativa é criado.
- [ ] Todos os 17 testes focais de §11 passam.
- [ ] Suíte canônica (`python -m pytest`) passa integralmente, salvo falha
      preexistente comprovada e isolada (registrada no relatório).
- [ ] Demonstração de §12 é executável nos três comandos.
- [ ] Escopo nominal de §6 foi respeitado ou a exceção de §13 foi usada
      corretamente.

---

## 16. Relatório de implementação esperado

Obrigatório em:

```text
docs/relatorios/IMP-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
```

Máximo normal: 900 palavras. Deve registrar somente:

- arquivos alterados;
- comportamento entregue;
- compatibilidade;
- testes focais;
- suíte integral;
- demonstração;
- desvios;
- exceções;
- bloqueios.

Não reproduzir a ADR nem este handoff.

---

## 17. Verificação interna do autor deste handoff

1. [x] Cobre somente H-0052.
2. [x] Lista nominal de implementação futura (§6).
3. [x] Preserva comportamento legado (§7.2, §11 itens 1, 3–6).
4. [x] Inclui `nivel_unico` (§7.2, §8, §11).
5. [x] Inclui `tabela` (§7.2, §7.3, §8, §11).
6. [x] Não implementa H-0053, H-0054 ou H-0055 (§3 item 5, §7.2).
7. [x] Não cria fallback indevido das políticas futuras (§7.1, §11 item 15).
8. [x] Não redefine `navegavel` (§4, §11 item 6).
9. [x] Não altera paginação (§6.1, §11 item 16).
10. [x] Não redefine foco, cursor ou seleção (§7.2 preserva mecanismos
    vigentes; nenhuma função de seleção é tocada).
11. [x] Possui testes focais reproduzíveis (§11).
12. [x] Possui demonstração reproduzível (§12).
13. [x] Distingue dados/fixtures/temporários/saídas (§10).
14. [x] Define relatório de implementação (§16).
15. [x] Não depende da branch defeituosa (nenhuma leitura ou remissão feita).
16. [x] Não exige leitura de relatórios históricos (leitura restrita às seis
    autoridades do manifesto e à descoberta focal de código).
17. [x] Não introduz arquitetura ou política nova (apenas uma função de
    resolução e uma validação de carga, ambas dentro dos mecanismos
    existentes).
18. [x] É exequível contra a implementação corrente (todos os pontos de
    intervenção foram lidos e citados por arquivo e linha em §5–§7).

---

## Resposta terminal

```yaml
status: CONCLUIDO
handoff: H-0052
arquivo: docs/handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
qa: H1_HANDOFF_APPROVED
implementacao: IMPLEMENTED
validacao_manual: MANUAL_VALIDATION_APPROVED
```
