# Relatório de Auditoria — H-0011 Renderização lado_a_lado e barra mínima do Orquestrador

## Status final

ARCHITECTURE_REVIEW_REQUIRED

## Escopo auditado

Foi auditado o handoff `docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md` contra os contratos e ADRs aplicáveis, o estado atual dos JSONs de tela, o código existente em `tela/` e os testes atuais.

O ciclo pretendido é coeso: renderização visual de `corpo.arranjo = "lado_a_lado"` para `console`/`lancador` e redução da `barra_de_menus` da tela raiz para `[Esc] Sair` e `[?] Ajuda`.

## Estado inicial do working tree

Comandos obrigatórios iniciais:

```text
git status --short
?? docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md

git log --oneline -3
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
ec0a59e docs: fecha contratos incrementais de tela json
```

Não há modificação pendente em `config/telas/orquestrador.json`. O único item pendente observado antes dos testes foi o próprio handoff H-0011 não rastreado. Não há impedimento operacional de working tree para auditar ou iniciar implementação, desde que o executor saiba que o handoff ainda não está versionado.

## Arquivos lidos

```text
docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_lancador.md
docs/adr/ADR-0008-modelo-configuracao-por-tela.md
docs/adr/ADR-0009-caminho-formato-jsons-tela.md
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/relatorios/RELATORIO_QA_H-0010A_FLUXO_MINIMO_LANCADOR_TELA_DESTINO.md
docs/relatorios/RELATORIO_VALIDACAO_H-0010A_DECLARATIVA_STUB_B.md
config/telas/orquestrador.json
config/telas/destino_minimo.json
config/telas/stub_b.json
tela/modelo.py
tela/renderizador.py
tela/demo.py
tela/diagnostico.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
tela/teste_diagnostico.py
```

## Consultas adicionais justificadas

Nenhuma consulta adicional foi necessária além dos arquivos obrigatórios e dos comandos de auditoria solicitados.

## Comandos executados

```bash
git status --short
git log --oneline -3
git diff --stat
git diff --name-only
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
python -m json.tool config/telas/stub_b.json >/dev/null && echo "stub_b.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
python tela/diagnostico.py
printf 'b\nd\n\x1b\n\x1b\n' | python tela/demo.py
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Resultados resumidos:

```text
JSONs: orquestrador.json OK; destino_minimo.json OK; stub_b.json OK
teste_loader.py: exit 0; 42 verificações, 0 falhas
teste_modelo.py: exit 0; 34 verificações, 0 falhas
teste_renderizador.py: exit 0; 102 verificações, 0 falhas
teste_diagnostico.py: exit 0; 28 verificações, 0 falhas
teste_demo.py: exit 0; 95 verificações, 0 falhas
tela/diagnostico.py: exit 0
demo pipe b,d,Esc,Esc: exit 0; 4 renders observados
find __pycache__: vazio
find *.pyc: vazio
git diff --stat: vazio
git diff --name-only: vazio
git status --short final: ?? docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
```

## Aderência ao contrato de processo

O handoff tem escopo explícito, critérios de aceite verificáveis e lista de arquivos permitidos/proibidos. Aderência geral é boa.

Há, porém, uma contradição com contrato ativo de composição no algoritmo autorizado para `lado_a_lado`. Pelo contrato de processo, artefato inferior não pode contradizer contrato superior; por isso o status final não pode ser aprovado.

## Aderência ao contrato_tela_json

O handoff respeita o modelo por tela: `config/telas/orquestrador.json` é a fonte da composição concreta, dos chips e dos elementos de corpo. Não propõe carregar lógica procedural arbitrária no JSON nem criar índice central/registry neste ciclo.

## Aderência ao contrato_composicao_corpo

Parcial. O handoff acerta ao usar `modelo.corpo.arranjo`, ao manter `dashboard` fora do eixo automático de `arranjo`, ao preservar `loader.py` e `modelo.py`, e ao proibir hardcoding por id de tela.

Falha bloqueante: a seção F-2c manda dividir `total_w` em duas colunas justapostas sem espaço entre caixas, enquanto `contrato_composicao_corpo.md` seção 5.6 determina que, em modo lado a lado, o espaço horizontal é distribuído em 3 vãos iguais: borda↔coluna_1, coluna_1↔coluna_2, coluna_2↔borda. O algoritmo do handoff autoriza layout sem esses vãos.

## Aderência ao contrato_barra_de_menus

Aderente. O handoff afirma que a lista concreta de chips vem do `tela.json`, que o renderer não deve inventar chips ausentes, não deve consultar contrato para preencher chips e não deve hardcodar lista de chips. A redução da barra do Orquestrador para `[Esc] Sair` e `[?] Ajuda` está justificada pelo modelo declarativo.

## Aderência ao contrato_lancador

Aderente no escopo auditado. O handoff preserva `lancador` como elemento de corpo, não o confunde com `barra_de_menus`, não conecta `stub_b`, não adiciona novos itens e mantém os itens existentes vindos do JSON.

## Aderência às ADR-0008 e ADR-0009

Aderente no modelo por tela e no caminho `config/telas/<id>.json`. O handoff usa `config/telas/orquestrador.json` como fonte da instância concreta e não propõe migrar artefatos globais nem criar registry central.

## Verificação da granularidade

O ciclo é coeso: uma mudança visual no renderer (`lado_a_lado`) e uma atualização declarativa mínima da barra da tela raiz. Não fragmenta em micro-handoffs e não mistura console real, paginação, seleção, registry de ações ou registry completo de telas.

## Verificação do algoritmo lado_a_lado

O handoff define claramente o acesso a `modelo.corpo.arranjo`, a separação de `console`/`lancador` versus `dashboard`, a preservação da ordem do JSON, a largura total/fallback, o padding por altura, a concatenação de linhas e a preservação de bordas curva/reta.

O algoritmo, entretanto, não é contratualmente seguro por dois motivos:

1. Autoriza `col_w = total_w // 2` e concatenação direta sem vão entre colunas, contrariando a distribuição em 3 vãos iguais prevista no contrato de composição.
2. Autoriza empilhar 3+ elementos `console`/`lancador` mesmo com `arranjo = "lado_a_lado"`, o que cria fallback por quantidade de elementos. O contrato fala em `lado_a_lado` para 2+ elementos `console`/`lancador` e o próprio handoff proíbe fallback que ignore `lado_a_lado`.

