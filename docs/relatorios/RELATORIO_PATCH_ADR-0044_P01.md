# Relatório do patch P01 — ADR-0044

**Item:** ITEM-0017
**ADR:** ADR-0044
**Origem:** `BLOCKED_USER_DECISION` durante CRIAR_HANDOFF H-0056

## Motivo

A criação do H-0056 revelou que a ADR-0044 separava configuração estrutural,
conteúdo pronto e runtime, mas ainda não fechava o campo, a localização, a
cardinalidade, a forma e a identidade das declarações de pop-up.

## Decisão incorporada

Foi incorporada a D-POP-25. Ela define `popups` no nível geral do JSON
estrutural da tela, como mapa/objeto de `0..N` declarações. A chave é o ID
estável da declaração, sem `id` interno obrigatório redundante. Cada valor
contém somente configuração estrutural/interativa. A abertura referencia o
ID e fornece envelope pronto, com contrato de resultado quando aplicável.
Declarações podem ser reutilizadas com envelopes compatíveis diferentes e
permanecem distintas das instâncias de runtime.

## Áreas alteradas

Foi adicionada a seção normativa D-POP-25 na área “Configuração, conteúdo e
estado vivo”, mantendo os tipos de conteúdo, geometria, navegação, envelopes,
retorno, validação, decomposição e fora de escopo existentes.

D-POP-01..24 foram preservadas integralmente; nenhuma decisão anterior foi
removida ou alterada.

## Verificações e bloqueios

- Confirmados literalmente `popups`, mapa/objeto, `0..N`, nível geral e exclusão de `cabecalho`, `corpo` e `barra_de_menus`.
- Confirmados ID estável na chave, ausência de `id` interno obrigatório, conteúdo concreto fora da configuração, abertura por ID + envelope pronto e reutilização.
- Confirmada a ausência de produtor, loader e ação de negócio no pop-up.
- Confirmado que nenhuma decisão de H-0057/H-0059 foi antecipada.
- `git diff --check` passou para os arquivos alterados.

**Bloqueios:** nenhum.
