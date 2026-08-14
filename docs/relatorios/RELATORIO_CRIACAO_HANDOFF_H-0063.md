# Relatório de criação do handoff H-0063

## rastreabilidade

```yaml
etapa: CRIAR_HANDOFF
objeto: H-0063
artefato_principal:
  docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
handoff_historico:
  id: H-0062
  relacao: substituicao_operacional
```

## execucao

```yaml
status: HANDOFF_CREATED
arquivos_criados:
  - docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  - docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0063.md
```

## resultado

```yaml
fatos_materiais:
  - H-0063 substitui operacionalmente H-0062 após reprovação manual.
  - A causa registrada é VM-H0062-001, VM-H0062-002 e VM-H0062-003.
  - O escopo foi reparticionado para uma tela normal estrutural e navegacional.
arquivos_implementacao_autorizados:
  - tela/estilo.py
  - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
  - tela/renderizacao/estilo.py
  - tela/renderizador.py
  - tela/renderizacao/contexto_execucao.py
  - demo/demo.py
  - tela/teste_estilo_h0063.py
  - demo/teste_demo_estilo_h0063.py
  - docs/relatorios/IMP-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
testes_requeridos:
  - estrutura normal, quatro pais, filhos dinâmicos e fronteira sem alteração de estilo
  - navegação canônica em dois níveis, foco/cursor e saída
  - resize largo, médio, estreito suportado, baixo e crescimento posterior
validacao_manual_prevista:
  - TTY real com F4 físico, tela completa, dois níveis, resize e ausência de resíduos
fora_de_escopo:
  - escolha ou aplicação de preset, candidato, baseline, divergência, Aplicar e confirmação
  - persistência, publicação, preview, popup e teclas F1, F11, F2, F3 e F5
bloqueios: []
```

Os dois artefatos foram materializados. H-0062 não foi alterado; não houve
implementação, QA, stage, commit ou push.
