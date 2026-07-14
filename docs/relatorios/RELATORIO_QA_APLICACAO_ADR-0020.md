# RELATORIO_QA_APLICACAO_ADR-0020

## 1. Identificação

- ADR auditada: `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- aplicação auditada: `scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md`
- QA de entrada: `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0020.md`
- etapa: `QA_APLICACAO_ADR`
- papel: auditor documental independente
- raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- branch: `master`
- commit-base: `f00b0bb`

## 2. Estado Git inicial

Antes do início desta auditoria, o repositório encontrava-se em conformidade com o commit-base declarado:
- **HEAD**: `f00b0bb` (confirmado)
- **Status do stage**: Vazio
- **Arquivos modificados rastreados**:
  - `M scripts/docs/NOMENCLATURA.md`
  - `M scripts/docs/adr/INDICE_ADR.md`
  - `M scripts/docs/contratos/contrato_composicao_corpo.md`
  - `M scripts/docs/contratos/contrato_json_tela_minima.md`
  - `M scripts/docs/contratos/contrato_tela_json.md`
- **Arquivos novos não rastreados (untracked)**:
  - `?? scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
  - `?? scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md`

Nenhum arquivo de código, teste ou configuração ativa do sistema foi alterado.

## 3. Autoridades consultadas

Foram lidas e consultadas na totalidade as seguintes autoridades normativas, processuais e levantamentos documentais:
- `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` (autoridade de composição e maiores restos)
- `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` (autoridade sobre ausência de distribuição e preenchimento vertical)
- `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` (autoridade sobre limite de 3 níveis de grupos)
- `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` (autoridade de design da matriz de grupos)
- `scripts/docs/adr/INDICE_ADR.md` (documento de destino de índice)
- `scripts/docs/NOMENCLATURA.md` (documento de destino terminológico)
- `scripts/docs/contratos/contrato_composicao_corpo.md` (contrato de destino principal)
- `scripts/docs/contratos/contrato_tela_json.md` (contrato de destino do schema do loader)
- `scripts/docs/contratos/contrato_json_tela_minima.md` (contrato de destino de tela mínima)
- `scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md` (autoridade processual do ciclo de QA da ADR)
- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0020.md` (autoridade de aprovação de design)
- `scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md` (relatório de declaração do trabalho)

## 4. Escopo físico esperado

A aplicação documental obedeceu rigorosamente ao limite de arquivos permitidos para edição e criação.
- **Arquivos existentes alterados (6)**:
  1. `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` (alterado em status)
  2. `scripts/docs/adr/INDICE_ADR.md` (alterado para registro da ADR-0020)
  3. `scripts/docs/NOMENCLATURA.md` (adicionada a seção 15)
  4. `scripts/docs/contratos/contrato_composicao_corpo.md` (adicionadas seções 3.3, 5.13-5.24, R-25-R-32, critérios de validação)
  5. `scripts/docs/contratos/contrato_tela_json.md` (adicionado seletor e validações futuras de matriz na seção 8)
  6. `scripts/docs/contratos/contrato_json_tela_minima.md` (adicionada seção 6.4, V-9-V-12, critérios de aceite)
- **Arquivo novo criado (1)**:
  1. `scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md`

**Total**: 6 arquivos existentes alterados + 1 arquivo novo criado = 7 arquivos envolvidos. Escopo físico fiel e livre de resíduos em diretórios não autorizados.

## 5. Verificação do relatório de aplicação

O `RELATORIO_APLICACAO_ADR-0020.md` foi analisado e confrontado com as alterações factuais:
- Identifica corretamente a ADR-0020, etapa `APLICAR_ADR`, papel de autor documental, raiz, branch, commit-base e o QA de entrada (`RELATORIO_QA_POS_PATCH_ADR-0020.md`).
- Registra corretamente a transição de status de `proposta` para `aceita`.
- Mapeia com perfeição a propagação de D1–D16 e do patch de distribuição obrigatória.
- Lista de forma coerente e idêntica os arquivos autorizados e as ações executadas sobre cada um.
- Informa o estado final do Git em stage vazio e linter limpo.
- Não introduz desvios ou afirmações divergentes sobre o estado documental final.

O relatório de aplicação é materialmente fiel à realidade do repositório.

## 6. Status da ADR e índice

- **Status no arquivo**: O arquivo `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` foi editado no frontmatter (`metadata.status: aceita`) e na seção `## Status` (`aceita`). Não foram feitas alterações nas decisões ou exemplos aprovados.
- **Status no índice**: O arquivo `scripts/docs/adr/INDICE_ADR.md` foi atualizado com a entrada da `ADR-0020` pós-`ADR-0019`, registrando o título canônico, o caminho do arquivo, a data e o status `aceita`.
- **Divergências históricas**: A divergência de status da `ADR-0018` (proposta no arquivo, aceita no índice) foi intencionalmente preservada e isolada, sem correções indevidas fora do escopo.

