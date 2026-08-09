cadeia:
  raiz: docs/relatorios/IMP-0054-selecao-multinivel.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0054_P02.md

origem:
  handoff: H-0054 P03
  decisao: D-MULTI-06-P03

# Relatório de patch de implementação — H-0054 P03

## Lacuna e solução

A implementação anterior propagava o Espaço somente para descendentes. Pais
selecionáveis, portanto, não eram materializados no conjunto de IDs quando
seus filhos eram marcados manualmente; a desseleção também não subia pelos
ancestrais. A causa era a ausência de reconciliação parental após o toggle.

Foi implementada uma rotina única em `tela/selecao.py`. O Espaço opera sobre o
item selecionável corrente e seus descendentes selecionáveis. Em seguida, a
rotina percorre a topologia em pós-ordem e, para cada pai selecionável com
filhos selecionáveis imediatos, aplica:

```text
pai ∈ seleção ⇔ todos os filhos selecionáveis imediatos ∈ seleção
```

O conjunto de IDs continua sendo a única fonte de verdade. Pais, pais
intermediários e folhas usam somente presença/ausência no conjunto; não há
estado parcial, estado derivado paralelo, contador ou terceiro símbolo. Nós
não selecionáveis são ignorados na unanimidade e permanecem fora do conjunto.

## Materialização e arquivos

Alterados no patch:

- `tela/selecao.py`: toggle recursivo e reconciliação binária ascendente;
- `tela/navegacao.py`: acionabilidade de Espaço somente para item selecionável;
- `tela/teste_navegacao.py`: casos A–F, profundidade arbitrária e regressões;
- `demo/teste_demo_console.py`: fixture, seleção, paginação e renderização;
- `config/telas/demo/h0054_selecao_multinivel_conteudo.json`: três pais de
  nível 1, primeiro ramo com dois pais de nível 2 e quatro folhas, item não
  selecionável e terceiro ramo volumoso para paginação.

Nenhuma fixture H-0053 foi alterada. A ordem global da barra não foi alterada.

## Verificação

- Testes focais: `84 passed`.
- Suíte completa: `1087 passed`.
- Demonstração H-0054: código 0.
- Regressão H-0053: código 0.

Os testes cobrem seleção direta de pai, construção manual de pai
intermediário e raiz, desseleção ascendente com irmão preservado, item não
selecionável sem `tg`, percurso de profundidade superior a três níveis,
paginação, seleção entre páginas, cursor independente, chips e o caminho real
de H-0053.

## Bloqueios

Nenhum. QA pós-patch, validação manual, atualização de backlog, stage, commit e
push permanecem fora desta etapa.
