# H-0075 — Aplicar, confirmar e persistir `filho_default`

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0026
adr: ADR-0048
handoff: H-0075
data_criacao: 2026-08-16
status: CONCLUIDO
patch: P02
qa_handoff_pos_patch: H1_HANDOFF_APPROVED
qa_implementacao: I1_IMPLEMENTATION_APPROVED
validacao_manual: MANUAL_VALIDATION_APPROVED
predecessor_imediato_do_patch: RELATORIO_QA_HANDOFF_H-0075_POS_P01.md
achados_tratados_p01:
  - QA-H0075-001
achados_tratados_p02:
  - QA-H0075-001
  - QA-H0075-002
predecessor: H-0074
relacao: continuacao_funcional
predecessor_estado:
  H-0074:
    estado: implementado_e_MANUAL_VALIDATION_APPROVED
    capacidade:
      - filho_default_obrigatorio_por_pai
      - validacao_fail_closed_na_carga
      - carregamento_pelo_documento_externo
      - baseline_inicial_derivada_de_filho_default
      - candidato_runtime_em_estado_selecoes
      - cursor_independente_da_escolha
      - ausencia_de_fallback_posicional
      - H-0055_e_H-0072_reconciliados
dimensionamento_da_atividade:
  H-0074: leitura_validacao_carregamento_baseline_e_candidato_runtime
  H-0075: acao_aplicar_popup_confirmacao_persistencia_no_documento_externo
item_0026:
  estado: ultimo_handoff
fronteira_posterior_item_0026: nenhuma
```

H-0075 é a segunda e última unidade executável do `ITEM-0026`. Consome o
estado de H-0074; não o reimplementa. Fecha o ciclo restante de
`contrato_console.md` §26.5–§26.10 e §26.12: `Aplicar`, snapshot da
tentativa, pop-up genérico, `ABORTADO`, `CONFIRMADO`, persistência
fail-closed, promoção da baseline e sincronização do candidato.

---

## 2. Capacidade coesa

```text
candidato divergente da baseline
  → Aplicar disponível
  → acionamento (Enter / chip ⏎)
  → snapshot imutável da tentativa
  → pop-up genérico tipo texto
  → ABORTADO | CONFIRMADO

ABORTADO:
  fecha a tentativa; nenhuma escrita; baseline e candidato preservados;
  Aplicar permanece ativo se ainda houver divergência

CONFIRMADO:
  persiste o snapshot no documento externo associado ao contexto carregado;
  somente filho_default pertinente muda; validação antes de autoridade;
  sucesso → nova baseline = documento persistido; candidato equalizado;
  Aplicar inativo

Falha:
  fail-closed; baseline persistida anterior permanece autoridade;
  candidato divergente preservado; tentativa não promove baseline;
  Aplicar permanece ativo
```

Unidade da aplicação: um snapshot coerente de **todos** os pais do documento
externo associado à tela aberta — não somente o pai sob o cursor.

---

## 3. Autoridades (leitura integral, sem reabertura)

- `docs/adr/ADR-0048-persistencia-escolha-filho-por-pai.md` — D-0026-01 a
  D-0026-12. Este handoff exercita D-0026-04 a D-0026-09 e consome
  D-0026-01/02/03/10/12 já materializados por H-0074.
- `docs/handoff/H-0074-filho-default-carregamento-baseline-runtime.md` —
  predecessor; fora de reabertura.
- `docs/contratos/contrato_console.md` §22.16 e §26.
- `docs/contratos/contrato_json_console.md` §16 / §16.7.
- `docs/contratos/contrato_popup.md` — sistema genérico; `CONFIRMADO` /
  `ABORTADO`; o pop-up não persiste.
- `docs/nomenclatura/32_CONSOLE.md` §4.12; `35_POPUP.md`; `42` §4.7; `43` §4.6.

Precedentes executivos de infraestrutura (não autoridade do ITEM-0026):
H-0066, H-0067, H-0068. A analogia é de filosofia/infraestrutura, não de
negócio com Estilo.

---

## 4. Achados factuais do código (fecham decisões executivas)

Nenhum dos pontos abaixo fica para o implementador decidir.

### 4.1 Candidato e baseline já existem — não criar segundo armazenamento

| Camada | Onde vive hoje (H-0074) |
|---|---|
| Escolha persistida / baseline | `pai.campos["filho_default"]` e `ConteudoExterno._raw` |
| Candidato | `estado["selecoes"][console.id]` — um filho direto por pai |
| Cursor | `estado["cursores"][console.id]` — independente |

Comparação de divergência: para cada pai de `conteudo.nos`, o ID escolhido
no candidato versus `pai.campos["filho_default"]`. Cursor não entra no
cálculo. Não há flag residual; `aplicar_disponivel` é derivado a cada
consulta, como H-0066 §5.C.

### 4.2 Ação `Aplicar` canônica já existe — não inventar tecla

Infraestrutura vigente (H-0066), a reutilizar sem redesign:

- Declaração: chip `id: chip_aplicar`, `tecla: ⏎`, `texto: Aplicar`,
  `regra_ativo: candidato_divergente` (H-0063, linhas 134–138).
- Avaliação visual: `tela/renderizacao/barra_menus.py` já interpreta
  `candidato_divergente` a partir de `_navegacao_atual["aplicar_disponivel"]`.
- Encaminhamento: `renderizar_tela(..., aplicar_disponivel=...)` já existe
  em `tela/renderizacao/tela.py` e `contexto_execucao.py`.
- Dispatch: `demo/demo.py` intercepta `comando in ("\r", "\n")` **antes**
  do ramo Todos/Executar da seleção múltipla, hoje só quando
  `tela_atual == h0063_estilo_estrutura_navegacao_dois_niveis`.

H-0055 e H-0072 **não** declaram `chip_aplicar` nem `popups`. Enter nessas
telas hoje cai no ramo de seleção múltipla (`politica_selecao: multipla`):
com `selecoes` já populadas por H-0074, Enter apenas reconcilia — não é
Todos. Este handoff especializa Enter nessas telas como `Aplicar`, no mesmo
padrão de H-0066, sem nova tecla e sem o dispatcher genérico do ITEM-0004.

Quando `Aplicar` está inativo, Enter é no-op (não cai em Todos).

### 4.3 Pop-up genérico já confirma `tipo: texto` — não criar tipo novo

`tela/renderizacao/popup.py` já: valida chip Enter em `tipo: texto`;
`consumir_tecla_popup` devolve `{"status": "CONFIRMADO"}` sem `valor` para
`\r`/`\n`; Esc devolve `{"status": "ABORTADO"}`; `abrir_popup(fonte, id,
conteudo)` resolve `popups[ID]` do JSON estrutural. A ramificação modal de
`demo/demo.py` (~903–943) consome toda tecla enquanto `estado["popup"]`
existe. **Não alterar `popup.py`.** Declarar um novo `popups[ID]` nas telas
alvo e um ramo de `popup_id` no dispatcher, paralelo ao de Estilo, sem
misturar os dois.

Literais dos chips: `"Voltar"` (Esc) e `"Confirmar"` (Enter) — exigidos
hoje por `_validar_chip`. Título/texto: margem de implementação, domínio da
escolha de filho, sem `filho_default` no envelope, sem listar IDs.

ID estrutural fechado:

```text
popup_confirmacao_aplicacao_filho_default
```

Envelope:

```yaml
conteudo_popup:
  tipo: texto
  texto: "<pergunta curta de confirmação, sem IDs nem filho_default>"
