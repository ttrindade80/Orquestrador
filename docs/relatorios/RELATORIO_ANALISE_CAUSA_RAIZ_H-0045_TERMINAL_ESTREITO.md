tipo_execucao: ANALISE_CAUSA_RAIZ
status_literal: ANALYSIS_COMPLETED
cadeia_raiz: VM-H0045-R08-001
achados_analisados:
  - VM-H0045-R08-001

# Relatório — terminal estreito no H-0045

## Reprodução e causa

Em reprodução controlada, a tela `h0045_fluxo_execucao_paginado` tem cinco
chips: `[Esc] Sair`, `[<] Anterior`, `[>] Proxima`, `[␣] Marcar` e
`[⏎] Todos`. As larguras mínimas individuais são 10, 12, 11, 10 e 9;
cada chip usa um vão interno de 1, há 2 espaços entre chips e margem
horizontal 1 em cada lado. Em 40 colunas: `content_w=37` e largura útil 35.
Com duas linhas em `coluna_a_coluna`, o preenchimento das colunas exige 36;
`_linhas_barra` lança exatamente o `RenderizadorErro` observado.

A causa imediata é, portanto, o limite efetivo de `linhas.maximo=2`, não
perda de conteúdo. A causa estrutural é a chamada de `_linhas_barra` dentro de
`_geometria_por_console`/`geometria_console` durante
`_reconciliar_paginacao_apos_resize`, antes do `try` que protege apenas o
render do corpo. `_resolver_conteudo` captura a exceção na renderização final,
mas `main` não captura a exceção no caminho de resize; o traceback chega ao
TTY. O mesmo risco existe em comandos de paginação/setas que consultam
geometria inválida. A abertura inicial e a renderização normal pelo ponto de
entrada exibem o quadro mínimo, porque `_resolver_conteudo` captura
`RenderizadorErro`; chamadas diretas a `renderizar_tela` ainda lançam.

## Regra efetiva e dimensões

O JSON declara apenas `distribuicao: "horizontal"`. O renderer normaliza esse
alias para o default de distribuição horizontal responsiva: uma linha,
multilinha até duas, `coluna_a_coluna`, margem 1, vãos 1/2/2 e
`overflow.quando_nao_couber: erro_layout`, com proibição de omitir, truncar ou
reordenar. O loader valida `politica_paginacao: "com"`; não define o teto da
barra. Os colchetes vêm do preset `Colchete` de `config/estilo.json`.

O comportamento de multilinha e o erro determinístico são normativos
(contrato da barra, §§17, 19, 20); o valor exato 2 é default normativo do
renderer/ADR-0014, aplicado indiretamente pelo alias, não uma decisão
explícita deste JSON, nem uma limitação provisória. Não é defeito o renderer
recusar arranjo fora do máximo; o defeito é deixar essa recusa escapar no
resize. Para esta tela, os primeiros limites medidos são:

| linhas | largura útil mínima | `content_w` mínimo | terminal mínimo | altura da caixa |
|---:|---:|---:|---:|---:|
| 1 | 60 | 62 | 65 | 3 |
| 2 | 36 | 38 | 41 | 4 |
| 3 | 24 | 26 | 29 | 5 |
| 4 | 23 | 25 | 28 | 6 |
| 5 | 12 | 14 | 17 | 7 |

No varrimento 20–120 × 8–40, os primeiros pares representativos foram
`65x8` (uma linha), `41x8` (duas) e `29x8` (três, se autorizadas). Com o
limite atual, `20x8` já é impossível; com até cinco linhas, `20x10` é o
primeiro quadro completo viável medido. Abaixo de 17 colunas nenhuma
distribuição útil existe mesmo com cinco linhas; em altura, a caixa exige
`linhas+2`, e cada linha adicional reduz em uma linha a área útil do console.

## Impactos, alternativas e recomendação

Mais linhas reduzem `l_corpo_disponivel` e a capacidade por página; podem
aumentar o total de páginas, alterar o indicador `página X/Y` e recalcular
`[<]`, `[>]` e `[✥]`. A reconciliação existente preserva foco, seleção e item
lógico/cursor, alterando apenas a página; troca explícita de página posiciona
no primeiro item navegável. Conteúdo e estado não devem ser reconstruídos.

A mantém espaço e resolve larguras reais, mas muda o default e aumenta o
impacto vertical. B mantém o contrato atual e mostra terminal insuficiente,
mas rejeita larguras que seriam representáveis. C combina o máximo
geometricamente viável com estado controlado e tem melhor cobertura, ao custo
de patch e testes. D (manter o último quadro) é simples, porém congela uma
interface enganosa e não deve ser adotada.

Recomendo C: autorizar explicitamente até cinco linhas para esta barra,
escolher a menor quantidade que caiba, e, se largura ou altura ainda forem
insuficientes, exibir o quadro canônico controlado de terminal pequeno. A
exceção não pode sair do resize; foco, seleção, cursor, página e conteúdo
devem permanecer em memória, e o retorno a uma dimensão válida deve
recalcular a página pelo item lógico e redesenhar automaticamente. Não é
necessário patch de contrato se o teto de cinco for uma configuração explícita
da tela; é necessário patch de configuração. Alterar o default global exige
patch documental adicional.

## Autorização, testes e handoff

`PATCH_HANDOFF` deve autorizar focalmente: `config/telas/demo/h0045_fluxo_execucao_paginado.json`; `tela/renderizador.py` (`_linhas_barra`,
`_geometria_por_console`/`geometria_console`, se o tratamento ficar nessa
camada); `demo/demo.py` (`_reconciliar_paginacao_apos_resize`,
`_com_geometria_real_do_console`, `_resolver_conteudo` e o trecho de resize
de `main`); e os testes focais correspondentes. `tela/paginacao.py` não
precisa de alteração produtiva, apenas de regressão.

Testes futuros: abertura suficiente; resize progressivo 1/2/3+ linhas;
menor largura viável e dimensão impossível; ausência de traceback e quadro
controlado; preservação de seleção, foco, cursor e página; recuperação
automática; ausência de perda, repetição, truncamento ou reordenação; rótulo
dinâmico de Esc; regressão das demais telas H-0045; suíte completa. A
validação manual em TTY continua pendente. Bloqueios: nenhum. Próxima
categoria: `PATCH_HANDOFF`.