## 7. Propagação D1–D16

| Decisão | Destinos esperados | Evidência encontrada | Resultado |
|---|---|---|---|
| **D1** | `ADR-0020`, `NOMENCLATURA` §15, `contrato_composicao` §3.3, `contrato_tela` §8, `contrato_minima` §6.2 | Formalizados comportamentos `livre` e `matriz` do grupo. | `FIEL` |
| **D2** | `ADR-0020`, `NOMENCLATURA` §15.1, `contrato_composicao` §3.3, `contrato_tela` §8 | Campo seletor canônico `estrutura` configurado com valores `"livre"` e `"matriz"`. | `FIEL` |
| **D3** | `ADR-0020`, `NOMENCLATURA` §15.1-15.2, `contrato_composicao` §3.3/§5.13, `contrato_tela` §8, `contrato_minima` §6.2/§6.4 | Ausência de `estrutura` equivale a `livre`, preservando comportamento legado. | `FIEL` |
| **D4** | `NOMENCLATURA` §15.2, `contrato_composicao` §3.3/§5.13, `contrato_tela` §8, `contrato_minima` §6.2 | Comportamento `livre` preservado, inclusive a omissão de distribuição regida pela `ADR-0018`. | `FIEL` |
| **D5** | `NOMENCLATURA` §15.3, `contrato_composicao` §5.14, `contrato_tela` §8, `contrato_minima` §6.4 | Limites dimensionais de 2 a 4 por eixo estabelecidos, sem fallback silencioso para `livre`. | `FIEL` |
| **D6** | `NOMENCLATURA` §15.4, `contrato_composicao` §5.15 + invariantes, `contrato_tela` §8, `contrato_minima` §6.4 | Distribuições em ambos os eixos obrigatórias (linhas/colunas), maiores restos por eixo, sem defaults ou heranças. | `FIEL` |
| **D7** | `NOMENCLATURA` §15.4, `contrato_composicao` §5.16, `contrato_tela` §8 | Grade de coordenadas comum compartilhada por todas as células da matriz para alinhamento. | `FIEL` |
| **D8** | `NOMENCLATURA` §15.4, `contrato_composicao` §5.17, `contrato_tela` §8, `contrato_minima` §6.4 | Coordenadas explícitas 1-based, mapeamento para `elementos[]`, sem duplicidade de coordenada/elemento. | `FIEL` |
| **D9** | `contrato_composicao` §5.19, `contrato_tela` §8 | Célula aceita tipos console, lançador, dashboard e grupo, preservando o limite de profundidade. | `FIEL` |
| **D10**| `NOMENCLATURA` §15.5, `contrato_composicao` §5.18, `contrato_tela` §8, `contrato_minima` §6.4 | Células vazias estritamente proibidas; preenchimento completo exigido nesta versão. | `FIEL` |
| **D11**| `NOMENCLATURA` §15.5, `contrato_composicao` §5.18 | Mesclagem (`rowspan`/`colspan`) explicitada como fora de escopo. | `FIEL` |
| **D12**| `NOMENCLATURA` §15.5, `contrato_composicao` §5.20/R-31, `contrato_tela` §8, `contrato_minima` §6.4 | Rejeição determinística e imediata de matriz inválida pelo loader, sem fallbacks silenciosos. | `FIEL` |
| **D13**| `NOMENCLATURA` §15.5, `contrato_composicao` §3.3/R-30, `contrato_tela` §8, `contrato_minima` §6.4 | O campo `arranjo` é expressamente proibido em `estrutura: "matriz"`. | `FIEL` |
| **D14**| `contrato_composicao` §5.21 | Redimensionamento (`SIGWINCH` / `ADR-0017`) preservado; política de área insuficiente na matriz em aberto. | `FIEL` |
| **D15**| Propagado em todos os documentos afetados | Retrocompatibilidade integral para grupos sem `estrutura` e para JSONs legados. | `FIEL` |
| **D16**| `contrato_composicao` §5.19/R-32, `contrato_tela` §8 | Matriz especializa o nó `grupo`, sem substituir a hierarquia da árvore do corpo. | `FIEL` |

