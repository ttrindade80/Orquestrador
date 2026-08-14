# RELATORIO_PATCH_IMPLEMENTACAO H-0071 P05

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
etapa: PATCH_IMPLEMENTACAO
patch: P05
data: 2026-08-14
status: IMPLEMENTATION_PATCHED
cadeia:
  raiz: docs/handoff/H-0071-correcao-chips-multitecla-barra-menus-estilo.md
  predecessor_documental: PATCH_HANDOFF P06 / QA_HANDOFF H1_HANDOFF_APPROVED
  nao_sobrescrito: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P04.md
arquivos_alterados:
  - config/estilo.json
  - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
  - config/telas/demo/h0054_selecao_multinivel.json
  - config/telas/demo/h0055_dois_niveis_por_foco.json
  - tela/teste_estilo_h0071.py
  - demo/teste_demo_estilo_h0063.py
  - demo/teste_demo_console.py
  - demo/teste_demo_estilo_h0064.py
  - demo/teste_demo_estilo_h0067.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P05.md
```

## 1. Escopo executado

Somente o delta de entrada/configuração e as regressões autorizadas.
Nenhum renderer, compositor, schema, ADR, contrato ou nomenclatura foi
alterado. Validação visual TTY permanece exclusiva do usuário.

A primeira parte do P05 materializou Curva × Ornamental, a reconciliação
declarativa de paginação e as regressões H-0071 / H-0063 / console.
Após autorização explícita do usuário, a mesma execução P05 foi
ampliada exclusivamente para as regressões causais H-0064 e H-0067.
Não houve P06 nem relatório novo.

## 2. Curva × Ornamental (ACH-H0071-P05-01)

O WIP materializava Ornamental com os delimitadores de Curva. Restaurado
em `config/estilo.json`:

- Curva: `╭` / `╮`
- Ornamental: `❲` / `❳`

Os dois presets permanecem distintos. Contra HEAD os delimitadores já
coincidem; o patch reverteu o WIP que os igualava.

## 3. Reconciliação H-0063 / H-0054 / H-0055 (ACH-H0071-P05-02)

Substituída a unidade legada `tecla: "PgUp][PgDn"` +
`regra_ativo: "quando_paginacao"` pelo par já consumido pelo agrupamento
vigente:

- `chip_pagina_anterior` (`PgUp`, `pagina_nao_e_primeira`)
- `chip_pagina_proxima` (`PgDn`, `pagina_nao_e_ultima`)
- `regra_existencia: console_com_paginacao`

Sem schema novo e sem semântica nova de paginação. H-0054 e H-0055
receberam só essa reconciliação; o restante da declaração foi preservado.

## 4. Estado de Páginas em 1/1

Com o par canônico, o avaliador vigente calcula PgUp/PgDn inativos quando
`total_paginas = 1` e transporta `cor_inativo` até o compositor. Nenhuma
pintura manual, ANSI forçado ou ramo especial no renderer.

## 5. Regressões

- `tela/teste_estilo_h0071.py`: expectativa canônica independente da
  configuração auditada; falha se Curva e Ornamental tiverem os mesmos
  delimitadores.
- `demo/teste_demo_estilo_h0063.py`: caminho real de
  carregamento/renderização da configuração H-0063 (não barra fabricada).
  Verifica ausência de `[PgUp][PgDn]`, presença de `[PgUp/PgDn] Páginas`,
  inatividade em `página 1/1` e unidade com `cor_inativo`.
- `demo/teste_demo_console.py`: expectativas H-0054/H-0055 passam a exigir
  `[PgUp/PgDn]`; `[PgUp][PgDn]` deixa de ser forma física válida.
- `demo/teste_demo_estilo_h0064.py` (FALHA-EXC-P05-01, causal, corrigida
  na continuação autorizada): deixa de exigir o id legado `chip_paginas`;
  passa a exigir o par canônico `chip_pagina_anterior` /
  `chip_pagina_proxima`, a ação Páginas na Barra e as amostras sob
  paginação forçada. Sem compatibilidade artificial com `chip_paginas`.
- `demo/teste_demo_estilo_h0067.py` (FALHA-EXC-P05-02, causal, corrigida
  na continuação autorizada): duas asserções de geometria de popup
  deixam de tratar `len(linha)` como largura visual. Reutilizam
  `_largura_sem_ansi`; SGR legítimo de `cor_inativo` não infla a
  geometria.

## 6. Testes executados

Primeira parte do P05:

| Suíte | Resultado |
|---|---|
| focais P05 (`teste_estilo_h0071`, `teste_demo_estilo_h0063`, `teste_demo_console`) | 70 passed |
| regressões do handoff (barra_menus, h0071, paginacao, popup, renderizador, demo, h0069, h0070) | 751 passed |
| suíte canônica `pytest` | 1378 passed, 4 failed |

Continuação autorizada (H-0064 e H-0067):

| Suíte | Resultado |
|---|---|
| focais da continuação (`teste_demo_estilo_h0064`, `teste_demo_estilo_h0067`) | 27 passed |
| regressões P05 (h0071, h0063, console, h0064, h0067) | 97 passed |
| regressões do handoff (mesmo conjunto) | 751 passed |
| suíte canônica `pytest` (resultado FINAL) | 1381 passed, 1 failed |

Falhas da suíte canônica da primeira parte, e destino na continuação:

1. `demo/teste_demo_estilo_h0064.py::test_paginacao_com_amostras_preserva_chip_paginas`
   — causal do P05 (id legado `chip_paginas`). Resolvida na continuação.
2. `demo/teste_demo_estilo_h0067.py` (2 testes de popup) — causal do P05
   (`len` vs largura visual com SGR de `cor_inativo`). Resolvidas na
   continuação.
3. `tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
   — recuo de `→` em filho de borda; sem relação causal com Curva ×
   Ornamental, reconciliação de paginação, `cor_inativo` ou os arquivos
   desta execução. Não alterada. Resíduo não causal persistente no
   resultado FINAL.

