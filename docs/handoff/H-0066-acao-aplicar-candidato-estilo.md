# H-0066 — Ação Aplicar sobre o candidato de estilo

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0066
data_criacao: 2026-08-12
status: READY_FOR_IMPLEMENTATION
predecessor: H-0065
relacao: continuacao_funcional
historico:
  H-0061:
    estado: aprovado
    capacidade:
      - baseline_runtime
      - candidato_runtime
      - materializacao
      - comparar_candidato_baseline
      - primitivas_de_persistencia_publicacao_para_etapas_posteriores
  H-0063:
    estado: aprovado
    capacidade:
      - tela_normal
      - dois_niveis_por_foco
      - barra_de_menus
      - F4
      - Esc
      - resize
      - paginacao
  H-0064:
    estado: aprovado
    capacidade:
      - amostras_visuais
  H-0065:
    estado: I1_IMPLEMENTATION_APPROVED
    capacidade:
      - candidato_fonte_semantica
      - Espaco_atualiza_candidato
      - selecoes_projeta_candidato
      - descarte_na_saida_sem_confirmacao
dependencias:
  - H-0061
  - H-0063
  - H-0064
  - H-0065
item_0010:
  estado: em_andamento
fronteira_posterior:
  - confirmacao_da_aplicacao
  - demonstracao_integrada_com_override_local
  - persistencia
  - publicacao
```

H-0066 é continuação funcional de H-0065, não substituição. A tela normal,
os quatro pais, `dois_niveis_por_foco`, amostras H-0064, fonte semântica
candidato, `Espaço`, reconciliação de `selecoes` e descarte na saída efetiva
permanecem integralmente vigentes. H-0062 permanece histórico/substituído e
não é reaberto; trechos técnicos já existentes da infraestrutura de
`Aplicar` (contexto `aplicar_disponivel`, regra `candidato_divergente`) podem
ser reutilizados como arquitetura vigente, sem restaurar o shell popup-like
de H-0062.

## 2. Objetivo exclusivo

Especificar e autorizar a fatia:

```text
AÇÃO APLICAR
```

Fronteira normativa desta capacidade:

```text
candidato modificado
→ ação Aplicar elegível
→ usuário aciona Aplicar (Enter / chip)
→ sistema produz somente a transição/intenção autorizada para a etapa
  posterior de confirmação
