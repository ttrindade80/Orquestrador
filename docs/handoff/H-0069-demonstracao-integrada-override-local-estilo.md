# H-0069 — Demonstração integrada com override local de estilo

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
item: ITEM-0010
adr: ADR-0046
handoff: H-0069
data_criacao: 2026-08-13
status: READY_FOR_IMPLEMENTATION
patch_aplicado: PATCH_HANDOFF_H-0069_P01
predecessor: H-0068
relacao: continuacao_funcional
historico:
  H-0063:
    capacidade: [tela_estilo_normal, navegacao_dois_niveis, F4, resize]
  H-0064:
    capacidade: [amostras_visuais_dinamicas_de_estilo]
  H-0065:
    capacidade: [candidato_runtime, selecao_por_espaco, descarte_da_visita]
  H-0066:
    capacidade: [aplicar_derivado_de_candidato, SolicitacaoAplicacaoEstilo_imutavel]
  H-0067:
    estado: ENCERRADO_TECNICAMENTE_E_MANUALMENTE
    capacidade: [popup_confirmacao, CONFIRMADO, ABORTADO]
  H-0068:
    estado: I1_IMPLEMENTATION_APPROVED
    capacidade:
      - aplicacao_definitiva_do_snapshot_confirmado
      - persistencia_atomica_via_H-0061
      - publicacao_global
      - promocao_da_baseline
      - reconciliacao_das_selecoes
      - fail_closed
item_0010:
  estado: em_andamento
