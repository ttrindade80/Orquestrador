# Relatório QA de Implementação — H-0063

```yaml
rastreabilidade:
  etapa: QA_IMPLEMENTACAO
  objeto: H-0063
  handoff: docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  implementacao: docs/relatorios/IMP-0063-tela-estilo-estrutura-navegacao-dois-niveis.md

resultado:
  status: I5_MANUAL_VALIDATION_REQUIRED
  verificacoes_executadas:
    - leitura integral do handoff, relatório de implementação e arquivos do manifesto
    - inspeção focal da política canônica de dois níveis, paginação, Cabeçalho, Console, Barra e resize
    - git diff solicitado; git diff --cached --name-only; git status --short --untracked-files=all
    - pytest focal: 19 passed
    - pytest completo: 1197 passed
    - demonstração non-TTY H-0063 em 100x30, 62x20, 80x24 e terminal insuficiente 8x4
    - probe independente de F4, quatro pais, escolhas, ausência de mutação, resize simulado e F1/F2/F3/F5/F11
  achados: []
  validacao_manual_necessaria:
    - id: VM-H0063-001
      requisito: F4 físico e aparência inequívoca de tela normal completa em TTY
      por_que_nao_comprovavel_automaticamente: testes comprovam a normalização e o pipeline; não comprovam a percepção física do terminal
      comando_fixture: python demo/demo.py; acionar F4 físico
      resultado_esperado: Cabeçalho, Console e Barra de Menus aparecem como uma única tela, sem popup, modal ou overlay
    - id: VM-H0063-002
      requisito: navegação física entre pais e filhos, legibilidade e cursor válido
      por_que_nao_comprovavel_automaticamente: a demonstração e os testes usam comandos normalizados/non-TTY, não teclado físico
      comando_fixture: python demo/demo.py; F4, setas, Espaço e Esc
      resultado_esperado: setas movem o corrente, Espaço transfere somente a escolha do pai e Esc retorna preservando-a
    - id: VM-H0063-003
      requisito: resize real com redução, crescimento e ausência de resíduos
      por_que_nao_comprovavel_automaticamente: dimensões variadas foram simuladas e o caminho SIGWINCH foi inspecionado, mas não exercitado em terminal real
      comando_fixture: python demo/demo.py; abrir H-0063 por F4 e redimensionar fisicamente
      resultado_esperado: recomposição normal, regiões preservadas, foco/escolhas válidos, sem resíduos e recuperação após crescimento
  desvios_avaliados:
    - id: DESVIO-PAG-H0063
      decisao: Caso A; [PgUp][PgDn] Páginas é compatível com a infraestrutura canônica
      evidencia: H-0063 declara politica_paginacao: com; contrato_console/contrato_barra_de_menus exige PageUp/PageDown e a representação [PgUp][PgDn]
    - id: TESTES-H0062
      decisao: remoção não gerou achado; os dois caminhos não existem no estado atual nem no HEAD, e a cobertura vigente equivalente está nos testes H-0063
  bloqueios: []
```

A implementação auditada passa pelo renderer normal: o JSON declara Cabeçalho,
um Console e Barra de Menus; `tela/estilo.py` apenas projeta conteúdo externo
em memória; não há composição de popup nem mutação de estilo. O probe confirmou
os quatro pais exigidos, 18 presets derivados dinamicamente, uma escolha inicial
por pai, distinção entre cursor e escolhido, transferência exclusiva por pai e
preservação de baseline, candidato, global e arquivo de configuração.

F4 foi verificado pelo decoder/dispatcher vigente; F1/F2/F3/F5/F11 não ganharam
ações. O fluxo non-TTY demonstrou abertura, entrada nos filhos, `[Esc] Retornar
aos pais`, paginação canônica, saída pela pilha e ausência de Aplicar,
CONFIRMADO e ABORTADO. O stage está vazio e `config/estilo.json` não tem delta.
Há outros deltas não staged no worktree, de etapas distintas; nenhum caminho
fora da autorização de implementação de H-0063 foi atribuído a esta etapa.
