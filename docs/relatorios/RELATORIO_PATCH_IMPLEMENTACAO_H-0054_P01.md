# Relatório do patch de implementação H-0054 P01

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0054.md

achados_tratados:
  - MV-H0054-001
  - MV-H0054-003
```

## Causa e correção

`MV-H0054-001` foi causado pelo mapa físico específico de
`selecao_multinivel` em `tela/renderizacao/console.py`. Cada nó hierárquico
era entregue ao paginador com `politica_quebra: evitar_quebra`. A política
fazia cada nó caber como unidade indivisível, embora todos ocupassem uma única
linha física, produzindo uma página por item.

O mapa agora entrega a política universal
`permitir_quebra_somente_se_maior_que_pagina`. Assim, as linhas hierárquicas
são agrupadas enquanto houver altura disponível; somente um item maior que a
página pode ser fragmentado. A política global de paginação não foi alterada.

`MV-H0054-003` foi resolvido causalmente pela correção da paginação. Com vários
itens na página, `[✥] Navegar` aparece; numa página com um único item, ele não
é forçado. Não houve alteração da semântica transversal do chip.

A fixture de conteúdo foi ampliada para 25 nós, mantendo profundidade
multinível e duas páginas na geometria nominal. A barra estrutural foi ordenada
como `Paginação → Selecionar`, preservando `[PgUp][PgDn] Páginas` e `[?] Ajuda`
como último chip.

## Arquivos alterados

- `tela/renderizacao/console.py`
- `demo/teste_demo_console.py`
- `config/telas/demo/h0054_selecao_multinivel.json`
- `config/telas/demo/h0054_selecao_multinivel_conteudo.json`
- este relatório

## Verificações

- Testes focais: `78 passed` com
  `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_console.py -q`.
- Suíte completa: `1081 passed` com
  `PYTHONDONTWRITEBYTECODE=1 python -m pytest`.
- Demonstração: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0054_selecao_multinivel` exibiu vários itens na página 1/2, `[✥] Navegar`, `[PgUp][PgDn] Páginas` antes de `[␣] Selecionar` e `[?] Ajuda` por último.
- Os testes cobrem agrupamento na mesma página, paginação sem unidade artificial por item, percurso multinível, presença condicional de `[✥]`, PageUp/PageDown, preservação da seleção entre páginas, ordem da barra e regressão H-0053.

Não foram executadas QA pós-patch nem nova validação manual TTY, conforme o
escopo transportado. Não há bloqueios ou desvios de implementação. Nenhum
stage, commit ou push foi realizado.
