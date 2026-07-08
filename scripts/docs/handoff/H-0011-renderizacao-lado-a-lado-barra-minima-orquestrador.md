---
name: H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador
description: Handoff de implementação — renderização visual lado_a_lado para elementos console/lancador e barra mínima da tela raiz; declarativo por JSON; sem hardcoding no renderer
metadata:
  type: handoff_implementacao
  status: HANDOFF_READY
  id: H-0011
  data_criacao: 2026-07-08
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_lancador.md
  adrs_aplicadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  handoffs_anteriores:
    - docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
---

# H-0011 — Renderização lado_a_lado e barra mínima do Orquestrador

## Status

`HANDOFF_READY`

---

## Contexto

O H-0010A implementou o fluxo mínimo de lançador com tela destino: o renderer
passou a ler `lancador.itens[]`, `dashboard.campos[]` e `barra_de_menus.chips[]`
do modelo/JSON, sem hardcoding. O QA aprovou o ciclo (`QA_APPROVED_WITH_NOTES`,
`36c55d2`).

Após o QA, foi realizada uma validação exploratória (`RELATORIO_VALIDACAO_H-0010A_DECLARATIVA_STUB_B.md`,
`f41bd2f`) que confirmou:

```text
- nova tela pode ser criada apenas por JSON;
- item novo pode ser adicionado ao lançador por JSON;
- dashboard muda de título por JSON;
- chips da barra_de_menus mudam por JSON;
- loader/modelo preservam corpo.arranjo = "lado_a_lado" quando declarado;
- renderer ainda exibe os elementos empilhados mesmo quando arranjo = "lado_a_lado".
```

O estado atual do repositório (limpo, `HEAD = f41bd2f`) tem `orquestrador.json`
com `arranjo = "sobreposto"` e `barra_de_menus` com 11 chips (incluindo chips
condicionais que não pertencem à tela raiz neste estágio). As mudanças
exploratórias da validação foram documentadas, mas **não foram incorporadas ao
commit**.

---

## Problema

Dois problemas coexistentes a corrigir neste ciclo:

**1. O renderer ignora `modelo.corpo.arranjo`.**
Quando `arranjo == "lado_a_lado"`, os elementos `console` e `lancador` devem
ser renderizados em colunas horizontais. O renderer atual empilha todos os
elementos verticalmente, independentemente do valor de `arranjo`. Isso contraria
a regra fundamental do contrato de composição de corpo (R-2):

> O renderer recebe a declaração validada e a executa. Não possui lógica de
> seleção de tipo, não possui fallback de tipo, e não toma nenhuma decisão de
> composição com base em condições de ambiente.

**2. A `barra_de_menus` do Orquestrador declara chips que não pertencem à tela.**
O `orquestrador.json` atual declara 11 chips na barra, incluindo chips
condicionais cujas capacidades correspondentes (`paginacao`, `colunas_ajustavel`,
`filtro_de_grupo`, `selecao_multipla`, `modo_verboso`) não estão implementadas
neste estágio. Isso viola o princípio declarativo: a tela declara apenas o que
pertence a ela agora. O renderer não deve inventar chips ausentes, nem a tela
deve declarar chips cujas condições são ainda puramente conceituais.

---

## Objetivo

Implementar, em um único ciclo coeso, duas mudanças:

```text
1. Implementar no renderer a execução visual de corpo.arranjo = "lado_a_lado".
2. Atualizar config/telas/orquestrador.json:
   a. Declarar arranjo = "lado_a_lado".
   b. Reduzir barra_de_menus para apenas [Esc] Sair e [?] Ajuda.
```

O objetivo arquitetural é consolidar que o renderer executa o arranjo declarado
sem decidir por conta própria, e que a tela declara apenas o que pertence a ela
no estágio atual.

---

## Leitura obrigatória realizada

O executor que preparou este handoff leu e analisou:

