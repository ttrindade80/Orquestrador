# QA H-0077 pós-P02

- D-0027-10: reconciliado; parágrafo lógico completo, palavras inteiras, linhas físicas e justificação posterior.
- Consumidores: hierarquia, dois níveis por foco, tabela e conjuntos de campos fornecem texto lógico sem pré-fragmentação; prefixos, indicadores, indentação, largura, colunas, campos, verboso/não verboso e truncamento permanecem locais. Escopo principal preservado, com condicionais explícitas.
- Medição/mapa/paginação: `_altura_quebra_item`, `_renderizar_participante_com_indicador` e `_larguras_mapa_fisico_matricial` devem usar a mesma composição efetivamente renderizada; mapa e paginação derivam das linhas reais, sem fragmentação histórica.
- P16: os três testes permanecem sujeitos a nova regressão semântica; fixtures podem ser reconstruídos para preservar as políticas, sem restaurar quebra antiga ou mascarar expectativas.
- Palavra maior que largura: permanece íntegra; não há escolha global de clipping, overflow, scroll, erro, fallback, truncamento ou expansão de container.
- Truncamento: `_truncar_com_marcador` permanece separado e não trata palavra larga no compositor.
- ANSI: largura visual, CSI íntegro, SGR sem vazamento e palavra estilizada indivisível; sem parser/wrap paralelo.
- Regressão H-0076: comando focal obrigatório permanece exatamente definido, sem redefinir núcleo ou popup aprovados.
- H-0070: `QA-IMPL-H0077-03` permanece fora do escopo, sem correção sem nova evidência causal.
- Validação manual posterior: `python demo/demo.py h0077_texto_amplo_justificado`, somente após a regressão técnica.
- Achados: nenhum.
- Status final: `H1_HANDOFF_APPROVED`.
