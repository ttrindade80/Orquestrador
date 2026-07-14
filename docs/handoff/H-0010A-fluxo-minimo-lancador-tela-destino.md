---
name: H-0010A-fluxo-minimo-lancador-tela-destino
description: Handoff de implementação — fluxo mínimo de lançador com tela destino; declarativo por JSON; sem hardcoding de itens no renderer
metadata:
  type: handoff_implementacao
  status: HANDOFF_READY
  id: H-0010A
  data_criacao: 2026-07-08
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_barra_de_menus.md
  adrs_aplicadas:
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  handoffs_anteriores:
    - docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md
  handoffs_substituidos:
    - docs/handoff/H-0010-lancador-visual-inerte.md
---

# H-0010A — Fluxo mínimo de lançador com tela destino

## Status

`HANDOFF_READY`

---

## Contexto

O H-0009 foi implementado, aprovado e commitado (`57f36d2`). O pacote
`tela/` contém: loader (H-0001), modelo (H-0002), renderizador
(H-0006/H-0007/H-0009), demo (H-0008/H-0009), diagnostico (H-0004) e os
cinco arquivos de teste correspondentes.

O H-0010 original foi bloqueado com `ARCHITECTURE_REVIEW_REQUIRED` pela
auditoria `RELATORIO_AUDITORIA_H-0010_HANDOFF.md`. O motivo: autorizava
itens hardcoded no renderer e tratava `tela_destino` como campo inativo,
em conflito com os contratos ativos (`contrato_lancador.md`,
`contrato_barra_de_menus.md`, `contrato_tela_json.md`) e com o princípio
arquitetural declarativo por tela.

---

## Problema que este ciclo corrige

Após o H-0009, o renderer (`tela/renderizador.py`) produz três caixas
com conteúdo **totalmente hardcoded**:

1. Caixa de cabeçalho — derivada do modelo (correto).
2. Caixa de dashboard — placeholder hardcoded com texto fixo
   `"Dashboard de teste"` e `"Sem dados carregados"`, sem leitura do JSON.
3. Caixa de menu — placeholder hardcoded com texto fixo
   `"[Esc] Sair    [B] Borda"`, sem leitura de `barra_de_menus.chips[]`
   nem de `corpo.elementos[]` do tipo `lancador`.

O renderer não lê `_campos_inertes` dos elementos. Não percorre
`barra_de_menus.chips[]`. Não percorre `lancador.itens[]`. Isso contraria
o contrato declarativo: qualquer mudança de conteúdo ou comportamento
deveria ser declaração no JSON, não alteração de código.

O orquestrador.json tem `lancador_principal.itens: []` — lista vazia.
Não existe ainda a tela `config/telas/destino_minimo.json`.

---

## Objetivo

Implementar, em um único ciclo coeso, o fluxo mínimo de lançador com
tela destino:

1. Criar `config/telas/destino_minimo.json`.
2. Declarar nela: dashboard simples com texto de teste, Esc Voltar.
3. Atualizar `orquestrador.json` com item real em
   `lancador_principal.itens[]` apontando para `destino_minimo`.
4. Alterar o renderer para ler `lancador.itens[]` do modelo/JSON — sem
   hardcodar itens.
5. Alterar o renderer para ler `barra_de_menus.chips[]` do JSON — sem
   hardcodar `[Esc] Sair` nem `[B] Borda`.
6. Alterar o renderer para ler campos do `dashboard` com
   `fonte: "literal"` — sem placeholder hardcoded para destino_minimo.
7. Alterar a demo para suportar `tela_atual` e `pilha_telas` —
   navegação mínima local.
8. Atualizar todos os testes existentes para refletir o novo output.
9. Ampliar os testes com as verificações do fluxo de navegação.

O objetivo arquitetural é provar que a separação declarativa funciona:
a tela é definida pelo JSON; o renderer interpreta o JSON; o renderer
não inventa composição nem hardcoda conteúdo.

---

## Leitura obrigatória realizada

O executor que preparou este handoff leu e analisou:

```
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_barra_de_menus.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md

config/telas/orquestrador.json

tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/diagnostico.py

tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

---

## Consulta adicional justificada

Nenhuma. Os arquivos obrigatórios foram suficientes para produzir este
handoff.

---

## Escopo positivo

O H-0010A especifica a implementação de:

```
1. Criar config/telas/destino_minimo.json.
2. Criar tela destino completa mínima (schema, id, cabecalho, corpo,
   barra_de_menus).
