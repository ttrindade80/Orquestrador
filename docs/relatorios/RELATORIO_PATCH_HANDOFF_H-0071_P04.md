# Relatório PATCH_HANDOFF — H-0071 P04

## Correções incorporadas

O H-0071 foi reconciliado com a ADR-0046 pós-P02. `Destaque Texto` agora
exige somente foreground no conteúdo, fundo normal em toda a unidade e um
espaço normal em cada lado. A composição multitecla tornou-se uniforme para
amostra de Estilo e Barra real: uma unidade única, teclas separadas por `/`
e delimitadores apenas nas extremidades. A forma renderizada de Páginas é
`[PgUp/PgDn] Páginas`.

Também foram fechados os critérios de preservação de ativo/inativo e a
estrutura física `ec → tg → tx`, mantendo cursor, toggle e texto em colunas
distintas e estáveis.

## Arquivos de implementação autorizados

Produção:

- `tela/renderizacao/barra_menus.py`;
- `tela/renderizacao/estilo.py`;
- `tela/renderizacao/conteudo_externo.py`.

Foram removidos da autorização P04 o carregador de estilo e a configuração
concreta, pois a correção não materializa campos adicionais. Nenhum diretório
inteiro foi autorizado.

## Critérios adicionados

Foram adicionados critérios observáveis para foreground sem alteração de
fundo, espaços laterais, unidade `[PgUp/PgDn]`, ausência da concatenação
antiga, `cor_inativo` em Aplicar e Páginas, estados funcionais diferentes de
PgUp/PgDn, colunas `ec/tg/tx`, estabilidade das colunas com e sem cursor,
Ponto, Destaque Fundo e paridade entre amostra e Barra real. Os testes devem
verificar saída final, sem reconstruir a implementação internamente.

## Semântica antiga e MF-ITEM0010-003

Foi removida a exigência de fundo lateral/assimétrico em `Destaque Texto` e a
concatenação renderizável `[PgUp][PgDn]`. `MF-ITEM0010-003` deixou de estar
fora de escopo e passou a ser achado a resolver neste handoff.

## Bloqueios

Nenhum bloqueio documental. Não houve implementação, alteração de testes,
QA ou commit nesta etapa.
