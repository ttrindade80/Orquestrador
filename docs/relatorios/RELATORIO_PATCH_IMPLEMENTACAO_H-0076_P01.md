# Relatório de patch de implementação H-0076 P01

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0076.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0076.md
achados_tratados:
  - QA-IMPL-H0076-01
```

## Causa

`_faixas_de_quebra` classificava runs por `isspace()` e fazia essa escolha
determinar as fronteiras da composição. Os testes do núcleo e do popup ainda
exigiam concatenação literal, preservação de múltiplos espaços, espaços
isolados e extremidades. Isso materializava no mecanismo comum uma política
global que não havia sido especificada.

## Arquivos alterados

- `tela/renderizacao/composicao_textual.py`
- `tela/teste_composicao_textual.py`
- `tela/teste_popup.py`
- `demo/teste_demo_popup.py`
- este relatório

`tela/renderizacao/popup.py` não precisou de alteração funcional: já consome o
núcleo canônico. Os consumidores reservados ao H-0077 permaneceram intactos.

## Correção

`_faixas_de_quebra` passou a calcular faixas exclusivamente por unidades
visuais e largura disponível. A composição continua limitada pela largura,
reparte segmentos longos e mantém as primitivas ANSI, CSI indivisível e
isolamento/restabelecimento de SGR. A justificação continua explícita e os
testes verificam largura e conteúdo não-whitespace, sem fixar distribuição.

## Remoção da política global

Foram removidas a classificação de separadores no núcleo, as asserções de
`"".join(linhas) == texto` e os contratos de forma literal para múltiplos
espaços, espaços isolados, extremidades e distribuição dos vãos. Nenhuma
normalização, condensação, trimming, remoção ou inserção sistemática foi
introduzida como substituta.

Não foi necessária compatibilidade local adicional no popup. Ele continua
usando o núcleo para composição e conserva apenas suas responsabilidades
estruturais, de geometria, ANSI e estado.

## Testes

Executado:

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_composicao_textual.py tela/teste_popup.py demo/teste_demo_popup.py
87 passed
git diff --check
```

## Busca focal

A busca solicitada não encontrou materialização de política global de
whitespace/separadores no núcleo ou em seus testes. As ocorrências restantes
de “preserva” referem-se somente a ANSI/SGR, ordem, estado ou overlay.

## Bloqueios

Nenhum.