3. Declarar dashboard simples com texto de teste.
4. Declarar Esc Voltar na tela destino.
5. Atualizar orquestrador.json com item real em
   corpo.elementos[].id=lancador_principal itens[].
6. Apontar tela_destino para destino_minimo.
7. Renderizar o lançador lendo itens[] do JSON/modelo — sem hardcoding.
8. Renderizar a barra_de_menus lendo chips[] do JSON/modelo — sem
   hardcoding.
9. Renderizar o dashboard de destino_minimo lendo campos com
   fonte: "literal" do JSON/modelo.
10. Acionar chip do lançador para abrir destino_minimo.
11. Usar Esc em destino_minimo para voltar ao Orquestrador.
12. Manter Esc no Orquestrador como Sair.
13. Preservar alternância de borda nas duas telas.
14. Preservar testes anteriores (atualizando _EXPECTED_* que mudarão).
```

---

## Escopo negativo

O H-0010A **não deve** implementar:

```
registry completo de telas
registry completo de ações
console real (console continua placeholder ou omitido)
dashboard real com dados de fontes externas
filtros
paginação
seleção
toggle
modo verboso
navegação por [✥]
processamento
índice central de telas
descoberta automática ampla de telas
validação funcional de tela_destino no loader
validação de itens[] no loader
avaliação de regra_existencia ou regra_ativo de chips
hardcoding de item, texto, chip ou destino do lançador no renderer
decisão de Sair/Voltar por id de tela hardcoded no renderer ou na demo
alteração de contratos
alteração de ADRs
alteração de NOMENCLATURA
micro-handoff separado para campo que pertence à mesma capacidade
reativação do H-0010 original
```

O H-0010A é uma capacidade coesa: fluxo mínimo de lançador com tela
destino. Não é decomponível em micro-handoffs por campo, por item, por
chip, por Esc ou por render separado.

---

## Arquivos permitidos

A seguir, a lista explícita e exaustiva de arquivos que o GLM/OpenCode
poderá criar ou alterar neste ciclo.

### Criar

```
config/telas/destino_minimo.json
docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md
```

### Alterar

```
config/telas/orquestrador.json

tela/renderizador.py
tela/demo.py

tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

### Justificativa para arquivos não alterados

**`tela/loader.py`** — NÃO ALTERAR.

O loader já suporta carregar qualquer tela por `id`:
`carregar_tela(None, "destino_minimo")` funcionará automaticamente quando
o arquivo `config/telas/destino_minimo.json` existir. O loader já valida
`schema`, `id`, `cabecalho`, `corpo`, `barra_de_menus` e `corpo.elementos[]`.
Validação funcional de `itens[]` do lançador (tela_destino existente,
texto ≤ 15 chars) está fora do escopo do loader neste ciclo — a validação
de texto ≤ 15 chars é responsabilidade do renderer ao percorrer `itens[]`.

**`tela/modelo.py`** — NÃO ALTERAR.

O modelo já preserva `itens[]` em `_campos_inertes` do `ElementoCorpo`
do tipo `lancador`. O renderer acessará `_campos_inertes["itens"]`
diretamente. Não é necessário criar método adicional no modelo para
este ciclo.

**`tela/diagnostico.py`** — NÃO ALTERAR.

O `diagnostico.py` apenas encadeia `carregar_tela` → `construir_modelo`
→ `renderizar_tela` para `id_tela = "orquestrador"`. O comportamento
externo continuará correto após as alterações no renderer. Apenas o
output esperado em `teste_diagnostico.py` mudará.

**`tela/__init__.py`** — NÃO ALTERAR (proibido).

---

## Arquivos proibidos

O executor **não pode** criar nem alterar:

```
docs/contratos/
docs/adr/
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/handoff/
config/estilo.json
config/lancador.json
config/barra_de_menus.json
config/cabecalho.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json
tela/__init__.py
```

A exceção é o próprio handoff em `docs/handoff/`, que foi criado pelo
processo de engenharia antes da implementação e não deve ser alterado
pelo executor.

---

## Especificação funcional

### F-1. Tela destino mínima

Criar `config/telas/destino_minimo.json` conforme a seção
"Especificação de JSONs de tela".

### F-2. Item real no lançador do Orquestrador