```

O pop-up não persiste, não altera baseline/candidato, não conhece o
documento externo.

### 4.4 Snapshot de Estilo é o precedente — copiar a forma, não o domínio

`SolicitacaoAplicacaoEstilo` (`tela/estilo.py`, `frozen`, `deepcopy` de
baseline/candidato no `__post_init__`) é o padrão. H-0075 introduz
`SolicitacaoAplicacaoFilhoDefault` em `tela/selecao.py` (onde já vive o
candidato). Não reutilizar a classe de Estilo nem o slot
`estado["solicitacao_aplicacao_estilo"]`.

Slot de sessão:

```text
estado["solicitacao_aplicacao_filho_default"]
```

### 4.5 Persistência de Estilo não é reutilizável como função

`persistir_configuracao_estilo` (`tela/carregamento/estilo.py:262-302`)
valida o documento como configuração de Estilo (`_exigir_candidato_dict` /
`materializar_configuracao_estilo`) e levanta `EstiloErro`. Chamá-la para
conteúdo externo importaria o domínio de Estilo e falharia a validação.

Não existe escritor genérico de JSON fora desse caminho. A **técnica**
atômica vigente (tempfile no mesmo diretório, `json.dump` + `\n`, `flush`,
`fsync`, `os.replace`, remoção do temporário em `finally`) é o precedente
executivo. Este handoff a replica em
`tela/carregamento/conteudo_externo.py` como
`persistir_conteudo_externo(documento, caminho_destino)`, levantando
`TelaEstruturaInvalida` em falha de escrita (família já usada pelo loader
de conteúdo; não criar exceção pública nova). Não extrair primitiva de
`estilo.py` (semântica de Estilo permanece intocada). Não chamar
`aplicar_candidato` nem publicar `estado["estilo"]`.

### 4.6 O caminho do arquivo é computado e descartado na carga — extensão mínima obrigatória

`carregar_conteudo_externo` (`tela/carregamento/conteudo_externo.py:645-698`)
compõe:

```text
base = _para_base(caminho_base)
raiz_telas = raiz_telas or "config/telas"
caminho_arquivo = base / raiz_telas / (id_conteudo + ".json")
```

Lê, valida e **devolve só o dict**. `ConteudoExterno` (`tela/modelo.py:208-222`)
guarda `_raw` (documento original, todos os campos) mas **não** o caminho.
`construir_modelo` não abre arquivo. `demo/demo.py::_CATALOGO_CONTEUDO_EXTERNO`
mapeia `id_tela → id_conteudo`; `_carregar_modelo_por_id` usa
`caminho_base=None` (raiz do repositório) e `_RAIZ_TELAS_DEMO`.

Proveniência fechada (não “descobrir na implementação”):

1. `id_tela` corrente (`estado["tela_atual"]`).
2. `id_conteudo = _CATALOGO_CONTEUDO_EXTERNO.get(id_tela)` — ausência ⇒ tela
   sem documento externo ⇒ esta capacidade não se aplica (H-0063 permanece
   fora: conteúdo sintético de Estilo, `Aplicar` já é o de H-0066–H-0068).
3. Caminho canônico:
   `resolver_caminho_conteudo_externo(caminho_base, id_conteudo, raiz_telas)`
   — **mesma** composição extraída de `carregar_conteudo_externo`, sem
   segunda fórmula.
4. Override de sessão, só para cópia/teste/demonstração:
   `estado["caminhos_conteudo_externo"][id_tela]` (Path). Não é schema
   público JSON. Quando presente, é o `caminho_arquivo` efetivo.
5. `ConteudoExterno.caminho_origem` (campo runtime, default `None`) recebe
   o Path efetivo no momento de `construir_conteudo_externo` /
   `construir_modelo`. Persistência lê **somente** esse campo congelado no
   snapshot; nunca o título visual da tela.

`carregar_conteudo_externo` ganha parâmetro opcional `caminho_arquivo=None`:
quando fornecido, usa-o no lugar da composição; a identidade `id_conteudo`
permanece para mensagens. Callers atuais omitem o parâmetro — comportamento
idêntico.

### 4.7 `_raw` é a fonte para escrita preservadora

`construir_conteudo_externo` atribui `_raw=conteudo_raw` (o dict validado
na carga). A persistência **copia** `_raw`, altera só `filho_default` dos
pais cujo ID está no snapshot e cujo valor diverge, e grava essa cópia.
Não reconstruir `dados` a partir de `NoConteudo` (perderia campos
desconhecidos: `titulo`, `navegavel`, `selecionavel`, tabelas, amostras,
campos adicionais).

Localização dos pais em `_raw["dados"]` (e, se um pai aplicável não for
topo, nos `filhos` aninhados): casar por `id` estável. H-0055 e H-0072
têm pais exclusivamente em `dados[]`.

### 4.8 Vários consoles podem compartilhar o mesmo documento (H-0072) — candidato único por pai

H-0072: três consoles, um `ConteudoExterno` (mesma referência via
`_propagar_conteudo_externo` — `console.conteudo_externo is
modelo.conteudo_externo` para os três). A identidade da escolha **não é o
console**: é o **pai** do documento externo carregado (`pai.id`, estável —
o mesmo objeto `NoConteudo`, compartilhado por referência entre os
consoles que exibem o mesmo documento). Unidade semântica fechada:

```text
documento externo + pai  →  uma baseline  →  um candidato
```

Não é unidade por console. Para o mesmo documento e o mesmo pai existem
uma única baseline semântica e um único candidato semântico. Foco, ordem
de consoles e `lista_foco` não possuem precedência: `lista_foco` ordena
travessia/navegação (contrato_console §22.2; nomenclatura 32 §4.5) e nada
além disso. `filho_default` permanece a única autoridade persistida.

Se o runtime apresentar valores distintos para o mesmo documento + pai,
isso é **defeito de estado interno**, não escolha do usuário. O sistema
não elege um dos valores.

**Representação runtime — sem novo armazenamento e sem schema externo
novo.** A estrutura de `estado["selecoes"]` de H-0074
(`console.id → lista de IDs`) permanece exatamente a mesma. Isoladamente,
H-0074 não replica a escolha de um console para os outros — comportamento
correto e preservado no escopo próprio de H-0074. Este patch acrescenta
somente: (1) sincronização, no mesmo evento de Espaço, da escolha **daquele
pai** nos destinos elegíveis; (2) validação de coerência na leitura do
mapa candidato, fail-closed se as representações do mesmo pai divergirem.

**Predicado fechado de destino (QA-H0075-002).** Um console só participa
do compartilhamento de candidato quando cumulativamente:

1. pertence ao `modelo` da sessão relevante (o mesmo objeto passado a
   `alternar` / às funções da §5);
2. referencia o mesmo objeto `ConteudoExterno` do console de origem —
   identidade `is`, não igualdade de valor nem ID de conteúdo; a garantia
   de "mesmo documento" vem de `_propagar_conteudo_externo`;
3. está sujeito à política `dois_niveis_por_foco`, identificada pelo
   mecanismo já existente `navegacao.tipo_navegacao_efetivo(console) ==
   "dois_niveis_por_foco"` (o mesmo discriminador de
   `validar_filho_default_dois_niveis` em H-0074; equivalente a
   `selecao._eh_dois_niveis_por_foco`, que lê `politica_navegacao.tipo`
   em `_campos_inertes` — nenhum marcador público novo);
4. apresenta o mesmo pai identificado: `pai.id` ocorre em
   `console.conteudo_externo.nos`;
5. utiliza a semântica de escolha exclusiva de filho governada por
   ITEM-0026 (a própria política `dois_niveis_por_foco` com conteúdo
   externo associado — H-0063 permanece fora, §4.9).

Apenas compartilhar o documento **não basta**. Destino exige a **mesma
política** `dois_niveis_por_foco` e o mesmo pai. Não propagar
`estado["selecoes"]` do ITEM-0026 para console que use política diferente,
possua semântica de seleção distinta, apenas compartilhe o mesmo
documento, ou não apresente aquele pai.

A enumeração dos destinos percorre a árvore de `modelo.corpo.elementos`
descendo em `tipo == "grupo"` — o mesmo descenso de
`validar_filho_default_dois_niveis` / `_validar_filho_default_em_elementos`.
`lista_foco` **não** é o conjunto de quem participa: ela só ordena foco.

**Propagação por pai, não por estado excessivo (extensão aditiva de
`tela/selecao.py`).** `alternar(estado, console, id_item, modelo=None)` e
`_transferir_escolha_dois_niveis(estado, console, id_item, modelo=None)`
ganham parâmetro opcional `modelo=None`, compatível com toda chamada de
H-0074 que não o informa (comportamento idêntico: sem propagação, sem
quebra de teste existente). Chamada sem `modelo` **não** ganha autoridade
para resolver concorrência entre consoles. Consumidores que operem um
modelo compartilhado e precisem da semântica ITEM-0026 passam
`modelo=modelo`. Se, por qualquer motivo, estado independente chegar à
etapa Aplicar, a validação de coerência (§4.8.1) impede persistência
arbitrária. H-0074 não é reaberto.

Quando `modelo` é informado e o console de origem satisfaz o predicado:
depois de reconciliar e gravar a transferência **daquele pai** no console
de origem (`_reconciliar_ids_dois_niveis` + `_escrever_selecao`, vigentes),
sincroniza-se somente a escolha referente a `pai_alvo` em cada destino
elegível. A estrutura existente é lista de IDs por `console.id`:

- preservar entradas independentes não relacionadas ao `pai_alvo`;
- na lista do destino, remover o ID que pertence aos filhos de
  `pai_alvo` e inserir o novo filho escolhido; reconciliar o destino com
  `_reconciliar_ids_dois_niveis`;
- não copiar a lista reconciliada inteira do originador;
- não copiar escolhas de pais que o destino não apresenta;
- não sobrescrever `estado["selecoes"]` de console fora do predicado.

`demo/demo.py` passa `modelo=modelo` no ramo de Espaço de
`dois_niveis_por_foco` (`modelo` já está em escopo, ao lado do ramo
H-0063 que já o usa).

Consequência observável no caminho saudável: mover o cursor ou trocar o
console focado não altera o candidato; alterar a escolha de um pai em um
console elegível atualiza, no mesmo evento, só essa escolha nos demais
elegíveis que apresentam esse pai. H-0072 (três consoles
`dois_niveis_por_foco`, mesmo `ConteudoExterno`) permanece caso positivo.

**Leitura para Aplicar (`mapa_candidato_filho_default`) — agrupamento
semântico, não eleição (QA-H0075-001).** A função **não** consulta um
console aplicável e adota o valor dele. Constrói o mapa agrupando
representações por documento externo + `pai.id`:

1. enumerar consoles do `modelo` pelo mesmo descenso da validação H-0074;
2. para cada pai `P` em `modelo.conteudo_externo.nos`, coletar a escolha
   reconciliada de `P` em cada console que satisfaz o predicado de destino
   e apresenta `P`;
3. zero ou mais representações equivalentes do mesmo candidato são
   aceitas; se todas as representações coletadas de `P` forem iguais,
   produzir uma única entrada `candidato[P.id]`;
4. se existirem dois valores distintos para o mesmo documento + `P`,
   falhar fechado (§4.8.1) — não produzir entrada vencedora;
5. nunca eleger valor por primeiro, último, console focado, console
   avulso, ou ordem de `lista_foco`.

`baseline[P.id] = P.campos["filho_default"]` como antes. O mapa é
indexado por `pai.id`, nunca por par console-pai.

`aplicar_disponivel_filho_default` só considera estado candidato
**coerente**. Inconsistência interna **não** é "divergência aplicável":
não interpreta o estado ambíguo como candidato válido pronto para
persistência; devolve `False`. Divergência aplicável é unicamente
`mapa_candidato != mapa_baseline` quando o mapa pôde ser construído de
forma coerente e única por pai, independente da ordem dos consoles.

Após sucesso, equalizar `selecoes` ao snapshot somente nos consoles que
satisfazem o predicado de destino (as três vistas H-0072 voltam a
coincidir). Consoles de outra política não são tocados.

### 4.8.1 Fail-closed para inconsistência runtime (QA-H0075-001)

Quando o agrupamento encontrar candidatos divergentes para o mesmo
documento + pai:

- não criar `SolicitacaoAplicacaoFilhoDefault`;
- não abrir confirmação para persistência desse estado;
- não gravar arquivo;
- não alterar baseline;
- não eleger vencedor;
- preservar o documento persistido anterior.

Sinalização interna, família já usada por este handoff (§4.5, §8.2):
`mapa_candidato_filho_default` levanta `TelaEstruturaInvalida`
(`tela.carregamento.erros`). Não é resultado público de pop-up nem schema
novo. `aplicar_disponivel_filho_default` e
`solicitar_aplicacao_filho_default` capturam essa exceção internamente:
disponibilidade `False`; solicitação `None`. Nenhuma das duas propaga a
exceção ao loop — o mesmo padrão já fechado para falha de persistência
em `aplicar_solicitacao_filho_default`. Enquanto houver inconsistência,
não há snapshot. A inconsistência é defeito de estado runtime, não
escolha do usuário.

### 4.9 H-0063 não é destino desta capacidade

Tela de Estilo: `Aplicar` / pop-up / persistência já pertencem a
H-0066–H-0068 (`config/estilo.json`, publicação global). O gate de H-0074
já ignora o console H-0063 em `construir_modelo` (`conteudo_externo is
None`). Dispatch de H-0075: **não** interceptar Enter quando
`tela_atual` é a tela de Estilo ou `tela_estilo` está ativo. Nenhuma
publicação de estilo ocorre neste delta.

### 4.10 Enter atômico: solicitação + pop-up + (no CONFIRMADO) persistência

Como H-0067/H-0068: no mesmo evento de Enter ativo, produzir o snapshot e
abrir o pop-up. No mesmo evento de Enter/Confirmar do pop-up, se
`CONFIRMADO`, persistir o snapshot retido — não reler o candidato mutável.
Nenhuma tecla intermediária alcança a tela (modalidade já vigente).

---

## 5. Controlador e fronteira de Aplicar

**Controlador:** funções novas em `tela/selecao.py` (módulo que já possui
o candidato). Não criar `ControladorTelaEstilo` paralelo nem módulo novo.

Funções nominais:

| Função | Contrato |
|---|---|
| `mapa_baseline_filho_default(modelo)` | `{pai_id: filho_id}` a partir de `pai.campos["filho_default"]` dos pais de `modelo.conteudo_externo` |
| `mapa_candidato_filho_default(estado, modelo)` | `{pai_id: filho_id}` único por pai, agrupado por documento + `pai.id` (§4.8). Representações equivalentes → uma entrada. Valores distintos para o mesmo pai → `TelaEstruturaInvalida` (§4.8.1). Não elege valor por console nem por ordem |
| `aplicar_disponivel_filho_default(estado, modelo)` | `True` somente se o mapa candidato for coerente e `mapa_candidato != mapa_baseline`. `False` se a capacidade não se aplica (`conteudo_externo is None`, nenhum console `dois_niveis_por_foco`) **ou** se a construção do mapa falhar fechado por inconsistência interna — inconsistência não é divergência aplicável. Captura `TelaEstruturaInvalida` internamente |
| `solicitar_aplicacao_filho_default(estado, modelo)` | Se não disponível ou se o mapa não for coerente, `None` (não cria snapshot). Senão, `SolicitacaoAplicacaoFilhoDefault` frozen com cópias profundas de baseline, candidato e `str(caminho_origem)` |
| `conteudo_popup_confirmacao_filho_default(solicitacao)` | envelope `tipo: texto` derivado da solicitação já recebida; não relê `selecoes` |
| `aplicar_solicitacao_filho_default(solicitacao, estado, modelo)` | consome `solicitacao.candidato`; persiste; promove baseline; sincroniza `selecoes`; devolve `(estado, sucesso: bool)`. Captura falha internamente; não propaga exceção ao loop |

Ponte UI (igual H-0066, outro controlador):

```text
aplicar_disponivel := aplicar_disponivel_filho_default(estado, modelo)
```

quando a tela corrente **não** é a de Estilo e a capacidade se aplica.
`demo/demo.py` injeta esse valor em `renderizar_tela` no mesmo ponto que
já injeta o de Estilo (hoje `None` fora de H-0063). Não flag independente.

Tela aplicável (deteção estrutural, **sem** hardcode de H-0055/H-0072 como
únicos destinos):

```text
modelo.conteudo_externo is not None
e existe console dois_niveis_por_foco com esse conteúdo
e ConteudoExterno.caminho_origem is not None
e tela_atual não é a tela de Estilo
```

H-0055 e H-0072 são as fixtures reais que satisfazem o predicado após a
declaração do chip/pop-up e o transporte do caminho.

---

## 6. Representação da solicitação / snapshot

```python
@dataclass(frozen=True)
class SolicitacaoAplicacaoFilhoDefault:
    caminho_destino: str
    baseline: dict   # pai_id -> filho_id
    candidato: dict  # pai_id -> filho_id (todos os pais, não só divergentes)
