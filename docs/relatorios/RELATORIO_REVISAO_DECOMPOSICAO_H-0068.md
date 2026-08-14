# Relatório — Revisão de Decomposição H-0068

```yaml
rastreabilidade:
  etapa: REVISAO_DECOMPOSICAO
  objeto: H-0068
  item: ITEM-0010
  adr: ADR-0046
  predecessor: H-0067
  fontes:
    - docs/handoff/H-0068-persistencia-publicacao-estilo-confirmado.md
    - docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0068.md
    - docs/handoff/H-0061-infraestrutura-estilo-runtime.md
    - docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md
    - tela/carregamento/estilo.py
    - tela/estilo.py
    - demo/demo.py
```

## resultado

```yaml
resultado:
  classificacao: H0068_JA_E_FATIA_PEQUENA
  justificativa: >
    Persistência, publicação, promoção de baseline, validação do candidato e
    fail-closed já estão encapsulados e testados em
    EstadoEstiloRuntime.aplicar_candidato() (H-0061;
    tela/carregamento/estilo.py:362-380; tela/teste_loader.py). H-0068, como
    escrito, não inventa segundo mecanismo nem junta responsabilidades
    materiais novas independentes: acrescenta orquestração mínima de sessão
    (consumir SolicitacaoAplicacaoEstilo retida por H-0067, obter destino,
    chamar a primitiva, sincronizar estado["estilo"], reconciliar seleções
    via método já existente, limpar a solicitação e capturar EstiloErro no
    dispatch). Contar efeitos observáveis (arquivo, global, baseline,
    seleções) como fatias distintas seria erro de decomposição: são
    consequências de uma única operação arquitetural prévia mais glue
    síncrono no mesmo evento CONFIRMADO. Não há política de retry, popup de
    erro, transição de tela nova nem segundo ponto de falha arquitetural a
    extrair para handoff posterior.
```

## capacidades_preexistentes

```yaml
capacidades_preexistentes:
  - id: validacao_candidato
    onde: EstadoEstiloRuntime.aplicar_candidato / materializar_estilo_local
    origem: H-0061
    evidencias:
      - tela/carregamento/estilo.py:362-365
  - id: persistencia_atomica
    onde: persistir_configuracao_estilo (tempfile + fsync + os.replace)
    origem: H-0061
    evidencias:
      - tela/carregamento/estilo.py:257-297
      - tela/carregamento/estilo.py:372
  - id: publicacao_global
    onde: troca unica de _EstadoEstiloRuntime.global_vigente apos persistir
    origem: H-0061
    evidencias:
      - tela/carregamento/estilo.py:374-380
  - id: promocao_baseline
    onde: mesma troca atomica (baseline := documento)
    origem: H-0061
    evidencias:
      - tela/carregamento/estilo.py:375-379
  - id: sincronizacao_candidato_runtime
    onde: mesma troca (candidato := documento == nova baseline)
    origem: H-0061
    evidencias:
      - tela/carregamento/estilo.py:375-379
  - id: fail_closed
    onde: EstiloErro antes/durante persistir; baseline/global/arquivo intactos
    origem: H-0061
    evidencias:
      - tela/teste_loader.py (testes nominais H-0061 de sucesso e falha)
  - id: solicitacao_imutavel_retida
    onde: SolicitacaoAplicacaoEstilo + slot estado["solicitacao_aplicacao_estilo"]
    origem: H-0066 / H-0067
    evidencias:
      - tela/estilo.py:95-110
      - demo/demo.py:866-881
  - id: reconciliar_selecoes_com_candidato
    onde: ControladorTelaEstilo.reconciliar_selecoes_com_candidato
    origem: H-0065
    nota: metodo ja existe; H-0068 apenas precisa chama-lo apos sucesso
    evidencias:
      - tela/estilo.py:346-358
  - id: ramo_confirmado_abortado
    onde: consumo modal do popup de confirmacao de estilo
    origem: H-0067
    evidencias:
      - demo/demo.py:866-882
```

