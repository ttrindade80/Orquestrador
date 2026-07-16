---
name: H-0033-ocupacao-integral-corpo
description: Implementação de DA-01 a DA-04 (ADR-0024): eliminar preenchimento externo vazio do corpo e garantir ocupação integral da área disponível por console, dashboard ou lancador
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0033
  data_criacao: 2026-07-16
rastreabilidade:
  adr_principal: docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
  adrs_relacionadas:
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
  contratos_aplicados:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
  relatorios_autoridade:
    - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
    - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0024.md
  handoffs_anteriores:
    - docs/handoff/H-0032-migracao-estrutural-demonstracao-configuracoes.md
    - docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
---

# H-0033 — Ocupação integral do corpo

## 1. Identificação

Handoff de implementação: `H-0033`.

Título: `Ocupação integral do corpo`.

Arquivo deste handoff:

```text
docs/handoff/H-0033-ocupacao-integral-corpo.md
```

Etapa futura autorizada por este documento: implementação técnica da ADR-0024
(DA-01 a DA-04) no renderer, nos testes e nas fixtures.

Próxima categoria esperada após a criação deste handoff: `QA_HANDOFF`.

---

## 2. Contexto e cronologia

### 2.1 Origem

O ciclo H-0030 concluiu o catálogo de telas utilizáveis e registrou, no
levantamento final (`docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md`), a
existência de linhas físicas vazias externas nas telas `destino_minimo` e
`grupo_minimo`. Essas linhas não pertencem a nenhum elemento visual: são
produzidas pelo renderer para completar a altura do corpo quando `distribuicao`
está ausente.

### 2.2 ADR-0024

A ADR-0024 (`docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md`) foi
criada, revisada, aprovada (QA `status_literal: ADR_APPROVED`) e aplicada
documentalmente. A aplicação documental atualizou ADR-0013, ADR-0018,
`contrato_composicao_corpo.md`, `contrato_tela_json.md`,
`contrato_json_tela_minima.md`, `NOMENCLATURA.md` e `INDICE_ADR.md`.
O QA da aplicação documental registrou `status_literal: ADR_APPLICATION_APPROVED`
e `proxima_categoria: CRIAR_HANDOFF`.

### 2.3 Numeração

O H-0033 é o próximo handoff real em numeração estritamente sequencial.

O salto de H-0032 para H-0034 foi erro gerencial no ciclo anterior. O H-0033
foi criado em 2026-07-16 após a conclusão e aprovação do fluxo documental da
ADR-0024. Os artefatos da ADR-0024 permanecem acumulados no workspace e ainda
não foram commitados. Essa conclusão documental não equivale a fechamento Git.
Cronologicamente, H-0033 é posterior ao H-0034 existente; não é um documento
retroativo ou antigo.

A numeração correta é preservada:
`H-0032 < H-0033 (criado agora) > H-0034 (já existe, criado antes)`.

Nenhum handoff existente é renumerado.
O H-0033 não foi reservado anteriormente e não existe commit do H-0033.

### 2.4 Estado git na criação deste handoff

Estado inicial observado:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
 M docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
