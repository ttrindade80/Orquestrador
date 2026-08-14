# H-0062 — Tela de seleção interativa dos presets de estilo

## 1. Identificação e objetivo

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0062
handoff_posterior: H-0063
estado_documental: ADR_APPLICATION_APPROVED
status: substituido
```

> **Situação:** este handoff foi substituído operacionalmente pelo H-0063
> (`docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md`). O
> H-0062 permanece integralmente preservado como registro histórico, com sua cadeia anterior
> mantida factual e não apagada.

Este handoff autoriza a implementação da tela global de edição dos presets de
estilo, aberta por `F4`. A tela deve editar um candidato em memória, tornar a
divergência contra a baseline observável e entregar o candidato ao fluxo
posterior. A tela não persiste, não publica o estilo global e não abre a
demonstração ou o pop-up do H-0063.

## 2. Estado predecessor

```yaml
predecessor:
  handoff: H-0061
  status: I1_IMPLEMENTATION_APPROVED
  achados: []
  bloqueios: []
```

O H-0061 já entregou baseline persistida, configuração candidata,
materialização local, comparação candidato × baseline, persistência controlada,
publicação global controlada, fail-closed, promoção da baseline e
sincronização do candidato. H-0062 deve consumir essas primitivas; não deve
recriar estado, materialização, escrita ou publicação.

## 3. Capacidade coesa

H-0062 entrega, como uma única capacidade:

- entrada global por `F4`;
- tela global de Estilo com exatamente os pais `borda`, `chip`,
  `indicadores.selecionado` e `indicadores.incluido`;
- filhos derivados em runtime dos respectivos mapas `presets`;
- navegação por `dois_niveis_por_foco`;
- escolha exclusiva do filho corrente por `Espaço`;
- amostras visuais derivadas dos próprios dados dos presets;
- candidato derivado da baseline, edição acumulável e divergência contextual;
- `Enter/Aplicar` ativo somente diante de divergência;
- saída que descarta somente diferenças não confirmadas;
- entrega isolada do candidato ao H-0063.

Não há edição de tiling, cores, `indicadores.concluido` ou outras categorias.

## 4. Estado atual comprovado

### 4.1 Estilo e runtime de H-0061

`tela/carregamento/estilo.py` já fornece `EstiloResolvido` imutável,
`EstadoEstiloRuntime`/`RuntimeEstilo`, `carregar_configuracao_estilo`,
`criar_candidato_estilo`, `definir_preset_candidato`,
`materializar_estilo_local`, `comparar_configuracoes_estilo` e
`persistir_configuracao_estilo`. Os únicos caminhos editáveis do candidato
são `borda.preset_default`, `chip.preset_default`,
`indicadores.selecionado.preset_default` e `indicadores.incluido.preset_default`.
`RuntimeEstilo.aplicar_candidato` já materializa, persiste primeiro e só então
promove baseline, candidato e estilo global.

`tela/loader.py` é a fachada pública dessas primitivas. O H-0062 deve receber
uma instância de `RuntimeEstilo` por injeção e usar suas propriedades e
métodos públicos. Não deve reler `config/estilo.json` a cada render, manter
catálogo próprio, mutar `EstiloResolvido` nem escrever configuração.

### 4.2 Navegação e entrada vigente

`tela/navegacao.py` já implementa `tipo_navegacao_efetivo`,
`estrutura_dois_niveis_valida`, `mover_cima`, `mover_baixo`,
`mover_direita`, `mover_esquerda`, `entrar_nivel_filhos`,
`retornar_nivel_pais`, `em_nivel_filhos`, `console_focado` e os estados dos
chips de navegação. `tela/selecao.py` já implementa a transferência exclusiva
por pai de `dois_niveis_por_foco`, reconciliação e leitura das escolhas.
Esses módulos são infraestrutura vigente e não devem ser redesenhados ou
alterados por H-0062.

`demo/demo.py` mantém o estado de foco, cursor, seleções e telas, usa
`processar_comando` como dispatcher central e `_ler_tecla_sessao` como decoder
único da entrada TTY. A busca focal não encontrou mapa global de funções nem
tratamento de F4 vigente. Sequências desconhecidas hoje são ignoradas; F4
deve ser acrescentado nesse mesmo decoder/dispatcher, com comando canônico
`F4`, sem criar dispatcher paralelo e sem tratar F1, F2, F3, F5 ou F11.

## 5. Arquivos e diretórios autorizados

Somente os caminhos abaixo podem ser criados ou modificados na implementação
de H-0062:

1. `tela/estilo.py` — novo controlador/modelo de edição da tela de Estilo.
2. `tela/renderizacao/estilo.py` — novo renderer de linhas, amostras e
   composição visual específica da tela de Estilo, reutilizando moldura,
   cores, delimitadores e barra canônicos existentes.
3. `tela/renderizacao/contexto_execucao.py` — somente para transportar, como
   contexto efêmero, a disponibilidade de `Aplicar` da tela de Estilo.
4. `tela/renderizacao/barra_menus.py` — somente para avaliar a condição
   contratual `candidato != baseline` no mecanismo de ativo/inativo já
   existente; preservar ordem, layout, cores e regras canônicas.
5. `tela/renderizador.py` — somente para reexportar a entrada pública do
   renderer específico, se necessário à fachada vigente.
6. `demo/demo.py` — integração focal do decoder/dispatcher de F4, ciclo de
   vida da tela H-0062, injeção única de `RuntimeEstilo`, entrega da solicitação
   de aplicação e desvio de renderização para a tela de Estilo.
7. `config/telas/demo/h0062_estilo.json` — shell declarativo mínimo exigido
   pelo loader vigente: cabeçalho, um console, política declarada,
   `barra_de_menus` e chips canônicos. Não pode conter nomes de presets,
   símbolos, delimitadores ou filhos concretos.
8. `tela/teste_estilo.py` — testes automatizados do controlador, modelo
   dinâmico, candidato, amostras e saída.
9. `demo/teste_demo_estilo.py` — testes automatizados do comando canônico F4,
   dispatcher e integração focal sem TTY.
10. `docs/relatorios/IMP-0062-tela-selecao-interativa-presets-estilo.md` —
    relatório obrigatório da implementação futura.

Nenhum diretório é liberado por curinga. Em particular, não são autorizados
`config/estilo.json`, `tela/carregamento/estilo.py`, `tela/loader.py`,
`tela/navegacao.py`, `tela/selecao.py`, documentação normativa, outros
fixtures persistentes, outros handoffs ou qualquer relatório adicional.

## 6. Shell declarativo e barra de menus

O shell `config/telas/demo/h0062_estilo.json` deve declarar uma única
instância de `console` com `politica_navegacao.tipo` igual a
`dois_niveis_por_foco`, `navegavel: true`, seleção declarada como `multipla`
para reutilizar a semântica vigente de `Espaço`, e sem paginação necessária.
Os pais e filhos não devem ser listados no shell: o controlador os monta em
memória a partir dos mapas de presets.

A barra deve usar a ordem canônica vigente e declarar somente os chips
aplicáveis:

```text
[Esc] Sair/Voltar → [✥] Navegar (condicional) → [␣] Selecionar
→ [⏎] Aplicar (candidato divergente) → [?] Ajuda
```

`[?] Ajuda` é obrigatório em toda tela, permanece sempre ativo e ocupa a
última posição da barra como chip visual canônico. A presença vigente de
`[?] Ajuda` não antecipa a futura ação global F1/Ajuda, que não faz parte deste
ciclo e não autoriza antecipar o ITEM-0029. `F4` é entrada global, não chip
adicional da barra. `Esc` no toroide de filhos retorna aos pais e preserva a
escolha; `Esc` no toroide de pais sai da tela e descarta a edição pendente.
`Aplicar` não pode ser materializado como `Todos` ou `Executar`; sua condição
é exclusivamente a divergência do candidato.

## 7. Construção dinâmica dos pais, filhos e amostras

`tela/estilo.py` deve construir uma visão em memória sobre uma cópia/snapshot
da configuração fornecida pelo `RuntimeEstilo`:

- a lista estrutural dos quatro pais é fixa e exatamente a deste handoff;
- cada mapa `presets` é percorrido na ordem declarada, sem lista paralela;
- o nome do preset e os dados completos do preset permanecem no nó/runtime;
- IDs internos podem ser opacos e gerados, com mapa interno para categoria e
  preset; nunca devem ser derivados por parsing de nome ou por delimitador
  visual;
- `preset_default` seleciona inicialmente um filho de cada pai;
- um preset acrescentado a uma fixture no mapa correspondente deve gerar um
  filho sem alteração de código ou de lista na tela.

Para cada filho, o renderer específico deve mostrar nome e amostra derivada
do próprio registro:

- `borda`: três linhas curtas, calculadas com os quatro cantos, traços e
  laterais do preset;
- `chip`: delimitadores, capitalização e campos visuais do próprio preset em
  uma amostra compacta;
- `indicadores.selecionado`: `simbolo` do próprio preset;
- `indicadores.incluido`: os valores `on` e `off` do próprio preset.

Não hardcodar nomes de presets, símbolos, cores, caracteres ou delimitadores.
Separadores e largura da miniatura são apenas geometria da amostra, não dados
de estilo. A moldura da tela e a forma da barra continuam vindo do
`EstiloResolvido` global vigente.

## 8. Navegação e candidato

O controlador deve adaptar a visão dinâmica à representação já consumida por
`dois_niveis_por_foco`, mantendo exatamente dois níveis: os quatro pais em um
toroide e um toroide de filhos para cada pai. Setas apenas movem o cursor.
`Espaço` no pai entra no toroide do pai; em filho transfere a escolha exclusiva
para o filho corrente. Cada pai mantém exatamente um filho escolhido.

Ao abrir, o candidato deve ser criado pelo `RuntimeEstilo` a partir da
baseline atual. A escolha inicial deve ser resolvida pelo `preset_default`,
não pela posição acidental do mapa. Ao transferir uma escolha, o controlador
deve localizar o caminho autorizado e chamar `definir_preset_candidato`; deve
validar/materializar localmente com `RuntimeEstilo.materializar_local` e
comparar com `RuntimeEstilo.comparar_candidato_baseline`. Mudanças em pais
distintos acumulam no mesmo candidato. Baseline, materialização global e
`config/estilo.json` permanecem inalterados.

O controlador não deve guardar uma baseline de fábrica. Deve consultar a
baseline vigente do runtime ao abrir e expor uma operação de rebase após uma
promoção externa confirmada pelo H-0063, recriando o candidato a partir da
nova baseline. Assim, uma saída posterior não desfaz uma aplicação confirmada.

## 9. Enter/Aplicar e fronteira H-0063

O chip `[⏎] Aplicar` e a tecla Enter ficam:

```yaml
ativo: RuntimeEstilo.comparar_candidato_baseline(candidato) == false
inativo: RuntimeEstilo.comparar_candidato_baseline(candidato) == true
```

Quando inativo, Enter não produz efeito. Quando ativo, H-0062 deve retornar
uma solicitação imutável, com cópias independentes de `candidato` e
`baseline`, por exemplo `SolicitacaoAplicacaoEstilo`, contendo também a
identidade da origem H-0062. Essa é a interface concreta para H-0063.

H-0062 termina nessa entrega. H-0063 consumirá a solicitação e será o único
responsável por demonstração, override local, Cabeçalho, Console, Dashboard,
barra representativa, pop-up, `ABORTADO`, `CONFIRMADO`, persistência,
publicação, atualização da baseline e validação E2E. H-0062 não deve abrir
popup, chamar `persistir_configuracao_estilo` ou `aplicar_candidato`, nem
produzir resultado ABORTADO/CONFIRMADO.

## 10. Saída da tela

Sem solicitação de aplicação pendente, sair no nível dos pais deve:

- abandonar o candidato editado;
- deixar intacta a baseline atual e o estilo global vigente;
- voltar pela pilha de telas existente, sem identificar telas por nome fixo;
- nunca restaurar padrão de fábrica.

Se H-0063 já tiver confirmado uma aplicação e atualizado o runtime, o rebase
da seção 8 deve fazer essa nova baseline permanecer aplicada. Um cancelamento
do H-0063 não deve descartar o candidato que foi entregue à demonstração;
essa decisão pertence ao retorno do H-0063.

## 11. Entradas, fixtures, temporários e saídas

Entrada real:

- `config/estilo.json`, lido/validado/materializado exclusivamente pelas
  primitivas H-0061;
- baseline, candidato e runtime global fornecidos por `RuntimeEstilo`.

Fixture:

- o shell declarativo H-0062 não contém catálogo de presets;
- testes podem copiar a configuração real para `tmp_path` e acrescentar um
  preset a um mapa, sem tocar na configuração real;
- não criar fixture persistente de preset nem catálogo paralelo.

Temporários:

- cópias em memória e diretórios `tmp_path` de testes;
- arquivos temporários internos da persistência H-0061, somente em testes que
  explicitamente exercitem essa infraestrutura fora do comportamento normal
  H-0062; nenhum temporário vira evidência persistente.

Saída de runtime:

- candidato editado;
- sinalização de divergência;
- cursor/escolhas por pai;
- `SolicitacaoAplicacaoEstilo` para H-0063.

Saída persistente normal: nenhuma.

## 12. Testes automatizados

`tela/teste_estilo.py` e `demo/teste_demo_estilo.py` devem comprovar sem TTY,
usando chamadas puras e captura controlada do decoder quando aplicável:

1. F4 chega ao dispatcher pelo mecanismo vigente e abre a tela correta; F1,
   F2, F3, F5 e F11 não são alterados.
2. Há exatamente quatro pais, na ordem estrutural definida.
3. Filhos vêm dos mapas `presets`; adicionar preset em fixture torna-o
   visível sem lista paralela.
4. A escolha inicial reflete cada `preset_default`.
5. Cursor se move sem alterar escolha; Espaço altera somente o filho do pai
   corrente e mantém exclusividade.
6. Alterações em vários pais acumulam no mesmo candidato.
7. Baseline e estilo global não são mutados pela edição; nenhuma publicação
   ocorre.
8. Aplicar é inativo para candidato igual à baseline e ativo para candidato
   divergente.
9. As quatro formas de amostra vêm dos dados reais de cada preset.
10. Saída descarta somente diferenças posteriores à baseline vigente e não
    desfaz uma baseline atualizada externamente.
11. Enter ativo entrega somente `SolicitacaoAplicacaoEstilo`; não abre popup,
    não persiste, não publica e não produz estados do H-0063.
12. A barra preserva a ordem canônica, mantém `[?] Ajuda` obrigatório, sempre
    ativo e como último chip, além dos estados ativo/inativo dos demais chips,
    com `[⏎] Aplicar` contextual.

Alvos futuros reproduzíveis:

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_estilo.py demo/teste_demo_estilo.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Validação manual posterior, sem aprovação automática: em TTY real, abrir a
demo, acionar F4, conferir navegação, amostras, saída e redesenho. Isso não
substitui os testes nem autoriza validar o E2E reservado ao H-0063.

## 13. Demonstração reproduzível

O shell `h0062_estilo.json` e o construtor dinâmico devem permitir:

```text
PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0062_estilo
```

Fora de TTY, a entrada por linhas deve aceitar `F4`, setas representadas pelo
comando vigente, espaço, Enter e Esc conforme o dispatcher testável. Em TTY,
F4 deve ser normalizado pelo decoder físico para `F4`. A demonstração termina
na tela de seleção ou na saída, sem fluxo de confirmação.

## 14. Critérios de aceite

- Todos os requisitos das seções 3, 6, 7, 8, 9, 10 e 12 são demonstrados por
  testes ou, apenas para a parte física de TTY, registrados como validação
  manual pendente.
- O conjunto exposto é exatamente o conjunto de quatro categorias; nenhuma
  categoria excluída aparece.
- Nenhum nome de preset, símbolo, cor ou delimitador concreto é duplicado no
  código, shell ou renderer.
- A escolha é sempre derivada do catálogo e o candidato é sempre separado da
  baseline/global.
- Não existe escrita normal de estilo em H-0062.
- Não existe popup, demonstração integrada, override local de demonstração,
  Cabeçalho/Console/Dashboard representativos, confirmação ou validação E2E
  de H-0063.
- A suíte focal e `PYTHONDONTWRITEBYTECODE=1 python -m pytest` passam no futuro
  relatório de implementação.

## 15. Relatório da implementação futura

Exigir exatamente:

```text
docs/relatorios/IMP-0062-tela-selecao-interativa-presets-estilo.md
```

O relatório deve registrar arquivos efetivamente alterados, contrato da
solicitação entregue ao H-0063, testes focais e canônicos, fatos sobre
baseline/global/persistência, resultado da validação manual TTY e qualquer
desvio ou bloqueio. Não deve atribuir a H-0062 trabalho de H-0063.

## 16. Exceção operacional e bloqueios

Nenhum bloqueio de implementação é conhecido após a leitura focal. A
ausência atual de F4 é uma lacuna prevista e deve ser resolvida somente nos
dois pontos autorizados do decoder/dispatcher vigente.

Se a implementação descobrir que precisa ler ou alterar caminho fora da
lista autorizada, deve parar antes da alteração e registrar:

```text
status: LEITURA_ADICIONAL_NECESSARIA
caminho: <caminho>
alvo: <dúvida concreta>
finalidade: <motivo>
impacto_sem_leitura: <impacto>
```

Se o branch, HEAD ou stage não coincidirem com a baseline transportada, deve
parar com `BLOCKED_REPOSITORY_STATE`. Não limpar, reverter, atribuir ou
substituir deltas existentes; não fazer stage, commit ou push.
