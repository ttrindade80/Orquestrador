# RELATÓRIO — PATCH_IMPLEMENTACAO H-0072 P02

```yaml
etapa: PATCH_IMPLEMENTACAO
objeto: H-0072
patch: P02
achado_origem: VM-H0073-001
predecessor_imediato: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0073.md
cadeia_raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: IMPLEMENTATION_PATCHED
```

## Causa técnica comprovada

`tabulacao.minimo`/`maximo` são lidos em
`tela/renderizacao/conteudo_externo.py`; a largura corrente chega por
`content_w`, após `_largura_renderizada_multinivel`, a cada chamada de
renderização. A instrumentação do fluxo real confirmou, em H-0055, largura
total 120→50 produzindo `content_w` 111→41. Não havia cache, default fixo de
largura, erro de loader ou configuração incorreta; SIGWINCH atualiza o estado
e o render seguinte recalcula.

O defeito estava em `_cabe_tabulacao`: a escolha usava somente
`content_w - prefixo >= 10` (`_MIN_UTIL_DOIS_NIVEIS_FILHO`). Assim, a largura
variava, mas a tabulação permanecia 10 enquanto a apresentação real já
exigia compactação. Em H-0063 isso deixava a tabela quebrar a coluna, em vez
de reduzir a tabulação. H-0055 e H-0063 compartilham o mesmo helper; por isso
a causa explica ambas. Os testes anteriores cobriam larguras diretas, mas o
teste de resize verificava apenas mudança de linha/ espaçamento e identidade,
não a mudança do valor efetivo da tabulação.

## Correção e arquivos

Antes, o maior candidato era aceito quando sobravam apenas 10 colunas úteis.
Agora, para texto, a largura mínima considerada é
`max(10, len(texto_filho))`; para tabela, é a soma das larguras globais das
colunas mais o espaçamento mínimo. A escolha continua sendo o maior valor no
intervalo declarado, sem reduzir abaixo do mínimo. O cálculo de espaçamento
3..8 não foi alterado.

Arquivos efetivamente alterados nesta execução:

- `tela/renderizacao/conteudo_externo.py`
- `tela/teste_formato_filho_dois_niveis_por_foco.py`
- `demo/teste_demo_h0073_h0055_reconciliado.py`
- `demo/teste_demo_h0073_h0063_reconciliado.py`
- este relatório

Nenhuma configuração, conteúdo, loader, modelo, `demo/demo.py`, documento
normativo ou artefato H-0072 P01 fora do delta causal foi alterado.

## Evidências

Na mesma estrutura e em renders sucessivos, H-0055 produz tabulação
`10, 9, 5` para larguras úteis `28, 27, 23`, preservando `A)`, a unidade
`ec`/`tg`/designador/conteúdo e as identidades. H-0063 produz `10, 9, 5`
para `51, 43, 39`, preservando preset/amostra, ausência de designador e
alinhamento; os gaps medidos entre colunas são `8, 3, 3`, dentro de 3..8.
Os novos testes também comprovam monotonicidade e item lógico constante.

## Regressões

Suíte focal mínima: `158 passed`.

H-0070 executado isoladamente: permanece falhando com `index("→") == 2`
(`>= 4` esperado), sem alteração do teste ou do caminho histórico.

Suíte canônica: `1455 passed, 1 failed`; a única falha é a mesma H-0070,
não causal ao patch. H-0055, H-0063, H-0072, texto, tabela, designadores,
navegação, seleção, quebra multilinha e demais geometrias passam.

Desvios: nenhum. Bloqueios: nenhum. Nova validação manual: necessária para
confirmar o comportamento em TTY real antes do QA pós-patch.
\n