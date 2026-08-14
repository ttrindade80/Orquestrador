# H-0068 — Persistência e publicação do estilo confirmado

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0068
data_criacao: 2026-08-12
status: READY_FOR_IMPLEMENTATION
predecessor: H-0067
relacao: continuacao_funcional
historico:
  H-0061:
    estado: aprovado
    capacidade:
      - baseline_persistida
      - candidato_runtime
      - materializacao_global
      - primitivas_de_persistencia
      - primitivas_de_publicacao
      - fail_closed
  H-0065:
    estado: aprovado
    capacidade:
      - candidato_fonte_semantica
      - selecoes_projeta_candidato
      - descarte_da_visita
  H-0066:
    estado: I1_IMPLEMENTATION_APPROVED
    capacidade:
      - SolicitacaoAplicacaoEstilo_imutavel
      - snapshot_baseline_candidato
  H-0067:
    estado: I1_IMPLEMENTATION_APPROVED
    capacidade:
      - popup_confirmacao
      - CONFIRMADO
      - ABORTADO
      - retencao_da_solicitacao_apos_CONFIRMADO
      - descarte_da_solicitacao_apos_ABORTADO
dependencias:
  - H-0061
  - H-0065
  - H-0066
  - H-0067
item_0010:
  estado: em_andamento
fronteira_posterior:
  - demonstracao_integrada_com_override_local
```

H-0068 é continuação funcional de H-0067, não substituição. `SolicitacaoAplicacaoEstilo`,
o popup genérico de confirmação, `CONFIRMADO`/`ABORTADO`, a tela normal de Estilo,
a navegação `dois_niveis_por_foco` e a fonte semântica candidato permanecem
integralmente vigentes. H-0062 permanece histórico/substituído e não é reaberto.

## 2. Objetivo exclusivo

Especificar e autorizar a fatia:

```text
APLICAÇÃO DEFINITIVA DO ESTILO CONFIRMADO
```

Entrada obrigatória, exclusiva:

```text
resultado == CONFIRMADO (H-0067)
+
SolicitacaoAplicacaoEstilo retida em estado["solicitacao_aplicacao_estilo"]
→ validação do snapshot
→ persistência
→ publicação
→ atualização da baseline
→ reconciliação de candidato/seleções
→ limpeza da solicitação
→ estado final da tela
```

A aplicação usa exclusivamente o snapshot confirmado (`solicitacao.candidato`).
Nunca reconstrói a operação a partir do candidato mutável do runtime — mesmo
que, na prática, os dois ainda coincidam no instante da consumação (§7).

H-0068 **não**:

- cria a demonstração integrada (Cabeçalho + Console + Dashboard + Barra sob
  override local) exigida pela ADR-0046 §5 — permanece capacidade não
  numerada, deliberadamente adiada desde H-0066 §15/H-0067 §13 (ver §17
  abaixo);
- cria segundo mecanismo de persistência ou publicação;
- inventa literais de resultado além dos já existentes (`EstiloErro`,
  `CONFIRMADO`/`ABORTADO`);
- reabre navegação, amostras, popup ou confirmação — todos permanecem
  exatamente como entregues por H-0063/H-0064/H-0065/H-0066/H-0067.

## 3. Compatibilidade com ADR-0046

A ADR-0046 §7 (tabela de transições) e §8 descrevem a aplicação confirmada
como parte da MESMA transição `CONFIRMADO`, não como um evento posterior
distinto disparado por uma segunda ação do usuário:

> "Demonstração + confirmação | `CONFIRMADO` e persistência bem-sucedida |
> Seleção/edição | Publica a nova materialização, retorna à seleção e
> equaliza candidato e baseline persistida"

E ADR-0046 §8, abertura: "No caminho `CONFIRMADO`, o chamador deve: 1.
persistir... 3. somente após esse sucesso substituir... 5. retornar à tela
de seleção; 6. tornar a configuração recém-aplicada a nova baseline...". Os
sete passos são descritos como consequência direta e no mesmo caminho do
evento `CONFIRMADO`, não como uma segunda transição posterior disparada por
outra tecla ou chip.

H-0067 já abre e fecha o popup dentro do mesmo evento de tecla que produz
`CONFIRMADO` (`demo/demo.py` ~868-882) e, deliberadamente, apenas retém a
`SolicitacaoAplicacaoEstilo` sem persistir — isso é `fronteira_posterior`
explícita de H-0067 (`persistencia`, `publicacao`,
`atualizacao_da_baseline_confirmada`), não uma decisão de que a aplicação
deva ocorrer em um evento humano separado. H-0067 §8 registra a
possibilidade teórica de edição intermediária ("se isso ocorrer antes de
uma etapa posterior consumir a solicitação retida...") como salvaguarda de
imutabilidade do snapshot, não como desenho pretendido do fluxo — não há
autoridade que declare, nem chip/lançador dedicado (H-0067 §7.4: "não há
caminho declarativo para abrir o popup de confirmação de estilo de outra
forma"), um segundo acionamento humano para "aplicar de fato" depois de
`CONFIRMADO`.

**Decisão desta etapa (não é conflito material, não exige
`BLOCKED_DOCUMENTATION`):** H-0068 estende exatamente o mesmo ramo de
`demo/demo.py` que hoje trata `CONFIRMADO`/`ABORTADO` para o popup
`ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO` (linhas ~868-882), de modo que a
aplicação definitiva ocorra no mesmo evento de tecla que fecha o popup com
`CONFIRMADO`. Isso é a leitura mais direta de ADR-0046 §7/§8 (uma única
transição combinada) e elimina por construção qualquer janela em que o
candidato mutável pudesse divergir do snapshot antes da consumação.

Diferença documental obrigatória:

| Capacidade | Papel |
|---|---|
| CONFIRMAÇÃO (H-0067) | Obter `CONFIRMADO`/`ABORTADO`; reter ou descartar a `SolicitacaoAplicacaoEstilo` |
| APLICAÇÃO DEFINITIVA (H-0068) | Consumir a solicitação retida por `CONFIRMADO`; validar, persistir, publicar, promover baseline, reconciliar candidato/seleções, limpar a solicitação |
| Demonstração integrada (posterior, não numerada) | Cabeçalho + Console + Dashboard + Barra sob override local, ainda não implementada por nenhum handoff |

## 4. Autoridade

Lidas integralmente:

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`
- `docs/handoff/H-0061-infraestrutura-estilo-runtime.md`
- `docs/handoff/H-0066-acao-aplicar-candidato-estilo.md`
- `docs/handoff/H-0067-confirmacao-aplicacao-estilo.md`
- `docs/contratos/contrato_estilo.md` (integral; especialmente §3.8, R-1,
  R-4, R-9 a R-13)

