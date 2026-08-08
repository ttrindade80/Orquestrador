status: HANDOFF_INSUFICIENTE_PARA_DEMO_TABELA_REAL
handoff: H-0052
patch: P07
origem: validacao_manual_3_de_3
defeito: fixture_tabela_passiva_nao_apresenta_tabela_real
tabela_de_referencia: config/telas/demo/h0036_tabela_conteudo.json
estrutura_real: "Documento externo tipo multinivel, formato.apresentacao=tabela, cabecalho Grupo/Campo/Valor, dois grupos e quatro linhas de dados; usado por h0036_console_tabela."
incompatibilidade: "A tabela visual canônica é conteúdo externo e só é associado pelo catálogo do demo ao ID h0036_console_tabela (ou às fixtures H-0037). H-0052 é uma tela envelope cujo tipo=tabela pertence a politica_navegacao do console; o loader/modelo não oferecem associação declarativa entre essa política e um documento externo. Sem alterar runtime/catalogo, H-0052 permanece sem conteudo_externo e renderiza o placeholder (console)."
decisao_necessaria: "Autorizar alteração do catálogo/runtime para associar H-0052 à tabela canônica, ou definir uma forma declarativa vigente de associação. Não criar híbrido nem novo schema."
correcao: "Não aplicada: a correção exigiria mudança fora dos arquivos permitidos ou contrato inexistente."
arquivos_alterados:
  - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0052_P07.md
testes:
  focal_fixture_h0052: "1 passed"
  tela_teste_navegacao_teste_loader: "135 passed"
suite_integral: "1060 passed in 28.66s"
validacao_manual: PENDENTE_REEXECUCAO_3_DE_3
bloqueios: "Não há forma vigente de associar a tabela externa real à política tipo=tabela de H-0052 sem alterar runtime/catalogo; nenhuma fixture, teste ou runtime foi alterado."

## Evidência

A estrutura de referência foi localizada pela busca prescrita e confirmada no
renderizador real. O console só exibe a tabela quando recebe `conteudo_externo`;
sem essa associação, o caminho real da demonstração exibe `(console)`. A
política `tipo: tabela` continua válida e passiva no envelope, mas não
transforma itens do console em conteúdo multinível tabular.

`git diff --check`: passou. Nenhum arquivo runtime ou contrato foi alterado.
