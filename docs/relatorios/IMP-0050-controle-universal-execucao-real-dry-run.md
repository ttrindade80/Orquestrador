# IMP-0050 — Controle universal de execução real e `dry-run`

status: IMPLEMENTED_AWAITING_QA

## Arquivos

Criados `tela/registro_acoes.py`, `tela/controle_execucao.py`,
`demo/executor_controle_execucao.py`, as duas configurações H-0050, a fixture
`demo/fixtures/h0050_execucao_universal_fixture.json` e os testes focais de
registro, controle e executor. Alterados `tela/carregamento/tela_json.py`,
`tela/renderizacao/barra_menus.py`, `demo/demo.py`, `tela/teste_loader.py`,
`tela/testes_renderizador/barra_menus.py` e `demo/teste_demo.py`.

## Comportamento entregue

O loader valida `controle_execucao` como objeto fechado, exigindo somente
`modo_inicial` e aceitando apenas `executar` ou `dry_run`, sem default e sem
estado vivo. O registro resolve referências explícitas e mantém categoria e
modos de execução autoritativos. Processos precisam declarar os dois modos
para que uma tela adotante seja elegível; navegação e visualização são
resolvidas sem essa exigência.

O controle mantém uma única instância por tela aberta, alterna exclusivamente
por `Insert`, preserva o modo durante suspensão/retorno e cria novo modo
inicial em nova sessão. A barra representa o chip específico com rótulo
dinâmico `[Insert] Executar` ou `[Insert] Dry-Run`; no segundo caso, o destaque
usa a cor resolvida por `cor_alerta`.

A requisição entregue à ação registrada é uma captura interna congelada, com
lote reconciliado e modo capturado. O executor sintético recebe somente essa
captura e a fixture determinística; alteração posterior de `Insert` não altera
a requisição já capturada.

## Demonstração e testes

As duas configurações demonstram os modos iniciais. A ação H-0050 é registrada
no mesmo mecanismo universal, sem metadado de compatibilidade no JSON. O smoke
automatizado da demo exibiu os dois rótulos, aplicou o destaque de `dry_run` e
terminou com código zero.

Testes focais aprovados: 245 testes. Suíte completa aprovada: 1.014 testes.
A regressão H-0044 (`tela/teste_fluxo_execucao.py` e os testes integrados da
demo) permaneceu aprovada; os arquivos preservados do H-0044 não receberam
delta.

## Desvios, exceções e bloqueios

Desvios: nenhum. Exceções operacionais: nenhuma. Alterações preexistentes do
workspace fora do manifesto foram preservadas e não foram usadas como parte
da implementação.

## Validação manual

```yaml
validacao_manual:
  necessaria: true
  executor: USUARIO_EM_TTY_REAL
  executada: false
  resultado: PENDENTE_USUARIO_TTY
```

O roteiro permanece abrir ambas as configurações na mesma sessão TTY, conferir
o texto apresentado com a cor resolvida por `cor_alerta`, alternar `Insert`,
executar, retornar, redimensionar, sair e reabrir.