Lidas focalmente:

- `docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md`
- `docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md`

Código inspecionado para determinar as primitivas reais existentes (sem
alteração nesta etapa documental):

- `tela/carregamento/estilo.py` — `EstadoEstiloRuntime` (`RuntimeEstilo`):
  `criar_candidato`, `materializar_local`, `comparar_candidato_baseline`,
  `persistir_candidato`, **`aplicar_candidato`** (linhas 362-380);
  `persistir_configuracao_estilo` (escrita atômica via `tempfile` +
  `os.replace`, linhas 257-297); `materializar_estilo_local`;
  `comparar_configuracoes_estilo`; `_para_base`/`_caminho_padrao_base`
  (`tela/carregamento/caminho_base.py`).
- `tela/estilo.py` — `ControladorTelaEstilo`, `SolicitacaoAplicacaoEstilo`
  (dataclass `frozen`, cópias profundas de `baseline`/`candidato` no
  `__post_init__`), `solicitar_aplicacao`, `aplicar_disponivel`,
  `reconciliar_selecoes_com_candidato`, `descartar_visita`.
- `demo/demo.py` — instanciação de `RuntimeEstilo()` sem `caminho_base`
  explícito (linha 2442, portanto raiz real do repositório); preservação de
  `estado["estilo_runtime"]`/`estado["tela_estilo"]`/
  `estado["solicitacao_aplicacao_estilo"]` entre comandos (linhas 799-806);
  ramificação modal de consumo de popup e tratamento de
  `CONFIRMADO`/`ABORTADO` (linhas 862-882); produção da solicitação e
  abertura do popup em `Enter/Aplicar` (linhas 1190-1211); **uso separado e
  não sincronizado de `estado["estilo"]`** pelos renderers (linhas 1359,
  1662, 1737, 1862, 1904) — ver achado crítico em §7.4.
- `tela/teste_loader.py` — `test_h0061_demonstracao_sucesso_persistencia_antes_publicacao`
  e `test_h0061_falha_persistencia_preserva_global_baseline_e_candidato`
  (linhas ~4643-4707): prova viva do comportamento exato de
  `aplicar_candidato` em sucesso e em falha.
- `demo/teste_demo_estilo_h0067.py` — testes que hoje afirmam ausência de
  persistência/publicação especificamente após `CONFIRMADO` (ver §16).

Não usar H-0062 como autoridade (histórico/substituído).

## 5. Achado central — a primitiva de aplicação já existe

`tela/carregamento/estilo.py:362-380` já contém
`EstadoEstiloRuntime.aplicar_candidato(candidato, caminho_destino)`:

```text
documento := candidato validado/copiado (EstiloErro se estrutura invalida)
materializacao := materializar_estilo_local(documento)      # validar
self._estado.candidato := documento                          # bookkeeping interno
persistir_configuracao_estilo(documento, caminho_destino)     # persistir (atomico)
# --- só chega aqui se persistir_configuracao_estilo NAO levantou ---
self._estado := (baseline=documento, candidato=documento, global_vigente=materializacao)
# uma unica troca de objeto Python: publicar + promover baseline +
# sincronizar candidato, simultaneamente
return materializacao
```

Isso **já** implementa integralmente, testado e fail-closed
(`tela/teste_loader.py:4643-4707`):

1. validação do snapshot completo (`materializar_estilo_local`);
2. persistência atômica (`persistir_configuracao_estilo`: escreve em
   temporário no mesmo diretório, `fsync`, `os.replace` — o destino só é
   substituído após escrita completa sem erro; arquivo anterior intocado em
   falha);
3. publicação (troca do único objeto `global_vigente`);
4. promoção da baseline (`baseline := documento`, somente após sucesso);
5. reconciliação do candidato do runtime (`candidato := documento`, igual à
   nova baseline);
6. fail-closed comprovado: se `persistir_configuracao_estilo` levanta,
   `EstiloErro` propaga de `aplicar_candidato`, `baseline`/`global_vigente`
   permanecem exatamente os anteriores, `candidato` permanece disponível
   (igual ao documento tentado — o mesmo valor da solicitação, portanto não
   perdido) e o arquivo de destino permanece com o conteúdo anterior
   (`tela/teste_loader.py:4679-4707`).

**Conclusão normativa:** H-0068 não cria um segundo mecanismo de
persistência/publicação. A única responsabilidade nova e legítima de
H-0068 é a **orquestração**: extrair `solicitacao.candidato` do slot
retido por H-0067, chamar `aplicar_candidato` com o destino real, tratar o
resultado (sucesso ou `EstiloErro`), sincronizar o slot separado
`estado["estilo"]` (§7.4), reconciliar `selecoes` e limpar a solicitação.
Nenhum novo algoritmo de escrita, de troca atômica ou de rollback é
autorizado ou necessário.

