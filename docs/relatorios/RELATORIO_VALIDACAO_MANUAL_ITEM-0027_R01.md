item: ITEM-0027
resultado: REPROVADA
origem: popup_texto_amplo_justificado
defeito:
  - palavras_partidas_por_largura_fisica
  - composicao_nao_trata_paragrafo_completo_como_unidade
decisao_de_retorno: PATCH_ADR-0049_P03

A falha foi observada visualmente durante resize, no popup com texto longo
justificado. O fechamento foi cancelado. Não houve commit e não houve push.