?? docs/relatorios/RELATORIO_QA_ADR-0024.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0024.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md
```

Essas alterações pertencem ao ciclo ADR-0024 e não são atribuídas ao autor
deste handoff.

---

## 3. Autoridades

As autoridades normativas fechadas para esta implementação são:

| Documento | Papel |
|---|---|
| `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md` | Autoridade normativa principal — proibição e DA-01 a DA-04 |
| `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md` | Autoridade complementar — cláusula 4 substituída; demais cláusulas vigentes |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | Autoridade complementar — D2 substituído; demais regras vigentes |
| `docs/contratos/contrato_composicao_corpo.md` | Contrato de composição — seções 4.7, 5.7, 5.9, 8 e 10 atualizados |
| `docs/contratos/contrato_tela_json.md` | Contrato da tela JSON — seções 8 e 9 atualizados |
| `docs/contratos/contrato_json_tela_minima.md` | Contrato da tela mínima — seções 6.2 e 6.3 atualizados |
| `docs/NOMENCLATURA.md` | Nomenclatura — seções 14.1 e 14.2 atualizados |
| `docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md` | Evidências mensuráveis do comportamento atual |

Relatórios são evidências de processo; não são autoridades arquiteturais.

---

## 4. Decisões fechadas

As quatro decisões a seguir foram aprovadas pelo usuário e incorporadas
normativamente à ADR-0024, seção 21. O executor não pode redefinir nem
substituir nenhuma delas.

### DA-01 — Cardinalidade unitária

Quando um corpo ou container possuir exatamente um descendente visual
aplicável, esse elemento deve ocupar integralmente toda a área disponível,
mesmo sem `distribuicao` declarada.

Esta regra:
- decorre da cardinalidade unitária;
- não representa `distribuicao: igual`;
- não cria distribuição entre múltiplos elementos;
- impede qualquer sobra atribuída ao corpo ou ao container.

### DA-02 — Múltiplos elementos sem distribuição

Quando dois ou mais elementos disputarem área no mesmo eixo, `distribuicao`
é obrigatória.

A ausência de `distribuicao`:
- não significa `igual`;
- não permite ao renderer escolher implicitamente quem recebe a sobra;
- não permite preenchimento externo vazio;
- torna a composição inválida quando houver área a distribuir entre
  múltiplos elementos.

A diferença semântica entre ausência de distribuição e `distribuicao: igual`
é preservada (ADR-0018, D5).

### DA-03 — Grupos e containers estruturais

O `grupo` continua exclusivamente estrutural e não conta como elemento visual.

Toda área atribuída a um grupo ou container estrutural deve ser repassada
integralmente aos seus descendentes visuais.

Regras:
1. com exatamente um descendente visual aplicável, ele ocupa a área
   integralmente (DA-01);
2. com múltiplos descendentes disputando o mesmo eixo, `distribuicao` é
   obrigatória (DA-02);
3. nenhuma linha, coluna ou célula pode permanecer atribuída exclusivamente
   ao grupo;
4. grupo não pode justificar preenchimento vazio externo;
5. ocupação visual final deve ser concretizada por `console`, `dashboard`
   ou `lancador`.

### DA-04 — Composição impossível

Quando uma configuração não permitir que toda a área do corpo pertença
visualmente a `console`, `dashboard` ou `lancador`, a composição é inválida.

O sistema deve:
- rejeitar explicitamente a composição;
- interromper construção ou renderização;
- emitir erro identificável;
- não inserir linhas ou áreas externas vazias;
- não aplicar distribuição implícita;
- não escolher silenciosamente um elemento;
- não alterar automaticamente o JSON;
- não usar fallback silencioso.

Detalhes técnicos que pertencem à implementação (não alteram a semântica):
- tipo nominal da exceção;
- função ou camada de detecção;
- estrutura interna da mensagem de erro;
- organização interna das validações.

---

## 5. Objetivo

Implementar DA-01 a DA-04 de forma que:

1. o corpo e seus containers estruturais nunca ocupem espaço visual próprio;
2. toda área física disponível do corpo pertença visualmente a `console`,
   `dashboard` ou `lancador`;
3. a tela `destino_minimo` não apresente faixa externa vazia;
4. a tela `grupo_minimo` não apresente faixa externa vazia;
5. configurações com múltiplos elementos sem `distribuicao` sejam rejeitadas
   explicitamente;
6. configurações com `distribuicao` explícita continuem renderizando
   corretamente, sem regressão;
7. grupos repassem integralmente sua área aos descendentes visuais;
8. composições impossíveis sejam rejeitadas com erro identificável.

---

## 6. Escopo positivo

O H-0033 autoriza:

- implementação de DA-01 a DA-04 no renderer;
- revisão de testes que verificam a presença de fill externo como
  comportamento esperado;
- criação de testes focais para cada decisão normativa;
- revisão e atualização (quando necessário) dos JSONs de telas inventariados;
- demonstração real em TTY com as dimensões obrigatórias;
- criação do relatório de implementação.

---

## 7. Escopo negativo

Os seguintes itens estão fora do escopo deste handoff:

- nova ADR;
- alteração de contratos;
- alteração de nomenclatura;
- mudança da lista de tipos visuais;
- novo modo de distribuição;
- transformação de grupo em elemento visual;
- escolha automática entre múltiplos elementos;
- fallback silencioso;
- alteração automática de JSON em runtime;
- cabeçalho com quebra ou reticências;
- outras revisões futuras do H-0030;
- responsividade do lançador (já tratada no H-0034);
- renumeração de handoffs;
- commit.

---

## 8. Separação de escopo: autor do handoff × futura implementação

O autor deste handoff criou exclusivamente:

```text
docs/handoff/H-0033-ocupacao-integral-corpo.md
```

Nenhum outro arquivo foi alterado pelo autor do handoff nesta etapa.

A restrição de criação de arquivo único vale somente para o **autor do
handoff**. O executor da futura implementação está autorizado — e onde
indicado, obrigado — a alterar todos os arquivos listados na seção 10.

---

## 9. Inventário completo dos JSONs de telas

### 9.1 Metodologia

O inventário cobriu:

1. todos os JSONs em `config/telas/` (rastreados);
2. JSONs com `schema: tela.v1` em outros diretórios;
3. JSONs referenciados por testes, demonstrações ou diagnóstico.

Verificação executada:

```bash
cd "$(git rev-parse --show-toplevel)"

# JSONs de configuração de telas rastreados
find config tela demo -name "*.json" | sort

# JSONs com schema tela.v1 fora de config/telas/
grep -rl '"schema": "tela.v1"' docs/ 2>/dev/null

