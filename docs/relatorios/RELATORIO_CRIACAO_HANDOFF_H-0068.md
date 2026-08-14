# Relatório — Criação do Handoff H-0068

```yaml
rastreabilidade:
  etapa: CRIAR_HANDOFF
  objeto: H-0068
  item: ITEM-0010
  adr: ADR-0046
  predecessor: H-0067
```

## Análise da aplicação definitiva

```yaml
analise_aplicacao:
  entrada_confirmada: >
    resultado == CONFIRMADO (H-0067, popup_resultado.status) mais
    SolicitacaoAplicacaoEstilo retida em estado["solicitacao_aplicacao_estilo"],
    slot ja deixado por H-0067 (demo/demo.py:1257-1260, preservado entre
    comandos em demo/demo.py:799-806).
  snapshot: >
    Consumir exclusivamente solicitacao.candidato (dataclass frozen,
    copias profundas desde H-0066 __post_init__). Nunca reler
    runtime.candidato como fonte, mesmo coincidindo na pratica, porque a
    aplicacao ocorre no mesmo evento de tecla que fecha o popup com
    CONFIRMADO (nenhuma tecla intermediaria e alcancavel).
  validacao: >
    Ja coberta pela primeira etapa interna de aplicar_candidato
    (materializar_estilo_local), que valida o documento completo antes de
    qualquer escrita. Nenhuma segunda validacao duplicada.
  persistencia: >
    Ja implementada e testada por H-0061: persistir_configuracao_estilo
    escreve em arquivo temporario no mesmo diretorio, fsync, os.replace
    atomico; arquivo anterior intocado em falha
    (tela/carregamento/estilo.py:257-297).
  publicacao: >
    Ja implementada por H-0061: uma unica troca de _EstadoEstiloRuntime
    (baseline=candidato, candidato=candidato, global_vigente=materializacao)
    imediatamente apos persistencia bem-sucedida, dentro da mesma chamada
    de aplicar_candidato (tela/carregamento/estilo.py:362-380).
  ordem: >
    validar -> persistir -> [publicar+baseline+candidato como uma unica
    troca atomica]. Literal de ADR-0046 par. 8 ("persistencia -> troca do
    estilo global e obrigatoria") e ja implementada exatamente assim por
    aplicar_candidato. Nao ha ordem alternativa materialmente plausivel;
    nao e BLOCKED_DOCUMENTATION.
  fail_closed: >
    Ja testado por H-0061 (tela/teste_loader.py:4643-4707): falha antes da
    persistencia nao muda nada; falha durante a persistencia preserva
    arquivo/baseline/global anteriores e mantem candidato disponivel
    (igual ao documento tentado); persistencia bem-sucedida nao tem janela
    de falha posterior porque a troca em memoria e uma unica atribuicao de
    objeto Python sem I/O intermediario.
  rollback: >
    Nao e necessario mecanismo de duas fases: a publicacao em memoria so
    ocorre depois que a escrita do arquivo ja terminou com exito, portanto
    nao existe intervalo em que ambos precisassem ser revertidos juntos.
    H-0061 ja e suficiente; nenhuma lacuna tecnica registrada.
  baseline: >
    baseline_nova := candidato_confirmado, somente apos sucesso completo,
    como parte da mesma troca atomica que publica o global. Nunca
    antecipada.
  candidato_selecoes: >
    Apos sucesso: candidato do runtime sincronizado com a nova baseline
    (por aplicar_candidato); estado["selecoes"] deve ser reconciliado
    explicitamente via reconciliar_selecoes_com_candidato ja existente
    (tela/estilo.py:346-358), no mesmo evento.
  solicitacao_sucesso: >
    Removida de estado apos aplicacao integral concluida, para impedir
    reaplicacao acidental de uma confirmacao ja consumida.
  solicitacao_falha: >
    Removida (descartada), identico ao tratamento ja existente para
    ABORTADO. Nao ha autoridade para retry automatico da mesma
    solicitacao; nova tentativa exige novo Enter/Aplicar -> popup ->
    Confirmar, o que produz uma SolicitacaoAplicacaoEstilo nova.
  estado_tela_sucesso: >
    Permanece na tela de Estilo (_ID_TELA_H0063); Aplicar fica inativo;
    selecoes refletem a nova baseline; F4 defensivo (reabertura) cria novo
    candidato a partir da baseline ja promovida.
  estado_tela_falha: >
    Permanece na tela de Estilo; Aplicar continua ativo (candidato ainda
    diverge da baseline inalterada); nenhum popup de erro novo e criado
    (sem autoridade para inventar um nesta fatia).
  literais_resultado: >
    Nenhum literal novo autorizado. Sucesso = retorno normal de
    aplicar_candidato (EstiloResolvido) mais estado observavel coerente;
    falha = EstiloErro (mecanismo estrutural ja existente em todo o
    modulo), capturada na camada de orquestracao sem propagar ao loop
    principal.
  suficiencia_documental: >
    Todas as perguntas tem resposta na ADR-0046, no contrato_estilo.md
    §3.8/R-1/R-4/R-9..R-13 e, principalmente, na primitiva ja
    implementada e testada aplicar_candidato (H-0061). O unico ponto de
    engenharia genuinamente novo e a orquestracao fina de estado de sessao
    (sincronizar estado["estilo"], reconciliar selecoes, limpar a
    solicitacao) e a exposicao publica minima do caminho de destino real,
    ambos derivaveis da arquitetura existente sem ambiguidade.
  encerramento_funcional: AINDA_REQUER_HANDOFF_POSTERIOR
```

## Achados centrais

