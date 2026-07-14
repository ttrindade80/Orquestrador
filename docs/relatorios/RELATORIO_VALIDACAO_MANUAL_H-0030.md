# Relatório de validação manual — H-0030

## 1. Identificação

```yaml
projeto: orquestrador_novo
handoff: H-0030
capacidade: "catálogo de telas utilizáveis"
tipo_validacao: "validação humana em TTY real"
executor: usuario
status_final: MANUAL_VALIDATION_APPROVED
```

## 2. Estado técnico anterior

```yaml
qa_final_implementacao:
  status_literal: I5_MANUAL_VALIDATION_REQUIRED
  status_normalizado: MANUAL_VALIDATION_REQUIRED
  relatorio: docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0030_IMPLEMENTACAO.md

suite_canonica:
  resultado_total: "1796/1796"
  scripts_com_codigo_saida_zero: "6/6"

validacao_automatizada: CONCLUIDA
validacao_manual_anterior: PENDENTE
```

## 3. Execução

A validação foi realizada pelo usuário em terminal real por meio do ponto de entrada vigente:

```bash
cd "$(git rev-parse --show-toplevel)/scripts"
python tela/demo.py
```

A validação humana não foi substituída por testes automatizados, pseudo-TTY ou interpretação de executor externo.

## 4. Resultado normalizado

O campo de status apresentado inicialmente continha as duas alternativas do modelo de resposta, mas os resultados informados são inequívocos: todos os cenários foram aprovados.

```yaml
status_literal_recebido: "MANUAL_VALIDATION_APPROVED | MANUAL_VALIDATION_FAILED"
status_normalizado: MANUAL_VALIDATION_APPROVED
cenarios_aprovados: 10
cenarios_reprovados: 0
cenarios_nao_executados: 0
bloqueios: NENHUM
```

## 5. Cenários validados

### 5.1 Orquestrador

```yaml
resultado: APROVADO
observacoes:
  - "Durante o redimensionamento, deve ser avaliado futuramente se o texto de descrição do cabeçalho poderá ser dividido em duas linhas ou substituído por reticências quando houver truncamento."
  - "Os chips do lançador não se reorganizam em colunas."
  - "Deve ser feita revisão futura dos contratos para determinar se a reorganização em colunas já é obrigatória, ainda não foi implementada ou exige nova ADR."
```

As observações não reprovaram o cenário e não bloqueiam o fechamento do H-0030.

### 5.2 Console único

```yaml
cenario: h0030_console_unico
resultado: APROVADO
observacoes:
  - "Os chips da barra de menus passam de linha para colunas sem erros."
```

### 5.3 Dashboard único

```yaml
cenario: h0030_dashboard_unico
resultado: APROVADO
observacoes: []
```

### 5.4 Matriz 2×2

```yaml
cenario: h0030_matriz_2x2
resultado: APROVADO
observacoes: []
```

### 5.5 Matriz 3×2

```yaml
cenario: h0030_matriz_3x2
resultado: APROVADO
observacoes: []
```

### 5.6 Matriz 2×4

```yaml
cenario: h0030_matriz_2x4
resultado: APROVADO
observacoes: []
```

### 5.7 Destino mínimo

```yaml
cenario: destino_minimo_d
resultado: APROVADO
observacoes:
  - "Existe um espaço entre o dashboard TESTE e a barra_de_menus."
```

A observação não reprova o cenário e fica registrada para revisão futura.

### 5.8 Grupo mínimo

```yaml
cenario: grupo_minimo_g
resultado: APROVADO
observacoes:
  - "Existe um espaço entre o dashboard TESTE e a barra_de_menus."
```

A observação não reprova o cenário e fica registrada para revisão futura.

### 5.9 Redimensionamento

```yaml
resultado: APROVADO
telas_testadas:
  - orquestrador
  - h0030_console_unico
  - h0030_dashboard_unico
  - h0030_matriz_2x2
  - h0030_matriz_3x2
  - h0030_matriz_2x4
observacoes:
  - "O redimensionamento foi testado em todas as telas."
```

### 5.10 Retorno e saída por Esc

```yaml
resultado: APROVADO
observacoes:
  - "Nenhum problema observado."
```

## 6. Resumo

```yaml
aprovados: TODOS
reprovados: NENHUM
nao_executados: NENHUM
bloqueios: NENHUM
status_final: MANUAL_VALIDATION_APPROVED
proxima_categoria: PRONTO_PARA_FECHAMENTO_MANUAL
```

## 7. Observações futuras não bloqueantes

Os itens abaixo não constituem falha da implementação H-0030 e não bloqueiam seu fechamento:

1. revisar o contrato e o comportamento de truncamento da descrição do cabeçalho;
2. avaliar quebra da descrição do cabeçalho em duas linhas ou uso de reticências;
3. verificar se os chips do lançador devem reorganizar-se em colunas quando faltar espaço horizontal;
4. avaliar necessidade de ADR somente se a regra de reorganização não existir nas autoridades ativas;
5. revisar o espaço entre o dashboard `TESTE` e a `barra_de_menus` em `destino_minimo`;
6. revisar o mesmo espaço em `grupo_minimo`.

Esses itens devem ser tratados em atividades futuras próprias, após verificação contratual, sem reabrir automaticamente o H-0030.

## 8. Estado Git anterior ao registro

Antes da criação deste relatório:

```yaml
stage: vazio
commit_h0030: inexistente
ultimo_commit: "9ae4aa4 fix: corrige distribuicao com cardinalidade unitaria"
cache_fora_da_entrega:
  - scripts/tela/__pycache__/
```

## 9. Conclusão

A validação humana em TTY real do H-0030 foi concluída com aprovação integral.

As cinco telas do catálogo, os destinos anteriores, o redimensionamento, o retorno ao lançador e a saída por `Esc` foram aprovados. Não houve cenário reprovado, cenário não executado ou bloqueio.

```text
MANUAL_VALIDATION_APPROVED
```