## 6. Snapshot confirmado é a autoridade

A implementação deve consumir exatamente:

```text
estado["solicitacao_aplicacao_estilo"].candidato
```

Esse é o slot canônico já deixado por H-0067 (`demo/demo.py:1257-1260`,
preservado entre comandos em `demo/demo.py:799-806`).
`SolicitacaoAplicacaoEstilo` é `frozen` e já copia profundamente
`baseline`/`candidato` no `__post_init__` (`tela/estilo.py:96-110`) — o
snapshot é imutável por construção desde H-0066.

A aplicação **não pode**:

- reler `runtime.candidato` como fonte da operação (mesmo que, por
  construção desta etapa — §3 — os dois ainda coincidam no instante exato
  da consumação, pois nenhuma tecla intermediária é possível entre
  `CONFIRMADO` e a aplicação no mesmo evento);
- reconstruir novo candidato;
- aplicar uma escolha feita depois da confirmação;
- misturar snapshot confirmado com estado mutável posterior.

`solicitacao.baseline` não é usada operacionalmente por H-0068 (a baseline
real de comparação é sempre `runtime.baseline`, gerida por
`EstadoEstiloRuntime`); ela existe na solicitação apenas como parte do
snapshot imutável de H-0066 e não precisa ser lida por esta fatia.

## 7. Matriz documental obrigatória

### 7.1 Pré-condições

| Pré-condição | Classificação | Determinação |
|---|---|---|
| `resultado == CONFIRMADO` | DETERMINADO_PELA_AUTORIDADE | Garantido estruturalmente: o ramo de aplicação só é alcançado dentro do `if popup_id == ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO` e `resultado_popup.get("status") == "CONFIRMADO"` já existentes (`demo/demo.py:878-881`). |
| Solicitação existente | DETERMINADO_PELA_AUTORIDADE | `"solicitacao_aplicacao_estilo" in novo`. Ausência (não deveria ocorrer neste ramo, pois só é setada junto com a abertura do popup) é tratada como no-op — nenhuma aplicação, nenhum erro novo inventado (H-0067 §7.4: não há caminho para popup sem solicitação). |
| Solicitação estruturalmente válida | DETERMINADO_PELA_AUTORIDADE | Garantida por construção desde H-0066 (`SolicitacaoAplicacaoEstilo` `frozen`, cópias profundas); H-0067 §7.4 já registra que não há caminho para snapshot inválido chegar ao popup. Nenhum tratamento adicional é autorizado. |
| Catálogo/presets ainda válidos | DERIVAVEL_DA_INFRAESTRUTURA_VIGENTE | Coberto por `materializar_estilo_local` dentro de `aplicar_candidato` (validação fechada completa antes de persistir). Falha aqui é tratada como falha de validação/persistência (§7.3), não como pré-condição verificada separadamente por H-0068. |
| Candidato confirmado materializável | DERIVAVEL_DA_INFRAESTRUTURA_VIGENTE | Idem — `materializar_estilo_local` já é a primeira etapa interna de `aplicar_candidato`; nenhuma segunda validação duplicada é autorizada. |

Se qualquer pré-condição estrutural falhar (solicitação ausente ou não é
instância de `SolicitacaoAplicacaoEstilo`), a operação é no-op: não
persistir, não publicar, não atualizar baseline — comportamento idêntico a
"nenhuma solicitação", sem literal de erro novo.

### 7.2 Persistência e publicação

Já cobertas integralmente por `aplicar_candidato` (§5). H-0068 apenas
fornece o destino real. **Achado de implementação (não normativo, apontado
para a etapa futura):** `EstadoEstiloRuntime` guarda a raiz resolvida em
`self._caminho_base` (atributo privado, `tela/carregamento/estilo.py:304`)
mas não expõe publicamente o caminho de destino de
`config/estilo.json`. Não existe hoje, em nenhum módulo, uma segunda
computação pública desse caminho fora do interior de
`_ler_configuracao_estilo` (`tela/carregamento/estilo.py:93-96`). Sem essa
exposição, o chamador (`tela/estilo.py`/`demo/demo.py`) não tem como obter
o destino real sem duplicar a lógica de resolução de `caminho_base` — o
que seria um segundo mecanismo, proibido pela ADR e pelos handoffs
anteriores.

Isso não é um bloqueio documental: é uma extensão mínima e pontual
autorizada em `tela/carregamento/estilo.py` (§9) — expor um acessor público
somente-leitura (propriedade ou método) em `EstadoEstiloRuntime` que
devolva `self._caminho_base / "config" / "estilo.json"`. Não é criação de
segunda persistência: é publicar o caminho que a primitiva já usa
internamente, para que o único chamador de `aplicar_candidato` (H-0068) não
precise recalculá-lo.

### 7.3 Ordem operacional

Extraída literalmente de ADR-0046 §7/§8 e já implementada por
`aplicar_candidato` (§5):

```text
validar (materializar_estilo_local)
→ persistir (persistir_configuracao_estilo, atômico)
→ [publicar + atualizar baseline + reconciliar candidato do runtime]
  como uma única troca de estado interna, indivisível do ponto de vista
  de qualquer consumidor externo
```