```text
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_lancador.md

docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md

docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/relatorios/RELATORIO_QA_H-0010A_FLUXO_MINIMO_LANCADOR_TELA_DESTINO.md
docs/relatorios/RELATORIO_VALIDACAO_H-0010A_DECLARATIVA_STUB_B.md

config/telas/orquestrador.json
config/telas/destino_minimo.json
config/telas/stub_b.json

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

**`tela/modelo.py`** — lido para determinar como o renderer deve acessar o
arranjo declarado no JSON. Justificativa objetiva: a especificação funcional do
renderer precisa nomear o atributo Python correto. Resultado da consulta:

```python
# Corpo é dataclass com campo:
@dataclass
class Corpo:
    arranjo: str | None   # <- valor de corpo.arranjo do JSON, ou None
    elementos: list

# Acesso no renderer:
modelo.corpo.arranjo  # retorna "lado_a_lado", "sobreposto", ou None
```

`modelo.corpo.arranjo` é o ponto de acesso canônico. O loader já preserva o
valor. O modelo já expõe via `Corpo.arranjo`. Nenhuma alteração em `loader.py`
ou `modelo.py` é necessária.

---

## Escopo positivo

O H-0011 especifica a implementação de:

```text
1. Alterar renderizador.py para executar arranjo "lado_a_lado":
   - quando modelo.corpo.arranjo == "lado_a_lado", renderizar elementos
     console/lancador em colunas horizontais;
   - dashboard não entra no bloco lado_a_lado (ver especificação).

2. Alterar config/telas/orquestrador.json:
   - mudar corpo.arranjo de "sobreposto" para "lado_a_lado";
   - reduzir barra_de_menus para [Esc] Sair e [?] Ajuda.

3. Atualizar testes existentes:
   - atualizar _EXPECTED_* para o novo output do renderer;
   - adicionar verificações de lado_a_lado;
   - atualizar verificações da barra mínima.

4. Preservar fluxo H-0010A:
   - [d] Destino -> destino_minimo continua funcionando;
   - Esc em destino_minimo -> Voltar;
   - Esc no Orquestrador -> Sair;
   - b alterna borda;
   - diagnóstico continua determinístico e não interativo.
```

---

## Escopo negativo

O H-0011 **não deve** implementar:

```text
registry completo de telas
registry completo de ações
navegação por [✥]
paginação
seleção
filtros
modo verboso
console real (continua placeholder "(console)")
dashboard real com dados de fontes externas
posicionamento horizontal completo do dashboard
sistema genérico de posicionamento de dashboard
conectar stub_b ao Orquestrador
adicionar novos itens ao lancador
alterar contratos
alterar ADRs
alterar NOMENCLATURA
hardcodar chips no renderer
hardcodar lista de elementos do corpo no renderer
hardcodar arranjo por id específico de tela
criar fallback que ignore lado_a_lado
criar fallback de arranjo por largura de terminal
remover ou quebrar destino_minimo
alterar destino_minimo.json
alterar stub_b.json
alterar demo.py (ver seção Arquivos permitidos)
```

---

## Arquivos permitidos

Lista explícita e exaustiva de arquivos que o executor poderá criar ou alterar.

### Alterar

```text
config/telas/orquestrador.json

tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_diagnostico.py
tela/teste_demo.py
```

### Criar

```text
docs/relatorios/IMP-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
```

### Justificativa para arquivos não incluídos

**`tela/demo.py`** — NÃO ALTERAR.
A demo chama `renderizar_tela(modelo, tipo_borda, largura)`. O renderer é que
muda seu comportamento interno quando `modelo.corpo.arranjo == "lado_a_lado"`.
A interface da demo com o renderer não muda. A navegação mínima (pilha, Esc,
chip de lançador) também não muda.

**`tela/loader.py`** — NÃO ALTERAR.
O loader já preserva `corpo.arranjo` como campo do dict retornado. A validação
empírica confirmou que `arranjo = "lado_a_lado"` chega ao modelo sem alteração.
Se a implementação exigir alterar o loader, parar com `ARCHITECTURE_REVIEW_REQUIRED`.

**`tela/modelo.py`** — NÃO ALTERAR.
`Corpo.arranjo` já é atributo declarado do dataclass. O valor de `orquestrador.json`
chega ao renderer via `modelo.corpo.arranjo`. Nenhuma mudança no modelo é
necessária. Se a implementação exigir alterar o modelo, parar com
`ARCHITECTURE_REVIEW_REQUIRED`.

**`tela/diagnostico.py`** — NÃO ALTERAR.
O diagnóstico encadeia `carregar_tela` → `construir_modelo` → `renderizar_tela`
para `id_tela = "orquestrador"`. O comportamento externo continuará correto
após as alterações no renderer. Apenas o output esperado em `teste_diagnostico.py`
mudará.

**`config/telas/destino_minimo.json`** — NÃO ALTERAR.
`destino_minimo` usa `arranjo = "sobreposto"`. Isso é correto: a tela tem apenas
um elemento (dashboard). Não há nada a mudar.

**`config/telas/stub_b.json`** — NÃO ALTERAR.
`stub_b` existe como artefato de validação declarativa. **Não conectar `stub_b`
ao Orquestrador neste ciclo.** A tela permanece disponível em disco mas não
acionada pela tela raiz. Conectar `stub_b` exigiria adicionar item ao lançador
e atualizar todos os expected literals — escopo desnecessário para H-0011.

**`tela/__init__.py`** — NÃO ALTERAR (proibido).

---

## Arquivos proibidos

O executor **não pode** criar nem alterar:

```text
docs/contratos/
docs/adr/
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/handoff/  (exceto o próprio H-0011, que é artefato de engenharia)
docs/relatorios/RELATORIO_QA_H-0010A_FLUXO_MINIMO_LANCADOR_TELA_DESTINO.md
docs/relatorios/RELATORIO_VALIDACAO_H-0010A_DECLARATIVA_STUB_B.md

config/telas/destino_minimo.json
config/telas/stub_b.json
config/estilo.json
config/lancador.json
config/barra_de_menus.json
config/cabecalho.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json

