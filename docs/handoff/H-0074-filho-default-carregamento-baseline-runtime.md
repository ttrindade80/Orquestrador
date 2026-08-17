# H-0074 — Leitura, validação e baseline runtime de `filho_default`

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0026
adr: ADR-0048
handoff: H-0074
data_criacao: 2026-08-16
status: CONCLUIDO
patch: P01
qa_handoff_pos_patch: H1_HANDOFF_APPROVED
qa_implementacao: I1_IMPLEMENTATION_APPROVED
validacao_manual: MANUAL_VALIDATION_APPROVED
predecessor_documental: ADR-0048 (patch P02) + aplicacao_documental_ADR-0048
predecessor_imediato_do_patch: RELATORIO_QA_HANDOFF_H-0074.md
achados_tratados_p01:
  - QA-H0074-001
  - QA-H0074-002
  - QA-H0074-003
  - QA-H0074-004
estado_documental_transportado:
  ADR-0048:
    patch: P02
    status: ADR_APPLIED
    decisao_fechada: filho_default (D-0026-12)
  aplicacao_documental_ADR-0048:
    status: ADR_APPLICATION_APPROVED
    contratos_reconciliados:
      - docs/contratos/contrato_console.md (secao 22.16, secao 26)
      - docs/contratos/contrato_json_console.md (secao 16, secao 16.7)
    nomenclatura_reconciliada:
      - docs/nomenclatura/32_CONSOLE.md (4.12)
      - docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md (4.7)
      - docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md (4.6)
  decisao_documental_aberta: nenhuma
dimensionamento_da_atividade:
  H-0074: leitura_validacao_carregamento_baseline_e_candidato_runtime (este handoff)
  H-0075: acao_aplicar_popup_confirmacao_persistencia_no_documento_externo
h0075_fora_de_escopo: true
```

Este handoff autoriza exclusivamente a **primeira metade** da implementação do
`ITEM-0026`: o caminho de **leitura**, desde `filho_default` no documento
externo até o candidato de runtime, materializando no produto o disposto em
`contrato_console.md` §26.2–§26.4 e §26.11 e em `contrato_json_console.md`
§16.7. Não autoriza persistência, `Aplicar`, pop-up de confirmação,
`CONFIRMADO`/`ABORTADO`, nem qualquer gravação de volta ao documento externo
— isso pertence a `H-0075`. O patch `P01` corrige QA-H0074-001 a QA-H0074-004;
não implementa código.

---

## 2. Capacidade coesa

Materializar, sobre a infraestrutura já existente de `dois_niveis_por_foco`
(ADR-0042; H-0055), o ciclo:

```text
filho_default (documento externo, por pai)
  → validação (documento inválido é rejeitado, sem fallback silencioso)
  → representação interna (NoConteudo.campos, já suportado sem mudança)
  → baseline persistida da tela
  → candidato de runtime (estado["selecoes"], já existente)
