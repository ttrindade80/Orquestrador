---
name: H-0013-demo-acesso-tela-grupo-minimo
description: Handoff de implementação — demo de acesso à tela grupo_minimo pelo fluxo demonstrável; entrada declarativa no lançador do Orquestrador + atualização de testes; sem alteração de código de módulos
metadata:
  type: handoff_implementacao
  status: HANDOFF_READY
  id: H-0013
  data_criacao: 2026-07-08
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_json_lancador.md
    - docs/contratos/contrato_json_tela_minima.md
  adrs_aplicadas:
    - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  handoffs_anteriores:
    - docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
  handoffs_cancelados:
    - docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
  handoffs_removidos:
    - H-0011A (nunca formalizado como documento — removido por granularidade excessiva)
---

# H-0013 — Demo de acesso à tela grupo mínimo

## Status

`HANDOFF_READY`

---

## Metadados de rastreabilidade

| Campo | Valor |
|---|---|
| ID | H-0013 |
| Data de criação | 2026-07-08 |
| HEAD base | `0bcb477` |
| Handoff anterior aprovado | H-0012 (QA_APPROVED_WITH_NOTES, 0 bloqueantes) |
| H-0011 | CANCELADO — não implementar (ver seção abaixo) |
| H-0011A | REMOVIDO — não recriar (ver seção abaixo) |
| ADR base | ADR-0010 |
| Sequência futura | H-0014 (segundo elemento no grupo) |

---

## Ordem de autoridade

Este handoff segue a hierarquia do `contrato_processo_desenvolvimento.md`:

1. Contrato de processo
2. ADRs aceitas
3. Contratos de módulo
4. **Este handoff**
5. Relatório de implementação

Qualquer contradição entre este handoff e um contrato ou ADR deve ser reportada
como `ARCHITECTURE_REVIEW_REQUIRED`. O handoff não pode sobrescrever contrato.

---

## Relação com H-0011 e H-0011A

**H-0011 — `CANCELADO_NAO_IMPLEMENTAR`**

O handoff H-0011 foi cancelado antes de qualquer implementação. Não deve ser
implementado, reaberto, corrigido nem usado como base. É mantido apenas para
rastreabilidade histórica.

**H-0011A — REMOVIDO por granularidade excessiva**

O handoff H-0011A foi planejado mas removido como handoff ativo antes de ser
escrito como documento completo. Não deve ser recriado. O H-0012 incorporou
o objetivo mínimo relevante.

**Regras de nomenclatura derivadas:**

- Não reabrir H-0011.
- Não recriar H-0011A.
- Não usar letras na sequência a partir de H-0012 (H-0013, H-0014, …).
- Não criar H-0013A, H-0013B nem micro-handoffs derivados.

---

## Contexto

O H-0012 foi implementado, aprovado em QA com ressalvas não bloqueantes
(`QA_APPROVED_WITH_NOTES`, 0 bloqueantes) e commitado em `0bcb477`. A
working tree estava limpa no commit base, exceto pelo próprio arquivo deste
handoff (não rastreado até o commit de documentação).

O H-0012 entregou:

- `config/telas/grupo_minimo.json` — tela isolada com grupo estrutural
  contendo exatamente 1 elemento funcional (`dashboard`).
- Suporte ao tipo `"grupo"` em `tela/loader.py` (valida invariantes do ciclo).
- Representação do grupo em `tela/modelo.py` (`ElementoCorpo.elementos`).
- Travessia do grupo em `tela/renderizador.py` (sem caixa visual própria).
- Testes cobrindo os casos positivo e negativo do grupo.

O H-0012 **não** alterou:

- `tela/demo.py` — demo permanece intacta.
- `config/telas/orquestrador.json` — lançador aponta apenas para `destino_minimo`.
- Contratos, ADRs, NOMENCLATURA.

**Estado observado que motiva o H-0013:**

`grupo_minimo` existe e funciona no código, mas não está acessível pelo fluxo
demonstrável (`python tela/demo.py`). O lançador do Orquestrador atualmente
declara apenas o item `d → destino_minimo`. Nenhum item aponta para
`grupo_minimo`. Para tornar o grupo acessível ao usuário sem alterar código
de módulos, basta declarar um novo item no lançador do `orquestrador.json`.

