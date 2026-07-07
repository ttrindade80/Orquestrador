---
name: RELATORIO_ARQUIVAMENTO_DOC-0032_HISTORICOS_TRANSICIONAIS
description: Auditoria e classificação de artefatos históricos/transicionais pós-ADR-0008/ADR-0009
metadata:
  type: relatorio_arquivamento
  status: APROVADO_COM_RESSALVAS
  data: 2026-07-07
  escopo: DOC-0032
rastreabilidade:
  adr_relacionadas:
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  artefatos_controle:
    - docs/build_docs/to_do.md
  configs_avaliados:
    - config/layout_dado.json
    - config/layout_menu.json
    - config/layout_console.json
    - config/lancador.json
    - config/barra_de_menus.json
    - config/cabecalho.json
    - config/estilo.json
    - config/telas/orquestrador.json
---

# Relatório de Arquivamento — DOC-0032

## 1. Objetivo

A DOC-0032 executou auditoria histórico/transicional pós-ADR-0008/ADR-0009,
com identificação de artefatos ativos, transicionais e históricos.

O arquivamento físico só seria executado caso houvesse artefato
inequivocamente histórico. Qualquer item com função ativa, referência
normativa, rastreabilidade ou dúvida razoável deveria ser preservado.

Regra aplicada:

```text
Arquivar somente o inequivocamente histórico.
Manter tudo que ainda tiver função ativa, referência normativa ou dúvida razoável.
```

## 2. Status inicial

A Fase 0 estava consolidada após ADR-0008 e ADR-0009, com o seguinte status
operacional correto antes da DOC-0032:

```text
PRONTO_COM_PENDENCIA_DE_ARQUIVAMENTO_HISTORICO
```

O estado Git observado no início das verificações estava limpo:

```text
git status --short
```

sem saída.

Também foi verificado que:

- `config/telas/orquestrador.json` existia e foi validado como JSON válido;
- `config/dashboard.json` não existia;
- os JSONs existentes em `config/` estavam bem formados.

## 3. Artefatos avaliados

| Artefato                                            | Categoria avaliada    | Observação                                    |
| --------------------------------------------------- | --------------------- | --------------------------------------------- |
| `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` | ADR ativa             | Modelo de configuração por tela               |
| `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`   | ADR ativa             | Caminho/formato dos JSONs de tela             |
| `docs/contratos/contrato_tela_json.md`              | contrato ativo        | Contrato do JSON de tela                      |
| `docs/contratos/contrato_chip.md`                   | contrato ativo        | Contrato de chips                             |
| `docs/contratos/contrato_console.md`                | contrato ativo        | Contrato do console                           |
| `docs/contratos/contrato_composicao_corpo.md`       | contrato ativo        | Composição do corpo                           |
| `docs/contratos/contrato_lancador.md`               | contrato ativo        | Lançador                                      |
| `docs/contratos/contrato_barra_de_menus.md`         | contrato ativo        | Barra de menus                                |
| `config/telas/orquestrador.json`                    | tela raiz ativa/draft | JSON válido                                   |
| `config/estilo.json`                                | config global ativa   | Biblioteca global de estilo                   |
| `config/layout_dado.json`                           | obsoleto/transicional | Preservado por rastreabilidade                |
| `config/layout_menu.json`                           | obsoleto/transicional | Preservado por rastreabilidade                |
| `config/layout_console.json`                        | ativo/transicional    | Canônico atual de console, ainda reavaliável  |
| `config/lancador.json`                              | ativo/transicional    | Canônico atual de lançador, ainda reavaliável |
| `config/barra_de_menus.json`                        | ativo/transicional    | Parâmetros ainda preservados                  |
| `config/cabecalho.json`                             | ativo/transicional    | Parâmetros ainda preservados                  |

## 4. Artefatos arquivados

```text
Nenhum artefato foi arquivado nesta rodada.
```

Justificativa:

- nenhum item foi identificado como inequivocamente histórico;
- `config/layout_dado.json` e `config/layout_menu.json` são
  obsoletos/transicionais, mas ainda preservados por rastreabilidade;
- DOC-B007 permanece `bloqueado_decisao`;
- ADR-0009 afirma que JSONs transicionais não são apagados nesta etapa;
- não existe pasta histórica/arquivo já estabelecida no projeto.

## 5. Artefatos mantidos ativos

| Artefato                                            | Justificativa                                        |
| --------------------------------------------------- | ---------------------------------------------------- |
| `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` | ADR aceita e normativa                               |
| `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`   | ADR aceita e normativa                               |
| `docs/contratos/contrato_tela_json.md`              | contrato ativo do JSON por tela                      |
| `docs/contratos/contrato_chip.md`                   | contrato ativo de chips                              |
| `docs/contratos/contrato_console.md`                | contrato ativo de console                            |
| `docs/contratos/contrato_composicao_corpo.md`       | contrato ativo de composição                         |
| `docs/contratos/contrato_lancador.md`               | contrato ativo de lançador                           |
| `docs/contratos/contrato_barra_de_menus.md`         | contrato ativo de barra de menus                     |
| `config/telas/orquestrador.json`                    | tela raiz vigente em estado draft, JSON válido       |
| `config/estilo.json`                                | biblioteca global de estilo preservada pela ADR-0008 |

