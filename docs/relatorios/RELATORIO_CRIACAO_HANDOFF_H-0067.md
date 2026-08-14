# Relatório — Criação do handoff H-0067

```yaml
rastreabilidade:
  etapa: CRIAR_HANDOFF
  objeto: H-0067
  item: ITEM-0010
  adr: ADR-0046
  predecessor: H-0066
```

## Autoridades lidas

Integralmente: `ADR-0046`, `H-0066`, `H-0061`, `ADR-0044`, `contrato_popup.md`
(inclusive §9.1, já vigente e específico para este uso), `35_POPUP.md`
(inclusive §6.1, já vigente), `contrato_barra_de_menus.md` §10.1/§11.
Focalmente: `H-0063`, `H-0065`, `H-0056`, `H-0057`, `H-0059`, `ADR-0045`.
`H-0062` foi consultado apenas como precedente histórico já declarado
explicitamente por `H-0066` (chip `[⏎] Aplicar`), nunca como autoridade
normativa própria, conforme exigido.

Código inspecionado (sem alteração): `tela/renderizacao/popup.py`,
`tela/estilo.py`, `demo/demo.py` (ramificação modal e tratamento de
`Enter/Aplicar` na tela H-0063), `tela/renderizacao/tela.py`,
`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`.

## Análise da confirmação

```yaml
analise_confirmacao:
  tipo_popup: >
    DETERMINADO_PELA_AUTORIDADE. contrato_popup.md §9.1 e 35_POPUP.md §6.1
    (ja vigentes no repositorio) ja nomeiam explicitamente a "Confirmacao de
    aplicacao de estilo (ADR-0046)" como consumidora do sistema generico de
    popup, tipo: texto, centralizado sobre a tela ativa. Nao e novo tipo.
  conteudo: >
    Titulo e pergunta obrigatorios estruturalmente (DETERMINADO), mas seu
    texto literal fica deliberadamente aberto (ADR-0046 §6: "nao fixa
    literal especifico... quando o contrato aplicavel nao exigir
    literalidade"). Nenhuma autoridade exige resumo do candidato no texto;
    como H-0067 nao abre demonstracao integrada, o texto permanece generico.
    Chips: Esc/"Voltar"->ABORTADO e Enter/"Confirmar"->CONFIRMADO; os
    literais de rotulo "Voltar"/"Confirmar" nao sao exigidos pela ADR (que
    permite outros, ex. "[Enter] Aplicar"), mas sao exigidos HOJE pelo
    codigo vigente de tela/renderizacao/popup.py (_validar_chip); mantidos
    para nao exigir generalizacao adicional dessa validacao.
  enter: >
    DETERMINADO_PELA_AUTORIDADE. Confirma (status: CONFIRMADO, sem valor,
    pop-up textual nao tem itens). Fixo, sem foco navegavel entre chips
    (isso so existe para itens de marcacao).
  esc_voltar: >
    DETERMINADO_PELA_AUTORIDADE. ABORTADO, fecha o popup, retorna a tela de
    Estilo (que permanece ativa por baixo), preserva integralmente o
    candidato (ADR-0046 §7) e NAO aciona a regra de descarte de saida
    efetiva de H-0065 -- essa regra pertence a uma camada de Esc distinta
    (saida da tela), que o Esc do popup nunca alcanca por precedencia modal.
  resultado_positivo: >
    Somente o resultado generico do popup (CONFIRMADO). Efeito adicional
    autorizado: a SolicitacaoAplicacaoEstilo de H-0066 permanece retida e
    intocada para uma etapa posterior consumir; nenhuma persistencia,
    publicacao ou promocao de baseline ocorre em H-0067; nenhum literal de
    maquina de estados novo e criado.
  resultado_negativo: >
    Popup fecha, retorna a tela de Estilo, candidato preservado, Aplicar
    permanece elegivel conforme divergencia; a solicitacao daquela tentativa
    e descartada (nao persiste como pendencia).
  literais: >
    CONFIRMADO/ABORTADO ja definidos literalmente pela autoridade vigente
    (contrato_popup.md §9/§9.1; ADR-0046 §6.4/§7); ao contrario de H-0066,
    pertencem exatamente a esta capacidade e sao usados tal como definidos.
  snapshot: >
    O popup consome a SolicitacaoAplicacaoEstilo ja produzida por H-0066
    (imutavel, copias independentes) e nao reconstroi um novo snapshot do
    candidato mutavel. A tela de Estilo fica modalmente bloqueada durante a
    abertura (precedencia ja generica de H-0059), garantindo que nada mute
    o candidato enquanto o popup decide.
  modalidade: >
    Reuso integral e sem alteracao da ramificacao modal generica de H-0059
    em demo/demo.py: enquanto estado["popup"] existir, toda tecla e
    consumida ali, antes de qualquer dispatch de tela/Barra. Nenhuma
    ambiguidade de precedencia identificada.
  resize: >
    Reuso integral da geometria/resize generico do popup (contrato_popup.md
    §4/§11; ADR-0044/ADR-0045), ja implementado e testado desde H-0056-H-0060.
    Nenhum mecanismo especifico de Estilo e criado.
  suficiencia_documental: >
    Suficiente. Todas as perguntas da matriz (A-G) resolvem por autoridade
    vigente + infraestrutura ja materializada. A unica lacuna encontrada
    (ver "Achado tecnico" abaixo) e de codigo, nao de autoridade documental,
    e a propria autoridade ja resolve inequivocamente o comportamento
    correto. Nao ha NAO_DETERMINADO com duas semanticas materialmente
    plausiveis. status: HANDOFF_CREATED.
```

