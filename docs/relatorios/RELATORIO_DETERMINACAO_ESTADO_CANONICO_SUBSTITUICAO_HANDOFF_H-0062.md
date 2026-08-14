# Determinação do estado canônico de substituição — H-0062

## rastreabilidade

```yaml
etapa: DETERMINAR_ESTADO_CANONICO_SUBSTITUICAO_HANDOFF
objeto: H-0062
predecessor: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0062.md
```

## resultado

```yaml
status: ESTADO_CANONICO_IDENTIFICADO
termo_canonico: substituido
significado: >-
  Handoff preservado como histórico, sem aprovação/conclusão, retirado da
  unidade ativa de continuação e substituído operacionalmente por novo handoff
  ou decomposição posterior.
autoridade_principal: docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
autoridades_complementares:
  - docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
  - docs/handoff/README.md
  - docs/contratos/contrato_processo_desenvolvimento.md
  - docs/adr/ADR-0033-separacao-backlog-historico-e-arquivo-documental.md
precedentes:
  - >-
    H-0024: metadata.status: substituido e aviso explícito de que foi
    substituído operacionalmente pelo H-0025.
  - >-
    H-0025: registra handoff_historico apontando para H-0024 e declara que o
    predecessor permanece preservado, sem alteração, renomeação ou remoção.
mecanismo_documental: >-
  No predecessor, registrar o literal status: substituido e uma declaração
  textual que nomeie o sucessor. No sucessor, registrar
  rastreabilidade.handoff_historico apontando para H-0062 e explicar a
  substituição operacional, preservando o predecessor integralmente. Não há
  campo canônico comprovado substituido_por; não criar esse campo.
arquivos_a_atualizar:
  - >-
    docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md — aplicar o
    status e a declaração nominal do sucessor, sem reescrever o conteúdo.
  - >-
    novo handoff sucessor — incluir rastreabilidade.handoff_historico para
    H-0062 e a relação de substituição.
  - >-
    docs/backlog.md ou docs/HISTORICO.md não são exigidos por esta marcação
    isolada; só mudam se houver fechamento/replanejamento do ITEM-0010 segundo
    ADR-0033.
sucessor_precisa_existir_previamente: >-
  Sim para aplicar o mecanismo completo: o sucessor precisa estar nomeado para
  o vínculo ser rastreável. O corpus não comprova marcador válido para
  sucessor desconhecido; handoff_posterior: H-0063 em H-0062 é apenas previsão,
  e o arquivo H-0063 não existe.
conflitos: []
bloqueios: []
```

## buscas_executadas

```yaml
- padrão: "supersed|substitu|suplant|obsolet|cancelad|cancelament|descontinu|invalidad|abandonad|arquivad|reparticion|decompos|handoff.*estado|estado.*handoff"
  caminho: docs/**/*.md
  finalidade: localizar candidatos terminológicos.
- padrão: "status: substituido|substituído operacionalmente|handoff_historico|sucessor"
  caminho: docs/handoff/*.md
  finalidade: confirmar precedentes concretos e o vínculo documental.
- padrão: "CANCELADO_NAO_IMPLEMENTAR|MANUAL_VALIDATION_FAILED|QA_FAILED|supersessão|SUBSTITUIDO"
  caminho: docs/handoff, docs/adr, docs/HISTORICO.md
  finalidade: separar cancelamento, falha, supersessão normativa e resultado histórico.
```

## candidatos_descartados

- `CANCELADO_NAO_IMPLEMENTAR`: H-0011 foi cancelado antes da implementação; não representa trabalho implementado que continuará em sucessor.
- `MANUAL_VALIDATION_FAILED`/`QA_FAILED`: expressam falha de validação, não retirada definitiva da unidade ativa nem preservação com sucessor.
- `SUBSTITUIDO` de `docs/HISTORICO.md`: é resultado de encerramento de item, não status operacional de handoff.
- `supersessão`: nos ADRs, descreve substituição parcial de regra ou autoridade, não o ciclo de vida de um handoff.
- `obsoleto`, `arquivado` e `descontinuado`: referem-se a documentos ou termos, sem o vínculo sucessor exigido neste caso.

O relatório de validação manual foi consultado somente como predecessor factual
da transição; seus achados não foram reavaliados.