```

Nenhuma arquitetura nova é criada. A capacidade reaproveita integralmente o
mecanismo de runtime já fechado por H-0055 (`estado["selecoes"]` como
candidato do pai corrente) e apenas substitui a **origem da inicialização**
desse estado: hoje é `pai.filhos[0]` (posição); passa a ser `filho_default`
(dado semântico do produtor).

---

## 3. Autoridades (leitura integral, sem reabertura)

- `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` — decisões
  D-0026-01 a D-0026-12 (patch `P02`). D-0026-01 a D-0026-03, D-0026-10 e
  D-0026-12 são as diretamente exercitadas por este handoff; D-0026-04 a
  D-0026-09 e D-0026-11 (Aplicar, pop-up, persistência) pertencem a
  `H-0075`.
- `docs/contratos/contrato_console.md` §22.16 (política `dois_niveis_por_foco`,
  ADR-0042, preservada integralmente) e §26 (ciclo comportamental completo de
  ADR-0048) — em particular §26.2 (camadas de estado), §26.3 (carga e
  baseline), §26.4 (alteração interativa produz somente candidato) e §26.11
  (restauração em nova execução).
- `docs/contratos/contrato_json_console.md` §16 (escolha ativa persistida) e
  §16.7 (literal público fechado `filho_default`, D-0026-12, patch `P02`).
- `docs/nomenclatura/32_CONSOLE.md` §4.10 (`dois_niveis_por_foco`, seleção
  exclusiva obrigatória de filho por pai) e §4.12 (baseline persistida ×
  candidato de runtime, ADR-0048).
- `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` §4.7 (escolha ativa
  persistida como dado semântico, distinta da posição do primeiro filho).
- `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` §4.6
  (restauração da escolha ativa por pai pertence ao carregamento; a
  persistência é responsabilidade distinta, do loader nunca).

Nenhuma decisão de schema fica em aberto: `filho_default` já é o literal
público fechado (D-0026-12); a forma estrutural (`pai.filho_default` referindo
um ID de `pai.filhos`) já está fechada em `contrato_json_console.md` §16.7.

---

## 4. Contrato público fechado (transportado sem reabertura)

Para cada pai sujeito a `politica_navegacao.tipo = "dois_niveis_por_foco"`
(`contrato_console.md` §22.16):

- `filho_default` é campo público obrigatório;
- seu valor é o ID estável de exatamente um filho direto presente em
  `filhos` daquele mesmo pai;
- cada pai possui seu próprio `filho_default` — não existe `filho_default`
  global nem mapa paralelo pai → filho;
- a ordem física dos filhos não determina nem substitui `filho_default`;
  não existe representação normativa por índice ordinal;
- o primeiro filho **não é fallback** para `filho_default` ausente;
- ausência de `filho_default` em um pai aplicável é documento inválido;
- referência a ID inexistente é documento inválido;
- referência a um filho de outro pai é documento inválido;
- identidade ambígua/duplicada é documento inválido (rejeição dura na
  carga — §5.7, §7.3);
- o valor carregado constitui a baseline persistida daquele pai.

---

## 5. Achados factuais do código existente (fecham decisões operacionais)

A leitura focal do código real (§9) produziu os achados abaixo. Eles fecham,
para a futura implementação, decisões que a ADR e os contratos
deliberadamente deixaram executivas — nenhuma delas fica para o
implementador decidir.

### 5.1 O comportamento predecessor de primeiro-filho existe em dois pontos — ambos obrigatórios de eliminar

1. `tela/selecao.py`, função `_reconciliar_ids_dois_niveis` (linha ~185–199):
   quando nenhum ID marcado em runtime pertence aos filhos de um pai, o
   fallback é `pai.filhos[0]`. Esta função é chamada por
   `inicializar_escolhas_dois_niveis` (usada em `demo.py::_preparar_estado_h0055`
   e em `tela/renderizacao/console.py::_parametros_renderizacao_multinivel`)
   e também por `_transferir_escolha_dois_niveis` / `reconciliar`. **Este é o
   ponto causal que decide a baseline** e deve passar a ler `filho_default`.
   **Obrigatório**: ausência ou invalidade de `filho_default` **não** pode
   ser substituída por `pai.filhos[0]`. Nenhuma função de reconciliação
   deste arquivo pode mascarar escolha inválida com o primeiro filho.
2. `tela/navegacao.py`, função `entrar_nivel_filhos` (linha ~669–687): quando
   nenhum ID em `estado["selecoes"]` pertence aos filhos do pai corrente, o
   fallback de posicionamento do cursor é `filhos[0][0]`
   (`next(..., filhos[0][0])`). **Este fallback deixa de ser opcional**
   (QA-H0074-002). Estado válido deve chegar a este ponto já com escolha
   reconciliada; ausência de escolha válida **não** pode posicionar
   silenciosamente o cursor no primeiro filho. `entrar_nivel_filhos` usa
   somente uma escolha válida já existente em `estado["selecoes"]` ou uma
   **guarda não posicional**: devolver o estado inalterado (não entra no
   nível de filhos inventando índice). Não se altera a política de
   navegação do caminho válido (Espaço no pai com escolha reconciliada
   continua posicionando no filho escolhido).

### 5.2 `NoConteudo.campos` já transporta `filho_default` sem mudança de tipagem em `modelo.py`

`tela/modelo.py::_construir_no_conteudo` preserva em `NoConteudo.campos`
qualquer campo do nó bruto que não seja `id`, `nivel` ou `filhos` — exatamente
como já faz hoje para `titulo`, `navegavel` e `selecionavel`. `filho_default`
já chega automaticamente a `pai.campos["filho_default"]` sem alteração da
tipagem. A única alteração autorizada em `tela/modelo.py` é a **chamada** da
validação após a associação (§5.4) — não a tipagem.

### 5.3 O validador genérico de conteúdo externo não conhece política de navegação

`tela/carregamento/conteudo_externo.py::validar_conteudo_externo` valida o
documento externo de forma genérica (schema multinível — ADR-0027, seção 12.5
do contrato), sem qualquer conhecimento de `politica_navegacao.tipo` do
console que vai consumi-lo — essa política vive apenas no JSON estrutural da
tela, um documento **separado**, carregado por `tela/carregamento/tela_json.py`.
A correlação entre "este console é `dois_niveis_por_foco`" e "este documento
de conteúdo tem pais/filhos" só existe depois que ambos os documentos são
combinados. **Este validador genérico não é o lugar de checar
`filho_default`** e não deve ser ampliado para isso.

Esse loader também **não** rejeita IDs duplicados de nós em `dados`/`filhos`
— só IDs duplicados de `formato.niveis` (validação 10). Duplicidade de
identidade de pai/filho **pode ocorrer no formato real** e só é detectada
hoje por `estrutura_dois_niveis_valida` (retorno `False` silencioso, não
rejeição de documento). Ver §5.7.

### 5.4 Fronteira comum de correlação/validação (QA-H0074-001)

Levantamento dos caminhos reais que constroem ou recebem o modelo com
conteúdo externo para `dois_niveis_por_foco`, nos arquivos autorizados:

| Caminho | O que faz | Atravessa a correlação estrutura+conteúdo? |
|---|---|---|
| `demo/demo.py::_carregar_modelo_por_id` | Carrega JSON estrutural e, se o id estiver em `_CATALOGO_CONTEUDO_EXTERNO`, o documento externo; entrega ambos a `construir_modelo` | Sim — único ponto de entrada da demo. Cataloga `h0055_dois_niveis_por_foco` e `h0072_formatacao_generica_dois_niveis_por_foco` (§5.8). Não cataloga `h0063` (§5.6). |
| `tela/modelo.py::construir_modelo` | Tipa o conteúdo (`construir_conteudo_externo` / `_construir_no_conteudo`) e associa a todos os consoles (`_propagar_conteudo_externo`) | **Sim — este é o ponto em que estrutura pai-filhos, `filho_default` em `campos` e `politica_navegacao.tipo` no console já coexistem.** Qualquer consumidor (demo, teste, futuro chamador) que construa o modelo com conteúdo externo passa aqui. |
| `tela/teste_navegacao.py` | Alguns testes chamam `construir_modelo` (telas H-0040/H-0045, sem conteúdo `dois_niveis`); o bloco H-0055 monta árvores in-memory (`_arvore_h0055`) **sem** `construir_modelo` | Helpers in-memory não são carga de documento; ficam sujeitos às regras de reconciliação/guarda (§5.1), não à validação de carga. |
| `tela/estilo.py::aplicar_ao_modelo` | Atribui árvore sintetizada **depois** de `construir_modelo`, com `conteudo_externo is None` no momento da construção | Não — H-0063 (§5.6). |

`tela/carregamento/formato_dois_niveis_por_foco.py` valida só
`formato.dois_niveis_por_foco.filho` no JSON estrutural (ADR-0047), chamado
por `tela/carregamento/tela_json.py` — sem documento de conteúdo. Não é
fronteira de `filho_default`.

**Fronteira comum derivada do fluxo, não de preferência de organização:**
o menor ponto em que (1) a estrutura pai-filhos já está tipada, (2)
`filho_default` já está em `NoConteudo.campos` e (3) a relação com a
política do console pode ser validada é o final de
`tela/modelo.py::construir_modelo`, **depois** de `_propagar_conteudo_externo`.

A função de validação permanece em `tela/navegacao.py` porque é ali que já
existem os discriminadores da política (`tipo_navegacao_efetivo`,
`estrutura_dois_niveis_valida`) — não se cria módulo novo. A **chamada**
não pode ser exclusiva de `demo/demo.py`: deve ocorrer em `construir_modelo`,
para que todo consumidor aplicável a atravesse.

`navegacao.py` importa `ModeloTela` de `modelo.py` no topo. A chamada em
`construir_modelo` usa **import local** no interior da função, após montar
o `ModeloTela`, para evitar ciclo de importação. Isso é mecânica de
importação Python, não pipeline novo.

Não há bloqueio: a fronteira comum existe no fluxo atual, sem mudança
arquitetural maior.

**Gating da função** `validar_filho_default_dois_niveis(modelo)`:
percorre `modelo.corpo.elementos` descendo em `tipo == "grupo"` (sem usar
`lista_foco`/`console_e_focalizavel`, que esconderiam o erro). Para cada
`tipo == "console"` com `tipo_navegacao_efetivo == "dois_niveis_por_foco"`
e `conteudo_externo is not None`: aplica §5.5 e §5.7. Consoles sem conteúdo
associado (H-0063 no momento de `construir_modelo`) são ignorados por
construção.

### 5.5 Camada de validação: exceção de carga, distinta da topologia silenciosa

`tela/navegacao.py::estrutura_dois_niveis_valida` (linha ~87–110) devolve
`False` silenciosamente para topologias inválidas (IDs duplicados, pai sem
filhos, terceiro nível, filho não selecionável) — é usada por
`console_e_focalizavel` para decidir foco, chamada repetidamente durante a
navegação em runtime, nunca para sinalizar "documento inválido" de forma
dura. Os contratos (§16.7) usam **"documento inválido"** para
ausência/inexistência/referência cruzada de `filho_default` e para
identidade ambígua, no mesmo registro das 20 validações de
`contrato_json_console.md` §12.5 — todas implementadas como exceções
(`TelaCampoObrigatorioAusente` / `TelaEstruturaInvalida`) levantadas **uma
vez, na carga**.

**Decisão operacional fechada**: a validação de `filho_default` é checagem
de carga (levanta exceção). `estrutura_dois_niveis_valida` continua
devolvendo `False` silenciosamente para os casos de topologia que já
cobria (terceiro nível, pai sem filhos, etc.) — este handoff não converte
essas falhas ADR-0042 em exceção. A checagem de `filho_default` (ausência,
ID inexistente, filho de outro pai) aplica-se quando a topologia básica
já é `True`. A duplicidade de identidade, porém, **não** pode ser
engolida por esse gate — ver §5.7.

### 5.6 `h0063` usa `dois_niveis_por_foco` mas não passa pelo loader de conteúdo externo — fora de escopo

`config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` declara
`politica_navegacao.tipo: "dois_niveis_por_foco"`, mas seu `conteudo_externo`
**não** é carregado por `tela/carregamento/conteudo_externo.py` nem associado
por `_CATALOGO_CONTEUDO_EXTERNO` em `demo.py` (a chave
`"h0063_estilo_estrutura_navegacao_dois_niveis"` não existe nesse catálogo).
`tela/estilo.py` sintetiza sua própria árvore de `NoConteudo`/`ConteudoExterno`
a partir de `config/estilo.json` (`preset_default` por categoria, H-0061) e a
atribui **depois** da construção do modelo, via `aplicar_ao_modelo`
(`console.conteudo_externo = self._conteudo`). `preset_default` do Estilo é o
precedente estrutural citado pela ADR-0048 (D-0026-12), mas permanece, por
decisão expressa da ADR (§6, §10), fora da autoridade do `ITEM-0026`:
`config/estilo.json` e `tela/estilo.py` **não são tocados**. Consequência:
quando `construir_modelo` corre a validação, o console de `h0063` ainda tem
`conteudo_externo is None` — o gate já o ignora, sem exceção nominal por ID
de tela.

### 5.7 Identidade duplicada/ambígua no formato real (QA-H0074-004 A)

`validar_conteudo_externo` não rejeita IDs duplicados de nós. A autoridade
vigente de identidade para esta política é o conjunto `ids` de
`estrutura_dois_niveis_valida`, que devolve `False` — **não rejeita o
documento e não impede baseline por fallback**. Não existe teste concreto
hoje que prove rejeição dura de duplicidade de nós em `dois_niveis_por_foco`.

Portanto a condição **pode ocorrer no formato real** e a validação de carga
**deve** levantá-la: para cada console aplicável (§5.4), antes de formar
baseline, acumular os IDs de pais e filhos diretos; ID vazio ou já visto →
`TelaEstruturaInvalida`. Não se produz candidato/baseline. Presença de
`filho_default` (mesmo coincidente com um dos IDs duplicados) **não**
contorna essa rejeição.

Esta checagem reutiliza o mesmo critério de conjunto já usado por
`estrutura_dois_niveis_valida`; a diferença operacional é o efeito: exceção
de carga, não `False` silencioso. Não se amplia o validador genérico de
§5.3.

### 5.8 H-0072 está sujeita a `filho_default` (QA-H0074-003)

Determinação pela estrutura efetiva, não pela origem de formatação:

- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json`:
  três consoles (`console_h0072_texto`, `console_h0072_tabela`,
  `console_h0072_sem_designador`), **todos** com
  `politica_navegacao.tipo = "dois_niveis_por_foco"`.
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json`:
  documento externo multinível com dois pais (`h0072_pai_01`, `h0072_pai_02`)
  e filhos diretos; **nenhum** `filho_default` hoje.
- `demo/demo.py::_CATALOGO_CONTEUDO_EXTERNO` associa
  `h0072_formatacao_generica_dois_niveis_por_foco` →
  `h0072_formatacao_generica_dois_niveis_por_foco_conteudo`.
- O carregamento é o mesmo de H-0055: `_carregar_modelo_por_id` →
  `carregar_conteudo_externo` → `construir_modelo` →
  `_propagar_conteudo_externo` (o mesmo conteúdo é associado aos três
  consoles).

Os pais H-0072 estão sujeitos a `dois_niveis_por_foco` e, portanto, a
`filho_default`. A fixture de conteúdo H-0072 entra nominalmente nesta
implementação (§8.3). O JSON estrutural H-0072 não muda (`filho_default`
não pertence a ele).

---

## 6. Arquivos nominais desta futura implementação (H-0074)

### 6.1 Arquivos a editar

| Arquivo | Papel atual | Delta causal exigido |
|---|---|---|
| `tela/modelo.py` | `construir_modelo` tipa e propaga conteúdo; não chama validação de política | Após `_propagar_conteudo_externo` e após montar o `ModeloTela`, chamar `navegacao.validar_filho_default_dois_niveis(modelo)` via import local (ciclo com `navegacao.py`). Sem mudança de tipagem de `NoConteudo`/`ConteudoExterno`. Sem essa chamada, consumidores fora da demo não atravessam a validação. |
| `tela/navegacao.py` | Não valida `filho_default`; `entrar_nivel_filhos` faz `next(..., filhos[0][0])` | (1) Adicionar `validar_filho_default_dois_niveis(modelo)`, importando `TelaCampoObrigatorioAusente` e `TelaEstruturaInvalida` de `tela.carregamento.erros`. Percorre elementos como em §5.4. Duplicidade → `TelaEstruturaInvalida` (§5.7). Quando `estrutura_dois_niveis_valida` é `True`: ausência de `filho_default` → `TelaCampoObrigatorioAusente`; valor que não é ID de filho direto daquele pai → `TelaEstruturaInvalida`. (2) **Obrigatório**: em `entrar_nivel_filhos`, eliminar `filhos[0][0]`. Usar somente o índice do filho cujo `id` está em `estado["selecoes"]`; se nenhum, guarda não posicional — `return dict(estado)`. Sem mudança em `estrutura_dois_niveis_valida`, `_indices_dois_niveis`, `_toroide_ativo_dois_niveis`, `em_nivel_filhos`, `rotulo_esc_dois_niveis`, `retornar_nivel_pais`, `mover_*`. |
| `tela/selecao.py` | `_reconciliar_ids_dois_niveis` usa `pai.filhos[0]` como fallback | Trocar o fallback posicional: se nenhum ID marcado pertence aos filhos do pai, buscar `filho.id == pai.campos.get("filho_default")` entre `pai.filhos`. Se `filho_default` estiver ausente ou não identificar exatamente um filho direto, **não** usar `pai.filhos[0]` — omitir escolha inventada para aquele pai. `alternar`, `_transferir_escolha_dois_niveis`, `inicializar_escolhas_dois_niveis`, `limpar` e `reconciliar` continuam chamando `_reconciliar_ids_dois_niveis` sem mudança de assinatura. Atualizar o docstring de `inicializar_escolhas_dois_niveis` (hoje diz "derivada da ordem dos filhos"). |
| `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` | 5 pais, 4 filhos cada, nenhum `filho_default` | Acrescentar `filho_default` a cada um dos 5 pais, usando IDs já existentes (§8.1). |
| `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json` | 2 pais, 3 filhos cada, nenhum `filho_default`; catalogada e sujeita à política (§5.8) | Acrescentar `filho_default` a cada pai, usando IDs já existentes (§8.3). Nenhum nó, campo estrutural, nível ou apresentação é criado, removido ou renomeado. |
| `tela/teste_navegacao.py` | Helpers `_no_selecao`, `_arvore_h0055`, `_arvore_h0055_com_formato_filho`, `_arvore_h0055_renderizavel` sem `filho_default`; testes H-0055 assumem `["a1", "b1"]` | Estender helpers para declarar `filho_default` nos pais via `campos`. Atualizar asserções que esperam `["a1", "b1"]` para os valores de §8.2. Acrescentar os testes de §10 que cabem neste arquivo (guarda sem escolha válida; helpers com `filho_default`). |
| `tela/teste_loader.py` | Cobre validações genéricas de conteúdo e o bloco `politica_navegacao.tipo` | Testes da validação de carga via `construir_modelo` (não via wrapper da demo): ausência, ID inexistente, ID de outro pai, identidade duplicada, travessia da fronteira comum, fixture H-0072 reconciliada (§10). |

`demo/demo.py` **não** entra em §6.1: `_carregar_modelo_por_id` já chama
`construir_modelo`; `_preparar_estado_h0055` já inicializa todo console
`dois_niveis_por_foco` da `lista_foco` (H-0055 e H-0072). Nenhuma chamada
exclusiva de validação na demo.

### 6.2 Arquivos avaliados e não autorizados a editar

| Arquivo | Motivo |
|---|---|
| `demo/demo.py` | Já atravessa `construir_modelo` (§5.4). Catálogo e `_preparar_estado_h0055` permanecem. |
| `tela/carregamento/conteudo_externo.py` | Validador genérico, sem `politica_navegacao.tipo` (§5.3). |
| `tela/carregamento/formato_dois_niveis_por_foco.py` | Só `formato.dois_niveis_por_foco.filho` (ADR-0047). |
| `tela/renderizacao/console.py` e demais renderers | Consomem `estado["selecoes"]` já populado; indiferentes à origem do valor inicial. |
| `tela/estilo.py`, `config/estilo.json` | H-0063 (§5.6). Fora do `ITEM-0026`. |
| `demo/teste_demo_console.py` (cenário `h0055_dois_niveis_por_foco`) | Sem asserção de baseline por pai identificada; se a implementação revelar dependência de `["a1","b1"]`, aplica-se o ajuste de §6.1 — sem editar preventivamente. |

### 6.3 Arquivos preservados (não alterar neste handoff)

- `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md`
- `docs/contratos/contrato_console.md`, `contrato_json_console.md`
- `docs/nomenclatura/32_CONSOLE.md`, `42_DADOS_EXTERNOS_MULTINIVEL.md`,
  `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`
- `docs/backlog.md`
- `config/telas/demo/h0055_dois_niveis_por_foco.json` (estrutural)
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json`
  (estrutural — `filho_default` é só do documento externo)
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`,
  `tela/estilo.py`, `config/estilo.json` (§5.6)
- Mecanismo de pop-up, scripts de persistência, ação `Aplicar` — `H-0075`
- Apresentação visual dos filhos além do vigente (ADR-0047)

---

## 7. Estado runtime (fechado, sem decisão para o implementador)

### 7.1 Camadas (idênticas a `contrato_console.md` §26.2)

| Camada | Conteúdo | Persiste? | Onde vive neste handoff |
|---|---|---|---|
| Escolha ativa persistida | `filho_default` de cada pai no documento externo | Sim | `pai.campos["filho_default"]` |
| Baseline persistida da tela | A escolha ativa persistida tal como carregada | Substituída somente por aplicação confirmada (H-0075) | É `filho_default` relido; H-0074 nunca grava |
| Candidato de runtime | Estado vivo acumulando transferências por Espaço | Não | `estado["selecoes"][console.id]` |
| Cursor | Mecanismo de navegação, independente da escolha | Não | `estado["cursores"][console.id]` (inalterado no caminho válido) |

### 7.2 Comportamento alvo

1. o loader recebe o documento externo (`carregar_conteudo_externo`,
   inalterado — §6.2);
2. `construir_modelo` associa estrutura e conteúdo e chama
   `validar_filho_default_dois_niveis` — **todo** consumidor aplicável
   atravessa esta chamada, inclusive a demo, sem chamada exclusiva nela;
3. a estrutura pai-filhos permanece intacta;
4. o runtime inicializa a escolha daquele pai pelo ID de `filho_default`
   (`_reconciliar_ids_dois_niveis`);
5. baseline persistida e candidato runtime começam equivalentes;
6. movimentar cursor não altera a escolha;
7. trocar a escolha em runtime altera somente o candidato;
8. pais diferentes permanecem independentes;
9. nenhuma mudança runtime grava arquivo nesta etapa;
10. nenhuma sessão anterior é usada como fonte da nova baseline;
11. estado sem escolha válida não posiciona o cursor no primeiro filho
    (`entrar_nivel_filhos` com guarda não posicional).

### 7.3 Duplicidade de identidade (rejeição de carga)

Não há rejeição dura anterior de IDs de nós em `dados` (§5.3, §5.7). A
validação de carga deste handoff levanta `TelaEstruturaInvalida` e não
produz baseline. Teste concreto: §10 item 9
(`teste_h0074_identidade_duplicada_rejeita_documento_sem_baseline`).
`filho_default` coincidente com um ID duplicado não contorna a rejeição
(o mesmo teste declara `filho_default` no documento duplicado).

---

## 8. Fixtures a reconciliar

Duas fixtures reais de `dois_niveis_por_foco` passam pelo caminho validado
(§5.6 exclui `h0063`; §5.8 inclui H-0072).

### 8.1 H-0055 — demonstração manual e testes

`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`

| Pai | Filhos existentes | `filho_default` |
|---|---|---|
| `pai_01` | `filho_01_01`..`filho_01_04` | `filho_01_02` |
| `pai_02` | `filho_02_01`..`filho_02_04` | `filho_02_03` |
| `pai_03` | `filho_03_01`..`filho_03_04` | `filho_03_01` |
| `pai_04` | `filho_04_01`..`filho_04_04` | `filho_04_04` |
| `pai_05` | `filho_05_01`..`filho_05_04` | `filho_05_02` |

Valores deliberadamente não uniformes em posição (2º, 3º, 1º, 4º, 2º).

### 8.2 Fixtures de teste (helpers Python, não JSON)

`tela/teste_navegacao.py::_arvore_h0055`:

| Pai | Filhos | `filho_default` |
|---|---|---|
| `pai_a` | `a1`, `a2`, `a3` | `a2` |
| `pai_b` | `b1`, `b2` | `b1` |

`_arvore_h0055_com_formato_filho` e `_arvore_h0055_renderizavel` carregam os
mesmos valores.

### 8.3 H-0072 — teste automatizado (não é a demonstração manual)

`config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json`

Os três consoles compartilham este documento. Um `filho_default` por pai
serve a todos.

| Pai | Filhos existentes | `filho_default` |
|---|---|---|
| `h0072_pai_01` | `h0072_filho_01_01`..`h0072_filho_01_03` | `h0072_filho_01_02` |
| `h0072_pai_02` | `h0072_filho_02_01`..`h0072_filho_02_03` | `h0072_filho_02_03` |

Posições 2º e 3º — não "sempre o primeiro". Cobertura por teste
automatizado (§10 item 14). A demonstração manual usa só H-0055 (§11).

---

## 9. Manifesto de leitura já exercitado nesta etapa

- `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` (íntegro)
- `docs/contratos/contrato_console.md` §22.16, §25, §26
- `docs/contratos/contrato_json_console.md` §7.1, §15, §16
- `tela/carregamento/formato_dois_niveis_por_foco.py`
- `tela/selecao.py`; `tela/navegacao.py` (funções `dois_niveis_por_foco`)
- `tela/modelo.py` (`NoConteudo`/`ConteudoExterno`/`construir_modelo`)
- `demo/demo.py` (catálogo, `_preparar_estado_h0055`, `_carregar_modelo_por_id`)
- `config/telas/demo/h0055_dois_niveis_por_foco.json`,
  `h0055_dois_niveis_por_foco_conteudo.json`,
  `h0063_estilo_estrutura_navegacao_dois_niveis.json`,
  `h0072_formatacao_generica_dois_niveis_por_foco.json`,
  `h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json`
- `tela/estilo.py` (pontual: `preset_default` / `aplicar_ao_modelo`)
- `tela/teste_navegacao.py` (bloco H-0055); `tela/teste_loader.py`
  (conteúdo externo e `dois_niveis_por_foco`)

---

## 10. Testes obrigatórios da futura implementação

Usar exclusivamente `tela/teste_navegacao.py` e `tela/teste_loader.py`.
Nenhum diretório paralelo. Todos executáveis por `pytest`, sem TTY real.

1. `filho_default` válido inicia como candidato
   (`teste_h0055_escolha_inicial_transferencia_idempotencia_e_isolamento`,
   valores de §8.2).
2. Defaults independentes por pai (mesmo teste: `a2` e `b1`).
3. Baseline derivada do documento (`inicializar_escolhas_dois_niveis`).
4. Cursor não altera escolha (reutilizar
   `teste_h0055_tab_reseta_cursor_sem_alterar_escolhas_e_preserva_resize` e
   `teste_h0055_toroides_independentes_wrap_entrada_e_retorno`).
5. Alteração runtime sem escrita: após `selecao.alternar`,
   `pai.campos["filho_default"]` inalterado
   (`teste_h0074_alternar_nao_altera_filho_default_de_origem` em
   `tela/teste_navegacao.py`).
6. Campo ausente → `TelaCampoObrigatorioAusente` via `construir_modelo`
   (não via wrapper da demo) em `tela/teste_loader.py`.
7. ID inexistente → `TelaEstruturaInvalida` via `construir_modelo`.
8. ID de filho de outro pai → `TelaEstruturaInvalida` via `construir_modelo`.
9. Identidade duplicada/ambígua: documento no formato real (dois nós com o
   mesmo `id` entre pais/filhos de um console `dois_niveis_por_foco`),
   **com** `filho_default` declarado, passado a `construir_modelo` →
   `TelaEstruturaInvalida`; nenhuma baseline/`estado["selecoes"]` é
   produzida. Nome:
   `teste_h0074_identidade_duplicada_rejeita_documento_sem_baseline`
   em `tela/teste_loader.py`.
10. Estado runtime sem escolha válida não gera fallback para o primeiro
    filho: console com topologia válida, cursor no pai, `selecoes` vazias
    ou só com IDs que não são filhos daquele pai; `entrar_nivel_filhos`
    devolve estado com cursor inalterado — não `filhos[0][0]`. Também:
    `_reconciliar_ids_dois_niveis` / `inicializar_escolhas_dois_niveis`
    sem `filho_default` válido não devolve o ID do primeiro filho.
    Em `tela/teste_navegacao.py`:
    `teste_h0074_sem_escolha_valida_nao_posiciona_primeiro_filho`.
11. Estrutura pai-filhos preservada (IDs, ordem, quantidade) antes/depois
    da validação e da inicialização.
12. Toroides/navegação preservados: testes H-0055 já existentes continuam
    verdes após §8.2 — só literais `["a1", "b1"]` quando aplicável.
13. Todos os consumidores aplicáveis atravessam a validação: os itens 6–9
    chamam `construir_modelo` diretamente. Isso cobre demo e qualquer
    outro chamador. Não se aceita teste que só invoque um wrapper da demo.
14. Fixture H-0072 reconciliada: `carregar_tela` +
    `carregar_conteudo_externo` + `construir_modelo` de
    `h0072_formatacao_generica_dois_niveis_por_foco` não levanta; cada pai
    de §8.3 tem `campos["filho_default"]` igual à tabela; após
    `inicializar_escolhas_dois_niveis` o candidato de cada console
    aplicável corresponde a esses IDs, não ao primeiro filho.

---

## 11. Demonstração reproduzível

Fixture manual suficiente:
`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`
(estrutural `h0055_dois_niveis_por_foco` inalterada). H-0072 fica coberta
pelo teste §10 item 14 — não é obrigatória na demonstração TTY.

Procedimento somente leitura (a demonstração **não** restaura nem reescreve
a fixture para mascarar alteração):

1. Obter digest **antes**:
   `sha256sum config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`
   — anotar `HASH_ANTES`.
2. Executar `demo/demo.py` (ponto de entrada real, `contrato_console.md`
   §20.5); abrir o cenário `h0055_dois_niveis_por_foco`.
3. Observar: cada um dos 5 pais inicia com o filho de §8.1, não com o
   primeiro da lista; ao menos dois pais em posições diferentes.
4. Mover o cursor entre pais e entre filhos — a escolha de nenhum pai muda.
5. Transferir a escolha por Espaço em um pai (somente runtime). Os demais
   pais permanecem com seus `filho_default`. Não existe `Aplicar` nesta
   etapa.
6. Encerrar a demonstração.
7. Obter digest **depois**, no mesmo arquivo, com o mesmo comando —
   anotar `HASH_DEPOIS`.
8. Confirmar `HASH_ANTES == HASH_DEPOIS`.

Reabrir o cenário (nova carga) restaura os `filho_default` do documento;
nenhum estado de sessão anterior é fonte.

Validação visual interativa em TTY, se necessária, permanece exclusiva do
usuário.

---

## 12. Relatório da futura implementação

Arquivo: `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0074.md`

Máximo normal: 900 palavras. Deve registrar exclusivamente:

- arquivos efetivamente alterados, frente à lista fechada de §6.1;
- confirmação de que os arquivos de §6.2 e §6.3 não foram tocados;
- onde `filho_default` é lido, validado (`construir_modelo` →
  `validar_filho_default_dois_niveis`) e onde vira baseline/candidato;
- confirmação de que a demo não é a única chamada de validação;
- fixtures reconciliadas (§8.1 e §8.3);
- testes executados (§10) e resultado;
- demonstração executada (§11), com os dois digests e a igualdade;
- desvios, se houver; bloqueios, se houver.

---

## 13. Exceção operacional futura

Se a implementação descobrir necessidade de alterar um caminho não
autorizado por este handoff (§6.1), deve **parar antes da alteração** e
informar: caminho; motivo; mudança necessária; impacto se não autorizado.
Não presumir autorização implícita para nenhum arquivo fora de §6.1.

---

## 14. Fronteiras — não cobertas por este handoff

- Gravação de `filho_default`; script de persistência; ação `Aplicar`;
  pop-up de confirmação; `CONFIRMADO`; `ABORTADO`; atualização da baseline
  após escrita; atomicidade — tudo pertence a `H-0075`.
- Apresentação `Pai: filho_ativo`; promoção visual — `ITEM-0023`.
- Geometria/distribuição de grupos — `ITEM-0024`.
- Redesenho de navegação, toroides, cursor, geometria ou apresentação dos
  filhos (ADR-0042/ADR-0047, já fechados e preservados integralmente).
- Registro/dispatcher genérico de ações (`ITEM-0004`).

---

## 15. Critérios de aceite do handoff (auto-verificação de fechamento)

- [ ] O schema de `filho_default` está transportado literalmente da ADR-0048
  P02 e de `contrato_json_console.md` §16.7, sem reabertura.
- [ ] A fronteira comum é `construir_modelo` após associação (§5.4); a
  demo não é a única chamada.
- [ ] A lista de arquivos de §6.1 é nominal e inclui `tela/modelo.py`,
  `entrar_nivel_filhos` obrigatório e a fixture H-0072.
- [ ] Fallback posicional em reconciliação e em `entrar_nivel_filhos` é
  obrigatoriamente eliminado (§5.1, §6.1).
- [ ] H-0072 está incluída com valores fechados (§5.8, §8.3), não excluída
  por origem de formatação.
- [ ] H-0063 permanece excluído com justificativa factual (§5.6).
- [ ] Teste negativo de identidade duplicada e prova por `sha256sum`
  constam de §10 item 9 e §11.
- [ ] Os 14 testes de §10 apontam para arquivos reais já existentes.
- [ ] H-0075 está explicitamente fora de escopo em §1 e §14.

---

## 16. Bloqueios

nenhum — a fronteira comum existe no fluxo atual (`construir_modelo` após
`_propagar_conteudo_externo`) sem módulo, pipeline ou arquitetura novos.
