---
name: relatorio-patch-aplicacao-adr-0048-p01
description: Patch documental P01 da aplicação da ADR-0048, corrigindo QA-APP-0048-001 a 003 e propagando D-0026-12
metadata:
  type: relatorio
  scope: orquestrador
---

# Relatório — Patch da aplicação documental da ADR-0048 (P01)

```yaml
cadeia:
  raiz: RELATORIO_APLICACAO_ADR-0048.md
  predecessor_imediato: RELATORIO_QA_APLICACAO_ADR-0048.md

achados_tratados:
  - QA-APP-0048-001
  - QA-APP-0048-002
  - QA-APP-0048-003
```

## Escopo

Este patch corrige exclusivamente os três achados acima e propaga a decisão
D-0026-12 (patch `P02` da ADR-0048), já aprovada, que fecha o literal público
`filho_default`. Não executa QA, não cria handoff, não implementa código e
não altera `ITEM-0023`/`ITEM-0024`.

## QA-APP-0048-001 — schema público materializado

`contrato_json_console.md` §16.7 foi reescrita: de "nome literal do campo
não fechado" para "literal público fechado: `filho_default`". A seção agora
registra, para cada pai: obrigatoriedade do campo; valor como ID estável de
exatamente um filho direto de `filhos`; pertencimento ao próprio pai;
inexistência de `filho_default` global ou mapa paralelo pai → filho;
irrelevância da ordem física e do índice ordinal; primeiro filho não é
fallback; ausência e referência inexistente/ambígua/de outro pai como
inválidas; e o valor como origem da baseline persistida. Nenhum campo, enum
ou versão de schema novo foi inventado — apenas a transcrição do já fechado
por D-0026-12.

`contrato_console.md` §26.3, §26.8, §26.9, §26.10 e §26.11 passaram a citar
`filho_default` explicitamente na carga/baseline, na substituição por
sucesso, na preservação em `ABORTADO` e falha, e na restauração — sem
alterar o comportamento já fechado, apenas nomeando o literal que antes era
genérico ("escolha ativa persistida").

`42_DADOS_EXTERNOS_MULTINIVEL.md` §4.7, §6 e §7 substituíram "schema literal
do campo: não fechado" por "literal público fechado: `filho_default`
(D-0026-12)", e o termo foi acrescentado à lista de termos proprietários
(§3). Módulos `32` e `43` não continham afirmação de schema aberto nem
exclusão do modelo — nenhuma alteração foi necessária neles.

## QA-APP-0048-002 — backlog reconciliado

O `ITEM-0026` já estava com `Status: pronto_para_handoff`, mas sua "Próxima
ação" ainda tratava o nome literal do campo como pendência aberta. A linha
foi reescrita para apontar a criação do handoff de implementação a partir da
ADR-0048 aplicada e dos contratos reconciliados (incluindo `filho_default`),
mantendo como detalhes executivos genuinamente abertos apenas nome de
script/função, caminho físico e mecanismo concreto de escrita atômica.
`ITEM-0023` e `ITEM-0024` não foram tocados.

## QA-APP-0048-003 — exclusão indevida do modelo removida

`contrato_json_console.md` §16.6 excluía "o modelo" da responsabilidade de
persistência — fronteira nunca decidida por D-0026-01 a D-0026-11. A frase
foi corrigida para preservar apenas as fronteiras aprovadas: persistência
pertence à camada responsável pelos dados; renderer não persiste; loader não
persiste (já fechado por ADR-0048 §3). Nenhuma nova decisão sobre o papel do
modelo foi introduzida.

## Arquivos efetivamente alterados

- `docs/contratos/contrato_json_console.md`
- `docs/contratos/contrato_console.md`
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md`
- `docs/backlog.md`
- `docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0048_P01.md` (este relatório)

`docs/nomenclatura/32_CONSOLE.md` e
`docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` foram lidos
focalmente e não exigiram alteração — nenhum trecho neles registrava schema
aberto ou exclusão do modelo.

## Verificações

- `rg` por delegação ao handoff (`nome.*campo.*abert|campo.*handoff|schema.*handoff|schema.*abert`) nos seis documentos: sem ocorrências.
- `rg 'filho_default'` nos cinco documentos aplicáveis: todas as ocorrências são própria por pai, sem propriedade global, consistentes com D-0026-12.
- `rg` por exclusão do `modelo`: sem ocorrências restantes.

## Detalhes executivos que continuam abertos

Nome de função, nome e caminho concreto do script, assinatura interna,
algoritmo físico de escrita e mecanismo de atomicidade — preservados como
pendências para a etapa de implementação, sem serem decididos aqui.

## Bloqueios

nenhum

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
  termos_adicionados:
    - "literal público `filho_default` (ADR-0048, D-0026-12)"
  termos_alterados: []
  distincoes_adicionadas: []
  fronteiras_alteradas:
    - "persistência não exclui mais o `modelo` sem decisão correspondente (contrato_json_console.md §16.6)"
  dependencias_condicionais_adicionadas: []
```