## 8. Nomenclatura

O documento `scripts/docs/NOMENCLATURA.md` foi expandido com a adição da seção 15:
- Define de forma normativa os conceitos e proibições de seletor `estrutura`, comportamento `livre` e `matriz`.
- Formaliza os 8 termos essenciais de `matriz de grupos` (linha, coluna, célula, coordenada explícita, distribuição de linhas, distribuição de colunas, grade comum e cobertura completa).
- Distingue normativamente `matriz de grupos` (especialização de grupo) do modo calculado de colunas automáticas do `lancador`.
- Enumera explicitamente como inválidos ou fora de escopo os termos: ordem implícita de células, matriz por grupos irmãos independentes, célula vazia, mesclagem (`rowspan`/`colspan`), distribuição implícita de eixo e `arranjo` em `matriz`.

Nenhuma terminologia concorrente ou pseudônimo desalinhado foi introduzido.

## 9. Contrato de composição do corpo

No arquivo `scripts/docs/contratos/contrato_composicao_corpo.md` (versão 0.3):
- Adicionados os termos `ADR-0019` e `ADR-0020` na lista `adrs_aplicadas` do frontmatter.
- Seções 3.3 e 5.13-5.24 estendem a distinção entre os comportamentos `livre` e `matriz`, listando todas as restrições de limites de 2 a 4 por eixo, obrigatoriedade de ambas as distribuições com maiores restos por eixo, grade comum, coordenadas 1-based, cobertura completa sem células vazias ou mesclagens, e rejeição sem fallback para `livre`.
- Regras de uso `R-25` a `R-32` adicionadas, condensando as invariantes em comandos diretos ao loader e ao renderer.
- Critérios de validação na seção 8 foram expandidos cobrindo exaustivamente todas as proibições, schemas incorretos e invalidações de coordenadas da matriz.

## 10. Contrato da tela JSON

No arquivo `scripts/docs/contratos/contrato_tela_json.md` (seção 8):
- Adicionada tabela de comportamento por valor de `estrutura` (ausente, `"livre"` ou `"matriz"`) e mapeamento de campos válidos/proibidos por estado.
- Configurada tabela com os campos obrigatórios por modo de distribuição de eixo matricial (`igual`, `percentual`, `fracao`).
- Mapeada a lista de validações que o loader deverá aplicar em tempo de carga, cobrindo dimensões, proibições de `arranjo`, duplicidade de elemento/coordenada, referências cruzadas e contagem de células.
- Toda a redação utiliza linguagem voltada para o futuro e obrigações contratuais ("o loader deverá futuramente validar"), evitando afirmações de implementação ativa ou loader ativo concluído.

