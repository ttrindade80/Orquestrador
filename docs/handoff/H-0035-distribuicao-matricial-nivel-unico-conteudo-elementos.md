---
name: H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos
description: Implementação da capacidade genérica distribuicao_matricial de nível único (ADR-0025) no loader, modelo e renderizador; interpretável por dashboard, console e lancador mediante adoção explícita; formação, ordem, dimensionamento, margens, vãos, distribuição, expansão, restos, alinhamento, fallback e determinismo; configurações permanentes de teste, demo dedicado e relatório de implementação
metadata:
  type: handoff_implementacao
  status: READY_FOR_IMPLEMENTATION
  id: H-0035
  data_criacao: 2026-07-16
rastreabilidade:
  adr_principal: docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
  adrs_relacionadas:
    - docs/adr/ADR-0001-menu-suporta-matriz.md
    - docs/adr/ADR-0002-menu-sobra-direita.md
    - docs/adr/ADR-0003-vaos-elasticos-menu.md
    - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
    - docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
    - docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
    - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
    - docs/adr/ADR-0023-largura-minima-funcional-lancador.md
    - docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
  contratos_aplicados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_json_dashboard.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_lancador.md
    - docs/contratos/contrato_json_lancador.md
  relatorios_autoridade:
    - docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
    - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
  handoffs_anteriores:
    - docs/handoff/H-0033-ocupacao-integral-corpo.md
    - docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
---

# H-0035 — Distribuição matricial configurável de nível único do conteúdo dos elementos

## 1. Identificação

Handoff de implementação: `H-0035`.

Título: `Distribuição matricial configurável de nível único do conteúdo dos elementos`.

Arquivo deste handoff:

```text
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Numeração confirmada por inspeção nominal de `docs/handoff/`: o maior número de
handoff efetivamente existente é `H-0034`. Não há `H-0035` ou superior. Este
ciclo cria efetivamente o `H-0035`. `H-0033` e `H-0034` não são reutilizados;
nenhuma lacuna histórica é preenchida; nenhuma cronologia é alterada.

Etapa futura autorizada por este documento: **implementação técnica** da ADR-0025
(capacidade genérica `distribuicao_matricial` de nível único) no loader, no
modelo, no renderizador, nos testes, nas configurações permanentes de
demonstração, no demo dedicado e no relatório de implementação.

Próxima categoria esperada após a criação deste handoff: `QA_HANDOFF`.

---

## 2. Status

```yaml
status: READY_FOR_IMPLEMENTATION
adr_base: aceita_e_aplicada
qa_da_adr: ADR_APPROVED_WITH_NOTES
qa_da_aplicacao: ADR_APPLICATION_APPROVED_WITH_NOTES
status_normalizado: APLICACAO_ADR_APROVADA_COM_OBSERVACOES
decisoes_ausentes: 0
contradicoes_documentais_ativas: 0
etapa_deste_documento: CRIAR_HANDOFF (concluída ao gravar este arquivo)
```

Este handoff não implementa código. Ele autoriza e delimita a implementação
futura.

---

## 3. Contexto e cronologia

### 3.1 Origem

A ADR-0025 (`aceita e aplicada`, 2026-07-16) define a capacidade genérica de
**distribuição matricial configurável de nível único** do conteúdo dos
elementos. A ADR fixou a semântica (formação, ordem, dimensionamento, margens,
vãos, distribuição do excedente, alinhamento, fallback, determinismo) e deixou
explicitamente para `APLICAR_ADR` a definição de nomes de campos, vocabulário
fechado e reconciliação com contratos específicos.

`APLICAR_ADR` (relatório `RELATORIO_APLICACAO_ADR-0025.md`) atualizou os
contratos, escolheu o nome do campo `distribuicao_matricial`, fechou o
vocabulário dos 26 caminhos declarativos e, no `PATCH_APLICACAO_ADR`, resolveu
três decisões complementares do usuário:

- **DEC-APP-0025-01** — `TRATAMENTO_INTERNO_DO_PARTICIPANTE` para `minimo_fixo`
  excedido (`contrato_json_dashboard.md` §9.2.1);
- **DEC-APP-0025-02** — `NOVA_CONFIGURACAO_TEM_PRECEDENCIA` no lançador
  (`contrato_lancador.md` §11.3; `contrato_json_lancador.md` §9.4);
- **DEC-APP-0025-03** — `NOVA_CONFIGURACAO_SUBSTITUI_POLITICAS_RELACIONADAS` no
  console (`contrato_json_console.md` §10.3).

O QA da aplicação normalizou o estado como
`APLICACAO_ADR_APROVADA_COM_OBSERVACOES`, com `0` decisões ausentes e `0`
contradições documentais ativas. A próxima categoria indicada foi
`CRIAR_HANDOFF`, executada por este documento.

### 3.2 Divergência histórica separada (H-0034)

O H-0034 tratou da distribuição responsiva do lançador (fila/matriz dirigida
por largura). Existe divergência registrada entre a disposição intencionada
(coluna vertical, eixo primário altura) e a implementação histórica (fila
horizontal dirigida por largura):

```yaml
disposicao_intencionada: coluna_vertical
eixo_primario_intencionado: altura
implementacao_historica: fila_horizontal_dirigida_por_largura
estado: FUTURA_NAO_BLOQUEANTE
```

**Esta implementação não corrige a divergência do H-0034.** Ela é ciclo
corretivo próprio e permanece separada (ver §33 e §36).

---

## 4. Objetivo

Implementar a capacidade genérica declarativa:

```text
distribuicao_matricial
```

para organizar, em **nível único**, os **participantes imediatos** do elemento
declarante, dentro da área útil já alocada a esse elemento.

A capacidade deve ser:

- **interpretada** por: loader (validação), modelo (representação),
  renderizador (cálculo geométrico e posicionamento);
- **usável explicitamente** por: `dashboard`, `console`, `lancador`.

A implementação deve incluir, como **uma única capacidade coesa**:

```text
configuração declarativa
        ↓
validação pelo loader
        ↓
representação no modelo
        ↓
interpretação pelo renderizador
        ↓
provas automatizadas
        ↓
configurações permanentes
        ↓
demo dedicado
```

Não dividir loader, modelo, renderer, testes e demo em handoffs independentes.
Não usar este handoff para corrigir capacidades não exigidas pela ADR-0025.

---

## 5. Autoridades (ler integralmente)

Base normativa:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
```

Preservação das políticas do lançador:

```text
docs/adr/ADR-0001-menu-suporta-matriz.md
docs/adr/ADR-0002-menu-sobra-direita.md
docs/adr/ADR-0003-vaos-elasticos-menu.md
docs/adr/ADR-0023-largura-minima-funcional-lancador.md
```

Composição e ocupação:

```text
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md
docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md
```

Demonstração e produto:

```text
docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md
docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
```

**Autoridade final** para nomes e semântica dos campos: `contrato_json_dashboard.md`
(§9.2 e §9.2.1), com remissões normativas de `contrato_json_console.md` (§10) e
`contrato_json_lancador.md` (§9) / `contrato_lancador.md` (§11).

Relatório histórico não é autoridade superior à ADR aplicada nem aos contratos
ativos.

---

## 6. Decisões fechadas (não reabrir)

