# QA pós-patch — ADR-0042 / P01

cadeia:
  raiz: docs/relatorios/RELATORIO_QA_ADR-0042.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_ADR-0042_P01.md

achados_resolvidos:
  - id: QA-ADR-0042-01
    verificacao: A ADR não fixa quantidade ou sequência de handoffs nem condiciona, por si, o avanço para aplicação, handoff ou implementação. As etapas posteriores permanecem apenas como etapas posteriores; D-MULTI-11 preserva critérios futuros de demonstração.
  - id: QA-ADR-0042-02
    verificacao: `tabela` permanece passiva, sem fallback para `nivel_unico`, e a declaração incompatível permanece `falha focal`, sem momento, camada ou mecanismo de rejeição/tratamento determinado.
  - id: QA-ADR-0042-03
    verificacao: No toroide de filhos, `Esc` retorna aos pais, preserva exatamente um filho selecionado por pai, não limpa a escolha e não cancela. A precedência é contextual, sem alteração das demais políticas e sem nova semântica de Enter, execução, confirmação ou persistência.

status: ADR_APPROVED
