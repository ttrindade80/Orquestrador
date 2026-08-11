# IMP-0056 — implementação do pop-up básico

## Arquivos criados

- `tela/renderizacao/popup.py`
- `tela/teste_popup.py`
- `demo/teste_demo_popup.py`
- `demo/fixtures/h0056_popup_texto.py`
- este relatório

## Arquivos alterados

- `tela/renderizacao/tela.py`
- `demo/demo.py`
- `config/telas/demo/demo.json`

## Comportamento implementado

Foi implementado o pop-up modal textual curto com moldura, título, conteúdo
runtime separado, chip próprio `[Esc] Voltar`, geometria intrínseca simples e
centralização sobre o bloco físico do corpo. A renderização reutiliza o estilo
resolvido e as primitivas de caixa existentes; a área do pop-up não usa a
barra de menus.

A declaração `popups.popup_basico` é resolvida pela chave do mapa, validada sem
`id` interno redundante e sem conteúdo concreto. O envelope demonstrativo é
fornecido pelo fixture Python em runtime. A instância modal captura todas as
teclas; somente `Esc` fecha e produz exatamente `{"status": "ABORTADO"}`.
A tela subjacente e sua instância permanecem preservadas, e voltam a receber
entrada após o fechamento.

## Testes focais

Comando:

`PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py -q`

Resultado: 20 testes aprovados. Foram cobertos mapa opcional, resolução,
rejeição de ID, ausência de `id` interno, separação/reutilização do conteúdo,
schema canônico do chip, domínios, geometria, centralização, overlay modal,
captura de tecla não declarada, `Esc`, `ABORTADO` sem payload, independência
da barra e ausência de paginação.

## Suíte canônica

Comando:

`PYTHONDONTWRITEBYTECODE=1 python -m pytest`

Resultado: 1117 testes aprovados, código de saída zero.

## Demonstração

Foi executado o `demo/demo.py` em fluxo non-TTY reproduzível com abertura por
`p`, tecla não declarada, `Esc`, interação posterior e encerramento. O processo
terminou com código zero; a saída confirmou programaticamente título, conteúdo
textual e chip do pop-up.

A inspeção visual/interativa final em TTY real permanece pendente do usuário.

## Desvios, exceções e bloqueios

Desvios efetivos: nenhum. Exceções: nenhuma. Bloqueios: nenhum.
