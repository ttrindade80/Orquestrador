---
name: H-0027-composicao-hierarquica-tres-niveis-grupos
description: Handoff de implementacao — composicao hierarquica do corpo com ate tres niveis de grupos; validacao recursiva com contagem de profundidade por nos grupo; multiplos filhos por grupo; grupos irmaos; distribuicao por container; renderizacao recursiva por container; remocao das restricoes historicas do H-0012 incompativeis com ADR-0019
metadata:
  type: handoff
  status: proposto
  data: 2026-07-12
rastreabilidade:
  adrs_base:
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
  contratos_aplicaveis:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
  levantamento_base: docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  handoff_precedente: docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
  relatorio_precedente: docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
  escopo_alteravel:
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
    - tela/teste_demo.py
    - docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
  escopo_somente_leitura:
    - docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
    - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
    - docs/adr/ADR-0007-tela-processamento-composicao.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
    - config/telas/orquestrador.json
    - config/telas/grupo_minimo.json
    - config/telas/destino_minimo.json
    - config/telas/stub_b.json
  relatorio_implementacao_esperado: docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
---

# H-0027 — Composição hierárquica do corpo com três níveis de grupos

## 1. Identificação e status

| Campo | Valor |
|---|---|
| Identificador | H-0027 |
| Status | proposto |
| Data | 2026-07-12 |
| ADR base | ADR-0019 (aceita, 2026-07-12) |
| Ciclo anterior fechado | H-0026 / IMP-0027 |
| Relatório esperado | IMP-0028 |

Este handoff **não** implementa código, **não** faz QA de si mesmo, **não** decide
arquitetura nova, **não** completa lacunas normativas e **não** prepara commit. É uma
ordem de trabalho fechada para o executor de implementação.

---

## 2. Estado comprovado do repositório

### 2.1 Referência Git

```text
branch:  HEAD (master)
commit:  40015b6 feat: implementa distribuicao horizontal percentual e fracionaria
stage:   vazio

alterações rastreadas (não no stage):
  M docs/NOMENCLATURA.md
  M docs/adr/ADR-0007-tela-processamento-composicao.md
  M docs/adr/INDICE_ADR.md
  M docs/contratos/contrato_composicao_corpo.md
  M docs/contratos/contrato_json_tela_minima.md
  M docs/contratos/contrato_tela_json.md

não rastreados:
  ?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  ?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  ?? docs/relatorios/RELATORIO_QA_ADR-0019.md
  ?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
  ?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
  ?? tela/__pycache__/

git diff --check: sem saída (sem conflitos de espaço em branco)
```

As seis alterações rastreadas são a aplicação documental da ADR-0019.
Os sete arquivos não rastreados são a ADR-0019, os relatórios do ciclo e o
diretório de cache. Todos permanecem intocados durante a implementação.

### 2.2 Verificação obrigatória no início da implementação

O executor deve executar antes de qualquer alteração:

```bash
git log -1 --oneline
git status --short
git diff --stat
git diff --check
git diff --cached --stat
```

Se o estado divergir do descrito em 2.1, parar com `BLOCKED_REPOSITORY_STATE`.

Arquivos não rastreados e alterações documentais não constituem divergência.
Qualquer alteração rastreada inesperada em `tela/*.py` é divergência relevante.

---

## 3. Autoridades normativas obrigatórias

O executor deve ler integralmente antes de iniciar a implementação:

| Documento | Decisões relevantes |
|---|---|
| `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | D1–D7: todas |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md` | Confirmação ADR_APPROVED |
| `docs/contratos/contrato_composicao_corpo.md` | Seções 3.2, 4.8, 4.9, 5.7–5.9, 8 |
| `docs/contratos/contrato_tela_json.md` | Seção 8 (composição hierárquica) |
| `docs/contratos/contrato_json_tela_minima.md` | Seções 6.2–6.3 |

O executor deve ler nas seções diretamente relevantes:

| Documento | Seções |
|---|---|
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | Decisões 1–10 |
| `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | D1–D7 |
| `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` | Taxonomia funcional |
| `docs/adr/ADR-0007-tela-processamento-composicao.md` | Pontos 1–10; superação parcial por ADR-0019 D7 |

O levantamento abaixo é evidência técnica, não autoridade normativa:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
```

---

## 4. Decisão fechada (ADR-0019)

As sete decisões abaixo foram aprovadas pelo usuário (status `aceita`,
QA `ADR_APPROVED`, aplicação documental `ADR_APPLICATION_APPROVED_WITH_NOTES`).
O executor não questiona, não complementa e não substitui nenhuma delas.

