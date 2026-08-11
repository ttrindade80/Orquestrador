# Relatório QA de implementação — H-0057

status: I2_IMPLEMENTATION_PATCH_REQUIRED
baseline: 1211a70

## Evidências executadas

- Leitura integral do handoff H-0057 e do relatório IMP-0057.
- Testes focais: `35 passed`, código `0`.
- Suíte canônica: `1132 passed`, código `0`.
- Demonstração non-TTY reproduzida com `w`, `x` e `Esc`: abertura do pop-up H-0057, texto longo, recomposição em larguras 80/75, quadro geral por altura insuficiente, restauração, tecla inerte, `ABORTADO` sem payload e retorno à tela `demo`.
- Auditoria de código confirmou preservação da instância modal, uso da área física do corpo, cálculo largura → wrapping → chips → altura → centralização, chips indivisíveis/multilinha, dimensões inválidas preservando o último par válido e separação das fronteiras H-0058/H-0059.
- `git diff --check`: sem apontamentos. Não há stage, commit, `__pycache__` ou `*.pyc`. `.pytest_cache` foi gerado pela execução desta QA.

## Escopo

O delta rastreado desde `1211a70` contém somente os seis caminhos de implementação/teste/configuração autorizados. A fixture `demo/fixtures/h0057_popup_texto_dinamico.py` é o novo arquivo autorizado. Os documentos H-0057 já não rastreados no worktree não foram atribuídos ao delta implementacional.

## Achado

### QA-H0057-IMP-001 — wrapping descarta separadores e não preserva integralmente o conteúdo

`_quebrar_texto` perde separadores quando a palavra seguinte não cabe na linha: a separação pendente só é incorporada se o candidato couber, e depois é descartada. Verificação direta:

```text
_quebrar_texto("a  b", 3)  -> ["a", "b"]
_quebrar_texto("     ", 3) -> ["   "]
```

Assim, espaços múltiplos e conteúdo composto apenas por espaços são alterados/truncados durante o wrapping. Isso contraria o handoff, que exige preservação integral da string e proíbe omissão de caracteres. Os testes atuais verificam palavras e caracteres não-espaço, mas não detectam essa perda.

Correção necessária: ajustar o wrapping para consumir todos os caracteres de separação de forma física e determinística, sem transformar a entrada em conteúdo diferente.

Não foi realizada validação TTY humana.