Nenhuma falha causal nova apareceu fora do escopo autorizado.

## 7. Verificação do ponto real

Caminho `_abrir()` / `_quadro()` da demonstração H-0063, configuração
`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`:

- ação Páginas composta (`chip_pagina_anterior` + `chip_pagina_proxima`);
- `[PgUp][PgDn]` ausente; `[PgUp/PgDn] Páginas` presente;
- em 100×40: `página 1/1`, ambos inativos, unidade com `cor_inativo`;
- Curva `╭`/`╮` distinta de Ornamental `❲`/`❳`.

Isso não substitui validação visual humana.

## 8. Desvios / exceções / bloqueios

Exceção operacional: uma, posteriormente autorizada pelo usuário.
A primeira parte do P05 registrou H-0064 e H-0067 desalinhados e fora
do escopo nominal, sem editá-los. O usuário autorizou ampliar a mesma
execução P05 exclusivamente a:

- `demo/teste_demo_estilo_h0064.py`
- `demo/teste_demo_estilo_h0067.py`

Nenhum renderer, compositor, carregamento ou produto adicional foi
alterado nesta continuação. Permanecem preservados, entre outros:

- `tela/renderizacao/barra_menus.py`
- `tela/renderizacao/estilo.py`
- `tela/carregamento/estilo.py`
- `tela/renderizacao/conteudo_externo.py`
- `tela/testes_renderizador/fundamentos.py`
- `tela/teste_estilo_h0070.py`

Bloqueios: nenhum. `MANUAL_VALIDATION_APPROVED` não declarado.
Validação TTY continua pendente e exclusiva do usuário.

`git diff --check` no escopo da continuação: limpo.
Delta P05 implementado. Resíduo não causal: somente H-0070.