→ H-0066 termina
```

H-0066 **não** executa a decisão de confirmação e **não** antecipa:

- desenho de popup;
- texto do popup;
- botões/opções do popup;
- `CONFIRMADO` / `ABORTADO`;
- demonstração integrada com override local;
- persistência em `config/estilo.json`;
- publicação do estilo global;
- preview real do candidato no runtime global.

## 3. Compatibilidade com ADR-0046

A ADR-0046 trata `Enter/Aplicar`, a demonstração+confirmação e a
persistência/publicação como etapas distintas do fluxo (§4–§8; tabela §7).
O evento `Enter/Aplicar` ativo dispara a transição *para* o estado composto
“Demonstração + confirmação”; a confirmação humana e seus resultados
(`CONFIRMADO`/`ABORTADO`) pertencem a esse estado destino, não à edição.

Portanto, a partição operacional de H-0066 — habilitar/acionar `Aplicar` e
entregar somente a intenção/solicitação estrutural para a etapa posterior —
é compatível com a ADR: este handoff cobre o lado origem da transição
(`Seleção/edição` + elegibilidade + acionamento) e deixa o destino
(demonstração, popup, decisão, persistência, publicação) para handoff(s)
posteriores. Não há conflito material que exija `BLOCKED_DOCUMENTATION`.

Diferença documental obrigatória:

| Capacidade | Papel |
|---|---|
| AÇÃO APLICAR (H-0066) | Detectar divergência, expor/habilitar a ação, receber o acionamento, produzir a solicitação/transição para confirmação |
| CONFIRMAÇÃO DA APLICAÇÃO (posterior) | Obter decisão humana sobre a tentativa; devolver `CONFIRMADO` ou `ABORTADO` |
| Persistência/publicação (posterior) | Somente após `CONFIRMADO`, na ordem fail-closed da ADR |

## 4. Autoridade principal

Lidas integralmente:

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`
- `docs/handoff/H-0061-infraestrutura-estilo-runtime.md`
- `docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md`
- `docs/contratos/contrato_estilo.md` (ciclo §3.8; R-1, R-11, R-12, R-13)
- `docs/nomenclatura/10_ESTILO.md` §4.8–§4.9
- `docs/contratos/contrato_barra_de_menus.md` §§7, 8.1, 8.2, 10, 10.1, 16.1, R-6, R-13
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` §4.5.1

Lidas focalmente:

- `docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md`
- `docs/handoff/H-0064-amostras-visuais-presets-estilo.md`

Código inspecionado somente para pontos de integração (sem alteração nesta
etapa):

- `tela/carregamento/estilo.py` — `comparar_configuracoes_estilo` /
  `EstadoEstiloRuntime.comparar_candidato_baseline`
- `tela/estilo.py` — `ControladorTelaEstilo`
- `demo/demo.py` — F4/`Espaço`/`Esc`/render da tela H-0063
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
- `tela/renderizacao/contexto_execucao.py` — campo `aplicar_disponivel`
- `tela/renderizacao/barra_menus.py` — `regra_ativo: candidato_divergente`
- `config/telas/demo/h0062_estilo.json` — precedente declarativo histórico
  do chip `[⏎] Aplicar` (não restaurar H-0062 como autoridade funcional)

## 5. Matriz documental obrigatória

### A. Existência de Aplicar

| Pergunta | Classificação | Determinação |
|---|---|---|
| A ação/chip deve existir sempre? | DETERMINADO_PELA_AUTORIDADE | Existência é estática (declaração no `tela.json`); ativo/inativo é dinâmico (`contrato_barra_de_menus.md` §8.1). Na tela de Estilo, o chip `[⏎]` com semântica `Aplicar` deve ser declarado e permanecer presente. |
| Só deve existir quando candidato difere? | DETERMINADO_PELA_AUTORIDADE (negativo) | Não. Ausência dinâmica violaria a distinção existência × ativo/inativo. |
| Deve existir desabilitada sem diferença? | DETERMINADO_PELA_AUTORIDADE | Sim. Sem divergência permanece inativa (`cor_inativo`), sem reagir ao acionamento (ADR-0046 §4; contrato_barra §10.1; R-6). |
| Literal/forma canônica? | DERIVAVEL_DA_ARQUITETURA_EXISTENTE | Ação normativa: `Enter/Aplicar`. Forma declarativa já usada pelo precedente H-0062 e pela regra vigente: `id` `chip_aplicar`, `tecla` `⏎`, `texto` `Aplicar`, `regra_ativo` `candidato_divergente`. A ADR não fixa rótulo textual novo além da semântica `Aplicar`. |

### B. Enter

| Pergunta | Classificação | Determinação |
|---|---|---|
| Enter aciona Aplicar? | DETERMINADO_PELA_AUTORIDADE | Sim (`contrato_barra_de_menus.md` §10.1; ADR-0046 §4/§7). |
| Em qual foco/nível? | DERIVAVEL_DA_ARQUITETURA_EXISTENTE | Enquanto a tela de Estilo estiver ativa, Enter é a ação contextual `Aplicar`, independentemente do toroide corrente (pais ou filhos). A ADR não restringe por nível; não há autoridade para criar restrição nova. |
| É contextual? | DETERMINADO_PELA_AUTORIDADE | Sim — especialização do consumidor Estilo; não redefine `[⏎]` nas demais telas. |
| Precedência? | DETERMINADO_PELA_AUTORIDADE | Não substitui `Espaço` (escolha candidata). Não conflita com `Esc` (navegação/saída H-0065). Não pode ser materializado como `Todos`/`Executar` da seleção múltipla. Quando inativo, o acionamento não produz efeito (ADR §7: “Enter/Aplicar inativo → nenhum efeito…”). |

### C. Condição de elegibilidade

**DETERMINADO_PELA_AUTORIDADE + primitivas H-0061.**

- Baseline = última configuração persistida conhecida pelo fluxo.
- Candidato = estado de edição (fonte semântica H-0065).
- Comparação canônica: `EstadoEstiloRuntime.comparar_candidato_baseline` /
  `comparar_configuracoes_estilo` (comparação semântica da configuração
  completa; não criar flag manual independente).

Fórmula semântica literal da comparação (não inverter):

```text
comparar_candidato_baseline() == True
→ candidato semanticamente igual à baseline
→ nenhuma alteração pendente

