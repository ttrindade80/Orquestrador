# Relatório QA de implementação — H-0059

Objeto: auditoria independente de `H-0059`, confrontando o handoff aprovado, o relatório `IMP-0059` e o comportamento efetivo.

Escopo auditado: diff e leitura focal de `tela/renderizacao/popup.py`, `tela/teste_popup.py`, `demo/demo.py`, `demo/teste_demo_popup.py` e `config/telas/demo/demo.json`; leitura integral do handoff e do relatório de implementação. O diff de implementação contém somente esses cinco caminhos autorizados. Não há alteração reportada em `tela/renderizacao/tela.py`, fixtures H-0058, autoridades normativas, backlog ou capacidades deferidas.

Resultado focal: `\r` e `\n` confirmam uma única vez apenas com regra `CONFIRMADO`; exclusiva devolve o ID vivo válido e múltipla devolve IDs na ordem declarada, inclusive `[]`. Estados inválidos permanecem sem resultado. O envelope confirmado contém somente `status` e `valor`; `Esc` produz somente `ABORTADO`. A instância fica terminal, o binding modal fecha-a, grava o envelope exato em `popup_resultado`, captura a tecla terminal e reativa a tela subjacente. Pop-ups textuais permanecem sem confirmação.

Evidência executada:

- testes focais: `70 passed`;
- suíte canônica: `1167 passed`;
- harness determinístico do handoff: confirmação `True` com `{'status': 'CONFIRMADO', 'valor': 'opcao_1'}` e aborto `True` com `{'status': 'ABORTADO'}`;
- verificação adicional de múltipla vazia, terminalidade, textual e configuração: aprovada;
- `git diff --check`: limpo.

O relatório de implementação é factual, incluindo arquivos, comportamento, testes, demonstração, ausência de TTY, desvios e bloqueios. TTY real não é necessária: os requisitos materiais ficaram cobertos por testes e harness reproduzível.

status: I1_IMPLEMENTATION_APPROVED
