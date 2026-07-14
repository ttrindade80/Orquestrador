# RELATORIO_QA_POS_PATCH_ADR-0020

## 1. Identificação

- ADR auditada: `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- QA anterior: `scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md`
- achado reauditado: `ACH-001 — Ambiguidade na semântica de ausência de distribuição nos eixos da matriz`
- etapa: `QA_POS_PATCH_ADR`
- papel: `auditor documental independente`
- raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- branch: `master`
- commit-base: `f00b0bb`

## 2. Estado Git inicial

Antes de iniciar esta auditoria, o repositório encontrava-se em estado limpo, com os seguintes arquivos novos/não rastreados presentes (referentes aos ciclos e levantamentos anteriores):
- `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` (versão pós-patch)
- `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`
- `scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md`
- `scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`

Nenhum arquivo modificado ou em stage existia antes desta execução.

## 3. Autoridades consultadas

Foram lidos e consultados integralmente os seguintes documentos normativos e de controle:
- `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- `scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md`
- `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- `scripts/docs/NOMENCLATURA.md`
- `scripts/docs/adr/INDICE_ADR.md`
- `scripts/docs/contratos/contrato_composicao_corpo.md`
- `scripts/docs/contratos/contrato_tela_json.md`
- `scripts/docs/contratos/contrato_json_tela_minima.md`

## 4. Síntese do achado anterior

O relatório de QA anterior identificou o achado médio:
- **ACH-001 — Ambiguidade na semântica de ausência de distribuição nos eixos da matriz**
  - *Falha*: A ADR proibia a conversão silenciosa de ausência de distribuição para o modo `igual` (alinhando com a ADR-0018), mas não definia se as distribuições dos eixos eram obrigatórias, como se comportava a matriz em caso de omissão de uma delas ou se caberia dimensionamento por conteúdo natural, deixando brechas de indeterminação para o cálculo e renderização.

## 5. Verificação do patch

| Item | Correção esperada | Evidência encontrada | Resultado |
|---|---|---|---|
| 1 | `matriz.linhas.distribuicao` obrigatória | Consta em D6: "No comportamento `matriz`, as distribuições dos dois eixos são obrigatórias... Devem estar presentes obrigatoriamente: `matriz.linhas.distribuicao`" | Resolvido |
| 2 | `matriz.colunas.distribuicao` obrigatória | Consta em D6: "No comportamento `matriz`, as distribuições dos dois eixos são obrigatórias... Devem estar presentes obrigatoriamente: `matriz.colunas.distribuicao`" | Resolvido |
| 3 | Ausência de distribuição invalida a matriz | Consta em D6: "A ausência da distribuição de qualquer eixo torna a matriz inválida." | Resolvido |
| 4 | Modo `igual` exige declaração explícita | Consta em D6: "Para obter divisão igual, o JSON deve declarar explicitamente: `\"distribuicao\": { \"modo\": \"igual\" }`" | Resolvido |
| 5 | Sem default implícito para `igual` | Consta em D6: "Não existe: [...] default para `igual`" | Resolvido |
| 6 | Sem dimensionamento por conteúdo natural | Consta em D6: "Não existe: [...] cálculo por conteúdo natural" e "Nenhum eixo matricial é dimensionado por conteúdo natural." | Resolvido |
| 7 | Sem herança, inferência ou reuso | Consta em D6: "Não existe: [...] herança de distribuição do container pai; inferência por quantidade de linhas ou colunas" e "A distribuição de um eixo não é herdada, inferida ou reutilizada pelo outro eixo." | Resolvido |
| 8 | Sem fallback silencioso para `livre` | Consta em D6: "Não existe: [...] fallback para `estrutura: livre`" e "Não existe fallback silencioso de matriz inválida para o comportamento `livre`." (D5) | Resolvido |
| 9 | Preservação da semântica `livre` (ADR-0018) | Consta em D6: "Esta regra é específica de `estrutura: matriz` e não altera a semântica de ausência de distribuição no comportamento `livre`." e em "Relação com ADR-0018" | Resolvido |

## 6. D6 — Distribuição obrigatória por eixo

