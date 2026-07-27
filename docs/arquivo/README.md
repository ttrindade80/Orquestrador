---
name: arquivo-orquestrador
description: Governança da área de documentos históricos sem autoridade vigente
metadata:
  type: governanca_arquivo
  scope: orquestrador
---

# Arquivo documental

## Finalidade

Esta área preserva integralmente documentos que deixaram de ser
documentação ativa, mantendo-os disponíveis para rastreabilidade
histórica, sem misturá-los com a documentação vigente do Orquestrador.

## Ausência de autoridade normativa

Nenhum documento depositado em `docs/arquivo/` possui autoridade normativa
vigente. Nada aqui contido é contrato, ADR ativa, handoff aplicável ou
fonte de verdade sobre o comportamento atual do sistema.

## Proibição de orientar trabalho atual

Documentos desta área não devem orientar decisão, implementação ou
planejamento de trabalho atual. Uma pendência ou instrução aqui registrada
não é válida enquanto tal — se ainda for necessária, precisa de novo
registro ativo em `docs/backlog.md` ou de decisão documental própria.

## Proibição de carregamento por padrão

Nenhum documento desta área é lido por padrão em sessão de trabalho,
onboarding ou ordem de leitura documental do Orquestrador. A leitura só
ocorre por decisão explícita, nunca por herança de rotina de leitura.

## Leitura restrita a pesquisa histórica autorizada

A leitura de conteúdo desta área somente é permitida quando explicitamente
autorizada para fins de pesquisa histórica — reconstrução de contexto,
auditoria ou rastreabilidade — nunca como insumo padrão de trabalho.

## Preservação da estrutura de origem

Cada subárea de `docs/arquivo/` preserva a estrutura de diretórios do
local de origem do documento migrado, para manter a rastreabilidade do
caminho histórico.

## Preservação do conteúdo histórico

Fora a inclusão do aviso de documento histórico no início de cada arquivo
migrado, o conteúdo original é preservado integralmente — sem correção de
referência, atualização de comando ou modernização de terminologia.

## Proibição de depositar documentação ativa

Nenhuma documentação ativa deve ser depositada nesta área. `docs/arquivo/`
recebe exclusivamente documentos que já deixaram de ser vigentes, por
decisão documental explícita de migração.

## Índice inicial

### `build_docs/`

Migração nominal inicial autorizada pela ADR-0033 (D-HIST-08):

- `docs/arquivo/build_docs/instruction.md`
- `docs/arquivo/build_docs/prompts.md`
- `docs/arquivo/build_docs/to_do.md`
