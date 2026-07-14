# RELATORIO_QA_ADR-0019

## 1. Identificação

- Artefato auditado: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- Categoria processual executada: `QA_ADR`
- Auditor: agente formal de QA da ADR-0019
- Data: 2026-07-12
- Branch: `master`
- Commit base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Evidência de origem: `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`

## 2. Objetivo

Auditar formalmente a ADR-0019 verificando se ela registra fielmente as decisões
explícitas do usuário D1 a D7, sem introduzir decisões novas, sem omitir consequências
necessárias e sem aplicar prematuramente a decisão aos demais documentos. O QA não
corrige a ADR, não a aplica, não altera contratos, nomenclatura, índices, código ou
testes. O único artefato produzido é este relatório.

## 3. Estado Git inicial

Comandos executados a partir de `scripts/` (raiz do repositório efetiva para os
caminhos declarados; toplevel Git em `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`).

```text
git rev-parse --show-toplevel
  /home/tiago/Dropbox/UFRGS/Survey/versao_0_1

git status --short
  ?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  ?? tela/__pycache__/

git diff --stat                   (sem saída)
git diff --name-only              (sem saída)
git diff --check                  (sem saída)
git diff --cached --stat          (sem saída)
git diff --cached --name-only     (sem saída)
git log --oneline -1
  40015b6 feat: implementa distribuicao horizontal percentual e fracionaria
```

Estado confirmado: stage vazio, nenhuma alteração rastreada, três entradas não
rastreadas (ADR-0019, relatório de levantamento, `tela/__pycache__/`). Coincide com o
estado comprovado informado pelo executor.

## 4. Artefatos consultados

Autoridades normativas (leitura integral, sem alteração):

- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/adr/ADR-0007-tela-processamento-composicao.md` (leitura adicional necessária
  para verificar D7 — ver seção 10 e achado QA-001)
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`

Artefato principal do QA (leitura integral):

- `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`

Evidência de origem (leitura integral):

- `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`

Inspeção adicional por `git diff --no-index /dev/null` confirmando ADR-0019 como arquivo
novo não rastreado.

Buscas de evidência via `rg` para localizar todas as ocorrências de "zero ou um
dashboard" e da definição de nível nas autoridades.

Implementação e testes não foram usados como fonte de arquitetura; as citações de
linhas de `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py` e
`tela/teste_loader.py` existentes na ADR-0019 foram tratadas apenas como descrição do
estado atual para consequência futura, não como autoridade normativa.

## 5. Decisões D1 a D7

### D1 — Contagem por níveis de grupos

Registrada na seção "D1 — O limite hierárquico é contado por níveis de grupos"
(`ADR-0019:103-130`). A formulação é fiel: a profundidade é contada exclusivamente por
níveis de grupos (nós estruturais `grupo`), não por listas `elementos[]` aninhadas;
o corpo raiz não conta como nível de grupo; elementos funcionais não acrescentam nível
de grupo. A ADR define o nível de grupo 1, 2 e 3 em bloco de código
(`ADR-0019:111-120`) coincidente com a definição do usuário. A ADR explicita que esta
decisão substitui a leitura operacional anterior.

### D2 — Profundidade máxima

Registrada em "D2 — Profundidade máxima de três níveis de grupos"
(`ADR-0019:134-145`), com apoio do bloco de definição de níveis em D1. A ADR mantém o
limite três, agora contado em níveis de grupos; declara válido o grupo de nível 3 e
inválido o grupo de nível 4. A validação futura deverá distinguir profundidade de
grupos de profundidade genérica de listas, sem definir texto de mensagem nem
implementar.

### D3 — Conteúdo funcional no terceiro grupo

Registrada em "D3 — Elementos funcionais dentro de um grupo do nível 3"
(`ADR-0019:149-159`). A ADR afirma que grupo de nível 3 pode conter um ou mais
elementos funcionais do conjunto permitido (`console`, `lancador`, `dashboard`); não
pode conter outro `grupo`; e que elementos funcionais não constituem nível 4 de grupo,
aplicando a regra de contagem da D1.

