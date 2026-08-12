# ADR-0045 — Resize responsivo das formações do pop-up de marcação

## Contexto e problema

O `ITEM-0028` trata exclusivamente da geometria responsiva da lista de
conteúdo `tipo: marcacao` do pop-up. O redimensionamento deve permitir que a
mesma instância altere sua formação física antes de aplicar o `quadro mínimo
de terminal pequeno`, sem alterar o conteúdo recebido, o estado vivo ou a
semântica da interação.

O contrato vigente de `pop-up` já define a sequência física
`coluna → matriz → linha`, o preenchimento vertical da matriz, a ausência de
placeholders e a preservação do estado lógico. Sua lacuna é o critério de
escolha da matriz durante o resize: atualmente determina o menor número de
colunas capaz de acomodar todos os itens. Esta ADR fecha o critério responsivo
do ITEM-0028 e substitui somente essa regra específica.

## Decisões

### D-ITEM0028-01 — Formação responsiva

As formações físicas continuam sendo:

```text
coluna → matriz → linha
```

O algoritmo normativo é:

1. Usar `coluna` sempre que todos os itens couberem integralmente em uma única
   coluna. Esta é a formação visualmente preferencial.
2. Se a coluna não couber e houver espaço vertical para pelo menos duas linhas
   físicas de itens, avaliar as formações válidas de `matriz`.
3. Na matriz, escolher a formação que caiba integralmente na área disponível e
   tenha o maior número de colunas fisicamente ocupadas.
4. Considerar como matriz válida somente a formação que conserve pelo menos
   duas linhas físicas. Uma formação de uma única linha não é matriz para esta
   política.
5. Preencher a matriz verticalmente por colunas, avançando da esquerda para a
   direita.
6. Não criar placeholders, células artificiais ou itens navegáveis vazios.
7. Usar `linha` somente quando houver espaço vertical para apenas uma linha
   física de itens e todos os itens couberem integralmente nessa linha.
8. Se nenhuma formação permitida couber integralmente, usar o `quadro mínimo
   de terminal pequeno` já vigente.

A formação é recalculada a cada novo par de dimensões válido, inclusive após
`SIGWINCH`. O processo é reversível: ao aumentar novamente o terminal, a mesma
instância pode retornar de `linha` para `matriz` e de `matriz` para `coluna`,
conforme os mesmos critérios.

Resize e recomposição preservam, por ID e na mesma instância, a ordem lógica,
o cursor e as marcações provisórias. A mudança de formação é exclusivamente
física.

A navegação continua toroidal por eixo conforme o contrato vigente:

- `coluna`: eixo vertical;
- `matriz`: eixos horizontal e vertical independentes;
- `linha`: eixo horizontal;
- eixo sem outro item ocupado: `SEM_MOVIMENTO`;
- células vazias não participam da navegação.

Esta decisão vale igualmente para `marcacao: exclusiva` e
`marcacao: multipla`.

### D-ITEM0028-02 — Critério objetivo de encaixe

O cálculo físico já vigente permanece como base para determinar se uma
formação cabe. Cada item ocupa exatamente uma linha física, sem wrapping e sem
truncamento.

A largura física de cada item considera integralmente:

- indicador de cursor;
- indicador de marcação;
- separação interna já vigente;
- texto integral do item.

A altura disponível para os itens é calculada depois de descontar o overhead
real do pop-up, incluindo:

- moldura;
- espaçamento superior;
- linhas físicas da instrução após wrapping;
- espaçamento entre conteúdo e chips;
- linhas físicas ocupadas pelos chips;
- espaçamento inferior.

O número de colunas usado pela política é o número de colunas efetivamente
ocupadas por itens. Colunas artificiais ou vazias não podem ser contabilizadas
para maximizar a formação.

Assim, “maior número de colunas fisicamente ocupadas” significa selecionar,
entre as matrizes válidas que caibam integralmente e conservem pelo menos duas
linhas físicas, aquela com a maior quantidade de colunas que contenham itens
reais. Não significa adicionar células vazias para aumentar a contagem.

### D-ITEM0028-03 — Vão horizontal

O vão horizontal é exatamente `2` espaços, tanto:

- entre colunas da matriz;
- entre itens da formação em linha.

Os `2` espaços integram simultaneamente o cálculo de encaixe e a
representação física.

## Estado preservado e compatibilidade

A aplicação desta ADR preserva integralmente:

