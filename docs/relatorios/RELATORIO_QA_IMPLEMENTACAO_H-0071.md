# Relatório de QA — H-0071

status: I2_IMPLEMENTATION_PATCH_REQUIRED

## Resultado

Os testes focais de H-0071 passaram, assim como a suíte focal da Barra: 35
passaram em `tela/teste_estilo_h0071.py` +
`demo/teste_demo_estilo_h0071.py`, e 85 passaram em
`tela/testes_renderizador/barra_menus.py`. A validação visual/interativa em
TTY não foi executada.

## Achados

### QA-H0071-001 — A — configuração padrão alterada indevidamente

- teste/caminho: `config/estilo.json`; `tela/teste_popup.py` (3 falhas);
  `demo/teste_demo_paginacao.py` (18 falhas); gate exibido por
  `tela/teste_loader.py` na suíte canônica.
- evidência focal: o diff altera `chip.preset_default` de `Colchete` para
  `Curva`, embora o handoff autorize somente adicionar
  `cor_fundo_esquerdo: "padrão"` e `cor_fundo_direito: "azul"`. As mensagens
  mostram formas/capitalização atuais como `╭A╮ UM`, ausência de expectativas
  `[Esc]`/`[✥]` e `Marcar`/`Voltar` não encontrados; o gate declara
  explicitamente que esperava o preset ativo `Colchete` e `caixa_alta == False`.
- impacto: regressão de comportamento vigente, além de violação da restrição
  de configuração do H-0071. A correção cabe em arquivo já autorizado.
- camada: IMPLEMENTACAO.

### QA-H0071-002 — A — forma ornamental não atende o requisito literal

- teste/caminho: composição focal de `tela/renderizacao/estilo.py` e
  `config/estilo.json`.
- evidência focal: a composição compartilhada funciona e usa `/`, mas a
  configuração materializa `Ornamental` como `❲PgUp/PgDn❳`; o requisito do
  H-0071 exige `╭PgUp/PgDn╮`. Os testes focais não detectam isso porque montam
  a expectativa a partir dos próprios caracteres da configuração.
- impacto: CA-H0071-05 não demonstrado/conforme. A correção também está no
  arquivo autorizado de configuração, mas não foi autorizada no delta
  concreto declarado pelo handoff.
- camada: IMPLEMENTACAO.

### QA-H0071-003 — D — resíduos da suíte canônica não determináveis pelo manifesto

- teste/caminho: demais falhas/erros da suíte canônica em arquivos fora do
  manifesto, incluindo `demo/teste_demo.py`, `demo/teste_demo_console.py`,
  `demo/teste_diagnostico.py`, `demo/teste_explorar_barra_de_menus.py`,
  `demo/teste_demo_estilo_h0063.py`, `demo/teste_demo_estilo_h0070.py` e
  `tela/teste_resultado_execucao.py`.
- evidência: a execução terminou com 1295 passed, 75 failed e 17 errors, mas
  o caminho/nome/mensagem exibidos não permitem separar todos os casos entre
  regressão, expectativa substituída ou falha independente sem abrir arquivos
  proibidos pelo manifesto. Não foram abertos.
- impacto: não há base para classificar esses casos como “legados” nem para
  usá-los como aprovação.
- camada: NAO_CONFIRMADO.

## Evidência adicional

`tela/teste_popup.py` terminou com 65 passed e 3 failed; `demo/teste_demo_paginacao.py`
com 110 passed e 18 failed. A suíte canônica confirmou os números declarados
no relatório de implementação, mas a suíte da Barra declarou 120 passed e a
execução atual produziu 85 passed. Essa discrepância reduz a confiabilidade
do relatório de implementação.

Conclusão: a implementação não deve ser aprovada. Corrigir os achados dentro
do escopo autorizado e repetir este QA; a validação manual posterior continua
pendente e não foi declarada.
