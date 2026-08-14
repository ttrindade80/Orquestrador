# RELATÓRIO — PATCH_HANDOFF H-0071 P02

```yaml
item: ITEM-0010
adr: ADR-0046
handoff: H-0071
patch_handoff: P02
raiz: docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0071.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0071_P01.md
data: 2026-08-13
```

## Motivo da ampliação

O QA pós-patch da implementação retornou `I3_HANDOFF_PATCH_REQUIRED`. Os
achados de implementação `QA-H0071-001` e `QA-H0071-002` estão resolvidos
(`preset_default` restaurado para `Colchete`; `Ornamental` materializado com
`╭`/`╮`); não há regressão H-0071 nos focos auditados. O QA classificou os
resíduos remanescentes (Barra 1 failed, paginação 2 failed, suíte canônica
13 failed/1 error) como expectativas de teste desatualizadas por efeito
direto das mudanças de representação já aprovadas neste handoff — não como
defeito de implementação. O escopo nominal de testes do H-0071 (seção 8.3)
não cobria esses arquivos, o que impede sua correção sem exceder o
escopo autorizado.

## Arquivos de teste adicionados ao escopo (§8.3.1)

- `tela/teste_renderizador.py`
- `demo/teste_demo.py`
- `demo/teste_demo_console.py`
- `demo/teste_demo_estilo_h0069.py`
- `demo/teste_demo_estilo_h0070.py`

Permanecem autorizados, sem mudança: `tela/testes_renderizador/barra_menus.py`
e `demo/teste_demo_paginacao.py`. `demo/teste_diagnostico.py` **não** foi
adicionado — seu erro é derivado do código de saída de
`tela/teste_renderizador.py` e deve desaparecer pela correção das
falhas-raiz, sem edição própria.

## Natureza restrita das atualizações autorizadas

Somente adaptação de expectativas à autoridade já vigente: (1) unidade
multitecla única com `/` substituindo formas separadas ou concatenadas;
(2) `[PgUp][PgDn]` → `[PgUp/PgDn]`; (3) capitalização conforme o preset
`Colchete` ativo (`"Confirmar"`, não `"CONFIRMAR"`); (4) asserções sobre
ANSI verificando conteúdo visível e contenção dentro da unidade, em vez de
literal bruto. A intenção funcional original de cada teste (ordem,
atividade, seleção, paginação, ausência de truncamento, navegação, estado
inativo, rótulos dinâmicos) deve ser preservada. Nenhuma mudança de código
de produção, configuração, ADR, contrato ou nomenclatura é autorizada por
este patch.

## Critérios de aceite materializados

`CA-H0071-14` a `CA-H0071-19` adicionados à seção 9 do handoff, cobrindo:
uso uniforme da unidade `/` (14); validação de ANSI por conteúdo/contenção
sem envelope antigo (15); capitalização respeitando o preset ativo (16);
preservação da intenção funcional dos testes (17); suíte canônica retornando
código zero salvo falha nova evidenciada (18); e não alteração de
`demo/teste_diagnostico.py` (19).

## Preservações

- `MF-ITEM0010-003` permanece explicitamente fora de escopo.
- `preset_default`, `Ornamental`, cursor, toggle, hierarquia não são
  reabertos por este patch.
- Nenhum código de produção, configuração, ADR, contrato ou nomenclatura foi
  alterado nesta etapa — apenas o próprio handoff `H-0071`.
- Proibições explícitas contra skip/xfail, remoção de teste sem substituto
  equivalente e enfraquecimento de asserts não afetados foram registradas no
  handoff.

## Bloqueios

Nenhum.
