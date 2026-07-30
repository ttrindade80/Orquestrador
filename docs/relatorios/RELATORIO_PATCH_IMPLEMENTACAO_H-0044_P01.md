---
name: REL-PATCH-H0044-IMPL-P01-terminal-pequeno-demais
description: "Delta factual: corrige o bloqueio visual 'terminal pequeno demais' persistente em TTY real durante os envelopes de resultado (RVM-H0044-06/07/08)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status: IMPLEMENTATION_PATCHED
  data: 2026-07-29
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: renderizador_envelope_resultado
  cadeia_raiz: H-0044
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0044.md
  handoff: docs/handoff/H-0044-integracao-fluxo-focal-dry-run-restauracao-origem.md
  achados_tratados: [VALIDACAO-MANUAL-H0044-001]
---

# REL-PATCH-H0044-IMPL-P01 — Patch

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
handoff: H-0044
achado_tratado: [VALIDACAO-MANUAL-H0044-001]
divergencia: TERMINAL_PEQUENO_DEMAIS
```

## 2. Cadeia

```yaml
raiz: H-0044
predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0044.md
achados_tratados: [VALIDACAO-MANUAL-H0044-001]
achados_resolvidos: [VALIDACAO-MANUAL-H0044-001]
achados_pendentes: []
novos_achados: []
validacao_manual:
  status: SUSPENSA_ATE_QA
  retomar_em: RVM-H0044-06
```

## 3. Causa raiz comprovada

O bloqueio visual `Terminal pequeno demais` permanecia mesmo com o terminal
maximizado e a fonte reduzida porque **não derivava das dimensões físicas**:
derivava de um off-by-one na contagem vertical da tela de resultado.

Reprodução isolada (PTY/largura fixa): ao acionar `Enter` sobre qualquer item
cujo resultado abre o **envelope** (`__falha_operacional__`,
`__resultado_invalido__`, `__interrupcao__` — exatamente RVM-06/07/08), o
renderer levantava `RenderizadorErro` com o padrão invariante

```text
altura insuficiente: corpo requer (H-5) linhas mas area disponivel e (H-6)
```

para **qualquer** `H` e **qualquer** largura. `_resolver_conteudo` (demo.py)
captura esse erro e exibe o quadro mínimo — daí a persistência do bloqueio.

Mecanismo: canais capturados do executor (stdout/stderr) e o próprio
`resultado_bruto` carregam `\n` à direita ou embutidos (ex.: o stderr do
controle sintético é `"ERRO: falha operacional sintetica.\n"`,
`demo/executor_sintetico.py:42`). O envelope `conjuntos_campos` coloca o valor
bruto em uma única linha de conteúdo; o `\n` vira uma quebra de linha física
fantasma dentro dessa "linha", inflando a contagem vertical em uma unidade.
Assim o corpo passava a exigir sempre `area_disponivel + 1`. A apresentação
`documento` (itens normais) não era afetada porque os valores de campo
produzidos pelo executor sintético para resultados normais não continham
quebras `\n`. Documento e envelope percorrem a mesma função de renderização.

Por que os testes PTY existentes não reproduziram: `test_h0044_pty_ciclo_basico`
abria resultado apenas sobre `item_01`, cujos valores de campo não continham
`\n` e, portanto, não acionavam o defeito. Os RVMs 01–05 usam resultados
normais sem essas quebras; 06–08 exercitam os três envelopes que as continham.

## 4. Delta aplicado

```yaml
delta_material:
  - id_achado: VALIDACAO-MANUAL-H0044-001
    alteracao: >
      normalizar o espaco em branco do texto visivel do valor de cada campo
      nome_valor do envelope (cada campo segue sendo uma unica linha visivel),
      eliminando a quebra fisica fantasma; o valor bruto do envelope permanece
      intocado
arquivos_alterados:
  - caminho: tela/renderizador.py
    delta: >
      _texto_valor_campo normaliza o texto visivel com " ".join(... .split())
      (uma linha); docstring registra a causa raiz. Alteracao funcional de
      uma linha; sem paginacao, rolagem, segunda tela ou mudanca material da
      composicao H-0044.
arquivos_testes_alterados:
  - caminho: tela/teste_renderizador.py
    delta: >
      testes focais do limite calculado, do envelope de falha/invalido/
      interrupcao, do redimensionamento e da normalizacao do valor de campo.
  - caminho: demo/teste_demo.py
    delta: >
      testes do ciclo completo RVM-06/07/08 (navegacao + selecao + Enter +
      resultado sem 'terminal pequeno demais'), PTY grande (192x50) e
      redimensionamento via _resolver_conteudo.
arquivos_criados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0044_P01.md
arquivos_removidos: []
```

Arquivos preservados com diff vazio confirmado: `tela/execucao_focal.py`,
`tela/resultado_execucao.py`, `tela/selecao.py`, `tela/navegacao.py`,
`tela/modelo.py`, `demo/executor_sintetico.py`,
`config/telas/demo/h0041_selecao_multipla_oito_itens.json`,
`config/telas/demo/resultado_execucao.json`,
`demo/fixtures/h0042_fixture_execucao.json`. `config/estilo.json` intocado
por este patch (seu delta pertence à aplicação documental da ADR-0037,
anterior ao ciclo H-0044).

## 5. Verificações locais

```yaml
verificacoes_executadas:
  - comando: >
      pytest tela/teste_renderizador.py tela/teste_fluxo_execucao.py demo/teste_demo.py
    resultado: 409 passed
  - comando: >
      pytest tela/teste_execucao_focal.py tela/teste_resultado_execucao.py tela/teste_fluxo_execucao.py
    resultado: 128 passed
  - comando: pytest (suite completa)
    resultado: 763 passed
  - comando: python -m json.tool config/telas/demo/h0044_fluxo_execucao_integrado.json
    resultado: valido
  - comando: git diff --check
    resultado: sem problemas de espaco em branco
  - comando: git diff --cached --name-only
    resultado: vazio (stage permanece vazio)
verificacoes_semanticas:
  - limite_calculado: >
      altura minima renderizavel do envelope de falha = altura natural do
      conteudo (15 a w=120); uma linha a menos produz RenderizadorErro
      (terminal realmente insuficiente).
  - tty_grande: >
      os tres envelopes (falha operacional, resultado invalido, interrupcao)
      renderizam sem 'terminal pequeno demais' a 120x30 e 192x50; valor bruto
      stderr mantido intacto no envelope.
  - redimensionamento: >
      abaixo do minimo (altura insuficiente) -> quadro minimo via
      _resolver_conteudo; dimensões suficientes -> tela normal, mesma
      instancia de fluxo e de modelo de resultado (sem releitura).
  - regressao: >
      H-0041/H-0042/H-0043 intactos; H-0044 origem mantem 8 itens em coluna
      unica, sem paginacao; apresentacao documento (RVM 01-05) inalterada.
```

Verificação local não equivale a QA independente.

## 6. Bloqueios e evidências

```yaml
bloqueios: []
evidencias_separadas: []
```

## 7. Observações

A correção não reduz conteúdo material nem oculta chips; não cria paginação,
rolagem, segunda tela ou mudança material da composição definida pelo H-0044.
A tela H-0044 continua com oito itens em uma coluna; `__falha_operacional__`
(sexta posição) é alcançável; seleção, toggle, execução e retorno não foram
modificados. A validação manual fica suspensa até QA proporcional, retomando
em RVM-H0044-06.