## 6. Artefatos mantidos transicionais

| Artefato                     | Justificativa                                                                                                                     | Condição futura para arquivamento                                 |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `config/layout_dado.json`    | obsoleto/transicional, substituído por `config/layout_console.json`, preservado por rastreabilidade da migração `dado -> console` | decisão DOC-B007 ou decisão específica de arquivo histórico       |
| `config/layout_menu.json`    | obsoleto/transicional, substituído por `config/lancador.json`, preservado por rastreabilidade da migração `menu -> lancador`      | decisão DOC-B007 ou decisão específica de arquivo histórico       |
| `config/layout_console.json` | canônico atual para console, mas ainda transicional no modelo pós-ADR-0008                                                        | decisão futura após fechamento de pendências de console/registry  |
| `config/lancador.json`       | canônico atual para lançador, mas ainda transicional no modelo pós-ADR-0008                                                       | decisão futura após migração/reavaliação da configuração por tela |
| `config/barra_de_menus.json` | ativo/transicional, ainda preserva ordem/parâmetros                                                                               | decisão futura após migração para tela_json/registry              |
| `config/cabecalho.json`      | ativo/transicional, ainda preserva parâmetros de apresentação                                                                     | decisão futura após revisão remanescente de cabeçalho/estilo      |

## 7. Referências atualizadas

```text
Nenhuma referência foi atualizada nesta etapa.
```

Justificativa:

- a DOC-0032 executou auditoria/classificação;
- não houve arquivamento;
- não houve alteração de índices, contratos ou nomenclatura;
- qualquer atualização documental de controle deve ocorrer em etapa posterior,
  após revisão deste relatório.

## 8. Referências preservadas por rastreabilidade

| Referência    | Motivo da preservação                                                    |
| ------------- | ------------------------------------------------------------------------ |
| `dado`        | nome antigo de `console`, preservado em contexto histórico/transicional  |
| `menu`        | nome antigo de `lancador`, preservado em contexto histórico/transicional |
| `Info`        | nome antigo/draft de instância de `dashboard`, não arquivo global        |
| `layout_dado` | arquivo obsoleto/transicional preservado por rastreabilidade             |
| `layout_menu` | arquivo obsoleto/transicional preservado por rastreabilidade             |

Essas referências antigas não foram classificadas como erro ativo quando
aparecem explicitamente como antigas, obsoletas, transicionais, legadas ou de
rastreabilidade.

## 9. Comandos/verificações executados

Com base nos levantamentos anteriores da DOC-0032, foram executadas as seguintes
verificações:

- `git status --short`;
- `find config docs -maxdepth 4 -type f | sort`;
- buscas por termos históricos/transicionais;
- validação dos JSONs com `python -m json.tool`;
- validação específica de `config/telas/orquestrador.json`;
- verificação de ausência de `config/dashboard.json`;
- verificação de versionamento de `config/layout_dado.json` e
  `config/layout_menu.json`.

Resultados essenciais:

- estado Git limpo antes da escrita do relatório;
- todos os JSONs existentes em `config/` estavam válidos;
- `config/telas/orquestrador.json` válido;
- `config/dashboard.json` ausente;
- `config/layout_dado.json` e `config/layout_menu.json` versionados e
  transicionais.

## 10. Resultado final

```text
APROVADO_COM_RESSALVAS
```

Justificativa:

- a auditoria foi concluída;
- nenhum artefato foi considerado inequivocamente histórico;
- nenhum arquivamento foi executado;
- a preservação dos transicionais não viola ADR/contrato vigente;
- DOC-B007 permanece como decisão operacional futura;
- a Fase 0 deve ser considerada auditada quanto ao arquivamento
  histórico/transicional, mas sem limpeza física nesta rodada.

## 11. Ressalvas

1. DOC-B007 permanece `bloqueado_decisao`.
2. `config/layout_dado.json` e `config/layout_menu.json` continuam na árvore
   ativa por rastreabilidade.
3. JSONs ativos/transicionais serão reavaliados após pendências de `tela_json`,
   console, registry, cabeçalho/estilo.
4. Nenhuma pasta de histórico/arquivo foi criada.
5. Nenhuma movimentação de arquivo foi feita.

## 12. Próxima ação recomendada

- Revisar este relatório.
- Se aprovado, em etapa posterior atualizar `docs/build_docs/to_do.md` para
  registrar a conclusão da DOC-0032.
- Não iniciar Fase 1 antes do commit documental final da Fase 0.
- Qualquer arquivamento físico futuro deve depender de decisão explícita de
  DOC-B007 ou item sucessor.