comparar_candidato_baseline() == False
→ candidato divergente da baseline
→ existe alteração pendente
```

Ponte literal obrigatória para a UI (a implementação **não** pode inferir
a inversão):

```text
aplicar_disponivel :=
    not EstadoEstiloRuntime.comparar_candidato_baseline()
```

(ou expressão equivalente usando a instância runtime real).

Significado de `aplicar_disponivel` (valor derivado/projetado, não segunda
fonte de verdade):

```text
aplicar_disponivel == True
→ regra `candidato_divergente` deve considerar Aplicar ativo

aplicar_disponivel == False
→ Aplicar permanece declarado, mas inativo
```

Qualquer armazenamento intermediário de `aplicar_disponivel` é **somente**
cache de renderização/contexto, nunca autoridade semântica. Em cada
preparação relevante da tela, deve ser novamente derivado da relação
candidato×baseline. Proibido tratar `self.aplicar_disponivel = True` (ou
equivalente) como estado independente capaz de sobreviver a A→B→A sem
recálculo.

Não inventar catálogo paralelo de alterações nem segundo baseline/candidato.

### D. Resultado de acionar Aplicar

**DETERMINADO_PELA_AUTORIDADE (efeito permitido antes da confirmação) +
partição operacional compatível.**

- Inativo: nenhum efeito de demonstração, confirmação, persistência ou runtime.
- Ativo: produzir **somente** a solicitação/transição estrutural imutável
  destinada à etapa posterior de confirmação, carregando snapshot/cópias
  independentes de `candidato` e `baseline` (e demais elementos mínimos já
  definidos nesta fatia) no instante do acionamento.

A solicitação **não** pode carregar referências mutáveis capazes de refletir
alterações posteriores do runtime. O contrato é de imutabilidade observável
do snapshot: não se obriga `deepcopy` literalmente se a implementação usar
estrutura imutável/materialização equivalente já existente; referências
diretas mutáveis que mudem retroativamente a solicitação **não** são
conformes. Não inventar literal novo de evento.

Ao acionar Aplicar ativo nesta fatia, o runtime permanece intacto:

- baseline runtime não muda;
- candidato runtime não é destruído;
- global não muda;
- arquivo não muda;
- nenhuma persistência;
- nenhuma publicação;
- nenhum popup abre nesta fatia.

A solicitação é somente snapshot/intenção estrutural.

H-0066 **não** abre demonstração, **não** abre popup, **não** obtém
confirmação humana, **não** persiste e **não** publica. O consumidor
posterior (fora deste handoff) é quem realiza o destino ADR
“Demonstração + confirmação”.

Não inventar literais de máquina de estados ADR como `APPLY_REQUESTED`,
`SOLICITAR_CONFIRMACAO` ou `PENDING_CONFIRMATION`. O efeito observável é
estrutural (objeto/sinal de solicitação + ausência dos efeitos proibidos).
Nomes internos de classe/função permanecem detalhe de implementação, desde
que preservem a semântica acima.

### E. Candidato antes da confirmação

**DETERMINADO_PELA_AUTORIDADE.** Acionar Aplicar, por si só:

- não altera baseline;
- não publica global;
- não escreve `config/estilo.json`;
- não destrói nem reinicializa o candidato antes da decisão posterior.

O candidato permanece o estado de edição da visita corrente.

### F. Esc

**DETERMINADO_PELA_AUTORIDADE (H-0065 + ADR).** Enquanto nenhuma confirmação
estiver aberta (e H-0066 não abre nenhuma), `Esc` permanece exatamente como
em H-0065. Distinguir obrigatoriamente:

**Esc filho→pais** (navegacional; não é saída efetiva):

```text
antes:  baseline=A, candidato=B
        comparar = False
        aplicar_disponivel = True
        Aplicar = ativo
Esc filho→pais
depois: baseline=A, candidato=B (preservados)
        aplicar_disponivel = True
        Aplicar = ativo
        nenhuma solicitação emitida
        nenhum descarte / persistência / publicação
```

**Esc de saída efetiva** (abandona a tela; restaura candidato da baseline
conforme H-0065; elegibilidade volta a inativa):

```text
antes:  baseline=A, candidato=B, Aplicar=ativo
depois: baseline=A, candidato=A, Aplicar=inativo
```

Não confundir Esc filho→pais com saída efetiva.

### G. Cancelamento/desabilitação dinâmica

**DETERMINADO_PELA_AUTORIDADE.** A elegibilidade/`aplicar_disponivel` é
recalculada/projetada a partir de candidato×baseline — nunca de flag
residual. Exemplo normativo A→B→A (sem flag residual):

```text
baseline=A, candidato=A
comparar = True
aplicar_disponivel = False
Aplicar = inativo

