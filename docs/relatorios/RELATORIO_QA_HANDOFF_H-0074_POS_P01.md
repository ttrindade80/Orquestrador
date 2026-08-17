# Relatório QA pós-patch — H-0074 P01

cadeia:
  raiz: H-0074
  predecessor_imediato: RELATORIO_PATCH_HANDOFF_H-0074_P01.md

achados_retestados:
  QA-H0074-001: resolvido
  QA-H0074-002: resolvido
  QA-H0074-003: resolvido
  QA-H0074-004: resolvido

novos_achados: []

status: H1_HANDOFF_APPROVED

O ponto comum em `construir_modelo`, após `_propagar_conteudo_externo`, reúne
estrutura, `filho_default` e política; o import local para a validação em
`navegacao.py` é executável e não cria ciclo ou importação parcial. H-0055,
H-0072 e futuros chamadores do construtor atravessam esse ponto; a demo não é
a única entrada.

O handoff exige a remoção dos dois fallbacks posicionais, a guarda sem escolha
válida e a rejeição de dados inválidos antes do runtime. Não há outro fallback
posicional material nos caminhos autorizados. H-0072 está catalogada, usa
conteúdo externo real e os IDs previstos pertencem aos respectivos pais; sua
estrutura permanece preservada. H-0063 continua fora do schema por usar
`preset_default` via Estilo.

A evidência prevista cobre duplicidade ambígua, rejeição sem baseline, guarda
de runtime, travessia comum, H-0072 e `sha256sum` antes/depois sem restauração
da fixture. O escopo não antecipa H-0075, ITEM-0023 ou ITEM-0024.