A decisão D6 foi inteiramente reestruturada para registrar de forma estrita, normativa e inequívoca:
- A obrigatoriedade absoluta das distribuições nos dois eixos (`linhas` e `colunas`).
- A total independência de cálculo entre os eixos.
- A rejeição determinística de qualquer omissão, classificando-a como inválida.
- A exigência de declaração explícita para o modo `igual`, sem defaults.
- Regras claras de validação (percentual com soma 100, frações com pesos positivos).
- Execução do algoritmo de arredondamento por maiores restos separadamente em cada eixo.
- Exclusão explícita de dimensionamento por conteúdo natural, herança ou inferência.

## 7. Relação com ADR-0018

A ADR distingue com perfeição e sem contradição os comportamentos:
- **`estrutura: livre`**: Preserva integralmente a ADR-0018. A ausência de distribuição continua orientada pelo conteúdo e não equivale ao modo `igual`.
- **`estrutura: matriz`**: Aplica a nova especialização, exigindo ambas as distribuições. A ausência é tratada como erro estrutural de validação, sem fallbacks.

A regra da matriz não é colocada como uma correção geral ou anulação da ADR-0018, que permanece totalmente vigente e soberana sobre o modo `livre`.

## 8. Exemplos válidos

Os exemplos válidos na ADR foram validados e estão perfeitamente coerentes:
- **Grupo `matriz` 2 × 4**: Declara explicitamente as distribuições de linhas (modo `fracao` com `[1, 2]`) e colunas (modo `fracao` com `[1, 2, 1, 2]`), com dimensões coerentes de valores.
- **Grupo `matriz` mínimo 2 × 2**: Declara explicitamente a distribuição em ambos os eixos no modo `igual` (`"distribuicao": {"modo": "igual"}`).
- **Grupo `livre`**: Mantém as distribuições e arranjos originais, inclusive preservando a validade da omissão de distribuição de acordo com a ADR-0018.

## 9. Exemplos inválidos

A seção de exemplos inválidos é robusta e cobre de forma impecável:
- **Distribuição de linhas ausente**: Demonstrada no exemplo JSON contendo colunas com distribuição e linhas sem distribuição.
- **Distribuição de colunas ausente**: Demonstrada no exemplo contendo linhas com distribuição e colunas sem distribuição.
- **Ambos os eixos sem distribuição (depender de default implícito)**: Rejeitado deterministicamente.
- **Somente um eixo com distribuição**: Rejeitado deterministicamente.
- **Conversão silenciosa para `livre`**: Exemplo detalhado proibindo fallback silencioso para evitar conversão silenciosa de matriz inválida para estrutura `livre`.

Os exemplos não introduzem campos concorrentes ou comportamentos incompatíveis com D1–D16.

## 10. Invariantes

A ADR estabelece com precisão as seguintes invariantes normativas sobre distribuição de eixos:
- `INV-MAT-DIST-01`: Toda matriz declara distribuição de linhas.
- `INV-MAT-DIST-02`: Toda matriz declara distribuição de colunas.
- `INV-MAT-DIST-03`: A ausência da distribuição de qualquer eixo invalida a matriz.
- `INV-MAT-DIST-04`: O modo igual depende de declaração explícita.
- `INV-MAT-DIST-05`: Nenhum eixo matricial é dimensionado por conteúdo natural.
- `INV-MAT-DIST-06`: A distribuição de um eixo não é herdada, inferida ou reutilizada pelo outro eixo.

Nenhuma outra seção da ADR contradiz estas invariantes.

## 11. Consequências futuras

### 11.1 Loader
Exige do loader a validação estrita, determinística e prévia (antes da construção do modelo e da renderização) de:
- Presença de `matriz.linhas.distribuicao` e `matriz.colunas.distribuicao`.
- Validade do modo (`igual`, `percentual`, `fracao`).
- Coerência de valores (soma 100 para percentual, pesos positivos para fração, contagem compatível com as dimensões do eixo).
- Rejeição imediata em caso de omissão de qualquer uma das distribuições.

### 11.2 Modelo
Exige que o modelo:
- Receba dados previamente validados, contendo distribuições explícitas por eixo.
- Não crie defaults, não preencha lacunas silenciosamente, não herde e não infira distribuições para eixos matriciais.

### 11.3 Renderizador
Exige do renderizador:
- Processamento determinístico de ambos os eixos com distribuições explícitas.
- Aplicação isolada do modo declarado separadamente por eixo, utilizando o algoritmo de maiores restos.
- Ausência total de cálculo por tamanho natural e de preenchimento automático para converter omissão em `igual`.