## capacidades_novas

```yaml
capacidades_novas:
  - id: consumir_solicitacao_confirmada
    descricao: >
      No ramo CONFIRMADO, ler exclusivamente
      estado["solicitacao_aplicacao_estilo"].candidato (nunca runtime.candidato).
  - id: expor_caminho_destino
    descricao: >
      Acessor publico somente-leitura em EstadoEstiloRuntime para
      caminho_base/config/estilo.json (expor o que ja e usado internamente;
      nao nova logica de persistencia).
  - id: chamar_aplicar_candidato
    descricao: >
      Uma chamada a primitiva H-0061 com o snapshot confirmado e o destino real.
  - id: sincronizar_estado_estilo
    descricao: >
      Apos sucesso, atribuir novo["estilo"] = materializacao retornada, para
      que os renderers (que leem estado["estilo"], nao global_vigente) usem
      imediatamente a nova materializacao (R-4 / ADR-0046 §8.4).
  - id: reconciliar_selecoes_pos_sucesso
    descricao: >
      Chamar reconciliar_selecoes_com_candidato ja existente apos sucesso.
  - id: limpar_solicitacao
    descricao: >
      Remover estado["solicitacao_aplicacao_estilo"] em sucesso e em falha
      (tentativa consumida; sem retry automatico).
  - id: capturar_estilo_erro_no_dispatch
    descricao: >
      Tratar EstiloErro na camada de sessao/demo sem propagar ao loop
      principal; sem literal novo e sem popup de erro.
```

## responsabilidades_excessivas

```yaml
responsabilidades_excessivas: []
notas:
  - >
    A enumeracao documental de validar→persistir→publicar→baseline no
    objetivo de H-0068 descreve efeitos da primitiva preexistente, nao
    responsabilidades novas a implementar. O proprio H-0068 §5 ja declara
    isso como conclusao normativa.
  - >
    Sincronizar estado["estilo"] e capturar EstiloErro sao pontos de glue
    obrigatorios no mesmo evento, nao politicas independentes (sem retry,
    sem segundo modal, sem transicao de tela nova).
  - >
    Demonstracao integrada com override local permanece fora de escopo
    (ADR-0046 §5) e nao deve ser puxada para esta fatia.
```

## escopo_minimo_recomendado_H0068

```yaml
escopo_minimo_recomendado_H0068:
  - Expor acessor de destino em EstadoEstiloRuntime.
  - Acrescentar em ControladorTelaEstilo orquestracao minima:
      extrair solicitacao.candidato → aplicar_candidato(destino) →
      reconciliar_selecoes_com_candidato.
  - Estender o ramo CONFIRMADO existente em demo/demo.py (~868-882):
      chamar a orquestracao; em sucesso sincronizar estado["estilo"] e
      limpar solicitacao; em EstiloErro limpar solicitacao sem propagar.
  - Manter ABORTADO exatamente como H-0067.
  - Atualizar somente as assercoes de H-0067 superadas pelo novo efeito
    pos-CONFIRMADO (§16 do handoff).
  - Nao reimplementar persistencia/publicacao/baseline/fail-closed.
```

## capacidades_para_handoffs_posteriores

```yaml
capacidades_para_handoffs_posteriores:
  - id: demonstracao_integrada_com_override_local
    origem: ADR-0046 §5
    status: ja_registrada_como_fronteira_posterior_de_H0068
    nota: >
      Nao e decomposicao de H-0068; e capacidade remanescente do ITEM-0010.
      Numeracao fica a criterio do gerente (nenhum H-0069 criado aqui).
  - id: popup_erro_visual_falha_persistencia
    status: explicitamente_fora_de_escopo_em_H0068
    nota: so se o gerente decidir enderecar feedback visual de falha.
```

## arquivos_minimos