- IDs estáveis dos itens;
- ordem lógica declarada;
- conteúdo recebido;
- estado vivo da instância;
- políticas `marcacao: exclusiva` e `marcacao: multipla`;
- confirmação e resultado;
- `Esc` com resultado `ABORTADO`;
- área própria de chips;
- espaçamentos declarados do pop-up;
- estilo universal;
- centralização;
- ausência de paginação;
- ausência de truncamento;
- ausência de redução silenciosa dos espaçamentos declarados.

O pop-up continua sendo uma apresentação modal e não é transformado em
`console`. Não se aplica ao pop-up o campo declarativo
`distribuicao_matricial` dos elementos funcionais.

O `quadro mínimo de terminal pequeno` continua sendo o quadro já vigente,
acionado quando nenhuma formação permitida couber integralmente. Ele não
substitui a recomposição responsiva enquanto alguma formação permitida couber,
nem altera a recuperação da mesma instância quando dimensões suficientes forem
restauradas.

## Conflito pontual e autoridade

Há um conflito específico com `docs/contratos/contrato_popup.md`: sua regra
vigente para a matriz determina o menor número de colunas capaz de acomodar
todos os itens. Para o resize responsivo do conteúdo `tipo: marcacao`, essa
regra é substituída por:

> escolher o maior número de colunas fisicamente ocupadas que forme uma matriz
> válida, conserve pelo menos duas linhas físicas e caiba integralmente na área
> disponível.

Preservam-se as demais regras contratuais de preenchimento vertical, ordem,
navegação, ausência de placeholders, preservação do estado lógico e
representação sem wrapping ou truncamento.

## Documentos a reconciliar na aplicação futura

Na futura aplicação documental desta ADR, deverão ser reconciliados, sem
alteração nesta etapa:

- `docs/contratos/contrato_popup.md`, especialmente a regra de escolha da
  matriz e a remissão ao resize e ao quadro mínimo;
- `docs/nomenclatura/35_POPUP.md`, nas descrições de geometria e das formações
  do pop-up de marcação;
- `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`, nas
  referências ao resize do pop-up e ao uso do quadro mínimo de terminal pequeno.

Essa reconciliação deverá manter a autoridade geral de redimensionamento,
`SIGWINCH`, par de dimensões válido, últimas dimensões válidas e quadro mínimo,
sem criar política universal concorrente.

## Consequências

- O resize pode alterar a representação física entre `coluna`, `matriz` e
  `linha` antes do quadro mínimo.
- Entre matrizes que caibam integralmente, a formação visualmente escolhida é
  a que ocupa mais colunas reais, desde que mantenha pelo menos duas linhas.
- A geometria passa a considerar explicitamente o vão horizontal de `2`
  espaços na matriz e na linha.
- A recomposição não altera a identidade, a ordem, o cursor, as marcações
  provisórias, o resultado ou a política de marcação da instância.
- O crescimento do terminal pode desfazer a redução física pela mesma regra,
  sem substituir a instância lógica.

## Fora de escopo

Esta ADR não decide nem altera:

- pop-up `tipo: texto`;
- paginação de pop-up;
- semântica de marcação;
- semântica de confirmação;
- contratos de resultado;
- comportamento de chips;
- ação de negócio;
- estilos;
- política universal de redimensionamento;
- `distribuicao_matricial` de elementos funcionais;
- composição do corpo.

## Critérios de aplicação

A aplicação desta ADR fica restrita ao conteúdo `tipo: marcacao` e deve:

1. aplicar a seleção normativa `coluna → matriz → linha`, com `linha` somente
   para a condição de uma única linha física e nunca como matriz de uma linha;
2. contar somente colunas fisicamente ocupadas por itens reais;
3. usar o cálculo físico vigente, incluindo o overhead real, a largura integral
   dos itens e o vão de exatamente `2` espaços tanto no encaixe quanto na
   representação;
4. recalcular a formação para cada par de dimensões válido, inclusive após
   `SIGWINCH`, preservando o estado lógico por ID;
5. retornar pela mesma regra quando o terminal crescer;
6. usar o quadro mínimo de terminal pequeno se nenhuma formação permitida
   couber integralmente;
7. manter as políticas `marcacao: exclusiva` e `marcacao: multipla`, a
   navegação vigente e todas as compatibilidades registradas nesta ADR;
8. não introduzir placeholders, truncamento, paginação, redução silenciosa de
   espaçamentos, comportamento de `console` ou uso de
  `distribuicao_matricial`.
