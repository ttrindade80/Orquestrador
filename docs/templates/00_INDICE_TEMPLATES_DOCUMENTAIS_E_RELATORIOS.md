# Índice de templates documentais e de relatórios — Orquestrador

> Use um único template por artefato ou relatório. O gerente resolve o caminho, o nome canônico e o template antes de gerar o prompt.

## Artefatos documentais

| Template | Uso |
|---|---|
| `TEMPLATE_ADR.md` | decisão arquitetural já fechada |
| `TEMPLATE_BUG.md` | registro de defeito reproduzível |
| `TEMPLATE_HANDOFF_IMPLEMENTACAO.md` | autorização de uma implementação |
| `TEMPLATE_HANDOFF_QA.md` | autorização de um QA independente |
| `TEMPLATE_RFC.md` | proposta que ainda exige decisão |

## Relatórios de execução

| Template | Uso |
|---|---|
| `TEMPLATE_RELATORIO_CRIACAO_DOCUMENTAL.md` | criação de ADR, handoff ou outro documento normativo |
| `TEMPLATE_RELATORIO_APLICACAO_ALTERACAO.md` | aplicação de ADR ou alteração material de artefatos fora de implementação |
| `TEMPLATE_RELATORIO_IMPL.md` | implementação inicial ou patch de implementação quando o handoff exigir esse template |
| `TEMPLATE_RELATORIO_PATCH.md` | patch documental ou correção incremental de artefato |
| `TEMPLATE_RELATORIO_QA.md` | QA de ADR, aplicação, handoff, implementação ou pós-patch |
| `TEMPLATE_RELATORIO_BUSCA_LEVANTAMENTO_VERIFICACAO.md` | busca, levantamento, inventário ou verificação material |
| `TEMPLATE_RELATORIO_ANALISE_DOCUMENTAL_FINAL.md` | análise documental final antes do fechamento manual |
| `TEMPLATE_RELATORIO_BLOQUEIO.md` | execução bloqueada após produzir resultado material |
| `TEMPLATE_EVIDENCIA_MATERIAL.md` | evidência separada indispensável por formato, tamanho ou reutilização direta |

## Regras comuns

- todos os relatórios e evidências dos agentes ficam em `docs/relatorios/`;
- nenhuma evidência material permanece somente em `/tmp`;
- nova execução gera novo relatório;
- relatório anterior não é sobrescrito, salvo correção factual da própria execução por comando de terminal manual;
- omitir seções e campos vazios;
- não copiar ADR, contrato, handoff, código, diff, log ou saída extensa;
- resposta terminal mínima não integra o relatório;
- leitura de relatório anterior ocorre somente quando o gerente a autorizar nominalmente, de preferência por busca focal.

## Orçamentos normais

| Tipo | Teto |
|---|---:|
| QA aprovado sem achado | 250 palavras |
| relatório comum | 600 palavras |
| implementação ou QA com achados materiais | 900 palavras |

Excesso exige justificativa em `extensao_excepcional.motivo`.

## Regras específicas do Orquestrador

- o gerente resolve os módulos de nomenclatura por `02_INDICE_NOMENCLATURA_ORQUESTRADOR.md`;
- leitura simples de módulo é feita diretamente pelo gerente a partir do arquivo carregado pelo usuário, sem agente, relatório ou QA;
- agentes só leem módulos nominalmente autorizados no manifesto fechado;
- validação visual ou interativa em TTY real é executada exclusivamente pelo usuário;
- a suíte canônica, quando aplicável, é `PYTHONDONTWRITEBYTECODE=1 python -m pytest`.
