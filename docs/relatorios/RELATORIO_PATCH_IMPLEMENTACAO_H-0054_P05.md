# Relatório de patch de implementação — H-0054 P05

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0054_P04.md

origem:
  handoff: H-0054 P04
  decisao: D-MULTI-07-P04
```

## Resultado

P05 implementa a coerência estrutural de selecionabilidade. O suporte
transitório a pai não selecionável com descendente selecionável foi removido:
`no_tem_alcance_selecao()` só considera o nó corrente selecionável, e
`_alvos_multinivel()` não atravessa mais um nó corrente não selecionável para
produzir alvos. Não foi criado mecanismo de rejeição, exceção, schema,
normalização ou mensagem nova.

Os quatro testes transitórios de P04 foram removidos: acionamento de pai não
selecionável com descendentes, segundo Espaço nesse pai, travessia profunda de
pais não selecionáveis e promoção/não promoção de ancestral nesse cenário.

## Configuração válida e preservações

A fixture H-0054 já estava materialmente coerente e não exigiu alteração:
todo nó com seleção abaixo e todos os seus ancestrais são selecionáveis, e
nenhum item não selecionável possui descendente selecionável. A nova cobertura
confirma `tg` em raízes, pais intermediários e folhas selecionáveis, sem `tg`
no item negativo.

No ramo `2.`, Espaço seleciona `2.` e todos os descendentes selecionáveis,
mantém o item não selecionável fora do conjunto e deixa a unanimidade de `2.`
considerar somente os filhos selecionáveis. A cobertura adicional também
confirma seleção ascendente completa no ramo `1.`, desseleção ascendente e
preservação do ramo irmão.

D-MULTI-06-P03 permanece íntegra: conjunto de IDs estáveis, estado binário,
propagação descendente, reconciliação ascendente, desseleção ascendente,
profundidade arbitrária, ausência de estado parcial e topologia única.

Paginação H-0054, múltiplos itens por página, PageUp/PageDown, `[✥] Navegar`,
cursor independente, `[Esc] Limpar`, `[?] Ajuda` por último e Enter sem nova
semântica foram preservados. A regressão integrada H-0053 permanece sem
seleção e sem `tg`, com foco, cursor, navegação, Expandir/Recolher e Espaço
preservados.

## Verificações

- Focais: `87 passed`.
- Suíte completa: `1090 passed`.
- `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0054_selecao_multinivel`: código 0.
- `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0053_arvore_colapsavel`: código 0.

## Arquivos e bloqueios

Alterados neste patch: `tela/navegacao.py`, `tela/selecao.py`,
`tela/teste_navegacao.py`, `demo/teste_demo_console.py` e este relatório.
As fixtures H-0054 foram conferidas; fixtures H-0053 não foram alteradas.

Bloqueios: nenhum.