---

## Objetivo

Tornar `grupo_minimo` acessível pela aplicação demonstrável (`python tela/demo.py`)
de forma que o usuário possa:

1. Ver o item do grupo no lançador do Orquestrador.
2. Acionar o item (chip `g` ou equivalente) e navegar para `grupo_minimo`.
3. Ver a tela `grupo_minimo` renderizada (cabeçalho, dashboard interno, menus).
4. Usar Esc em `grupo_minimo` para voltar ao Orquestrador.
5. Alternar borda (`b`) em qualquer ponto do fluxo.

O H-0013 é uma ponte de uso/demonstração. Ele não adiciona segundo elemento
ao grupo, não implementa composição horizontal e não migra o Orquestrador para
estrutura hierárquica.

---

## Relação com H-0012

O H-0013 é continuação natural do H-0012. O H-0012 criou a capacidade de
código (tipo `"grupo"` estrutural, `grupo_minimo.json` carregável e
renderizável). O H-0013 expõe essa capacidade no fluxo demonstrável por meio
de uma declaração no JSON do Orquestrador.

O H-0013 não relaxa nenhum invariante do H-0012. `grupo_minimo` continua com
exatamente 1 elemento funcional interno. O loader continua rejeitando grupos
com 2+ elementos. A tela `grupo_minimo.json` não é alterada.

---

## Leitura obrigatória realizada

O preparador deste handoff leu e analisou:

```
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_json_tela_minima.md
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
docs/relatorios/RELATORIO_QA_H-0012_GRUPO_ESTRUTURAL_MINIMO_TELA_ISOLADA.md

config/telas/orquestrador.json
config/telas/destino_minimo.json
config/telas/grupo_minimo.json

tela/demo.py
tela/renderizador.py
tela/loader.py
tela/modelo.py
tela/teste_demo.py
tela/teste_diagnostico.py
tela/teste_renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
```

Nota: `tela/teste_loader.py` e `tela/teste_modelo.py` foram verificados como
referência para entender cobertura existente, mas provavelmente não precisam
de alteração neste ciclo (ver calibração abaixo).

---

## Calibração técnica

### Como `demo.py` localiza itens do lançador

A função `processar_comando` em `tela/demo.py` itera `modelo.corpo.elementos`,
filtra elementos de `tipo == "lancador"`, e para cada item em
`_campos_inertes["itens"]` verifica se `item.get("chip") == comando`. Ao
encontrar coincidência, empilha a tela atual e troca para `item.get("tela_destino")`.

**Conclusão:** o binding já percorre `lancador.itens[]` declarados no JSON. O
código não hardcoda nenhum chip nem destino. Adicionar um item ao JSON do
Orquestrador é suficiente para que `processar_comando` reconheça o novo chip e
navegue para `grupo_minimo`. **Nenhuma alteração de código em `demo.py` é
necessária.**

### Se adicionar item ao `orquestrador.json` é suficiente para acionar a nova tela

Sim. O fluxo completo já existe:

```
demo.py main()
  → _carregar_modelo_por_id("orquestrador")  [carregar_tela + construir_modelo]
  → processar_comando(estado, "g", modelo)   [reconhece chip "g" no lancador]
  → estado["tela_atual"] = "grupo_minimo"
  → _carregar_modelo_por_id("grupo_minimo")  [já suportado pelo H-0012]
  → renderizar_tela(modelo_grupo, ...)       [já suportado pelo H-0012]
  → Esc → pop pilha → volta ao Orquestrador
```

Nenhum código de módulo precisa mudar.

### Se `grupo_minimo.json` já é carregável

Confirmado pelo H-0012 e pelo QA: `carregar_tela(None, "grupo_minimo")` carrega
sem erro. O modelo e o renderer já suportam grupos. A saída do renderizador
inclui a caixa do `dashboard` interno sem caixa visual própria do grupo.

### Por que o H-0013 é um handoff completo e não apenas uma declaração pontual

O `contrato_processo_desenvolvimento.md` seção 9 diz que mudança puramente
declarativa em JSON não exige handoff próprio quando **todas** as condições
abaixo forem satisfeitas simultaneamente:

