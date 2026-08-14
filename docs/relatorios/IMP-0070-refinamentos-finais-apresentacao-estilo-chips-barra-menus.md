# IMP-0070 — Refinamentos finais de apresentação, chips e Barra de Menus

## Arquivos alterados/criados

- `tela/estilo.py`
- `tela/renderizacao/estilo.py`
- `tela/renderizacao/conteudo_externo.py`
- `tela/renderizacao/barra_menus.py`
- `tela/teste_estilo_h0070.py`
- `demo/teste_demo_estilo_h0070.py`
- `demo/teste_demo_paginacao.py`
- `tela/testes_renderizador/barra_menus.py`
- `tela/teste_estilo_h0064.py`
- este relatório.

## Comportamento entregue

Os filhos da tela Estilo deixaram de renderizar ordinais alfabéticos. A
indentação, os indicadores vigente/não vigente e a largura do prefixo foram
preservados; o cursor passou a ocupar a região visual liberada pelo ordinal,
com a mesma coluna de texto para foco e não foco.

As amostras agora são compostas após o maior nome visual de cada categoria.
O padding usa `_ljust_sem_ansi` e a largura usa `_largura_sem_ansi`, portanto
ANSI não interfere na coluna, inclusive nas amostras coloridas de chip.

`tela/teste_estilo_h0064.py` recebeu somente a atualização da expectativa
geométrica diretamente afetada:

```text
natureza: expectativa_predecessora_superada_por_H0070
motivo: alinhamento_em_coluna_comum_das_amostras
comportamento_preservado: semantica_visual_H0064
```

## Chips e Barra real

O agrupamento exclusivo de `chip_pagina_anterior`/`chip_pagina_proxima` agora
discrimina a família pelos campos resolvidos do estilo. Presets delimitados
continuam produzindo `[PgUp][PgDn]` sem `/`. Ponto produz uma unidade
` PgUp/PgDn.`; Destaque Texto produz uma unidade ` PgUp/PgDn ` com cor no
conteúdo; Destaque Fundo produz a mesma unidade com fundo cobrindo os dois
espaços laterais. O texto da ação permanece fora do chip.

O caminho real da Barra usa o preset recebido em runtime, aplica as cores
quando a unidade é multitecla e mantém chamadas de uma tecla no comportamento
vigente. A geometria continua usando a única largura visual canônica, sem
ANSI contado, com recomposição após troca de estilo e resize.

## Testes focais e regressões

- `tela/teste_estilo_h0064.py`: 12 passed.
- `tela/teste_estilo_h0070.py` e `demo/teste_demo_estilo_h0070.py`: 7 passed.
- regressão genérica de hierarquia/conteúdo H-0036/H-0055:
  `tela/testes_renderizador/conteudo_externo.py`: 17 passed.
- `tela/testes_renderizador/conteudo_externo.py` e
  `demo/teste_demo_estilo_h0069.py`: 24 passed no conjunto executado.
- bateria combinada de H-0063–H-0069, popup, Barra, integração e paginação:
  416 passed; falhas restantes foram classificadas abaixo.
- suíte completa: **1.261 passed, 74 failed, 17 errors**.

## Demonstração

`demo/teste_demo_estilo_h0070.py` passou integralmente e exercitou a Barra
real com Ponto, Destaque Texto e Destaque Fundo, ação multitecla, ação de uma
tecla, troca de estilo em runtime, resize, ANSI e largura visual. O fluxo
integrado H-0069 permaneceu coberto pelos testes existentes.

## Falhas externas remanescentes e bloqueios

As falhas remanescentes estão concentradas em expectativas anteriores que
exigem chips de uma tecla ou ações genéricas com delimitadores `[...]`, embora
`config/estilo.json` vigente use `Ponto`; popup, H-0041/H-0043/H-0050,
H-0053–H-0058 e vários testes de demo derivam dessa expectativa. Também há
asserções de `[Esc]`, `[✥]` e chips de seleção no mesmo formato antigo. Essas
falhas não foram alteradas por não serem comportamento novo de H-0070 nem
arquivos autorizados para expansão adicional.

Não há bloqueio de implementação. A validação manual TTY permanece pendente
e obrigatória (`validacao_manual_final_ITEM0010: OBRIGATORIA`).