| ID | Decisão | Autoridade |
|---|---|---|
| Nome do campo | `distribuicao_matricial` | `RELATORIO_APLICACAO_ADR-0025.md` §4.1 |
| Vocabulário completo dos 26 caminhos | fechado | `contrato_json_dashboard.md` §9.2 |
| `minimo_fixo` excedido | `TRATAMENTO_INTERNO_DO_PARTICIPANTE` (DEC-APP-0025-01) | `contrato_json_dashboard.md` §9.2.1 |
| Precedência no lançador | `NOVA_CONFIGURACAO_TEM_PRECEDENCIA` (DEC-APP-0025-02) | `contrato_lancador.md` §11.3; `contrato_json_lancador.md` §9.4 |
| Substituição no console | `NOVA_CONFIGURACAO_SUBSTITUI_POLITICAS_RELACIONADAS` (DEC-APP-0025-03) | `contrato_json_console.md` §10.3 |
| Fallback | estado canônico `quadro mínimo de terminal pequeno` (ADR-0017, ADR-0023); sem fallback concorrente | `NOMENCLATURA.md` §16.2; contratos JSON |

O executor não decide nenhum desses itens. Se a implementação exigir decidir
semântica não fechada, aplicar as condições de bloqueio (§34).

---

## 7. Base de caminhos

Raiz operacional = raiz Git do projeto. Todos os caminhos são relativos à raiz:

```text
config/
demo/
docs/
tela/
```

Não usar prefixo `scripts/`. Não prefixar caminhos com o nome do projeto. Não
misturar bases de caminhos.

---

## 8. Estado Git de referência

Estado observado no início deste ciclo `CRIAR_HANDOFF` (registrado apenas como
referência; **não** atribuível à criação do handoff):

```yaml
arquivos_rastreados_modificados: 8
arquivos_nao_rastreados: 6
stage: vazio
git_diff_cached: vazio
```

Rastreados modificados (ciclo documental ADR-0025):

```text
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_tela_json.md
```

Não rastreados (ciclo documental ADR-0025):

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
docs/relatorios/RELATORIO_QA_ADR-0025.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
```

Instrução para a futura implementação: **não** remover, restaurar, adicionar ao
stage nem commitar esses arquivos preexistentes; eles pertencem ao ciclo
documental da ADR-0025 e não a este ciclo de implementação.

---

## 9. Separação entre escopo do autor e escopo da implementação

### 9.1 Arquivo alterável pelo autor deste handoff (etapa `CRIAR_HANDOFF`)

Durante `CRIAR_HANDOFF`, o autor pôde alterar **somente**:

```text
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Essa limitação vale apenas para a etapa `CRIAR_HANDOFF`. **Ela não é limitação
da futura implementação.**

### 9.2 Escopo da futura implementação

A futura implementação está autorizada a alterar/criar os arquivos nominais
listados em §22 e §23, e somente esses.

---

## 10. Inventário técnico confirmado (código real)

Inspeção realizada em `tela/` e `demo/`. Símbolos confirmados:

**`tela/loader.py`** (validação de configurações): `carregar_tela`,
`_validar_distribuicao_corpo`, `_validar_grupo`, `_validar_matriz_grupo`,
`_validar_quantidade_matriz`, `_validar_distribuicao_matriz`,
`_validar_celulas_matriz`, `_eh_numero_nao_bool`, classes de erro `TelaErro`,
`TelaEstruturaInvalida`, `TelaTipoDesconhecido`, etc.

**`tela/modelo.py`** (modelo interno): `construir_modelo`,
`_construir_elementos_recursivo`, classes `ModeloTela`, `Corpo`,
`ElementoCorpo`, `ModeloTelaErro`.

**`tela/renderizador.py`** (renderização — superfícies geométricas
equivalentes): `renderizar_tela` (ponto público), `_renderizar_container`,
`_renderizar_container_vertical`, `_renderizar_container_horizontal`,
`_renderizar_container_matriz`, `_montar_corpo_horizontal`,
`_caixa_de_elemento`, `_linhas_console`, `_linhas_dashboard`,
`_linhas_lancador`, `_distribuir_alturas`, `_distribuir_larguras`,
`_pesos_distribuicao`, `_quadro_minimo_global`, sinal global
`_quadro_minimo_lancador_ativo`, classe `RenderizadorErro`.

**Testes existentes**: `tela/teste_loader.py`, `tela/teste_modelo.py`,
`tela/teste_renderizador.py`, `demo/teste_demo.py`, `demo/teste_diagnostico.py`,
`demo/teste_explorar_barra_de_menus.py`.

**Demo e diagnóstico**: `demo/demo.py` (ponto de entrada TTY do demo principal;
raiz `_RAIZ_TELAS_DEMO = config/telas/demo`, tela raiz `"demo"`, navegação por
itens de `lancador` `chip → tela_destino`, redimensionamento por `SIGWINCH`,
saída por comando/tecla), `demo/diagnostico.py`
(`gerar_diagnostico_tela(id_tela="demo")` encadeia
`carregar_tela → construir_modelo → renderizar_tela`).

**Configurações permanentes**: `config/telas/demo/*.json` (telas de demo, ex.:
`demo.json`, `destino_minimo.json`, `grupo_minimo.json`, família `h0029_*`,
família `h0030_*`), `config/elementos/*.json` (`barra_de_menus.json`,
`cabecalho.json`, `lancador.json` — transicional), `config/layouts/*.json`.

**Convenção de relatório de implementação**: `docs/relatorios/IMP-<NNNN>-<slug>.md`
(ex.: `IMP-0033-...`, `IMP-0034-...`).

**Convenção de nomes de tela de demo**: prefixo por ciclo (`h0029_*`, `h0030_*`).
Este ciclo usa o prefixo **`h0035_`**.

Regra vinculante: no restante deste handoff, somente caminhos confirmados são
usados como permissão; nenhum curinga; cada arquivo existente autorizado e cada
novo arquivo são listados nominalmente (§22, §23). Se durante a implementação
um caminho necessário não puder ser determinado, **parar com bloqueio** em vez
de inventá-lo (§34).

---

## 11. Escopo positivo (o que implementar)

Implementar a capacidade `distribuicao_matricial` cobrindo integralmente:

1. validação declarativa (loader) dos 26 caminhos;
2. representação fiel no modelo (sem defaults estruturais novos);
3. cálculo geométrico determinístico centralizado (renderer);
4. formação, ordem, dimensionamento, margens, vãos, distribuição horizontal e
   vertical, ordem de expansão, restos inteiros, alinhamento interno;
5. tratamento de `minimo_fixo` excedido (DEC-APP-0025-01);
6. fallback canônico e recuperação determinística;
7. preservação de compatibilidade (ausência do campo → comportamento anterior);
8. adoção explícita por `dashboard`, `console` e `lancador`, com precedência
   (DEC-APP-0025-02) e substituição (DEC-APP-0025-03);
9. testes automatizados em todas as camadas;
10. configurações permanentes de demonstração (famílias mínimas de §26);
11. demo dedicado à distribuição de conteúdo;
12. relatório de implementação.

---

## 12. Estrutura declarativa e local contratual

Local contratual do campo:

```text
corpo.elementos[] > elemento funcional (dashboard | console | lancador) > distribuicao_matricial
```

A adoção é sempre **explícita**. A ausência de `distribuicao_matricial` preserva
integralmente o comportamento anterior do elemento.

Campos desconhecidos dentro de `distribuicao_matricial` são **rejeitados por
validação controlada** (erro de domínio). Não há defaults implícitos: todos os
campos marcados como obrigatórios ("sempre") devem estar presentes quando
`distribuicao_matricial` está presente.

---

## 13. Os 26 caminhos normativos

