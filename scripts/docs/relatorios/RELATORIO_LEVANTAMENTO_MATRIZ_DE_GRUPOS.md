# Relatório de levantamento documental — matriz de grupos

## 1. Identificação

- projeto: `orquestrador_novo`
- raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- branch: `master`
- data: Sun Jul 12 2026
- etapa: LEVANTAMENTO (Etapa única do prompt)
- objetivo: Localizar, comparar e registrar evidências documentais relacionadas à definição de grupo, composição hierárquica, distribuição, alinhamento, grades e matrizes para subsidiar futura tomada de decisão neutra.
- escopo: Levantamento neutro exclusivo, sem alterações substantivas subsequentes, sem alteração de código, contratos ou documentação normativa ativa.

## 2. Estado comprovado de entrada

Os dois últimos ciclos comprovadamente fechados e homologados são:

- **Ciclo H-0026**
  - Capacidade: distribuição horizontal percentual e fracionária
  - Commit final: `40015b6` (`feat: implementa distribuicao horizontal percentual e fracionaria`)

- **Ciclo H-0027**
  - Capacidade: composição hierárquica do corpo com até três níveis de grupos
  - Commit-base do desenvolvimento: `40015b6`
  - Commit final: `c003f3e` (`feat: implementa composicao hierarquica do corpo com tres niveis de grupos`)
  - QA de handoff: `H1_HANDOFF_APPROVED`
  - QA de implementação: `I1_IMPLEMENTATION_APPROVED`
  - Testes: 1004/1004 aprovados (conforme `IMP-0028`)
  - Estado do ciclo: FECHADO

A especificação H-0025 permanece `NAO_CONFIRMADO` e não integra este levantamento.

## 3. Autoridades localizadas

