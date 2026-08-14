# RELATÓRIO — PATCH_HANDOFF H-0071 P05

```yaml
projeto: Orquestrador
handoff: H-0071
patch: P05
etapa: PATCH_HANDOFF
data: 2026-08-14
status: PATCH_HANDOFF_CONCLUIDO
```

## Cadeia H-0071

H-0071 permanece a fatia de correção pós-validação manual do ITEM-0010,
sob ADR-0046. Estado documental transportado: ADR-0046 pós-P03
`ADR_APPROVED`; aplicação documental pós-P03/P01
`ADR_APPLICATION_APPROVED_WITH_NOTES` (nota só de proveniência do WIP;
sem achado material pendente). Este P05 atualiza somente o handoff; não
implementa, não executa QA e não altera o relatório P04.

Afirmações de
`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0071_P04.md` deixam de
ser evidência vigente, inclusive as de que a Barra real já produz
`[PgUp/PgDn]` e já preserva `cor_inativo`.

## ACH-H0071-P05-01

O H-0071 vigente ainda preservava Ornamental como `╭`/`╮`, tratando-o
como equivalente à Curva. Corrigido: Curva = `╭`/`╮`; Ornamental =
`❲`/`❳`. Exemplos canônicos: Colchete `[PgUp/PgDn]`, Curva
`╭PgUp/PgDn╮`, Ornamental `❲PgUp/PgDn❳`. A configuração concreta
`config/estilo.json` entra no escopo futuro para restaurar essa
distinção.

## ACH-H0071-P05-02

O escopo executável antigo obrigava alteração em renderers e
carregamento. A causa confirmada é entrada declarativa legada: H-0063
declara um único `chip_paginas` com `tecla: "PgUp][PgDn"` e
`regra_ativo: "quando_paginacao"`. O compositor envolve corretamente
esse payload; `[PgUp][PgDn]` não é defeito do delimitador. Em 1/1 o
estado inativo não chega ao compositor porque a regra agregada não é
reconhecida. A correção autorizada é reconciliar a representação/entrada
já consumida pelo agrupamento vigente
(`chip_pagina_anterior`/`chip_pagina_proxima`), sem schema nem semântica
novos.

A mesma declaração legada em H-0054 e H-0055 entra no escopo só para
impedir persistência do defeito, sem comportamento novo.

## Escopo nominal mínimo de implementação

Autorizados:

- `config/estilo.json`
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
- `config/telas/demo/h0054_selecao_multinivel.json`
- `config/telas/demo/h0055_dois_niveis_por_foco.json`
- relatório futuro de implementação

Obrigação de alteração revogada para os defeitos atuais:

- `tela/renderizacao/barra_menus.py`
- `tela/renderizacao/estilo.py`
- `tela/carregamento/estilo.py`
- `tela/renderizacao/conteudo_externo.py`
- `tela/testes_renderizador/fundamentos.py`

Evidência positiva futura de necessidade de algum desses arquivos exige
exceção operacional antes da alteração.

## Testes / regressão do ponto real

Obrigatórios:

- `tela/teste_estilo_h0071.py` — expectativa canônica independente Curva
  × Ornamental;
- `demo/teste_demo_estilo_h0063.py` — caminho real da configuração
  H-0063; ausência de `[PgUp][PgDn]`; composição canônica; inativo em
  1/1;
- `demo/teste_demo_console.py` — forma física vigente no lugar da
  expectativa `[PgUp][PgDn]`.

Não basta fixture com dois chips bem formados. Helpers unitários,
`INTEGRACAO_PARCIAL` H-0071, fixtures H-0045 e inspeções em
`fundamentos.py` não provam sozinhos a tela H-0063 real. Demais testes
já exigidos podem permanecer como regressão sem obrigação de mudar
conteúdo. Validação visual final permanece do usuário em TTY.

## Verificações

- leitura integral: H-0071, ADR-0046, `contrato_chip.md`;
- busca focal somente no H-0071;
- `git diff --check` nos dois artefatos desta etapa.

## Bloqueios

Nenhum. Não houve decisão de arquitetura, schema, formato visual,
semântica de paginação ou arquivo executável fora dos fatos
transportados.
