---
name: RELATORIO_QA_ADR-0047_POS_P01
description: "QA pós-patch P01 da ADR-0047 — verifica se QA-ADR-0047-001 foi integralmente resolvido"
metadata:
  type: relatorio
  etapa: QA_POS_PATCH_ADR
  objeto: ADR-0047
rastreabilidade:
  cadeia:
    raiz: docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md
    predecessor_imediato: docs/relatorios/RELATORIO_PATCH_ADR-0047_P01.md
  achado_original: QA-ADR-0047-001
---

# Relatório — QA_POS_PATCH_ADR ADR-0047 (pós-P01)

## QA-ADR-0047-001: RESOLVIDO

A nova §4.13 fecha localização, forma e nomes literais das três capacidades
(tabulação, designador local, apresentação/tabela) sob
`formato.dois_niveis_por_foco.filho` no elemento `console` do JSON estrutural
da tela — nunca no documento externo de conteúdo. §5, §6, §7, §8, §9 e §10
foram reescritos de forma consistente com essa localização; D-DNF-04 e
D-DNF-11 (§3) não atribuem mais as capacidades ao schema semântico
multinível. `grep` confirmou ausência de linguagem residual de decisão
aberta ("não fixado", "deferida"): as duas ocorrências remanescentes de
"pontos de extensão" pertencem ao contexto histórico (§2.1) e à afirmação
explícita de não-integração a esses pontos (§5), não a lacuna. `APLICAR_ADR`
não precisa mais escolher localização, cardinalidade ou literal novo.

## Verificações focais

1. **QA-ADR-0047-001** — resolvido; ver acima.
2. **APLICAR_ADR sem decisão de schema** — confirmado; §4.13 fecha local,
   tipos, cardinalidades (`tabulacao.minimo/maximo`, `tabela.colunas[].campo`
   com mínimo 1 item, `tabela.espacamento.minimo/maximo`) e valores desta
   atividade (5/10, 3/8).
3. **Separação configuração × conteúdo** — correta; §4.13 e §5 reafirmam que
   o documento externo permanece exclusivamente dados, inclusive para
   conteúdo dinâmico (H-0063 futura); nenhuma remissão residual aos blocos
   `formato.espacamento`/`formato.alinhamento`/`conteudo` do schema
   multinível (`contrato_json_console.md` §12.2/§12.3) permanece.
4. **Compatibilidade estrutural do local** — confirmada por leitura de
   `config/telas/demo/h0055_dois_niveis_por_foco.json`: o elemento `console`
   já possui `formato.excesso.politica_modo` como bloco real e vigente no
   mesmo nível hierárquico; `formato.dois_niveis_por_foco.filho` ocupa o
   mesmo local estrutural, sem conflito com campos existentes, exatamente
   como o próprio §4.13 declara (precedente `console.formato.excesso`).
5. **Suficiência e não contradição** — os campos e cardinalidades fechados
   (tabulação min/max, designador, apresentação texto/tabela, colunas com
   `campo` e sem `numero_colunas`, espaçamento min/max) não contradizem
   `contrato_json_console.md` §12.6 (proibição de geometria calculada no
   documento externo) nem `contrato_console.md` §19.4/§19.6; são suficientes
   para propagação direta aos contratos.
6. **Apresentação tabular não vira nova política** — §4.5 mantém
   explicitamente que a capacidade não altera `politica_navegacao.tipo`, não
   cria terceiro nível e cada linha permanece do mesmo item lógico filho;
   consistente com `contrato_console.md` §22.11/§22.16 (ADR-0042, autoridade
   preservada).
7. **H-0063 como formatação pura** — §4.11 e D-DNF-09 mantêm a lista de
   proibições de conteúdo (nomes, textos, exemplos, símbolos, ordem, valores
   de estilo, seleção, candidato, baseline, aplicação, persistência,
   publicação); os dois campos de `tabela.colunas` referenciam campos reais
   já existentes, sem inventar ou renomear; a fixture atual de H-0063 ainda
   não declara `formato.dois_niveis_por_foco.filho` — reconciliação futura
   prevista e não exigida nesta ADR (§4.12, §7 custos).

Nenhum achado novo decorre materialmente do delta P01.

## Status final

status: ADR_APPROVED
\n