# Relatório — Patch ADR-0048 P02

```yaml
cadeia.raiz: ADR-0048
predecessor_material: QA-APP-0048-001
etapa: PATCH_ADR
papel: autor documental
item: ITEM-0026
data: 2026-08-16
```

## Predecessor

O QA da aplicação documental (`QA-APP-0048`) resultou em
`BLOCKED_DOCUMENTATION`. Dos três achados relacionados, somente
`QA-APP-0048-001` — nome/representação pública da escolha persistida não
fechado — exigia nova decisão da ADR. `QA-APP-0048-002` (backlog avançado
prematuramente) e `QA-APP-0048-003` (aplicação excluiu modelo sem
autoridade) pertencem à futura correção da aplicação e não foram tratados
nesta etapa.

## Decisão do usuário incorporada

O usuário determinou que o schema persistido de `dois_niveis_por_foco`
replique a forma estrutural já usada pelo Estilo para registrar o preset
persistido de cada categoria (`preset_default`/`presets`). Essa decisão foi
registrada como **D-0026-12** (patch `P02`), preservando integralmente
D-0026-01 a D-0026-11.

## Literal público fechado

`filho_default` — nome exato, obrigatório, por pai, contendo o ID de
exatamente um filho direto daquele pai. Não substituível por `filho_ativo`,
`filho_ativo_id`, `selecionado`, `selected`, `active` ou outro alias.

## Trechos ajustados na ADR

- **Introdução**: registra o patch `P02`, o resultado `BLOCKED_DOCUMENTATION`
  do QA da aplicação e o achado `QA-APP-0048-001` como motivador.
- **Nova seção 2.12 (D-0026-12)**: literal fechado, forma estrutural (coleção
  `filhos`, campo `filho_default` por pai, sem `filho_default` global, sem
  mapa paralelo, sem índice ordinal), semântica normativa de 17 pontos,
  relação com o padrão estrutural do Estilo (analogia de padrão de
  persistência, não de autoridade), representação conceitual ilustrativa e
  reafirmação do que a decisão não altera.
- **Seção 3 (Camadas de estado)**: nota indicando que a escolha ativa
  persistida é representada, no documento externo, por `filho_default`.
- **Seção 6 (Relação com ADR-0046)**: acréscimo estendendo a analogia de
  filosofia ao nível estrutural do nome do campo.
- **Seção 7 (Distinções terminológicas)**: nova linha `preset_default` ×
  `filho_default`.
- **Seção 8 (Consequências positivas)**: item registrando o fechamento do
  literal como resolução do bloqueio de QA.
- **Seção 9 (Documentos potencialmente afetados)**: nota de que a forma
  literal já está fechada e deve ser usada tal como decidida.
- **Seção 10 (Itens fora de escopo)**: item que antes dizia que o "schema
  executivo literal" pertencia à aplicação foi substituído — agora só a
  redação concreta nos contratos/nomenclatura permanece executiva; a decisão
  de nome está fechada.
- **Seção 11 (Critérios para aplicação)**: dois critérios novos exigindo o
  literal exato `filho_default` e a ausência de mapa global paralelo ou
  índice ordinal como identidade.
- **Seção 12 (Alternativas consideradas)**: referência atualizada de
  D-0026-01–11 para D-0026-01–12.

## Decisões anteriores preservadas

D-0026-01 a D-0026-11 permanecem integralmente — autoridade no documento
externo, baseline × candidato, cursor × escolha, confirmação por pop-up,
persistência delegada, sucesso, `ABORTADO`, fail-closed, restauração e
fronteiras (incluindo `ITEM-0023`/`ITEM-0024` fora de escopo).

## Detalhes executivos que continuam abertos

Nome de função, nome e caminho do script, assinatura interna, algoritmo
físico de escrita, mecanismo concreto de escrita atômica, e a redação textual
concreta do literal `filho_default` nos contratos/nomenclatura afetados.

## Verificações

- `rg` focal em `filho_default|filho_ativo|filho_ativo_id|nome.*campo|literal|schema.*abert|handoff.*campo|campo.*handoff` sobre a ADR: `filho_default` é o único literal público escolhido; as ocorrências de `filho_ativo`/`filho_ativo_id` são exclusivamente rejeição explícita de alias ou a apresentação visual preexistente `Pai: filho_ativo` do `ITEM-0023` (não alterada, fora de escopo); nenhum trecho delega a escolha do campo ao handoff.
- `git status --porcelain`: confirma que somente a ADR-0048 (já não rastreada) foi modificada nesta execução, além deste relatório.

## Bloqueios

Nenhum.