# Referências em código
rg -n "config/telas|carregar_tela|construir_modelo" tela demo
```

O arquivo `docs/relatorios/anexos/orquestrador_stub_b_validacao.json`
contém `schema: tela.v1` mas possui `metadados.status: "draft"` e não é
referenciado por nenhum arquivo de código (`tela/`, `demo/`). É documento
conceptual de relatório, não configuração permanente de tela. Não incluído
no inventário operacional.

### 9.2 Tabela de inventário nominal

| Caminho | Identidade da tela | Uso | Estrutura do corpo | Distribuição atual | Avaliação inicial | Ação autorizada no H-0033 |
|---|---|---|---|---|---|---|
| `config/telas/demo/demo.json` | `demo` | Tela raiz da demonstração | vertical, 3 elementos: console_principal + dashboard_info + lancador_principal | `fracao: [2, 1, 2]` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/destino_minimo.json` | `destino_minimo` | Tela destino da navegação; caso A | sobreposto (alias vertical), 1 elemento: dashboard_teste (dashboard, título `Teste`) | `None` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/grupo_minimo.json` | `grupo_minimo` | Tela com grupo estrutural; caso B | vertical, 1 grupo: grupo_principal → dashboard_conteudo (dashboard, título `Conteudo`) | `None` (corpo e grupo) | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/stub_b.json` | `stub_b` | Fixture de stub para testes de navegação | sobreposto, 1 elemento: dashboard_teste (dashboard) | `None` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0029_dashboard_fracao.json` | `h0029_dashboard_fracao` | Fixture H-0029: dashboard com fracao[1] | vertical, 1 elemento: dashboard_fracao (dashboard) | `fracao: [1]` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0029_dashboard_igual.json` | `h0029_dashboard_igual` | Fixture H-0029: dashboard com igual | vertical, 1 elemento: dashboard_igual (dashboard) | `igual` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0029_dashboard_percentual.json` | `h0029_dashboard_percentual` | Fixture H-0029: dashboard com percentual[100] | vertical, 1 elemento: dashboard_percentual (dashboard) | `percentual: [100]` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0029_grupo_fracao.json` | `h0029_grupo_fracao` | Fixture H-0029: grupo com fracao[1] em dois níveis | vertical, 1 grupo: grupo_fracao (dist fracao[1]) → dashboard_grupo_fracao | `fracao: [1]` (corpo e grupo) | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0029_grupo_igual.json` | `h0029_grupo_igual` | Fixture H-0029: grupo com igual em dois níveis | vertical, 1 grupo: grupo_igual (dist igual) → dashboard_grupo_igual | `igual` (corpo e grupo) | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0029_grupo_percentual.json` | `h0029_grupo_percentual` | Fixture H-0029: grupo com percentual[100] em dois níveis | vertical, 1 grupo: grupo_percentual (dist percentual[100]) → dashboard_grupo_percentual | `percentual: [100]` (corpo e grupo) | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0029_grupo_pai_distribuido.json` | `h0029_grupo_pai_distribuido` | Fixture H-0029: grupo sem distribuição com corpo distribuído | vertical, 1 grupo: grupo_sem_dist (sem dist) → dashboard_interno | `fracao: [1]` (corpo); `None` (grupo) | POTENCIALMENTE_INCOMPATIVEL | REVISAR_E_ATUALIZAR_SE_INCOMPATIVEL |
| `config/telas/demo/h0030_console_unico.json` | `h0030_console_unico` | Catálogo H-0030: console único | vertical, 1 elemento: console_catalogo (console) | `igual` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0030_dashboard_unico.json` | `h0030_dashboard_unico` | Catálogo H-0030: dashboard único | vertical, 1 elemento: dashboard_catalogo (dashboard) | `igual` | COMPATIVEL | REVISAR_E_PRESERVAR |
| `config/telas/demo/h0030_matriz_2x2.json` | `h0030_matriz_2x2` | Catálogo H-0030: matriz 2×2 | vertical, 1 grupo: g_2x2 (sem dist, estrutura=matriz) → 4 dashboards | `igual` (corpo); `None`/matriz (grupo) | POTENCIALMENTE_INCOMPATIVEL | REVISAR_E_ATUALIZAR_SE_INCOMPATIVEL |
| `config/telas/demo/h0030_matriz_2x4.json` | `h0030_matriz_2x4` | Catálogo H-0030: matriz 2×4 | vertical, 1 grupo: g_2x4 (sem dist, estrutura=matriz) → 8 dashboards | `igual` (corpo); `None`/matriz (grupo) | POTENCIALMENTE_INCOMPATIVEL | REVISAR_E_ATUALIZAR_SE_INCOMPATIVEL |
| `config/telas/demo/h0030_matriz_3x2.json` | `h0030_matriz_3x2` | Catálogo H-0030: matriz 3×2 | vertical, 1 grupo: g_3x2 (sem dist, estrutura=matriz) → 6 dashboards | `igual` (corpo); `None`/matriz (grupo) | POTENCIALMENTE_INCOMPATIVEL | REVISAR_E_ATUALIZAR_SE_INCOMPATIVEL |

### 9.3 Justificativa por avaliação

**COMPATIVEL por DA-01** — `destino_minimo.json`, `grupo_minimo.json`,
`stub_b.json`:

Esses três arquivos têm `corpo.distribuicao: None` com único descendente
visual aplicável (ou único grupo contendo único descendente visual). O conteúdo
real dos JSONs não autoriza preenchimento externo vazio: a ausência de
`distribuicao` em cardinalidade unitária é declarativamente válida sob DA-01,
sem equivaler a `distribuicao: igual` e sem criar disputa entre múltiplos
elementos.

DA-01 determina que esse descendente visual ocupe integralmente a área
disponível. O comportamento incompatível pertence ao renderer atual, que aplica
o bloco de fill externo em `renderizar_tela` linhas 1693–1708 e insere linhas
físicas de largura total entre o último elemento visual e a `barra_de_menus`.
Portanto: compatibilidade do JSON ≠ conformidade do renderer atual.

A ação autorizada é `REVISAR_E_PRESERVAR`: o executor deve revisar nominalmente
cada arquivo, confirmar que permanece compatível após a correção do renderer e
não realizar alteração artificial se a estrutura continuar conforme DA-01 a
DA-04. Os testes que verificam o comportamento antigo (fill externo como
esperado) devem ser atualizados.

**POTENCIALMENTE_INCOMPATIVEL** — `h0029_grupo_pai_distribuido.json`,
`h0030_matriz_*`:

Esses arquivos têm `distribuicao` declarada no corpo (sem bloco de fill
externo na função principal). O grupo interno não tem distribuição própria
ou usa estrutura de matriz. O comportamento atual parece correto — o
elemento visual recebe a área via fill individual bordado, que é espaço
interno legítimo. Porém, a implementação de DA-01/DA-03 pode alterar o
caminho interno de propagação de área. O executor deve verificar se o
comportamento pós-implementação continua correto para essas fixtures; se
alguma apresentar regressão ou nova violação, deve ser atualizada.

**COMPATIVEL** — demais JSONs:

Esses arquivos têm `distribuicao` explícita no corpo. O bloco de fill
externo em `renderizar_tela` é ignorado quando `_corpo_vertical_distribuido
= True`. A área é alocada internamente via cotas. Nenhuma faixa externa
vazia é produzida. Devem ser revisados e nominalmente registrados como
preservados no relatório de implementação.

---

## 10. Arquivos autorizados para a futura implementação

### 10.1 Código

| Arquivo | Papel | Necessidade |
|---|---|---|
| `tela/renderizador.py` | Renderer — bloco de fill externo (linhas 1693–1708), DA-01 a DA-04 | OBRIGATÓRIO |
| `tela/modelo.py` | Modelo — validação estrutural se DA-02/DA-04 for implementada aqui | CONDICIONAL |
| `tela/loader.py` | Loader — validação de composição se DA-04 for implementada aqui | CONDICIONAL |

