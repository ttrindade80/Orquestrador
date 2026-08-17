# Relatório — Criação da ADR-0048

```yaml
etapa: CRIAR_ADR
item: ITEM-0026
titulo_item: Persistência da escolha de filho por pai
data: 2026-08-16
status: ADR_CREATED
```

## Baseline Git

- branch: `master`
- HEAD: `3a8425a` (confirmado por leitura; igual à baseline transportada)
- stage: vazio
- worktree: sem modificações em arquivos rastreados; havia um único arquivo
  não rastreado pré-existente
  (`docs/relatorios/RELATORIO_LEVANTAMENTO_ITEM-0023_ITEM-0024_ITEM-0026_R01.md`),
  em zona de não leitura, não aberto e não alterado por esta execução.
- Nenhuma operação Git de escrita foi executada.

## ADR criada

- `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md`

Não houve colisão do identificador ADR-0048 em `docs/adr/`.

## Decisões materializadas

D-0026-01 a D-0026-11, transportadas integralmente e sem alteração:

- autoridade persistida no JSON externo de conteúdo, fornecida pelo produtor
  (D-0026-01);
- exclusividade persistida — exatamente um filho ativo por pai, explícito, sem
  tratar o primeiro filho como autoridade (D-0026-02);
- baseline persistida × candidato de runtime, com cursor independente
  (D-0026-03);
- `Aplicar` somente sob divergência, com a filosofia da ADR-0046 (D-0026-04);
- reuso do pop-up genérico com `CONFIRMADO`/`ABORTADO` (D-0026-05);
- persistência delegada à camada responsável pelos dados, sem fechar nomes,
  caminhos, assinaturas ou algoritmo de escrita (D-0026-06);
- sucesso: nova baseline, candidato equalizado, retorno à seleção, `Aplicar`
  inativo (D-0026-07);
- `ABORTADO`: nada alterado, candidato preservado (D-0026-08);
- falha de persistência fail-closed (D-0026-09);
- restauração em nova execução a partir do documento externo (D-0026-10);
- fronteiras não alteradas, incluindo ITEM-0023, ITEM-0024, ITEM-0004 e
  política global de estilo (D-0026-11).

A ADR registra ainda: camadas de estado, tabela de transições,
compatibilidade, relação com ADR-0042 e com a filosofia da ADR-0046 (sem
transformar Estilo em autoridade dos dados), distinções terminológicas
obrigatórias, consequências, documentos potencialmente afetados pela futura
aplicação, fora de escopo e critérios de aplicação.

## Autoridades utilizadas

Leitura integral do manifesto fechado (16 documentos): `docs/backlog.md`;
ADR-0042; ADR-0046; `contrato_console.md`; `contrato_json_console.md`;
`contrato_estilo.md`; `contrato_popup.md`; `contrato_barra_de_menus.md`;
módulos de nomenclatura `01`, `02`, `10`, `31`, `32`, `35`, `42` e `43`.
Nenhuma busca ampla executada. Nenhum documento de `docs/relatorios/**`,
outro ADR, handoff, código-fonte, teste ou configuração concreta foi lido.

## Verificações executadas

- Existência confirmada dos dois arquivos obrigatórios
  (`docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` e este
  relatório).
- `git diff --check` sobre os dois arquivos: sem apontamentos.
- `git status`: nenhum outro arquivo alterado por esta execução além dos dois
  artefatos permitidos.

## Bloqueios

Nenhum.