## Verificação do dashboard fora do eixo de arranjo

Aderente. O handoff preserva `dashboard` fora do bloco horizontal de `console`/`lancador`, renderizando-o verticalmente após o bloco lado a lado. Não manda transformar `dashboard` em coluna horizontal nem implementar `posicao_dashboard = "horizontal"`.

## Verificação da barra mínima do Orquestrador

Aderente. O handoff permite atualizar `config/telas/orquestrador.json` para declarar apenas `[Esc] Sair` e `[?] Ajuda`, com justificativa correta: chips concretos pertencem à tela, o contrato define semântica/invariantes e o renderer não inventa chips ausentes.

## Verificação de stub_b

Aderente. O handoff manda não conectar `stub_b` ao Orquestrador neste ciclo e tratá-lo como artefato disponível de validação declarativa. Também proíbe alterar `config/telas/stub_b.json`.

## Verificação de arquivos permitidos/proibidos

A lista de arquivos permitidos é suficiente e restrita:

```text
config/telas/orquestrador.json
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_diagnostico.py
tela/teste_demo.py
docs/relatorios/IMP-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
```

`tela/demo.py` é corretamente proibido e a justificativa é adequada. Contratos, ADRs, NOMENCLATURA, índice, backlog, issues, JSONs transicionais, `destino_minimo`, `stub_b`, `loader.py`, `modelo.py`, `diagnostico.py` e `__init__.py` estão proibidos.

## Verificação de ausência de hardcoding

O handoff proíbe hardcodar chips, itens, ids de elementos, id `orquestrador`, fallback que ignore `lado_a_lado` e chips ausentes.

Ressalva operacional: o comando sugerido para hardcoding procura `lado_a_lado|sobreposto` e ao mesmo tempo exige que o renderer compare `modelo.corpo.arranjo == "lado_a_lado"`. Isso pode gerar falso positivo se interpretado literalmente como "nenhuma ocorrência de `lado_a_lado` em código executável". A intenção correta deve ser proibir arranjo hardcoded por id de tela, não a constante de valor necessária para comparar o campo declarativo.

## Verificação de critérios de aceite

Os critérios são amplos e majoritariamente objetivos: JSON válido, preservação de `arranjo`, render horizontal real, dashboard fora do bloco, barra mínima, ausência de hardcoding, preservação do fluxo H-0010A, testes atualizados, comandos obrigatórios, sem cache e sem commit.

Dois critérios/trechos precisam revisão antes da implementação:

- O critério visual de `lado_a_lado` deve ser ajustado para obedecer aos 3 vãos iguais do contrato, ou o contrato precisa ser alterado antes.
- A verificação por `grep` deve distinguir ocorrência legítima da string de arranjo de hardcoding por tela/elemento.

## Achados bloqueantes

1. **Algoritmo `lado_a_lado` contradiz o contrato de composição.**  
   O handoff autoriza duas caixas justapostas com `col_w = total_w // 2`, sem vão entre colunas. O contrato de composição seção 5.6 exige distribuição do espaço horizontal em 3 vãos iguais. Isso é contradição entre handoff e contrato superior.

2. **Fallback para 3+ elementos `console`/`lancador` contradiz a regra declarativa.**  
   O handoff permite empilhar 3+ elementos mesmo quando `arranjo = "lado_a_lado"`. Isso autoriza ignorar o arranjo declarado por quantidade de elementos, apesar de o contrato aplicar o arranjo a 2+ elementos e o próprio handoff proibir fallback que ignore `lado_a_lado`.

## Achados não bloqueantes

1. O working tree tem `docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md` como arquivo não rastreado. Não há alteração pendente em `config/telas/orquestrador.json` e não há diff tracked.

2. A verificação de ausência de hardcoding por `grep` inclui `lado_a_lado`/`sobreposto`, mas o renderer precisará comparar o valor declarativo `lado_a_lado`. Recomenda-se reformular a checagem para proibir ids específicos e decisões por tela, não a presença inevitável da constante de comparação.

## Recomendações

- Revisar o algoritmo visual de `lado_a_lado` no handoff para cumprir a distribuição em 3 vãos iguais do `contrato_composicao_corpo.md`, ou abrir revisão contratual antes da implementação.
- Remover ou redefinir a autorização de empilhar 3+ elementos com `arranjo = "lado_a_lado"`.
- Ajustar o comando de inspeção de hardcoding para aceitar a comparação declarativa com `"lado_a_lado"` e focar em ids específicos (`orquestrador`, `console_principal`, `lancador_principal`, `dashboard_info`) e chips/textos hardcoded.
- Versionar o handoff H-0011 antes de entregá-lo ao executor, se esse for o fluxo desejado do processo.

## Conclusão

O H-0011 está bem delimitado, preserva a arquitetura declarativa na maior parte do texto e não apresenta bloqueio operacional de working tree. Porém, o algoritmo de `lado_a_lado` autorizado pelo handoff contradiz regra contratual explícita de distribuição horizontal e ainda permite fallback empilhado para 3+ elementos. Por isso, o handoff não deve ser enviado ao GLM/OpenCode sem revisão arquitetural/documental.