Espaço em B:
baseline=A, candidato=B
comparar = False
aplicar_disponivel = True
Aplicar = ativo

Espaço volta para A:
baseline=A, candidato=A
comparar = True
aplicar_disponivel = False
Aplicar = inativo
```

Pontos mínimos de recálculo/projeção de `aplicar_disponivel` (sem nova
arquitetura de eventos): sempre que a tela for preparada/renderizada depois
de:

- abertura/F4;
- Espaço bem-sucedido;
- falha/reconciliação, se houver recomposição;
- redraw;
- resize;
- retorno de Esc filho→pais;
- restauração da baseline na saída efetiva, enquanto a tela/contexto ainda
  estiver sendo concluído.

Setas não afetam elegibilidade. Resize/redraw não inventam alterações nem
perdem o estado derivado da comparação.

## 6. Reuso obrigatório de H-0061

Reutilizar exclusivamente:

- `EstadoEstiloRuntime.comparar_candidato_baseline` /
  `comparar_configuracoes_estilo` para elegibilidade;
- o candidato e a baseline já mantidos pelo runtime;
- nenhuma segunda estrutura de “tem_alteracoes” persistente.

`tem_alteracoes` / elegibilidade / `aplicar_disponivel`, se expostos, são
**derivados** da comparação canônica no instante da consulta, via a ponte
literal da §5.C:

```text
aplicar_disponivel := not EstadoEstiloRuntime.comparar_candidato_baseline()
```

Não há segunda fonte de verdade.

## 7. Barra de Menus

Introduzir/ativar o chip `[⏎] Aplicar` na declaração da tela H-0063,
respeitando a política vigente:

```text
[Esc] → … → [⏎] Aplicar → … → [?] Ajuda
```

Regras:

- preservar `[PgUp][PgDn] Páginas` quando aplicável;
- preservar `[?] Ajuda` sempre ativo e último;
- não resolver ordenação global nem `ITEM-0032`;
- não inventar reordenação canônica nova;
- ordem relativa: `Aplicar` na posição canônica de `[⏎]` (antes dos
  específicos e de `[?]`), conforme `contrato_barra_de_menus.md` §7.

Infraestrutura já existente a consumir sem redesenho: `aplicar_disponivel`
em `contexto_execucao` e avaliação `candidato_divergente` em
`barra_menus.py`. A injeção/projeção de `aplicar_disponivel` deve usar
explicitamente a fórmula da §5.C (`not comparar_candidato_baseline()`),
nunca o retorno bruto de `comparar` sem a inversão.

## 8. Navegação dois níveis e H-0065

Preservar integralmente H-0063/H-0065. `Aplicar` não pode:

- substituir `Espaço`;
- modificar o significado das setas;
- desfazer a escolha candidata;
- alterar a fonte semântica candidato;
- tornar `selecoes` segunda autoridade.

## 9. H-0064

Preservar amostras integralmente. Existência/elegibilidade de `Aplicar` não
muda borda compacta, chip `Ab`/`AB`, indicadores nem ANSI.

## 10. Saída sem Aplicar / sem confirmação

Preservar H-0065: abandono efetivo da tela sem passar pela futura
confirmação descarta o candidato não confirmado e reconcilia à baseline.
H-0066 não altera essa regra. Acionar `Aplicar` nesta fatia **não** conta
como confirmação; até a etapa posterior obter `CONFIRMADO`, as diferenças
continuam “não confirmadas” para efeito de saída.

## 11. Sem persistência, sem publicação, sem preview real

Mesmo após acionar `Aplicar` dentro de H-0066:

- `config/estilo.json` intacto;
- baseline intacta;
- global intacto;
- candidato permanece candidato até confirmação posterior;
- proibido aplicar o candidato ao runtime global “só para demonstrar Aplicar”.

## 12. Arquivos autorizados para implementação

Lista mínima nominal, a partir da arquitetura real:

### Declaração e controlador

- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json` —
  declarar o chip `[⏎] Aplicar` (`chip_aplicar`, `regra_ativo:
  candidato_divergente`), preservando Ajuda último e paginação vigente.
- `tela/estilo.py` — expor elegibilidade derivada de
  `comparar_candidato_baseline` e a capacidade de produzir a solicitação
  estrutural imutável ao acionar Aplicar ativo; sem abrir popup/demo e sem
  persistir/publicar.