Fonte normativa: `contrato_json_dashboard.md` §9.2 (vocabulário) e §9.2.1
(tratamento de `minimo_fixo`). `contrato_json_console.md` §10.2 e
`contrato_json_lancador.md` §9.2 remetem a esse vocabulário sem exceção.

A tabela abaixo reproduz os 26 caminhos, de `formacao.politica` até
`alinhamento_interno.vertical`. O executor deve verificar, por este handoff, que
cada caminho aplicável foi contemplado no loader, no modelo e no renderer.

| # | Caminho | Tipo | Valores fechados | Obrigatoriedade | Dependências / restrições cruzadas | Mín. | Máx. | Combinações inválidas |
|---|---|---|---|---|---|---|---|---|
| 1 | `formacao.politica` | string | `preferencia_linhas`, `preferencia_colunas`, `matriz_fixa` | sempre | governa validade dos campos `linhas`/`colunas` | — | — | valor fora do vocabulário |
| 2 | `formacao.linhas.minimo` | int | inteiro ≥ 1 | opcional | só para políticas responsivas (`preferencia_*`) | 1 | — | presente com `politica == matriz_fixa`; < 1 |
| 3 | `formacao.linhas.maximo` | int | inteiro ≥ `minimo` | opcional | só responsivas; exige coerência com `minimo` | `linhas.minimo` | — | `maximo < minimo`; presente com `matriz_fixa` |
| 4 | `formacao.linhas.fixo` | int | inteiro ≥ 1 | obrigatório sse `politica == matriz_fixa` | inválido nas demais políticas | 1 | — | presente com `preferencia_*`; ausente com `matriz_fixa`; < 1 |
| 5 | `formacao.colunas.minimo` | int | inteiro ≥ 1 | opcional | só responsivas | 1 | — | presente com `matriz_fixa`; < 1 |
| 6 | `formacao.colunas.maximo` | int | inteiro ≥ `minimo` | opcional | só responsivas; coerência com `minimo` | `colunas.minimo` | — | `maximo < minimo`; presente com `matriz_fixa` |
| 7 | `formacao.colunas.fixo` | int | inteiro ≥ 1 | obrigatório sse `politica == matriz_fixa` | inválido nas demais | 1 | — | presente com `preferencia_*`; ausente com `matriz_fixa`; < 1 |
| 8 | `ordem` | string | `por_linha`, `por_coluna` | sempre | independente da formação | — | — | valor fora do vocabulário |
| 9 | `dimensionamento.colunas.politica` | string | `maior_da_coluna`, `uniforme`, `minimo_fixo` | sempre | `minimo_fixo` exige campo 10 | — | — | valor fora do vocabulário |
| 10 | `dimensionamento.colunas.minimo` | int | inteiro ≥ 0 | obrigatório sse coluna `politica == minimo_fixo` | dependente do campo 9 | 0 | — | presente sem `minimo_fixo`; ausente com `minimo_fixo`; < 0 |
| 11 | `dimensionamento.linhas.politica` | string | `maior_da_linha`, `uniforme`, `minimo_fixo` | sempre | `minimo_fixo` exige campo 12 | — | — | valor fora do vocabulário |
| 12 | `dimensionamento.linhas.minimo` | int | inteiro ≥ 0 | obrigatório sse linha `politica == minimo_fixo` | dependente do campo 11 | 0 | — | presente sem `minimo_fixo`; ausente com `minimo_fixo`; < 0 |
| 13 | `espacamento.margem_superior` | `{minimo, maximo?}` | int ≥ 0 | sempre | `maximo ≥ minimo` quando presente | 0 | opcional | `maximo < minimo`; `minimo < 0` |
| 14 | `espacamento.margem_inferior` | `{minimo, maximo?}` | int ≥ 0 | sempre | `maximo ≥ minimo` quando presente | 0 | opcional | `maximo < minimo`; `minimo < 0` |
| 15 | `espacamento.margem_esquerda` | `{minimo, maximo?}` | int ≥ 0 | sempre | `maximo ≥ minimo` quando presente | 0 | opcional | `maximo < minimo`; `minimo < 0` |
| 16 | `espacamento.margem_direita` | `{minimo, maximo?}` | int ≥ 0 | sempre | `maximo ≥ minimo` quando presente | 0 | opcional | `maximo < minimo`; `minimo < 0` |
| 17 | `espacamento.vao_horizontal` | `{minimo, maximo?}` | int ≥ 0 | sempre | `maximo ≥ minimo` quando presente | 0 | opcional | `maximo < minimo`; `minimo < 0` |
| 18 | `espacamento.vao_vertical` | `{minimo, maximo?}` | int ≥ 0 | sempre | `maximo ≥ minimo` quando presente | 0 | opcional | `maximo < minimo`; `minimo < 0` |
| 19 | `distribuicao_horizontal.politica` | string | `inicio`, `centro`, `fim`, `entre_participantes`, `uniforme`, `margens_limitadas` | sempre | independente do eixo vertical | — | — | valor fora do vocabulário |
| 20 | `distribuicao_vertical.politica` | string | `inicio`, `centro`, `fim`, `entre_linhas`, `uniforme`, `margens_limitadas` | sempre | independente do eixo horizontal | — | — | valor fora do vocabulário |
| 21 | `ordem_expansao.horizontal` | string | `margens_primeiro_depois_vaos`, `uniforme_margens_e_vaos`, `vaos_primeiro_depois_margens` | sempre | independente do eixo vertical | — | — | valor fora do vocabulário |
| 22 | `ordem_expansao.vertical` | string | `margens_primeiro_depois_vaos`, `uniforme_margens_e_vaos`, `vaos_primeiro_depois_margens` | sempre | independente do eixo horizontal | — | — | valor fora do vocabulário |
| 23 | `politica_resto.horizontal` | string | `ao_primeiro`, `ao_ultimo` | sempre | — | — | — | valor fora do vocabulário |
| 24 | `politica_resto.vertical` | string | `ao_primeiro`, `ao_ultimo` | sempre | — | — | — | valor fora do vocabulário |
| 25 | `alinhamento_interno.horizontal` | string | `inicio`, `centro`, `fim` | sempre | atua dentro da célula; independente da distribuição global | — | — | valor fora do vocabulário |
| 26 | `alinhamento_interno.vertical` | string | `topo`, `centro`, `base` | sempre | atua dentro da célula; independente da distribuição global | — | — | valor fora do vocabulário |

Observações normativas herdadas dos contratos:

- **`matriz_fixa`**: exige `formacao.linhas.fixo` e `formacao.colunas.fixo`;
  `minimo`/`maximo` de linhas e colunas são inválidos nessa política.
- **`minimo_fixo`** (campos 9–12): sempre acompanhado do `minimo` correspondente
  (campos 10/12). Comportamento quando participante excede: §17 (DEC-APP-0025-01).
- **`{minimo, maximo?}`**: `minimo` inteiro não negativo obrigatório; `maximo`
  opcional; quando presente, `maximo ≥ minimo`. Mínimos são invioláveis; máximos
  são invioláveis quando declarados.

A autoridade final para nomes e semântica permanece
`contrato_json_dashboard.md`. Se a implementação identificar caminho aplicável
não contemplado por esta tabela, tratar como divergência e **parar com bloqueio**
(§34).

---

## 14. Nível único (escopo exclusivo)

A implementação organiza **somente os participantes imediatos** do elemento
declarante. É **proibido**:

