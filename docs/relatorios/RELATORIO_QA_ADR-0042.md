# Relatório QA — ADR-0042

status: ADR_REJECTED
adr: ADR-0042-navegacao-multinivel-do-console
data: 2026-08-08

## Resultado

A ADR-0042 permanece com status `proposta` e contém achados materiais que
exigem correção documental.

## Achados

### QA-ADR-0042-01 — Planejamento de handoffs incorporado como obrigação

- **Requisito violado:** a decomposição, a quantidade e a sequência de
  handoffs não pertencem ao conteúdo normativo desta ADR. D-MULTI-01 a
  D-MULTI-11 não fecham esse planejamento; D-MULTI-11 apenas preserva
  critérios para etapas futuras.
- **Evidência focal:** a ADR afirma que o backlog registra a decomposição em
  handoffs sequenciais (§2.1, linhas 66–72), registra como papel do backlog a
  “exigência de decomposição em quatro handoffs sequenciais” (§2.3, linha
  113) e afirma que, sem a ADR, o item não poderia avançar para “aplicação,
  handoff e implementação” (§7, linhas 464–468).
- **Impacto:** o plano de execução do backlog, que não é contrato nem
  autorização, é promovido a restrição arquitetural/documental e passa a
  vincular quantidade, sequência e avanço do ciclo.
- **Correção necessária:** remover a quantidade, sequência e obrigação de
  handoffs e a afirmação de que a ADR condiciona esse avanço. Pode permanecer
  somente o reconhecimento de que implementação e handoffs são posteriores,
  com os critérios de D-MULTI-11.

### QA-ADR-0042-02 — Momento não decidido para a falha focal de `tabela`

- **Requisito violado:** D-MULTI-04 determina apenas falha focal para
  declaração incompatível de tabela navegável. Não é permitido fixar momento,
  camada ou mecanismo concreto da falha.
- **Evidência focal:** §4.4, linhas 331–335, determina que a declaração seja
  “rejeitada antes de qualquer renderização” e não convertida silenciosamente.
- **Impacto:** a ADR introduz uma etapa e uma estratégia de tratamento que
  não foram decididas, restringindo validação, diagnóstico e fluxo de
  apresentação.
- **Correção necessária:** manter a classificação como `falha focal`, sem
  determinar quando, em que camada ou por qual mecanismo ela ocorre. O
  requisito de não usar fallback para `nivel_unico` deve ser preservado.

### QA-ADR-0042-03 — Colisão de `Esc` em `dois_niveis_por_foco`

- **Requisito violado:** D-MULTI-08 exige que `Esc` no nível dos filhos
  retorne aos pais; D-MULTI-09 exige que cada pai permaneça com exatamente um
  filho escolhido. A autoridade vigente também deve ser preservada.
- **Evidência focal:** §4.7, linhas 371–381, fixa o retorno por `Esc` e a
  escolha obrigatória. Porém, `docs/contratos/contrato_console.md` §23.4,
  linhas 1186–1195, determina que `Esc` com seleção ativa limpa a seleção e
  permanece na tela. A ADR não estabelece precedência ou exceção para a nova
  política.
- **Impacto:** como há sempre um filho escolhido, a regra vigente pode
  impedir o retorno e deixar o pai sem filho escolhido, produzindo
  comportamento contraditório e ambiguidade funcional.
- **Correção necessária:** explicitar a precedência de D-MULTI-08 para essa
  política: `Esc` deve retornar ao nível dos pais preservando a escolha
  obrigatória, sem introduzir semântica de cancelamento.
