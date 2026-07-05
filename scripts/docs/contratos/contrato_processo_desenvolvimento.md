---
name: contrato-processo-desenvolvimento
description: Regras documentais para desenvolvimento por contrato, handoff e QA
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: modelo
---

# Contrato — Processo Documental

## 1. Objetivo

Definir um processo minimo para desenvolver scripts por especificacao. Este
contrato governa documentos, papeis, handoffs, relatorios e mudancas de regra.
Ele nao especifica nenhum modulo concreto.

## 2. Principio central

Implementacao so deve ocorrer quando houver:

1. contrato aplicavel;
2. handoff fechado;
3. criterios de aceite verificaveis;
4. limites claros de arquivos permitidos e proibidos.

## 3. Autoridade documental

Ordem de autoridade, da maior para a menor:

1. Contrato de processo;
2. ADRs aceitas;
3. Contrato do modulo;
4. Handoff;
5. Relatorio de implementacao;
6. Relatorio de QA.

Se um artefato inferior contradiz um superior, prevalece o superior.

## 4. Papeis

| Papel | Responsabilidade | Nao pode |
|---|---|---|
| Engenharia | Escrever contratos, ADRs e handoffs | Implementar escopo nao especificado |
| Implementacao | Executar handoff conforme contrato | Alterar contrato ou decidir arquitetura |
| QA | Verificar aderencia ao contrato | Aprovar violacao contratual |
| Usuario | Aprovar decisoes e executar comandos reais quando necessario | Ser substituido por inferencia automatica |

## 5. Ciclo padrao

1. Registrar necessidade no backlog ou issue.
2. Criar ou atualizar contrato.
3. Registrar ADR se houver decisao arquitetural.
4. Criar handoff de implementacao.
5. Produzir relatorio de implementacao.
6. Criar handoff de QA.
7. Produzir relatorio de QA.
8. Fechar issue/backlog com evidencia.

## 6. Mudanca de contrato

Nenhuma mudanca de contrato pode ser escondida em implementacao. Se a tarefa
exigir nova regra, criar RFC ou ADR antes de continuar.

## 7. Criterios de aceite

Todo handoff deve conter criterios:

- observaveis;
- testaveis ou auditaveis;
- vinculados a regra contratual;
- pequenos o bastante para serem verificados item a item.

Exemplo:

```markdown
- [ ] Para entrada valida, `modulo_exemplo` retorna objeto com campos `id` e `status`.
- [ ] Para entrada invalida, retorna erro documentado sem alterar estado persistido.
- [ ] Nenhum arquivo fora de `scripts/modulo_exemplo/` e modificado.
```

## 8. Bloqueio

O executor deve bloquear quando:

- contrato aplicavel nao existe;
- handoff contradiz contrato;
- escopo permitido e insuficiente;
- criterio de aceite nao e verificavel;
- decisao arquitetural esta faltando.

Status recomendado: `ARCHITECTURE_REVIEW_REQUIRED` para lacuna estrutural ou
`BLOCKED` para impedimento operacional.

## 9. Exemplos neutros de nomes

```text
docs/contratos/contrato_modulo_exemplo.md
docs/handoff/para_implementacao/H-0001-criar-comando-exemplo.md
docs/relatorios/implementacao/IMP-0001-criar-comando-exemplo.md
docs/handoff/para_qa/QA-0001-revisar-comando-exemplo.md
docs/relatorios/qa/REL-QA-0001-revisar-comando-exemplo.md
```