tela/loader.py
tela/modelo.py
tela/diagnostico.py
tela/demo.py
tela/__init__.py
```

---

## Especificação funcional

### F-1. Alteração de `config/telas/orquestrador.json`

#### F-1a. Arranjo lado_a_lado

Mudar o campo `corpo.arranjo` de:

```json
"arranjo": "sobreposto"
```

para:

```json
"arranjo": "lado_a_lado"
```

Nenhuma outra mudança na estrutura de `corpo.elementos[]`.

#### F-1b. Barra mínima

Substituir a lista `barra_de_menus.chips[]` por exatamente dois chips:

```json
"chips": [
  {
    "id": "chip_esc",
    "tipo": "acao",
    "tecla": "Esc",
    "texto": "Sair",
    "acao": {
      "tipo": "acao_contextual_esc",
      "nota": "Limpar quando ha selecao ativa; Sair na tela raiz sem selecao (contrato_barra_de_menus secao 9)"
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
```

Remover os chips:
- `chip_paginas` (`<>` Páginas)
- `chip_colunas` (`-+` Colunas)
- `chip_grupos` (`#` Grupos)
- `chip_alternar` (`⇆` Alternar)
- `chip_navegar` (`✥` Navegar)
- `chip_selecionar` (`␣` Selecionar)
- `chip_enter` (`⏎` Todos)
- `chip_estilo` (`|` Estilo)
- `chip_verboso` (`V` Verboso)

**Justificativa**: a especificação concreta de quais chips aparecem em uma tela
pertence ao `tela.json` da própria tela. O contrato define semântica e
invariantes, não força a presença de todos os chips no Orquestrador. O renderer
não deve inventar chips ausentes nem consultar uma lista contratual para preencher
a barra. Chips condicionais cujas capacidades ainda não estão implementadas não
devem ser declarados na tela.

### F-2. Renderização de `lado_a_lado` no renderer

#### F-2a. Detecção do arranjo

O renderer deve verificar `modelo.corpo.arranjo` antes de decidir como renderizar
os elementos do corpo:

```python
if modelo.corpo.arranjo == "lado_a_lado":
    # renderização lado_a_lado
else:
    # renderização atual (empilhada)
```

O renderer **não decide o arranjo por conta própria**. Ele executa o valor
declarado. Ausência de `arranjo` (None) equivale ao comportamento empilhado
atual. O renderer não inventa fallback por largura de terminal.

#### F-2b. Separação de elementos por grupo

Em modo `lado_a_lado`, o renderer deve separar os elementos de
`modelo.corpo.elementos` em dois grupos, preservando a ordem declarada no JSON:

```python
grupo_lado_a_lado = [e for e in modelo.corpo.elementos if e.tipo in ("console", "lancador")]
grupo_dashboard   = [e for e in modelo.corpo.elementos if e.tipo == "dashboard"]
```

`dashboard` não entra no bloco lado_a_lado. Tem eixo próprio de posicionamento
(`posicao_dashboard`). Para este ciclo: dashboard renderiza verticalmente
(comportamento atual preservado), após o bloco lado_a_lado.

#### F-2c. Bloco lado_a_lado para 2 elementos

Quando `grupo_lado_a_lado` tiver exatamente 2 elementos, o renderer deve:

1. Calcular `col_w = total_w // 2`.
2. Renderizar cada elemento individualmente como string de caixa com largura
   `col_w` (usando as mesmas funções `_caixa`, `_linhas_*`).
3. Dividir cada string em linhas.
4. Padded para altura igual: a caixa mais curta recebe linhas em branco de
   `col_w` espaços até igualar a altura da maior.
5. Combinar as linhas: para cada índice `i`, concatenar linha_esq[i] + linha_dir[i].
6. Juntar as linhas combinadas com `"\n"`.

**Exemplo conceitual de output** (não normativo — dimensões ajustadas ao terminal):

```
╭ ITENS ─────────────╮╭ NAVEGAR ──────────╮
│ (console)          ││ [d] Destino        │
╰────────────────────╯╰───────────────────╯
```

O renderer não precisa inserir espaço entre as duas caixas. As linhas de cada
caixa já somam `total_w` quando `col_w = total_w // 2` e ambas têm `col_w`
chars.

**Caso com número ímpar de total_w**: usar `col_w = total_w // 2`. A segunda
coluna pode ter largura `total_w - col_w` para absorver o caractere extra, ou
ambas com `col_w`. O executor deve escolher a abordagem mais simples que
mantenha o invariante de que cada linha de output tenha comprimento consistente.

#### F-2d. Bloco lado_a_lado com 1 elemento

Se `grupo_lado_a_lado` tiver apenas 1 elemento: renderizar normalmente com
largura `total_w` (comportamento empilhado). Não há par para dispor lado a lado.

#### F-2e. Bloco lado_a_lado com 3+ elementos

Para este ciclo, o Orquestrador tem exatamente 2 elementos console/lancador.
O executor **não precisa** implementar `lado_a_lado` para 3+ elementos. Se por
algum motivo o modelo tiver 3+ elementos, o renderer pode renderizá-los
empilhados normalmente (não é caso de uso do H-0011).

#### F-2f. Ordem de renderização em modo lado_a_lado

```text
1. Caixa de cabeçalho (comportamento atual preservado)
2. Bloco lado_a_lado (grupo_lado_a_lado, na ordem do JSON)
3. Elementos dashboard (grupo_dashboard, empilhados, na ordem do JSON)
4. Caixa de barra_de_menus (comportamento atual preservado)
```

Para o Orquestrador atual (`console_principal`, `dashboard_info`, `lancador_principal`):
- `grupo_lado_a_lado` = [`console_principal`, `lancador_principal`] (ordem do JSON mantida)
- `grupo_dashboard` = [`dashboard_info`]
- Output: cabeçalho → [console|lancador lado_a_lado] → dashboard → menus

#### F-2g. Modo empilhado preservado

Quando `modelo.corpo.arranjo != "lado_a_lado"` (inclui `None` e `"sobreposto"`),
o renderer deve usar exatamente o comportamento atual: percorrer
`modelo.corpo.elementos` em ordem e renderizar cada caixa com largura `total_w`.

Não alterar o caminho de código do modo empilhado. `destino_minimo` e `stub_b`
usam `arranjo = "sobreposto"` e devem continuar funcionando sem alteração.

---

## Especificação de arranjo lado_a_lado

Regras arquiteturais que o executor deve cumprir e verificar:

**R-L1. Renderer executa o arranjo declarado.**
`modelo.corpo.arranjo` é a única fonte de decisão de arranjo quando declarado.
O renderer não pode ignorar `lado_a_lado` nem decidir voltar para empilhado
por condição de ambiente (largura de terminal, quantidade de elementos, etc.).

**R-L2. Sem fallback por largura.**
O renderer não verifica se a tela é "larga o suficiente" para decidir usar
`lado_a_lado`. Se declarado, usa. Cabe ao declarante do JSON garantir que o
terminal suportará a largura.

**R-L3. Sem hardcoding de composição.**
O renderer percorre `grupo_lado_a_lado` dinamicamente. Não pode ter constante
fixando quais elementos formam o par. O par é derivado da lista de elementos
com tipo `console` ou `lancador`.

**R-L4. Dashboard separado do arranjo.**
Nenhum elemento de `grupo_dashboard` entra no bloco de colunas lado_a_lado.
`posicao_dashboard` é campo da instância (`posicao_dashboard = "vertical"` no
Orquestrador). Para este ciclo, preservar comportamento vertical atual do
dashboard: renderizar como caixa independente com largura `total_w`, após o
bloco lado_a_lado. Posicionamento horizontal de dashboard (`posicao_dashboard =
"horizontal"`) está **fora de escopo** deste ciclo.

**R-L5. `destino_minimo` e `stub_b` não são afetados.**
Ambos declaram `arranjo = "sobreposto"`. O renderer deve continuar produzindo
output empilhado para essas telas sem alteração.

---

## Especificação de dashboard fora do eixo de arranjo

O `contrato_composicao_corpo.md` seção 5.6 estabelece:

> Aplica-se exclusivamente ao arranjo de 2+ elementos console/lancador. Nunca
> decide a posição do dashboard — esse é o campo posicao_dashboard declarado
> na instância (seção 4.3).

E a seção 9 registra como pendência explícita:

> **Combinação arranjo = lado_a_lado + dashboard presente ao mesmo tempo**: comportamento
> do indicador de paginação e posicionamento do dashboard quando ambas as condições
> estão ativas simultaneamente. Sem caso de uso real até o momento — não especificar
> nem implementar até surgir caso concreto.

Portanto, para este ciclo:

```text
- Dashboard renderiza como caixa vertical independente (largura total_w),
  após o bloco lado_a_lado.
- Não transformar dashboard em coluna do arranjo lado_a_lado.
- Não implementar posicao_dashboard = "horizontal".
- Não implementar sistema completo de posicionamento de dashboard.
- Se a implementação exigir decidir como posicionar dashboard horizontal
  em modo lado_a_lado sem contrato explícito, parar com
  ARCHITECTURE_REVIEW_REQUIRED.
```

---

## Especificação da barra mínima do Orquestrador

A barra de menus da tela raiz deve ficar declarada com exatamente dois chips:

```text
[Esc] Sair
[?] Ajuda
```

**Por que remover os outros chips?**

Os chips condicionais removidos (`[<>] Páginas`, `[-+] Colunas`, `[#] Grupos`,
`[⇆] Alternar`, `[✥] Navegar`, `[␣] Selecionar`, `[⏎] Todos`, `[|] Estilo`,
`[V] Verboso`) existem no `orquestrador.json` como declarações conceituais
de capacidades futuras. Nenhuma dessas capacidades está implementada. O renderer
não avalia `regra_existencia` neste estágio — renderiza todos os chips declarados.
Resultado: a barra exibe chips que não têm comportamento real, confundindo a
leitura do estado real da tela.

**Regra arquitetural**:

> A especificação concreta de quais chips aparecem em uma tela pertence ao
> `tela.json` da própria tela. O contrato define semântica e invariantes, não
> força a presença de todos os chips no Orquestrador. O renderer não deve
> inventar chips ausentes nem consultar uma lista contratual para preencher a
> barra.

Quando as capacidades correspondentes forem implementadas, cada chip voltará
ao `orquestrador.json` como declaração concreta — não como placeholder.

**O renderer NÃO deve**:

```text
- Hardcodar lista de chips da barra_de_menus.
- Verificar se há chips "obrigatórios" ausentes.
- Completar a barra com chips canônicos que o JSON não declarou.
- Filtrar chips da lista retornada pelo JSON.
```

O renderer percorre `modelo.barra_de_menus["chips"]` e renderiza o que encontrar.
Com apenas dois chips no JSON, a barra exibirá apenas dois chips.

---

## Critérios de aceite

O executor deve verificar **todos** os itens abaixo antes de considerar a
implementação concluída. Nenhum item pode ser ignorado.

```text
CA-01. orquestrador.json é JSON sintaticamente válido.
CA-02. orquestrador.corpo.arranjo == "lado_a_lado".
CA-03. destino_minimo.json e stub_b.json permanecem sem alteração.
CA-04. loader preserva arranjo = "lado_a_lado" do orquestrador (lido
       via teste_loader.py).
CA-05. modelo preserva arranjo = "lado_a_lado" (modelo.corpo.arranjo ==
       "lado_a_lado" verificado em teste_modelo.py).
CA-06. renderer usa lado_a_lado para renderizar console/lancador em
       composição horizontal quando modelo.corpo.arranjo == "lado_a_lado".
CA-07. saída visual do Orquestrador não é apenas empilhada: console e
       lancador aparecem na mesma linha horizontal (output contém linhas
       combinadas lado a lado).
CA-08. dashboard do Orquestrador não é tratado como coluna do bloco
       lado_a_lado — renderiza como caixa independente com largura
       total_w.
CA-09. barra_de_menus do Orquestrador exibe somente [Esc] Sair e [?] Ajuda.
CA-10. renderer não inventa chips ausentes (barra não exibe chips não
       declarados no JSON).
CA-11. renderer não contém lista hardcoded de chips da barra_de_menus.
CA-12. renderer não contém lista hardcoded de elementos do corpo.
CA-13. renderer não contém lógica de arranjo baseada em id específico
       de tela.
CA-14. destino_minimo continua renderizando empilhado (arranjo =
       "sobreposto" preservado).
CA-15. [d] Destino -> destino_minimo continua funcionando.
CA-16. Esc em destino_minimo -> Voltar continua funcionando.
CA-17. Esc no Orquestrador -> Sair continua funcionando.
CA-18. b alterna borda nas duas telas.
CA-19. diagnóstico continua determinístico e não interativo.
CA-20. testes anteriores são atualizados para os novos expected literals
       do orquestrador (lado_a_lado + barra mínima).
CA-21. todos os cinco testes obrigatórios passam com exit 0.
CA-22. sem __pycache__ ou .pyc.
CA-23. sem commit.
CA-24. relatório IMP-0011 criado pelo executor.
```

---

## Comandos obrigatórios de verificação

O executor deve executar **todos** os comandos abaixo e confirmar que nenhum
retorna erro ou output inesperado.

### Validade dos JSONs

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
python -m json.tool config/telas/stub_b.json >/dev/null && echo "stub_b.json OK"
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

Sequência completa (preservação do fluxo H-0010A):

```bash
printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py
```

Saída esperada: 4 renders com saída limpa (exit 0):
1. Orquestrador com borda curva e layout lado_a_lado.
2. Orquestrador com borda reta e layout lado_a_lado (após `b`).
3. destino_minimo com borda reta e layout empilhado (após `d`).
4. Orquestrador com borda reta e layout lado_a_lado (após Esc em destino).
5. Sem render extra (após Esc no Orquestrador: saindo = True, sai).

### Verificação de ausência de hardcoding

```bash
grep -n "lado_a_lado\|sobreposto\|console_principal\|lancador_principal\|dashboard_info\|orquestrador" tela/renderizador.py
```

Nenhuma ocorrência de IDs específicos de tela ou valores de arranjo hardcoded
deve aparecer em código executável do renderer. Comentários são permitidos.

### Verificação de cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Ambos devem retornar vazio.

```bash
git status --short
git diff --stat
git diff --name-only
```

O executor não faz commit. O relatório IMP-0011 deve registrar os arquivos
alterados observados por esses comandos.

---

## Condições de bloqueio

O executor deve parar imediatamente e reportar o status indicado se encontrar
qualquer uma das situações abaixo.

### `ARCHITECTURE_REVIEW_REQUIRED`

Parar com este status se a implementação exigir:

```text
alterar contrato (qualquer arquivo em docs/contratos/)
alterar ADR (qualquer arquivo em docs/adr/)
alterar NOMENCLATURA
alterar loader.py ou modelo.py
decidir sem contrato como posicionar dashboard horizontal em modo lado_a_lado
implementar registry completo de telas
implementar registry completo de ações
implementar sistema genérico de ações
hardcodar chips no renderer
hardcodar lista de elementos do corpo por id de tela
hardcodar arranjo por id específico de tela
ignorar lado_a_lado por largura de terminal
criar fallback de arranjo não declarado no JSON e não coberto por estilo.json
```

### `BLOCKED`

Parar com este status se encontrar impedimento operacional objetivo:

```text
config/telas/orquestrador.json ausente ou JSON inválido
tela/renderizador.py, tela/loader.py, tela/modelo.py ausentes
erro de importação em tela/ que impeça executar os testes
arquivo necessário não está na lista de arquivos permitidos
```

---

## Resultado esperado

Ao final do ciclo, o executor deve entregar:

```text
1. config/telas/orquestrador.json alterado:
   - arranjo = "lado_a_lado";
   - barra_de_menus com apenas [Esc] Sair e [?] Ajuda.

2. tela/renderizador.py alterado:
   - modo lado_a_lado implementado para 2 elementos console/lancador;
   - dashboard não entra no bloco lado_a_lado;
   - modo empilhado preservado para arranjos diferentes de "lado_a_lado";
   - sem hardcoding de ids de tela, elementos ou chips.

3. Cinco arquivos de teste atualizados:
   - _EXPECTED_ORQUESTRADOR e _EXPECTED_ORQUESTRADOR_RETA refletem
     o novo output do renderer com lado_a_lado + barra mínima;
   - verificações de lado_a_lado adicionadas;
   - verificações de barra mínima adicionadas;
   - todos os testes passam com exit 0.

4. docs/relatorios/IMP-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
   criado com descrição do que foi implementado, arquivos alterados,
   saídas dos comandos de verificação e status final.

5. Nenhum __pycache__ ou .pyc.
6. Nenhum commit realizado.
7. Nenhum arquivo normativo alterado.
```
