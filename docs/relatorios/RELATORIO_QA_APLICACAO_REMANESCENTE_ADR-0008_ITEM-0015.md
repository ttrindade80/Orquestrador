---
item: ITEM-0015
adr: docs/adr/ADR-0008-modelo-configuracao-por-tela.md
status: ADR_APPLICATION_REJECTED
relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
achados:
  - id: QA-08-01
    requisito_violado: QA-08 — `docs/nomenclatura/30_CABECALHO.md` deve distinguir parâmetros locais, aparência global e estado vivo.
    evidencia_focal: "Em `docs/nomenclatura/30_CABECALHO.md:80-92`, o módulo distingue parametrização local e `config/estilo.json`, mas não define nem menciona estado vivo/runtime; a busca autorizada por `estado de runtime` não encontrou ocorrência nesse arquivo."
    impacto: "A nomenclatura não fecha a fronteira completa da ADR-0008 e pode deixar valores de execução confundidos com configuração declarativa do cabeçalho."
    correcao_necessaria: "Atualizar o módulo 30 para declarar explicitamente que estado vivo/runtime pertence à execução e não é armazenado no JSON estrutural da tela, preservando a autoridade dos módulos 01/02 e do contrato do cabeçalho."
---