### D4 — Proibição do quarto grupo

Registrada em "D4 — Proibição de grupo no nível de grupo 4 ou superior"
(`ADR-0019:163-170`). A ADR declara estruturalmente inválido o `grupo` filho de grupo
do nível 3; estruturas com grupo no nível 4 ou superior devem ser rejeitadas com erro
estrutural determinístico; a forma exata do erro é decisão de implementação futura,
registrando apenas a proibição normativa.

### D5 — Multiplicidade de grupos irmãos

Registrada em "D5 — Multiplicidade de grupos irmãos" (`ADR-0019:174-183`). A ADR
permite múltiplos grupos irmãos em qualquer nível permitido; declara que o sistema não
limita cada nível a um único grupo; afirma que esta ADR não introduz cardinalidade
máxima para quantidade de grupos irmãos.

### D6 — Multiplicidade de elementos funcionais

Registrada em "D6 — Multiplicidade de elementos funcionais dentro de grupos"
(`ADR-0019:187-204`). A ADR permite mais de um elemento funcional por grupo, inclusive
no nível 3; declara inexistente a regra geral de "exatamente um elemento funcional por
grupo"; lista regras já existentes (ordem declarada, filhos diretos como unidade de
distribuição, arranjo, distribuição, associação posicional) que permanecem em vigor,
sem reescrevê-las nem aplicá-las aos contratos nesta etapa.

### D7 — Remoção da cardinalidade global de dashboard

Registrada em "D7 — Remoção da cardinalidade global de um dashboard por tela"
(`ADR-0019:208-232`). A ADR remove "zero ou um dashboard por tela" como regra global do
tipo; permite mais de um dashboard na mesma tela, inclusive em grupos diferentes;
afirma não criar cardinalidade máxima substituta; preserva natureza passiva,
navegabilidade, comportamento de `[✥]`, arranjo, distribuição, estrutura interna e
regras específicas de telas concretas com apenas um dashboard.

## 6. Matriz de cobertura das decisões

| Decisão | Cobertura na ADR | Evidência por linha | Resultado |
| ------- | ---------------- | ------------------- | --------- |
| D1 — contagem por níveis de grupos | Registrada em seção própria | `ADR-0019:103-130` | FIEL |
| D2 — profundidade máxima três níveis de grupos | Registrada em seção própria; definição dos níveis em D1 | `ADR-0019:111-120`, `134-145` | FIEL |
| D3 — conteúdo funcional no nível 3 | Registrada em seção própria | `ADR-0019:149-159` | FIEL |
| D4 — proibição do quarto grupo | Registrada em seção própria | `ADR-0019:163-170` | FIEL |
| D5 — multiplicidade de grupos irmãos | Registrada em seção própria | `ADR-0019:174-183` | FIEL |
| D6 — multiplicidade de elementos funcionais | Registrada em seção própria | `ADR-0019:187-204` | FIEL |
| D7 — remoção da cardinalidade global de dashboard | Registrada em seção própria | `ADR-0019:208-232` | FIEL |

Todas as sete decisões estão registradas, com formulação fiel, sem omissão de
conteúdo, sem ampliação normativa, sem restrição não autorizada e sem transformação
indevida em detalhe de implementação.

## 7. Análise de autoridade

A ADR-0019 cita corretamente as autoridades de origem:

- ADR-0015, Decisão 3, linhas 93-103 — definia `corpo.elementos[]` como nível 1 e
  `grupo.elementos[]` como criador do próximo nível. Confirmado em
  `ADR-0015:93-103`.
- `contrato_composicao_corpo.md:132-137` — definição de nível e profundidade máxima.
  Confirmado.
- `contrato_composicao_corpo.md:87-89` — presença "Zero ou um por tela" do
  `dashboard`. Confirmado em `contrato_composicao_corpo.md:89`.