- percorrer descendentes para reorganizá-los;
- achatar níveis;
- criar recursão, herança ou cascata;
- propagar configuração a filhos;
- misturar margens ou vãos de níveis distintos;
- propagar fallback entre níveis;
- definir semântica multinível.

Um participante é uma **unidade** perante a matriz externa. Sua organização
interna pertence ao próprio participante e aos contratos aplicáveis
(ADR-0025 §7 e §8; `contrato_composicao_corpo.md` §11.1).

---

## 15. Formação

Suporte obrigatório aos literais exatos: `preferencia_linhas`,
`preferencia_colunas`, `matriz_fixa`.

A formação deve: respeitar mínimos/máximos; respeitar linhas/colunas declaradas;
respeitar mínimos geométricos; usar critérios completos de desempate; ser
determinística; rejeitar combinação declarativa inválida; acionar o quadro
mínimo quando nenhuma formação permitida couber.

- **Preferência por linhas**: prioriza a ocupação no sentido definido
  contratualmente para linhas (ADR-0025 §15; contrato). Reproduzir a semântica
  do contrato; não inventar algoritmo alternativo.
- **Preferência por colunas**: prioriza a ocupação no sentido definido
  contratualmente para colunas.
- **Matriz fixa**: a quantidade declarada de `linhas.fixo`/`colunas.fixo` não
  pode ser reduzida, aumentada ou reorganizada silenciosamente para forçar
  encaixe. Se não couber respeitando todos os mínimos, ocorre o fallback (§21).

---

## 16. Ordem de preenchimento e dimensionamento

### 16.1 Ordem

Literais: `por_linha`, `por_coluna`. A sequência original dos participantes é
**preservada**; a política altera apenas a célula ocupada por cada posição. São
proibidos: reordenação semântica, perda, duplicação, preenchimento parcial e
seleção silenciosa de subconjunto.

### 16.2 Dimensionamento

Colunas: `maior_da_coluna`, `uniforme`, `minimo_fixo`.
Linhas: `maior_da_linha`, `uniforme`, `minimo_fixo`.

Literais exatos do contrato. `minimo_fixo` sempre com o campo `minimo`
associado.

---

## 17. `minimo_fixo` excedido — `TRATAMENTO_INTERNO_DO_PARTICIPANTE`

Decisão fechada DEC-APP-0025-01 (`contrato_json_dashboard.md` §9.2.1). Quando um
participante exigir dimensão superior à área externa calculada sob `minimo_fixo`:

- a linha/coluna externa **não cresce automaticamente** por essa exigência
  interna;
- a formação externa **não é invalidada** apenas por essa exigência;
- o participante **recebe a área calculada** e **trata seu conteúdo
  internamente**;
- o renderer externo **não reorganiza descendentes**;
- o renderer externo **não introduz** truncamento, quebra, rolagem ou paginação;
- o renderer externo **não propaga fallback interno**;
- os mínimos externos permanecem invioláveis.

A área externa ainda pode receber excedente pela própria política de distribuição
(`distribuicao_*`, `ordem_expansao`); essa ampliação decorre da distribuição
externa, não da exigência interna.

Testes obrigatórios devem provar: ausência de crescimento externo; ausência de
invalidação externa; área exata entregue ao participante; ausência de
reorganização dos descendentes; ausência de política interna inventada pelo
distribuidor externo.

---

## 18. Margens, vãos e distribuição

### 18.1 Margens e vãos (independentes)

Suporte independente a: `margem_superior`, `margem_inferior`, `margem_esquerda`,
`margem_direita`, `vao_horizontal`, `vao_vertical`. Para cada medida: mínimo
inteiro não negativo; máximo opcional; `maximo ≥ minimo`; mínimo inviolável;
máximo inviolável quando declarado. Nenhuma medida é inferida de outra sem regra
expressa.

### 18.2 Distribuição horizontal

Literais: `inicio`, `centro`, `fim`, `entre_participantes`, `uniforme`,
`margens_limitadas`. Diferenciar: posição global da matriz; margens da matriz;
vãos internos; alinhamento do participante dentro da célula. Centralizar a
matriz **não** implica centralizar cada participante na sua célula.

### 18.3 Distribuição vertical

Literais: `inicio`, `centro`, `fim`, `entre_linhas`, `uniforme`,
`margens_limitadas`. A política vertical **não** é derivada implicitamente da
horizontal (eixos independentes — ADR-0025 §17).

### 18.4 Ordem de expansão

Literais: `margens_primeiro_depois_vaos`, `uniforme_margens_e_vaos`,
`vaos_primeiro_depois_margens`. Sequência: (1) aplicar mínimos; (2) calcular
sobra; (3) distribuir sobra na ordem declarada; (4) respeitar máximos; (5)
encaminhar sobra restante conforme a política; (6) distribuir restos inteiros
deterministicamente. Não criar ordem de expansão global não declarada.

### 18.5 Restos inteiros (`politica_resto`)

Literais: `ao_primeiro`, `ao_ultimo` (horizontal e vertical). Cobrir: resto
horizontal e vertical; uma linha; uma coluna; um participante; múltiplos
participantes; ausência de divisão por zero; ordem determinística de entrega das
unidades residuais. O valor esperado dos testes é calculado **independentemente**
da saída observada.

### 18.6 Alinhamento interno

Horizontal: `inicio`, `centro`, `fim`. Vertical: `topo`, `centro`, `base`. Atua
**dentro da célula**; não substitui a distribuição global da matriz. Regra
determinística para resto ímpar em centralização (documentar).

---

## 19. Área útil

Todos os cálculos ocorrem dentro da área útil já entregue ao conteúdo do
elemento. Preservar: bordas, cabeçalhos, títulos, barras, padding estrutural,
ocupação integral do corpo (ADR-0024), distinção entre espaço interno e
preenchimento externo indevido. A implementação **não reabre nem redefine** a
composição estrutural do corpo (ADR-0015, ADR-0024). As margens desta capacidade
são internas e distintas do preenchimento externo proibido pela ADR-0024.

---

## 20. Sequência conceitual do cálculo (ordem normativa)

1. obter a área útil;
2. obter os participantes imediatos;
3. validar a configuração;
4. obter requisitos mínimos;
5. construir as formações permitidas;
6. calcular a geometria mínima;
7. descartar formações inválidas;
8. selecionar a formação válida por desempate determinístico;
9. aplicar mínimos;
10. calcular sobra horizontal;
11. calcular sobra vertical;
12. aplicar ordem de expansão;
13. respeitar máximos;
14. distribuir restos;
15. calcular células;
16. alinhar participantes nas células;
17. renderizar todos os participantes;
18. acionar fallback quando necessário.

Uma etapa posterior **não pode** reparar silenciosamente violação produzida por
etapa anterior. A validação (etapa 3) ocorre **antes de qualquer efeito
observável**: não pode haver renderização parcial antes do erro.

---

## 21. Fallback e recuperação

Quando nenhuma formação válida comportar todos os participantes, todos os
mínimos, todas as margens obrigatórias, todos os vãos obrigatórios e as
dimensões obrigatórias, o resultado é o estado canônico:

```text
quadro mínimo de terminal pequeno
```

A condição pode ser descrita como "terminal muito pequeno", mas **não** existe
um segundo fallback concorrente. No fallback são **proibidos**: paginação
automática, ocultação, truncamento do conjunto, perda, duplicação, sobreposição,
coordenadas negativas, redução silenciosa dos mínimos, alteração automática do
JSON, renderização parcial, seleção de subconjunto.