```

`SolicitacaoAplicacaoFilhoDefault` somente é criada depois de
`mapa_candidato_filho_default` devolver mapa coerente, único por pai e
independente da ordem dos consoles. Inconsistência interna (§4.8.1) não
produz instância. Uma vez criada, permanece frozen.

`__post_init__` faz `deepcopy` de `baseline` e `candidato` e congela
`caminho_destino` como `str`. Mutar `estado["selecoes"]` depois **não**
altera a instância. `CONFIRMADO` persiste `solicitacao.candidato`, nunca
uma releitura de `selecoes`.

O mapa candidato inclui pais não divergentes para que a tentativa seja o
estado coerente completo; a escrita (seção 8) altera somente os
`filho_default` cujo valor no candidato difere do valor em `_raw` no
instante da persistência (ou, equivalentemente, de `solicitacao.baseline`
— os dois coincidem se `_raw` não foi mutado, o que H-0074 garante).

---

## 7. Integração do pop-up e transições

### 7.1 Abertura

No ramo Enter de `demo/demo.py`, **depois** do intercepto H-0063 e
**antes** do Todos/reconciliação, se a tela é aplicável (§5):

1. `solicitacao = solicitar_aplicacao_filho_default(...)`
2. se `None`: no-op; não abrir pop-up; não Todos — cobre Aplicar inativo
   **e** inconsistência interna (§4.8.1)
3. senão: `abrir_popup(modelo, "popup_confirmacao_aplicacao_filho_default",
   conteudo_popup_confirmacao_filho_default(solicitacao))`; gravar
   `estado["solicitacao_aplicacao_filho_default"]` e `estado["popup"]`

A declaração `popups[popup_confirmacao_aplicacao_filho_default]` vive no
JSON **estrutural** da tela (H-0055 e H-0072), forma idêntica à de H-0063
(tipo texto, chips Esc/Voltar→ABORTADO, Enter/Confirmar→CONFIRMADO).

### 7.2 ABORTADO

Na ramificação modal, se `popup_id == popup_confirmacao_aplicacao_filho_default`
e `status == ABORTADO`:

1. fechar pop-up (`popup=None`, gravar `popup_resultado`);
2. descartar `solicitacao_aplicacao_filho_default`;
3. permanecer na mesma `tela_atual`;
4. não escrever arquivo;
5. não alterar `selecoes`, cursores, `pai.campos`, `_raw`;
6. `aplicar_disponivel` recalcula (permanece True se ainda houver divergência);
7. nova tentativa posterior é permitida (novo Enter produz novo snapshot).

`Esc` do pop-up não é saída efetiva da tela (não confunde com Esc da
navegação `dois_niveis_por_foco`).

### 7.3 CONFIRMADO

No mesmo evento, se `status == CONFIRMADO`:

1. fechar pop-up;
2. se a solicitação retida não for instância válida: no-op (sem escrita);
3. senão chamar `aplicar_solicitacao_filho_default`;
4. sucesso ou falha: descartar a solicitação daquela tentativa (sem retry
   automático da mesma instância — novo Enter gera nova);
5. não propagar exceção ao loop (`TelaEstruturaInvalida` capturada).

Não abrir demonstração integrada de Estilo (H-0069). O pop-up abre sobre a
própria tela de seleção (`contrato_popup.md` §2).

---

## 8. Persistência, destino, validação e promoção

### 8.1 Função e camada

`tela/carregamento/conteudo_externo.py`:

- `resolver_caminho_conteudo_externo(caminho_base, id_conteudo, raiz_telas=None)`
  — composição canônica (§4.6).
- `aplicar_filho_default_no_documento(documento, mapa_candidato)` —
  `copy.deepcopy(documento)`; para cada objeto-pai (nó com `filhos` lista)
  cujo `id` está em `mapa_candidato` e cujo `filho_default` atual difere,
  atribuir o novo ID; demais chaves e nós intocados; devolve a cópia.
- `persistir_conteudo_externo(documento, caminho_destino)` — técnica
  atômica da §4.5; destino obrigatório; não valida schema de Estilo.

Orquestração em `aplicar_solicitacao_filho_default`:

```text
documento := deepcopy(modelo.conteudo_externo._raw)
patch := aplicar_filho_default_no_documento(documento, solicitacao.candidato)
validar_conteudo_externo(patch)
validar IDs de filho_default do patch (mesmo critério de H-0074:
  exatamente um filho direto daquele pai; sem fallback posicional)