- o schema já suporta a declaração → ✓
- o loader/modelo já preserva e valida os campos declarados → ✓
- o renderer/binding já interpreta a declaração → ✓
- não há novo comportamento de código → ✓
- não há novo tipo estrutural → ✓
- **não há nova ação, navegação, binding ou regra de renderização → ✗**

A condição marcada com ✗ falha porque estamos **criando uma nova rota de
navegação** (`orquestrador → grupo_minimo`) que não existia. Embora o suporte
técnico de código exista, a rota em si é nova e precisa ser verificada e
documentada em ciclo completo.

Além disso, vários harnesses de teste possuem comparação estrita de strings
com a saída do Orquestrador. Adicionar um item ao lançador **quebra** esses
testes se não forem atualizados. Os testes afetados são:

| Arquivo | Constante afetada | Conteúdo que muda |
|---|---|---|
| `tela/teste_diagnostico.py` | `_EXPECTED_ORQUESTRADOR` | lancador com `[d] Destino` → precisa incluir `[g] Grupo Min.` |
| `tela/teste_demo.py` | `_EXPECTED_CURVA`, `_EXPECTED_RETA` | idem, largura 80 |
| `tela/teste_demo.py` | `_EXPECTED_DIAGNOSTICO_CURVA_42` | idem, largura 42 |
| `tela/teste_renderizador.py` | `_EXPECTED_*` para orquestrador | verificar e atualizar se necessário |

A escala de atualização de testes (comparação estrita, novos casos de
navegação para `grupo_minimo`) justifica um ciclo formal completo com
relatório de implementação.

### Quais testes precisam ser alterados

**Obrigatório:**

1. `tela/teste_diagnostico.py` — atualizar `_EXPECTED_ORQUESTRADOR` (42 chars)
   para incluir a nova linha de lançador.

2. `tela/teste_demo.py` — atualizar:
   - `_EXPECTED_CURVA` (80 chars)
   - `_EXPECTED_RETA` (80 chars)
   - `_EXPECTED_DIAGNOSTICO_CURVA_42` (42 chars)
   - Adicionar `_EXPECTED_GRUPO_MINIMO_CURVA_80` e `_EXPECTED_GRUPO_MINIMO_RETA_80`
     como constantes para os testes de navegação.
   - Adicionar testes de navegação para `grupo_minimo` em `teste_navegacao_minima`
     e em `teste_navegacao_subprocess`.

**Condicional (verificar antes de alterar):**

3. `tela/teste_renderizador.py` — verificar se contém constantes `_EXPECTED_*`
   para a saída do Orquestrador que incluam o lançador `[d] Destino`. Se
   existirem, atualizar para incluir o novo item. Se não existirem, não alterar.

**Provavelmente não precisa alterar:**

4. `tela/teste_loader.py` — não tem comparação estrita com saída do Orquestrador;
   o loader já suporta `tela_destino: "grupo_minimo"` como valor declarativo
   inerte. Verificar para confirmar; não alterar se não houver caso que quebre.

5. `tela/teste_modelo.py` — mesmo raciocínio do loader. Verificar; provavelmente
   não precisa alterar.

---

## Escopo positivo

O H-0013 deve implementar **apenas** o seguinte:

1. **Alterar `config/telas/orquestrador.json`**:
   - Adicionar item ao array `lancador_principal.itens[]` com os campos
     obrigatórios `id`, `chip`, `texto` (máx. 15 caracteres) e `tela_destino`.
   - Valor recomendado para `chip`: `"g"` (livre — não existe nos chips do
     lançador atual nem nos controles internos `b`/`s`/`\x1b` da demo).
   - Valor recomendado para `texto`: `"Grupo Min."` (10 chars, dentro do limite).
   - `tela_destino`: `"grupo_minimo"` (arquivo já existente em
     `config/telas/grupo_minimo.json`).
   - O executor pode escolher chip/texto diferentes desde que:
     - `chip` seja único no lançador e não conflite com `b`, `s` ou `\x1b`.
     - `texto` ≤ 15 caracteres.
     - `tela_destino` seja exatamente `"grupo_minimo"`.
   - O item existente `d → destino_minimo` não deve ser alterado nem removido.