```yaml
arquivos_minimos:
  implementacao:
    - path: tela/carregamento/estilo.py
      motivo: acessor publico do destino real (extensao pontual)
    - path: tela/estilo.py
      motivo: orquestracao a partir da solicitacao confirmada
    - path: demo/demo.py
      motivo: consumir CONFIRMADO no ramo existente + sincronizar estado["estilo"]
  testes:
    - path: tela/teste_estilo_h0068.py
      motivo: orquestracao no controlador (sucesso/falha/snapshot)
    - path: demo/teste_demo_estilo_h0068.py
      motivo: E2E Enter/Aplicar → Confirmar + sync estado["estilo"]
    - path: demo/teste_demo_estilo_h0067.py
      motivo: somente reestruturar as 3 assercoes superadas pos-CONFIRMADO
    - path: tela/teste_loader.py
      motivo: opcional e focal — so o acessor de caminho; nao retestar aplicar_candidato
  relatorio:
    - path: docs/relatorios/IMP-0068-persistencia-publicacao-estilo-confirmado.md
arquivos_autorizados_nao_necessarios_alem_do_minimo: []
nota: >
  A lista autorizada do H-0068 §18 ja coincide com o minimo. Nenhum arquivo
  adicional e necessario para a menor fatia.
```

## testes_minimos

```yaml
testes_minimos:
  regressoes_primitiva_H0061_ja_existentes:
    - tela/teste_loader.py::test_h0061_demonstracao_sucesso_persistencia_antes_publicacao
    - tela/teste_loader.py::test_h0061_falha_persistencia_preserva_global_baseline_e_candidato
    regra: >
      Nao reimplementar nem reassertar exaustivamente o interior de
      aplicar_candidato; manter intactos salvo adicao focal do acessor.
  novos_testes_orquestracao_H0068:
    - sucesso E2E a partir de CONFIRMADO real (arquivo + estado["estilo"] +
      aplicar_disponivel False + selecoes reconciliadas + solicitacao ausente)
    - ABORTADO / ausencia de solicitacao → no-op (sem persistir)
    - uso exclusivo de solicitacao.candidato (snapshot)
    - falha injetada em persistir_configuracao_estilo → fail-closed de sessao
      (captura EstiloErro, solicitacao removida, candidato disponivel,
      estado["estilo"] intacto)
    - atualizacao nominal das 3 assercoes de demo/teste_demo_estilo_h0067.py
      identificadas em H-0068 §16
```

## acao_recomendada

```yaml
acao_recomendada:
  - MANTER_HANDOFF
razao: >
  H-0068 ja esta escrito como orquestracao sobre uma unica primitiva
  aprovada. Nao ha responsabilidade material nova independente que justifique
  PATCH_HANDOFF_PARA_REDUZIR nem DIVIDIR_ANTES_DE_IMPLEMENTAR. A unica
  capacidade remanescente do ITEM-0010 (demonstracao integrada) ja esta
  corretamente fora do escopo.
```

## bloqueios

```yaml
bloqueios: []
```

## Evidência de código (somente leitura)

```text
aplicar_candidato (H-0061) — uma operacao:
  validar → persistir → [publicar + baseline + candidato] em uma troca

demo/demo.py ~868-882 — CONFIRMADO ainda so retém solicitacao:
  # CONFIRMADO: solicitacao permanece retida para etapa posterior.

estado["estilo"] — copiado adiante; nao sincronizado apos publicacao:
  novo["estilo"] = estado["estilo"]  (demo/demo.py ~833-834)
  renderers leem estado["estilo"]

ControladorTelaEstilo — sem metodo de aplicacao definitiva; ja possui
  solicitar_aplicacao, conteudo_popup_confirmacao,
  reconciliar_selecoes_com_candidato.
```

Nenhum código foi alterado. Nenhum handoff posterior foi criado. Stage/commit/push não realizados.