**Recuperação**: quando a área voltar a ser suficiente, o fallback é removido, a
distribuição é reconstruída, o resultado é determinístico e nenhum estado
residual permanece. Reutilizar o mecanismo canônico global já existente
(`_quadro_minimo_global` / sinal global do renderer); **não** criar fallback
local concorrente (ADR-0023, ADR-0017).

---

## 22. Arquivos existentes autorizados a alterar

Somente os seguintes arquivos existentes podem ser alterados pela implementação:

| Arquivo | Papel na implementação |
|---|---|
| `tela/loader.py` | Validação declarativa de `distribuicao_matricial` (26 caminhos, tipos, literais, limites, dependências, combinações inválidas, campos desconhecidos), com erro de domínio material |
| `tela/modelo.py` | Representação fiel dos 26 caminhos no modelo; ausência sem default estrutural; sem I/O; sem lógica geométrica |
| `tela/renderizador.py` | Interpretação geométrica; chamada ao motor centralizado; integração com `renderizar_tela`, `_caixa_de_elemento`, `_linhas_console`, `_linhas_dashboard`, `_linhas_lancador`, `_quadro_minimo_global`; adaptações de fronteira por consumidor |
| `tela/teste_loader.py` | Testes de validação do loader |
| `tela/teste_modelo.py` | Testes de representação no modelo |
| `tela/teste_renderizador.py` | Testes de integração do renderer com os três consumidores e regressão das telas existentes |
| `demo/teste_diagnostico.py` | Testes de diagnóstico das novas telas (pipeline `carregar → construir → renderizar`) via `gerar_diagnostico_tela(id)` |

Nenhum outro arquivo existente pode ser alterado. Em particular, **não** alterar
`demo/demo.py`, `demo/teste_demo.py`, `demo/diagnostico.py`,
`demo/explorar_barra_de_menus.py`, `config/elementos/lancador.json`, nem
qualquer JSON de tela preexistente (ver §24).

---

## 23. Novos arquivos autorizados a criar

### 23.1 Código

| Arquivo | Papel |
|---|---|
| `tela/distribuicao_matricial.py` | Motor geométrico **centralizado** da capacidade: enumeração de formações, seleção determinística, aplicação de mínimos, sobra, ordem de expansão, máximos, restos, células, alinhamento. Sem I/O. Reutilizado pelos três consumidores no renderer |
| `tela/teste_distribuicao_matricial.py` | Testes do motor geométrico (unitários, expectativas independentes, geometria fechada) |

Observação de arquitetura: `tela/distribuicao_matricial.py` é o **ponto central**
recomendado para o cálculo, evitando versões independentes e divergentes por
consumidor. O executor deve, antes de codificar, inventariar as superfícies
equivalentes de renderização (§28) e confirmar que todas reutilizam uma única
semântica. Se o inventário indicar ponto central diferente já existente no
renderer, o executor deve justificar a escolha no relatório; em nenhum caso pode
duplicar o algoritmo.

### 23.2 Demo dedicado

| Arquivo | Papel |
|---|---|
| `demo/demo_distribuicao.py` | Demo dedicado à distribuição de conteúdo (separado do demo principal) |
| `demo/teste_demo_distribuicao.py` | Testes do demo dedicado (catálogo, seleção, identidade semântica, smoke, pseudo-TTY, quadro mínimo, recuperação) |

### 23.3 Configurações JSON permanentes (prefixo `h0035_`)

Todas em `config/telas/demo/`, nominais, sem colisão com telas existentes:

| Arquivo | Consumidor | Cobre família(s) de §26 |
|---|---|---|
| `config/telas/demo/h0035_pref_linhas.json` | dashboard | 1, 19 (se 1 linha), ordem por linha |
| `config/telas/demo/h0035_pref_colunas.json` | dashboard | 2, ordem por coluna |
| `config/telas/demo/h0035_matriz_fixa_cabe.json` | dashboard | 3, 14 |
| `config/telas/demo/h0035_matriz_fixa_quadro_minimo.json` | dashboard | 15, 16 (recuperação por redimensionamento) |
| `config/telas/demo/h0035_centralizado_h_colunas.json` | dashboard | 4 |
| `config/telas/demo/h0035_esquerda_margens_min_max.json` | dashboard | 5 |
| `config/telas/demo/h0035_h_uniforme.json` | dashboard | 6 |
| `config/telas/demo/h0035_h_margens_limitadas.json` | dashboard | 7 |
| `config/telas/demo/h0035_v_margens_min.json` | dashboard | 8 |
| `config/telas/demo/h0035_v_margens_min_max.json` | dashboard | 9 |
| `config/telas/demo/h0035_v_uniforme.json` | dashboard | 10 |
| `config/telas/demo/h0035_um_centralizado.json` | dashboard | 11, 18 |
| `config/telas/demo/h0035_tres_centralizados.json` | dashboard | 12 |
| `config/telas/demo/h0035_quatro_centralizados.json` | dashboard | 13 |
| `config/telas/demo/h0035_minimo_fixo_excedido.json` | dashboard | 17 |
| `config/telas/demo/h0035_uma_linha.json` | dashboard | 19 |
| `config/telas/demo/h0035_uma_coluna.json` | dashboard | 20 |
| `config/telas/demo/h0035_resto_horizontal.json` | dashboard | 21 |
| `config/telas/demo/h0035_resto_vertical.json` | dashboard | 22 |
| `config/telas/demo/h0035_console_com.json` | console | 23 |
| `config/telas/demo/h0035_console_sem.json` | console | 24 |
| `config/telas/demo/h0035_lancador_com.json` | lancador | 25 |
| `config/telas/demo/h0035_lancador_sem.json` | lancador | 26 |
| `config/telas/demo/h0035_dashboard_com.json` | dashboard | 27 |
| `config/telas/demo/h0035_dashboard_sem.json` | dashboard | 28 |
| `config/telas/demo/h0035_catalogo.json` | tela raiz do demo dedicado (lancador de navegação para as telas acima) | — |

Uma configuração pode provar mais de uma família desde que a identidade
semântica seja clara e o relatório indique exatamente quais propriedades cada
uma prova. Todas as 28 famílias de §26 devem permanecer cobertas. Se a
implementação precisar de um JSON adicional não listado, **parar e pedir
autorização** (§30) — nenhum JSON fora desta lista pode ser criado
silenciosamente.

### 23.4 Relatório de implementação

| Arquivo | Papel |
|---|---|
| `docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md` | Relatório de implementação (estrutura em §35) |

---

## 24. Arquivos preservados na futura implementação