## 11. Contrato JSON de tela mínima

No arquivo `scripts/docs/contratos/contrato_json_tela_minima.md`:
- Mapeado o suporte de retrocompatibilidade do grupo sem `estrutura` e do grupo com `estrutura: "livre"`.
- Nova seção 6.4 especifica os campos mínimos de um grupo com `estrutura: "matriz"`, inserindo o exemplo normativo mínimo de matriz 2x2 com modo `igual` explícito nos dois eixos.
- Enumera as proibições e a obrigatoriedade absoluta de distribuições nos dois eixos com modo `igual` declarado explicitamente.
- Regras de validação `V-9` a `V-12` incorporadas à seção 8, cobrando validações estruturais de matriz do loader.
- Adicionados 5 critérios de aceite de matriz nos critérios de aceite documental, permitindo testabilidade da aplicação.

## 12. Correção do ACH-001

A correção do achado de ambiguidade do eixo omitido (`ACH-001`) foi estritamente propagada para todos os documentos de destino:
- `matriz.linhas.distribuicao` e `matriz.colunas.distribuicao` são obrigatórias nos três contratos.
- A ausência de qualquer distribuição invalida a matriz imediatamente.
- O modo `igual` depende de declaração explícita de `{"modo": "igual"}`; não existe default implícito de `igual` por omissão ou inferência.
- Nenhum eixo matricial é dimensionado por conteúdo natural ou tamanho de caracteres dos elementos.
- A distribuição de um eixo não é herdada, inferida, replicada ou reutilizada pelo outro.
- A ausência de distribuição em `livre` permanece regida pela `ADR-0018` (orientada ao conteúdo), mantendo a perfeita distinção conceitual.

## 13. Relação com ADR-0015

- A composição em árvore, tipos funcionais e o algoritmo de maiores restos (método determinístico para células inteiras com resíduos por resto e desempate declarativo) são preservados integralmente.
- O arredondamento por maiores restos é aplicado de forma totalmente independente por eixo na matriz (linhas e colunas calculam seus restos de forma isolada).
- A sincronização de cortes de grupos unidimensionais irmãos permanece preservada para `livre` sob as condições de restrições coincidentes.

## 14. Relação com ADR-0018

- Preserva integralmente o comportamento `livre` (ausência de distribuição orientada pelo conteúdo, sem default de divisão igual).
- Em `matriz`, as distribuições por eixo são obrigatórias, sem fallbacks para conteúdo natural, e a sobra de cota é preenchida internamente com espaços (eixos de largura) ou linhas em branco (eixos de altura) dentro da moldura da célula, nunca como sobra externa do container matricial.
- A divergência histórica de status da `ADR-0018` no índice e no arquivo permanece inalterada e tratada como pendência externa, sem anulações indevidas.

## 15. Relação com ADR-0019

- O limite máximo de 3 níveis de grupos permanece intocado e rigorosamente verificado.
- A matriz de grupos não adiciona níveis na contagem de profundidade (linhas, colunas e células não contam).
- Um nó `grupo` aninhado dentro de uma célula da matriz conta normalmente para a profundidade. O exemplo inválido `EX-MAT-I8` demonstra explicitamente o erro estrutural de se declarar um grupo no nível 4 contido em célula.

## 16. Schema e exemplos

Todos os exemplos JSON foram revisados estruturalmente por varredura manual de sintaxe:
- **EX-MAT-V1** (matriz 2x2 com `igual` explícito nos dois eixos), **EX-MAT-V2** (matriz 2x4 com frações diferentes), **EX-MAT-V3** (modos mistos: `igual` em linhas e `percentual` em colunas), **EX-MAT-V4** (grupo livre sem `estrutura`) e **EX-MAT-V5** (grupo livre explícito) estão com schemas sintaticamente válidos, referências de `id` consistentes em `elementos[]` e sem campos concorrentes.
- Os exemplos inválidos (**EX-MAT-I1** a **EX-MAT-I9**) descrevem perfeitamente cada uma das proibições (omissão de distribuição, duplicidade de coordenada, duplicidade de elemento, célula excedente/faltante, `arranjo` em matriz, grupo no nível 4 em célula e conversão silenciosa proibida).

