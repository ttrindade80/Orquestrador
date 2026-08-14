# Relatório do patch documental do ITEM-0031

## Baseline Git observada

- Branch: `master`.
- HEAD: `77bd8bf3772985325bc51a850f7c6d76d61ad573`.
- Stage: vazio.

## Não conformidade recebida do QA

O ITEM-0031 não materializava o mapa global de teclas nem as restrições de F2, F3 e F5 exigidas pelo critério de aprovação.

## Alteração realizada no ITEM-0031

A descrição passou a registrar F1 = Ajuda, F4 = Estilo e F11 = Tela Cheia, mantendo explícita a subordinação da implementação e da definição comportamental de F11 ao ITEM-0030. Também registra F2, F3 e F5 como teclas sem função concreta neste momento, condiciona qualquer reserva futura a necessidade real e à consideração de convenções conhecidas, e impede sua ocupação apenas por estarem disponíveis. Foi acrescentada relação compacta com o ITEM-0029 e o ITEM-0030.

## Preservação dos demais itens

O patch alterou exclusivamente o bloco do ITEM-0031 em `docs/backlog.md`; os demais itens, nomenclatura, ordenação e escopo documental foram preservados.

## Validação

- `git diff --check`: passou.

## Arquivos efetivamente tocados

- `docs/backlog.md`
- `docs/relatorios/RELATORIO_PATCH_BACKLOG_ITEM-0031_P01.md`