Adicionar exatamente um item em `orquestrador.json` na lista
`corpo.elementos[id=lancador_principal].itens[]`:

```json
{
  "id": "item_destino_minimo",
  "chip": "d",
  "texto": "Destino",
  "tela_destino": "destino_minimo"
}
```

- `texto: "Destino"` → 7 caracteres → ≤ 15 → válido.
- `chip: "d"` → tecla minúscula → compatível com modo pipe da demo.
- `tela_destino: "destino_minimo"` → coincide com o id e nome base de
  `config/telas/destino_minimo.json`.

Remover o campo `pendencia_itens` do JSON do orquestrador após adicionar
o item.

### F-3. Renderer declarativo

O renderer (`tela/renderizador.py`) deve:

a. **Lançador**: para cada elemento de `corpo.elementos[]` cujo `tipo`
   seja `"lancador"`, acessar `elemento._campos_inertes["itens"]`
   (lista) e renderizar cada item como uma caixa bordeada (ou linhas
   internas) com o título do lançador no label e cada item exibido como
   `[{chip}] {texto}`. Rejeitar item com `texto` acima de 15 caracteres
   levantando `RenderizadorErro` — nunca truncar, nunca abreviar.

b. **Dashboard**: para cada elemento de `corpo.elementos[]` cujo `tipo`
   seja `"dashboard"`, acessar `elemento._campos_inertes["campos"]`
   (lista). Para cada campo com `fonte: "literal"`, exibir o `valor` do
   campo como linha de conteúdo dentro da caixa. Campos com
   `fonte: "pendente"` são ignorados na renderização (sem texto de
   placeholder, sem erro).

c. **Console**: para cada elemento de `corpo.elementos[]` cujo `tipo`
   seja `"console"`, renderizar uma caixa com o título (se disponível em
   `_campos_inertes`) e conteúdo placeholder `"(console)"` indicando que
   o console está fora de escopo deste ciclo.

d. **Barra de menus**: ler `modelo.barra_de_menus["chips"]` (lista).
   Renderizar todos os chips declarados como
   `[{tecla}] {texto}` em linha(s) dentro de uma caixa. Não avaliar
   `regra_existencia` nem `regra_ativo` neste ciclo — renderizar todos
   os chips declarados.

e. **Não hardcodar** nenhum texto de item, chip, tecla, tela_destino,
   rótulo de menu ou texto de dashboard. Qualquer conteúdo que apareça
   na saída deve vir do modelo/JSON.

f. **`[B] Borda` deixa de aparecer na saída** — nunca foi declarado no
   JSON. O `b` permanece como comando interno da demo (sem binding
   declarativo), mas não deve ser hardcoded no renderer.

### F-4. Navegação mínima na demo

Ver seção "Especificação de navegação mínima na demo".

---

## Especificação de JSONs de tela

### `config/telas/destino_minimo.json` — CRIAR

Estrutura obrigatória:

```json
{
  "schema": "tela.v1",
  "id": "destino_minimo",
  "cabecalho": {
    "titulo": "Destino Minimo",
    "descricao": "Tela de destino para teste do lancador"
  },
  "corpo": {
    "arranjo": "sobreposto",
    "elementos": [
      {
        "id": "dashboard_teste",
        "tipo": "dashboard",
        "titulo": "Teste",
        "campos": [
          {
            "id": "msg_teste",
            "rotulo": "Mensagem",
            "fonte": "literal",
            "valor": "Tela de destino para teste do lancador"
          }
        ]
      }
    ]
  },
  "barra_de_menus": {
    "distribuicao": "horizontal",
    "chips": [
      {
        "id": "chip_esc",
        "tipo": "acao",
        "tecla": "Esc",
        "texto": "Voltar",
        "acao": {
          "tipo": "acao_contextual_esc",
          "nota": "Voltar na tela interna sem selecao ativa (contrato_barra_de_menus secao 9)"
        },
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "rotulo_dinamico"
      },
      {
        "id": "chip_ajuda",
        "tipo": "acao",
        "tecla": "?",
        "texto": "Ajuda",
        "acao": {"tipo": "abrir_ajuda"},
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "visivel_ativo"
      }
    ]
  }
}
```

Regras obrigatórias:

- `id: "destino_minimo"` deve coincidir com o nome base do arquivo
  (`destino_minimo.json`) — requisito do ADR-0009.
