# H-0067 — Confirmação da aplicação do estilo

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0067
data_criacao: 2026-08-12
status: READY_FOR_IMPLEMENTATION
predecessor: H-0066
relacao: continuacao_funcional
historico:
  H-0061:
    estado: aprovado
    capacidade:
      - baseline
      - candidato
      - primitivas_runtime
      - infraestrutura_de_persistencia_publicacao_para_etapa_posterior
  H-0063:
    estado: aprovado
    capacidade:
      - tela_normal_estilo
      - navegacao_dois_niveis
      - barra_de_menus
      - F4
      - Esc
  H-0064:
    estado: aprovado
    capacidade:
      - amostras_visuais
  H-0065:
    estado: aprovado
    capacidade:
      - candidato_fonte_semantica
      - selecoes_projeta_candidato
      - descarte_na_saida_sem_confirmacao
  H-0066:
    estado: I1_IMPLEMENTATION_APPROVED
    capacidade:
      - Aplicar_sempre_presente
      - aplicar_disponivel_derivado
      - Enter_contextual
      - SolicitacaoAplicacaoEstilo_imutavel
dependencias:
  - H-0061
  - H-0063
  - H-0065
  - H-0066
item_0010:
  estado: em_andamento
fronteira_posterior:
  - persistencia
  - publicacao
  - atualizacao_da_baseline_confirmada
```

H-0067 é continuação funcional de H-0066, não substituição. `SolicitacaoAplicacaoEstilo`,
`aplicar_disponivel`, o protocolo atômico de `Espaço` (H-0065), a tela normal e a
navegação `dois_niveis_por_foco` (H-0063) permanecem integralmente vigentes.
H-0062 permanece histórico/substituído e não é reaberto; é citado apenas como
precedente histórico já declarado por H-0066 (chip `[⏎] Aplicar` — não é
autoridade normativa para este handoff).

## 2. Objetivo exclusivo

Especificar e autorizar a fatia:

```text
CONFIRMAÇÃO DA APLICAÇÃO DO ESTILO
```

Fronteira normativa desta capacidade:

```text
SolicitacaoAplicacaoEstilo (produzida por H-0066)
→ popup de confirmação
→ usuário decide (Enter/Confirmar ou Esc/Voltar)
→ resultado estrutural da decisão
→ H-0067 termina
```

A entrada é exclusivamente a `SolicitacaoAplicacaoEstilo` já produzida por
H-0066. A saída é exclusivamente a decisão de confirmação ou
cancelamento/volta, segundo o contrato genérico de pop-up (`status:
CONFIRMADO` ou `status: ABORTADO`).

H-0067 **não**:

- persiste `config/estilo.json`;
- atualiza a baseline persistida;
- publica o candidato como estilo global;
- executa a aplicação definitiva;
- abre demonstração integrada (Cabeçalho + Console + Dashboard + Barra sob
  override local) — essa capacidade da ADR-0046 §5 permanece deliberadamente
  fora desta partição e não é numerada aqui;
- cria um segundo sistema de pop-up ou reabre a tela de seleção (`ITEM-0010`
  §8 do estado transportado).

Essas ações ficam para handoff(s) posteriores, a decidir pelo gerente.

## 3. Compatibilidade com ADR-0046

A ADR-0046 §6/§7 descreve o pop-up de confirmação como abrindo *sobre a
demonstração integrada*. O particionamento incremental já usado por H-0061,
H-0063, H-0065 e H-0066 divide essa etapa combinada da ADR em partições
menores; H-0066 já cobriu "acionar Aplicar → solicitação estrutural" sem
demonstração nem pop-up. Este handoff cobre exclusivamente "solicitação →
decisão de confirmação", também sem demonstração integrada — que continua
não numerada, a critério do gerente, como já ocorreu nas fronteiras
posteriores de H-0063/H-0065/H-0066.

Como a demonstração integrada com override local ainda não existe, o pop-up
desta capacidade abre sobre a **tela de Estilo já ativa** (a mesma tela onde
`Enter/Aplicar` foi acionado), reutilizando o conceito genérico de "tela
ativa" do contrato de pop-up (`docs/contratos/contrato_popup.md` §2), e não
sobre uma tela de demonstração que este handoff não cria. Isso não contradiz
a ADR: a ADR não fixa handoff nem exige que a demonstração exista antes da
confirmação poder ser particionada; apenas descreve o fluxo completo
combinado. Não há conflito material que exija `BLOCKED_DOCUMENTATION`.

Diferença documental obrigatória:

| Capacidade | Papel |
|---|---|
| AÇÃO APLICAR (H-0066) | Detectar divergência, expor/habilitar a ação, receber o acionamento, produzir a solicitação/transição para confirmação |
| CONFIRMAÇÃO DA APLICAÇÃO (H-0067) | Apresentar a decisão ao usuário sobre a `SolicitacaoAplicacaoEstilo`; devolver `CONFIRMADO` ou `ABORTADO`; reter ou descartar a solicitação conforme a decisão |
| Demonstração integrada (posterior, não numerada) | Cabeçalho + Console + Dashboard + Barra sob override local do candidato |
| Persistência/publicação (posterior, não numerada) | Somente após `CONFIRMADO`, na ordem fail-closed da ADR |

## 4. Autoridade

Lidas integralmente:

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`
- `docs/handoff/H-0066-acao-aplicar-candidato-estilo.md`
- `docs/handoff/H-0061-infraestrutura-estilo-runtime.md`
- `docs/adr/ADR-0044-popup-modal-generico-de-decisao.md`
- `docs/contratos/contrato_popup.md` (inclusive §9.1, já vigente e específico
  para este uso)
