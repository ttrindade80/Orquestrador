# Relatório de Validação Manual — H-0073

```yaml
etapa: REGISTRAR_VALIDACAO_MANUAL
objeto: H-0073 / capacidade consumida H-0072
executor_da_validacao: USUARIO
ambiente: TTY_REAL
status: MANUAL_VALIDATION_FAILED
predecessor_imediato:
  docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0073.md
achados:
  - VM-H0073-001
proxima_acao: PATCH_IMPLEMENTACAO_H0072_P02
```

## 1. Identificação

Registro exclusivo do resultado factual da validação manual TTY feita pelo
usuário após `RELATORIO_QA_IMPLEMENTACAO_H-0073.md`. Não houve diagnóstico,
correção, alteração de configuração/testes/handoff/ADR/contratos/nomenclatura,
nem nova validação ou QA nesta etapa.

## 2. Comandos e percursos executados

- H-0055: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0055_dois_niveis_por_foco`
- H-0063: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py`, abertura da tela
  Estilo pelo caminho real via F4.

Ambas as telas concretas de H-0073 foram validadas em TTY real.

## 3. Fatos observados em H-0055

Apresentação texto. Ao redimensionar horizontalmente a tela, a tabulação entre
pai e filho permaneceu visualmente constante. Não foi observada variação do
valor efetivo entre o mínimo 5 e o máximo 10. Critério: **FALHOU**.

## 4. Fatos observados em H-0063

Apresentação tabela.

1. Espaçamento entre as duas colunas: comportamento mínimo/máximo observado
   como correto. Critério: **APROVADO**.
2. Tabulação entre nível pai e nível filho: ao redimensionar horizontalmente,
   permaneceu visualmente constante; não foi observada variação do valor
   efetivo entre mínimo 5 e máximo 10. Critério: **FALHOU**.

## 5. Critério positivo preservado

`H-0063 / espacamento_entre_colunas_3_8`: **APROVADO_NA_VALIDACAO_MANUAL**.

Esse critério não integra o achado VM-H0073-001 e não deve ser reaberto sem
evidência causal nova.

## 6. Achado VM-H0073-001

**Título:** `TABULACAO_DINAMICA_PAI_FILHO_NAO_REAGE_A_RESIZE`

Nas telas reais H-0055 e H-0063, ambas configuradas com `tabulacao` mínimo 5
e máximo 10, o usuário redimensionou horizontalmente o TTY e não observou
alteração do recuo efetivo pai→filho.

A falha é comum às duas apresentações (texto e tabela). Não deve ser
registrada como defeito específico da distância entre colunas da tabela
H-0063.

## 7. Comportamento esperado já fechado

Referência normativa transportada, sem nova regra:

- tabulação declarada define intervalo mínimo/máximo;
- o renderer escolhe o maior valor que caiba;
- enquanto 10 couber, pode permanecer 10;
- quando 10 deixar de caber, deve reduzir progressivamente até 5;
- resize deve recalcular a geometria;
- a unidade inteira do filho continua deslocada.

## 8. Limites do que foi observado

Não se afirma qual função possui o defeito, qual arquivo deve ser alterado,
que o erro está comprovadamente no renderer, que o loader está incorreto, que
a configuração está incorreta, nem que H-0073 é a camada causal. Esses pontos
pertencem ao PATCH_IMPLEMENTACAO.

## 9. Gate de fechamento

Resultado global: `MANUAL_VALIDATION_FAILED`. O fechamento de ADR-0047 /
H-0072 / H-0073 fica bloqueado até correção e revalidação.

## 10. Próxima ação

A falha foi observada nas telas concretas de H-0073, mas incide sobre a
capacidade genérica já contratada por H-0072: tabulação dinâmica 5..10 +
recálculo em resize. Próxima ação: `PATCH_IMPLEMENTACAO_H0072_P02`, para
investigação e correção focal dessa capacidade. Roteamento pelo requisito
proprietário que falhou em duas telas consumidoras; não é diagnóstico
antecipado.
\n