**A primitiva de aplicação já existe e já é testada.**
`EstadoEstiloRuntime.aplicar_candidato(candidato, caminho_destino)`
(`tela/carregamento/estilo.py:362-380`), entregue por H-0061, já implementa
integralmente validar → persistir (atômico) → publicar/baseline/candidato
(troca atômica única), com fail-closed comprovado por
`tela/teste_loader.py:4643-4707`. H-0068 não cria segundo mecanismo de
persistência ou publicação: sua única responsabilidade nova legítima é a
orquestração — extrair o candidato do snapshot confirmado, chamar essa
primitiva com o destino real, e manter o estado de sessão coerente.

**Gap de acesso ao destino real.** `EstadoEstiloRuntime` guarda a raiz
resolvida em `self._caminho_base` (privado); nenhum módulo hoje expõe
publicamente o caminho de `config/estilo.json` derivado dela. H-0068
autoriza uma extensão pontual mínima em `tela/carregamento/estilo.py`
(acessor somente-leitura), sem criar lógica nova — apenas expor o que a
primitiva já usa internamente.

**Gap de sincronização de `estado["estilo"]`.** `demo/demo.py` mantém dois
objetos de estilo: `estado["estilo_runtime"]` (gerido por H-0061) e
`estado["estilo"]`, que é o objeto efetivamente lido por todos os
renderers e nunca é atualizado depois da carga inicial em `main()`. Sem
sincronizar explicitamente esse segundo slot após `aplicar_candidato`, o
requisito de R-4 ("consumidores passam a usar imediatamente a nova
materialização") não se cumpriria de fato, apesar de arquivo e
`global_vigente` estarem corretos. Isso foi identificado por inspeção de
código e registrado como acréscimo obrigatório do handoff.

**Ordem operacional resolvida sem ambiguidade.** ADR-0046 §7 descreve
`CONFIRMADO` e a aplicação bem-sucedida como uma única linha da tabela de
transições, e §8 descreve os passos como consequência direta do mesmo
caminho `CONFIRMADO`. H-0068 estende o mesmo evento de tecla que hoje só
retém a solicitação (H-0067), eliminando por construção qualquer janela em
que o candidato mutável pudesse divergir do snapshot confirmado.

**Testes predecessores nominalmente identificados.** Em
`demo/teste_demo_estilo_h0067.py`, três testes afirmam literalmente
ausência de persistência/publicação especificamente no cenário pós-
`CONFIRMADO`: `test_enter_popup_produz_confirmado_retendo_solicitacao`,
a sub-sequência pós-`CONFIRMADO` de `test_fronteiras_apos_confirmado_e_abortado`
e a seção final de `test_demonstracao_non_tty_ciclo_confirmacao`. Somente
essas asserções são autorizadas a mudar; as garantias equivalentes para
`ABORTADO` permanecem intocadas em todos os três.

## Resultado

```yaml
resultado:
  status: HANDOFF_CREATED
  handoff:
    docs/handoff/H-0068-persistencia-publicacao-estilo-confirmado.md
  capacidade:
    - validacao_do_snapshot_confirmado
    - persistencia_via_aplicar_candidato
    - publicacao_via_aplicar_candidato
    - sincronizacao_de_estado_estilo
    - promocao_da_baseline
    - reconciliacao_candidato_selecoes
    - limpeza_da_solicitacao
    - fail_closed_reutilizado_de_h0061
  arquivos_implementacao_autorizados:
    - tela/carregamento/estilo.py (extensao pontual: acessor publico do
      destino real de config/estilo.json)
    - tela/estilo.py (orquestracao da aplicacao a partir da solicitacao
      confirmada)
    - demo/demo.py (extensao do ramo CONFIRMADO/ABORTADO ja existente;
      sincronizacao de estado["estilo"])
    - tela/teste_estilo_h0068.py
    - demo/teste_demo_estilo_h0068.py
    - tela/teste_loader.py (somente teste focal do novo acessor, se criado)
    - docs/relatorios/IMP-0068-persistencia-publicacao-estilo-confirmado.md
  testes_requeridos:
    - sucesso completo (arquivo, baseline, global, estado["estilo"],
      selecoes, aplicar_disponivel, solicitacao consumida)
    - abortado/ausente sem efeito
    - snapshot confirmado exclusivo (nunca candidato mutavel posterior)
    - falha de persistencia fail-closed
    - arquivo e publicacao semanticamente corretos multi-categoria
    - regressao integral de H-0063/H-0064/H-0065/H-0066 e dos testes de
      popup, com atualizacao nominal dos tres testes de H-0067 identificados
    - suite completa
  fora_de_escopo:
    - demonstracao integrada com override local (ADR-0046 §5)
    - novo popup de erro visual
    - politica de retry automatico da solicitacao
    - segundo mecanismo de persistencia/publicacao
    - tiling, cor_inativo, cor_alerta, indicadores.concluido
    - ITEM-0024, ITEM-0032, F1, F11, F2, F3, F5
  bloqueios: []
```

## Encerramento da cadeia

`H-0068` **não** é o último handoff funcional do `ITEM-0010`. Após sua
implementação, resta exclusivamente a demonstração integrada com override
local (Cabeçalho + Console + Dashboard + Barra de Menus, ADR-0046 §5),
explicitamente adiada por H-0065 §22, H-0066 §15 e H-0067 §13, e ainda não
implementada por nenhum handoff aprovado até aqui. A numeração desse
handoff posterior fica a critério do gerente; nenhum H-0069 é criado por
esta etapa.

## Git — verificação (somente leitura)

```text
branch: master
HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
git diff --cached --name-only: (vazio)
```

Stage permaneceu vazio durante toda a execução desta etapa. Nenhum
arquivo além dos dois listados em `resultado.handoff` e deste próprio
relatório foi criado ou alterado.
