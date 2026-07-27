---
name: IMP-NNNN-descricao
description: "[preencher] Resultado factual da execução"
metadata:
  type: relatorio_implementacao
  tipo_execucao: IMPLEMENTACAO | PATCH_IMPLEMENTACAO
  status: IMPLEMENTED
  handoff_origem: H-NNNN
  data: YYYY-MM-DD
rastreabilidade:
  contrato_alvo: null
  adr_relacionadas: []
  issues_relacionadas: []
  bugs_abertos: []
  autorizacoes_operacionais: []
  cadeia_raiz: null
  predecessor_imediato: null
  achados_tratados: []
---

# IMP-NNNN — Relatório de implementação

> Relatório sucinto, factual, assertivo e autocontido. Omitir seções e campos vazios.
>
> Teto normal: 600 palavras. Até 900 somente quando necessário para preservar conteúdo material não resumível.
>
> Este relatório não aprova formalmente a implementação e não sobrescreve relatório de execução anterior.

## 1. Identificação e status

```yaml
handoff: H-NNNN — [título]
tipo_execucao: IMPLEMENTACAO | PATCH_IMPLEMENTACAO
status_literal: IMPLEMENTED | BLOCKED | ARCHITECTURE_REVIEW_REQUIRED
status_normalizado:
```

## 2. Delta material

- [Capacidade implementada, correção aplicada ou fato material]

Não descreva o passo a passo do agente. Não copie código, diff completo, handoff, logs extensos ou metodologia.

### Cadeia de patch

[Omitir na implementação inicial.]

```yaml
raiz:
predecessor_imediato:
achados_tratados: []
achados_resolvidos: []
achados_pendentes: []
novos_achados: []
```

## 3. Artefatos criados ou alterados

```yaml
diretorios_criados: []
arquivos_criados:
  - caminho:
    finalidade:
arquivos_alterados:
  - caminho:
    delta:
arquivos_removidos:
  - caminho:
    motivo_autorizado:
```

Não enumere itens autorizados que permaneceram inalterados, salvo quando isso for material.

## 4. Dados, temporários e saídas

[Omitir quando não aplicável.]

```yaml
entradas_reais: []
fixtures: []
configuracoes: []
temporarios_operacionais: []
caches: []
saidas_geradas: []
politica_de_sobrescrita_observada:
limpeza_realizada:
```

Nenhuma evidência material pode permanecer somente em `/tmp`.

## 5. Verificações e evidência

```yaml
verificacoes_executadas:
  - comando_ou_metodo:
    resultado_compacto:
    prova_semantica:
criterios_de_aceite:
  - id:
    evidencia:
    resultado: OK | FALHA | NAO_VERIFICADO
```

Registre valores esperados independentes da saída observada. Código de saída zero, isoladamente, não comprova a entrega.

## 6. Demonstração operacional

[Omitir quando não exigida.]

```yaml
cwd: "."
comando:
entrada_ou_fixture:
configuracao:
saida_observada:
comparacao_com_esperado:
prova_semantica:
codigo_de_saida:
```

## 7. Evidências separadas

[Omitir quando toda a evidência material estiver contida neste relatório.]

```yaml
evidencias_separadas:
  - arquivo: docs/relatorios/<arquivo>
    finalidade:
    leitura_necessaria_para: []
```

Use arquivo separado somente quando o conteúdo não couber de forma sucinta, precisar preservar formato próprio ou for reutilizado diretamente por execução futura.

## 8. Estado Git observado

Registre somente o resumo factual necessário:

```yaml
branch:
HEAD:
staged:
unstaged:
nao_rastreados:
divergencias_materiais: []
```

Não copie a saída Git completa quando o estado estiver conforme.

## 9. Bloqueios, ressalvas e observações para QA

```yaml
bloqueios: []
ressalvas: []
observacoes_para_qa: []
validacao_manual:
  executor_exclusivo_quando_TTY: USUARIO
  necessaria:
  executada:
  resultado:
  itens_pendentes: []
```
