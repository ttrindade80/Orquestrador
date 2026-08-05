# Relatório do patch de handoff — H-0049 / P03

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0049 / P03
  predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_HANDOFF_H-0049_P02.md

bloqueio_tratado:
  tipo: fixtures_preexistentes_fora_do_manifesto
  arquivos_reportados:
    - tela/teste_resultado_execucao.py
    - tela/testes_renderizador/integracao.py
```

## Descoberta exaustiva

```yaml
descoberta_exaustiva:
  suite_integral_executada: true
  resultado_suite: "20 failed, 973 passed, 2 errors em 29.18s"
  busca_textual_executada: true
  inventario_ast_executado: true
  arquivos_com_fixture_incompativel:
    - tela/teste_resultado_execucao.py
    - tela/testes_renderizador/integracao.py
    - tela/teste_navegacao.py
    - tela/testes_renderizador/composicao_corpo.py
    - tela/testes_renderizador/comum.py
    - tela/testes_renderizador/lancador.py
    - tela/testes_renderizador/matriz_participantes.py
    - tela/testes_renderizador/selecao.py
    - demo/teste_demo_navegacao.py
    - demo/teste_demo_paginacao.py
    - demo/teste_diagnostico.py
  terceiros_encontrados:
    - tela/teste_navegacao.py
    - tela/testes_renderizador/composicao_corpo.py
    - tela/testes_renderizador/comum.py
    - tela/testes_renderizador/lancador.py
    - tela/testes_renderizador/matriz_participantes.py
    - tela/testes_renderizador/selecao.py
    - demo/teste_demo_navegacao.py
    - demo/teste_demo_paginacao.py
    - demo/teste_diagnostico.py
