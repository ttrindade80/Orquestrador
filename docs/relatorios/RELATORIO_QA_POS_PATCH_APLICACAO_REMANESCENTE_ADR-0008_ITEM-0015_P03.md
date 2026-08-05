# Relatório QA pós-patch — ADR-0008 / ITEM-0015 / P03

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P03.md

achados_retestados:
  - H49-QA-01
  - H49-QA-09
```

## H49-QA-01 — resolvido

O contrato define `descricao.max_caracteres` como inteiro entre `1` e `200`,
com limites inclusivos, sem default. Também determina rejeição explícita de
zero, valores negativos, valores superiores a `200` e valores não inteiros.
A nomenclatura registra o domínio `1..200` e remete o comportamento normativo
ao contrato. Não permanece a formulação que permitia qualquer inteiro
positivo sem limite superior.

## H49-QA-09 — bloqueado, não resolvido

O patch fechou a ordem de processamento da descrição — corte por
`max_caracteres`, capitalização, alinhamento e recuo, e limitação geométrica já
contratada — e documentou o algoritmo de `inicio_de_frase`, incluindo
preservação literal, transformação exclusiva do primeiro caractere alfabético,
não transformação de frases posteriores, retorno inalterado sem caractere
alfabético e string vazia. Os seis exemplos normativos exigidos estão
presentes e são compatíveis.

Contudo, nenhuma autoridade define o significado operacional de “caractere
alfabético”. Não foi determinada a política entre ASCII, Unicode, locale ou
lista manual de caracteres. Assim, ainda existe uma escolha material para o
implementador; a suficiência operacional de `inicio_de_frase` permanece
indeterminada. O P03 declara `algoritmo fechado` e `bloqueios: []`, mas essa
conclusão não corresponde ao texto normativo efetivamente auditado.

## Verificações e escopo

Foram executadas as leituras integrais autorizadas, as duas buscas focais do
handoff, o `git diff` obrigatório dos três caminhos do patch, as duas buscas
normativas autorizadas e `git diff --check`. O diff dos documentos versionados
do escopo corresponde às alterações declaradas pelo P03; o relatório P03 foi
conferido diretamente como arquivo criado.

Novo bloqueio: QPP03-04 — determinação insuficiente de “caractere alfabético”.
Não foram alterados documentos, handoff, código, testes, JSONs, backlog ou
stage durante este QA.

```yaml
status: BLOCKED_DOCUMENTATION
patch_h0049_liberado: false
proxima_acao: ESPECIFICACAO
```