- `docs/nomenclatura/35_POPUP.md` (inclusive §6.1, já vigente)
- `docs/contratos/contrato_barra_de_menus.md` §10.1, §11 (precedência do
  console focado; não redefine `[⏎]` fora de Estilo)

Lidas focalmente:

- `docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md`
- `docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md`
- `docs/handoff/H-0056-popup-basico-exibicao-voltar.md`
- `docs/handoff/H-0057-popup-geometria-dinamica-wrapping-resize.md`
- `docs/handoff/H-0059-popup-confirmacao-binding-integracao-decisao.md`
  (precedente técnico do binding `CONFIRMADO`/`ABORTADO`, hoje restrito a
  `tipo: marcacao` — ver §6.1)
- `docs/adr/ADR-0045-resize-responsivo-formacoes-popup-marcacao.md`

Consultado apenas como precedente histórico já declarado por H-0066 (não
autoridade normativa, não reaberto):

- `docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md`

Código inspecionado somente para pontos de integração (sem alteração nesta
etapa):

- `tela/renderizacao/popup.py` — `validar_declaracao_popup`, `_validar_chip`,
  `consumir_tecla_popup`, `_confirmar_marcacao`, `abrir_popup`,
  `geometria_popup`, `renderizar_popup`, `sobrepor_no_corpo`.
- `tela/estilo.py` — `ControladorTelaEstilo.solicitar_aplicacao`,
  `SolicitacaoAplicacaoEstilo`.
- `demo/demo.py` — ramificação modal (linhas ~860–872), tratamento de
  `Enter/Aplicar` na tela H-0063 (linhas ~1173–1190), renderização com
  `popup=` (linha ~1344).