| Arquivo | Tipo | Estado | Autoridade | Relevância |
|---|---|---|---|---|
| `scripts/docs/NOMENCLATURA.md` | Glossário/Nomenclatura | Ativo | Máxima (para nomes e schemas) | Define termos, taxonomias e schemas de JSON de tela (seção 0, 3, 4, 8, 11). |
| `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` | ADR | Ativa (status no arquivo: aceita; índice: aceita; aplicação documental: aprovada; ciclo relacionado: H-0027) | Máxima (para regras de profundidade) | Define limite de 3 níveis de grupos, contagem de profundidade por grupos estruturais e remoção do limite de dashboards. |
| `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` | ADR | Decisão incorporada aos contratos ativos; pendência: divergência textual de status (arquivo: `proposta`; índice: `aceita`) | Máxima (para ausência de distribuição) | Define que a ausência de distribuição do container preserva a construção orientada pelo conteúdo e não equivale a `igual`. QA: `ADR_APPROVED_WITH_NOTES`; aplicação documental: `ADR_APPLICATION_APPROVED_WITH_NOTES`. A divergência de status não anula as decisões normativas incorporadas, mas impede apresentar o status interno como coerente. |
| `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | ADR | Ativa | Máxima (para árvore de composição) | Modelou o corpo como árvore, introduziu o nó estrutural `grupo`, arranjos e distribuições de containers. |
| `scripts/docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` | ADR | Ativa | Máxima (para dashboard no corpo) | Define `dashboard` como elemento funcional do corpo e descontinua `posicao_dashboard` como eixo separado. |
| `scripts/docs/contratos/contrato_composicao_corpo.md` | Contrato | Ativo | Alta (norma de aplicação direta) | Detalha todas as invariantes, regras de layout, taxonomias e critérios de validação do corpo da tela. |
| `scripts/docs/contratos/contrato_tela_json.md` | Contrato | Ativo | Alta (norma de aplicação direta) | Define o schema conceitual e as regras de versionamento, validação e pipeline de renderização da tela. |
| `scripts/docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` | Handoff | Histórico — ciclo FECHADO (status declarado no arquivo: proposto; QA: `H1_HANDOFF_APPROVED`; implementado; commit de fechamento: `c003f3e`) | Média (registro de escopo executado) | Especifica as regras para loader, modelo e renderizador que aplicaram a ADR-0019. QA de implementação: `I1_IMPLEMENTATION_APPROVED`; 1004/1004 testes aprovados. |
| `scripts/docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md` | Relatório | Ativo/Fechado | Baixa (evidência de conformidade) | Registra o escopo executado, testes de regressão passados e o sucesso das 1004 verificações. |

## 4. Definição atual de grupo

- **Definição de grupo:** O `grupo` é definido como o único nó estrutural do corpo da tela. Ele não possui natureza funcional de dados, não é navegável por cursor e não possui conteúdo visual ou moldura próprios. Seu papel é receber uma área alocada pelo container pai e redistribuí-la de forma recursiva entre seus filhos.
- **Autoridade normativa:** `contrato_composicao_corpo.md` seção 3.2:
  > "`grupo` é o único nó estrutural do corpo. Não é tipo funcional. ... não tem borda própria; não tem moldura visual; não tem título visual próprio; não tem conteúdo próprio; não é navegável por `[✥]`; ... recebe uma área do container pai; redistribui essa área entre seus filhos diretos; declara seu próprio `arranjo`; declara sua própria `distribuicao`"
- **Campos JSON do grupo:**
  - `id`: identificador estável (obrigatório).
  - `tipo`: deve ser `"grupo"` (obrigatório).
  - `elementos[]`: lista não vazia de elementos filhos (obrigatório).
  - `arranjo`: opcional.
  - `distribuicao`: opcional.
- **Valores implícitos e ausência de seletor:** Se `arranjo` não for declarado no grupo, herda do tiling global ou do container pai? Conforme `contrato_composicao_corpo.md` R-17:
  > "O arranjo de um container (corpo ou grupo) define o eixo de composição dos seus filhos diretos: arranjo = horizontal organiza os filhos no eixo horizontal; arranjo = vertical organiza os filhos no eixo vertical. O arranjo, sozinho, não reparte nem aloca a dimensão disponível...".
  Quando o seletor `arranjo` está ausente, o renderer usa o campo `tiling` do estilo ativo como default. Se `distribuicao` estiver ausente, ela não se converte em `igual` (ADR-0018); em vez disso, preserva-se o comportamento de "construção orientada pelo conteúdo" (as caixas usam suas dimensões naturais).
- **Existência de seletor estrutural atual:** Atualmente, todos os grupos compartilham do mesmo e único comportamento de grupo (a composição hierárquica recursiva). Não existe seletor declarativo de especialização de comportamento do grupo (ex.: hierárquico versus matricial). O comportamento padrão de grupo hierárquico estrutural recursivo é aplicado em toda a sua extensão.

## 5. Estrutura JSON atual

| Campo | Documento | Obrigatoriedade | Semântica | Evidência |
|---|---|---|---|---|
| `schema` | `contrato_tela_json.md`#4 | Obrigatório | Versão do schema declarativo (ex: `"tela.v1"`) | `"schema": "tela.v1"` |
| `id` | `contrato_tela_json.md`#5 | Obrigatório | Identificador estável do elemento no escopo da tela | `"id": "g1"` |
| `tipo` | `contrato_composicao_corpo.md`#4.1 | Obrigatório | Tipo de elemento do corpo (`console`, `lancador`, `dashboard`, `grupo`) | `tipo: "grupo"` |
| `elementos[]` | `contrato_composicao_corpo.md`#3.2 | Obrigatório | Lista não-vazia de elementos filhos diretos de um container | `"elementos": [...]` |
| `arranjo` | `contrato_composicao_corpo.md`#4.2 | Opcional | Orientação de composição dos filhos (`vertical` \| `horizontal`) | `"arranjo": "vertical"` |
| `distribuicao` | `contrato_composicao_corpo.md`#4.9 | Opcional | Objeto declarando o modo e cotas de alocação de área | `"distribuicao": { "modo": "igual" }` |

## 6. Regras atuais de composição hierárquica

- **Níveis de aninhamento:** A profundidade hierárquica do corpo é limitada a no máximo **três níveis de grupos**, contados exclusivamente pelos nós de tipo `"grupo"`.
- **Contagem de profundidade (ADR-0019 D1):**
  > "nível de grupo 1: grupo que é filho direto de corpo.elementos[]; nível de grupo 2: grupo que é filho direto de um grupo do nível 1; nível de grupo 3: grupo que é filho direto de um grupo do nível 2. O corpo raiz não é contado como nível de grupo. Elementos funcionais ... não acrescentam um novo nível de grupo..."
- **Nível 4 inválido (ADR-0019 D4):** Um grupo filho de um grupo de nível 3 estaria no nível 4 e é estruturalmente inválido. Loader rejeita com erro determinístico `TelaGrupoInvalido` indicando o caminho afetado (ex: `"Grupo 'g4' em 'corpo → g1 → g2 → g3' criaria nivel 4..."`).
- **Quantidade mínima ou máxima de filhos:** O mínimo é 1 filho (elementos[] não pode ser vazio); não há limite superior numérico quantitativo para o número de filhos funcionais ou grupos irmãos.
- **Mistura de grupos e funcionais:** É permitida em qualquer nível. Um grupo no nível 3 pode conter múltiplos elementos funcionais (`console`, `dashboard` ou `lancador`), e o container pai pode misturar grupos irmãos e funcionais na mesma lista de `elementos` (ADR-0019 D5 e D6).
- **Limitações declaradas:** Os métodos `elemento_por_id` e `elementos_por_tipo` em `tela/modelo.py` possuem escopo estritamente plano (não recursivo), varrendo apenas os elementos do primeiro nível. A navegação de grupos internos deve ser feita varrendo a árvore por `grupo.elementos`.
- **Preservações exigidas:** Devem ser mantidas as renderizações de caixas planas sem grupos, o preenchimento de altura disponível para o corpo por meio de linhas em branco do renderizador (ADR-0013, ADR-0017) e o redimensionamento reativo por `SIGWINCH`.

## 7. Regras atuais de distribuição

- **Campos usados:** Objeto `distribuicao` contendo os atributos `modo` e `valores`.
- **Modos de distribuição e semântica:**
  - `igual`: Divide a área útil disponível igualmente entre os filhos diretos (peso idêntico). Só ocorre por declaração explícita.
  - `percentual`: Cotas relativas em porcentagem (`valores[]`). A soma dos valores deve ser exatamente 100 e todos os valores devem ser positivos.
  - `fracao`: Pesos proporcionais livres (`valores[]`). Aceita qualquer vetor de pesos inteiros positivos, onde a cota é `valor / soma_pesos`. O renderizador não pode ser especializado para um vetor fixo (ex: `[2, 1, 2]` é apenas um exemplo de configuração).
- **Correspondência de valores:** `len(distribuicao.valores) == len(elementos)` para o container onde está declarada. Não conta netos.
- **Funcionamento por orientação:**
  - Container vertical: distribui altura útil (linhas).
  - Container horizontal: distribui largura útil (colunas).
- **Arredondamento e restos:** Converte cotas ideais (float) para células de terminal inteiras usando o algoritmo dos maiores restos (Largest Remainder Method). Os resíduos são distribuídos aos maiores restos inteiros. Empates de resto são desambiguados seguindo a ordem original de declaração dos elementos em `elementos[]`.
- **Distribuição por container:** A distribuição é uma propriedade local de cada container (`corpo` ou `grupo`). Não há um conceito de distribuição bidimensional paralela compartilhada (grade 2D em um só container). Mas subgrupos aninhados com orientações alternadas produzem partições combinadas locais.
- **Ausência de distribuição (ADR-0018 D2):** A ausência de `distribuicao` não se converte em `igual`; em vez disso, preserva-se a construção baseada no conteúdo natural de cada filho (cada elemento usa sua dimensão natural).

## 8. Limites atuais

- **Níveis de grupos:** Máximo de 3 níveis de grupos. Nível 4 é inválido.
- **Largura/altura de terminal:** Sempre dinâmicas, respondendo reativamente a `SIGWINCH` sem reinicialização.
- **Terminal pequeno demais:** A ADR-0017 regula que terminais menores que o limite de exibição mínima do quadro devem suspender a exibição normal e renderizar o "quadro mínimo de terminal pequeno" ("terminal pequeno demais"), sem encerrar a sessão TUI e recuperando-se automaticamente ao expandir a janela.
- **Limites de grade/matriz do corpo:** Não existem limites de dimensões de caixas (como 2x2 a 4x4) regulados nos contratos do corpo da tela. Os únicos limites quantitativos referem-se à profundidade máxima (3 níveis de grupos).

## 9. Garantias atuais de alinhamento

- **Alinhamento entre grupos irmãos:**
  - No arranjo vertical: as caixas são dispostas contiguamente, de forma que o topo de uma segue imediatamente a base da anterior, sem linhas em branco externas adicionadas automaticamente pelo compositor (ADR-0015 D9).
  - No arranjo horizontal: as caixas são dispostas por particionamento contíguo. Não existem vãos externos entre molduras adjacentes (molduras coladas, gerando contatos de bordas verticais como `││`, `╮╭`, `╯╰`).
- **Grade comum e divisórias globais:** `NAO_CONFIRMADO`. Não há grade de coordenadas globais compartilhadas ou barramento de divisórias para grupos vizinhos com estruturas distintas. Cada grupo realiza seus cálculos e cortes de área de forma local e encapsulada.
- **Sincronização de cortes de grupos irmãos (contrato_composicao_corpo.md#5.12):** Só é garantida sob condições estritas: mesmo eixo de arranjo, mesma quantidade de filhos, mesma distribuição declarada, mesma dimensão e mesma assinatura de restrições dimensionais (`minimo`, `preferido`, `maximo`, etc.). Caso essas restrições difiram, o alinhamento de divisórias internas não é garantido automaticamente.

## 10. Ocorrências de matriz, grade, linhas, colunas e células

| Termo | Arquivo | Seção | Classificação | Evidência | Observação |
|---|---|---|---|---|---|
| `matriz` | `NOMENCLATURA.md` | 8.2 | `ATIVA` | "### 8.2 Modo matriz" | Refere-se à disposição dos itens do corpo tipo `lancador` preenchidos coluna-a-coluna. |
| `matriz` | `NOMENCLATURA.md` | 4.1 | `ATIVA` | "cima/baixo move dentro da coluna, esquerda/direita move entre colunas" | Refere-se à navegação 2D do cursor no `console` navegável em formato de grade. |
| `matriz` | `contrato_composicao_corpo.md` | 1 | `ATIVA` | "não redefine nem duplica suas regras. ... sem rowspan ou colspan" | Refere-se à composição plana versus bidimensional. Mesclagens e layouts matriciais complexos de caixas do corpo são omitidos. |
| `matriz` | `scripts/docs/adr/ADR-0001-menu-suporta-matriz.md` | — | `ATIVA` | "`menu` suporta modo matriz (múltiplas colunas)" | Refere-se à disposição dos chips de navegação interna do menu/lancador. |
| `grade` | `NOMENCLATURA.md` | 8.2 | `ATIVA` | "dentro de cada coluna da grade, o chip ([R]) alinha à esquerda" | Refere-se à disposição de chip e rótulo de itens do lancador como sub-colunas. |
| `grade` | `NOMENCLATURA.md` | 4.1 | `ATIVA` | "Corpo tipo console em formato de matriz/grade" | Refere-se à geometria 2D do cursor do console. |
| `linhas` / `colunas` | `NOMENCLATURA.md` | 8.3 | `ATIVA` | "Se não couber em uma linha, distribui em matriz" | Refere-se às linhas e colunas de texto de terminal para disposição do lancador. |
| `célula` / `celula` | `NOMENCLATURA.md` | 4.1 | `ATIVA` | "só a última coluna pode ficar incompleta... sem entrar em célula vazia" | Refere-se à célula vazia na navegação toroidal de cursor no console. |
| `rowspan` / `colspan` | `contrato_composicao_corpo.md` | 1 | `ATIVA` | "(ausência inicial de mesclagem de células, rowspan ou colspan)" | Descartado ou adiado intencionalmente na documentação ativa. |
| `matriz` (declarativa de grupo) | — | — | `NAO_CONFIRMADO` | — | Nenhuma definição de matriz de composição de caixas de grupos está documentada na TUI ativa. |

## 11. Precedentes de seleção declarativa de comportamento

Não há no JSON do grupo atual nenhum campo para selecionar entre comportamentos alternativos de grupos. No entanto, o JSON de tela possui precedentes de seleção de comportamentos, modos ou renderizações em outras partes:
- **`corpo.arranjo` e `grupo.arranjo`:** Seleciona entre `"vertical"` e `"horizontal"` (e aliases transicionais `"sobreposto"`, `"lado_a_lado"`) para determinar a orientação de composição de eixos.
- **`distribuicao.modo`:** Seleciona o algoritmo de alocação de cotas de área (`"igual"`, `"percentual"`, `"fracao"`).
- **`console.tipo_exibicao`:** Seleciona o modo de exibição de itens do console (`"normal"` \| `"verboso"`), chaveando o renderizador de modo de visualização.
- **`barra_de_menus.distribuicao`:** Chaveia o modo de alinhamento visual de chips (string `"horizontal"` como alias para o modo objeto `"horizontal_responsiva"`).
- **`ordem.politica`:** Chaveia a forma de ordenação de chips (`"declaracao"` \| `"grupos_declarados"`).

## 12. Análise terminológica neutra

| Termo | Uso atual | Tipo de uso | Conflitos | Disponibilidade documental |
|---|---|---|---|---|
| `livre` / `aberto` | Menções a "schema aberto" e proibição de "lógica livre". | Conceitual / Normativo | Sem conflito direto. | Disponível para indicar comportamento flexível ou não-alinhado. |
| `hierarquico` | Refere-se à árvore de grupos atual e aninhamento limitado. | Estrutural / Normativo | Sem conflito. Já identifica a árvore atual. | Não disponível para novos conceitos (já é a palavra canônica para a árvore padrão). |
| `matriz` | Disposição de itens do lancador (coluna-a-coluna) e cursor de console. | Disposição interna / Navegação | Possui conflito potencial com a disposição interna do lancador. | Parcialmente disponível se qualificada (ex: "comportamento matriz de grupo"). |
| `grade` | Navegação de cursor de console e alinhamento de chip/rótulo de lancador. | Geometria interna / Cursor | Similar ao de `matriz`. | Parcialmente disponível se qualificada (ex: "comportamento grade de grupo"). |
| `estrutura` | Usado conceitualmente ("erro estrutural", "estrutura macro"). | Abstrato / Diagnóstico | Sem conflito direto. Não é campo JSON. | Disponível como campo de seletor declarativo no JSON do grupo. |
| `comportamento` | Usado de forma descritiva na documentação e relatórios. | Descritivo / Abstrato | Sem conflito direto. Não é campo JSON. | Totalmente disponível como campo de seletor declarativo no JSON do grupo. |
| `modo` | Usado em `distribuicao.modo` e `tipo_exibicao`. | Palavra-chave JSON | Conflito se usado solto, pois já possui escopo restrito em distribuição. | Disponível se aninhado ou qualificado. |
| `tipo` | Define tipo de elemento do corpo (`"console"`, `"grupo"`, etc.). | Palavra-chave JSON | Alto conflito se usado para selecionar comportamento interno do grupo. | Não disponível (já possui uso estrutural chaveado no loader). |
| `arranjo` | Define a orientação de filhos em container (`vertical`/`horizontal`). | Palavra-chave JSON | Alto conflito. Define estritamente o eixo do container. | Não disponível para uso como seletor geral. |

## 13. Compatibilidade e validação atuais

- **Regulamentação de novos campos:** Os novos campos devem ser opcionais e integrados ao pipeline de validação de schema. Nenhum campo de seletor declarativo de comportamento de grupo existe hoje; todos os grupos seguem o comportamento hierárquico recursivo atual. Não existe, portanto, fallback entre `hierárquico` e outro comportamento de grupo — há apenas um comportamento vigente. A preservação do comportamento atual quando um futuro seletor estiver ausente é uma decisão candidata ainda não formalizada em ADR.
- **Validação antes da renderização:** Toda tela declarada por JSON é processada e validada pelo loader antes de ser montada no modelo e enviada ao renderizador (`contrato_tela_json.md` seções 22 e 25).
- **Tratamento de ausência e defaults:** O loader de tela valida a tipagem e estrutura. Se um grupo omitir a distribuição, ela é válida e dispara o comportamento de tamanho natural dos dados. Se o arranjo for omitido, o renderer busca o default de tiling no estilo ativo.
- **Rejeição de campos inválidos:** Configurações que firam as restrições ativas (como soma de percentuais != 100, pesos negativos, ou profundidade de grupo ≥ 4) são ativamente rejeitadas no loader com exceções do tipo `TelaGrupoInvalido` ou `TelaEstruturaInvalida`, sem fallbacks silenciosos (R-22 do contrato de composição).
- **Compatibilidade retroativa de JSONs:** Os arquivos JSON legados (`orquestrador.json`, `grupo_minimo.json`, `destino_minimo.json`, `stub_b.json`) são carregados e validados perfeitamente sob as regras do H-0027, e o renderizador monta suas saídas sem alterações ou perdas.

## 14. Documentos potencialmente afetados

Caso uma futura proposta de especialização de grupo matriz seja formalizada por uma ADR, os seguintes documentos normativos ativos seriam impactados:

| Documento | Ação potencial | Motivo | Evidência | Dependências |
|---|---|---|---|---|
| `scripts/docs/NOMENCLATURA.md` | `ATUALIZAR` | Adicionar os termos e definições do grupo tipo matriz (linhas, colunas, células, limites de tamanho, alinhamento de divisórias). | Seção 3 e seção 11 registram os nós estruturais e limites vigentes de grupos. | Nova ADR aprovada. |
| `scripts/docs/contratos/contrato_composicao_corpo.md` | `ATUALIZAR` | Especificar as regras de layout de caixas da matriz, cálculo de divisórias e vãos de células, ordem de preenchimento, e validação de terminal pequeno. | Seções 3.2, 5.12 e R-15 especificam o papel do grupo e limitações de alinhamento. | Nova ADR aprovada. |
| `scripts/docs/contratos/contrato_tela_json.md` | `ATUALIZAR` | Adicionar os novos campos de especialização de comportamento e as propriedades de grade (linhas, colunas) ao schema da tela. | Seção 8 registra o elemento `grupo` e suas propriedades declarativas. | Contrato de composição atualizado. |
| `scripts/docs/contratos/contrato_json_tela_minima.md` | `ATUALIZAR` | Integrar as regras de validação declarativa do JSON mínimo para aceitar os campos da matriz de grupos. | Seção 6.2/6.3 registra as regras e validações do corpo. | Contrato de composição atualizado. |
| `scripts/docs/adr/INDICE_ADR.md` | `ATUALIZAR` | Registrar a nova ADR de matriz de grupos na tabela de decisões arquiteturais registradas. | Tabela de decisões aceitas da seção 28. | Nova ADR aceita. |

## 15. Contradições documentais

- **Status da ADR-0018:** Existe um desalinhamento documental conhecido (achado ACH-008 do H-0027) entre o índice de ADRs (`scripts/docs/adr/INDICE_ADR.md` linha 48) que cataloga a ADR-0018 como `aceita` e o cabeçalho do arquivo `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` linha 6 que a declara com `status: proposta`.
- **Ausência de contradições ativas de profundidade:** A ambiguidade sobre a profundidade no nível 3 (ACH-007) e a cardinalidade global de dashboards (ACH-009) foram sanadas e reconciliadas com a ADR-0007, ADR-0010 e ADR-0015 no ciclo H-0027, unificando a contagem de profundidade exclusivamente nos nós estruturais `grupo`.

## 16. Lacunas documentais

Não existem na documentação normativa ativa regras ou definições para:
1. **Comportamentos especializados de grupo:** Não há especificação de múltiplos comportamentos para o nó estrutural `grupo`; todos operam de forma uniforme como árvore hierárquica recursiva.
2. **Nomenclatura do comportamento hierárquico:** O comportamento atual do grupo não possui um nome ou identificador normativo próprio (é referido apenas como "grupo" ou "hierarquia").
3. **Seletor declarativo de comportamento de grupo:** Ausência de campos para chaveamento declarativo de comportamentos estruturais de grupo no JSON da tela.
4. **Matriz declarativa de grupos (posição 2D):** Não há regras para criação de matriz bidimensional declarativa de caixas funcionais no corpo.
5. **Propriedades de linhas, colunas e células de grupo:** Ausência de parâmetros para definir e validar dimensões de matriz (tais como limites 2x2 a 4x4) ou o preenchimento de suas células.
6. **Ordem de preenchimento de células de grupo:** Não há definição sobre o fluxo de preenchimento (linha-a-linha versus coluna-a-coluna) para múltiplos elementos em grade bidimensional de caixas do corpo.
7. **Distribuição independente por eixos na matriz:** Ausência de schema ou algoritmo para processar distribuições de linhas e de colunas simultaneamente em um container.
8. **Aninhamento dentro de células de matriz:** Ausência de regras sobre a permissão ou proibição de declarar subgrupos dentro de células de uma matriz.
9. **Alinhamento e divisórias compartilhadas de matriz:** Não há especificação sobre o alinhamento perfeito de bordas e divisórias das células vizinhas, compartilhamento de coordenadas ou uma grade 2D global de composição.
10. **Tratamento de terminal pequeno na matriz:** Ausência de limites de terminal pequeno específicos para a integridade de uma matriz (por exemplo, quando o terminal é menor do que as dimensões de células mínimas exigidas por uma matriz 4x4).
11. **Mesclagem de células (`rowspan`/`colspan`):** Atualmente é uma lacuna intencional e descartada na composição do corpo ("sem mesclagem de células, rowspan ou colspan").

## 17. Decisões ainda necessárias do usuário

Para que um estudo preliminar ou ADR sobre matriz de grupos possa ser formalizado no futuro, as seguintes decisões do usuário precisam ser estabelecidas:
- **Escolha do termo declarativo:** Qual termo (ex: `comportamento` ou `estrutura`) será adotado para o seletor declarativo de comportamento do grupo e qual será a palavra canônica para designar o comportamento hierárquico atual.
- **Formato de declaração das dimensões da matriz:** Como as dimensões (2x2 a 4x4) serão expressas no JSON (ex.: `"colunas": 4, "linhas": 2` ou um array compactado).
- **Mecanismo de preenchimento:** Se a ordem de posicionamento dos elementos filhos nas células seguirá o fluxo por linha (horizontal) ou por coluna (vertical).
- **Distribuição bidimensional por eixo:** Como declarar e parametrizar as distribuições de cotas para as linhas e as colunas de forma independente no mesmo grupo.
- **Aninhamento e células vazias:** Se células vazias são permitidas na matriz (e qual seu preenchimento visual), e se grupos hierárquicos ou outras matrizes podem ser aninhados dentro das células.
- **Layout de divisórias comuns e alinhamento:** Se o renderizador garantirá o alinhamento perfeito de divisórias por uma grade geométrica comum compartilhada, ou se as células adjacentes herdam as coordenadas do container principal.
- **Validação de terminal pequeno na matriz:** Qual será a política de tamanho limite e comportamento de erro do renderizador quando a largura ou altura do terminal/container pai for menor que o espaço mínimo exigido pela matriz.

## 18. Evidências não confirmadas

As seguintes afirmações/regras permanecem com o status `NAO_CONFIRMADO` por ausência de evidência documental normativa ou contratual ativa:
- **Garantias de alinhamento de divisórias entre grupos irmãos independentes:** Não há garantia de alinhamento perfeito ou grade comum global documentada para divisórias de grupos distintos.
- **Comportamento de mesclagem de células de grupo (`rowspan`/`colspan`):** Sem qualquer confirmação normativa (atualmente descartado).
- **Limite quantitativo de 4x4 ou restrição mínima de 2x2 para composição:** Não há evidência dessa faixa de limites numéricos nos contratos vigentes.
- **Seletor declarativo de comportamento de grupo preexistente:** Não há evidência de nenhum campo JSON ou estrutura funcional para selecionar comportamento do grupo no loader ou renderizador atuais.

## 19. Conclusão factual

A documentação e a implementação atuais cobrem composição hierárquica recursiva com até três níveis de grupos, conforme as autoridades e evidências listadas. O ciclo H-0027 está fechado (commit `c003f3e`); o ciclo H-0026 está fechado (commit `40015b6`). 1004/1004 verificações aprovadas conforme `IMP-0028`.

O grupo atual é inteiramente uniforme, seguindo o arranjo unidimensional local (`vertical` ou `horizontal`) e distribuindo suas cotas de área de forma contígua através de algoritmos de maiores restos.

Conceitos bidimensionais como matriz declarativa, grade de divisórias perfeita compartilhada, linhas e colunas de grupos, células e mesclagens de caixas do corpo permanecem **inexistentes** e **lacunas normativas completas** na documentação ativa. A introdução de uma especialização de grupo matriz exigirá a criação de uma ADR para formalizar essas lacunas e regras, afetando diretamente a `NOMENCLATURA.md` e os contratos de composição de corpo, de JSON de tela e do JSON mínimo.

A divergência textual de status da ADR-0018 (arquivo: `proposta`; índice: `aceita`) é uma pendência documental localizada e separada, registrada na seção 15. Não existe hoje seletor declarativo de comportamento de grupo, schema matricial, linhas, colunas ou células documentados nos contratos ativos. Nenhuma dessas decisões foi formalizada em ADR.
