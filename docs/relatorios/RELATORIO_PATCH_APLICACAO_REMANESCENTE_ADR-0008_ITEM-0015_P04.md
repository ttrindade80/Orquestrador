# Relatório de patch — ADR-0008 / ITEM-0015 / P04

```yaml
rastreabilidade:
  etapa: PATCH_APLICACAO_ADR
  objeto: ITEM-0015 / ADR-0008 / P04
  cadeia_raiz: docs/relatorios/RELATORIO_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P03.md
  bloqueio_tratado:
    - QPP03-04

execucao:
  status: PATCH_APLICACAO_ADR_COMPLETED
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P04.md
  arquivos_alterados:
    - docs/contratos/contrato_cabecalho.md
    - docs/nomenclatura/30_CABECALHO.md

resultado:
  delta_material:
    - adoção de str.isalpha() (semântica Python) como única fonte de verdade sobre o que conta como "caractere alfabético" em inicio_de_frase, eliminando a indeterminação apontada em QPP03-04;
    - substituição do primeiro caractere alfabético localizado pelo resultado exato de str.upper() (semântica Python), aplicado somente a esse único caractere;
    - declaração explícita de independência de locale — nenhuma configuração de idioma ou região altera o resultado de isalpha()/upper();
    - declaração explícita de ausência de normalização Unicode (NFC/NFKC) antes da busca do caractere;
    - tratamento normativo da expansão de upper() em mais de um caractere Unicode, com incorporação integral do resultado sem truncamento;
    - preservação literal do prefixo (caracteres anteriores) e do sufixo (caracteres posteriores) mantida e reafirmada dentro do algoritmo renumerado;
    - ampliação da tabela de exemplos normativos com área útil, çalışma e Δ resultado (casos Unicode/locale) e com o novo caso ßeta → SSeta, que demonstra expansão real da conversão.
  verificacoes_executadas:
    - execução direta em Python 3.14 do laço de busca por isalpha()/upper() sobre as amostras ßeta, ﬃ teste, área e Δ resultado, confirmando ßeta -> SSeta como expansão real e não presumida;
    - rg de isalpha, upper, Unicode, locale, normaliza e caractere alfabético nos dois documentos do escopo;
    - rg de ASCII, A-Z, a-z, lista manual e "dependente de locale" nos dois documentos do escopo — todas as ocorrências são negações que vedam essas interpretações, nenhuma as adota;
    - git diff --check nos três caminhos do patch — sem problemas de espaço em branco;
    - git diff dos dois arquivos alterados, conferindo que o novo texto substitui integralmente a semântica antes indeterminada.
  bloqueios: []
```

## Contexto do bloqueio tratado

O QA do P03 (`RELATORIO_QA_POS_PATCH_APLICACAO_REMANESCENTE_ADR-0008_ITEM-0015_P03.md`,
achado H49-QA-09) confirmou que o algoritmo de `inicio_de_frase` estava
estruturalmente fechado — ordem de transformação, preservação literal,
não propagação a frases posteriores, casos de string vazia e de ausência de
caractere alfabético — mas apontou que nenhuma autoridade definia o
significado operacional de "caractere alfabético" entre ASCII, Unicode,
locale ou lista manual. Esse é o bloqueio QPP03-04, registrado como
`BLOCKED_DOCUMENTATION`.

## Decisão aplicada

Este patch fecha a lacuna adotando `str.isalpha()` e `str.upper()` da
linguagem Python como única semântica normativa, sem locale, sem
normalização Unicode prévia e sem biblioteca externa. O contrato
(`docs/contratos/contrato_cabecalho.md`, seção 5) foi reescrito com um
algoritmo renumerado de 11 passos que incorpora essa decisão, acrescenta a
observação de que a conversão pode expandir um caractere em mais de um, e
amplia a tabela de exemplos normativos com os casos Unicode/locale
(`área útil`, `çalışma`, `Δ resultado`) e com o caso de expansão real
(`ßeta` → `SSeta`), obtido por execução direta no ambiente.

A nomenclatura (`docs/nomenclatura/30_CABECALHO.md`, seção 4.4) recebeu
apenas o resumo dessa decisão — critério `isalpha()`, independência de
locale, ausência de normalização, uso de `upper()` no primeiro caractere —
sem duplicar o algoritmo, a ordem das etapas ou os exemplos, que permanecem
de autoridade exclusiva do contrato.

## Verificação da expansão

A execução do laço de busca em Python 3.14 sobre as amostras `ßeta`,
`ﬃ teste`, `área` e `Δ resultado` confirmou que `"ß".upper()` produz `"SS"`,
gerando `ßeta -> SSeta`. Esse resultado, obtido por execução e não
presumido, foi incorporado ao contrato como evidência da regra geral do
passo 6 (incorporar por inteiro o resultado de `upper()`), sem transformá-lo
em regra específica do caractere `ß`.

## Escopo respeitado

Foram alterados somente os dois arquivos autorizados
(`contrato_cabecalho.md` e `30_CABECALHO.md`) e criado somente este
relatório. Os relatórios P03 e QA-P03 não foram tocados. O handoff
`H-0049` não foi alterado. Nenhum código, teste, JSON ou item de backlog foi
tocado neste patch.

```yaml
status: PATCH_APLICACAO_ADR_COMPLETED
patch_h0049_liberado: false
proxima_acao: QA_POS_PATCH
```
