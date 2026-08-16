# Relatório de fechamento — ADR-0047 / H-0072 / H-0073

## Identificação e resultado

- Branch: `master`.
- HEAD pré-commit: `8668ea3`.
- ADR: ADR-0047, aceita e aplicada.
- Handoffs: H-0072 e H-0073 concluídos.
- Status final: `STAGE_PRONTO_PARA_COMMIT`.

## Capacidades concluídas

Capacidade genérica de formatação dos filhos de `dois_niveis_por_foco`, com
tabulação estrutural dinâmica 5..10, designador configurável por
`prefixo`/`sufixo`, apresentações `texto`/`tabela`, alinhamento global,
wrap, preservação da identidade lógica e correção do truncamento ANSI no
resize. Aplicação real concluída em H-0055, preservando `A)`, e em H-0063,
com tabela `preset`/`amostra`, espaçamento 3..8 e fundo de “Destaque Fundo”
restrito ao chip. A separação entre configuração estrutural e conteúdo foi
preservada.

## Aprovações finais e resíduos

- QA final: `I1_IMPLEMENTATION_APPROVED`.
- Revalidação manual final: `MANUAL_REVALIDATION_APPROVED`.
- VM-H0073-001: `RESOLVIDO`.
- VM-H0073-002: `RESOLVIDO`.
- H-0055, tabulação dinâmica: `APROVADO`.
- H-0063, tabulação dinâmica: `APROVADO`.
- H-0063, espaçamento de colunas 3..8: `PRESERVADO`.
- Achados abertos do ciclo: nenhum.
- H-0070: `FALHA_HISTORICA_NAO_CAUSAL`; permanece fora do ciclo, sem
  correção e sem alteração do teste.

## Reconciliação documental do fechamento

Marcadores finais reconciliados, sem reescrever decisões, em ADR-0047,
H-0072, H-0073, `INDICE_ADR.md` e `HISTORICO.md`. Nenhum contrato ou módulo
de nomenclatura recebeu alteração semântica neste fechamento.

## Manifesto nominal

```text
docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/nomenclatura/32_CONSOLE.md
docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md
docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
docs/HISTORICO.md
docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md
docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md
config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json
config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json
tela/carregamento/formato_dois_niveis_por_foco.py
tela/carregamento/tela_json.py
tela/modelo.py
tela/navegacao.py
tela/renderizacao/conteudo_externo.py
tela/renderizacao/console.py
tela/renderizacao/matriz_participantes.py
tela/renderizacao/texto_ansi.py
demo/demo.py
demo/teste_demo_console.py
tela/teste_formato_filho_dois_niveis_por_foco.py
demo/teste_demo_h0072_formatacao_generica.py
config/telas/demo/h0055_dois_niveis_por_foco.json
config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
tela/estilo.py
tela/teste_navegacao.py
demo/teste_demo_h0073_h0055_reconciliado.py
tela/teste_estilo_h0073_h0063.py
demo/teste_demo_h0073_h0063_reconciliado.py
docs/relatorios/RELATORIO_CRIACAO_ADR-0047.md
docs/relatorios/RELATORIO_QA_ADR-0047.md
docs/relatorios/RELATORIO_PATCH_ADR-0047_P01.md
docs/relatorios/RELATORIO_QA_ADR-0047_POS_P01.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0047.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0047.md
docs/relatorios/RELATORIO_PATCH_ADR-0047_P02.md
docs/relatorios/RELATORIO_QA_ADR-0047_POS_P02.md
docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0047_P01.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0047_POS_P01.md
docs/relatorios/RELATORIO_PATCH_ADR-0047_P03.md
docs/relatorios/RELATORIO_QA_ADR-0047_POS_P03.md
docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0047_P02.md
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0047_POS_P02.md
docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0072.md
docs/relatorios/RELATORIO_QA_HANDOFF_H-0072.md
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0072.md
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0072_P01.md
docs/relatorios/RELATORIO_QA_HANDOFF_H-0072_POS_P01.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P01.md
docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P01.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P02.md
docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P02.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P03.md
docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P03.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P04.md
docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P04.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P05.md
docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P06.md
docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P05_P06.md
docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0073.md
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0073_P01.md
docs/relatorios/RELATORIO_QA_HANDOFF_H-0073_POS_P01.md
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0073_P02.md
docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0073_P03.md
docs/relatorios/RELATORIO_QA_HANDOFF_H-0073_POS_P03.md
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0073.md
docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0073.md
docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0073.md
docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0073_POS_H0072_P04.md
docs/relatorios/RELATORIO_REVALIDACAO_MANUAL_H-0073_POS_H0072_P05_P06.md
docs/relatorios/RELATORIO_FECHAMENTO_H-0072_H-0073_ADR-0047.md
```

## Verificações Git

- `git diff --check`: aprovado.
- Stage nominal: 75 arquivos do manifesto; nenhum arquivo estranho.
- `git diff --cached --check`: aprovado.
- Comparação stage × manifesto: conjuntos idênticos (75/75).
- Delta do ciclo não staged: nenhum.
- Resíduo Git desconhecido: nenhum.
- Commit e push: não executados.

Mensagem de commit proposta:

```text
feat: formata filhos em dois niveis por foco
```