Preservar nominalmente (não alterar):

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_json_lancador.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0025.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0025.md
```

Preservar também:

- **JSON produtivo principal do lançador** (`config/elementos/lancador.json` e
  qualquer tela produtiva do lançador): não adicionar `distribuicao_matricial`,
  não migrar, não reescrever snapshots (§33). Regra preferencial: **não alterar**
  o JSON produtivo do lançador neste ciclo;
- `config/telas/demo/demo.json` e demais telas de demo preexistentes
  (`destino_minimo.json`, `grupo_minimo.json`, `h0029_*`, `h0030_*`, `stub_b.json`);
- `demo/demo.py`, `demo/teste_demo.py`, `demo/diagnostico.py`,
  `demo/explorar_barra_de_menus.py`, `demo/teste_explorar_barra_de_menus.py`;
- outras ADRs, contratos, nomenclatura, índices, handoffs históricos e
  relatórios históricos.

A descoberta do demo dedicado ocorre pelo comando próprio (§29) e pelo relatório
de implementação — **não** por inflação do demo principal.

---

## 25. Compatibilidade

```yaml
jsons_antigos_mudam_sem_o_campo: false
migracao_automatica: false
reescrita_automatica: false
aplicacao_recursiva: false
default_estrutural_novo: false
campos_desconhecidos: rejeicao_controlada
configuracao_invalida: erro_de_dominio_controlado
```

A ausência de `distribuicao_matricial` preserva exatamente o comportamento
anterior. Testes de regressão devem cobrir configurações existentes de:
dashboard, console, lancador, composição do corpo e demo principal.

---

## 26. Famílias mínimas de telas (configurações permanentes)

Cobrir, no mínimo, as 28 famílias abaixo (mapeadas para JSONs em §23.3):

1. preferência por linhas;
2. preferência por colunas;
3. matriz fixa;
4. conteúdo centralizado horizontalmente com preferência por colunas;
5. conteúdo à esquerda com margens horizontais mínimas e máximas;
6. distribuição horizontal uniforme entre margens e participantes;
7. margens horizontais limitadas, com sobra entre participantes;
8. margens superior e inferior mínimas;
9. margens verticais mínimas e máximas, com sobra entre linhas;
10. distribuição vertical uniforme;
11. um participante centralizado horizontal e verticalmente;
12. três participantes centralizados nos dois eixos, com distribuição uniforme;
13. quatro participantes centralizados nos dois eixos, com distribuição uniforme;
14. matriz fixa que cabe exatamente;
15. matriz fixa que aciona quadro mínimo;
16. recuperação após aumentar a janela;
17. `minimo_fixo` com participante internamente maior;
18. cardinalidade unitária;
19. uma linha;
20. uma coluna;
21. resto horizontal;
22. resto vertical;
23. console com `distribuicao_matricial`;
24. console sem `distribuicao_matricial`;
25. lançador de teste com `distribuicao_matricial`;
26. lançador sem o campo, preservando política histórica;
27. dashboard com `distribuicao_matricial`;
28. dashboard antigo sem o campo.

### 26.1 Elementos usados nas telas

Os participantes de teste devem ter conteúdo que permita confirmar: identidade,
ordem, célula, linha, coluna, alinhamento, ausência de perda e ausência de
duplicação. Usar rótulos semanticamente inequívocos (por exemplo,
identificadores ordenados), conforme a convenção real do projeto. **Não** usar
conteúdo idêntico em todos os participantes.

---

## 27. Demo dedicado

Arquivo: `demo/demo_distribuicao.py` (separado do demo principal `demo/demo.py`).

Definições nominais obrigatórias:

- **Caminho do novo arquivo**: `demo/demo_distribuicao.py`.
- **Mecanismo de seleção das telas**: tela raiz de catálogo
  `config/telas/demo/h0035_catalogo.json` (um `lancador` cujos itens navegam por
  `chip → tela_destino` para cada tela `h0035_*` de §23.3), reutilizando a
  navegação já existente no demo (`chip → tela_destino`); adicionalmente, o
  comando aceita um argumento opcional de id de tela para abrir diretamente uma
  família (`python demo/demo_distribuicao.py <id_tela>`), com id inválido
  produzindo mensagem de erro material e código de saída não zero.
- **Configuração inicial**: tela `h0035_catalogo`, borda `curva`, dimensões
  lidas do terminal (ioctl) com tratamento de `SIGWINCH`, reutilizando a
  infraestrutura de sessão TTY existente em `demo/demo.py` por **importação**
  (sem duplicação e sem alterar `demo/demo.py`).
- **Comando exato de execução**: `python demo/demo_distribuicao.py` (raiz do
  projeto).
- **Identidade semântica exibida** (ver §29): nome da tela, família de
  distribuição, formação, ordem, consumidor testado e estado (normal ou quadro
  mínimo).
- **Mensagens de erro**: id de tela inexistente, JSON inválido e configuração
  `distribuicao_matricial` inválida devem produzir mensagem material
  identificável (classe de erro de domínio), sem renderização parcial.
- **Comportamento ao redimensionar**: recalcular a distribuição a cada
  `SIGWINCH`; acionar o quadro mínimo canônico quando a área for insuficiente e
  reconstruir determinísticamente ao aumentar.
- **Como sair do demo**: comando/tecla de saída equivalente ao do demo principal
  (documentar exatamente no relatório e no cabeçalho do arquivo).

A expressão "ponto de entrada real" refere-se ao **ponto de entrada real e
executável do próprio artefato demonstrado** (`demo/demo_distribuicao.py`), e
**não** ao ponto de entrada do produto real. Preservar ADR-0021 (separação
demo/produto e política de caminhos) e ADR-0022 (tela inicial do produto).

### 27.1 Relação com o demo principal

O demo principal **não** recebe todas as novas telas e **não** deve virar
catálogo das configurações matriciais. Nenhuma alteração em `demo/demo.py` nem
em `config/telas/demo/demo.json` é autorizada por este handoff. A reutilização
de infraestrutura ocorre por importação, sem duplicação.

---

## 28. Cobertura de superfícies equivalentes (renderer)

O executor deve inventariar todos os pontos de entrada que recebem
participantes, formação, dimensões, margens, vãos, alinhamento e área útil, e
garantir que **toda superfície equivalente** aplique a mesma política. Pontos de
entrada confirmados a inventariar: `renderizar_tela`, `_renderizar_container`,
`_renderizar_container_vertical`, `_renderizar_container_horizontal`,
`_renderizar_container_matriz`, `_montar_corpo_horizontal`, `_caixa_de_elemento`,
`_linhas_console`, `_linhas_dashboard`, `_linhas_lancador`,
`_quadro_minimo_global`.

Exigências:

1. inventariar todos os pontos de entrada equivalentes;
2. identificar o ponto central adequado para o cálculo;
3. reutilizar uma única semântica (motor de §23.1);
4. preservar adaptações específicas apenas nas fronteiras necessárias
   (dashboard, console, lancador);
5. testar chamadas diretas e indiretas;
6. evitar duplicação de algoritmo;
7. aplicar validação antes de qualquer efeito observável;
8. não produzir renderização parcial antes do erro;
9. não corrigir apenas o primeiro símbolo encontrado.

Não escolher nomes de funções sem verificar o código real.

---

## 29. Identidade semântica da demonstração

O demo dedicado deve confirmar **positivamente**: nome da tela carregada;
família de distribuição; formação; ordem; consumidor testado; estado (normal ou
quadro mínimo). Código de saída zero **não** prova que a tela correta foi
carregada. O smoke test deve verificar **conteúdo material** da identidade.

---

## 30. Consumidores: dashboard, console, lançador

### 30.1 Dashboard

Quando um `dashboard` declarar `distribuicao_matricial`: a capacidade organiza
seus participantes imediatos; formação, ordem, dimensionamento, margens, vãos,
distribuição e alinhamento seguem a nova configuração; a ausência do campo
preserva o comportamento anterior; nenhum JSON antigo muda; sem migração
automática. A pendência histórica de alinhamento horizontal do dashboard
permanece **fora do escopo**, salvo o que a presença de `distribuicao_matricial`
já resolve. Não usar esta implementação para resolver genericamente a pendência.

### 30.2 Console (DEC-APP-0025-03)

Quando um `console` declarar `distribuicao_matricial`, ela **substitui
integralmente** as políticas geométricas anteriores do mesmo conjunto
(`politica_composicao.alinhamento`, espaçamento borda↔conteúdo,
quantidade/ajuste de colunas, alinhamento de colunas, vãos, formação e
distribuição geométrica anteriores). **Sem** coexistência, soma, complemento,
cascata, herança parcial ou dupla autoridade geométrica.

Permanecem as políticas **funcionais não geométricas**: `overflow_normal`,
navegação, seleção, paginação própria do console, exibição, ação de item,
filtros, formação de seleção, origem dos dados, itens. A paginação funcional do
console **não** se torna paginação da capacidade ADR-0025. Quando ausente, todo
o comportamento anterior permanece. Testar os **dois estados**: campo presente e
campo ausente.

### 30.3 Lançador (DEC-APP-0025-02)

Quando um `lancador` declarar `distribuicao_matricial`, a nova configuração tem
**precedência** sobre as políticas geométricas históricas sobrepostas: algoritmo
fila/matriz (ADR-0001), bloco à esquerda + sobra à direita (ADR-0002), vãos
elásticos (ADR-0003), margens históricas borda↔bloco, e demais decisões
históricas de formação/margem/vão/alinhamento/distribuição cobertas pela nova
estrutura.

Permanecem: identidade dos itens, comandos, ações, navegação, conteúdo textual,
subcolunas funcionais não substituídas, largura mínima funcional, fallback
global (ADR-0023), parâmetros não relacionados ao layout matricial.

Quando ausente: ADR-0001, ADR-0002, ADR-0003 e ADR-0023 permanecem; JSONs
antigos mantêm o comportamento.

---

## 31. Validações do loader

O loader deve: aceitar a estrutura válida; rejeitar tipo incorreto; rejeitar
campo desconhecido; rejeitar literal fora do vocabulário; rejeitar número
negativo; rejeitar máximo inferior ao mínimo; rejeitar linhas/colunas inválidas;
rejeitar matriz fixa incompleta; rejeitar dependência obrigatória ausente;
rejeitar combinação contraditória; preservar ausência da estrutura; produzir
erro de domínio com mensagem material verificável. Os testes **não** aceitam
exceção genérica como prova suficiente.

---

## 32. Modelo e renderer

### 32.1 Modelo

Representar todos os 26 caminhos; preservar ausência da estrutura; **não**
aplicar defaults estruturais novos; manter tipos explícitos; transportar valores
sem alteração silenciosa; permitir acesso determinístico pelo renderer; sem I/O
de configuração; sem lógica geométrica (que pertence ao renderer/motor).

### 32.2 Renderer

Implementação **centralizada** da geometria (§23.1, §28). Validação antes de
qualquer efeito observável; sem renderização parcial antes do erro; determinismo
completo (ADR-0025 §28) com critérios completos de desempate.

---

## 33. Divergência do H-0034 (não corrigir)

Este handoff **não** corrige a divergência histórica do H-0034. Para evitar
correção silenciosa:

- **não** adicionar `distribuicao_matricial` ao JSON produtivo atual do lançador;
- **não** migrar automaticamente a configuração do lançador principal;
- **não** reescrever snapshots produtivos como se a divergência estivesse
  resolvida;
- **não** declarar H-0034 corrigido;
- usar **configurações próprias e permanentes de teste** (`h0035_lancador_com.json`,
  `h0035_lancador_sem.json`) para demonstrar o novo suporte no lançador.

A implementação da capacidade genérica não substitui o ciclo corretivo
específico do H-0034.

---

## 34. Condições de bloqueio

Parar com:

```text
H3_BLOCKED_DOCUMENTATION
```

se: faltar contrato indispensável; existir contradição normativa ativa; não for
possível listar os arquivos necessários; a implementação exigir alterar
autoridade documental; o suporte exigir decidir semântica não fechada; não for
possível separar esta capacidade da correção H-0034.

Parar com:

```text
BLOCKED_USER_DECISION
```

se faltar decisão explícita do usuário para tornar a implementação executável.

Não completar lacunas. Não inventar arquitetura. Não criar permissões genéricas.

---

## 35. Relatório de implementação

Criar `docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md`
contendo, no mínimo:

1. identificação; 2. handoff executado; 3. autoridades; 4. estado Git inicial;
5. arquivos alterados; 6. arquivos criados; 7. inventário das superfícies
equivalentes; 8. arquitetura efetivamente utilizada; 9. estrutura declarativa
implementada; 10. cobertura dos 26 caminhos; 11. validações do loader; 12.
propagação no modelo; 13. algoritmo do renderer; 14. formação; 15. ordem; 16.
dimensionamento; 17. margens e vãos; 18. expansão; 19. restos; 20. alinhamento;
21. `minimo_fixo`; 22. dashboard; 23. console; 24. lançador; 25. fallback; 26.
recuperação; 27. compatibilidade; 28. configurações permanentes; 29. demo
dedicado; 30. identidade semântica; 31. testes focais; 32. suíte canônica; 33.
smoke; 34. pseudo-TTY; 35. validação manual pendente; 36. exceções autorizadas;
37. desvios; 38. estado Git final; 39. `git diff --check`; 40. limitações; 41.
conclusão factual.

O relatório **não** pode declarar aprovação da própria implementação.

---

## 36. Validação manual em TTY

A mudança é visual e geométrica. O executor da implementação deve: criar os
cenários permanentes; fornecer os comandos; executar testes automatizados;
executar smoke e pseudo-TTY quando aplicável; **registrar que a validação humana
permanece pendente**. Somente o usuário confirma o resultado visual em TTY real.

O relatório deve usar:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

até o usuário informar o resultado. Não exigir dimensões fixas como única prova
manual. A validação deve incluir: abrir o demo dedicado; selecionar diferentes
famílias; maximizar a janela; restaurar ou reduzir; redimensionar livremente;
produzir quadro mínimo; aumentar novamente; confirmar recuperação; confirmar
ordem; confirmar ausência de perda e duplicação; confirmar diferenças entre
políticas; confirmar que o demo principal não foi inflado indevidamente.

Se o cenário não puder ser reproduzido ou identificado: `VALIDACAO_MANUAL_INCONCLUSIVA`.
Se o cenário for reproduzido e estiver incorreto: `MANUAL_VALIDATION_FAILED`.

---

## 37. Testes automatizados obrigatórios

### 37.1 Loader (`tela/teste_loader.py`)

estrutura válida completa; estrutura válida mínima; ausência; campos
desconhecidos; tipos; literais; limites; dependências; combinações inválidas.

### 37.2 Modelo (`tela/teste_modelo.py`)

armazenamento dos 26 caminhos; ausência sem default estrutural; igualdade ou
serialização aplicável; propagação entre loader e renderer.

### 37.3 Motor / Renderer (`tela/teste_distribuicao_matricial.py`, `tela/teste_renderizador.py`)

todas as formações; ambas as ordens; dimensionamento por linha; por coluna;
uniforme; mínimo fixo; tratamento interno; margens; vãos; máximos; ordem de
expansão; restos; alinhamentos; cardinalidade unitária; uma linha; uma coluna;
formação impossível; fallback; recuperação; determinismo; ausência de efeito
parcial.

### 37.4 Dashboard (`tela/teste_renderizador.py`)

campo presente; campo ausente; compatibilidade; alinhamento controlado pela
estrutura; ausência de dupla autoridade.

### 37.5 Console (`tela/teste_renderizador.py`)

substituição das políticas geométricas quando presente; preservação integral das
políticas antigas quando ausente; preservação das políticas funcionais;
paginação funcional fora da nova capacidade.

### 37.6 Lançador (`tela/teste_renderizador.py`)

precedência da nova configuração quando presente; preservação de ADR-0001,
ADR-0002, ADR-0003 quando ausente; preservação da ADR-0023; ausência de correção
silenciosa do H-0034; JSON produtivo principal sem migração automática.

### 37.7 Demo (`demo/teste_demo_distribuicao.py`)

catálogo dedicado; seleção de todas as configurações; identidade semântica;
comando de entrada; quadro mínimo; recuperação; demo principal preservado.

### 37.8 Diagnóstico (`demo/teste_diagnostico.py`)

configurações válidas detectadas; configurações inválidas rejeitadas; identidade
dos novos artefatos; ausência de dependência de estado externo.

### 37.9 Independência dos valores esperados

Os testes geométricos **não** calculam o valor esperado chamando o mesmo
algoritmo da produção. Aceitáveis: coordenadas derivadas manualmente; tabelas de
expectativa; casos pequenos com geometria fechada; invariantes independentes;
comparação com resultados explicitamente enumerados. **Não** suficientes:
reproduzir o algoritmo de produção no teste; comparar a saída consigo mesma;
verificar apenas ausência de exceção; verificar apenas código de saída zero;
snapshots sem identidade semântica; asserções permissivas.

### 37.10 Provas de rejeição

Todo teste de configuração inválida deve: exigir a classe correta de erro de
domínio; falhar se houver sucesso; falhar se houver exceção genérica diferente;
verificar dados materiais da mensagem; provar ausência de efeito parcial quando
aplicável.

---

## 38. Suíte canônica e comandos de verificação

Usar `PYTHONDONTWRITEBYTECODE=1` quando compatível com a prática atual. Executar
da raiz do projeto.

**Suíte focal:**

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_renderizador.py -q --tb=short
```

