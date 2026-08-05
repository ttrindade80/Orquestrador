# Relatório de QA pós-patch — ADR-0008 / ITEM-0015 / P05

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P05.md

objeto_retestado:
  - descricao.capitalizacao.preservar
  - impacto_do_inicio_de_frase_nas_72_telas

resultado:
  enumeracao_confirmada:
    campo: cabecalho.apresentacao.descricao.capitalizacao
    valores: [maiusculas, inicio_de_frase, preservar]
    obrigatorio: true
    preservar_e_default_ou_fallback: false
  semantica_preservar: aprovada
  outras_operacoes_preservadas: true
  titulo_inalterado: true
  ordem_confirmada:
    - corte por max_caracteres
    - capitalizacao
    - alinhamento e recuo
    - limitacao geometrica
  telas_auditadas: 72
  descricoes_afetadas_por_inicio_de_frase: 17
  correspondencia_nominal_dos_17: exata
  escopo_p05:
    - docs/contratos/contrato_cabecalho.md
    - docs/nomenclatura/30_CABECALHO.md
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P05.md
  h0049_alterado_pelo_p05: false
  git_diff_check: aprovado
  novos_achados: []
  status: ADR_APPLICATION_APPROVED
  patch_h0049_liberado: true
  proxima_acao: PATCH_HANDOFF
```

O contrato define `preservar` como identidade sobre o texto já cortado:
nenhum caractere é convertido, inserido, removido ou normalizado, sem
`upper()`, `lower()`, `isalpha()` ou locale; prefixo, sufixo, frases
posteriores e string vazia permanecem literais. Os exemplos e o contraste com
`inicio_de_frase` e `maiusculas` estão presentes. As semânticas anteriores de
`maiusculas` e `inicio_de_frase`, inclusive `str.upper()`, `isalpha()`,
expansões Unicode, ausência de locale e ausência de normalização, permanecem
aprovadas.

A nomenclatura declara os três valores, atribui a escolha concreta à tela e
remete algoritmo, ordem e exemplos ao contrato, sem default, fallback ou
enumeração concorrente. A busca ampla classificou as ocorrências normativas
no contrato/nomenclatura, a ocorrência do relatório P05 como relatório, o
`inicio_de_frase` ainda presente no H-0049 como handoff posterior e demais
ocorrências como lexicais não relacionadas. O H-0049 não foi reprovação nesta
etapa e está liberado para o patch de handoff.