2. **Alterar `tela/teste_diagnostico.py`**:
   - Atualizar `_EXPECTED_ORQUESTRADOR` (42 chars) inserindo a linha do novo
     item de lançador na posição correta (após a linha de `[d] Destino`).
   - Manter todos os demais testes e verificações sem alteração.

3. **Alterar `tela/teste_demo.py`**:
   - Atualizar `_EXPECTED_CURVA` (80 chars) com a nova linha do lançador.
   - Atualizar `_EXPECTED_RETA` (80 chars) idem.
   - Atualizar `_EXPECTED_DIAGNOSTICO_CURVA_42` (42 chars) idem.
   - Adicionar `_EXPECTED_GRUPO_MINIMO_CURVA_80` e `_EXPECTED_GRUPO_MINIMO_RETA_80`
     como constantes para os testes de navegação (gerar via `renderizar_tela` ou
     definir inline, a critério do executor, desde que seja determinístico e
     verificável).
   - Em `teste_navegacao_minima`: adicionar casos cobrindo:
     - chip do grupo (ex.: `"g"`) muda `tela_atual` para `"grupo_minimo"`.
     - chip do grupo empilha `"orquestrador"` em `pilha_telas`.
     - Esc em `grupo_minimo` volta para `"orquestrador"`.
     - Esc em `grupo_minimo` não define `saindo == True`.
   - Em `teste_navegacao_subprocess`: adicionar caso cobrindo:
     - `"g\n\x1b\n\x1b\n"` → renders: orquestrador-curva, grupo_minimo-curva, orquestrador-curva.
     - Verificar que `"GRUPO MINIMO"` aparece no stdout.
     - Verificar que o stderr está vazio.
   - Manter todos os casos existentes passando, incluindo os de `destino_minimo`.

4. **Alterar `tela/teste_renderizador.py`** (condicional):
   - Verificar se existe constante `_EXPECTED_*` para a saída do Orquestrador
     que inclua `[d] Destino`. Se existir, atualizar para incluir o novo item.
   - Se não existir tal constante, **não alterar** o arquivo.

5. **Criar `docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md`**:
   - Relatório de implementação conforme padrão do projeto.
   - Conteúdo mínimo: seção de escopo implementado, arquivos criados/alterados,
     decisões locais, preservações, testes executados (saída completa), cobertura
     dos critérios de aceite, resultado final.

---

## Escopo negativo

O executor **não deve** implementar nada além do escopo positivo acima.
A lista abaixo é exaustiva e obrigatória.

```
NÃO alterar tela/demo.py.
NÃO alterar tela/loader.py.
NÃO alterar tela/modelo.py.
NÃO alterar tela/renderizador.py.
NÃO alterar tela/diagnostico.py.
NÃO alterar config/telas/grupo_minimo.json.
NÃO alterar config/telas/destino_minimo.json.
NÃO adicionar segundo elemento ao grupo em grupo_minimo.json.
NÃO implementar lado_a_lado.
NÃO implementar grupo aninhado.
NÃO implementar distribuição por percentual ou fração.
NÃO migrar o Orquestrador inteiro para estrutura hierárquica.
NÃO alterar a semântica de "grupo".
NÃO criar novo tipo funcional.
NÃO criar registry novo.
NÃO alterar contratos em docs/contratos/.
NÃO alterar ADRs em docs/adr/.
NÃO alterar docs/NOMENCLATURA.md.
NÃO alterar docs/INDICE.md.
NÃO alterar docs/backlog.md.
NÃO alterar docs/issues.md.
NÃO alterar docs/handoff/ (exceto o handoff H-0013 já criado e o relatório IMP-0013).
NÃO reabrir H-0011.
NÃO recriar H-0011A.
NÃO usar letras na nomenclatura (H-0014, H-0015, …).
NÃO criar micro-handoff separado para qualquer parte deste ciclo.
NÃO implementar console real.
NÃO implementar foco.
NÃO implementar seleção.
NÃO implementar navegação por [✥] no grupo ou em seus elementos.
NÃO implementar nova ação registrada.
NÃO criar novo tipo de chip, novo mecanismo de chip, nova semântica de chip,
novo registry de chip nem novo binding de chip.
O chip `g` do item declarativo previsto em F-1 é um valor de campo JSON em
`lancador.itens[]` já suportado pelo código existente — não é um novo tipo de
chip nem um novo mecanismo. Adicionar esse item ao JSON do Orquestrador é o
escopo central deste handoff e está explicitamente autorizado.
NÃO transformar "grupo" em caixa visual própria.
NÃO fazer commit.
```

