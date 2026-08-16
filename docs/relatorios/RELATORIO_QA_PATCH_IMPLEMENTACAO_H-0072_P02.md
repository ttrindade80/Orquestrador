# RELATÓRIO — QA_POS_PATCH H-0072 P02

```yaml
etapa: QA_POS_PATCH
objeto: H-0072
patch_implementacao: P02
achado_origem: VM-H0073-001
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P02.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: I2_IMPLEMENTATION_PATCH_REQUIRED
```

## Auditoria

`tabulacao.minimo` e `maximo` continuam validados pelo loader e transportados
integralmente pelo modelo. O caminho de renderização recebe a largura corrente
em cada chamada; não há cache de tabulação. O diagnóstico anterior é coerente
com `_cabe_tabulacao`: a condição antiga só exigia a reserva fixa mínima de 10
colunas, portanto aceitava 10 mesmo quando texto ou tabela já não cabiam.
Texto e tabela compartilham esse helper.

P02 passou a calcular, para texto, `max(10, len(texto_filho)`), e, para tabela,
as larguras globais das colunas mais o espaçamento mínimo. A busca continua
escolhendo o maior candidato no intervalo e preservando o mínimo; o algoritmo
separado de espaçamento continua escolhendo o maior valor entre 3 e 8.
Conceitualmente isso atende “maior valor que caiba”, mas a medição tabular não
é compatível com a largura física vigente.

## Achados

1. **Medição visual incompatível — H-0063.** A projeção real de H-0063 contém
   amostras ANSI, por exemplo `Destaque Texto`; P02 calcula suas larguras com
   `len()`, contando sequências SGR, enquanto o renderer usa
   `_largura_sem_ansi` para a geometria física. Na mesma estrutura, em
   `content_w=43`, P02 seleciona tabulação 9; visualmente a maior coluna é 8,
   e tabulação 10 ainda cabe com espaçamento 7. Em `content_w=39`, tabulação 10
   ainda cabe com espaçamento mínimo 3, mas P02 seleciona 5. Portanto a
   evidência declarada `10, 9, 5` não demonstra a regra física para H-0063 e o
   algoritmo P02 pode compactar tabulação prematuramente. É defeito material,
   não hipótese Unicode: ocorre nos dados reais da tela.

2. **Evidência de resize incompleta.** Os testes focais de H-0055 e H-0063
   percorrem larguras chamando diretamente
   `_linhas_dois_niveis_formatado_com_mapa`. O teste de navegação apenas
   verifica preservação do cursor em `navegacao.redimensionar`; não encadeia
   render L1, geometria G1, mudança de largura, novo render e G2. O código
   mostra que `renderizar_estado` repassa a largura novamente ao renderer e
   que SIGWINCH atualiza o estado antes de renderizar, mas os testes P02 não
   comprovam esse fluxo automatizado.

## Preservação e telas consumidoras

H-0055 preserva `A)`, conteúdo externo, unidade `ec → tg → designador →
conteúdo`, navegação e seleção; os testes exibem 10, 9, 5. H-0063 preserva
designador ausente, preset/amostra, alinhamento global, navegação, seleção,
item lógico e quebra física. O intervalo e a função de escolha de espaçamento
3..8 não foram alterados; os testes obtêm gaps 8, 3, 3. Não houve stretch,
mudança de preset/amostra ou alteração estrutural da tabela.

## Testes e escopo

- Focais obrigatórios: **158 passed**.
- H-0070 isolado: **falha histórica**, `index("→") == 2`, esperado `>= 4`;
  não causal ao P02.
- Suíte canônica: **1455 passed, 1 failed**, somente H-0070.
- Escopo nominal declarado pelo P02: `tela/renderizacao/conteudo_externo.py`,
  os três testes H-0072/H-0073 indicados e este relatório. Configurações,
  modelo, loader, contratos e documentos adicionais são deltas acumulados e
  não foram atribuídos ao P02.

Revalidação manual em TTY continua sendo gate posterior e não foi executada.
O achado visual exige patch de implementação; a evidência automatizada de
resize também deve ser completada antes da prontidão para revalidação.
\n