- `schema: "tela.v1"` — versão reconhecida pelo loader.
- `barra_de_menus.chips[id=chip_esc].texto` deve ser `"Voltar"` — não
  `"Sair"`. A diferença de comportamento vem da declaração no JSON,
  não de exceção hardcoded no código.
- O campo do dashboard usa `fonte: "literal"` com `valor` contendo
  o texto de teste. Isso é uma extensão mínima do schema conceitual do
  contrato (seção 11 de `contrato_tela_json.md`), necessária para
  declarar conteúdo textual estático neste ciclo. Nenhuma alteração
  contratual é necessária — o contrato não proíbe campos adicionais
  na declaração inerte.

### `config/telas/orquestrador.json` — ALTERAR

Adicionar item em `corpo.elementos[id=lancador_principal].itens[]`:

```json
{
  "id": "item_destino_minimo",
  "chip": "d",
  "texto": "Destino",
  "tela_destino": "destino_minimo"
}
```

Remover `"pendencia_itens"` do elemento `lancador_principal` após
adicionar o item.

Nenhuma outra alteração em `orquestrador.json`.

---

## Especificação de renderização

### Formato das caixas

O renderer continua usando o sistema de caixas bordeadas herdado do
H-0006/H-0007/H-0009 (funções `_caixa`, `_linha_topo`, `_linha_base`,
`_linha_conteudo`). A largura segue o mesmo parâmetro `largura` (ou
fallback `TOTAL_WIDTH = 42`).

### Renderização do lançador

```
╭ {TÍTULO_LANÇADOR} ────────────────────╮
│ [{chip}] {texto}                      │
│ ...                                   │
╰───────────────────────────────────────╯
```

- O label da caixa é `elemento._campos_inertes.get("titulo", "LANCADOR")`.
- Para cada item em `elemento._campos_inertes.get("itens", [])`:
  - Compor a linha de conteúdo: `"[{chip}] {texto}"`.
  - Se `len(texto) > 15`: levantar `RenderizadorErro` com mensagem
    descritiva — nunca truncar, nunca abreviar.
  - Se `itens` for lista vazia: renderizar caixa sem linhas de conteúdo
    (apenas borda superior e inferior).
- O renderer não cria item não declarado. `itens[]` vazio é renderizado
  como caixa vazia, sem texto de placeholder.

### Renderização do dashboard

```
╭ {TÍTULO_DASHBOARD} ───────────────────╮
│ {valor_campo_literal}                 │
│ ...                                   │
╰───────────────────────────────────────╯
```

- O label da caixa é `elemento._campos_inertes.get("titulo", "DASHBOARD")`.
- Para cada campo em `elemento._campos_inertes.get("campos", [])`:
  - Se `campo.get("fonte") == "literal"`: incluir `campo.get("valor", "")`
    como linha de conteúdo.
  - Caso contrário (`"pendente"` ou outro): ignorar — não emitir linha.
- Se nenhum campo literal: renderizar caixa sem linhas de conteúdo.

Para o `dashboard_info` do `orquestrador.json` (todos os campos com
`fonte: "pendente"`), a caixa será renderizada **sem linhas de conteúdo**
— apenas borda superior e inferior com o título "INFO".

Para o `dashboard_teste` do `destino_minimo.json` (campo com
`fonte: "literal"`, `valor: "Tela de destino para teste do lancador"`),
a caixa exibirá esse texto.

### Renderização do console

```
╭ {TÍTULO_CONSOLE} ─────────────────────╮
│ (console)                             │
╰───────────────────────────────────────╯
```

- O label da caixa é `elemento._campos_inertes.get("titulo", "CONSOLE")`.
- Linha de conteúdo fixa: `"(console)"` — placeholder explícito de
  que o console está fora de escopo neste ciclo.
- Essa linha é a **única exceção** de texto não proveniente do JSON
  permitida neste ciclo, e é explicitamente declarada aqui como
  placeholder de escopo.

### Renderização da barra de menus

```
╭ Menus ────────────────────────────────╮
│ [{tecla}] {texto}   [{tecla}] {texto} │
╰───────────────────────────────────────╯
```

- O label da caixa é fixo `"Menus"` ou o valor do campo `titulo` se
  o executor preferir. O importante é que o **conteúdo** dos chips venha
  do JSON.