- `tela/renderizacao/tela.py` — encaminhamento de `popup` a
  `sobrepor_no_corpo` (já genérico, parâmetro `popup=None` existente).
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` —
  ausência atual de campo `popups`.

## 5. Matriz documental obrigatória

### A. Tipo do popup

| Pergunta | Classificação | Determinação |
|---|---|---|
| Existe tipo canônico de popup de aplicação? | DETERMINADO_PELA_AUTORIDADE | `contrato_popup.md` §9.1 e `35_POPUP.md` §6.1 já declaram nominalmente "Confirmação de aplicação de estilo (ADR-0046)" como consumidor do sistema genérico, `tipo: texto`. Não é novo tipo de pop-up. |
| É popup centralizado sobre a tela atual? | DETERMINADO_PELA_AUTORIDADE | `contrato_popup.md` §4/§9.1: centralizado na área física do corpo da tela ativa (a tela de Estilo, já aberta — ver §3 acima), preservando o máximo possível dela visível. |
| Possui borda/título/texto/chips declarativos? | DETERMINADO_PELA_AUTORIDADE | Estrutura obrigatória de qualquer declaração de `popups[ID]` (`contrato_popup.md` §3.1/§4/§9; `tela/renderizacao/popup.py:_CAMPOS_POPUP`). |
| Há infraestrutura já implementada por handoffs anteriores? | DERIVAVEL_DA_INFRAESTRUTURA_VIGENTE | Sim, integralmente: `tela/renderizacao/popup.py` (H-0056–H-0060), binding modal em `demo/demo.py` (H-0059), encaminhamento genérico em `tela/renderizacao/tela.py`. Reutilizar sem criar segundo sistema. |

**Achado que precisa ser registrado (não é conflito normativo, é lacuna de
implementação já resolvida pela autoridade):** o código atual de
`tela/renderizacao/popup.py` **rejeita** declarações `tipo: texto` com chip
`Enter`: `validar_declaracao_popup` levanta `PopupErro("popup textual nao
aceita regra de confirmacao")` quando `tipo == "texto"` e há `chips_enter`; e
`consumir_tecla_popup` só despacha teclas de marcação/confirmação quando
`declaracao.get("tipo") == "marcacao"`, retornando `None` para `Enter` em
popups textuais. Essa restrição foi escrita durante H-0059, cujo próprio
texto já registrava isso como escopo daquela etapa ("os pop-ups textuais
demonstrativos continuam sem contrato de payload confirmado **nesta
etapa**"), não como fronteira arquitetural permanente. `contrato_popup.md`
§9.1 (já vigente, já aplicado ao repositório) e `ADR-0046` §6.4 exigem
exatamente o oposto para este uso: um pop-up `tipo: texto` que devolve
`CONFIRMADO`. Não há ambiguidade na autoridade — o código é que ainda não
foi estendido. Portanto isto **não bloqueia** H-0067; é um item obrigatório
da lista de arquivos autorizados (§7) e não constitui criação de novo
sistema de pop-up, apenas generalização pontual do já existente (mesmo
padrão de `_confirmar_marcacao`, aplicado a `tipo: texto`, sem `valor`).

### B. Conteúdo

| Item | Classificação | Determinação |
|---|---|---|
| Título | DETERMINADO_PELA_AUTORIDADE (existência) + margem aberta (texto literal) | Campo obrigatório (`contrato_popup.md` §4/§9.1). O texto exato não é fixado: "Esta ADR não fixa literal específico para a pergunta nem para os rótulos dos chips quando o contrato aplicável não exigir literalidade" (ADR-0046 §6). Implementação deve escolher um título curto, de domínio (aplicação de estilo), sem símbolo/preset hardcoded. |
| Pergunta/mensagem | DETERMINADO_PELA_AUTORIDADE (natureza) + margem aberta (texto literal) | `tipo: texto`, pergunta se o estilo (candidato/solicitação) deve ser aplicado (ADR-0046 §6.2). Texto literal não fixado pela autoridade; não deve ser inventado como se fosse normativo — registrar como margem de implementação. |
| Resumo do candidato no texto | NAO_EXIGIDO_PELA_AUTORIDADE | Nenhuma autoridade exige listar os quatro presets no texto do pop-up. A ADR fala em pop-up textual simples perguntando pela aplicação do "estilo demonstrado"; como H-0067 não abre demonstração (§3), não há necessidade nem mandato de resumo. Implementação pode manter o texto genérico; não é obrigada a serializar `SolicitacaoAplicacaoEstilo` no texto. |
| Chips de ação | DETERMINADO_PELA_AUTORIDADE + margem operacional fechada | Um chip `Esc` (`ABORTADO`) e um chip `Enter` (`CONFIRMADO`), conforme `contrato_popup.md` §9/§9.1. O texto do chip `Esc` deve ser literalmente `"Voltar"` e o do chip `Enter` literalmente `"Confirmar"` — não porque a ADR exija esses literais exatos (ADR-0044 permite rótulos como `[Enter] Aplicar`/`[Enter] Executar`), mas porque `tela/renderizacao/popup.py:_validar_chip` **hoje** exige exatamente esses dois literais para qualquer pop-up (`"o chip Esc demonstrativo deve ter texto 'Voltar'"` / `"'Confirmar'"`). Manter esses literais evita generalizar essa validação sem necessidade; é a opção de menor diff compatível com a infraestrutura vigente. |
| Ordem dos chips | DERIVAVEL_DA_INFRAESTRUTURA_VIGENTE | `Esc`/Voltar antes de `Enter`/Confirmar, seguindo o padrão já declarado por H-0059 §7 ("acrescentar um chip específico de Enter, na ordem declarada depois do chip de aborto"). |

### C. Enter

| Pergunta | Classificação | Determinação |
|---|---|---|
| Qual ação Enter executa? | DETERMINADO_PELA_AUTORIDADE | Confirma a aplicação; produz `status: CONFIRMADO` sem `valor` (pop-up `tipo: texto` não tem itens/marcação — `contrato_popup.md` §9). |
| A opção positiva é Aplicar/Confirmar? | DETERMINADO_PELA_AUTORIDADE | Sim, semanticamente "aplicar o estilo demonstrado" (ADR-0046 §6.2); rótulo do chip é `"Confirmar"` (ver §5.B). |
| Há foco entre ações ou Enter é fixo? | DERIVAVEL_DA_INFRAESTRUTURA_VIGENTE | Fixo. Pop-up `tipo: texto` não tem cursor navegável entre chips (isso só existe para itens de `marcacao`); `Enter` sempre resolve contra a regra de confirmação declarada, `Esc` sempre aborta. Não há alternância de foco entre os dois chips. |

### D. Esc

| Pergunta | Classificação | Determinação |
|---|---|---|
| Esc significa Voltar/cancelar? | DETERMINADO_PELA_AUTORIDADE | Sim; produz `status: ABORTADO`, sem payload (`contrato_popup.md` §9). |
| Fecha o popup e retorna à tela de Estilo? | DETERMINADO_PELA_AUTORIDADE | Sim — a tela subjacente é a própria tela de Estilo (§3), que permanece materializada durante a abertura (`contrato_popup.md` §2) e volta a receber interação ao fechar. |
| Preserva candidato ao voltar? | DETERMINADO_PELA_AUTORIDADE | Sim, integralmente: ADR-0046 §7, linha `ABORTADO`: "encerra a demonstração, retorna à seleção, preserva integralmente o candidato e não altera persistência nem estilo global." |
| Não deve executar a regra H-0065 de descarte da visita | DETERMINADO_PELA_AUTORIDADE | Correto e obrigatório. O descarte de H-0065 (§12.2 daquele handoff) é acionado apenas por **saída efetiva** da tela de Estilo (Esc no nível dos pais com efeito de sair/retornar pela pilha). O `Esc` consumido pelo pop-up nunca chega ao dispatcher da tela de Estilo (precedência modal, §5.G/§6.11) e não é, por si, uma saída efetiva. As duas camadas de `Esc` (pop-up × tela) não podem ser confundidas. |

### E. Resultado positivo

`CONFIRMADO` produz **somente** o resultado estrutural genérico do pop-up
(`status: CONFIRMADO`, sem `valor`) já definido pelo contrato. O que este
handoff autoriza como efeito observável adicional, exigido pela fronteira
posterior da ADR (persistência → publicação, ainda não implementada):

- a `SolicitacaoAplicacaoEstilo` já produzida por H-0066 permanece
  **retida e íntegra** — não é reconstruída, não é descartada, não é
  mutada — disponível para a etapa posterior consumir;
- nenhuma persistência, publicação ou promoção de baseline ocorre nesta
  fatia;
- baseline, `config/estilo.json` e estilo global permanecem intactos;
- o candidato runtime permanece o estado de edição vigente (não é
  reinicializado por `CONFIRMADO`).

Não se inventa literal de máquina de estados novo (ex.: `PENDING_EXECUCAO`,
`APLICACAO_CONFIRMADA`) para representar "confirmado, aguardando a etapa
posterior": o único literal observável do pop-up continua sendo
`CONFIRMADO`/`ABORTADO` (contrato genérico); a retenção da solicitação é
efeito estrutural, não um novo status.

### F. Resultado negativo

`ABORTADO` produz **somente**:

- popup fecha;
- retorna à tela de Estilo, sem sair dela;
- candidato permanece disponível para edição, sem alteração;
- `Aplicar`/`aplicar_disponivel` continua ativo se o candidato ainda
  divergir da baseline (derivado de `comparar_candidato_baseline`, nunca
  flag independente — H-0066 §5.C, reutilizado sem alteração);
- a `SolicitacaoAplicacaoEstilo` daquela tentativa específica é descartada
  (não persiste como pendência); uma nova tentativa de `Enter/Aplicar`
  produzirá uma nova solicitação, se ainda houver divergência.

### G. Literais

`CONFIRMADO` e `ABORTADO` são `DETERMINADO_PELA_AUTORIDADE`: já definidos
literalmente por `contrato_popup.md` §9/§9.1, `35_POPUP.md` §6/§6.1 e
`ADR-0046` §6.4/§7. Diferente de H-0066 (onde esses literais pertenciam a
uma etapa posterior e não podiam ser antecipados), aqui eles pertencem
exatamente a esta capacidade e devem ser usados tal como definidos. Nenhum
literal adicional é criado por H-0067.

## 6. Regra de bloqueio — conclusão

Todas as perguntas da matriz têm resposta suficiente na autoridade vigente,
combinada com a infraestrutura de pop-up já materializada (H-0056–H-0060) e
com a `SolicitacaoAplicacaoEstilo` já materializada por H-0066. A única
lacuna encontrada (§5.A) é uma restrição de **código**, não de autoridade
documental, e a própria autoridade (`contrato_popup.md` §9.1, já vigente)
resolve inequivocamente qual deve ser o comportamento correto — não há duas
semânticas materialmente plausíveis em aberto. Não há ponto
`NAO_DETERMINADO` que exija `BLOCKED_DOCUMENTATION`. H-0067 é, portanto,
`READY_FOR_IMPLEMENTATION`.

## 7. Especificação funcional adicional

### 7.1 Snapshot e modalidade

O pop-up representa o snapshot da `SolicitacaoAplicacaoEstilo` produzida no
instante do `Enter/Aplicar` (H-0066), não um novo snapshot do candidato
mutável. O envelope de conteúdo (`conteudo_popup`, `tipo: texto`) deve ser
derivado dessa solicitação já recebida — não deve reconsultar
`runtime.candidato` no momento de abrir o popup, mesmo que na prática nesta
janela eles ainda coincidam (nada pode mutar o candidato enquanto a tela
está modalmente bloqueada, ver abaixo). Enquanto o popup estiver aberto, a
tela de Estilo está suspensa para interação (`contrato_popup.md` §2): o
usuário não pode acionar `Espaço`, setas ou qualquer outra mutação do
candidato. Isso já é garantido genericamente pela ramificação modal de
`demo/demo.py` (toda tecla é consumida pelo popup enquanto `estado["popup"]`
existir — H-0059) e deve ser preservada sem redesenho.

### 7.2 Geometria

Reutilizar integralmente a geometria genérica do pop-up (`contrato_popup.md`
§4/§11; `ADR-0044`/`ADR-0045`; `tela/renderizacao/popup.py:geometria_popup`,
`renderizar_popup`, `sobrepor_no_corpo`): centralização no corpo da tela de
Estilo, tamanho intrínseco com wrapping quando exceder a largura do corpo,
espaçamentos `0|1`/`1..5` declarativos, resize via `SIGWINCH` já vigente em
`demo/demo.py`, e `quadro mínimo de terminal pequeno` quando não houver
espaço suficiente. Não criar geometria fixa nem segundo mecanismo de resize
específico da confirmação de estilo.

### 7.3 Chips declarativos

A declaração do pop-up deve residir em `popups[ID]` do JSON estrutural da
tela H-0063 (`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`,
que hoje não declara `popups`), reutilizando a mesma forma de chip validada
por `tela/renderizacao/popup.py:_validar_chip` (`referencia_regra.resultado`
para `ABORTADO`/`CONFIRMADO`, conforme H-0059 §7). Não desenhar chips
hardcoded no renderer; o renderer genérico (`renderizar_popup`) já consome a
declaração.

### 7.4 Falhas internas

Sem autoridade para inventar política nova além da infraestrutura existente:

- **solicitação ausente:** se `Enter/Aplicar` é acionado sem que
  `aplicar_disponivel` seja `True`, `ControladorTelaEstilo.solicitar_aplicacao()`
  já retorna `None` (H-0066, inalterado); nenhum popup deve abrir nesse
  caso — comportamento já coberto e preservado, não uma falha nova de
  H-0067;
- **popup acionado com Aplicar inativo:** não pode ocorrer por construção,
  pois a abertura do popup é consequência direta e no mesmo evento de uma
  solicitação não nula (§8); não há caminho declarativo para abrir o popup
  de confirmação de estilo de outra forma (não há chip/lançador dedicado
  fora do fluxo de `Enter/Aplicar`);
- **snapshot inválido:** `SolicitacaoAplicacaoEstilo` é `frozen` e copia
  profundamente `baseline`/`candidato` no `__post_init__` (H-0066); não há
  caminho para um snapshot estruturalmente inválido chegar ao popup sem que
  H-0066 já tivesse falhado antes. Nenhum tratamento adicional de erro é
  autorizado aqui;
- **geometria não couber:** aplica-se o `quadro mínimo de terminal pequeno`
  já genérico (§7.2); nenhum fallback específico de Estilo.

### 7.5 Barra subjacente e precedência modal

Enquanto o popup estiver aberto, a tela de Estilo (Console e Barra de Menus)
permanece renderizada por baixo (`popup=` já encaminhado por
`tela/renderizacao/tela.py` a `sobrepor_no_corpo`), mas suspensa para
interação: nenhuma tecla chega à Barra, ao Console ou ao dispatcher da tela
de Estilo enquanto `estado["popup"]` existir — a ramificação modal de
`demo/demo.py` (linhas ~860–872) já intercepta e consome toda tecla antes de
qualquer outro dispatch, e essa precedência deve ser preservada sem
alteração. Não há ambiguidade de precedência a resolver.

## 8. Candidato e transição — desenho mínimo autorizado

No mesmo evento atômico em que `Enter/Aplicar` produz uma
`SolicitacaoAplicacaoEstilo` não nula (H-0066, ponto de integração em
`demo/demo.py` ~linha 1185), esse mesmo acionamento deve também abrir a
instância do popup de confirmação declarado em `popups[ID]` da tela H-0063,
com o envelope de conteúdo derivado dessa solicitação. Não introduzir uma
detecção separada, em evento posterior, de "solicitação pendente sem popup
aberto": a transição `Seleção/edição → confirmação` é uma única transição
observável (ADR-0046 §7, linha `Enter/Aplicar` ativo), e produzi-la em dois
passos discretos (solicitar e só depois, num evento futuro, abrir)
reabriria a janela que H-0066 already fecha (nenhum popup nesta fatia) sem
necessidade.

Ao decidir:

- **`ABORTADO`:** fechar o popup (grava `popup_resultado`, limpa
  `estado["popup"]`, já genérico por H-0059); descartar a
  `SolicitacaoAplicacaoEstilo` daquela tentativa (ex.: limpar o campo de
  sessão que a mantinha); preservar candidato, baseline, global e arquivo
  intactos; permanecer na tela de Estilo.
- **`CONFIRMADO`:** fechar o popup; **manter** a `SolicitacaoAplicacaoEstilo`
  retida e íntegra, disponível para a etapa posterior; não persistir, não
  publicar, não promover baseline; permanecer na tela de Estilo, agora
  novamente interativa (o candidato pode voltar a ser editado — se isso
  ocorrer antes de uma etapa posterior consumir a solicitação retida, a
  solicitação retida não deve ser alterada retroativamente, preservando a
  garantia de imutabilidade já provada por H-0066 §13/critério 7).

## 9. Arquivos autorizados para implementação

Lista mínima nominal, decorrente da arquitetura real e do reuso obrigatório
da infraestrutura de pop-up já materializada:

### Infraestrutura de pop-up (extensão pontual, não novo sistema)

- `tela/renderizacao/popup.py` — (a) em `_validar_chip`/`validar_declaracao_popup`,
  substituir a rejeição incondicional de `chips_enter` para `tipo == "texto"`
  por uma validação que aceite um chip `Enter` compatível (mesma exigência
  de `referencia_regra.resultado == {"status": "CONFIRMADO"}` já usada para
  `marcacao`); (b) em `consumir_tecla_popup`, estender o despacho de `\r`/`\n`
  para instâncias `tipo: texto` com regra de confirmação declarada,
  produzindo `{"status": "CONFIRMADO"}` sem `valor` (mesmo padrão de
  `_confirmar_marcacao`, sem lista/ID de item). Preservar integralmente o
  comportamento vigente de `tipo: marcacao` e de `Esc`/`ABORTADO`.

### Declaração e controlador da tela de Estilo

- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` —
  acrescentar o campo `popups` com a declaração do pop-up de confirmação
  (`tipo: texto`, chips `Esc`/`"Voltar"`→`ABORTADO` e
  `Enter`/`"Confirmar"`→`CONFIRMADO`), sem alterar cabeçalho, corpo ou
  barra de menus já vigentes.
- `tela/estilo.py` — acrescentar a capacidade mínima de produzir o envelope
  `conteudo_popup` (`tipo: texto`) a partir de uma `SolicitacaoAplicacaoEstilo`
  já recebida (não reconsultar o candidato mutável), e expor o ID
  estrutural do pop-up declarado, seguindo o padrão já usado por
  `ID_TELA_ESTILO`/`ID_CONSOLE_ESTILO`. Não recriar `SolicitacaoAplicacaoEstilo`,
  não persistir, não publicar.

### Integração de dispatch e render

- `demo/demo.py` — no mesmo ponto onde `Enter/Aplicar` já produz a
  solicitação (H-0066, ~linha 1185), abrir a instância do pop-up de
  confirmação no mesmo evento (§8); tratar `CONFIRMADO`/`ABORTADO` na
  ramificação modal já existente (~linhas 860–872), retendo ou descartando
  a solicitação conforme §8; nenhuma persistência, publicação ou nova tela
  é criada. Não duplicar a ramificação modal genérica (H-0059).

Permanecem, como já valia em H-0063/H-0065/H-0066, fontes/infraestrutura
canônicas a consumir sem alteração: `tela/carregamento/estilo.py`,
`config/estilo.json`, `tela/loader.py`, `tela/navegacao.py`,
`tela/selecao.py`, `tela/renderizacao/tela.py`,
`tela/renderizacao/console.py`, `tela/renderizacao/contexto_execucao.py`,
`tela/renderizacao/barra_menus.py`, `tela/renderizador.py`, e os contratos
vigentes.

### Testes

- `tela/teste_popup.py` — cobertura focal da extensão de `tipo: texto` +
  `Enter`/`CONFIRMADO` em `tela/renderizacao/popup.py` (§9, infraestrutura):
  validação de declaração compatível, `\r`/`\n` equivalentes, ausência de
  `valor` no resultado, regressão de `Esc`/`ABORTADO` para `tipo: texto`,
  regressão integral de `tipo: marcacao`.
- `demo/teste_demo_popup.py` — regressão pura das declarações demonstrativas
  H-0056–H-0059 (`popup_basico`, `popup_texto_dinamico`,
  `popup_lista_exclusiva`, `popup_lista_multipla`); nenhuma delas declara
  `Enter` para `tipo: texto`, portanto não deve haver mudança de
  comportamento observável nelas.
- `tela/teste_estilo_h0067.py` — testes dedicados do envelope de conteúdo
  produzido a partir de `SolicitacaoAplicacaoEstilo`, ausência de
  persistência/publicação/mutação de candidato por essa produção.
- `demo/teste_demo_estilo_h0067.py` — testes de integração ponta a ponta:
  abertura atômica do popup junto da solicitação; `CONFIRMADO` retém a
  solicitação e não persiste/publica; `ABORTADO` descarta a solicitação,
  preserva candidato e `aplicar_disponivel`, sem disparar a regra de
  descarte de saída efetiva de H-0065; modalidade (teclas subsequentes
  enquanto o popup está aberto não alteram candidato/cursor da tela de
  Estilo); resize com popup aberto; ausência de popup quando
  `aplicar_disponivel` é `False`.
- `docs/relatorios/IMP-0067-confirmacao-aplicacao-estilo.md` — relatório
  futuro da implementação.

### Atualização autorizada de expectativas predecessoras "sem popup"

H-0067 supera deliberadamente a expectativa predecessora de H-0066 de que
`Enter/Aplicar` ativo não abre popup nesta capacidade. Autoriza-se atualizar
**somente** as asserções que dependem literalmente dessa ausência,
preservando todas as demais garantias (baseline/global/arquivo intactos,
ausência de `CONFIRMADO`/`ABORTADO` antes de decisão, imutabilidade do
snapshot):

- `demo/teste_demo_estilo_h0066.py`:
  - `test_aplicar_presente_ativo_enter_produz_somente_solicitacao` —
    substituir as asserções `estado.get("popup") is None` /
    `estado.get("popup_resultado") is None` (linhas 140–141) por asserções
    de que o popup de confirmação abriu com a solicitação correspondente;
    preservar as demais asserções (baseline/global/arquivo intactos,
    ausência de `CONFIRMADO`/`ABORTADO` no quadro antes de decisão).
  - `test_fronteiras_apos_enter_aplicar_sem_popup_persistencia_publicacao` —
    o nome e a premissa ("sem popup") ficam superados; reestruturar para
    verificar a fronteira real de H-0067 (popup aberto, mas ainda sem
    persistência/publicação/`CONFIRMADO`/`ABORTADO` até decisão), sem
    enfraquecer as garantias de arquivo/baseline/global intactos e
    candidato não destruído.
  - `test_snapshot_imutavel_apos_mutacao_posterior_via_dispatch` — como o
    popup passa a abrir no mesmo evento do `Enter` (linha ~339), os
    comandos subsequentes do teste (setas/Espaço/Esc, linhas ~346–349), que
    hoje assumem que chegam ao dispatcher normal da tela de Estilo,
    passariam a ser consumidos pelo popup modal. É necessário inserir um
    passo explícito de fechamento do popup (`Esc`/`ABORTADO`, por exemplo)
    antes de continuar a sequência de mutação do candidato, mantendo a
    referência Python já capturada de `solicitacao_1` para provar a mesma
    garantia de imutabilidade de H-0066 após esse fechamento.

Não ampliar outros arquivos "por garantia". Não autorizar alteração de
`tela/carregamento/estilo.py`, `config/estilo.json`,
`tela/teste_estilo_h0063.py`, `tela/teste_estilo_h0065.py`,
`tela/teste_estilo_h0066.py` (nível de controlador — permanece válido sem
mudança, pois `ControladorTelaEstilo.solicitar_aplicacao()` continua sem
abrir popup por si mesma), `demo/teste_demo_estilo_h0063.py`,
`demo/teste_demo_estilo_h0064.py` ou `demo/teste_demo_estilo_h0065.py`, ADR,
contratos, nomenclatura ou backlog nesta implementação — nenhuma dessas
suítes assume abrir popup logo após `Enter` (todas testam cenários sem
`Enter` acionado com `Aplicar` ativo, portanto continuam corretas).

## 10. Testes automatizados mínimos

### Entrada válida

- Com `aplicar_disponivel is True`, acionar `Enter/Aplicar` produz a
  `SolicitacaoAplicacaoEstilo` (H-0066, inalterado) e, no mesmo evento, abre
  a instância do pop-up de confirmação declarado.

### Entrada inválida

- Com `aplicar_disponivel is False`, `Enter/Aplicar` continua no-op (H-0066);
  nenhum popup abre.

### Enter positivo (`CONFIRMADO`)

- Fecha o popup;
- não persiste `config/estilo.json`;
- não publica o estilo global;
- não altera a baseline;
- a `SolicitacaoAplicacaoEstilo` original permanece disponível, íntegra e
  imutável (repetir a prova de H-0066: mutar o candidato depois não altera
  a solicitação já retida).

### Esc/Voltar (`ABORTADO`)

- Fecha o popup;
- retorna à tela de Estilo (mesma tela, `tela_atual` inalterado);
- candidato preservado (não reinicializado à baseline — distinto da saída
  efetiva de H-0065);
- `aplicar_disponivel` continua `True` se o candidato ainda divergir;
- a solicitação daquela tentativa é descartada; um novo `Enter/Aplicar`
  produz uma nova solicitação.

### Modalidade

- Enquanto o popup está aberto, setas/Espaço/outra tecla não navegam nem
  mutam a tela de Estilo (candidato, cursor e `selecoes` inalterados);
  somente o popup consome a tecla.
- A Barra de Menus subjacente não executa ação alguma enquanto o popup
  estiver aberto.

### Snapshot

- O envelope de conteúdo do popup e o resultado da decisão usam a
  `SolicitacaoAplicacaoEstilo` do acionamento original, nunca uma
  reconstrução posterior do candidato.

### Resize

- Popup aberto sobrevive a redimensionamento (largura confortável, largura
  menor ainda suportada, altura reduzida, crescimento após redução),
  preservando a mesma instância lógica (`contrato_popup.md` §11).

### Fronteiras

- Em todo cenário testado (antes da decisão, após `CONFIRMADO`, após
  `ABORTADO`): baseline intacta; `config/estilo.json` intacto; estilo
  global intacto; nenhuma persistência; nenhuma publicação; nenhuma
  promoção de baseline.

### Regressão da infraestrutura de pop-up

- `tipo: marcacao` (H-0056–H-0060) permanece integralmente inalterado:
  navegação, marcação exclusiva/múltipla, confirmação, `ABORTADO`, resize.
- `tipo: texto` sem chip `Enter` declarado (popups demonstrativos
  H-0056/H-0057) continua sem contrato de confirmação, preservando
  H-0059 §2 ("Se `Enter` não estiver declarado... a tecla não confirma").

## 11. Regressões

Exigir regressão integral de H-0063, H-0064, H-0065, H-0066, da
infraestrutura de pop-up (H-0056–H-0060) e da suíte completa, com as
atualizações nominais da §9 para as expectativas "sem popup"
deliberadamente superadas por H-0067. As mudanças predecessoras limitam-se
exatamente aos três testes nominados em `demo/teste_demo_estilo_h0066.py`;
nenhuma outra suíte predecessora assume popup ausente no cenário
especificamente superado (Enter acionado com Aplicar ativo).

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py tela/teste_estilo_h0067.py demo/teste_demo_estilo_h0067.py demo/teste_demo_estilo_h0066.py
```

## 12. Validação manual

Geometria, eventos e estado devem ser provados automaticamente (estado do
runtime, `estado["popup"]`/`popup_resultado`, leitura de
`config/estilo.json`, comparação candidato×baseline). Nenhum requisito
visual novo é introduzido além do já coberto por H-0056–H-0060 (moldura,
título, wrapping, chips), cuja legibilidade já foi validada manualmente
naqueles handoffs. Não é necessário gate TTY humano dedicado a H-0067; se a
implementação concreta alterar a leitura física de teclas de modo que os
testes não consigam comprovar a distinção entre `Enter` e `Esc` do popup
(mesma ressalva já registrada por H-0059 §14), realizar verificação manual
pontual e registrar no relatório de implementação, sem substituir os
testes.

## 13. Fora de escopo

- persistência em `config/estilo.json`;
- publicação de novo estilo global;
- promoção/atualização da baseline persistida;
- demonstração integrada (Cabeçalho + Console + Dashboard + Barra sob
  override local do candidato) e o override local em si;
- preview real do candidato no runtime global;
- criação de novo sistema/tipo de pop-up;
- reabertura da tela de seleção de presets dentro do popup (o popup não
  lista presets nem substitui a navegação H-0063);
- `tiling`, `cor_inativo`, `cor_alerta`, `indicadores.concluido`;
- `ITEM-0024`, `ITEM-0032`;
- F1, F11, F2, F3, F5.

## 14. Critérios de aceite

H-0067 está concluído quando a prova automatizada demonstrar que:

1. `Enter/Aplicar` ativo produz, no mesmo evento, a `SolicitacaoAplicacaoEstilo`
   (H-0066, inalterada) e abre a instância do pop-up de confirmação
   declarado, `tipo: texto`, reutilizando o sistema genérico de pop-up;
2. sem solicitação (Aplicar inativo), nenhum popup de confirmação abre;
3. `Enter/Confirmar` dentro do popup produz `status: CONFIRMADO`, fecha o
   popup, retém a `SolicitacaoAplicacaoEstilo` íntegra e imutável, e não
   persiste, não publica, não altera baseline nem candidato;
4. `Esc/Voltar` dentro do popup produz `status: ABORTADO`, fecha o popup,
   retorna à tela de Estilo (sem executar a regra de descarte de saída
   efetiva de H-0065), preserva o candidato e a elegibilidade de
   `Aplicar` conforme a divergência vigente, e descarta a solicitação
   daquela tentativa;
5. enquanto o popup está aberto, nenhuma tecla alcança a tela de Estilo ou
   sua Barra de Menus subjacente;
6. o popup e seu resultado usam exclusivamente o snapshot da solicitação
   original, nunca uma reconstrução do candidato mutável;
7. resize com popup aberto preserva a mesma instância lógica, sem quebrar
   geometria nem perder estado;
8. a extensão de `tela/renderizacao/popup.py` para `tipo: texto` +
   `Enter`/`CONFIRMADO` não regride `tipo: marcacao` nem os popups
   demonstrativos H-0056/H-0057 sem `Enter` declarado;
9. testes predecessores atualizados apenas nas expectativas "sem popup"
   nominalmente autorizadas (§9), demais garantias preservadas;
10. suíte completa passa.

## 15. Fronteira posterior

Após aprovação de H-0067, a próxima partição do `ITEM-0010` —
persistência em `config/estilo.json`, publicação do novo estilo global e
promoção da baseline confirmada, junto com a eventual demonstração
integrada com override local ainda não numerada — será decidida pelo
gerente. Este documento não numera esse handoff posterior.
