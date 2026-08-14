# IMP-0068 — Persistência e publicação do estilo confirmado

```yaml
rastreabilidade:
  etapa: IMPLEMENTAR
  objeto: H-0068
  predecessor: H-0067
  artefato_principal:
    docs/handoff/H-0068-persistencia-publicacao-estilo-confirmado.md
  item: ITEM-0010
  adr: ADR-0046

execucao:
  status: IMPLEMENTED
  arquivos_criados:
    - tela/teste_estilo_h0068.py
    - demo/teste_demo_estilo_h0068.py
    - docs/relatorios/IMP-0068-persistencia-publicacao-estilo-confirmado.md
  arquivos_alterados:
    - tela/carregamento/estilo.py
    - tela/estilo.py
    - demo/demo.py
    - demo/teste_demo_estilo_h0067.py
    - tela/teste_loader.py

resultado:
  delta_material:
    - >
      EstadoEstiloRuntime.caminho_destino: acessor publico somente-leitura
      de config/estilo.json (mesma composicao interna ja usada).
    - >
      ControladorTelaEstilo.aplicar_solicitacao_confirmada consome
      exclusivamente solicitacao.candidato, chama aplicar_candidato no
      destino do runtime e, em sucesso, reconcilia selecoes.
    - >
      demo.py, no mesmo evento CONFIRMADO: aplica o snapshot, sincroniza
      estado["estilo"] com a materializacao e remove a solicitacao.
      EstiloErro e capturado no dispatch; tentativa consumida; sem retry
      e sem popup de erro. ABORTADO permanece sem aplicacao.
  testes:
    - tela/teste_estilo_h0068.py: 6 passed
    - demo/teste_demo_estilo_h0068.py: 8 passed
    - demo/teste_demo_estilo_h0067.py: 19 passed
    - tela/teste_estilo_h0067.py: 3 passed
    - h0061_sucesso_e_fail_closed: 2 passed
    - acessor_caminho_destino: 1 passed
    - regressao_h0063_a_h0068: 127 passed
    - suite_completa: 1311 passed
  demonstracao: >
    processar_comando non-TTY: divergir candidato → Enter/Aplicar →
    Enter/Confirmar → arquivo, baseline, global, candidato e
    estado["estilo"] iguais a materializacao; Aplicar inativo;
    solicitacao ausente; tela de Estilo ativa.
  excecoes:
    - >
      Falha de publicacao isolada nao existe nesta arquitetura
      (troca unica apos persistencia); coberta pela falha de persistencia.
    - >
      test_enter_com_popup_nao_reexecuta_aplicar_da_tela e
      test_snapshot_confirmado_permanece_ligado_ao_original passaram a
      usar tmp_path (CONFIRMADO agora persiste) e a esperar solicitacao
      consumida. ABORTADO, modalidade, popup e geometria P01 intactos.
  bloqueios: []
  validacao_manual_necessaria: []
  fronteira_posterior: >
    Demonstracao integrada com override local (ADR-0046 §5) permanece
    fora de H-0068. ITEM-0010 segue em_andamento.
```

## Resumo da implementação

H-0068 orquestra a aplicação definitiva no mesmo evento `CONFIRMADO`.
Não reimplementa validar/persistir/publicar/baseline: reutiliza
`aplicar_candidato`. O snapshot `solicitacao.candidato` é a única fonte.
Após sucesso, `estado["estilo"]` recebe a materialização retornada.
Falha de persistência é fail-closed; a solicitação da tentativa é
removida sem retry automático.

## Inspeção final

- `config/estilo.json`: sem delta de teste
- stage: vazio
- nenhuma segunda primitiva de persistência/publicação
- H-0063 a H-0066: arquivos de teste não alterados
- `git diff --check` limpo nos arquivos desta fatia
