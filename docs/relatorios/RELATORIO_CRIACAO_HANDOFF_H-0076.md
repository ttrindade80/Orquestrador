# Relatório de criação — H-0076

## Handoff criado

Foi criado `docs/handoff/H-0076-composicao-textual-canonica-popup.md` para o
`ITEM-0027`, sob a `ADR-0049`.

## Capacidade

O handoff autoriza a criação do núcleo canônico em
`tela/renderizacao/composicao_textual.py`, sua integração exclusiva no popup,
testes unitários fortes do núcleo e regressão focal do popup e de sua
recomposição por largura.

## Arquivos futuros

Foram fixados como criáveis o módulo canônico, seu teste unitário e o relatório
de implementação; como alteráveis, `popup.py`, `tela/teste_popup.py` e
`demo/teste_demo_popup.py`. `texto_ansi.py` só pode ser alterado por
necessidade estrita de reutilização/coerência das primitivas ANSI existentes.
Os demais arquivos listados no handoff permanecem preservados.

## Testes previstos

O handoff exige `tela/teste_composicao_textual.py`, regressão de
`tela/teste_popup.py`, recomposição em `demo/teste_demo_popup.py` e o comando
focal obrigatório especificado nele.

## Fronteira com H-0077

Conteúdo externo e consumidores correlatos permanecem fora desta etapa. Não
foi criado o H-0077 nem transferido trabalho para H-0076.

## Verificações e bloqueios

Foram lidos integralmente os documentos e arquivos do manifesto fechado, além
da leitura focal autorizada de `conteudo_externo.py`. Foram criados somente os
dois artefatos autorizados. Não houve implementação, QA do handoff, stage ou
commit. Não houve bloqueio documental nem necessidade de decisão adicional do
usuário.