### Por que `demo.py` está proibido

A função `processar_comando` em `demo.py` já itera `lancador.itens[]` do
modelo e reconhece qualquer chip declarado no JSON. Não há nenhuma razão
técnica para alterar `demo.py` neste ciclo. Se a implementação exigir alterar
`demo.py`, isso indica lacuna de análise — o executor deve parar com
`ARCHITECTURE_REVIEW_REQUIRED` antes de qualquer modificação.

### Por que loader/modelo/renderizador estão proibidos

O H-0012 já implementou o suporte completo. Nenhuma nova capacidade de código
é necessária para navegar até `grupo_minimo`. Se a implementação exigir alterar
qualquer desses módulos, isso indica problema arquitetural não antecipado —
parar com `ARCHITECTURE_REVIEW_REQUIRED`.

---

## Especificação funcional

### F-1. Declaração do item no lançador do Orquestrador

Em `config/telas/orquestrador.json`, no elemento `lancador_principal`, campo
`itens[]`, adicionar após o item existente:

```json
{
  "id": "item_grupo_minimo",
  "chip": "g",
  "texto": "Grupo Min.",
  "tela_destino": "grupo_minimo"
}
```

Regras obrigatórias:

- `id` deve ser único no escopo do lançador.
- `chip` deve ser único no lançador e não conflitar com controles internos
  da demo (`b`, `s`) nem com Esc (`\x1b`).
- `texto` máximo 15 caracteres — rejeitado pelo renderer se exceder
  (`RenderizadorErro`).
- `tela_destino` deve ser `"grupo_minimo"` — arquivo existe em
  `config/telas/grupo_minimo.json`.
- O item existente `"item_destino_minimo"` (chip `d`, destino `destino_minimo`)
  permanece inalterado.

Após esta declaração, o Orquestrador renderizará:

```
╭ NAVEGAR ─────────────────────────────────────────────────────────────────────╮
│ [d] Destino                                                                  │
│ [g] Grupo Min.                                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

(Exemplo com largura 80. A largura exata depende da configuração de terminal.)

### F-2. Fluxo de navegação esperado

```
Usuário digita "g" no Orquestrador
→ processar_comando reconhece chip "g" no lancador_principal
→ pilha_telas = ["orquestrador"]
→ tela_atual = "grupo_minimo"
→ _carregar_modelo_por_id("grupo_minimo")
→ renderizar_tela(modelo_grupo_minimo, tipo_borda, largura)
→ Tela grupo_minimo exibida com dashboard interno e [Esc] Voltar

Usuário digita Esc em grupo_minimo
→ processar_comando reconhece Esc com pilha não vazia
→ tela_atual = "orquestrador" (pop da pilha)
→ pilha_telas = []
→ renderizar_tela(modelo_orq, tipo_borda, largura)
→ Orquestrador exibido
```

Este fluxo já funciona pelo código existente de `demo.py`. Nenhuma linha de
código de módulo precisa mudar.

### F-3. Atualização das constantes de expected output

As constantes de expected output que dependem da saída do lançador do
Orquestrador **devem** ser atualizadas para incluir a nova linha:

- **Para largura 80**: nova linha após `│ [d] Destino` →
  `│ [g] Grupo Min.                                                               │`
- **Para largura 42**: nova linha após `│ [d] Destino` →
  `│ [g] Grupo Min.                         │`

O executor **não deve** tentar calcular o padding manualmente — deve derivar
a string correta executando `renderizar_tela` sobre o modelo carregado, ou
usar o padrão `content_w = largura - 3` (ex.: largura 80 → content_w 77).

### F-4. Novos testes de navegação

Os novos testes devem cobrir o caminho demonstrável completo para `grupo_minimo`:

```
teste_navegacao_minima (processamento unitário):
- chip "g" muda tela_atual para "grupo_minimo"
- chip "g" empilha "orquestrador" em pilha_telas
- chip "g" nao altera tipo_borda nem saindo
- Esc em grupo_minimo (pilha = ["orquestrador"]) volta para "orquestrador"
- Esc em grupo_minimo NAO define saindo == True
- ciclo completo: orquestrador → grupo_minimo → orquestrador via Esc

