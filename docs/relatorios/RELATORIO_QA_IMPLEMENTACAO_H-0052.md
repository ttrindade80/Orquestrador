# Relatório QA da implementação H-0052

```yaml
status: I5_MANUAL_VALIDATION_REQUIRED
handoff: H-0052
```

A implementação automatizada está conforme o handoff. O diff real contém
alterações somente em `tela/navegacao.py`,
`tela/carregamento/envelope_pre_adr_0028.py`, `tela/teste_navegacao.py` e
`tela/teste_loader.py`, além das duas fixtures H-0052 e do relatório de
implementação declarados. O `git status --short` também mostra deltas
documentais externos ao escopo da implementação; não foram atribuídos a
H-0052. `git diff --check` passou.

Foram confirmados: fallback apenas para política objeto sem `tipo`; rejeição
sem fallback para forma não objeto, tipo desconhecido ou não textual; os cinco
literais fechados; equivalência de `nivel_unico` legado e explícito; tabela
passiva, fora do foco, sem cursor/chip e sem efeito nas quatro APIs de
movimento; rejeição de tabela navegável; transporte literal e inércia dos três
tipos futuros; preservação da paginação e ausência de antecipação de H-0053,
H-0054 e H-0055. As fixtures carregam e têm schema/id coerentes.

Testes reexecutados:

- focal exato: `147 passed, 0 failed` em `0,43s`;
- suíte integral exata: `1059 passed, 0 failed`, sem skips, em `30,72s`.

Não há achado material de implementação. A validação manual TTY não foi
simulada e permanece necessária pelo usuário. Execute:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0045_validacao_nova_pagina.json
PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0052_nivel_unico_explicito.json
PYTHONDONTWRITEBYTECODE=1 python -m demo.demo_navegacao --tela config/telas/demo/h0052_tabela_passiva.json
```
