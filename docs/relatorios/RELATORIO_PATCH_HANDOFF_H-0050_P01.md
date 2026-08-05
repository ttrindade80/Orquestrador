# Relatório de patch do handoff — H-0050 P01

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0050.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_HANDOFF_H-0050.md
achados_tratados:
  - QA-H0050-03
  - QA-H0050-04
  - QA-H0050-09
decisoes_aplicadas:
  - D-DRY-10
  - D-DRY-11
```

## Trechos corrigidos

A ordem de autoridade agora nomeia D-DRY-10, D-DRY-11 e
`docs/contratos/contrato_registro_acoes.md`. Foram removidos os bloqueios por
falta de política de propriedades adicionais, categoria, modos aceitos ou
registro autoritativo. Permanecem somente contradição documental real, decisão
material nova e insuficiência da leitura focal como condições de bloqueio.

`controle_execucao` passou a ser requisito explícito de objeto fechado: contém
exatamente `modo_inicial`, aceita apenas `executar` e `dry_run`, não tem default
nem estado vivo e rejeita propriedade interna adicional.

## Registro, captura e universalidade

O manifesto escolhe `tela/registro_acoes.py` e
`tela/teste_registro_acoes.py`, pois as buscas autorizadas não identificaram
proprietário vigente mais adequado. O registro é reutilizável e autoritativo:
resolve referências vigentes, exige categoria fechada e, para processo, modos
efetivamente implementados. A validação de tela adotante falha fechada antes de
executar; navegação e visualização não exigem ambos os modos. A ação sintética
H-0050 deve usar o mesmo registro, sem metadado JSON nem exceção por ID.

A antiga formulação pública rígida foi substituída por uma dataclass privada,
imutável e reversível, com lote reconciliado e modo capturado. Ela não muda a
identidade do lote, não é protocolo público e o executor demonstrativo recebe
apenas essa captura e a fixture.

## Manifesto, testes e preservações

O manifesto futuro inclui os proprietários de validação, registro, estado,
barra, captura real em `demo/demo.py`, executor, demonstração e testes. A
fachada `tela/renderizador.py`, `tela/resultado_execucao.py`,
`tela/navegacao.py` e H-0044 permanecem preservados. O roteiro manual usa
“texto apresentado com a cor resolvida por cor_alerta”; nenhuma cor concreta é
regra normativa.

Foram acrescentados casos para categorias, subconjuntos de modos, ausência e
desconhecimento, elegibilidade, anti-inferência, resolução da ação
demonstrativa, ausência de metadados JSON, captura privada e regressão H-0044.

```yaml
verificacoes:
  - objeto_fechado_nomeado
  - compatibilidade_ausente_do_JSON
  - registro_autoritativo_e_falha_fechada_nomeados
  - Insert_atribuido_a_demo/demo.py
  - requisicao_privada_e_reversivel_nomeada
  - H-0044_preservado
bloqueios: []
status: HANDOFF_PATCHED_AWAITING_QA
proxima_acao: QA_HANDOFF
```
