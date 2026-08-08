status: PATCH_IMPLEMENTACAO_CONCLUIDO
handoff: H-0052
patch: P08
origem: bloqueio_P07_resolvido_por_decisao_do_gerente
defeito: fixture_tabela_passiva_sem_conteudo_externo_real
tabela_reutilizada: config/telas/demo/h0036_tabela_conteudo.json
mecanismo_existente_reutilizado: "demo/demo.py:_CATALOGO_CONTEUDO_EXTERNO -> id_conteudo_externo_de -> carregar_conteudo_externo -> construir_modelo"
arquivo_de_associacao_alterado: demo/demo.py
arquivos_alterados:
  - demo/demo.py
  - demo/teste_demo_console.py
  - tela/teste_loader.py
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0052_P08.md
testes:
  - "demo/teste_demo_console.py: 6 passed"
  - "foco H-0052 (tela/teste_navegacao.py + tela/teste_loader.py): 23 passed, 112 deselected"
  - "tela/teste_navegacao.py + tela/teste_loader.py: 135 passed"
  - "git diff --check: passou"
suite_integral: "1060 passed in 28.87s"
validacao_manual: PENDENTE_REEXECUCAO_3_DE_3
bloqueios: nenhum

## Implementação

O demo já associava IDs de telas a documentos externos por meio do catálogo
interno de `demo/demo.py`. P08 adicionou somente a associação nominal
`h0052_tabela_passiva: h0036_tabela_conteudo`, reutilizando o mesmo loader e o
mesmo renderer. A fixture estrutural mantém `politica_navegacao.tipo = tabela`.

O teste H-0052 percorre o caminho real de `demo.demo_navegacao`, confirma que o
documento carregado é materialmente igual à tabela canônica H-0036 e verifica
no renderer o cabeçalho `Grupo/Campo/Valor`, linhas reais e a ausência do
placeholder `(console)`. A tela permanece fora da lista de foco, sem cursor,
sem efeito de setas e sem `[✥] Navegar`; `[?] Ajuda` permanece como último
chip.

Após autorização explícita de escopo, `demo/teste_demo_console.py` foi
atualizado somente para refletir o catálogo real de 10 associações, incluindo
H-0052. Nenhum comportamento de produção adicional, schema, contrato, loader
paralelo ou generalização de runtime foi criado; a tabela de referência não
foi alterada.

A validação TTY/visual manual de 3/3 permanece pendente, conforme solicitado.