Não há mais de uma ordem materialmente plausível: a ADR fixa "persistência
→ troca do estilo global" como obrigatória (§8, parágrafo final) e proíbe
"estilo parcialmente persistido ou materialização parcialmente resolvida
como sucesso". `aplicar_candidato` já respeita essa ordem literalmente e é
a única primitiva de aplicação vigente (H-0061 §7: "Publicar nunca pode
preceder a persistência"). Não é `BLOCKED_DOCUMENTATION`.

Camada de orquestração de H-0068, em torno dessa chamada única, na mesma
sequência:

```text
1. extrair candidato do snapshot confirmado (§6)
2. chamar aplicar_candidato(candidato, destino)   # valida+persiste+publica+baseline+candidato
3a. sucesso:
    sincronizar estado["estilo"] com a materializacao retornada (§7.4)
    reconciliar estado["selecoes"] a partir do novo candidato (== nova baseline)
    remover estado["solicitacao_aplicacao_estilo"]
3b. falha (EstiloErro):
    nao propagar excecao para fora do loop de eventos
    remover estado["solicitacao_aplicacao_estilo"] (tentativa consumida)
    nao tocar estado["estilo"], baseline, global, arquivo (ja preservados por aplicar_candidato)
    tela permanece a mesma; aplicar_disponivel continua True (candidato ainda diverge)
```

### 7.4 Achado crítico — sincronização de `estado["estilo"]`

`demo/demo.py` mantém **dois** objetos de estilo distintos em runtime:

- `estado["estilo_runtime"]` (`RuntimeEstilo`/`EstadoEstiloRuntime`) —
  gerencia baseline/candidato/`global_vigente`;
- `estado["estilo"]` (`EstiloResolvido`) — objeto efetivamente lido por
  **todos** os renderers (`demo/demo.py:1359,1662,1737,1862,1904`),
  atribuído uma única vez em `main()` e apenas **copiado adiante** a cada
  comando (`demo/demo.py:833-834`: `novo["estilo"] = estado["estilo"]`).

Nenhum handoff anterior sincroniza `estado["estilo"]` a partir de
`estilo_runtime.global_vigente` após uma troca — porque nenhum handoff
anterior publicou de fato (H-0065/H-0066/H-0067 são todos anteriores a
qualquer persistência real). Se H-0068 chamar `aplicar_candidato` e não
atualizar também `estado["estilo"]`, o requisito contratual "os
consumidores passam a usar imediatamente a nova materialização, sem exigir
reconstrução integral da tela" (contrato_estilo.md R-4; ADR-0046 §8.4) **não
se cumpre de fato** — os renderers continuariam desenhando com o objeto
antigo, apesar de `config/estilo.json` e `estilo_runtime.global_vigente` já
estarem corretos.

Portanto: **é acréscimo obrigatório de H-0068**, no mesmo evento de sucesso,
atribuir `novo["estilo"] = materializacao` (o `EstiloResolvido` retornado
por `aplicar_candidato`), antes de retornar o estado do comando. Isso não é
segunda fonte global — é o único slot que os renderers de fato consomem,
mantido sincronizado com a única materialização publicada por
`estilo_runtime`.

## 8. Fail closed

Cenários, todos já cobertos pela combinação de `aplicar_candidato` (runtime)
mais a orquestração fina de H-0068 (estado de sessão):

### Falha antes da persistência (validação do candidato)

`materializar_estilo_local`, primeira chamada interna de
`aplicar_candidato`, levanta `EstiloErro` antes de qualquer escrita e antes
de qualquer troca de `self._estado`. Nada muda: baseline, `global_vigente`,
candidato do runtime e arquivo permanecem exatamente como estavam.

### Falha durante a persistência

`persistir_configuracao_estilo` levanta `EstiloErro` (arquivo temporário é
removido em `finally`, `os.replace` nunca ocorre —
`tela/carregamento/estilo.py:266-296`). O arquivo de destino permanece
com o conteúdo anterior válido; `self._estado.global_vigente` e
`self._estado.baseline` **ainda são os do `estado_anterior`** (a troca só
ocorre depois da chamada de persistência, que já lançou); o candidato do
runtime fica igual ao documento tentado (mesmo valor de
`solicitacao.candidato`) — disponível, não destruído, não parcial.

### Persistência bem-sucedida + falha posterior

Não existe janela observável nesta arquitetura: a troca de `self._estado`
que publica global + promove baseline + sincroniza candidato é uma única
atribuição de objeto Python imediatamente após `persistir_configuracao_estilo`
retornar sem erro, dentro da mesma chamada de `aplicar_candidato` — não há
E/S nem chamada externa entre a persistência bem-sucedida e essa troca. A
única extensão que H-0068 acrescenta depois do retorno de
`aplicar_candidato` (sincronizar `estado["estilo"]`, reconciliar
`selecoes`, limpar a solicitação) é aritmética pura em memória, no mesmo
evento síncrono, sem I/O — não introduz janela de estado partido. Não é
aceito, e a arquitetura vigente não permite, `arquivo novo + global antigo
+ baseline antiga` nem qualquer combinação incoerente.

## 9. Rollback/compensação

H-0061 já resolve atomicidade da forma suficiente para um runtime de
processo único: escrita atômica de arquivo (`tempfile` + `os.replace`) e
troca atômica em memória (uma única substituição de `_EstadoEstiloRuntime`,
`dataclass(frozen=True)`, portanto o objeto anterior nunca é mutado
parcialmente). Não há necessidade de commit em duas fases entre arquivo e
memória porque a publicação em memória só ocorre **depois** que a escrita
do arquivo já terminou com sucesso — não existe intervalo em que ambos
precisem ser revertidos juntos. H-0068 não inventa mecanismo alternativo:
reutiliza integralmente essa garantia via `aplicar_candidato`.

Não há lacuna técnica a registrar aqui: a única lacuna real (exposição
pública do caminho de destino, §7.2) é de acesso/orquestração, não de
atomicidade.

## 10. Baseline

```text
baseline_nova := candidato_confirmado (solicitacao.candidato)
```

Só ocorre dentro de `aplicar_candidato`, **após** persistência bem-sucedida
e como parte da mesma troca atômica que publica o global (§5, §9). Nunca
antecipada. Após sucesso, `comparar_candidato_baseline()` retorna `True`
(candidato do runtime foi sincronizado ao mesmo documento na mesma troca).

## 11. Candidato e seleções após sucesso

Confirmado documentalmente (ADR-0046 §8.6-8.7; contrato_estilo.md §3.8,
último parágrafo; R-13):

```text
baseline = estilo confirmado
candidato = estilo confirmado          (sincronizado por aplicar_candidato)
selecoes = projeção desse estilo       (reconciliar_selecoes_com_candidato)
Aplicar = inativo                      (aplicar_disponivel deriva de
                                         comparar_candidato_baseline(), que
                                         agora é True — sem flag residual,
                                         mesma ponte literal de H-0066 §5.C)
```

`reconciliar_selecoes_com_candidato` (já existente, `tela/estilo.py:346-358`)
deve ser chamada explicitamente após o sucesso, com o `modelo` da tela de
Estilo ainda ativa, para que `estado["selecoes"]` não retenha a projeção da
visita anterior à confirmação (mesma obrigação já fixada por H-0065 §9.3
para os demais pontos de reconciliação).

## 12. Estado após falha

Determinado pela combinação de ADR-0046 §7 ("Seleção/edição não
confirmada... conserva-o [candidato] disponível para nova tentativa ou
edição") e da ausência de qualquer autoridade para popup de erro novo
(H-0067 §7.4; prompt operacional desta etapa, §24):

- candidato continua disponível (igual ao valor tentado — `runtime.candidato`
  não é destruído nem revertido para um terceiro valor);
- a solicitação daquela tentativa **não** permanece para retry automático —
  é descartada (mesmo padrão já usado por `ABORTADO`, `demo/demo.py:879-880`)
  porque não há autoridade para uma segunda aplicação da mesma
  `SolicitacaoAplicacaoEstilo` sem passar de novo por `Enter/Aplicar` →
  popup → `Confirmar` (H-0067 §7.4: não há caminho declarativo alternativo);
- o popup já está fechado (fechado no mesmo evento que produziu
  `CONFIRMADO`, antes mesmo de a aplicação ser tentada);
- `Aplicar` continua ativo, porque `comparar_candidato_baseline()` continua
  `False` (baseline não mudou; candidato do runtime permanece divergente
  dela);
- não há resultado/erro visível novo (nenhum popup de erro é criado nesta
  fatia — margem documental explícita, não lacuna a bloquear);
- o usuário pode tentar aplicar novamente: um novo `Enter/Aplicar` produz
  nova `SolicitacaoAplicacaoEstilo` e reabre o popup normalmente, pois
  `aplicar_disponivel` continua `True`.

Nenhuma política de retry automático é inventada.

## 13. Resultado da aplicação

Nenhum literal novo é autorizado (`APPLIED`, `STYLE_SAVED`, `PERSIST_FAILED`
etc. — proibidos explicitamente por esta etapa). A infraestrutura já
existente é suficiente e deve ser reutilizada tal como está:

- sucesso: retorno normal de `aplicar_candidato` (objeto `EstiloResolvido`)
  + estado observável coerente (`baseline == candidato`, `estado["estilo"]`
  atualizado, `aplicar_disponivel is False`, arquivo persistido, solicitação
  ausente);
- falha: exceção `EstiloErro` (já o mecanismo estrutural de erro de todo o
  módulo `tela/carregamento/estilo.py`), capturada pela camada de
  orquestração de H-0068 no ponto de dispatch, nunca propagada até o loop
  principal da demo. O "resultado" observável de falha é estrutural: ausência
  de mudança em arquivo/baseline/global, candidato disponível, `Aplicar`
  ativo, solicitação removida — não um campo/literal dedicado novo.

## 14. `config/estilo.json` após sucesso

Já garantido, byte a byte quanto à estrutura semântica, por
`persistir_configuracao_estilo`/`aplicar_candidato`
(`tela/teste_loader.py:4643-4677`): o documento persistido é exatamente o
candidato confirmado completo, preservando todos os campos fora dos quatro
`preset_default` editáveis (`_meta`, catálogos completos, `cor_inativo`,
`cor_alerta`, `indicadores.concluido`, `indicadores.selecionado.off`).
Categorias continuam exclusivamente as quatro do ITEM-0010:

```text
borda
chip
indicadores.selecionado
indicadores.incluido
```

Teste de H-0068 verifica o **caminho E2E completo** a partir do evento
`CONFIRMADO` (não apenas a primitiva isolada, já coberta por H-0061): abrir
tela, escolher preset, `Enter/Aplicar`, `Enter/Confirmar`, ler
`config/estilo.json` do destino de teste e comparar semanticamente com
`solicitacao.candidato`.

## 15. Publicação global após sucesso

Teste semanticamente, na representação de cada camada:

```text
arquivo persistido == estilo_runtime.baseline == estilo_runtime.global_vigente
  == estilo_runtime.candidato == estado["estilo"] (materializado)
  == solicitacao.candidato (materializado)
```

A igualdade de `estado["estilo"]` com a nova materialização é o teste novo
introduzido por H-0068 (§7.4) — nenhum handoff anterior verificava esse
slot porque nenhum publicava de fato.

## 16. Testes predecessores superados

Inspecionados nominalmente em `demo/teste_demo_estilo_h0067.py`. H-0068
supera **apenas** as asserções que afirmam literalmente ausência de
persistência/publicação especificamente no cenário pós-`CONFIRMADO`
(cenário que deixa de existir sem aplicação, pois passa a existir com
aplicação real). Nenhuma outra garantia é enfraquecida.

- `test_enter_popup_produz_confirmado_retendo_solicitacao` (linhas
  126-156): as asserções `runtime.baseline == baseline_antes`,
  `runtime.global_vigente == global_antes` e
  `destino.read_text(...) == original` (linhas 151-154), tomadas
  **imediatamente após o `Enter/Confirmar`**, tornam-se falsas por
  construção quando H-0068 aplica no mesmo evento. Reestruturar para
  refletir a fronteira real de H-0068: após `CONFIRMADO`,
  `destino.read_text(...)` deve conter o candidato persistido,
  `runtime.baseline`/`runtime.global_vigente` devem refletir a nova
  configuração, e `estado["tela_estilo"].aplicar_disponivel` deve ser
  `False` (não mais `True`, linha 156). As demais asserções (ausência de
  `"valor"` no `popup_resultado`, `popup is None`, `tela_atual` inalterado)
  permanecem válidas sem modificação.
- `test_fronteiras_apos_confirmado_e_abortado` (linhas 282-306): a
  sub-sequência específica **após `CONFIRMADO`** (linhas 292-296:
  `runtime.baseline == baseline_antes`, `runtime.global_vigente ==
  global_antes`, `destino.read_text(...) == original`) é superada pela
  mesma razão. A sub-sequência **após `ABORTADO`** (linhas 298-306) **não**
  é tocada — `ABORTADO` continua sem qualquer efeito de
  persistência/publicação, exatamente como hoje.
- `test_demonstracao_non_tty_ciclo_confirmacao` (linhas 312-378): a seção
  final "Sem persistencia/publicacao" (linhas 373-378), que roda depois de
  um segundo `Enter/Confirmar` bem-sucedido (`solicitacao_2`, linhas
  364-370), é superada. A primeira metade do teste — a tentativa abortada
  com `Esc` (linhas 356-362) — permanece intocada: candidato preservado,
  `aplicar_disponivel` continua `True`, nenhuma persistência.

Não ampliar outros arquivos "por garantia". Nenhuma outra suíte
predecessora assume ausência de persistência especificamente no cenário
`CONFIRMADO` (as demais tratam `ABORTADO`, modalidade, resize ou snapshot,
que continuam corretas sem modificação).

Não autorizar alteração de `tela/teste_estilo_h0063.py`,
`tela/teste_estilo_h0065.py`, `tela/teste_estilo_h0066.py`,
`demo/teste_demo_estilo_h0063.py`, `demo/teste_demo_estilo_h0064.py`,
`demo/teste_demo_estilo_h0065.py`, `demo/teste_demo_estilo_h0066.py`, ADR,
contratos, nomenclatura ou backlog nesta implementação futura.

## 17. Encerramento da cadeia do ITEM-0010

```yaml
H-0068: AINDA_REQUER_HANDOFF_POSTERIOR
capacidade_remanescente: demonstracao_integrada_com_override_local
```

A ADR-0046 §5 exige uma demonstração integrada (Cabeçalho + Console +
Dashboard + Barra de Menus, sob override local do candidato) **antes** da
confirmação, no fluxo combinado original. Todos os handoffs desde H-0065
(§22), passando por H-0066 (§15) e H-0067 (§13, "fronteira posterior"
implícita), registraram essa capacidade como explicitamente fora de
escopo e ainda não implementada por nenhum deles — o popup de confirmação
já implementado abre diretamente sobre a tela de Estilo (H-0067 §3), não
sobre uma demonstração. `docs/backlog.md` ITEM-0010 também lista
"demonstracao do candidato antes da confirmacao" como parte do escopo
completo do item.

H-0068 não implementa essa capacidade (não é seu objetivo, §2) e não a
amplia. Após H-0068, a aplicação definitiva do estilo confirmado já é
real, persistida e publicada, tornando o restante do ITEM-0010
funcionalmente utilizável mesmo sem a demonstração visual prévia — mas o
ITEM-0010, como descrito pela ADR e pelo backlog, permanece
`em_andamento` até essa capacidade ser endereçada por um handoff
posterior, cuja numeração fica a critério do gerente (não é criado aqui).

## 18. Arquivos de implementação futura autorizados

Lista nominal mínima, decorrente da arquitetura real inspecionada (§4-§7);
nenhum arquivo predecessor é autorizado sem conflito factual comprovado
(§16).

### Infraestrutura de estilo (extensão pontual mínima)

- `tela/carregamento/estilo.py` — acrescentar somente um acessor público
  somente-leitura em `EstadoEstiloRuntime` que devolva o caminho real de
  destino já usado internamente (`self._caminho_base / "config" /
  "estilo.json"`), reaproveitando exatamente a mesma composição de
  `_ler_configuracao_estilo` (linha 96). Não criar nova lógica de
  persistência, publicação, validação ou resolução de caminho — apenas
  expor o que já existe internamente. `aplicar_candidato` e as demais
  primitivas permanecem inalteradas.

### Controlador da tela de Estilo

- `tela/estilo.py` — acrescentar em `ControladorTelaEstilo` a capacidade
  mínima de orquestrar a aplicação definitiva a partir de uma
  `SolicitacaoAplicacaoEstilo` já confirmada: extrair
  `solicitacao.candidato`, chamar `self.runtime.aplicar_candidato(...)`
  com o destino real (novo acessor acima), propagar sucesso/falha ao
  chamador, e — em sucesso — reconciliar `estado["selecoes"]` via
  `reconciliar_selecoes_com_candidato` já existente. Não recriar
  `SolicitacaoAplicacaoEstilo`, não duplicar `aplicar_candidato`, não
  reler `runtime.candidato` como fonte (§6).

### Integração de dispatch

- `demo/demo.py` — estender o ramo já existente que trata
  `CONFIRMADO`/`ABORTADO` para `ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO`
  (~linhas 868-882): no mesmo evento em que `CONFIRMADO` é produzido,
  chamar a nova capacidade de `tela/estilo.py`; em sucesso, sincronizar
  `novo["estilo"]` com a materialização retornada (§7.4, acréscimo
  obrigatório) e remover `solicitacao_aplicacao_estilo`; em falha
  (`EstiloErro`), apenas remover `solicitacao_aplicacao_estilo` sem
  propagar a exceção. `ABORTADO` permanece exatamente como hoje (linhas
  879-880), sem qualquer alteração. Não duplicar a ramificação modal
  genérica (H-0059), não criar segundo ponto de dispatch para `CONFIRMADO`.

### Testes e relatório

- `tela/teste_estilo_h0068.py` — testes dedicados de orquestração no
  controlador: sucesso (persistência+publicação+baseline+reconciliação),
  falha injetada (fail-closed, solicitação descartada, candidato
  disponível), uso exclusivo do snapshot confirmado (nunca
  `runtime.candidato` mutado depois), ausência de segunda persistência.
- `demo/teste_demo_estilo_h0068.py` — testes de integração ponta a ponta a
  partir do evento real `Enter/Aplicar` → popup → `Enter/Confirmar`:
  arquivo persistido corretamente, `estado["estilo"]` sincronizado,
  `aplicar_disponivel` inativo após sucesso, solicitação consumida, falha
  de persistência/publicação injetada com fail-closed completo, ausência
  de aplicação quando `ABORTADO` ou quando não há solicitação confirmada,
  regressão dos três testes nominados em §16 (com asserções
  reestruturadas, não removidas).
- `tela/teste_loader.py` — somente se o acessor público de §18.1 for
  adicionado: um teste focal dedicado desse acessor (caminho correto para
  `caminho_base` explícito e para o default). Não duplicar
  `test_h0061_demonstracao_sucesso_persistencia_antes_publicacao` nem
  `test_h0061_falha_persistencia_preserva_global_baseline_e_candidato`,
  que já cobrem `aplicar_candidato` isoladamente e permanecem válidos sem
  modificação.
- `docs/relatorios/IMP-0068-persistencia-publicacao-estilo-confirmado.md`
  — relatório futuro da implementação.

Permanecem, como já valia em H-0063/H-0065/H-0066/H-0067, fontes/infraestrutura
canônicas a consumir sem alteração adicional além da pontual de §18.1:
`config/estilo.json` como autoridade persistida real (nunca escrita
diretamente por testes fora de raiz temporária), `tela/loader.py`,
`tela/navegacao.py`, `tela/selecao.py`, `tela/renderizacao/tela.py`,
`tela/renderizacao/console.py`, `tela/renderizacao/popup.py`,
`tela/renderizacao/contexto_execucao.py`, `tela/renderizacao/barra_menus.py`,
`tela/renderizador.py`, `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`,
e os contratos vigentes.

## 19. Testes automatizados mínimos

### Sucesso

- solicitação confirmada válida (`CONFIRMADO` real, via popup);
- `config/estilo.json` de destino de teste contém exatamente o candidato
  confirmado, preservando campos fora do escopo (§14);
- `estilo_runtime.global_vigente`, `estilo_runtime.baseline`,
  `estilo_runtime.candidato` e `estado["estilo"]` todos iguais à nova
  materialização (§15);
- `aplicar_disponivel` passa a `False`;
- `estado["selecoes"]` reconciliado com a nova baseline;
- `estado["solicitacao_aplicacao_estilo"]` ausente após a aplicação;
- tela permanece `_ID_TELA_H0063`.

### Abortado/ausente

- `ABORTADO` não persiste, não publica, não atualiza baseline (regressão
  intocada de H-0067);
- ausência de solicitação confirmada (nenhum `Enter/Aplicar` acionado, ou
  acionado com `aplicar_disponivel is False`) → nenhuma aplicação, no-op.

### Snapshot

- mutar o candidato do runtime **depois** de `CONFIRMADO` mas antes do
  processamento da aplicação não é um caminho alcançável nesta arquitetura
  (mesmo evento síncrono, §3); teste defensivo replica
  `test_snapshot_confirmado_permanece_ligado_ao_original`
  (`demo/teste_demo_estilo_h0067.py:241-259`) para comprovar que, mesmo que
  fosse possível, a aplicação usaria `solicitacao.candidato`, nunca uma
  releitura de `runtime.candidato`.

### Falha de persistência

- injetar falha controlada em `persistir_configuracao_estilo` (mesma
  técnica de `tela/teste_loader.py:4693-4702`, via monkeypatch);
- `config/estilo.json` de teste permanece com o conteúdo anterior;
- `baseline`/`global_vigente`/`estado["estilo"]` permanecem os anteriores;
- candidato do runtime permanece disponível;
- `aplicar_disponivel` continua `True`;
- `estado["solicitacao_aplicacao_estilo"]` é removida (tentativa
  consumida, sem retry automático — §12);
- nenhuma exceção escapa do dispatch de comando.

### Falha de publicação

- Como `aplicar_candidato` publica via uma única troca de objeto
  imediatamente após persistência bem-sucedida, sem I/O intermediário, não
  há falha de publicação isolável de falha de persistência nesta
  arquitetura. Documentar essa ausência de cenário distinto, em vez de
  inventar um mecanismo de falha que a infraestrutura não expõe.

### Arquivo e publicação

- comparação semântica completa (§14, §15) em pelo menos duas categorias
  simultâneas divergentes (ex.: `borda` e `chip` no mesmo candidato
  confirmado), para comprovar que a aplicação não é de campo único.

### Regressão

- `tela/teste_estilo_h0063.py`, `tela/teste_estilo_h0065.py`,
  `tela/teste_estilo_h0066.py` — intactos, sem modificação;
- `demo/teste_demo_estilo_h0063.py`,
  `demo/teste_demo_estilo_h0064.py`,
  `demo/teste_demo_estilo_h0065.py`,
  `demo/teste_demo_estilo_h0066.py` — intactos, sem modificação;
- `demo/teste_demo_estilo_h0067.py` — apenas os três testes nominados em
  §16, com as asserções reestruturadas conforme especificado;
- `tela/teste_popup.py`, `demo/teste_demo_popup.py` — intactos;
- `tela/teste_loader.py` — intacto, exceto pela adição opcional focal do
  novo acessor (§18);
- suíte completa do projeto:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_estilo_h0068.py demo/teste_demo_estilo_h0068.py demo/teste_demo_estilo_h0067.py tela/teste_loader.py
```

## 20. Validação manual

H-0068 deve ser integralmente automatizável. Persistência, rollback,
baseline e publicação são inteiramente verificáveis por fixtures/probes
programáticas (estado do runtime, leitura de `config/estilo.json` em raiz
temporária, comparação semântica, monkeypatch de falha) — mesma técnica já
usada e validada por H-0061 e H-0067. Nenhum gate manual é necessário
apenas para confirmar mudança de dados.

O único requisito visual do ITEM-0010 ainda pendente (demonstração
integrada com Cabeçalho + Console + Dashboard + Barra sob override local,
§17) não pertence a H-0068 e não é validado nesta etapa — nenhuma
validação manual TTY é criada aqui além do que já foi validado em
H-0056–H-0067 para o popup e a tela de Estilo, ambos reutilizados sem
alteração estrutural.

## 21. Persistência/publicação não são preview

H-0068 aplica **definitivamente** o estilo confirmado a
`config/estilo.json` e ao único objeto global vigente consumido por todos
os renderers (`estado["estilo"]`, §7.4). Isso é distinto de:

- preview local (H-0065: candidato em memória, nunca aplicado a nenhum
  consumidor visual);
- override demonstrativo (ADR-0046 §5, ainda não implementado);
- amostras H-0064 (descrição do preset via `PresetEstilo.dados`, nunca
  preview aplicado à tela).

Após H-0068, qualquer tela renderizada na mesma sessão — inclusive uma
nova visita a F4 — usa o estilo recém-publicado, sem reinício do processo.

## 22. Demonstração integrada (fora de escopo, registrado)

A aplicação definitiva de H-0068 já torna possível observar a mudança
global de forma automatizada e programática (comparação de
`estado["estilo"]` antes/depois, ou renderização de qualquer tela já
existente após a aplicação). Isso **não substitui** a demonstração
integrada com override local exigida pela ADR-0046 §5 (Cabeçalho + Console
+ Dashboard + Barra de Menus compostos sob o candidato antes da
confirmação) — essa capacidade continua sem numeração própria e é
registrada em §17 como trabalho posterior, não implementada aqui.

## 23. Fora de escopo

- demonstração integrada com override local (ADR-0046 §5) e o próprio
  override local;
- popup, `CONFIRMADO`, `ABORTADO`, navegação, amostras — todos
  reutilizados sem alteração de comportamento;
- novo tipo/sistema de pop-up;
- novo popup de erro visual para falha de persistência/publicação;
- política de retry automático da mesma solicitação;
- segundo mecanismo de persistência ou publicação além de
  `aplicar_candidato`;
- `tiling`, `cor_inativo`, `cor_alerta`, `indicadores.concluido`;
- `ITEM-0024`, `ITEM-0032`;
- F1, F11, F2, F3, F5.

## 24. Critérios de aceite

H-0068 está concluído quando a prova automatizada demonstrar que:

1. um `Enter/Aplicar` ativo seguido de `Enter/Confirmar` real (via popup)
   persiste `config/estilo.json` (raiz de teste) com o candidato
   confirmado completo, preservando campos fora do escopo;
2. após esse sucesso, `estilo_runtime.baseline`,
   `estilo_runtime.global_vigente`, `estilo_runtime.candidato` e
   `estado["estilo"]` (o slot efetivamente consumido pelos renderers) são
   todos iguais à nova materialização;
3. após sucesso, `aplicar_disponivel` é `False`, `estado["selecoes"]`
   reflete a nova baseline e `estado["solicitacao_aplicacao_estilo"]` está
   ausente;
4. `ABORTADO` continua sem qualquer efeito de persistência/publicação
   (regressão intocada de H-0067);
5. falha injetada de persistência é fail-closed: arquivo, baseline, global
   e `estado["estilo"]` anteriores preservados; candidato do runtime
   disponível; `aplicar_disponivel` continua `True`; solicitação daquela
   tentativa removida; nenhuma exceção escapa do dispatch;
6. a aplicação usa exclusivamente `solicitacao.candidato` (snapshot
   confirmado), nunca uma releitura do candidato mutável do runtime;
7. nenhuma segunda primitiva de persistência ou publicação é criada —
   `aplicar_candidato` (H-0061) é reutilizada sem duplicação;
8. os três testes nominados em §16 são atualizados exatamente nas
   asserções superadas, preservando todas as demais garantias;
9. suíte completa do projeto passa.

## 25. Fronteira posterior

Após aprovação de H-0068, resta ao `ITEM-0010` exclusivamente a
demonstração integrada com override local (Cabeçalho + Console + Dashboard
+ Barra de Menus, ADR-0046 §5), ainda não implementada por nenhum handoff.
A decisão de numerar e especificar esse handoff posterior cabe ao gerente,
observando o resultado real desta aplicação definitiva. Este documento não
numera nem especifica esse handoff.