**Nota sobre o renderer:** O bloco de preenchimento externo identificado pela
ADR-0024 está em `tela/renderizador.py` linhas 1693–1708 (função
`renderizar_tela`). Este é o bloco que insere `"\n".join(" " * total_w for _
in range(l_corpo_fill))` quando `l_corpo_fill > 0 and arranjo_corpo !=
"horizontal" and not _corpo_vertical_distribuido`. Este bloco deve ser
substituído pela lógica de DA-01 a DA-04.

A localização exata da validação de DA-02/DA-04 (renderer, modelo ou loader) é
decisão técnica do executor — não altera a semântica normativa.

### 10.2 Testes automatizados

| Arquivo | Papel |
|---|---|
| `tela/teste_renderizador.py` | Testes do renderer — atualização de expectativas de destino_minimo/grupo_minimo/stub_b; novos testes focais DA-01 a DA-04 |
| `tela/teste_loader.py` | Testes do loader — se validação for implementada no loader |
| `tela/teste_modelo.py` | Testes do modelo — se validação for implementada no modelo |
| `demo/teste_demo.py` | Testes de demonstração e navegação — verificação de renderização correta pós-implementação |
| `demo/teste_diagnostico.py` | Testes do diagnóstico — smoke test do pipeline com telas afetadas |
| `demo/teste_explorar_barra_de_menus.py` | Testes de exploração de barra — regressão |

### 10.3 JSONs

Todos os 16 JSONs do inventário da seção 9.2 estão autorizados para revisão.
Para alteração estrutural, apenas os avaliados como
`POTENCIALMENTE_INCOMPATIVEL` quando a revisão confirmar incompatibilidade, ou
qualquer JSON que a revisão técnica demonstre violar DA-01 a DA-04. JSON
declarativamente compatível não deve receber alteração artificial.

Lista nominal completa:

```text
config/telas/demo/demo.json
config/telas/demo/destino_minimo.json
config/telas/demo/grupo_minimo.json
config/telas/demo/stub_b.json
config/telas/demo/h0029_dashboard_fracao.json
config/telas/demo/h0029_dashboard_igual.json
config/telas/demo/h0029_dashboard_percentual.json
config/telas/demo/h0029_grupo_fracao.json
config/telas/demo/h0029_grupo_igual.json
config/telas/demo/h0029_grupo_percentual.json
config/telas/demo/h0029_grupo_pai_distribuido.json
config/telas/demo/h0030_console_unico.json
config/telas/demo/h0030_dashboard_unico.json
config/telas/demo/h0030_matriz_2x2.json
config/telas/demo/h0030_matriz_2x4.json
config/telas/demo/h0030_matriz_3x2.json
```

### 10.4 Demonstração e fixtures

| Arquivo | Papel |
|---|---|
| `demo/demo.py` | Ponto de entrada real da demonstração interativa |
| `demo/diagnostico.py` | Diagnóstico executável — pipeline completo para tela específica |

### 10.5 Relatório

```text
docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
```

---

## 11. Arquivos preservados na futura implementação

Os arquivos abaixo **não podem ser alterados** durante a implementação do H-0033:

```text
docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0024.md
docs/relatorios/RELATORIO_QA_ADR-0024.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0024.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0024.md
docs/handoff/H-0033-ocupacao-integral-corpo.md
docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
```

Todos os relatórios de implementação e QA anteriores, todos os outros
handoffs, e o histórico Git não podem ser alterados.

---

## 12. Regra de implementação conjunta dos JSONs

Durante a futura implementação:

1. todos os 16 JSONs inventariados serão efetivamente revisados;
2. os classificados como `POTENCIALMENTE_INCOMPATIVEL`, e qualquer JSON que a
   revisão técnica demonstre violar DA-01 a DA-04, serão reavaliados com o
   código implementado — se incompatíveis confirmados, serão atualizados dentro
   do H-0033;
3. nenhum JSON incompatível ficará para ciclo futuro;
4. JSONs compatíveis não receberão alteração artificial;
5. cada JSON compatível será nominalmente registrado como revisado e
   preservado, com justificativa por arquivo no relatório;
6. não pode permanecer fixture histórica ativa reproduzindo preenchimento
   externo vazio como comportamento esperado;
7. alterações nos JSONs devem ser feitas somente quando necessárias para
   conformidade com DA-01 a DA-04;
8. não é permitida alteração automática ou silenciosa de JSON em runtime;
9. o H-0033 não apagará ou substituirá fixtures sem justificativa nominal.

---

## 13. Especificação por módulo

### 13.1 `tela/renderizador.py` — bloco de fill externo

**Localização:** linhas 1693–1708, função `renderizar_tela`.

**Comportamento atual (a eliminar):**

```python
l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
if l_corpo_fill > 0 and arranjo_corpo != "horizontal" and not _corpo_vertical_distribuido:
    partes.append(
        "\n".join(" " * total_w for _ in range(l_corpo_fill))
    )
```

Este bloco insere linhas físicas de largura total (`" " * total_w`) entre o
último elemento visual do corpo e a `barra_de_menus`. Viola ADR-0024.

**Comportamento esperado após implementação:**

- DA-01: se houver exatamente um descendente visual aplicável, ele recebe
  toda a área disponível (`l_corpo_disponivel`) — sem fill externo.
- DA-02: se houver múltiplos elementos disputando o mesmo eixo sem
  `distribuicao`, emitir erro identificável (DA-04).
- DA-03: área de grupo ou container estrutural é repassada integralmente
  aos descendentes visuais.
- DA-04: composições incapazes de satisfazer o invariante são rejeitadas
  explicitamente — sem fallback, sem distribuição implícita.

### 13.2 Propagação da `altura_disponivel`

Quando DA-01 é aplicado, o descendente visual único deve receber
`altura_disponivel = l_corpo_disponivel`. A propagação de `altura_disponivel`
para grupos e seus descendentes já existe em `_renderizar_container_vertical`
e `_renderizar_container_horizontal`. A implementação deve garantir que:

- o descendente visual único recebe o `altura_disponivel` completo;
- o preenchimento interno bordado (fill dentro da moldura do elemento)
  continua sendo o mecanismo legítimo para absorver a área;
