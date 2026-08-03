# Relatório QA — ADR-0039

## Objeto auditado

`docs/adr/ADR-0039-modularizacao-estrutural-do-runtime-de-telas.md` — Modularização estrutural do runtime de telas.

## Autoridades usadas

Foram lidos integralmente a ADR auditada, `docs/nomenclatura/01_NUCLEO_COMUM.md`, `20_TELA_CORPO_E_COMPOSICAO.md`, `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`, `32_CONSOLE.md`, `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`, e os contratos `contrato_tela_json.md`, `contrato_composicao_corpo.md`, `contrato_console.md` e `contrato_json_console.md`. Também foi executada a busca focal autorizada em `docs/adr/INDICE_ADR.md` e a busca autorizada em `docs/backlog.md`.

## Verificações executadas

Foram confrontadas as decisões D-MOD-01 a D-MOD-08, a abertura da lista de módulos internos, a sucessão da ADR-0038, as referências documentais e seções citadas, `contratos_afetados: []`, a distinção entre decisão, aplicação e implementação, e os metadados/status. Não há referência material à ADR-0039 no backlog.

## Achados

### QA-ADR0039-01

```yaml
id: QA-ADR0039-01
requisito_violado: "Status e metadados compatíveis com o fluxo vigente de ADR recém-criada antes do resultado do QA; critério de aprovação do QA."
evidencia_focal: "A ADR declara `metadata.status: aceita` (ADR-0039:6) e `Status: aceita` (ADR-0039:23-25). O índice afirma registrar as ADRs aceitas (INDICE_ADR.md:17), contém ADR-0038 como última entrada (INDICE_ADR.md:70) e não contém ADR-0039."
impacto: "A ADR se apresenta como aceita antes deste QA e fica incoerente com a convenção do índice, comprometendo a rastreabilidade do ciclo."
correcao_necessaria: "Ajustar o status da ADR ao estado pré-QA previsto pelo fluxo; a promoção para aceita e a inclusão no índice devem ocorrer somente conforme o resultado aprovado deste QA."
```

### QA-ADR0039-02

```yaml
id: QA-ADR0039-02
requisito_violado: "Critérios de aplicação não podem transferir para a aplicação documental obrigações de aceite dos três handoffs; decisão arquitetural, aplicação documental e implementação posterior devem permanecer distintas."
evidencia_focal: "A seção 4 vincula cada handoff aos critérios de aplicação e aceite da seção 9 (ADR-0039:185-191). A seção 9, intitulada `Critérios para aplicação`, exige que cada handoff comprove os dez critérios de D-MOD-08, preserve fachadas, preserve integralmente os testes do Handoff 3 e não introduza mudanças (ADR-0039:271-287)."
impacto: "A aplicação documental passa a carregar verificações de implementação e aceite, podendo transformar uma alteração de documentos em autorização ou obrigação de executar os handoffs."
correcao_necessaria: "Restringir a seção de aplicação documental à propagação e consistência dos documentos; remeter os dez critérios e as preservações específicas aos critérios de aceite dos respectivos handoffs, sem misturá-los ao resultado da aplicação da ADR."
```

### QA-ADR0039-03

```yaml
id: QA-ADR0039-03
requisito_violado: "Metadados e seção de bloqueios devem representar o mesmo estado operacional."
evidencia_focal: "`rastreabilidade.handoffs_bloqueados` lista os três handoffs (ADR-0039:15-18), enquanto a seção `10. Bloqueios` declara `Nenhum` (ADR-0039:289-291)."
impacto: "O documento não permite determinar se os handoffs estão bloqueados ou apenas previstos, produzindo estado operacional contraditório."
correcao_necessaria: "Alinhar a chave de rastreabilidade e a seção de bloqueios: declarar os bloqueios reais, ou substituir a chave por metadado de handoffs previstos caso não exista bloqueio."
```

## Status

`ADR_REJECTED`

## Bloqueios

A ADR exige correção documental nos três pontos acima antes de ser aprovada.