## Achado técnico relevante (não bloqueante)

`tela/renderizacao/popup.py` hoje **rejeita** declarações `tipo: texto` com
chip `Enter` (`_validar_chip`/`validar_declaracao_popup` levantam
`PopupErro`), e `consumir_tecla_popup` só despacha `Enter` para instâncias
`tipo: marcacao`. Essa restrição foi escrita em H-0059, cujo próprio texto já
a registrava como escopo daquela etapa, não como fronteira permanente. Já
`contrato_popup.md` §9.1 e `35_POPUP.md` §6.1 — ambos vigentes e já
aplicados ao repositório como parte da aplicação de ADR-0046 — exigem
exatamente que este uso (`tipo: texto`, ADR-0046) devolva `CONFIRMADO`. Não
há conflito material entre autoridades: a autoridade documental já resolveu
a questão; o código é que ainda não foi estendido. Por isso, o handoff
autoriza nominalmente a extensão pontual de `tela/renderizacao/popup.py`
(não um segundo sistema de pop-up) como pré-requisito de implementação, e
registra isso explicitamente na matriz (§5.A) e na lista de arquivos
autorizados.

Também foram identificados, por inspeção de `demo/teste_demo_estilo_h0066.py`,
exatamente três testes cuja premissa "Enter ativo não abre popup" é
deliberadamente superada por H-0067 (`test_aplicar_presente_ativo_enter_produz_somente_solicitacao`,
`test_fronteiras_apos_enter_aplicar_sem_popup_persistencia_publicacao` e
`test_snapshot_imutavel_apos_mutacao_posterior_via_dispatch`, este último
exigindo um passo adicional de fechamento do popup antes de continuar a
sequência de comandos). As demais suítes predecessoras (H-0063/H-0064/H-0065
e o restante de H-0066) não pressupõem `Enter` acionado com `Aplicar` ativo
nos pontos em que verificam ausência de popup, portanto permanecem válidas
sem alteração — verificado nominalmente por leitura direta dos arquivos, não
presumido.

## Resultado

```yaml
resultado:
  status: HANDOFF_CREATED
  handoff:
    docs/handoff/H-0067-confirmacao-aplicacao-estilo.md
  capacidade:
    - confirmacao_da_aplicacao_de_estilo
    - reuso_popup_generico_tipo_texto_com_confirmacao
    - retencao_da_solicitacao_apos_confirmado
    - descarte_da_solicitacao_apos_abortado
  arquivos_implementacao_autorizados:
    - tela/renderizacao/popup.py
    - config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json
    - tela/estilo.py
    - demo/demo.py
    - tela/teste_popup.py
    - demo/teste_demo_popup.py
    - tela/teste_estilo_h0067.py
    - demo/teste_demo_estilo_h0067.py
    - demo/teste_demo_estilo_h0066.py (somente as 3 asserções/testes
      nominados na secao 9 do handoff)
    - docs/relatorios/IMP-0067-confirmacao-aplicacao-estilo.md
  testes_requeridos:
    - entrada valida (Aplicar ativo abre popup com a solicitacao)
    - entrada invalida (sem solicitacao, sem popup)
    - Enter positivo (CONFIRMADO, retencao, sem persistencia/publicacao)
    - Esc/Voltar (ABORTADO, candidato preservado, sem regra de saida H-0065)
    - modalidade (teclas subsequentes consumidas pelo popup)
    - snapshot (popup e resultado usam a solicitacao original)
    - resize com popup aberto
    - fronteiras (baseline/global/arquivo intactos em todo cenario)
    - regressao integral H-0063/H-0064/H-0065/H-0066/pop-up H-0056-H-0060/suite completa
  fora_de_escopo:
    - persistencia em config/estilo.json
    - publicacao de novo estilo global
    - promocao/atualizacao da baseline persistida
    - demonstracao integrada (Cabecalho+Console+Dashboard+Barra sob override)
    - preview real do candidato no runtime global
    - novo sistema/tipo de pop-up
    - reabertura da tela de selecao de presets dentro do popup
    - tiling, cor_inativo, cor_alerta, indicadores.concluido
    - ITEM-0024, ITEM-0032, F1, F11, F2, F3, F5
  bloqueios: []
```
