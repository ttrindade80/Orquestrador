# Relatório QA — Handoff H-0052

```yaml
status: H2_HANDOFF_PATCH_REQUIRED
handoff: H-0052
artefato: docs/handoff/H-0052-fundacao-e-compatibilidade-das-politicas-de-navegacao.md
```

## Achados materiais

### H-0052-A — fallback além da ausência de `tipo`

**Requisito:** somente a ausência de `politica_navegacao.tipo` em um objeto
válido pode resolver para `nivel_unico`; configuração não-objeto deve ser
rejeitada pelo contrato estrutural.

**Evidência focal:** ADR-0042 D-MULTI-13 e `contrato_json_console.md` §7.1
limitam o fallback à ausência do campo e exigem `politica_navegacao` como
objeto. O H-0052 §7.1, porém, prescreve `nivel_unico` também quando o valor
não é `dict`. O carregador rejeita esse formato na variante de itens em
`_validar_valores_envelope_pre_adr_0028` (linhas 130–135), mas isso não torna
correta a regra de resolução ampliada; além disso, a variante histórica de
geração retorna antes da validação escalar.

**Impacto:** amplia indevidamente a compatibilidade e pode mascarar entrada
estrutural inválida, convertendo-a em comportamento de nível único.

**Correção material necessária:** restringir o fallback ao caso em que
`politica_navegacao` é objeto e não possui `tipo`; entrada não-objeto não pode
ser normalizada para `nivel_unico`. Incluir teste da fronteira corrigida,
além da regressão de rejeição no carregamento.

### H-0052-B — enumeração fechada deixada opcional

**Requisito:** quando presente, `tipo` aceita exatamente os cinco valores
fechados do contrato.

**Evidência focal:** `contrato_json_console.md` §7.1 e ADR-0042 D-MULTI-12
declaram a enumeração fechada. O H-0052 §7.1/§7.3 diz que sua validação não é
obrigatória e a deixa como opção do implementador. A camada indicada já
valida outros valores fechados em `_validar_valores_envelope_pre_adr_0028`,
mas atualmente só confirma que `politica_navegacao` é objeto.

**Impacto:** valor desconhecido ou não textual pode ser aceito e, na lógica
proposta de focalização, passar pelo caminho de nível único sem falha; nenhum
handoff posterior é proprietário nominal dessa validação.

**Correção material necessária:** tornar obrigatória, no carregamento, a
validação de `tipo` presente contra os cinco valores, sem criar matriz
adicional `navegavel × tipo`. Acrescentar teste automatizado para valor fora
da enumeração (inclusive tipo não textual, se aplicável ao validador).

### H-0052-C — teste obrigatório de setas em `tabela` não é exequível como especificado

**Requisito:** `tabela` não pode sofrer movimento de cursor pelas setas, e o
teste obrigatório §11 item 9 deve chamar os quatro `mover_*` diretamente.

**Evidência focal:** em `tela/navegacao.py`, `console_e_focalizavel` e
`lista_foco` filtram a elegibilidade, mas `_mover_horizontal` e
`_mover_vertical`, consumidos por `mover_direita/esquerda/baixo/cima`, operam
diretamente sobre o console recebido e não consultam essa elegibilidade.
Logo, tornar `tabela` não focalizável não garante o resultado exigido pelo
teste direto. A afirmação do H-0052 §7.2 de que nenhum `mover_*` precisa mudar
contradiz o próprio critério de teste.

**Impacto:** a implementação prescrita pode passar pelos fluxos de foco, mas
falhar no teste obrigatório e deixar a API focal de movimento com comportamento
incompatível com a passividade declarada.

**Correção material necessária:** alinhar a especificação do teste e do
mecanismo de entrada para preservar ausência de efeito também no cenário
direto, sem deixar essa propriedade implícita na lista de foco.

## Verificações materiais sem achado

- **QH52-CRIT-03:** aprovado como inércia técnica mínima e explicitamente
  limitada a esta etapa: os três literais são transportados, não caem em
  `nivel_unico`, e não recebem árvore, seleção, geometria ou teclas futuras.
  A fundação permanece extensível para o dispatch dos handoffs seguintes.
- **QH52-CRIT-04:** aprovado. `TelaEstruturaInvalida` já é a exceção canônica
  de estrutura (`tela/carregamento/erros.py`), e a função indicada já valida
  valores estruturais equivalentes no carregamento.
- A capacidade permanece coesa: preserva `nivel_unico`, torna `tabela`
  passiva e não antecipa Enter, execução, persistência, geometria ou as três
  navegações futuras.
- O escopo nominal é suficiente: os quatro módulos de código/teste e as duas
  fixtures novas cobrem resolução, carregamento, testes e demonstração; não há
  necessidade material de `ESCOPO_ADICIONAL_NECESSARIO`.
- A demonstração usa o runner TTY existente e os três comandos com `--tela`,
  incluindo legado, `nivel_unico` explícito e `tabela`; a aprovação TTY continua
  manual do usuário.
- A matriz de testes cobre legado/explícito, `navegavel`, passividade, falha
  focal, políticas futuras, paginação e regressão integral. Os testes faltantes
  decorrentes dos achados A e B foram registrados acima.

Nenhum arquivo de código, teste, configuração, contrato, ADR, nomenclatura ou
handoff foi corrigido. Este relatório é o único artefato materializado pela
auditoria.
