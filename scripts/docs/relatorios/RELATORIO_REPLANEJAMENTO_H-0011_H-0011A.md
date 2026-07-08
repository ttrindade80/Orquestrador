# Relatório — Replanejamento H-0011 / H-0011A

## Status

APROVADO_PARA_COMMIT_DOCUMENTAL

## Contexto

- H-0010A concluiu e validou o fluxo declarativo mínimo.
- H-0011 foi preparado para uma direção que foi corrigida pela ADR-0010.
- ADR-0010 definiu que dashboard não é eixo especial externo; dashboard,
  console e lancador são elementos funcionais do corpo.
- H-0011A tentou corrigir a direção do H-0011, mas ficou grande demais para o
  próximo ciclo de implementação.

## Decisão

- H-0011 fica cancelado e não deve ser implementado.
- H-0011A é removido como handoff ativo.
- A implementação prevista será fragmentada em ciclos menores.
- A sequência futura não usará letras.
- O próximo handoff de implementação deverá começar em H-0012.
- Este relatório não cria H-0012.

## Motivo do cancelamento do H-0011

O H-0011 foi superado pela correção arquitetural formalizada na ADR-0010. O
handoff antigo tratava a posição do dashboard e o arranjo `lado_a_lado` a partir
de uma direção anterior, enquanto a ADR-0010 consolidou que a composição visual
pertence à estrutura declarada no `corpo` da tela.

Por isso, o H-0011 não deve servir de base para implementação. Ele permanece no
repositório apenas como registro histórico do bloqueio e da mudança de direção.

## Motivo da remoção do H-0011A

O H-0011A concentrava escopo demais para um único ciclo:

- grupo estrutural;
- loader;
- modelo;
- renderer;
- demo;
- migração do `orquestrador.json`;
- preservação do fluxo H-0010A;
- compatibilidade de lista plana;
- preparação para próximos layouts.

A decisão atual é fragmentar a implementação em ciclos numerados menores,
começando por H-0012. O H-0011A não deve permanecer como handoff ativo porque a
sequência futura não usará letras.

## Fora de escopo deste ajuste

- Não implementar código.
- Não alterar JSON de produção.
- Não criar H-0012.
- Não criar ADR nova.
- Não alterar contratos.
- Não renumerar histórico já commitado.
- Não reescrever H-0010A.

## Pendências documentais registradas

Foram encontradas referências normativas ou quase normativas à sequência
H-0011A-D em ADR e contratos, incluindo ADR-0010 e contratos de composição/JSON.
Este ajuste não altera arquitetura, ADRs ou contratos; portanto essas
referências ficam registradas como pendência para limpeza documental futura.

Também permanecem relatórios históricos de auditoria mencionando H-0011 e
H-0011A. Essas ocorrências são rastreabilidade, não handoffs ativos, e não foram
reescritas neste ciclo.

## Verificações realizadas

- `git status --short`: antes do ajuste havia arquivos não rastreados
  relacionados ao H-0011A.
- `find . -path '*H-0011*' -o -path '*0011*'`: confirmou os caminhos reais sob
  `docs/`.
- `grep -R "H-0011A\|H-0011 " -n docs scripts/docs 2>/dev/null || true`:
  identificou referências históricas, contratuais e de ADR à sequência antiga.
- `git ls-files ...`: confirmou que o H-0011 é rastreado e o H-0011A estava não
  rastreado.

## Resultado

- `docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md`
  marcado como `CANCELADO_NAO_IMPLEMENTAR`.
- `docs/handoff/H-0011A-layout-hierarquico-vertical-compativel.md` removido como
  handoff ativo não rastreado.
- `docs/relatorios/RELATORIO_REPLANEJAMENTO_H-0011_H-0011A.md` criado.
- Nenhum código alterado.
- Nenhum JSON de produção alterado.
- Commit gerado: este relatório acompanha o commit documental do
  replanejamento.
