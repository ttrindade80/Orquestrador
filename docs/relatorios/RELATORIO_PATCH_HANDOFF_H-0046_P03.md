---
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0046
  artefato_principal: docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md
  cadeia_raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0046.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0046_P02.md
  achados_tratados:
    - QA-PP-H0046-P02-01
    - QA-PP-H0046-P02-02
    - QA-PP-H0046-P02-03

execucao:
  status: HANDOFF_PATCHED
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0046_P03.md
  arquivos_alterados:
    - docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md

resultado:
  delta_material: []
  verificacoes_executadas:
    - compilação dos blocos Python alterados com compile(..., "exec")
    - casos sintéticos do detector de ciclos, fachada e aliases técnicos
    - casos de __all__ com símbolo ausente e símbolo extra
  bloqueios: []
---

# Relatório do patch P03

Foram corrigidos exclusivamente os três achados pendentes do QA pós-patch P02.

- O detector de ciclos passou a distinguir `ast.Import` simples do pacote
  `tela.renderizacao`, cobrindo `import tela.renderizacao` e a forma com alias,
  além das quatro formas proibidas e quatro permitidas, com normalização
  idêntica para aliases.
- A prova da fachada recebeu um mapa nominal fechado de módulos e símbolos
  reexportáveis. Imports genéricos, símbolos de módulo permitido mas não
  autorizados, proprietários incorretos e aliases arbitrários são rejeitados.
  A prova também confronta `__all__` com a lista fechada sem exigir ordem.
  Identidade de objeto e origem AST da reexportação usam o mesmo mapa.
- `aliases_autorizados` foi substituído por mapas de origem exata. O comando
  valida módulo, nome importado, nome local e ausência de import relativo para
  `calcular_distribuicao` e `alinhar_na_celula`.

As verificações sintéticas confirmaram todas as passagens e rejeições previstas;
os blocos Python alterados foram compilados com o nome de arquivo exigido. Não
foram alterados código, testes, arquitetura ou decisões funcionais.
