# H-0065 — Vinculação da escolha de preset ao candidato de estilo

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0065
data_criacao: 2026-08-12
status: READY_FOR_IMPLEMENTATION
predecessor: H-0064
relacao: continuacao_funcional
historico:
  H-0061:
    estado: aprovado
    capacidade:
      - infraestrutura_runtime_de_estilo
      - baseline
      - candidato
      - materializacao
      - persistencia/publicacao_fail_closed_para_etapas_futuras
  H-0062:
    estado: substituido
  H-0063:
    estado: aprovado
    capacidade:
      - tela_normal
      - dois_niveis_por_foco
      - filho_corrente
      - filho_escolhido_observacional
      - F4
      - resize
      - paginacao
  H-0064:
    estado: I1_IMPLEMENTATION_APPROVED
    capacidade:
      - amostras_visuais_dos_presets
dependencias:
  - H-0061
  - H-0063
  - H-0064
item_0010:
  estado: em_andamento
patches:
  - id: P01
    origem: docs/relatorios/RELATORIO_QA_HANDOFF_H-0065.md
    achados:
      - QA-H0065-001
      - QA-H0065-002
      - QA-H0065-003
  - id: P02
    origem: docs/relatorios/RELATORIO_QA_HANDOFF_H-0065_P01.md
    achados:
      - QA-H0065-002
      - QA-H0065-003
    preservados_como_resolvidos:
      - QA-H0065-001
```

H-0065 é continuação funcional de H-0064, não substituição. A tela normal, os
quatro pais, a navegação `dois_niveis_por_foco`, a Barra de Menus, as amostras
visuais e a fronteira de estado navegacional/mutação fixada por H-0063 e
H-0064 permanecem integralmente vigentes, exceto no ponto exato que este
handoff altera deliberadamente: `Espaço` sobre um filho passa a também
atualizar o candidato de estilo (H-0061), o que H-0063/H-0064 explicitamente
não faziam. H-0062 permanece histórico/substituído e não é reaberto.

## 2. Objetivo exclusivo

Especificar e autorizar a implementação da transição:

```text
ESCOLHA NAVEGACIONAL DE PRESET → ATUALIZAÇÃO DO CANDIDATO RUNTIME
```

Somente o candidato pode mudar. Este handoff não introduz aplicação real do
estilo: não há preview integrado, não há troca de borda/chip/indicadores em
nenhum consumidor visual da aplicação, não há persistência em
`config/estilo.json` e não há publicação de novo estilo global. O único
efeito observável autorizado é a mutação do candidato de runtime já
materializado por H-0061 (`EstadoEstiloRuntime`/`RuntimeEstilo`) e a
reconciliação da observação de "filho escolhido" com esse candidato.

## 3. Autoridade principal

Lidas integralmente:

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`
- `docs/handoff/H-0061-infraestrutura-estilo-runtime.md`
- `docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md`
- `docs/handoff/H-0064-amostras-visuais-presets-estilo.md`

Lidas focalmente:

- `docs/contratos/contrato_estilo.md` §3.8, R-1, R-4, R-11, R-12, R-13
- `docs/nomenclatura/10_ESTILO.md` §4.8, §4.9

Código existente inspecionado para identificar primitivas já materializadas:

- `tela/carregamento/estilo.py` — `EstadoEstiloRuntime`/`RuntimeEstilo`,
  `criar_candidato_estilo`, `definir_preset_candidato`,
  `materializar_estilo_local`, `comparar_configuracoes_estilo`,
  `CAMINHOS_PRESET_DEFAULT_PERMITIDOS`.
- `tela/estilo.py` — `ControladorTelaEstilo` (H-0063/H-0064).
- `demo/demo.py` — instanciação de `RuntimeEstilo()` por sessão (linhas
  2346-2354), tratamento de `F4` (linhas 860-875) e `_anexar_tela_estilo`
  (linhas 320-334).

Nenhum destes arquivos foi alterado por esta etapa.

## 4. Ciclo de vida do candidato — determinação documental obrigatória

Antes de especificar o comportamento funcional, este handoff fixa
normativamente as sete perguntas exigidas, cada uma classificada.

### 4.1 Quando o candidato nasce

**DETERMINADO_PELA_AUTORIDADE.** ADR-0046 §7, linha `F4`: "Abre a
funcionalidade com candidato derivado da última configuração persistida."
ADR-0046 §4: "No início da visita à tela, o candidato é formado a partir da
última configuração persistida". O candidato nasce a cada **visita** à tela
de Estilo — não uma única vez por sessão.

### 4.2 De qual estado ele é inicializado

**DETERMINADO_PELA_AUTORIDADE.** Da baseline (última configuração
persistida conhecida pelo fluxo, `config/estilo.json` neste ciclo, sem
mudança por este handoff). "Suas escolhas correntes vêm dos
`preset_default`" (ADR-0046 §4) — ou seja, o candidato nasce igual à
baseline nas quatro categorias expostas.

### 4.3 Se abrir F4 cria/reinicializa candidato

**DETERMINADO_PELA_AUTORIDADE.** Sim. Cada abertura da tela (transição para
`_ID_TELA_H0063`) forma um candidato novo a partir da baseline vigente
naquele instante (ADR-0046 §7, linha `F4`).

### 4.4 Se candidato já existente é reaproveitado

