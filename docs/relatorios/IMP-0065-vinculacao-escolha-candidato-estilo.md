# IMP-0065 — Vinculação da escolha de preset ao candidato de estilo

```yaml
rastreabilidade:
  etapa: IMPLEMENTAR
  objeto: H-0065
  predecessor: H-0064
  artefato_principal:
    docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md
  item: ITEM-0010
  adr: ADR-0046

execucao:
  status: IMPLEMENTED
  arquivos_criados:
    - tela/teste_estilo_h0065.py
    - demo/teste_demo_estilo_h0065.py
    - docs/relatorios/IMP-0065-vinculacao-escolha-candidato-estilo.md
  arquivos_alterados:
    - tela/estilo.py
    - demo/demo.py
    - demo/teste_demo_estilo_h0063.py
    - demo/teste_demo_estilo_h0064.py

autorizacao_adicional_de_escopo:
  arquivos:
    - demo/teste_demo_estilo_h0063.py
    - demo/teste_demo_estilo_h0064.py
  motivo:
    - expectativas predecessoras de candidato imutavel apos Espaco foram
      superadas pela capacidade H-0065

tratamento_regressoes_historicas:
  testes_ajustados:
    - demo/teste_demo_estilo_h0063.py::test_espaco_transfere_escolha_e_muta_apenas_candidato
    - demo/teste_demo_estilo_h0064.py::test_navegacao_e_espaco_respeitam_fronteira_candidato_vs_aplicado
  testes_renomeados:
    - test_espaco_transfere_escolha_exclusiva_sem_mutar_estilo
      -> test_espaco_transfere_escolha_e_muta_apenas_candidato
    - test_navegacao_nao_muta_estilo_com_amostras
      -> test_navegacao_e_espaco_respeitam_fronteira_candidato_vs_aplicado
  invariantes_preservados:
    - baseline
    - global
    - arquivo
    - ausencia_de_Aplicar
    - ausencia_de_popup
    - ausencia_de_persistencia
    - ausencia_de_preview_real
```

## Resultado

### fonte_semantica

Candidato runtime é a fonte única do preset escolhido. `estado["selecoes"]`
é projeção/cache navegacional; enquanto existir, reflete os quatro
`preset_default` do candidato.

### reconciliacao

`ControladorTelaEstilo.reconciliar_selecoes_com_candidato()` lê o candidato,
localiza dinamicamente o filho de cada pai e reconstrói a escolha exclusiva.
Usada em F4/abertura, Espaço (sucesso e falha), prepare/redraw/resize e
saída efetiva.

### espaco_atomico

Protocolo: preparar → `definir_preset_candidato` em cópia →
`materializar_local` → reconciliar `selecoes`. Setas permanecem só
navegacionais.

### falha

Preset inválido preserva candidato anterior, reconcilia `selecoes` para ele;
baseline/global/`config/estilo.json` intactos; sem mutação parcial.

### esc_filho

Esc filho→pais não descarta candidato nem desfaz escolha candidata.

### saida_efetiva

Antes do pop: `criar_candidato()` da baseline → reconciliar `selecoes` →
verificar invariável → concluir. Pós-saída imediato: baseline = candidato =
selecoes = A nas quatro categorias.

### F4

Cada visita cria candidato da baseline e reconcilia (redundância defensiva
após saída correta).

### fronteira_estado

Sem Aplicar, Enter-como-Aplicar, popup, CONFIRMADO/ABORTADO, persistência,
publicação ou preview real. Amostras H-0064 intactas (descritivas).
Primitivas H-0061 reutilizadas; renderer não alterado nesta etapa.

### testes

```yaml
testes:
  h0065: 25 passed (tela + demo)
  regressao_h0063_h0064: 39 passed
  suite_completa: 1242 passed
```

### demonstracao

- F4 forma candidato da baseline; Espaço atualiza candidato e `selecoes`;
  Esc filho preserva; saída efetiva restaura; reabertura limpa;
  sem Aplicar/popup/persistência/preview real (non-TTY / estado).

### validacao_manual_necessaria

[]

### desvios

[]

### bloqueios

[]