| ID | Enunciado normativo |
|---|---|
| D1 | Profundidade hierárquica contada exclusivamente pelo aninhamento de nós estruturais `grupo`; corpo raiz não conta; listas `elementos[]` não contam; elementos funcionais não contam |
| D2 | Profundidade máxima: **três níveis de grupos** (contados conforme D1) |
| D3 | Grupo do nível 3 **pode** conter um ou mais elementos funcionais; esses elementos **não** constituem nível 4 de grupo |
| D4 | `grupo` filho de grupo do nível 3 está no nível 4 e é **estruturalmente inválido**; deve ser rejeitado com erro estrutural determinístico |
| D5 | Múltiplos grupos irmãos são **permitidos** em qualquer nível de grupo válido |
| D6 | Múltiplos elementos funcionais por grupo são **permitidos** em qualquer nível |
| D7 | A restrição "zero ou um `dashboard` por tela" está **removida** como regra global; não existe limite global de dashboards |

Regras mantidas pelas ADRs precedentes e preservadas integralmente por este handoff:

- ADR-0015: arranjo por container, distribuição por container, associação posicional,
  maiores restos, desempate por ordem declarada, preenchimento de área alocada.
- ADR-0018: ausência de `distribuicao` preserva construção orientada pelo conteúdo;
  ausência não equivale a `igual`; `igual` só existe quando declarado.
- ADR-0010: taxonomia funcional fechada (`console`, `lancador`, `dashboard`);
  `dashboard` passivo e não navegável por `[✥]`; `grupo` não é tipo funcional.

---

## 5. Objetivo

Implementar a composição hierárquica do corpo com até três níveis de grupos,
incorporando as decisões D1–D7 da ADR-0019 nas três camadas (loader, modelo,
renderizador) e nos quatro conjuntos de testes, de forma coesa e indivisível.

As três camadas precisam concordar sobre a mesma árvore. Este handoff trata a
capacidade como um único ciclo coeso.

---

## 6. Diagnóstico da implementação atual

### 6.1 Loader (`tela/loader.py`)

| Linha | Comportamento atual | Conflito com ADR-0019 |
|---|---|---|
| 243–251 | Rejeita `grupo.arranjo` em `horizontal`/`lado_a_lado` com `TelaGrupoInvalido` | D5, D6: arranjo horizontal é válido por container |
| 269–273 | Rejeita `len(sub) > 1` com `TelaGrupoInvalido` | D5, D6: múltiplos filhos são permitidos |
| 302–306 | Rejeita `tipo_item == "grupo"` com `TelaGrupoInvalido` | D2, D3: grupos aninhados são válidos até nível 3 |
| — | Sem validação recursiva de profundidade por nós `grupo` | D1, D2, D4 |
| — | Sem validação de `grupo.distribuicao` | ADR-0015 dec. 5–8 |

A função `_validar_grupo` contém as restrições históricas do H-0012 que são
incompatíveis com a ADR-0019. Deve ser substituída por validação recursiva.

### 6.2 Modelo (`tela/modelo.py`)

| Linha | Comportamento atual | Conflito |
|---|---|---|
| 127–133 | `_construir_elementos_internos_grupo`: não recursivo; assume exatamente 1 item não-grupo | D2, D5, D6 |
| 127 | Docstring: "Não há recursão: grupo dentro de grupo é rejeitado pelo loader" | Premissa deixa de ser válida |
| 90–106 | `elemento_por_id` e `elementos_por_tipo`: percorrem apenas `corpo.elementos` (planos) | — (ver seção 14.2) |

### 6.3 Renderizador (`tela/renderizador.py`)

| Linha | Comportamento atual | Conflito |
|---|---|---|
| 1107–1117 | Modo vertical/sem distribuição: itera `elemento.elementos` apenas 1 nível | D2, D5, D6 |
| 1083–1094 | Modo vertical+distribuição: aplica cota ao funcional interno; apenas 1 nível | D2, D5, D6 |
| 808–809, 846–856 | Modo horizontal: grupo vira slot visualmente vazio (não expandido) | D2, D5, D6 |
| — | Sem aplicação de `grupo.arranjo` e `grupo.distribuicao` | ADR-0015 dec. 4–5 |
| — | Sem composição recursiva por container | D2 |

### 6.4 Testes (`tela/teste_loader.py`)

Os seguintes testes validam restrições históricas que **não têm autoridade ativa** após
a ADR-0019 e devem ser alterados, não removidos — a cobertura deve ser substituída
por testes coerentes com as regras vigentes:

| Linha aprox. | Teste atual | Motivo da alteração |
|---|---|---|
| 645–654 | "grupo com 2 elementos → TelaGrupoInvalido" | ADR-0019 D5, D6: múltiplos filhos são agora válidos |
| 656–664 | "grupo dentro de grupo → TelaGrupoInvalido" | ADR-0019 D2: grupos aninhados são válidos até nível 3 |
| 666–673 | "grupo com arranjo 'horizontal' → TelaGrupoInvalido" | ADR-0019 D5: arranjo horizontal é válido por container |
| 675–682 | "grupo com arranjo 'lado_a_lado' → TelaGrupoInvalido" | ADR-0019 D5: alias de horizontal, igualmente válido |

