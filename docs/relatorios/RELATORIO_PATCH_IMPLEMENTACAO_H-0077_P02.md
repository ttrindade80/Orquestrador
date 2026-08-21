---
cadeia:
  raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0077.md
  origem_reabertura: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0076_POS_P02.md
  handoff_atualizado: docs/relatorios/RELATORIO_QA_HANDOFF_H-0077_POS_P02.md

decisao_aplicada:
  - D-0027-10

autorizacao_adicional:
  arquivo:
    - tela/teste_formato_filho_dois_niveis_por_foco.py
  motivo: fixtures_dependentes_de_fragmentacao_de_palavra_incompativel_com_D-0027-10
  alcance:
    - teste_quebra_multilinha_quando_nao_cabe_mesmo_apos_compactacao
    - teste_continuacao_sem_novo_cursor_toggle_ou_identidade
---

# Relatório do patch de implementação H-0077 P02

## Resultado inicial e classificação

A suíte focal inicial registrou `630 passed, 6 failed`; a regressão H-0076
registrou `91 passed`; os três P16 registraram `1 passed, 2 failed`.

As falhas foram classificadas assim:

- A: os dois testes de tabela de `teste_formato_filho_dois_niveis_por_foco.py`
  dependiam da fragmentação física de `Valor1`; foram reconciliados com duas
  palavras lógicas (`Valor um`), preservando a continuação e os indicadores.
- A: os dois P16 que falharam e a contagem do item grande usavam fixtures cuja
  ocupação física dependia da antiga composição; foram reconstruídos no arquivo
  autorizado de paginação.
- A: o teste ANSI esperava múltiplas linhas para uma única palavra estilizada;
  passou a usar duas palavras estilizadas, mantendo CSI/SGR íntegros.
- D: `tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
  permanece o resíduo independente `QA-IMPL-H0077-03`.

Os dois testes autorizados de dois níveis passaram isoladamente (`2 passed`).

## Alterações e consumidores

Alterações desta execução: `tela/teste_formato_filho_dois_niveis_por_foco.py`,
`tela/teste_paginacao.py`, `tela/teste_estilo_h0073_h0063.py` e este relatório.
Nenhuma alteração funcional nova foi feita no núcleo ou nos consumidores; o
estado transportado já usa `compor_texto` em hierarquia, dois níveis por foco,
tabela, conjuntos, matriz e paginação.

`_altura_quebra_item`,
`_renderizar_participante_com_indicador` e
`_larguras_mapa_fisico_matricial` usam a composição canônica e a largura útil
da célula. O mapa físico e a paginação derivam das linhas físicas reais; não há
wrapper local de composição nem reutilização de linhas como entrada lógica.
Truncamento deliberado continua separado em `_truncar_com_marcador`.

## P16, palavra larga e ANSI

Foi criado um fixture exclusivo P16 com palavras de 37 colunas e largura
textual efetiva 76: 7/5 palavras produzem 4/3 linhas e 17 palavras produzem 9
linhas. As políticas de fluxo contínuo, movimento integral condicional e
fragmentação somente quando maior que a página permaneceram inalteradas.
Resultado isolado: `3 passed`.

Palavra maior que a largura permanece íntegra e não é truncada, dividida,
hifenizada ou convertida em fallback. Os testes canônicos de palavra
indivisível, recomposição, justificação e ANSI passaram (`5 passed`); os testes
ANSI focais passaram (`2 passed`).

## Demonstrações, autoridade e suítes finais

Demonstrações focais: conteúdo externo `4 passed`; matriz `12 passed`;
mapa/paginação `3 passed`. A busca de autoridade encontrou apenas
`composicao_textual.py` como implementação genérica; `_quebrar_sem_ansi` segue
restrita à primitiva ANSI existente.

Suíte focal final: `635 passed, 1 failed`, somente o H-0070 independente.
Regressão H-0076 final: `91 passed`.

## Bloqueios e situação H-0070

Não há bloqueio de escopo após a autorização focal. H-0070 não foi alterado.
Não foi feita validação manual, nem stage, commit ou push.