### Integração de dispatch e render

- `demo/demo.py` — interceptar Enter na tela de Estilo como `Aplicar`
  (não `Todos`/`Executar`); quando inativo, no-op; quando ativo, receber a
  solicitação estrutural sem executar confirmação/persistência/publicação;
  injetar `aplicar_disponivel` no caminho de render da tela de Estilo via
  `aplicar_disponivel := not …comparar_candidato_baseline()` (não o retorno
  bruto de `comparar`).
- `tela/renderizacao/tela.py` — somente o encadeamento pontual do parâmetro
  `aplicar_disponivel` até `_preparar_contexto_navegacao` (espelhando o
  padrão já existente de `executar_disponivel`), necessário porque o caminho
  atual não encaminha esse campo e acaba zerando-o. Não autoriza redesign
  global do renderer nem renderer específico novo de Estilo.

### Testes e relatório

- `tela/teste_estilo_h0066.py`
- `demo/teste_demo_estilo_h0066.py`
- `docs/relatorios/IMP-0066-acao-aplicar-candidato-estilo.md`

### Atualização autorizada de expectativas predecessoras “sem Aplicar”

H-0066 supera deliberadamente a expectativa predecessora de ausência de
`Aplicar`. Autoriza-se atualizar **somente** as asserções que afirmam
literalmente inexistência de Aplicar/chip_aplicar, preservando todas as
demais garantias:

- `demo/teste_demo_estilo_h0063.py` —
  `test_ajuda_ultimo_e_sem_aplicar_nem_entrada_no_nivel`,
  `test_fronteira_sem_confirmado_abortado_aplicar_popup` e asserções
  equivalentes `"Aplicar" not in …` / `"chip_aplicar" not in ids`
- `demo/teste_demo_estilo_h0064.py` — asserção `"Aplicar" not in quadro`
- `demo/teste_demo_estilo_h0065.py` — asserções de ausência de `Aplicar` no
  quadro/chips / `test_sem_aplicar_nem_preview_real_no_quadro`
- `tela/teste_estilo_h0063.py` — `"Aplicar" not in dir(controlador)` (se
  ainda presente)
- `tela/teste_estilo_h0065.py` — `"Aplicar" not in dir(controlador)` e
  fronteiras que neguem a existência da ação agora introduzida

Não ampliar outros arquivos “por garantia”. Não autorizar alteração de
`tela/carregamento/estilo.py`, `config/estilo.json`, ADR, contratos,
nomenclatura ou backlog nesta implementação.

Consumir sem alterar (já suficientes): `tela/renderizacao/contexto_execucao.py`
e a avaliação `candidato_divergente` em `tela/renderizacao/barra_menus.py`.

## 13. Testes automatizados mínimos

### Fórmula `aplicar_disponivel`

Provar literalmente que a ponte UI é:

```text
aplicar_disponivel = not comparar_candidato_baseline()
```

(e que injetar o retorno bruto de `comparar` sem a inversão não é conforme).

### Baseline igual candidato

- `Aplicar` presente e inativo;
- Enter/chip não produzem solicitação nem efeitos colaterais;
- nenhuma transição indevida.

### Candidato diferente

- `Aplicar` ativo;
- acionar produz somente a solicitação/transição estrutural autorizada;
- baseline, global e arquivo intactos; candidato preservado.

### Volta à baseline (A→B→A)

- inativo → ativo → inativo;
- `aplicar_disponivel` False → True → False;
- sem flag residual.

### Quatro categorias

Mudança em qualquer uma das quatro categorias afeta a elegibilidade de
forma coerente.

### Setas

Não afetam elegibilidade.

### Resize/redraw

Não perdem elegibilidade derivada nem inventam alterações.

### Esc filho→pais (distinto da saída efetiva)

Preparação: `baseline=A`, `candidato=B` → Aplicar ativo; estar no nível dos
filhos. Executar Esc filho→pais. Resultado obrigatório:

- candidato continua B;
- baseline continua A;
- `aplicar_disponivel` continua True;
- Aplicar continua ativo;
- nenhuma solicitação é emitida;
- não ocorre descarte;
- não ocorre persistência/publicação.

Esse teste é distinto da saída efetiva da tela.

### Esc de saída efetiva

Preserva a regra H-0065 de descarte na saída efetiva. Exemplo obrigatório:

