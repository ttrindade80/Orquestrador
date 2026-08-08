status: I5_MANUAL_VALIDATION_REQUIRED
handoff: H-0052
patch: P08
achado_corrigido: fixture_tabela_passiva_sem_conteudo_externo_real
teste_manual_1_de_3: APROVADO_NAO_REPETIR
teste_manual_2_de_3: APROVADO_NAO_REPETIR
teste_manual_3_de_3: PENDENTE_REEXECUCAO
proxima_acao: VALIDACAO_MANUAL_3_DE_3

## Resultado

P08 adiciona somente a associação nominal `h0052_tabela_passiva` →
`h0036_tabela_conteudo` em `demo/demo.py`, reutilizando o catálogo e o
pipeline existentes (`id_conteudo_externo_de` → `carregar_conteudo_externo` →
`construir_modelo`). A tabela canônica H-0036 não foi alterada.

O caminho real carrega o conteúdo externo H-0036 e o renderer materializa a
apresentação tabular com cabeçalho `Grupo / Campo / Valor` e linhas reais; o
placeholder `(console)` não aparece. A política permanece `tipo=tabela` e
`navegavel=false`: a tabela fica fora do foco, sem cursor, setas não alteram
estado navegável, `[✥] Navegar` não aparece e `[?] Ajuda` permanece o último
chip.

O teste exato do catálogo foi reconciliado de 9 para 10 associações, incluindo
nominalmente H-0052, sem wildcard ou enfraquecimento. Não há loader, caminho
paralelo, generalização, schema ou contrato novo.

Testes: demo 6 passed; foco H-0052 23 passed (112 deselected); navegação +
loader 135 passed; suíte integral 1060 passed; `git diff --check` passou.

Resta apenas a validação visual/TTY manual 3/3; 1/3 e 2/3 não foram repetidas
nem simuladas.