- o bloco de fill externo na função principal (`renderizar_tela`) é removido.

### 13.3 Detecção de composição inválida (DA-02 e DA-04)

O ponto de detecção (renderer, modelo ou loader) é decisão do executor. O
comportamento de rejeição explícita é normativo:

- `RenderizadorErro` (ou equivalente já presente no sistema) com mensagem
  identificável que inclua o motivo da invalidade;
- sem fallback silencioso;
- sem distribuição implícita como modo de recuperação.

---

## 14. Casos obrigatórios

### Caso A — `destino_minimo`

**Identidade:**
- tela: `destino_minimo` (arquivo: `config/telas/demo/destino_minimo.json`)
- cabeçalho.título: `Destino Minimo`
- corpo.arranjo: `sobreposto` (alias transicional de `vertical`)
- corpo.distribuicao: `None`
- único elemento visual direto: `dashboard_teste` (tipo `dashboard`,
  título `Teste`)

**Resultado obrigatório:**
- DA-01 aplicado: dashboard ocupa integralmente a área disponível do corpo;
- nenhuma faixa externa vazia entre o dashboard e a `barra_de_menus`;
- espaço interno legítimo do dashboard continua permitido.

**Evidência anterior (estado atual violador):**

| Dimensão | Linhas do dashboard `Teste` | Linha da `barra_de_menus` | Linhas externas vazias |
|---|---|---|---|
| 42×20 | 3–5 | 17 | 6 a 16 (11 linhas) |
| 80×30 | 3–5 | 27 | 6 a 26 (21 linhas) |

### Caso B — `grupo_minimo`

**Identidade:**
- tela: `grupo_minimo` (arquivo: `config/telas/demo/grupo_minimo.json`)
- cabeçalho.título: `Grupo Minimo`
- corpo.arranjo: `vertical`
- corpo.distribuicao: `None`
- filho direto do corpo: `grupo_principal` (tipo `grupo`, arranjo `vertical`,
  sem `distribuicao`)
- filho do grupo: `dashboard_conteudo` (tipo `dashboard`, título `Conteudo`)
- **Não existe dashboard `TESTE` nesta tela.**

**Resultado obrigatório:**
- grupo permanece estrutural;
- DA-01 e DA-03 aplicados conjuntamente: área do grupo é integralmente
  repassada ao dashboard; dashboard ocupa integralmente essa área;
- nenhuma faixa externa vazia entre `dashboard_conteudo` e `barra_de_menus`.

### Caso C — Múltiplos elementos sem distribuição

O executor deve construir, dentro dos testes autorizados, ao menos uma fixture
inválida nominal que represente múltiplos elementos disputando o mesmo eixo
sem `distribuicao`.

**Resultado obrigatório:**
- composição rejeitada;
- erro identificável;
- nenhum modo `igual` implícito;
- nenhum preenchimento externo;
- nenhum fallback silencioso.

A fixture deve ser definida **como fixture inválida nominal** — não
transformar uma configuração permanente válida em inválida para o teste.

### Caso D — Múltiplos elementos com distribuição explícita

A tela `demo.json` (`id: demo`, cabeçalho `Orquestrador`,
`distribuicao: fracao[2,1,2]`, três elementos: console_principal +
dashboard_info + lancador_principal) é a fixture primária para este caso.
Outras fixtures H-0029 com distribuição explícita também se qualificam.

**Resultado obrigatório:**
- composição continua válida;
- distribuição declarada continua sendo respeitada;
- não há regressão para `igual`, `fracao` ou `percentual`;
- nenhuma sobra externa é criada.

### Caso E — Cardinalidade unitária em container aninhado

A tela `grupo_minimo.json` também cobre este caso (dashboard_conteudo dentro
de grupo_principal, que está dentro do corpo). Adicionalmente, as fixtures
H-0029 com grupo aninhado (`h0029_grupo_*`) cobrem variações.

**Resultado obrigatório:**
- a área atravessa o container estrutural (grupo);
- o descendente visual ocupa integralmente a cota;
- o container (grupo) não retém espaço próprio.

---

## 15. Critérios de aceite

**AC-01 — Ausência de linhas externas:**
Toda linha renderizada entre `cabecalho` e `barra_de_menus` pertence à moldura
de um elemento visual (`console`, `dashboard` ou `lancador`).

**AC-02 — Cobertura total por elementos visuais:**
O renderer não produz área vazia não coberta por nenhum dos três tipos.

**AC-03 — `destino_minimo` conforme:**
`destino_minimo` não apresenta área externa vazia entre o dashboard `Teste`
(`id: dashboard_teste`) e a `barra_de_menus`.

**AC-04 — `grupo_minimo` conforme:**
`grupo_minimo` não apresenta área externa vazia entre o dashboard `Conteudo`
(`id: dashboard_conteudo`) e a `barra_de_menus`.

**AC-05 — Identidades corretas confirmadas:**
Nenhum teste confunde `dashboard_teste` de `destino_minimo` com
`dashboard_conteudo` de `grupo_minimo`. Nenhuma menção a dashboard `TESTE`
em `grupo_minimo` está presente em testes ou expectativas.

**AC-06 — Código de saída zero não é prova suficiente:**
O aceite exige verificação da composição visual linha a linha.

**AC-07 — Verificação em múltiplas dimensões:**
Conformidade verificada em 42×20 e 80×30 no mínimo.

**AC-08 — Independência das expectativas:**
Testes materiais não usam a própria saída observada do comportamento antigo
como expectativa de referência.

**AC-09 — Descendente único ocupa integralmente a área:**
Prova que o elemento único preenche toda a área sem sobra externa.

**AC-10 — Múltiplos elementos sem distribuição são rejeitados:**
Composição inválida produz erro identificável; nenhum fallback ocorre.

**AC-11 — Múltiplos elementos com distribuição válida continuam funcionando:**
Sem regressão em telas com `distribuicao` explícita.