A suíte focal **não** substitui a suíte canônica completa.

**Suíte canônica completa** (base histórica: 6 scripts; este ciclo acrescenta 2
scripts novos, totalizando 8):

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_distribuicao_matricial.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_diagnostico.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_demo_distribuicao.py
PYTHONDONTWRITEBYTECODE=1 python demo/teste_explorar_barra_de_menus.py
```

**Smoke do demo dedicado:**

```bash
PYTHONDONTWRITEBYTECODE=1 python demo/demo_distribuicao.py
```

O smoke deve confirmar identidade material (§29), não apenas código de saída
zero. Pseudo-TTY: incluir prova em pseudo-terminal (pty) no
`demo/teste_demo_distribuicao.py`, cobrindo seleção de família, quadro mínimo e
recuperação por redimensionamento, quando aplicável.

**Higiene de whitespace:**

```bash
git diff --check
```

---

## 39. Critérios de aceite

1. todos os 26 caminhos reconhecidos; 2. estrutura válida aceita; 3. estrutura
inválida rejeitada; 4. ausência do campo preserva comportamento; 5. nível único
preservado; 6. preferência por linhas implementada; 7. preferência por colunas
implementada; 8. matriz fixa implementada; 9. ordem por linha implementada; 10.
ordem por coluna implementada; 11. dimensionamento implementado; 12.
`minimo_fixo` tratado internamente; 13. margens implementadas; 14. vãos
implementados; 15. máximos respeitados; 16. expansão determinística; 17. restos
determinísticos; 18. alinhamento interno implementado; 19. dashboard suportado;
20. console substitui políticas geométricas quando o campo está presente; 21.
console preserva políticas antigas quando ausente; 22. lançador aplica
precedência quando presente; 23. lançador preserva políticas históricas quando
ausente; 24. H-0034 não corrigido silenciosamente; 25. quadro mínimo acionado
corretamente; 26. recuperação determinística; 27. nenhum participante perdido;
28. nenhum participante duplicado; 29. nenhuma sobreposição inválida; 30. nenhuma
coordenada negativa; 31. nenhuma renderização parcial; 32. JSONs antigos
preservados; 33. configurações permanentes criadas; 34. demo dedicado criado;
35. identidade semântica comprovada; 36. suíte focal verde; 37. suíte canônica
verde; 38. smoke verde; 39. pseudo-TTY verde, quando aplicável; 40. validação
manual marcada como pendente do usuário; 41. arquivos dentro do escopo; 42.
relatório fiel; 43. stage vazio; 44. `git diff --check` limpo; 45. nenhum commit
realizado.

---

## 40. Escopo negativo (fora do escopo)

distribuição multinível; recursão; herança; cascata; propagação entre níveis;
paginação da nova capacidade; migração automática de JSONs; reescrita de JSONs
existentes; correção da divergência H-0034; redefinição da ADR-0023; alteração
da tela inicial do produto; alteração da separação entre demo e produto; correção
do alinhamento horizontal histórico do dashboard; novas políticas funcionais de
console; novas políticas funcionais de lançador; implementação de truncamento
interno; implementação de rolagem interna; alteração de contratos; alteração de
ADRs; alteração de nomenclatura; commit.

---

## 41. Exceção operacional

```text
Arquivo fora da lista nominal não pode ser alterado silenciosamente.

