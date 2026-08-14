# Relatório QA Handoff — H-0071 pós-P05

status: H2_HANDOFF_PATCH_REQUIRED

## ACH-QA-H0071-P05-01

- requisito: O handoff deve definir caminho nominal do relatório futuro de implementação ou regra inequívoca para esse caminho.
- evidência focal: A seção 6.1 apenas afirma que o relatório futuro permanece “autorizado e separado”. A seção 9 nomeia somente o relatório da etapa PATCH_HANDOFF (`docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0071_P05.md`) e afirma que o relatório futuro será produzido depois da implementação, sem indicar seu caminho. A referência a `RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P04.md` na seção 1 é explicitamente tratada como relatório anterior e não define o artefato futuro.
- impacto: A implementação pode ser concluída sem destino documental inequívoco para seu relatório obrigatório, tornando o handoff documentalmente incompleto e dificultando a localização e a rastreabilidade do resultado.
- correção necessária: Em novo patch, nomear explicitamente o caminho do relatório futuro de implementação ou estabelecer regra única e inequívoca de nomeação/localização, distinguindo-o do relatório PATCH_HANDOFF e do relatório P04 histórico.