- `RELATORIO_LEVANTAMENTO...:287-295` (ACH-007) e `:306-313` (ACH-009). Confirmados.
- `RELATORIO_LEVANTAMENTO...:297-304` (ACH-008 — divergência de status da ADR-0018).
  Confirmado.

A ADR-0019 preserva a hierarquia: as decisões D1-D7 são registradas como decisões
explícitas do usuário; a ADR não escolhe arquitetura adicional, não completa lacunas e
não introduz regras além das enunciadas (`ADR-0019:97-99`). Implementação e testes não
foram usados como fonte de arquitetura; as citações de `tela/*.py` aparecem somente na
seção de consequências futuras, como descrição do estado divergente atual.

A divergência de status da ADR-0018 (índice `aceita` × arquivo `proposta`) é
registrada como pendência documental separada (`ADR-0019:422-428`), sem ser corrigida
ou decidida pela ADR-0019. Correto.

## 8. Análise de terminologia e profundidade

A ADR distingue claramente:

- **corpo raiz**: "O corpo raiz não é contado como nível de grupo" (`ADR-0019:122`).
- **nível de grupo**: definido em D1 como aninhamento de nós estruturais `grupo`
  (`ADR-0019:109-120`).
- **lista `elementos[]`**: referida como unidade que NÃO cria nível por si só
  (`ADR-0019:105-107`, `128-130`).
- **elemento estrutural**: "nós estruturais do tipo `grupo`" (`ADR-0019:106`).
- **elemento funcional**: "`console`, `lancador`, `dashboard`" (`ADR-0019:124`).
- **profundidade de grupos** × **profundidade genérica da árvore**: "A validação futura
  deverá distinguir a profundidade de grupos da profundidade genérica de listas
  `elementos[]`" (`ADR-0019:142-143`).

A ADR não propaga a regra antiga segundo a qual cada `grupo.elementos[]` cria
necessariamente um novo nível hierárquico no limite; pelo contrário, D1 substitui
explicitamente essa leitura (`ADR-0019:128-130`).

Está explícito que:

- grupo do nível 3 pode conter elementos funcionais (`ADR-0019:151-154`);
- elementos funcionais não criam nível de grupo (`ADR-0019:124-126`, `157-159`);
- grupo dentro de grupo de nível 3 é inválido (`ADR-0019:155`, `165-166`).

Observação terminológica (não bloqueante): a ADR usa "substitui a leitura operacional
anterior" em D1 (`ADR-0019:128`) e "especializa a regra de contagem" na "Relação com
ADR-0015" (`ADR-0019:401`) para descrever a mesma mudança. Os termos são
reconciliáveis, mas a inconsistência poderia sugerir ambiguidade entre substituição e
especialização da ADR-0015. Ver achado QA-003.

Observação adicional (não bloqueante): `docs/NOMENCLATURA.md` seção 14
(`NOMENCLATURA.md:1140-1206`) utiliza numeração distinta (corpo raiz = nível 0) e
afirma "Nível 3 proibido na versão atual — estruturas com profundidade ≥ 3 são
rejeitadas" (`NOMENCLATURA.md:1154-1155`), o que é mais restritivo que a ADR-0015 e
contraditório com a D2 da ADR-0019. A ADR-0019 identifica NOMENCLATURA para revisão
(`ADR-0019:439`), mas a nota de consequência não sinaliza a gravidade específica dessa
formulação. Ver achado QA-004.

## 9. Análise de multiplicidade

A ADR:

- permite múltiplos grupos irmãos em qualquer nível permitido (`ADR-0019:176-181`);
- permite múltiplos elementos funcionais por grupo, inclusive no nível 3
  (`ADR-0019:189-194`);
- não exige um único grupo por nível (`ADR-0019:179-181`);
- não exige exatamente um filho por grupo (`ADR-0019:192-194`);
- não cria quantidade mínima obrigatória de grupos para toda tela (escopo negativo:
  `ADR-0019:452` "cardinalidade mínima de grupos por tela");