---

## 7. Arquivos somente para leitura

O executor pode ler mas **não pode alterar** durante a implementação:

```text
docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/adr/ADR-0007-tela-processamento-composicao.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
docs/NOMENCLATURA.md
config/telas/orquestrador.json
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/telas/stub_b.json
```

---

## 8. Arquivos permitidos para alteração

O executor pode criar ou alterar somente os arquivos abaixo:

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
```

Se a implementação exigir fixtures JSON de teste que não existam, o executor pode
criar arquivos **exclusivamente** no diretório `config/telas/`, com nomes descritivos
e sem alterar os quatro JSONs existentes. Cada fixture criada deve ser listada no
relatório de implementação.

---

## 9. Arquivos proibidos

Durante a implementação, é proibido alterar:

```text
docs/adr/          (qualquer arquivo)
docs/contratos/    (qualquer arquivo)
docs/NOMENCLATURA.md
docs/handoff/      (qualquer arquivo, incluindo este)
docs/relatorios/   (exceto IMP-0028, que deve ser criado)
config/telas/orquestrador.json
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/telas/stub_b.json
```

---

## 10. Escopo positivo

Este handoff autoriza exclusivamente:

- Validação recursiva de grupos no loader com contagem de profundidade por nós `grupo`
- Aceitação de grupos nos níveis 1, 2 e 3
- Rejeição estrutural de grupo no nível 4 com `TelaGrupoInvalido` e mensagem determinística
- Múltiplos filhos por grupo (funcionais e grupos) em todos os níveis válidos
- Múltiplos grupos irmãos no mesmo container
- `grupo.arranjo` válido: `None`, `"vertical"`, `"horizontal"`, `"sobreposto"`, `"lado_a_lado"`
- Validação de `grupo.distribuicao` quando declarada (modos `igual`, `percentual`, `fracao`)
- Ausência de `grupo.distribuicao` como estado válido (construção orientada pelo conteúdo)
- Construção recursiva do modelo preservando a árvore integral
- `ElementoCorpo.elementos` contendo sub-árvore recursiva para grupos
- Composição recursiva no renderizador por container (corpo raiz e grupos)
- Aplicação de `grupo.arranjo` ao compor os filhos diretos de um grupo
- Aplicação de `grupo.distribuicao` ao repartir a área entre os filhos diretos de um grupo
- Grupo como nó estrutural: sem borda, moldura, título ou conteúdo visual próprio
- Ausência de limite global de dashboards
- Testes novos e alterados cobrindo a matriz de cenários da seção 18
- Relatório `IMP-0028`

---

## 11. Escopo negativo

Este handoff proíbe explicitamente:

- Quarta camada de grupos ou profundidade ilimitada
- Novos tipos funcionais além de `console`, `lancador`, `dashboard`
- Novos campos JSON além dos já definidos nos contratos
- Novos modos de distribuição além de `igual`, `percentual`, `fracao`
- Alteração do algoritmo de maiores restos ou de desempate por ordem
- Nova política de overflow ou de conteúdo maior que a cota
- Mudança na estrutura interna de `dashboard`
- Mudança de navegabilidade de qualquer tipo
- Alteração de `[✥]`, `[⏎]`, `[␣]` ou outros chips
- Alteração de bindings
- Correção da divergência de status da ADR-0018 (pendência documental separada)
- Alteração das configurações `config/telas/*.json` existentes
- Aplicação documental adicional em ADRs, contratos ou nomenclatura
- Nova ADR
- Preparação de commit
- Commit ou push

---

## 12. Preservações obrigatórias

O executor deve verificar que todas as capacidades abaixo continuam funcionando
após a implementação:

- Composições planas (lista de funcionais sem grupos): `orquestrador`, `destino_minimo`, `stub_b`
- Composição com um nível de grupo: `grupo_minimo`
- Comportamento do corpo raiz (arranjo vertical, horizontal, ausente)
- Distribuição vertical e horizontal do corpo raiz (modos `igual`, `percentual`, `fracao`)
- Ausência de distribuição no corpo raiz (construção orientada pelo conteúdo)
- Ordem declarada em `elementos[]` como critério de desempate
- Maiores restos e soma exata da área distribuída
- Tipos funcionais: `console`, `lancador`, `dashboard`
- `grupo` como nó estrutural sem borda ou conteúdo visual
- `dashboard` como elemento passivo não navegável por `[✥]`
- Regras de navegação: `[✥]` restrito a `console`
- Ocupação vertical da janela (ADR-0013, ADR-0017)
- Redimensionamento reativo sem alteração da composição declarativa (ADR-0017)
- Diagnósticos para erros existentes (arquivo ausente, JSON inválido, tipo desconhecido, etc.)
- Todos os testes das suítes anteriores que não validam restrições históricas incompatíveis

---

## 13. Especificação do loader

### 13.1 Substituição de `_validar_grupo`

A função `_validar_grupo` atual deve ser substituída por uma função de validação
recursiva. A nova função deve:

1. Receber: `elemento` (dict), `id_grupo` (str), `nivel_grupo` (int, começa em 1),
   `caminho` (str, para diagnóstico — ex.: `"corpo → grupo_a"`)
2. Validar `grupo.arranjo` contra `ARRANJOS_CORPO_VALIDOS` (o mesmo conjunto já
   definido para `corpo.arranjo`); se inválido, levantar `TelaGrupoInvalido` com
   caminho
3. Validar que `elementos` existe, é lista não vazia; se ausente ou vazio,
   levantar `TelaGrupoInvalido`
4. Para cada item em `elementos[]`:
   a. Validar que tem `id` (str não vazio) e `tipo` (str não vazio)
   b. Se `tipo == "grupo"`:
      - Se `nivel_grupo == 3`: levantar `TelaGrupoInvalido` com mensagem que
        inclua o caminho completo e indique que o nível 4 é inválido
      - Se `nivel_grupo < 3`: chamar recursivamente com `nivel_grupo + 1` e
        caminho estendido com `" → " + id_do_subgrupo`
   c. Se `tipo in TIPOS_CORPO_VALIDOS`: aceitar
   d. Senão: levantar `TelaTipoDesconhecido`
5. Se `distribuicao` presente no elemento: validar usando `_validar_distribuicao_corpo`
   (ou função equivalente) com `n_elementos = len(elementos)` e mensagem de erro
   incluindo o caminho do grupo

### 13.2 Chamada no `carregar_tela`

O laço em `carregar_tela` já identifica `tipo == "grupo"` e chama `_validar_grupo`.
Essa chamada deve passar `nivel_grupo=1` e `caminho="corpo"` para a nova função.
O resto do laço permanece intacto.

### 13.3 Constantes reutilizáveis

- `ARRANJOS_CORPO_VALIDOS`: reusável para `grupo.arranjo` (já inclui `None`,
  `"vertical"`, `"horizontal"`, `"sobreposto"`, `"lado_a_lado"`)
- `MODOS_DISTRIBUICAO_CORPO_VALIDOS`: reusável para `grupo.distribuicao.modo`
- `TIPOS_CORPO_VALIDOS`: reusável para filhos funcionais dos grupos

### 13.4 Mensagem de diagnóstico de nível 4

A mensagem de `TelaGrupoInvalido` para grupo no nível 4 deve:

- Ser determinística (mesma entrada, mesma mensagem)
- Incluir o `id` do grupo ofensor
- Incluir o caminho completo que levou ao nível inválido (ex.: `"corpo → g1 → g2 → g3"`)
- Indicar que o limite máximo de aninhamento de grupos é 3 níveis

O texto exato é decisão de implementação, respeitando os requisitos acima.
Não use o padrão de mensagem de `_validar_grupo` do H-0012 para isso.

### 13.5 Ausência de dashboards com limite global

Não deve existir validação que rejeite uma segunda ou terceira instância de
`dashboard` em `corpo.elementos[]` ou em `grupo.elementos[]`. A remoção da
cardinalidade global (ADR-0019 D7) significa que nenhuma verificação de "zero
ou um por tela" deve ser introduzida ou preservada no loader.

---

## 14. Especificação do modelo

### 14.1 Construção recursiva da árvore

A função `_construir_elementos_internos_grupo` deve ser substituída por uma
função recursiva que aceita uma lista `elementos_raw` e retorna a lista de
`ElementoCorpo` correspondente, tratando corretamente:

- Filhos funcionais (`console`, `lancador`, `dashboard`): criam `ElementoCorpo`
  com `elementos=[]`
- Filhos do tipo `grupo`: criam `ElementoCorpo` com `tipo="grupo"` e
  `elementos` preenchido recursivamente pela mesma função

O campo `_campos_inertes` de um grupo preserva `arranjo`, `distribuicao` e
quaisquer outros campos do dict que não sejam `id`, `tipo`, `elementos`.
O renderizador acessa `grupo._campos_inertes.get("arranjo")` e
`grupo._campos_inertes.get("distribuicao")` para compor os filhos do grupo.

O construtor `construir_modelo` deve invocar a função recursiva para cada
elemento do tipo `grupo` encontrado em `corpo.elementos[]`.

### 14.2 Métodos `elemento_por_id` e `elementos_por_tipo`

Esses métodos permanecem com semântica **plana**: percorrem somente
`self.corpo.elementos` diretos, sem descer na árvore de grupos.

Os contratos ativos e as docstrings atuais não definem se essas buscas devem
ser planas ou recursivas. A implementação existente percorre somente
`self.corpo.elementos`, e o H-0027 deve preservar esse comportamento
observável para não ampliar implicitamente a API pública. O renderizador não
usa esses métodos (acessa `modelo.corpo.elementos` diretamente). A árvore
hierárquica deve ser preservada integralmente no modelo por meio de
`ElementoCorpo.elementos`, sem obrigar esses dois métodos a percorrê-la
recursivamente neste ciclo. Caso a implementação edite o corpo desses métodos
ou a área correspondente em `tela/modelo.py`, as docstrings devem ser
atualizadas para declarar explicitamente o escopo plano preservado: elementos
dentro de grupos são acessíveis via navegação direta da árvore
(`elemento.elementos`), não por esses métodos. Busca recursiva pública,
alteração da semântica desses métodos ou criação de API recursiva permanecem
fora do escopo do H-0027 e dependem de decisão e documentação próprias.

### 14.3 `ElementoCorpo.elementos` para grupos

`ElementoCorpo.elementos` continua sendo a lista de sub-elementos. Para grupos
com múltiplos níveis, essa lista pode conter instâncias de `ElementoCorpo` com
`tipo="grupo"`, que por sua vez têm suas próprias `elementos`. A árvore é
preservada integralmente pelo modelo.

---

## 15. Especificação do renderizador

### 15.1 Princípio de composição recursiva por container

O renderizador deve implementar composição recursiva por container. O padrão:

```
_renderizar_container(arranjo, distribuicao, elementos, borda, largura, altura)
  → para cada elemento:
      se funcional → _caixa_de_elemento(...)
      se grupo    → _renderizar_container(
                        grupo._campos_inertes.get("arranjo"),
                        grupo._campos_inertes.get("distribuicao"),
                        grupo.elementos,
                        borda,
                        largura_alocada_ao_grupo,
                        altura_alocada_ao_grupo
                    )
```

O grupo não gera caixa visual própria. Sua área é preenchida pelos filhos.

### 15.2 Composição vertical do corpo raiz

O comportamento atual dos três ramos verticais do corpo raiz
(sem distribuição, com distribuição vertical, sem altura) permanece.

Para grupos: o ramo atual que itera `elemento.elementos` (linhas 1107–1117 e
1083–1094) precisa ser substituído pelo despacho recursivo. O grupo recebe a
área calculada pelo container pai (cota da distribuição ou dimensão natural) e
a passa integralmente para `_renderizar_container` recursivo com o arranjo e
distribuição próprios do grupo.

### 15.3 Composição horizontal do corpo raiz

O comportamento atual de `_montar_corpo_horizontal` permanece. Para grupos
como filhos diretos do corpo em modo horizontal: o grupo ocupa a largura do
slot que lhe foi alocado (pela distribuição do corpo ou pelo particionamento
uniforme) e renderiza seus filhos com `_renderizar_container` recursivo dentro
dessa largura. O grupo não gera slot vazio — o comportamento atual de "slot
vazio" para grupo horizontal deve ser substituído por composição recursiva.

### 15.4 Composição vertical de grupo interno

Quando um grupo tem `arranjo = "vertical"` (ou `arranjo = None`):

- Se o grupo tiver `distribuicao` declarada: repartir a altura alocada ao grupo
  entre seus filhos diretos usando maiores restos; cada filho recebe `altura_alvo`
  preenchida até a cota
- Se o grupo não tiver `distribuicao`: composição orientada pelo conteúdo;
  cada filho usa sua altura natural

A área total disponível ao grupo é a área que o container pai lhe alocou.

### 15.5 Composição horizontal de grupo interno

Quando um grupo tem `arranjo = "horizontal"` (ou alias `"lado_a_lado"`):

- Se o grupo tiver `distribuicao` declarada: repartir a largura alocada ao grupo
  entre seus filhos diretos usando maiores restos
- Se o grupo não tiver `distribuicao`: particionamento uniforme entre os filhos
  (comportamento análogo ao atual do corpo sem distribuição horizontal)

A lógica de `_montar_corpo_horizontal` pode ser fatorada e reutilizada para
grupos horizontais, com a largura sendo a área alocada ao grupo pelo pai.

### 15.6 Independência entre arranjos de pai e filho

O arranjo do container pai não obriga o arranjo dos grupos filhos. Um grupo
vertical pode conter grupos horizontais e vice-versa. A composição de cada
container usa somente o seu próprio `arranjo` e `distribuicao`.

### 15.7 Distribuição associada somente aos filhos diretos

A distribuição de um container aplica-se somente aos seus filhos diretos.
`len(distribuicao.valores) == len(elementos)` conta somente filhos diretos do
container onde a distribuição está declarada. Filhos de grupos internos não
entram nessa contagem.

### 15.8 Ausência de distribuição em grupos

Quando um grupo não declara `distribuicao`, a construção é orientada pelo
conteúdo dos filhos. Não equivale ao modo `igual` (ADR-0018). O comportamento
é o mesmo que o corpo raiz sem distribuição: cada filho usa sua dimensão
natural.

### 15.9 Múltiplos dashboards

O renderizador não deve impor nem verificar cardinalidade global de `dashboard`.
Cada instância de `dashboard` em qualquer grupo é renderizada como elemento
passivo independente.

---

## 16. Requisitos para múltiplos dashboards

- Nenhuma verificação de cardinalidade global de `dashboard` deve existir no
  loader, no modelo ou no renderizador
- Dois ou mais `dashboard` em grupos distintos da mesma tela devem ser
  renderizados independentemente como elementos passivos
- A natureza passiva de `dashboard` (não navegável por `[✥]`) permanece
  independente da cardinalidade
- Testes com múltiplos dashboards devem ser incluídos (seção 20)

---

## 17. Critérios de diagnóstico

### 17.1 Grupo no nível 4

- Exceção: `TelaGrupoInvalido`
- A mensagem deve ser determinística e incluir:
  - O `id` do grupo que criaria o nível 4
  - O caminho completo dos grupos antecessores
  - Indicação de que o máximo é 3 níveis de grupos
- Não deve ser silenciosamente ignorado nem aceito

### 17.2 Diagnósticos existentes preservados

Os diagnósticos existentes para as seguintes condições devem ser preservados
sem regressão:

- Grupo sem campo `elementos`
- Grupo com `elementos` vazio
- Elemento interno sem `id`
- Elemento interno sem `tipo`
- Elemento interno com tipo desconhecido
- `grupo.distribuicao` inválida (modo inválido, vetor com tamanho errado,
  valores não positivos, soma != 100 para percentual)

### 17.3 Caminho no diagnóstico

Erros em elementos dentro de grupos devem incluir o caminho no grupo onde
o erro foi encontrado, para que o diagnóstico seja localizável sem ambiguidade.

---

## 18. Matriz de cenários hierárquicos

| Cenário | Estrutura | Resultado esperado |
|---|---|---|
| Plano (sem grupos) | `corpo → [console, dashboard, lancador]` | Válido; sem alteração de comportamento |
| 1 nível de grupo | `corpo → grupo1 → [funcional]` | Válido; funcional renderizado no slot do grupo |
| 2 níveis de grupos | `corpo → grupo1 → grupo2 → [funcional]` | Válido; composição recursiva |
| 3 níveis de grupos | `corpo → grupo1 → grupo2 → grupo3 → [funcional]` | Válido; composição recursiva |
| Grupo no nível 4 | `corpo → g1 → g2 → g3 → g4` | TelaGrupoInvalido determinístico |
| Funcionais no nível 3 | `corpo → g1 → g2 → g3 → [dash, console]` | Válido; D3 — não constituem nível 4 |
| Múltiplos filhos no grupo | `grupo → [console, dashboard]` | Válido; D6 |
| Múltiplos grupos irmãos nível 1 | `corpo → [grupo_a, grupo_b]` | Válido; D5 |
| Múltiplos grupos irmãos nível interno | `grupo1 → [grupo2a, grupo2b]` | Válido; D5 |
| Mistura grupo + funcional | `corpo → [console, grupo, dashboard]` | Válido |
| Grupo vertical em corpo vertical | `corpo(v) → grupo(v) → [funcional]` | Válido; arranjos independentes |
| Grupo horizontal em corpo horizontal | `corpo(h) → grupo(h) → [funcional]` | Válido |
| Grupo horizontal em corpo vertical | `corpo(v) → grupo(h) → [f1, f2]` | Válido; D5/D6; arranjos independentes |
| Grupo vertical em corpo horizontal | `corpo(h) → grupo(v) → [f1, f2]` | Válido; arranjos independentes |
| Três níveis com arranjos alternados | `corpo(v) → g1(h) → g2(v) → [funcional]` | Válido |
| Grupo sem distribuição | `grupo → elementos` sem `distribuicao` | Orientado pelo conteúdo; não equivale a `igual` |
| Grupo com distribuição `igual` | `grupo.distribuicao = {modo: "igual"}` | Repartição igual entre filhos diretos |
| Grupo com distribuição `percentual` | `grupo.distribuicao = {modo: "percentual", valores: [...]}` | Maiores restos; soma == 100 |
| Grupo com distribuição `fracao` | `grupo.distribuicao = {modo: "fracao", valores: [...]}` | Maiores restos; pesos positivos |
| Distribuição associada aos filhos diretos | `grupo.distribuicao` com 2 valores, 2 filhos diretos | `len(valores) == len(elementos)` |
| Distribuição com vetor inválido | `len(valores) != len(filhos)` | TelaEstruturaInvalida |
| Múltiplos dashboards na mesma tela | `corpo → [g1 → dash, g2 → dash]` | Válido; D7 |
| Múltiplos dashboards em grupos distintos | `corpo → [g1 → [dash1], g2 → [dash2]]` | Válido; D7 |
| Grupo em nível 4 (caminho exato) | `corpo → g1 → g2 → g3 → g4` | TelaGrupoInvalido com caminho `corpo → g1 → g2 → g3` |

---

## 19. Critérios de aceite

O ciclo H-0027 está concluído quando:

1. `python tela/teste_loader.py` — código de saída 0; todas as suítes aprovadas
2. `python tela/teste_modelo.py` — código de saída 0; todas as suítes aprovadas
3. `python tela/teste_renderizador.py` — código de saída 0; todas as suítes aprovadas
4. `python tela/teste_demo.py` — código de saída 0; todas as suítes aprovadas
5. `git diff --check` — sem saída (sem problemas de espaço em branco)
6. Todos os cenários da seção 18 têm cobertura executável (não apenas unitária)
7. As quatro suítes existentes não regridem em testes que cobrem capacidades
   anteriores não relacionadas à hierarquia de grupos
8. Os quatro testes históricos identificados na seção 6.4 foram substituídos por
   testes coerentes com as regras vigentes (não simplesmente removidos)
9. O relatório `IMP-0028` existe, está preenchido e registra o estado Git final
10. `git diff --cached --stat` — stage vazio ao final

---

## 20. Testes obrigatórios

### 20.1 Testes a substituir (não remover) em `teste_loader.py`

Os quatro testes abaixo validam restrições históricas incompatíveis. Devem ser
**substituídos** por testes positivos coerentes. A cobertura para as restrições
normativas vigentes deve ser criada no mesmo arquivo:

| Teste atual | Substituição obrigatória |
|---|---|
| "grupo com 2 elementos → TelaGrupoInvalido" | Teste positivo: grupo com 2 elementos funcionais é válido |
| "grupo dentro de grupo → TelaGrupoInvalido" | Teste positivo: grupo dentro de grupo (nível 1→2) é válido; adicionar teste de nível 4 → TelaGrupoInvalido |
| "grupo com arranjo 'horizontal' → TelaGrupoInvalido" | Teste positivo: grupo com arranjo horizontal é válido |
| "grupo com arranjo 'lado_a_lado' → TelaGrupoInvalido" | Teste positivo: grupo com arranjo lado_a_lado é válido (alias de horizontal) |

### 20.2 Novos testes obrigatórios em `teste_loader.py`

- Composição plana sem grupos: preservação (já existe, verificar regressão)
- Um nível de grupo com um elemento funcional (preservação de `grupo_minimo`)
- Um nível de grupo com múltiplos elementos funcionais
- Dois níveis de grupos (`g1 → g2 → funcional`)
- Três níveis de grupos (`g1 → g2 → g3 → funcional`)
- Três níveis de grupos com múltiplos funcionais no nível 3
- Rejeição de grupo no nível 4 (`g1 → g2 → g3 → g4`) — `TelaGrupoInvalido` com caminho
- Múltiplos grupos irmãos no nível 1 (`corpo → [ga, gb]`)
- Múltiplos grupos irmãos no nível 2 (`g1 → [g2a, g2b]`)
- Mistura de grupo e funcional no mesmo container (`corpo → [console, grupo]`)
- Grupo com arranjo horizontal válido
- Grupo com arranjo vertical válido
- Grupo com arranjo ausente (válido)
- Grupo com `distribuicao` modo `igual`: válido
- Grupo com `distribuicao` modo `percentual` com soma 100: válido
- Grupo com `distribuicao` modo `fracao` com pesos positivos: válido
- Grupo com `distribuicao` cujo `len(valores) != len(elementos)`: `TelaEstruturaInvalida`
- Grupo com `distribuicao.modo` inválido: `TelaEstruturaInvalida`
- Múltiplos `dashboard` na mesma tela (sem rejeição por cardinalidade global)
- Mensagem determinística para profundidade inválida: verificar que inclui caminho

### 20.3 Novos testes obrigatórios em `teste_modelo.py`

- Construção do modelo com dois níveis de grupos preserva a árvore (`grupo.elementos` recursivo)
- Construção do modelo com três níveis de grupos
- `ElementoCorpo` com `tipo="grupo"` tem `elementos` não vazio com filhos recursivos
- Múltiplos filhos em grupo representados corretamente
- `_campos_inertes` do grupo preserva `arranjo` e `distribuicao`
- `elemento_por_id` e `elementos_por_tipo` permanecem planos (verificar limitação documentada)

### 20.4 Novos testes obrigatórios em `teste_renderizador.py`

- Grupo vertical de nível 1 com um funcional (regressão de `grupo_minimo`)
- Grupo vertical de nível 1 com múltiplos funcionais
- Dois níveis de grupos, corpo vertical, grupos verticais
- Três níveis de grupos, corpo vertical, grupos verticais
- Grupo horizontal de nível 1 com múltiplos funcionais (dois filhos lado a lado)
- Corpo horizontal com dois grupos filhos
- Combinação vertical → horizontal (corpo vertical, grupo nível 1 horizontal)
- Combinação horizontal → vertical (corpo horizontal, grupo nível 1 vertical)
- Três níveis com arranjos alternados (ex.: v → h → v)
- Grupo sem distribuição: orientado pelo conteúdo (sem fallback `igual`)
- Grupo com distribuição `igual`
- Grupo com distribuição `percentual`
- Grupo com distribuição `fracao`
- Distribuição associada somente aos filhos diretos do grupo (não netos)
- Múltiplos grupos irmãos no nível 1 renderizados como blocos separados
- Múltiplos grupos irmãos em nível interno
- Múltiplos dashboards na mesma tela renderizados como elementos passivos independentes
- Múltiplos dashboards em grupos distintos
- Preservação da ordem declarada em grupos com distribuição
- Regressão de distribuição vertical e horizontal do corpo raiz (`igual`, `percentual`, `fracao`)
- Regressão da ausência de distribuição no corpo raiz
- Regressão das telas existentes (`orquestrador`, `grupo_minimo`, `destino_minimo`, `stub_b`)

---

## 21. Comandos exatos das suítes

O executor deve executar as suítes na seguinte ordem:

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
git diff --check
```

Todas as suítes devem retornar código de saída 0 e reportar aprovação integral.
Não fixar contagens absolutas de testes (a quantidade cresce com os novos casos).
Qualquer `FALHOU` é bloqueante.

---

## 22. Relatório de implementação esperado

O executor deve criar o arquivo:

```text
docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md
```

O relatório deve conter:

1. Identificação: handoff, data, commit base, branch
2. Estado Git inicial (verificado conforme seção 2.2)
3. Arquivos alterados (lista exata com breve descrição de cada alteração)
4. Comportamento implementado por camada (loader, modelo, renderizador)
5. Validação de profundidade: como a contagem por nós `grupo` foi implementada
6. Recursão por camada: estratégia de recursão em cada módulo
7. Multiplicidade: como múltiplos filhos e grupos irmãos foram tratados
8. Múltiplos dashboards: confirmação de ausência de restrição global
9. Testes adicionados: lista com nome e breve descrição
10. Testes alterados: lista dos quatro testes históricos e suas substituições
11. Testes executados: saída resumida de cada suíte (com contagem de aprovados)
12. Resultados: código de saída de cada suíte
13. Preservações confirmadas: lista das capacidades anteriores verificadas
14. Limitações conhecidas: incluir que `elemento_por_id` e `elementos_por_tipo`
    permanecem planos (limitação documentada, não bug)
15. Estado Git final: `git status --short`, `git diff --stat`, `git diff --check`,
    `git diff --cached --stat`
16. Bloqueios encontrados: descrever qualquer condição que impediu o cumprimento
    completo do escopo

---

## 23. Condições de bloqueio da implementação

O executor deve parar sem completar a implementação se:

- O estado Git inicial divergir do descrito na seção 2.2 → `BLOCKED_REPOSITORY_STATE`
- Uma regra necessária não estiver definida nas autoridades (e não neste handoff) →
  `ARCHITECTURE_REVIEW_REQUIRED`
- Houver contradição entre ADR-0019 e um contrato que não esteja explicada em
  nenhuma das autoridades → `ARCHITECTURE_REVIEW_REQUIRED`
- A implementação recursiva exigir alteração de ADR, contrato ou nomenclatura →
  `ARCHITECTURE_REVIEW_REQUIRED`
- A implementação não couber nos arquivos permitidos da seção 8 →
  `BLOCKED_SCOPE`
- As suítes não atingirem código de saída 0 após implementação → documentar como
  bloqueio no relatório; não fazer commit

---

## 24. Proibição de commit

O executor **não deve** criar commit neste ciclo.

A preparação e criação do commit são etapas processuais separadas, executadas
após QA aprovado da implementação. Commit criado pelo executor sem autorização
explícita do usuário é violação do processo.

---

## 25. Limite de encerramento

Concluída a implementação e criado o relatório `IMP-0028`, parar.

Não fazer QA da própria implementação.
Não alterar autoridades.
Não preparar commit.
Não gerar o prompt da etapa seguinte.
Não iniciar outro ciclo.

Retornar ao gerente com o resultado.