teste_navegacao_subprocess (integração via subprocess):
- demo com "g\n\x1b\n\x1b\n" encerra com código 0
- stdout contém "GRUPO MINIMO" (título da tela grupo_minimo)
- stdout contém "[Esc] Voltar" (chip da barra de grupo_minimo)
- stdout gera 3 renders: orquestrador-curva, grupo_minimo-curva, orquestrador-curva
- stderr está vazio
```

---

## Arquivos permitidos

Lista explícita e exaustiva. O executor **só pode** criar ou alterar arquivos
desta lista.

### Alterar obrigatório

```
config/telas/orquestrador.json
tela/teste_demo.py
tela/teste_diagnostico.py
```

### Alterar condicional (verificar antes de alterar)

```
tela/teste_renderizador.py
  Somente se existirem constantes _EXPECTED_* para o Orquestrador que incluam
  a linha do lançador "│ [d] Destino". Se não existirem tais constantes ou se
  os testes não quebrarem com a adição do item, NÃO alterar.

tela/teste_loader.py
  Somente se existirem casos de teste que dependam de uma contagem específica
  de itens no lançador do Orquestrador. Verificar; muito provavelmente NÃO
  precisará ser alterado.

tela/teste_modelo.py
  Mesmo raciocínio. Verificar; muito provavelmente NÃO precisará ser alterado.
```

### Criar

```
docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md
```

---

## Arquivos proibidos

O executor **não pode** criar nem alterar:

```
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/estilo.json
config/lancador.json
config/barra_de_menus.json
config/cabecalho.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json
tela/demo.py
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/diagnostico.py
tela/__init__.py
docs/contratos/
docs/adr/
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/handoff/
  (exceto o handoff H-0013 já criado antes da implementação
   e o relatório IMP-0013 que o executor deve criar)
qualquer arquivo não listado como permitido acima
```

---

## Critérios de aceite

O executor deve verificar **todos** os itens abaixo antes de considerar
a implementação concluída. Nenhum item pode ser ignorado.

### Sobre a declaração no Orquestrador

```
CA-01. config/telas/orquestrador.json é JSON sintaticamente válido após a alteração.
CA-02. lancador_principal.itens[] contém o novo item com id, chip, texto e tela_destino.
CA-03. tela_destino do novo item é "grupo_minimo".
CA-04. texto do novo item tem no máximo 15 caracteres.
CA-05. chip do novo item não duplica nenhum chip existente no lançador.
CA-06. O item existente id="item_destino_minimo" (chip="d", tela_destino="destino_minimo")
       está preservado e inalterado.
```

### Sobre o fluxo demonstrável

```
CA-07. python tela/demo.py (TTY real ou subprocess) permite acionar grupo_minimo
       pelo chip declarado no lançador.
CA-08. Após acionar o chip, a tela grupo_minimo é exibida com:
       - cabeçalho "GRUPO MINIMO"
       - dashboard interno com o campo literal
       - barra de menus com [Esc] Voltar e [?] Ajuda