```

## Evidência

A suíte integral (`pytest -q --maxfail=0`) confirma falha material em três
frentes, não apenas nos dois arquivos reportados:

1. **`tela/teste_resultado_execucao.py`** — `_tela_base` (linha 70) fabrica
   `cabecalho` só com `titulo`/`descricao`; 18 testes falham com
   `TelaCampoObrigatorioAusente: cabecalho.apresentacao` porque passam por
   `carregar_tela`.
2. **`tela/testes_renderizador/integracao.py`** — o teste
   `test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao` (linha 352)
   fabrica um documento JSON com `cabecalho` incompleto e chama
   `carregar_tela`; falha com a mesma exceção, propagada via a fachada
   `tela/teste_renderizador.py` e via `demo/teste_diagnostico.py`.
3. **`demo/teste_diagnostico.py`** — `teste_telas_h0035_diagnostico` (linha
   388) fabrica um JSON inválido esperando `TelaEstruturaInvalida`; recebe
   `TelaCampoObrigatorioAusente` porque a validação de `cabecalho.apresentacao`
   antecede a validação de `distribuicao_matricial`. Este é um terceiro
   arquivo, com bloqueio próprio, independente dos dois reportados.
4. **`tela/testes_renderizador/composicao_corpo.py`** —
   `test_rejeicoes_loader_preservadas` (helper `_tela_horizontal`, linha
   2054) chama `carregar_tela` esperando `TelaEstruturaInvalida` por
   percentual/peso inválido; recebe `TelaCampoObrigatorioAusente` pelo mesmo
   motivo. Confirmado por execução isolada (`ERROR at teardown`, gate
   H-0038): `'T-NR03: loader rejeita percentual soma != 100 em horizontal'`,
   `'T-NR03: loader rejeita fracao com peso zero em horizontal'`.

Além dessas falhas *observadas* na suíte atual, o inventário AST (estendido
para cobrir também `cabecalho=` como argumento nomeado de `ModeloTela`, não
só dicionários literais de documento) encontrou **58 ocorrências em 13
arquivos** de `cabecalho` com `titulo`+`descricao` e sem `apresentacao`.
Dessas, duas (`tela/teste_modelo.py`, `tela/testes_renderizador/
fundamentos.py`) já pertencem ao manifesto original de três arquivos
autorizados a fabricar fixtures do H-0049 e não constituem bloqueio novo.
As demais nove pertencem a arquivos fora de qualquer manifesto:
`tela/teste_navegacao.py`, `tela/testes_renderizador/composicao_corpo.py`,
`tela/testes_renderizador/comum.py`, `tela/testes_renderizador/
lancador.py`, `tela/testes_renderizador/matriz_participantes.py`,
`tela/testes_renderizador/selecao.py`, `demo/teste_demo_navegacao.py`,
`demo/teste_demo_paginacao.py` e `demo/teste_diagnostico.py`.

Essas nove ainda **passam na suíte atual** porque `tela/renderizacao/
tela.py:114,349` consome `modelo.cabecalho.get("apresentacao")` — um
fallback que degrada para o comportamento antigo quando o campo está
ausente. Esse fallback é exatamente o que o H-0049 determina remover na
etapa "Renderer e geometria" ("o renderer... não pode... introduzir
fallback"). Portanto essas nove fixtures são estruturalmente inválidas
perante o schema fechado, mesmo sem falhar hoje: quando o fallback for
removido, cada uma quebrará pelo mesmo motivo dos arquivos já reportados.

## Fixtures incompatíveis (nominal, resumido)

```yaml
fixtures_incompativeis:
  - arquivo: tela/teste_resultado_execucao.py
    simbolo_ou_teste: _tela_base
    destino: [carregar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: tela/testes_renderizador/integracao.py
    simbolo_ou_teste: test_h0045_p04_ids_duplicados_impedem_qualquer_renderizacao (+ 8 ModeloTela diretos)
    destino: [carregar_tela, construir_modelo]
    falta: [cabecalho.apresentacao]
  - arquivo: demo/teste_diagnostico.py
    simbolo_ou_teste: teste_telas_h0035_diagnostico
    destino: [carregar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: tela/testes_renderizador/composicao_corpo.py
    simbolo_ou_teste: test_rejeicoes_loader_preservadas (_tela_horizontal) + 9 ModeloTela diretos
    destino: [carregar_tela, construir_modelo]
    falta: [cabecalho.apresentacao]
  - arquivo: tela/teste_navegacao.py
    simbolo_ou_teste: 6 fabricas ModeloTela (_construir e afins)
    destino: [construir_modelo, renderizar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: tela/testes_renderizador/comum.py
    simbolo_ou_teste: _modelo_h0029
    destino: [construir_modelo, renderizar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: tela/testes_renderizador/lancador.py
    simbolo_ou_teste: 6 fabricas ModeloTela (_h0034_modelo_*, _modelo_mc)
    destino: [construir_modelo, renderizar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: tela/testes_renderizador/matriz_participantes.py
    simbolo_ou_teste: 7 fabricas ModeloTela (_modelo_matriz_render_h0028 e afins)
    destino: [construir_modelo, renderizar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: tela/testes_renderizador/selecao.py
    simbolo_ou_teste: teste do H-0041 P21 (ModeloTela direto)
    destino: [construir_modelo, renderizar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: demo/teste_demo_navegacao.py
    simbolo_ou_teste: 2 fabricas ModeloTela
    destino: [construir_modelo, renderizar_tela]
    falta: [cabecalho.apresentacao]
  - arquivo: demo/teste_demo_paginacao.py
    simbolo_ou_teste: 4 fabricas ModeloTela
    destino: [construir_modelo, renderizar_tela]
    falta: [cabecalho.apresentacao]
```

## Execução

```yaml
execucao:
  status: BLOCKED_DOCUMENTATION
  arquivos_alterados: []
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0049_P03.md
```

## Decisão

O manifesto de bloqueio de dois arquivos, indicado no estado transportado, é
factualmente incompleto. Existem no mínimo nove arquivos adicionais com o
mesmo tipo de fixture incompatível — três deles já provocam falha material
na suíte atual (`demo/teste_diagnostico.py`,
`tela/testes_renderizador/composicao_corpo.py`, e o já conhecido
`integracao.py`), e outros seis ficam mascarados por um fallback do
renderer que o próprio H-0049 exige remover. Autorizar somente os dois
arquivos originalmente reportados deixaria a implementação bloqueada
novamente na mesma etapa, com o mesmo tipo de erro, assim que o fallback for
removido. Por essa razão, o handoff não foi alterado e o manifesto de
adequação de fixtures preexistentes precisa ser redefinido a partir da lista
completa acima antes de qualquer novo patch.

```yaml
resultado:
  arquivos_adicionados_ao_manifesto: []
  novas_fixtures_autorizadas: 0
  fixtures_persistentes_autorizadas: 0
  verificacoes_executadas:
    - "pytest -q --maxfail=0 (suíte integral): 20 failed, 973 passed, 2 errors"
    - "rg cabecalho em tela/teste_*.py, tela/testes_renderizador/*.py, demo/teste_*.py"
    - "inventário AST de dict literais 'cabecalho' sem 'apresentacao'"
    - "inventário AST estendido: argumento nomeado cabecalho= em chamadas ModeloTela(...)"
    - "execução isolada de tela/testes_renderizador/composicao_corpo.py::TestDistribuicaoHorizontalH0026::test_rejeicoes_loader_preservadas"
    - "leitura de tela/renderizacao/tela.py:114,349 confirmando fallback modelo.cabecalho.get('apresentacao')"
  bloqueios:
    - "9 arquivos com fixture incompatível fora do manifesto de 2 reportados e fora dos 3 já autorizados pelo H-0049 base"
```
