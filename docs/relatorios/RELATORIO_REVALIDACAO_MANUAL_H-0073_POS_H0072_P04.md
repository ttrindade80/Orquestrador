# Relatório de Revalidação Manual — H-0073 (pós H-0072 P04)

```yaml
etapa: REGISTRAR_REVALIDACAO_MANUAL
objeto: H-0073 / capacidade consumida H-0072
executor_da_validacao: USUARIO
ambiente: TTY_REAL
status: MANUAL_REVALIDATION_FAILED
predecessor_imediato:
  docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P04.md
achados:
  - VM-H0073-001
  - VM-H0073-002
proxima_acao: PATCH_IMPLEMENTACAO_H0072_P05
```

## 1. Identificação

Registro exclusivo do resultado factual da revalidação manual TTY feita pelo
usuário após `RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P04.md`. A revalidação
foi focal: tabulação dinâmica pai→filho após H-0072 P03/P04, nas duas telas
reais. Não houve diagnóstico, correção, alteração de
configuração/testes/handoff/ADR/contratos/nomenclatura, execução de testes,
QA, stage nem commit nesta etapa.

## 2. Comandos e percursos executados

- H-0055: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0055_dois_niveis_por_foco`
  (tela `config/telas/demo/h0055_dois_niveis_por_foco.json`, apresentação texto);
- H-0063: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py`, abertura da tela
  Estilo pelo caminho real via F4 (apresentação tabela).

## 3. Fatos observados em H-0055

Ao diminuir/aumentar horizontalmente a largura do terminal, a tabulação entre
pai e filho permanece visualmente fixa; não ocorre a variação mínimo/máximo
esperada. `TABULACAO_DINAMICA`: **FALHOU**.

### Diretriz explícita do usuário para H-0055

A correção de H-0055 deve aplicar o mesmo comportamento de tabulação
mínimo/máximo que já está funcionando corretamente na segunda tela H-0063/F4.
Não criar nova política específica para H-0055. Não se diagnostica nesta etapa
qual função precisa ser alterada.

## 4. Fatos observados em H-0063

A tabulação entre nível pai e nível filho varia corretamente durante o
redimensionamento horizontal. `TABULACAO_DINAMICA`:
**APROVADO_NA_REVALIDACAO_MANUAL**.

## 5. Estado do achado VM-H0073-001

O achado anterior não permanece comum às duas apresentações:

```yaml
VM-H0073-001:
  H-0055: PENDENTE
  H-0063: RESOLVIDO
  estado_global: PARCIALMENTE_RESOLVIDO
```

## 6. Novo achado VM-H0073-002

**Título:** `VAZAMENTO_DE_FUNDO_ANSI_EM_RESIZE_H0063`

Na H-0063/F4, ao reduzir horizontalmente a largura do terminal, o chip
"Destaque Fundo" apresenta vazamento visual de sua cor de fundo. Conforme a
largura, a cor pode aparecer na região inferior, na superior, ou ocupar grande
parte/toda a tela. O defeito aparece durante resize horizontal.

### Limites do achado

Não se afirma: qual sequência ANSI ficou aberta; se falta reset SGR; se é
defeito de wrap ou de padding; se pertence a `tela/estilo.py`, ao renderer
genérico ou ao de tabela; se é consequência direta de P03. Registra-se somente
o sintoma visual. O diagnóstico pertence ao próximo PATCH_IMPLEMENTACAO.

O defeito não autoriza alterar nome "Destaque Fundo", cor de fundo, preset,
amostra, conteúdo ou valores de estilo: o problema é de
renderização/disposição durante resize.

## 7. Critério positivo preservado

`H0063_ESPACAMENTO_COLUNAS_3_8`: **APROVADO_NA_VALIDACAO_MANUAL** (preservado).
O vazamento de fundo NÃO reabre automaticamente mínimo 3, máximo 8 nem o
alinhamento das colunas: não há evidência manual de regressão nesses critérios.

## 8. Estado operacional

```yaml
H-0055:
  tabulacao_dinamica: FALHOU
H-0063:
  tabulacao_dinamica: APROVADO
  espacamento_colunas_3_8: PRESERVADO
  vazamento_fundo_ansi: FALHOU
achados_abertos:
  - VM-H0073-001 / somente H-0055
  - VM-H0073-002
fechamento: BLOQUEADO
```

## 9. Próxima ação

`PATCH_IMPLEMENTACAO_H0072_P05`. Motivo: os dois sintomas pertencem à
apresentação física fornecida pela capacidade de formatação dos filhos de
`dois_niveis_por_foco`. Classificação apenas de roteamento operacional; o P05
deve investigar causalidade antes de alterar código.

### Diretriz de simplicidade transportada do usuário

Para a tabulação H-0055, não inventar algoritmo novo: usar o comportamento já
comprovadamente funcional na apresentação H-0063/F4 como referência de
funcionamento do mesmo contrato mínimo/máximo.
\n