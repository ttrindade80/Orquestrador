---
name: relatorio-aplicacao-adr-0044
description: Relatório factual da aplicação documental da ADR-0044
metadata:
  type: relatorio
  scope: aplicacao_documental
  adr: docs/adr/ADR-0044-popup-modal-generico-de-decisao.md
  item: ITEM-0017
---

# Relatório de aplicação documental — ADR-0044

## Arquivos criados

- `docs/contratos/contrato_popup.md`
- `docs/nomenclatura/35_POPUP.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0044.md`

## Arquivos alterados

- `docs/adr/ADR-0044-popup-modal-generico-de-decisao.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_chip.md`
- `docs/nomenclatura/00_INDICE.md`
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`
- `docs/nomenclatura/10_ESTILO.md`
- `docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md`
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md`
- `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`
- `docs/NOMENCLATURA.md`
- `docs/INDICE.md`
- `docs/backlog.md`

## Contrato especializado

O contrato fecha a natureza modal sobreposta, a referência física no corpo,
a suspensão da tela subjacente, a geometria intrínseca, moldura, título,
conteúdo, área própria de chips, tipos `texto`/`marcacao`, políticas
`marcacao: exclusiva` e `marcacao: multipla`, navegação toroidal, envelopes,
retorno, validação fechada e resize. Mantém explícito que o pop-up não é
console, elemento funcional, região permanente ou executor de negócio.

## Propagação normativa material

O `contrato_tela_json.md` registra somente a separação entre configuração
estrutural e conteúdo runtime, sem escolher cardinalidade, coleção, mapa/lista,
nome de campo ou localização estrutural não fechados pela ADR. O contrato de
chip registra o consumo pela área própria do pop-up, preservando estilo,
distinção entre tecla/rótulo/retorno e a ordem canônica da barra. Os módulos
transversais registram apenas remissões e fronteiras necessárias. A ADR foi
marcada como `aplicada`.

## Backlog

`ITEM-0017` foi reconciliado para a capacidade de pop-up modal genérico de
decisão, com status `em_andamento`. O item preserva que a implementação ainda
não ocorreu e aponta, após a aprovação da aplicação documental, para handoffs
incrementais.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_criados:
    - docs/nomenclatura/35_POPUP.md
  modulos_alterados: []
  termos_adicionados: []
  termos_alterados: []
  distincoes_adicionadas: []
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```

O vocabulário próprio e suas distinções estão contidos no módulo 35 criado;
as alterações nos demais módulos são remissões de integração, sem mudança de
propriedade terminológica.

## Verificações

- Artefatos obrigatórios criados e caminhos autorizados conferidos.
- Busca focal confirmou que a necessidade concorrente legada não permanece no
  `ITEM-0017`.
- Busca focal no contrato e no módulo 35 confirmou a distinção entre
  `marcacao: exclusiva` e `seleção única`.
- Busca focal confirmou a proibição de paginação no contrato.
- Busca focal confirmou conteúdo pronto e ausência de origem, produtor ou
  loader para o pop-up.
- `git diff --check` e diff restrito aos arquivos autorizados.

## Bloqueios

Nenhum. A ADR não fecha schema estrutural adicional; por isso a integração
com o JSON geral foi materializada somente na fronteira autorizada.
