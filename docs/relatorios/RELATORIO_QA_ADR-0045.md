# Relatório QA — ADR-0045

status: ADR_APPROVED

## Conclusão

A ADR-0045 está conforme às decisões fechadas e às autoridades documentais
autorizadas. Não há achado material.

## Base focal da aprovação

A ADR restringe explicitamente a capacidade ao conteúdo `tipo: marcacao`,
mantém a preferência `coluna → matriz → linha` e exige pelo menos duas linhas
para uma matriz. A seleção da matriz passa expressamente a maximizar as
colunas fisicamente ocupadas por itens reais, sem placeholders ou colunas
artificiais, substituindo de modo explícito a regra vigente do menor número de
colunas.

Também estão registrados: o uso de `linha` somente para uma única linha física
com todos os itens cabendo; o fallback ao `quadro mínimo de terminal pequeno`
após o esgotamento das formações; recomposição para cada par de dimensões
válido, inclusive após `SIGWINCH`, com retorno reversível; preservação por ID da
ordem, cursor e marcações; vão de exatamente `2` espaços no cálculo e na
representação; e manutenção das políticas `marcacao: exclusiva` e
`marcacao: multipla`.

As fronteiras negativas também estão explícitas: não reabre `tipo: texto`,
paginação, estilo, composição, ação de negócio ou política universal de
resize; preserva chips, centralização, espaçamentos, resultados e estados
`CONFIRMADO`/`ABORTADO`; e não confunde a matriz interna com
`distribuicao_matricial` de elementos funcionais.
