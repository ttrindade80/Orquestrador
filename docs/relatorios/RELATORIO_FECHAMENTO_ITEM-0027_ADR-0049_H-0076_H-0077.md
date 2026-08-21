# Relatório de fechamento — ITEM-0027 / ADR-0049 / H-0076 / H-0077

## Identificação

```yaml
item: ITEM-0027
adr:
  - ADR-0049
handoffs:
  - H-0076
  - H-0077
resultado: CONCLUIDO
```

## Decisão final

D-0027-10 fixa a autoridade canônica de composição textual da TUI:

```text
parágrafo lógico completo
→ formação das linhas com palavras inteiras
→ justificação das linhas aplicáveis
→ representação física
```

A R01 reprovou a validação manual porque o popup longo justificado partia
palavras pela largura física e não tratava o parágrafo completo como unidade
lógica; o resize perpetuava fragmentos. D-0027-10 responde a esse defeito:
palavras permanecem indivisíveis; não há divisão arbitrária por
largura/células, hifenização automática nem separação silábica; cada
recomposição parte do texto lógico original; linhas físicas anteriores não
são reentrada lógica; a justificação ocorre depois da formação das linhas e
expande apenas os vãos entre palavras das linhas aplicáveis.

Palavra maior que a largura permanece indivisível para o compositor; não
houve política global de clipping, overflow, scroll, fallback ou truncamento
desse caso. A última linha e whitespace/separadores arbitrários permanecem
sem política canônica específica. Truncamento deliberado continua distinto da
composição multilinear. ANSI, largura visual, CSI e SGR permanecem
preservados. Medição, mapa físico e paginação usam a mesma composição da
renderização.

## Cadeia final

- ADR-0049 pós-P04: `ADR_APPROVED`;
- aplicação documental pós-P03: `ADR_APPLICATION_APPROVED`;
- H-0076 handoff pós-P01: `H1_HANDOFF_APPROVED`;
- H-0076 implementação pós-P02: `I1_IMPLEMENTATION_APPROVED`;
- H-0077 handoff pós-P02: `H1_HANDOFF_APPROVED`;
- H-0077 implementação pós-P02: `I1_IMPLEMENTATION_APPROVED`;
- validação manual R02: `APROVADA`.

## Evidência técnica

```yaml
testes:
  H0076:
    resultado: 91_passed

  H0077_suite_focal:
    resultado: 635_passed_1_failed
    falha_independente:
      - QA-IMPL-H0077-03

  P16:
    resultado: 3_passed

validacao_manual:
  R02: APROVADA
```

A R02 aprovou o popup longo justificado: nenhuma palavra quebrada;
recomposição correta no resize; nenhuma perda ou duplicação observada. O
corpo externo não justificado é comportamento correto, porque o consumidor
não solicita justificação. O defeito da R01 não voltou a ocorrer.
`docs/relatorios/RELATORIO_VALIDACAO_MANUAL_ITEM-0027_R01.md` permanece
inalterado como evidência histórica da reprovação que originou a reabertura.

## Resíduo não pertencente ao fechamento

`QA-IMPL-H0077-03` permanece fora do ITEM-0027. A falha conhecida

```text
tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados
```

é resíduo independente de H-0070, sem nexo causal com D-0027-10, e não
bloqueia este fechamento. Não foi corrigida nem marcada como resolvida. O
registro já existente nos relatórios e no handoff H-0077 é preservado.

## Resultado

O ITEM-0027 está documentalmente encerrado. ADR-0049 está `aceita e
aplicada`. H-0076 e H-0077 estão `CONCLUIDO`. Não há bloqueio conhecido do
ITEM-0027 para commit.
