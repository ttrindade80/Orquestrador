# H-0057 — pop-up: geometria dinâmica, wrapping e resize

```yaml
handoff: H-0057
item: ITEM-0017
adr: ADR-0044
handoff_anterior: H-0056
handoff_anterior_status: concluido
baseline_commit: 1211a70
entrega: geometria_dinamica_wrapping_resize
status: concluido
```

## 1. Objetivo e autoridade

Evoluir a capacidade de pop-up textual entregue por H-0056 para que a
representação física seja calculada a partir do conteúdo e do corpo disponível
da tela. H-0056 é a baseline funcional: sua instância lógica, resolução por
`popups[ID]`, envelope textual pronto, moldura, título, área própria de chips,
`[Esc] Voltar`, bloqueio modal, retorno `ABORTADO` e reativação da mesma tela
devem permanecer íntegros.

H-0057 não reimplementa essa base. A declaração `popup_basico` e a fixture
`h0056_popup_texto.py` não devem sofrer mudança semântica. Para a demonstração,
usar uma declaração adicional `popup_texto_dinamico` e uma fixture nova. O
envelope continua sendo recebido em runtime:

```yaml
conteudo_popup:
  tipo: texto
  texto: "string semântica pronta"
```

Não adicionar campo ao envelope, dimensão fixa ou conteúdo concreto ao JSON.

## 2. Geometria normativa

O corpo materializado pela composição vigente é a única área física de
referência. O ponto de integração em `tela.py` deve obter a largura real das
linhas de `bloco_corpo` e sua altura já calculada, delegando ao renderer do
pop-up a geometria interna. Não usar consulta independente do terminal, o
retângulo do cabeçalho ou a caixa da `barra_de_menus` como disponibilidade do
pop-up. Não modificar as regras de composição de
`tela/renderizacao/composicao_corpo.py`.

A largura é ajustada antes da altura:

1. calcular a largura intrínseca em uma única linha, considerando moldura,
   título, `espacamento_horizontal`, texto e todos os chips em uma linha;
2. usar essa largura se couber na largura física do corpo;
3. caso contrário, usar a largura máxima do corpo;
4. com a largura final, refazer wrapping e distribuição dos chips;
5. calcular a altura derivada e centralizar o retângulo final no corpo.

Usar as primitivas de `tela/renderizacao/geometria_caixa.py`, inclusive a
convenção de largura da moldura e a política vigente para sobra ímpar: a sobra
horizontal/vertical deve ser dividida com `// 2` no lado inicial e o restante
no lado final. A mesma entrada e as mesmas dimensões devem produzir a mesma
posição em todos os redraws. Título que não caiba na moldura mínima e largura
útil não positiva são inviabilidade geométrica, não autorização para truncar.

O título permanece na moldura superior. A altura deve ser exatamente:

```text
borda superior
+ espacamento_superior
+ linhas físicas do conteúdo
+ espacamento_conteudo_chips
+ linhas físicas de chips
+ espacamento_inferior
+ borda inferior
```

Os três espaçamentos declarados, inclusive quando `0`, não podem ser reduzidos.

## 3. Wrapping e alinhamento

Implementar wrapping físico no renderer, mantendo a entrada como string
semântica. Preferir limites entre palavras; conservar cada palavra inteira
quando couber; dividir somente uma palavra maior que a largura útil quando isso
for indispensável. Nenhum caractere pode ser omitido, truncado ou substituído
por reticências. Não criar paginação.

Aplicar o alinhamento depois do wrapping:

- `esquerda`: preencher à direita;
- `centralizado`: dividir a sobra segundo a política geométrica vigente;
- `justificado`: justificar toda linha física que ainda tenha conteúdo depois
  dela, distribuindo a sobra entre os vãos da esquerda para a direita; a última
  linha física permanece alinhada à esquerda.

O texto continua sendo uma string sem quebras estruturais no envelope. A
implementação deve manter a validação fechada existente para campos e tipos.

## 4. Chips

A área própria deve aceitar layout de uma ou várias linhas, sem se tornar a
`barra_de_menus`. Reutilizar a primitiva de texto/medição canônica disponível
em `tela/renderizacao/barra_menus.py` — em particular `_texto_chip_barra` e a
medição sem ANSI — somente para a aparência e a largura do chip. Não chamar
`_linhas_barra`, não ler a declaração da barra, não promover `[Esc]`, não usar
ordem canônica da barra e não criar estilo local.

Usar o espaçamento comum vigente entre chips. O algoritmo físico é:

1. tentar todos os chips em uma linha;
2. se não couberem, percorrer a ordem declarada e colocar em cada linha o maior
   número de chips inteiros que couber;
3. continuar nas linhas seguintes até consumir todos;
4. centralizar cada linha independentemente.

Chip é indivisível: não dividir tecla e texto, não truncar, não alterar ordem e
não reduzir padding. Se um chip isolado não couber na largura útil, sinalizar
inviabilidade geométrica para a política geral de terminal pequeno.

A demonstração usa apenas `[Esc] Voltar`. Para a cobertura de múltiplos chips,
testar o helper puro de distribuição com entidades que usem os campos canônicos
de chip já existentes e sem abrir uma nova capacidade interativa. As entidades
adicionais de teste devem ser inertes, não podem introduzir `Enter`, confirmação,
payload ou marcação e não devem ser adicionadas ao acionamento da demo. Não
inventar campo ou novo schema para viabilizar esses testes.

## 5. Resize e terminal pequeno

Reutilizar o fluxo vigente em `demo.py`: `SIGWINCH`,
`_obter_dimensoes_apos_sigwinch`, par válido, últimas dimensões válidas,
redesenho e quadro geral. Não criar cache de dimensões do pop-up, listener
concorrente, fallback próprio ou reconstrução de instância.

Com o pop-up aberto, resize deve apenas recalcular largura intrínseca/máxima,
wrapping, chips, altura e centralização. A mesma referência de
`PopupInstancia` deve sobreviver; conteúdo, configuração, estado modal e tela
subjacente permanecem inalterados. Resize nunca fecha, emite resultado ou
reabre o pop-up.

Quando o retângulo completo não couber na altura ou quando um chip mínimo não
couber na largura útil, preservar a instância e deixar o erro geométrico entrar
na cadeia já existente de `_resolver_conteudo`/`_e_insuficiencia_geometrica`,
que exibe o quadro controlado geral de terminal pequeno. Não retornar um
quadro local de `popup.py`. Erros de declaração, envelope ou contrato não
podem ser classificados como insuficiência geométrica.

Ao retornar dimensões suficientes, o quadro geral desaparece e o mesmo pop-up é
representado novamente, com layout recalculado, sem nova abertura. Dimensões
inválidas consultadas durante resize preservam o último par válido e não podem
perder a instância.

## 6. Arquivos resolvidos

### Existentes a alterar

- `tela/renderizacao/popup.py` — ampliar medição, wrapping, alinhamento,
  distribuição de chips, altura derivada, detecção de inviabilidade e overlay;
  preservar a validação/envelope e o comportamento `Esc` de H-0056.
- `tela/renderizacao/tela.py` — integrar o overlay usando a área física real
  do corpo e manter a composição de cabeçalho/barra fora da referência do
  pop-up; não criar fallback local.
- `tela/teste_popup.py` — acrescentar a suíte unitária de geometria e layout,
  mantendo os testes de regressão H-0056.
- `demo/demo.py` — carregar a fixture H-0057 sem alterar a fixture H-0056,
  selecionar o envelope conforme a declaração acionada e classificar somente
  a insuficiência geométrica do pop-up na cadeia geral já existente.
- `demo/teste_demo_popup.py` — cobrir a declaração nova, recomposição,
  persistência da instância, terminal pequeno e restauração.
- `config/telas/demo/demo.json` — adicionar `popups.popup_texto_dinamico` e
  um acionamento demonstrativo separado, preservando `popup_basico` e seu
  acionamento atual. A nova declaração usa apenas campos já autorizados,
  contém somente `[Esc] Voltar` e não contém conteúdo runtime.

### Novo arquivo estritamente necessário

- `demo/fixtures/h0057_popup_texto_dinamico.py` — fixture Python que retorna
  string textual longa, determinística, sem lista, marcação ou arquivo externo;
  não modificar `demo/fixtures/h0056_popup_texto.py`.

### Relatório obrigatório da implementação futura

- `docs/relatorios/IMP-0057-popup-geometria-dinamica-wrapping-resize.md` —
  materializar somente após a implementação, com decisões, testes,
  demonstração e evidências da suíte.

`tela/renderizacao/geometria_caixa.py`,
`tela/renderizacao/composicao_corpo.py` e
`tela/renderizacao/barra_menus.py` são primitivas de reutilização e não devem
ser alterados neste handoff. Nenhum diretório inteiro é autorizado.

## 7. Configuração e demonstração

