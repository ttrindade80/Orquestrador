---
item: ITEM-0015
adr: ADR-0008
etapa: QA_POS_PATCH

cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P01.md

achados_retestados:
  - QA-08-01

resultado:
  status: ADR_APPLICATION_APPROVED_WITH_NOTES
  achados_resolvidos:
    - QA-08-01
  achados_novos: []
---

# QA pós-patch — ADR-0008 / ITEM-0015 / P01

## QA-08-01

Resolvido. `docs/nomenclatura/30_CABECALHO.md` declara que textos e
parâmetros locais do cabeçalho são configuração declarativa no JSON estrutural
da tela; distingue a aparência global compartilhada em `config/estilo.json`;
e registra que o estado vivo é produzido ou mantido durante a execução, não é
armazenado no JSON estrutural da tela e não pertence a `config/estilo.json`.

O módulo remete a definição geral aos módulos `01_NUCLEO_COMUM` e
`02_ARTEFATOS_CONFIGURACAO_E_RUNTIME`, sem redefinir esses termos, e mantém
`docs/contratos/contrato_cabecalho.md` como autoridade comportamental completa.

## Verificações focais

- Leitura integral do módulo 30 e do relatório P01.
- Buscas focais autorizadas nos módulos 01 e 02 e no achado original QA-08-01.
- Diff obrigatório restrito aos dois caminhos do patch; o working tree mostra o
  módulo 30 modificado e o relatório P01 presente como arquivo novo.
- Preservados: cabeçalho como região fixa e obrigatória, campos `titulo` e
  `descricao`, schema de apresentação, origem local no JSON estrutural,
  fronteira com aparência global e proveniência da ADR-0008.
- `git diff --check -- docs/nomenclatura/30_CABECALHO.md docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P01.md`: aprovado.

## Nota factual sobre o relatório P01

O relatório P01 registra `resultado.delta_material: []`, embora o diff contenha
alteração material no módulo 30. Trata-se de correção factual do próprio
relatório, sem defeito semântico remanescente e sem necessidade de reabrir o
patch documental. Próxima ação: correção factual manual e pontual do relatório
P01 existente.

status: ADR_APPLICATION_APPROVED_WITH_NOTES
proxima_acao: CORRECAO_FACTUAL_RELATORIO
