# RELATORIO_PATCH_HANDOFF_H-0073_P01

## Rastreabilidade

- etapa: `PATCH_HANDOFF`
- objeto: `H-0073`
- patch: `P01`
- cadeia_raiz: `docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md`
- predecessor_imediato: `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0047_POS_P01.md`
- data: 2026-08-15

## Bloqueio removido

O `BLOCKED_DOCUMENTATION` de H-0063, registrado na criação por ausência de
dois campos semânticos separados, deixou de estar ativo. O H-0073 marca
`BLOQUEIO DOCUMENTAL RESOLVIDO`. O histórico do motivo permanece em §9.1
como contexto; §9.2 e o metadata declaram inequívoco que o bloqueio não
rege mais o escopo. H-0063 passou de `escopo_bloqueado` para
`fechado_para_implementacao`.

## Decisão preset/amostra transportada

Transportada de ADR-0047 §4.11.1 (P02) e da aplicação documental aprovada:

- `campos["preset"]` inalterado, coluna 1;
- `campos["titulo"]` integralmente inalterado;
- `campos["amostra"]` novo só na projeção, mesmo valor de
  `amostra_de_preset`, sem parsing de `titulo`;
- nenhum campo existente removido, renomeado ou redefinido;
- nenhum conteúdo visível autorizado a mudar.

Configuração estrutural fechada em
`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`:
tabulação 5..10, designador `nenhum`, `apresentacao = tabela`, colunas
`preset` e `amostra`, espaçamento 3..8. Política permanece
`dois_niveis_por_foco`.

## Escopo H-0063 agora fechado

A reconciliação de H-0063, antes pendente de decisão externa, está
autorizada neste handoff: JSON estrutural + extensão compatível da
projeção em `ControladorTelaEstilo._construir_conteudo`.

## Arquivos nominais adicionados ao escopo

Edição: o JSON estrutural de H-0063 e `tela/estilo.py`.

Novos: `tela/teste_estilo_h0073_h0063.py` e
`demo/teste_demo_h0073_h0063_reconciliado.py`.

Leitura, sem edição: `tela/renderizacao/estilo.py` (`amostra_de_preset`
reutilizável sem mudança causal).

H-0055 permanece com os arquivos já fechados na criação.

## Testes e demonstrações nominais fechados

Nenhum curinga. Testes existentes de H-0063 não são alterados. A suíte
focal lista quinze caminhos literais, inclusive H-0055, H-0063, regressão
H-0070 e regressão H-0072. Demonstração de H-0063:
`demo/teste_demo_h0073_h0063_reconciliado.py` via `demo/demo.py`.

## Tratamento da regressão H-0070

`tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
entra na regressão a executar. Assertiva não é alterada. Se a configuração
nova fizer o teste passar, registra-se resolução causal pelo H-0073; se
continuar falhando, o QA determina causalidade. Maquiagem proibida.

## H-0055 preservado no escopo

Reconciliação de
`config/telas/demo/h0055_dois_niveis_por_foco.json` com
`apresentacao = texto`, designador `alfabetico_maiusculo` e conteúdo
externo intocado permanece exatamente como na criação. Não foi reaberta
nem transformada em tabela.

## H-0062 / H-0072 preservados

`config/telas/demo/h0062_estilo.json` continua precedente histórico sem
produtor ativo, fora da reconciliação.

As fixtures
`h0072_formatacao_generica_dois_niveis_por_foco{,_conteudo}.json`
permanecem intocadas; a suíte H-0072 entra na regressão obrigatória.

## Verificações

- leitura integral do H-0073, ADR-0047, `contrato_tela_json.md`,
  `contrato_json_console.md` e do predecessor QA da aplicação;
- `rg` focal: `h0063_estilo_estrutura_navegacao_dois_niveis`,
  `ControladorTelaEstilo`, `_construir_conteudo`, `campos["preset"]`,
  `campos["titulo"]`, `amostra_de_preset`, testes `h0063` e H-0070;
- H-0063 não aparece mais como bloqueada para implementação;
- `preset` e `amostra` estão literais; `titulo` permanece preservado;
- arquivos futuros nominais; sem descoberta transferida a IMPLEMENTAR;
- `git diff --check` nos dois artefatos desta etapa.

## Bloqueios restantes

Nenhum.
\n