persistir_conteudo_externo(patch, solicitacao.caminho_destino)
# só após retorno sem exceção:
atualizar pai.campos["filho_default"] e _raw in-memory a partir do patch
equalizar estado["selecoes"] dos consoles que satisfazem o predicado
  de destino (§4.8) ao snapshot — não tocar console fora do predicado
```

Caminho: `solicitacao.caminho_destino`, que foi copiado de
`modelo.conteudo_externo.caminho_origem` no acionamento. Se
`caminho_origem` for `None` no acionamento, `solicitar_aplicacao` devolve
`None` (Aplicar inativo / sem persistência adivinhada).

### 8.2 Fail-closed observável

- Validação falha ⇒ nenhuma escrita; `os.replace` não ocorre.
- Escrita falha ⇒ temporário removido; arquivo destino intocado; baseline
  in-memory intocada; candidato intocado; `aplicar_disponivel` True.
- Não há sucesso parcial de um subconjunto de pais: um único `os.replace`
  do documento completo.
- Não mascarar falha com primeiro filho ou outro valor.
- Não promover baseline se a escrita falhou.

Teste de falha: monkeypatch de `persistir_conteudo_externo` levantando
`TelaEstruturaInvalida`, como H-0068 faz com `persistir_configuracao_estilo`.

### 8.3 Promoção e sincronização

Somente após persistência válida:

- `_raw` e `pai.campos["filho_default"]` passam a refletir o patch
  (nova baseline);
- `selecoes` dos consoles que satisfazem o predicado de destino (§4.8) =
  lista de IDs do snapshot candidato (ordem: percorrer pais de
  `conteudo.nos`); consoles de outra política ou que não apresentam os
  pais permanecem intocados;
- cursores inalterados (sem promoção/reposicionamento);
- `aplicar_disponivel` deriva False.

Nova carga (`carregar_conteudo_externo` + `construir_modelo` +
`inicializar_escolhas_dois_niveis`) restaura os novos defaults do arquivo
— regressão de H-0074 sobre o documento já persistido (cópia de teste).

---

## 9. Relação com H-0074 e com Estilo

**Reutilizar de H-0074:** `filho_default` em `campos`; validação de carga;
`_reconciliar_ids_dois_niveis` / `inicializar_escolhas_dois_niveis`;
`estado["selecoes"]`; fixtures H-0055/H-0072 já reconciliadas; guarda não
posicional de `entrar_nivel_filhos`. Não alterar essas regras. Única
extensão aditiva autorizada por este patch sobre essa superfície: o
parâmetro opcional `modelo=None` de `alternar` /
`_transferir_escolha_dois_niveis` e a sincronização **por pai** que ele
habilita nos destinos do predicado fechado (§4.8) — assinatura
compatível; comportamento de H-0074 idêntico quando `modelo` não é
informado; chamada sem `modelo` não resolve concorrência.

**Reutilizar de Estilo (infraestrutura):** chip `chip_aplicar` +
`candidato_divergente` + `aplicar_disponivel`; dataclass frozen de
solicitação; `abrir_popup` / modalidade / `CONFIRMADO`/`ABORTADO`; Enter
no mesmo evento; persistência atômica tempfile+`os.replace`; descarte da
solicitação após ABORTADO ou após CONFIRMADO consumido; fail-closed sem
popup de erro novo.

**Não importar:** `config/estilo.json`; `persistir_configuracao_estilo`;
`aplicar_candidato`; publicação / `estado["estilo"]`; override H-0069;
`preset_default`; categorias visuais; `ControladorTelaEstilo`;
`ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO`.

---

## 10. Arquivos nominais da futura implementação

### 10.1 Arquivos a editar

| Arquivo | Delta causal |
|---|---|
| `tela/selecao.py` | Dataclass `SolicitacaoAplicacaoFilhoDefault`; funções da §5 e orquestração da §8; constante `ID_POPUP_CONFIRMACAO_FILHO_DEFAULT = "popup_confirmacao_aplicacao_filho_default"`. Parâmetro opcional `modelo=None` em `alternar` e `_transferir_escolha_dois_niveis` com sincronização **por pai** nos destinos do predicado fechado da §4.8 (extensão aditiva; sem mudança de assinatura para chamadores que não o informam). `mapa_candidato_filho_default` agrupa por documento + pai e falha fechado se as representações divergirem (§4.8.1). |
| `tela/carregamento/conteudo_externo.py` | `resolver_caminho_conteudo_externo`; `caminho_arquivo` opcional em `carregar_conteudo_externo`; `aplicar_filho_default_no_documento`; `persistir_conteudo_externo`. `validar_conteudo_externo` inalterado em política. |
| `tela/modelo.py` | Campo runtime `caminho_origem=None` em `ConteudoExterno`; `construir_conteudo_externo(..., caminho_origem=None)`; `construir_modelo(..., caminho_conteudo=None)` propaga ao tipar o dict. Sem mudança de tipagem de `filho_default`. Sem schema JSON novo. |
| `demo/demo.py` | (1) `_carregar_modelo_por_id(id_tela, caminho_conteudo=None)` usa override ou `resolver_caminho_conteudo_externo` e passa `caminho_conteudo` a `construir_modelo`. (2) Preservar `solicitacao_aplicacao_filho_default` e `caminhos_conteudo_externo` no copy de `processar_comando`. (3) Enter aplicável §7.1. (4) Ramo modal do novo `popup_id` §7.2–§7.3. (5) Injetar `aplicar_disponivel` fora de Estilo via §5. (6) No ramo de Espaço de `dois_niveis_por_foco` (chamada a `selecao.alternar`, hoje sem `modelo`), passar `modelo=modelo` para habilitar a sincronização por pai da §4.8. Callers do loop passam `estado.get("caminhos_conteudo_externo", {}).get(id_tela)`. Catálogo inalterado. |
| `config/telas/demo/h0055_dois_niveis_por_foco.json` | Acrescentar `chip_aplicar` (antes de Ajuda, depois dos chips específicos) e `popups.popup_confirmacao_aplicacao_filho_default`. Não alterar corpo, política de navegação nem formatação. |
| `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json` | Idem: `chip_aplicar` + o mesmo `popups[ID]`. |
| `tela/teste_filho_default_h0075.py` | Testes de controlador/snapshot/persistência isolada com `tmp_path` (§12). |
| `demo/teste_demo_filho_default_h0075.py` | Integração ponta a ponta via `processar_comando` + cópia em `tmp_path` (§12). |
| `tela/teste_loader.py` | Somente testes focais de `resolver_caminho_conteudo_externo`, `caminho_arquivo` opcional e `persistir_conteudo_externo` (sucesso/falha atômica) em `tmp_path`. Não reescrever testes H-0074. |
| `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0075.md` | Relatório futuro. |

### 10.2 Consumir sem alterar

`tela/renderizacao/popup.py`, `tela/renderizacao/tela.py`,
`tela/renderizacao/barra_menus.py`, `tela/renderizacao/contexto_execucao.py`,
`tela/navegacao.py` (validação H-0074), `tela/estilo.py`,
`tela/carregamento/estilo.py`, `config/estilo.json`.

### 10.3 Preservados

ADRs; contratos; nomenclatura; backlog; JSON **de conteúdo** H-0055/H-0072
(não reabrir `filho_default` de H-0074; testes gravam só cópias);
renderização visual não relacionada; ITEM-0023; ITEM-0024; publicação
global de Estilo.

JSON estrutural H-0055/H-0072: alteração **somente** chip + `popups` (§10.1).
Não “corrigir” indentação/EOF históricos de `politica_paginacao` em H-0055.

Reavaliação P02: as correções QA-H0075-001 e QA-H0075-002 cabem nos
arquivos já autorizados por §10.1. Nenhum arquivo novo.

---

## 11. Compatibilidade com o worktree

| Classe de delta | Tratamento |
|---|---|
| Delta H-0075 | Somente §10.1 |
| Delta predecessor H-0074 (código/fixtures/testes ainda não commitados) | Não reabrir; não misturar no diff desta implementação além do estritamente exigido por um teste H-0074 que quebre por presença nova de `Aplicar` |
| Resíduos EOF/whitespace históricos fora do manifesto | Não corrigir neste handoff; FECHAMENTO poderá tratar whitespace/EOF mecânico do manifesto acumulado |

Se um teste predecessor afirmar literalmente ausência de `Aplicar` /
`chip_aplicar` em H-0055 ou H-0072, atualizar **somente** essa asserção.
Nenhum teste H-0055/H-0072 inspecionado afirma isso hoje
(`demo/teste_demo_h0073_h0055_reconciliado.py`, `demo/teste_demo_console.py`).

---

## 12. Testes obrigatórios da futura implementação

Arquivos: `tela/teste_filho_default_h0075.py`,
`demo/teste_demo_filho_default_h0075.py`, acréscimos focais em
`tela/teste_loader.py`. Executáveis por `pytest`, sem TTY. **Toda escrita
em `tmp_path` ou cópia; nunca no fixture do repositório.** Itens 37–46
cabem nesses arquivos já autorizados; o caso negativo sintético (item 43)
constrói o cenário em memória, sem fixture versionada nova.

1. Aplicar inativo sem divergência.
2. Aplicar ativo com um pai divergente.
3. Aplicar ativo com vários pais divergentes no mesmo snapshot.
4. Cursor (e, em H-0072, foco de console) sem impacto em `aplicar_disponivel`.
5. Enter ativo cria `SolicitacaoAplicacaoFilhoDefault` com baseline/candidato
   do instante; mutar `selecoes` depois não altera a instância.
6. Pop-up genérico abre somente com Aplicar válido; inativo ⇒ nenhum pop-up.
7. Modalidade: setas/Espaço com pop-up aberto não mutam `selecoes`/cursores.
8. ABORTADO preserva candidato.
9. ABORTADO não escreve (hash/conteúdo da cópia inalterado).
10. ABORTADO mantém Aplicar ativo.
11. CONFIRMADO persiste o snapshot da solicitação, não o candidato posterior.
12. Somente `filho_default` esperado muda no JSON da cópia.
13. Campos não relacionados preservados (`id`, `titulo`, `filhos`, tabelas,
    amostras, demais chaves de `_raw`).
14. Vários pais persistidos em conjunto coerente (um `os.replace`; dois pais
    divergentes no mesmo CONFIRMADO).
15. Sucesso promove nova baseline in-memory (`campos["filho_default"]`).
16. Sucesso sincroniza candidato (`selecoes` equalizadas, inclusive os três
    consoles H-0072).
17. Sucesso torna Aplicar inativo.
18. Nova carga da cópia (`carregar_conteudo_externo` + `construir_modelo` +
    `inicializar_escolhas_dois_niveis`) restaura os novos defaults.
19. Falha injetada: arquivo anterior preservado.
20. Falha: baseline anterior preservada.
21. Falha: candidato divergente preservado.
22. Falha: Aplicar permanece ativo.
23. Nenhuma publicação de estilo: `config/estilo.json` do repositório
    intocado; `estado["estilo"]` inalterado quando presente.
24. Cobertura H-0055 (cópia do conteúdo).
25. Cobertura H-0072 (cópia do conteúdo; dois pais; três consoles).
26. H-0072: o mesmo pai visível em dois consoles inicia com a mesma
    baseline (`mapa_baseline_filho_default` e a escolha reconciliada de
    cada console aplicável coincidem, ambas derivadas de
    `pai.campos["filho_default"]`).
27. H-0072: alterar a escolha de um pai no console A (via `alternar` com
    `modelo`) sincroniza somente essa escolha no console B —
    `estado["selecoes"][B.id]` reflete o novo filho daquele pai no mesmo
    evento, sem Aplicar/CONFIRMADO; as escolhas dos demais pais de B
    permanecem.
28. H-0072: alterar a escolha do mesmo pai a partir do console B propaga
    de volta ao candidato já compartilhado (mesmo valor final,
    independentemente de qual console iniciou a mudança) — nenhum
    candidato concorrente é criado para o pai.
29. H-0072: mudar o console focado (ou mover o cursor) não altera o
    candidato de nenhum pai — `mapa_candidato_filho_default` antes e depois
    da troca de foco é idêntico.
30. H-0072: `aplicar_disponivel_filho_default` detecta uma única
    divergência por pai; construir `lista_foco` em ordem invertida não
    muda o resultado.
31. H-0072: `mapa_candidato_filho_default` contém um único valor por
    `pai.id`, nunca um valor por par console-pai.
32. H-0072: `CONFIRMADO` persiste esse valor único no `filho_default` do
    pai correspondente no documento.
33. H-0072: reabrir/recarregar qualquer um dos três consoles após
    `CONFIRMADO` restaura o mesmo `filho_default` persistido.
34. H-0072: inverter a ordem de `lista_foco(modelo)` (helper de teste que
    monta a lista de consoles em ordem distinta) não altera o valor lido
    por `mapa_candidato_filho_default` nem o valor persistido.
35. H-0072: inspeção do controlador (`tela/selecao.py`) e da orquestração
    de Aplicar (`tela/selecao.py`, funções da §5) não contém lógica que
    eleja um valor entre representações distintas do mesmo pai; Espaço
    sincroniza só o pai transferido (§4.8); divergência residual entre
    representações é rejeitada por §4.8.1.
36. Regressão H-0074: `tela/teste_navegacao.py` e testes H-0074 em
    `tela/teste_loader.py` continuam verdes (validação, ausência de fallback
    posicional, fixtures reconciliadas) — inclusive as chamadas existentes
    a `alternar`/`_transferir_escolha_dois_niveis` sem `modelo`.
37. Dois consoles aplicáveis, mesmo documento + pai, mesmo candidato:
    `mapa_candidato_filho_default` contém uma entrada para esse `pai.id`.
38. Dois consoles aplicáveis, mesmo documento + pai, candidatos
    divergentes: `mapa_candidato_filho_default` falha fechado
    (`TelaEstruturaInvalida`); não devolve um dos valores.
39. A divergência interna do item 38 não depende da ordem de `lista_foco`
    (inverter a enumeração produz a mesma rejeição, nunca um vencedor).
40. Divergência interna não cria `SolicitacaoAplicacaoFilhoDefault`
    (`solicitar_aplicacao_filho_default` devolve `None`).
41. Divergência interna não abre persistência válida (`aplicar_disponivel_filho_default`
    é `False`; Enter aplicável é no-op — sem pop-up).
42. Divergência interna não escreve arquivo (cópia em `tmp_path` com hash
    inalterado).
43. Caso negativo sintético em memória (sem fixture versionada nova):
    mesmo objeto `ConteudoExterno`; dois consoles no mesmo modelo; um
    `dois_niveis_por_foco`; o outro com política distinta (`selecao_multinivel`
    ou equivalente já suportado pelos helpers de `tela/teste_navegacao.py`).
    Alterar o candidato no primeiro via `alternar(..., modelo=modelo)`
    **não** modifica `estado["selecoes"]` do segundo.
44. Console que não apresenta o pai (mesmo modelo; `pai.id` ausente em
    `conteudo_externo.nos` daquele console) não recebe alteração relativa
    àquele pai — a lista de IDs dele não ganha o filho transferido.
45. Sincronização de um pai preserva escolhas de outros pais: com dois
    pais no documento compartilhado, transferir só `P1` no console A
    atualiza `P1` no destino elegível e deixa `P2` do destino intacto
    (inclusive se `P2` já divergia — essa divergência residual é então
    matéria de §4.8.1 no Aplicar, não de eleição silenciosa).
46. H-0072 continua compartilhando corretamente entre seus três consoles
    aplicáveis (regressão positiva dos itens 26–34 após o predicado
    fechado e a sincronização por pai).

Comandos:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest \
  tela/teste_filho_default_h0075.py \
  demo/teste_demo_filho_default_h0075.py \
  tela/teste_loader.py \
  tela/teste_navegacao.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

---

## 13. Demonstração reproduzível

Persistência e JSON: cobertos automaticamente pelo item 24 da §12 (cópia
H-0055 em `tmp_path`). **Não** confirmar Aplicar na demo TTY contra o
fixture `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`.

Procedimento TTY (opcional, critérios para o usuário), sempre sobre cópia:

0. Copiar o conteúdo H-0055 para arquivo temporário; anotar `HASH_ANTES`
   (`sha256sum` da cópia). Abrir a tela fazendo
   `estado["caminhos_conteudo_externo"]["h0055_dois_niveis_por_foco"]`
   apontar para a cópia (o ponto de entrada deve honrar esse slot — §10.1).
1. Registrar o conteúdo/`filho_default` inicial da cópia (tabela H-0074 §8.1).
2. Abrir `h0055_dois_niveis_por_foco`.
3. Transferir a escolha de pelo menos um pai (Espaço no nível filhos).
4. Confirmar chip `Aplicar` ativo (`candidato_divergente`).
5. Enter/Aplicar → pop-up genérico sobre a mesma tela.
6. Esc/Voltar (`ABORTADO`): cópia com `HASH` inalterado; candidato na tela
   preservado; Aplicar ainda ativo.
7. Nova tentativa Enter/Aplicar.
8. Enter/Confirmar (`CONFIRMADO`).
9. `filho_default` do(s) pai(s) alterado(s) na cópia; `HASH` distinto.
10. Demais campos do JSON da cópia preservados.
11. Aplicar inativo.
12. Reabrir/recarregar a mesma cópia: novos defaults restaurados; cursor
    não “promovido” arbitrariamente.

Se o visual exigir TTY real, o usuário confirma: pop-up centralizado,
chips Voltar/Confirmar, tela subjacente visível e suspensa. A prova de
arquivo não depende de TTY.

---

## 14. Relatório da futura implementação

Arquivo: `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0075.md`

Máximo normal: 900 palavras. Registrar: arquivos alterados; Aplicar;
snapshot; popup; ABORTADO; CONFIRMADO; persistência; caminho de destino;
fail-closed; baseline/candidato; testes; demonstração; bloqueios.

---

## 15. Exceção operacional futura

Se for necessário alterar arquivo fora de §10.1: parar antes e informar
caminho, necessidade, delta, impacto sem autorização.

---

## 16. Critérios de aceite do handoff

A implementação futura executa sem decidir: como localizar o documento
(§4.6); quem persiste (§8.1); como Aplicar é habilitado e como
inconsistência interna é recusada (§4.8.1, §5); como a solicitação é
congelada (§6); o predicado de destino e a sincronização por pai (§4.8);
como o pop-up é integrado (§7); o que ABORTADO e CONFIRMADO fazem
(§7.2–§7.3); quando a baseline muda (§8.3); como falha preserva estado
(§8.2); quais arquivos alterar (§10); quais testes (§12).

---

## 17. Fora de escopo

- Reabertura de H-0074 (validação de carga, fallback posicional, fixtures
  de `filho_default`).
- ITEM-0023, ITEM-0024.
- Novo tipo de pop-up; schema público de caminho de arquivo.
- Publicação global de Estilo; `config/estilo.json`.
- Dispatcher genérico do ITEM-0004.
- Correção geral de resíduos EOF/whitespace.

---

## 18. Bloqueios

nenhum — o caminho é recuperável pela composição já usada na carga mais
o campo runtime `caminho_origem` / override de sessão; o pop-up genérico
já confirma `tipo: texto`; a técnica atômica de escrita já existe como
precedente; H-0055 e H-0072 são fixtures, não destinos únicos hardcoded
da capacidade.
