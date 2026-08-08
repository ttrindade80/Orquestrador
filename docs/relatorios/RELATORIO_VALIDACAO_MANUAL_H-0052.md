status: VALIDACAO_MANUAL_APROVADA
handoff: H-0052
executor: USUARIO
teste_1_de_3: APROVADO
teste_2_de_3: APROVADO
teste_3_de_3: APROVADO
resultado_global: APROVADO
proxima_acao: FECHAMENTO_H-0052

# Relatório de validação manual — H-0052

## Teste 1 de 3 — comportamento legado

Fixture: `config/telas/demo/h0045_validacao_nova_pagina.json`

Resultado: `APROVADO`.

Foi confirmado, em terminal grande e pequeno, que cada item começa em uma
nova página e que um item ocupa múltiplas páginas somente quando não cabe em
uma única página. O comportamento legado exigido para H-0052 permaneceu
funcional.

Foi observado, como achado externo ao aceite, que o cursor pode não reaparecer
antes do item ao ampliar ou maximizar o terminal estando em uma página de
continuação de um item multipágina que passa a caber em uma página. O achado
foi diagnosticado como `DEFEITO_PREEXISTENTE`, não é regressão de H-0052 e não
reprova este teste.

## Teste 2 de 3 — `nivel_unico` explícito

Fixture: `config/telas/demo/h0052_nivel_unico_explicito.json`

Resultado final: `APROVADO`.

Após os patches P01–P06, foram confirmados cinco itens navegáveis reais, a
presença de `[✥] Navegar`, a navegação horizontal e vertical, e os
comportamentos toroidais horizontal e vertical. Células matriciais vazias não
recebem cursor. A distribuição se recompõe ao redimensionar o terminal,
inclusive entre uma única linha e uma única coluna; em terminal estreito, os
cinco itens puderam formar uma coluna. O cursor acompanhou o mesmo item e a
navegação permaneceu funcional após as recomposições. A barra final respeitou
a ordem `[Esc] Sair  [✥] Navegar  [?] Ajuda`, com `[?] Ajuda` como último chip.

## Teste 3 de 3 — `tabela` passiva

Fixture: `config/telas/demo/h0052_tabela_passiva.json`

Resultado final: `APROVADO`.

A primeira tentativa foi insuficiente para demonstração por exibir somente
`(console)`. Após o patch P07 identificar o bloqueio e o patch P08 reutilizar a
tabela canônica existente, a validação foi repetida e aprovada. Foi confirmada
uma tabela visual real com o cabeçalho `Grupo / Campo / Valor` e linhas reais
de dados; `(console)` não permaneceu como substituto. A tabela permaneceu
passiva: não recebeu foco, não apresentou cursor de navegação e as setas não
navegaram por linhas ou células. `[✥] Navegar` não apareceu, os chips
pertinentes foram mantidos e `[?] Ajuda` permaneceu como último chip.

## Resultado consolidado

Os três testes manuais foram aprovados. O defeito de cursor observado no teste
1/3 permanece registrado somente como `DEFEITO_PREEXISTENTE`, fora do aceite de
H-0052.