Adicionar uma chave estrutural `popup_texto_dinamico` no mapa geral `popups`,
sem `id` interno redundante, com o mesmo formato de `popup_basico`: tipo
`texto`, título, um dos três alinhamentos, os três espaçamentos verticais, o
padding horizontal e uma lista contendo apenas o chip canônico `[Esc] Voltar`.
Adicionar acionamento no formato já usado, preferencialmente com tecla `w`,
referenciando essa chave. O conteúdo longo deve vir exclusivamente de
`conteudo_popup_h0057()` em runtime.

Em TTY real, uma única sessão deve permitir:

1. abrir a demo e pressionar `w`;
2. observar moldura, título, wrapping e centralização;
3. reduzir a largura e observar mais linhas;
4. aumentar a largura e observar menos linhas;
5. reduzir a altura até surgir o quadro geral de terminal pequeno;
6. restaurar dimensões e observar o mesmo pop-up voltar automaticamente;
7. pressionar uma tecla não declarada, como `x`, e comprovar que a tela
   inferior não reage;
8. pressionar `Esc`, comprovar `ABORTADO` e interagir novamente com a mesma
   tela subjacente.

## 8. Testes focais obrigatórios

Em `tela/teste_popup.py`, preservar H-0056 e acrescentar testes para:

- largura intrínseca que cabe, largura que excede o corpo, cap pela largura
  máxima e respeito ao padding horizontal;
- texto curto sem quebra, quebra por palavras, múltiplas linhas, palavra maior
  que a largura útil, ausência de truncamento, reticências e paginação;
- alinhamentos `esquerda`, `centralizado` e `justificado`, incluindo última
  linha do justificado à esquerda;
- altura derivada pelo número de linhas, espaçamentos `0|1` preservados e
  chips multilinha aumentando a altura;
- chips em uma linha, em várias linhas, ordem preservada, indivisibilidade,
  centralização independente por linha e chip isolado inviável;
- crescimento e redução de largura e altura, determinismo de posição e
  ausência de emissão de resultado durante resize;
- entrada em terminal pequeno, instância ainda viva, dimensões inválidas
  preservando últimas dimensões válidas, restauração automática e conteúdo
  preservado.

Em `demo/teste_demo_popup.py`, acrescentar a declaração/fixture H-0057 e
verificar a mesma instância através de renderizações e mudanças de dimensões,
o quadro geral durante inviabilidade, retorno automático, bloqueio modal,
`Esc → ABORTADO`, ausência de payload, tela subjacente e regressão de
`popup_basico`. Não antecipar lista, cursor, marcação ou confirmação.

Ao final da implementação, executar a suíte canônica sem bytecode:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Baseline de referência: `1118 passed`; a contagem pode aumentar, mas nenhuma
regressão é aceitável.

## 9. Critérios de aceite e exclusões

Aceitar somente se largura intrínseca, cap pelo corpo, wrapping sem perda,
três alinhamentos, altura derivada, chips multilinha, ordem/indivisibilidade,
resize, mesma instância, últimas dimensões válidas, quadro geral e restauração
estiverem demonstrados e cobertos pelos testes; não houver paginação; H-0056
continuar íntegro; a demonstração for reproduzível; os testes focais e a suíte
canônica passarem; e o relatório `IMP-0057...` estiver materializado.

Ficam fora de H-0057: listas, cursor e setas de item, matriz de itens,
`Espaço`, `marcacao: exclusiva`, `marcacao: multipla`, `Enter`, confirmação,
payload confirmado, compatibilidade chamador↔retorno, execução de decisão,
paginação, hierarquia, busca, edição de texto e mudança da política global de
estilo. Não criar H-0058 ou H-0059.

## 10. Fechamento factual

```yaml
status: concluido
validacao_manual: MANUAL_VALIDATION_APPROVED
limitacao_conhecida:
  id: MV-H0057-001
  area: texto_justificado
  descricao: Em determinadas larguras, a composição visual pode apresentar diferença de uma coluna ou distribuição desigual entre linhas.
  impacto: nao compromete wrapping, resize, centralizacao do popup, modalidade ou retorno
  decisao_usuario: ACEITA_PARA_FECHAMENTO
deferimento:
  tema: composicao_e_justificacao_global_de_texto
  estado: DEFERIDO_PARA_ITEM_FUTURO
  escopo_futuro: Adotar algoritmo canônico/global de composição de parágrafo e justificação para todas as ocorrências de texto justificado da TUI, evitando soluções locais por componente.
  momento_registro_backlog: fechamento final do ITEM-0017, depois de H-0058 e H-0059
proxima_entrega:
  handoff: H-0058
  tema: lista_navegavel_e_marcacao_exclusiva_multipla
  status: nao_iniciada
```
