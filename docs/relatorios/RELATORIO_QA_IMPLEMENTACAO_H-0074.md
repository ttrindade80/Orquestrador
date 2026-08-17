# RELATORIO_QA_IMPLEMENTACAO_H-0074

status: I5_MANUAL_VALIDATION_REQUIRED

Escopo auditado: handoff H-0074, relatório de implementação, diff real de
`modelo.py`, `navegacao.py`, `selecao.py`, fixtures H-0055/H-0072 e testes
`teste_navegacao.py`/`teste_loader.py`. O delta semântico é somente H-0074;
remoções de literal EOF em arquivos autorizados são não semânticas e foram
necessárias para parsing.

`filho_default` é preservado em `NoConteudo.campos`; `construir_modelo` valida
após `_propagar_conteudo_externo`, por import local sem ciclo/efeito colateral.
O gate incide apenas em consoles `dois_niveis_por_foco` com conteúdo; H-0063
sem conteúdo externo não é rejeitada. Ausência, referência inválida e
identidade ambígua falham fechado, antes de baseline. Baseline/candidato usam
o default documental, pais permanecem independentes, cursor é separado e não
há fallback material `filhos[0]`/`filhos[0][0]`.

Testes focais canônicos não coletam por `tela_json.py` no HEAD. A suíte
canônica também terminou com 42 erros de coleta. Esses resíduos EOF/JSON e
`demo.py` foram confirmados como `PREEXISTENTE_NAO_CAUSAL`; não há
`CAUSAL_H0074` nem `NAO_CONFIRMADO`. Com hook somente em memória: 16 passed.

H-0055/H-0072 têm defaults existentes e pertencentes aos pais. Hash repetido:
`54fdb90080d404e31ef6fbe7cfb6809df38229399183b8756277c184aad2efe2` antes/depois.
Não há Aplicar, pop-up, persistência ou H-0075. Nenhum achado técnico.

Validação visual/TTY permanece pendente e momentaneamente bloqueada pela
infraestrutura histórica de `demo.py`; deve ser executada pelo usuário.
