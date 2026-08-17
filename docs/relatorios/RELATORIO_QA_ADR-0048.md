# Relatório de QA — ADR-0048

```yaml
item: ITEM-0026
adr: ADR-0048
etapa: QA_ADR
status: ADR_REJECTED
```

## Resultado

`ADR_REJECTED`

A ADR cobre materialmente D-0026-01 a D-0026-11: localiza a autoridade no
JSON externo de conteúdo, preserva a exclusividade explícita por pai, separa
baseline e candidato, define aplicação por divergência, confirmação genérica,
sucesso, aborto, falha fail-closed e restauração por nova carga. Também
preserva as fronteiras de produtor/consumidor, loader/persistência,
cursor/escolha, conteúdo semântico/representação física e exclui ITEM-0023,
ITEM-0024 e as demais fronteiras de D-0026-11. Não fixa schema literal,
assinatura, caminho de script ou algoritmo físico de escrita.

## Achado material

### QA-ADR0048-001 — Reuso do termo canônico “seleção única”

- **Requisito:** preservar D-MULTI-09 e a nomenclatura vigente: a escolha
  persistida deve ser denominada “seleção exclusiva obrigatória de filho por
  pai”, sem reutilizar “seleção única”.
- **Evidência focal:** ADR-0048, §2.2, afirma que a estrutura persistida
  representa “seleção única dentro de cada conjunto de filhos”. A ADR-0042,
  D-MULTI-09 e o `contrato_console.md` §22.7 reservam “seleção única” ao item
  sob cursor, mecanismo não persistido e distinto da escolha do filho.
- **Impacto:** a formulação pode atribuir à escolha persistida a semântica do
  cursor e conflita diretamente com a autoridade terminológica anterior,
  apesar das distinções corretas registradas em outras seções da ADR.
- **Correção necessária:** substituir a formulação de §2.2 pela forma
  canônica ou por “escolha ativa exclusiva”, mantendo intacta a decisão de
  exatamente um filho ativo por pai. Não aplicar nesta etapa.

Sem outros achados materiais: o fluxo, as responsabilidades, as exclusões de
escopo, os critérios para aplicação e as autoridades enumeradas permanecem
coerentes.
