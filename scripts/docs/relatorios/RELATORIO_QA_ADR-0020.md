# RELATORIO_QA_ADR-0020

## 1. Identificação

- ADR auditada: `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- Relatório: `scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md`
- Etapa: `QA_ADR`
- Origem processual: incorporação da auditoria independente B
- Commit-base: `f00b0bb`
- Identificação do QA: `auditoria independente da ADR-0020`
- Agente Auditor: auditor documental independente
- Data: Domingo, 12 de julho de 2026
- Escopo: Auditoria formal de conformidade e integridade da ADR-0020

## 2. Estado Git

- **RAIZ_GIT**: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- **Branch**: `master`
- **Últimos Commits**:
  - `f00b0bb` docs: registra substituicao do H-0024 pelo H-0025
  - `c003f3e` feat: implementa composicao hierarquica do corpo com tres niveis de grupos
  - `40015b6` feat: implementa distribuicao horizontal percentual e fracionaria
- **Status de Arquivos**:
  - `?? scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
  - `?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`
  - `?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`
- **Git Diff e Status**: Sem alterações modificadas ou em stage.

## 3. Autoridades consultadas

- **Nomenclatura**: `scripts/docs/NOMENCLATURA.md`
- **Índice de ADRs**: `scripts/docs/adr/INDICE_ADR.md`
- **ADR-0015**: `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- **ADR-0018**: `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- **ADR-0019**: `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- **Contratos de Composição de Corpo**: `scripts/docs/contratos/contrato_composicao_corpo.md`
- **Contratos de Schema**: `scripts/docs/contratos/contrato_tela_json.md` e `scripts/docs/contratos/contrato_json_tela_minima.md`
- **Evidências Processuais e Técnicas**:
  - `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`
  - `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`
  - `scripts/docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`
  - `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md`
  - `scripts/docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md`
  - `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md`
  - `scripts/docs/relatorios/RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md`

## 4. Estado factual de entrada

Confirma-se o estado factual inicial do repositório:
- `H-0026` (commit `40015b6`): estado fechado.
- `H-0027` (commit `c003f3e`): estado fechado; `qa_handoff` é `H1_HANDOFF_APPROVED`; `qa_implementacao` é `I1_IMPLEMENTATION_APPROVED`; testes `1004/1004`.
- `ADR-0019`: aceita no arquivo e no índice; aplicação documental aprovada.
- `ADR-0018`: proposta no arquivo e aceita no índice; decisão incorporada aos contratos; divergência textual de status registrada (sem bloqueio).

## 5. Auditoria D1–D16

- **D1 (Dois comportamentos)**: `FIEL`. Comportamentos `livre` e `matriz` formalizados.
- **D2 (Seletor canônico)**: `FIEL`. Seletor declarativo `estrutura` formalizado.
- **D3 (Compatibilidade por ausência)**: `FIEL`. Ausência equivale a `livre`.
- **D4 (Modo livre preserva comportamento)**: `FIEL`. Semântica original sem alterações.
- **D5 (Dimensões 2x2 a 4x4)**: `FIEL`. Limites bem definidos e sem fallback silencioso.
- **D6 (Distribuição independente por eixo)**: `FIEL`. Linhas e colunas com distribuições separadas.
- **D7 (Grade comum de coordenadas)**: `FIEL`. Grade compartilhada por todas as células.
- **D8 (Coordenadas explícitas)**: `FIEL`. Índices baseados em 1, referências válidas e sem duplicidade.
- **D9 (Conteúdo permitido)**: `FIEL`. Células aceitam `console`, `lancador`, `dashboard` ou `grupo` sujeitos a limites de profundidade.
- **D10 (Células vazias proibidas)**: `FIEL`. Proibição explícita.
- **D11 (Sem mesclagem)**: `FIEL`. `rowspan`, `colspan` e mesclagens fora de escopo.
- **D12 (Rejeição determinística)**: `FIEL`. Sem fallback ou correções silenciosas.
- **D13 (Proibição de arranjo)**: `FIEL`. `arranjo` é proibido em `estrutura: matriz`.
- **D14 (Regras de terminal)**: `FIEL`. Preserva SIGWINCH e regras globais, restando detalhes em aberto.
- **D15 (Compatibilidade retroativa)**: `FIEL`. Preserva todos os JSONs e comportamentos existentes.
- **D16 (Especialização de grupo)**: `FIEL`. Matriz especializa `grupo`, sem substituir a hierarquia.

## 6. Auditoria do schema conceitual

O exemplo conceitual fornecido é consistente e obedece a todas as restrições:
- Usa `tipo: "grupo"` e `estrutura: "matriz"`.
- Possui objeto `matriz`.
- Declara `linhas` e `colunas` separadamente.
- Associa dois valores para duas linhas e quatro valores para quatro colunas.
- Usa índices de linha e coluna iniciados em 1.
- Referencia somente IDs válidos em `elementos[]`.
- Não repete coordenadas nem elementos.
- Cobre todas as coordenadas sem células vazias e sem misturar `arranjo`.
- O schema é apresentado corretamente como conceitual e não aplicado aos contratos ativos.
- Exemplos inválidos são consistentes com as decisões.

## 7. Distribuição por eixo

- Preserva `igual`, `percentual` e `fracao`.
- Quantidade de valores corresponde à dimensão do eixo.
- Percentual exige soma 100, fração exige pesos positivos, e maiores restos são aplicados de forma independente por eixo.
- **Destaque de ambiguidade (Severidade: MEDIO)**: A ADR determina que a ausência de distribuição em um eixo de matriz não pode ser convertida silenciosamente em `igual` (em linha com a ADR-0018). Contudo, a ADR-0020 deixa ambígua qual é a semântica real para o eixo omitido (por exemplo, usar tamanho com base em conteúdo ou disparar erro de validação). Como as células de uma linha ou coluna de uma matriz compartilham as dimensões, a ausência de distribuição torna a renderização e o cálculo de áreas não determinísticos caso não haja diretriz explícita.

## 8. Coordenadas e cobertura

- Linhas e colunas usam índices baseados em 1.
- Posição é determinada por coordenadas, não pela ordem do array.
- Coordenadas/elementos duplicados e referências inválidas são estritamente proibidos.
- Toda célula é preenchida e todo filho é associado exatamente uma vez (sem preenchimento automático).

## 9. Hierarquia e profundidade

- Matriz especializa `grupo`, não alterando a contagem de profundidade (linhas/colunas não são níveis adicionais).
- Somente nós `grupo` são computados para o limite máximo de 3 níveis da ADR-0019.
- Elemento `grupo` contido em célula é válido desde que respeite o limite. Matriz não cria novo tipo funcional.

## 10. Compatibilidade retroativa

- Garantida de forma integral. Grupos sem `estrutura` operam como `livre` e preservam a totalidade das regras unidimensionais, maiores restos, tipos funcionais, navegação e comportamento responsivo sob `SIGWINCH`.

## 11. Relações normativas

- Preserva integralmente e complementa as ADRs anteriores:
  - **ADR-0015**: sem cancelamento, mantendo o particionamento contíguo.
  - **ADR-0018**: mantendo a semântica da ausência de distribuição e destacando a divergência textual do status como pendência histórica separada.
  - **ADR-0019**: mantendo o limite de 3 níveis.
  - Não afirma que já está aplicada aos contratos ativos.

## 12. Consequências futuras

- Loader, modelo, renderizador e testes futuros são detalhados como consequências futuras legítimas, sem prescrição de código concreto desnecessário e sem declarar implementação já concluída.

## 13. Fora de escopo

- Delimita de forma clara o que está fora de escopo: implementação de código, testes, alteração de contratos ativos, correção de status da ADR-0018, células vazias, mesclagem, paginação/rolagem de matriz e nova política global de terminal pequeno.

## 14. Achados

- **ACH-001 (MEDIO) — Ambiguidade na semântica de ausência de distribuição nos eixos da matriz**:
  - *Descrição*: A ADR-0020 proíbe converter ausência silenciosamente para `igual` (em linha com a ADR-0018). Contudo, ela não define o comportamento do eixo quando sua distribuição é omitida e não decide se a omissão é inválida ou se deve seguir um algoritmo orientado pelo conteúdo. Isso deixa o cálculo do tamanho das linhas ou colunas indefinido, não permite que o implementador escolha essa política de forma arbitrária e exige correção normativa antes da aplicação documental.
- **OBS-001 (OBSERVAÇÃO) — Preservação da Divergência de Status da ADR-0018**:
  - *Descrição*: A ADR-0020 identifica de forma fidedigna a divergência documental histórica da ADR-0018 (proposta no arquivo × aceita no índice), mantendo-a como pendência externa ao seu escopo e sem transformá-la em achado corretivo desta ADR.

## 15. Estado Git final

- **Estado Git**: Inalterado. Nenhum arquivo do repositório foi modificado ou criado de forma experimental, restando apenas a criação deste relatório canônico.

## 16. Status final

```yaml
status_final: ADR_REJECTED
bloqueantes: 0
altos: 0
medios: 1
baixos: 0
observacoes: 1
```

## 17. Próxima categoria processual

`PATCH_ADR`
