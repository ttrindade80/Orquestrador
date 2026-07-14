# Relatório de Auditoria — ADR-0011 e ADR-0012

## Status

QA_REJECTED

## Contexto

Auditoria documental das alterações relacionadas a:

- ADR-0011 — Terminologia de arranjo: `vertical`/`horizontal`;
- ADR-0012 — `barra_de_menus` declarativa por tela.

A auditoria verificou coerência documental, limitação de escopo e prontidão
para commit. Não foram alterados código, JSONs, handoffs ou contratos além
deste relatório de auditoria.

## Arquivos lidos

- `docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`
- `docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0011_ADR-0012.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`

## Verificações executadas

```text
git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md
?? docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md
?? docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md
?? docs/relatorios/RELATORIO_DOCUMENTAL_ADR-0011_ADR-0012.md
```

```text
git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 20 ++++++++--
 scripts/docs/adr/INDICE_ADR.md                     |  2 +
 scripts/docs/contratos/contrato_barra_de_menus.md  | 13 +++++++
 .../docs/contratos/contrato_composicao_corpo.md    | 43 ++++++++++++++--------
 .../docs/contratos/contrato_json_tela_minima.md    | 10 ++++-
 scripts/docs/contratos/contrato_tela_json.md       | 12 ++++++
 6 files changed, 79 insertions(+), 21 deletions(-)
```

```text
git diff --name-only
scripts/docs/NOMENCLATURA.md
scripts/docs/adr/INDICE_ADR.md
scripts/docs/contratos/contrato_barra_de_menus.md
scripts/docs/contratos/contrato_composicao_corpo.md
scripts/docs/contratos/contrato_json_tela_minima.md
scripts/docs/contratos/contrato_tela_json.md
```

## Verificação da ADR-0011

ADR-0011 foi criada com escopo correto e registra:

- `vertical` e `horizontal` como nomes finais de `corpo.arranjo`;
- `vertical` como substituto conceitual de `sobreposto` e `empilhado`;
- `horizontal` como substituto conceitual de `lado_a_lado`;
- `sobreposto` e `lado_a_lado` como aliases transicionais até migração específica;
- novos handoffs e novos JSONs usando `vertical`/`horizontal`, salvo compatibilidade transicional explícita;
- referências H-0011A-D como históricas, sem orientar novos ciclos;
- ausência de migração de código, JSON ou testes nesta ADR.

Resultado: aprovada quanto ao conteúdo da ADR em si.

## Verificação da ADR-0012

ADR-0012 foi criada com escopo correto e registra:

- `barra_de_menus` declarativa por tela;
- Orquestrador não obrigado a declarar todos os chips canônicos por padrão;
- cada tela declara apenas chips aplicáveis;
- renderer, loader, modelo e demo não geram chips canônicos;
- testes validam chips declarados no JSON, não conjunto global obrigatório;
- chip canônico existente não implica presença em toda tela;
- chips condicionais só aparecem quando a capacidade existir ou aplicar;
- remoção futura de chips extras do Orquestrador como alteração declarativa se o suporte já existir;
- ausência de remoção de chips e ausência de alteração de JSON nesta ADR.

Resultado: aprovada quanto ao conteúdo da ADR em si.

## Verificação de contratos e NOMENCLATURA

As alterações em `NOMENCLATURA.md`, `contrato_composicao_corpo.md`,
`contrato_tela_json.md` e `contrato_json_tela_minima.md` atualizam a
terminologia principal para `vertical`/`horizontal` e registram aliases
transicionais sem torná-los valores finais.

As alterações em `contrato_barra_de_menus.md` e `NOMENCLATURA.md` registram
a política declarativa por tela e declaram que o Orquestrador não precisa
de todos os chips canônicos.

Entretanto, permanecem contradições em trechos ativos:

- `docs/contratos/contrato_barra_de_menus.md` ainda define
  `[Esc]`, `[⏎]` e `[?]` como "chips canônicos de existência sempre presente"
  em toda instância de `barra_de_menus`.
- `docs/NOMENCLATURA.md` ainda marca `[Esc]`, `[⏎]` e `[?]` como presença
  "sempre" na tabela de chips canônicos.
- ADR-0012 declara que a existência de chip canônico como categoria semântica
  não obriga sua presença em toda tela e deixa a definição de conjunto mínimo
  obrigatório explicitamente fora do escopo.

Também permanecem menções operacionais a H-0011A em contratos ativos
(`contrato_composicao_corpo.md`, `contrato_json_tela_minima.md` e
`contrato_json_dashboard.md`) relacionadas a compatibilidade/migração de
`posicao_dashboard`. Parte do texto novo esclarece que H-0011A-D é histórico,
mas esses trechos ainda podem ser lidos como orientação operacional futura
por H-0011A.

## Verificação de escopo

`git diff --name-only` não contém:

- `scripts/config/`
- `scripts/tela/`
- `scripts/docs/handoff/`

Não houve alteração indevida em código, JSON ou handoffs.

`contrato_json_dashboard.md` permaneceu inalterado. Isso é aceitável quanto à
divergência `dashboard.campos[]` vs `conteudo`/`regras_exibicao`, que segue
fora de escopo. A ressalva é apenas a permanência de referências operacionais
a H-0011A.

## Achados bloqueantes

1. Contradição ativa entre ADR-0012 e contratos/NOMENCLATURA sobre chips
   canônicos sempre presentes. A ADR-0012 afirma que chip canônico não implica
   presença em toda tela e deixa o conjunto mínimo obrigatório fora de escopo,
   mas `contrato_barra_de_menus.md` e `NOMENCLATURA.md` ainda definem
   `[Esc]`, `[⏎]` e `[?]` como sempre presentes.

2. Referências operacionais residuais a H-0011A em contratos ativos podem
   contradizer a decisão de que H-0011A-D permanece apenas como histórico e
   não orienta novos ciclos.

## Achados não bloqueantes

0.

## Pontos positivos

- ADR-0011 e ADR-0012 estão bem separadas, conforme decisão gerencial.
- O índice de ADRs registra corretamente ADR-0011 e ADR-0012.
- A terminologia `vertical`/`horizontal` foi aplicada nos pontos centrais dos
  contratos alterados.
- O escopo Git está limitado a documentação em `docs/`, sem mudanças em
  `config/`, `tela/` ou `docs/handoff/`.
- A documentação preserva fora de escopo: sem migração de código, JSON ou
  testes neste ciclo.

## Conclusão

Não pode seguir para commit documental ainda.

As ADRs estão corretas em si e o escopo de arquivos está limpo, mas há
inconsistência documental ativa entre ADR-0012 e trechos de contrato/glossário
sobre chips canônicos sempre presentes, além de referências residuais a
H-0011A como orientação operacional. Recomenda-se ajustar esses trechos antes
do commit.