capacidade_pretendida: demonstracao_integrada_com_override_local
```

## 2. Correção de P01 em relação à versão anterior

A versão anterior deste handoff foi emitida `BLOCKED_DOCUMENTATION` porque o
prompt de autoria daquela etapa transportava um requisito indevido: que "um
override declarado por tela/componente deve permanecer divergente de `G2`
depois que `G2` for confirmado". Esse requisito não existe em ADR-0046 §4/§5
e foi identificado, corretamente, como uma segunda noção de override não
autorizada.

O gerente resolveu essa interpretação contra as autoridades vigentes: o
único override existente é o candidato efêmero de uma única tentativa de
`Enter/Aplicar` (ADR-0046 §4, linha "Override de demonstração"; §5). Este
patch remove integralmente o requisito indevido, elimina o bloqueio e
reformula a capacidade como executável dentro do modelo já autorizado. Não
foi criada segunda noção de override.

## 3. Objetivo exclusivo

Especificar a demonstração integrada (Cabeçalho + Console + Dashboard +
Barra de Menus) que a ADR-0046 §5 exige entre `Enter/Aplicar` e o popup de
confirmação, materializando o candidato como override local somente nessa
demonstração e no popup sobre ela, sem tocar o estilo global vigente,
seguida da reutilização integral de H-0067 (`CONFIRMADO`/`ABORTADO`) e
H-0068 (aplicação definitiva).

H-0069 **não**:

- cria segunda noção de override declarada por tela/componente;
- exige ou prova que qualquer override sobreviva a uma aplicação
  `CONFIRMADA`;
- cria segundo mecanismo de persistência, publicação ou confirmação;
- reabre navegação, amostras, candidato ou popup — todos permanecem
  exatamente como entregues por H-0063–H-0068.

## 4. Semântica correta de override local

Existem exatamente quatro camadas, nesta ordem de distância do estilo
consumido pela execução (ADR-0046 §4):

1. configuração persistida (`config/estilo.json`);
2. materialização global vigente (`estilo_runtime.global_vigente`, espelhada
   em `estado["estilo"]`);
3. candidato (`estilo_runtime.candidato`, acumulado durante a edição);
4. override local de demonstração — visão derivada do candidato, aplicada
   somente à demonstração e ao popup de uma única tentativa em curso.

O override local:

- é temporário — existe apenas enquanto a demonstração daquela tentativa
  está aberta;
- é derivado do candidato, nunca um valor independente;
- aplica-se somente à tela de demonstração e ao popup dessa demonstração;
- não é persistido;
- não altera a baseline;
- não altera o `global_vigente`;
- não vaza para nenhuma outra tela;
- não constitui configuração declarativa persistente por tela ou
  componente.

Não há granularidade de override independente do candidato inteiro: não
existe override por campo, por categoria isolada ou por componente que se
componha separadamente com `estado["estilo"]`.

## 5. Fluxo correto antes da confirmação

Estado inicial conceitual: `global = G1`, `baseline = B1`, `candidato = C`,
com `C != B1` e `Aplicar` ativo (`comparar_candidato_baseline() is False`).

Ao acionar `Enter/Aplicar`:

1. abre-se a demonstração integrada;
2. a demonstração materializa localmente `C` via `materializar_local`
   (`tela/carregamento/estilo.py:347`), sem tocar `baseline` nem
   `global_vigente`;
3. a demonstração renderiza sob essa materialização local;
4. `global_vigente` permanece `G1`;
5. qualquer outra tela, se alcançável, continua consumindo `G1`
   (`estado["estilo"]` não é reescrito);
6. `config/estilo.json` permanece inalterado.

A demonstração é uma prévia local do candidato, não uma segunda
configuração declarativa.

## 6. Tela integrada

Composição obrigatória: Cabeçalho, Console, Dashboard e Barra de Menus, com
variedade suficiente de chips/estados na Barra para tornar visíveis os
efeitos do candidato (ADR-0046 §5). O objetivo é demonstrar visualmente o
candidato antes da decisão final — não provar precedência de um override
persistente por componente.

## 7. Popup

Sobre a demonstração abre-se o popup pequeno de confirmação já existente
(H-0067). O popup:

- reutiliza o sistema genérico de popup vigente, sem tipo novo;
- é renderizado sob a mesma materialização local derivada do candidato;
- apenas produz `CONFIRMADO` ou `ABORTADO`;
- não persiste nem publica diretamente (ADR-0046 §6.5-6.6).

## 8. ABORTADO

```text
ABORTADO
→ encerrar demonstração
→ retornar à tela Estilo
→ preservar candidato C
→ preservar baseline B1
→ preservar global G1
→ não persistir
→ não publicar
→ Aplicar continua ativo enquanto C != B1
```

O override local deixa de existir ao encerrar a demonstração. Não há
requisito de sobrevivência fora dela — essa era exatamente a exigência
indevida removida por este patch (§2).

## 9. CONFIRMADO

Fluxo já implementado pelos predecessores, reutilizado sem alteração de
mecanismo (H-0068):

```text
CONFIRMADO
→ persistência completa e válida de C (aplicar_candidato)
→ publicação global
→ nova baseline = C
→ candidato sincronizado com baseline
→ estado["estilo"] sincronizado com a nova materialização
→ retornar à tela Estilo
→ Aplicar fica inativo
```

Depois disso: `global = G2`, `baseline = G2`, `candidato = G2`. O override
local da demonstração não precisa coexistir divergente de `G2`: cumpriu sua
função de prévia temporária e deixa de ser uma camada relevante após a
aplicação.

## 10. Prova correta

### Estado A — global

`G1` é usado normalmente pela demonstração antes de `Enter/Aplicar`, e por
qualquer tela fora da demonstração durante toda a sequência.

### Estado B — demonstração temporária

Candidato `C` divergente é materializado somente na demonstração e no
popup, enquanto `G1` permanece globalmente vigente.

### ABORTADO

Retorno à seleção preserva `C` e mantém `G1`.

### CONFIRMADO

`C` é persistido/publicado (via H-0068) e passa a ser o novo global `G2`.

Essa sequência é suficiente para demonstrar as quatro camadas autorizadas
(§4). Não é exigida nenhuma prova de override sobrevivendo a `G2`.

## 11. Prova de isolamento

Enquanto a demonstração com `C` está aberta, os testes devem comprovar:

- a demonstração consome `C`;
- o popup consome `C`;
- `estilo_runtime.global_vigente` continua `G1`;
- `estilo_runtime.baseline` continua `B1`;
- `config/estilo.json` (raiz de teste) continua com o conteúdo de `B1`;
- nenhuma outra tela recebe `C` por efeito dessa demonstração
  (`estado["estilo"]` fora da demonstração permanece `G1`).

Esse é o significado correto de "local".

## 12. Prova após ABORTADO

- `global_vigente` continua `G1`;
- `baseline` continua `B1`;
- `candidato` continua `C`;
- demonstração fechada;
- retorno à tela Estilo;
- `aplicar_disponivel` continua `True`.

## 13. Prova após CONFIRMADO

Reutiliza H-0068 para a aplicação definitiva. H-0069 exige somente
integração suficiente para provar:

- antes da confirmação: demonstração e popup usam `C` localmente;
- após confirmação: `C` torna-se `global_vigente`/`baseline`/`estado["estilo"]`,
  exatamente como já coberto por H-0068 §14/§15/§19;
- nenhuma segunda primitiva de persistência ou publicação é criada por
  H-0069.

Não duplicar a cobertura completa de H-0068; apenas comprovar que o novo
passo (demonstração) não introduz caminho alternativo de aplicação.

## 14. Categorias visuais

A demonstração deve tornar observáveis as quatro categorias vigentes do
ITEM-0010: `borda`, `chip`, `indicadores.selecionado`,
`indicadores.incluido`. Não é obrigatório alterar as quatro simultaneamente
em todo teste, mas a fixture deve ser representativa o suficiente para
permitir validação visual real. Não incluir `tiling`, `cor_inativo`,
`cor_alerta` nem `indicadores.concluido` (fora de escopo de ADR-0046 §1.4).

## 15. Fixture

Nenhuma fixture existente em `config/telas/demo/` combina Cabeçalho +
Console + Dashboard + Barra de Menus com variedade de chips em uma única
tela (inspecionado nominalmente: `h0044_fluxo_execucao_integrado.json` tem
Cabeçalho + Console + Barra, mas não Dashboard; as fixtures `h0029_*`/
`h0030_*` têm Dashboard isolado, sem composição integrada com Barra).
Autoriza-se uma fixture nova específica, `h0069_estilo_demonstracao_
integrada.json`, com conteúdo suficiente para expor bordas, chips,
indicador selecionado e indicador incluído em uma composição real. Não criar
renderer paralelo: a fixture é consumida pelos renderers genéricos
existentes (`tela/renderizacao/*`), exatamente como qualquer outra tela.

## 16. Arquivos de implementação futura autorizados

- `demo/demo.py` — estender o ramo já existente de `Enter/Aplicar` na tela
  de Estilo (~linhas 1203-1231) para abrir a demonstração local em vez de
  abrir o popup diretamente sobre a tela de Estilo; a demonstração usa
  `estilo_runtime.materializar_local(candidato)` para produzir a
  materialização local e a expõe somente aos renderers da demonstração
  (não a `estado["estilo"]` global). O popup passa a abrir sobre a
  demonstração, reutilizando exatamente `ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO`
  e o ramo `CONFIRMADO`/`ABORTADO` já existente (~linhas 862-906), que passa
  a também fechar a demonstração local ao encerrar. Não duplicar dispatch de
  popup, não criar segundo tipo de popup.
- `config/telas/demo/h0069_estilo_demonstracao_integrada.json` — fixture
  nova (§15).
- `tela/teste_estilo_h0069.py` — testes dedicados da materialização local
  isolada (§11-§12).
- `demo/teste_demo_estilo_h0069.py` — testes de integração E2E
  (`Enter/Aplicar` → demonstração → popup → `CONFIRMADO`/`ABORTADO`).
- `docs/relatorios/IMP-0069-demonstracao-integrada-override-local-estilo.md`
  — relatório futuro da implementação.

Não autorizar alteração de renderers genéricos
(`tela/renderizacao/tela.py`, `console.py`, `popup.py`, `barra_menus.py`,
`contexto_execucao.py`, `tela/renderizador.py`) sem necessidade técnica
comprovada durante a implementação; nenhuma foi identificada nesta etapa
documental. Não alterar `tela/carregamento/estilo.py`,
`tela/estilo.py`, ADR, contratos, nomenclatura ou backlog além do já
previsto por H-0068.

## 17. Testes automatizados mínimos

1. candidato `C` divergente de `B1`;
2. abertura da demonstração via `Enter/Aplicar`;
3. demonstração materializada com `C` (Cabeçalho + Console + Dashboard +
   Barra);
4. `global_vigente` permanece `G1` durante a demonstração;
5. `baseline`/`config/estilo.json` (raiz de teste) permanecem `B1`;
6. popup usa a mesma materialização local `C`;
7. `ABORTADO`: fecha demonstração, preserva `C`, preserva `G1`/`B1`,
   `aplicar_disponivel` continua `True`;
8. `CONFIRMADO`: reutiliza o fluxo H-0068 existente sem modificação de
   mecanismo; `C` vira nova baseline/global; `estado["estilo"]`
   sincronizado; `aplicar_disponivel` fica inativo;
9. nenhuma escrita em `config/estilo.json` de produção pelos testes (raiz
   de teste isolada, mesma técnica de H-0061/H-0068);
10. pelo menos uma integração real cobrindo Cabeçalho + Console + Dashboard
    + Barra simultaneamente sob o candidato.

## 18. Validação manual obrigatória

H-0069 deve continuar exigindo validação manual TTY real pelo usuário,
verificando visualmente:

- **Antes de Aplicar**: tela normal consumindo o global vigente.
- **Durante a demonstração**: candidato visualmente aplicado à tela
  integrada; Cabeçalho, Console, Dashboard e Barra coerentes entre si;
  popup usando a mesma aparência candidata.
- **ABORTADO**: retorno à tela Estilo; candidato preservado; `Aplicar`
  ainda ativo.
- **CONFIRMADO**: após confirmação, novo estilo passa a vigorar
  globalmente; retorno coerente à tela Estilo; `Aplicar` inativo.
- **Resize** básico da demonstração e do popup, para garantir ausência de
  regressão visual.

## 19. Gate manual final do ITEM-0010

```yaml
VALIDACAO_MANUAL_FINAL_ITEM_0010: OBRIGATORIA
```

O gerente determinou uma validação manual integrada final antes do
fechamento do `ITEM-0010`, além da validação funcional específica de
H-0069 (§18). Essa rodada final pode identificar pequenos refinamentos de
apresentação de chips; este documento não especifica nem antecipa essas
mudanças.

## 20. Encerramento funcional

```yaml
ULTIMO_HANDOFF_FUNCIONAL_DO_ITEM: true
```

H-0069, ao cobrir demonstração local do candidato, popup sobre a
demonstração, `ABORTADO` integrado e `CONFIRMADO` integrado reutilizando
H-0068, esgota a capacidade funcional restante de ADR-0046 §5. Pequenos
refinamentos visuais eventualmente observados na validação manual final
(§19) não transformam, por si só, a arquitetura em novo handoff; serão
classificados pelo gerente conforme a natureza quando observados.

## 21. Fora de escopo

- segunda noção de override declarada por tela/componente;
- override sobrevivendo a uma aplicação `CONFIRMADA`;
- granularidade de override por propriedade/tela/componente;
- `tiling`, `cor_inativo`, `cor_alerta`, `indicadores.concluido`;
- novo tipo de popup;
- segundo mecanismo de persistência ou publicação além de
  `aplicar_candidato` (H-0068);
- redesign de renderers genéricos.