```text
antes:  baseline=A, candidato=B, Aplicar=ativo
depois: baseline=A, candidato=A, Aplicar=inativo
```

Não confundir com Esc filho→pais.

### Snapshot imutável da solicitação

Preparação: `baseline=A`, `candidato=B`, Aplicar ativo. Acionar
Enter/Aplicar e capturar `solicitacao_1` (representa baseline=A,
candidato=B). Depois, **sem** modificar `solicitacao_1`, alterar o
runtime/candidato de forma válida (ex.: candidato=C, ou retorno a A).
Assert:

- `solicitacao_1.baseline` continua A;
- `solicitacao_1.candidato` continua B;
- a solicitação já emitida não passa a representar C/A.

No mesmo acionamento, preservar: baseline/candidato runtime intactos (não
destruídos), global/arquivo intactos, sem persistência, sem publicação, sem
popup nesta fatia.

### Fronteiras pré-confirmação

Após acionar Aplicar ativo nesta fatia:

- baseline intacta;
- global intacto;
- arquivo intacto;
- nenhuma persistência;
- nenhuma publicação;
- nenhum popup/`CONFIRMADO`/`ABORTADO`;
- nenhuma demonstração integrada.

### Regressões

Exigir regressão integral de H-0063, H-0064, H-0065 e suíte completa, com as
atualizações nominais da seção 12 para expectativas “sem Aplicar”
deliberadamente superadas. As mudanças predecessoras limitam-se a
expectativas concretamente superadas pela presença/ação de Aplicar (ex.:
Aplicar ausente, `chip_aplicar` inexistente, `"Aplicar" not in quadro`,
controlador sem capacidade `solicitar_aplicacao`). Não enfraquecer
invariantes de baseline/global/arquivo intactos, ausência de popup,
persistência, publicação ou preview real.

Comandos:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_estilo_h0066.py demo/teste_demo_estilo_h0066.py
```

## 14. Validação manual

Nenhuma. Estado habilitado, dispatch de Enter/Aplicar e ausência de
persistência/publicação/popup são comprováveis automaticamente (estado do
runtime, chips/`estado_ativo_chips`, solicitação estrutural, leitura do
arquivo).

## 15. Fora de escopo

- popup de confirmação e seus literais/rótulos;
- `CONFIRMADO` / `ABORTADO`;
- demonstração integrada (Cabeçalho + Console + Dashboard + Barra sob
  override);
- override local de demonstração;
- preview real do candidato no runtime global;
- persistência / publicação / promoção de baseline;
- `tiling`, `cor_inativo`, `cor_alerta`, `indicadores.concluido`;
- `ITEM-0032` e reordenação global da Barra;
- F1, F11, F2, F3, F5.

## 16. Critérios de aceite

H-0066 está concluído quando a prova automatizada demonstrar que:

1. com candidato == baseline, `Aplicar` existe e está inativo; Enter não
   produz solicitação nem efeitos; `aplicar_disponivel =
   not comparar_candidato_baseline()`;
2. com candidato != baseline (em qualquer das quatro categorias), `Aplicar`
   fica ativo; acionar produz somente a solicitação/transição estrutural
   autorizada (snapshot imutável);
3. A→B→A produz inativo→ativo→inativo (`aplicar_disponivel`
   False→True→False) sem flag residual;
4. setas não alteram elegibilidade; resize/redraw preservam o derivado da
   comparação;
5. Esc filho→pais com candidato divergente preserva candidato/baseline e
   Aplicar ativo, sem solicitação/descarte/persistência/publicação;
6. Esc/saída efetiva preservam H-0065 e restabelecem Aplicar inativo;
7. após Aplicar ativo nesta fatia, baseline/global/arquivo/candidato runtime
   permanecem intactos; snapshot da solicitação permanece imutável após
   mutação posterior do candidato; não há popup/confirmação/persistência/
   publicação/demo;
8. amostras H-0064 e navegação H-0063/H-0065 permanecem corretas;
9. testes predecessoras atualizados apenas nas expectativas “sem Aplicar”
   autorizadas, demais garantias preservadas;
10. suíte completa passa.

## 17. Fronteira posterior

Após aprovação de H-0066, a próxima partição do `ITEM-0010` — demonstração
integrada, popup de confirmação, `CONFIRMADO`/`ABORTADO`, persistência e
publicação — será decidida pelo gerente. Este documento não numera esse
handoff posterior.
