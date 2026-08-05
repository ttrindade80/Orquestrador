# Relatório de QA do patch de handoff — H-0049 / P06

```yaml
cadeia:
  raiz: docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P06.md

enumeração:
  campo: cabecalho.apresentacao.descricao.capitalizacao
  valores: [maiusculas, inicio_de_frase, preservar]
  obrigatorio: true
  ausencia_invalida: true
  preservar_e_default_ou_fallback: false
  valor_desconhecido_invalido: true
  negativos_exigidos: [null, inteiro, lista, objeto]

baseline_migratorio:
  titulo:
    posicao: esquerda
    recuo_lateral: 0
    capitalizacao: maiusculas
    formato_na_borda: com_espacos_laterais
  descricao:
    max_caracteres: 200
    alinhamento: esquerda
    recuo: 1
    capitalizacao: preservar

titulo:
  inalterado: true
  preservar_aceito: false

ocorrencias_inicio_de_frase:
  total: 22
  classificacao:
    valor_suportado: [43, 92, 97, 403, 411]
    algoritmo_normativo: [107, 523, 530]
    teste_especifico: [583, 586, 598, 1014]
    exemplo_de_contraste: [738]
    registro_do_baseline_anterior_rejeitado: [54, 199, 205, 302, 969, 1010]
    criterio_de_bloqueio: [879, 884, 889]
  ocorrencias_baseline_antigo: 0

evidencia_desc_fab:
  arquivo: tela/testes_renderizador/fundamentos.py
  teste: teste_modelo_fabricado
  entrada: "desc fab"
  resultado_anterior: "desc fab"
  resultado_com_inicio_de_frase: "Desc fab"
  resultado_com_preservar: "desc fab"
  expectativa_alterada: false

testes_exigidos:
  preservar:
    - "desc fab → desc fab"
    - "Desc fab → Desc fab"
    - "  execução da API REST →   execução da API REST"
    - "123 - execução → 123 - execução"
    - "ßeta → ßeta"
    - "vazio → vazio"
  inicio_de_frase: "mantido, inclusive ßeta → SSeta, sem locale ou normalização"
  maiusculas: "mantido com str.upper(), separadamente"
  semantica_preservar: "texto_capitalizado = texto_cortado após max_caracteres"

contagens_preservadas:
  jsons: {total: 80, telas_estruturais: 72, conteudos_externos: 8}
  fixtures: {ocorrencias_antigas: 58, arquivos_com_ocorrencias: 13,
    arquivos_autorizados: 14, arquivos_adicionais: 11,
    falhas_observadas: 4, mascarados_pelo_fallback: 7}
  demais: "max_caracteres 1..200; baseline geométrico 0/1; descarte 3/10; pytest -q --maxfail=0; hashes e proibições preservados"

escopo:
  somente: [docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md,
    docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P06.md]
  arquivos_nao_rastreados: true
  git_diff_no_index_retorno: 1
  whitespace: aprovado
  stage_ou_commit: false

novos_achados: []
status: H1_HANDOFF_APPROVED
implementacao_liberada: true
proxima_acao: IMPLEMENTAR
```

As 22 ocorrências de `inicio_de_frase` são exclusivamente suportadas pelas
categorias permitidas; nenhuma determina baseline de preservação. A busca
mecânica registrou `ocorrencias_preservar: 9` e `suspeitas: 0`. O P06 e o
handoff correspondem quanto à enumeração, baseline `preservar`, título,
impacto `72/17`, fixtures `58/13`, testes, verificações e ausência de
bloqueios.