CA-09. Esc em grupo_minimo volta ao Orquestrador sem definir saindo=True.
CA-10. O item destino_minimo (chip "d") continua funcionando após a alteração.
CA-11. Esc no Orquestrador (com pilha vazia) continua saindo.
CA-12. Esc em destino_minimo (com pilha = ["orquestrador"]) continua voltando.
CA-13. "b" alterna borda no Orquestrador, em destino_minimo e em grupo_minimo.
CA-14. grupo_minimo continua com exatamente 1 elemento funcional interno.
CA-15. Nenhum segundo elemento foi adicionado ao grupo.
CA-16. Nenhuma composição horizontal foi implementada.
```

### Sobre os testes

```
CA-17. python tela/teste_loader.py     → exit 0, sem [FALHOU], sem traceback.
CA-18. python tela/teste_modelo.py     → exit 0, sem [FALHOU], sem traceback.
CA-19. python tela/teste_renderizador.py → exit 0, sem [FALHOU], sem traceback.
CA-20. python tela/teste_demo.py       → exit 0, sem [FALHOU], sem traceback.
CA-21. python tela/teste_diagnostico.py  → exit 0, sem [FALHOU], sem traceback.
CA-22. python tela/diagnostico.py      → exit 0 (integridade do Orquestrador).
```

### Sobre escopo e rastreabilidade

```
CA-23. tela/demo.py não foi alterado (nenhum diff).
CA-24. tela/loader.py não foi alterado (nenhum diff).
CA-25. tela/modelo.py não foi alterado (nenhum diff).
CA-26. tela/renderizador.py não foi alterado (nenhum diff).
CA-27. tela/diagnostico.py não foi alterado (nenhum diff).
CA-28. config/telas/grupo_minimo.json não foi alterado (nenhum diff).
CA-29. config/telas/destino_minimo.json não foi alterado (nenhum diff).
CA-30. Nenhum contrato em docs/contratos/ foi alterado.
CA-31. Nenhuma ADR em docs/adr/ foi alterada.
CA-32. docs/NOMENCLATURA.md não foi alterado.
CA-33. Nenhum arquivo fora da lista de permitidos foi criado ou alterado.
CA-34. docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md foi criado.
CA-35. Nenhum commit foi realizado pelo executor.
CA-36. Nenhum __pycache__ ou .pyc permanece após os testes.
```

---

## Comandos obrigatórios de verificação

O executor deve executar **todos** os comandos abaixo e confirmar saída limpa.

### Validade do JSON alterado

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

### JSONs de produção inalterados (verificação de integridade)

```bash
python -m json.tool config/telas/grupo_minimo.json >/dev/null && echo "grupo_minimo.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
```

### Testes automatizados

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
```

Todos devem encerrar com código de saída 0, não imprimir linhas `[FALHOU]` e
não produzir traceback.

### Diagnóstico (integridade do Orquestrador)

```bash
python tela/diagnostico.py
```

Deve encerrar com exit 0. A saída deve refletir o novo item do lançador
(incluir a linha do grupo) e estar em acordo com `_EXPECTED_ORQUESTRADOR`
atualizado em `teste_diagnostico.py`.

### Verificação do novo chip via loader

```bash
python -c "
import sys; sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path('tela/loader.py').resolve().parent.parent))
from tela.loader import carregar_tela
raw = carregar_tela(None, 'orquestrador')
itens = raw['corpo']['elementos'][2]['itens']
chips = [i['chip'] for i in itens]
destinos = [i['tela_destino'] for i in itens]
print('chips:', chips)
print('destinos:', destinos)
print('OK' if 'grupo_minimo' in destinos else 'FALHOU — grupo_minimo nao encontrado')
"
```

Nota: ajustar o índice `[2]` se o lançador não for o terceiro elemento de
`corpo.elementos[]`; verificar a estrutura real do JSON.

### Verificação de navegação via subprocess (demo)

```bash
python -c "
import subprocess, sys, os
env = {k: v for k, v in os.environ.items() if k != 'COLUMNS'}
p = subprocess.run(
    [sys.executable, 'tela/demo.py'],
    cwd='.',
    input='g\n\x1b\n\x1b\n',
    capture_output=True, text=True, env=env
)
print('exit:', p.returncode)
print('GRUPO MINIMO no stdout:', 'GRUPO MINIMO' in p.stdout)
print('Esc Voltar no stdout:', '[Esc] Voltar' in p.stdout)
print('stderr vazio:', p.stderr == '')
"
```

### Cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --name-only
```

### Verificação manual interativa (TTY real)

```bash
python tela/demo.py
```

Sequência manual:
1. Orquestrador é exibido; lançador mostra `[d] Destino` e o novo item.
2. Digitar o chip do grupo (ex.: `g`) → `grupo_minimo` é exibida.
3. Verificar cabeçalho "GRUPO MINIMO", dashboard interno, barra com `[Esc] Voltar`.
4. Digitar `b` → borda alterna.
5. Digitar `Esc` → volta ao Orquestrador.
6. Digitar `d` → `destino_minimo` ainda funciona.
7. Digitar `Esc` → volta ao Orquestrador.
8. Digitar `Esc` → sai.

**Nota:** este teste manual requer TTY real e não pode ser automatizado por
subprocess. Os critérios automatizáveis estão nos testes de unidade e de
integração via subprocess. Não falhar um CA por impossibilidade de automação
de TTY; diferenciar no relatório o que foi testado automaticamente do que
foi testado manualmente.

---

## Relatório de implementação obrigatório

O executor deve criar:

```
docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md
```

O relatório deve conter no mínimo:

1. Lista exaustiva de arquivos criados e alterados.
2. Decisões de implementação tomadas (incluindo chip escolhido, texto, id).
3. Quais constantes `_EXPECTED_*` foram atualizadas e como (mostrar o diff
   das constantes).
4. Saída completa de cada comando de verificação executado.
5. Status final: PASSOU / FALHOU (com detalhe de cada falha).
6. Confirmação de que `demo.py`, `loader.py`, `modelo.py`, `renderizador.py`
   e `diagnostico.py` não foram alterados.
7. Confirmação de que nenhum commit foi realizado.
8. Resultado do teste manual via TTY real (se realizado) ou justificativa da
   impossibilidade.

---

## Instrução de bloqueio ao executor (GLM/OpenCode)

Leia este handoff integralmente antes de escrever qualquer código ou alterar
qualquer arquivo.

**Regras de execução obrigatórias:**

1. Não decidir arquitetura nova. Toda decisão arquitetural que não esteja
   coberta por este handoff ou pelos contratos citados deve ser reportada
   como `ARCHITECTURE_REVIEW_REQUIRED`.

2. Não alterar contrato, ADR, NOMENCLATURA nem INDICE.

3. Não resolver lacuna por inferência. Se faltar regra, arquivo permitido
   ou critério verificável, parar com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`
   e descrever o que falta.

4. Não fazer commit.

5. Não implementar nada fora do escopo positivo listado.

6. Criar o relatório de implementação `IMP-0013-demo-acesso-tela-grupo-minimo.md`
   antes de encerrar.

7. Não alterar `demo.py`. Se a análise indicar que `demo.py` precisa ser
   alterado para que o ciclo funcione, parar com `ARCHITECTURE_REVIEW_REQUIRED`
   e descrever o motivo antes de qualquer alteração. Isso indica lacuna de
   análise, pois o binding já existe.

8. Não alterar `loader.py`, `modelo.py` nem `renderizador.py`. Se a análise
   indicar necessidade, parar com `ARCHITECTURE_REVIEW_REQUIRED`.

### Parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

```
- A implementação exigir alterar demo.py, loader.py, modelo.py ou renderizador.py.
- A implementação exigir criar registry, nova classe de elemento ou novo
  mecanismo de binding não coberto por este handoff.
- A saída visual do Orquestrador mudar de forma inesperada (além do novo item
  do lançador).
- Houver contradição entre este handoff e um contrato ou ADR vigente.
- Houver lacuna de especificação que impeça decidir sem assumir arquitetura.
- O chip escolhido conflitar com controles internos da demo ou com chips da
  barra_de_menus de forma que quebre o fluxo.
```

### Parar com `BLOCKED` se:

```
- config/telas/orquestrador.json não puder ser alterado.
- config/telas/grupo_minimo.json não existir em disco.
- tela/teste_demo.py ou tela/teste_diagnostico.py estiverem ausentes.
- Algum critério de aceite não puder ser verificado pelos meios disponíveis.
- Algum arquivo obrigatório não estiver na lista de permitidos.
```

---

## Próximo ciclo previsto

**H-0014** — Adicionar segundo elemento funcional ao grupo.

O H-0014 relaxará a restrição do H-0012 de "exatamente 1 elemento funcional
dentro do grupo". Ele é fora do escopo do H-0013 e **não deve** ser antecipado
nem planejado neste ciclo.

O H-0013 não decide arquitetura de grupos com 2+ elementos. Essa decisão
pertence ao H-0014 e ao seu respectivo handoff.
