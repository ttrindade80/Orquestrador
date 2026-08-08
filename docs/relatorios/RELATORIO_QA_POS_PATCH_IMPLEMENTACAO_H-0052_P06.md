status: I5_MANUAL_VALIDATION_REQUIRED
handoff: H-0052
patch: P06
achado_corrigido: chip_ajuda_nao_permaneceu_como_ultimo_chip
teste_manual_1_de_3: APROVADO_NAO_REPETIR
teste_manual_2_de_3:
  navegacao: APROVADA_NAO_REPETIR
  ordem_chips: PENDENTE_CONFIRMACAO_FOCAL
teste_manual_3_de_3: PENDENTE
proxima_acao: VALIDACAO_MANUAL_FOCAL_ORDEM_CHIPS

## Auditoria

A causa foi exclusivamente declarativa: antes do P06, `chip_ajuda` vinha antes de `chip_navegar`; o renderer preserva a ordem relativa dos chips. A fixture agora resulta em `[Esc] Sair`, `[✥] Navegar`, `[?] Ajuda`, com `[?] Ajuda` por último. `[Esc]`, `[✥]` e `[?]` permanecem presentes; nenhum chip ou regra de existência foi criado.

O diff P06 está restrito à reordenação da fixture e ao teste preventivo em `tela/teste_navegacao.py`; o renderer/runtime não foi alterado. O teste usa loader, modelo e `renderizar_tela`, confere a saída real, a presença dos dois chips, a posição relativa e o término da linha em `[?] Ajuda`, sem fixar espaços.

Resultados: focal `1 passed`; `tela/teste_navegacao.py tela/teste_loader.py`: `135 passed`; suíte integral: `1060 passed in 28.77s`; `git diff --check`: aprovado. Resta apenas a confirmação visual focal da ordem pelo usuário; o teste manual 3/3 permanece pendente.