### 11.4 Testes
A ADR dita explicitamente a necessidade de cobertura mínima e futura para:
- Matriz com `igual` explícito em ambos os eixos.
- Matriz com modos diferentes de distribuição entre linhas e colunas (ex: `igual` em linhas e `fracao` em colunas).
- Cenários de falha e rejeição por ausência de distribuição em linhas, em colunas, em ambos, ou com apenas um eixo preenchido.
- Rejeição de tentativa de uso de `igual` implícito.
- Preservação do comportamento `livre` com ausência de distribuição (conforme ADR-0018) e rejeição de queda de matriz inválida para `livre`.

## 12. Pendências

Não restam pendências relativas à obrigatoriedade da distribuição, comportamento em caso de ausência ou cálculo por conteúdo na matriz. Permanecem como pendências externas legítimas e normativas:
1. Política específica para área insuficiente na matriz (quando as dimensões do terminal forem insuficientes após as cotas e a ADR-0017 não for capaz de resolver de forma geral).
2. Suporte futuro a células vazias.
3. Suporte futuro a mesclagem (`rowspan`/`colspan`).
4. Suporte futuro a dimensões acima de 4 × 4.

## 13. Regressão D1–D16

Cada uma das decisões D1 a D16 foi auditada para garantir que o patch não introduziu regressão ou distorções no escopo do design original:

- **D1 — Dois comportamentos estruturais de grupo**: `FIEL`. Os comportamentos `livre` e `matriz` permanecem intactos.
- **D2 — Seletor declarativo**: `FIEL`. O campo `estrutura` é preservado.
- **D3 — Compatibilidade por ausência**: `FIEL`. Ausência de seletor resulta estritamente em `livre`.
- **D4 — Relação com o comportamento atual**: `FIEL`. Preserva integralmente todas as semânticas e regras do modo `livre`.
- **D5 — Dimensões permitidas da matriz**: `FIEL`. Limites entre 2x2 e 4x4 rigorosamente mantidos, sem fallbacks.
- **D6 — Distribuição independente por eixo**: `FIEL`. Reforçada e corrigida pelo patch, agora com obrigatoriedade estrita.
- **D7 — Grade comum de coordenadas**: `FIEL`. Mantém o princípio de alinhamento determinístico de bordas e divisórias.
- **D8 — Coordenadas explícitas para células**: `FIEL`. Associações por coordenadas 1-based, indexação correta e limites de preenchimento.
- **D9 — Conteúdo das células**: `FIEL`. Preserva taxonomia de filhos e limites de profundidade hierárquica.
- **D10 — Células vazias**: `FIEL`. Proibição absoluta mantida.
- **D11 — Mesclagem de células**: `FIEL`. Mantida fora de escopo.
- **D12 — Matriz inválida**: `FIEL`. Rejeição determinística total mantida.
- **D13 — Interação com `arranjo`**: `FIEL`. `arranjo` é proibido em `estrutura: matriz`.
- **D14 — Terminal e área insuficiente**: `FIEL`. Preserva ADR-0017 e SIGWINCH.
- **D15 — Preservação retroativa**: `FIEL`. Retrocompatibilidade de todos os JSONs ativos garantida.
- **D16 — Matriz não substitui a hierarquia**: `FIEL`. Matriz especializa `grupo`, mantendo a contagem por níveis de grupo.

## 14. Achados

- **OBS-001 (OBSERVAÇÃO) — Preservação da Divergência de Status da ADR-0018**:
  - *Descrição*: A ADR-0020 identifica de forma fidedigna a divergência documental histórica da ADR-0018 (proposta no arquivo × aceita no índice), mantendo-a como pendência externa ao seu escopo e sem transformá-la em achado corretivo desta ADR.

Nenhum achado de severidade `BLOQUEANTE`, `ALTO`, `MEDIO` ou `BAIXO` foi identificado na versão pós-patch da ADR-0020.

## 15. Estado Git final

O repositório mantém-se totalmente íntegro e inalterado. Não houve modificação em nenhum arquivo ativo ou configuração existente, registrando-se somente a criação do presente relatório.
- **Estado do stage**: Vazio.
- **Histórico de commits**: Preservado na integridade da branch `master`.

## 16. Status final

```yaml
status_final: ADR_APPROVED_WITH_NOTES
bloqueantes: 0
altos: 0
medios: 0
baixos: 0
observacoes: 1
```

## 17. Próxima categoria processual

`APLICAR_ADR`
