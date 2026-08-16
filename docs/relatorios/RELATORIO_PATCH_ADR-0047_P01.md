---
name: RELATORIO_PATCH_ADR-0047_P01
description: "Correção da fronteira configuração x conteúdo e fechamento do schema literal em ADR-0047, tratando QA-ADR-0047-001"
metadata:
  type: relatorio
  etapa: PATCH_ADR
  objeto: ADR-0047
rastreabilidade:
  cadeia:
    raiz: docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md
    predecessor_imediato: docs/relatorios/RELATORIO_QA_ADR-0047.md
  achado_tratado: QA-ADR-0047-001
---

# Relatório — PATCH_ADR ADR-0047 (P01)

## Achado tratado

`QA-ADR-0047-001`: a ADR não fixava localização, cardinalidade nem
nomenclatura literal para tabulação min/max, designador local, apresentação
e colunas, deixando decisão material de schema aberta para `APLICAR_ADR`, e
atribuía essas declarações — por meio de remissão a
`contrato_json_console.md` §12.2/§12.3 — ao envelope declarativo do
documento externo de conteúdo, que é ele próprio dados, não configuração.

## Correção da fronteira configuração × conteúdo

Todas as passagens que ancoravam as novas capacidades aos blocos
`formato.espacamento`/`formato.alinhamento` do documento externo de
conteúdo ou ao mecanismo `conteudo` por nível (§4.5, §4.8, §5, §7, §8, além
de `integracao` em D-DNF-04 e da chave raiz de D-DNF-11 em §3) foram
reescritas: as três capacidades passam a pertencer exclusivamente ao
elemento `console` do JSON estrutural da tela, no mesmo local já usado pelo
precedente `console.formato.excesso.politica_modo` (D23). O documento de
conteúdo permanece fornecendo somente dados — reafirmado explicitamente
para telas de conteúdo dinâmico (H-0063).

## Schema literal fechado

Nova §4.13 fecha, sob `politica_navegacao.tipo = "dois_niveis_por_foco"`, o
bloco `formato.dois_niveis_por_foco.filho` com `tabulacao.{minimo,maximo}`
(5/10), `designador` (mecanismos já vigentes), `apresentacao` (`"texto"` |
`"tabela"`) e, quando `"tabela"`, `tabela.colunas[].campo` (array, ≥1,
ordem = ordem visual, sem `numero_colunas`, declaração única por tela) e
`tabela.espacamento.{minimo,maximo}` (3/8). §4.2, §4.5, §4.8 e §5 foram
ajustadas para remeter a esse local; §5 deixou de afirmar nomenclatura não
fixada. §4.11 (H-0063) passou a expressar o bloco concreto instanciado
(`designador.tipo = nenhum`, `apresentacao = tabela`, 2 colunas, campos
existentes de texto/nome e exemplo visual, sem inventar/renomear campos
reais).

## Trechos materiais corrigidos

- §3, D-DNF-04 (`integracao`) e D-DNF-11 (chave raiz): removida a
  atribuição ao schema semântico multinível/documento externo.
- §4.2, §4.5, §4.8, §4.11, §5, §6, §7, §8, §9, §10: reescritos para apontar
  ao envelope estrutural do `console` (§4.13) e remover toda menção a
  nomenclatura "não fixada"/"deferida à aplicação documental".
- §9: removido o item "fora de escopo" sobre fixar nomenclatura literal —
  deixou de ser lacuna nesta ADR.
- §10: acrescentados critérios específicos do schema fechado (localização
  exclusiva no JSON estrutural, tipos/limites de `tabulacao` e
  `espacamento`, regras de `apresentacao`/`tabela.colunas`) e reescrito o
  critério de H-0063 com os valores concretos.

## Verificações

- Leitura integral do manifesto fechado (ADR, `RELATORIO_QA_ADR-0047.md`,
  `contrato_tela_json.md`, `contrato_console.md`, `contrato_json_console.md`,
  fixtures H-0055 e H-0063) antes da edição.
- `grep` pós-edição confirmou ausência de resíduos de "não fixa"/"não
  fixada"/"deferida"/"documento de conteúdo/apresentação"/"pontos de
  extensão já reservados" na ADR.
- Nenhuma alteração de código, teste, configuração ou aplicação da ADR foi
  realizada.
- Único arquivo alterado: `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`.
  Único arquivo criado: este relatório.

## Bloqueios

nenhum
\n