Se um arquivo fora da lista for estritamente necessário para cumprir o
handoff, preservar a suíte obrigatória ou evitar abortar a entrega, o executor
deve parar e pedir autorização explícita ao usuário.

O pedido deve informar:

- arquivo;
- motivo;
- mudança exata;
- escopo;
- consequência de não alterar.

Se o usuário autorizar, a implementação pode continuar sem patch retroativo
do handoff, desde que o relatório registre:

- autorização;
- arquivo;
- justificativa;
- escopo concedido;
- mudança realizada.

A autorização não permite nova semântica, arquitetura ou política.
```

Esta cláusula não é proibição absoluta que torne a implementação inexequível;
ela disciplina o caso de necessidade comprovada fora da lista nominal.

---

## 42. Observações não bloqueantes (preservar)

- **Observação 1** — A abertura da seção 11 de `contrato_lancador.md` ainda
  contém formulação histórica sobre "reconciliação futura", embora as subseções
  normativas fechem a precedência. Não tratar isso como autorização para reabrir
  o contrato.
- **Observação 2** — A divergência H-0034 permanece futura e separada.
- **Observação 3** — O alinhamento horizontal histórico do dashboard permanece
  pendência futura delimitada.

Nenhuma dessas observações bloqueia a implementação da ADR-0025.

---

## 43. Proibição de commit e limite de encerramento

A futura implementação **não** deve preparar nem executar commit. Ao final: stage
vazio; `git diff --check` limpo; nenhum commit realizado. O commit é decisão
posterior e separada.

Durante `CRIAR_HANDOFF`, somente este arquivo foi criado. Nenhuma implementação
foi executada: nenhum código, teste, configuração JSON ou demo foi criado, e
nenhum commit foi autorizado.

Depois de aprovado por QA com `H1_HANDOFF_APPROVED`, este handoff constitui a
autoridade de escopo para uma etapa futura e separada `IMPLEMENTAR`. Nessa etapa
futura, o executor poderá alterar ou criar somente os arquivos nominalmente
autorizados por este handoff (§22 e §23), respeitando o escopo positivo (§11), o
escopo negativo (§40), os arquivos preservados (§24), os critérios de aceite (§39),
os testes (§37), a demonstração (§27), o relatório de implementação (§35) e a
cláusula de exceção operacional (§41).

A implementação futura não pode começar antes de `H1_HANDOFF_APPROVED`.