- Para cada chip em `modelo.barra_de_menus.get("chips", [])`:
  - Compor: `"[{tecla}] {texto}"`.
  - Concatenar todos em uma ou mais linhas de conteúdo (dentro da
    largura disponível).
- O renderer não hardcoda nenhum chip, tecla, texto nem ordem.
  Percorre `chips[]` na ordem declarada no JSON.
- `regra_existencia` e `regra_ativo` **não são avaliadas** neste ciclo
  — todos os chips declarados são renderizados.

---

## Especificação de navegação mínima na demo

### Estado inicial

```python
def criar_estado_inicial():
    return {
        "tipo_borda": "curva",
        "saindo": False,
        "tela_atual": "orquestrador",
        "pilha_telas": []
    }
```

### Regras de navegação

```
chip do lançador → push tela_atual em pilha_telas; tela_atual = tela_destino
Esc com pilha_telas não vazia → pop pilha_telas; tela_atual = tela anterior
Esc com pilha_telas vazia → saindo = True
```

A lógica de Sair/Voltar está **na demo**, não no renderer. O renderer
apenas lê o texto do chip declarado no JSON (`"Sair"` ou `"Voltar"`).
A demo decide a ação de Esc com base no estado da pilha. Isso é
intencional: o renderer é declarativo; a demo implementa o fluxo mínimo
de navegação.

### Assinatura de `processar_comando`

```python
def processar_comando(estado, comando, modelo=None):
```

O terceiro argumento `modelo` é **opcional** (padrão `None`) para
manter compatibilidade com os testes existentes que chamam
`processar_comando(estado, comando)` sem o terceiro argumento — nesses
casos, o comportamento de `"b"`, `"s"` e `"\x1b"` deve ser preservado
exatamente.

Lógica obrigatória:

```
novo = cópia do estado

Se comando == "b":
    alternar tipo_borda

Se comando == "\x1b" ou comando == "s":
    Se pilha_telas não vazia:
        tela_atual = pilha_telas[-1]
        pilha_telas = pilha_telas[:-1]
    Caso contrário:
        saindo = True

Se modelo não é None e comando não reconhecido:
    Para cada elemento do corpo com tipo "lancador":
        Para cada item em _campos_inertes["itens"]:
            Se item["chip"] == comando:
                push tela_atual em pilha_telas
                tela_atual = item["tela_destino"]
                break

Retornar novo (não modificar o dict original)
```

### Mudança em `main()`

A `main()` da demo deve:
1. Inicializar estado com `criar_estado_inicial()`.
2. Carregar modelo inicial via `carregar_tela(None, estado["tela_atual"])` → `construir_modelo(...)`.
3. Renderizar e imprimir.
4. No loop (TTY ou pipe): ao receber comando, chamar
   `processar_comando(estado, ch, modelo)`.
5. Se `tela_atual` mudou após `processar_comando`, carregar novo modelo
   via `carregar_tela(None, estado["tela_atual"])` → `construir_modelo(...)`.
6. Após mudança de tela ou após `"b"`, renderizar e imprimir o novo
   estado com o modelo atualizado.

Helper recomendado (não obrigatório se o executor preferir inline):

```python
def _carregar_modelo_por_id(id_tela):
    tela_raw = carregar_tela(None, id_tela)
    return construir_modelo(tela_raw)
```

### Sequência de entrada em modo pipe para validar navegação

A sequência obrigatória para verificar o fluxo completo é:

```bash
printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py
```

Interpretação passo a passo:

```
b     → alterna borda (curva → reta); renderiza orquestrador reta
d     → aciona item do lançador (chip "d") → abre destino_minimo;
        renderiza destino_minimo (borda reta)
\x1b  → Esc em destino_minimo → pilha não vazia → volta ao orquestrador;
        renderiza orquestrador (borda reta)
\x1b  → Esc no orquestrador → pilha vazia → saindo = True; sai sem render
```

Saída esperada: render reta do orquestrador + render reta do
destino_minimo + render reta do orquestrador de volta (total: 3 renders).

Para verificação mínima da navegação sem borda:

```bash
printf 'd\n\x1b\n\x1b\n' | python tela/demo.py
```

Saída esperada: render curva do orquestrador (inicial) + render curva
do destino_minimo + render curva do orquestrador de volta (total: 3
renders).

---

## Critérios de aceite