## 17. Ausência de implementação indevida

Nenhuma das seções alteradas afirma que o loader, o modelo ou o renderizador do sistema já contam com suporte implementado para a matriz. Foram usadas consistentemente construções futuras e obrigações de design, como:
- "O loader deverá futuramente validar"
- "O renderizador deverá futuramente recalcular"
- "A implementação futura de código e testes está fora de escopo"
- "A aplicação documental não implementa nenhuma dessas consequências"

A aplicação documental manteve-se estritamente restrita a contratos, nomenclatura e índice.

## 18. Pendências preservadas

- Continuam pendentes, sem solução inventada ou fechada antecipadamente:
  1. Política específica para área insuficiente na matriz (quando as dimensões reais do terminal não comportam a grade mesmo com as regras da `ADR-0017`).
  2. Suporte futuro a células vazias (placeholders, nulos, reservados).
  3. Suporte futuro a mesclagem (`rowspan`/`colspan`).
  4. Suporte futuro a dimensões acima de 4x4.
- Não continuam pendentes (estão resolvidas de forma normativa e explícita):
  - A obrigatoriedade absoluta das distribuições nos dois eixos de matriz.
  - A invalidade da omissão de distribuição em matriz.
  - A exigência de declaração explícita para o modo `igual` na matriz.
  - A proibição de dimensionamento natural nos eixos de matriz.

## 19. Resíduos e contradições

A busca de resíduos e contradições cobriu todo o escopo alterado e confirma:
- Nenhuma matriz com distribuição opcional foi autorizada.
- Nenhuma divisão igual implícita ou default de distribuição foi permitido na matriz.
- Nenhuma mesclagem, `rowspan` ou `colspan` foi dada como válida na matriz.
- Nenhuma célula vazia ou placeholder foi inserido como válido.
- O campo `arranjo` está consistentemente proibido em grupos matriciais.
- Não há contradições entre os três contratos alterados, que guardam perfeito alinhamento estrutural e de validações.

## 20. Escopo Git

Verificação física do repositório Git:
- **Código, testes e configurações**: Nenhuma alteração nos diretórios `scripts/tela`, `scripts/config`, `tela`, `config`, `tests` ou `scripts/tests`.
- **Status do stage**: Vazio (limpo).
- **Consistência de whitespace**: Nenhuma violação ou erro de quebra de linha.

## 21. Achados

### OBSERVAÇÕES

- **OBS-001 — Preservação da Divergência de Status da ADR-0018**
  - *Descrição*: A divergência documental histórica da `ADR-0018` (status `proposta` no arquivo e `aceita` no índice de ADRs) foi fielmente identificada e mantida como pendência externa ao escopo do ciclo atual. Não foram introduzidas alterações corretivas ou tentativas de modificação sobre os arquivos da `ADR-0018`.

Nenhum achado de severidade `BLOQUEANTE`, `ALTO`, `MEDIO` ou `BAIXO` foi identificado na aplicação documental.

## 22. Estado Git final

O repositório mantém-se totalmente íntegro e inalterado em relação ao estado de entrada, acrescido exclusivamente deste relatório de QA da aplicação documental:
- **Estado do stage**: Vazio (limpo).
- **HEAD**: `f00b0bb` (confirmado)

## 23. Status final

```yaml
status_final: ADR_APPLICATION_APPROVED
bloqueantes: 0
altos: 0
medios: 0
baixos: 0
observacoes: 1
```

## 24. Próxima categoria processual

`BASE_DOCUMENTAL_APROVADA`
