---
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_BLOCKED
objeto: H-0045 / VM-H0045-R08-001
patch: P24
data: "2026-08-02"
rastreabilidade:
  cadeia_raiz: VM-H0045-R08-001
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P23.md
  achados_tratados:
    - QA-H0045-P23-001
    - QA-H0045-P23-002
    - QA-H0045-P23-003
arquivos_alterados: []
---

# RELATÓRIO DE BLOQUEIO — PATCH P24 (H-0045 / VM-H0045-R08-001)

## status: IMPLEMENTATION_BLOCKED

A correção focal exigida pelos três achados QA-P23 colide com asserções
existentes em `demo/teste_demo.py`, arquivo **expressamente excluído** do
escopo autorizado pelo patch P24. Nenhuma alteração de código foi aplicada;
`git diff --check` permanece limpo e a suíte completa segue verde (base
confirmada antes do bloqueio).

## Análise dos produtores reais (QA-P23-001)

Enumeração dos produtores efetivos em `tela/renderizador.py`:

- `erro_layout:` — produtor **único** em `:2483`
  (`"erro_layout: chips da barra_de_menus ({0}) nao cabem em {1} caracteres
  uteis ... overflow.quando_nao_couber='erro_layout' proibe
  omitir/truncar/reordenar"`). Demais ocorrências são valor de config (`:185`),
  comparação `!= "erro_layout"` (`:1915`) e docstrings. Formato específico e
  exclusivo da barra — ancorável com segurança.
- `altura insuficiente:` — três produtores genuinamente geométricos
  (`:4455`, `:4504`, `:4512`): terminal/corpo baixo demais para
  cabeçalho+barra+corpo.
- Códigos `DA-02`/`DA-04` (`:3606`, `:3613`, `:3691`, `:3948`, `:4526`) —
  todos estruturais ("composição inválida ... sem distribuição declarada"),
  **não** geométricos. `DA-01` não tem produtor de erro real.

**Conclusão QA-P23-001:** nenhum código `DA` é exclusivamente geométrico; a
família `DA-0` deve ser removida da classificação. A correção focal
(ancorar `erro_layout` no formato específico da barra + reconhecer
`altura insuficiente`) é factível sem tocar o renderer. **Sem bloqueio
neste achado.**

## Bloqueio real — QA-P23-002 (propagação de erros estruturais)

QA-P23-002 exige que `_resolver_conteudo` (e não só os caminhos de consulta
de geometria) **relance** qualquer `RenderizadorErro` estrutural em vez de
mascará-lo para quadro mínimo.

**Colisão:** `demo/teste_demo.py`, função `teste_redimensionamento_reativo_h0023`
(assinatura em `:1724`), seção 8.12, linhas `2313-2317`:

```
with _patch("demo.demo.renderizar_estado", side_effect=_RenderizadorErro("r")):
    r_rc_err = _resolver_conteudo(_estado_rc, _modelo_rc, 80, 30)
_registrar("8.12: RenderizadorErro: retorna quadro minimo",
           r_rc_err.count("\n") == 30)
```

O teste injeta `RenderizadorErro("r")` (erro estrutural sintético, fora de
qualquer produtor geométrico) e registra como PASSOU que `_resolver_conteudo`
retorna o quadro mínimo de 30 linhas. QA-P23-002 ordena exatamente o oposto:
esse erro deve propagar. Aplicar a correção faz a verificação falhar
(`[FALHOU]` em `_registrar`, retornado como código ≠ 0 por `_finalizar`),
quebrando a suíte — e `demo/teste_demo.py` **não consta** entre os arquivos
autorizados (`demo/demo.py`, `tela/teste_renderizador.py`,
`demo/teste_demo_paginacao.py`, `demo/teste_demo_navegacao.py`).

## Bloqueio real — QA-P23-003 (quadro controlado unificado)

QA-P23-003 exige que **todas** as insuficiências geométricas aceitas
(barra, altura, área externa) usem semanticamente o **mesmo** quadro
controlado (`Terminal pequeno demais` / `Aumente a janela para continuar`).

**Colisão confirmada empiricamente:** `demo/teste_demo.py`,
`test_h0044_p01_redimensionamento_resolve_bloqueio_visual` (`:3969`),
linhas `3984-3985`:

```
saida_peq = _demo_mod._resolver_conteudo(estado, modelo_res, 120, 10)
assert "terminal pequeno demais" in saida_peq
```

Reprodução direta: em `120x10` com resultado H-0044 ativo, `renderizar_estado`
levanta `altura insuficiente: corpo requer 9 linhas mas area disponivel e 4
linhas ...` — erro geométrico real que `_e_insuficiencia_geometrica` já
classifica como `True`. O P23 atual o roteia ao quadro **mínimo canônico**
(`terminal pequeno demais`, minúsculo); QA-P23-003 manda roteá-lo ao quadro
**controlado** (`Terminal pequeno demais`, maiúsculo). O `assert` acima casa
o texto minúsculo e quebraria com a unificação. `demo/teste_demo.py` não é
autorizado.

## Função, motivo e autorização necessária

- **Funções afetadas:** `demo/demo.py::_resolver_conteudo` (foco QA-P23-002/003);
  secundariamente `_e_insuficiencia_geometrica`, `_e_erro_layout_barra` e
  `_quadro_terminal_insuficiente` (QA-P23-001/003, factíveis).
- **Motivo do bloqueio:** as correções de QA-P23-002 (relançar erro
  estrutural) e QA-P23-003 (unificar o quadro controlado para altura
  insuficiente) são incompatíveis com asserções **vigentes e verdes** em
  `demo/teste_demo.py` (seção 8.12 e `test_h0044_p01`), arquivo fora do
  escopo autorizado. O próprio manifesto estabelece a contradição: exige
  simultaneamente (a) remover o mascaramento em `_resolver_conteudo`,
  (b) manter a suíte completa verde e (c) não alterar `demo/teste_demo.py`.
- **Autorização adicional necessária:** inclusão nominal de
  `demo/teste_demo.py` no escopo do P24, restrita a:
  (1) `teste_redimensionamento_reativo_h0023` seção 8.12
  (`:2313-2317`) — substituir a expectativa de quadro mínimo por propagação
  do erro estrutural sintético (ou remover o subcaso do monkeypatch);
  (2) `test_h0044_p01_redimensionamento_resolve_bloqueio_visual`
  (`:3984-3985`) — alinhar a asserção ao quadro controlado unificado
  (`Terminal pequeno demais`) para o caso de altura insuficiente.
  Sem essa autorização, qualquer uma das duas correções quebra a suíte.

## Preservações

O estado lógico do P23 (objeto canônico de distribuição, `linhas.minimo=1`,
`linhas.maximo=5`, escolha da menor quantidade válida, default global de
duas linhas, `overflow erro_layout`, ausência de omissão/truncamento/
reordenação, recuperação automática, `rotulo_dinamico_esc`, duplo Esc,
comandos geométricos como no-op durante geometria inválida) permanece
intacto: nenhuma linha de produção foi alterada.

## Verificações

- `git diff --check` (sem alterações aplicadas): limpo.
- Suíte completa antes do bloqueio: verde.

## Limite

Pausado antes de qualquer alteração de código. Não foi feito QA, validação
manual, stage ou commit.