**AC-12 — Grupos não retêm espaço próprio:**
Toda área de grupo é repassada aos descendentes visuais.

**AC-13 — Composições impossíveis são rejeitadas explicitamente:**
Erro identificável; sem preenchimento externo, sem distribuição implícita.

**AC-14 — Ausência de fallback silencioso:**
Nenhum caminho do renderer produz área vazia não pertencente a elemento visual
sem emitir rejeição explícita.

**AC-15 — Inventário completo de JSONs:**
O relatório apresenta inventário nominal com classificação e justificativa por
arquivo. Nenhum JSON ficou sem classificação ou sem resultado registrado.

**AC-16 — Validação humana em TTY real:**
Ausência de faixas vazias externas confirmada por observação humana direta em
mais de uma dimensão de terminal.

---

## 16. Preservação do espaço interno dos elementos

### Proibido

- linha de largura total pertencente exclusivamente ao corpo (não a nenhum
  elemento visual);
- sobra de grupo ou container estrutural;
- célula sem elemento visual;
- faixa vazia entre o último elemento visual e a `barra_de_menus` causada
  pelo corpo.

### Permitido

- conteúdo vazio dentro da moldura do elemento;
- padding interno normativo (linha em branco entre borda e conteúdo);
- linhas internas de `console`, `dashboard` ou `lancador` — preenchimento
  bordado (`borda["v"] + " " * inner_w + borda["v"]`) dentro da moldura do
  elemento;
- bordas do elemento;
- espaços necessários à renderização interna.

**Os testes não podem reprovar espaço interno legítimo como se fosse
preenchimento externo.**

---

## 17. Testes obrigatórios

### 17.1 Testes focais (a criar ou atualizar em `tela/teste_renderizador.py`)

| Cobertura | Origem |
|---|---|
| DA-01: filho visual direto único ocupa área integralmente | novo |
| DA-01: filho visual aninhado (em grupo) ocupa área integralmente | novo |
| DA-02: múltiplos elementos no mesmo eixo sem `distribuicao` → erro | novo |
| DA-02: múltiplos elementos com `distribuicao` explícita → OK | existente; verificar regressão |
| DA-03: grupo repassa área ao descendente único | novo |
| DA-04: composição impossível → erro identificável, sem fallback | novo |
| Distinção espaço externo vs. espaço interno | novo |
| `destino_minimo` sem faixa externa | atualizar expectativa existente |
| `grupo_minimo` sem faixa externa | atualizar expectativa existente |
| `stub_b` sem faixa externa | atualizar expectativa existente |
| Todos os 16 JSONs inventariados: carregamento ou rejeição esperada | novo/atualizar |
| Dimensão 42×20 | novo/atualizar |
| Dimensão 80×30 | novo/atualizar |
| Redimensionamento determinístico | novo/atualizar |

**Testes a atualizar na suíte existente:**

- `TestCardinalidadeUnitariaH0029.test_integracao_json_grupo_minimo`
  (linha 5741): verifica `fill externo H-0015 presente` como comportamento
  esperado → deve ser alterado para verificar **ausência** de fill externo.
- `TestCardinalidadeUnitariaH0029.test_preservacao_jsons_sem_dist`
  (linha 5774): verifica `destino_minimo` e `stub_b` — expectativas sobre
  fill externo devem ser atualizadas para comportamento conforme DA-01.
- Quaisquer snapshots ou expectativas que incluam linhas `" " * 42` ou
  `" " * 80` externas como saída esperada de `destino_minimo`, `grupo_minimo`
  ou `stub_b`.

### 17.2 Suíte canônica vigente

Antes da implementação, executar e registrar a baseline:

```bash
cd "$(git rev-parse --show-toplevel)"

python tela/teste_renderizador.py
python tela/teste_loader.py
python tela/teste_modelo.py
python demo/teste_demo.py
python demo/teste_diagnostico.py
python demo/teste_explorar_barra_de_menus.py
```

Contagens registradas na data de criação deste handoff:

| Arquivo | Verificações | Estado |
|---|---|---|
| `tela/teste_renderizador.py` | 1065 | 1065 passaram, 0 falharam |
| `tela/teste_loader.py` | 283 | 283 passaram, 0 falharam |
| `tela/teste_modelo.py` | 163 | 163 passaram, 0 falharam |
| `demo/teste_demo.py` | 358 | 358 passaram, 0 falharam |
| `demo/teste_diagnostico.py` | 30 | 30 passaram, 0 falharam |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 38 passaram, 0 falharam |
| **Total** | **1937** | **1937 passaram, 0 falharam** |

A implementação não pode produzir regressão nessa suíte além das expectativas
que verificam comportamento antigo (fill externo) explicitamente substituído
por DA-01 a DA-04.

### 17.3 Independência das expectativas

É proibido:
- gerar o esperado a partir da própria saída observada do comportamento antigo;
- copiar a saída atual com fill externo e tratá-la como correta;
- usar apenas código de saída zero;
- considerar "não lançou exceção" prova suficiente.

Os valores esperados materiais devem ser derivados das autoridades, das
constantes da composição ou de cálculo geométrico independente.

### 17.4 Inventário como teste obrigatório

A implementação deve incluir verificação automatizada que compare:
- conjunto real de JSONs encontrados em `config/telas/demo/`;
- conjunto registrado no inventário do relatório de implementação.

Nenhum JSON de tela pode ficar sem classificação, sem resultado registrado ou
com incompatibilidade não resolvida.

---

## 18. Demonstração real

### 18.1 Ponto de entrada

```bash
cd "$(git rev-parse --show-toplevel)"
python demo/demo.py
```

A demo inicia com a tela `demo` (id: `demo`,
`config/telas/demo/demo.json`). A navegação usa chips do lançador.

### 18.2 Comandos exatos para abrir cada tela

**`destino_minimo`:**
```bash
python demo/demo.py
```
Na sessão interativa: pressionar o chip `d` ou a tecla `d`.

**`grupo_minimo`:**
```bash
python demo/demo.py
```
Na sessão interativa: pressionar o chip `g` ou a tecla `g`.