**DETERMINADO_PELA_AUTORIDADE (resposta negativa) + DERIVAVEL_DAS_PRIMITIVAS_EXISTENTES
(distinção de escopo).** Entre visitas distintas, não — cada visita forma
candidato novo (§4.3). Dentro da **mesma** visita (sem sair da tela), o
mesmo candidato é reaproveitado e acumula escolhas de várias categorias:
"alterações de várias categorias acumulam-se somente no candidato" (ADR-0046
§4). Isso é distinto da persistência da instância única de
`RuntimeEstilo`/`EstadoEstiloRuntime` por sessão (`demo/demo.py:2346-2354`,
comentário "H-0061/H-0062: uma unica instancia de runtime separa baseline,
candidato e materializacao global durante toda a sessao") — essa instância
de runtime não é recriada por este handoff; apenas o **valor** do seu
candidato é (re)formado a cada visita, via `EstadoEstiloRuntime.criar_candidato()`,
primitiva já existente (`tela/carregamento/estilo.py:329-336`).

### 4.5 O que ocorre ao sair da tela sem Aplicar

**DETERMINADO_PELA_AUTORIDADE + FECHADO_POR_ESTE_HANDOFF (P01/P02).**
ADR-0046 §7, linha "saída sem aplicação": "Descarta somente diferenças ainda
não confirmadas e restaura logicamente a última configuração persistida."
Como H-0065 ainda não possui `Aplicar`, toda divergência candidato × baseline
é, por definição, não confirmada.

```text
ESC QUE EFETIVAMENTE SAI DA TELA DE ESTILO DESCARTA IMEDIATAMENTE TODAS AS
DIFERENÇAS NÃO CONFIRMADAS.
```

Qualquer **SAÍDA EFETIVA** da tela de Estilo fecha-se como **uma única
sequência ordenada** (detalhamento normativo em §12.2):

1. **Etapa 1 — descartar candidato não confirmado:** recriar/reinicializar
   o candidato a partir da baseline vigente via
   `EstadoEstiloRuntime.criar_candidato()`. Depois: `candidato == baseline`.
2. **Etapa 2 — reconciliar a projeção navegacional:** antes de concluir a
   saída, executar `reconciliar_selecoes_com_candidato()` (§9.2) sobre o
   candidato recém-recriado. Depois:
   `estado["selecoes"] == projeção determinística dos preset_default do
   candidato`. Como nesse instante `candidato == baseline`, também vale
   semanticamente `selecoes == projeção da baseline`.
3. **Etapa 3 — verificar invariável:** a saída não pode ser concluída se
   houver `candidato != fonte_semantica_de(selecoes)` (ou equivalente).
4. **Etapa 4 — concluir a saída:** somente após candidato e projeção
   coerentes — remover/popar a tela, retornar à tela anterior, concluir o
   evento.

Não persistir; não publicar; não alterar baseline; não alterar global.

No instante **imediatamente posterior** à saída efetiva, para cada uma das
quatro categorias (representando por `A` os presets projetados da baseline):

```text
baseline = A
candidato = A
selecoes = A
```

Mais precisamente, para cada categoria:

```text
candidato.<categoria>.preset_default
  == preset representado por estado["selecoes"] naquele pai
  == baseline.<categoria>.preset_default
```

Nenhum estado abandonado da visita anterior pode permanecer em `selecoes`.
Não se admite retenção do candidato divergente nem de cache de seleção
abandonado até a próxima abertura. Preferir reconciliação explícita a
deixar a limpeza indefinida (§12.2).

### 4.6 O que ocorre ao reabrir a tela

**DETERMINADO_PELA_AUTORIDADE + FECHADO_POR_ESTE_HANDOFF (P01/P02).**
`F4` cria/reinicializa o candidato a partir da baseline vigente (§4.3). Isso
continua sendo feito mesmo que a saída anterior já tenha restaurado
`candidato == baseline` e `selecoes == baseline` (§4.5). A repetição
defensiva é intencional e mantém cada visita isolada — não é contradição.

Cada `F4` pode repetir defensivamente:

```text
criar_candidato()
→ reconciliar_selecoes_com_candidato()
```

Depois disso:

- as escolhas iniciais refletem a baseline vigente (via o candidato
  recém-formado, semanticamente igual a ela).

### 4.7 Como baseline/candidato/global se relacionam durante essa fase

**DETERMINADO_PELA_AUTORIDADE** (`contrato_estilo.md` §3.8; ADR-0046 §4).
Baseline (configuração persistida) e materialização global vigente
permanecem inalteradas durante toda a fase coberta por este handoff — não há
persistência nem publicação nele. O candidato é o único estado mutável,
isolado, derivado da baseline e comparável semanticamente a ela via
`comparar_configuracoes_estilo`/`EstadoEstiloRuntime.comparar_candidato_baseline`
(já existentes).

### 4.8 Conclusão

Todas as sete perguntas têm resposta suficiente na autoridade vigente,
combinada com primitivas já materializadas por H-0061 e com o fechamento
temporal de descarte e reconciliação de `selecoes` fixado por este handoff
(P01/P02). O protocolo atômico de `Espaço` (QA-H0065-001) permanece
preservado e não reaberto. Não há ponto `NAO_DETERMINADO` com mais de uma
semântica materialmente diferente possível necessária a este handoff.
H-0065 é, portanto, `READY_FOR_IMPLEMENTATION`.

## 5. Categorias (preservadas, sem expansão)

Mantidas exatamente as quatro categorias de H-0063/H-0064:

- `borda`
- `chip`
- `indicadores.selecionado`
- `indicadores.incluido`

Continuam fora de escopo: `tiling`, `cor_inativo`, `cor_alerta`,
`indicadores.concluido`.

## 6. Semântica funcional — foco/navegação (setas)

Preservada integralmente de H-0063/H-0064: setas alteram somente o cursor
(filho corrente) dentro do toroide vigente. Setas nunca alteram o candidato,
a baseline, `config/estilo.json` ou o estilo global. Nenhuma mudança de
comportamento nesta capacidade.

## 7. Semântica funcional — `Espaço` sobre filho

`Espaço` sobre um filho válido, no nível dos filhos, é uma **única transição
atômica** disparada pelo mesmo evento. A direção semântica obrigatória é:

```text
preset solicitado
→ candidato validado/aceito
→ projeção navegacional do candidato
```

A UI não deve primeiro escolher e depois tentar fazer o candidato acompanhar.

ADR-0046 §7, linha `Espaço`, funde as duas metades do mesmo evento em uma só
célula da tabela de transições: "Transfere a escolha exclusiva do pai para o
filho corrente e atualiza o candidato" — não são dois efeitos independentes
nem opcionalmente sequenciáveis.

### 7.1 Protocolo atômico obrigatório (QA-H0065-001)

Ao pressionar `Espaço` sobre filho válido:

#### Fase A — preparar

1. identificar pai/categoria;
2. identificar preset corrente (do nó de filho sob o cursor —
   `categoria`/`preset` já disponíveis em `NoConteudo.campos`, conforme
   `tela/estilo.py:117-122`);
3. capturar o candidato atual como estado anterior;
4. **NÃO** alterar ainda `estado["selecoes"]`.

#### Fase B — candidato proposto

5. produzir a mutação candidata usando as primitivas vigentes de H-0061
   (`definir_preset_candidato` sobre cópia/estrutura transitória);
6. alterar somente o caminho da categoria correspondente (§8);
7. validar/materializar a proposta pela infraestrutura runtime existente
   (`EstadoEstiloRuntime.materializar_local`).

#### Fase C — falha

Se a validação/materialização falhar:

- o candidato runtime deve continuar exatamente no estado anterior;
- `estado["selecoes"]` não pode consolidar o novo filho;
- reconciliar `selecoes` a partir do candidato anterior
  (`reconciliar_selecoes_com_candidato()`, §9.2);
- baseline permanece intacta;
- global permanece intacto;
- arquivo permanece intacto;
- o evento termina sem mutação parcial observável.

Não fazer rollback inventado de persistência/global porque eles nunca
mudaram nesta capacidade.

#### Fase D — sucesso

Somente depois de o candidato ser aceito:

- o candidato runtime passa a conter o novo preset;
- reconstruir/reconciliar `estado["selecoes"]` a partir desse candidato
  (`reconciliar_selecoes_com_candidato()`, §9.2);
- o novo filho passa a ser observado como escolhido;
- o anterior deixa de ser escolhido;
- outras categorias preservam seus valores candidatos.

### 7.2 Fronteira de commit observável

O evento de `Espaço` só é considerado concluído com sucesso quando:

1. o candidato contém o novo preset;
2. `selecoes` reconciliado representa esse mesmo preset;
3. as demais categorias permanecem coerentes com o candidato.

Antes disso, a interface não deve retornar ao ciclo normal de renderização
com estado intermediário. A atomicidade é responsabilidade da coordenação
controlador/runtime/dispatch — não da camada visual/renderer.

### 7.3 Efeitos preservados do evento bem-sucedido

No sucesso, o mesmo evento:

1. transfere a escolha exclusiva do pai para o filho corrente, via projeção
   do candidato sobre o mecanismo canônico `dois_niveis_por_foco` (H-0055,
   preservado por H-0063 §4.4/§5 — não redesenhado);
2. atualiza no candidato **somente** a categoria correspondente àquele pai;
3. preserva todas as demais categorias do candidato;
4. não persiste (`config/estilo.json` intacto);
5. não publica (materialização global vigente intacta);
6. não abre demonstração, popup ou qualquer efeito de `Aplicar`.

## 8. Mapeamento pai → candidato

Fechado explicitamente, sem lógica por nome de preset — a chave identifica
apenas o campo estrutural, nunca decide o valor:

| Pai (categoria) | Caminho no candidato | Permitido por H-0061 |
|---|---|---|
| `borda` | `borda.preset_default` | `("borda", "preset_default")` |
| `chip` | `chip.preset_default` | `("chip", "preset_default")` |
| `indicadores.selecionado` | `indicadores.selecionado.preset_default` | `("indicadores", "selecionado", "preset_default")` |
| `indicadores.incluido` | `indicadores.incluido.preset_default` | `("indicadores", "incluido", "preset_default")` |

Esses quatro caminhos já são exatamente `CAMINHOS_PRESET_DEFAULT_PERMITIDOS`
(`tela/carregamento/estilo.py:53-59`) e já correspondem, campo a campo, ao
mapeamento `_CAMINHOS_CATEGORIAS` já existente em `tela/estilo.py:30-35`
(cada categoria + `("preset_default",)`). Nenhum caminho novo é criado; o
valor concreto do preset (`preset`) sempre vem do catálogo dinâmico já
projetado por H-0063/H-0064 (`presets`), nunca de literal por nome.

## 9. Fonte semântica única e projeção candidato → selecoes

### 9.1 Fonte semântica única (QA-H0065-002)

```text
CANDIDATO RUNTIME É A FONTE SEMÂNTICA ÚNICA DO PRESET ESCOLHIDO.
```

Depois de H-0065:

- o preset escolhido de cada uma das quatro categorias é determinado pelo
  candidato;
- `estado["selecoes"]` **não** é autoridade semântica;
- `estado["selecoes"]` existe apenas como projeção/cache navegacional
  necessário à política `dois_niveis_por_foco`.

Não pode existir uma regra em que:

```text
candidato = B
selecoes = A
```

seja considerado estado válido.

A infraestrutura navegacional `dois_niveis_por_foco` (H-0055) permanece o
mecanismo de renderização/navegação canônico e **não** é redesenhada nem
substituída (proibido por ADR-0046 §3). O que muda é a autoridade: toda
observação de "filho escolhido" deve ser projeção do candidato, nunca uma
segunda fonte independente.

### 9.2 Operação conceitual obrigatória — `reconciliar_selecoes_com_candidato()`

Nome documental da operação. Não é obrigatório que esse seja o nome final da
função de código.

A operação deve:

1. ler os quatro `preset_default` do candidato;
2. localizar dinamicamente o filho correspondente em cada pai (pelo
   `preset`/`categoria` já projetados nos nós — sem mapa de nomes de
   presets);
3. reconstruir a escolha exclusiva de cada pai;
4. substituir/reconciliar `estado["selecoes"]`;
5. não modificar candidato;
6. não modificar baseline;
7. não modificar global;
8. não escrever arquivo.

A operação é determinística.

### 9.3 Quando reconciliar

Reconciliação candidato → `selecoes` é obrigatória em **todos** estes pontos:

- abertura/`F4` após criar candidato;
- `Espaço` bem-sucedido;
- falha de tentativa de `Espaço`;
- antes de render/redraw quando houver possível residual;
- após resize/reconciliação estrutural quando aplicável;
- **SAÍDA EFETIVA**, imediatamente após recriar o candidato da baseline e
  antes de concluir a saída (§4.5/§12.2).

A ausência da saída nessa lista reabriria divergência pós-descarte
(candidato restaurado, `selecoes` ainda da visita abandonada). A intenção é
que nenhum caminho observável consiga sustentar divergência.

### 9.4 Invariável global de `selecoes`

```text
ENQUANTO estado["selecoes"] EXISTIR, ELE DEVE SER UMA PROJEÇÃO VÁLIDA DO
CANDIDATO RUNTIME.
```

Não existem exceções temporais permitidas para:

- pós-`Espaço`;
- falha;
- redraw;
- resize;
- saída.

Estados intermediários internos podem existir durante uma função atômica,
desde que não sejam observáveis e a função não retorne sem restaurar a
invariável. Contrato mínimo: nenhum `selecoes` existente pode divergir do
candidato. A estratégia implementável preferencial na saída é reconciliar
antes de concluir (§12.2); se a implementação concreta remover integralmente
o cache junto com o objeto/tela, isso só é aceitável se o estado deixar de
existir de forma inequívoca.

### 9.5 Falha extraordinária da projeção

Como a projeção parte de um candidato já validado e dos presets vigentes,
ela deve ser determinística. Mesmo assim, uma inconsistência interna de
projeção:

- não pode ser silenciosamente ignorada;
- não pode deixar a tela renderizar candidato/`selecoes` divergentes;
- deve ser tratada como falha de invariável;
- antes de nova renderização, `selecoes` deve ser reconstruído novamente da
  fonte semântica candidato ou a operação deve falhar de forma controlada.

Não criar nova política de persistência.

### 9.6 Troca sucessiva

Torne explícito:

```text
estado inicial: candidato=A, selecoes=A

Espaço em B com sucesso:
  candidato=B
  selecoes=B

Espaço em C com sucesso:
  candidato=C
  selecoes=C

Nunca:
  candidato=C
  selecoes=B
```

### 9.7 Pais independentes

Mantido:

- borda pode mudar para B1;
- depois chip pode mudar para C1;
- candidato final conserva `borda=B1` e `chip=C1`;
- `selecoes` de cada pai é projetado desse mesmo candidato.

## 10. Estado inicial da tela

A escolha inicialmente mostrada em cada pai corresponde ao `preset_default`
do **candidato** no momento em que ele é formado ao abrir a tela — não é
lida diretamente da baseline (embora, no instante da formação, os dois
valores coincidam por definição, §4.2) e não é presumida como constante
arquitetural independente da autoridade: a origem é o candidato recém-criado
por `EstadoEstiloRuntime.criar_candidato()`, seguido imediatamente de
`reconciliar_selecoes_com_candidato()`.

## 11. Divergência candidato × baseline

H-0065 pode usar `EstadoEstiloRuntime.comparar_candidato_baseline`/
`comparar_configuracoes_estilo` (já existentes, `tela/carregamento/estilo.py:233-237,348-350`)
exclusivamente para testar coerência interna (ex.: comprovar que a baseline
não muda enquanto o candidato diverge após `Espaço`). Este handoff não
introduz `Enter`/`Aplicar`, não cria chip novo na Barra de Menus e não expõe
a divergência na interface.

## 12. Esc e saídas

### 12.1 Esc no nível dos filhos

`Esc` dentro do nível de filhos → retorna aos pais.

Esse `Esc`:

- não descarta candidato;
- não restaura baseline;
- não desfaz escolhas candidatas válidas da visita corrente;
- **nenhum descarte ocorre**.

Preserva filho corrente e filho escolhido de cada pai — comportamento
herdado literalmente de H-0063 §5, inalterado quanto ao retorno de nível.
Isso diferencia retorno de nível de saída efetiva.

Exemplo normativo:

```text
Durante a visita:     baseline=A, candidato=B, selecoes=B
Esc filho→pais:       baseline=A, candidato=B, selecoes=B
```

Como as escolhas candidatas permanecem, `selecoes` continua refletindo o
candidato (já reconciliado).

### 12.2 Esc que efetivamente sai da tela (QA-H0065-002 / QA-H0065-003)

```text
ESC QUE EFETIVAMENTE SAI DA TELA DE ESTILO DESCARTA IMEDIATAMENTE TODAS AS
DIFERENÇAS NÃO CONFIRMADAS.
```

Como H-0065 ainda não possui `Aplicar`, toda divergência candidato × baseline
é não confirmada. O descarte de candidato/`selecoes` ao sair é apenas ciclo
de vida transitório — continua fora: Aplicar, Enter como Aplicar, chip
Aplicar, popup, confirmação, CONFIRMADO, ABORTADO, preview real,
persistência, publicação global.

#### Sequência ordenada obrigatória

Quando uma ação efetivamente sai da tela de Estilo, aplicar integralmente:

```text
recriar candidato da baseline
→ reconciliar selecoes
→ verificar coerência
→ sair
```

**Etapa 1 — descartar candidato não confirmado.** Recriar/reinicializar o
candidato a partir da baseline vigente (`EstadoEstiloRuntime.criar_candidato()`).
Depois: `candidato == baseline`.

**Etapa 2 — reconciliar a projeção navegacional.** Antes de concluir a
saída, `reconciliar_selecoes_com_candidato()` sobre o candidato
recém-recriado. Depois: `selecoes` == projeção determinística dos
`preset_default` do candidato (== projeção da baseline, pois
`candidato == baseline`). Preferir reconciliação; não deixar limpeza
indefinida. `selecoes` continua sendo estado navegacional/cache válido do
controlador enquanto existir e deve permanecer coerente com sua fonte
semântica. Remoção integral do cache junto com o objeto/tela só é aceitável
se o estado deixar de existir de forma inequívoca. Contrato mínimo: nenhum
`selecoes` existente pode divergir do candidato.

**Etapa 3 — verificar invariável.** Não concluir a saída se
`candidato != fonte_semantica_de(selecoes)` (ou equivalente).

**Etapa 4 — concluir a saída.** Somente após coerência: remover/popar a
tela; retornar à tela anterior; concluir o evento.

#### Estado imediatamente após a saída

Para as quatro categorias, com `A` = presets projetados da baseline:

```text
baseline = A
candidato = A
selecoes = A
```

Para cada categoria:

```text
candidato.<categoria>.preset_default
  == preset em estado["selecoes"] daquele pai
  == baseline.<categoria>.preset_default
```

Global e `config/estilo.json` intactos. Nenhum estado abandonado da visita
pode permanecer em `selecoes`.

#### Exemplo normativo

```text
### Durante a visita
baseline:   borda: A
candidato:  borda: B
selecoes:   borda: B

### Esc de saída efetiva
1. candidato volta para A;
2. selecoes é reconciliado para A;
3. só então a tela é encerrada.

### Estado pós-saída
baseline:   borda: A
candidato:  borda: A
selecoes:   borda: A

Proibido (mesmo que a tela já não esteja visível):
baseline: A
candidato: A
selecoes: B
```

### 12.3 Reabertura via F4

`F4` continua criando/reinicializando candidato a partir da baseline.
Mesmo que a saída anterior já tenha restaurado `candidato == baseline` e
`selecoes == baseline`, `F4` pode repetir defensivamente:

```text
criar_candidato()
→ reconciliar_selecoes_com_candidato()
```

Isso não é contradição: é garantia de isolamento entre visitas (§4.6).

### 12.4 Saída por outros caminhos

Qualquer **SAÍDA EFETIVA** equivalente deve cumprir a mesma sequência:

```text
recriar candidato da baseline
→ reconciliar selecoes
→ verificar coerência
→ sair
```

Aplica-se, por exemplo, a qualquer comando que realmente abandone a tela.

Não se aplica a:

- `Esc` filho → pais;
- `PageUp`/`PageDown`;
- resize;
- redraw;
- mudança de foco interna.

## 13. Amostras H-0064

Preservadas integralmente: borda compacta em uma linha, chip `Ab`/`AB` com
cor e reset ANSI, símbolo de `selecionado`, par `on`/`off` de `incluido`. A
lógica de materialização das amostras (`tela/renderizacao/estilo.py`,
`compor_titulo_com_amostra`) não é alterada por este handoff — a amostra
continua sendo descrição do preset (leitura de `PresetEstilo.dados`), não
preview aplicado à tela, e independe de qual `preset_default` está ativo no
candidato.

## 14. Sem preview real

H-0065 não aplica o candidato visualmente à tela nem a nenhum outro
consumidor. Escolher preset de borda não troca a borda global; escolher
preset de chip não troca a Barra global; selecionar indicador não muda
outros componentes da aplicação. Isso pertence a etapas posteriores da
ADR-0046 (demonstração integrada, override local — ADR-0046 §5).

## 15. Sem persistência/publicação

Proibido nesta capacidade:

- chamar `persistir_configuracao_estilo`/`EstadoEstiloRuntime.persistir_candidato`;
- chamar `EstadoEstiloRuntime.aplicar_candidato`;
- escrever `config/estilo.json`;
- atualizar baseline persistida;
- publicar novo estilo global (`global_vigente`);
- emitir `CONFIRMADO` ou `ABORTADO`.

O candidato é estado transitório em memória, isolado por `RuntimeEstilo`
(já implementado por H-0061).

## 16. Relação com H-0061 — proibição de duplicar

A implementação reutiliza obrigatoriamente as primitivas já materializadas
por H-0061 em `tela/carregamento/estilo.py`:

- `EstadoEstiloRuntime.criar_candidato()` — para nascimento/reinicialização
  do candidato a cada visita (§4) e para o descarte imediato na saída
  efetiva (§4.5/§12.2);
- `definir_preset_candidato(candidato, caminho, preset)` — para a mutação de
  uma única categoria (§7/§8), com validação fechada de caminho permitido e
  de existência do preset no catálogo do próprio candidato;
- `EstadoEstiloRuntime.materializar_local(candidato)` — para validar e
  comitar atomicamente a mutação como novo candidato do runtime, sem
  publicar (§7/§17);
- `EstadoEstiloRuntime.comparar_candidato_baseline`/`comparar_configuracoes_estilo`
  — uso interno de teste (§11).

Nenhuma nova estrutura de candidato específica da tela é autorizada. Não
duplicar baseline, candidato, materialização ou validação estrutural — H-0061
já fornece tudo isso.

## 17. Atomicidade da mutação local

A atualização de uma categoria deve seguir o protocolo de §7.1.

`definir_preset_candidato` levanta `EstiloErro` sem mutar o documento em
memória do candidato quando o preset não existe no catálogo daquela
categoria ou o caminho não é um dos quatro permitidos;
`EstadoEstiloRuntime.materializar_local` valida o documento completo antes
de substituir o candidato interno do runtime — em caso de falha, a exceção
se propaga **antes** de qualquer atribuição ao estado interno
(`tela/carregamento/estilo.py:338-346`), preservando o candidato anterior
íntegro.

A implementação de H-0065 deve usar exatamente essa ordem (mutar cópia →
validar/materializar → só então comitar o candidato → só então reconciliar
`selecoes`) e não introduzir mutação direta e não validada do dicionário
interno do runtime. Em falha, reconciliar `selecoes` a partir do candidato
anterior; não inventar rollback de persistência/global. Nenhuma
persistência fail-closed é antecipada; a garantia exigida é apenas de
integridade em memória e ausência de janela observável divergente.

## 18. Arquivos autorizados para implementação

Lista nominal mínima, decorrente de §16 (reuso obrigatório de H-0061, sem
duplicar) e da ausência de qualquer exigência visual estrutural nova (§13):

### Tela/controlador (evolução de H-0063/H-0064)

- `tela/estilo.py` — evoluir `ControladorTelaEstilo` para: (a) formar um
  candidato novo do `runtime_estilo` na construção de cada instância nova
  (correspondendo a cada visita real, já que uma instância nova só é criada
  ao entrar na tela — `demo/demo.py:867` e primeira criação em
  `_anexar_tela_estilo`, `demo/demo.py:329-333`); (b) sourcing de
  `_catalogo`/escolha inicial a partir desse candidato, não mais da
  baseline diretamente, com `reconciliar_selecoes_com_candidato()`;
  (c) expor a capacidade de aplicar, de forma atômica conforme §7.1, a
  mutação de uma categoria do candidato a partir do nó de filho sob o
  cursor no momento de `Espaço`; (d) reconciliar `selecoes` nos pontos
  obrigatórios de §9.3. Não recriar a estrutura de pais/filhos nem a
  fronteira de estado navegacional já fechada por H-0063; não alterar a
  composição de amostra (H-0064). Não autorizar alteração de renderer: a
  atomicidade é responsabilidade da coordenação controlador/runtime/dispatch,
  não da camada visual.

### Integração de dispatch (evolução pontual)

- `demo/demo.py` — somente o ponto focal onde `Espaço` já é despachado para
  o Console de Estilo (mesma região que já intercepta `F4`/`Esc` para
  `_ID_TELA_H0063`, `demo/demo.py:860-895`): acrescentar a chamada à nova
  capacidade de mutação do candidato descrita acima, no mesmo evento atômico
  de §7.1; e aplicar a sequência ordenada de saída efetiva de §4.5/§12.2
  (recriar candidato → reconciliar selecoes → verificar coerência → sair)
  em toda saída efetiva da tela. Não criar decoder ou dispatcher paralelo;
  não duplicar o tratamento de `F4`/`Esc` já existente.

Permanecem, como já valia em H-0063/H-0064, fontes/infraestrutura canônicas
a consumir sem alteração: `config/estilo.json`, `tela/loader.py`,
`tela/navegacao.py`, `tela/selecao.py`, `tela/renderizacao/tela.py`,
`tela/renderizacao/console.py`, `tela/renderizacao/estilo.py`,
`tela/renderizador.py`, `tela/renderizacao/contexto_execucao.py`,
`tela/carregamento/estilo.py` e os contratos vigentes. Nenhuma alteração
autorizada em `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
— nenhuma mudança declarativa é necessária. Renderer permanece fora da lista
de arquivos autorizados a alterar.

### Fixture/demo e testes (dedicados a H-0065)

- `tela/teste_estilo_h0065.py` — testes dedicados de vinculação
  escolha↔candidato, ciclo de vida (nascimento/reinicialização/descarte
  imediato), atomicidade, fonte única, reconciliação de filho escolhido,
  pais independentes, preset inválido, redraw/resize, Esc filho vs saída;
  não duplica os testes estruturais/de navegação/de amostra já cobertos por
  `tela/teste_estilo_h0063.py` e `tela/teste_estilo_h0064.py`.
- `demo/teste_demo_estilo_h0065.py` — demonstração reproduzível com `F4`,
  `Espaço` mutando candidato, verificação de baseline/global/arquivo
  intactos, saída efetiva com descarte imediato e reabertura; reutiliza o
  mesmo F4/pilha de telas/decoder de `demo/demo.py` sem caminho paralelo.
- `docs/relatorios/IMP-0065-vinculacao-escolha-candidato-estilo.md` —
  relatório futuro da implementação.

Não criar fixture persistente paralela de presets: testes que precisarem de
um preset sintético ou de um preset inválido devem copiar
`config/estilo.json` para diretório temporário, como já praticado em H-0063
e H-0064.

## 19. Testes automatizados mínimos

### Inicialização

- Ao abrir a tela (nova instância de `ControladorTelaEstilo`), o candidato
  do runtime é formado conforme o ciclo de vida de §4 (igual à baseline no
  instante da abertura).
- As quatro escolhas mostradas pela tela correspondem ao `preset_default`
  do candidato recém-formado em cada categoria, após
  `reconciliar_selecoes_com_candidato()`.

### Setas

- Mover o cursor entre filhos altera apenas o filho corrente.
- Candidato, baseline, `config/estilo.json` e estilo global permanecem
  inalterados.

### Espaço — atomicidade (sucesso)

Para cada uma das quatro categorias (borda, chip, `indicadores.selecionado`,
`indicadores.incluido`):

- candidato anterior A;
- `Espaço` em B;
- candidato final B;
- `selecoes` final B;
- demais categorias do candidato preservadas;
- baseline, estilo global e `config/estilo.json` intactos.

Testar no nível em que o evento é concluído: sucesso só retorna após
candidato e `selecoes` estarem coerentes.

### Espaço — atomicidade (falha)

- candidato anterior A;
- `selecoes` anterior A;
- tentativa de preset inválido B;
- candidato continua A;
- `selecoes` continua/reconcilia A;
- nenhuma consolidação do novo escolhido;
- baseline/global/arquivo intactos.

### Nenhuma janela observável divergente

No controlador/dispatch do evento:

- sucesso só retorna após candidato e `selecoes` coerentes;
- falha retorna sem consolidação do novo escolhido.

### Fonte única — divergência artificial

- preparar `selecoes` local deliberadamente divergente do candidato;
- executar a rotina de reconciliação/renderização autorizada;
- resultado final deve refletir o candidato.

Isso prova que `selecoes` é cache/projeção, não segunda autoridade.

### Troca sucessiva

- estado inicial: candidato=A, selecoes=A;
- `Espaço` em B com sucesso → candidato=B, selecoes=B;
- `Espaço` em C com sucesso → candidato=C, selecoes=C;
- nunca candidato=C com selecoes=B.

### Pais independentes

- borda → B1; depois chip → C1;
- candidato final conserva borda=B1 e chip=C1;
- `selecoes` de cada pai projetado desse mesmo candidato.

### Redraw/resize

- candidato aponta preset B;
- provocar redraw/resize;
- escolhido continua/reconcilia B;
- não retorna silenciosamente a `preset_default` da baseline;
- nenhuma categoria candidata é perdida.

### Esc filho → pais

Separadamente da saída efetiva (este teste deve continuar distinto):

```text
baseline=A, candidato=B, selecoes=B
Esc filho→pais
resultado: candidato=B, selecoes=B
```

Assim não se confunde retorno de nível com saída da tela. Nenhum descarte
ocorre.

### Saída efetiva — instante exato (antes de qualquer novo F4)

Preparação:

```text
baseline:   borda: A
candidato:  borda: B
selecoes:   borda: B
```

Executar `Esc` de saída efetiva. Assert **imediatamente** (antes de qualquer
novo `F4`):

```text
baseline.borda == A
candidato.borda == A
selecoes.borda == A
global inalterado
config/estilo.json inalterado
```

Repetir conceitualmente para as quatro categorias ou usar parametrização.

Não aceitar como prova apenas: sair → abrir F4 → verificar A. A correção
deve ser verificável antes da reabertura.

### Saída efetiva — todas as categorias na mesma visita

Mesma visita altera mais de uma categoria:

```text
baseline:   borda: A, chip: C
candidato:  borda: B, chip: D
selecoes:   borda: B, chip: D
```

Após saída efetiva:

```text
candidato:  borda: A, chip: C
selecoes:   borda: A, chip: C
```

Isso comprova restauração do estado transitório completo.

### Saída efetiva — cache divergente antes da saída

Teste defensivo:

- candidato é recriado da baseline;
- `selecoes` ainda contém artificialmente valor antigo;
- o protocolo de saída/reconciliação deve corrigir `selecoes` antes de
  concluir.

Isso comprova que a saída não depende de o cache já estar correto.

### F4 após saída (garantia defensiva, não prova do descarte)

Somente depois de comprovar o estado pós-saída (§ acima):

- executar novo `F4`;
- confirmar novamente: `candidato == baseline` e `selecoes == candidato`.

Isso prova a garantia defensiva de nova visita, não o descarte original.

## 20. Regressões

Exigida preservação integral, sem modificação de fixture/arquivo desses
testes:

- `tela/teste_estilo_h0063.py`
- `demo/teste_demo_estilo_h0063.py`
- `tela/teste_estilo_h0064.py`
- `demo/teste_demo_estilo_h0064.py`

E suíte completa do projeto (`PYTHONDONTWRITEBYTECODE=1 python -m pytest`).

Não regredir: `F4`, tela normal, amostras, paginação, resize, Barra de
Menus, ANSI, escolha exclusiva por pai.

## 21. Validação manual

H-0065 deve ser completamente automatizável. A mutação do candidato, sua
atomicidade e a reconciliação com o filho escolhido são inteiramente
verificáveis por asserção programática (estado do runtime, comparação
candidato×baseline, leitura de `estado["selecoes"]`) — nenhum requisito
visual novo é introduzido (§13/§14), logo nenhuma validação manual TTY é
prevista para esta capacidade.

## 22. Fora de escopo

- `Enter`/`Aplicar` contextual e sua habilitação/desabilitação visual;
- chip novo na Barra de Menus;
- popup de confirmação, `CONFIRMADO`, `ABORTADO`;
- demonstração integrada (Cabeçalho + Console + Dashboard + Barra sob
  override) e Dashboard de demonstração;
- override local de demonstração;
- preview real do candidato aplicado a qualquer tela;
- persistência em `config/estilo.json`;
- publicação de novo estilo global;
- `tiling`, `cor_inativo`, `cor_alerta`, `indicadores.concluido`;
- `ITEM-0024` (agrupar pai+filhos entre páginas);
- `ITEM-0032` (política global da Barra de Menus);
- F1, F11, F2, F3, F5.

Fronteiras preservadas nesta etapa: amostras H-0064, estrutura H-0063,
Barra, paginação e resize. Continuam fora: Aplicar, Enter contextual para
Aplicar, popup, confirmação, preview real, persistência, publicação,
CONFIRMADO, ABORTADO.

## 23. Critérios de aceite

H-0065 está concluído quando prova automatizada demonstrar que:

1. abrir a tela de Estilo forma o candidato conforme o ciclo de vida fixado
   em §4, com as quatro escolhas iniciais correspondentes ao candidato após
   reconciliação;
2. setas alteram somente cursor/filho corrente, sem tocar candidato,
   baseline, estilo global ou `config/estilo.json`;
3. `Espaço` sobre filho segue o protocolo atômico de §7.1: candidato aceito
   primeiro, depois projeção de `selecoes`; sucesso só conclui com ambos
   coerentes; falha preserva candidato anterior e reconcilia `selecoes`
   para ele — sem divergência e sem segunda autoridade;
4. baseline, estilo global e `config/estilo.json` nunca mudam nesta
   capacidade, em nenhum cenário testado;
5. trocas sucessivas no mesmo pai terminam com exatamente um filho
   escolhido, coerente com o candidato (nunca candidato=C com selecoes=B);
6. pais independentes acumulam mutações corretamente no mesmo candidato,
   com `selecoes` projetado desse candidato;
7. preset inválido/inexistente não produz mutação parcial — candidato
   permanece íntegro e `selecoes` reconcilia para o candidato anterior;
8. divergência artificial de `selecoes` é corrigida pela reconciliação a
   favor do candidato; redraw/resize não perde categorias candidatas nem
   retorna silenciosamente à baseline;
9. `Esc` nos filhos preserva candidato e `selecoes` (baseline=A,
   candidato=B, selecoes=B permanece); saída efetiva cumpre a sequência
   recriar candidato → reconciliar selecoes → verificar → sair, deixando
   imediatamente `baseline=A`, `candidato=A`, `selecoes=A` (incluindo
   restauração multi-categoria e correção de cache divergente artificial);
   reabertura via `F4` reforça defensivamente `criar_candidato()` +
   reconciliação — prova distinta do descarte original;
10. as amostras de H-0064 continuam corretas e inalteradas em sua lógica de
    composição;
11. nenhum preview real, popup, `Aplicar`, persistência ou publicação
    ocorre em qualquer teste;
12. os testes de H-0063 e H-0064 continuam passando integralmente sem
    modificação de suas fixtures/arquivos;
13. a suíte completa do projeto passa.

## 24. Fronteira posterior

Após a aprovação de H-0065, a próxima partição do `ITEM-0010` — `Enter`/
`Aplicar` contextual, divergência candidato×baseline exposta na interface,
demonstração integrada com override local e popup de confirmação — será
decidida pelo gerente, observando o resultado real desta vinculação. Este
documento não numera nem especifica handoffs posteriores.
