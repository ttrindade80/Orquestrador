# RELATORIO_PATCH_IMPLEMENTACAO H-0072 P01

```yaml
etapa: PATCH_IMPLEMENTACAO
objeto: H-0072
patch: P01
data: 2026-08-15
status: IMPLEMENTATION_PATCHED
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0072_POS_P01.md
causa: ADR-0047 P03 / H-0072 handoff P01
nao_sobrescrito: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
```

## 1. Proveniência

Antes desta execução, `git status --short --untracked-files=all` mostrava
os quatro arquivos autorizados como não rastreados (implementação original
de H-0072, QA `I1_IMPLEMENTATION_APPROVED`). Este P01 não redesenha essa
capacidade. O delta causal desta execução é somente: validação de
`prefixo`/`sufixo` no loader; adornos no console tabular da fixture
genérica; testes §21.1; asserções `(A)`/`(B)` na demonstração. O diff
integral contra HEAD mistura o original e não prova isoladamente este
patch.

Arquivos de §4.2 (modelo, renderer, navegação, `demo.py`) e os
preservados (`h0055`, `h0063`, H-0073, conteúdo externo H-0072,
`RELATORIO_IMPLEMENTACAO_H-0072.md`) não foram editados.

## 2. Arquivos efetivamente alterados/criados nesta execução

- `tela/carregamento/formato_dois_niveis_por_foco.py`
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json`
- `tela/teste_formato_filho_dois_niveis_por_foco.py`
- `demo/teste_demo_h0072_formatacao_generica.py`
- `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P01.md` (este)

## 3. Loader

`_validar_designador_filho` passou a admitir exclusivamente `tipo`,
`prefixo` e `sufixo`. `tipo` permanece obrigatório e restrito a
`decimal_composto`, `alfabetico_maiusculo` e `nenhum`. Ausência de
`prefixo`/`sufixo` continua válida (retrocompatibilidade). Exceção
canônica: `TelaEstruturaInvalida`. Sem fallback silencioso.

V-DNF-01..11 preservadas. Delta P01:

| Código | Condição |
|---|---|
| V-DNF-12 | `prefixo` presente e não string |
| V-DNF-13 | `sufixo` presente e não string |
| V-DNF-14 | chave desconhecida em `designador` |
| V-DNF-15 | `tipo: nenhum` com `prefixo` |
| V-DNF-16 | `tipo: nenhum` com `sufixo` |

Renderer não alterado. Composição `prefixo + nucleo + sufixo` permanece em
`tela/renderizacao/designadores.py::_texto_designador`.

## 4. Fixture genérica

Somente `console_h0072_tabela`:

```yaml
designador:
  tipo: alfabetico_maiusculo
  prefixo: "("
  sufixo: ")"
```

Preservados: `console_h0072_texto` (`decimal_composto` sem adornos),
`console_h0072_sem_designador` (`nenhum` sem adornos), demais dados e
semântica. Conteúdo externo não alterado.

## 5. Prefixo/sufixo e caso `A)`

Comprovado por teste sobre o renderer vigente, sem duplicar composição:

- alfabetico sem adornos → `A` (nunca `A)` por default);
- alfabetico + `sufixo: ")"` → `A)` / `B)` — capacidade equivalente a
  H-0055; o `)` vem da configuração estrutural do teste, não de
  `h0055_*` (intocados) nem do documento externo;
- prefixo isolado → `(A`;
- prefixo+sufixo → `(A)` / `(B)`;
- decimal sem adornos → `1.1`;
- decimal com `[` / `]` → `[1.1]` (base inalterada);
- `nenhum` sem adornos não produz designador.

## 6. Testes focais

```
PYTHONDONTWRITEBYTECODE=1 python -m pytes\
  tela/teste_formato_filho_dois_niveis_por_foco.py\
  demo/teste_demo_h0072_formatacao_generica.py\
  tela/teste_navegacao.py\
  tela/teste_loader.py\
  demo/teste_demo_console.py -q
```

Resultado: **232 passed**.

Regressão original dos 18 critérios de H-0072 mantida. §21.1 materializado
no teste dedicado (V-DNF-12..16, adornos, `A)`, navegação/seleção,
texto/tabela).

## 7. Demonstração

Fluxo real `catálogo → loader → modelo → runtime/comando → renderer →
saída física` (`demo/teste_demo_h0072_formatacao_generica.py` via
`demo/demo.py`). Console tabular comprova `(A)` e `(B)`. Não é teste
isolado do helper de designador.

## 8. Suíte canônica

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q
```

Resultado: **1431 passed, 1 failed**.

Falha residual:

`tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`

`assert linhas[corrente].index("→") >= 4` (obtido 2). Mesma falha já
registrada na implementação original de H-0072; o teste exercita
`_linhas_apresentacao_hierarquia_com_mapa` / estilo H-0070, fora do
loader de designador deste P01. Não causal. Não corrigida.

Nenhuma falha causal ao P01.

## 9. Desvios / bloqueios

Desvios: nenhum.
Bloqueios: nenhum.
Autorização de escopo: não necessária.
Stage/commit: não feitos.
\n