**Configuração válida com múltiplos elementos e distribuição (`demo.json`):**
```bash
# demo.py inicia diretamente nesta tela (tela raiz)
python demo/demo.py
# Nenhuma navegação necessária — tela inicial = demo.json
```

Em TTY real, as dimensões não são impostas por variáveis de ambiente. O ponto
de entrada consulta o tamanho real do terminal antes de usar qualquer fallback.

### 18.3 Diagnóstico não interativo para verificação do pipeline

Para verificação do pipeline sem TTY interativo (uso em testes ou inspeção):

```bash
cd "$(git rev-parse --show-toplevel)"

# Pipeline direto para tela específica:
python -c "
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela
for id_tela in ['destino_minimo', 'grupo_minimo']:
    t = carregar_tela(None, id_tela, 'config/telas/demo')
    m = construir_modelo(t)
    print('=== {} 42x20 ==='.format(id_tela))
    print(renderizar_tela(m, largura=42, altura=20))
    print('=== {} 80x30 ==='.format(id_tela))
    print(renderizar_tela(m, largura=80, altura=30))
"
```

### 18.4 Dimensões obrigatórias de prova

| Dimensão | Aplicação |
|---|---|
| 42×20 | Dimensão canônica mínima dos testes existentes |
| 80×30 | Dimensão ampla dos testes existentes |

Para validação humana em TTY real, o método reproduzível depende do tamanho
real do terminal:

**Cenário 42x20 (42×20):**
1. abrir um terminal real;
2. redimensionar fisicamente a área do terminal;
3. confirmar antes da execução:

```bash
stty size
```

A saída deve ser exatamente:

```text
20 42
```

4. executar a partir da raiz Git:

```bash
python demo/demo.py
```

5. usar o chip `d` ou a tecla `d` para `destino_minimo`;
6. repetir a partir da tela raiz usando o chip `g` ou a tecla `g` para
   `grupo_minimo`;
7. confirmar semanticamente a identidade da tela aberta.

**Cenário 80x30 (80×30):**
1. repetir o procedimento em terminal real;
2. confirmar antes da execução:

```bash
stty size
```

A saída deve ser exatamente:

```text
30 80
```

3. executar:

```bash
python demo/demo.py
```

4. repetir a navegação e a confirmação semântica para `destino_minimo` e
   `grupo_minimo`.

**Redimensionamento durante execução:**
1. iniciar em uma das dimensões confirmadas por `stty size`;
2. abrir a tela nominal;
3. redimensionar fisicamente o terminal;
4. confirmar que o tratamento existente de redimensionamento redesenha a tela;
5. verificar que nenhuma faixa externa vazia reaparece.

Para testes automatizados ou pseudo-TTY, manter a prova separada da validação
humana e usar somente mecanismo já existente ou comando cuja capacidade de
definir o tamanho da PTY tenha sido confirmada. Se o repositório não possuir
harness que imponha dimensões à PTY, a prova exata em TTY real depende do
redimensionamento físico confirmado por `stty size`.

Adicione outras dimensões quando necessário para cobrir:
- redimensionamento (variações intermediárias);
- arranjo horizontal (`demo.json` em terminais estreitos);
- grupos aninhados (h0029_*, grupo_minimo);
- limites mínimos (LARGURA_MINIMA_TELA = 10).

### 18.5 Identidades semânticas para confirmação

A demonstração e os smoke tests devem confirmar, conforme aplicável:

| Tela | Marcador esperado na renderização |
|---|---|
| `demo.json` | cabeçalho com `Orquestrador`; corpo vertical; `distribuicao` explícita em modo `fracao`; valores `[2, 1, 2]`; três elementos participantes |
| `destino_minimo.json` | cabeçalho com `Destino Minimo`; dashboard com título `Teste` |
| `grupo_minimo.json` | cabeçalho com `Grupo Minimo`; dashboard com título `Conteudo` (não `TESTE`) |

Marcador nominal de `demo.json`:

```yaml
tela:
  id: demo
  cabecalho_titulo: Orquestrador
```

Código de saída zero não prova que a tela correta foi aberta.

### 18.6 Necessidade de validação em TTY real

Esta é uma mudança visual e geométrica. O executor **não pode** declarar
aprovação visual em lugar do usuário. A seção 19 define os critérios de
validação manual que exigem TTY real.

---

## 19. Critérios de validação manual (TTY real)

O handoff exige validação humana em TTY real para os comportamentos visuais.

Critérios mínimos:

1. `destino_minimo` não apresenta faixa externa vazia;
2. `grupo_minimo` não apresenta faixa externa vazia;
3. o dashboard correto em `grupo_minimo` é `Conteudo` (não `TESTE`);
4. espaços internos legítimos continuam dentro das molduras dos elementos;
5. a `barra_de_menus` permanece posicionada corretamente;
6. o comportamento permanece correto em 42×20;
7. o comportamento permanece correto em 80×30;
8. o redimensionamento não recria preenchimento externo;
9. configurações válidas continuam renderizando sem erro;
10. configurações inválidas são rejeitadas com erro, não apresentadas
    silenciosamente.

A futura implementação deve registrar no relatório:

```yaml
validacao_manual:
  status: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
  dimensoes_validadas: []
  criterios_aprovados: []
  observacoes: ""
```

até o usuário informar o resultado. O executor não pode declarar aprovação
visual própria em lugar do usuário.

---

## 20. Relatório de implementação

O executor deve criar:

```text
docs/relatorios/IMP-0033-ocupacao-integral-corpo.md
```

Conteúdo mínimo (os campos abaixo não são exaustivos):

