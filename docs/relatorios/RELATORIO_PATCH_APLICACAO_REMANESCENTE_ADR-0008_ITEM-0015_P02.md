```yaml
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ITEM-0015 / ADR-0008 / P02
  cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  bloqueio_resolvido: schema_local_do_cabecalho_insuficientemente_determinado

decisao_materializada:
  titulo_e_descricao_permanecem_strings: true
  bloco_adicionado: cabecalho.apresentacao

execucao:
  status: PATCH_APLICACAO_ADR_COMPLETED
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P02.md
  arquivos_alterados:
    - docs/contratos/contrato_cabecalho.md
    - docs/nomenclatura/30_CABECALHO.md

resultado:
  delta_material:
    - cabecalho definido como objeto fechado com titulo, descricao e apresentacao como campos diretos obrigatorios.
    - titulo e descricao preservados como strings; apresentacao.titulo e apresentacao.descricao fechados com seus quatro campos obrigatorios cada.
    - configuracao local vinculada ao JSON estrutural de cada tela, sem fallback, valor implicito, fonte global, alias ou parametro desconhecido.
    - nomenclatura registra apresentacao e os dois subobjetos, preservando a autoridade integral do contrato para tipos, enumeracoes, limites e comportamento.
  verificacoes_executadas:
    - busca focal em docs/contratos/contrato_json_console.md; nenhuma afirmacao material incompatível localizada; arquivo não alterado.
    - busca de exatamente/somente/apresentacao nos documentos do cabeçalho.
    - busca dos oito campos de apresentação no contrato do cabeçalho.
    - git diff --check nos arquivos do patch.
    - git diff nos arquivos do patch.
  bloqueios: []
```
