# QA pós-patch de implementação — H-0045 P23

status: I2_IMPLEMENTATION_PATCH_REQUIRED

## Estado

`VM-H0045-R08-001` permanece aberta. O QA técnico não é conforme devido aos
achados de seletividade e de propagação de erros abaixo. A validação manual
do usuário não foi executada.

## Configuração e escolha de linhas

`h0045_fluxo_execucao_paginado.json` contém o objeto canônico suportado. A
comparação estrutural com o default global encontrou somente
`linhas.maximo: 5` contra `2`; permanecem `coluna_a_coluna`, `minimo: 1`,
`preferir_menor_numero: true`, margem mínima 1, vãos declarados, overflow
`erro_layout` e as três proibições. Chips, teclas, textos, ordem, regras,
cores observadas e `rotulo_dinamico_esc` foram preservados. Nenhuma outra
configuração foi atribuída ao P23.

Execução real pelo loader, normalizador e renderer confirmou a menor
quantidade válida: 65/120 colunas → 1 linha; 41/64 → 2; 29/40 → 3;
28 → 4; 17/20 → 5; 16 → `erro_layout`. O default global permaneceu em duas
linhas.

## Classificação seletiva e testes negativos

Há achado material. `_e_insuficiencia_geometrica` usa `startswith("DA-0")`.
O renderer produz `DA-02` e `DA-04` para composição/invariante estrutural,
não para falta de área externa; a mesma expressão também aceita `DA-01`,
`DA-099` e códigos futuros. A expressão `startswith("erro_layout")` aceita,
analogamente, `erro_layout: modelo invalido`, embora o produtor conhecido
seja o erro específico de chips da barra. Assim, a comparação não é precisa
nem segura.

Reproduções temporárias em memória confirmaram: distribuição com
`linhas.maximo=0` e valor de preenchimento fora do vocabulário propagam pela
consulta de geometria, mas `_resolver_conteudo` os converte em quadro mínimo;
um modelo estrutural inválido também é mascarado; uma composição inválida
que produz `DA-02` é absorvida como geometria ausente. Os testes P23 cobrem
apenas mensagens sintéticas genéricas e não esses casos reais.

## Quadro controlado

Para largura insuficiente, não houve traceback, interface parcial ou quadro
congelado; a mensagem `Terminal pequeno demais` / `Aumente a janela para
continuar` apareceu e dimensões extremas foram seguras. Porém, para altura
insuficiente com largura ampla (por exemplo, `80x8`), o caminho retorna só o
quadro mínimo `terminal pequeno demais`, sem a segunda mensagem, embora ela
caiba. Isso não satisfaz o requisito semântico do estado controlado.

## Preservação e recuperação

Sequência contínua no mesmo estado lógico, com item `item_18` selecionado e
página 2, percorreu larguras 65, 41, 29, 28, 17, 14 e o retorno até 120.
As transições normais preservaram tela, pilha, foco, cursor, item, seleção,
página, modo e estado de saída; em 14 colunas os comandos de página/setas
foram no-op. Esc limpou a seleção sem sair, e a recuperação trouxe a tela
normal e `[Esc] Sair`.

## Matriz de dimensões

Os 60 pares exigidos foram executados; não houve exceção não tratada. O
resultado normal/controlado por altura, nas larguras `16,17,20,28,29,40,41,64,65,120`, foi:

| altura | resultado (`C` controlado, `N` normal) |
|---|---|
| 6 | C C C C C C C C C C |
| 8 | C C C C C C C C C C |
| 10 | C C C C C C N N N N |
| 15, 24, 40 | C N N N N N N N N N |

Nas células normais, a altura da barra foi `linhas + 2`; capacidades
observadas foram de 3–7 linhas em altura 15, 12–16 em altura 24 e 28–32 em
altura 40, com páginas recalculadas pelo plano físico real.

## Suítes e escopo

`-k "P23 or p23"`: 30 passed; suíte focal: 475 passed; suíte completa:
927 passed; `git diff --check` focal: limpo. O worktree contém alterações
históricas não pertencentes ao P23 em vários módulos, configurações e
documentos. A auditoria atribui ao P23 somente os cinco arquivos declarados;
não houve evidência focal de delta P23 em `tela/renderizador.py`,
`tela/paginacao.py`, `tela/navegacao.py`, `tela/selecao.py`, contratos,
ADRs, handoff ou outras configurações.

## Necessidade de validação manual

Permanece necessária após um patch corretivo e novo QA; não é, neste estado,
a única pendência.
