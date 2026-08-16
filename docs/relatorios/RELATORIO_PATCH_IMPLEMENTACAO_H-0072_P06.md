# RELATÓRIO — PATCH_IMPLEMENTACAO H-0072 P06

```yaml
etapa: PATCH_IMPLEMENTACAO
objeto: H-0072
patch: P06
achado_origem: VM-H0073-001
predecessor_imediato:
  docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P05.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: IMPLEMENTATION_PATCHED
```

## Por que P05 com maximo 3 não bastou

A tabulação genérica não foi alterada. Em H-0055 o texto curto ainda cabe com
tabulação 10 em W=80/48/40. A barra tem 5 unidades visuais (PgUp/PgDn
agrupados). Com `coluna_a_coluna`, `linhas.maximo: 3` produz 2 colunas e o
piso permanece W=39 (`erro_layout`). A compactação textual 10→9→5 exige
content_w ≈ 28→27→23, isto é W≈37..32, abaixo desse piso. Copiar `maximo: 3`
de H-0063 não alcança essa faixa.

## Medição empírica

Fluxo real (`demo/demo.py` / `renderizar_estado`), nível filho, `linhas.maximo`
crescente a partir de 3. Nenhuma fórmula de tabulação foi tocada.

| maximo | largura mínima | tab 10 | intermediária | tab 5 |
|--------|----------------|--------|---------------|-------|
| 3 | 40 (erro em 39) | sim | não | não |
| 4 | 35 (erro em 34) | até 37 | 36→9, 35→8 | não |
| 5 | 24 (erro em 23) | até 37 | 36..33 → 9..6 | 32..24 |

`maximo` 6 e 7 não baixam o piso além de 24 nem mudam 10/inter/5. Com 5
unidades visuais, só 5 linhas permitem 1 coluna. Primeiro valor suficiente:
**5**. W=32 é a última largura com `Filho 01.01` integral; W=31 já elide o
rótulo. Por isso L3=32, não um valor abaixo.

## Configuração alterada

Somente `config/telas/demo/h0055_dois_niveis_por_foco.json`, campo
`barra_de_menus.distribuicao.linhas.maximo`: 3 → 5. Nenhuma outra
propriedade do JSON mudou.

## Sequência real

Continuidade sem recriar a tela: entrar no nível filho → render L1 →
`navegacao.redimensionar` → render L2 → resize → render L3.

Larguras: 80 → 36 → 32. Tabulações: 10 → 9 → 5.

Em L1/L2/L3: `A)` permanece; `)` vem do sufixo estrutural; conteúdo externo
byte-a-byte; mesmo pai ativo, mesmo filho lógico, foco, cursor, seleção e
identidade; apresentação texto.

## Barra em largura normal

`linhas.maximo` é teto. Em W=90 e W=80 a barra permanece 1 linha de conteúdo,
idêntica com maximo 3 ou 5. Só compacta em faixas estreitas (4 linhas em
W=36; 5 em W=32).

## Preservações

H-0063 JSON, espaçamento 3..8, tabulação dinâmica aprovada e correção ANSI
P05 não foram editados. Não se alterou `_cabe_tabulacao`,
`_escolher_maior_que_cabe`, minimo 5, maximo 10, cálculo textual, designador,
`sufixo: ")"`, conteúdo H-0055, navegação nem seleção.
`tela/renderizacao/matriz_participantes.py`, `texto_ansi.py` e
`conteudo_externo.py` permaneceram intactos. VM-H0073-002:
PRESERVADO_COMO_CORRIGIDO.

## Testes

Focal H-0055: **7 passed**. Suíte focal P06 (H-0055, H-0063, estilo H-0073,
formato filho, navegação, console): **168 passed**. H-0070 isolado:
**1 failed**, `index("→") == 2`, esperado `>= 4`;
`FALHA_HISTORICA_NAO_CAUSAL`; teste intocado. Suíte canônica:
**1460 passed, 1 failed**, somente H-0070. Sem stage.

## Bloqueios

Nenhum. A faixa 10→intermediário→5 é alcançável pelo quadro completo.

## Validação manual

NECESSARIA. P05+P06 devem ser auditados conjuntamente no QA posterior, antes
da revalidação TTY. Próxima ação: QA_POS_PATCH.
\n