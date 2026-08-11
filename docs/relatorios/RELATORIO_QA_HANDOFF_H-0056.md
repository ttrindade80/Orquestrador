# Relatório QA documental — H-0056

```yaml
item: ITEM-0017
adr: ADR-0044
handoff: H-0056
patch_handoff: P01
status: HANDOFF_REJECTED
```

## Escopo e verificações

Foram auditados integralmente o handoff e os três contratos e a nomenclatura
indicados no manifesto fechado. A inspeção focal confirmou o escopo incremental,
a separação entre declaração e conteúdo runtime, a resolução por
`popups["popup_basico"]`, a modalidade sobre a mesma tela, a geometria simples,
os domínios de espaçamento, o retorno `status: ABORTADO` sem payload, as
exclusões de H-0057/H-0058/H-0059, os caminhos nominais, os testes focais, o
roteiro demonstrativo e o relatório obrigatório de implementação.

`git diff --check`: aprovado, sem saída.

## Achado material

**QA-H0056-001 — declaração demonstrativa de chip incompatível com o contrato**

O handoff define como “configuração estrutural demonstrativa fechada”
(`H-0056`, linhas 133–147) um chip contendo somente:

```json
{
  "tecla": "Esc",
  "rotulo": "Voltar"
}
```

Isso não satisfaz os campos mínimos do `contrato_chip.md`, seção 4, nem seus
critérios de validação da seção 17: faltam `id`, `tipo`, `texto`,
`acao`/`referencia_regra`, `regra_existencia`, `regra_ativo` e
`forma_exibicao`. Além disso, `rotulo` não é o campo normativo `texto`.
O contrato não estabelece exceção para chips consumidos por pop-ups; ao
contrário, afirma que a mesma entidade `chip` pode ser consumida pela área
própria do pop-up. A validação fechada do pop-up também exige rejeição de chip
inválido.

Assim, a configuração que o handoff manda materializar é rejeitada antes da
abertura, tornando o fluxo demonstrativo inexequível e mantendo uma
contradição material com a autoridade contratual. O handoff não pode ser
encaminhado para `IMPLEMENTAR` enquanto a declaração do chip não for tornada
compatível com o contrato aplicável, preservando a separação entre tecla,
rótulo e retorno não confirmatório.

Não foram identificados outros achados materiais nem bloqueio residual
independente do achado acima.