O executor deve verificar **todos** os itens abaixo antes de considerar
a implementação concluída. Nenhum item pode ser ignorado.

```
CA-01. destino_minimo.json existe e é JSON sintaticamente válido.
CA-02. destino_minimo.id == "destino_minimo" (coincide com nome base do arquivo).
CA-03. destino_minimo possui schema, id, cabecalho, corpo e barra_de_menus.
CA-04. destino_minimo renderiza "Tela de destino para teste do lancador"
       na saída do renderer.
CA-05. destino_minimo renderiza texto "Voltar" no chip de Esc.
CA-06. Orquestrador continua renderizando texto "Sair" no chip de Esc.
CA-07. orquestrador.json possui item real em
       corpo.elementos[id=lancador_principal].itens[].
CA-08. O item do lançador declara tela_destino: "destino_minimo".
CA-09. O renderer renderiza o lançador lendo itens[] do JSON/modelo;
       não possui constante hardcoded de itens do lançador.
CA-10. O renderer não possui constante hardcoded de chips da barra
       de menus.
CA-11. Texto de item do lançador acima de 15 caracteres é rejeitado
       pelo renderer levantando RenderizadorErro — sem truncar, sem
       abreviar.
CA-12. Acionar chip "d" na demo abre destino_minimo (tela_atual muda
       para "destino_minimo").
CA-13. Esc em destino_minimo volta para Orquestrador (tela_atual volta
       para "orquestrador").
CA-14. Esc no Orquestrador (com pilha_telas vazia) define saindo = True.
CA-15. Alternância de borda afeta Orquestrador e destino_minimo.
CA-16. Testes anteriores continuam passando (com _EXPECTED_* atualizados
       para refletir o novo output do renderer).
CA-17. Nenhum arquivo normativo é alterado (contratos, ADRs, NOMENCLATURA,
       INDICE, handoffs).
CA-18. Nenhum __pycache__ ou .pyc permanece no repositório após os testes.
CA-19. Relatório de implementação IMP-0010A é criado pelo executor.
CA-20. Commit não é realizado pelo executor — apenas o relatório é
       entregue; o commit é responsabilidade do processo de QA.
```

---

## Impacto obrigatório nos testes existentes

Os arquivos de teste têm `_EXPECTED_*` com output literal do renderer.
Após o H-0010A, o renderer mudará. Os `_EXPECTED_*` **devem** ser
atualizados.

### `tela/teste_renderizador.py`

Atualizar `_EXPECTED_ORQUESTRADOR` e `_EXPECTED_ORQUESTRADOR_RETA` para
o novo output do renderer sobre `orquestrador.json`.

Remover verificações que esperam `"[B] Borda"` — esse texto não estará
mais na saída (nunca foi declarado no JSON).

Adicionar verificações:
- Saída contém texto do chip Esc do JSON (`"Sair"`).
- Saída contém chip `"[d]"` e texto `"Destino"` do item do lançador.
- Saída não contém hardcoding de item (`assert "[d] Destino" not in
  codigo_fonte_renderizador`).
- `renderizar_tela` sobre modelo fabricado de `destino_minimo` contém
  `"Voltar"` e `"Tela de destino para teste do lancador"`.
- Item com texto > 15 chars levanta `RenderizadorErro`.

### `tela/teste_demo.py`

Atualizar `_EXPECTED_CURVA` e `_EXPECTED_RETA` para o novo output do
renderer.

Atualizar testes de `processar_comando` para incluir `"pilha_telas": []`
no dict de estado (compatibilidade com novos campos do estado).

Atualizar testes de integração via subprocess para a nova sequência de
output.

Adicionar verificações de navegação:
- `processar_comando` com chip `"d"` e modelo com lançador → muda
  `tela_atual` para `"destino_minimo"`.
- `processar_comando` com `"\x1b"` e `pilha_telas: ["orquestrador"]` →
  pop pilha; `tela_atual` volta para `"orquestrador"`.
- Subprocess com `"d\n\x1b\n\x1b\n"` → encerra com código 0 e exibe
  3 renders (orquestrador, destino_minimo, orquestrador).

### `tela/teste_diagnostico.py`

Atualizar `_EXPECTED_ORQUESTRADOR` para o novo output do renderer.

Remover verificação de `"[B] Borda"`.

Adicionar verificação de `"Sair"` (chip Esc declarado no JSON).

### `tela/teste_loader.py`

