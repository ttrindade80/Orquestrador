# RELATORIO_QA_PATCH_IMPLEMENTACAO H-0072 P01

```yaml
etapa: QA_POS_PATCH
objeto: H-0072
patch_implementacao: P01
status: I1_IMPLEMENTATION_APPROVED
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P01.md
achados_materiais: nenhum
```

## Auditoria

O delta causal auditado está restrito ao loader, fixture estrutural H-0072 e
dois arquivos de teste autorizados, além do relatório P01. A inspeção nominal
por Git confirmou que H-0055 e H-0063 não foram reconciliados; H-0073 e todos
os caminhos de preservação permanecem fora do delta P01. O worktree contém
deltas acumulados anteriores, portanto o diff total contra `HEAD` não foi
usado isoladamente como prova causal.

`_validar_designador_filho` mantém `tipo` obrigatório e o vocabulário fechado
exato (`decimal_composto`, `alfabetico_maiusculo`, `nenhum`), admite somente
`prefixo`/`sufixo` opcionais string e rejeita chaves desconhecidas e adornos
com `nenhum`, sempre por `TelaEstruturaInvalida`, sem fallback. V-DNF-01..11
permanecem cobertas; V-DNF-12..16 estão materializadas e passam.

O modelo transporta integralmente o dict de `filho` e
`conteudo_externo.py` repassa `designador_cfg` integral a `_texto_designador`.
O renderer preservado compõe `prefixo + base + sufixo`; não há duplicação.
Testes comprovam `A`, `A)`, prefixo isolado, `(A)`, `1.1`, `[1.1]`, `nenhum`,
ausência retrocompatível, navegação, seleção e apresentações texto/tabela. O
caso equivalente a H-0055 obtém `)` exclusivamente da configuração estrutural.

Na fixture, somente o console tabular alfabético recebeu `"("`/`")"` e
renderiza `(A)`/`(B)`; decimal sem adornos, `nenhum`, conteúdo externo e demais
semânticas foram preservados.

## Evidências executadas

- focais: **232 passed** (igual ao declarado);
- demonstração: **5 passed**, pelo fluxo catálogo → loader → modelo →
  runtime/comando → renderer → saída física, com `(A)`/`(B)`;
- suíte canônica: **1431 passed, 1 failed** (igual ao declarado).

A falha residual H-0070 permanece em
`test_filhos_sem_ordinais_cursor_e_indicadores_preservados` (`2 >= 4`). O teste
intacto chama o caminho histórico `_linhas_apresentacao_hierarquia_com_mapa`;
nenhum comportamento causal seu foi modificado pelo P01. Falha não causal.

Conclusão: patch correto, suficiente e sem regressão causal; H-0073 está
pronto para retomada.
\n