---
name: REL-PATCH-H0045-P23-barra-cinco-linhas-e-estado-controlado
description: "Delta factual do patch que autoriza de uma a cinco linhas na barra de menus da tela h0045_fluxo_execucao_paginado e introduz o estado controlado de terminal insuficiente, eliminando o traceback de RenderizadorErro (erro_layout) que escapava por uma consulta de geometria durante o resize (VM-H0045-R08-001)"
metadata:
  type: relatorio_patch
  tipo_execucao: PATCH_IMPLEMENTACAO
  status_literal: IMPLEMENTATION_PATCHED
  data: "2026-08-02"
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0045
  cadeia_raiz: VM-H0045-R08-001
  achados_tratados:
    - VM-H0045-R08-001
---

# REL-PATCH-H0045-P23 — Barra de cinco linhas e estado controlado de terminal insuficiente

## 1. Identificação e status

```yaml
tipo_execucao: PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTATION_PATCHED
```

## 2. Causa tratada

`VM-H0045-R08-001`: ao reduzir o terminal em `python demo/demo.py
h0045_fluxo_execucao_paginado`, a barra de cinco chips deixava de caber no
máximo efetivo de duas linhas (alias `"horizontal"` → default global
`linhas.maximo=2`). O `RenderizadorErro` (`erro_layout`) escapava por uma
consulta de geometria durante o resize — `_reconciliar_paginacao_apos_resize`
chama `geometria_console` → `_linhas_barra`, que lança `erro_layout` FORA do
bloco `try/except RenderizadorErro` de `_geometria_por_console` — e encerrava
a demonstração com traceback. O mesmo escape ocorria nos comandos de
página/seta via `_com_geometria_real_do_console`.

## 3. Configuração materializada

`config/telas/demo/h0045_fluxo_execucao_paginado.json`: o alias simples
`"distribuicao": "horizontal"` foi substituído pelo objeto canônico já
suportado pelo loader/renderer, com `linhas.minimo=1`, `linhas.maximo=5`,
`preferir_menor_numero=true`, preservando coluna_a_coluna, margem horizontal
mínima 1, vãos internos/entre chips, `overflow.quando_nao_couber: erro_layout`
e as proibições de omissão/truncamento/reordenação. Nenhum campo novo foi
criado; o default global de duas linhas não foi alterado.

## 4. Arquivos alterados

```yaml
produtivos:
  - config/telas/demo/h0045_fluxo_execucao_paginado.json
  - demo/demo.py
testes:
  - tela/teste_renderizador.py
  - demo/teste_demo_paginacao.py
  - demo/teste_demo_navegacao.py
```

## 5. Renderer

`tela/renderizador.py` **NÃO foi alterado** por este patch. O objeto canônico
de distribuição com `linhas.maximo=5` já era suportado (`_linhas_barra` percorre
`range(inicio_multilinha, maximo+1)`; `_validar_distribuicao` aceita qualquer
`maximo >= minimo`). A alteração do renderer não era indispensável.

## 6. Classificação seletiva do erro

Novo helper `_e_insuficiencia_geometrica` classifica `RenderizadorErro` por
prefixo estável da mensagem: `erro_layout` (barra que não cabe na
largura/linhas), `altura insuficiente` (terminal baixo demais) e `DA-0*`
(area externa descoberta). Somente insuficiência geométrica autoriza o estado
controlado. Erros estruturais (modelo/configuração/campo/invariante) usam
outros prefixos e propagam normalmente nos caminhos de consulta de geometria.

## 7. Quadro controlado

`_quadro_terminal_insuficiente` exibe semanticamente "Terminal pequeno
demais" / "Aumente a janela para continuar", adequados à geometria
disponível (mensagem quebrada/truncada em dimensões extremas, sem nova
exceção). Aplicado especificamente ao `erro_layout` da barra. Demais
insuficiências geométricas e erros defensivos do render permanecem no quadro
mínimo canônico ("terminal pequeno demais"), preservando o comportamento
coberto por testes de H-0023/H-0044.

## 8. Preservação e recuperação

`_reconciliar_paginacao_apos_resize` e `_com_geometria_real_do_console`
passaram a capturar seletivamente `erro_layout` (e apenas insuficiência
geométrica), preservando seleção, foco, cursor, item lógico, página, pilha,
modo verboso e estado de execução. Os comandos dependentes de geometria
(página/setas/Tab) tornam-se no-op sob geometria inválida. A recuperação é
automática ao ampliar: geometria reconsultada, repaginação, localização do
item lógico corrente e restauração da tela normal.

## 9. Resultados da matriz

Matriz 10 larguras (16,17,20,28,29,40,41,64,65,120) × 6 alturas
(6,8,10,15,24,40) = 60 células exercitadas, **0 exceções não tratadas**.
Transições materiais confirmadas (resultado real derivado da configuração):

- 65 colunas → 1 linha (todas as alturas);
- 41 colunas → 2 linhas;
- 29 colunas → 3 linhas;
- 28 colunas → 4 linhas;
- 17 colunas → até 5 linhas (quando a altura permite);
- 16 colunas → `erro_layout` → quadro controlado;
- altura insuficiente (h=6/8 em larguras estreitas) → quadro controlado/mínimo.

## 10. Testes focais

30 novos testes (seleção `-k "P23 or p23"`): casos 1-9 (barra 1-5 linhas,
menor qtd válida, erro_layout abaixo do limite), 10-13 (ausência de traceback
no resize e em comandos; quadro controlado), 14-19 (preservação de
seleção/foco/cursor/item/pagina/pilha), 20-22 (recuperação automática sem
perda/repetição), 23-24 (ausência de truncamento/reordenação), 25
(rotulo_dinamico_esc), 26-27 (primeiro Esc limpa; segundo sai), 28 (regressão
demais telas H-0045), 29 (regressão telas com máximo de duas linhas), 30
(matriz obrigatória).

## 11. Suíte completa

```yaml
focal: "475 passed (tela/teste_renderizador.py, demo/teste_demo_paginacao.py, demo/teste_demo_navegacao.py)"
completa: "927 passed"
antes: "897 passed"
delta: "+30 casos P23"
```

## 12. git diff --check

```yaml
saida: limpa
exit_code: 0
```

## 13. Bloqueios

Nenhum. Todos os caminhos necessários estavam entre os autorizados; nenhum
arquivo fora do escopo foi alterado.
