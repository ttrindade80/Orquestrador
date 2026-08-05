# Relatório do patch documental — ADR-0008 / ITEM-0015 / P05

```yaml
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ITEM-0015 / ADR-0008 / P05
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P04.md

bloqueio_tratado:
  arquivo: tela/testes_renderizador/fundamentos.py
  teste: teste_modelo_fabricado
  entrada: "desc fab"
  resultado_anterior: "desc fab"
  resultado_inicio_de_frase: "Desc fab"

decisao:
  campo: cabecalho.apresentacao.descricao.capitalizacao
  valor_adicionado: preservar
  semantica: operacao_identidade_apos_max_caracteres
  titulo_alterado: false

impacto_nas_72_telas:
  total: 72
  descricoes_que_mudariam_com_inicio_de_frase: 17
  caminhos:
    - config/telas/demo/h0035_centralizado_h_colunas.json
    - config/telas/demo/h0035_console_com.json
    - config/telas/demo/h0035_dashboard_com.json
    - config/telas/demo/h0035_esquerda_margens_min_max.json
    - config/telas/demo/h0035_h_margens_limitadas.json
    - config/telas/demo/h0035_h_uniforme.json
    - config/telas/demo/h0035_lancador_com.json
    - config/telas/demo/h0035_minimo_fixo_excedido.json
    - config/telas/demo/h0035_pref_colunas.json
    - config/telas/demo/h0035_pref_linhas.json
    - config/telas/demo/h0035_resto_horizontal.json
    - config/telas/demo/h0035_resto_vertical.json
    - config/telas/demo/h0035_v_margens_min.json
    - config/telas/demo/h0035_v_margens_min_max.json
    - config/telas/demo/h0035_v_uniforme.json
    - config/telas/demo/h0045_validacao_continuacao.json
    - config/telas/demo/h0045_validacao_vazio.json

execucao:
  status: PATCH_APLICACAO_ADR_COMPLETED
  arquivos_alterados:
    - docs/contratos/contrato_cabecalho.md
    - docs/nomenclatura/30_CABECALHO.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P05.md

resultado:
  verificacoes_executadas:
    - leitura integral dos cinco documentos do manifesto e buscas focais autorizadas
    - busca terminológica por capitalizacao e preservar
    - auditoria Python somente leitura das 72 descrições, com original[:200], isalpha() e upper()
    - rg normativo dos valores e das semânticas em contrato e nomenclatura
    - verificação mecânica dos três valores em ambos os documentos
    - confirmação focal de que a enumeração do título não recebeu preservar
    - git diff --check e git diff dos três caminhos do patch
  bloqueios: []
```

`preservar` foi incluído somente na enumeração de
`cabecalho.apresentacao.descricao.capitalizacao`. O contrato define a
operação identidade após o corte por `max_caracteres`, e a nomenclatura remete
algoritmo e exemplos completos ao contrato. A escolha continua pertencendo à
tela; migrações de descrições anteriormente literais devem usar `preservar`,
enquanto `inicio_de_frase` permanece uma escolha explícita. O título não foi
ampliado e o H-0049 não foi alterado.

A auditoria das 72 telas encontrou 17 descrições que mudariam com
`inicio_de_frase`; nenhuma alteração de JSON foi feita. Não houve QA,
alteração de código, testes ou preparação de stage.
