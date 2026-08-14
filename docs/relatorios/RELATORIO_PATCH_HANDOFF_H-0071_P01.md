# RELATÓRIO — PATCH_HANDOFF H-0071 P01

## Metadata

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
patch: P01
tipo: PATCH_HANDOFF
data: 2026-08-13
```

## Achado tratado

`QA-H0071-002` — insuficiência de autorização concreta para o preset
`Ornamental` em `config/estilo.json`.

## Contradição interna corrigida

O H-0071 exigia, como critério de aceite fechado (`CA-H0071-05`) e como
item da demonstração manual (seção 11, item 2), a forma `╭PgUp/PgDn╮` para
o preset `Ornamental`. A configuração concreta vigente materializa
`❲PgUp/PgDn❳` para esse preset. A seção 8.2 original, no entanto, restringia
a alteração autorizada em `config/estilo.json` exclusivamente à adição de
`cor_fundo_esquerdo`/`cor_fundo_direito` em `Destaque Texto`, sem qualquer
autorização para tocar os campos de delimitador do preset `Ornamental`.
Isso tornava `CA-H0071-05` inexequível dentro do próprio escopo de
implementação que o handoff definia — uma contradição interna entre a
seção 9 (critérios de aceite) e a seção 8.2 (escopo de configuração).

## Nova autorização concreta em `config/estilo.json`

A seção 8.2 foi estendida para autorizar explicitamente, no preset
`chip.presets["Ornamental"]`, a correção dos campos de schema já
existentes `caractere_esquerdo` e `caractere_direito` para os valores
`"╭"` e `"╮"`. Não é criação de campo, preset ou schema novo: é correção
de valor concreto de campos de schema já aprovados, com finalidade
exclusiva de materializar a forma já exigida pelo próprio handoff.

## Preservação do restante do H-0071

Nenhuma outra seção foi alterada. Permanecem intocados: composição
multitecla com `/`, os demais presets (Colchete, Curva, Traço, Ponto,
Destaque Texto, Destaque Fundo), os valores `"padrão"`/`"azul"` já
autorizados, a lista de arquivos de implementação e testes já autorizados
(seções 8.1, 8.3, 8.4, 8.5), os critérios de aceite (seção 9, inalterados
em texto — apenas tornados exequíveis), a seção de testes (10), a
demonstração manual (11) e os bloqueios (13). `MF-ITEM0010-003` permanece
fora de escopo, sem menção adicional.

## Verificações

1. `CA-H0071-05` agora pode ser implementado sem exceção de escopo — a
   seção 8.2 autoriza explicitamente os dois campos necessários.
2. A autorização para `config/estilo.json` inclui explicitamente os
   delimitadores Ornamental `╭` e `╮`.
3. Nenhuma decisão normativa nova foi criada: os campos
   `caractere_esquerdo`/`caractere_direito` já são schema aprovado;
   apenas seu valor concreto foi corrigido para atender exigência já
   fechada no próprio handoff.
4. `QA-H0071-001` (preset_default alterado de Colchete para Curva,
   caixa_alta, falhas de popup/paginação) permanece integralmente
   reservado ao futuro `PATCH_IMPLEMENTACAO` — não tratado aqui.
5. `QA-H0071-003` não produziu expansão especulativa de escopo: nenhuma
   alteração foi feita com base em itens `NAO_CONFIRMADO` da suíte
   canônica.
6. Nenhum outro arquivo foi alterado além de
   `docs/handoff/H-0071-correcao-chips-multitecla-barra-menus-estilo.md`
   e deste relatório.

## Bloqueios

Nenhum.
