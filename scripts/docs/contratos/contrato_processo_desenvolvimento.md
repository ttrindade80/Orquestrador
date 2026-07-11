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

## 7. Precedente de violação dupla do ciclo

Uma implementação que introduza decisão arquitetural sem ADR precedente viola
o ciclo padrão. Uma implementação iniciada sem handoff precedente também viola
o ciclo padrão.

Quando as duas violações ocorrerem na mesma tentativa, a aceitação deve ser
interrompida: a decisão deve ser registrada por ADR, o handoff correto deve
ser criado e as etapas posteriores devem passar por QAs separados.
Implementação e autoavaliação no mesmo prompt ou execução não substituem QA
separado.

O caso `IMP-0022` é a referência histórica concreta dessa violação dupla.

## 8. Criterios de aceite

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

## 9. Bloqueio

O executor deve bloquear quando:

- contrato aplicavel nao existe;
- handoff contradiz contrato;
- escopo permitido e insuficiente;
- criterio de aceite nao e verificavel;
- decisao arquitetural esta faltando.

Status recomendado: `ARCHITECTURE_REVIEW_REQUIRED` para lacuna estrutural ou
`BLOCKED` para impedimento operacional.

## 10. Mudanças declarativas em JSON

Mudança puramente declarativa em JSON não exige handoff próprio quando
**todas** as condições abaixo são satisfeitas simultaneamente:

- o schema já suporta a declaração (campo existe e é reconhecido);
- o loader/modelo já preserva e valida os campos declarados;
- o renderer/binding já interpreta a declaração e produz o comportamento
  esperado;
- não há novo comportamento de código;
- não há novo tipo estrutural;
- não há nova ação, navegação, binding ou regra de renderização;
- não há mudança de contrato;
- não há mudança de arquitetura.

**Exemplos validados de mudança declarativa sem handoff próprio:**

- adicionar tela simples por JSON quando loader e renderer já suportam
  o tipo;
- apontar item de lancador para tela existente por JSON;
- alterar título de dashboard declarado;
- remover ou adicionar chip já suportado na `barra_de_menus` da própria
  tela;
- alterar texto de item de lancador respeitando o limite de 15 caracteres.

**Ciclo formal é obrigatório quando a alteração exigir qualquer um dos
itens abaixo:**

- novo binding entre dado e campo declarado;
- nova validação estrutural ou novo campo de schema;
- nova regra de renderização;
- nova navegação entre telas ou dentro de tela;
- nova ação;
- novo tipo estrutural (tipo de elemento, tipo de chip, tipo de item);
- mudança de contrato;
- mudança de arquitetura;
- alteração de código de qualquer módulo.

**Mudança declarativa pode exigir verificação, revisão ou commit**, mas não
precisa virar handoff próprio quando o suporte já existe. Se houver dúvida
sobre se o suporte existe, tratar como ciclo formal até confirmar.

A regra acima foi formalizada a partir da validação declarativa com `stub_b`
registrada em `f41bd2f`.

### 10.1 JSON necessário a um handoff que também altera código (ADR-0018)

A distinção da seção 10 é preservada: mudança **puramente** declarativa em JSON,
com suporte completo já existente (todas as condições da seção 10 satisfeitas),
pode continuar **sem handoff próprio**. Esta subseção não transforma toda
alteração JSON em ciclo de implementação.

Porém, quando uma alteração de JSON for **necessária para implementar, demonstrar
ou validar um handoff que também altera código** (ADR-0018, 2026-07-11), essa
alteração declarativa deve integrar o **próprio handoff**. Nesse caso, o handoff
deve:

- listar o caminho do arquivo JSON alterável;
- especificar a alteração declarativa exigida;
- registrar os valores concretos já decididos;
- incluir a validação sintática do JSON;
- incluir os critérios de aceite e os testes correspondentes.

O implementador **não** pode introduzir alteração de JSON omitida pelo handoff.
Esta regra **não** autoriza o renderer a hardcodar valores do JSON: a
configuração concreta pertence ao JSON da tela; o algoritmo genérico pertence ao
código.

## 11. Alteração por termo específico completo (ADR-0014)

Substrings ambíguas circulam no sistema com significados distintos. Por
exemplo, `vertical` e `horizontal` aparecem em `corpo.arranjo` (ADR-0011),
em `barra_de_menus.distribuicao` (ADR-0014) e em
`ocupacao_vertical_terminal` (ADR-0013) — três conceitos diferentes. Aplicar
uma decisão procurando apenas por substring atinge campos/conceitos errados.

Regras:

- **filtros parciais podem ser usados para busca**, auditoria e localização
  de candidatos (`rg`/`grep` por `vertical`, `horizontal`, `barra`, `chip`,
  `arranjo`, etc.);
- **alterações normativas e implementações devem atingir apenas termos
  específicos completos** — ex.: `corpo.arranjo = "vertical"`,
  `barra_de_menus.distribuicao = "horizontal"`, `ocupacao_vertical_terminal`,
  `preenchimento_altura_corpo`;
- **filtros parciais NÃO podem ser usados como critério de alteração
  normativa automática** — substituição global por substring é proibida;
- **ADRs e handoffs devem declarar exatamente o campo/conceito afetado**,
  nomeando o termo específico completo por extenso;
- **auditorias devem bloquear substituição por substring ambígua** quando
  houver mais de um termo específico candidato para a mesma substring.

A busca por substring é etapa de levantamento; a alteração é etapa normativa
distinta e exige confirmação termo a termo. Esta regra vale para ADRs
futuras, handoffs, implementações, migrações e QAs.

## 12. Exemplos neutros de nomes

```text
docs/contratos/contrato_modulo_exemplo.md
docs/handoff/para_implementacao/H-0001-criar-comando-exemplo.md
docs/relatorios/implementacao/IMP-0001-criar-comando-exemplo.md
docs/handoff/para_qa/QA-0001-revisar-comando-exemplo.md
docs/relatorios/qa/REL-QA-0001-revisar-comando-exemplo.md
```
