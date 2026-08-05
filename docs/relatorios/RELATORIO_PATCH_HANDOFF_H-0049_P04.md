# Relatório do patch de handoff — H-0049 / P04

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0049 / P04
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P03.md

descoberta_transportada:
  ocorrencias: 58
  arquivos_com_ocorrencias: 13
  arquivos_ja_autorizados: 2
  arquivos_adicionados_ao_manifesto: 11
  arquivos_com_falha_observada: 4
  arquivos_mascarados_pelo_fallback: 7

correcao_factual_p03:
  frase_incorreta: outros_seis_ficam_mascarados
  quantidade_correta: 7
  lista_nominal_preservada: true
```

## Objeto do patch

Redefinir integralmente o manifesto de adequação de fixtures preexistentes
do H-0049, com base na descoberta exaustiva do P03, sem implementar código,
sem migrar JSON e sem alterar o relatório P03.

## Verificação da lista nominal transportada

Os onze arquivos leram-se integralmente (não por amostragem) para confirmar,
símbolo a símbolo, a classificação do P03 antes de redigir o manifesto:

- `tela/teste_resultado_execucao.py` — fábrica única `_tela_base` (linha 69),
  reutilizada por 5 funções de teste (18 casos parametrizados). Nenhuma
  mutação testada toca `cabecalho`/`apresentacao`.
- `tela/teste_navegacao.py` — 6 literais `ModeloTela(cabecalho=...)` inline,
  um por função de teste, sem fábrica compartilhada entre `def test_*`
  diferentes (um `_construir` local é reaproveitado 3× dentro de uma única
  função). Nenhum teste do arquivo levanta exceção de schema.
- `tela/testes_renderizador/integracao.py` — 8 `ModeloTela(...)` diretos
  mais 1 dict JSON cru (teste de IDs duplicados, linha 355) = 9 ocorrências,
  batendo com "+ 8 ModeloTela diretos" do P03. Confirmada a exceção
  `TelaEstruturaInvalida` com `"id de console duplicado" in str(exc)`.
- `tela/testes_renderizador/composicao_corpo.py` — `_tela_horizontal`
  (linha 2053, único caminho que passa pelo loader real) mais 9 sítios de
  `ModeloTela(`, dos quais dois são as fábricas compartilhadas
  `_modelo_horizontal` (~30 usos) e `_modelo_hierarquico` (~21 usos).
  Confirmados os dois casos de `test_rejeicoes_loader_preservadas`
  (percentual soma ≠ 100; fração com peso zero), ambos esperando
  `TelaEstruturaInvalida` sem asserção de texto — por isso a fixture precisa
  de `apresentacao` válida, para que a exceção não seja mascarada por um
  motivo de cabeçalho coincidente em classe.
- `tela/testes_renderizador/comum.py` — fábrica `_modelo_h0029` (linha 292),
  confirmada como fonte reutilizada pelos ~20 testes de
  `TestCardinalidadeUnitariaH0029` em `matriz_participantes.py`.
- `tela/testes_renderizador/lancador.py` — 6 fábricas confirmadas
  (`_h0034_modelo_lancador`, `_h0034_modelo_isolado`,
  `_h0034_modelo_alinhamento`, mais 3 inline/`_modelo_mc`), todas exclusivas
  de lançador/navegação responsiva; nenhuma toca matriz ou participante.
- `tela/testes_renderizador/matriz_participantes.py` — 7 fábricas
  confirmadas (`_modelo_matriz_render_h0028` e 6 afins em
  `TestDistribuicaoMatricialH0035`), cobrindo matriz H-0028 e grade H-0035.
- `tela/testes_renderizador/selecao.py` — 1 `ModeloTela` direto confirmado
  (`TestRotuloDinamicoEscP21`, linha 833). Único achado textual de
  "apresentacao" no arquivo é o nome de outro teste
  (`test_h0041_p04_chip_ativo_preserva_apresentacao`), falso positivo léxico
  sem relação com o schema do cabeçalho — não é negativa intencional.
- `demo/teste_demo_navegacao.py` — 2 `ModeloTela` diretos confirmados
  (linhas 313 e 664), ambos de navegação/indicador visual, sem tocar
  paginação.
- `demo/teste_demo_paginacao.py` — 4 `ModeloTela` diretos confirmados
  (linhas 1034, 1179, 3390, 3410), todos de paginação/navegação combinadas.
- `demo/teste_diagnostico.py` — fixture única `tela_inv` dentro de
  `teste_telas_h0035_diagnostico` (linha ~390), esperando
  `TelaEstruturaInvalida` por `distribuicao_matricial.ordem: diagonal`, sem
  asserção de texto.

Nenhum dos onze arquivos contém teste cuja finalidade seja rejeitar
intencionalmente `cabecalho.apresentacao` ou algum de seus campos — a
ausência em todos é incidental, anterior ao contrato do H-0049. A
contagem fecha em 13 arquivos com ocorrências antigas (2 já autorizados + 11
acrescentados), consistente com o P03.

## Correção factual do P03

A frase "outros seis ficam mascarados" do relatório P03 é erro aritmético: a
própria lista nominal do P03 enumera sete arquivos mascarados pelo fallback
do renderer (`tela/teste_navegacao.py`, `tela/testes_renderizador/comum.py`,
`tela/testes_renderizador/lancador.py`, `tela/testes_renderizador/
matriz_participantes.py`, `tela/testes_renderizador/selecao.py`,
`demo/teste_demo_navegacao.py`, `demo/teste_demo_paginacao.py`). O P03 não
foi alterado; a correção fica registrada aqui e no handoff.

## Alteração produzida

`docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md`
recebeu a seção "Manifesto adicional de fixtures preexistentes (P04)",
inserida entre "Testes e demonstração autorizados" e "Validação
obrigatória", contendo: o manifesto de 14 arquivos autorizados (3 originais
+ 11 acrescentados); a política corrigida de fixtures; o bloco obrigatório
de apresentação válida; o tratamento de fixtures inválidas por outro motivo
(com os três pontos sensíveis nominados); a confirmação de ausência de
negativas intencionais nos onze arquivos; o escopo por arquivo; a proibição
de alteração funcional; a preservação visual; a orientação de estado
parcial da implementação; a validação focal futura; a validação das
negativas originais; o inventário AST futuro; a conferência de diff futura;
os campos adicionais do relatório `IMP-0049`; e os treze critérios de
aceite adicionais. Nenhum outro conteúdo do handoff foi alterado.

## Execução

```yaml
execucao:
  status: PATCH_HANDOFF_COMPLETED
  arquivos_alterados:
    - docs/handoff/H-0049-materializacao-local-dos-parametros-do-cabecalho.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P04.md
```

## Resultado

```yaml
resultado:
  novos_cenarios_autorizados: 0
  novas_fixtures_autorizadas: 0
  fixtures_persistentes_autorizadas: 0
  verificacoes_executadas:
    - "leitura integral dos 11 arquivos acrescentados ao manifesto (tela/teste_resultado_execucao.py, tela/teste_navegacao.py, tela/testes_renderizador/integracao.py, tela/testes_renderizador/composicao_corpo.py, tela/testes_renderizador/comum.py, tela/testes_renderizador/lancador.py, tela/testes_renderizador/matriz_participantes.py, tela/testes_renderizador/selecao.py, demo/teste_demo_navegacao.py, demo/teste_demo_paginacao.py, demo/teste_diagnostico.py)"
    - "leitura focal de tela/teste_modelo.py e tela/testes_renderizador/fundamentos.py confirmando helper _cabecalho_h0049 já completo nos dois arquivos originais"
    - "leitura focal de tela/renderizacao/tela.py:114,349 confirmando o fallback modelo.cabecalho.get('apresentacao') a ser removido pela implementação"
    - "conferência símbolo a símbolo de cada fábrica/fixture nominal do P03 contra o conteúdo real dos 11 arquivos: nenhuma divergência encontrada"
    - "confirmação de ausência de negativas intencionais do H-0049 nos 11 arquivos acrescentados"
    - "rg -n -C 4 sobre os nomes dos 11 arquivos no handoff atualizado, confirmando presença de todos"
    - "rg -n -C 5 sobre '58|13 arquivos|11 arquivos|quatro arquivos|sete arquivos|negativas intencionais|fixture persistente' no handoff atualizado"
    - "git diff --check nos dois arquivos alterados/criados: sem problema de espaço em branco"
    - "git diff dos dois arquivos alterados/criados: revisado manualmente, contém somente o manifesto documental descrito"
  bloqueios: []
```