```yaml
handoff: H-0033
adr: ADR-0024
arquivos_alterados:
implementacao:
  DA_01:
  DA_02:
  DA_03:
  DA_04:
inventario_jsons:
  # Uma entrada por arquivo — todos os 16 do inventário
  config/telas/demo/demo.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/destino_minimo.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/grupo_minimo.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/stub_b.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0029_dashboard_fracao.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0029_dashboard_igual.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0029_dashboard_percentual.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0029_grupo_fracao.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0029_grupo_igual.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0029_grupo_percentual.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0029_grupo_pai_distribuido.json:
    avaliacao_inicial: POTENCIALMENTE_INCOMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0030_console_unico.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0030_dashboard_unico.json:
    avaliacao_inicial: COMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0030_matriz_2x2.json:
    avaliacao_inicial: POTENCIALMENTE_INCOMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0030_matriz_2x4.json:
    avaliacao_inicial: POTENCIALMENTE_INCOMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
  config/telas/demo/h0030_matriz_3x2.json:
    avaliacao_inicial: POTENCIALMENTE_INCOMPATIVEL
    avaliacao_pos_implementacao:
    acao_realizada:
    justificativa:
jsons_atualizados: []
jsons_revisados_e_preservados: []
jsons_invalidos_de_teste:
  # fixtures inválidas nominalmente definidas para Caso C
testes_focais:
suite_canonica:
  baseline_antes: 1937
  resultado_apos:
demonstracao_real:
identidades_confirmadas:
  demo:
    id: demo
    cabecalho_titulo: Orquestrador
    corpo_arranjo: vertical
    distribuicao:
      modo: fracao
      valores: [2, 1, 2]
      participantes: 3
dimensoes_testadas:
validacao_manual:
  status: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
  dimensoes_validadas: []
  criterios_aprovados: []
excecoes_operacionais_autorizadas: []
git:
bloqueios: []
```

O relatório **não pode** autoavaliar formalmente a implementação como aprovada.

---

## 21. Exceção operacional futura

> Se, durante a implementação, um arquivo fora da lista nominal desta seção 10
> for estritamente necessário para cumprir o handoff, preservar a suíte
> obrigatória ou evitar aborto desproporcional, o executor deve parar antes
> da alteração e pedir autorização explícita ao usuário. Deve informar o
> arquivo, o motivo, o escopo exato e a mudança esperada. A autorização não
> permite nova semântica, arquitetura ou política.

Uma autorização focal posterior não exige patch retroativo deste handoff
quando não houver decisão nova, mas deve ser registrada no relatório e
auditada pelo QA.

---

## 22. Condições de bloqueio

Pare com `ARCHITECTURE_REVIEW_REQUIRED` se encontrar:

- decisão normativa ausente para satisfazer DA-01 a DA-04;
- contradição entre a ADR-0024 e os contratos que impeça a implementação;
- necessidade de novo tipo visual;
- necessidade de política não coberta por DA-01 a DA-04;
- JSON cuja semântica exija decisão nova;
- impossibilidade de criar fixture inválida nominal para o Caso C sem
  alterar configuração permanente válida;
- impossibilidade de distinguir espaço interno de espaço externo no código.

---

## 23. Verificação de exequibilidade

Confirmações executadas antes de fechar este handoff:

1. **Todos os JSONs de telas foram inventariados:** 16 arquivos em
   `config/telas/demo/` confirmados; `docs/relatorios/anexos/orquestrador_stub_b_validacao.json`
   excluído por ser draft não referenciado por código. ✓

2. **Cada JSON aparece nominalmente nas permissões ou preservações:** 16
   arquivos listados na seção 10.3 e na tabela da seção 9.2. ✓

3. **JSONs incompatíveis confirmados podem ser atualizados no H-0033:** nenhum
   JSON declarativamente válido por DA-01 está classificado como
   `INCOMPATIVEL`; `destino_minimo`, `grupo_minimo` e `stub_b` são
   `COMPATIVEL + REVISAR_E_PRESERVAR`.
   Os `POTENCIALMENTE_INCOMPATIVEL` serão
   reavaliados com o código implementado e atualizados se a incompatibilidade do
   próprio JSON for confirmada. ✓

4. **Código, testes, demonstração e relatório possuem arquivos autorizados:**
   seção 10 lista nominalmente todos os arquivos. ✓

5. **Nenhum arquivo necessário está simultaneamente proibido:** os arquivos
   de código e teste autorizados (seção 10) não constam na lista de
   preservação (seção 11). ✓

6. **A suíte canônica pode ser atualizada e executada:** todos os arquivos de
   teste estão autorizados (seção 10.2); comandos exatos estão na seção 17.2. ✓

7. **`destino_minimo` e `grupo_minimo` podem ser demonstrados pelo ponto de
   entrada real:** `demo/demo.py` abre a tela raiz e a navegação por chip ou
   tecla `d`/`g` abre as telas nominais. As dimensões de TTY real são
   confirmadas por redimensionamento físico e `stty size`, conforme seção 18.4.
   ✓

8. **Existe prova para composição inválida:** Caso C — fixture inválida nominal
   a ser criada nos testes (seção 14). ✓

9. **Existe prova para composição válida com distribuição:** Caso D — `demo.json`
   e h0029_* com distribuição explícita. ✓

10. **Existe critério independente para detectar espaço externo:** ausência de
    linhas `" " * total_w` fora de molduras de elemento visual; verificação
    geométrica linha a linha (AC-01, AC-02). ✓

11. **O relatório pode registrar todo o inventário:** estrutura do relatório
    na seção 20 inclui entrada por arquivo para todos os 16 JSONs. ✓

12. **A validação humana em TTY real é reproduzível:** o procedimento exige
    redimensionamento físico do terminal, confirmação prévia por `stty size`
    com saída `20 42` ou `30 80`, execução do ponto de entrada real, sequência
    exata de entrada (`d`/`g`) e confirmação semântica da tela alvo. ✓

13. **Não existe decisão arquitetural pendente:** DA-01 a DA-04 estão
    completamente definidas; detalhes técnicos pertencem ao executor. ✓

14. **O escopo forma uma única capacidade coesa:** eliminar preenchimento
    externo vazio do corpo, implementar DA-01 a DA-04, verificar todos os
    JSONs existentes. ✓
