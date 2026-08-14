# Relatório — Patch de aplicação documental da ADR-0046 (P02)

```yaml
item: ITEM-0010
adr: docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md
patch_adr: P01
etapa: PATCH_APLICACAO_ADR
raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0046.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0046_P01.md
```

## Arquivos alterados

- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/nomenclatura/10_ESTILO.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`

## Materialização das decisões

`contrato_chip.md` passou a ser a autoridade única e especializada da
composição multitecla, para evitar mecanismo concorrente. Novas seções
10.1–10.5: unidade visual única com delimitadores externos e separador `/`
(`DEC-01`); preset Ponto em multitecla (`DEC-02`); `/` como constante
estrutural, não campo de preset nem hardcoding (`DEC-05`); contenção de
cor/fundo sem vazamento para texto ou chip seguinte (`DEC-03`); largura
visual efetiva desconsiderando ANSI (`DEC-06`). A notação histórica
`[PgUp][PgDn]` (seção 7) foi anotada como identificador documental, não mais
forma renderizável concorrente.

`contrato_estilo.md` (autoridade de schema) recebeu a extensão opcional por
preset `cor_fundo_esquerdo`/`cor_fundo_direito` (`DEC-04`), preservando a
assimetria decidida (delimitador esquerdo na cor do terminal, direito na cor
de destaque) sem reduzi-la à equivalência `cor_texto`/`cor_fundo`; não amplia
os cinco campos obrigatórios (R-3). Novas regras R-14 (composição/contenção)
e R-15 (largura visual efetiva), com cross-referência a `contrato_chip.md`
em vez de duplicar a regra.

`contrato_barra_de_menus.md` recebeu a seção 18.1 e a regra R-14,
estabelecendo que a Barra real consome a mesma composição de chip e o mesmo
estilo global da demonstração, sem mecanismo visual paralelo (`DEC-03`); a
seção 24.4 (`representacao_canonica` da ADR-0041) foi anotada para
reconciliar com a unidade única, sem apagar a decisão histórica de tecla e
rótulo.

`DEC-ITEM0010-CHIP-07` não foi tocado: nenhuma alteração de ordem,
indentação, cursor/toggle ou nomenclatura de console foi feita.

## Extensão de schema

Extensão mínima em `contrato_estilo.md` §3.2: dois campos opcionais por
preset de chip (`cor_fundo_esquerdo`, `cor_fundo_direito`), nome semântico de
cor, sem valor concreto de produção definido nesta etapa e sem alteração de
`config/estilo.json`.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados:
    - docs/nomenclatura/10_ESTILO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  termos_adicionados:
    - separador canônico "/" de composição multitecla
    - unidade visual de chip multitecla
    - cor_fundo_esquerdo
    - cor_fundo_direito
    - largura visual efetiva (chip)
    - contenção de estilo do chip
  distincoes_adicionadas:
    - unidade visual multitecla × concatenação individual por tecla (H-0070 substituída)
    - notação documental em colchetes × forma visual renderizada
```

## Verificações executadas

`git diff` restrito ao manifesto, antes e depois da edição, confirmando que
somente os cinco artefatos autorizados foram tocados e que o delta
corresponde às decisões `DEC-ITEM0010-CHIP-01` a `-06`. Releitura de cada
edição aplicada para conferir ausência de duplicação de autoridade entre
`contrato_chip.md` e os demais artefatos.

## Bloqueios

Nenhum.
