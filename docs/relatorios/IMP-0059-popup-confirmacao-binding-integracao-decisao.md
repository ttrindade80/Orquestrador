# IMP-0059 — Popup: confirmação, binding e integração da decisão

## Escopo executado

Arquivos alterados:

- `tela/renderizacao/popup.py`
- `tela/teste_popup.py`
- `demo/demo.py`
- `demo/teste_demo_popup.py`
- `config/telas/demo/demo.json`

Arquivo criado:

- `docs/relatorios/IMP-0059-popup-confirmacao-binding-integracao-decisao.md`

As fixtures runtime H-0058 não foram alteradas.

## Comportamento entregue

`Enter` físico é aceito como `\r` ou `\n` e somente confirma quando há chip
de `Enter` com regra declarada `CONFIRMADO`. Pop-ups textuais continuam sem
contrato de confirmação. A confirmação exclusiva exige exatamente uma
marcação viva válida e produz `{"status": "CONFIRMADO", "valor": "<id>"}`.
A confirmação múltipla aceita zero a N marcações e produz `valor` como lista
de IDs na ordem lógica declarada. Estados inválidos não são convertidos em
resultado. O retorno não inclui cursor, formação, coordenadas ou histórico,
nem usa chave `payload`; o valor retornado é independente do estado vivo.

Após um resultado terminal, a instância não produz novo resultado. `Esc`
permanece produzindo exatamente `{"status": "ABORTADO"}`, sem `valor`.

No binding modal de `demo.processar_comando`, toda tecla continua pertencendo
exclusivamente ao pop-up enquanto ele existe. `CONFIRMADO` e `ABORTADO` limpam
`estado["popup"]` e gravam o envelope em `estado["popup_resultado"]`; a mesma
tecla não segue para o dispatcher subjacente. A configuração recebeu chips
de confirmação somente nas duas listas H-0058.

## Testes e demonstração

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py`
  — 70 passed.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest` — 1167 passed.
- Harness determinístico do handoff — `CONFIRMACAO True {'status':
  'CONFIRMADO', 'valor': 'opcao_1'}` e `ABORTO True {'status':
  'ABORTADO'}`.

O harness observou `popup is None` e `popup_resultado` após
`processar_comando`, evidenciando consumo real do retorno. Os testes também
verificaram retomada da tela subjacente, preservação de tela/pilha, ordem
lógica múltipla, lista vazia, equivalência `\r`/`\n`, não duplicação e as
regressões H-0056..H-0058.

## Validação TTY, desvios e bloqueios

Não foi realizada interação TTY manual. Não foi necessária para esta execução:
os testes automatizados e o harness determinístico cobriram as entradas
`\r`/`\n`, o fechamento modal e o binding. Não houve desvio de escopo,
exceção operacional ou bloqueio material.

`git diff --check` foi executado sem apontamentos.