- não obriga toda composição a usar os três níveis (escopo negativo:
  `ADR-0019:453` "obrigação de existirem todos os três níveis em toda tela").

Sem defeitos nesta dimensão.

## 10. Análise da cardinalidade de dashboard

A ADR:

- remove somente a cardinalidade global de um dashboard por tela (`ADR-0019:210-211`);
- permite múltiplos dashboards na mesma tela, inclusive em grupos diferentes
  (`ADR-0019:215-216`);
- não cria nova cardinalidade máxima (`ADR-0019:218`);
- não altera navegação, passividade ou estrutura interna (`ADR-0019:220-228`);
- distingue regra global do tipo de configuração de uma tela concreta
  (`ADR-0019:227-228`, `378-380`).

Identificação de documentos que contêm a restrição antiga:

- `contrato_composicao_corpo.md:89` — identificado pela ADR (`ADR-0019:51`, `436`).
  Confirmado.
- `NOMENCLATURA.md:235` e `:249` — presentes no contexto de "tela de processamento".
  NOMENCLATURA está na lista de documentos a revisar (`ADR-0019:439`), cobrindo
  genericamente a cardinalidade de dashboard por D7 (`ADR-0019:318-320`).
- `docs/adr/ADR-0007-tela-processamento-composicao.md:71` e `:123` — contêm "zero ou
  um `dashboard`" no ponto de decisão 3 e no exemplo de composição de tela de
  processamento. **A ADR-0019 não identifica ADR-0007 em nenhuma seção de
  consequências documentais nem inclui uma seção "Relação com ADR-0007".** A ADR-0019
  possui "Relação com ADR-0010", "Relação com ADR-0015" e "Relação com ADR-0018", mas
  não com ADR-0007. Ver achado QA-001.

A D7 estabelece "uma tela pode conter mais de um dashboard" como permissão global e
preserva apenas "regras específicas de uma tela concreta" (`ADR-0019:227-228`).
ADR-0007 estabelece "zero ou um `dashboard`" para telas de processamento (um tipo de
tela, não uma tela concreta). A relação entre a D7 e ADR-0007 não é esclarecida: não
se sabe se a formulação de ADR-0007 está suprimida pela D7 (regra global do tipo
removida) ou preservada como política particular (exceção da D7). Esta lacuna é um
defeito corrigível na própria ADR.

## 11. Análise dos exemplos

A ADR apresenta exemplos conceituais (`ADR-0019:238-239`), sem inventar campos JSON e
sem se apresentar como schema completo:

- três níveis de grupos com múltiplos elementos funcionais no nível 3
  (`ADR-0019:241-256`) — dois elementos funcionais no grupo de nível 3, coerente com
  D3 e D6;
- múltiplos grupos irmãos (`ADR-0019:258-268`) — dois grupos nível 1 e um elemento
  funcional misturados no corpo, coerente com D5;
- múltiplos dashboards em grupos distintos (`ADR-0019:270-283`) — dois dashboards em
  dois grupos nível 1, coerente com D7;
- grupo de nível 4 inválido (`ADR-0019:285-296`) — coerente com D4.

Os exemplos não contradizem as decisões, não criam cardinalidades novas e não
transformam exemplo em obrigação normativa geral. A ADR ainda contém o exemplo visual
conceitual herdado do levantamento apenas como contexto, sem caráter normativo.

Observação (não bloqueante): não existe exemplo explícito de mais de um dashboard no
mesmo grupo (apenas em grupos distintos). A D7 não exige esse exemplo e "inclusive em
grupos diferentes" admite ambos os arranjos, mas o exemplo único cobre apenas o caso
em grupos distintos.

## 12. Relação com ADRs anteriores

- **ADR-0010** (`ADR-0019:384-393`): a ADR-0019 declara-se coerente com ADR-0010 e
  afirma que a remoção da cardinalidade global reforça que `dashboard` segue o
  mecanismo geral de composição. ADR-0010 permanece vigente em todos os demais pontos.
  Correto.
