---
name: relatorio-qa-aplicacao-adr-0047
description: QA da aplicacao documental da ADR-0047 (formatacao dos filhos de dois_niveis_por_foco)
metadata:
  type: relatorio
  scope: orquestrador
  etapa: QA_APLICACAO_ADR
  status: ADR_APPLICATION_APPROVED
---

# Relatório — QA da Aplicação da ADR-0047

## 1. Identificação

- etapa: `QA_APLICACAO_ADR`
- status: `ADR_APPLICATION_APPROVED`
- ADR auditada: `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
- aplicação auditada: `docs/relatorios/RELATORIO_APLICACAO_ADR-0047.md` (`ADR_APPLIED`)

## 2. Verificações materiais realizadas

- `ADR-0047` está `aceita`, com QA `ADR_APPROVED` (QA-ADR-0047-001 resolvido
  em §4.13) e `QA_APLICACAO_ADR` corretamente registrado como pendente até
  esta auditoria.
- `INDICE_ADR.md` registra a ADR-0047 de forma coerente com o padrão das
  demais linhas, incluindo status transportado e data.
- `contrato_tela_json.md` §36 fecha o schema (`formato.dois_niveis_por_foco
  .filho`) exclusivamente na camada de configuração da tela, com
  localização, cardinalidade única por tela, nomes literais, tipos e a
  relação condicional `texto`/`tabela` fechados; nenhuma configuração
  repetida por filho.
- `contrato_console.md` §25 propaga comportamento sem introduzir decisão
  nova; todas as remissões internas (§19.4, §19.6, §21.3, §21.7, §21.8,
  §22.4, §22.5, §22.6, §22.16) foram conferidas e existem com o conteúdo
  alegado.
- `contrato_json_console.md` §15 preserva o documento externo como
  conteúdo/dados; confirmado que os blocos reservados `espacamento`/
  `alinhamento` (§12.2) e o mecanismo `conteudo` (§12.3) permanecem
  exclusivos do documento externo e não foram reaproveitados para o schema
  desta ADR. Campos de `tabela.colunas[].campo` permanecem dados; a
  exibição em coluna permanece decisão da tela.
- Módulo `44` recebeu somente terminologia de apresentação; módulo `32`
  recebeu somente "unidade inteira do filho deslocada", delegando
  explicitamente tabulação/apresentação ao módulo `44`, sem absorção
  indevida.
- Delta terminológico do relatório (6 termos, 3 distinções, 1 fronteira)
  corresponde integralmente às alterações reais nos dois módulos.
- Nenhuma alteração em `config/**`; nenhum ITEM, handoff, campo de conteúdo
  novo ou política de navegação nova foi inventado.
- O relatório de aplicação é factualmente compatível com o diff real e não
  omite alteração material.

## 3. Achados

Nenhum achado material.
\n