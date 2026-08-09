# Relatório de patch de implementação — H-0054 P02

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0054_P01.md

achados_tratados:
  - MV-H0054-004
  - MV-H0054-005
```

## MV-H0054-004 — `tg` em raízes selecionáveis

A causa foi a fixture demonstrativa: `h0054_raiz` e `h0054_raiz_2` estavam
declaradas com `selecionavel: false`. A projeção/renderização já derivava a
presença de `tg` da selecionabilidade do nó, independentemente da profundidade.

As duas raízes foram marcadas como selecionáveis em
`h0054_selecao_multinivel_conteudo.json`. O item
`h0054_nao_selecionavel` foi preservado como fronteira explícita e continua
sem `tg`. Foram acrescentadas asserções integradas para raiz, pai
selecionável, folha selecionável e item não selecionável.

## MV-H0054-005 — regressão de H-0053

A causa foi o boundary de inicialização no ponto de entrada: `_estabelecer_foco_paginacao_inicial`
só materializava foco para consoles com paginação. Na abertura direta de
`h0053_arvore_colapsavel`, a lista de foco existia, mas o estado começava com
`foco_console=None` e sem cursor; o renderer e os chips respeitavam esse estado
e, portanto, não exibiam cursor, `[✥] Navegar` ou o chip contextual de árvore.

O boundary passou a inicializar também `arvore_colapsavel`, com cursor no
primeiro nó. A árvore não recebe estado de página. O dispatch compartilhado
de setas, Espaço, `ramos_fechados`, cursor e chips foi preservado; não foi
criada implementação paralela para H-0053.

Foi adicionado teste integrado pelo `demo.py` real, cobrindo foco, cursor,
`[✥] Navegar`, setas, fechamento/reabertura, alternância de Expandir/Recolher,
ausência de seleção e Espaço sem efeito em folha. O caminho também foi
reexecutado pela demonstração automatizada.

## Arquivos alterados neste P02

- `demo/demo.py`
- `demo/teste_demo_console.py`
- `config/telas/demo/h0054_selecao_multinivel_conteudo.json`
- este relatório

Os demais módulos autorizados já alterados no estado transportado de P01 não
foram ampliados neste patch. As fixtures H-0053 permaneceram inalteradas.

## Verificações

- Testes focais: `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_console.py -q` — **79 passed**.
- Suíte completa: `PYTHONDONTWRITEBYTECODE=1 python -m pytest` — **1082 passed**.
- Demonstração H-0054: renderizou múltiplos itens, `[✥] Navegar`, `tg` nas raízes selecionáveis, paginação, Paginação antes de Selecionar e Ajuda por último.
- Demonstração H-0053: renderizou cursor e `[✥] Navegar`; o teste integrado confirmou navegação, Expandir/Recolher, retorno dos filhos, folha sem ação, ausência de seleção e ausência de `tg`.

A ordenação global da barra de menus não foi alterada. O posicionamento
declarativo observado para `[✥]` permanece deferido ao ciclo futuro; foram
preservadas apenas as regras vigentes de Paginação antes de Selecionar e Ajuda
por último. Não foi realizada nova validação manual em TTY nem QA pós-patch.

Bloqueios ou desvios: nenhum.