Ampliar com:
- `lancador_principal.itens` possui exatamente 1 item após a alteração.
- O item tem `id`, `chip`, `texto` e `tela_destino`.
- `texto == "Destino"` (exatamente 7 chars).
- `tela_destino == "destino_minimo"`.

### `tela/teste_modelo.py`

Ampliar com:
- `lancador_principal._campos_inertes["itens"]` é lista com 1 item.
- O item preserva `chip`, `texto`, `tela_destino` como declaração inerte.

---

## Comandos obrigatórios de verificação

O executor deve executar **todos** os comandos abaixo e confirmar que
nenhum retorna erro ou output inesperado.

### Validade dos JSONs

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
```

### Testes unitários e de integração

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
python tela/diagnostico.py
```

Todos devem encerrar com código de saída 0.

### Verificação de comportamento da demo em modo pipe

Sequência mínima (sem navegação):

```bash
printf 'b\n\x1b\n' | python tela/demo.py
```

Sequência completa de navegação (obrigatória para CA-12, CA-13, CA-14):

```bash
printf 'd\n\x1b\n\x1b\n' | python tela/demo.py
```

Sequência com borda alternada e navegação (verificação combinada):

```bash
printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py
```

Esperado para a sequência `'b\nd\n\x1b\n\x1b\n'`:
1. Render inicial do orquestrador (borda curva) — produzido antes do
   loop de pipe.
2. Render do orquestrador com borda reta (após `b`).
3. Render do destino_minimo com borda reta (após `d`).
4. Render do orquestrador com borda reta (após `\x1b` em
   destino_minimo).
5. Sem render final (após `\x1b` no orquestrador: `saindo = True`, sai).

Total: 4 renders impressos, código de saída 0.

### Verificações de cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Ambos devem retornar vazio (nenhum arquivo de cache no repositório).

```bash
git status --short
git diff --stat
git diff --name-only
```

O executor não faz commit. O relatório IMP-0010A deve descrever os
arquivos alterados observados por esses comandos.

---

## Condições de bloqueio

O executor deve parar imediatamente e reportar o status indicado se
encontrar qualquer das situações abaixo.

### `ARCHITECTURE_REVIEW_REQUIRED`

Parar com este status se a implementação exigir:

```
alterar contrato (qualquer contrato em docs/contratos/)
alterar ADR (qualquer ADR em docs/adr/)
alterar NOMENCLATURA
criar registry completo de telas
criar registry completo de ações
criar sistema genérico de ações
hardcodar item de lançador no renderer
hardcodar texto, tecla ou chip de barra_de_menus no renderer
decidir comportamento de Esc (Sair/Voltar) por id específico de tela
  hardcoded no renderer ou na demo
criar micro-handoff separado para campo, item, chip ou Esc que pertença
  à mesma capacidade coesa do H-0010A
```

### `BLOCKED`

Parar com este status se encontrar impedimento operacional objetivo:

```
config/telas/orquestrador.json ausente ou JSON inválido
config/telas/destino_minimo.json ausente após tentativa de criar
tela/loader.py, tela/modelo.py ou tela/renderizador.py ausentes
Erro de importação em tela/ que impeça executar os testes
Escopo de arquivos insuficiente (arquivo necessário não está na lista
  de arquivos permitidos)
```

---

## Resultado esperado do executor

Ao final do ciclo, o executor deve entregar:

1. `config/telas/destino_minimo.json` criado e válido.
2. `config/telas/orquestrador.json` alterado com item real no lançador.
3. `tela/renderizador.py` alterado: lê lançador, dashboard e
   barra_de_menus do modelo/JSON; não hardcoda conteúdo.
4. `tela/demo.py` alterado: estado com `tela_atual` e `pilha_telas`;
   `processar_comando` com terceiro argumento opcional `modelo=None`.
5. Todos os cinco arquivos de teste alterados/ampliados com
   `_EXPECTED_*` atualizados e novas verificações de navegação.
6. Todos os comandos de verificação executados e com saída limpa.
7. `docs/relatorios/IMP-0010A-fluxo-minimo-lancador-tela-destino.md`
   criado com descrição do que foi implementado, arquivos alterados,
   saídas dos comandos de verificação e status final.
8. Nenhum `__pycache__` ou `.pyc` no repositório.
9. Nenhum commit realizado.
10. Nenhum arquivo normativo alterado.