- **ADR-0015** (`ADR-0019:397-408`): a ADR-0019 "especializa" a regra de contagem de
  nível da ADR-0015; a ADR-0015 permanece vigente em todos os demais pontos; a ADR-0019
  não reescreve nem cancela ADR-0015. A mudança da contagem (de "toda `elementos[]`
  cria nível" para "somente aninhamento de `grupo` cria nível") está corretamente
  atribuída. Ver observação QA-003 sobre o par "substitui"/"especializa".
- **ADR-0018** (`ADR-0019:412-418` e `422-428`): a ADR-0019 não altera ADR-0018; a
  divergência de status da ADR-0018 (índice `aceita` × arquivo `proposta`,
  ACH-008 do levantamento) é tratada como pendência documental separada, não decidida
  nem corrigida pela ADR-0019. Correto.
- **ADR-0007**: ausente. A ADR-0019 não contém seção "Relação com ADR-0007", embora
  ADR-0007 contenha "zero ou um `dashboard`" diretamente relevante à D7. Ver achado
  QA-001.

A divergência de status da ADR-0018 permanece como pendência documental separada,
conforme exigido. A ADR-0019 não corrige nem decide o status da ADR-0018. Correto.

## 13. Consequências documentais

A ADR identifica para aplicação futura (sem aplicar):

- `docs/contratos/contrato_composicao_corpo.md` (`ADR-0019:436`)
- `docs/contratos/contrato_tela_json.md` (`ADR-0019:437`)
- `docs/contratos/contrato_json_tela_minima.md` (`ADR-0019:438`)
- `docs/NOMENCLATURA.md` (`ADR-0019:439`)
- `docs/adr/INDICE_ADR.md` (`ADR-0019:440`)

Os cinco documentos estão também em `contratos_afetados` do frontmatter
(`ADR-0019:12-17`).

Defeito identificado: `docs/adr/ADR-0007-tela-processamento-composicao.md` (status
`aceita`) contém "zero ou um `dashboard`" no ponto de decisão 3
(`ADR-0007:71`) e no exemplo (`ADR-0007:123`), formulação diretamente afetada pela D7,
e não está identificado nas consequências documentais da ADR-0019. Ver achado QA-001.

Não foi identificado outro documento normativo (contrato ou nomenclatura) além dos já
listados que exija necessariamente inclusão. `contrato_processo_desenvolvimento.md`
não é afetado por D1-D7 (a ADR não altera regras processuais). Os contratos
`contrato_lancador.md`, `contrato_console.md`, `contrato_barra_de_menus.md`,
`contrato_estilo.md` e `contrato_json_dashboard.md` não contêm a regra de
cardinalidade global de dashboard nem a definição de nível de grupo, e portanto não
exigem inclusão.

Relatórios históricos (incluindo o `RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`)
não são normativos e não exigem alteração como aplicação normativa; a ADR-0019 não os
altera, corretamente.

## 14. Escopo negativo

A ADR declara explicitamente fora de escopo (`ADR-0019:444-468`):

- textos exatos de mensagens de erro;
- implementação de validação, loader, modelo ou renderizador;
- alteração de testes;
- cardinalidade máxima de grupos irmãos por nível;
- cardinalidade mínima de grupos por tela;
- obrigação de existirem todos os três níveis em toda tela;
- obrigação de todo grupo conter outro grupo;
- cardinalidade mínima ou máxima geral de elementos funcionais por grupo;
- política de mistura além das autoridades ativas;
- nova regra de distribuição, arredondamento, dimensão ou overflow;
- novo formato de erro;
- nova estrutura interna de `dashboard`;
- limites específicos por tipo funcional;
- comportamento de renderização;
- estratégia de implementação;
- correção da divergência de status da ADR-0018;
- atualização do índice de ADRs;
- alteração de qualquer contrato ou nomenclatura;
- criação de handoff;
- preparação de commit.

Todos os itens exigidos pelo roteiro de QA estão presentes. A "estratégia de recursão
no código" é coberta por "estratégia de implementação" e "comportamento de
renderização". Sem defeitos nesta dimensão.

## 15. Metadados e ausência de aplicação prematura

- ID correto `ADR-0019` (`ADR-0019:2`, `21`).
- Título coerente: "Profundidade contada por aninhamento de grupos, multiplicidade
  estrutural e remoção da cardinalidade global de dashboard" (`ADR-0019:21`).
- Status `proposta` (`ADR-0019:6`, `25`) — adequado para ADR criada mas ainda não
  aprovada.
- `substitui: null` (`ADR-0019:8`) — coerente com o tratamento de "especialização" e
  com o padrão observado na ADR-0018 (que também substitui parcialmente ADR-0015 e
  mantém `substitui: null`).
- `handoffs_bloqueados: []` (`ADR-0019:18`) — a ADR não bloqueia handoff específico;
  apropriado, pois a ADR-0019 não endereça um handoff particular como a ADR-0015 fez
  com H-0019.
- Ausência de afirmação de aplicação concluída: "Esta ADR não altera código, testes,
  JSON de tela, contratos, nomenclatura, handoffs, relatórios, índice de ADRs, estado
  operacional ou histórico Git. Cria somente este arquivo." (`ADR-0019:511-514`).
- Ausência de atualização antecipada do índice: `INDICE_ADR.md` não foi modificado
  (confirmado por `git status`); a ADR lista a atualização do índice como consequência
  futura (`ADR-0019:440`, `465`, `489`).
- Ausência de alteração de arquivos existentes: confirmado por `git diff --stat` vazio
  e `git diff --cached --stat` vazio.

Sem defeitos de metadados ou aplicação prematura.

## 16. Achados

### QA-001

- ID: `QA-001`.
- Severidade: média.
- Categoria: `CONSEQUENCIA_DOCUMENTAL_INCOMPLETA`.
- Descrição: A ADR-0019 não identifica `docs/adr/ADR-0007-tela-processamento-composicao.md`
  (status `aceita`) nas consequências documentais da D7, embora ADR-0007 contenha
  "zero ou um `dashboard`" no ponto de decisão 3 e no exemplo de composição de tela de
  processamento. A ADR-0019 possui seções de relação com ADR-0010, ADR-0015 e
  ADR-0018, mas não com ADR-0007. A D7 estabelece "uma tela pode conter mais de um
  dashboard" como permissão global e preserva apenas "regras específicas de uma tela
  concreta"; ADR-0007 estabelece "zero ou um `dashboard`" para telas de processamento
  (um tipo de tela, não uma tela concreta). A relação entre D7 e ADR-0007 não é
  esclarecida: não se sabe se a formulação de ADR-0007 está suprimida pela D7 (regra
  global do tipo removida) ou preservada como política particular (exceção da D7).
- Decisão ou autoridade afetada: D7; ADR-0007; `ADR-0007:71`, `:123`.
- Evidência por arquivo e linha:
  - `ADR-0007:71` — "Para uma tela de processamento, a composição envolve um ou mais
    `console`, zero ou um `dashboard`, e chips específicos";
  - `ADR-0007:123` — "zero ou um `dashboard` — por exemplo estado agregado do processo";
  - `ADR-0019:208-232` — D7 remove a cardinalidade global e preserva apenas regras de
    "tela concreta";
  - `ADR-0019:384-428` — seções de relação com ADR-0010, ADR-0015, ADR-0018; ausência
    de relação com ADR-0007;
  - `ADR-0019:434-440` — tabela de documentos a atualizar sem ADR-0007.
- Impacto: a aplicação documental futura pode deixar ADR-0007 com uma formulação
  conflitante ("zero ou um `dashboard`" para telas de processamento) em relação à D7
  ("uma tela pode conter mais de um dashboard"), gerando ambiguidade normativa sobre
  se telas de processamento podem ou não conter múltiplos dashboards.
- Exige patch da ADR: sim. A ADR deve adicionar ADR-0007 à identificação de
  consequências documentais e/ou adicionar uma seção "Relação com ADR-0007"
  esclarecendo se a formulação está suprimida ou preservada.
- Exige nova decisão do usuário: possivelmente. Se a classificação (regra global vs.
  política particular de tipo de tela) não for determinável a partir de D7, será
  necessário o usuário esclarecer se telas de processamento permanecem limitadas a
  "zero ou um `dashboard`" ou passam a admitir múltiplos. Esta possibilidade deve ser
  avaliada pelo autor da ADR ao corrigir o achado.

### QA-002

- ID: `QA-002`.
- Severidade: baixa.
- Categoria: `OBSERVACAO_NAO_BLOQUEANTE`.
- Descrição: erro de grafia "nívels" em lugar de "níveis" em
  `ADR-0019:477` ("pela contagem exclusiva por nívels de grupos (D1)").
- Decisão ou autoridade afetada: nenhuma (D1).
- Evidência: `ADR-0019:477`.
- Impacto: nenhum impacto normativo; apenas ortografia.
- Exige patch da ADR: não (não bloqueante), mas recomendado.
- Exige nova decisão do usuário: não.

### QA-003

- ID: `QA-003`.
- Severidade: baixa.
- Categoria: `TERMINOLOGIA_AMBIGUA`.
- Descrição: a ADR usa "substitui a leitura operacional anterior" em D1
  (`ADR-0019:128`) e "especializa a regra de contagem de nível da ADR-0015" na seção
  de relação (`ADR-0019:401`) para descrever a mesma mudança na contagem de
  profundidade. Os termos são reconciliáveis (a especialização substitui a leitura
  operacional anterior), mas a inconsistência pode sugerir ambiguidade sobre se a
  ADR-0015 é parcialmente substituída ou apenas especializada no ponto da contagem.
- Decisão ou autoridade afetada: D1; relação com ADR-0015.
- Evidência: `ADR-0019:128`, `:401`, `:407-408`.
- Impacto: baixo; não afeta a fidelidade das decisões, apenas a clareza da relação
  normativa com ADR-0015.
- Exige patch da ADR: não (não bloqueante), mas recomendada padronização terminológica.
- Exige nova decisão do usuário: não.

### QA-004

- ID: `QA-004`.
- Severidade: baixa.
- Categoria: `OBSERVACAO_NAO_BLOQUEANTE`.
- Descrição: `docs/NOMENCLATURA.md` seção 14 (`NOMENCLATURA.md:1154-1155`) afirma
  "Nível 3 proibido na versão atual — estruturas com profundidade ≥ 3 são rejeitadas",
  com numeração corpo raiz = nível 0. Esta formulação é mais restritiva que a ADR-0015
  (profundidade máxima 3 níveis, nível 4 rejeitado) e diretamente contraditória com a
  D2 da ADR-0019 (três níveis de grupos permitidos). A ADR-0019 identifica NOMENCLATURA
  para revisão (`ADR-0019:439`), mas a nota de consequência ("Revisar definição de
  nível hierárquico; alinhar à contagem por grupos") não sinaliza a gravidade
  específica da formulação "Nível 3 proibido", que exigirá revisão substantiva — não
  apenas alinhamento terminológico — na etapa de aplicação.
- Decisão ou autoridade afetada: D2; NOMENCLATURA seção 14.
- Evidência: `NOMENCLATURA.md:1149-1155`; `ADR-0019:439`.
- Impacto: a aplicação documental futura precisa tratar NOMENCLATURA seção 14 como
  revisão substantiva (a formulação "Nível 3 proibido" conflita com D2); a nota atual
  pode subestimar o escopo da revisão.
- Exige patch da ADR: não (não bloqueante); a identificação de NOMENCLATURA já está
  presente. Recomenda-se apenas refinar a nota de consequência.
- Exige nova decisão do usuário: não.

## 17. Conclusão

A ADR-0019 registra fielmente todas as sete decisões explícitas do usuário (D1 a D7),
sem introduzir decisões novas, sem ampliação normativa, sem restrição não autorizada e
sem aplicação prematura. A terminologia de níveis, a multiplicidade estrutural, a
cardinalidade de dashboard, os exemplos, a relação com ADR-0010/0015/0018, as
preservações, o escopo negativo e os metadados estão corretos.

Foi identificado um defeito corrigível na própria ADR: a omissão de ADR-0007 nas
consequências documentais da D7 (QA-001, média). ADR-0007 (aceita) contém "zero ou um
`dashboard`" para telas de processamento, formulação diretamente afetada pela D7, e a
ADR-0019 não esclarece se essa formulação está suprimida ou preservada. Este é um caso
de `CONSEQUENCIA_DOCUMENTAL_INCOMPLETA`, que exige correção da ADR antes da aplicação.

Os demais achados (QA-002, QA-003, QA-004) são observações não bloqueantes que não
exigem correção antes da aplicação.

Nenhuma decisão nova foi introduzida pela ADR. Nenhuma contradição interna foi
encontrada nas decisões D1-D7. Nenhuma política arquitetural indispensável fora de
D1-D7 foi identificada como pendente (ressalvada a possibilidade, em QA-001, de o
autor da ADR precisar esclarecer com o usuário se telas de processamento permanecem
limitadas a "zero ou um `dashboard`").

## 18. Status final

```text
ADR_REJECTED
```

Justificativa: existe defeito corrigível na própria ADR — `CONSEQUENCIA_DOCUMENTAL_INCOMPLETA`
(QA-001). A ADR-0019 não identifica ADR-0007 nas consequências documentais da D7 nem
esclarece a relação entre a remoção da cardinalidade global de dashboard e a
formulação "zero ou um `dashboard`" de ADR-0007 para telas de processamento. Este
defeito é corrigível na própria ADR (adição de ADR-0007 à identificação de
consequências e/ou seção de relação), sem exigir necessariamente nova decisão do
usuário — embora o autor da ADR deva avaliar se o esclarecimento exige input do
usuário quanto ao escopo de "tela de processamento" sob a exceção de "tela concreta"
da D7.

As decisões D1-D7, individualmente, são todas `FIEL`. O bloqueio refere-se
exclusivamente à consequência documental incompleta, não à fidelidade das decisões.

## 19. Próxima categoria processual (sem executá-la)

A próxima categoria processual permitida é a correção da ADR-0019 pelo executor,
restringindo-se a:

- adicionar ADR-0007 às consequências documentais identificadas e/ou adicionar seção
  "Relação com ADR-0007" esclarecendo se a formulação "zero ou um `dashboard`" de
  ADR-0007 está suprimida pela D7 ou preservada como política particular;
- opcionalmente, corrigir a grafia "nívels" → "níveis" (QA-002) e padronizar a
  terminologia "substitui"/"especializa" na relação com ADR-0015 (QA-003);
- opcionalmente, refinar a nota de consequência de NOMENCLATURA para sinalizar a
  gravidade da formulação "Nível 3 proibido" (QA-004).

Esta categoria não foi executada neste QA. Após correção, a ADR-0019 deverá ser
reauditada antes de qualquer aplicação documental.

## 20. Estado Git final

```text
git status --short
  ?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
  ?? docs/relatorios/RELATORIO_QA_ADR-0019.md
  ?? tela/__pycache__/

git diff --stat                   (sem saída)
git diff --name-only              (sem saída)
git diff --check                  (sem saída)
git diff --cached --stat          (sem saída)
git diff --cached --name-only     (sem saída)
```

O único novo arquivo adicional criado é
`docs/relatorios/RELATORIO_QA_ADR-0019.md`. Nenhum arquivo rastreado foi alterado. A
ADR-0019, o relatório de levantamento e `tela/__pycache__/` permanecem não rastreados,
sem alteração, remoção, movimentação ou stage. Stage permanece vazio.
